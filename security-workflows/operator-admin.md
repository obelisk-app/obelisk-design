# Operator Admin

Operator admin surfaces are high-trust tools. They should be boring, explicit, and hard to confuse with normal user flows.

## Rules

- Admin access must prove control of the configured operator pubkey.
- SFU operator auth remains NIP-98 over HTTP, verified server-side against the effective operator key.
- Relay admin auth remains challenge-based and must only mint a token after a valid signed event.
- Dangerous actions, including process restarts and whitelist bypasses, require explicit confirmation in the UI.

## Service Boundaries

- The SFU is a separate trust boundary because it terminates WebRTC media and runs as its own Nostr identity.
- Relays, SFUs, and app frontends should be independently replaceable and discoverable rather than centralized behind one global service.
