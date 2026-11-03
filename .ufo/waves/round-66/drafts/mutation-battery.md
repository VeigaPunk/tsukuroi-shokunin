2026-11-03T21:06:30Z

# Counter mutation battery — C1 and C2 (round 66, w1, seat M1MutBattery)

Mutation-tester probe against the **frozen counting commands** of SCORECARD.md
"Round 66 — declaration" (base `c68bfe97`). Fixtures were built and attacked in
scratch only (`/fast/scratch/hyaku/tsukuroi-r66/M1MutBattery`), never in the lane.
No tracked file was read-modified; no lane tool was run.

Axes walked: **counter discrimination** (does the named command distinguish a
conforming artifact from a defective one), **mutation coverage** (which defect
classes survive), **operability** (rc semantics, false negatives on legitimate
input), **reproducibility** (fixture bodies and one-line diffs kept here, since
scratch is deleted).

Baseline discipline: each claim's detector was run on a pristine fixture first.
Mutants are separate files, each differing from the pristine by exactly one
mutation (unified diffs below). The pristine fixtures' sha256 were identical
before and after the whole battery (restoration section).

## 0. The counters under test (verbatim from the declaration)

C2 counting command column:

```
grep -cE '^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \|' corpus/knowledge/adjacency-recheck-r66.md   → 10
grep -c '^## Erratum (round 66)' corpus/knowledge/adjacency-anchors-r19.md   → 1
```

C1 counting command column:

```
git cat-file -e <rev>:corpus/knowledge/systemd262-credentials-boot-policy-r66.md
grep -c '^| CB' <note>
grep -cE '^\| S[0-9]{3,}' corpus/SOURCES.md
the census validate and check-knowledge-header.py at round end
```

plus the prose clauses "`^\| CB` rows **≥ 5**", "SOURCES **≥ 283** with S283
directly after S282 (NF 13, Gate quote ≤ 25 words)".

Both target notes were **ABSENT** at probe time (`.ufo/waves/round-66/drafts/` has
no cb note; `corpus/knowledge/systemd262-credentials-boot-policy-r66.md` and
`corpus/knowledge/adjacency-recheck-r66.md` both absent — `[ -f ]` test), so every
verdict below is about the counter, not about a peer's artifact.

## 1. Fixtures (sha256, final state)

Pristine rows carry the **real** values from the authority register
`corpus/knowledge/adjacency-anchors-r19.json` (10 outbound anchors; sibling commits
40-hex, blob sha256 64-hex), so the C2 control is a genuine, fully-resolvable table.

```
c1/a-sources-282-283.md             bytes= 934 sha256=ad239e87e2710ec304a4e65d1f5ad33604a90ec97457f3d5701f5a5b0c7fdedc
c1/b-sources-283-before-282.md      bytes= 934 sha256=0f6c324a35f37199391b6d1fffbc5252f19c337e131ef53fb2525e6315745a56
c1/c-sources-283-escaped-pipe.md    bytes= 938 sha256=9ce4018aa7d24bb6e9441c24ce460b3023077840eb5c3e22546e9fd8054b577c
c1/d-note-cb5.md                    bytes= 473 sha256=027e83a4639ccbd67d0d7dca2f81cf67ec938d1e3c1955fbe095fc9cdcea574d
c1/d2-note-cb5-noheader.md          bytes= 418 sha256=43d97e09df1870a41fd194ad77afa1870299b6891cea826b11c1d084807fc77b
c1/e-note-cb4.md                    bytes= 430 sha256=a5552940f18903a69552983256b429058f927b658aa81ee2ebd13059b787a6ea
c1/e2-note-cb4-noheader.md          bytes= 375 sha256=b12cc68fa0fe4d1ee725b47f6404d2b669e1084fa4e205f421f195ad31efd431
c1/f-note-cb0-noheader.md           bytes=  60 sha256=b855457a1086b4a2df77e99aeb01df8a01f8fdc1409d17b8787fa31baad015a6
c1/g-duplicate-s283.md              bytes=1331 sha256=ae986570419e969aa3e3f5c1e03fddf361459a158c17ddb5587ff5b5643de3e8
c2/a-pristine-10.md                 bytes=1725 sha256=90b82b996dbc77abf55c32ab93862a9662e4a134cfc6e9f5d7a74d42150f76a3
c2/b-9-rows.md                      bytes=1560 sha256=151495d33e5b084125c76ac63b50af3f4b6b631aae210651b82e185b67ea902d
c2/c-fabricated-head.md             bytes=1725 sha256=4c2c95ac0c209082990c69db176f2c8fa8160f5326d5bd92518112df05068cfd
c2/d-unlocated.md                   bytes=1727 sha256=388474a0ef7bcf84a71528e7f57885a3f01a066d813ca12396915f46c54364c6
c2/e-space-padded-sibling.md        bytes=1726 sha256=96097d0ace437832a03685d9967de4757a5418918d55eea0ecf6c15831b64975
c2/f-duplicate-out.md               bytes=1725 sha256=39db5aa2a282faaf3edfaf50551b8613072d3018ddacc6516e83bf203b0d80a2
```

## 2. C2 — frozen counter, six probes

Command (the detector, exactly the frozen regex; one argv element):

```
grep -cE '^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \|' <fixture>
```

Verbatim transcript (the driver's `$` lines are `"$@"`-flattened, so the regex
appears unquoted; the argv itself was the single quoted argument above):

```
--- a-pristine-10.md ---
$ grep -cE ^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \| .../c2/a-pristine-10.md
10
rc=0

--- b-9-rows.md ---
9
rc=0

--- c-fabricated-head.md ---
10
rc=0

--- d-unlocated.md ---
9
rc=0

--- e-space-padded-sibling.md ---
9
rc=0

--- f-duplicate-out.md ---
10
rc=0
```

| # | mutant (one change from pristine) | count | rc | equals frozen target 10 | verdict |
|---|---|---|---|---|---|
| C2-a | none — pristine, 10 real rows from the r19 register | 10 | 0 | yes | **baseline** (detector accepts a conforming note) |
| C2-b | AR10 row deleted (9 rows) | 9 | 0 | no | **KILLED** |
| C2-c | AR1 live HEAD replaced by `fee7b0682d23747d7c197917e52eded5d4f580f7` (well-formed 40-hex, exists nowhere) | 10 | 0 | yes | **SURVIVED** — class S-A |
| C2-d | AR6 status `located` → `unlocated` | 9 | 0 | no | **KILLED** |
| C2-e | AR2 sibling `kama` → `" kama"` (one extra space, semantically inert in Markdown) | 9 | 0 | no | **KILLED** as a mutation — but see S-F: the mutation is not a defect, so this is a counter *false negative* |
| C2-f | AR4 row rewritten as OUT-003/kagi (OUT-003 twice, OUT-004 absent; still 10 row-shaped lines) | 10 | 0 | yes | **SURVIVED** — class S-B |

One-line diffs (proof each mutant is a single mutation):

```
### c2/b-9-rows.md
@@ -12 +11,0 @@
-| AR10 | OUT-010 | tameshi | 01d586ddbc5fcd78659557c4e93a6ee8517b87d1 | 8006da5db27d2188ff2f3fc20ae402d0d30c7b5c5fcf9ca26c6793d2ff7e080f | located | PROVINCE.md:7 |

### c2/c-fabricated-head.md
@@ -3 +3 @@
-| AR1 | OUT-001 | mori | 91940fa339e38006f8db5bd7d78bb6f037f4d016 | 73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130 | located | PROVINCE.md:9 |
+| AR1 | OUT-001 | mori | fee7b0682d23747d7c197917e52eded5d4f580f7 | 73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130 | located | PROVINCE.md:9 |

### c2/d-unlocated.md
@@ -8 +8 @@
-| AR6 | OUT-006 | kumitate | 1770305fae20826b39905a8251ddeca6b4957ac4 | fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f | located | PROVINCE.md:3 |
+| AR6 | OUT-006 | kumitate | 1770305fae20826b39905a8251ddeca6b4957ac4 | fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f | unlocated | PROVINCE.md:3 |

### c2/e-space-padded-sibling.md
@@ -4 +4 @@
-| AR2 | OUT-002 | kama | e75cf680b53484a61709ee1b2787d8dbc6419f74 | 799432d748bd40bcf859de806cc2ef90df069da14c8e5c07bf72250ac411c7a6 | located | PROVINCE.md:12 |
+| AR2 | OUT-002 |  kama | e75cf680b53484a61709ee1b2787d8dbc6419f74 | 799432d748bd40bcf859de806cc2ef90df069da14c8e5c07bf72250ac411c7a6 | located | PROVINCE.md:12 |

### c2/f-duplicate-out.md
@@ -6 +6 @@
-| AR4 | OUT-004 | mado | a4046a8216080d4004de3f268c62cf142095ac07 | 1b25bb1e980925b356663602d002c1c15307a0dfac8bfafd9988bd4d8df7464b | located | PROVINCE.md:6 |
+| AR4 | OUT-003 | kagi | c2cab35bc92e57e39e5489bac3386db078345b3f | 4a346e2df81f7b2e649914d0d99da974d6c484caf12fed1c6bd530d106a78523 | located | PROVINCE.md:3 |
```

Auxiliary identity check for C2-f (NOT in the frozen predicate):

```
$ awk -F'|' '/^\| AR[0-9]+ \|/{gsub(/ /,"",$3); print $3}' f-duplicate-out.md | sort | uniq -c
      1 OUT-001
      1 OUT-002
      2 OUT-003
      1 OUT-005
      1 OUT-006
      1 OUT-007
      1 OUT-008
      1 OUT-009
      1 OUT-010
rc=0
```

OUT-004 is absent, OUT-003 is doubled, and the frozen count is still 10.

## 3. Fabrication check — the check the counter omits

Git dir: the real sibling checkout `/home/vgpnk/Projects/shokunin/mori-shokunin`
(asserted, read-only commands only):

```
$ git rev-parse --show-toplevel
/home/vgpnk/Projects/shokunin/mori-shokunin
rc=0

$ git cat-file -e 91940fa339e38006f8db5bd7d78bb6f037f4d016^{commit}   # positive control: real r19 anchor for OUT-001
rc=0

$ git cat-file -e fee7b0682d23747d7c197917e52eded5d4f580f7^{commit}   # fabricated head from mutant C2-c
fatal: Not a valid object name fee7b0682d23747d7c197917e52eded5d4f580f7^{commit}
rc=128

$ git cat-file -e fee7b0682d23747d7c197917e52eded5d4f580f7            # same, untyped
rc=1

$ git cat-file -e 84c6cbc3b47c536a504aaee329c77897d389935e^{commit}   # peer live head for AR1 (drafts/c2-anchors-live.tsv)
rc=0
```

Reading: the fabricated HEAD is rejected by the repository (rc 128 typed, rc 1
untyped) while the counter reports a clean 10/rc 0. The C2 **kill rule** already
names this defect ("a sibling HEAD unreadable … → that row is not `located` and the
count is below 10"), but **no listed counting command observes it** — the kill rule
is prose, the instrumentation is a regex. The typed form `^{commit}` is required:
an untyped `cat-file -e` would accept a blob or tree hash as a "HEAD".

## 4. C1 — frozen counters, nine probes

Commands:

```
grep -cE '^\| S[0-9]{3,}' <fixture>                      # frozen counter for the SOURCES clause
awk -F'|' '/^\| S283 /{print "S283 NF=" NF}' <fixture>    # the NF 13 clause
awk -F'|' '/^\| S283 /{exit (NF==13)?0:1}' <fixture>      # NF 13 as a gate
grep -nE '^\| S28[23] ' <fixture>                         # the "directly after S282" clause
grep -c '^| CB' <note>                                    # frozen counter for the note clause
```

Transcript:

```
--- a-sources-282-283.md ---
$ grep -cE ^\| S[0-9]{3,} .../c1/a-sources-282-283.md
2
rc=0
$ awk -F| /^\| S283 /{print "S283 NF=" NF} .../c1/a-sources-282-283.md
S283 NF=13
rc=0
$ awk -F| /^\| S283 /{exit (NF==13)?0:1} .../c1/a-sources-282-283.md
rc=0
$ grep -nE '^\| S28[23] ' a-sources-282-283.md
3:| S282 | ... |
4:| S283 | ... |
rc=0

--- b-sources-283-before-282.md ---
$ grep -cE ^\| S[0-9]{3,} ...
2
rc=0
$ awk -F| /^\| S283 /{print "S283 NF=" NF} ...
S283 NF=13
rc=0
$ grep -nE '^\| S28[23] ' b-sources-283-before-282.md
3:| S283 | ... |
4:| S282 | ... |
rc=0

--- c-sources-283-escaped-pipe.md ---
$ grep -cE ^\| S[0-9]{3,} ...
2
rc=0
$ awk -F| /^\| S283 /{print "S283 NF=" NF} ...
S283 NF=14
rc=0
$ awk -F| /^\| S283 /{exit (NF==13)?0:1} ...
rc=1

--- CB notes ---
$ grep -c ^| CB .../c1/d-note-cb5.md        # header + CB1..CB5
6
rc=0
$ grep -c ^| CB .../c1/e-note-cb4.md        # header + CB1..CB4
5
rc=0
$ grep -c ^| CB .../c1/d2-note-cb5-noheader.md
5
rc=0
$ grep -c ^| CB .../c1/e2-note-cb4-noheader.md
4
rc=0
$ grep -c ^| CB .../c1/f-note-cb0-noheader.md
0
rc=1

--- g-duplicate-s283.md ---
$ grep -cE ^\| S[0-9]{3,} ...
3
rc=0
$ grep -nE '^\| S283 ' g-duplicate-s283.md
4:| S283 | ... |
5:| S283 | ... |
rc=0
$ awk -F| /^\| S283 /{print "S283 NF=" NF} ...
S283 NF=13
S283 NF=13
rc=0
```

| # | mutant | command | output | rc | verdict |
|---|---|---|---|---|---|
| C1-a | S282 then S283, both NF 13 | `grep -cE '^\| S[0-9]{3,}'` | 2 | 0 | **baseline** (both rows counted; S283 counted) |
| | | `awk … NF` | `S283 NF=13` | 0 | NF clause holds |
| C1-b | S283 placed **before** S282 | `grep -cE …` | 2 | 0 | **SURVIVED** — class S-C. The order check shows `3:S283 / 4:S282`, so "directly after S282" is false while the counter is unchanged |
| C1-c | one escaped pipe `\|` in the S283 teaches cell | `grep -cE …` | 2 | 0 | **SURVIVED by the grep** — class S-D |
| | | `awk … NF` / `NF==13` gate | `S283 NF=14` / rc 1 | 0 / 1 | **KILLED by the NF check** (which is not in the counting-command column; the declaration delegates it to the census, not run here) |
| C1-d | note = header `\| CB \| …` + CB1…CB5 | `grep -c '^\| CB'` | 6 | 0 | PASS, but **+1 overcount** — class S-E |
| C1-e | note = header `\| CB \| …` + CB1…CB4 | `grep -c '^\| CB'` | 5 | 0 | **SURVIVED** — ≥5 satisfied by **4 data rows** — class S-E |
| C1-d2 | CB1…CB5, no header (control) | `grep -c '^\| CB'` | 5 | 0 | exact count (control isolates the header as the cause) |
| C1-e2 | CB1…CB4, no header (control) | `grep -c '^\| CB'` | 4 | 0 | **KILLED** (control) |
| C1-f | note with 0 CB rows | `grep -c '^\| CB'` | 0 | **1** | **KILLED**, and rc 1 — operability hazard (see S-G) |
| C1-g | SOURCES with a duplicated S283 row | `grep -cE …` | 3 | 0 | **SURVIVED** — class S-B; both S283 rows are NF 13, so the duplicate is invisible to every named check and inflates the ≥283 count |

Header-cause proof (the only difference between the pairs is the table header):

```
$ diff -u c1/d2-note-cb5-noheader.md c1/d-note-cb5.md
@@ -1,3 +1,5 @@
+| CB | aspect | evidence | receipt |
+|---|---|---|---|
 | CB1 | documented mechanism | ... |

$ diff -u c1/e2-note-cb4-noheader.md c1/e-note-cb4.md
@@ -1,3 +1,5 @@
+| CB | aspect | evidence | receipt |
+|---|---|---|---|
 | CB1 | documented mechanism | ... |

$ grep -n "^| CB" c1/d-note-cb5.md
1:| CB | aspect | evidence | receipt |     <-- the header, counted
3:| CB1 | documented mechanism | ... |
4:| CB2 | host boot chain | ... |
5:| CB3 | policy inputs | ... |
6:| CB4 | applicability | ... |
7:| CB5 | unknowns | ... |
rc=0

$ grep -n "^| CB" c1/e-note-cb4.md
1:| CB | aspect | evidence | receipt |     <-- the header, counted
3:| CB1 | ... |
4:| CB2 | ... |
5:| CB3 | ... |
6:| CB4 | ... |
rc=0
```

`^| CB` is a **prefix** match, not a row-identity match: it counts the header row
and would count any cell starting with `CB` (e.g. `| CB_unknown |`). The frozen
≥5 threshold is therefore met by 4 data rows whenever the note's first header cell
is `CB` — the natural header for this table. The contrast with C2 is structural:
C2's regex is row-shaped (`AR<n>`, `OUT-<nnn>`, two hex widths, `located`), so its
header cannot inflate it; C1's is a two-character prefix.

## 5. Survivor classes

| class | defect the counter cannot see | evidence |
|---|---|---|
| **S-A** fabrication / unreferenced commit | a well-formed 40-hex HEAD that no sibling repository contains; row still counts as `located` | C2-c (10, rc 0) vs `git cat-file -e` rc 128 |
| **S-B** row identity / uniqueness | 10 row-shaped lines that do not cover OUT-001…OUT-010 (duplicate + missing id); likewise a duplicated `S<n>` row inflating the ≥283 count | C2-f (10), C1-g (3, both NF 13) |
| **S-C** ordering / adjacency | "S283 directly after S282" — `grep -cE` is order-blind | C1-b (2, order reversed) |
| **S-D** escaping / column count | an escaped pipe changes NF but not the row count; only the separate `awk NF==13` gate sees it, and that gate is not in the counting-command column | C1-c (grep 2 / NF 14) |
| **S-E** header / prefix inflation | the table header satisfies `^| CB`, so ≥5 is met by 4 data rows | C1-e (5) vs C1-e2 (4) |
| **S-F** whitespace fragility *(false negative, not a survivor)* | a space-padded but semantically identical cell drops a legitimate row from the count | C2-e (9 for a valid 10-row table) |
| **S-G** rc semantics *(operability)* | `grep -c` exits 1 when the count is 0, so a `set -e` pipeline or a `cmd && ok` chain misreads "0 rows" as an error and never reaches the comparison | C1-f (0, rc 1) |

S-F note: Markdown strips cell padding when rendering, so `|  kama |` is the same
cell as `| kama |`. The counter is not invariant under that cosmetic change; a
scribe who pads a column for readability silently loses a row. This is a
counter-quality defect, not a defense — it kills the mutant for the wrong reason.

S-E note: the 10 register sibling tokens are all lowercase alphabetic
(`mori, kama, kagi, mado, mori, kumitate, mori, kaidoku, revenger, tameshi`;
`python3 -c` over `corpus/knowledge/adjacency-anchors-r19.json`), so `[a-z]+`
has no *current* false negative from hyphenation, and all eight distinct siblings
have a checkout at the fleet root (`[ -d */\.git ]` listing). The fragility is
whitespace-only today.

## 6. Proposed single counter change (text only — not applied)

Target: the S-A survivor (C2-c). The frozen check is one `grep -c … → 10`; the
proposal replaces **that one command** with a resolve-then-count pipeline that
keeps the identical row shape, resolves every row's HEAD as a commit in the named
sibling checkout, and fails loudly instead of counting an unresolvable row:

```sh
set -o pipefail
grep -E '^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \|' \
     corpus/knowledge/adjacency-recheck-r66.md \
| awk -F'|' '{gsub(/ /,"",$4); gsub(/ /,"",$5); printf "%s\t%s\n", $4, $5}' \
| { n=0; bad=0
    while IFS="$(printf '\t')" read -r sib head; do
      if git -C ../"$sib"-shokunin cat-file -e "$head^{commit}" 2>/dev/null; then
        n=$((n+1))
      else
        echo "UNRESOLVED $sib $head" >&2
        bad=$((bad+1))
      fi
    done
    echo "count=$n"
    [ "$bad" -eq 0 ]
  }
```

Fields 4 and 5 are the sibling and HEAD cells (`| AR1 | OUT-001 | mori | <head> | …`
→ `$1` empty, `$2` AR, `$3` OUT, `$4` sibling, `$5` HEAD). `^{commit}` is required
so a blob/tree hash cannot pass as a HEAD.

Measured in scratch, run from the lane root so `../<sib>-shokunin` resolves
(text-only validation; nothing in the lane was modified):

```
=== a-pristine-10.md ===
count=10
pipeline_rc=0

=== c-fabricated-head.md ===
UNRESOLVED mori fee7b0682d23747d7c197917e52eded5d4f580f7
count=9
pipeline_rc=1

=== f-duplicate-out.md ===
count=10
pipeline_rc=0

=== d-unlocated.md ===
count=9
pipeline_rc=0

=== e-space-padded-sibling.md ===
count=9
pipeline_rc=0

=== b-9-rows.md ===
count=9
pipeline_rc=0
```

So with this one replacement the frozen `→ 10` no longer holds for C2-c (count 9,
rc 1, offending row named) while the conforming table still reads `count=10,
rc 0`. **C2-c is killed; C2-f survives** — the change is deliberately narrow, as
asked, and does not claim to fix S-B.

Limitations, stated so the L1 can price it: the pipeline inherits the `[a-z]+`
whitespace fragility (C2-e still reads 9) and the `[a-z]+` token class; it assumes
the sibling cell names the checkout stem, which is true for all 10 register rows
today.

## 7. Restoration and non-contamination evidence

- No in-place mutation: each mutant is its own file; the pristine fixtures were
  read-only inputs. Their sha256 before and after the entire battery:
  `90b82b99…50f76a3` (c2/a), `ad239e87…c7fdedc` (c1/a), `027e83a4…cea574d` (c1/d)
  — identical in both captures.
- Every fixture lives under `/fast/scratch/hyaku/tsukuroi-r66/M1MutBattery`;
  that directory is deleted before yield, so the bodies needed to reproduce the
  battery are in the appendix.
- Lane writes: only this file and `.ufo/waves/round-66/w1/M1MutBattery.md`.
  No tracked file (`corpus/*`, `SCORECARD.md`, `LOG.md`, `tools/*`, `PROVINCE.md`,
  `SKILL.md`), no `MANIFEST.json`, no `.ufo/state/`, no sibling repo was written.
- No `tools/tsukuroi-census.sh`, no lane selftest, no background job, no
  delegation, no sudo, no pacman transaction, no install.

## Appendix — pristine fixture bodies (reproduce with these bytes)

`c2/a-pristine-10.md` (sha256 `90b82b996dbc77abf55c32ab93862a9662e4a134cfc6e9f5d7a74d42150f76a3`):

```
| AR | OUT | sibling | live HEAD | blob sha256 | status | locator |
|---|---|---|---|---|---|---|
| AR1 | OUT-001 | mori | 91940fa339e38006f8db5bd7d78bb6f037f4d016 | 73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130 | located | PROVINCE.md:9 |
| AR2 | OUT-002 | kama | e75cf680b53484a61709ee1b2787d8dbc6419f74 | 799432d748bd40bcf859de806cc2ef90df069da14c8e5c07bf72250ac411c7a6 | located | PROVINCE.md:12 |
| AR3 | OUT-003 | kagi | c2cab35bc92e57e39e5489bac3386db078345b3f | 4a346e2df81f7b2e649914d0d99da974d6c484caf12fed1c6bd530d106a78523 | located | PROVINCE.md:3 |
| AR4 | OUT-004 | mado | a4046a8216080d4004de3f268c62cf142095ac07 | 1b25bb1e980925b356663602d002c1c15307a0dfac8bfafd9988bd4d8df7464b | located | PROVINCE.md:6 |
| AR5 | OUT-005 | mori | 91940fa339e38006f8db5bd7d78bb6f037f4d016 | 73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130 | located | PROVINCE.md:8 |
| AR6 | OUT-006 | kumitate | 1770305fae20826b39905a8251ddeca6b4957ac4 | fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f | located | PROVINCE.md:3 |
| AR7 | OUT-007 | mori | 91940fa339e38006f8db5bd7d78bb6f037f4d016 | 73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130 | located | PROVINCE.md:12 |
| AR8 | OUT-008 | kaidoku | d1d981d2cc041dda4656c5b01d2c8445d8d17124 | 63920930b77f9604c6ff7f5db8859344ef97fa50de9e4d0028897da4288859ac | located | PROVINCE.md:3 |
| AR9 | OUT-009 | revenger | cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97 | 63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f | located | PROVINCE.md:3 |
| AR10 | OUT-010 | tameshi | 01d586ddbc5fcd78659557c4e93a6ee8517b87d1 | 8006da5db27d2188ff2f3fc20ae402d0d30c7b5c5fcf9ca26c6793d2ff7e080f | located | PROVINCE.md:7 |
```

`c1/a-sources-282-283.md` (sha256 `ad239e87e2710ec304a4e65d1f5ad33604a90ec97457f3d5701f5a5b0c7fdedc`):

```
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S282 | systemd v262 release notes — https://api.github.com/repos/systemd/systemd/releases/tags/v262 | docs | A | The systemd v262 release body own NvPCR/UKI requirement | Changes in the TPM Subsystem, first bullet; release v262 | the UKI must embed a signed PCR policy bound to the initrd phase | mined | 2026-11-03 | on-release | corpus/knowledge/systemd262-credentials-boot-policy-r66.md |
| S283 | systemd v262 release body — https://api.github.com/repos/systemd/systemd/releases/tags/v262 | docs | A | The systemd.credentials_boot_policy= plane on the pinned v262 body | Changes in the system and service manager: | the option accepts strict, tofu, relaxed, off, scoped to the null key | mined | 2026-11-03 | on-release | corpus/knowledge/systemd262-credentials-boot-policy-r66.md |
```

`c1/d-note-cb5.md` (sha256 `027e83a4639ccbd67d0d7dca2f81cf67ec938d1e3c1955fbe095fc9cdcea574d`):

```
| CB | aspect | evidence | receipt |
|---|---|---|---|
| CB1 | documented mechanism | four values strict/tofu/relaxed/off; null-key scope | S283 bullet |
| CB2 | host boot chain | limine protocol: efi; UKI present; stub version | probes/r66-limine-keys.txt |
| CB3 | policy inputs | cmdline token absent; no TPM2; SecureBoot disabled | probes/r66-cmdline.txt |
| CB4 | applicability | verdict with a named falsifier | this note |
| CB5 | unknowns | none open | this note |
```

Mutant bodies are the pristine bodies with the one-line diffs in §2 and §4 applied;
the `noheader` controls are the same rows with the two header lines removed.
