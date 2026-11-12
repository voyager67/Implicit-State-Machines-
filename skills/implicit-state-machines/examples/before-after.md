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
      const result = await fetchUser(id);
      setUser(result);
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
| non-matching state/request | stale result | unchanged |

## After: explicit state + request identity

```tsx
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
      return state.status === "loading" &&
        state.requestId === event.requestId
        ? { status: "ready", user: event.user }
        : state;
    case "REJECT":
      return state.status === "loading" &&
        state.requestId === event.requestId
        ? { status: "error", message: event.message }
        : state;
    default: {
      const exhaustive: never = event;
      return exhaustive;
    }
  }
}
```

The effect owner must still prevent duplicate work, cancel or replace old requests if that is the intended policy, and send the request ID with the result. Cancellation is an optimization; checking request identity at the state boundary is the correctness guard.

**Integration note:** adapt the fetch client to accept an optional `AbortSignal` only if the existing public contract can safely support it. Otherwise retain the current signature and rely on request identity. Review effect cleanup and component lifecycle in the target framework.

This is an illustration, not a drop-in migration recipe. Preserve the target application's established request policy and public contracts.
