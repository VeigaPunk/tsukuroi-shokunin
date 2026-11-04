status: complete
verdict: counter HELD on all ten frozen clauses (11/11 self-tests, every isolation fixture fires its own token); two instrument gaps found (content-free `quote=""` is admitted — defect; duplicate registry ids shadow each other — limitation) and five named lexical limits proven (scripted non-reader, negation with tokens kept, unanchored quote, duplicated row content, copied declared rows). The three pinned snapshots re-measure byte-exact against upstream systemd v262.

# E1Counter — the frozen C1 counter attacked as an adversary

Seat: L2 attack seat, tsukuroi lane round 73 (hyaku run 15), wave w1.
Item: exercise `tools/count-ul-rows-r73.py` as its adversary — re-run its self-test and
absence controls, build an independent mirror of the note, write a scripted non-reader,
isolate every frozen clause, and prove the negation blind spot. **The tool was not edited.**

## Axes

1. **Clause falsification** — does every frozen clause fire when only that clause is violated?
2. **Non-reading admission** — can a writer that never reads the sources satisfy the predicate?
3. **Provenance** — are the three committed "v262" snapshots actually the v262 bytes?
4. **Frozen identity / hermeticity** — is the scored instrument the declared one, and does its
   self-test stay inside `$TMPDIR`?

## 1. Frozen identity and controls

Counter sha256 `542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6` — matches the
declaration's frozen digest. Git blob of the tool is identical at the declaration commit, at HEAD,
and in the worktree:

```
$ git rev-parse 749371321c00f04d98c29d2c26b57d75a92d7e37:tools/count-ul-rows-r73.py
26ce286b66e34b0fc618b9342b3eb708c05249f2
$ git rev-parse HEAD:tools/count-ul-rows-r73.py
26ce286b66e34b0fc618b9342b3eb708c05249f2
$ git hash-object tools/count-ul-rows-r73.py
26ce286b66e34b0fc618b9342b3eb708c05249f2
```

Self-test (`S=/fast/scratch/hyaku/tsukuroi-r73/E1Counter; TMPDIR=$S python3 tools/count-ul-rows-r73.py --selftest`):

```
PASS (SELFTEST-CONTROL) rc=0 expect=0 token=UL_TARGET
PASS (SELFTEST-SHORT) rc=1 expect=1 token=statement-words
PASS (SELFTEST-UNREGISTERED) rc=1 expect=1 token=source-unregistered
PASS (SELFTEST-QUOTE) rc=1 expect=1 token=quote-absent
PASS (SELFTEST-FIVE) rc=1 expect=1 token=UL_ROWS=5
PASS (SELFTEST-DUPID) rc=1 expect=1 token=duplicate-id
PASS (SELFTEST-REUSE) rc=1 expect=1 token=snapshot-reuse
PASS (SELFTEST-UNGROUNDED) rc=1 expect=1 token=statement-grounding
PASS (SELFTEST-MALFORMED) rc=1 expect=1 token=malformed-row
PASS (SELFTEST-DIGEST) rc=1 expect=1 token=digest-mismatch
PASS (SELFTEST-OWNWORK) rc=1 expect=1 token=source-kind
SELFTEST: PASS (11 cases, 11 passed, 0 failed)
rc=0
```

Self-test environment guards (all rc 2, no tree left behind — `$S` contained only my fixtures after
the passing run):

```
$ env -u TMPDIR python3 tools/count-ul-rows-r73.py --selftest
SELFTEST: FAIL (SELFTEST-TMPDIR) $TMPDIR names no directory
rc=2
$ TMPDIR=/nonexistent-xyz python3 tools/count-ul-rows-r73.py --selftest
SELFTEST: FAIL (SELFTEST-TMPDIR) $TMPDIR names no directory
rc=2
$ TMPDIR=/tmp python3 tools/count-ul-rows-r73.py --selftest
SELFTEST: FAIL (SELFTEST-HERMETIC) TMPDIR is /tmp
rc=2
```

Absence controls — base, declaration and HEAD all read rc 128:

```
$ python3 tools/count-ul-rows-r73.py --revision eb1057575d5d8b940c4846e21611674cf5571aea
UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md
rc=128
$ python3 tools/count-ul-rows-r73.py --revision 749371321c00f04d98c29d2c26b57d75a92d7e37
UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md
rc=128
$ python3 tools/count-ul-rows-r73.py --revision HEAD
UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md
rc=128
```

## 2. Independent mirror — six rows this seat wrote from the pinned snapshots

Fixtures are built by `w1/E1Counter/build_fixtures.py` (mirror + clause isolation + scripted
control + negation) and `w1/E1Counter/build_more.py` (second battery). The mirror copies
`before/src` unchanged and supplies a registry with S304–S306 (XML=docs, unit.c/install.c=code).
No row is copied from the tool's `SAMPLE_ROWS`; each quote was asserted whitespace-normalized
verbatim in its snapshot at build time (the builder aborts otherwise).

```
$ python3 tools/count-ul-rows-r73.py --fixture $S/fx/mirror
UL_ROW ok UL1 source=S304 snapshot=systemd.unit.xml
UL_ROW ok UL2 source=S304 snapshot=systemd.unit.xml
UL_ROW ok UL3 source=S305 snapshot=unit.c
UL_ROW ok UL4 source=S305 snapshot=unit.c
UL_ROW ok UL5 source=S306 snapshot=install.c
UL_ROW ok UL6 source=S306 snapshot=install.c
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1
rc=0
```

The six rows (full text in `w1/E1Counter/mirror-note.md`; quotes are code/doc evidence, not prose
reconstructions):

| row | claim I derived | quote I located |
|---|---|---|
| UL1 | earlier load-path directory overrides a same-name unit lower in the list | `Unit files are loaded from a set of paths determined during compilation, described in the two tables below.` |
| UL2 | `$SYSTEMD_UNIT_PATH` replaces the compile-time path; a trailing colon appends it | `the contents of this variable overrides the unit load path` |
| UL3 | reload when the recomputed drop-in list differs, or a stored drop-in is newer | `if (!strv_equal(u->dropin_paths, dropins))` |
| UL4 | a masked unit stays fresh while `null_or_empty` holds for its fragment path | `return !null_or_empty(&st);` |
| UL5 | mask writes a `/dev/null` symlink, runtime flag selects the runtime config dir | `config_path = (flags & UNIT_FILE_RUNTIME) ? lp.runtime_config : lp.persistent_config;` |
| UL6 | a dangling alias is reported as a dangling install change and ignored | `case INSTALL_CHANGE_IS_DANGLING:` |

So the predicate is satisfiable by genuine reading — it is not a false-negative instrument.

## 3. Scripted non-reader control (QUALITY 81)

`build_fixtures.py` also writes `scripted`: for each snapshot it takes **the first line with 4–24
words and no `|`/`"`** as the quote and a **16-token block of the file's own most frequent tokens**
as the statement. No one reads the text; the quote is a licence header.

```
$ python3 tools/count-ul-rows-r73.py --fixture $S/fx/scripted
UL_ROW ok UL1 source=S304 snapshot=systemd.unit.xml
... (6/6 ok)
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1
rc=0
```

The generated note (`w1/E1Counter/scripted-note.md`) contains rows such as:

```
| UL1 | version doctype refentry public oasis docbook oasis-open docbookx entity entities system custom-entities spdx-license-identifier lgpl-2 or-later systemd | source=S304 | snapshot=systemd.unit.xml | digest=eb9479be… | quote="<!-- SPDX-License-Identifier: LGPL-2.1-or-later -->" |
| UL5 | spdx-license-identifier lgpl-2 or-later include fcntl fnmatch stdio unistd alloc-util bus-common-errors chase conf-files conf-parser constants dirent-util errno-util | source=S306 | snapshot=install.c | digest=c11cd575… | quote="/* SPDX-License-Identifier: LGPL-2.1-or-later */" |
```

**Result: the frozen predicate admits the scripted non-reader (`met=1`, rc 0).** No clause stops it:
the statement-words, grounding and quote-location clauses are all lexical, and the script's
statement is 100 % file vocabulary, so grounding scores 16/16 while saying nothing. The only
clauses that could object are the ones that are *not* about reading (count, id, registry, digest),
and the script satisfies them from the committed fixtures.

## 4. Clause isolation — one fixture per frozen clause

Each fixture is the passing mirror with exactly one mutation; the table records the only finding
that fixture prints (full transcript in `w1/E1Counter/counter-runs.txt`).

| frozen clause | fixture | mutation | printed finding | rc |
|---|---|---|---|---|
| id contiguity | `iso-id` | UL6 renamed UL7 (gap, no duplicate) | `UL_ROW fail ids-not-contiguous` | 1 |
| statement words | `iso-words` | UL1 statement cut to 8 words, still grounded 7/7 | `UL_ROW fail UL1 statement-words=8` | 1 |
| grounding | `iso-ground` | UL1 statement replaced with 13 absent tokens | `UL_ROW fail UL1 statement-grounding=0/13` | 1 |
| source kind | `iso-kind` | registry S306 kind → `own-work` | `UL_ROW fail UL5 source-kind=own-work`, same for UL6 | 1 |
| digest (snapshot bytes) | `iso-digest` | one `\n` appended to the fixture's `unit.c` | `UL_ROW fail UL3 digest-mismatch`, same for UL4 | 1 |
| map binding — digest half | `iso-mapdigest` | `SOURCES.json` `unit.c.sha256` → 64 zeros | `UL_ROW fail UL3 map-digest`, same for UL4 | 1 |
| map binding — URL half | `iso-mapurl` | registry S305 source cell URL removed | `UL_ROW fail UL3 source-not-bound`, same for UL4 | 1 |
| anchor binding | `iso-anchor` | `install.c` removed from S306 anchor cell | `UL_ROW fail UL5 anchor-not-bound`, same for UL6 | 1 |
| quote location | `iso-quote-loc` | one word changed in the UL2 quote | `UL_ROW fail UL2 quote-absent` | 1 |
| quote length | `iso-quote-len` | UL1 quote = a 45-word verbatim run | `UL_ROW fail UL1 quote-words=45` | 1 |
| snapshot reuse | `iso-reuse` | UL3 also cites `systemd.unit.xml` (bindings still correct) | `UL_ROW fail snapshot-reuse systemd.unit.xml=3` | 1 |

Non-isolable / structural notes:

- `source-kind`, `digest-mismatch`, `map-digest`, `source-not-bound`, `anchor-not-bound` are
  registry- or snapshot-scoped, so with 6 rows / 3 snapshots / 2 rows per snapshot each violation
  necessarily names its pair of rows. One row cannot be singled out without changing the row set.
- `snapshot-reuse` can be isolated as a *finding token*, but a third citation of one snapshot
  necessarily misses `UL_SNAPSHOTS>=3` (6 rows, 3 snapshots, max reuse 2 is tight). It fires with
  `UL_SNAPSHOTS=3` in my fixture only because the other two snapshots are still cited.
- A valid row indented by one space is a `malformed-row` (see `iso-indent`): the row regex is
  anchored at column 0. Strict, not lenient — it cannot hide a row, it fails one.

## 5. Blind spot — negation with every token kept

`blind-negate` inserts only `never` into UL1, leaving every other token, the quote, digest and
bindings untouched. The statement is now false:

```
| UL1 | Unit files are loaded from a compilation-time path list, and a unit file found in an earlier directory never overrides the same name lower in the list | source=S304 | snapshot=systemd.unit.xml | digest=eb9479be… | quote="Unit files are loaded from a set of paths determined during compilation, described in the two tables below." |
```

```
$ python3 tools/count-ul-rows-r73.py --fixture $S/fx/blind-negate
UL_ROW ok UL1 source=S304 snapshot=systemd.unit.xml
... 6/6 ok
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1
rc=0
```

**Proven and recorded as a named limit, not a defect**: the predicate has no semantic clause; a
negated (or otherwise inverted) statement that keeps its vocabulary reads `met=1`. The only
defences are human review and the wave's own claim text — the instrument cannot supply them.

## 6. Additional admitted variants (second battery)

| fixture | attack | observed | class |
|---|---|---|---|
| `iso-emptyquote` | `quote=""` — a row with no evidence at all | `UL_ROWS=6 UL_VERIFIED=6 … met=1` rc 0 | **defect D1** |
| `iso-onewordquote` | `quote="override"` — one common word | `met=1` rc 0 | defect D1 (instance) |
| `iso-unanchored` | load-path statement, quote from the XML licence header | `met=1` rc 0 | named limit (quote not tied to claim) |
| `iso-dupecontent` | UL2 repeats UL1's statement and quote byte-for-byte | `met=1` rc 0 | named limit (no uniqueness clause) |
| `iso-shadow` | corrupt S305 source cell, then append a second S305 row carrying the URL | `met=1` rc 0 | **limitation D2** |
| `iso-fabricated` | all three snapshots replaced with "Fabricated …" prose; map and digests made self-consistent | `met=1` rc 0 | named limit (provenance is not bound, see §7) |
| `declared-spec` | the wave spec's own six rows (`w1/L1Entry/note.md`, untracked) | `met=1` rc 0 | expected: the declaration fixes the rows |

The `declared-spec` row set carries the same six statements, quotes and snapshots as the tool's
`SAMPLE_ROWS` (`identical_rows=6/6`, compared after cell extraction). It is the
declared answer, so its pass is expected; it also shows the admission is copyable from the
declaration and from the frozen tool, which is why the mirror in §2 — not the self-test CONTROL —
is the discriminating control.

## 7. Provenance — re-opened at the pinned tag

I fetched the three v262 URLs named in `before/src/SOURCES.json` (read-only network) and compared
sha256 with the committed bytes and with `SHA256SUMS`:

```
systemd.unit.xml upstream=eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6
unit.c          upstream=47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7
install.c       upstream=c11cd57579931f04ab08f17fe058fd9d4a962c0fe5c4c4a9d5ae2e86c7e6ef4d
```

All three match the committed snapshots and `SHA256SUMS` exactly, so the "byte-exact v262"
premise of C1 holds **on this reading**. It is worth being explicit that the C1 counter itself
never checks this: `iso-fabricated` proves that a fabricated snapshot plus a matching
`SOURCES.json` plus matching rows reads `met=1`. The file↔upstream binding lives outside the
instrument and must be evidenced separately (this table, or a one-line `curl` + `sha256sum` in the
wave). Recommend the closure note carry that command and its output.

## Survived (attacks the predicate admitted)

| # | attack | command | observed |
|---|---|---|---|
| 1 | scripted non-reader (licence header quote, frequency tokens) | `--fixture $S/fx/scripted` | `met=1` rc 0 |
| 2 | negation with all tokens kept | `--fixture $S/fx/blind-negate` | `met=1` rc 0 |
| 3 | empty quote, `quote=""` | `--fixture $S/fx/iso-emptyquote` | `met=1` rc 0 |
| 4 | one-word quote, `quote="override"` | `--fixture $S/fx/iso-onewordquote` | `met=1` rc 0 |
| 5 | statement and quote from different regions | `--fixture $S/fx/iso-unanchored` | `met=1` rc 0 |
| 6 | duplicated row content (UL1 == UL2) | `--fixture $S/fx/iso-dupecontent` | `met=1` rc 0 |
| 7 | duplicate registry id shadows a corrupt row | `--fixture $S/fx/iso-shadow` | `met=1` rc 0 |
| 8 | fabricated snapshots + self-consistent map | `--fixture $S/fx/iso-fabricated` | `met=1` rc 0 |
| 9 | declared rows copied from spec/tool | `--fixture $S/fx/declared-spec` | `met=1` rc 0 |

## Killed (predicate fired)

| # | attack | command | observed |
|---|---|---|---|
| 1 | id gap (UL1..UL5, UL7) | `--fixture $S/fx/iso-id` | `ids-not-contiguous` rc 1 |
| 2 | statement of 8 words, still grounded | `--fixture $S/fx/iso-words` | `statement-words=8` rc 1 |
| 3 | ungrounded token soup | `--fixture $S/fx/iso-ground` | `statement-grounding=0/13` rc 1 |
| 4 | own-work registry kind | `--fixture $S/fx/iso-kind` | `source-kind=own-work` rc 1 |
| 5 | snapshot byte changed | `--fixture $S/fx/iso-digest` | `digest-mismatch` rc 1 |
| 6 | map digest changed | `--fixture $S/fx/iso-mapdigest` | `map-digest` rc 1 |
| 7 | registry source cell loses the URL | `--fixture $S/fx/iso-mapurl` | `source-not-bound` rc 1 |
| 8 | anchor cell loses the basename | `--fixture $S/fx/iso-anchor` | `anchor-not-bound` rc 1 |
| 9 | quote absent from snapshot | `--fixture $S/fx/iso-quote-loc` | `quote-absent` rc 1 |
| 10 | 45-word quote | `--fixture $S/fx/iso-quote-len` | `quote-words=45` rc 1 |
| 11 | third citation of one snapshot | `--fixture $S/fx/iso-reuse` | `snapshot-reuse systemd.unit.xml=3` rc 1 |
| 12 | indented valid row | `--fixture $S/fx/iso-indent` | `malformed-row` + `ids-not-contiguous` + `UL_ROWS=5` rc 1 |
| 13 | note absent at base / declaration / HEAD | `--revision …` | `UL_NOTE absent` rc 128 |
| 14 | self-test tamper cases | `--selftest` | 11/11 PASS |
| 15 | self-test outside a private TMPDIR or with none | `--selftest` with unset/absent/`/tmp` | rc 2 |

## Defect and limits

### D1 (defect) — a content-free quote is admitted

`quote=""` passes every clause: `words("") == 0 <= MAX_QUOTE_WORDS`, no `|`, and
`norm("") in norm(snap)` is `True`, so `quote-absent` never fires. A UL row can therefore carry
**no evidence at all** and still read `UL_VERIFIED`, which defeats the row's purpose. Proven above
(`iso-emptyquote`). The self-test has no empty/short-quote case.

Proposed repair (the tool is frozen; the L1 owns the edit and the re-run of the before control):

1. At line 44-45, add one constant:

```python
MAX_QUOTE_WORDS = 25
MIN_QUOTE_WORDS = 4
MAX_SNAPSHOT_REUSE = 2
```

2. At the quote checks (around line 229-233), replace:

```python
            if "|" in quote:
                problems.append("quote-pipe")
            if words(quote) > MAX_QUOTE_WORDS:
                problems.append(f"quote-words={words(quote)}")
```

with:

```python
            if "|" in quote:
                problems.append("quote-pipe")
            if words(quote) < MIN_QUOTE_WORDS:
                problems.append(f"quote-short={words(quote)}")
            if words(quote) > MAX_QUOTE_WORDS:
                problems.append(f"quote-words={words(quote)}")
```

3. Add the missing self-test case before `case("CONTROL", None, 0, "UL_TARGET")`:

```python
    def empty_quote(root):
        p = root / NOTE
        out = []
        for l in p.read_text().splitlines():
            if l.startswith("| UL1 |"):
                l = re.sub(r'quote="[^"]*"', 'quote=""', l)
            out.append(l)
        p.write_text("\n".join(out) + "\n")

```

and after `case("MALFORMED", malformed, 1, "malformed-row")`:

```python
    case("EMPTYQUOTE", empty_quote, 1, "quote-short")
```

Threshold check: the six declared rows have quotes of 19, 20, 11, 9, 5 and 10 words (shortest is
UL5 `Unit %s is masked, ignoring.`), so `MIN_QUOTE_WORDS = 4` keeps the declared set valid while
killing the empty and one-word attacks. `re` is already imported by the tool.

### D2 (limitation) — duplicate registry ids shadow silently

`registry_rows` builds a dict keyed by `S###`; a later duplicate overwrites an earlier one, so the
last row wins. `iso-shadow` keeps a corrupt S305 (no URL) in the table and appends a second S305,
and the note reads `met=1` — the registry then contains two conflicting rows for one id with no
finding. Proposed minimal change at lines 147-151 (first row wins, so an earlier defect stays
visible):

```python
        rows.setdefault("S" + m.group("n"), {
            "source": cells[2] if len(cells) > 2 else "",
            "kind": (cells[3] if len(cells) > 3 else "").strip(),
            "anchor": cells[6] if len(cells) > 6 else "",
        })
```

If the lane prefers loud detection, have `registry_rows` also return the duplicate id set and emit
`UL_ROW fail registry-duplicate S###` from `evaluate` (larger change; both keep the clause set).

### Named limits (no repair proposed; they bound what the instrument can claim)

- **Semantics** — negation with the same tokens passes (§5). No textual predicate can decide truth.
- **Quote/claim coupling** — `iso-unanchored` passes; the quote is located in the snapshot anywhere,
  not near or about the statement's subject.
- **Row uniqueness** — `iso-dupecontent` passes; two rows may share statement and quote.
- **Repository provenance** — the counter checks note↔file↔map↔registry consistency, never
  file↔upstream; `iso-fabricated` passes. Verified separately in §7.
- **Substring bindings** — `source-not-bound`/`anchor-not-bound` are substring tests; my mirror's
  cells (`mirror unit.c — <url>`, anchors with prose around the basename) pass by construction.
- **Self-test CONTROL identity** — its rows are the tool's `SAMPLE_ROWS`, byte-identical to the
  wave spec's rows; the self-test scores mechanics only (its own comment says so), and the
  discriminating control for C1 is an independent mirror like §2.

## Artifacts

| path | content |
|---|---|
| `w1/E1Counter/report.md` | this report |
| `w1/E1Counter/counter-runs.txt` | every command and its full output (self-test, guards, 22 fixtures) |
| `w1/E1Counter/mirror-note.md`, `mirror-registry.md` | my six rows and the mirror registry |
| `w1/E1Counter/scripted-note.md`, `scripted-picks.txt` | scripted non-reader and its selections |
| `w1/E1Counter/blind-negate-note.md` | negation proof row |
| `w1/E1Counter/fabricated-note.md` | provenance-limit fixture |
| `w1/E1Counter/declared-spec-note.md` | the wave spec's rows scored |
| `w1/E1Counter/build_fixtures.py`, `build_more.py` | fixture builders (assert every quote verbatim) |

No tool was installed or upgraded (`pacman` paused and unused; no `uv`/`npx`/binary fetch). The
only network use was the read-only `curl` of the three v262 raw files in §7. Scratch
`/fast/scratch/hyaku/tsukuroi-r73/E1Counter` was removed before yielding; nothing outside
`w1/E1Counter/` and `w1/E1Counter.md` was written.
