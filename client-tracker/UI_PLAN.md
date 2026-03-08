# Ping — UI/UX Plan

> A lightweight client request tracker. Tasks come in from WhatsApp, you triage them here.

---

## Branding

**Name:** Ping

Short, memorable, implies a notification arriving. "You got pinged by a client."

**Colors:**

| Role | Value | Usage |
|------|-------|-------|
| Primary | `#2563EB` (Blue 600) | Action buttons, active states, links |
| Accent | `#F59E0B` (Amber 500) | Badges, warnings, "In Progress" state |
| Success | `#10B981` (Emerald 500) | "Done" state, completion indicators |
| Background | `#FAFAFA` | Page bg |
| Surface | `#FFFFFF` | Cards |
| Text | `#1E293B` / `#64748B` | Primary / secondary text |
| Border | `#E2E8F0` | Dividers, card borders |

Why these: Blue is trust/professional without being boring. Amber for active work creates urgency. Green for done is universal. No gradients, no dark theme (v1).

**Typography:** Inter. Clean, excellent on mobile, free. One font, three weights: 400 (body), 500 (labels), 600 (headings).

**Corner radius:** 12px cards, 8px buttons, 20px pills/badges.

---

## Mobile — The Main Event

Commander uses this on his phone 90% of the time. Everything is designed thumb-first.

### Screen 1: Task List (Home)

Opens here. Always.

**Top bar:**
- Left: "Ping" wordmark (small, not a logo parade)
- Right: tiny summary chip → `4 open` in muted text. Tapping it goes to Stats screen.

**Filter bar** (horizontally scrollable pills, directly below top bar):
- `All` · `Pending` · `In Progress` · `Done` · `Bugs` · `Features`
- Active pill gets filled blue bg, rest are outlined
- Sticky on scroll

**Task cards** (vertically stacked, full width minus 16px padding each side):

```
┌─────────────────────────────────┐
│  🔴 Bug                  2h ago │
│  Login page crashes on Safari   │
│  Rahul • screenshot attached 📎 │
│                                 │
│  ┌──────────┐                   │
│  │ Pending ▾│                   │
│  └──────────┘                   │
└─────────────────────────────────┘
```

Each card shows:
- **Category badge** top-left: red dot + "Bug" or blue dot + "Feature"
- **Time** top-right: relative ("2h ago", "Yesterday")
- **Title** — the one-liner extracted from the transcript. Bold, 16px, max 2 lines.
- **Client name** — who sent it. Muted text.
- **Attachment indicator** — 📎 if there's media
- **Status dropdown button** — bottom-left of card. This is THE interaction.

**The status button is a chunky, tappable dropdown.** Not a swipe gesture (too easy to trigger accidentally), not a long press (too hidden). A visible button with the current status as label and a tiny chevron. One tap opens a bottom sheet with three options:

```
─────────────────────
  Change Status
─────────────────────
  ○ Pending
  ● In Progress  ✓
  ○ Done
─────────────────────
  [Cancel]
```

Selecting a new status: card briefly flashes the new status color, bottom sheet closes, toast appears: "Moved to In Progress · WhatsApp notified ✓" (auto-dismiss 2s).

**Why a bottom sheet, not inline?** Because fat fingers. A bottom sheet gives big tap targets. And it confirms the action visually before dismissing.

**Empty state:** When all tasks are done (rare but possible): centered illustration-free message — "Nothing open. Enjoy the silence." with a muted emoji ☕

**Pull to refresh.** Standard. Syncs with backend.

**Sort:** Tasks sorted by newest first. No sort options in v1 — keep it simple.

### Screen 2: Task Detail

Tapping a card opens this. Full screen, slides in from right.

**Layout (top to bottom):**

1. **Back arrow** + "Task Detail" header
2. **Status button** (same dropdown style as list, but larger here)
3. **Title** — full text, large (20px semi-bold)
4. **Meta row:** `Rahul · Bug · Mar 7, 2025 · 3:42 PM`
5. **Divider**
6. **Transcript section:**
   - Header: "Original Message"
   - The raw transcript from WhatsApp, in a slightly indented block with a left blue border (like a blockquote)
   - If from audio: small "🎙 Transcribed from voice note" label above
7. **Attachments section** (if any):
   - Header: "Attachments"
   - Image thumbnails in a horizontal scroll. Tap to fullscreen.
   - Files shown as download chips.
8. **Activity log** (bottom):
   - "Created · Mar 7"
   - "Status → In Progress · Mar 7 · 5:10 PM"
   - "Status → Done · Mar 8 · 10:00 AM"
   - Minimal, muted, small text. Just a paper trail.

No edit button. No comments. Commander doesn't write here — he reads and changes status. That's it.

### Screen 3: Stats (Optional, accessed from top-right chip)

Simple summary. Not a dashboard — a glance.

**Layout:**

Three big number cards at top:
```
┌────────┐ ┌────────┐ ┌────────┐
│   4    │ │   2    │ │   8    │
│ Open   │ │ Today  │ │ Done   │
│        │ │        │ │ this wk│
└────────┘ └────────┘ └────────┘
```

Below: simple breakdown
```
Bugs:     ███████░░░  7
Features: █████░░░░░  5
```

Below that: "Busiest client: Rahul (6 tasks)" — just a fun stat.

No charts. No graphs. Numbers only.

---

## Desktop — Secondary View

For when Commander opens it on laptop. Same data, more space.

**Layout:**

```
┌──────────────┬──────────────────────────────────────┐
│              │                                      │
│   Filters    │   Task List                          │
│              │                                      │
│   All  (12)  │   ┌─────────────────────────────┐    │
│   Pending (4)│   │ Login crash · Rahul · Bug    │    │
│   In Prog (2)│   │ Pending ▾        2h ago      │    │
│   Done  (6)  │   ├─────────────────────────────┤    │
│              │   │ Add dark mode · Priya · Feat  │    │
│   ────────   │   │ In Progress ▾    Yesterday   │    │
│   Bugs  (7)  │   ├─────────────────────────────┤    │
│   Features(5)│   │ ...                          │    │
│              │   └─────────────────────────────┘    │
│              │                                      │
│   ────────   │                                      │
│   Stats ↗    │                                      │
│              │                                      │
└──────────────┴──────────────────────────────────────┘
```

- **Left sidebar** (240px): Filter list with counts. Click to filter. Active filter highlighted.
- **Main area**: Cards in a single-column list (not a table — keeps consistency with mobile). Cards are wider, showing more info inline.
- **Click a card**: Detail panel slides in from right as a side panel (doesn't replace the list). Two-pane: list + detail visible simultaneously.
- **Status dropdown**: Same interaction, but opens as a regular dropdown instead of bottom sheet.
- **Keyboard shortcut** (nice-to-have): `1/2/3` to change status when a task is selected.

No table view. Cards everywhere. Consistency > density.

---

## Interaction Design

### Status Change (the core action)

This is the #1 thing Commander does. Must be effortless.

**Mobile:** Tap status button on card → bottom sheet appears → tap new status → done. Two taps total. Bottom sheet has big 48px-tall rows. Hard to mis-tap.

**Confirmation:** None. Status changes are instant and reversible. The toast shows "WhatsApp notified ✓" so Commander knows it went through. If he tapped wrong, he taps again to change it back.

**Visual feedback:**
- Status badge color changes immediately (gray → amber → green)
- Subtle scale animation on the badge (100% → 105% → 100%, 200ms)
- Toast slides up from bottom

### Filters

**Mobile:** Horizontal pill bar. Tap to select. Only one active at a time. "All" is default. Switching filters: task list cross-fades (150ms opacity transition). No fancy animation — just fast.

**Desktop:** Sidebar click. Same behavior.

### Transitions

- **List → Detail (mobile):** Slide from right, 250ms ease-out
- **Detail → List:** Slide back left
- **Bottom sheet:** Slides up from bottom, 200ms, with a dim overlay behind
- **Card appearance on filter change:** Fade in, staggered 50ms per card (max 5 cards animated, rest appear instantly)
- **Pull to refresh:** Standard iOS/Android native feel

### Haptics (mobile)

- Status change: light tap feedback
- Pull to refresh: standard

---

## What This Should Feel Like

**Things 3** — The calm, minimal aesthetic. White space. Tasks feel manageable, not overwhelming. Status is visual and obvious.

**Linear (mobile app)** — The filter pills, the card density, the speed. Everything loads instantly and feels native.

**Apple Reminders** — The simplicity. No feature creep. You open it, you see your stuff, you act on it, you leave.

Not Jira. Not Notion. Not a "platform." A tool that gets out of the way.

---

## What We're NOT Building (v1)

- No dark mode
- No user accounts / auth (single user: Commander)
- No drag-and-drop reordering
- No comments or notes
- No due dates or priorities
- No notifications inside the app (WhatsApp IS the notification layer)
- No kanban board view
- No search (filter is enough for <50 tasks)

Keep it tight. Ship it. Add later if needed.

---

## Technical Notes for Bolt

- Single-page app, client-side routing
- Three routes: `/` (list), `/task/:id` (detail), `/stats` (summary)
- Mobile breakpoint: <768px
- Use CSS variables for the color tokens above
- Status dropdown: Headless UI or Radix popover on desktop, custom bottom sheet on mobile
- Animations: CSS transitions only, no animation library
- Font: `Inter` via Google Fonts, subset latin

---

*Plan by Flare · March 2025*
