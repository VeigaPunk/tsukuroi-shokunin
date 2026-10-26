VERDICT: supports

# GateHeaderRecheck — item G-1, lane gates at master and base

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (read-only; `git status --porcelain` shows 0 tracked-dirty lines after every run).
master = `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` (`git rev-parse master`), base = `8bd001f58bfda29c92d90d2a7a413825c0ca9fcb`.
Every run used `TMPDIR=/fast/scratch/hyaku/tsukuroi-r38/GateHeaderRecheck`. No package, service, sysfs, `/etc`, hook or repo mutation; no `pacman`; no tool install was needed.

## 1. CLI (learned first, as the item asks)

`python3 tools/check-knowledge-header.py --help` → `usage: check-knowledge-header.py [-h] (--revision REV | --selftest) [--lane REPO] [--branch BRANCH]`, "required: 7-64 hex commit; HEAD/@/refs are rejected" (exit 0).
`python3 tools/check-recheck-commands.py --help` → `usage: check-recheck-commands.py [-h] (--revision REV | --selftest) [--paths PATH [PATH ...]] [--exec-log PATH] [--branch BRANCH] [--forbid LIST]`, default paths `corpus/knowledge`, `--branch` default `master` (exit 0).

## 2. Both gates at both revisions — all green, exit 0

| gate | revision | exit | summary (verbatim JSON fields) |
|---|---|---|---|
| check-knowledge-header | `5edb6c2` (master) | 0 | `status=PASS note_count=59 complete_count=59 clean_count=59 finding_count=0 findings=[]` |
| check-knowledge-header | `8bd001f` (base) | 0 | `status=PASS note_count=58 complete_count=58 clean_count=58 finding_count=0 findings=[]` |
| check-recheck-commands | `5edb6c2` (master) | 0 | `status=PASS file_count=59 clean_count=43 finding_count=0 invocation_count=81 pointer_section_count=42 resolved_count=16 flagged_count=0` |
| check-recheck-commands | `8bd001f` (base) | 0 | `status=PASS file_count=58 clean_count=42 finding_count=0 invocation_count=81 pointer_section_count=42 resolved_count=16 flagged_count=0` |

Receipts: `w1/GateHeaderRecheck/kh-master.txt`, `kh-base.txt`, `rc-master.txt`, `rc-base.txt`.

**No red at master that was green at base.** The round added exactly one knowledge entry and it is clean at master: master's `notes[]` contains `{"path": "corpus/knowledge/pacman-hook-order-r38.md", "lines": {"recheck": 3, "source": 1, "verified-at": 2}, "problems": []}` (`kh-master.txt`), and base's `notes[]` has no `r38` path at all — the same gate run at base resolves 58 notes with the file absent, so the gate is genuinely revision-scoped (`notes_at` / `read_blob`, `tools/check-knowledge-header.py:139-152`), not worktree-reading.

Delta master − base, both gates: +1 file, +1 clean, findings 0 → 0, flagged 0 → 0; `invocation_count`, `pointer_section_count`, `resolved_count` unchanged. `git diff --name-status base master -- corpus/knowledge corpus/SOURCES.md SCORECARD.md` → `M SCORECARD.md`, `M corpus/SOURCES.md`, `A corpus/knowledge/pacman-hook-order-r38.md` (only one knowledge file added; the two modified files are outside both gates' scope).

The recheck gate was also run scoped to the new note: `--paths corpus/knowledge/pacman-hook-order-r38.md` at master → `status=PASS file_count=1 clean_count=1 flagged_count=0`, exit 0 (`rc-master-scoped-r38note.json`). Note the new note's `recheck:` text names "pacman" in prose ("on-release of pacman for S208–S211", `corpus/knowledge/pacman-hook-order-r38.md:3`) and is not flagged: the gate's forbidden-invocation rule is command-position aware, not a bare word match — confirmed by the M3 control below, which is flagged at the same line shape when the token is an actual command.

## 3. The green is not the round weakening its own gates

`git diff --stat base master -- tools/check-knowledge-header.py tools/check-recheck-commands.py` is empty, and `git show <rev>:tools/<gate>.py | sha256sum` gives the identical digests at both revisions:
`592b6c2e765e2a0aec94cc745271878ef748ef3a2e2303ec722828d7cc13f919` (check-knowledge-header), `1c6f349d4c298a3867c7163c7c3fb32f1c768adb0df7110fc7b216a4656b8cd1` (check-recheck-commands). Both selftests pass: `{"cases": 25, "failures": [], "passed": 25, "status": "PASS"}`, `{"cases": 95, "failures": [], "passed": 95, "status": "PASS"}`, exit 0 each (`kh-selftest.txt`, `rc-selftest.txt`).

## 4. Green is not vacuous — mutant controls

Scratch clone of the lane (`git clone -q --shared`, `origin` removed, fixture identity only inside it), four mutants derived from `corpus/knowledge/pacman-hook-order-r38.md`, committed at `c005eec` / `4f7b7b7` / `c04b415`; the clone was under `/fast/scratch/hyaku/tsukuroi-r38/GateHeaderRecheck/fx.jHZts2` and has been deleted:

- `zz-m1-noverified.md` (`verified-at:` line removed) → `KNOWLEDGE-HEADER-MISSING`, exit 1.
- `zz-m2-baddate.md` (`verified-at: 2026-02-30`) → `KNOWLEDGE-HEADER-VALUE: ISO date is not a calendar date at line 2`, exit 1.
- `zz-m4-emptyrecheck.md` (`recheck:` with no procedure) → `KNOWLEDGE-HEADER-VALUE: recheck: carries no ISO date, no <N>d cadence and no on-release at line 3` at kh; `E-RECHECK-EMPTY` (CANNOT_EVALUATE, exit 2, first failure wins) at rc.
- `zz-m3-forbidden.md` (`recheck:` line naming `sudo pacman -Syu`) → `RECHECK-FORBIDDEN-INVOCATION: recheck procedure invokes pacman` at `corpus/knowledge/zz-m3-forbidden.md:3`, exit 1, `flagged_count=1`.
- `--exec-log` control, log line `$ pacman -Syu --noconfirm` → additionally `EXEC-STEER-VIOLATION: executed command invokes pacman` at `.ufo/exec-log-fixture.txt:1`, exit 1.

Receipts: `mutant-kh.json`, `mutant-rc.json`, `mutant-rc-execlog.json`. Both gates therefore fail on exactly the defects item G-1 worries about, so the PASS at `5edb6c2` is a measured result.

## 5. Gate health along the round (same two gates, same TMPDIR)

| revision | check-knowledge-header | check-recheck-commands |
|---|---|---|
| `7cbaeb6` freeze | PASS 58/58/58, findings 0 | PASS files 58, clean 42, flagged 0 |
| `52ffd65` C1 impl | PASS 58/58/58, findings 0 | PASS files 58, clean 42, flagged 0 |
| `1fe28e7` C2 note added | PASS 59/59/59, findings 0 | PASS files 59, clean 43, flagged 0 |
| `9c9bb64` amendment | PASS 59/59/59, findings 0 | PASS files 59, clean 43, flagged 0 |

No intermediate round commit is red; the C2 note arrives clean and nothing later regresses it. Receipts `kh-<rev>.txt`, `rc-<rev>.txt`.

## 6. Limits and boundary (stated, not claimed green)

- Item G-1 names two gates out of 33 in `tools/check-*.py` (`ls tools/check-*.py` → 33). The other 31, including `check-registry-coverage.py`, `check-adjacency-anchors.py`, `check-hook-order-r38.py`, `check-storage-health.py` and `check-self-assessment.py`, were **not run by this seat**; their state at master is unmeasured here and belongs to the wave's other gate seats. My no-harm finding is confined to the two named gates.
- `clean_count` in the recheck gate means "no findings, no invocation hits, no unresolved pointers" (`tools/check-recheck-commands.py:731`), so 43 of 59 clean with `finding_count=0` is the normal baseline shape (42 of 58 at base), not a hidden red. The 16-file gap matches `resolved_count=16`.
- Both gates scope `corpus/knowledge` only, so the round's `SCORECARD.md` and `corpus/SOURCES.md` edits are invisible to them by design.
- Not done, deliberately: no host action, no package/service/hook/sysfs touch, no `check-hook-order-r38.py` or C1/C2 counter runs (other seats own those), no lane tracked-file write. Only this report and `w1/GateHeaderRecheck/` receipts were written in the lane; scratch was removed (copies already in the seat dir).

## Receipts

`w1/GateHeaderRecheck/summary.txt` (commands, exit codes, all summary lines, mutant results), `kh-master.txt`, `kh-base.txt`, `rc-master.txt`, `rc-base.txt`, `rc-master-scoped-r38note.json`, `kh-<rev>.txt` / `rc-<rev>.txt` for `7cbaeb6`,`52ffd65`,`1fe28e7`,`9c9bb64`, `kh-selftest.txt`, `rc-selftest.txt`, `mutant-kh.json`, `mutant-rc.json`, `mutant-rc-execlog.json`.

## Proposed text for the wave record (item G-1 asks for exact text where it asks for a draft; this item does not, so this is offered only as the one-line gate statement)

> Lane gates at round 38: `tools/check-knowledge-header.py` and `tools/check-recheck-commands.py` exit 0 at base `8bd001f` and at master `5edb6c2` (header 58→59 notes, all complete/clean, findings 0→0; recheck 58→59 files, clean 42→43, findings 0→0, flagged 0→0); the round's sole new knowledge entry `corpus/knowledge/pacman-hook-order-r38.md` is clean at master, both gate blobs are byte-identical to base, and mutant controls red both gates on a missing header key, an impossible date, an empty `recheck:` and a forbidden invocation.
