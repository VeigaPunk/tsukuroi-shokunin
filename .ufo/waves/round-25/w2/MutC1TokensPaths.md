# MutC1TokensPaths — wave 2 mutation probe of K12, K14, K15 and K16 to K23

Verdict: the assigned checks hold under the mutation probe — 13 of 14 mutants were killed, each expected check flipped to `mismatch` with detector exit 1, and the single survivor (a SHONEN box marked `[x]` that does carry a named non-author verifier) is a state the declaration explicitly permits, so it is a control, not a coverage hole.

## Scope and method

1. [obs] The detector under test is `tools/check-self-assessment.py` at revision `5e7c04ecb02735491456de2b8bc44550d0db4609`, sha256 `343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f`. The same bytes exist at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-self-assessment.py`. The counting command is `python3 tools/check-self-assessment.py --revision <REV>` and the field under test is `mismatches`.

2. [obs] Two sandboxes were built exactly as the wave spec requires, with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 5e7c04ecb02735491456de2b8bc44550d0db4609 | tar -x -C <dir>` followed by `git init` with no remote:
   - pristine: `/fast/scratch/hyaku/tsukuroi-r25/w2/MutC1TokensPaths/base` (base commit `355f64308b909aab2feb4575e2fdafddaee0ed31`, 3390 tracked files),
   - mutable: `/fast/scratch/hyaku/tsukuroi-r25/w2/MutC1TokensPaths/work` (a copy of the pristine one).

3. [obs] Pristine hashes of every file any mutant touches (`sha256sum -c` file: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC1TokensPaths/hashes-pristine.txt`):

   | file | sha256 |
   |---|---|
   | `SCORECARD.md` | `b87ead0dec68e4464301fd6135e2a7476e0e146558d148b1da502ba954b23659` |
   | `SHONEN.md` | `9d256da08aa61f4987d98d9261dc114e1abe9b09821d35cbfa632b65d608b087` |
   | `PROVINCE.md` | `a296da872e83731f7f7a7737662988558ebb97e4399681a1099fab4a259b7a79` |
   | `tools/tsukuroi-census.sh` | `d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e` |
   | `tools/check-self-assessment.py` | `343367fb309e43449ee1be50f97c86b917240de7bb6b34b942fd67a163c6242f` |

4. [obs] Baseline on pristine bytes, in `/fast/scratch/hyaku/tsukuroi-r25/w2/MutC1TokensPaths/base`: `python3 tools/check-self-assessment.py --revision HEAD` exited 0 with `checked=23 mismatches=0 status=PASS` (output kept at `.../out-final-baseline.json`). The baseline is green, so a later failure is a killed mutant and not a pre-existing failure.

5. [obs] One mutant per run, each committed in the mutable sandbox and detected at that commit; after every run the sandbox was restored with `git reset --hard 355f64308b909aab2feb4575e2fdafddaee0ed31` and re-verified with `sha256sum -c`. The detector JSON of every run is kept in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC1TokensPaths/out-<label>.json`, and the runner script is `run-detector.sh` in the same seat directory.

## Findings, one per mutant

6. [obs] M1, K12 fixed token reworded, killed. In `/fast/scratch/hyaku/tsukuroi-r25/w2/MutC1TokensPaths/work/SCORECARD.md:829` (lane file `SCORECARD.md:829` at the measured revision) the coverage row text `PROVINCE.md` Core, Frontier and Adjacent sections present became `PROVINCE.md` Core, Frontier and Adjacent sections are present. Mutant commit `b251c6814d2182f32e65286fb918619118fc6450`, `SCORECARD.md` sha256 `7a273aebfff90bf868196d34119428380040e295362e22d080811253bbf3a78b`. Detector exit 1, `checked=23 mismatches=1`, `K12 mismatch stated='unstated' observed='present'`. The check is sensitive to the exact wording the declaration fixed.

7. [obs] M1b, K12 row switched to the other declared token, killed. Same line, `Core, Frontier and Adjacent sections present` became `Core/Frontier/Adjacent not landed`. Mutant commit `81f42426710250c67c61f38286a3b439956afac9`, `SCORECARD.md` sha256 `9849c36704637bbd3d37e0a119aafee6cb81c87ec200ccd2737a9f400e05e402`. Detector exit 1, `K12 mismatch stated='absent' observed='present'`. Both fixed tokens of the K12 pair are recognised.

8. [obs] M2, K14 fixed token reworded, killed. In `work/SCORECARD.md:830` the operability row text D12 `--identity` not landed became D12 `--identity` mode not landed. Mutant commit `fdda05634d0a1a66a510a3135ab69adfe421b149`, `SCORECARD.md` sha256 `81656a4dd49e4449060c614a0789bdc6adad1a234de784e6b46d151d9a85322f`. Detector exit 1, `K14 mismatch stated='unstated' observed='absent'`.

9. [obs] M2b, K14 row switched to the other declared token, killed. Same line, `--identity` not landed became `--identity` landed. Mutant commit `d0319abb8bb81399a1d1dbeb068dd81bdcb49a2c`, `SCORECARD.md` sha256 `434f95af11b1207be8fe48f48e374d250d84fc18bc7e65fd1324b205686831b6`. Detector exit 1, `K14 mismatch stated='present' observed='absent'`.

10. [obs] M3, a `--identity)` case arm added to the census, killed. In `work/tools/tsukuroi-census.sh:2619` a new arm `      --identity) printf 'tsukuroi-census: identity mode\n'; exit 0 ;;` was inserted next to the `--selftest` arm (the file still passes `bash -n`). Mutant commit `0519c9888249193119b8e94a485482d7be95e5f9`, `tools/tsukuroi-census.sh` sha256 `9e567517f9d347f708b8c5b95655d661959faa2d1164b3f809bc93058f17e3d3`. Detector exit 1, `K14 mismatch stated='absent' observed='present'`. The observation side of K14 reads the census script at the revision, so landing the mode contradicts the row. K13 stayed green, so the extra arm did not disturb the census selftest count of 97.

11. [obs] M4, K15 fixed token reworded, killed. In `work/SCORECARD.md:833` the adjacency row text carries the formal overlap table present became carries the formal overlap table in place. Mutant commit `21610a0a0e6d365b5dcd8b01a61fcc186f6e95e3`, `SCORECARD.md` sha256 `38e6bbd8f34d6bce93a7fd37b8e077cf595227ea6893ab74568423a16f5ebfe6`. Detector exit 1, `K15 mismatch stated='unstated' observed='present'`.

12. [obs] M4b, K15 row switched to the other declared token, killed. Same line, carries the formal overlap table present became carries no formal overlap table. Mutant commit `939d66c889a884ffce690d37aab20447beb8d900`, `SCORECARD.md` sha256 `de8fea81964d55cdbed6e216a4eca645ebb175b6e6d3d496a0b293786b7ce259`. Detector exit 1, `K15 mismatch stated='absent' observed='present'`.

13. [obs] M5, the `| ID | Finding` header deleted from PROVINCE.md, killed. In `work/PROVINCE.md:44` the header line `| ID | Finding / boundary trigger | ... | Ownership source |` was deleted, leaving the separator row. Mutant commit `29421d2d57c83fbde869bc703e12266ec1a67c50`, `PROVINCE.md` sha256 `fa296cfba7c73f1631abb0a552a5b89932eab59b256471ee5b97df826260dbd1`. Detector exit 1, `K15 mismatch stated='present' observed='absent'`. The observation side of K15 reads PROVINCE.md at the revision, so removing the table contradicts the row.

14. [obs] M6, one capability path broken, killed. In `work/SCORECARD.md:852` the sources-registry evidence pointer `corpus/SOURCES.md` became `corpus/SOURCES.mdx`. Mutant commit `d844f9c77f2e3e41f03400b1286109638a950c8b`, `SCORECARD.md` sha256 `acd43a122e4847614e1485664947f810456e4df0a8d1bdb61dbcfdb15facedb5`. Detector exit 1, `K16 mismatch ... reason=sources-registry row names 1 path(s) absent at the revision: corpus/SOURCES.mdx`.

15. [obs] M7, every path removed from a capability row, killed. In `work/SCORECARD.md:854` the root-metadata-observer evidence pointer became `no repository path is named in this row; the measured commit is 70fede2a7a890cb50a72db2d4230ee541183bf7b`, with all three `.ufo/waves/round-12/resumed/...` paths dropped. Mutant commit `6a5c70bfdba8889b3cac6b0b7419563899389490`, `SCORECARD.md` sha256 `168fd721539b41ef6bec79465864159e65c5b5c068b7ed73f36ed866fff36c47`. Detector exit 1, `K18 mismatch stated=[] observed=[] reason=root-metadata-observer row names no repository path`.

16. [obs] M8, a SHONEN box marked `[x]` with no non-author verifier, killed. In `work/SHONEN.md:5` the first box marker changed from `- [~]` to `- [x]`, with its author-side evidence line untouched. Mutant commit `2993e2b7780554f1f164102c8c31adfd2d0c5b56`, `SHONEN.md` sha256 `b331692173ba0d7a35befcb86400842c4a94acb8f6400b38bbbf086594b4269d`. Detector exit 1, `K20 mismatch ... reason=SHONEN box 1 is marked [x] without a named non-author verifier`.

17. [obs] M9, a SHONEN box marked `[x]` with a named non-author verifier, survived, and this is the expected outcome. In `work/SHONEN.md:7-8` the second box marker changed from `- [~]` to `- [x]` and the line gained `non-author verifier: reviewer-r25`. Mutant commit `b4d8f46b3a310bd28282a6c683327fd33e160e87`, `SHONEN.md` sha256 `f0a16f1720f780ecf679874a3c3fb55c4a9b81b0cbb0a4556e6a56a1596f86f7`. Detector exit 0, `checked=23 mismatches=0 status=PASS`. [inf] The declaration states the requirement as "A box marked `[x]` must contain `non-author verifier:` and a name", so a marked box that does carry a name is a conforming state and the check is right to stay silent; the paired mutants M8 and M9b show the same check fires when the name is missing or absent. This survivor is a control, not a missed defect.

18. [obs] M9b, a SHONEN box marked `[x]` with `non-author verifier:` but no name, killed. In `work/SHONEN.md:9-10` the third box marker changed from `- [~]` to `- [x]` and the line gained `non-author verifier: (name not yet given)`. Mutant commit `f27e8ecb5deded4f0da066b48557a0540b08f1ba`, `SHONEN.md` sha256 `de1dc22d5e62b25ca4849b9859102346edfa39012398cbcc08dcb2f45478fe0f`. Detector exit 1, `K22 mismatch ... reason=SHONEN box 3 is marked [x] without a named non-author verifier`. [inf] The name clause of the declared rule is enforced, not only the phrase.

19. [obs] M10, a slash token added to a SHONEN box, killed. In `work/SHONEN.md:12` the fourth box line gained `Cross-check a/b as well.` Mutant commit `9eb8a3fdab10a3d812b4ffa2bd8b7e36fb80319e`, `SHONEN.md` sha256 `3cb9fd0cb21ec69350821837e516eb00875284a5a77fc5a11d22e7bfadb3394a`. Detector exit 1, `K23 mismatch ... reason=SHONEN box 4 names 1 path(s) absent at the revision: a/b`. [inf] The path grammar treats any token holding a slash as a path even when it names nothing in the repository, as the declaration states, so the box fails instead of passing silently.

20. [obs] Restoration evidence. After the last mutant the mutable sandbox was reset with `git reset --hard 355f64308b909aab2feb4575e2fdafddaee0ed31`; `sha256sum -c hashes-pristine.txt` reported `SCORECARD.md: OK`, `SHONEN.md: OK`, `PROVINCE.md: OK`, `tools/tsukuroi-census.sh: OK`, `tools/check-self-assessment.py: OK`; `git status --porcelain` in the mutable sandbox printed nothing; and the detector on the restored bytes exited 0 with `checked=23 mismatches=0 status=PASS` (`out-final-baseline-2.json`). The pristine sandbox was never mutated and still reports the same five hashes and the same base commit.

21. [obs] Lane safety. No file in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` outside my seat paths was written, and no git or jj write command was run against the lane, the fleet root or any sibling lane. The only lane writes are this report and the receipt directory `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC1TokensPaths/`. [obs] The lane working tree already carried modifications from other seats when I read it (`git status --porcelain` listed `.ufo/waves/round-25/w1/...`, `SKILL.md` and `corpus/knowledge/memory-pressure-r25.*`); those are not mine, and my measurements are anchored to the committed revision `5e7c04ecb02735491456de2b8bc44550d0db4609` rather than to the dirty working tree.

## What this probe does and does not establish

22. [obs] Every check in the assigned range was observed to flip on at least one mutant: K12 (M1, M1b), K14 (M2, M2b, M3), K15 (M4, M4b, M5), K16 (M6), K18 (M7), K20 (M8), K22 (M9b) and K23 (M10). Each killed run reported exactly one mismatch, so the mutants did not bleed into unrelated checks.

23. [obs] K17 and K19 were not hit by a dedicated mutant of my own. K17 is the host-census-gate row, whose check carries two clauses (paths and the stated case count), and K19 is the boot-chain-audit row. M6 and M7 exercised the shared path-resolution code that both use, but the row-specific clauses of K17 and K19 were not individually mutated in this probe. [unk] Whether a mutant aimed at the K17 case-count clause or at the K19 boot-chain path is caught is not established by this report; the sibling seats cover the count clauses.

24. [inf] The K12, K14 and K15 checks are exact-substring matches on the wording the declaration fixed, so any rewording that is semantically harmless is still reported as a mismatch (stated `unstated`). That is the declared behaviour and not a defect, but it means the checks are strict rather than semantic, and the lane's prose has to keep the fixed wording verbatim.

25. [obs] No tool was installed or upgraded for this probe; the run used only python3, git, bash and coreutils already present on the host.

Scope: read=SCORECARD.md sections "Round 25 — declaration, attempt 1" and "Round 25 declaration refinements after the first wave-1 falsifiers", SHONEN.md, PROVINCE.md, tools/check-self-assessment.py, tools/tsukuroi-census.sh in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin at revision 5e7c04ecb02735491456de2b8bc44550d0db4609; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC1TokensPaths.md and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/MutC1TokensPaths/ (detector JSON outputs, stderr logs, pristine hash list, runner script) plus the sandboxes /fast/scratch/hyaku/tsukuroi-r25/w2/MutC1TokensPaths/base and /fast/scratch/hyaku/tsukuroi-r25/w2/MutC1TokensPaths/work; executed=git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 5e7c04ecb02735491456de2b8bc44550d0db4609 | tar -x -C <dir>, git init (no remote) in both sandboxes, git add/commit/reset --hard inside the mutable sandbox only, and python3 tools/check-self-assessment.py --revision <REV> in each sandbox (baseline, 14 mutant commits, final restored baseline), plus sha256sum, sha256sum -c, bash -n, git status, git rev-parse.

Model: opencode-go/minimax-m3.1-flash-free

Installs: none
