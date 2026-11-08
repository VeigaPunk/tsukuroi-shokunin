# ScoutSources — round-96 w1 — the S390/S391 SOURCES row, the S389 re-open, the Sphinx caveat

Seat: SCOUT (leaf member; no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
@ `a814f24dc31270bca4e8999ac3cd907ecd72f100` (HEAD detached; `refs/heads/master` at the same commit).
Axis: **freshness**. Date: 2026-11-08. Scratch: `/fast/scratch/hyaku/tsukuroi-r96/ScoutSources/`
(created before the first command, removed on exit).
Files written by this seat: **only** `.ufo/waves/round-96/w1/ScoutSources/` (this report + `receipts/`
+ `pins/`) and the wave-level report `.ufo/waves/round-96/w1/ScoutSources.md`. No lane file outside
that seat dir was edited; no lane file was edited at all.
No git/jj mutation was run in the lane (`git rev-parse`, `git log`, `git ls-tree`, `git cat-file`,
`git diff`, `git status`, `git archive` only — all read-only). `git archive` was piped into
`tar x` **inside the scratch dir**, never into the lane.
No tool was installed, upgraded or removed: every command used a preinstalled `curl`, `python3`,
`sha256sum`, `wc`, `cmp`, `git`. **No installs, no updates, no channel.**

**Note on the lane's state at the time of writing.** The registry at HEAD **already carries an
S390 row** — landed by the L1 in commit `59cbfe2f` ("… and corpus entry S390 (census 389->390)"),
which is the commit that also landed `corpus/knowledge/limine-bound-per-component-r96.md` and
`corpus/lessons/round-96.md`. My seat was dispatched to *draft* the S390 row; by the time the
seat ran, the row existed. So this report does three things: it **verifies the landed S390 row
against the source, byte by byte**; it **drafts the corrected row** the landed row needs under
CORPUS.md rule 2 (a correction is a new row whose `teaches` opens `supersedes S0NN —`); and it
**gates both shapes** through `scripts/sources-census.sh validate`. Three findings are filed.

Receipts (all under `.ufo/waves/round-96/w1/ScoutSources/`):

| receipt | content |
|---|---|
| `receipts/pin-table.tsv` | URL, HTTP status, bytes, sha256, access date, local copy for every fetch (4 rows) |
| `receipts/receipt-01-sys-int-info.txt` | the new source: both URL forms, sha256/size, page title, the quoted sentence and where its bytes actually are, the tier-A grounding, and the four things the page does **not** state |
| `receipts/receipt-02-stdtypes-reopen.txt` | the S389 re-open: status, size, sha256, byte-identity with the r95 pin, all four recorded offsets re-measured, and the Sphinx "Last updated" caveat |
| `receipts/receipt-03-s390-row-draft.txt` | the two drafted rows (A and B) in full, and the eight census gates with their exits |
| `receipts/receipt-04-findings.txt` | F1–F4 against the landed S390 row, plus what is correct in it |
| `receipts/receipt-05-lesson-gate-draft.txt` | the `## Gate` draft lines for the lesson |
| `receipts/gate-*.out` | the raw census output for each gate |
| `pins/python-3-sys.html` | the fetched bytes of the new source (280632 bytes) |
| `pins/python-3-stdtypes.html` | the re-opened S389 page (815447 bytes) |

---

## 1. Item 1 — the new source: `sys.int_info.default_max_str_digits`

Fetched (read-only GET), the URL the brief named:

```
$ curl -sS -L -o sys.html -w "HTTP:%{http_code} SIZE:%{size_download} URL:%{url_effective}\n" \
    'https://docs.python.org/3/library/sys.html#sys.int_info.default_max_str_digits'
HTTP:200 SIZE:280632 URL:https://docs.python.org/3/library/sys.html#sys.int_info.default_max_str_digits
```

**Access date: 2026-11-08.** The version-pinned form was fetched as a cross-check and is
**byte-identical** (`cmp` → identical, same sha256, same 280632 bytes):
`https://docs.python.org/3.15/library/sys.html#sys.int_info.default_max_str_digits` → HTTP 200.
(`sys.html` does not redirect; `stdtypes.html` does — `/3/library/stdtypes.html` →
`/3/builtins/stdtypes.html`, 1 redirect.)

```
$ sha256sum pins/python-3-sys.html
a7e005875e4152bcccaf44b9a834c123cc69bf7b66b3b8398aef91cffe77dd0e
$ wc -c pins/python-3-sys.html
280632
```

Page identity: `<title>sys — System-specific parameters and functions — Python 3.15.2 documentation</title>`,
build stamp `Last updated on Nov 08, 2026 (07:53 UTC)` (byte 280348).

### The requested quote and where it actually is

> "The default value for sys.get_int_max_str_digits() when it is not otherwise explicitly configured."

**12 words** (≤ 25). It is the `<dd>` body of the `sys.int_info.default_max_str_digits`
attribute. On the pinned bytes it is **split by the reference link and a newline**, so no single
raw byte resolves it:

| what | raw byte offset in the 280632-byte pin |
|---|---|
| `<dt class="sig sig-object py" id="sys.int_info.default_max_str_digits">` (the anchor element) | **157495** |
| the `id` attribute value `sys.int_info.default_max_str_digits` | **157529** (the `id="` attribute starts at 157525) |
| inner `id="sys.int_info"` | **155979** |
| the visible attribute-name text `default_max_str_digits` | **157698** |
| `<dd><p>` opening | **157844** |
| text run 1 — "The default value for " | **157851** |
| `<span class="pre">sys.get_int_max_str_digits()</span>` | **158032** |
| the newline | **158096** |
| text run 2 — "when it is not otherwise explicitly configured." | **158097** (ends 158142) |
| contiguous in the rendered text (html.parser) | **42794** (whitespace-normalised: 40511) |

**PASS** — page fetched (HTTP 200), pinned with sha256 `a7e00587…` and byte size 280632, the
anchor element `id="sys.int_info.default_max_str_digits"` located (byte 157495), and the quoted
sentence located in full with both of its raw text runs recorded.

### Which text grounds tier A — and what it does NOT state

**Tier A grounding.** The row's scope is *CPython's decimal-conversion limit default*. Tier A is
grounded by the attribute's **own upstream definition**: the CPython project's reference
documentation of the interpreter that implements the limit, i.e. the sentence *"The default value
for sys.get_int_max_str_digits() when it is not otherwise explicitly configured."* The page is
primary and authoritative for exactly that scope — where the limit's default comes from and
what it is called (`sys.int_info.default_max_str_digits`). It is the same tier and the same kind
(`docs`, A) as the sibling S389 row, which the r95 verifier admitted for the same reason.

**What it does NOT state** (checked by byte search on the 280632-byte pin):

| search | count | consequence |
|---|---|---|
| `b"4300"` | **0** | the page never states the default's *numeric* value — that is S389's stdtypes page |
| `b"640"` | **0** | the page never states the check threshold |
| `b"Limine"` | **0** | the page states **no Limine behaviour whatsoever** |
| `b"limine"` | **0** | idem |
| `b"as provided by"` | **0** | the `str_digits_check_threshold` entry names `sys.set_int_max_str_digits()`, `PYTHONINTMAXSTRDIGITS` and `-X int_max_str_digits` but no number |

So the page grounds *the default value of the limit* — that a default exists, and where it is
configured — and nothing else. It cannot certify that 4300 is the number (S389 can), and it says
nothing about Limine, about version components, or about the gate's 9-digit per-component cap
(the lane's own design).

**Host-side confirmation** (read-only, no install):
`python3 -c "import sys; print(sys.int_info.default_max_str_digits, sys.int_info.str_digits_check_threshold)"`
→ **4300 640** on this host's CPython 3.14.8.

---

## 2. Item 2 — the S389 re-open, and the Sphinx "Last updated" caveat

```
$ curl -sS -L -o stdtypes.html -w "HTTP:%{http_code} SIZE:%{size_download} URL:%{url_effective}\n" \
    'https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation'
HTTP:200 SIZE:815447 URL:https://docs.python.org/3/builtins/stdtypes.html      (1 redirect)

$ sha256sum pins/python-3-stdtypes.html
6bf2ce2ba49d30974485266d70aecd4c4eb89334eb73367f3f99bfa036c7e9a8
$ wc -c pins/python-3-stdtypes.html
815447
$ cmp pins/python-3-stdtypes.html .ufo/waves/round-95/w1/ScoutSources/pins/python-3-stdtypes.html
-> BYTE-IDENTICAL to the r95 pin
```

The 4300-digit sentence:

> "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits."

**10 words** (≤ 25), at raw byte **785297** — exactly the offset the landed S389 row records.
All four offsets the S389 row carries re-resolve on today's bytes:

| the S389 row's anchor | measured today |
|---|---|
| `<section id="integer-string-conversion-length-limitation">` byte 780197 | **780197** ✓ |
| inner `<span id="int-max-str-digits">` byte 780256 | **780256** ✓ |
| the `4300` sentence byte 785297 | **785297** ✓ |
| the `ValueError` sentence byte 782228 | **782228** ✓ |

(For completeness: the threshold sentence is at byte 785568, and the page's own exception text
"ValueError: Exceeds the limit (4300 digits) for integer string conversion: value has 5432
digits" at byte 783348.)

**The Sphinx "Last updated" caveat, as the r95 Gate recorded it.** From
`corpus/lessons/round-95.md` line 38 (the "Two notes the L1 must carry with the row", note 2) and
`corpus/lessons/round-95-verifier-spotcheck.md` §3:

> the pin's sha256 is Sphinx-stamp dependent ("Last updated on Nov 08, 2026 (07:53 UTC)" is a
> moving line), so re-verify the row by the page title/version string and the two sentence
> offsets (785297 and 782228), never by the digest — the same caveat S385 already records.

This seat's measurement today: **both** pins carry the same stamp as the r95 pin
(`07:53 UTC`), and the stdtypes page therefore reproduces the r95 digest byte-for-byte; the
sys.html page's digest `a7e00587…` is likewise reproducible today. That equality is a property
of *this* docs build, not a guarantee for the next one — a re-stamp changes the bytes and the
digest with them, while the title and the sentence offsets stay put. The caveat therefore
stands unchanged, and the drafted row cites the offsets, not the digest, as its re-verify handle.

**PASS** — S389 re-opened at HTTP 200, 815447 bytes, sha256 `6bf2ce2b…`, byte-identical to the r95
pin; the 4300-digit sentence at byte 785297; the Sphinx caveat recorded.

---

## 3. Item 3 — the drafted row, in the 11-column schema

Full text of both shapes is in `receipts/receipt-03-s390-row-draft.txt`. **Draft A** is the row
the brief names (id **S390**, `queued`, `180d`, `used-by corpus/knowledge/limine-bound-per-component-r96.md`,
version-pinned URL, the anchor as re-measured above). **Draft B** is the same row re-id'ed
**S391** with `teaches` opened `supersedes S390 —`, because the id S390 is already taken at the
landed tree (CORPUS.md §SOURCES.md rule 2: *append-only; only `status`, `recheck` and `used-by`
change in place; a correction is a new row whose `teaches` opens `supersedes S0NN —`*).

Schema conformance of both drafts, asserted in the generator before writing:

| requirement | Draft A | Draft B |
|---|---|---|
| 11 columns (NF = 13) | ✓ | ✓ |
| no `|` inside any cell | ✓ (asserted per cell) | ✓ (asserted per cell) |
| id `S` + 3 digits, next unused | S390 (free only on a registry without the landed row) | S391 (free at HEAD) |
| source: title — canonical URL | ✓ | ✓ |
| kind `docs` | ✓ | ✓ |
| tier `A` | ✓ | ✓ |
| scope = CPython's decimal-conversion limit default | ✓ | ✓ |
| anchor = section id + byte offset + access date 2026-11-08 | ✓ (`sys.int_info.default_max_str_digits`, bytes 157495 / 157525 / 157851 / 158097, "fetched 2026-11-08") | ✓ |
| teaches ≤ 25 words | ✓ (12-word quote) | ✓ (12-word quote + supersedes clause) |
| status `queued` | ✓ | `mined` (the used-by path exists at HEAD, so `mined` is the truthful status; `queued` is also clean) |
| opened 2026-11-08 | ✓ | ✓ |
| recheck `180d` | ✓ | ✓ |
| used-by `corpus/knowledge/limine-bound-per-component-r96.md` | ✓ (exists at HEAD `a814f24d`) | ✓ |

**PASS** — a conforming row is drafted for the id the brief names (A) and for the id the contract
requires at the landed tree (B).

---

## 4. Item 4 — the census gate on the appended row

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
    --file <mirror>/corpus/SOURCES.md
```

Every mirror is a `git archive` extract of the lane (read-only) in scratch, or a copy of the
lane's `corpus/`; nothing in the lane was written.

| gate | shape under test | exit | E findings | notes |
|---|---|---|---|---|
| **GATE 0** | HEAD `a814f24d` extract, row untouched (baseline) | **0** | 0 | final line `file ok …/final/corpus/SOURCES.md`; the lane's 57 W04 + 1 W01 warning set unchanged |
| **GATE 1** | HEAD extract + **Draft B** appended (S391) | **0** | 0 | no S390/S391 findings; 58 W (the pre-existing 57 W04 + 1 W01) |
| **GATE G** | HEAD extract with the landed S390 removed + **Draft A** appended (id S390, `queued`) | **0** | 0 | proves Draft A is itself a clean row |
| **GATE D** | HEAD extract + S391 keeping S390's URL *and* scope, `teaches` opened `supersedes S390` | **0** | 0 | the census waives E04 for a row that declares supersession |
| GATE INPLACE | HEAD extract with S390's anchor cell edited in place | 0 | 0 | census-clean but **breaks CORPUS.md rule 2** (anchor is not one of the three in-place cells) — not recommended |
| GATE NEG (control) | S391 with S390's URL **and** S390's scope, no supersedes clause | 1 | **E04** | `S391 duplicate url docs.python.org/3/library/sys.html within scope the configured default of CPython's int-to-str decimal-conversion digit limit, the cap a parser that hands a component to int() must bound itself` — the census refusing an uncorrected duplicate |
| GATE NEG2 (control) | S391 with S390's URL but a **different** scope, no supersedes clause | 0 | 0 (W04 only) | `W04 S391 duplicate url docs.python.org/3/library/sys.html across scopes` — a same-URL row at a *different* scope is only a warning; the E04 error fires only when the scope matches too |
| GATE F (control) | Draft A appended under id S390 while the landed S390 is present | 1 | **E03** | `S390 duplicate id` — this is why the row cannot keep the id S390 at the landed tree |

**PASS** — the appended row gates clean: **exit 0, no E findings** (the expected exit 0; the 58
W findings are the pre-existing warning baseline, which the contract permits). The negative
controls confirm the census is actually discriminating, not merely permissive: E04 fires for a
same-URL+same-scope duplicate that does not declare supersession, and E03 fires for a reused id.

**Raw output**: `receipts/gate-0-baseline.out`, `gate-1-s391-appended.out`,
`gate-G-draftA-as-S390.out`, `gate-D-s391-same-url-supersedes.out`, `gate-inplace.out`,
`gate-neg.out`, `gate-neg2.out`, `gate-F-duplicate-id.out`.

---

## 5. Findings against the row the L1 already landed (S390)

Full detail in `receipts/receipt-04-findings.txt`. Summary:

**F1 — the anchor byte does not resolve to the quoted sentence.** The landed row cites
"byte 157653 of the 2026-11-08 pin (sha256 `a7e00587…`)". On that exact pin, byte 157653 is a
**single space** inside the tag `<span class="sig-name descname">` (tag starts at 157648;
`b[157653:157654] == b' '`). It is not the attribute id (157529), not the visible name text
(157698), and not any part of the quoted sentence (157851 / 158097). The sentence's bytes are
split by the reference link and a newline, so no single raw byte can resolve it — the anchor
must cite the two text runs (or the rendered-text offset 42794). **The same wrong byte is
repeated in `corpus/lessons/round-96.md`'s Gate table** ("(byte 157653)"), so the lesson's Gate
record carries it too.

**F2 — the source URL is the rolling `/3/` alias, not version-pinned.** The lane's own precedent
is `S385`, which supersedes `S377` precisely because "a version-pinned URL keeps the locator from
drifting with the next Python release" (r93 ScoutSource note, `r92-rows-freshness.md` §1), and
the sibling r95 row `S389` uses the version-pinned form. Measured today the two URL forms are
byte-identical, so this is a **drift exposure, not a current factual error** — but the next
Python release moves `/3/` and the row's locator and the "Python 3.15.2 documentation" title in
its anchor cell stop agreeing.

**F3 — the scope cell states a design consequence the source does not state.** The landed scope
reads "…the cap a parser that hands a component to int() must bound itself". The page says only
what the default value of `sys.get_int_max_str_digits()` is; it says nothing about parsers,
components or caps. This is the QUALITY.md 66 shape. (The lesson's Gate *prose* may describe the
row's usefulness in those terms — that is fine; the scope **cell** is the claim the row stands
for.) The drafted scope keeps the claim inside what the page says.

**F4 — what the page does not state** (see §1): no 4300, no 640, no Limine. The landed `teaches`
cell correctly stops at the quoted sentence and imports no Limine behaviour, so this is a scope
limit, not a defect in the landed `teaches` cell.

**What is correct in the landed row** (verified, not assumed): the quote is verbatim and 12
words; the sha256 prefix reproduces this seat's independent fetch exactly; the `used-by` path
exists at HEAD (`git ls-tree` → blob `061ddb94…`), so `mined` is not dangling; the row is
census-clean at HEAD (GATE 0, exit 0, 0 E). The landed row is a **valid row that is slightly
mis-anchored** — the fix is a superseding row (CORPUS.md rule 2), which GATE 1 proves validates.

---

## 6. What the L1 is asked to do

1. Land **Draft B** (S391, `supersedes S390 —`) in `corpus/SOURCES.md` after the S390 row — the
   correction CORPUS.md rule 2 requires, gated clean at exit 0 (GATE 1). Draft B's `used-by`
   path `corpus/knowledge/limine-bound-per-component-r96.md` exists at HEAD, so `mined` is
   truthful; if the L1 prefers `queued`, the census is equally clean (GATE G).
2. Correct the byte in `corpus/lessons/round-96.md`'s Gate table for S390, or record the S391
   supersession there with the two text-run offsets (157851 / 158097) — the draft lines are in
   `receipts/receipt-05-lesson-gate-draft.txt`.
3. Consider version-pinning S390's URL (F2) or leaving the drift to the superseding row (Draft B
   already uses the version-pinned form).

## 7. Tooling

No tool was installed, upgraded or removed. Every command used a preinstalled binary (`curl`,
`python3`, `sha256sum`, `wc`, `cmp`, `grep`, `awk`, `sed`, `git`, `tar`). No pacman transaction
was run (pacman is paused host-wide); no `uv`/`npx`/`~/.local/bin` write. **No installs, no
updates, no channel.**

---

## Verdict per expected line

| # | expected | observed | verdict |
|---|---|---|---|
| 1 | `https://docs.python.org/3/library/sys.html#sys.int_info.default_max_str_digits` fetched (read-only GET), pinned under the seat dir | HTTP 200, 280632 bytes, sha256 `a7e005875e4152bcccaf44b9a834c123cc69bf7b66b3b8398aef91cffe77dd0e`, pinned at `pins/python-3-sys.html` | **PASS** |
| 2 | HTTP status, byte size, sha256 recorded | 200 / 280632 / `a7e00587…` | **PASS** |
| 3 | byte offset + verbatim quote "The default value for sys.get_int_max_str_digits() when it is not otherwise explicitly configured." (≤25 words) | 12 words, verbatim; raw text runs at 157851 and 158097 (rendered-contiguous at 42794) — the offset is split across the link markup, so both runs are recorded | **PASS** (offset resolved and reported as the two runs it actually is) |
| 4 | which text grounds tier A, and what it does NOT state (no Limine behaviour) | tier A = the attribute's own upstream definition in the CPython reference docs; does not state: 4300 (0 occurrences), 640 (0), Limine (0), "as provided by" (0) | **PASS** |
| 5 | S389 re-open: status, size, sha256 | HTTP 200, 815447 bytes, sha256 `6bf2ce2b…`, byte-identical to the r95 pin | **PASS** |
| 6 | the 4300-digit sentence offset | byte 785297 — identical to the landed S389 row's offset | **PASS** |
| 7 | the Sphinx "Last updated" caveat from the r95 Gate | recorded and quoted (round-95.md:38; round-95-verifier-spotcheck.md §3); both pins carry the same stamp today and reproduce the r95 digest, but the digest is not the re-verify handle | **PASS** |
| 8 | S390 row drafted in the 11-column schema, no `\|` inside any cell | Draft A (id S390, as the brief names) and Draft B (id S391, the shape rule 2 requires at the landed tree); NF = 13; no `|` in any cell | **PASS** |
| 9 | gate the append: mirror the lane's corpus/ in scratch, append the row, `sources-census.sh validate --file <mirror>/corpus/SOURCES.md` → exit 0 (warnings allowed) | **exit 0**, 0 E findings, 58 W (the pre-existing baseline); negative controls confirm the gate discriminates (E03 duplicate id, E04 duplicate url within the same scope) | **PASS** |
| 10 | (additional) the landed S390 row's anchor resolves to its quote | it does not — byte 157653 is markup whitespace (F1) | **FAIL** (filed as F1) |
| 11 | (additional) the landed S390 row's URL is version-pinned | it is the rolling `/3/` alias (F2) | **FAIL** (filed as F2) |
| 12 | (additional) the landed S390 row's scope stays inside what the source states | it adds a parser-cap consequence the page does not state (F3) | **FAIL** (filed as F3) |

**Receipts' paths.** All under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-96/w1/ScoutSources/`:
`report.md` (this file), `receipts/pin-table.tsv`, `receipts/receipt-01-sys-int-info.txt`,
`receipts/receipt-02-stdtypes-reopen.txt`, `receipts/receipt-03-s390-row-draft.txt`,
`receipts/receipt-04-findings.txt`, `receipts/receipt-05-lesson-gate-draft.txt`,
`receipts/gate-0-baseline.out`, `receipts/gate-1-s391-appended.out`,
`receipts/gate-G-draftA-as-S390.out`, `receipts/gate-D-s391-same-url-supersedes.out`,
`receipts/gate-inplace.out`, `receipts/gate-neg.out`, `receipts/gate-neg2.out`,
`receipts/gate-F-duplicate-id.out`, `pins/python-3-sys.html`, `pins/python-3-stdtypes.html`.

{"seat":"ScoutSources","verdict":"findings","notes":"Fetched and pinned docs.python.org/3/library/sys.html (200, 280632 B, sha256 a7e00587...) and re-opened S389's stdtypes page (200, 815447 B, sha256 6bf2ce2b..., byte-identical to the r95 pin; 4300 sentence at 785297 as recorded). The 12-word quote is verbatim; its bytes are split by the reference link, so it resolves at raw text runs 157851 and 158097 (rendered-contiguous 42794) - byte 157653, which the landed S390 row cites, is markup whitespace (F1). The page states no 4300, no 640 and no Limine behaviour (F4). Drafted the row in the 11-column schema (Draft A id S390; Draft B id S391 supersedes S390, the shape CORPUS.md rule 2 requires because S390 already landed in 59cbfe2f); no '|' in any cell, NF=13. Gate: scripts/sources-census.sh validate --file <mirror>/corpus/SOURCES.md -> exit 0, 0 E findings, 58 W (pre-existing baseline); negative controls fire E03 (duplicate id) and E04 (duplicate url within scope). Three findings filed against the landed row: F1 mis-anchored byte, F2 rolling /3/ URL not version-pinned (S385/S389 precedent), F3 scope cell states a parser-cap consequence the source does not state. The r95 Sphinx 'Last updated' caveat recorded verbatim. No tool installed or upgraded."}
