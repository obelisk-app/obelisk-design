# Design System

Obelisk uses the La Crypta visual system across the app, relay admin, SFU admin, and SDK-backed login surfaces.

## Core Rules

- Prefer existing `lc-*` utility classes and CSS variables before adding new styling primitives.
- Keep operational tools dense, quiet, and scannable. Avoid marketing-style hero sections inside admin or moderation workflows.
- Use `#b4f953` as the primary green accent and dark neutral surfaces for La Crypta-admin surfaces.
- Use cards for bounded tools, modals, or repeated entities. Do not stack decorative cards inside page sections.
- Keep buttons action-specific; use icon buttons only when the symbol is familiar or has a tooltip.

## Canonical Pages

- [La Crypta tokens and patterns](la-crypta.md)
- [Admin console shell](admin-shell.md) - the shared sidebar, header banner, grid background, profile card and product logos
- [Logos](logos/) - SVG product marks for Obelisk Relay, Obelisk SFU and Obelisk Agents. Use these for the product, never an instance's own icon (e.g. the purple "P" of `public.obelisk.ar`)
