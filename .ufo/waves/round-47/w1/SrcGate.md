VERDICT: defect-found

Seat SrcGate (roster id `SrcGate-2`), lane round 47 / w1, item F-1 — sources discipline for
round 47. Lane `tsukuroi-shokunin`, read-only throughout: no lane file created, edited or
deleted; no git/jj mutation in the lane; no host mutation; no tool installed. Scratch
`/fast/scratch/hyaku/tsukuroi-r47/SrcGate-2/` (removed at end; receipts copied first).
Counted revision for all reads: `77e9e2b2e96b85d8f048ae2087e246a542b71611`; base
`916019057147d7e9ba6b137647b2cee26decf4b8`. Lane HEAD at seat start was `f6bc6d05`.

Headline: **(a) and (b) pass with clean exits.** The S252 row parses as a well-formed
11-data-column registry row and the round touches no other row. **(c) produces the draft, and
the quote is on the page — but two fidelity defects stand in the Gate material**: the lesson
names the snapshot file `mktemp.1.html` while the frozen file is `mktemp.html` (F2), and the
`-t` line that S252 pins does not reach the code path the row claims to ground (F1). Both are
cheap to fix before integration; neither invalidates the fetch or the digest.

---

## (a) S252 row parses — PASS

Row bytes (`corpus/SOURCES.md:261`, identical at base+1, at the freeze revision and in the
worktree — `git diff 77e9e2b..HEAD` and `git diff HEAD` on the file are both empty):

```
| S252 | Linux man-pages mktemp(1) — https://man7.org/linux/man-pages/man1/mktemp.1.html | docs | A | Where mktemp places the template when TMPDIR is set — the census selftest fixture-base contract | page fetched 2026-10-27, raw HTML (sha256 74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266) | -t interpret TEMPLATE as a single file name component, relative to a directory: $TMPDIR, if set | mined | 2026-10-27 | 180d | corpus/lessons/round-47.md |
```

Column split (`awk -F'|'`, receipt `04-s252-row-fields.txt`): `NF=13 data_fields=11` — the
registry contract's 11 columns (`id source kind tier scope anchor teaches status opened
recheck used-by`), no cell containing a literal or escaped `|` (`grep -c '\|'` over the row
= 0), single `S252` id (no E03 duplicate), `kind=docs`, `tier=A`, `status=mined`,
`opened=2026-10-27` = today, `recheck=180d` (valid `NNd` form; E09 does not fire), and
`used-by=corpus/lessons/round-47.md` resolves to a real file (5186 bytes,
`ls -l` in receipt `04`).

Registry command and exit, as briefed:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
… 40 × "W04 … duplicate url … across scopes" (S038 … S230) …
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
exit=0
```

Row count (`census` mode, receipt `02-census-counts.txt`): `tsukuroi rows 252`,
`FLEET rows 252`, `FLEET.tier.invalid 0`, `FLEET.status.invalid 0`, `FLEET.missing 0`,
`exit=0`. The 39 W04 warnings are pre-existing duplicate-URL warnings across *other* rows;
none names S252, and warnings never change a clean lane's status.

**The validator is live, not decorative** — I mutated a byte-identical fixture copy of the
registry (`sha256 c91520a2…` = lane HEAD's file) inside a fixture lane root and re-ran
`validate --root … mirror`; each defect class fires with `exit=1`
(receipt `07-mutant-battery.txt`):

| mutant on S252 | validator |
|---|---|
| baseline (unmutated) | `ok`, exit 0 |
| `recheck=180` / `recheck=180D` | `E09 S252 recheck=…`, exit 1 |
| `status=watch` | `E07 S252 status=watch`, exit 1 |
| `kind=doc` | `E05 S252 kind=doc`, exit 1 |
| `tier=D` | `E06 S252 tier=D`, exit 1 |
| `opened=2027-01-01` | `E08 S252 opened=2027-01-01`, exit 1 |
| `used-by … round-47-nope.md` | `E11 S252 missing used-by …`, exit 1 |
| `id=S25` | `E02 S25`, exit 1 |
| escaped pipe `\|` in the anchor cell | `E01 S252 fields=12`, exit 1 |

(F3, note not defect: `recheck=soon` passes — `symbolic()` at
`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:582` accepts any
`^[A-Za-z][A-Za-z0-9 _-]*$`. That laxness is fleet-wide and pre-existing; S252 uses the
stricter `180d`, so it is unaffected.)

## (b) Round-wide SOURCES delta — PASS, S252 insertion only

```
$ git -C …/tsukuroi-shokunin diff 9160190… 77e9e2b2… -- corpus/SOURCES.md
@@ -258,6 +258,7 @@
 | S249 | …
 | S250 | …
 | S251 | …
+| S252 | Linux man-pages mktemp(1) — … | docs | A | … | mined | 2026-10-27 | 180d | corpus/lessons/round-47.md |
 
 ## Paths
```

`--stat`: `1 file changed, 1 insertion(+)`. No deletion, no edit to any pre-existing row, no
second hunk (receipt `03-sources-diff.txt`). Registry row count 251 → 252. `9160190..HEAD` on
the file is byte-identical to the above (the post-freeze commit `f6bc6d05` does not touch
SOURCES.md), and the worktree copy equals HEAD. **No row was touched old→new in any way other
than the S252 insertion** — nothing to re-check against a changed S252 predecessor.

## (c) Gate entry draft + verbatim check — quote present, draft supplied

Verbatim check against the frozen fetch
`.ufo/waves/round-47/frozen/src/mktemp.html` (9832 bytes, 237 lines, sha256
`74186433…3266` = the row's pin = `frozen/src/SHA256SUMS`). After HTML tag strip and
whitespace collapse the row's teaches text is present:

```
quote_words = 16            (≤ 25 ✓)
present_after_tagstrip_and_whitespace_collapse = True
present_as_raw_byte_substring = False   (inline <b>-t</b>, a run of spaces, and the page
                                         continues "; else the")
page_context = "-t interpret TEMPLATE as a single file name component, relative to a
                 directory: $TMPDIR, if set; else the directory specified via -p ; else
                 /tmp [deprecated]"
```

so the quote is verbatim **modulo markup and run-length whitespace** — state it that way; it
is not a raw byte substring of the HTML (receipts `05-quote-verbatim.txt`).

Live re-open, access date 2026-10-27 (`06-live-refetch.txt`): `curl -sS` →
`http_code=200 size=9832`; `sha256sum` live = `74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266`;
`cmp` live vs frozen → no output, `cmp_exit=0`. **The frozen snapshot is byte-identical to a
fresh fetch nine hours after capture**, which is the receipt the lesson's line 31
("Live re-open and byte-compare: wave seat SrcGate receipt") asks for.

### Draft — Gate new-row table entry (matches the lesson's current 4-column header)

```markdown
| S252 | https://man7.org/linux/man-pages/man1/mktemp.1.html (access 2026-10-27) | "-t interpret TEMPLATE as a single file name component, relative to a directory: $TMPDIR, if set" (16 words) | frozen/src/mktemp.html lines 101-103, `-t` description (snapshot sha256 74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266) |
```

Differences from the entry now in `corpus/lessons/round-47.md:27`, all fidelity fixes:
location `mktemp.1.html` → `frozen/src/mktemp.html` (F2), plus explicit line range and the
digest so the quote can be re-checked without the digest prose at line 29; access date moved
into the URL cell so the row is self-contained if the header changes.

### Draft (recommended) — if F1 is accepted, the *registry row* also needs its scope/teaches narrowed

```markdown
| S252 | Linux man-pages mktemp(1) — https://man7.org/linux/man-pages/man1/mktemp.1.html | docs | A | Where mktemp takes a template's parent directory from $TMPDIR: only with -t / --tmpdir; the census selftest passes an absolute TEMPLATE, so its fixture base is the harness's own filter, not mktemp's | page fetched 2026-10-27, raw HTML lines 94-103 (sha256 74186433c4e851311ded2cc0f8b14acab913d1c9ba1a2ef9a436548a9c073266) | -t places the template under $TMPDIR if set; -p uses $TMPDIR when DIR is omitted; without either, the page states no $TMPDIR rule, and a probe of coreutils 9.12 shows an explicit template being used as given | mined | 2026-10-27 | 180d | corpus/lessons/round-47.md |
```

11 data columns, no pipe inside any cell (checked by the same `awk -F'|'` count above when
applied to the string). If the L1 prefers not to rewrite the freeze-time row, the minimum
honest alternative is to keep the row and add one limit sentence under the Gate table:
"the -t clause documents TMPDIR precedence for `-t` only; the selftest calls
`mktemp -d` with an absolute template, so this row does not ground the fallback."

## Findings

**F1 — the pinned anchor does not reach the code path it is cited for.** The census
selftest's fixture base is built at
`tools/tsukuroi-census.sh:2055-2059`:

```
2055:  local st_base=${TMPDIR:-/tmp}
2056:  case "$st_base" in
2057:    *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
2058:  esac
2059:  work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")
```

That is `mktemp -d` with an **explicit absolute TEMPLATE**, and the TMPDIR-vs-/tmp decision is
the harness's own `case`, executed *before* mktemp runs. mktemp's `$TMPDIR` rule (the quoted
`-t` line, `mktemp.html:101-103`, and the `-p` form at `94-97`) is therefore never consulted on
that line; DESCRIPTION (`mktemp.html:77-78`, "If TEMPLATE is not specified … `--tmpdir` is
implied") is also out of scope because a template *is* specified. Live probe on this host
(coreutils 9.12, scratch only, receipt `08-anchor-vs-codepath.txt`): `TMPDIR` set + `-t` → the
file lands in `$TMPDIR`; `TMPDIR` set + plain relative template → lands in cwd, `TMPDIR`
ignored; `-d` with absolute template (the census shape) → the template path is used as given.
So the row's scope cell ("Where mktemp places the template when TMPDIR is set — the census
selftest fixture-base contract") overstates the anchor's reach: the S252 text is true, the
contract it is attached to is the harness's filter. This is the round-46 F-style
"anchor adjacent, not binding" shape and it costs one scope-cell edit to close now.

**F2 — snapshot filename is wrong in the lesson (not in the registry).**
`corpus/lessons/round-47.md:27` says `mktemp.1.html, the -t option description` and line 29
says "(`mktemp.1.html `74186433…`)". The frozen file is
`.ufo/waves/round-47/frozen/src/mktemp.html` and `frozen/src/SHA256SUMS` lists `mktemp.html`.
A reader following the lesson's location lands on a nonexistent path. Fix both mentions.

**F3 — (note, out of scope for S252) recheck validation accepts any word.** `symbolic()`
(`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:582`) matches
`^[A-Za-z][A-Za-z0-9 _-]*$`, so `recheck=soon` validates clean (`07-mutant-battery.txt`).
Fleet-wide, pre-existing, not introduced this round; flagged only so the Gate does not claim
"valid recheck" as a strong check.

**F4 — tool-environment caveat, not host evidence.** In this seat's bash wrapper the token
`mktemp` reports as a shell builtin and answers `--version` with `mktemp 0.8.0`; under
`sh -c`, `bash -c` and `bash --noprofile --norc` it resolves to `/usr/bin/mktemp` (GNU
coreutils 9.12, same inode as `/bin/mktemp`, inode 13516849). Every mktemp observation above
was therefore re-run through `env -i PATH=/usr/bin:/bin sh -c …`. No lane claim should cite
the wrapper's version string.

## What I did not do

- Did not re-run the census selftest or any C1/C2 counter (not my item; cost guard).
- Did not write, edit or stage any lane file; my only lane writes are this report and
  `.ufo/waves/round-47/w1/SrcGate/` (8 receipts, 36 KB).
- Did not verify that the two `(R47-C2)` pinning cases pass — that is the C2 seats' verdict.
- Did not touch the pre-existing dirty lane file `.ufo/waves/round-47/w1.ready.partial`
  (already ` M` in `git status` at seat start, one line deleted; not mine).
- The 40 W04 duplicate-URL warnings in the fleet run were not triaged (pre-existing, not S252).

## Receipts

`.ufo/waves/round-47/w1/SrcGate/` — `01-validate-root.txt` (fleet validate, exit 0),
`02-census-counts.txt` (rows 252, invalid 0), `03-sources-diff.txt` (round diff + stat +
counts), `04-s252-row-fields.txt` (column split, escaped pipes, used-by, SHA256SUMS),
`05-quote-verbatim.txt` (tag-strip/word count), `06-live-refetch.txt` (HTTP 200, digest, cmp),
`07-mutant-battery.txt` (nine mutants, E01–E11 with exits), `08-anchor-vs-codepath.txt`
(code lines, page lines, mktemp probes, binary identity, wrapper caveat).

Tools installed: none. Host commands: read-only (`git show/diff`, `grep`, `awk`, `curl`,
`sha256sum`, `cmp`, `mktemp` under scratch, `ls`, `stat`, `sed -n`). Scratch removed.
