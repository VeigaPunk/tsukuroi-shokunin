# CritClaimFraming2: round 31, wave 2 (falsify), claim framing of C1 and C2 at f3a5723a

Verdict: C1 fails as a depth target that a do-nothing control cannot reach. C2 holds as operability, and no wave-1 mutant undercuts the landed diff.

- **C1.** A fetched-but-not-read control (K6: the lane's own K3 junk rows plus one source-free dictionary word per sealed key group) scores `new_sourced` 8 of 8, exit 0, under the frozen counter. So the declared after-value cannot separate reading from fetching. Any depth credit rests only on the non-author per-row reviews. Those reviews are not in the frozen predicate, and no wave-2 row verdict had landed when I wrote this.
- **C2.** The fix changes a real result. Under an `LD_LIBRARY_PATH` that shadows git's `libpcre2-8`, `check-kernel-taint.py --selftest` fails 56 of 56 cases at the base and passes 56 of 56 at the tip, with the same stdout as an uninjected run.

## C1: depth

1. [obs] I reproduced the after-value at the revision under attack. Command: `python3 tools/check-btrfs-repair-r31.py --revision f3a5723a988bf1c2835985880e7a38d477462cd0 --lane /fast/scratch/hyaku/tsukuroi-r31/CritClaimFraming2/repo`. Result: exit 0, last line `"new_sourced": 8, "of": 8`, counter sha256 4f69a109…cb8. Receipt: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/CritClaimFraming2/c1-tip-f3a5723a.jsonl (sha256 b4ec4340…f726). `git diff --stat 13ca52d0 f3a5723a -- tools SKILL.md corpus PROVINCE.md` is empty, so the tip carries the same C1 and C2 bytes as the integration commit.
2. [obs] K3 fails on R7 alone. The committed K3 receipt (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/measure/controls/c1-K3-junk-real.jsonl, lines 2-9) shows that every one of the 8 rows fails only with `R7 sealed answer-key group N missing`. R1-R6 and R8 all pass. K3 is "a junk-row commit" in the declaration's own words (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:1211), and the hyaku addendum names exactly this class (kake r34, /home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-31.md:352-354). I rebuilt K3 with `git am` of `measure/controls/patches/0001-K3-junk-real.patch` on f4861f4d in a sandbox clone (commit aeb00a4b). It reads 0 of 8 with fail lists identical to the committed receipt (`diff` of the fail fields gives no output). Receipt: …/w2/CritClaimFraming2/c1-K3-rebuilt.jsonl.
3. [obs] **Strongest counterexample: K6 reaches the target.**
   - Build: on top of the rebuilt K3, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/CritClaimFraming2/k6_build.py` (sha256 b6febb04…b7dc) appends ` Words: <w1> <w2> …` to each junk statement.
   - Each word comes from a 90,870-word dictionary that opens no btrfs text: cracklib-small, the counter's own question texts and tokens, numbers 0-1000 crossed with 19 unit suffixes, and SKILL.md, PROVINCE.md and corpus/ at BASE 2077e2fa.
   - Script output: `{"dictionary_size": 90870, "groups_questions_only": 13, "groups_cracklib_only": 13, "groups_numbers_only": 4, "groups_lane_base_only": 17, "groups_recovered": 24, "missing": []}`.
   - Scored with `python3 tools/check-btrfs-repair-r31.py --revision 1d280a619097e70e55762ba74ebb6ad98ffaad16 --lane /fast/scratch/hyaku/tsukuroi-r31/CritClaimFraming2/k6` (tree 1d78dca6), K6 gives exit 0, every row `"new_sourced": true, "fail": []`, and summary `"new_sourced": 8, "of": 8`. Receipt: …/w2/CritClaimFraming2/c1-K6-fetched-not-read.jsonl (sha256 401e2d16…ef45).
   - The diff from K3 to K6 is one file, 8 changed lines. Each statement still reads "The <token> topic is recorded in this row of the lane for the record only and nothing more." followed by the word list (word list redacted here). The SKILL.md lines stay `<token> fixture line`.
   - Plaintext words stay only in the sandbox tree, never in the lane.
   - This confirms by execution what wave-1 CritKeyDictionary finding 7 predicted but did not run.
4. [inf] **Impact on §9.**
   - §9 requires "A target must be one a do-nothing control cannot reach" and "Declare each after-state as one concrete value that the closure can re-derive with one command over committed bytes" (/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-31.md:352 and :344-345). The one-command value, counter 8 of 8, is reached by K6, which skips the claimed work: decision lines a reader can act on, per AXES.md depth "no filler" (/home/vgpnk/Projects/shokunin/AXES.md:11).
   - The added cost over K3 is a dictionary lookup that needs no source.
   - The declared kill rule names only K0-K4 (SCORECARD.md:1211). K6 is built after data, so it cannot trigger the declared withdrawal. It does show that the declared value is not a depth measurement. This is the same failure class as round 30 (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-30-verifier-spotcheck.md, section 2), moved one step: then a sourceless forgery passed, now a fetched-but-unread forgery passes.
5. [inf] **"8 of 8 plus wave-2 per-row reviews".**
   - The reviews would reject K6, since its statements are filler, so the combination can tell K6 apart from real rows. But all of that discrimination sits in the reviewers, and their verdict is neither the frozen predicate nor a one-command value.
   - The declaration did assign row truth and usefulness to reviewers before data (SCORECARD.md:1211, the "Declared ceiling" sentence; counter docstring lines 37-41). Leaning on them is therefore not a target narrowed after data.
   - [unk] The per-row verdicts: when I wrote this, `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/` held only `swarm-registry.json` and this seat's files, so no RevRowQ01-Q08 report existed to check.
6. [obs] **Q04 integrator edit.** It changes one byte: a deleted space.
   - A field-by-field comparison of the scribe draft (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/ScribeSrcMountOpts/Q04-row.json) with the integrated row (corpus/knowledge/btrfs-repair-r31.json) gives `statement [('delete', ' ', '')]` and `keys_equal_otherwise True`. The SKILL.md line equals the scribe's Q04-skill.md.
   - The source spells the value the integrated way: `sed -n '38p' …/ScribeSrcMountOpts/ch-mount-options.rst | grep -cF "currently it's 64KiB)"` gives 1.
   - The as-drafted receipt reads 7 of 8 with Q04 `R7 sealed answer-key group 2 missing` (…/round-31/l1/c1-as-drafted-q04-sandbox.jsonl, line 5; finished 23:06:22Z). The after receipt at 13ca52d0 includes the edit.
7. [inf] **Judgement on Q04.** The edit preserves meaning and changes no rule, counter or target, so it is not a rule change after data. Process-wise, though, the 8th point exists only because the key holder edited a row after seeing a failing score. Under the frozen rule, the writer-produced state was 7 of 8, a miss. Two things limit the weight of this objection:
   - The counter prints which group is missing. Any writer could have found the same spelling by trying variants against that output and the source line, without the plaintext.
   - R7 here tests a number-plus-unit spelling ("64 KiB" against "64KiB"), not depth.

   So the edit is defensible but should be reported as "8 of 8 with Q04 integrator-repaired (as-drafted 7 of 8)". It does not change the C1 verdict, which already fails on K6.
8. **Impacted axes:** depth (the after-value does not measure the claimed surface) and calibration (lesson line 39 says "The seal is a format check, as the declared ceiling says"; K6 shows that the whole counter value, not just the seal, can be met without reading).
9. **Smallest safe correction (no rule, counter, target or probe change):**
   - Commit the K6 receipt beside K1 in the round record.
   - State plainly that the frozen counter's 8 of 8 is also reached by a fetched-but-unread junk-row control.
   - Credit C1 depth only as the number of rows that non-author reviewers pass for truth, usefulness and fact novelty, reported next to the counter's 8, not in place of it.

   Whether that count may stand in for a §9 one-command value is the canonical judge's call. On §9 as written, the declared depth target is one a do-nothing control reaches, and the judge should reject it as a depth move.

## C2: operability

10. [obs] **The after-value at the tip.** The frozen probe run at f3a5723a (`python3 tools/probe-git-child-env-r31.py --revision f3a5723a… --lane /fast/scratch/hyaku/tsukuroi-r31/CritClaimFraming2/repo --scratch …/probe-scratch`) was stopped by this seat's own `timeout 900` wrapper (exit 124), so it did not fail on its own and printed no summary line. Before that, 21 of 33 pairs had finished, all with `leak: False`: all three channels of check-adjacency-overlap, check-freshness-r17, check-kernel-taint, check-memory-pressure, check-registry-coverage, check-storage-health and mutants-adjacency-overlap (/fast/scratch/hyaku/tsukuroi-r31/CritClaimFraming2/c2-tip.jsonl). The tip reproduction is partial: 12 pairs were never run (mutants-kernel-taint, check-self-assessment and the two owed-statement batteries). The full 33-pair after receipt at 13ca52d0 reads `"leaking": 0`, `"harness_errors": []`, exit 0 (…/measure/after-13ca52d0/c2-declared.jsonl, last two lines). I saw no spurious dotgit-pointer verdict in the pairs I observed.
11. [obs] **Diff review of the landed fix.**
    - `git diff 8cff9e7c 13ca52d0 -- tools`: 13 files, 17 insertions, 13 deletions. Every changed line widens a name-prefix filter from `'GIT_'` to `('GIT_', 'LD_', 'PYTHON')` (counted with `grep '^[+-]' | sort | uniq -c`).
    - An `ast` scan of all 55 spawn calls (subprocess.run, Popen, check_output and so on) in the 13 files finds `without_env 0`. Each passes `env=` from one of the widened builders (`clean_env()` 17, `env` 20, `ENV` 10, `git_env…` 6, `_revision.clean_env()` 1, `clean_env(lane)` 1).
    - `grep -nE "LD_|PYTHON|realpath|TMPDIR|libprobe|git-child-env"` over the 13 files matches only the 13 filter lines.
    - So none of the hollow shapes in wave-1 CritProbeC2Design findings 1, 2, 4 and 5 is present: no realpath re-add, no padded value, no probe fingerprinting, no replay. The seven mutants that read 0 while children still get the injection do not undercut this after-value; they are probe blind spots, closed here by the diff review.
    - The q3-cc-bingit and q3-dp-read shapes are also absent. Every git call in the listed spawn sites uses bare `git` with `-C <repo>` (or `init <path>`, or `check-ref-format`, which needs no repository), and the probe pins `PATH=/usr/bin:/bin` (probe line 90).
12. [obs] **The fix changes a result the probe does not measure.**
    - `ldd` shows that /usr/bin/git loads `libpcre2-8.so.0` and `libz-ng.so.2`; /usr/bin/python3 loads neither.
    - With `LD_LIBRARY_PATH` pointing at a directory holding an empty `libpcre2-8.so.0`, `python3 tools/check-kernel-taint.py --selftest` behaves as follows:
      - base 8cff9e7c: rc=1, `"cases": 56, "failed": 56`, stderr `git: error while loading shared libraries: …/libpcre2-8.so.0: file too short`;
      - tip f3a5723a: rc=0, `"failed": 0`, stdout sha256 prefix b06bcb24…, identical to both uninjected runs.
    - Record: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/CritClaimFraming2/c2-libpcre2-shadow-demo.txt.
    - This is the AXES.md operability test, "A checklist item can be run and produces the stated outcome" (/home/vgpnk/Projects/shokunin/AXES.md:13): at the base, the tool cannot produce its outcome under a library path that only git consults; at the tip, it can.
13. [inf] **Operability, or re-scoring a held rule?**
    - The lane held "drop `GIT_*` names" (round 30). It did not hold loader or interpreter isolation, and the base tools fail under it (finding 12). The change is therefore new behaviour on the claimed surface, the child-process environment, not a held rule re-scored on new inputs (§9, prompt lines 361-363).
    - Errata item 3 says "None of the 11 base leaks changed an exit code, stdout digest or git exec count" (SCORECARD.md:1223). That is true of the probe's benign libm injection, not of the fix's effect.
    - Sizing caveats:
      - The counted value (`loader-env` 11 → 0) measures propagation, not harm.
      - The 22 guard pairs are 0 → 0 regression guards (errata item 3), not fixes.
      - The fix is one filter line in each of 13 files. The ordinal declared is 9 → 9, which is consistent with that.
    - [inf] A hidden-regression risk that I did not test: a host whose git needs `LD_LIBRARY_PATH` to start would now fail. On this host /usr/bin/git uses only system libraries, and the after receipt's parity checks pass.
14. **Impacted axes:** operability (holds); calibration (errata item 3's "not a changed result" undersells the fix; finding 12 is the counter-evidence).
15. **Smallest safe correction:** record finding 12's demo, or an equivalent, in the C2 notes as the result-level evidence. Keep the admission of `leaking 0` tied to the diff review in finding 11, because the probe alone cannot rule out the hollows in CritProbeC2Design findings 1-5. No probe change.

Scope: read=SCORECARD.md:1196-1229, corpus/lessons/round-31.md, tsukuroi-round-31.md:330-365, AXES.md, counter check-btrfs-repair-r31.py, probe header and targets, build-c1-controls.py, controls receipts K3 and the as-drafted Q04 receipt, w1 CritKeyDictionary.md and CritProbeC2Design.md, ScribeSrcMountOpts Q04 draft and ch-mount-options.rst:30-45, the 13 changed tools (grep and ast), the after-13ca52d0 C2 receipt; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/CritClaimFraming2.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/CritClaimFraming2/{c1-tip-f3a5723a.jsonl,c1-K3-rebuilt.jsonl,c1-K6-fetched-not-read.jsonl,k6_build.py,c2-libpcre2-shadow-demo.txt}, /fast/scratch/hyaku/tsukuroi-r31/CritClaimFraming2/ (clones repo and k6, exports t-base and t-tip, badlib, probe scratch); executed=sandbox git clone/checkout/am/commit (only in /fast/scratch/hyaku/tsukuroi-r31/CritClaimFraming2/k6), read-only git diff/archive/show/rev-parse, the C1 counter at f3a5723a (exit 0, 8 of 8), K3-rebuilt (exit 1, 0 of 8) and K6 (exit 0, 8 of 8), k6_build.py, the frozen C2 probe at f3a5723a (stopped by this seat's own timeout 900, exit 124: 21 of 33 pairs completed, 0 leaking), check-kernel-taint.py --selftest at base and tip with and without the libpcre2 shadow, ldd
Model: not exposed
Installs: none
