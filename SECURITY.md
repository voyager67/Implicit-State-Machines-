# Security Policy

## Reporting a vulnerability

Do not publish secrets, tokens, private source code, or exploitable details in a public issue. Contact the repository maintainer through GitHub's private vulnerability reporting mechanism when it is enabled, or use a private maintainer contact listed on the repository profile.

## Scope

This repository primarily contains Markdown instructions, examples, a small validation script, and GitHub Actions configuration. It does not include an application runtime or request credentials. Reports about unsafe instructions, destructive coding-agent behavior, malicious examples, or workflow permissions are in scope.

## Safe use

The skills instruct coding agents to inspect working-tree changes, preserve user files, avoid exposing secrets, and ask before high-risk API or data migrations. Always review agent-proposed patches before merging them.
