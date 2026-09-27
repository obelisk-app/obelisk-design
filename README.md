# Obelisk Design

Canonical design, security workflow, and development style documentation for the Obelisk family of projects.

This repository collects the shared rules that were previously scattered across `obelisk`, `obelisk-dex`, `obelisk-relay`, and `obelisk-sfu`. It should stay concise and link back to implementation-specific docs when the details belong in a product repo.

## Sections

- [Design system](design-system/README.md) - La Crypta/Obelisk visual language, tokens, and UI rules.
- [Security workflows](security-workflows/README.md) - Nostr auth, operator admin, storage, and threat-model defaults.
- [Development style](development-style/README.md) - Engineering conventions for frontend, docs, tests, and specs.

## Source References

- `obelisk_repo/README.md` and `obelisk-dex/README.md` for contribution and design-system guidance.
- `obelisk-sfu/docs/sfu-system.md` for operator-run SFU trust boundaries.
- `obelisk-relay/frontend/src/components/admin/AdminPanel.tsx`, `obelisk-sfu/admin-ui/src/components/Console.tsx` and `obelisk-agents/frontend/src/components/Layout.tsx` for the shared admin shell.
- `obelisk_repo/docs/uploads.md` for storage threat-model language.
- `obelisk_repo/docs/admin-cli.md` for operator and agent-admin workflows.
