# AI QA Agent — Proof of Concept

This POC turns the CaseFlow lab from a scripted automation portfolio into a small autonomous QA exploration system.

## What it does

- Crawls pages within the same origin, up to a configurable page limit.
- Inventories visible inputs, textareas, selects, buttons, links and images.
- Prefers robust selectors such as `data-testid`, `id`, `name` and `aria-label` when available.
- Generates first-pass functional test ideas automatically:
  - happy path
  - negative validation
  - boundary testing
  - navigation
  - generic interaction coverage
- Runs a conservative reflected-input/XSS probe against visible text fields.
- Produces a machine-readable JSON report with explored pages, discovered elements, test ideas and findings.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r qa_agent/requirements.txt
playwright install chromium
python qa_agent/agent.py http://localhost:3000 --max-pages 8
```

To watch the browser:

```bash
python qa_agent/agent.py http://localhost:3000 --headed
```

Default report:

```text
artifacts/qa-agent-report.json
```

## Design principles

This agent is intentionally deterministic for the first iteration. It does not require an LLM key and therefore remains reproducible in local development and CI. A later layer can feed the structured page model and report into an LLM for natural-language querying, richer scenario generation and risk-based prioritization.

The security probe is only an initial signal. A reflected marker is reported as a potential issue and requires human verification; the agent does not claim exploitability.

## Roadmap

1. Add reusable Playwright Page Objects and executable generated specs.
2. Add login/session handling and interaction-sequence discovery.
3. Add API discovery/testing from OpenAPI.
4. Add accessibility checks.
5. Add k6 performance scenarios.
6. Add cross-browser execution.
7. Add GitHub Actions quality gates and report artifacts.
8. Add an optional LLM reasoning layer over the structured exploration data.
9. Add risk-based prioritization and Jira/MCP issue creation.

## Human review

The agent accelerates exploration and test design; release decisions, business-rule validation and final defect classification stay human-reviewed.
