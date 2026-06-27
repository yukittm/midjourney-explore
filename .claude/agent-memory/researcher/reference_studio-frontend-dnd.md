---
name: studio-frontend-dnd
description: Studio tool (automation/studio/static/index.html) front-end — current drag impl, SortableJS recommendation for FLIP reorder, no-build direction
metadata:
  type: reference
---

The IG studio tool is a single static `automation/studio/static/index.html` (inline CSS+JS, vanilla) served by Python stdlib `http.server`. No build step, no npm. May run offline (localhost) → vendor libs as one file into `static/vendor/`.

**Grid drag (as of 2026-06):** hand-rolled pointer-drag in `makeDraggable()` (~line 181). A fixed-position full-opacity ghost clone follows the cursor; on hover it `insertBefore`s the card to reflow — but tiles JUMP (no animation / no smooth gap-opening). Only `.card.sel` tiles get `makeDraggable`; locked/published tiles (`.live`/upcoming) are non-draggable already. onUp collects `[...grid.querySelectorAll(".card.sel")].map(c=>c.dataset.key)` and POSTs `/api/order`.

**Recommended FLIP reorder lib: SortableJS** (v1.15.7, MIT, ~45KB min / ~12KB gzip; single UMD `Sortable.min.js` vendorable offline; actively maintained, releases through Feb 2026). `animation:150` gives the iOS "items shift out of the way" effect for free. Lock non-sel tiles with `filter:'.card:not(.sel)'`; constrain drops so a sel can't land among locked tiles via `onMove(evt){ return evt.related.classList.contains('sel'); }`. Read new order with `sortable.toArray()` (set `dataIdAttr:'data-key'`) inside `onEnd`. Touch: set `delayOnTouchOnly:true, delay:120` if needed. Alternatives rejected: Muuri (stale, v0.9.5, archived-ish), pragmatic-drag-and-drop (no built-in shift anim, multi-package, build-oriented), View Transitions API (snapshot-based, not for live drag).

**Front-end direction:** stay no-build vanilla + targeted vendored libs (SortableJS now; Alpine.js ~15KB if reactive state grows). Avoid React/Svelte+Vite — a build pipeline contradicts the stdlib-served / offline / single-operator constraints. Web Components/lit only if a reusable component system is genuinely needed later.
