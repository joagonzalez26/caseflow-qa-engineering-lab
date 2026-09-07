# CaseFlow QA Engineering Lab

> End-to-end QA Engineering portfolio project integrating product requirements, Jira/MCP workflows, manual testing, API testing, Playwright E2E automation, Docker, GitHub Actions and AWS.

## Project goal

CaseFlow is a fictitious case and document management platform designed to simulate a real software delivery environment. The objective is not only to build a working application, but to demonstrate a complete Quality Engineering workflow from requirement analysis to automated quality gates and cloud deployment.

## What this project demonstrates

- Requirements analysis and user-story refinement
- Jira-based backlog and defect management
- Manual QA strategy and test design
- API testing
- End-to-end automation with Playwright
- AI-assisted workflows using MCP
- Traceability from requirement to automated test
- Git/GitHub collaboration workflow
- CI/CD quality gates with GitHub Actions
- Dockerized development/test environment
- AWS deployment and observability
- QA reporting and metrics

## Planned architecture

```text
Jira / User Stories
        |
   Atlassian MCP
        |
        v
Requirement Analysis
        |
        v
React Frontend <----> FastAPI Backend <----> PostgreSQL
        |                    |
        +------ API Tests ---+
        |
        +------ Playwright E2E
                      |
                      v
                GitHub Actions
                      |
                 Quality Gate
                      |
                    Docker
                      |
                     AWS
```

## Repository structure

```text
.
├── backend/
├── frontend/
├── tests/
│   ├── api/
│   ├── e2e/
│   └── fixtures/
├── docs/
│   ├── product-brief.md
│   ├── qa-strategy.md
│   ├── risk-analysis.md
│   ├── traceability-matrix.md
│   ├── definition-of-ready.md
│   ├── definition-of-done.md
│   ├── git-strategy.md
│   └── bugs/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── workflows/
│   └── pull_request_template.md
├── docker-compose.yml
└── README.md
```

## Delivery roadmap

### Sprint 0 — Foundation
- Product scope
- Architecture
- Jira project
- Initial backlog
- Definition of Ready
- Definition of Done
- QA strategy
- Git strategy
- Repository structure

### Sprint 1 — Authentication
- Login flow
- Roles and permissions
- API coverage
- E2E coverage
- First defects and traceability

### Sprint 2 — Case management
- Create and edit cases
- Assign responsible users
- State transitions
- Search and filters
- Audit trail

### Sprint 3 — MCP workflow
- Jira / Atlassian MCP
- Playwright MCP exploration
- AI-assisted requirement and test analysis
- Human QA review and validation

### Sprint 4 — DevOps
- Docker
- GitHub Actions
- Automated quality gates
- Test reports and artifacts

### Sprint 5 — Cloud
- AWS deployment
- Logging / monitoring
- Final portfolio demo
- LinkedIn case study

## Quality principle

AI can assist with exploration, requirements analysis and first-pass test design, but final test strategy, prioritization, validation and release decisions remain human-reviewed.

## Status

**Sprint 0 — In progress**
