DOES NOT MEET the C1 after-value: matches=0 of=24, harness_errors=[], exit=1.

1. [obs] Axes: coverage, control:junk. Exactly one census variant commit was created in the isolated sandbox: 5a3b40e5b320fc75688e171e92bb424a5fbc03f8, parent 6b4561e43e15c1cce038e390ad7d4691b0af4cc8. It changes only tools/tsukuroi-census.sh by appending three comment lines and an unused no-op function, tsukuroi_r35_junk_bytes() { :; }. It adds no pacnew/pacsave arm, input reader or output line. The original file lacks a final newline, so Git displays the unchanged final main invocation as a replaced line when showing this append. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes/junk-bytes.patch:1-19. The sandbox push URL was disabled before the variant was built. No lane source was edited.

2. [obs] Expected detector: the declared VERSION 1 counter must reject this control because the required drift line is absent; meeting the after-value requires matches=24 of=24, no harness errors and exit 0. Its predicate checks one drift line, all eight oracle fields, an allowed bounded census exit, and unchanged fixture bytes, modes and inode change times. The variant was scored exactly once, without --seed or --fixtures. Actual summary: {"exit_code": 1, "harness_errors": [], "matches": 0, "of": 24, "summary": 1}. The receipt footer records timed_out=false and empty stderr_tail. Its counter_sha256 is 19d25d14f9ee6ad15c036c75f997f2fba7aa756779c9e3b70a0ff136297e0155; census_sha256 is 3a9a8e9a683d86ea155da1e1c3934e2e6a3c4ed25541e363c04b4201965e31cc; fresh seed is 1072559743342611178. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes/junk-bytes.jsonl:1-2 and :27-28.

The exact variant scoring command, exit 1, was:
timeout 900 env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/run-receipt.py --lane /fast/scratch/hyaku/tsukuroi-r35/K02JunkBytes/repo --revision 5a3b40e5b320fc75688e171e92bb424a5fbc03f8 --tool-revision 6b4561e43e15c1cce038e390ad7d4691b0af4cc8 --out /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes/junk-bytes.jsonl --timeout 800 -- tools/score-pacnew-arm-r35.py --lane '{lane}' --revision '{rev}'

3. [obs] Per-fixture results follow. Every fixture has matches=false, reported=null and census exit=2, which is an allowed census exit under the predicate. The rejection reason is the missing drift line, not a harness error. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes/junk-bytes.jsonl:3-26.
Fixture 0: reason=drift_lines=0 (receipt line 3).
Fixture 1: reason=drift_lines=0 (receipt line 4).
Fixture 2: reason=drift_lines=0 (receipt line 5).
Fixture 3: reason=drift_lines=0 (receipt line 6).
Fixture 4: reason=drift_lines=0 (receipt line 7).
Fixture 5: reason=drift_lines=0 (receipt line 8).
Fixture 6: reason=drift_lines=0 (receipt line 9).
Fixture 7: reason=drift_lines=0 (receipt line 10).
Fixture 8: reason=drift_lines=0 (receipt line 11).
Fixture 9: reason=drift_lines=0 (receipt line 12).
Fixture 10: reason=drift_lines=0 (receipt line 13).
Fixture 11: reason=drift_lines=0 (receipt line 14).
Fixture 12: reason=drift_lines=0 (receipt line 15).
Fixture 13: reason=drift_lines=0 (receipt line 16).
Fixture 14: reason=drift_lines=0 (receipt line 17).
Fixture 15: reason=drift_lines=0 (receipt line 18).
Fixture 16: reason=drift_lines=0 (receipt line 19).
Fixture 17: reason=drift_lines=0 (receipt line 20).
Fixture 18: reason=drift_lines=0 (receipt line 21).
Fixture 19: reason=drift_lines=0 (receipt line 22).
Fixture 20: reason=drift_lines=0 (receipt line 23).
Fixture 21: reason=drift_lines=0 (receipt line 24).
Fixture 22: reason=drift_lines=0 (receipt line 25).
Fixture 23: reason=drift_lines=0 (receipt line 26).

4. [obs] The same bounded VERSION 1 detector also ran once on pristine bytes before the append and once on restored bytes after removing it, each using its normal fresh random seed and the committed-receipt form. Both used --revision 6b4561e43e15c1cce038e390ad7d4691b0af4cc8, with outputs pristine.jsonl and restored.jsonl respectively; all other scoring arguments were the same as above. Both returned matches=0 of=24, harness_errors=[], exit_code=1, with no runner timeout or stderr. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes/pristine.jsonl:27-28 and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes/restored.jsonl:27-28. [inf] Mutation verdict: inconclusive, not killed, because the pristine baseline already fails the after-value. As a pre-freeze negative control, the junk variant DOES NOT MEET the after-value; this is not a general counter-soundness claim.

5. [obs] Exact byte restoration is complete. Pristine and restored census SHA-256 both equal 7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5; the scored mutant equals 3a9a8e9a683d86ea155da1e1c3934e2e6a3c4ed25541e363c04b4201965e31cc. The counter hash stayed 19d25d14f9ee6ad15c036c75f997f2fba7aa756779c9e3b70a0ff136297e0155. These include a direct timeout 30 sha256sum observation of the worktree before mutation and after restoration, not only revision labels. The restored receipt deliberately reads the original candidate commit, whose bytes equal the restored worktree; the lone mutant commit remains available in the sandbox and no restoration commit was made. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes/restoration.txt:1-12 and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes/restored.jsonl:2. Every invoked command returned; no background jobs, services or package transactions were started.

Scope: read=godspeed and shokunin guidance, candidate declaration, lane QUALITY, pinned counter, receipt runner, census tail and seat receipts; wrote=/fast/scratch/hyaku/tsukuroi-r35/K02JunkBytes/repo (clone, one census-only commit and exact worktree restoration), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes/ (three receipts, variant patch and restoration evidence), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K02JunkBytes.md; executed=timeout-wrapped mkdir, git show/clone/checkout/remote/add/commit/rev-parse/diff, sha256sum twice, and run-receipt.py with score-pacnew-arm-r35.py once each for pristine, mutant and restored revisions
Model: openai-codex/gpt-6.1-sol
Installs: none
