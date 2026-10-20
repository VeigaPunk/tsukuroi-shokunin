# JjDocSweep — jj findings × tsukuroi HEAD-as-revision (R17)

Sources read in full: `.ufo/waves/hyaku/jj-w1/reports/JjAuditTsukuroi.md`,
`JjTrialTsukuroi.md`; `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh`
(702 ln, current). Baseline `6923fe0`: HEAD attached, `master = origin/master`.
Tool anchors below verified with `git show HEAD:<path>`; the audit's table drifts
from HEAD by +1 on its `show`/resolve lines and +3/+4 on its wrapper lines (e.g.
locator wrapper `443` = HEAD `439`) — do not mix the two.

In flight [obs]: all five tools are ` M`; `tools/check-revision-binding.py` and
`tools/check-seat-scope.py` are untracked. Worktree now rejects HEAD in 4/5
(locator:35, root-dac:32, section:61, source-scope:27); `measure-update-recheck.py:45`
still `HEAD|[0-9a-fA-F]{4,64}`.

## 1. Findings routed to tsukuroi

Sev: report-graded where stated, else `[inf]`. Owner L = lane repo (writable);
F = fleet helper `scripts/hyaku/jj-lane.sh` (report-only from this lane).

| id | sev | anchor | disposition / fix | owner |
|---|---|---|---|---|
| JJ-R1 | high | locator:30,464,475; root-dac:27,242,352; section:55,420,432; source-scope:26,376,506; measure:38,434,476; SKILL.md:1818,1819 | HEAD resolves to `@-` (= previous commit), so a gate PASS can certify bytes the worktree no longer has. Fix: hex-only REV, drop HEAD from grammar/help/docs; pre-commit = worktree mode, post-commit = landed hex | L |
| JJ-R2 | high [inf] | same resolve sites; section BASE `db68e62` (:36) at :756 | No `merge-base --is-ancestor`/`show-ref` anywhere, so abandoned, unpushed and `@` objects all verify. Fix: bind to `refs/heads/<branch>` then `refs/remotes/origin/<branch>`; `E-REVISION-NOT-LANDED`/`-NOT-PUSHED`, exit 2 | L |
| JJ-R3 | latent | lane `.git/hooks` 14 × `*.sample`, 0 active; no `.gitattributes` | jj runs no git hooks and no attribute filters; nothing bypassed today. Decide: helper enforcement, or a lane policy note before any hook/attr is added | F |
| JJ-S1 | none | audit R1 evidence (conflicted id absent from git) | Already loud: cite fails `E-REVISION-INVALID`. No fix | — |
| JJ-S2 | med [inf] | REV grammar (5 files above) | `--revision master` rejected by design; tip nameable only by hash, which pressures HEAD use. Keep hex-only; document that JSON `branch_tip` is the citable tip | L |
| JJ-S3 | none | `jj commit` empties the git index | No index reader in the lane (class C = 0). No action | — |
| JJ-S4 | low [inf] | `@` is a real git object, non-ancestor, moving | Doc: never cite `@`; binding turns it into NOT-LANDED | L |
| JJ-S5 | med [inf] | measure:443 `read_git`→`None`→`ABSENT` rc 0; the four gates map `None`→`*-MISSING` FAIL | Align the probe's missing-path semantics or state the asymmetry in SKILL | L |
| JJ-S6 | low | HEAD root-dac:226 `git()` had no timeout | Already fixed in worktree: `GIT_TIMEOUT=30` :234, `E-GIT-TIMEOUT` :243; peers have `timeout=30` (locator:459, section:410, source:358, measure:427) | L (in flight) |
| JJ-S7 | latent | all five use `git -C ROOT` → root `.git` | Non-colocated `jj git init` leaves no `.git`; document colocate-only, or read `.jj/repo/store/git` | L |
| JJ-S8 | ungraded | section BASE `db68e62` (:36), resolved in `main()` with no ancestry check | Contract binds `--revision` only; bind BASE too, or a rewritten history still resolves as a dangling object | L |
| JJ-RES | doc | SKILL.md:624,862 worktree `md5sum` identity vs SKILL.md:1592 `git show af8adf1:` | State the convention (worktree vs blob); under jj the two diverge after any edit | L |
| JT-H1 | med [inf] | `.ufo/interactive-sessions/**.jsonl` 1,886,589 B > 1 MiB cap; `--include-ignored` at helper :551 | Add `.ufo/interactive-sessions/` to the helper denylist. Not re-measured here | F |
| JT-H2/H4/H5/H7 | none | intent-to-add killed by `none()` (:68); index reset irrelevant; author fixed by `metaedit`; no symlinks/LFS/nested git | No action | — |
| JT-H3 | doc | after first helper commit HEAD is detached, `@{u}` fails | Lane tools pass explicit revs and do not break; docs must stop equating HEAD with the branch tip | L |
| JT-H6 | stale | lock keyed on `basename` | Already fixed: `lane_realdir` + `take_lock` key on the physical path (helper :74-90, :132-140, :365) | — |
| JT-REC1 | stale | "cite `pushed`, never `committed`" | Current helper prints only `landed <hash>` (:22, :58, :243, :249); lane convention = cite `landed` | L |
| JT-REC2 | none | "adopt `jj-lane.sh` as-is; no lane config or `.gitignore` change" | Accepted; lane keeps tracking `.ufo/interactive-sessions/` as ignored. Canonical-absolute-path caveat is already enforced by `lane_realdir` | — |

## 2. Lane doc locations encoding HEAD-as-revision

### 2a Operative (grammar or re-runnable command)

| path:line | content |
|---|---|
| SKILL.md:1818, 1819 | `REV = HEAD or 4–64 hex` for locator-clarification / measure-update-recheck — now contradicts the worktree tools |
| SKILL.md:1737, 1778, 1857 | `--revision <commit>` entry commands (hex-compatible; omit the landed/pushed requirement). 1857 says `<commit>`, not HEAD — the audit's HEAD claim holds only for 1818-1819 |
| SKILL.md:1826 | `revision: worktree`; "a comparable verdict names a commit via `--revision`" |
| plans/completion-evidence.md:39, 142 | "worktree == `git show HEAD:` blob"; runnable `git show HEAD:… \| md5sum` must equal the worktree |
| plans/round-10.plan.md:8, 229 | "re-hashed here against `git show HEAD:`"; "freeze revision = HEAD blob" |
| plans/round-11.plan.md:255 | "Census (HEAD blob, re-hashed)" |
| plans/round-8.plan.md:168 | "(HEAD revision) md5 …" |
| plans/round-9.plan.md:194 | "(HEAD revision) md5 …" |
| plans/round-5-record-draft.md:41, 147, 158 | "= HEAD bytes"; "worktree = HEAD bytes"; "committed HEAD bytes" |

### 2b HEAD as historical state label (hash adjacent; inert, but asserts HEAD was the tip)

`SKILL.md:866, 1009` · `LOG.md:113, 243, 253, 383, 413, 423, 529` · `PROVINCE.md:83` ·
`plans/round-4-record-draft.md:91` · `round-5-record-draft.md:38, 144, 445` ·
`round-6-record-draft.md:20` · `round-7-record-draft.md:19` ·
`round-8-record-draft.md:23` · `round-9-record-draft.md:26` ·
`round-10-record-draft.md:30, 150, 569` · `round-8.plan.md:4` · `round-9.plan.md:4` ·
`round-10.plan.md:4, 7` · `round-11.plan.md:4, 87, 149, 158, 192, 250` ·
`completion-evidence.md:21, 32, 82, 103, 104`.

### 2c Adjacent surface (no HEAD token, same grammar)

`SCORECARD.md:306, 325, 370, 389, 423, 424, 493` — `--revision <commit>` counting
commands. `corpus/`, `reports/`, `.ufo/` carry further HEAD prose; none is a gate
entry command.

## 3. Contract coverage

**Fixes.** JJ-R1: HEAD becomes `E-REVISION-INVALID`, so `@-` is unreachable —
but SKILL.md:1818/1819 must move in the same landing or the docs document a
rejected form. JJ-R2: landed + pushed ancestry with distinct exit-2 ids closes
abandoned, unpushed and `@` objects. JJ-S4 in effect.

**Partial.** JJ-S2: refs stay rejected; `branch_tip` in JSON supplies the hex.
JJ-R1's core harm survives one step — any *landed* ancestor hex still passes, so
a stale hash can certify old bytes. The contract proves landed, not tip/current.

**Not fixed.** JJ-S1 (already loud), JJ-S5, JJ-S7, JJ-S8 (internal BASE), JJ-R3,
JJ-RES, JT-H1; JJ-S6 fixed separately in the worktree; JT-H6 already fixed;
JT-REC1 is wording only.

**Consequence.** `check-section-citations.py` has no worktree mode (the
`revision = "worktree"` default is overwritten before use; CLI requires
`--revision` or `--selftest`). With HEAD rejected, its only non-selftest path is
post-landing. Accept and document, or add tree mode.

**Count risk.** `check-revision-binding.py` (untracked) demands all three
behaviours from all five tools; `measure-update-recheck.py` still admits HEAD at
read time, so 5/5 is not yet reachable.

Scope: executed=grep,sed,cut,sort,uniq,head,ls,wc,git show,git rev-parse,git symbolic-ref,git merge-base --is-ancestor,git status,git ls-files,git check-ignore
