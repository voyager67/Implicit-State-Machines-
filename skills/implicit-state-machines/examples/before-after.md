# Before / after: a fetch lifecycle

This example shows why boolean state is difficult to reason about—and why a reducer alone does not solve asynchronous races.

## Before: boolean soup

```tsx
function UserCard({ id }: { id: string }) {
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [user, setUser] = useState<User | null>(null);

  async function load() {
    setIsLoading(true);
    try {
      const res = await fetchUser(id);
      setUser(res);
    } catch {
      setIsError(true); // stale error can survive a retry
    } finally {
      setIsLoading(false);
    }
  }

  if (isLoading) return <Spinner />;
  if (isError) return <ErrorView onRetry={load} />;
  if (user) return <Card user={user} />;
  return null;
}
```

The flags and nullable data can disagree. Rapid requests can also resolve out of order, allowing an older response to overwrite newer data.

## Model

States: `idle`, `loading(requestId)`, `error(message)`, and `ready(user)`.

| Current state | Event | Next state |
|---|---|---|
| any | `RESET` | `idle` |
| any | `LOAD(requestId)` | `loading(requestId)` |
| matching `loading` | `RESOLVE(requestId, user)` | `ready(user)` |
| matching `loading` | `REJECT(requestId, message)` | `error(message)` |
| non-matching state/request | stale `RESOLVE` or `REJECT` | unchanged |

The example below uses latest-request-wins semantics. Starting a new request aborts the previous request when the underlying fetch supports `AbortSignal`. Request identity is still checked because cancellation is best-effort and some clients may resolve after abort.

## After: explicit state + request identity

```tsx
import { useCallback, useEffect, useReducer, useRef } from "react";

type State =
  | { status: "idle" }
  | { status: "loading"; requestId: number }
  | { status: "error"; message: string }
  | { status: "ready"; user: User };

type Event =
  | { type: "RESET" }
  | { type: "LOAD"; requestId: number }
  | { type: "RESOLVE"; requestId: number; user: User }
  | { type: "REJECT"; requestId: number; message: string };

function reducer(state: State, event: Event): State {
  switch (event.type) {
    case "RESET":
      return { status: "idle" };
    case "LOAD":
      return { status: "loading", requestId: event.requestId };
    case "RESOLVE":
      return state.status === "loading" && state.requestId === event.requestId
        ? { status: "ready", user: event.user }
        : state;
    case "REJECT":
      return state.status === "loading" && state.requestId === event.requestId
        ? { status: "error", message: event.message }
        : state;
    default: {
      const exhaustive: never = event;
      return exhaustive;
    }
  }
}

function UserCard({ id }: { id: string }) {
  const [state, dispatch] = useReducer(reducer, { status: "idle" });
  const sequence = useRef(0);
  const activeRequest = useRef<AbortController | null>(null);

  const load = useCallback(async () => {
    // Latest request wins. Abort is an optimization; requestId is the correctness guard.
    activeRequest.current?.abort();
    const controller = new AbortController();
    activeRequest.current = controller;
    const requestId = ++sequence.current;
    dispatch({ type: "LOAD", requestId });

    try {
      // Adapt this call to the existing data client; do not change a public API casually.
      const user = await fetchUser(id, { signal: controller.signal });
      dispatch({ type: "RESOLVE", requestId, user });
    } catch (error) {
      if (!controller.signal.aborted) {
        dispatch({
          type: "REJECT",
          requestId,
          message: error instanceof Error ? error.message : "Unknown error",
        });
      }
    } finally {
      if (activeRequest.current === controller) {
        activeRequest.current = null;
      }
    }
  }, [id]);

  useEffect(() => {
    // A changed resource id invalidates and aborts work for the previous id.
    activeRequest.current?.abort();
    activeRequest.current = null;
    sequence.current += 1;
    dispatch({ type: "RESET" });

    return () => {
      activeRequest.current?.abort();
      activeRequest.current = null;
      sequence.current += 1;
    };
  }, [id]);

  switch (state.status) {
    case "idle":
      return <EmptyState onLoad={load} />;
    case "loading":
      return <Spinner />;
    case "error":
      return <ErrorView message={state.message} onRetry={load} />;
    case "ready":
      return <Card user={state.user} />;
    default: {
      const exhaustive: never = state;
      return exhaustive;
    }
  }
}
```

**Integration note:** `fetchUser` must support an optional `AbortSignal` for the abort optimization shown above. If the existing client cannot be changed safely, retain its signature and keep request-ID validation; do not silently widen a public API. Also review effect cleanup and the actual component lifecycle in the target framework.

## Three-Lens result

| Lens | Gain |
|---|---|
| **UX** | The UI renders one explicit phase, and stale responses cannot replace the latest result. |
| **DX** | A single union defines state-specific data; transitions are centralized and exhaustively checked. |
| **AX** | State, event, and request identity are explicit and easy to locate; the table and tests can document the lifecycle. |

## What this example does not prove

It is illustrative, not a drop-in migration recipe. It does not establish that every app should use latest-request-wins semantics, that `fetchUser` accepts a signal, or that all race conditions are solved. Preserve the target application's established request policy and public contracts.
