# Contributing

Thanks for helping make stateful code easier to reason about.

## Good contributions

- Detection signals for a language, framework, or workflow not covered.
- A before/after example with tests and clearly stated assumptions.
- Better guidance for request identity, retries, cancellation, cleanup, and concurrency.
- Improvements to the UX/DX/AX review criteria or report template.
- Fixes to installation notes or validation tooling.

## Contribution rules

1. Keep skills portable: plain Markdown and conservative YAML frontmatter.
2. Keep each skill self-contained so it can be installed independently.
3. Do not claim compatibility with an agent unless its current documentation supports the stated installation method.
4. Do not claim a refactor is behavior-preserving without relevant tests or evidence.
5. Avoid adding runtime dependencies. Development dependencies need a clear reason.
6. Mark fictional examples as fictional. Do not use fabricated benchmark numbers or real project claims.
7. Keep changes focused and update the README when the repository structure changes.

## Validate locally

```bash
python scripts/validate_skills.py
```

The validator checks required skill metadata, directory/name alignment, local Markdown links, and the presence of the primary instruction files. It is intentionally lightweight and does not replace the target agent's own skill loader.
