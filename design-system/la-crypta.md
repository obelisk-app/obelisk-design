# La Crypta Tokens and Patterns

## Tokens

- Background: `#0a0a0a`
- Surface: `#171717`
- Border: `#262626`
- Accent: `#b4f953`
- Text: `#fafafa`
- Muted text: `#a3a3a3`
- Danger: `#ef4444`

## Component Patterns

- Use `lc-card` for framed admin panels and modal-like surfaces.
- Use `lc-pill-primary` for the primary action and `lc-pill-secondary` for secondary actions.
- Use `lc-spinner` for in-place async state, not custom loading text that shifts layout.
- Preserve the green accent for trust, authentication, online, and primary confirmation states.

## Login Surfaces

- Prefer `@nostr-wot/ui` with `theme="la-crypta"` when the host app has a bundler and React/Preact compatibility.
- Static admin pages may use `@nostr-wot/signers` signer primitives and keep their local HTML/CSS shell.
