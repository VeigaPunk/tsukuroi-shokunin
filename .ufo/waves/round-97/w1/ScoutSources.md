# ScoutSources — round 97 wave w1: the NEW source for the SOURCES row C1 will cite, the two r96 Python-docs rows re-opened, and the r96 false-era-sentence sweep

Seat: `ScoutSources`. Lane: `tsukuroi-shokunin` (git branch master, jj-colocated; no mutating git/jj
command was run). All writes are under this seat dir plus the scratch root
`/fast/scratch/hyaku/tsukuroi-r97/ScoutSources` (deleted at the end of this seat's work).

## 0. Pre-flight: the frozen instrument manifest

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
$ sha256sum -c .ufo/waves/round-97/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r97.py: OK
tools/make-r97-bends.py: OK
tools/check-registry-content.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-97.md: OK
.ufo/waves/round-97/before/plan-frozen.md: OK
.ufo/waves/round-97/claims.json: OK
.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py: OK
.ufo/waves/round-97/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-97/before/controls/do-nothing-registry-coverage.py: OK
.ufo/waves/round-97/before/controls/do-nothing-r96-calibration.py: OK
.ufo/waves/round-97/before/controls/bends/N05-z-cap-8.py: OK
.ufo/waves/round-97/before/controls/bends/N06-leading-zero-reject.py: OK
.ufo/waves/round-97/before/registry-baseline.json: OK
.ufo/waves/round-97/before/fixtures/doctored.diff: OK
.ufo/waves/round-97/before/fixtures/doctored-recipe.txt: OK
.ufo/waves/round-97/before/fixtures/build-doctored-fixture.sh: OK
.ufo/waves/round-97/before/dev/run-dev.sh: OK
```
exit 0, 21/21 OK, 0 FAILED. Receipt: `receipts/instruments-sha256-check.txt`.

No tool was installed or upgraded by this seat (system `curl 8.23.0` / `python3` were already
present; no pacman transaction was made — pacman is paused host-wide).

---

## 1. The round's NEW source for the SOURCES row C1 will cite

### 1a. Fetch (HTTP status, byte count, sha256)

The round's new source is the CPython `int()` constructor page; the row that will cite it is
**S392** in `corpus/SOURCES.md` (worktree, uncommitted: `M corpus/SOURCES.md`), and the knowledge
entry that will cite it is `corpus/knowledge/limine-bound-9digit-z-r97.md`
("S392 documents `int(x, base)`'s string form as optionally carrying 'leading zeros' for an
explicit base, and records that base 0 disallows them").

```
$ curl -sSL -o functions.html -w 'EFFECTIVE=%{url_effective}\nHTTP=%{http_code}\nBYTES=%{size_download}\nREDIRECTS=%{num_redirects}\n' \
    'https://docs.python.org/3/library/functions.html'
EFFECTIVE=https://docs.python.org/3/builtins/functions.html
HTTP=200
BYTES=331022
REDIRECTS=1
$ sha256sum functions.html
d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7  functions.html
```

- **URL requested:** `https://docs.python.org/3/library/functions.html`
- **HTTP status:** `301` → `Location: https://docs.python.org/3/builtins/functions.html` → `200`
  (final `content-length: 331022`, `last-modified: Sun, 08 Nov 2026 07:54:38 GMT`, `server: nginx`)
- **Byte count:** `331022` bytes
- **sha256 of the exact bytes:** `d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7`
- Page title: `Built-in functions — Python 3.15.2 documentation`
- **Pinned bytes saved:** `.ufo/waves/round-97/w1/ScoutSources/pins/int-functions.html`
  (331022 bytes, 0.32 MiB — under the 2 MiB cap, so the whole page is retained as the evidence).
  Its sha256 was re-verified after the copy and equals the value above.
- **The pin is reproducible:** the same sha256 was obtained from three independent fetches — this
  seat's `pins/int-functions.html`, the sibling seat's
  `.ufo/waves/round-97/w1/ScribeLesson/pins/functions.html`, and the lane's own
  `.ufo/waves/round-97/after/gate/functions.html` (all three `d92580dd…`, 331022 bytes).
  The version-pinned URL `https://docs.python.org/3.15/library/functions.html` (301 →
  `/3.15/builtins/functions.html`) serves the **byte-identical** file (`cmp` → identical), so the
  pin is stable across the `/3/` and `/3.15/` locators today.

### 1b. The located quote (≤ 25 words), with BYTE offset, surrounding line and anchor evidence

All offsets below are **byte** offsets into the pinned file `pins/int-functions.html`
(sha256 `d92580dd…`, 331022 bytes), computed by slicing the raw bytes.

**PRIMARY QUOTE — 17 words, byte 159303 … 159682** (the `</p>` terminator), starting on **line 1339**
of the pinned page:

> "Base 0 also disallows leading zeros: int('010', 0) is not legal, while int('010') and int('010', 8) are."

Raw bytes at the offset (the sentence is split across two source lines by the HTML):

```
byte 159303: b'Base\n0 also disallows leading zeros: <code class="docutils literal notranslate"><span class="pre">int(\'010\',</span> <span class="pre">0)</span></code> is not legal, while\n<code class="docutils literal notranslate"><span class="pre">int(\'010\')</span></code> and'
```

Surrounding lines (raw):

```
line 1339: b'in that the actual base is 2, 8, 10, or 16 as determined by the prefix. Base'
line 1340: b'0 also disallows leading zeros: <code ...><span class="pre">int(\'010\',</span> <span class="pre">0)</span></code> is not legal, while'
line 1341: b'<code ...><span class="pre">int(\'010\')</span></code> and <code ...><span class="pre">int(\'010\',</span> <span class="pre">8)</span></code> are.'
```

Why this is the right sentence for C1's `LEADING-ZERO-NORMALIZE` family: it states in one sentence
both halves the family rests on — `int('010')` (base 10 by default) **is** legal with leading
zeros, while the base-0 spelling is not. That is exactly the behaviour the family exercises
(`12.09.4`, `000000012.9.4`, `12.000000009.000000005`, `000000000.000000000.000000000` are
accepted and normalized by `int()`), and it is the sentence the r97 knowledge entry PC2 leans on.

**Supporting sentence (the base-10 half), 5 words, byte 158393, line 1335:**

```
byte 158393: b'default <em>base</em> is 10. The allowed bases are 0 and 2\xe2\x80\x9336. Base-2, -8, and -16'
```
Rendered: "The default base is 10."

**Anchor evidence for the section (`id=` offset):**

- `id="int"` occurs **once** in the whole page, at **byte 153202** (line 1302):
  ```
  byte 153172: b'<dt class="sig sig-object py" id="int">\n<span class="property">...'
  byte 153202: b'id="int">\n<sp'
  ```
  The anchor-bearing element `<dt class="sig sig-object py" id="int">` starts at **byte 153172**.
  So the `https://docs.python.org/3/library/functions.html#int` fragment resolves to the `int`
  class heading at bytes 153172/153202.
- The adjacent anchor-bearing sites that carry the quoted sentence's subject matter:
  `have leading zeros, be surrounded by whitespace,` at **byte 157767** (line 1330);
  `Optionally, the string can be preceded by` at **byte 157540** (line 1329);
  `Base\n0 also disallows leading zeros:` at **byte 159303** (line 1339).

**Note on the alternative sentence (not used as the quote):** "Optionally, the string can be
preceded by + or - (with no space in between), have leading zeros, be surrounded by whitespace, and
have single underscores interspersed between digits." (byte 157540 … 157872) is **29 words** — over
the ≤ 25-word bar — so the 17-word base-0 sentence is the quotable one.

### 1c. FINDING — the S392 row's two cited offsets are CHARACTER offsets, not byte offsets

The landed (worktree) S392 row reads:

```
| S392 | CPython `int()` — built-in functions (https://docs.python.org/3/library/functions.html#int) | docs | A |
   the string form of `int(x, base)`: an explicit base accepts leading zeros, base 0 does not |
   `int` heading (`id="int"` at byte 153028) of the 2026-11-08 pin, sha256 d92580dd… (331022 bytes);
   quoted phrase at byte 157622 | ...
```

Measured against the very pin the row names (`sha256 d92580dd…`, 331022 bytes — the sha256 and byte
count in the row are **correct**):

| S392 cites | read as BYTE offset | read as CHARACTER offset (utf-8 decoded) |
|---|---|---|
| `id="int"` at 153028 | `b'an class="pre">builtins.input/result</span></code>\nwith the '` — **ABSENT** | `'<dt class="sig sig-object py" id="int">\n<span class="pr'` — lands on the **element** carrying the id (the `id="int"` attribute itself is at char 153058) |
| quoted phrase at 157622 | `b'e"><span class="pre">+</span></code> or <code class="docutil'` — **ABSENT** | `'have leading zeros, be surrounded by whitespace,\nand ha'` — lands **exactly** on the quoted phrase |

So S392's two offsets are character offsets of the decoded page presented as byte offsets. This is
inconsistent with the r96 rows on the same table, which are byte offsets and land exactly when read
as bytes (verified in §2). `corpus/lessons/round-97.md:17` repeats the same convention
("byte 157622 of the 331022-byte pin"). The sibling seat `ScribeLesson` measured the same fact
(`.ufo/waves/round-97/w1/ScribeLesson/receipts/05-gate-quote-bytes.txt`).

This is the r96 S390/S391 defect class (a locator whose stated unit does not survive re-reading),
and it is the kind of thing QUALITY 139/140 would catch: the number is certified against a pin
whose bytes are pinned, so it must be re-derived by slicing the pinned bytes. **Recommendation to
the L1 (not applied here — `corpus/` is out of this seat's write scope):** restate S392's anchor as
byte offsets `153202` (`id="int"`) and `157767` (the quoted phrase), or state the unit as characters
explicitly; the sibling row S389/S391 use byte offsets, so byte offsets are the table's convention.

---

## 2. Re-open of the two r96 Python-docs rows

Both re-opens were fetched fresh over HTTPS (curl, `-L`, one redirect for the stdtypes row).

### 2a. S389 — `https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation`

```
$ curl -sSL -o stdtypes.html -w 'EFFECTIVE=%{url_effective}\nHTTP=%{http_code}\nBYTES=%{size_download}\nREDIRECTS=%{num_redirects}\n' \
    'https://docs.python.org/3/library/stdtypes.html'
EFFECTIVE=https://docs.python.org/3/builtins/stdtypes.html
HTTP=200
BYTES=815447
REDIRECTS=1
$ sha256sum stdtypes.html
6bf2ce2ba49d30974485266d70aecd4c4eb89334eb73367f3f99bfa036c7e9a8  stdtypes.html
```
- **HTTP status:** `301` → `Location: https://docs.python.org/3/builtins/stdtypes.html` → `200`
- **Byte count:** `815447`
- **sha256:** `6bf2ce2ba49d30974485266d70aecd4c4eb89334eb73367f3f99bfa036c7e9a8`
- **Comparison with the r96 pin `6bf2ce2b…`:** **byte-identical — no drift.** The r96 row recorded
  815447 bytes / `6bf2ce2b…`; both reproduce exactly. The version-pinned locator
  `https://docs.python.org/3.15/library/stdtypes.html` (→ `/3.15/builtins/stdtypes.html`) serves the
  **same bytes** (`cmp` → identical), so the pin is stable across both locators today.
- The r96 row's own offsets still land exactly when read as bytes (re-verified on the fresh copy):
  `byte 780197` → `b'<section id="integer-string-conversion-length-limitation">'` (element start),
  `byte 780256` → `b'<span id="int-max-str-digits"></span>'`, `byte 785297` →
  `b'The default limit is 4300 digits as provided '`.
- Pinned copy kept at `pins/stdtypes.html`.

### 2b. S391 — `https://docs.python.org/3.15/library/sys.html#sys.int_info.default_max_str_digits`

```
$ curl -sSL -o sys315.html -w 'EFFECTIVE=%{url_effective}\nHTTP=%{http_code}\nBYTES=%{size_download}\nREDIRECTS=%{num_redirects}\n' \
    'https://docs.python.org/3.15/library/sys.html'
EFFECTIVE=https://docs.python.org/3.15/library/sys.html
HTTP=200
BYTES=280632
REDIRECTS=0
$ sha256sum sys315.html
a7e005875e4152bcccaf44b9a834c123cc69bf7b66b3b8398aef91cffe77dd0e  sys315.html
```
- **HTTP status:** `200` (no redirect)
- **Byte count:** `280632`
- **sha256:** `a7e005875e4152bcccaf44b9a834c123cc69bf7b66b3b8398aef91cffe77dd0e`
- **Comparison with the r96 pin `a7e00587…`:** **byte-identical — no drift.** The r96 row recorded
  280632 bytes / `a7e00587…`; both reproduce exactly. (The superseded S390 locator
  `https://docs.python.org/3/library/sys.html` also serves the identical bytes today, sha
  `a7e00587…`, 280632 bytes.)
- The r96 row's own offsets still land exactly when read as bytes: `byte 157525` →
  `b'id="sys.int_info.default_max_str_digits">\n<span cl'`, `byte 157851` →
  `b'The default value for <a class="reference int'`.
- Pinned copy kept at `pins/sys315.html`.

**Both r96 rows re-open as byte-identical, unreachable neither:** admit, unchanged. This matches the
r96 closure judge's own re-open (`.ufo/waves/round-96/before`/spot-check table) and extends it: the
**new** page (S392's `functions.html`) is likewise pin-stable across `/3/` and `/3.15/`.

---

## 3. Sweep for the r96 false docstring sentence

```
$ grep -rn "answers era B for" /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --include='*.py' --include='*.md'
```
15 hits (receipt: `receipts/sweep-answers-era-b-for.txt`, saved verbatim):

| # | file:line | what it is |
|---|---|---|
| 1 | `.ufo/waves/round-96/w1/ReviewBattery.md:244` | r96 review report — **quotes the false sentence to refute it** ("F-B … answers **era A** for that value — correctly") |
| 2 | `.ufo/waves/round-96/w1/ReviewBattery/report.md:244` | same report, seat copy |
| 3 | `.ufo/waves/round-96/w1/ScoutDrift.md:201` | r96 scout report — quotes it, then shows the sentence is "not satisfiable" |
| 4 | `.ufo/waves/round-96/w1/ScoutDrift.md:333` | r96 scout report's final JSON line (embeds the same quoted text) |
| 5 | `.ufo/waves/round-96/w1/ScoutDrift/probe-output.txt:12` | r96 probe output — quotes it while probing it |
| 6 | `.ufo/waves/round-96/w1/ScoutDrift/probes.py:51` | r96 probe script — quotes it ("is not satisfiable") |
| 7 | `.ufo/waves/round-96/w1/ScoutDrift/receipts.txt:154` | r96 probe receipt — the docstring's bytes echoed |
| 8 | `.ufo/waves/round-96/w1/ScoutDrift/report.md:201` | r96 scout report, seat copy |
| 9 | `.ufo/waves/round-96/w1/ScoutDrift/report.md:333` | r96 scout report's final JSON line |
| 10 | `.ufo/waves/round-96/w1/ScribeKnowledge.md:37` | r96 scribe summary — quotes it and corrects it ("X of that value is 0, so an X-only era reader answers era **A**") |
| 11 | `.ufo/waves/round-96/w1/ScribeKnowledge/knowledge-draft.md:110` | r96 knowledge draft — quotes it and calls it "false as written" |
| 12 | `.ufo/waves/round-96/w1/ScribeKnowledge/receipts/make_mutants.py:5` | r96 mutant-maker header comment — quotes it to define the mutant |
| 13 | `.ufo/waves/round-96/w1/ScribeKnowledge/report.md:236` | r96 scribe report — quotes it and calls it false |
| 14 | `.ufo/waves/round-96/w1/ScribeKnowledge/report.md:297` | r96 scribe report's final JSON line |
| 15 | `.ufo/waves/round-97/make-spec.py:129` | the round-97 spec text naming the sweep itself |

The broader sweep (all file types, `grep -rn "answers era B for" .` minus `.git/`) adds exactly two
more hits, and both are the **live/frozen r96 battery bytes**:

| # | file:line | what it is |
|---|---|---|
| 16 | `tools/limine-pin-battery-r96.py:1776` | **the live r96 battery's docstring still asserts the false claim** |
| 17 | `.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py:1776` | the frozen round-97 do-nothing control — byte-identical copy of the above |

(`.../round-97/w1-spec.json:58` and `.../w1-dispatch.json:207` also carry the phrase inside the
dispatch prompt text; they are the spec echoed into the wave dispatch, not assertions.)

### Answers to the two questions the item asks

**Is the r97 instrument's correction the only remaining occurrence?** **No, and the phrasing needs
care.** The r97 instrument `tools/limine-pin-battery-r97.py` does **not** contain the string
"answers era B for" at all — `grep -n "answers era B for" tools/limine-pin-battery-r97.py` exits 1
(no match). The r97 correction **replaced** the sentence with a `LIMIT (r96 CriticClaims F-4, …)`
paragraph, at lines 1786–1790 of the r97 battery:

```
1786:    both; one that applies `<= 8` to Y refuses the cap member and fails. LIMIT (r96 CriticClaims
1787-    F-4, corrected here in r97): an era reader that looks at X alone is NOT caught by this family —
1788-    X=12 and X=0 answer era B and era A correctly for these two members; that reader is caught by
1789-    `EXPLICIT-VERSION-ERA` on its `12.9.4` row. The r96 docstring claimed otherwise; the sentence is
1790-    corrected, the family and its expectation are unchanged."""
```

So the sentence survives in **two** places: the **live** `tools/limine-pin-battery-r96.py:1776` and
its **frozen** twin `.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py:1776`. Both are
the r96 landed bytes:

```
$ sha256sum tools/limine-pin-battery-r96.py .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py
f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba  tools/limine-pin-battery-r96.py
f06d90ae4f0069d41bd1a88da8ebc9e4818bff761a0f30df9e09fbdffae73bba  .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py
```
(receipt: `receipts/r96-battery-vs-control.txt`; the control copy is pinned in
`instruments.sha256` at `f06d90ae…`, so the pair cannot be separated by editing one of them.)

**Does any other file still assert the false claim?** **Yes — `tools/limine-pin-battery-r96.py`
(line 1776), the r96 battery that is still a live, registry-listed tool.** Its docstring says:
"…and one that reads the era from X alone answers era B for `0.999999999.0` and fails." That
sentence is false (an X-only reader answers era **A** for `0.999999999.0`, which is the correct
era, and passes the family 4 of 4 — measured by r96's own `w1/ScribeKnowledge/receipts/mut-M-x-only-era.json`).

Why the correction landed in the successor file rather than in place, and whether that is acceptable:
- `tools/limine-pin-battery-r96.py` is **not** a member of `.ufo/waves/round-97/before/instruments.sha256`,
  but its bytes are frozen *indirectly*: C1's target binds the r96 do-nothing battery as
  "`.ufo/waves/round-97/before/controls/do-nothing-battery-r96.py`, sha256 `f06d90ae…`,
  **byte-identical to the r96 landed bytes**". Editing `tools/limine-pin-battery-r96.py` in round 97
  would break that byte-identity clause and would make the C1 target's do-nothing leg unreadable as
  stated. `tools/check-registry-content.py` also binds that file's roster size by AST count, which a
  docstring edit would not change.
- The r96 battery remains **live and reachable**: it has an operative `SKILL.md` registry row
  (`SKILL.md:5938`), it is cited by `corpus/README.md:1155` and
  `corpus/knowledge/limine-bound-per-component-r96.md`, and `tools/check-registry-content.py` binds
  two of its cells (`RC-ROSTER-VERDICT`, `RC-ROSTER-PINNED` → `tools/limine-pin-battery-r96.py`).
  A reader of the registered tool still reads the false sentence.

**Corpus is clean.** No file under `corpus/`, and no `SKILL.md` / `PROVINCE.md` / `SCORECARD.md`
entry, asserts the false claim (`grep -rn "answers era" corpus/ SKILL.md PROVINCE.md SCORECARD.md` →
no hits). Where the corpus discusses the sentence it states the corrected version:
`corpus/knowledge/limine-bound-per-component-r96.md:60` ("an X-only reader passes it and is caught by
`EXPLICIT-VERSION-ERA` (the Y docstring's claim is false — routed to r97)") and
`corpus/lessons/round-96.md:79` ("such a reader answers `0.999999999.0` as era A (correct)").

**Route to the L1 (a decision, not a blocker):** the routed defect 2/3 from the r96 spot-check
("the Y-family docstring's era claim is false … Lane owes: a docstring correction with its own
manifest") is closed only in the *successor* instrument. The false sentence remains readable in the
live registered `tools/limine-pin-battery-r96.py:1776`, and the C1 do-nothing byte-identity clause
currently prevents correcting it in place. Options for the L1: (a) accept the successor-file
correction and record the surviving r96 string as a known, named limit (the r96 battery is a
superseded instrument); (b) correct `tools/limine-pin-battery-r96.py` in a round whose C1 clause
does not pin its bytes; or (c) amend the C1 do-nothing clause to bind the control copy's bytes
rather than the live file's. This seat did not edit any of these files (out of scope).

---

## 4. A named rejection

**Rejected candidate: `https://man.archlinux.org/man/python.1`** (the second candidate the item
names).

```
$ curl -sSL -o python1.html -w 'EFFECTIVE=%{url_effective}\nHTTP=%{http_code}\nBYTES=%{size_download}\nREDIRECTS=%{num_redirects}\n' \
    'https://man.archlinux.org/man/python.1'
EFFECTIVE=https://man.archlinux.org/man/python3.14.1.en
HTTP=200
BYTES=41788
REDIRECTS=1
$ sha256sum python1.html
11c40ea191395fda4991cd254305162603edf2a0437bcc5341691201ccca10c7  python1.html
```
- HTTP status: `302` → `Location: /man/python3.14.1.en` → `200`; 41788 bytes;
  sha256 `11c40ea191395fda4991cd254305162603edf2a0437bcc5341691201ccca10c7`;
  page title `python3.14(1) — Arch manual pages`.
- **Reason for rejection: the page states no behaviour about `int()`'s string form.** It is the
  interpreter's command-line manual (NAME / SYNOPSIS / DESCRIPTION / OPTIONS / ENVIRONMENT).
  A text scan of the fetched bytes finds **zero** occurrences of "leading zero", "int(",
  "base 10", "base 8" and "radix"; the single hit for "decimal" is unrelated
  (`PYTHONHASHSEED … The integer must be a decimal number in the range [0,4294967295]`).
  It therefore cannot ground C1's `LEADING-ZERO-NORMALIZE` family or S392's "an explicit base
  accepts leading zeros, base 0 does not" claim — it is a **generic** manual page with no
  behaviour for the cited claim. (It is also a *moving* target: `python.1` currently redirects to
  the `python3.14.1` build, so the URL is a version alias, not a pinned locator.)
- Pinned copy kept at `pins/python1-arch-man.html` (evidence of the rejection).

**Also checked and rejected as a duplicate:** `https://docs.python.org/3/library/functions.html#int`
is the **same resource** as item 1 — the fragment is stripped by the 301, the final URL and the
bytes are identical:

```
$ curl -sSL -o /dev/null -w 'final=%{url_effective} http=%{http_code} bytes=%{size_download}\n' \
    'https://docs.python.org/3/library/functions.html#int'
final=https://docs.python.org/3/builtins/functions.html http=200 bytes=331022
```
sha256 `d92580dd…` — identical to item 1. It is one source, not two, and the `#int` fragment
adds no bytes.

---

## 5. Receipts (all written by this seat, under this seat dir)

| path | content |
|---|---|
| `.ufo/waves/round-97/w1/ScoutSources/pins/int-functions.html` | the pinned new source, 331022 bytes, sha256 `d92580dd…` (under 2 MiB; whole page retained) |
| `.ufo/waves/round-97/w1/ScoutSources/pins/stdtypes.html` | re-opened S389 page, 815447 bytes, sha256 `6bf2ce2b…` |
| `.ufo/waves/round-97/w1/ScoutSources/pins/sys315.html` | re-opened S391 page, 280632 bytes, sha256 `a7e00587…` |
| `.ufo/waves/round-97/w1/ScoutSources/pins/python1-arch-man.html` | the rejected candidate, 41788 bytes, sha256 `11c40ea1…` |
| `.ufo/waves/round-97/w1/ScoutSources/receipts/fetches.json` | machine-readable fetch record: URL, final URL, HTTP status, byte count, sha256, redirect count for all five fetches |
| `.ufo/waves/round-97/w1/ScoutSources/receipts/sweep-answers-era-b-for.txt` | the verbatim grep output of §3 (15 lines) |
| `.ufo/waves/round-97/w1/ScoutSources/receipts/instruments-sha256-check.txt` | `sha256sum -c` of the frozen manifest, 21/21 OK |
| `.ufo/waves/round-97/w1/ScoutSources/receipts/r96-battery-vs-control.txt` | sha256 of `tools/limine-pin-battery-r96.py` and its frozen do-nothing twin (both `f06d90ae…`) |
| `.ufo/waves/round-97/w1/ScoutSources/report.md` | this report |

Scratch root `/fast/scratch/hyaku/tsukuroi-r97/ScoutSources` was deleted after the last measurement
(every byte cited above lives under this seat dir). No file outside this seat dir and the scratch
root was written; no mutating git/jj command was run; no tool was installed.

---

## 6. PASS/FAIL per expected line

| expected line | verdict | evidence |
|---|---|---|
| Fetch `https://docs.python.org/3/library/functions.html` over HTTPS; record HTTP status, byte count, sha256 of the exact bytes | **PASS** | 301 → 200 (final `/3/builtins/functions.html`); 331022 bytes; sha256 `d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7` |
| Locate a ≤ 25-word sentence about decimal-string conversion of an integer (leading zeros / base 10) | **PASS** | "Base 0 also disallows leading zeros: int('010', 0) is not legal, while int('010') and int('010', 8) are." — 17 words; supporting "The default base is 10." (5 words) |
| Report the quote's BYTE offset and the surrounding line | **PASS** | bytes 159303–159682; lines 1339–1341 (raw lines quoted in §1b) |
| Report the `id=` anchor offset of the section if present | **PASS** | `id="int"` at byte 153202 (line 1302); the anchor-bearing `<dt class="sig sig-object py" id="int">` starts at byte 153172; only occurrence in the page |
| Save the pinned bytes under `pins/int-functions.html`, under 2 MiB | **PASS** | `.ufo/waves/round-97/w1/ScoutSources/pins/int-functions.html`, 331022 bytes (0.32 MiB), sha256 re-verified after the copy |
| Re-open `…/stdtypes.html#integer-string-conversion-length-limitation`; compare sha256 with the r96 pin `6bf2ce2b…` | **PASS** | 301 → 200; 815447 bytes; sha256 `6bf2ce2ba49d…` → **byte-identical, no drift** |
| Re-open `…/3.15/library/sys.html#sys.int_info.default_max_str_digits`; compare sha256 with the r96 pin `a7e00587…` | **PASS** | 200 (no redirect); 280632 bytes; sha256 `a7e005875e41…` → **byte-identical, no drift** |
| Record for each page whether byte-identical, drifted, or unreachable | **PASS** | both byte-identical; none unreachable |
| Sweep `grep -rn "answers era B for" … --include='*.py' --include='*.md'` and report every hit with file:line | **PASS** | 15 hits, all listed in §3 with file:line; verbatim output in `receipts/sweep-answers-era-b-for.txt` |
| State whether the r97 instrument's correction is the only remaining occurrence | **PASS (answer: no)** | the r97 battery does not contain the string at all (`grep` exit 1); it replaced it with the `LIMIT (r96 CriticClaims F-4 …)` paragraph at lines 1786–1790; the sentence survives in `tools/limine-pin-battery-r96.py:1776` and its frozen twin `…/before/controls/do-nothing-battery-r96.py:1776` |
| State whether any other file still asserts the false claim | **PASS (answer: yes)** | `tools/limine-pin-battery-r96.py:1776` — a live, `SKILL.md`-registered tool (row `SKILL.md:5938`) and a `check-registry-content.py` binding target; corpus/`SKILL.md`/`PROVINCE.md`/`SCORECARD.md` are clean |
| Report a reject decision with its reason | **PASS** | `https://man.archlinux.org/man/python.1` → 302 → `/man/python3.14.1.en` 200, 41788 bytes — rejected: generic interpreter manual, zero mentions of leading zeros / int() / radix, so it states no behaviour for the cited claim (and `python.1` is a moving version alias) |

**Extra finding (not an expected line, reported because it bears on the row C1 will cite):** the
S392 row's two anchor offsets (153028, 157622) are **character** offsets presented as byte
offsets — read as bytes they land on unrelated markup; read as characters they land exactly. The
sha256 and byte count in the row are correct. Detail in §1c.

{"seat":"ScoutSources","verdict":"findings","notes":"All 4 items met with receipts under .ufo/waves/round-97/w1/ScoutSources/ (pins/ + receipts/ + report.md). New source fetched: https://docs.python.org/3/library/functions.html -> 301 -> /3/builtins/functions.html, HTTP 200, 331022 bytes, sha256 d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7, pinned at pins/int-functions.html; quote 'Base 0 also disallows leading zeros: int(\"010\", 0) is not legal, while int(\"010\") and int(\"010\", 8) are.' (17 words) at bytes 159303-159682, lines 1339-1341; anchor id=\"int\" at byte 153202 (<dt ... id=\"int\"> starts 153172). Both r96 Python-docs rows re-open byte-identical, no drift: stdtypes 815447 bytes sha256 6bf2ce2ba49d30974485266d70aecd4c4eb89334eb73367f3f99bfa036c7e9a8 (pin 6bf2ce2b), sys 3.15 280632 bytes sha256 a7e005875e4152bcccaf44b9a834c123cc69bf7b66b3b8398aef91cffe77dd0e (pin a7e00587); none unreachable. Sweep for 'answers era B for': 15 hits with --include='*.py' --include='*.md' (all in r96 wave evidence that quotes-and-refutes, plus the r97 spec text), plus 2 more in the broader sweep - tools/limine-pin-battery-r96.py:1776 (LIVE, registry-listed, still asserts the false claim) and its frozen twin .ufo/waves/round-97/before/controls/do-nothing-battery-r96.py:1776 (both sha256 f06d90ae, which C1's do-nothing clause pins as byte-identical to the r96 landed bytes). The r97 instrument does NOT contain the string at all (grep exit 1): tools/limine-pin-battery-r97.py:1786-1790 replaces it with 'LIMIT (r96 CriticClaims F-4, corrected here in r97): an era reader that looks at X alone is NOT caught by this family'. Corpus/SKILL.md/PROVINCE.md/SCORECARD.md assert no false claim. Reject recorded: https://man.archlinux.org/man/python.1 -> 302 -> /man/python3.14.1.en, 200, 41788 bytes - rejected as generic (zero mentions of leading zeros, int(, radix or base 10; only an unrelated PYTHONHASHSEED 'decimal' hit); also functions.html#int is the same resource as the fetch (identical sha256). FINDING for the L1: the worktree S392 row cites id=\"int\" at 'byte 153028' and the quoted phrase at 'byte 157622', but those are CHARACTER offsets - read as bytes they land on unrelated markup, while the r96 rows S389/S391 use byte offsets that land exactly; recommend restating S392's anchors as bytes 153202 and 157767 (corpus/ is out of this seat's write scope). Second, the routed r96 docstring defect is closed only in the successor instrument, so the live tools/limine-pin-battery-r96.py:1776 still asserts the false era claim - L1 decision needed (successor-file correction vs in-place edit that would break C1's do-nothing byte-identity clause)."}
