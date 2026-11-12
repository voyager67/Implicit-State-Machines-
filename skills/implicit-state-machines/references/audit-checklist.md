# State-machine audit checklist

Use this as a review aid, not a mandate to formalize every variable.

## Discovery

- [ ] Identify the workflow boundary and source of truth.
- [ ] Find explicit machines, reducers, enums, and transition functions.
- [ ] Find implicit states encoded in booleans, nullable values, status strings, effects, refs, or timers.
- [ ] Trace state across components, hooks, stores, services, routes, jobs, and persistence.
- [ ] Identify events from users, network responses, timers, subscriptions, and external systems.
- [ ] Distinguish true lifecycles from independent toggles and unrelated flags.

## Correctness and lifecycle

- [ ] Are mutually exclusive states represented as mutually exclusive?
- [ ] Are impossible combinations prevented or detected?
- [ ] Are important transitions and rejected events handled?
- [ ] Can stale or out-of-order async work overwrite newer state?
- [ ] Are duplicate events and submissions safe?
- [ ] Are cancellation, cleanup, retries, timeouts, and idempotency defined?
- [ ] Is reset behavior consistent across retry, navigation, refresh, remount, and restoration?
- [ ] Is persisted state validated and versioned where appropriate?
- [ ] Are side effects separated from pure transition decisions where useful?

## UX

- [ ] Is progress visible and understandable?
- [ ] Are success and failure states truthful and timely?
- [ ] Can users recover without losing input or context?
- [ ] Are disabled, loading, retry, and cancel actions clear?
- [ ] Are focus, keyboard behavior, labels, and status announcements handled?
- [ ] Is the existing visual output preserved when the task is behavior-only refactoring?

## DX

- [ ] Is state ownership obvious?
- [ ] Are state names, events, and invariants explicit?
- [ ] Can transitions be tested without excessive setup?
- [ ] Are logs and errors useful?
- [ ] Does the proposed change fit existing conventions?

## AX — Agent experience

- [ ] Can a coding agent locate the transition owner?
- [ ] Are state, event, guard, and effect contracts explicit?
- [ ] Are types narrow enough to prevent invalid combinations?
- [ ] Are tests and fixtures deterministic?
- [ ] Can a localized change be made without guessing at hidden coupling?
- [ ] Are repository instructions discoverable and non-contradictory?

## Compatibility and verification

- [ ] Record pre-existing failures and working-tree changes.
- [ ] Add tests for important transitions and regressions.
- [ ] Test failure, retry, cancellation, reset, duplicate work, and stale results where relevant.
- [ ] Check compatibility of routes, APIs, events, props, persistence, and visual output.
- [ ] Run relevant tests, lint, type-check, and build.
- [ ] Record checks not run, assumptions, and residual risks.
