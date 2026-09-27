# Admin Console Shell

The layout shared by the three Obelisk operator consoles. They must look like one family:

| Console | Code | Served at |
|---|---|---|
| Relay admin | `obelisk-relay/frontend/src/components/admin/AdminPanel.tsx` | `/admin` on the relay |
| SFU admin | `obelisk-sfu/admin-ui/src/components/Console.tsx` | `/admin/` on the SFU |
| Agents manager | `obelisk-agents/frontend/src/components/Layout.tsx` | `agents.obelisk.ar` |

All three are Preact + Vite + Tailwind 3, with `lc-*` classes in each repo's `style.css`. The relay console is the reference: when the three disagree, match the relay.

```
┌──────────────┬──────────────────────────────────────────────┐
│ [logo] Name  │ Section title                                │  ← header banner, 112px
│              │ One-sentence blurb                           │    (never scrolls)
├──────────────┼──────────────────────────────────────────────┤  ← one continuous 1px rule
│ ▣ Overview   │                                              │
│   short desc │   scroll region — the only thing that        │
│ ▣ Access     │   scrolls, 60px line grid behind the cards   │
│   short desc │                                              │
│ …            │                                              │
├──────────────┤                                              │
│ [footer act] │                                              │
│ ┌──────────┐ │                                              │
│ │ ◯ Name  ⇥│ │  ← profile card                              │
│ └──────────┘ │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

## Sidebar

- **Width:** 18rem (288px). The main column is offset by the same amount (`lg:pl-72`, or `md:w-72` on the relay).
- **Background:** `#171717` (`--color-bg-secondary`), opaque, with no blur. The right border is `1px solid #262626`.
- **Brand block:** at the top, the same height as the header banner, with a `#262626` bottom border so the rule runs straight across into the header. It holds the 32px logo and the product name, which is `font-extrabold text-lg`, with the product word in the accent colour.
- **Nav:** a column with `gap: 8px` and `padding: 12px`. It scrolls internally (`flex-1 min-h-0 overflow-y-auto`), so the footer never gets pushed below the fold.
- **Nav item:** two lines, as below.

  | Part | Style |
  |---|---|
  | Label | 14px, weight 600, `#fafafa` |
  | Description | 12px, `#a3a3a3`, 2px below the label |
  | Icon | 20px (18px on the relay's own 20×20 set), opacity 0.8, 10px gap to the text |
  | Box | `padding: 12px`, `border-radius: 8px`, 1px transparent border |
  | Hover | `rgba(255,255,255,0.03)` background |
  | Active | background `rgba(accent, 0.09)`, border `rgba(accent, 0.26)`, label in the accent colour, description in `rgba(accent, 0.78)` |

  In the SFU and agents consoles these are the `.lc-nav-item`, `.lc-nav-label` and `.lc-nav-desc` classes.
- **Footer:** separated by a top border. It holds the product-specific actions (the relay's **Open Chat**, the SFU's Live/refresh badge, the agents "part of the Obelisk family" line) and then the profile card, which is always last.
- **Nav entries are data.** Each entry is `{ id | href, label, description, blurb, icon }`, declared once. `description` is the line under the sidebar entry and `blurb` is the header sentence. Pages must not repeat their own title in the body.
- **Links out:** a destination that is its own page is still a nav entry, rendered as an `<a>` in the same style. For example, the relay's **Docs** entry opens `/docs` in a new tab.

## Menu structure

Each console declares its menu once, as an array. The sidebar, the header banner and (on the relay) the global search all read from it.

```ts
interface NavItem {
  id: string            // SFU/relay: the view key (the SFU keeps it in location.hash); agents: `href` (a route)
  label: string         // sidebar label and header <h1>
  description: string   // one short line under the sidebar label, 2–4 words
  blurb: string         // one sentence in the header banner under the title
  icon: () => JSX.Element
}
```

- **Order:**
  1. Overview (health) first.
  2. The main working sections.
  3. Settings.
  4. Links out (Docs) last.
- **Writing `description` and `blurb`:**
  - `description` says what the section *is*: "Tiers, search and blocks".
  - `blurb` says what you *do or see* there, as a full sentence.
  - Do not repeat the label in either.
- **Active state:**
  - A sub-page highlights its parent (agents: `/bots/:name` → Fleet) and keeps the parent's header.
  - Hidden sections are filtered out of the array, not greyed out. Example: the SFU drops Test peers when `snap.testPeers === null`.
- **Sidebar footer order, top to bottom:** product actions, then status badge, then profile card.

### Relay admin (`AdminPanel.tsx`, `tabs`)

| Label | Description | Blurb |
|---|---|---|
| Overview | Relay health | Live health, what is configured, and anything that needs attention. |
| Access | Tiers, search and blocks | Every rule that decides who can connect, and who each one lets in. |
| Groups | Metadata and moderation | Browse relay groups, metadata, members, and stored events. |
| Reports | User moderation reports | What users have reported, grouped by what was reported, with the decision you made. |
| Storage | Database and pruning | What this relay has stored, and whether anything is being deleted. |
| Settings | Reset and recovery | Operational controls for identity, admins, backups, version, restart, and recovery. |
| Docs ↗ | Relay documentation | *(link to `/docs` in a new tab: its own page with its own section rail)* |

- **Footer:** **Open Chat** (primary, filled accent), which opens `https://obelisk.ar/app?relay=<this host>`, then the profile card.
- **Removed:** the old "Open Docs" and "Sign out" footer buttons. Docs is now a menu entry, and sign-out lives in the profile card.

### SFU admin (`Console.tsx`, `VIEWS`)

| Label | Description | Blurb |
|---|---|---|
| Overview | Media server health | Live health of the media server: rooms, relay subscriptions and advertising. |
| Access | Who can start calls | Who may start calls — people, follow lists and the test bypass. Changes apply immediately, no restart needed. |
| Settings | Configuration | Saved to runtime.json. Relay changes need a restart; everything else applies live. |
| Test peers | Synthetic callers | Spawn an ffmpeg-driven peer into a voice channel to test media without a second person. |

- **Footer:** the Live / refresh badge, then the profile card.
- **Overview body:** keeps the dynamic `URL · region · engine · uptime` line as its first row.

### Agents manager (`Layout.tsx`, `NAV`)

| Label | Description | Blurb |
|---|---|---|
| Fleet | Your bots | Every bot runs with its own Nostr identity — this is how they look to the world. |
| Operator | AI agent with repo access | Ask an AI agent to build a new bot, tweak one, or investigate a problem. |
| Settings | Fleet-wide defaults | Fleet-wide defaults — changes save automatically. Each bot's own page can override any of this for itself. |
| Docs | Guides and reference | How the fleet works, and how to build and run bots on it. |

- **Footer:** the `agents.obelisk.ar · part of the Obelisk family` line (11px, muted at 60%), then the profile card.
- **Page actions stay in the body, right-aligned:** Fleet's "New bot" and the Settings "saving…" indicator.

### Icons

- **Style:** 24×24 viewBox, `stroke="currentColor"`, stroke-width 2, round caps and joins, `fill="none"`.
- **Relay exception:** the relay's own set is 20×20 at stroke 1.6, in `admin/icons.tsx`.
- **Colour:** inherited, so the active state recolours the icon too.
- **One icon per section,** reused wherever that section appears (for example, the relay's search results and its `/docs` rail).

## Header banner

- Uses the `.admin-header-bar` class:
  ```css
  display: flex; align-items: center; min-height: 112px;   /* 84px below 768px */
  background: linear-gradient(rgba(255,255,255,0.015), rgba(255,255,255,0.015)), #0a0a0a;
  border-bottom: 1px solid #262626;
  ```
  It must stay opaque, because dropdowns (such as the relay's global search) overlap the content beneath it.
- Content: the active section's `label` as `<h1 class="text-2xl font-bold">`, then its `blurb` in `.admin-header-blurb`.
  ```css
  .admin-header-blurb { margin-top: 4px; max-width: 72ch; font-size: 13px; line-height: 19px; color: #a3a3a3; }
  ```
  Optional right-hand tools, such as search, go in the same bar.
- **The title stays fixed through layout, not `position: sticky`.** The shell is `h-screen overflow-hidden`. Main is a flex column: header (`flex-shrink-0`), then scroll region (`flex-1 min-h-0 overflow-y-auto`), then an optional save bar.
  - Sticky inside a container that stretches to its content silently does nothing, because nothing scrolls against it. That bug shipped once in the relay console; the comments in `AdminPanel.tsx` record it.
- **Sub-pages** keep the section's header. For example, `/bots/:name` stays under the "Fleet" header and renders the bot's name as an `h2` in the body.

## Background grid

The scroll region carries `.lc-grid-bg`:

```css
.lc-grid-bg {
  background-image:
    linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}
```

Cards (`lc-card` and the admin settings cards) stay opaque `#171717`, so the grid shows only between them. Keep the grid off the header and the sidebar.

## Profile card

Always bottom-left, and always the last element of the sidebar footer.

```tsx
<div class="lc-identity">
  <Avatar picture={profile?.picture} label={name} size={36} />   {/* round */}
  <div class="min-w-0 flex-1">
    <div class="text-sm font-semibold truncate">{name}</div>
    <div class="text-[11px] text-lc-muted font-mono truncate">{profile?.nip05 ?? shortNpub(pubkey)}</div>
  </div>
  <button class="lc-icon-btn" title="Sign out" onClick={logout}><LogoutIcon /></button>
</div>
```

```css
.lc-identity   { display: flex; align-items: center; gap: 10px; padding: 10px; border-radius: 12px;
                 background: #121212; border: 1px solid #262626; }
.lc-icon-btn   { width: 32px; height: 32px; border-radius: 8px; color: #a3a3a3; }
.lc-icon-btn:hover { color: #fafafa; background: #262626; }
.lc-avatar img, .lc-avatar-mono { object-fit: cover; box-shadow: 0 0 0 3px #171717, 0 4px 16px rgba(0,0,0,.5); }
.lc-avatar-mono { font-weight: 800; color: #0a0a0a; background: linear-gradient(135deg, accent, …); }
```

- **Name:** `display_name || name || fallback`. The fallback is "Admin" on the relay and agents, "Operator" on the SFU.
- **Second line:** the NIP-05 exactly as published, not verified. Without one, it shows a shortened npub, `npub.slice(0, 12) + '…' + npub.slice(-6)`.
- **Avatar:** only `http(s)` picture URLs are loaded, with `referrerpolicy="no-referrer"`. If the picture is missing or fails to load, it shows a two-letter initials monogram.
- **Profile source:** kind 0 (the latest event wins) from public profile relays. The relay and SFU consoles fetch it in the browser; the agents manager fetches it on the server and returns it inside `/api/auth/session`. See [Nostr auth](../security-workflows/nostr-auth.md).
- **Sign-out** does the full logout described in [Operator admin](../security-workflows/operator-admin.md#logout), never just a token clear.

## Mobile (below `lg`, or `md` on the relay)

- **SFU and agents:** the sidebar is hidden. A sticky 56px top bar holds the logo, the avatar and a menu button. The menu button opens a drawer with the same nav and profile card.
- **Section header:** renders under the top bar in normal flow, and the page scrolls as a whole.
- **Relay:** the sidebar becomes a horizontal scrolling tab row above the header.

## Logos and the banner brand block

### Brand block (sidebar banner, top-left)

```tsx
<div class="admin-header-bar px-5">                       {/* same 112px + bottom rule as the page header */}
  <a href="/" class="flex items-center gap-2.5 font-extrabold text-lg">
    <Logo size={32} />
    <span>Obelisk <span class="text-lc-green">SFU</span></span>   {/* product word in accent */}
  </a>
</div>
```

- **Relay:** shows the relay's own NIP-11 `icon` (32×32, radius 7px). It falls back to the stroked `RelayIcon` when the icon is unset or fails to load. The name comes from NIP-11 `name`, with an "Admin console" subtitle. It also sets that icon as the favicon.
- **Mobile top bar:** the same brand element at the same 32px.
- **Login screen:** `<Logo size={56} glow />` above the product name. On mobile it is centred above the card.

### Existing marks

| Product | Mark | File |
|---|---|---|
| Obelisk SFU | A forwarding hub: one ringed node routing to four peers | [`logos/obelisk-sfu.svg`](logos/obelisk-sfu.svg) |
| Obelisk Agents | A bot head: antenna, ears, two lit eyes | [`logos/obelisk-agents.svg`](logos/obelisk-agents.svg) |
| Obelisk Relay | Broadcast waves around a dot, stroked, no tile (`RelayIcon`), or the operator's NIP-11 icon | — |

### Making a logo for a new product

1. **Tile.** 64×64 viewBox with a `<rect width="64" height="64" rx="15">` filled by a diagonal gradient from `#c5ff6e` (top-left) to `#5a8f1f` (bottom-right).
2. **Glyph.**
   - One idea that says what the product *does*, drawn in solid `#0a0a0a`.
   - Use 3.5px strokes and round caps.
   - Keep it inside a roughly 8px safe margin.
   - Accent details, such as the Agents eyes, go in `#b4f953` on the dark glyph.
   - No text and no emoji.
3. **Check it at 16px.** It must still read as a favicon. Merge or drop any detail finer than 2px at 64.
4. **Save it** as `src/assets/logo.svg` in the product and as `design-system/logos/<product>.svg` here.
5. **Add `src/components/Logo.tsx`,** which renders the same drawing inline:

```tsx
import { useId } from 'preact/hooks'

export function Logo({ size = 32, glow = false, class: className = '' }: { size?: number; glow?: boolean; class?: string }) {
  // Per-instance gradient id: the logo is mounted in the (display:none on
  // mobile) sidebar AND the mobile top bar; a url(#id) that resolves into the
  // hidden copy paints nothing and the tile disappears.
  const gid = `obelisk-<product>-logo-${useId()}`
  return (
    <svg viewBox="0 0 64 64" width={size} height={size} aria-hidden="true"
      class={`lc-logo flex-shrink-0 ${glow ? 'lc-logo-glow' : ''} ${className}`}>
      <defs>
        <linearGradient id={gid} x1="0" y1="0" x2="1" y2="1">
          <stop offset="0" stop-color="#c5ff6e" />
          <stop offset="1" stop-color="#5a8f1f" />
        </linearGradient>
      </defs>
      <rect width="64" height="64" rx="15" fill={`url(#${gid})`} />
      {/* glyph */}
    </svg>
  )
}
```

```css
.lc-logo      { display: block; border-radius: 23%; }
.lc-logo-glow { box-shadow: 0 0 40px rgba(180,249,83,0.25); }
```

6. **Favicon** in `index.html`. Vite fingerprints it at build time.
   ```html
   <link rel="icon" type="image/svg+xml" href="/src/assets/logo.svg" />
   <link rel="alternate icon" href="/favicon.ico" type="image/x-icon" />  <!-- if a .ico exists -->
   ```
7. **Replace every old brand mark** (`.lc-brand-mark` with a glyph inside) in the sidebar, the mobile bar and both login-screen positions.

Do not use Unicode glyphs (◉, ⛩) as marks: they render differently on every platform, and were replaced for that reason.

## Theming and retint

- Accent colours go through `--color-accent` and `--color-accent-rgb` where the app defines them (the relay does), or else through the literals `#b4f953`, `#c5ff6e` and `180,249,83`.
- The public relay is shipped **purple**. `obelisk-relay/scripts/retint-branding.sh` rewrites exactly those literals in the built CSS. Any other shade of green survives the retint and shows up green on a purple site.
- Canvas or JS-drawn colour must read the CSS variable at runtime, as `ShootingStars.tsx` does.

## Shipping a shell change

| Repo | Build | Goes live |
|---|---|---|
| obelisk-sfu | `npm run build:admin` (or `npm run build`, which also compiles the server) | Immediately. The server reads `admin-ui/dist` from disk (`cache-control: no-store`), so no restart is needed. `sfu-raise.sh` only builds when `dist/` is *missing*. |
| obelisk-agents | `npm run frontend:build` | Immediately. The manager reads `frontend/dist` per request, and `index.html` is `no-cache`. Restart pm2 `obelisk-agents-manager` only for server changes. |
| obelisk-relay | Docker image (`docker compose build public_relay --build-arg CARGO_BUILD_JOBS=1`) | See the steps below. |

Relay steps:

1. Build the image.
2. Run `scripts/retint-branding.sh <image>`.
3. Update **both sides** of the CSS bind-mount line in `compose.yml` to the new hash.
4. Run `docker compose up -d public_relay`.
5. Confirm `/health`, that the site is still purple, and the follow-graph count in the logs.

Skipping step 2 or 3 silently reverts the site to green; see `obelisk-relay/docs/known-issues.md` §11.

Verify every shell change with screenshots at 1440px and 390px wide. Check: sidebar, header rule alignment, title fixed while scrolling, grid, profile card, logo on both breakpoints.

## Change log

- **2026-09 — shell unification.**
  - SFU and agents took the relay's grey 288px sidebar, two-line nav with 20px icons, the fixed header banner and one-place titles, plus new SVG logos.
  - The relay gained the profile card, the grid background and Docs as a menu entry, and kept Open Chat.
  - Relay sign-out now clears signers and the SDK session as well as the token (see [Admin console auth](../security-workflows/admin-console-auth.md#logout)).

## Checklist for a new console or a shell change

- [ ] Sidebar is 288px and `#171717`, with two-line nav items and 20px icons.
- [ ] The brand block and the header banner are both 112px, and their bottom rules meet.
- [ ] The title stays put while the content scrolls, because the header sits outside the scroll region.
- [ ] `.lc-grid-bg` is on the scroll region only.
- [ ] The profile card is last in the sidebar footer and signs out fully.
- [ ] The SVG logo is inline with a per-instance gradient id, and there is an SVG favicon.
- [ ] Screenshots at 1440px and 390px wide.
