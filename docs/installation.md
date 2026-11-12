# Installation

This repository follows the open Agent Skills format. Each skill is a self-contained directory with a `SKILL.md` file, YAML frontmatter, and Markdown instructions.

## Install with the Agent Skills CLI

Requires Node.js 22.20 or later. From your project, run:

```bash
npx skills add voyager67/Implicit-State-Machines-
```

Choose `implicit-state-machines`, `vibe-refactor-protocol`, or both when prompted, then select the coding agent(s) to install to.

For a private checkout, configure GitHub authentication before running the command. Public access is not required for members who already have repository access.

## Manual installation

Copy either skill directory—or both—into a skills directory recognized by your agent:

- `skills/implicit-state-machines/`
- `skills/vibe-refactor-protocol/`

Common project-local conventions include `.agents/skills/`, `.claude/skills/`, `.cursor/skills/`, and `.github/skills/`. Global locations and discovery behavior differ by tool and may change; follow the target agent's current documentation.

## Which skill should I use?

- **implicit-state-machines:** repository-wide discovery, inventory, ranking, transition modeling, and safe improvement decisions.
- **vibe-refactor-protocol:** code-first diagnosis and focused refactoring with the Diagnosis → Refactored Code → UX/DX/AX output.

Both skills are self-contained. They do not require XState or another runtime dependency.
