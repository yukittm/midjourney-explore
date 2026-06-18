---
purpose: Single source of truth for all `.claude/PROGRESS.md` rules (entry format, Rule 1, cross-actor boundary). Shared by Claude and Codex.
status: standing
applies-to: any session (Claude or Codex) reading or writing `.claude/PROGRESS.md`
referenced-by:
  - CLAUDE.md §Continuity
  - AGENTS.md §Plan And Track
adoption-history:
  - 2026-06-17: adopted
---

# PROGRESS.md Management — SSoT

`.claude/PROGRESS.md` is the single progress-tracking SSoT for this project. **Both Claude and Codex read and write the same file.** This document is the SSoT for all PROGRESS.md rules; `CLAUDE.md` and `AGENTS.md` hold pointers only.

This is the **mid-weight baseline** (entry format + Rule 1 + cross-actor boundary + immutability). Heavier machinery — slim protocol, session registry, self-archive — is listed in §6 as opt-in for when the project grows (the full reference implementation lives only in the author's monorepo; see the §6 note).

---

## ⚡ Quick Reference (cheat sheet)

Before writing a new entry, confirm these:

1. **Entry format**: `` YYYY-MM-DD [Actor:scope][s:UUID-8] **{emoji} title — status / committed `<hash>`** ``
2. **`[Actor]`**: `Claude` or `Codex` — identifies who wrote the entry (both share one file)
3. **`[s:UUID-8]`**: first 8 hex chars of the current session UUID (`[s:unknown]` if unobservable — never silently omit)
4. **Rule 1**: a `🟢 PASS` entry must cite a commit hash. If not yet committed, write `PENDING_COMMIT` and resolve it before the next entry in the same scope.
5. **Cross-actor boundary**: only touch your own `[Actor:scope]` entries; never edit the other actor's entries.
6. **Past entries are immutable** — show status transitions with a new entry, not by editing the old one.

### §0 Solo simplification

For a solo, single-actor project (only Claude, or only Codex, ever writes this file), you may fix `[Actor:scope]` to a single actor (e.g. `[Claude:setup]`) and **omit `[s:UUID-8]`**. Rule 1 (commit hash on PASS) still applies — it guards against claim-ahead drift even with one actor. Adopt the full `[Actor:scope][s:UUID-8]` form only when Claude and Codex actually run against the same file.

---

## 1. Entry Format

```
YYYY-MM-DD [{Actor}:{scope}][s:{UUID-8}] **{emoji} {title} — {status} / committed `<hash>`**
```

- **Actor**: `Claude` or `Codex`
- **scope**: snake-case discriminator (e.g. `setup`, `feature-x`, `refactor`)
- **UUID-8**: first 8 hex chars of the current session UUID. If unobservable, use `[s:unknown]` (silent omission = format violation).
  - Claude: `echo $CLAUDE_CODE_SESSION_ID | cut -c1-8` (env var; equals the stem of the active `~/.claude/projects/<project>/<uuid>.jsonl`).
  - Codex: the `<uuid>` embedded in the active session file `~/.codex/sessions/YYYY/MM/DD/rollout-<timestamp>-<uuid>.jsonl` (first 8 hex). Note: `~/.codex/sessions/` is Codex's own runtime store, auto-created — it is unrelated to the retired `.codex/PROGRESS.md`.
  - **Solo / single-actor projects may omit `[s:UUID-8]` entirely** (see §0).

### Status emoji
- `🟢` PASS (done; commit hash required = Rule 1)
- `🟡` IN PROGRESS / HOLD
- `🔴` BLOCKED / FAILED

### Body (bullets)
- What was done (concrete file paths / change summary)
- Verification (test result / agent review / scoped diff)
- Boundary (what is out of scope / no-impact declaration)
- Remaining / next step

---

## 2. Rule 1 — PASS claims require a commit hash

```
🟢 ... — PASS / committed `<hash>`     (committed)
🟢 ... — PASS / `PENDING_COMMIT`        (not yet committed, placeholder)
```

- Before writing the **next entry in the same scope**, resolve any prior `PENDING_COMMIT` (edit the placeholder → `<hash>`; this is the allowed exception to immutability §4).
- Adding a new entry while a `PENDING_COMMIT` is unresolved = format violation.
- Effect: prevents claim-ahead drift (declaring PASS without actually committing).

Lint: `grep -nE "🟢 .* — PASS\*\*$" .claude/PROGRESS.md` → hash-less PASS candidates.

---

## 3. Cross-Actor Boundary

Both actors write the same file, so attribution discipline replaces file separation.

- Each entry is owned by its `[Actor:scope]`. Edit only your own entries.
- A Claude session does not edit Codex entries, and vice versa.
- Identify who wrote what via the `[Actor:scope]` prefix; retrieve a session's entries via `[s:UUID-8]`.

---

## 4. Past Entries — immutable

- Once written, an entry is not edited. Exceptions:
  - **Rule 1 retrofit**: `PENDING_COMMIT` → `<hash>`
  - (when the slim protocol §6 is adopted) archiving an entry to another file
- Status transitions (🟡 → 🟢) are shown with a **new entry**; the old entry is left untouched.

---

## 5. Retrieval

| Purpose | Command |
|---|---|
| All entries of a session | `grep -F "[s:UUID-8]" .claude/PROGRESS.md` |
| Latest of a scope | `grep -F "[Actor:scope]" .claude/PROGRESS.md \| tail -1` |
| Rule 1 violations | `grep -nE "🟢 .* — PASS\*\*$" .claude/PROGRESS.md` |

Combine the Rule 1 commit hash with `git show <hash>` to recover the actual change at that point.

---

## 6. Optional — adopt when the project grows

This mid-weight baseline intentionally omits the machinery below. Each item is self-contained enough to adopt from this description; a fuller worked reference exists at `marketing-ops/.claude/protocols/progress-management.md` (present only in the author's `~/Desktop/dev/` monorepo — if that path is absent, the summaries here are sufficient).

**Watch this even on mid-weight** (cheap, no extra files): if `wc -l .claude/PROGRESS.md` grows past ~1500 lines, adopt Rule 2 below.

- **Rule 2 (slim protocol)**: keep the newest N≈10 🟢 PASS entries per scope in `.claude/PROGRESS.md`; move older ones to `.claude/progress-archive/{YYYY-MM-DD}_{Actor}_{scope}.md` (append-only, small frontmatter: `archived-from`, `archive-date`, `scope`). 🟡 / 🔴 entries are never archived. Do the archive-write + source-delete in one atomic commit.
- **Session Identifier Registry / Active Session UUIDs tables**: header tables tracking which scopes and sessions are active — useful under heavy parallel Claude+Codex operation.
- **Session-Hydrate procedure**: a startup routine that checks Rule 1 / Rule 2 before work begins (can be wired to a `.claude/agents/session-hydrate.md` agent).
