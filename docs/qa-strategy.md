# QA Strategy

## Objectives
- Validate business-critical workflows.
- Detect functional, integration and authorization defects early.
- Maintain traceability between requirements, manual scenarios and automation.
- Automate stable, high-value regression scenarios.
- Run automated checks continuously in CI.

## Test levels
### Requirement testing
Review acceptance criteria, ambiguities, edge cases and testability before development.

### Manual functional testing
Validate new features, exploratory scenarios and UX behavior.

### API testing
Validate status codes, payloads, validation, authorization and business rules.

### E2E testing
Automate critical user journeys with Playwright.

### Performance testing
Add targeted workload tests after core flows stabilize.

## Priority model
- P0: Authentication, authorization, data integrity.
- P1: Case creation, assignment, status transitions.
- P2: Search, filtering, audit trail.
- P3: Secondary UX and non-critical presentation behavior.

## Automation rule
Automate scenarios that are stable, repetitive, business-critical, valuable for regression and deterministic enough for CI.

## Evidence
Failures should preserve test reports, screenshots, traces and relevant logs.

## MCP policy
MCP and AI may assist with requirement review, scenario ideation, exploratory navigation, defect reproduction and draft documentation. All final QA decisions are human-reviewed.
