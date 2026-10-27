VERDICT: draft

Both cited defects are confirmed against the bytes and both correction notes are now in place, appended only (the
original lines stay). Item F-11 asked for exact Markdown; the two blocks below are the exact committed-to-working-tree
text, and every number in them was recomputed by this seat, not copied from the routed defect text.

## What I did

- Verified D2 (`R45C-D7-CITATION`) myself and appended the final one-line note to
  `.ufo/waves/round-44/w1/C1ExecLiveRead/commands.txt` (now `:88`) and `.ufo/waves/round-44/w2/SkillReview.md`
  (now `:104`).
- Verified D3 (`R45C-ASMGATE-RECEIPT`) myself and appended the final section to
  `.ufo/waves/round-45/a2w1/AsmGate.md` (now `:22-74`).
- Diff is append-only: `git -C <lane> diff --stat` on the three files = `2 +`, `2 +`, `56 +-` (59 insertions,
  1 deletion); the single deleted line is the same byte-for-byte sentence re-emitted with a trailing newline
  (`git diff -U0 … | cat -A` shows `-No campaign tools were run … No tools installed.` + `\ No newline at end of file`
  followed by `+No campaign tools were run … No tools installed.`). No original sentence was altered.
- Note for the L1: the working tree already carried earlier appends to the same three files (mtimes
  `2026-10-27 02:21:45`, all three within the same second; author not verifiable from the tree — `[INFERENCE]` a
  scripted append from this wave). I replaced those two blocks with the text below because they diverged from the
  item in three ways: D2 cited `cat-file -e 2042117c:<path>` instead of the implementation revision the item names
  (`a4477049`), D3 attributed the recount to "the round-46 L1" (provenance I could not verify; the recount was made
  by this seat), and D3 gave neither the pasted commands/outputs nor the 25 omitted ids. Both earlier variants were
  factually true as far as they went.

## Axis chosen

Evidence-axis only: the deliverable is auditable text. I did not touch product code, counters, gates, or any other
receipt, and ran no census/counter (neither is in this item's scope).

## D2 — exact appended text (identical in both files; one line, appended after a blank line)

```
Correction (round 46, R45C-D7-CITATION): the log cited above as `strace-rev-live1.log` is committed only compressed, as `.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log.gz` (lane path; blob `ec1848d66a288993c99e5f70ea901e62a412c502`, 79436 B, added by `ea6e0ee3`). `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -e a44770491eb5ca15ce9f8b3207309d1af683ffaf:.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log` -> exit 128, `fatal: path '.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log' does not exist in 'a44770491eb5ca15ce9f8b3207309d1af683ffaf'`; the identical command ending `.log.gz` -> exit 0 (at base `2042117cfb724170772f4c128cc2ddba0b61d817` the same pair is 128 / 0, and the blob id is unchanged). `zcat` of the committed file yields 15077 lines / 1358989 bytes - the size this line's "15077 lines (1,358,989 B)" records - so the receipt is intact and must be read with `zcat`, not from a file named `.log`.
```

`SkillReview.md` carries the same sentence with the size cross-reference spelled
"`w1/C1ExecLiveRead/commands.txt:26` records for this trace" instead of "this line's", because in that file the cited
sentence is at `:55`, not on the note's own line.

### D2 evidence (commands and observed output)

```
$ git -C … cat-file -e a4477049…:.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log
fatal: path '.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log' does not exist in 'a44770491eb5ca15ce9f8b3207309d1af683ffaf'
exit=128
$ git -C … cat-file -e a4477049…:.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log.gz
exit=0
$ git -C … cat-file -e 2042117c…:.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log   → exit=128 (same fatal)
$ git -C … cat-file -e 2042117c…:.ufo/waves/round-44/w1/C1ExecLiveRead/strace-rev-live1.log.gz → exit=0
$ git -C … rev-parse 2042117c:…log.gz  a4477049:…log.gz
ec1848d66a288993c99e5f70ea901e62a412c502
ec1848d66a288993c99e5f70ea901e62a412c502
$ git -C … cat-file -s a4477049:…log.gz  → 79436
$ git -C … log --diff-filter=A --oneline -1 -- '*strace-rev-live1.log.gz'
ea6e0ee3 round-45: declaration + frozen counters (…); D1 IN-109 repin 2468->2582; D7 round-44 untracked evidence committed (gz) with .ready markers
$ git -C … log --all --oneline --diff-filter=A -- '*strace-rev-live1.log'   → (no output: never committed uncompressed in any ref)
$ zcat …/strace-rev-live1.log.gz | wc -lc
  15077 1358989
$ sha256sum …/strace-rev-live1.log.gz
16085e679ef500cb9919bce715a332dc58cddb225f6f578a94fb2b6596130dd5
$ zcat …/strace-rev-live1.log.gz | sed -n '1,3p'
947327 openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
947327 openat(AT_FDCWD, "/usr/lib/libreadline.so.8", O_RDONLY|O_CLOEXEC) = 3
947327 openat(AT_FDCWD, "/usr/lib/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
$ zcat …/strace-rev-live1.log.gz | tail -2
947327 --- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=1016159, si_uid=1000, si_status=0, si_utime=0, si_stime=0} ---
947327 +++ exited with 2 +++
```

`zcat` exit status was 0 (compound pipeline, `set -o pipefail` not set in the seat shell; the decompressed line/byte
counts and the readable first/last lines are the direct evidence). The decompressed byte count `1358989` equals the
`1,358,989 B` recorded at `commands.txt:26`, so the gz is the same trace, not a truncated stand-in; the trailing
`+++ exited with 2 +++` matches the recorded `exit=2`.

## D3 — exact appended text (`.ufo/waves/round-45/a2w1/AsmGate.md:22-74`)

````
## Correction (round 46, R45C-ASMGATE-RECEIPT)

The id figures above ("183 registry ids, 147 staged ids, 30 intersections") do not reproduce against the bytes at
round 45's measured revision `44560592857660a20c6a2b296fa14fa7a90464b5` (`SCORECARD.md:2908`). Recounted in round 46
with the round prompt's 0-3-leading-space extractor: lane registry **249** ids (S001-S249), staged **147** ids
(S200-S346), intersection **50** (S200-S249).

```sh
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
K=/home/vgpnk/Projects/shokuknow
$ git -C "$L" show 44560592857660a20c6a2b296fa14fa7a90464b5:corpus/SOURCES.md \
    | grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' | grep -oE 'S[0-9]{3,}' | sort -u > reg-ids
$ grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' "$K/merge/tsukuroi/SOURCES.append.md" \
    | grep -oE 'S[0-9]{3,}' | sort -u > staged-ids
$ wc -l < reg-ids ; wc -l < staged-ids ; comm -12 reg-ids staged-ids | wc -l
249
147
50
$ sed -n '1p;$p' reg-ids ; sed -n '1p;$p' staged-ids ; comm -12 reg-ids staged-ids | sed -n '1p;$p'
S001
S249
S200
S346
S200
S249
```

The gap is not an indentation convention. At that revision every row of `corpus/SOURCES.md` starts at column 0, and
every plausible variant of the extractor returns 249: `grep -cE '^\| S[0-9]'` -> 249, `grep -cE '\| *S[0-9]{3,}'` ->
249, unique `S[0-9]{3}` tokens -> 249. A fixture carrying rows at 0, 1, 2, 3 and 4 leading spaces (plus one `- S006`
list item) shows the 0-3 branch returning `S001 S002 S003 S004` and dropping the 4-space row and the list item, so
the extractor does recognize the permitted indent and still counts 249.

The kept `AsmGate/id-collisions.txt` (30 lines) therefore does not back its own "30 intersections". Five of its ids
are not lane registry ids at that revision - **S250, S251, S252, S262, S268** (each is present in `staged-ids`) - and
it omits 25 genuine collisions: **S203, S204, S207, S208, S212, S214, S215, S216, S217, S218, S219, S220, S221, S226,
S227, S229, S232, S233, S234, S240, S241, S245, S246, S247, S248**. Only 25 of the 50 real collisions appear in it.

```sh
$ wc -l < .ufo/waves/round-45/a2w1/AsmGate/id-collisions.txt
30
$ comm -23 listed reg-ids | tr '\n' ' '   # listed, but not a lane registry id
S250 S251 S252 S262 S268
$ comm -13 listed collisions | tr '\n' ' '   # genuine collisions the kept file omits
S203 S204 S207 S208 S212 S214 S215 S216 S217 S218 S219 S220 S221 S226 S227 S229 S232 S233 S234 S240 S241 S245 S246 S247 S248
$ comm -13 listed collisions | wc -l
25
```

Cite `.ufo/waves/round-45/assimilation/collisions` - the true 50-line collision set, S200-S249, with `reg-ids` (249
lines) and `staged-ids` (147 lines) beside it in the same directory - for round 45's collision set, not this receipt.
The substantive finding above is unaffected and is understated rather than overstated: staged rows S200-S249 collide
with an existing lane registry id, which is the reason not to append the staged registry as-is.
````

### D3 evidence (what the numbers rest on)

- Measured revision: `SCORECARD.md:2908` — "Measured revision `44560592857660a20c6a2b296fa14fa7a90464b5`
  (integration of wave `a2w1` and residual `a2r1`)". `git cat-file -t 4456059…` → `commit`.
- Registry extraction at that revision: `249` unique ids, first `S001`, last `S249`; the revision's
  `corpus/SOURCES.md` is 351 lines.
- Staged extraction: `147` unique ids, `S200`–`S346`, from
  `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`.
- Intersection: `50`, `S200`–`S249` — i.e. the staged block of 50 ids `S200…S249` is exactly the tail of the lane
  registry at that revision, which is why `MERGE-REPORT.md:9`'s own line ("lane registry currently holds **199**
  rows; first staged id is **S200**") is stale: the merge report was staged against an older registry.
- Kept receipt: `.ufo/waves/round-45/a2w1/AsmGate/id-collisions.txt` has 30 lines; `comm` against the true sets gives
  the 5 non-registry ids and the 25 omitted collisions listed above (receipts `nonreg-5.txt`, `missing-25.txt`).
- Guard fixture (`fx.md`): extractor output `| S001`, ` | S002`, `  | S003`, `   | S004` — the 0/1/2/3-space rows
  match, the 4-space row and the `- S006` item do not, so the count of 249 is not a silent under-count of indented
  rows (there are none: `grep -cE '^ \| S[0-9]'` on the registry at that revision → 0).
- Corroboration, not evidence for my numbers (independent prior recording of the same defect):
  `.ufo/waves/round-45/a2w1/ScribeLesson.md:216` row `R45-ASMGATE-IDCENSUS` likewise records 249 / 147 / 50, the five
  non-registry ids and the 25 omissions.

## Residual site I did not touch (out of this item's scope)

`.ufo/waves/round-44/w2/SkillReview/evidence.md:43` still reads "w1/C1ExecLiveRead/strace-rev-live1.log exists." That
is the same basename defect in a third file; my item named only `commands.txt` and `SkillReview.md`, so I left it
unmodified. Proposed follow-up: either add the same D2 sentence there, or reword `:43` to name the `.gz`. Note also
that its literal claim ("exists") is false as written — there is no such path in either revision
(`cat-file -e` → 128) and no such file in the working tree.

## Limits — what I did not do

- I did not run the C1 counter, a census selftest, the C2 counter, or any gate; none is part of this item, and the
  claim bodies C1/C2 are outside it. No PASS/FAIL here is new: the report asserts only receipt-text defects.
- I did not re-measure the host, and I did not verify the strace trace's *content* semantics (that it covers the
  required syscall classes) — only that the committed gz decompresses to the cited line/byte count, ends in
  `exited with 2`, and is cited under a name that does not exist.
- I did not establish how the round-45 AsmGate seat obtained 183; no plausible extractor variant reproduces it at
  that revision (four variants tested, all 249), so the correction states non-reproduction, not a cause.
- `zcat` exit status was observed through a compound command; the decoded content is the evidence, not a captured
  `$?`.
- The staged file lives in the read-only source `/home/vgpnk/Projects/shokuknow`; I used it read-only and did not
  check whether it changed after round 45 (mtime `2026-10-24 23:33`, before round 45's measurements; round-46
  AsmGate's own extraction also returned 147, which is consistent but was not re-verified against a round-45-era copy).

## Housekeeping

- Scratch `/fast/scratch/hyaku/tsukuroi-r46/D2D3Draft/` removed after copying receipts; nothing built under `/tmp`,
  no writes outside the lane's `.ufo/waves/round-46/w1/D2D3Draft/` and the three named receipt files.
- No tools installed or upgraded; no package manager, service, timer, sysfs, or mount operation; no git mutation in
  the lane (working-tree edits only, uncommitted — the L1 commits).
- Receipts: `.ufo/waves/round-46/w1/D2D3Draft/` — `transcript.txt` (all commands with observed output),
  `reg-ids-4456059` (249), `reg-4456059.md` (registry bytes at `4456059`), `staged-ids` (147), `collisions` (50),
  `listed` (30, the kept AsmGate set), `nonreg-5.txt`, `missing-25.txt`, `fx.md` (guard fixture).
