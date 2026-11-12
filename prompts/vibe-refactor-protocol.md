# Vibe-Refactor Protocol — direct invocation

Paste this into an AI coding agent with the repository open, or install the `vibe-refactor-protocol` skill.

> Inspect this codebase for implicit state machines: boolean clusters, nested conditional rendering, scattered status strings, nullable state combinations, refs used as flags, timers, retries, and asynchronous flows with possible races.
>
> Diagnose the highest-impact lifecycle first. Identify the states, events, transitions, guards, effects, invalid combinations, and concrete failure paths. Then choose the smallest safe representation—such as a discriminated union, enum, reducer, or transition function—and refactor one lifecycle at a time.
>
> Improve all three: user experience (UX), developer experience (DX), and agent experience (AX). Preserve existing public APIs, props, function signatures, data contracts, routes, event names, persistence formats, and visual output. Characterize current behavior before changing it, keep compatibility adapters while old callers remain, and handle stale async results, duplicate work, cancellation, and cleanup deliberately. Do not add dependencies without a demonstrated need. Do not promise zero regressions.
>
> Output: (1) The Diagnosis, (2) The Refactored Code or focused patch, (3) the UX/DX/AX breakdown, and (4) exact verification results, unrun checks, assumptions, and residual risks. If behavior is ambiguous or a change crosses an unapproved contract boundary, stop before editing and explain what needs validation.
