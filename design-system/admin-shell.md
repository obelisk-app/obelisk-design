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

## Logos

Each product has an SVG mark on a green tile: a 64×64 viewBox, `rx=15`, and a `#c5ff6e → #5a8f1f` diagonal gradient, with the glyph in `#0a0a0a` and accent details in `#b4f953`.

| Product | Mark | File |
|---|---|---|
| Obelisk SFU | A forwarding hub: one ringed node routing to four peers | [`logos/obelisk-sfu.svg`](logos/obelisk-sfu.svg) |
| Obelisk Agents | A bot head: antenna, ears, two lit eyes | [`logos/obelisk-agents.svg`](logos/obelisk-agents.svg) |
| Obelisk Relay | Broadcast waves around a dot, stroked, no tile (`RelayIcon` in `admin/icons.tsx`) | — |

Implementation rules:
- **Render inline** as a `Logo` component (`components/Logo.tsx`), so the logo appears with the first paint. Sizes: 32px in the sidebar and top bar, 56px with `.lc-logo-glow` on the login screen.
- **Use a per-instance gradient id** (`useId()`). The logo is mounted twice (the desktop sidebar and the mobile top bar), and a `url(#id)` that resolves into the `display:none` copy paints nothing: the tile disappears on mobile.
- **Favicon:** the same file, `<link rel="icon" type="image/svg+xml" href="/src/assets/logo.svg">`. Vite fingerprints it at build time.
- **Do not use Unicode glyphs** (◉, ⛩) as brand marks. They render differently on every platform.

## Theming and retint

- Accent colours go through `--color-accent` and `--color-accent-rgb` where the app defines them (the relay does), or else through the literals `#b4f953`, `#c5ff6e` and `180,249,83`.
- The public relay is shipped **purple**. `obelisk-relay/scripts/retint-branding.sh` rewrites exactly those literals in the built CSS. Any other shade of green survives the retint and shows up green on a purple site.
- Canvas or JS-drawn colour must read the CSS variable at runtime, as `ShootingStars.tsx` does.

## Checklist for a new console or a shell change

- [ ] Sidebar is 288px and `#171717`, with two-line nav items and 20px icons.
- [ ] The brand block and the header banner are both 112px, and their bottom rules meet.
- [ ] The title stays put while the content scrolls, because the header sits outside the scroll region.
- [ ] `.lc-grid-bg` is on the scroll region only.
- [ ] The profile card is last in the sidebar footer and signs out fully.
- [ ] The SVG logo is inline with a per-instance gradient id, and there is an SVG favicon.
- [ ] Screenshots at 1440px and 390px wide.
