# Sample audit (fictional example)

> This is illustrative data for learning the report format. It is not evidence about any real repository.

## Executive readout

The fictional account settings page has one high-priority implicit lifecycle: profile saving. Three related booleans and a nullable error value can represent contradictory UI states. The smallest proposed change is a typed save status with request identity, while keeping the existing `onSave` prop unchanged.

## Inventory

| Workflow | Owner | Candidate states | Confidence |
|---|---|---|---|
| Profile save | `ProfileEditor` | idle, saving, saved, error | High |
| Avatar preview | `AvatarPicker` | closed/open | High; independent toggle, leave as-is |

## Transition model

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> Saving: submit
    Saving --> Saved: current request succeeds
    Saving --> Error: current request fails
    Error --> Saving: retry
    Saved --> Saving: edit and submit
```

## Finding F-01

- **Severity:** High
- **Confidence:** High
- **Evidence:** `ProfileEditor.tsx` writes `isSaving`, `hasSaved`, and `saveError` in the same submit handler.
- **Failure mode:** a previous error can remain visible after a successful retry.
- **UX:** conflicting save feedback.
- **DX:** lifecycle behavior is spread across three setters.
- **AX:** an agent must infer allowed combinations from multiple branches.
- **Change risk:** Medium; save behavior is user-visible and should be characterized first.

## Decision

Add tests for initial save, success, failure, retry, and stale responses. If they confirm the inferred contract, replace the related flags with a discriminated union, keep the public `onSave` contract unchanged, and derive any legacy read-only flags during migration.

## Verification

No commands were run. This sample intentionally makes no claim that code or tests pass.
