# AGENTS.md

This project is in Stage 0. Keep changes small, local, and easy to inspect.

## Hard Constraints

- Do not connect to real APIs.
- Do not create complex agents or multi-agent workflows.
- Do not create n8n workflows or automated schedules.
- Do not add databases, vector stores, external caches, or external storage.
- Do not write API keys, passwords, tokens, or credentials into the repository.
- Do not provide deterministic stock trading recommendations, such as advising users to buy, sell, hold, overweight, or expect guaranteed returns.
- Required safety disclaimers may mention buy, sell, or hold in a negative form, such as stating that the report does not provide buy, sell, or hold recommendations.
- Keep stock-related reports strictly as research assistance and not investment advice.

## Preferred Approach

- Use simple Python standard library code unless a dependency is clearly necessary.
- Keep generated reports as Markdown files.
- Keep tests focused on the Stage 0 contract.
- Document future ideas in `docs/roadmap.md` instead of implementing them early.
