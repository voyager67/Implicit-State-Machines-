# Detection signals

Use these to hunt for implicit state machines. Every hit is a *candidate*, not a verdict. Confirm by checking whether code behavior differs depending on which phase something is in.

## Boolean clusters

Two or more booleans in the same component, store, or class may describe one lifecycle.

```bash
rg -n "useState\\((false|true)\\)" --glob "*.{tsx,jsx,ts,js}"
rg -n "\\b(is|has|should|did|was)(Loading|Fetching|Submitting|Saving|Error|Success|Done|Ready|Open|Visible|Retrying|Dirty)\\b"
```

Strong signal: several flags are read or written together in the same handlers, or the code can represent combinations such as `isLoading && isError && data`.

## Status, step, and mode strings

```bash
rg -n "(status|state|phase|step|mode|stage)\\s*(===|!==|==|!=)\\s*['\"]"
rg -n "case ['\"](idle|loading|pending|success|error|done|failed)['\"]"
rg -n "currentStep|activeStep|wizardStep"
```

Strong signal: the same literals are compared in multiple files without one authoritative type or allowed-value definition.

## Nullable combinations

```bash
rg -n "(data|user|result|session) && !(error|loading)"
rg -n "!(data|user|result) && !(error|loading)"
```

Strong signal: rendering logic infers phase from which values happen to be null.

## Refs and variables as flags

```bash
rg -n "useRef\\((false|true|null)\\)"
rg -n "\\.current\\s*=\\s*(true|false)"
rg -n "isMounted|didInit|hasRun|alreadySubmitted|initialized"
```

Strong signal: a ref guards a side effect from running twice. That is hidden lifecycle state.

## Timers, retries, and debounces

```bash
rg -n "setTimeout|setInterval|clearTimeout|clearInterval|debounce|throttle"
rg -n "retry|retries|attempt|backoff|maxAttempts"
```

Strong signal: a counter or timer changes what event is allowed next.

## Multi-step flows

Look at checkout, onboarding, auth/token refresh, file upload, payment, reconnect flows, permission prompts, form wizards, and optimistic updates with rollback.

```bash
rg -n "refreshing|reconnect|connecting|disconnected|authenticated|unauthenticated"
rg -n "optimistic|rollback|revert"
```

## Backend lifecycles

```bash
rg -n "status\\s*(=|==|===|!=|!==)"
rg -n "(processed|completed|failed|cancelled|started)_at"
rg -n "retry_count|attempts|locked_by|claimed"
```

Strong signal: status changes in multiple handlers, jobs, or scripts with no single transition policy. Check for database constraints.

## Mobile and native

- Swift: clusters of `@Published var` booleans in one view model.
- Kotlin: several `MutableStateFlow<Boolean>` values describing one lifecycle.
- Flutter: multiple `bool is...` fields in one `State` class.

## Agent and tool loops

Look for phases such as planning, awaiting approval, executing, retrying, recovering, and stopping. Check whether phase state is explicit in run records and tool contracts.

## Impossible-state check

For a cluster of N related booleans, list the (2^N) combinations and mark which are valid. A reachable but meaningless combination is evidence for further investigation, not automatic proof of a bug.

## False positives — usually leave alone

- A single independent toggle (dropdown open, tooltip visible, checkbox checked).
- Flags in unrelated scopes that happen to share a name.
- Pure derived values already computed from one source of truth.
- Third-party library internals.
