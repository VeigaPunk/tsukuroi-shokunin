VERDICT: defect-found

# SentScope — G-6 scope sweep (tsukuroi round 41, w1)

Seat `SentScope-3`. Read-only sweep at 15:04–15:10 (-03, 2026-10-26), reference instant REF =
`.ufo/waves/round-41/controls/run_controls.py` mtime `2026-10-26 14:17:56.006102739 -0300`. Raw captures:
`.ufo/waves/round-41/w1/SentScope/receipt-scope-sweep.txt`. I ran no counter, installed no tool, created no scratch
dir, signalled no process, deleted nothing. My only writes are this report and that receipt.

Headline: the fleet root is clean of tsukuroi round-41 artifacts, the lane is clean of seat writes outside `w1/`, and
two of the three surfaces named by the item are clean — but **w1 built in `/tmp`**, which the lane rules forbid
("Never build under /tmp. A /tmp path is never evidence."), and a **pre-written lesson claims artifacts that do not
exist**. Detail below, with impact and the smallest remediation.

---

## S1 — medium (scope / evidence) — w1 selftest work and a census fixture landed in `/tmp`

**Observed paths** (all created during w1, all after REF):
- `/tmp/self-assessment-census-5ypff308` — dir, **300 MB**, 15:03, `git archive` tree of the lane tip
  (contains `SCORECARD.md` 424565, `SKILL.md` 645822, `tools/`, `corpus/`). Gone by 15:09 (owner cleaned up).
- `/tmp/tsukuroi-r3-2-selftest.dDInZ2` — census selftest fixture (`bin/.dispatch` + `bin/{pacman,journalctl,systemctl,
  dmesg,lsmod,expac,pacman-conf,nvidia-smi}` symlinks, `fx/` with 59 fixture dirs incl. `blocked-boot-target`,
  `blocked-empty-ring`, `blocked-bus`, `blocked-empty-pkgdb`). 15:07, gone by 15:09.
- `/tmp/tsukuroi-r3-2-selftest.rR8CO1` — same shape, **live at 15:09:32** (7.9 MB, mtime
  `2026-10-26 15:07:39.394930620 -0300`).
- `/var/tmp`: no `tsukuroi*`/`round-41` entry newer than REF (only other lanes': `r17-census-hygiene.eek7l75z`,
  `souji-r29-*`).

**Owner attribution (two independent chains).**
1. `GateSelfAssessment` receipt run — process tree read from `/proc/<pid>/cmdline` at 15:07:46:
   `omp.real` → `python3 tools/run-receipt.py --revision 71851d6… --out .ufo/waves/round-41/w1/GateSelfAssessment/
   receipt-self-assessment.jsonl -- tools/check-self-assessment.py --revision 71851d6…` → `3830006
   /usr/bin/python3 /fast/scratch/hyaku/run-receipt-dbh7wyp3/tools/check-self-assessment.py --revision
   71851d636ab1bffaf8fee5016617c88878a666f1` (**no `--scratch`**) → `3903845 bash tools/tsukuroi-census.sh --selftest`,
   `cwd=/tmp/self-assessment-census-5ypff308`, `TMPDIR=<unset>`. Both of its receipts are now on disk
   (`w1/GateSelfAssessment/`): `receipt-self-assessment.jsonl` (13853 B, 15:08, `exit_code: 1`, header
   `"tool_sha256": "1e1ab611…"` = the tip tool) — this is the run that left the 300 MB tree and `dDInZ2` in `/tmp`;
   and `receipt-self-assessment-with-scratch.jsonl` (1637 B, 15:06, **`exit_code: 2`**, `stderr_tail`:
   `"check-self-assessment.py: error: unrecognized arguments: --scratch /fast/scratch/hyaku/tsukuroi-r41/
   GateSelfAssessment/tmp"`). The seat tried the correct flag first, but `run-receipt.py` checks out
   `tool_revision` (default `--revision`, here the tip `71851d6`) — and the tip tool has no `--scratch` — so that
   attempt measured nothing and the only gate receipt with content is the `/tmp` one.
2. `RoutedSelfAssessScratch` (old-vs-new control) — `3223837 python3 …/RoutedSelfAssessScratch/old.py
   --revision 71851d6… --repo <lane>`, children `3941241`, `3964898` `bash tools/tsukuroi-census.sh --selftest`,
   `cwd=…/RoutedSelfAssessScratch/t/self-assessment-census-xsc1flim`, `TMPDIR=<unset>`; at 15:09:32 these were the
   only census processes with TMPDIR unset, and `rR8CO1` was the live `/tmp` fixture (by then a second one,
   `/tmp/tsukuroi-r3-2-selftest.Wm0riT`, 15:10, `fx/` at 89 entries, was filling as well). `old.py` is byte-identical
   to the tip tool (`sha256` prefix `1e1ab6113d665684` for both), and `new.py` (53556 B) is the patched working copy.
   Its work tree lands in scratch because the seat exported `TMPDIR=…/t`, but the census *child* is spawned with
   `git_env()`, whose base is `CHILD_ENV_BASE = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C'}`
   (`tools/check-self-assessment.py:94`) — no `TMPDIR` — so the child falls back to `${TMPDIR:-/tmp}`. By elimination
   `dDInZ2` belongs to the gate chain (it vanished with that chain) and `rR8CO1`/`Wm0riT` to
   `RoutedSelfAssessScratch`.

**Why it happens (code, at the revision measured).**
- `tools/tsukuroi-census.sh:1930` — `work=$(mktemp -d "${TMPDIR:-/tmp}/tsukuroi-r3-2-selftest.XXXXXX")`; comments at
  `:385` and `:570` name the same `${TMPDIR:-/tmp}` family. With `TMPDIR` unset the fixture is `/tmp`.
- lane **tip** `tools/check-self-assessment.py:181` (via `git show 71851d6:…`) —
  `work = tempfile.mkdtemp(prefix="self-assessment-census-")` with **no `dir=`**, and the census child is spawned with
  `env=git_env()` (no `TMPDIR`). The tip therefore lands the extracted tree *and* the fixture in `/tmp`.
- lane **working copy** `tools/check-self-assessment.py:185` `…dir=scratch` and `:193-194`
  `child_env = dict(git_env(), TMPDIR=child_tmp)` — exactly the uncommitted L1 diff (docstring "Round 41
  (R40-TMP-MISROOT)"). The fix exists but is **not at the tip**, and `run-receipt.py` extracts the tip into
  `/fast/scratch/hyaku/run-receipt-dbh7wyp3/` and runs *that* copy.

**Exploit path.** Any receipt or seat that measures the tip through `run-receipt.py` (or runs the census with `TMPDIR`
unset) writes its 300 MB extracted tree and a fixture tree — including the deliberately planted
`fx/storage-mounts-fifo/mounts` FIFO — under `/tmp`, where the rules say no build may live and no path is evidence.
Two concrete consequences, both reachable today: (1) the gate's only content-bearing receipt (`exit_code: 1`) was
produced by that tree, and its header/argv carry no trace of the `/tmp` extraction (`argv` has no `--scratch`; the
`"repo"` it names, `/fast/scratch/hyaku/run-receipt-dbh7wyp3`, is deleted by `run-receipt.py`'s `finally`), so a reader
cannot tell the measured census ran in `/tmp` and cannot re-derive it from any keeper — while the honest
`--scratch` invocation is the one that died with `exit_code: 2`; (2) every seat in a wave runs as the same uid, so a
sibling seat — or anything a seat executes — can rewrite `/tmp/tsukuroi-r3-2-selftest.*/fx/*` or `bin/.dispatch`
between cases, which makes a selftest run from `/tmp` a tamperable witness for the mutant kills this wave is judged on
(`bin/.dispatch` answers *from `$TSUKUROI_FIXTURE`*, `tools/tsukuroi-census.sh:1937-1942`, i.e. from the fixture tree
itself). `/tmp` is also on the root disk (`df -h /tmp` → `/dev/nvme1n1p1 128G 3.1G`), so a run that leaves 300 MB
behind competes with the host. No host mutation and no privileged read occurred: every fixture binary is the census's
own `bin/.dispatch` dispatcher, and no fixture was found outside the two seats named above.

**Smallest remediation.** (a) Land the working-copy `tools/check-self-assessment.py` diff, then re-issue the gate
receipt as `tools/run-receipt.py --revision <rev> --tool-revision <rev-with-the-fix> --out .ufo/waves/round-41/w1/
GateSelfAssessment/receipt-self-assessment.jsonl -- tools/check-self-assessment.py --revision <rev> --scratch
/fast/scratch/hyaku/tsukuroi-r41/GateSelfAssessment/tmp` — `--scratch` only means anything when `--tool-revision`
resolves to a tool that implements it, which is exactly the `exit_code: 2` failure seen here; (b) for the old-vs-new
control, set `TMPDIR` *inside* the child env of the `old.py` copy (`CHILD_ENV_BASE` at `tools/check-self-assessment.py:94`
drops it) or run the control inside `unshare -rm` with a private `/tmp`; (c) for direct census runs,
`export TMPDIR=/fast/scratch/hyaku/tsukuroi-r41/<seat>/tmp` — the seats that did this (`C1ExecRerun`,
`C1SentScratch`, `C1HeldOutGuards`, `CritSeparability`, `C1CritLabels`, `C1CritDecoy`, `C1CritParams`, all visible in
`/proc/<pid>/environ`) wrote no `/tmp` fixture.

## S2 — medium (provenance) — the pre-written lesson cites artifacts that do not exist

`corpus/lessons/round-41.md` (untracked, 9045 B, mtime **14:21:12**, i.e. before `w1.ready` 15:03:31 and before any
seat ran) states at `:4-5` that outcome lives in `SCORECARD.md` section "Round 41 — measured outcome" and in
`.ufo/waves/round-41/w1-results.json`. Neither exists now: `grep -n "^#\+ .*Round 41" SCORECARD.md` returns only
`:2454 ## Round 41 — declaration (2026-10-26, base 0e5805a1…, before any seat)`, and
`ls .ufo/waves/round-41/w1-results.json` → "No such file or directory". The file's own header credits
`author: tsukuroi L1 (TsukuroiR41)`, so this is L1 scaffolding, not a seat write — but if it is committed as-is it
asserts a measured outcome that was never measured. Impact: a reader of the landed lesson cannot tell pre-draft text
from measurement. Remediation: after the wave settles, replace the header pointer and add the outcome section only
from receipt values (or drop the `w1-results.json` reference).

## S3 — low (no-harm blocker) — a `cp` has been blocked on a FIFO for 1 h 52 m in L1 scratch

`ps -o pid,etime,args= -p 2970499` at 15:10: `cp -- /fast/scratch/hyaku/tsukuroi-r41/L1/c1/r41c1.xzp_mzmq/capture/tmp/
tsukuroi-r3-2-selftest.XMP9dE/fx/storage-mounts-fifo/mounts /fast/scratch/hyaku/tsukuroi-r41/L1/c1/r41c1.xzp_mzmq/
cap/114.mounts`, ELAPSED `01:52:29`. It is the census's deliberately-planted mount-table FIFO
(`tools/tsukuroi-census.sh:1902-1904` hardened the census against exactly this read), and `cp` has no timeout, so it
never finishes; it also pins 114 MB of capture dirs and will block the L1's scratch cleanup. I did not signal it (not
my process). Remediation: the L1 kills PID 2970499 and re-captures with `cp --no-target-directory` replaced by a
bounded read (`timeout 5 cat`) or `cp` on the regular-file fixture only.

## S4 — informational — lane writes outside `w1/` are L1 dispatch machinery plus one item-authorized tracked edit

`git -C <lane> status --porcelain` at 15:09:32, nothing else:

| path | size / mtime | attribution |
|---|---|---|
| `M tools/check-self-assessment.py` | 53556, 13:57:57 | L1 (the named allowed file; its diff is the S1 fix) |
| `M corpus/knowledge/pacman-exec-environment-r40.md` | 16485, **15:06:45** | seat `RoutedS220Anchor` |
| `?? .ufo/waves/round-41/make-w1-spec.py` | 47097, 14:58:08 | L1 dispatch builder |
| `?? …/revs.json` `?? …/w1-dispatch.{json,err}` `?? …/w1-spec.json` `?? …/w1.ready(.dispatched\|.partial)` | 15:03:24–15:09 | L1 dispatch state (`w1.ready` content: `{"lane":"tsukuroi","round":41,"wave":"w1","l1":"TsukuroiR41"}`) |
| `?? corpus/lessons/round-41.md` | 9045, 14:21:12 | L1 (header `author: tsukuroi L1`) — see S2 |
| `?? .ufo/waves/round-41/w1/` | — | in bounds: reports at `w1/<Seat>.md`, receipts at `w1/<Seat>/` |

No `D` entries; `git index` mtime 15:03:45, `.jj/repo` and `.jj/working_copy` 15:03 — no mutating `git`/`jj` command
left a newer trace. The tracked edit is **authorized by the seat's own item**: `w1-spec.json` `items[54].prompt`
("a corrected sentence appended to /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/
pacman-exec-environment-r40.md … without editing the row"). Its diff is a pure 8-line append under
`## Anchor correction (appended round 41; round-40 closure §6.4)`, and `git status --porcelain -- corpus/SOURCES.md`
is empty, so CORPUS.md rule 2 held. Action for L1: include this file in the round commit and confirm the append-only
form. Note the item text I was given lists only `tools/check-self-assessment.py` as the L1's own uncommitted file;
these seven scaffolding paths are what actually exists.

## S5 — clean surfaces (positive evidence, so the zeros are auditable)

- **Fleet root** `/home/vgpnk/Projects/shokunin`: `git status --porcelain` → only
  `?? .ufo/reports/round-44/mado.md`, `?? .ufo/reports/round-48/tameshi.md` (other lanes' round reports; `mado.md:5`
  still carries `<<TIP>>`/`<<W2N>>`, `tameshi.md:3` `@@LANE@@`). The earlier ` M .scratch/goal-20261026-hyaku-run9.md`
  was an orchestrator edit (file header line 1: "ORCHESTRATOR-OWNED run state (hyaku run 9)"; +18 lines about
  kengaku r40 / kasegi r37 / souji r33) and was gone from porcelain by 15:09. `find -maxdepth 4 -name '*round-41*'`
  outside the lane yields only fleet-root prompts (`.ufo/prompts/tsukuroi-round-41.md`, 13:00) and the pre-run
  `.ufo/waves/round-41/` (2026-10-25 21:03). **No tsukuroi round-41 artifact was written at the fleet root** — no
  misroot of a report or receipt.
- **tabi/tameshi-style `/tmp` residue is absent for this lane**: `find /tmp -newer REF \( -name '*tsukuroi-r41*'
  -o -name '*round-41*' -o -name '*hyaku*' \)` → 0. The hits in S1 are named after the tools
  (`tsukuroi-r3-2-selftest`, `self-assessment-census`), not the lane, which is why the item's literal name filter
  would have missed them.
- **PATH surface**: `find /home/vgpnk/.local/bin -newer REF` → 0 entries, so the r40 kengaku `git`-shim write did not
  recur in this wave.
- **Read-only sources**: `shokuknow` has no working file newer than REF (only its `.git` entry, mtime 14:18); its
  `--no-optional-locks status` modifications are its own campaign state, all pre-REF.
- **Sibling lanes**: files newer than REF under `kaidoku` (r39), `kasegi` (r37), `kengaku` (r40), `mado` (r44),
  `souji` (r33), `tabi` (r32) are each their own round's corpus/lesson files; none names `tsukuroi-r41` or a
  tsukuroi seat.
- **Scratch base** `/fast/scratch/hyaku/tsukuroi-r41`: 3.0 GB, 50 entries at 15:06 → 44 dirs at 15:10 → 39 at 15:11,
  **all seat-named**, none foreign or unnamed; the list shrinks as seats finish (`C1ExecSelftest`,
  `C1ExecPriorCounters`, `C2ExecRerun`, `C2RevPA1` were present at 15:06 and gone by 15:10 — seats are honouring
  their `trap … rm -rf`), so no leftover directory is attributable to a finished seat at sweep time. Outside that base,
  `run-receipt.py:80-82` (`tempfile.mkdtemp(prefix='run-receipt-', dir='/fast/scratch/hyaku')`) created
  `run-receipt-dbh7wyp3` (339 MB) + `run-receipt-home-77tywiji` at 15:07; both were removed by the tool by 15:09, so
  this is tool design, not a seat leak — but it is why a 339 MB receipt tree exists outside the mandated seat path
  while a receipt runs.

## What I did not do

Did not read seat reports for content correctness (scope only), did not re-run any counter, did not inspect `/etc`,
`/usr`, sysfs or any host service (outside the assigned surface), and touched `/home/vgpnk/Projects/shokunin` only with
`git status` / `find` / `/proc` reads. The surface is live: `/tmp/self-assessment-census-5ypff308` and
`/tmp/tsukuroi-r3-2-selftest.dDInZ2` were removed by their owners while I swept, and new fixtures were appearing after
my final snapshot (`Wm0riT` at 15:10), so the sizes quoted are the values observed at the stated times, and a re-sweep
after the wave settles may show a different set. A `C1` seat's counter run was in progress throughout
(`score-selftest-mounts-r41.py --jobs 4`, ~05:07 elapsed at 15:10), so counter-level conclusions remain outside this
sweep.
