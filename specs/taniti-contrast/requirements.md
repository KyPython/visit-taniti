# Requirements: Taniti contrast gate

Spec ID: TAN · Issue: #6 · Status: proposed; Ky approves by merging this spec-only PR

## Introduction

The coral text and button palette must meet WCAG 2.2 AA against page
backgrounds, enforced by a contrast-ratio test that replaces the echo stub.

## Requirements

### Requirement 1: Coral contrast (TAN-1)

**User Story:** As Ky, I want coral pairs proven readable, so that the
prototype meets AA without eyeballing hex codes.

#### Acceptance Criteria

1. TAN-1.1 WHEN white text sits on coral or coral-hover, or coral text
   sits on sand or white, THEN the WCAG 2.2 contrast ratio SHALL be at
   least 4.5 to 1.
