# Operator Admin

Operator admin surfaces are high-trust tools. They should be boring, explicit, and hard to confuse with normal user flows.

## Rules

- Admin access must prove control of the configured operator pubkey.
- SFU operator auth remains NIP-98 over HTTP, verified server-side against the effective operator key.
- Relay admin auth remains challenge-based and must only mint a token after a valid signed event.
- Dangerous actions, including process restarts and whitelist bypasses, require explicit confirmation in the UI.

## Logout

Signing out must clear every layer that could sign the operator back in:

1. **The server session.** Revoke the token or cookie server-side where an endpoint exists.
2. **The stored signers.** `signer.close()`, then `clearPersistedNip46()` and `clearPersistedNsec()` from `@nostr-wot/signers`.
3. **The SDK session.** `useLogout()` from `@nostr-wot/ui`.
4. **The login screen after logout.** Show it with an explicit-choice flag (`fresh` / `awaitingChoice`). A NIP-07 extension is always re-derivable, so without the flag the auto sign-in effect logs straight back in.

The per-console implementation is in [Admin console auth](admin-console-auth.md#logout).

## Service Boundaries

- The SFU is a separate trust boundary because it terminates WebRTC media and runs as its own Nostr identity.
- Relays, SFUs, and app frontends should be independently replaceable and discoverable rather than centralized behind one global service.
