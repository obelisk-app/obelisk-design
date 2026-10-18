# Real Footage Backlog

Every place where an Obelisk README or video shows a drawing, a mock or an old still because no real recording of the product exists yet. "Real" means a screen or device recording of the live product, made by the scripted recording kit in `obelisk-media/recording/` or by hand.

Surveyed 2026-10-17 from the README of every public `obelisk-app` repo, `obelisk-media/PRODUCTION-PLAN.md`, `obelisk-media/RENDER-REPORT.md` (the 2026-10-08 recording session) and the files under `obelisk-media/videos/`. Shot ids (A1, C4, …) are the production plan's. Update this page when a shot is recorded or a gap is filled; [README showcase](readme-showcase.md) says how the footage goes into a README.

## At a glance

| Repo | Real motion in its README today | Main gap |
|---|---|---|
| obelisk | One demo video (GitHub user-attachment) | Every feature shown only as a still; voice uses a test pattern, not people |
| obelisk-sky | None (stills, a stills slideshow, drawn SVGs) | A recording of the village: posting, walking, zaps, calls |
| obelisk-relay | None (console stills) | Console clips D1–D6 are recorded but unused; terminal install E1 never recorded |
| obelisk-sfu | None (stills from a 2026-09-26 demo run, drawn SVGs) | A real multi-person call through the SFU; current console stills |
| obelisk-agents | None (stills, drawn chat and terminal SVGs) | Bot answering in a channel; a bot build from New bot to online |
| obelisk-apps | None (stills, a drawn Chain Reaction game) | Two people playing each game in a channel |
| obelisk-menhir | **No media at all** | Everything: the desktop app, one-click hosting, a friend joining over Tor |
| obelisk-kindle-lite | None, and its README is a copy of obelisk's | A photo or clip of the client on a Kindle |
| .github (org profile) | Sky's stills slideshow only | A short real cut of the app |
| obelisk-design | Not a product; no footage needed | Optional: stills of the three consoles in the "One shell" table |

## What already exists

### Recorded clips (2026-10-08, `videos/_captures/recordings/`)

Eleven clips passed review, 1920×1080, 60 fps (Playwright source re-encoded):

| Clip | What | Caveat |
|---|---|---|
| A7 | Following feed, frame-exact scroll, 8 s | |
| A10 | Settings: profile and appearance, 20 s | Marketplace thumbnails broken on screen |
| C1 | Agents fleet dashboard | Agents UI was in English |
| C3-preview | New bot form with the job typed, cancelled | No bot built |
| C6 | Agents settings, write-only secret fields | |
| D1–D6 | Relay landing → admin, overview, access check, groups, reports, storage | D4 shows Events only, not Members; **D5 shows real reports: blur names**; D6 may need its "Counting" indicator cut |

None of these is used in any README yet.

### Finished or draft videos (`videos/*/renders/`)

None of these is linked from a README, and no repo records a published URL for any of them (no YouTube links found).

| Video | File | State (production plan) |
|---|---|---|
| Promo, EN and ES, 40 s | `obelisk-promo/renders/obelisk-promo.mp4`, `-es.mp4`, `-9.99mb.mp4` | Done |
| Relay explainer, 183 s | `obelisk-relay/renders/obelisk-relay.mp4`, `-60fps.mp4` | Masters restored |
| Shorts ×11, 16:9 and 9:16 | `obelisk-shorts/renders/obelisk-{hangout,install,ladder,numbers,sigma,snapshot,speedrun,thisis,whatis}-*.mp4`, `obelisk-relay-shorts/renders/obelisk-aura-*.mp4` | `hangout` uses drawn call tiles, waiting on A8/A9 |
| Getting started v9 | `obelisk-getting-started/renders/…-v9-60fps-high-from-00m08s.mp4` | Provisional captures; v10 waits on A1/B1 |
| Agents promo v1 | `obelisk-agents/promo-video/renders/obelisk-agents-v1-10fps.mp4` | 10 fps review cut; 60 fps final waits on review notes |
| Quantum-safe DMs v5 | `obelisk-quantum-safe-dms/renders/…-v5-steady-music-cta-24fps.mp4` | Waits on real chat screenshots and a closing line |
| Live wallpaper | `obelisk-wallpaper/renders/obelisk-wallpaper-*.mp4` | Done |

The demo video in obelisk's README is a GitHub user-attachment (`4b6e31a9-…`); which cut it is could not be checked from here.

## Missing, by repo

### obelisk (the app)

README today: the animated logo GIF, four stills committed by 2026-10-09, two guide diagrams and the demo video. The voice still shows a test peer streaming SMPTE colour bars.

| Shot | What it should show | Status / blocker (2026-10-08) |
|---|---|---|
| A1 | New account: Connect → Create → nsec backup → profile | Login UI came out in English. Fresh identities are now not allowed (real-account QR only), so this needs a decision on how to show account creation |
| A2 | Server list → join La Crypta → channels | Held: pending NIP-42 signer overlay (kind 22242) on screen |
| A3 | Chat: send, reply, ⚡ react, emoji/GIF/sticker picker, @mention | Held: `#Stress Test` shows a lock and no composer for the account |
| A4 | `/zap` and Zap Bot answering | Not run: needs `--allow zap` (spends 1 sat) |
| A5 | Forum → open a post → reply | Held: signer overlay; flow opens the child-channel chat, not the thread reader |
| A6 | DM with the quantum-safe (PQ) shield | Held: the DM shield shows standard encryption, not PQ |
| A8 | Voice: join, second person, speaking rings, screen share, call chat | Held: second camera never appears; UI waits on a kind 20078 media signature ("Sincronizando medios") |
| A9 | Chain Reaction, Vesta and Stacker started from chat | Held: the second account can't find `#Stress Test` |
| A11 | Server admin: roles, emoji admin | Held: signer overlay |
| B1 | Phone: create an account | Same as A1 |
| B2 | Phone: channel drawer → chat → send | Held with A3 |
| B3 | Phone: Following feed with photos | Visual fail: desktop layout inside phone emulation |
| B4 | Phone: Amber / NIP-46 sign-in | Manual only (`scrcpy`), never done |
| B5 | Phone: join a call, open a game | Fails: join-voice button selector not found |

Also missing: a real voice/SFU call with people instead of colour bars, for the README's voice still.

### obelisk-sky

README today: 14 stills, a stills slideshow (`tour.webp`) and three drawn SVGs. Some stills (nostr-wot HQ, café, parrilla in the landmarks collage) predate the current header. Sky has **no shots in the production plan**.

Wanted, all as short real clips (desktop 16:9, plus a phone cut):

- Posting in a channel and the character walking to its house; the sign's count going up
- Replying to someone and walking over to them
- A zap flying sender → recipient and bursting into coins
- Day turning to night (lit windows, lamps)
- Mate going round a bench; the café and the parrilla
- Riding a nostrich round the track; swimming the river under a bridge
- A voice call joined from a pavilion; a shared screen on the theater wall
- The look creator, then seeing yourself in the village
- First-person walk with the minimap
- The guest island for a logged-out visitor
- The same on a phone (thumb stick, tap to walk)

### obelisk-relay

README today: seven console stills.

| Shot | Status |
|---|---|
| D1–D6 | Recorded (see above), not used. D4 needs a retake that opens Members; D5 needs names blurred |
| E1 | Terminal: `git clone` → `./setup.sh` → `./expose.sh` → relay online. Never recorded; must run in a fresh VM. Also wanted as an `asciinema` cast |

### obelisk-sfu

README today: four console stills from a 2026-09-26 demo run (before the console restyle and the new mark; captioned as such), the app's colour-bar voice still, and two drawn SVGs. The SFU has **no shots in the production plan**, and the console redeploy with the new logo (plan task 0.3) is still open.

- A call with three or more real participants routed through the SFU: speaking rings, then a screen share
- The admin console during that call: live rooms and peers
- Current console stills after the 0.3 redeploy
- Mobile joining the same call (overlaps B5)

### obelisk-agents

README today: four stills, a drawn chat SVG and a drawn terminal SVG (some values in it are examples).

| Shot | Status |
|---|---|
| C2 | Restart a bot and tail its logs. Fails: "Manage →" doesn't open the bot page |
| C3 | New bot built for real. Not run: needs `--allow build` (a paid Codex build) |
| C4 | Operator run streaming to "bot online". Recorded only the history; doesn't open a finished run |
| C5 | `!asado` (or the new bot's command) answered in Obelisk. Skipped: no asado bot exists |

Also wanted: a real `npm run new-bot` and `pm2 logs` terminal session to replace the drawn terminal, and price-bot answering `!btc` in a channel to replace the drawn chat.

### obelisk-apps

README today: stills of chess, Vesta, Stacker and the lobby (from an obelisk-dex session) and a drawn Chain Reaction game.

- Two people playing each game from a channel: Chain Reaction, chess, Vesta, Stacker (overlaps A9)
- A Chain Reaction still or clip mid-game (the only capture shows a single orb)
- Publishing an app: the build, the Blossom upload and the app appearing in the catalog

### obelisk-menhir

README today: badges only. The latest release is v0.1.6 (2026-07-31).

- The desktop app: hosting a server in one click, the onion address appearing
- Sharing the `obelisk://join` link and a friend joining over Tor
- Channels: chat, publications, replies, emoji
- The headless relay starting (terminal) and the terminal client
- The Android client-only build
- At least four stills for the README

### obelisk-kindle-lite

Its README is a copy of obelisk's (same GIF, stills and text). It needs its own: a photo or clip of the client running on a Kindle, and stills of its pages.

### .github (org profile) and obelisk-design

- Org profile: a short real cut of the app (from the A shots) to sit next to Sky's slideshow
- obelisk-design: optional stills of the relay, SFU and agents consoles for the "One shell, three consoles" table

## Decisions needed before recording

From the 2026-10-08 report, still open:

1. Signing overlays: channel shots keep showing pending NIP-42 (kind 22242) signer requests even after successful AUTH acks. Clear them before A2, A5, A11.
2. `#Stress Test` access for both the main account and Dummy (A3, A9, B2).
3. Kind 20078 media signatures for a second participant (A8).
4. PQ capability for the paired accounts (A6).
5. How to film account creation now that fresh identities are off the table (A1, B1).
6. Whether to spend the sat (A4) and the paid build (C3).
7. Blurring D5's report names before any use.

Sky, SFU, apps and menhir need shot lists added to `obelisk-media/PRODUCTION-PLAN.md` before the kit can record them.
