# Nostr Auth

## Signer Order

1. NIP-07 browser signer for local desktop flows.
2. NIP-46 bunker/Nostr Connect for remote or mobile signing.
3. Imported nsec only when the user explicitly chooses it.

## Protocol Use

- Relay connection auth uses NIP-42 AUTH and should be renegotiated after reconnects.
- HTTP admin operations use NIP-98 when the server verifies method, URL, freshness, and signature.
- Existing relay admin challenge auth uses kind `22242` and should stay compatible unless the backend contract changes.

## Storage

- Prefer SDK signer storage for NIP-46 pairings and remembered imported nsecs.
- Do not store a second private-key copy under product-specific keys once SDK storage is active.
- Explicit logout should clear active signer state and persisted signer records.
