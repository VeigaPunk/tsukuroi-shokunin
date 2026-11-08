# ScoutSources — round 99 wave w1 — source anchors for the own-work row

Seat: `ScoutSources`. Role: scout (leaf member; no subagent dispatch).
Scope: open the source this round's claims rest on and record byte-level anchors for the proposed
own-work row (CORPUS.md contract v1 rule 1; QUALITY 141). No files outside this seat dir and the
seat scratch were written; `corpus/SOURCES.md` was **not** edited.

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scratch (created, used, deleted before yield): `/fast/scratch/hyaku/tsukuroi-r99/ScoutSources`.
Network: two read-only `curl -sS` GETs; no network write, no credential material, nothing quoted
from the environment.

---

## 0. Preconditions — instrument integrity (PASS)

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-99/before/instruments.sha256
tools/limine-pin-battery-r99.py: OK
tools/make-r99-bends.py: OK
tools/check-registry-content-r99.py: OK
tools/check-limine-pins.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
tools/limine-pin-battery-r98.py: OK
tools/check-registry-content-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-battery-r98.py: OK
.ufo/waves/round-99/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-99/before/controls/do-nothing-checker-r98.py: OK
.ufo/waves/round-99/before/controls/bends/N09-y-era.py: OK
.ufo/waves/round-99/before/controls/bends/N11-x-era.py: OK
.ufo/waves/round-99/before/dev/make-fixtures.py: OK
.ufo/waves/round-95/before/controls/count-runs.py: OK
.ufo/plans/round-99.md: OK
exit=0        (17 files OK)
```

```
$ sha256sum tools/check-limine-pins.py tools/limine-pin-battery-r99.py
7d79ac296daacc462e7688f24801568ce10a0289d9fe4e3bafc3b293d6090d32  tools/check-limine-pins.py
c2e8c8fc87dccef0591323dfb2a589d16540150eaf65628abce6db6373619f99  tools/limine-pin-battery-r99.py
```

Both digests equal the manifest's. Every measurement below is against these bytes.
Disk guard was checked before the pass (`/fast/scratch/hyaku` 60% used, 328.4 G free; `/tmp` 48.1 G
free) — no ENOSPC.

**PASS — instrument integrity.**

---

## 1. Byte-level anchors — the gate `tools/check-limine-pins.py` (sha256 `7d79ac29…`, 30286 bytes)

### Commands

```
$ grep -abo '"limine_version"' tools/check-limine-pins.py
11230:"limine_version"
16931:"limine_version"
18866:"limine_version"

$ grep -abo '"visibility_era"' tools/check-limine-pins.py
11344:"visibility_era"
17037:"visibility_era"
19205:"visibility_era"
```

### The exact python expression used for every offset / line / quote below

```python
b = open('<path>','rb').read()
off = b.find(b'<needle>')          # byte-level search on the BYTES
line = b[:off].count(b'\n') + 1
ls = b.rfind(b'\n',0,off) + 1      # line-start byte
le = b.find(b'\n',off)
quote = b[ls:le].decode()
```

(Equivalently `grep -abo` on the same pinned bytes. A character index from a decoded `str.find` is
never used — QUALITY 141.)

### Table of every site

| # | site | byte offset | line | located quote (≤25 words) |
|---|---|---|---|---|
| a1 | MAIN return — `"limine_version"` | **16931** | 316 | `"limine_version": limine_version,` |
| a2 | MAIN return — `"visibility_era"` | **17037** | 318 | `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5",` |
| b1 | EARLY (CANNOT-EVALUATE) return — `"limine_version"` | **11230** | 200 | `"limine_version": limine_version,` |
| b2 | EARLY (CANNOT-EVALUATE) return — `"visibility_era"` | **11344** | 202 | `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5",` |
| — | (not an emission site) consumer of the echo | 18866 | 357 | `r = check(conf, esp, sb, tpm, **({} if ver is None else {"limine_version": ver}))` |
| — | (not an emission site) consumer of the era | 19205 | 361 | `and (want_era is None or r["visibility_era"] == want_era))` |

Site identification (read-only `sed -n`):

* MAIN return = lines 314-319, the `return {"schema": "tsukuroi-limine-pins-v3", "verdict": …, "rc": …, …}`
  dict inside `check()` after the pin loop; a1/a2 are its 3rd and 5th entries.
* EARLY return = lines 198-203, the `except OSError as e:` branch returning
  `{"verdict": "CANNOT-EVALUATE", "rc": 2, "pins": [], …, "error": "conf unreadable: …"}`; b1/b2 are
  its 5th and 7th entries.
* The third byte matches (18866 / 19205) sit in the gate's **own selftest expectations**, not in a
  return. They are listed so a reader does not mistake them for a third emission pair — the
  R98-ANCHOR-FIRST-SITE trap.

This reproduces the r98 lesson's S394 pair exactly (MAIN 16931/17037, early 11230/11344), and the
early/main assignment is the one S394 corrected.

**PASS — (a) and (b) located.**

---

## 2. Byte-level anchors — the battery `tools/limine-pin-battery-r99.py` (sha256 `c2e8c8fc…`, 117542 bytes)

### Commands

```
$ grep -abo 'def meta_ok' tools/limine-pin-battery-r99.py
99305:def meta_ok

$ grep -abo 'check_echo' tools/limine-pin-battery-r99.py
5313 / 6363 / 23670 / 79017 / 79895 / 81668 / 83175 / 84392 / 99435

$ grep -abo 'check_era' tools/limine-pin-battery-r99.py
5330 / 6380 / 23765 / 79041 / 80416 / 81692 / 83199 / 84416 / 99528
```

(the bare-token hits above are the *token* offsets inside their lines; the table records the
`c.check_… = True` / `if c.check_…` token offsets, all measured with `bytes.find` on the bytes.)

### (c) `meta_ok`'s two assertion lines

| site | byte offset | line | located quote |
|---|---|---|---|
| `meta_ok` definition | 99305 | 2179 | `def meta_ok(c, got):` |
| echo assertion | **99430** | 2181 | `if c.check_echo and not (got[8] == c.version and got[9] == "flag"):` |
| era assertion | **99523** | 2183 | `if c.check_era and got[10] != ("12.9.5+" if c.era_b() else "pre-12.9.5"):` |

The tuple indices these read are populated from the gate's JSON at battery lines 2172-2173:
`out.get("limine_version")`, `out.get("limine_version_source")`, `out.get("visibility_era")`.

### (d) `c.check_echo = True` / `c.check_era = True` sites — one per family

| roster family | family function (def line) | echo site byte/line | era site byte/line | located line text |
|---|---|---|---|---|
| `REFUSAL-VERSIONS-9DIGIT` (**X cap — r99**) | `fam_refusal_versions_9digit` (1764) | **79015 / 1775** | **79039 / 1776** | `    c.check_echo = True` / `    c.check_era = True` |
| `EXPLICIT-VERSION-ECHO` | `fam_explicit_version_echo` (1786) | 79893 / 1792 | — | `    c.check_echo = True` |
| `EXPLICIT-VERSION-ERA` | `fam_explicit_version_era` (1796) | — | 80414 / 1801 | `    c.check_era = True` |
| `REFUSAL-VERSIONS-9DIGIT-Y` (**Y cap — r99**) | `fam_refusal_versions_9digit_y` (1805) | **81666 / 1817** | **81690 / 1818** | `    c.check_echo = True` / `    c.check_era = True` |
| `REFUSAL-VERSIONS-9DIGIT-Z` | `fam_refusal_versions_9digit_z` (1831) | 83173 / 1840 | 83197 / 1841 | `    c.check_echo = True` / `    c.check_era = True` |
| `LEADING-ZERO-NORMALIZE` | `fam_leading_zero_normalize` (1845) | 84390 / 1857 | 84414 / 1858 | `    c.check_echo = True` / `    c.check_era = True` |

The two families this round's C1 changes are therefore:

* **X cap** — `fam_refusal_versions_9digit`, roster name `REFUSAL-VERSIONS-9DIGIT` (`FAMILIES` line
  2030), accepted member `REFUSAL_DIGIT9 = "9"*9 + ".9.9"` (line 1744) = `999999999.9.9`;
  echo at BYTE 79015 (line 1775), era at BYTE 79039 (line 1776).
* **Y cap** — `fam_refusal_versions_9digit_y`, roster name `REFUSAL-VERSIONS-9DIGIT-Y`
  (`FAMILIES` line 2034), members `Y_DIGIT9 = ("12.999999999.4", "0.999999999.0")` (line 1750);
  echo at BYTE 81666 (line 1817), era at BYTE 81690 (line 1818).

`FAMILY_ROSTER` is at BYTE 92103, line 2042, and has **105** entries (unchanged from r98) — the
claim's "roster unchanged at 105" reproduces from the bytes.

### The two new selftest lie kinds (the r98 scoreboard's structural gap)

| site | byte offset | line | located quote |
|---|---|---|---|
| `LIE_KINDS = (` | 108277 | 2369 | `LIE_KINDS = ("exit-code", "rc-field", "line", …` |
| new member `limine-version` | **108455** | 2370 | `"limine-version", "visibility-era")` |
| new member `visibility-era` | **108473** | 2370 | `"limine-version", "visibility-era")` |
| lie-application branch `limine-version` | 107815 | 2356 | `elif KIND == "limine-version":` |
| lie-application branch `visibility-era` | 107920 | 2359 | `elif KIND == "visibility-era":` |

Measured against the pinned r98 battery (`tools/limine-pin-battery-r98.py`, sha256 `8198bd84…`):
`LIE_KINDS` there is at BYTE 106583, line 2345, and holds **12** members, none of them
`limine-version`/`visibility-era`. The r99 battery holds **14**. This is the r98 scoreboard's
"lie-kind coverage" structural gap, closed by the two new members.

**PASS — (c) and (d) located.**

---

## 3. SOURCES row candidate (draft only — `corpus/SOURCES.md` NOT edited)

Written to **`sources-row-candidate.md`** in this seat dir.

**ID collision, stated plainly:** `S395` is **already taken** in the working tree —
`corpus/SOURCES.md` line 406 carries an `S395` row for this round's subject
(`git show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S395[[:space:]]*\|'` → **0**, so it is
new in the round's uncommitted tree). I re-measured every anchor that row claims and **all of them
reproduce byte-exactly**: `def meta_ok` 99305, echo assertion 99430, era assertion 99523, the five
echo sites 79015/79893/81666/83173/84390, the five era sites 79039/80414/81690/83197/84414, the
`LIE_KINDS` members at 108455 (line 2370), and the gate's 16931/17037. **The landed S395 is
grounded; this seat found no defect in it.**

Because contract v1 forbids reusing an id, a wider-scope row would have to take **S396** and open
`teaches` with `supersedes S395 — `; that is the L1's call, not this seat's. The candidate file
carries (i) the row as specified by this seat's brief, marked for id S396 if it is wanted, and
(ii) the full anchor-by-anchor groundings with a ≤25-word quote per anchor (3-12 words each).

The candidate's `teaches` sentence is grounded in two halves, both on the bytes above: the ten
`c.check_* = True` opt-in switches plus `meta_ok`'s two assertion lines (a family certifies a
reported field only if it reads that field on its own cases), and the 12→14 `LIE_KINDS` growth
(an assertion removal is invisible to the selftest without a lie kind per field).

---

## 4. S392 re-open — `https://docs.python.org/3/library/functions.html#int`

```
$ curl -sS -w '%{http_code}\n' -o s392-int.html 'https://docs.python.org/3/library/functions.html#int'
301                       <- the URL now 301-redirects

$ curl -sSL -w 'http_code=%{http_code} size=%{size_download} url=%{url_effective}\n' \
      -o s392-int.html 'https://docs.python.org/3/library/functions.html#int'
http_code=200 size=331022 url=https://docs.python.org/3/builtins/functions.html

$ wc -c s392-int.html
331022 s392-int.html

$ sha256sum s392-int.html
d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7  s392-int.html
```

Three pinned offsets re-measured on the fetched bytes (`bytes.find`):

```
have leading zeros, be surrounded by whitespace -> byte 157767 line 1330
id="int"                                  -> byte 153202 line 1302
disallows leading zeros                   -> byte 159315 line 1340
```

**VERDICT: identical — no drift.** 331022 bytes, sha256 `d92580dd…` — the r98 pin's digest and
length exactly; all three of the row's offsets (157767 / 153202 / 159315) reproduce. The URL shape
changed (`/3/library/functions.html` → `/3/builtins/functions.html` by 301) but the *content bytes*
are unchanged, so the row's anchor stays valid; the `source` cell may keep its original URL.

**PASS — S392 re-opened, identical.**

---

## 5. Rejection candidate — `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md`

```
$ curl -sS -w '%{http_code}\n' -o limine-config.md \
      'https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md'
200
$ wc -c limine-config.md
27609 limine-config.md
$ sha256sum limine-config.md
f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763  limine-config.md

$ grep -c 'limine_version' limine-config.md   -> 0
$ grep -c 'visibility_era' limine-config.md   -> 0
$ grep -c 'echo'          limine-config.md    -> 0
$ grep -c 'version'       limine-config.md    -> 0
```

Sanity that the file is not empty (so the zeros are real absences, not a failed fetch): 495 lines;
`timeout` → 7, `protocol` → 17; case-insensitive `version`/`echo` → 0.

**VERDICT: reject.** HTTP 200, 27609 bytes, sha256 `f44f3a19…` (byte-identical to the r98
measurement). The page documents Limine's *config keys* and their values; it mentions none of the
gate's JSON report fields, so it grounds none of this round's propositions. It is kept as evidence
of taste (contract v1: a rejection is kept), not as a mined row.

**PASS — rejection candidate measured and rejected.**

---

## 6. Receipts (all under this seat dir)

| receipt | content |
|---|---|
| `receipts/01-manifest-verify.txt` | `sha256sum -c` of the frozen instrument manifest (17 OK, exit 0) |
| `receipts/02-gate-offsets.txt` | raw `grep -abo` output for the gate's two field tokens + gate sha256 |
| `receipts/03-byte-anchors-measured.txt` | the site table with offsets, lines, quotes, the exact python expression, and the site identification |
| `receipts/04-s392-reopen-and-config-reject.txt` | S392 re-open (HTTP/bytes/sha256/3 offsets) and the CONFIG.md rejection measurement |
| `receipts/05-python-bytes-find.txt` | raw output of the byte-level measurement run (token byte, line-start byte, line, quote) |
| `receipts/06-config-md-reject-counts.txt` | CONFIG.md grep counts + sanity greps + head |
| `sources-row-candidate.md` | the S395/S396 candidate row and its anchor groundings |
| `report.md` | this file |

Scratch root `/fast/scratch/hyaku/tsukuroi-r99/ScoutSources` was deleted before yield; the two
fetched external bodies were **not** copied into the lane (the receipts carry their lengths and
digests, and both are re-fetchable read-only).

## 7. PASS/FAIL per expected line

| expected line | verdict | evidence |
|---|---|---|
| gate MAIN return `"limine_version"` / `"visibility_era"` emission lines located | **PASS** | 16931 (line 316) / 17037 (line 318) |
| gate EARLY (CANNOT-EVALUATE) return copies located | **PASS** | 11230 (line 200) / 11344 (line 202) |
| `meta_ok`'s two assertion lines located in the r99 battery | **PASS** | 99430 (line 2181) / 99523 (line 2183); `def meta_ok` 99305 (line 2179) |
| `c.check_echo = True` / `c.check_era = True` sites located, one per family | **PASS** | ten sites over six families; X cap 79015/79039, Y cap 81666/81690 |
| every site recorded with byte offset, line and ≤25-word quote, with the exact commands | **PASS** | §1-§2 tables; receipts 03 and 05 |
| S395 candidate row drafted, `corpus/SOURCES.md` not edited | **PASS** | `sources-row-candidate.md`; `S395` already taken in the working tree — see §3 |
| S392 re-opened, identical or drifted | **PASS** | identical: 331022 bytes, sha256 `d92580dd…`, offsets 157767/153202/159315 |
| CONFIG.md rejection candidate measured and adjudicated | **PASS** | HTTP 200, 27609 bytes, sha256 `f44f3a19…`, counts 0/0/0 → reject |

## 8. Findings and unknowns

1. **`S395` is already taken in the working tree** (`corpus/SOURCES.md:406`), landed by the round's
   own scribe seat in the uncommitted tree. Every anchor it claims reproduces byte-exactly on the
   pinned bytes, so it is grounded. A wider-scope row must take **S396** with
   `supersedes S395 — `, per contract v1 rule 2. **Decision for the L1.**
2. The landed S395's anchor names the two new `LIE_KINDS` members as "BYTE 108455 (line 2370)" —
   one offset for two members. `"limine-version"` is at 108455 and `"visibility-era"` at **108473**
   (both line 2370). A one-offset cell for a two-member claim is imprecise but not false; the
   correction is append-only and belongs in a superseding row, not an in-place edit.
3. The gate's `visibility_era` token appears three times (11344 / 17037 / 19205) and `limine_version`
   three times (11230 / 16931 / 18866). Only the first two of each are emission sites; 18866 and
   19205 are the gate's own selftest expectations. Recorded so no reader anchors to them.
4. **Unknown / not measured here:** this seat measured *source* anchors only. It did not re-run the
   gate, the battery, the bends, the lie wrappers, or the checker, so it neither confirms nor
   contradicts the L1's run readings (`105/105 met`, N09 `104/105`, N11 `103/105`, wrappers
   `93/105` and `95/105` unmet, r99 selftest `PASS 17/17`, M07 `FAIL 16/17`). Those are other
   seats' receipts.
5. **No network write, no credential material, nothing quoted from the environment.** The only
   external fetches are two public documentation pages, fetched read-only with `curl -sS`/`-sSL`
   into the seat scratch, which has been deleted.

```json
{"seat":"ScoutSources","verdict":"met","notes":"Byte-level anchors located on pinned bytes: gate MAIN return limine_version 16931 (line 316) / visibility_era 17037 (line 318); EARLY CANNOT-EVALUATE copies 11230 (line 200) / 11344 (line 202); r99 battery meta_ok def 99305 (line 2179), echo assertion 99430 (line 2181), era assertion 99523 (line 2183); ten c.check_*=True sites over six families (X cap 79015/79039, Y cap 81666/81690); LIE_KINDS 108277 (line 2369) with new members 108455/108473 (line 2370). S392 re-opened identical (331022 bytes, sha256 d92580dd..., offsets 157767/153202/159315). CONFIG.md reject (HTTP 200, 27609 bytes, sha256 f44f3a19..., grep -c 0/0/0). FINDING: S395 id already taken in the working tree corpus/SOURCES.md:406 and every anchor it claims reproduces byte-exactly; a wider-scope row must take S396. corpus/SOURCES.md not edited."}
```
