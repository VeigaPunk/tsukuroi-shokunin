VERDICT: defect-found

# SentMisroot — X-5 misroot / scope sweep, tsukuroi round 43, wave w1

Sweep window: 2026-10-26 19:20–19:24 -03 (wave dispatch marker `w1.ready` = 19:01:14; reference mtime = `make-w1-spec.py` 19:00:58). Read-only throughout; nothing deleted. Machine snapshot: `.ufo/waves/round-43/w1/SentMisroot/sweep-snapshot.txt`.

Axes checked, per the seat item: (a) fleet-root untracked naming tsukuroi round 43, (b) lane status outside `.ufo/waves/round-43/w1/`, (c) `/tmp` + `/var/tmp` newer than `make-w1-spec.py` naming `tsukuroi-r43`/`bootinputs`, (d) new `~/.local/bin` entries, (e) host tmpfs mounts naming `r43lib`/`r43view`, (f) leftovers under `/fast/scratch/hyaku/tsukuroi-r43`.

## Clean axes (negative result, evidence given)

| axis | result | evidence |
|---|---|---|
| fleet root untracked | **0 entries** | `git -C /home/vgpnk/Projects/shokunin status --porcelain \| wc -l` → `0` (19:23:19). Ignored-list grep for `tsukuroi\|r43\|round-43` shows only the pre-existing orchestrator state pair (`.ufo/state/tsukuroi.*`) and the lane directory itself. |
| `/tmp` + `/var/tmp` names | **0 entries** | `find /tmp -newermt @1793052058 \( -name '*tsukuroi*r43*' -o -name '*bootinputs*' \)` → empty; same for `/var/tmp`. No `tmp.*` scratch dirs newer than the reference in either. |
| `~/.local/bin` | **no new entry** | newest entry is `…/bin/omp` at **18:10**, i.e. before the wave; `find ~/.local/bin -newermt '2026-10-26 18:00'` → only the directory itself + `omp`. No symlink in `~/.local/bin` resolves into `/fast/*`, `/tmp/*`, `/var/tmp/*` or any `*scratch*` path; `$PATH` contains no `/fast`, `/tmp` or `scratch` element; no profile file references `/fast/scratch`. No shim, no PATH write. |
| host tmpfs / mounts | **none leaked** | `findmnt -t tmpfs` lists only `/dev/shm`, `/run`, `/run/credentials/*`, `/run/user/1000`; `findmnt -o TARGET \| grep -iE 'r43\|tsukuroi'` → `NONE`; scanning every `/proc/[0-9]*/mountinfo` for `r43lib\|r43view\|tsukuroi-r43` → no hit. `/dev/shm` empty. |
| lane history state | **no seat mutation** | reflog head `7d0ed1c2 HEAD@{2026-10-26 19:01:12}: export from jj`; no entry after 19:01:12; `git stash list` empty; `.jj/repo` and `.jj/working_copy` mtimes = 19:01 (the L1 export); `.git/HEAD` 19:01:12. `.git/index` was rewritten at **19:07:04**, which is the ordinary index-refresh side effect of a read-only `git status`/`git diff`; HEAD, reflog and stash are unchanged, so no add/commit/checkout/reset. |
| host package/service | **untouched** | `/var/log/pacman.log` last transaction `2026-10-20`; `find /etc -newermt @1793052058` → empty; `systemctl list-units --state=running` and `--user` filtered for `r43\|tsukuroi\|harness` → none; no `unshare|setpriv` process of this lane alive (the live `bwrap` processes belong to `kengaku-r43` and `mado-r47`, other lanes). |

## F1 — lane write outside `w1/`: `tools/__pycache__/*.pyc`, hidden by `.gitignore` (severity: low; the one real scope breach)

Two bytecode files were written **inside the lane, outside `.ufo/waves/round-43/w1/`**, during wave w1:

```
2026-10-26 19:08:50  25116  tools/__pycache__/score-bootinputs-r43.cpython-314.pyc
2026-10-26 19:21:04  27430  tools/__pycache__/check-scrub-record-r43.cpython-314.pyc
```

`stat -c '%y %s %n'` as above; both postdate the 19:01:14 dispatch marker, so both are wave-w1 activity.

Why the porcelain sweep misses it: `git -C <lane> check-ignore -v tools/__pycache__` → `.gitignore:2:__pycache__/`, and `git ls-files tools/__pycache__` → empty (untracked). Consequence: `git status --porcelain`, the check named in my item, reports **clean** for this path while the write actually happened. Everything the L1 would see is `?? .ufo/waves/round-43/w1.ready`, `?? .ufo/waves/round-43/w1.ready.dispatched`, `?? .ufo/waves/round-43/w1/`.

Mechanism (bounded): running a counter as a script (`python3 tools/<x>.py`) does not produce a `__main__` pyc, so some seat loaded the counter through the import machinery (e.g. `importlib.util.spec_from_file_location(...).exec_module`, or `py_compile`/`compileall`); the hyphenated filenames rule out a plain `import`. I did **not** identify which seat (single uid `vgpnk`; a C1 seat at 19:08:50, a C2 seat at 19:21:04 — e.g. `C2RevCounter`/`C2CritControl`, which were reading those counters then).

Tamper check — the loaded source was the genuine lane counter, not a doctored copy. pyc header `(src_mtime, src_size)`:

```
score-bootinputs-r43  header 1793051405 / 15848  vs tools/score-bootinputs-r43.py 1793051405 / 15848  MATCH
check-scrub-record-r43 header 1793051605 / 15981  vs tools/check-scrub-record-r43.py 1793051605 / 15981  MATCH
```

So this is a write-path leak, not an evidence-substitution leak.

Impact: bytecode only; no tracked content changed; no counter verdict is affected. The real cost is that the sweep named in the dispatch is blind to it, so any future ignored-path write (a `.pyc` compiled from a *modified* counter, a `*.log`, a `.venv`) would also pass the same check.

Smallest remediation — one line in the dispatch shell (no lane edit by me):

```sh
export PYTHONDONTWRITEBYTECODE=1   # seats that load counters as modules
```

and widen the post-wave scope check to ignored paths:

```sh
git -C "$LANE" status --porcelain --ignored
find "$LANE" -newer .ufo/waves/round-43/make-w1-spec.py -type f -not -path '*/.ufo/waves/round-43/w1/*'
```

## F2 — `/fast/scratch/hyaku/tsukuroi-r43` shared-root strays, pre-wave (severity: low; provenance hazard)

At the *shared* scratch root, not under any `/<seat>/` directory, ten entries sit outside a seat:

| path | type | size | mtime | owner |
|---|---|---|---|---|
| `linux-ioctl.c` | regular file | 145601 | 18:42 | L1 / pre-wave worker (uid vgpnk) |
| `hybrid.sh` | regular file (bash) | 53425 | 18:47 | L1 / pre-wave worker |
| `n.c` | regular file (C) | 169 | 18:51 | L1 / pre-wave worker |
| `n` | regular file, ELF x86-64 pie, **executable** | 15968 | 18:51 | L1 / pre-wave worker |
| `ko-ioctl.c` | regular file | 145999 | 18:54 | L1 / pre-wave worker |
| `tsukuroi-bootchain-selftest.XBeIcT/` | dir, 30 files | 116K | 18:45 | L1 / pre-wave worker |
| `tsukuroi-bootchain-selftest.EvDLGL/` | dir, 32 files | 116K | 18:47 | L1 / pre-wave worker |
| `tsukuroi-bootchain-selftest.HQHuHD/` | dir, 32 files | 116K | 18:47 | L1 / pre-wave worker |
| `t1/`, `controls-c1/`, `controls-c2/`, `after-c1/`, `before-c1/` | empty dirs | 0 | 18:49–18:57 | L1 / pre-wave worker |

All timestamps precede `w1.ready` (19:01:14), so **no w1 seat owns them**; they belong to the L1/pre-wave phase and I could not narrow further (every process here runs as uid `vgpnk`).

The three `tsukuroi-bootchain-selftest.*` dirs are the tool's own fixtures and prove `TMPDIR` was the *shared root*, not a seat dir: `tools/boot-chain-audit.sh:887` — `T=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-bootchain-selftest.XXXXXX")`. Nothing cleaned them up, so the fixture trio (348K, mode 700) is left at the root.

Provenance note on the two `ioctl.c` copies — neither can masquerade as the frozen source, which is worth stating because a mutable copy of a frozen artifact at a shared path is exactly how a substituted source reaches a counter:

```
frozen src/ioctl.c   sha256 7b3488f2f83563134fec1a3d40c4149a5fe3606de6628cd33f7897fd4534ba01
ko-ioctl.c           sha256 7b3488f2…  (byte-identical to frozen; diff → 0 lines)
linux-ioctl.c        sha256 08992385…  (diff vs frozen → 71 lines, a different tree's file)
```

`hybrid.sh` is the **pre-fix** candidate, diverging from the shipped tool at exactly the repaired line:

```
469c469,470
<     if find "$@" -newermt "@$epoch" -print -quit 2>/dev/null | grep -q .; then   # hybrid.sh
---
>     hit=$(find "$@" -newermt "@$epoch" -print -quit 2>/dev/null)
>     if [ -n "$hit" ]; then                                                       # tools/boot-chain-audit.sh
```

i.e. the scratch-root copy carries the pipefail-decided fail-open that C1 claims to have removed at `717b716`. It is not wired into any counter (the counter runs the lane file/lane revision), but it is a live, mutable copy of the defect sitting one `cp` away from the frozen tool path.

`n.c` / `n` are a build probe for the C2 axis (`BTRFS_IOC_SCRUB_PROGRESS` value + `sizeof(struct btrfs_ioctl_scrub_args)`), pre-dating the wave.

Smallest remediation: after the wave, `rm -rf` these ten root entries (I deleted nothing, per my read-only remit); and set `TMPDIR=/fast/scratch/hyaku/tsukuroi-r43/<seat>` in the seat shell so `mktemp` fixtures land where the scratch rule says.

## F3 — two SIGSEGV cores from a seat-built harness (severity: informational, host-visible state)

```
Mon 2026-10-26 19:19:07 -03  pid 3546800  SIGSEGV  present  /fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro/harness   29.8K
Mon 2026-10-26 19:19:24 -03  pid 3580942  SIGSEGV  present  /fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro/harness     31K
```

`coredumpctl list --since '2026-10-26 18:40'`; cores land in `/var/lib/systemd/coredump` via `kernel.core_pattern = |/usr/lib/systemd/systemd-coredump …`, so the seat did not write that path itself — but ~61 KB of host state is attributable to `C2ExecTailRepro`'s w1 work. No local `core`/`core.*` file exists in the fleet root or the lane (`find … -maxdepth 2 -name 'core*'` → empty).

Not visibly deliberate: `grep -rIl 'SIGSEGV\|raise(SIG\|abort()' /fast/scratch/hyaku/tsukuroi-r43/C2ExecTailRepro` → no match (that seat's receipt in `w1/C2ExecTailRepro.md` reads `VERDICT: supports`). I am not judging the probe — flagging so the C2 reviewer can ask whether the harness crashed on a case it counted, since a segfaulting driver at 19:19 and a `supports` verdict can both be true only if the crash was one of the modelled branch cases.

The other wave-window cores are not this lane: `python3.14` ×2 at 18:45:21 (pre-wave, plus a `strace` SIGSEGV), `sasquatch` ×5 at 18:54–18:55 (another lane's emulator).

## F4 — L1/orchestrator entries outside `w1/` (severity: none, listed for completeness)

`?? .ufo/waves/round-43/w1.ready` (160 B, 19:01:14, contains `"l1":"TsukuroiR43"`) and `?? .ufo/waves/round-43/w1.ready.dispatched` (1561 B, 19:19:58, timestamp + seat→agent-id map) are the planner's dispatch markers, not seat writes, and neither is gitignored — the L1 is the only committer and should decide whether they belong in the round commit or `.gitignore`. Everything else already-tracked under `round-43/` (`before/`, `after/`, `controls/`, `frozen/`, `make-w1-spec.py`, `w1-spec.json`, `w1-dispatch.json`, `w1-dispatch.err`) shows only its 18:41–19:01 authoring time, consistent with commit `7d0ed1c2` at 19:01:12.

## Scratch inventory at sweep time (live seats, not leftovers)

`/fast/scratch/hyaku/tsukuroi-r43` totals **1.3 G**; `/fast/scratch/hyaku` at 25 % use, disk-guard log entries `ok` at 19:19:53.

| dir | files | du | note |
|---|---|---|---|
| `ScribeReadme` | 15762 | 652M | includes a 322M lane clone (`ScribeReadme/lane`) — within its own seat dir |
| `C1CritEvasion` | 31494 | 644M | `input/` + `pathenv/` counter trees |
| `C1MutFix` | 15768 | 322M | clone + mutants |
| `AdjPins`, `AsmGate`, `C1RevCounter`, `C1RevFix`, `C1SentScope`, `C2CritControl`, `C2ExecCallGraph`, `C2ExecKernelPatch`, `C2ExecTailRepro`, `C2RevCounter`, `ScoutR42Defects-2`, `ScribeLesson`, `SrcGateS237`, `SrcGateS240`, `CritSeparability` | 1–178 | — | live seats |
| `C1CritChannels`, `C2DraftRevSR6`, `ConsiderMap`, `SentMisroot` (mine) | 0 | — | see below |

No non-regular file exists under the root except fixture symlinks inside seat trees (`tsukuroi-bootchain-selftest.*/tree-a/new_root -> sysroot`, and round-35 `ScribeC2Draft/pacman-*` links inside `C1CritEvasion/input|pathenv` and `C1MutFix/clone` copies of the lane). No world-writable or setuid entry at depth ≤ 2. My own `SentMisroot/` is removed at exit; the receipt is copied into `w1/SentMisroot/` first.

`C1CritChannels` and `C2DraftRevSR6` have **zero scratch files** yet both already wrote a receipt (`w1/C1CritChannels.md` = `defect-found`, `w1/C2DraftRevSR6.md` = `draft`). Not a scope breach, but neither seat left a local trail for its claims; if either verdict rests on a run, that run's outputs are not in the seat dir. `C2DraftRevSR6` is the seat whose subject is the draft row text, so a text-only verdict is plausible.

## What I did not do

Did not re-run any counter, census or check (verification is main's job and the witnesses own their runs); did not open the contents of the 31 k-file seat trees file by file (only top-level layout, counts and symlink/perm anomalies); did not attribute the shared-root strays to a named seat (single uid, only mtime ordering is available — all predate dispatch); did not attribute the `/tmp` `/var/tmp` population to a lane beyond the content heads quoted below; did not touch, move or delete any file, mount, service or process, and signalled nothing.

Adjacent `/tmp` population, for the record — **not** this wave and not named `tsukuroi-r43`/`bootinputs`, but it is the only wave-window `/tmp` churn, so the source is identified rather than left ambiguous:

- `/tmp/sc_base.md`, `/tmp/sc_at_base.md` (272196 B, 19:14) and `/tmp/ledger_base.json` (3511644 B, 19:14) — first line `# tameshi-shokunin — Scorecard` / `"schema": "tameshi-coldread-ledger-v2"` → tameshi lane's seat; they merely *mention* tsukuroi rows (`tsukuroi`, `tsukuroi/mado`, `tsukuroi-census/…`).
- `/tmp/src_freeze.md`, `/tmp/src_docs.md` (19:11) — `# SOURCES — where kengaku learns` → kengaku lane.
- `/tmp/build.log`, `/tmp/test.log` (19:01) — `nightwire@0.1.0` → nightwire project.
- `/tmp/bh.out`, `/tmp/bh.err`, `/tmp/bh2.out` (19:07) — `netgear_be_v3_0_lzma` firmware probes → firmware lane, not this one.
- `/tmp/self-assessment-git-y94cav55` (19:21, transient, already gone) — from `tools/check-self-assessment.py:69`, `_GIT_SANDBOX = tempfile.TemporaryDirectory(prefix="self-assessment-git-")`: a module-level temp dir that ignores `--scratch` and lands in the caller's `TMPDIR`. It reproduced during w1 (`ScribeReadme`/`CritSeparability` were running that tool with `--scratch` under their own seat dirs), so a seat that does not export `TMPDIR` still writes to `/tmp` for the life of the run. One-line fix on the caller side is the same `TMPDIR=` export as F2; a tool-side fix is `dir=` on that line. It leaves nothing behind, so it is not a leftover — it is the mechanism that would produce one if the process died.

## Verdict

`VERDICT: defect-found` — one genuine lane write outside `w1/` during the wave (F1, bytecode, invisible to `git status --porcelain` because of `.gitignore:2`), ten pre-wave shared-root scratch strays including a mutable copy of the pre-fix `inputs_newer_than` body and two divergent `ioctl.c` copies (F2), and two seat-attributable SIGSEGV cores in the host coredump store (F3). No fleet-root write, no `/tmp`/`/var/tmp` artifact of this wave, no `~/.local/bin` entry, no leaked mount or namespace, no package/service/`/etc` change, no git/jj history mutation, no signal sent. Severity across F1–F3 is low; none of them touches a frozen claim, and F1 is the one that a sweep built on `git status --porcelain` alone would have certified as clean.
