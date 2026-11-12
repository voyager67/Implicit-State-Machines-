# Detection signals

Use these to hunt for implicit state machines. Every hit is a *candidate*, not a verdict. Confirm by checking whether the code behaves differently depending on which phase something is in.

## Contents
- Boolean clusters
- Status, step and mode strings
- Nullable combinations
- Refs and variables as flags
- Timers, retries, debounces
- Multi-step flows
- Backend lifecycles
- Mobile and native
- Agent and tool loops
- Impossible-state check
- False positives

## Boolean clusters

Two or more booleans in the same component, store or class that describe a lifecycle.

```
rg -n "useState\((false|true)\)" --glob "*.{tsx,jsx,ts,js}"
rg -n "\b(is|has|should|did|was)(Loading|Fetching|Submitting|Saving|Error|Success|Done|Ready|Open|Visible|Retrying|Dirty)\b"
rg -n "\b(loading|error|success|done|ready|submitted|pending)\s*[:=]\s*(false|true)"
```

Strong signal: three or more of these in one scope, or flags that are set together in handlers (`setLoading(true); setError(false);`).

## Status, step and mode strings

```
rg -n "(status|state|phase|step|mode|stage)\s*(===|!==|==|!=)\s*['\"]"
rg -n "case ['\"](idle|loading|pending|success|error|done|failed)['\"]"
rg -n "currentStep|activeStep|wizardStep"
```

Strong signal: the same string literals compared in more than one file, or no single type or enum listing the allowed values.

## Nullable combinations

```
rg -n "(data|user|result|session) && !(error|loading)"
rg -n "!(data|user|result) && !(error|loading)"
rg -n "\? .* : .* \? .* :"   # nested ternaries rendering by phase
```

Strong signal: rendering logic that infers the phase from which values are null.

## Refs and variables as flags

```
rg -n "useRef\((false|true|null)\)"
rg -n "\.current\s*=\s*(true|false)"
rg -n "isMounted|didInit|hasRun|alreadySubmitted|initialized"
```

Strong signal: a ref that guards a side effect from running twice. That is a hidden state.

## Timers, retries, debounces

```
rg -n "setTimeout|setInterval|clearTimeout|debounce|throttle"
rg -n "retry|retries|attempt|backoff|maxAttempts"
```

Strong signal: a counter or timer whose value changes what the next event does.

## Multi-step flows

Checkout, onboarding, auth and token refresh, file upload, payment, connection or reconnection (websocket, SSE, BLE), permission prompts, form wizards, optimistic updates with rollback.

```
rg -n "refreshing|reconnect|connecting|disconnected|authenticated|unauthenticated"
rg -n "optimistic|rollback|revert"
```

## Backend lifecycles

```
rg -n "status\s*(=|==|!=)\s*['\"]"                    # Python, Ruby, JS
rg -n "\.status\s*(=|==|!=)"
rg -n "(processed|completed|failed|cancelled|started)_at"
rg -n "WHERE .*_at IS (NOT )?NULL"
rg -n "retry_count|attempts|locked_by|claimed"
```

Strong signal: status changed by many handlers, jobs or scripts, with no single function that owns legal transitions. Check the database for a status column with no CHECK constraint.

## Mobile and native

- Swift: `var is[A-Z]\w* = false` clusters in view models, `@Published var` booleans that imply a phase.
- Kotlin: several `MutableStateFlow<Boolean>` in one ViewModel; UI state spread across flows.
- Flutter: multiple `bool _is...` fields in one `State` class.

## Agent and tool loops

Loops that call a model, run tools, wait for approval, recover from errors or stop on budget. Look for phases encoded as flags (`awaitingApproval`, `isRecovering`, `done`) or as string statuses on a run record.

## Impossible-state check

For a cluster of N booleans, list the 2^N combinations. Mark which are valid. Any combination that is reachable in code but meaningless (for example `isLoading && isError && data`) is evidence of a bug waiting to happen, and a strong case for refactoring.

## False positives (usually leave alone)

- A single independent toggle (dropdown open, tooltip visible, checkbox checked).
- Flags in unrelated scopes that happen to share a name.
- Pure derived values that are already computed from one source of truth.
- Third-party library internals.
