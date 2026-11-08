# SOURCES rows for round 100 — S396 (own-work) and S397 (docs)

Draft only. `corpus/SOURCES.md` was NOT edited by this seat (binding rule: a scout writes under its
own seat dir only). Contract v1 column order is
`id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by` —
11 columns, `NF=13` with the leading/trailing pipes.

## 0. Id collision — read this first

**`S396` and `S397` are already taken in the lane's HEAD tree.** The lane tip when this seat was
dispatched is `c450cd68` ("round-100: land — … SOURCES S396-S398"), whose parent is the wave-w1
dispatch commit `60b5636f`; `743ce449` (the freeze) is the grandparent.

```bash
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show HEAD:corpus/SOURCES.md \
  | grep -oE 'S[0-9]+' | sort -u | tail -3
# S397
# S398
# S5
```

At the **freeze tip** `743ce449` the maximum was `S395` and `S396`/`S397` were indeed the next free
ids — the same command against that blob prints `S394 / S395 / S5`, i.e. `S396` and `S397` were
free. But the L1 landed rows under those two ids in `c450cd68` while this wave was running, so at
scoring time they are **occupied**:

```bash
git -C … show HEAD:corpus/SOURCES.md | awk 'NR==407||NR==408'   # the two rows
# | S396 | tsukuroi round-100 instruments — … |
# | S397 | CPython `re` module — regular expression operations (https://docs.python.org/3/library/re.html) | …
```

`S399` and `S400` are the next unused ids at HEAD (both `grep -c` → 0).

**Decision for the L1:** do **not** land a second row under `S396`/`S397` — ids are never reused
(contract v1 rule 2), and a duplicate id is census code `E03`. The rows that landed in `c450cd68`
are **this seat's rows** (same subjects, same byte anchors, verified below byte-for-byte). This
file is therefore the *provenance and verification record* of the landed `S396`/`S397`, not a new
proposal, and it carries the two anchor corrections the landed rows still need.

## 1. The two rows as they stand at HEAD (`c450cd68`), byte-verified

Both rows are byte-identical to `HEAD:corpus/SOURCES.md` lines 407-408
(`receipts/landed-rows-S396-S397.txt`, 1589 bytes, `awk -F'|'` → `NF=13` on both lines, i.e. the
11-column contract shape holds, and neither cell contains a literal `|`).

### S396 — own-work, tier A

```
| S396 | tsukuroi round-100 instruments — the component-keyed echo bends and the registry label-set binder (`tools/make-r100-bends.py`, `tools/check-registry-content-r100.py`, own-work) | own-work | A | which reported gate field a component-keyed bend must falsify, and how one registry cell's N-label set is bound across separators | generator emission lines at BYTE 2615 (N12) and BYTE 3384 (N13) of the 4471-byte file (sha256 7ccfe69e…); checker `def parse_label_set` at BYTE 12134 and `TOKEN`/`SEPARATORS` at BYTEs 12025/12073 of the 38009-byte file (sha256 7a23a522…), all at the round-100 freeze 743ce449 | An echo lie keyed on one version component makes exactly the family that asserts that spelling fail, and a fullmatch-tokenised label set binds a union cell while refusing prose and suffix tokens | mined | 2026-11-08 | 180d | corpus/knowledge/limine-echo-bends-r100.md, corpus/lessons/round-100.md |
```

Anchor-by-anchor, re-measured on the pinned bytes (`grep -abo`, QUALITY 141):

| the row's anchor claim | my independent byte measurement | verdict |
|---|---|---|
| generator emission line at BYTE 2615 (N12) | `grep -abo '"limine_version": ("999999998.9.9"'` → **2615** | agrees |
| generator emission line at BYTE 3384 (N13) | `grep -abo '"limine_version": ("12.999999998.4"'` → **3365**; `grep -abo '"12.999999998.4" if'` → **3384** | **partial** — 3384 is the `if`-clause start, not the emission-line start (3365). Both offsets point inside the same one-line substitution; see §2.1 |
| checker `def parse_label_set` at BYTE 12134 | **12134** | agrees |
| checker `TOKEN` at BYTE 12025 | `grep -abo 'TOKEN'` → **12025** (the `TOKEN = re.compile(...)` definition) and 12657 (the `TOKEN.fullmatch(part)` call site) | agrees — 12025 is the definition |
| checker `SEPARATORS` at BYTE 12073 | `grep -abo 'SEPARATORS'` → **12073** (the definition) and 12567 (the use) | agrees — 12073 is the definition |
| generator is the 4471-byte file, sha256 `7ccfe69e…` | `git show 743ce449:tools/make-r100-bends.py` → 4471 bytes, sha256 `7ccfe69e52604ec5bb8db423e377cf9f0eb468baf03d0ef7be77b3209654e695` | agrees |
| checker is the 38009-byte file, sha256 `7a23a522…` | `git show 743ce449:tools/check-registry-content-r100.py` → 38009 bytes, sha256 `7a23a522871ab5dd33a94ae51b09c70ab182a0d2a53d7380f82bb11a13f3c2d2` | agrees |

Both generator offsets land on the *same kind* of thing only if the unit is named. N12's 2615 is
the start of the whole `"limine_version": ("…` clause; N13's 3384 is the start of the falsified
value `"12.999999998.4" if`, 19 bytes inside the clause. The unit the row uses for N12 ("emission
line") and the unit it uses for N13 ("emission line") are therefore different, and the row does not
say so. This is the finding in §2.1.

The N12 offset also appears verbatim in the *emitted* bend (`git show 743ce449:.ufo/waves/round-100/before/controls/bends/N12-x-echo.py`,
sha256 `eb247e16…`, 30409 bytes) at BYTE 16931, and the N13 bend (`…/N13-y-echo.py`, sha256
`e1e5916f…`, 30446 bytes) at BYTE 16931 — the same gate line, same byte, one changed clause in
each (`diff -u` against the gate `7d79ac29…` shows exactly one `-`/`+` line pair per bend).

### S397 — docs, tier A

```
| S397 | CPython `re` module — regular expression operations (https://docs.python.org/3/library/re.html) | docs | A | the two primitives the label-set tokeniser relies on: `fullmatch` anchoring a token to the whole part, and `\b` as a word boundary | `id="re.fullmatch"` at BYTE 111489 and its sentence at BYTE 112171; the `\b` sentence at BYTE 69787 of the 2026-11-08 fetch (257722 bytes, sha256 69d64759…) | `re.fullmatch` requires the whole token to match, so a letter suffix cannot ride along, and `\b` asserts a word boundary rather than a literal character | mined | 2026-11-08 | 180d | corpus/knowledge/limine-echo-bends-r100.md, corpus/lessons/round-100.md |
```

| the row's anchor claim | my independent byte measurement | verdict |
|---|---|---|
| `id="re.fullmatch"` at BYTE 111489 | `bytes.find(b'id="re.fullmatch"')` → **111489** | agrees |
| "its sentence at BYTE 112171" | `bytes.find(b'If the whole <em>string</em> matches the regular expression <em>pattern</em>, return a')` → **112171** | agrees on the offset; see §2.2 for the quote-text defect |
| the `\b` sentence at BYTE 69787 | `bytes.find(b'Matches the empty string, but only at the beginning or end of a word.')` → **69787** (verbatim, 14 words) | agrees |
| the 2026-11-08 fetch is 257722 bytes, sha256 `69d64759…` | `curl` → HTTP **200**, `size_download=257722`, sha256 `69d64759ed7e269bd617470594dfb8c7970b61fa4def81530a5ea2953d42493b`; a second fetch (`re2.html`) is byte-identical (`cmp` → identical) | agrees — the page is stable across two fetches |

The page's own "Last updated" line, for the freshness record:
`bytes.find(b'Last updated on Nov 08, 2026 (14:27 UTC).')` → **257438**.

## 2. Findings for the L1 — two defects in the landed rows

Both are recorded here because this seat may not edit `corpus/SOURCES.md`, `corpus/lessons/`, or
`corpus/knowledge/` (binding rules). Each is a *text* defect in a landed row/lesson, not a defect
in the measured instruments.

### 2.1 S396's N13 offset is measured on a different unit than its N12 offset (routed, needs a wording amendment)

The row says "generator emission lines at BYTE 2615 (N12) and BYTE 3384 (N13)". Re-measured:

* N12 — `grep -abo '"limine_version": ("999999998.9.9"'` → **2615**: the start of the whole
  `"limine_version": ("…` clause.
* N13 — `grep -abo '"limine_version": ("12.999999998.4"'` → **3365**: the same unit.
* 3384 is `grep -abo '"12.999999998.4" if'` → the start of the *falsified value*, 19 bytes into the
  clause.

So "2615 (N12)" is a clause start and "3384 (N13)" is a value start. A reader re-measuring N13 the
way the row measures N12 lands on **3365**, and one measuring it the way the row states lands on
**3384** — the row names no unit, so it is not self-consistent. QUALITY 141 requires the offset's
unit to be named; the row names neither.

Both numbers are true offsets of true things, and both point inside the N13 substitution, so no
measured claim is falsified. What is wrong is the *pairing*: the row presents them as one kind of
thing.

**Proposed amendment** (append-only, in the round's amendment slot; the frozen `claims.json`
sentence is untouched — this is the SOURCES row's anchor cell, not the claim):

> generator emission lines at BYTE 2615 (N12) and BYTE 3365 (N13), each the start of the
> `"limine_version": ("…` clause in the 4471-byte file (sha256 7ccfe69e…); the N12 falsified value
> `"999999998.9.9" if` at BYTE 2634 and the N13 falsified value `"12.999999998.4" if` at BYTE 3384;
> checker `def parse_label_set` at BYTE 12134, `TOKEN` at BYTE 12025 and `SEPARATORS` at BYTE 12073
> of the 38009-byte file (sha256 7a23a522…), all at the round-100 freeze 743ce449

which names both units (clause start and value start) for both bends, so any reader re-measures to
the same four numbers.

### 2.2 The lesson's S397 located quote is not verbatim in the fetched bytes (routed)

`corpus/lessons/round-100.md`'s Gate block quotes, for S397:

> `If the whole string matches the regular expression pattern, return a corresponding match object`
> (BYTE 112171, under `id="re.fullmatch"` at BYTE 111489)

The offset is right. The **quote text is not in the file**:

```bash
bytes.find(b'If the whole string matches the regular expression pattern, return a corresponding match object')
# → -1   (not found)
```

The bytes at 112171 are the HTML source with markup:

```
If the whole <em>string</em> matches the regular expression <em>pattern</em>, return a
corresponding <a class="reference internal" href="#re.Match" title="re.Match"><code class="xref py py-class docutils literal notranslate"><span class="pre">Match</span></code></a>.  Return <code class="docutils literal notranslate"><span class="pre">None</span></code> if the string does not match
the pattern; note that this is different from a zero-length match.
```

Stripping the tags yields "…return a corresponding **Match**." — a class reference, not "a
corresponding match object". Two consequences:

1. The quote as printed is a **paraphrase, not a located quote**: it is not a substring of the
   pinned bytes, so it cannot be re-found at 112171 by `bytes.find`/`grep -abo`. A "located quote"
   that is not present at its own offset is not located.
2. "a corresponding match object" is not the page's wording for that sentence — the page writes
   "a corresponding `Match`" (the `re.Match` class). The phrase "match object" does occur on the
   page, but at BYTE **57131**, in an unrelated table cell ("when processing match object *m*").

**Proposed replacement quote** (verbatim in the fetched bytes, ≤25 words):

| row | quote (verbatim) | byte | words |
|---|---|---|---|
| S397 | `Matches the empty string, but only at the beginning or end of a word.` | 69787 | 14 |
| S397 | `If the whole <em>string</em> matches the regular expression <em>pattern</em>, return a` | 112171 | 13 |

and the teaches cell should be softened accordingly — the page says `\b` is a word boundary *outside
a set* and a backspace *inside* one (`not a word boundary as outside a set`, BYTE 39044), while the
row's teaches cell says "`\b` asserts a word boundary rather than a literal character" without
naming the outside-a-set condition. The checker's own use (`re.search(r"\bVARIANTS\b(.*)", cell)`,
BYTE 19924) is outside a set, so the taught claim is true of the instrument — but QUALITY 66 (a
teaches cell keeps every branch its quoted source states) wants the in-set branch named, or the
sentence scoped to "outside a character set".

### 2.3 S396's teaches cell — one branch is missing

"An echo lie keyed on one version component makes **exactly the family** that asserts that spelling
fail". The round's own measured target is that the **N12** bend fails **two** families
(`EXPLICIT-VERSION-ECHO` and `REFUSAL-VERSIONS-9DIGIT`) while N13 fails one
(`REFUSAL-VERSIONS-9DIGIT-Y`) — the r99 battery's `check_echo` is set on both the X-cap family and
the explicit-echo family, and both send `999999999.9.9` (battery bytes 79015 / 79893). "exactly the
family" (singular) is therefore wrong for N12. QUALITY 66 wants both branches. Proposed:

> An echo lie keyed on one version component makes exactly the families that assert that spelling
> fail — two for the X-cap spelling, one for the Y-cap spelling

### 2.4 Not a defect, recorded for completeness

The S397 row's `used-by` cites `corpus/knowledge/limine-echo-bends-r100.md` and
`corpus/lessons/round-100.md`. Both exist on disk at HEAD (5972 and 7641 bytes), so census `E11`
(dangling used-by) does not fire — confirmed by the clean `ok` line of the frozen census run.

## 3. Census — before-state, re-derived

The frozen command, run verbatim:

```bash
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --root /home/vgpnk/Projects/shokunin tsukuroi
```

**BEFORE-state (the freeze tip `743ce449`, re-derived by this seat, not copied):** the freeze tree
was extracted read-only with `git archive 743ce449 | tar -x -C <scratch>` and the census run against
that tree:

```
$ bash …/sources-census.sh validate --root <scratch>/beforestate <scratch>/beforestate
… 57 × W04, 1 × W01, then:
beforestate	ok	<scratch>/beforestate/corpus/SOURCES.md
exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' <scratch>/beforestate/corpus/SOURCES.md
395
```

→ **before-state: 395 rows, exit 0**, and the code profile is identical to the after-state
(57 W04 + 1 W01, zero E-codes) — the landing added no new error and no new warning. The two W04s
the frozen receipt `.ufo/waves/round-100/before/census-before-after.txt` names for the BEFORE run
(S386, S387 duplicate URL across scopes) are the last two of the same 57; that receipt's own tail
is consistent with my re-derivation.

**AFTER-state (HEAD `c450cd68`):**

```
$ bash …/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
… 57 × W04, 1 × W01, then:
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
exit=0
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md
398
```

→ **after-state: 398 rows, exit 0**, zero E-codes. Receipts:
`receipts/census-before-743ce449.txt` (59 lines) and `receipts/census-after-head.txt` (59 lines).

## 4. The Gate-quote block the lesson must carry

Reproduced here for the L1's convenience; the landed lesson's block differs on the S397 quote
(§2.2). Word counts are of the quoted string only.

```
## Gate (sources opened this round; contract `CORPUS.md` §SOURCES.md)

| row | source opened 2026-11-08 | tier | located quote (≤25 words) | admit / reject |
|---|---|---|---|---|
| S396 (new, own-work) | `tools/make-r100-bends.py` (sha256 `7ccfe69e…`, 4471 bytes) and `tools/check-registry-content-r100.py` (sha256 `7a23a522…`, 38009 bytes) at the freeze `743ce449` | A | `"limine_version": ("999999998.9.9" if limine_version.split(".")[0] == "999999999" else limine_version)` (BYTE 2615 of the generator, the N12 emission clause); `def parse_label_set` at BYTE 12134 of the checker | **admit** — the row's anchor names both emission sites (clause starts at BYTES 2615 / 3365), the label-set parser and its `TOKEN`/`SEPARATORS` pair (BYTES 12134 / 12025 / 12073), all measured at the BYTE level with `grep -abo` on the pinned bytes (QUALITY 141) |
| S397 (new, docs) | https://docs.python.org/3/library/re.html (HTTP 200, 257722 bytes, sha256 `69d64759…`, footer "Last updated on Nov 08, 2026 (14:27 UTC)") | A | `Matches the empty string, but only at the beginning or end of a word.` (BYTE 69787); `id="re.fullmatch"` at BYTE 111489 | **admit** — grounds the two primitives the tokeniser relies on: `fullmatch` (whole-token match, so a suffix cannot ride along; the `dd` sentence opens at BYTE 112171) and `\b` (word boundary outside a character set) |

Census (frozen command `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin
tsukuroi`): before — 395 rows, exit 0 (re-derived on the `743ce449` tree extracted read-only with
`git archive`); after — 398 rows, exit 0, zero E-codes. Receipts:
`.ufo/waves/round-100/w1/ScoutSources/receipts/census-before-743ce449.txt` and
`…/census-after-head.txt`.
```

Byte-offset unit named, once, for the whole block: **BYTE offset into the named file's bytes**
(`grep -abo` / `bytes.find` on the pinned bytes; QUALITY 141). For `S397` the offsets are into the
2026-11-08 fetch of `https://docs.python.org/3/library/re.html`, 257722 bytes, sha256
`69d64759ed7e269bd617470594dfb8c7970b61fa4def81530a5ea2953d42493b`.

## 5. Scope note

Source anchors only. This seat did not re-run the gate, the battery, the bends, the checker or its
selftest, and did not touch `corpus/SOURCES.md`, `corpus/lessons/`, `corpus/knowledge/`, `tools/`
or `.ufo/plans/`. Two read-only public-document fetches (no credentials, no network write).
`git archive` and `git show` only; no git or jj mutation of any kind.
