# Frontend Style

## Auth and Data

- Do not add a second auth store for the same user identity.
- For Nostr login, prefer `@nostr-wot/ui` where React/Preact compatibility exists.
- For static or non-React surfaces, use `@nostr-wot/signers` and keep the host UI simple.
- Relay-derived data should go through the established client/bridge layer instead of ad hoc subscriptions scattered through components.

## UI

- Admin pages should optimize for repeated use, not first-visit persuasion.
- Keep status, error, and loading states stable so controls do not shift while signing or reconnecting.
- Follow the La Crypta tokens for Obelisk-owned admin and relay surfaces.
