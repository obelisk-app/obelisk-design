# Admin Console Authentication

How the three Obelisk operator consoles sign people in, as implemented in September 2026. This page describes the code as it is. The rules to follow are in [Nostr auth](nostr-auth.md) and [Operator admin](operator-admin.md). Gaps between the two are listed under [Known gaps](#known-gaps).

| Console | Client | Server |
|---|---|---|
| Relay admin | `obelisk-relay/frontend/src/components/admin/{AdminAuth.tsx,adminSigner.ts}`, `services/AdminApiClient.ts` | `obelisk-relay/src/admin.rs` (Rust, axum) |
| SFU admin | `obelisk-sfu/admin-ui/src/{auth.ts,api.ts,main.tsx,components/Login.tsx}` | `obelisk-sfu/src/{admin.ts,admin-session.ts,http-server.ts}` |
| Agents manager | `obelisk-agents/frontend/src/{auth.ts,api.ts,main.tsx,components/Login.tsx}` | `obelisk-agents/server/{auth.mjs,index.mjs,config.mjs}` |

## Client libraries (the same in all three)

| Package | Version | Used for |
|---|---|---|
| `@nostr-wot/ui` | 0.7.1 | `NostrSessionProvider`, `LoginModal` / `LoginWidget`, `useSigner`, `useLogout` |
| `@nostr-wot/signers` | 1.2.0 | Signer types, `BunkerSigner`, and the persistence helpers `clearPersistedNip46` and `clearPersistedNsec` |
| `nostr-tools` | 2.x | `SimplePool` profile fetch; `verifyEvent` on the Node servers |

`@nostr-wot/ui` is written for React. Each Vite config aliases `react` to `preact/compat`.

### Wiring

```tsx
// main.tsx: wraps the whole app
<NostrSessionProvider theme="la-crypta" autoRestore>…</NostrSessionProvider>
```

- **Hooks:** only `useSigner()` and `useLogout()` are used. Nothing reads `usePubkey` or `useSession`; the server session, not the SDK, is the source of truth for who is signed in.
- **Sign-in UI:**
  - SFU and agents use `<LoginModal>`, which opens automatically if the SDK has not restored a signer within 450 ms.
  - The relay uses an inline `<LoginWidget showRememberToggle>`.
- **Sign-in UI props (all three):**
  - `methods={['nip07','nip46','import']}`
  - `nip46Mode="qr"`
  - `flatLayout`
  - `nip46Metadata={{ name: '<Product> Admin', url: location.origin }}`

### Signers

- **Signer order:** NIP-07 extension, then NIP-46 (bunker QR / `nostrconnect://`), then nsec import.
- **Auto sign-in:** a signer the SDK restored signs in without a click.
- **NIP-46 rendezvous relays:**
  - SFU and agents: `wss://public.obelisk.ar`, `wss://relay.damus.io`, `wss://nos.lol`, `wss://relay.primal.net`.
  - Relay: its own origin first, then damus, nos.lol and primal.
- **Restoring a dead bunker:**
  - A stored NIP-46 pairing is rebuilt from `localStorage[SIGNER_STORAGE_KEY_NIP46]` with `BunkerSigner.fromBunker(clientSecret, bp)`, *without replaying `connect`*.
  - Errors matching `/not open anymore|signer is closed|no longer open/i` mean the signer is dead. The console retries once with a rebuilt signer; failing that, it discards the stored pairing and says "Sign in again".
- **Signer timeouts:** 30 s in the SFU and agents, 15 s in the relay.
- **Mobile deep link:** `Nip46SignerDeepLink.tsx` watches the widget's QR box for a `nostrconnect://` URI and adds an "Open in signer app →" link. The SFU and agents copies are byte-identical, ported from the relay's.
- **The `awaitingChoice` / `fresh` pattern:**
  - A NIP-07 extension is always present in `window.nostr`, so after a logout the SDK re-derives a signer immediately, and the auto sign-in effect would log straight back in.
  - After logout, "Use another signer", or discarding a dead signer, the login screen is therefore mounted with `fresh` / `awaitingChoice = true`, and nothing authenticates until the person picks a method.

## Proof sent to the server

**SFU: NIP-98** (HTTP Auth, kind 27235). There is no challenge.

```ts
{ kind: 27235, created_at: now, content: '',
  tags: [['u', location.origin + '/admin/session'], ['method', 'POST']] }
// POST /admin/session   Authorization: Nostr base64(JSON(event))
```

- Every other admin endpoint also accepts a per-request NIP-98 header when there is no session cookie. This is for scripts.

**Relay and agents: a challenge event** (kind 22242, the NIP-42 shape over HTTP).

```ts
const { challenge } = await GET('/api/admin/challenge')      // agents: /api/auth/challenge
{ kind: 22242, created_at: now, content: '',
  tags: [['relay', location.origin.replace(/^http/, 'ws')], ['challenge', challenge]] }
// POST /api/admin/auth  { signed_event }                     // agents: POST /api/auth/login { event }
```

## Server verification

| | SFU | Agents | Relay |
|---|---|---|---|
| Signature | `verifyEvent` | `verifyEvent` | `event.verify()` (id + sig) |
| Freshness | `created_at` within ±60 s | challenge < 5 min **and** `created_at` within ±600 s | challenge < 300 s; `created_at` not checked |
| Binding | `method` must match; the `u` path + query must match (host ignored on purpose) | `relay` tag not checked | `relay` tag not checked |
| Replay | the 60 s window only | single-use challenge | single-use challenge (consumed only after the admin check passes) |
| Who is allowed | one operator: `SFU_OPERATOR_PUBKEY`, falling back to the SFU's own key; overridable in `runtime.json` | `MANAGER_ADMIN_NPUBS` (comma list; the default is the owner's npub) | YAML `admin_pubkeys` + `config/admin_pubkeys_runtime.json`, editable at runtime; first-run `POST /api/admin/setup` only while the list is empty |
| Non-admin response | 403 `not the operator` | 400 `pubkey … is not an admin` | 403 `Not an admin pubkey` |

## Sessions

| | SFU | Agents | Relay |
|---|---|---|---|
| Carrier | cookie `obelisk_sfu_admin` | cookie `obelisk_manager` | `Authorization: Bearer <token>` |
| Cookie flags | `Path=/admin; HttpOnly; SameSite=Strict`, plus `Secure` behind https | `Path=/; HttpOnly; SameSite=Strict` (no `Secure`) | — |
| Client storage | none (HttpOnly) | none (HttpOnly) | `sessionStorage['admin_token']` |
| Token | 32 random bytes, hex | 32 random bytes, hex | 32 random bytes, hex |
| Server storage | sha256 of the token, `admin-sessions.json` (mode 0600), survives restarts | plaintext token, `state/manager/sessions.json` (mode 0600) | memory only, so a restart signs everyone out |
| TTL | 12 h | 30 days | 4 h |
| Session check | `GET /admin/session` → `{authed, pubkey}` | `GET /api/auth/session` → `{authed, npub, pubkey, profile}` | `GET /api/admin/session` → `{valid, pubkey}`, or 401 |
| Operator key change | re-checked per request, so existing sessions are revoked | — | — |
| Other defences | — | server binds 127.0.0.1; `Origin` host must match (403 otherwise) | — |
| On 401 | `UnauthorizedError`, toast "Session expired", back to login | shows the error text only | `clearToken()`, "Session expired" |

## Logout

The rule (see [Operator admin](operator-admin.md#logout)) is to clear **all three** layers, then show the login screen with `fresh`.

```ts
await api.logout().catch(() => {})     // 1. server session (DELETE / POST …/logout)
await clearStoredSigners(signer)       // 2. signer.close() + clearPersistedNip46() + clearPersistedNsec()
await sdkLogout().catch(() => {})      // 3. @nostr-wot/ui session (useLogout)
onLogout()                             // → <Login fresh />
```

- **SFU and agents:** do all three steps.
- **Relay:** has no server logout endpoint. It clears its token, the stored signers and the SDK session, and the server token lapses at its 4 h TTL.
  - Until the September 2026 shell update, the relay cleared only the token. The login screen then silently signed back in with the still-held signer.

## Profile of the signed-in identity

Kind 0 from public relays, with the newest event winning. It is shown in the sidebar profile card (see [Admin shell](../design-system/admin-shell.md#profile-card)).

| | Where | Relays |
|---|---|---|
| SFU | browser, `profiles.ts` (`useProfiles`) | purplepag.es, damus, nos.lol, primal |
| Agents | server, `profiles.mjs`; returned in the session response; 2 min cache on disk | `MANAGER_PROFILE_RELAYS`, defaulting to the same four |
| Relay | browser, `services/ProfileFetcher.ts` | damus, nos.lol, purplepag.es |

## Known gaps

Recorded so they are fixed on purpose, not rediscovered.

1. **Agents: session cookie has no `Secure` flag.** It sits behind TLS termination, so add `Secure` when `x-forwarded-proto` is https, as the SFU does.
2. **Agents: session tokens are stored in plaintext on disk.** Hash them, as `admin-session.ts` in the SFU does.
3. **Agents: a non-admin key gets 400, not 403.** The frontend also has no 401 handling, so an expired session shows raw error text instead of returning to login.
4. **Relay and agents: the `relay` tag of the 22242 event is not checked.** A challenge is single-use and server-issued, so the practical risk is low. Still, binding the tag to the serving origin closes cross-service reuse.
5. **Relay: `created_at` is not checked**; only the challenge age is.
6. **Relay: no server-side logout.** The token stays valid until its TTL even after the operator signs out.
7. **SFU: NIP-98 replay is bounded only by the ±60 s window.** There is no seen-id cache. Acceptable for a single operator; add one if more admins are allowed.
8. **Three copies of the signer helpers** (`auth.ts` / `adminSigner.ts`, `Login.tsx`, `Nip46SignerDeepLink.tsx`). They have already drifted: the timeouts and relay lists differ. They are candidates for a shared package.
