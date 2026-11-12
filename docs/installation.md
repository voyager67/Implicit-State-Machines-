# Installation

This repository uses the open Agent Skills-style convention: each skill is a directory containing a `SKILL.md` file with YAML frontmatter and Markdown instructions.

## Install with a skills installer

Where your agent supports the skills CLI, install the repository with:

```bash
npx skills add YOUR_GITHUB_USERNAME/implicit-state-machines
```

Replace `YOUR_GITHUB_USERNAME` with the repository owner. Check the installer's current agent list and flags; installer support changes independently of this repository.

## Manual installation

Copy either skill directory—or both—into a skills directory recognized by your agent:

- `skills/implicit-state-machines/`
- `skills/vibe-refactor-protocol/`

Common project-local conventions include `.agents/skills/`, `.claude/skills/`, `.cursor/skills/`, and `.github/skills/`. Global locations and discovery behavior differ by tool and may change; follow the target agent's current documentation.

## Which skill should I use?

- **implicit-state-machines:** repository-wide discovery, inventory, ranking, transition modeling, and safe improvement decisions.
- **vibe-refactor-protocol:** code-first diagnosis and focused refactoring with the requested Diagnosis → Refactored Code → UX/DX/AX output.

Both skills are self-contained. They do not require XState or another runtime dependency.
