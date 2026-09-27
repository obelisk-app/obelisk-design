# App sandbox

**The rules for running third-party app code (games, widgets) inside any Obelisk client, as a cross-project policy.** The wire format, the host API and the full threat model live next to the implementation, in [obelisk-apps/docs](https://github.com/obelisk-app/obelisk-apps/tree/main/docs): `app-format.md`, `host-api.md` and `security.md`.

## Trust boundary

An Obelisk app is code published by whoever can write to a relay. **It is untrusted, always.** It runs in an opaque-origin iframe that the host controls. The host (obelisk-dex, obelisk-tauri, the games.obelisk.ar Playground) is the only side that holds a signer, relay sockets or user data. Anything arriving from the frame is input to validate, including claims made by the SDK the app bundled.

## Rules for any host

1. **The sandbox attributes are fixed:**
   - `sandbox="allow-scripts"`, never `allow-same-origin`, `allow-popups`, `allow-top-navigation*` or `allow-forms`;
   - `allow=""`;
   - `referrerpolicy="no-referrer"`.
2. **No signer crosses the boundary.** The host builds every event the app causes. In v1 that's kind 2390 only, with the host setting `h`, `e`, `t` and `op`, and `n` the only tag an app may add. A new capability (another kind, encryption, payments) is a design change and gets a section here first.
3. **Run only pinned code.** Every blob is verified against the sha256 in the session's `create` event before the frame sees it. Nothing the app fetches itself is code the user agreed to run, which is one reason the frame has no network.
4. **The frame origin is its own.** The loader is served from `frame.obelisk.ar`, with the CSP in obelisk-apps `security.md`. It is never served from a console or app origin that holds a login session (for example `games.obelisk.ar`).
5. **Identity labels are drawn outside the frame.** The host draws the app's title and author (NIP-05 or short npub, per the "keys are never labels" rule) in chrome the frame can't reach. Toasts are prefixed with the app name.
6. **Discovery follows the relay rules.** Clients read manifests (kind 32390) from the active relay only, the same single-relay rule as groups. Publishing to a relay is what makes an app available there. Moderation is the relay operator's existing tools.
7. **The frame runs only while it's visible.** No background frames, and a stall watchdog offers "stop this app".
8. **Every allowed-origin list moves together.** Adding a host origin means updating the loader's `frame-ancestors` and `boot` allowlist, dex `src/proxy.ts` `frame-src`, and the obelisk-tauri CSP in the same change.

## Accepted defaults vs. future hardening

**Accepted for v1:**
- Participants' names and avatars are handed to the app as Blobs.
- Session events are delivered in full.
- Per-app localStorage in the host (256 KiB).

**Future hardening, not designed yet:**
- Per-app permissions declared in the manifest and approved by the user.
- An operator "featured apps" list.
- A WoT badge on app authors.
- An Obelisk-run Blossom server for first-party bundles.

## Known gaps

Recorded so they get fixed on purpose rather than rediscovered. Product-level gaps are in obelisk-apps `docs/known-issues.md`; only the cross-project ones are here.

1. **Self-navigation and WebRTC can still exfiltrate.** CSP can stop neither. A frame can navigate itself to a URL carrying data, and can open an `RTCPeerConnection` to any STUN/TURN server. Hosts detect a second iframe `load` and kill the frame, but only after the request has gone out.
2. **The Tauri CSP is maintained by hand.** `obelisk-tauri/src-tauri/tauri.conf.json` has its own `frame-src`, separate from dex's `src/proxy.ts`. The two have drifted before (Tauri's embed list is shorter).
3. **The frame loader has no deploy yet,** and so no owner. The frame origin needs the same `/health`-and-chunks deploy check as the other consoles once it exists.
4. **Kind 32390 is refused by NIP-29 relays** that require an `h` tag. obelisk-relay needs it added to `NON_GROUP_ALLOWED_KINDS`, and third-party group relays won't have a catalog at all.
5. **No signing-prompt budget.** With a NIP-07 extension, every app publish can raise an approval prompt that names the host, not the app. The host's rate limit is the only brake, and the prompt can't say which app is asking.
