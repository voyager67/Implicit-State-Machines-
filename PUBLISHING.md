# Publishing checklist

1. Create a public GitHub repository named `implicit-state-machines` (or choose a matching name before publishing).
2. Upload the contents of this directory to the repository root—not the enclosing parent folder.
3. Set the repository description to:

   `Portable AI agent skills to discover hidden application state machines and safely refactor boolean soup across UX, DX and agent experience.`

4. Add topics such as `agent-skills`, `state-machines`, `vibe-coding`, `refactoring`, `software-architecture`, `coding-agents`, `developer-experience`, and `ai-agents`.
5. Run `python scripts/validate_skills.py` locally and confirm the GitHub Actions workflow passes.
6. Review the rendered README and SVG banner on both desktop and mobile widths.
7. Add a release tag after reviewing the repository and license.

Suggested first release: `v1.1.0`.

Do not promise instant stars or guaranteed support for every AI tool. State clearly that auto-discovery and installation locations depend on the target agent.
