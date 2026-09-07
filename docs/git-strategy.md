# Git Strategy

## Long-lived branches
- `main`: stable/releasable
- `develop`: integration branch during the learning project

## Working branches
- `feature/CF-<id>-short-name`
- `test/CF-<id>-short-name`
- `fix/CF-<id>-short-name`
- `docs/CF-<id>-short-name`

## Commit convention
```text
CF-12 feat: add case creation endpoint
CF-12 test: add case creation API coverage
CF-21 test: automate assignment workflow
CF-27 fix: reject invalid state transition
CF-30 docs: update traceability matrix
```

## Pull requests
Every meaningful change should explain the Jira ticket, what changed, how it was tested, evidence and risks.
