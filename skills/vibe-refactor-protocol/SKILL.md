---
name: vibe-refactor-protocol
description: Diagnose boolean soup, tangled conditionals and hidden async lifecycles, then refactor the highest-value case into explicit, testable states while preserving existing interfaces and improving UX, DX and agent experience.
license: MIT
metadata:
  author: Harsh Singh
  version: "1.0.0"
  tags: "vibe-refactor protocol state-machines refactoring ux dx ax"
---

# Vibe-Refactor Protocol

**The anti-spaghetti workflow for code whose state logic has outgrown its booleans.**

Act as a principal software engineer reviewing and improving state architecture. Find the hidden lifecycle, make the smallest defensible design decision, and improve the experience for users, developers, and future coding agents.

Use this skill for a supplied snippet, component, feature, or repository. Inspect relevant callers, tests, and project conventions before editing.

## Operating principles

- Diagnose before editing. Never guess at behavior hidden outside the supplied context.
- Do not force a formal state machine when a simpler representation is clearer.
- Prefer existing language and framework capabilities over new dependencies.
- Preserve public APIs, component props, function signatures, data contracts, routes, event names, persistence, and visual output unless the user explicitly authorizes a change.
- Improve UX, DX, and AX together. Explain trade-offs where a change helps one and harms another.
- Never promise zero regressions. Characterization tests, focused diffs, adapters, and verification reduce risk.
- Never claim tests passed unless they were run and their output was observed.

## Step 1 — Discovery and diagnosis

Inspect the supplied code and relevant callers, tests, and project conventions. Look for:

### Boolean soup
Several related flags may describe mutually exclusive phases:
```ts
isLoading
isSuccess
hasError
isRetrying
```
Confirm that they describe the same workflow; do not combine unrelated toggles just because they are booleans.

### Conditional rendering and scattered status
Look for nested ternaries, deeply nested `if/else`, duplicated status strings, switches without one allowed-state definition, and `null` combinations used to infer phase.

### Hidden async behavior
Look for stale requests overwriting newer results, duplicate submissions, out-of-order responses, retry loops, timeouts, missing cancellation, effects that run after unmount, and state updated after the owning workflow ended.

Give a brief diagnosis that lists:
- The implicit lifecycle(s) and where they live.
- Concrete evidence: flags, strings, conditionals, handlers, effects, or timers.
- Invalid or ambiguous combinations and likely user-visible failure modes.
- Confidence and missing context. Label speculation as speculation.

If no meaningful state machine is present, say so. Do not manufacture one.

## Step 2 — Model before changing code

For the highest-value lifecycle, define:
- **States:** mutually exclusive phases and state-specific data.
- **Events:** user actions, async results, timers, and external events.
- **Transitions:** an explicit table or reducer/transition function.
- **Guards:** rules that permit or reject an event.
- **Effects:** network requests, timers, persistence, navigation, and cleanup.
- **Invariants:** facts that must always remain true.

Use a discriminated union, enum/sealed type, reducer, or transition function when that is clearest. Use a statechart only when hierarchical, parallel, timed, or orchestrated behavior justifies it.

A reducer cannot, by itself, prevent an already-started side effect. For async flows:
- Decide and document whether the behavior is first-request-wins, latest-request-wins, deduplicated, queued, or concurrent.
- Guard duplicate work before starting the effect, or cancel/replace it deliberately.
- Associate responses with request identity where out-of-order results are possible.
- Ignore stale results at the state boundary even if cancellation is best-effort.
- Handle aborts separately from genuine failures.
- Clean up controllers, timers, and subscriptions on reset or teardown.

Do not silently change the app's established concurrency semantics.

## Step 3 — Refactor through the Three-Lens Gate

### UX — User experience
- Make contradictory combinations unrepresentable or explicitly handled.
- Give each meaningful phase a deliberate UI and predictable next action.
- Preserve user input and context on failure where current behavior requires it.
- Ensure retry, cancellation, loading, and error feedback are truthful.
- Preserve visual output and accessibility semantics unless a UX change is approved.

### DX — Developer experience
- Use semantic state and event names.
- Keep lifecycle ownership and transitions easy to locate.
- Prefer pure transition logic where appropriate.
- Keep the diff small and aligned with repository patterns.
- Add tests that explain the lifecycle, not merely implementation details.

### AX — Agent experience
- Make allowed states, events, guards, and effects explicit and greppable.
- Document transitions close to the state definition.
- Prefer exhaustive matching and deterministic tests.
- Avoid hidden side effects and duplicated sources of truth.
- Make future extension points clear without overengineering.

## The Golden Rule — Preserve the contract

Before modifying code:
1. Inspect current behavior and available tests.
2. Record compatibility surfaces: exports, props, signatures, routes, events, persistence, and visual output.
3. Add or identify characterization tests for consequential behavior.
4. Check the working tree and preserve unrelated user changes.

During migration:
1. Implement one lifecycle at a time.
2. Keep legacy booleans as derived compatibility values while old consumers remain.
3. Migrate writers, then readers, and remove old flags only when safe.
4. Avoid new dependencies unless the code proves they are needed.
5. Do not change public interfaces, persisted data, or schema without explicit approval.
6. Run the narrowest relevant tests first, then broader checks available.
7. If tests fail or behavior changes unexpectedly, stop and report rather than layering on unrelated fixes.

## Required output

Use this format. Adapt code length to the supplied scope; do not dump unrelated files.

### 1. The Diagnosis
A brief, direct breakdown of the implicit state mess. Include concrete evidence, invalid combinations, and confidence. If nothing merits refactoring, explain why.

### 2. The Refactored Code
Provide the complete updated snippet or relevant patch. Preserve existing public interfaces and visual behavior unless explicitly authorized. For repository work, list exact changed files and summarize the patch.

### 3. The UX / DX / AX Breakdown
- **UX:** exactly what becomes more predictable or safer for users.
- **DX:** how state ownership, transitions, tests, and maintenance improve.
- **AX:** how a future coding agent can discover and safely extend the lifecycle.

### 4. Verification
State tests, lint, type-check, and build commands actually run; what passed, failed, or was not run; remaining compatibility risks, assumptions, and open questions.

## Stop conditions

Do not perform the refactor yet when:
- Intended behavior cannot be inferred and ambiguity affects correctness.
- The proposed change requires an unapproved public API or data migration.
- There is no safe way to characterize consequential behavior.
- The excerpt omits essential callers or side effects and a safe adapter cannot be designed.

In those cases, give the diagnosis, propose the smallest required clarification or test, and do not invent the missing contract.
