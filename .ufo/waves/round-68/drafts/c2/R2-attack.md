2026-11-03T22:36:18Z
# R2Reviewer — attack on C2 draft `check-knowledge-refs-r68.py`

Draft under attack: `.ufo/waves/round-68/drafts/c2/check-knowledge-refs-r68.py`, 513 lines,
sha256 `d4390b7aa2c7fa1418ea5ff078f95c3faef19c6d12ecb6473d426a90fe7858d5` (mtime 22:34:26Z).
Drift disclosed: I first read the file at sha `6dec466a…` (23936 bytes); it was edited
during my read to `d4390b7a…` (23984 bytes, still 513 lines). The rule lines I cite
(48, 61-63, 101, 153-193, 204-215, 282, 397, 500) were re-checked in the current version by grep.
I did NOT re-read every line of the new version. Verdicts apply to `d4390b7a…`.

Header-gate rules (`tools/check-knowledge-header.py`, read in full): column-0 `key:` only,
fenced blocks skipped via `FENCE = ^ {0,3}(`{3,}|~{3,})`, closing fence must be same char, run >= opener,
no info string; operative line = LAST occurrence; binding via `tools/_revision.py`; `sys.dont_write_bytecode`
set before the shared import; exit 0/1/2; JSON on stdout.

## Live base (required)
$ git clone --shared -q /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$S/lane" && git -C "$S/lane" checkout -q 42400ec6 && cp <draft> "$S/lane/tools/check-knowledge-refs-r68.py" && python3 -B "$S/lane/tools/check-knowledge-refs-r68.py" --revision 42400ec6 --lane "$S/lane"
rc=0 (LIVE_BASE_RC=0)
{"status": "PASS", "revision": "42400ec65c45709ade07a92ed72d1277e3478bbb", "branch": "master", "note_count": 85, "sourced_count": 85, "ref_count": 247, "dangling_count": 0, "registry_id_count": 285, "finding_count": 0}
Independent oracle at base (my own Python, same fence rule, registry `^\| (S\d+) \|`): 85 operative source lines, 285 registry rows, 0 dangling. Unique-per-note id count = 247 (matches). Non-unique token count = 275.
Sandbox `git status` after checkout: only `?? tools/check-knowledge-refs-r68.py` (the copy). No `__pycache__` in the sandbox tools/.

## Attacks

Fixture repos were `git init` under scratch (toplevel asserted before every mutation). Commits A/B/C are fixture commits; the fixture never touched the lane.

1. **(a) Revision binding; committed bytes only — SURVIVES.**
   Lines 110-129 (`git cat-file -t` / `git show` at `sha:path`), 153-171 (registry read at `sha`), 282 (`_revision.bind`).
   Dirty-worktree probe: at commit B I wrote an uncommitted `p09` note citing `S555` and an uncommitted registry row `| S555 |`.
   $ python3 -B <draft> --revision <B> --lane <fx>  →  rc=1, p09 `refs ['S138','S149'] dangling []` (committed bytes).
   Binding refusal: `--revision HEAD` → rc=2, `{"id":"E-REVISION-INVALID","site":"revision","detail":"7-64 hex commit required"}`.

2. **(b) Fence skip identical to header gate — SURVIVES.**
   Lines 61 and 175-193 against header gate `FENCE` and `header_lines`: same state machine, same closing rule (`run[0]==fence[0] and len(run)>=len(fence)`, no info string). Lines 185-187 and 186 `line.strip()[len(run):]` match the header gate exactly.
   Cross-check on 8 fence probes (commit C), draft `source_line` vs `check-knowledge-header.py` `lines.source`: all 8 agree.
   `q1_quad_fence_nested` 8=8, `q2_closing_longer` 7=7, `q3_indented_opener` 4=4, `q4_unclosed_after_op` 3=3, `q5_crlf_fence` 6=6, `p12_indented_not_operative` None=None, `p15_last_wins` 8=8, `p17_tilde_fence_hides` 7=7.

3. **(c) Id regex; S-ids glued to other word characters — FALSIFIED.**
   Line 62: `ID = \bS\d{3,}\b`. The frozen C2 predicate (SCORECARD "Round 68 — declaration", C2 row) says the gate "extracts the `S\d{3,}` ids on the operative `source:` line". The draft's word boundary is narrower than the frozen predicate and silently drops these:
   - `source: own-work S999a` → `refs []`, `dangling []` (p01). `S\d{3,}` would extract `S999`.
   - `source: S138_S999` → `refs []` (p02). Neither `S138` nor `S999` is seen.
   - `source: own-work 1S999` → `refs []` (p03).
   Control that the item's wording allows: `source: own-work MS999` → `refs []` (p04). This is the (c) rule as the item states it (MS123 not an id), so it survives on its own terms; it is NOT an evasion of the frozen predicate, which would flag it.
   Non-evasion controls that pass correctly: `S138, S999` (comma, p06), `S138/S999` (p19), `S138+S999` (p20), `S999's` (p11), CRLF `S999\r` (p10). All extract `S999`.
   Fix direction for E1Probe: use the frozen `S\d{3,}` form (optionally `(?<![A-Za-z])`), and add a red selftest case `S999a` / `S138_S999`.

4. **(d-i) Registry read at the bound revision, not HEAD — SURVIVES.**
   Line 291 `registry_ids_at(repo, sha)`; line 155 `read_blob(repo, sha, REGISTRY)`.
   Probe: fixture A is the revision whose registry lacks `S999`. HEAD was then commit C (`e6016a4…`).
   $ python3 -B <draft> --revision <A> --lane <fx>  (HEAD = e6016a4)  →  registry_id_count 285, p18 dangling `['S999']`.
   The registry used is A's, not HEAD's.

5. **(d-ii) Registry parse ignores fences — FALSIFIED (fail-open).**
   Lines 163-167: `ROW.match` runs over every line with no fence state. `ROW = ^\|\s*(S\d{3,})\s*\|` (line 63).
   Probe: fixture B adds `` ```text / | S999 | fenced example row only | / ``` `` to `corpus/SOURCES.md`.
   $ python3 -B <draft> --revision <B> --lane <fx>  →  rc=1, `registry_id_count` 286 (base 285), `finding_count` 2 (was 9 at A).
   Every `S999` citation clears: p05 `<!-- S999 -->`, p06, p08, p10, p11, p18, p19, p20 all `dangling []`. The two remaining findings are p07 `S0001` and p14 `S٩٩٩`.
   One example row inside a fence is enough to disable the gate for that id across all notes.
   Fix direction: apply the same fence state machine (lines 175-193) to `registry_ids_at`, and add a red selftest case with a fenced registry row.

6. **(e) Id in a trailing comment on the source line — SURVIVES.**
   Line 192 keeps the whole value; line 204 scans all of it.
   p05 `source: own-work <!-- S999 -->` → `dangling ['S999']`. Comments are not stripped, so the id is counted (conservative).

7. **(f) Raw note text echoed into JSON — SURVIVES.**
   Output carries only: `source_line` as an integer (line 240), `refs`/`dangling` as id strings, and finding details built from the id and line number (line 209). Error details come from git stderr capped at 120 chars (lines 127, 135), not note text.
   Probe: a fake token `ghp_EXAMPLEFIXTURE000000000000000000` on the source line of p13.
   $ grep -c 'ghp_EXAMPLE' fxA.json  →  `0`.
   Residual: git stderr could echo a path (not content).

8. **(g) Writes / bytecode — SURVIVES for the run path.**
   Line 48 sets `sys.dont_write_bytecode` before the import of `_revision` (line 101). Only git read plumbing runs (`cat-file`, `show`, `ls-tree`, `rev-parse`, `merge-base`).
   After fixture runs: `find <fx> -name '__pycache__' -o -name '*.pyc'` → empty. `git status --porcelain --ignored` → clean (except intended dirt).
   Residual: `--selftest` uses `tempfile.mkdtemp` (line 397) with the inherited TMPDIR and removes it (line 500). The header gate does the same. Run with `TMPDIR` set explicitly: `tmp_left=0`.

9. **Unicode digits and tooling-level checks — SURVIVES (conservative false positive).**
   `\d` matches Unicode digits: `source: S٩٩٩` → `refs ['S٩٩٩']`, `dangling ['S٩٩٩']` (p14). This over-reports; it hides nothing.
   Selftest: $ TMPDIR=<scratch> python3 -B <draft> --selftest → rc=0, `{"selftest": {"cases": 19, "failures": [], "passed": 19, "status": "PASS"}}`. Its 19 cases do NOT include a glued-suffix case or a fenced-registry-row case, which is why attacks 3 and 5 pass its own selftest.
   Operative-line rule: p15 `source: S999` … later `source: S138` → operative line 8, `dangling []`. Matches the header gate.

## Verdict summary
ATTACKS=9. FALSIFIED=2 (attack 3 glued-id evasion vs the frozen `S\d{3,}` predicate; attack 5 fenced registry row fail-open). SURVIVES=7 (1, 2, 4, 6, 7, 8, 9). LIVE_BASE_RC=0. DRAFT=PRESENT.

Commands run (all read-only with respect to lane and fleet): `git cat-file/show/ls-tree/rev-parse/status`, `git clone --shared`, `git init`/`commit` in fixture repos under scratch only, `python3 -B` runs of the draft and the header gate, my own oracle. No sudo, no pacman, no service calls, no writes to the lane.
