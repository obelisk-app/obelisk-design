# Nostr Links

Every link an Obelisk surface shows for a Nostr thing (a person, a note, a hashtag) points at the hosted Obelisk client, **never** at njump.me, primal.net or another third party. That keeps the reader and the link preview inside the project, and gives someone who has never used Nostr a page that opens in a browser.

The routes are implemented in `obelisk-dex` (`src/app/[locale]/p/[id]`, `notes/[id]`, `t/[tag]`). The canonical builders are in `obelisk-dex/src/services/social/note-links.ts`. Mirror them; don't invent new shapes.

## Routes

| What | URL | Identifier |
| --- | --- | --- |
| Profile | `https://obelisk.ar/p/<id>` | `nprofile1…` (preferred) or `npub1…` |
| Note / article | `https://obelisk.ar/notes/<id>` | `nevent1…` / `naddr1…` (preferred), `note1…`, 64-char hex |
| Hashtag | `https://obelisk.ar/t/<tag>` | lowercase tag, URL-encoded |
| Group message | `https://obelisk.ar/app?c=<groupId>&m=<eventId>&relay=<host>` | NIP-29 deep link into the app |

- Both pages render on the server, with OpenGraph metadata, so a pasted link previews with the person's or the note's name, picture and text. They are `noindex, follow`.
- A `nostr:` prefix is accepted and stripped.
- Locale prefixes are optional: `/es/p/…` and `/pt/p/…` work, and unprefixed URLs are English. Build links without a locale.
- **Don't put bare hex under `/p/`.** A 64-char hex is parsed as an *event* id, so `/p/<hex>` is a 404. Encode the pubkey as npub or nprofile first.

## Profiles: npub vs nprofile

Use an **nprofile** when you know where the person publishes, and an npub otherwise. This is the same as `profileUrl(pubkey, relays)` in obelisk-dex:

```ts
import { nip19 } from 'nostr-tools'

export function obeliskProfileUrl(pubkey: string, relays: string[] = []): string {
  const id = relays.length
    ? nip19.nprofileEncode({ pubkey, relays: relays.slice(0, 3) })
    : nip19.npubEncode(pubkey)
  return `https://obelisk.ar/p/${id}`
}
```

Rules for relay hints (`safeRelayHints` in `obelisk-dex/src/services/social/identifier.ts`):

- **At most 3.** Extra hints are dropped.
- **Public `wss://` URLs only.** Hints come from a user-supplied link, so the server rejects `ws://`, localhost and private-network hosts; that stops a crafted link from aiming the server at its own network. Never put an internal relay URL in a link.
- Hints are added *in front of* the viewer's default relays, not used instead of them.

**Current limitation:** the server-side profile page fetches kind 0 from its fixed public set only: `relay.damus.io`, `nos.lol`, `relay.primal.net`, `relay.nostr.band` and `purplepag.es` (`fetchAuthorForViewer` passes no hints). A profile that exists only on a whitelisted or NIP-42-gated relay (for example `public.obelisk.ar`) shows "profile not found", even with a correct nprofile. **Anything we want people to look up, including our bots, must publish its kind 0 to those public relays.** Keep the nprofile hints anyway: they cost nothing, other Nostr clients use them, and the page will use them once the viewer passes them through.

## Notes

- Prefer `nevent` with `author`, `kind` and relay hints; a bare `note1` or hex only finds notes that have spread to the public relays.
- For a **NIP-29 group event**, the relay hint is required: the event exists on the group's relay and very likely nowhere else. obelisk-relay's console does this in `frontend/src/utils/obelisk-links.ts` (`noteUrl` always hints its own relay).
- Addressable kinds (30000–39999, such as long-form articles) use `naddr`, so the link follows edits instead of freezing one revision.
- To send the reader back into the conversation, link the group view (`/app?c=&m=&relay=`) as well. `groupNoteUrl` in obelisk-dex builds it.

## Where these links live today

| Surface | Code |
| --- | --- |
| obelisk-dex (share menus, viewers) | `src/services/social/note-links.ts` |
| obelisk-relay console | `frontend/src/utils/obelisk-links.ts` |
| obelisk-agents manager ("view on Nostr" on a bot) | `frontend/src/components/BotDetail.tsx`: nprofile with the bot's own relays |
| blossom-server admin (user detail) | `src/admin/user-detail-page.tsx` |

Self-hosted deployments still link to `https://obelisk.ar`, not to their own origin. A relay or agents console isn't a note viewer, so the reader has to land somewhere that can render one.

## Checklist for a new link

- [ ] Points at `https://obelisk.ar/{p,notes,t}/…`, not a third-party gateway.
- [ ] Profiles: an nprofile when relays are known, otherwise an npub. Never bare hex.
- [ ] Notes: nevent/naddr with relay hints. Group events always hint the group's relay.
- [ ] At most 3 hints, public `wss://` only.
- [ ] Opens in a new tab with `rel="noreferrer"` (or `noopener noreferrer`) from admin consoles.
