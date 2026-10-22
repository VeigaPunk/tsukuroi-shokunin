# RevMarkerO03 — attack of C1 marker `R29-OWED-O03` at 10d5288fc1051364e711203855e7c53710dfcc21

Verdict: **holds** — marker `R29-OWED-O03` in `corpus/knowledge/kill-event-deep-r8.md:400` survives
attack on all three checked fronts: (a) the original statement stands byte-unchanged, (b) `qualified`
is the right verdict, (c) both basis references resolve and every clause of the `now` text is
supported by the cited kernel bytes; no defect found.

## Findings

1. **(a) original unchanged — holds** [obs]. The anchor line is line 147:
   `[inference] under a kernel OOM the scan prefers the higher-scored, larger-RSS tasks first; a kernel pick of`
   (`grep -cF` over the file = 2: this base line + the marker's own `original:` quote at :400).
   sha256 of that line without newline =
   `1b1563e3c28865a691ef58705b59e516d3d2574024538bca052bdd8b872e9b88`, which equals
   `BASE_DIGEST['O03']` (`tools/check-owed-statements-r29.py:91`), so the counter's M1 append-only
   rule passes; line 147 sits in §4 prose, outside any fence or HTML comment and outside the marker.

2. **(b) verdict `qualified` is right — holds** [obs]. The original claims preference ("prefers the
   higher-scored, larger-RSS tasks first"). Outcome-level it is true — the argmax picks the highest
   badness, and RSS is its baseline term — while "scan … first" is a false mechanism (no ordered walk).
   Wave-1 `.ufo/waves/round-29/w1/RevOomMechanism.md` ("O03" section) said the core claim is
   "substantively right", warranting `rebutted` — "or `qualified` if the scribes want to fix the
   'scan first' phrasing and add the bypass-path caveat". The landed `now` does exactly that second
   option: it replaces the ordering reading with the argmax rule and adds the three bypasses.
   Calibration is consistent with the sibling marker: O04 in the same file ("the +200 band is scanned
   first", a pure mechanism claim) is `corrected`, while O03 keeps its true preference core.
   So `qualified` — not `rebutted` — is the correct label.

3. **(c) basis resolution — holds** [obs].
   - `corpus/SOURCES.md:154` (S148) and `:155` (S149) both parse to status `mined`, opened
     `2026-10-22`, used-by cell containing `corpus/knowledge/kill-event-deep-r8.md` (M6/M7 fields;
     M7 also needs absence at base: `git show 16e9ab2a:corpus/SOURCES.md | grep -cE "S14[89]"` → 0).
   - Snapshot fidelity: my own fresh fetches today —
     `https://raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c` → sha256
     `452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e` and
     `.../Documentation/filesystems/proc.rst` → sha256
     `e760f716f8278deefab17a63739033cadc7faee93663c49e76455afaaf40d126` — match the sha256 declared
     in the S148/S149 rows, and `diff -q` shows the wave-1 snapshots
     `.ufo/waves/round-29/w1/ScribeSrcOomKill/S149.c` (1257 lines) and
     `.ufo/waves/round-29/w1/ScribeSrcProcRst/S148-proc.rst` (2495 lines) are byte-identical to
     upstream. Copies saved as `.ufo/waves/round-29/w2/RevMarkerO03/oom_kill.c.upstream` and
     `proc.rst.upstream`.
   - Line refs resolve: S149 306–377 = `oom_evaluate_task` (306) through the close of
     `select_bad_process` (377); 1122 = `if (task_will_free_mem(current))`; 1145–1151 = the
     `sysctl_oom_kill_allocating_task` branch through the `oom_kill_process` call. S148 1761–1789 =
     §3.1 body; line 1777–1779: "The value of /proc/<pid>/oom_score_adj is added to the badness score
     before it" with the −1000…+1000 range — the basis for "the adjustment term".

4. **`now` clause-by-clause support — holds** [obs], against S149 bytes (line numbers of the
   byte-identical snapshot):
   - "single argmax over eligible tasks": `select_bad_process` keeps one `oc->chosen`/
     `chosen_points` over `for_each_process` (372) or the memcg scan (367); replacement only on
     strictly greater points (340, 348).
   - "resident pages plus swap entries plus page-table pages": 228–229
     `points = get_mm_rss_sum(p->mm) + get_mm_counter_sum(p->mm, MM_SWAPENTS) +`
     `mm_pgtables_bytes(p->mm) / PAGE_SIZE`.
   - "plus the adjustment term": 233–234 `adj *= totalpages / 1000; points += adj;`.
   - "nothing is visited first": 371–375 iterate the task list unsorted; no score-ordered visiting.
   - "ties fall to iteration order": 340 skips only `points < oc->chosen_points`, so an exact tie
     falls through to `select` and the later-iterated task wins — tie resolved purely by iteration
     order, as stated.
   - "higher-scored and larger-RSS tasks do win": argmax semantics; RSS dominates the sum.
   - bypasses: allocating-task (1145–1151) and free-memory (1122–1126) return before
     `select_bad_process` is ever called; origin (334–337) sets `points = LONG_MAX; goto select;`
     so `oom_badness` is never computed for that task.
   `now` contains no numbers, so there was nothing to recompute inside it [obs]. As context I also
   recomputed the neighbouring round-29 correction-prose numbers (kill-event-deep-r8.md:392–399,
   outside the marker line): (31,721,800+31,722,876)/4/1000 = 15,861 and
   (31,721,800+35,917,176)/4/1000 = 16,909 both check; +100/+200/+300/−900 point totals and GiB
   conversions all recompute exactly; live `/proc/meminfo` still shows MemTotal 31,721,800 kB and
   SwapTotal 31,722,876 kB as quoted.

5. **Marker hygiene** [obs]: M2 uniqueness — `grep -c "R29-OWED-O03"` over the six target files is 1,
   only in `kill-event-deep-r8.md` (its own file); M3 — the `original:` quote is byte-equal to the
   frozen anchor.

6. **Minor wording nuance, not a defect** [obs]: "the … origin bypasses can skip the comparison
   entirely" is exact for the origin task itself (334–337 jumps to `select` before the 339 scoring
   call), but unlike the allocating-task and free-memory paths the task-list walk still runs and
   later candidates trivially lose against `LONG_MAX`. A stricter phrasing would say the origin
   bypass skips the *scoring*, not the whole scan. Does not change the verdict, the support claim,
   or the counter outcome.

## Residual risk and verification gaps

- [unk] Whether the counter at the revision actually prints `marked 12 of 12` was not re-run here
  (counter execution is the L1/main verification; this audit is file-and-source level).
- [inf] S148's row notes raw.githubusercontent.com answered HTTP 429 to the scribe and the bytes came
  from git.kernel.org/jsdelivr mirrors; my fresh raw.githubusercontent fetch succeeded and matched,
  so that dependency is closed today.
- [obs] The prose nuance in finding 6 is the only improvable wording; nothing fails.

Scope: read=lane files kill-event-deep-r8.md, SOURCES.md, check-owed-statements-r29.py, w1 snapshots S149.c and S148-proc.rst, RevOomMechanism.md, SCORECARD.md, w1/w2 spec jsons, /proc/meminfo; wrote=.ufo/waves/round-29/w2/RevMarkerO03.md, .ufo/waves/round-29/w2/RevMarkerO03/oom_kill.c.upstream, .ufo/waves/round-29/w2/RevMarkerO03/proc.rst.upstream; executed=grep/sha256sum/diff/python3 one-liners, read-only `git show 16e9ab2a:corpus/SOURCES.md` with GIT_* unset, curl of the two public raw.githubusercontent.com v7.2 files — no lane writes outside seat paths, no git writes, no pacman, no service or config changes
Model: zai/glm-5.3-flash
Installs: none
