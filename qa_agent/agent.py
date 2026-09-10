from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

from playwright.sync_api import Page, sync_playwright


@dataclass
class ElementInfo:
    kind: str
    text: str
    selector: str
    attributes: dict[str, str]


@dataclass
class TestCase:
    title: str
    category: str
    steps: list[str]
    expected: str


@dataclass
class Finding:
    severity: str
    title: str
    url: str
    evidence: str


class QAAgent:
    """Small autonomous web QA agent POC.

    It explores a same-origin web app, inventories interactive elements,
    generates first-pass functional test ideas, runs a conservative reflected
    XSS probe against visible text inputs, and writes a JSON report.
    """

    def __init__(self, start_url: str, max_pages: int = 8, headless: bool = True):
        self.start_url = start_url.rstrip("/")
        self.origin = self._origin(self.start_url)
        self.max_pages = max_pages
        self.headless = headless
        self.visited: set[str] = set()
        self.pages: list[dict[str, Any]] = []
        self.test_cases: list[TestCase] = []
        self.findings: list[Finding] = []

    @staticmethod
    def _origin(url: str) -> str:
        p = urlparse(url)
        return f"{p.scheme}://{p.netloc}"

    @staticmethod
    def _normalize(url: str) -> str:
        p = urlparse(url)
        clean = p._replace(fragment="")
        return clean.geturl().rstrip("/") or clean.geturl()

    def _same_origin(self, url: str) -> bool:
        try:
            return self._origin(url) == self.origin
        except Exception:
            return False

    @staticmethod
    def _selector_for(page: Page, handle) -> str:
        try:
            testid = handle.get_attribute("data-testid")
            if testid:
                return f'[data-testid="{testid}"]'
            element_id = handle.get_attribute("id")
            if element_id:
                return f"#{element_id}"
            name = handle.get_attribute("name")
            tag = handle.evaluate("el => el.tagName.toLowerCase()")
            if name:
                return f'{tag}[name="{name}"]'
            aria = handle.get_attribute("aria-label")
            if aria:
                return f'{tag}[aria-label="{aria}"]'
            return tag
        except Exception:
            return "unknown"

    def _extract_elements(self, page: Page) -> list[ElementInfo]:
        results: list[ElementInfo] = []
        handles = page.query_selector_all(
            "input:visible, textarea:visible, select:visible, button:visible, a:visible, img:visible"
        )
        for h in handles:
            try:
                tag = h.evaluate("el => el.tagName.toLowerCase()")
                text = (h.inner_text() or h.get_attribute("alt") or "").strip()[:180]
                attrs = {}
                for key in ("type", "name", "placeholder", "href", "role", "aria-label"):
                    value = h.get_attribute(key)
                    if value:
                        attrs[key] = value
                results.append(
                    ElementInfo(
                        kind=tag,
                        text=text,
                        selector=self._selector_for(page, h),
                        attributes=attrs,
                    )
                )
            except Exception:
                continue
        return results

    def _discover_links(self, page: Page) -> list[str]:
        links: list[str] = []
        for h in page.query_selector_all("a[href]"):
            href = h.get_attribute("href")
            if not href or href.startswith(("mailto:", "tel:", "javascript:")):
                continue
            absolute = self._normalize(urljoin(page.url, href))
            if self._same_origin(absolute):
                links.append(absolute)
        return list(dict.fromkeys(links))

    def _generate_test_cases(self, url: str, elements: list[ElementInfo]) -> None:
        inputs = [e for e in elements if e.kind in {"input", "textarea", "select"}]
        buttons = [e for e in elements if e.kind == "button"]
        links = [e for e in elements if e.kind == "a"]

        if inputs:
            self.test_cases.append(
                TestCase(
                    title=f"Happy path form submission on {url}",
                    category="happy-path",
                    steps=[
                        "Open the page",
                        "Populate all visible required fields with valid data",
                        "Submit using the primary action",
                    ],
                    expected="The operation completes successfully and user feedback is clear.",
                )
            )
            self.test_cases.append(
                TestCase(
                    title=f"Required-field validation on {url}",
                    category="negative",
                    steps=["Open the page", "Leave required fields empty", "Attempt to submit"],
                    expected="Submission is blocked and field-level validation explains what is missing.",
                )
            )
            self.test_cases.append(
                TestCase(
                    title=f"Boundary input lengths on {url}",
                    category="boundary",
                    steps=[
                        "Identify text inputs",
                        "Try empty, 1-character, max-length and over-limit values",
                        "Submit each variation",
                    ],
                    expected="Documented limits are enforced without truncation surprises or server errors.",
                )
            )

        if buttons:
            self.test_cases.append(
                TestCase(
                    title=f"Interactive actions remain usable on {url}",
                    category="functional",
                    steps=["Open the page", "Exercise each visible button once", "Observe state changes"],
                    expected="Each action performs the intended transition once and provides visible feedback.",
                )
            )

        if links:
            self.test_cases.append(
                TestCase(
                    title=f"Navigation links are valid on {url}",
                    category="navigation",
                    steps=["Open the page", "Follow each internal link", "Check resulting page"],
                    expected="Links resolve successfully and stay within the expected application flow.",
                )
            )

    def _xss_probe(self, page: Page, url: str) -> None:
        marker = "qaagent_xss_probe_7f31"
        payload = f'<img src=x onerror="console.log(\'{marker}\')">'
        candidates = page.query_selector_all(
            'input:visible:not([type="password"]):not([type="file"]), textarea:visible'
        )
        if not candidates:
            return

        for h in candidates[:3]:
            try:
                h.fill(payload)
            except Exception:
                continue

        # Submit only if a visible form submit control exists; otherwise this is
        # a reflection-in-DOM check, not an exploit attempt.
        submit = page.query_selector('button[type="submit"]:visible, input[type="submit"]:visible')
        if submit:
            try:
                submit.click(timeout=1500)
                page.wait_for_timeout(500)
            except Exception:
                pass

        content = page.content()
        if marker in content and payload in content:
            self.findings.append(
                Finding(
                    severity="medium",
                    title="Potential reflected/unsanitized HTML input",
                    url=url,
                    evidence=f"Probe marker {marker} was reflected into page HTML. Manual verification required.",
                )
            )

    def run(self, output: Path) -> dict[str, Any]:
        queue = [self.start_url]

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            context = browser.new_context(ignore_https_errors=True)
            page = context.new_page()

            while queue and len(self.visited) < self.max_pages:
                url = self._normalize(queue.pop(0))
                if url in self.visited or not self._same_origin(url):
                    continue
                self.visited.add(url)

                try:
                    response = page.goto(url, wait_until="domcontentloaded", timeout=15000)
                    page.wait_for_timeout(250)
                    status = response.status if response else None
                    title = page.title()
                    elements = self._extract_elements(page)
                    self._generate_test_cases(url, elements)
                    self._xss_probe(page, url)
                    links = self._discover_links(page)
                    queue.extend([u for u in links if u not in self.visited])
                    self.pages.append(
                        {
                            "url": url,
                            "status": status,
                            "title": title,
                            "elements": [asdict(e) for e in elements],
                            "discovered_links": links,
                        }
                    )
                except Exception as exc:
                    self.findings.append(
                        Finding(
                            severity="high",
                            title="Page exploration failed",
                            url=url,
                            evidence=re.sub(r"\s+", " ", str(exc))[:500],
                        )
                    )

            browser.close()

        report = {
            "target": self.start_url,
            "pages_visited": len(self.pages),
            "pages": self.pages,
            "generated_test_cases": [asdict(t) for t in self.test_cases],
            "findings": [asdict(f) for f in self.findings],
        }
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        return report


def main() -> None:
    parser = argparse.ArgumentParser(description="CaseFlow autonomous QA agent POC")
    parser.add_argument("url", help="Application URL to explore")
    parser.add_argument("--max-pages", type=int, default=8)
    parser.add_argument("--headed", action="store_true")
    parser.add_argument("--output", default="artifacts/qa-agent-report.json")
    args = parser.parse_args()

    report = QAAgent(args.url, max_pages=args.max_pages, headless=not args.headed).run(Path(args.output))
    print(
        f"Visited {report['pages_visited']} page(s), generated "
        f"{len(report['generated_test_cases'])} test case(s), found {len(report['findings'])} finding(s)."
    )


if __name__ == "__main__":
    main()
