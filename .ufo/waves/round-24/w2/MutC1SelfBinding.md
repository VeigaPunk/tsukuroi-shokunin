# Round 24 wave 2 — MutC1SelfBinding (claim C1, self-binding)

Verdict: C1's self-binding survives the working-tree drift attack — an uncommitted edit to
`tools/report-red-causes.py` is detected and the command exits 2 with the
`working-tree report tool differs from the revision blob` message, and the absent-tool
message still fires at `f169b3ba`. The second probe is a surviving mutant: a committed edit
that weakens `preserved` by dropping the incomplete-seat requirement passes the selftest
11/11, so the selftest does not catch that weakening (coverage finding; not a license to
change the contract). The measured claim (268/268 at 22fd1642, exit 0) is not falsified.

## Findings

1. [obs] Self-binding implementation. `run()` reads the tool's own blob at the bound
   revision (`git_blob(binding.sha, SELF)`, report-red-causes.py:190) and compares it to
   the working-tree bytes; on mismatch it raises
   `working-tree report tool differs from the revision blob` (lines 193-194), which
   `main()` converts to exit 2, status `CANNOT_EVALUATE`, finding `RED-CAUSES-READ`
   (lines 282-284). If the blob is absent at the revision, the earlier branch raises
   `tools/report-red-causes.py is absent at this revision` (lines 189-192).
   Evidence: /fast/scratch/hyaku/tsuku24w2-MutC1SelfBinding/lane/tools/report-red-causes.py:187-194, 278-286.

2. [obs] Pristine baseline reproduced the measured outputs. From the clone at
   22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0 (clean tree, master):
   `python3 tools/report-red-causes.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`
   exited 0, `preserved` true, `attributed_findings` 268/268, `split_matches` true,
   `incomplete_seat_is_frozen` true, `pin_mismatches` [] — matching
   .ufo/waves/round-24/measure/c1-22fd1642.json. The same command at
   `f169b3ba9a59abaf3e324c1b591e1e07a4d6003a` exited 2 with
   `{"status":"CANNOT_EVALUATE","findings":[{"id":"RED-CAUSES-READ","site":"tools/report-red-causes.py is absent at this revision"}]}` — matching .ufo/waves/round-24/measure/c1-f169b3ba.json.
   `--selftest` exited 0, PASS 11/11. Evidence: /fast/scratch/hyaku/tsuku24w2-MutC1SelfBinding/pristine-r22fd.json, pristine-rbase.json, pristine-selftest.json (exit codes recorded in the run transcript).

3. [obs] Probe A — uncommitted working-tree mutation is detected (self-binding survives).
   Added one comment line inside the tool's docstring (behavior-neutral; file sha256
   39df60410936111bb423cd43691537360553dba49a4deb67a27682722991ec08 →
   e4744ffef4dc3001ce13f674ebe371e449dfde273f01741e088c1df25ffb50e8) and reran:
   `python3 tools/report-red-causes.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`
   exited 2 with
   `{"status":"CANNOT_EVALUATE","findings":[{"id":"RED-CAUSES-READ","site":"working-tree report tool differs from the revision blob"}]}`.
   The same mutated working tree at `f169b3ba` exited 2 with the absent-tool message
   (the absent-tool branch runs before the working-tree comparison, so base behavior is
   unchanged by the mutation). W: /fast/scratch/hyaku/tsuku24w2-MutC1SelfBinding/mutated-r22fd.json, mutated-rbase.json.

4. [obs] Probe B — committed weakening of `preserved` survives the selftest. A committed
   edit (clone branch `mut-p1-selfbind`, commit 23fb655) replaced line 180
   `and result.get('status') == 'CANNOT_EVALUATE' and bool(incomplete)`
   with
   `and result.get('status') == 'CANNOT_EVALUATE'`,
   dropping the requirement that the trace contain at least one incomplete seat
   (`bool(incomplete)`, where `incomplete` collects seats with `complete` False, line 155-156).
   `python3 tools/report-red-causes.py --selftest` exited 0 with
   `{"status":"PASS","cases":11,"failed":0,...}` — the selftest does not catch the
   weakening. The `incomplete-seat-dropped` fixture (line 229) still returns 1 only
   because, with the seat marked complete, the `SCOPE-TRACE-INCOMPLETE` finding becomes
   unattributed and trips `attributed == total` (lines 142-151, 179); no fixture exercises
   the `bool(incomplete)` clause independently, so removing it is invisible to the
   selftest. Evidence: /fast/scratch/hyaku/tsuku24w2-MutC1SelfBinding/weakened-selftest.json, committed-weakened-sha1.txt (sha256 9a6362200fb7a59906755620c75d58e6f9fa24a5d1bbf02982b11539dbf090d4).

5. [obs] Interaction with self-binding: from the committed-but-unpushed weakened state,
   `--revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0` still exits 2 with the
   `working-tree report tool differs` message (weakened-r22fd.json), so the declared
   counting command can only ever execute the frozen-cohort tool bytes; the `preserved`
   weakening cannot be observed through the claim's own command, and the selftest, the
   only other detector, also passes. The measured 268/268 therefore remains truthful even
   while `preserved` semantics are weaker.

6. [inf] Smallest corrections. (a) Self-binding: none needed — probe A shows it behaves as
   declared. (b) Selftest coverage gap: add a fixture in which all other `ok` clauses hold
   but the trace has no incomplete seat (e.g. `base` minus the `SCOPE-TRACE-INCOMPLETE`
   entry, `trace(True)`, status `CANNOT_EVALUATE`, code 2, unknown-key site present,
   recollection intact) and expect `attribute()` to return 1; with that fixture, dropping
   `bool(incomplete)` would fail the selftest. Alternatively, assert
   `preserved and incomplete_seats` directly in `selftest()`.

## Restoration evidence

After probe A: `git checkout -q -- tools/report-red-causes.py` restored sha256
39df60410936111bb423cd43691537360553dba49a4deb67a27682722991ec08 (byte-identical to
pristine, restored-sha1.txt). After probe B: switched back to master at 22fd164 (the
landed commit), deleted branch `mut-p1-selfbind`; final sha256 identical to pristine
(final-restored-sha1.txt) and `git status --short` empty. No fleet-repo file was written or
edited; all mutations and git writes occurred only in
/fast/scratch/hyaku/tsuku24w2-MutC1SelfBinding/lane.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md (round-24 declaration and refinements), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/{ExecRedCauses,RevC1Attribution,CritC1Construction}.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/measure/{c1-22fd1642,c1-f169b3ba}.json, clone tools/report-red-causes.py and tools/_revision.py at 22fd1642 (via /fast/scratch/hyaku/tsuku24w2-MutC1SelfBinding/lane), /home/vgpnk/.omp/agent/RULES.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/MutC1SelfBinding.md, probe artifacts under /fast/scratch/hyaku/tsuku24w2-MutC1SelfBinding/ (pristine/mutated/weakened JSON runs, sha1 records, clone); executed=git clone, git checkout -q 22fd1642, git status (read-only), git show via tool internals, python3 tools/report-red-causes.py --revision 22fd1642 (exit 0 pristine / exit 2 mutated and weakened), --revision f169b3ba (exit 2, absent-tool message), --selftest (exit 0, 11/11 pristine and weakened), git checkout -- restore, git switch/git branch -D/git commit in the scratch clone only.
Installs: none
