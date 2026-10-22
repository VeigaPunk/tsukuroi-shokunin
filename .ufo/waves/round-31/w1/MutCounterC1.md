# MutCounterC1 — mutation test of the C1 frozen counter (round 31, wave 1)

Verdict: holds with one coverage hole — twelve of thirteen mutations are killed by at least one
fixture, and the single survivor is dropping the R8 novelty check (`M08-drop-R8`), which cannot
fire for any fixture because the counter's own frozen token list has zero hits at BASE; two
legitimacy findings came out of building the positive fixture, one of which (the sealed answer
keys are recoverable in one pass over the committed snapshots) was already declared as a ceiling
and is now measured.

## Method and fixtures

1. [obs] Sandbox clone at the revision under work: `/fast/scratch/hyaku/tsukuroi-r31/MutCounterC1/repo`
   is `git clone --no-local` of the lane, `HEAD = 8cff9e7cfb034b49c645d548801ac3185a827cb4`. All
   git runs were prefixed `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE` and every write
   landed under `/fast/scratch/hyaku/tsukuroi-r31/MutCounterC1` or the seat dir. No git write was
   run in the lane or the fleet repo.
2. [obs] The six pinned snapshots were fetched from
   `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/<file>` and their bytes
   match the counter's pins exactly (sha256, saved under
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/MutCounterC1/snap/`):
   Defragmentation.rst `71ad07a3f200284b01d6ee18fc4cc8732fe0542b80556e2cc798247505daa60b`,
   btrfs-rescue.rst `838504fe8b00d221e017457e7953717f3ca2a0e886a48a4c457367b8c4063a1d`,
   btrfs-check.rst `927b67b4ab13f681866e699fcd6ea4917a42ef08e4db1731b0adf065022d955c`,
   ch-mount-options.rst `aac3b1b68ba55259f6c2b8e6d1e30e41560eaee3b0f4863af58387271bc9985f`,
   btrfs-replace.rst `da4bf595f072a96a309535c1022b0171a8657a4f207a3d3da73250886fd8bc9e`,
   Trim.rst `2a114d56f29d727002a981e868cc97e89d7dd77a5e1cf42ad5a9ff05bfcf0ffc`.
3. [obs] The committed controls were rebuilt with the committed builder
   (`--toolrev 8cff9e7cfb034b49c645d548801ac3185a827cb4`, `--snapdir` the six files above):
   `K2-restate-r30 = 1558cedc14349b2bd196cf37706f552a9644e25a`,
   `K3-junk-real = 9f4a219ac313c17ff5c5f077398c77acf84d9857`,
   `K4-quote-copy = 9d17d2c2d152b2b590d1dab9003f24f7c2bb8a64` in
   `/fast/scratch/hyaku/tsukuroi-r31/MutCounterC1/work/c1-controls`. The sealed controls were
   reused from the existing sealed clone (read-only): `K1-sourceless-forged =
   bf2c014aff4dad845e66c3f322dfd4617ee2d896`, `K5-reader-ceiling =
   92cdff13496762c89e1baa2681b8baccb1cf8ed3`.
4. [obs] My own positive fixture `P1-my-positive = 5175b34c16452cba25f99840f92268d5bff9b5b2`
   (builder `build-my-positive.py`) places the six real snapshots under
   `.ufo/waves/round-31/mutc1/`, adds S164–S169 `mined` registry rows with the frozen URL and
   sha256, one `| [R31-Qnn] ` SKILL.md line each, and statements I wrote from the fetched bytes,
   e.g. Q01 "Defragmentation rewrites the layout of a file's extents and breaks the sharing of
   those blocks, so a file copied with reflink or held in several snapshots will afterwards
   consume more data space than before." It reads **8 of 8** under the unmutated counter
   (`--revision 5175b34c… --lane …/work/c1-fixture`, exit 0).
5. [obs] Seventeen one-rule-violating fixtures were derived from P1 through `git show` of the
   pristine commit (never from the mutating working tree), each tripping exactly one rule:
   `N-R1dup 2f626789…`, `N-R1extra 9da5b965…`, `N-R2 613fb42a…`, `N-R3sha 0d5e86a3…`,
   `N-R3path 9e0904dd…`, `N-R4line ff0c3a52…`, `N-R4words 618dfda5…`, `N-R5status 6c14033f…`,
   `N-R5count e92c1eac…`, `N-R5base 45f2425a…`, `N-R6skill cc196300…`, `N-R6fence a5f0307c…`,
   `N-R6comment fc57db2f…`, `N-R7key 0c054acc…`, `N-R7run6 c70b7c5d…`, `N-R7run5 838d7d72…`,
   `N-pinprefix 486cba97…` (builder `build-negatives.py`).
6. [obs] Baseline scores under the unmutated counter (`baseline-table.md`, `mutant-results.json`):
   K0-base 0, K1-sealed-forged 0, K2-restate-r30 0, K3-junk-real 0, K4-quote-copy 0,
   K5-sealed-positive 8, P1-my-positive 8; every N-fixture 7 except N-R1extra 0 and N-R7run5 8.
   The K5 read of 8 independently reproduces the committed K5 receipt.

## Mutants (each applied to a copy of the counter, one exact-substring edit each)

7. [obs] Results, from `mutant-table.md` (per-mutant files and diffs under `mutants/<name>/`):

| mutant | killed | fixture (baseline -> mutant) |
|---|---|---|
| M01-drop-R1 (duplicate/extra-id checks removed; a missing row still fails) | yes | N-R1dup (7->8), N-R1extra (0->8) |
| M02-drop-R2 (row-key set check) | yes | N-R2 (7->8) |
| M03-drop-R3 (whole path/existence/pin block) | yes | K1-sealed-forged (0->7), N-R3sha (7->8), N-R3path (7->8), N-pinprefix (7->8) |
| M03b-weaken-pin (sha256 comparison truncated to 4 hex chars) | yes | N-pinprefix (7->8) |
| M04-drop-R4 (quote length, line int, quote-at-line) | yes | N-R4line (7->8), N-R4words (7->8) |
| M05-drop-R5 (whole source/registry block) | yes | N-R5status (7->8), N-R5count (7->8), N-R5base (7->8) |
| M05b-weaken-base-registry (only the "row exists at base" check removed) | yes | N-R5base (7->8) |
| M06-drop-R6 (SKILL.md line count and the three token checks) | yes | N-R6skill (7->8), N-R6fence (7->8), N-R6comment (7->8) |
| M07-drop-R7 (12-word floor, sealed groups, 6-word run) | yes | K3-junk-real (0->8), K4-quote-copy (0->8), N-R7key (7->8), N-R7run6 (7->8) |
| **M08-drop-R8 (base novelty hits)** | **SURVIVOR** | none |
| M09-window-7 (6-word window -> 7) | yes | N-R7run6 (7->8) |
| M10-window-5 (6-word window -> 5) | yes | N-R7run5 (8->7) |
| M11-drop-fence-comment-skip | yes | N-R6fence (7->8), N-R6comment (7->8) |

8. [obs] Survivor `M08-drop-R8` — the mutant diff is exactly the removal of
   `for tok in q['tokens']: if hits[tok]: fail.append(...)` (`mutants/M08-drop-R8/mutant.diff`,
   mutant sha256 `607833351ee845ee…`). Cause: R8 is evaluated only against the counter's frozen
   token list and BASE, so its verdict is constant per question and no fixture can change it. I
   measured all 14 frozen tokens at BASE with the counter's own `git grep -i -F -c … 2077e2fa -- SKILL.md PROVINCE.md corpus`: `defragment 0, reflink 0, zero-log 0, log tree 0, --repair 0,
   autodefrag 0, defragmentation 0, commit= 0, periodic transaction commit 0, nodatacow 0,
   nodatasum 0, btrfs replace 0, replace start 0, fstrim 0`. So R8 can never fail for any
   revision a writer could produce, and its removal costs nothing — a coverage finding about R8,
   not permission to change the contract (the rule stays as frozen).
9. [obs] The mutants are not score-neutral by accident: dropping R1 does **not** rescue the
   do-nothing base (K0 stays 0, M01's `changed` map lists only N-R1dup and N-R1extra), dropping
   R3 promotes the sealed sourceless forgery from 0 to 7, and dropping R7 promotes both junk
   controls from 0 to 8. R7 is the load-bearing rule for K3/K4; R3 for K1.
10. [obs] Both window mutations and both weakened checks are discriminated by construction rather
    than by luck: `N-pinprefix` is Trim.rst with an appended `<!-- pad 166 -->` line whose sha256
    begins `2a118931` (4 hex shared with the pin, full digest `2a118931ff99f2e9…`, 167 grind
    iterations), and `N-R7run5`/`N-R7run6` append exactly 5 and 6 consecutive quote words to an
    otherwise passing statement.

## Legitimacy findings about the counter itself

11. [obs] The sealed answer keys are recoverable from the counter's own committed material in one
    pass: computing `sha256('tsukuroi-r31 ' + word)[:16]` for the 1721 distinct words of the six
    pinned snapshots (plus their `-`/`/`/`.` pieces) resolves **24 of 24** answer-key groups
    (`keymap.py`, `keymap.json`), e.g. Q07 group 1 = `devid`, Q05 group 3 = `300`, Q08 group 2 =
    `discard=async`. 1721 hashes is under a second. This corroborates the declaration's own erratum
    `SCORECARD.md:1220` (wave-1 CritKeyDictionary, 24 of 24 from a 103,090-word source-free
    dictionary) and sharpens it: no external dictionary is needed at all, the vocabulary is in the
    same commit's `.ufo/waves/round-31/` snapshots. The declared sentence "a writer who skips the
    source cannot copy them from this file" is therefore weaker than stated, as that erratum says.
    Row truth and novelty remain with the wave-2 per-row reviews; I changed no rule.
12. [obs] A legitimate reader's vocabulary does hit R7 without any digest work: my statements were
    written from the fetched bytes and the first scoring run of P1 (before I fixed my own builder
    bug) already passed every sealed group for all eight questions — its only failures were
    `R5 3 registry rows for S167` on Q04/Q05/Q06. So R7 is not a barrier to an honest writer.
13. [obs] Erratum `SCORECARD.md:1220` says K1 "scores 0 because of the snapshot pin (R3), not the
    seal"; the mutation matrix confirms it independently — dropping R3 (M03) lifts K1 from 0 to 7,
    while dropping R7 leaves K1 at 0, so the pin is the only thing holding the sourceless forgery
    down.


14. [obs][inf] A writer trap worth naming: three of the eight questions cite ch-mount-options.rst,
    so they must share exactly one S167 registry row; my builder emitted one row per question and
    the counter refused three otherwise-correct rows (`R5 3 registry rows for S167`, score 5 of 8).
    The rule is right and the message names the id, but the shape is only implied by the counter.

## Restoration and containment evidence

15. [obs] No lane file was modified. Lane counter and sandbox counter are byte-identical to the
    frozen tool: `sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-btrfs-repair-r31.py`
    = `4f69a109e9b56b3fcba0df5a3555f7ff833b6b04fff28176060efe82ebde5cb8` = the `counter_sha256` in
    the committed K0–K5 receipts, and `git -C <lane> status --porcelain -- tools/check-btrfs-repair-r31.py`
    is empty. Mutations exist only as copies under the seat dir; nothing was applied in place.
16. [obs] The mutants, the results table, the fixtures' builders, the keymap and the imported
    snapshots are committed in my sandbox clone only:
    `6232007dbdcdad4acd064ca8d0af16eb60a08637` on branch `mutc1` at
    `/fast/scratch/hyaku/tsukuroi-r31/MutCounterC1/repo`, path
    `.ufo/waves/round-31/w1/MutCounterC1/…`; the same content is exported as
    `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w1/MutCounterC1/MutCounterC1.patch`
    (7366 lines) and as plain files under that seat dir. No git write command ran in the lane or
    the fleet repo.
17. [obs] Reproduce: `python3 run-mutants.py` from the seat dir regenerates
    `mutant-results.json` (baseline per fixture, per-mutant sha256, killed/changed map) in about
    40 seconds.

Scope: read=SCORECARD.md:1196-1222 (round-31 declaration and its errata), lane tips 8cff9e7/f4861f4, tools/check-btrfs-repair-r31.py, .ufo/waves/round-31/measure/controls/build-c1-controls.py and c1-K0..K5 receipts, corpus/SOURCES.md rows S150-S163, six btrfs-progs v7.1 Documentation files; wrote=.ufo/waves/round-31/w1/MutCounterC1.md, .ufo/waves/round-31/w1/MutCounterC1/ (snap/, mutants/, mutant-results.json, mutant-table.md, baseline-table.md, build-my-positive.py, build-negatives.py, keymap.py, keymap.json, run-mutants.py, MutCounterC1.patch), /fast/scratch/hyaku/tsukuroi-r31/MutCounterC1/ (repo clone, work/c1-controls, work/c1-fixture, mutants); executed=mkdir, git clone/checkout/show/log/rev-parse/status/format-patch/commit (sandbox clone only), curl of the six raw.githubusercontent.com v7.1 Documentation files, sha256sum, python3 build-c1-controls.py, build-my-positive.py, build-negatives.py, run-mutants.py, keymap.py, tools/check-btrfs-repair-r31.py against 24 fixtures under 13 mutant copies, git grep at BASE for the 14 novelty tokens, grep/sed/cat/wc/diff, awk
Model: not exposed
Installs: none
