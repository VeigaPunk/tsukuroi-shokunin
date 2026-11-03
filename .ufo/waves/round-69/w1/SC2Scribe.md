# Seat SC2Scribe — round 69 w1 (scribe: registry rows and lesson draft)

2026-11-03T23:23:00Z

## Behavior

Drafted, as prose only, the two C1 registry rows S288 and S289 and the round-69 lesson skeleton.
No product code, note, counter, registry, SCORECARD, LOG or lesson-final file was edited. No git or jj
mutation. No tool installed. No host probe outside the read-only set; no pacman, systemctl or sudo call.

## Touched surfaces (writes)

- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/sources-rows.md` (S288, S289)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/lesson.md` (skeleton)
- this report

Read-only: `corpus/SOURCES.md` (header line 5, rows S138/S140/S158/S284-S287, tail), `corpus/QUALITY.md:169`,
`corpus/lessons/round-68.md`, `SCORECARD.md` round-69 declaration (lines 5185-5229),
`.ufo/waves/round-69/before/{src/*,host.txt,FETCH.txt}`, `.ufo/waves/round-69/w1-spec.json`.

## Receipts

`$ date -u +%Y-%m-%dT%H:%M:%SZ` → `2026-11-03T23:21:37Z` (drafting); final evidence run `2026-11-03T23:22:31Z`.

### Snapshots

    $ cd .ufo/waves/round-69/before/src && sha256sum -c SHA256SUMS
    tk-v7211.rst: OK
    vm-v7211.h: OK
    rc=0

    $ sha256sum .ufo/waves/round-69/before/src/tk-v7211.rst .ufo/waves/round-69/before/src/vm-v7211.h
    727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  tk-v7211.rst
    0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea  vm-v7211.h
    rc=0

    $ wc -l .ufo/waves/round-69/before/src/tk-v7211.rst .ufo/waves/round-69/before/src/vm-v7211.h
    191 tk-v7211.rst
     48 vm-v7211.h

`before/src/FETCH.txt` (3 lines, read with `cat -A`): stable tree URL for each file with `?h=v7.2.11`, and
`fetched 2026-11-03 by tsukuroi L1 round 69; method curl -sS --max-time 60`.

### Cell counts on the drafted rows

    $ awk -F'|' '/^\| S28[89] /{print $2": NF="NF" cells="NF-2}' .ufo/waves/round-69/drafts/c1/sources-rows.md
     S288 : NF=13 cells=11
     S289 : NF=13 cells=11
    rc=0     (re-run 2026-11-03T23:22:14Z after the anchor line-range fixes, same output)

    $ grep -c '^| S28[89] ' .ufo/waves/round-69/drafts/c1/sources-rows.md
    2

No cell contains a literal or escaped pipe. One `\|` occurs in the file, on line 15 inside the indented shell
command block (`awk` regex), not inside a row.

### Quote locations and word counts

S288 (tk-v7211.rst):

    $ grep -n 'bitfield' .ufo/waves/round-69/before/src/tk-v7211.rst
    72:number, as it is a bitfield, where each bit indicates the absence or presence of
    $ sed -n '72,73p' .ufo/waves/round-69/before/src/tk-v7211.rst | tr '\n' ' ' | grep -cF 'number, as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint.'
    1
    $ grep -cF 'number, as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint.' .ufo/waves/round-69/before/src/tk-v7211.rst
    0
    rc=1
    $ printf '%s\n' 'number, as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint.' | wc -w
    20

Quote starts at line 72 and ends at line 73; 20 words. The single-line search returns 0 because the sentence
spans the line break, which is why the row cites the pair 72-73.

S289 (vm-v7211.h):

    $ grep -n 'Simply sanity' .ufo/waves/round-69/before/src/vm-v7211.h
    12:/* Simply sanity version stamp for modules. */
    $ grep -cF '/* Simply sanity version stamp for modules. */' .ufo/waves/round-69/before/src/vm-v7211.h
    1
    $ printf '%s\n' '/* Simply sanity version stamp for modules. */' | wc -w
    8

Line 12; 8 words by `wc -w`, which counts the `/*` and `*/` delimiters (6 content words). The row states the
`wc -w` number and that the delimiters are included.

### Anchor line ranges (verified against the snapshots)

    $ sed -n '81,86p' .ufo/waves/round-69/before/src/tk-v7211.rst
    (blank)
    ===  ===  ======  ========================================================
    Bit  Log  Number  Reason that got the kernel tainted
    ===  ===  ======  ========================================================
      0  G/P       1  proprietary module was loaded
      1  _/F       2  module was force loaded
    $ grep -n '^ *[0-9][0-9]*  _/' .ufo/waves/round-69/before/src/tk-v7211.rst | sed -n '1p;$p'
    86:  1  _/F       2  module was force loaded
    104: 19  _/J  524288  userspace used a mutating debug operation in fwctl
    $ grep -n '^===  ===  ======' .ufo/waves/round-69/before/src/tk-v7211.rst
    82:===  ===  ======  =======================================================
    84:===  ===  ======  =======================================================
    105:===  ===  ======  =======================================================

So the table occupies lines 83-105 (header 83, bit 0 at 85, bit 19 at 104, closing rule 105). The runtime-query
sentence starts at line 50 ("At runtime, you can query the tainted state by reading") and names
`cat /proc/sys/kernel/tainted` at line 51; the row cites 50-52.

    $ sed -n '40,48p' .ufo/waves/round-69/before/src/vm-v7211.h   (numbered view)
    41 #define VERMAGIC_STRING
    42 UTS_RELEASE " "
    43 MODULE_VERMAGIC_SMP MODULE_VERMAGIC_PREEMPT
    44 MODULE_VERMAGIC_MODULE_UNLOAD MODULE_VERMAGIC_MODVERSIONS
    45 MODULE_ARCH_VERMAGIC
    46 MODULE_RANDSTRUCT

Macro definitions: line 14 `#define MODULE_VERMAGIC_SMP "SMP "`, line 21 `#define MODULE_VERMAGIC_PREEMPT "preempt "`,
line 26 `#define MODULE_VERMAGIC_MODULE_UNLOAD "mod_unload "`, line 31 `#define MODULE_VERMAGIC_MODVERSIONS "modversions "`
(all from `grep -n`). The row's anchor cites these plus 41-46.

### Registry context used for the reject list

    $ grep -c 'raw.githubusercontent.com/torvalds/linux/v7.2' corpus/SOURCES.md
    22
    $ sed -n '146p' corpus/SOURCES.md | grep -o 'sha256 [0-9a-f]\{64\}'
    sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841
    $ grep -c 'vermagic' corpus/SOURCES.md
    0
    rc=1
    $ awk -F'|' '/^\| S[0-9]+ \|/{n++} END{print n}' corpus/SOURCES.md
    287

S140 (line 146) is the registered torvalds-v7.2 row for `Documentation/admin-guide/tainted-kernels.rst` and
records the same sha256 as S288. No `vermagic` row exists, so the vermagic half of gate candidate 3 has no
registered duplicate; the lesson skeleton marks that half as `(L1 fills)` rather than asserting a reject.

`corpus/QUALITY.md:169` read verbatim (rule 86): a rule row is verified only when its `source:` cell names at
least one `corpus/SOURCES.md` row whose `kind` is not `own-work` and whose locator names the upstream artifact at
the pinned revision; an `own-work` row may carry a host observation, a count or a capture digest and never makes
the rule verified by itself. This is the stated basis for reject 4.

### Lesson skeleton

    $ grep -n '^## ' .ufo/waves/round-69/drafts/c1/lesson.md
    11:## Gate
    67:## Mistakes
    78:## Trend verdicts
    86:## Considerthese
    94:## Sources

All five headings present and in the item's order; 17 `(L1 fills ...)` markers; no invented count, defect id,
verdict or proposal title.

## Findings

1. Both rows read NF 13 / 11 cells and match the header schema of `corpus/SOURCES.md:5`; `status` mined,
   `opened` 2026-11-03, `recheck` on-release, `used-by` `corpus/knowledge/kernel-taint-plane-r69.md`.
2. S288 is drafted as a re-pin, not a second document: its teaches cell begins `supersedes S140 — re-pin:` under the
   registry convention of S280/S281, states that the v7.2.11 bytes are byte-identical to S140's torvalds v7.2
   snapshot (L1-reported `cmp` rc 0; S140's recorded sha256 read at `corpus/SOURCES.md:146`), claims no new document
   content, and keeps S140 current for the torvalds v7.2 tag. The declaration fixes S288/S289 as the round's sources,
   so the row does not amend the predicate.
3. S289 carries the only code-level anchor for the host's `mod_unload`/`SMP preempt` vermagic tokens; its quoted
   line is the file's purpose comment, and the token composition is a stated anchor (41-46), not a quote, because
   those lines hold macro line continuations and double quotes that would break the `quote="..."` envelope.
4. The lesson skeleton lists two admits and two rejects as asked. Reject 3 is now the narrow candidate the L1 named in
   the correction: a second torvalds-v7.2 registration of `tainted-kernels.rst`, refused as a duplicate of S140
   (`corpus/SOURCES.md:146`, same sha256; 22 rows pin torvalds v7.2 URLs). The skeleton records, as a named limit
   rather than a verdict, that no `vermagic.h` row exists at any tag (`grep -c vermagic` = 0), so that reject covers
   `tainted-kernels.rst` only. Reject 4 is the own-work capture row, refused on QUALITY 86. S288 is recorded as
   admit-with-reason (re-pin).
5. The `awk` cell check must not be run over the whole draft file: prose lines contain pipes. The drafted filter
   `^\| S28[89] ` scopes it to the rows.

## Corrections applied after the first draft

L1 `TsukuroiR69` sent one correction at 2026-11-03T23:2xZ (IRC), after the first yield:

- S288 must be worded as a re-pin in the registry convention of S280/S281, with the teaches cell beginning
  `supersedes S140 — re-pin:`, the running kernel's own tag v7.2.11, bytes byte-identical to S140 (sha256
  `727ddb82…` for both; L1 `cmp` rc 0 against `.ufo/waves/round-27/sources/S140.rst`), no new document content
  claimed, S140 staying current for the torvalds v7.2 tag. Applied to the S288 teaches and anchor cells and to the
  lesson's Gate item 1, Admitted line and Sources bullet.
- The lesson Gate must record S288 as admit-with-reason (re-pin) and carry exactly two rejects: (a) a second
  torvalds-v7.2 registration of `tainted-kernels.rst` (duplicate of S140, refused) and (b) an own-work capture row
  (QUALITY 86, refused). Applied; the earlier hedge about the vermagic half is now a one-clause named limit.

Post-correction re-verification: `$ awk -F'|' '/^\| S28[89] /{print $2": NF="NF" cells="NF-2}' …` at
2026-11-03T23:26:00Z → ` S288 : NF=13 cells=11`, ` S289 : NF=13 cells=11`, rc 0; S288 cell 7 now begins
`supersedes S140 — re-pin:`. The correction's `cmp` receipt was supplied by the L1 and is cited as such; this seat
did not re-run it.

## Out of scope / not done (by assignment)

No `corpus/knowledge/kernel-taint-plane-r69.md`, no `tools/count-kr-rows-r69.py`, no `corpus/SOURCES.md` edit,
no `tools/tsukuroi-census.sh` edit, no SCORECARD/LOG edit, no lane census or selftest run, no lesson final
(only the skeleton), no considerthese or assimilation work, no commit.

## Limits and unreachable values

- I did not run `cmp` against `.ufo/waves/round-27/sources/S140.rst`; the byte-identity claim inside the S288 row and
  the lesson Gate cites the L1's correction (`cmp` rc 0) and is labelled L1-reported. This seat verified only the
  v7.2.11 snapshot digests against `before/src/SHA256SUMS` and read S140's recorded digest at `corpus/SOURCES.md:146`.
- The torvalds-v7.2 `include/linux/vermagic.h` was not fetched and no row exists for it, so it is recorded as a named
  limit beside the duplicate reject, not as a reject verdict.
- `before/src/FETCH.txt` carries no per-line timestamp beyond the "fetched 2026-11-03" line; the fetch time is not
  recorded in the snapshot directory.
- Scratch dir `/fast/scratch/hyaku/tsukuroi-r69/SC2Scribe` was created empty and removed before yield; it holds
  no receipts.
