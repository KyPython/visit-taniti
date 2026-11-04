# Requirements: Static-site quality gate

Spec ID: VTS · Issue: #9 · Status: proposed; Ky approves by merging this spec-only PR

## Introduction

The prototype verifies offline without deploying: page/link checks with
fault fixtures run under `pnpm test`, `pnpm build` verifies the static
output plus shared JavaScript syntax, and a pinned CI workflow runs both
on PR and push.

## Requirements

### Requirement 1: Offline verification (VTS-1)

**User Story:** As Ky, I want the static site proven link-clean offline,
so that a broken page never needs a deploy to discover.

#### Acceptance Criteria

1. VTS-1.1 WHEN `pnpm test` runs THEN page/link checks plus fault
   fixtures SHALL execute with 0 failures.
2. VTS-1.2 WHEN `pnpm build` runs THEN it SHALL run the test suite and
   verify shared JavaScript syntax, and SHALL NOT deploy.
3. VTS-1.3 WHEN a PR or push touches the site THEN the static-site
   workflow SHALL run the same verification with pinned actions.
