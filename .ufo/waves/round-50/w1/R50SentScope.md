VERDICT: defect-found

# R50SentScope — item D-7: sentinel audit of the round's write scope

Seat class EXEC-AUTHORIZED — only the item's commands plus read-only `ls/find/stat/head/grep/git status|diff|show|rev-parse|log|reflog|check-ignore|ls-files` and two throwaway `python3` scanners were run. All scanners ran under `/fast/scratch/hyaku/tsukuroi-r50/R50SentScope/` (removed at exit). Nothing was written in the lane (except this report + receipts dir, per spec), the fleet repo, a sibling lane, `/tmp`, a PATH dir, `~/.omp`, `~/.agents`, or `/home/vgpnk/Projects/shokuknow`. No tools installed. Snapshot: `2026-10-28T16:15`→`16:18` — the wave was live (`w1` grew 57→91 entries during the run), so w1 counts are point-in-time.

## Axes

(a) misroot — untracked fleet-root files naming this lane/round vs other lanes; (b) lane write-scope conformance vs declared scope (lane repo, the report, the L0 file); (c) forbidden-surface integrity; (d) tracked-lane-file mutation by seats. Kept moves that improve one axis without weakening another.

## (a) Fleet root `git status --porcelain` (10 entries; receipt `fleet-status.txt`)

| entry | first lines / evidence | verdict |
|---|---|---|
| `M .scratch/goal-20261028-hyaku-run11.md` | diff adds `## Run log (orchestrator, append-only)` lines (closures 13:15–13:36, routing deviation 15:55) | orchestrator's own run log on a tracked file; not a seat write, not lane/round naming — informational |
| `?? .scratch/closure-mado-r50.json` | `"lane": "mado", "round": 50, "verdict": "rejected-honest-stop"`, Oct 27 06:38 | other lane's work (mado r50, run 10) — never touch |
| `?? .scratch/closure-r54/` | `manifest-entry.json`: `"lane": "tameshi", "round": 54, "admitted": true` | other lane's work — never touch |
| `?? .scratch/kasegi-r44/` | seat dirs `R44Scribe5/…`, `R44Critic5/…` | other lane's live work (kasegi r44) — never touch |
| `?? .scratch/source-routing-queue.md` | "Source-routing queue — operator directives 2026-10-27 (hyaku run 10)" | operator artifact — untouched |
| `?? .ufo/reports/round-50/tsukuroi.md` | "tsukuroi — round 50 (hyaku run 11, attempt 1). L1: TsukuroiR50" | **names this lane/round; it is the declared L0 file** at the conventional path (`.ufo/reports/round-49/tsukuroi.md` is tracked; `.ufo/reports/round-50/<lane>.md` siblings tracked) — in scope, correct location |
| `?? lane3/` | own `.git`, `remote origin url = /home/vgpnk/Projects/shokunin/kengaku-shokunin`, log `297e179 round-50: receipt notes…` | **misroot**: a full sibling-lane clone inside the fleet working tree; names kengaku round-50 work — never touch, but see F-1 |
| `?? o.bin` | Cloudflare "Just a moment..." challenge HTML, 5867 B, Oct 27 16:58 | misrooted fetch dump; no lane/round naming; pre-existing stray |
| `?? oldrep1.out` | census selftest "PASS healthy: all planes pass…", 15314 B, Oct 28 09:10 | tsukuroi-content but pre-round-50 (09:10 ≈ round-48 window; cf. round-48 `ScribeLesson.md:268` at 8029cdba listing it as "other agents'"; `R49SentScopeB/fleet-status.txt:7-9` saw it at 14:45) — see F-2 |
| `?? oldrep2.out` | identical 15314 B, Oct 28 09:11 | same as oldrep1 |

## (b) Lane `git status --porcelain` (4 entries; receipt `lane-status.txt`)

- ` M LOG.md` — `git diff --name-only` = `LOG.md`; `git diff --stat` = 35 insertions, the appended block is `## Round 50 — declaration (2026-10-28, base b866a1d3, freeze 43bcce06, amendment 8029cdba)` — the L1's integrator declaration. In scope (L1-only write surface).
- `?? .ufo/waves/round-50/w1.ready.partial` / `w1.ready.dispatched` — dispatcher bookkeeping, not a seat write: `scripts/hyaku/inline-dispatcher.py:47-48` — "{seat: job id} in `<wave>`.ready.partial and, once full, on the second line of `<wave>`.ready.dispatched". In scope (wave control surface).
- `?? .ufo/waves/round-50/w1/` — the seat report+receipts dir. In scope.
- `?? corpus/lessons/round-50.md` — lane lesson, mtime 15:57, L1-authored (documents the freeze-amendment K-pass corrections and `S256`/`S240` gate rows). Inside the lane repo → in declared scope.
- No other modified/untracked lane path exists; `git status --ignored` shows only pre-existing residue (`.jj`, `.ruff_cache`, old rounds' `__pycache__`).

## (c) Forbidden surfaces (receipt `forbidden-surfaces.txt`)

- `MANIFEST.json` — `git status --porcelain -- MANIFEST.json` empty; `git diff --quiet` rc=0. Untouched. (mtime 15:54 — content matches HEAD.)
- `templates/`, `scripts/` — porcelain empty; dir mtimes Oct 19. Untouched.
- `.ufo/state/` — porcelain empty (only `.gitkeep` tracked). Writes are dispatcher-owned: `inline-dispatcher.log`/`disk-guard.log` (16:14,16:15) and per-lane `tsukuroi.report-baseline|mission|out|round`; writer at `scripts/hyaku/inline-dispatcher.py:66`.
- `.ufo/watchdog.log` — gitignored (`.gitignore:10`), mtime 16:09:50; tail is watchdog launch lines → watchdog-owned. Untouched by seats.
- Sibling repos — `find <all siblings> -iname '*tsukuroi*' -o -iname '*R50*' -newermt today` → empty; sibling `status --porcelain` contains only their own rounds (kaidoku r48, kasegi r43/44, tameshi r56, kama nested `kama-shokunin/`). Receipt `sibling-status.txt`.
- `/home/vgpnk/.omp` — `config.yml` mtime 13:10:10 (predates wave 15:38); other writes today are harness-owned (`blobs/`, `history.db`, `terminal-sessions/`). Untouched by the round.
- `/home/vgpnk/Projects/shokuknow` — no tree file modified today; `.git/` dir mtime 16:00:50 with **no child entry changed** (index Oct 24) → a transient `.git` entry (e.g., `index.lock`) from a read-only git call. Informational: the read-only surface saw a lock event, content intact.

## (d) Seats vs tracked lane files (receipt `seat-inventory.txt`)

- `git -C tsukuroi-shokunin diff --name-only` = `LOG.md` — nothing else; reflog shows only `export from jj` for the integrator's commits (`39e69493`, `8029cdba`, `43bcce06`); `.jj` ops at 15:56:23-25 coincide with L1's `w1.ready` write at 15:56 and predate the first seat artifact (16:02:03, `R50MutCounterC/`).
- Seat report count at end of run: **41 `.md` reports** (of 71 dispatched; dispatcher shows `tsukuroi/w1: live 43/71` at 16:14:38). Every `w1/` entry — md file or receipt dir — names a dispatch seat exactly (0 foreign names, 0 loose files at `w1/` root; receipt `seat-inventory.txt` "not matching dispatch: []").
- Seat scratch root `/fast/scratch/hyaku/tsukuroi-r50/` contains only `R50*` seat dirs plus L1-owned `controls|l1|plan.json` (receipt `perimeter.txt`); `/tmp` holds no `R50`/`round-50` entries — `/tmp/closure-tsukuroi-r49.json` (15:36) and older selftest dirs predate the wave (observed, not written).
- **Nothing unexpected**: no seat wrote a tracked lane file, a fleet tracked file, a sibling, or a misrooted path.

## Findings

- **F-1 (medium, misroot, other lane's — never touch): `lane3/`** is a full clone of `kengaku-shokunin` sitting untracked inside the fleet working tree (`.git/config` remote url; log `297e179 round-50…`). Exploit/risk path: a `git add -A`/commit at the fleet root would record a foreign gitlink (corrupting fleet content), and any fleet-wide status/diff audit miscounts a sibling repo as fleet residue. Smallest remediation: move it under `/fast/scratch/hyaku/kengaku-r50/` (owner: kengaku L1 or orchestrator), or delete if disposable.
- **F-2 (low, misroot, pre-existing): `o.bin`, `oldrep1.out`, `oldrep2.out`** at fleet root — fetch/selftest dumps unattributed since ≤ round 48 (`ScribeLesson.md:268` at 8029cdba lists them as "other agents'"; `R49SentScopeB` re-flagged them at 14:45). They persist across rounds; the fleet root accumulates strays that future audits must keep re-classifying. Smallest remediation: sweep to `/fast/scratch/` or delete (orchestrator).
- **F-3 (info): fleet-root `.scratch/` holds other lanes' scratch** (mado r50 closure JSON, tameshi r54 work, kasegi r44 seats) and the tracked goal file carries an orchestrator append — expected surfaces, not this round's concern; listed only to bound the audit.
- **F-4 (info): shokuknow `.git/` transient entry at 16:00:50** (lock-file class event from a git read; index and content untouched).
- **F-5 (info): `kama-shokunin/kama-shokunin/`** nested untracked dir inside a sibling — same misroot class as F-1, observed only (other lane's surface).

Verdict basis: the round itself is clean on all four axes — no seat wrote out of scope (b, d), all forbidden surfaces untouched (c), the only round-50/tsukuroi-named untracked fleet file is the declared L0 report (a). The defect-found grade reflects F-1's live foreign-repo misroot in the fleet working tree (existing condition this round still permits), not a round-50 seat violation.

Receipts: `.ufo/waves/round-50/w1/R50SentScope/` — `fleet-status.txt`, `lane-status.txt`, `sibling-status.txt`, `untracked-heads.txt`, `forbidden-surfaces.txt`, `seat-inventory.txt`, `perimeter.txt`.
