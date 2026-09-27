# Security Workflows

Obelisk security workflows are Nostr-first: identity is a key, authorization is event-based, and privileged services have explicit operator boundaries.

## Defaults

- Do not introduce a parallel auth store when a Nostr signer/session already exists.
- Keep private keys in the browser signer path when possible: NIP-07, NIP-46, or SDK signer storage.
- Use NIP-42 for relay authentication, NIP-98 for HTTP authorization, and service-specific challenge events only where already established.
- Treat every media or storage boundary as a threat-model decision, not a styling or routing detail.

## Canonical Pages

- [Nostr auth](nostr-auth.md)
- [Operator admin](operator-admin.md)
- [Admin console auth](admin-console-auth.md) - how the relay, SFU and agents consoles actually sign in, verify, hold sessions and log out, with known gaps
