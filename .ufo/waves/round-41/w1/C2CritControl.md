VERDICT: falsifies

# C2CritControl — the counter's PASS is reachable with zero reading, and the verdict gate is not a read

Falsified clause: *"The lexical checks are shape gates (a relation-literal writer passes them, control
C2-K2); the verdict files are the read."* The first half holds. The second half does not: `verdicts_ok`
is reachable by eight two-line files written by the same candidate commit, and I have produced a full
`PASS` artifact whose rule cells are de-regexed relation literals, whose quotes are groff/`gettext`
boilerplate, and whose provenance rows point at `https://demo.invalid/`. The counter's entire git surface
is `git show`, `git ls-tree <rev>:<dir>`, and `git grep … BASE` (`tools/check-package-anatomy-r41.py:255`,
`:262`, `:272`); there is no history read and no author read, so nothing in it can distinguish a reviewer
from an author.

## 1. Counterexample — the cheapest passing writer

Fixture clone of the lane at tip `71851d636ab1bffaf8fee5016617c88878a666f1`, variant committed on `master`
(`git -C "$D" rev-parse --show-toplevel` = `$D`, identity `fixture@shokunin.local`):

```
git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin D; git -C D remote remove origin
python3 gen.py D            # the writer, receipt: w1/C2CritControl/cheapest-writer.py
git -C D commit             # 779a5b050de513ebc0c7a839087bd657bb2f2a73
python3 tools/check-package-anatomy-r41.py --repo D --revision 779a5b05…
```

Observed (receipt `w1/C2CritControl/pass-demo.json`, full counter record):

```
rules_verified 8  verdicts_ok 8  host_ok 6  source_ok 1
duplicate_rows 0  duplicate_headings 0  novelty_base_hits 0   result PASS  exit 0
```

Cost of that PASS: one counter invocation at the base revision (0.19 s, `time` on
`--revision 0e5805a1…`; the counter prints every expected value it compares against), one ~120-line
generator, 10 files touched (`corpus/knowledge/alpm-package-anatomy-r41.md`, `corpus/SOURCES.md`,
8 × 2-line verdict files) — diffstat `10 files changed, 39 insertions(+), 55 deletions(-)` against the tip.
**No pinned source was read for meaning, the host capture was never opened, and no reviewer existed.**
The artifact is visibly content-free (`w1/C2CritControl/pass-entry.md`): PA1's rule cell is
`.BUILDINFO and .MTREE and .PKGINFO; must and root; optional and .INSTALL and the snapshot records it here`,
PA5's quote is `msg2 "$(gettext "Generating .MTREE file...")"`, PA8's is `static void parseEVR(char *evr, const`,
and every provenance row is `— https://demo.invalid/…`.

## 2. Holes

### H1 — `verdicts_ok` has no attribution: the candidate mints its own verdicts
Row binding is the **filename**, the verdict is **line 1**, and the only other condition is that the id
appears somewhere in the body (`:276`, `:280`, `:282`). The candidate commit is the tested tree, so the
candidate supplies all eight files. Demonstrated: `C2RevPA1-author-self-attested.md` … `C2RevPA8-…`, body
`PA<n> self-attested by the author of this commit.` → `verdicts_ok 8`. The `[A-Za-z0-9-]*` tail means the
author chooses a filename no reviewer convention produces and it still counts.
The declaration ("per-row reviewer VERDICT files … first line `VERDICT: holds|partly|fails`") describes the
mechanism correctly but not its force: nothing ties the file to a reviewer, a review, or an identity.

### H2 — an honest `fails` is retractable by deleting the file, because only the tested tree is read
`:272` lists the directory *at `rev`* only. Two commits on top of the same passing artifact:
`6bacf3d7` adds `C2RevPA2.md` = `VERDICT: fails` → `verdicts_ok 7, FAIL`;
`618920f3` deletes that file and commits the deletion with the entry → `verdicts_ok 8, PASS`
(receipts `variant-A1-fails-present.json`, `variant-A2-fails-deleted.json`). A reviewer's veto is a file the
candidate can delete in the landing commit; `git log` is never consulted (`grep -n "log --|blame|rev-list|
cat-file" tools/check-package-anatomy-r41.py` → no match).

### H3 — malformed-but-counted: only line 1 is parsed, and the body may contradict it
`:280` takes `splitlines()[0]`; `:282` only needs `\bPA<n>\b` anywhere in the body. Demonstrated
(`variant-BC-contradicting-body.json`): `C2RevPA6.md` with first line `VERDICT: holds\r\n` (CRLF — `\s*$`
accepts it) and body `Review scope: PA2. PA6 was never reviewed; this file names PA6 only in passing, and
the row is false.` → counts as PA6 `holds`, `result PASS`. A verdict file may be about another row, may deny
the row, and may say it was never reviewed.
Not a hole in the same direction: a `holds` line that is **not** on line 1 is discarded as malformed — i.e.
the honest path is stricter than the cheat path, and a reviewer who writes `# PA2 review` first is silently
converted into `verdicts_ok - 1`. Likewise `partly` is collected and then never read (`:321` tests only
`holds` and `fails`), so a reviewer's `partly` loses to the author's `holds`.

### H4 — the glob binds a file to a row by name only, so one row's file counts as another's
Demonstrated (`variant-D-glob-match.json`): with `C2RevPA8.md` removed, `C2RevPA8-copy-of-PA1.md` whose body
is `This file is the PA1 check, copied; PA8 is named only here.` with line 1 `VERDICT: holds` → PA8 `holds`,
`result PASS`. Any stale or misfiled verdict that happens to match `^C2Rev(PA\d+)[A-Za-z0-9-]*\.md$` counts
for the row in its name; `.ufo/waves/round-41/residual` is scanned the same way (`:60`).

### H5 — `rules_verified == 8` without reading the sources
Three separate free answers, all inside the frozen tool:
- **value cells**: `vals` is computed from the snapshot and then printed in the record (`:312`) on *any*
  revision, including the base revision where the entry is absent. One 0.19 s run yields
  `.BUILDINFO .MTREE .PKGINFO; optional .INSTALL`, `$srcdir: package prepare build check; $startdir: verify`, …
- **rule cells**: `RELATIONS` (`:97-114`) is a Python literal; de-regexing it (`\b`→space, `.*`→`and`,
  `\.{n,m}`→`and`, `\.`→`.`) yields text that still satisfies `re.search(rel, rc)` for all 30 relations
  (`:351`). That is the writer in `cheapest-writer.py:57-63`.
- **quote gate**: `:370-381` accepts any 4-25 word substring of the collapsed cited lines that is not itself
  in the rule cell. A 5-word run lifted mechanically from the window passes; no comprehension is required,
  and the chosen run need not support the claim (PA1: `.LP The contents of an`; PA6: `int check_pkg_full(alpm_pkg_t *pkg) { const`).
Also free: `host_ok` (`:391`) is substring containment of `host_expect`, which the counter prints in the same
record — so a host column is a verbatim copy of the judge's own expectation, never a measurement. The demo's
PA1/PA4/PA5/PA6/PA7/PA8 host cells are exactly those pastes, and PA2/PA3 carry
`unmeasured: nothing was measured` and still pass, because they are not in `hexp`.

### H6 — provenance is self-declared end to end (`source_ok`, per-row `upstream`)
`:330` accepts a `source:` line whose ids are rows that are `mined` and name the entry; `:364` accepts an
`upstream` row that is new versus BASE, `mined`, opened `2026-10-26`, not `own-work`, naming the entry, and
whose **title** contains the rev tag and path tail. The title is text the candidate writes: eight rows
titled `demo lib/libalpm/be_package.c at 54d9411 — https://demo.invalid/lib/libalpm/be_package.c` satisfy
both (`pass-sources.diff`). `anchor` is parsed from the table but never compared with the entry's cited range,
no URL is resolved, no digest is compared, and the frozen snapshot's existence is never linked to the row.

### H7 — `novelty_base_hits` is not a candidate property
`novelty_hits(repo)` greps **BASE**, not `rev` (`:262`), and `nov_total = sum(nov.values())` (`:393`). Nothing
the candidate writes can move it, and if BASE had a hit no candidate could ever pass. The predicate term is
mislabelled: it is a base-side precondition, not a check on the entry.

### Non-holes checked
Frozen inputs are sha-pinned and raise `Tampered` (`:137-152`) — the snapshot and capture cannot be swapped.
`REF_RE` requires a `<required-file>:lo-hi` inside the row's window and rejects the whole `src_cell` otherwise
(`:371-377`). `duplicate_rows` / `duplicate_headings` are real but vacuous for a clean writer. Entry absence
and malformed verdict files fail closed. The defect is not tampering; it is that every remaining gate is text
the candidate itself writes.

## 3. Impacted axes

- **C2 depth (read) — primary.** `verdicts_ok == 8` no longer evidences eight read rows; the predicate's only
  non-lexical term is author-writable. A PASS says "eight claims exist", not "eight rows were reviewed".
- **C2 sourced — secondary.** `source_ok == 1` and the eight `upstream` hits are satisfied by fabricated
  `*.invalid` rows: title matching, not provenance.
- **PA1-PA8 per-row `host_ok`** — the host column is a copy of the judge's own `host_expect`, so the "six host
  values from the frozen capture" are inherited, not measured, in any entry that passes cheaply.
- **SCORECARD declaration for C2** — the sentence "the verdict files are the read" is the falsified part and
  must be amended; the counter itself is frozen-correct for what it does.
- **Controls** — C2-K2 (FAIL, `rules_verified 8 / verdicts_ok 0`) understates the hole by exactly the
  verdict term; the wave now needs a control that closes it with `PASS`.
- Unaffected: C1 (separate counter), QUALITY 88, `_revision.bind` (landed/pushed binding is sound and my
  fixture run bypassed only origin, which is a scratch-clone artefact, not a hole).

## 4. Smallest safe correction

No counter change can make a self-authored verdict evidence, so the safe correction is two parts, and only the
first may happen in this round.

**(a) Amend the declaration sentence (this round; text only).** Replace

> The lexical checks are shape gates (a relation-literal writer passes them, control C2-K2); the verdict files
> are the read.

with

> The lexical checks are shape gates (a relation-literal writer passes them, control C2-K2). The verdict files
> are an unauthenticated claim: the counter checks only that eight `VERDICT: holds` first lines naming their row
> exist in the tested tree, with no `fails` first line beside them, and cannot attribute them to a reviewer — an
> author can write them (control C2-K9). The read is the wave's reviewer process, not the counter.

**(b) Land C2-K9 (this round; control only).** Replay `w1/C2CritControl/cheapest-writer.py` against a fixture
clone of the lane at the wave tip and record the full record `rules_verified 8, verdicts_ok 8, host_ok 6,
source_ok 1, duplicate 0/0, novelty 0, PASS, exit 0` (already produced at variant `779a5b05…`; receipts in
`w1/C2CritControl/`). K9 must PASS, and that is the finding.

**(c) Round-42 counter shape (queue, do not edit the frozen counter).** Three edits, ~25 lines, closing H2,
H3/H4 and stale reuse — not H1, which no counter can close:
1. `verdicts()` takes `<rev>`'s tree **and** accumulates over `git rev-list BASE..rev`: a `fails` first line
   seen at any commit vetoes the row unless a later file for the same row carries
   `VERDICT: retracted <digest>` (closes H2).
2. First line becomes `VERDICT: <verdict> <16-hex>` over `collapse(rule) + '\n' + collapse(value) + '\n' +
   src_cell` of that row at `rev`; mismatch → malformed (closes H4 and every stale verdict, and forces a
   reviewer to have the row text in front of them).
3. `novelty_hits` gains a `rev` leg (`git grep … rev`) so the term tests the candidate, not BASE (closes H7).

Until (c) lands, treat `verdicts_ok` as a shape gate with the same standing as the lexical ones, and let the
wave's reviewer roster carry the read.

## 5. What I ran and did not run

Ran: `tools/check-package-anatomy-r41.py` read-only against a scratch clone (`--repo` into
`/fast/scratch/hyaku/tsukuroi-r41/C2CritControl/D`), twelve invocations total (base; four generator
iterations; four discarded variants committed with repo-relative `git rm` paths that matched nothing; the
four variants reported here), each 0.19-0.23 s. The four discarded commits (`8e827326`, `92450bdb`,
`60f233dc`, and one empty) were reset away before the reported ones; the reported revisions are `6bacf3d7`
(A1), `618920f3` (A2), `4aeeef5a` (BC), `5f9ca5e3` (D), all on `779a5b05`. Read: the counter, `_revision.bind`, `controls/controls-c2.jsonl`, `corpus/SOURCES.md` row format.
Did not run: C1's census or `score-selftest-mounts-r41.py` (not my item); the counter against the real lane
tip (my item is the C2 control hole, and the lane is being written by siblings — no read of their trees was
needed). No host, service, package, `/etc` or git state outside my scratch clone and my seat dir was touched;
no subagents, no broadcasts. Tooling installed: none. Scratch removed at exit; receipts kept under
`.ufo/waves/round-41/w1/C2CritControl/`.
