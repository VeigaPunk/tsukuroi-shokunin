# ScoutSources — round 98, wave w1

Seat: `ScoutSources` (scout). Scope: re-open the two sources the round cites (S392 external,
S393 own-work), record one reject candidate with its reason, and sweep for the stale statements
the round corrects.

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Scratch (deleted at yield):
`/fast/scratch/hyaku/tsukuroi-r98/ScoutSources`.

No file outside this seat dir was written. No git/jj mutation was run. `tools/`,
`corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `.ufo/plans/`, `.ufo/waves/round-98/before/`
and `claims.json` were read only.

## 0. Instrument manifest verified before any measurement

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && sha256sum -c .ufo/waves/round-98/before/instruments.sha256
tools/check-limine-pins.py: OK
tools/limine-pin-battery-r98.py: OK
tools/make-r98-bends.py: OK
tools/check-registry-content-r98.py: OK
tools/check-registry-coverage.py: OK
tools/check-r96-calibration.py: OK
.ufo/plans/round-98.md: OK
.ufo/waves/round-98/before/plan-frozen.md: OK
.ufo/waves/round-98/claims.json: OK
.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py: OK
.ufo/waves/round-98/before/controls/do-nothing-gate.py: OK
.ufo/waves/round-98/before/controls/do-nothing-checker-r97.py: OK
.ufo/waves/round-98/before/controls/bends/N07-era-field-lie.py: OK
.ufo/waves/round-98/before/controls/bends/N08-echo-norm.py: OK
.ufo/waves/round-98/before/registry-baseline-r98.json: OK
.ufo/waves/round-98/before/fixtures/build-doctored-fixture-r98.sh: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D1: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2: OK
.ufo/waves/round-98/before/fixtures/doctored-r98-D2lie: OK
.ufo/waves/round-98/before/dev/c1-gate-runs3.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-bend-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N07-runs1.json: OK
.ufo/waves/round-98/before/dev/c1-dn-N08-runs1.json: OK
.ufo/waves/round-98/before/dev/c2-selftest-r98.txt: OK
.ufo/waves/round-98/before/dev/c2-selftest-r97.txt: OK
.ufo/waves/round-98/before/dev/c2-doctored-summary.txt: OK
```

**PASS — 28/28 OK, 0 FAILED.** Every measurement below is taken against these pinned bytes.

Tooling: no install was needed and none was made. Used the host's existing
`curl 8.23.0 (x86_64-pc-linux-gnu) libcurl/8.23.0`, `grep (pi-uu-grep) 0.2.0`,
`sha256sum (GNU coreutils) 0.8.0`, `python3 3.14.8`. No pacman transaction (paused host-wide),
no `sudo`, no PATH-directory write.

## 1. S392 re-open — `https://docs.python.org/3/library/functions.html#int` (external)

Commands and raw output: `receipts/02-s392-refetch.txt`, `receipts/03-s392-byte-offsets.txt`.

```
$ curl -sSL -o s392.html -w 'HTTP %{http_code} bytes %{size_download}\n' https://docs.python.org/3/library/functions.html#int
HTTP 200 bytes 331022
$ sha256sum s392.html
d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7  s392.html
$ wc -c s392.html
331022 s392.html
```

Redirect chain (the cited URL 301-redirects to the builtins page):

```
$ curl -sS -o /dev/null -w 'no-follow http=%{http_code} redirect=%{redirect_url}\n' https://docs.python.org/3/library/functions.html
no-follow http=301 redirect=https://docs.python.org/3/builtins/functions.html
$ curl -sSL -o s392b.html -w 'final_url=%{url_effective} http=%{http_code} redirects=%{num_redirects} bytes=%{size_download}\n' https://docs.python.org/3/library/functions.html#int
final_url=https://docs.python.org/3/builtins/functions.html http=200 redirects=1 bytes=331022
```

**Comparison with the r97 pin** (`corpus/SOURCES.md` S392 row: sha256
`d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7`, 331022 bytes):

| | sha256 | bytes | verdict |
|---|---|---|---|
| r97 pin (S392 row) | `d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7` | 331022 | — |
| live fetch 2026-11-08 | `d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7` | 331022 | **BYTE-IDENTICAL (no drift)** |

Also byte-identical to the three committed r97 snapshots of the same page:
`.ufo/waves/round-97/w1/ScoutSources/pins/int-functions.html`,
`.ufo/waves/round-97/w1/ScribeLesson/pins/functions.html`,
`.ufo/waves/round-97/after/gate/functions.html` (all `d92580dd…`, 331022 bytes; `cmp` clean).

**Quote offsets re-measured at BYTE level on the pinned bytes** (`grep -abo`, QUALITY 141):

```
$ grep -abo 'have leading zeros, be surrounded by whitespace' s392.html
157767:have leading zeros, be surrounded by whitespace
$ grep -abo 'id="int"' s392.html
153202:id="int"
$ grep -abo 'disallows leading zeros' s392.html
159315:disallows leading zeros
```

Each anchor occurs exactly once in the file (1/1/1).

| anchor | row states | measured | verdict |
|---|---|---|---|
| `id="int"` | BYTE 153202 | BYTE 153202 | **PASS** |
| quoted phrase ("have leading zeros, be surrounded by whitespace,") | BYTE 157767 | BYTE 157767 | **PASS** |
| base-0 contrast ("disallows leading zeros") | BYTE 159315 | BYTE 159315 | **PASS** |

Located quote with its context (tags stripped, whitespace collapsed; the quote itself is 7 words,
inside the row's ≤25-word bound):

> "…Optionally, the string can be preceded by + or - (with no space in between), **have leading
> zeros, be surrounded by whitespace,** and have single underscores interspersed between digits…"

> "…Base **0 also disallows leading zeros:** `int('010', 0)` is not legal, while …"

The quote supports the row's `teaches` cell ("an explicit base accepts leading zeros, base 0 does
not") on the pinned bytes. One wording note, measured: the row's `teaches` cell phrases the source
as "an explicit base accepts a radix string with leading zeros", while the page's own wording is
"a base-n integer string" — `b'radix string'` occurs 0 times and `b'base-n integer string'` occurs
once in the pinned bytes. The paraphrase is faithful in substance (the `int` class docs' base-n
string form admits leading zeros; base 0 does not) but the phrase "radix string" is the row's
wording, not the page's.

**PASS — S392 re-opens byte-identical; all three row offsets re-measure exactly.**

## 2. S393 re-open — `tools/check-limine-pins.py` (own-work)

Commands and raw output: `receipts/04-s393-gate-reopen.txt`, `receipts/05-s393-gate-byte-offsets.txt`.

### 2a. The gate run on a leading-zero spelling and a Z spelling

Fixture (scratch-local only): a `limine.conf` with one entry, one `protocol: efi` line and one
`path: boot():/boot.efi#<blake2b>` pin matching a scratch-local `esp/boot.efi`; the gate is invoked
as `python3 -I <gate> --conf <scratch>/limine.conf --esp <scratch>/esp --limine-version <SPELLING>`.

```
[
  { "flag": "12.09.4",                       "rc": 0, "limine_version": "12.09.4",                       "limine_version_source": "flag", "visibility_era": "pre-12.9.5", "verdict": "HEALTHY", "findings": [] },
  { "flag": "000000012.9.4",                 "rc": 0, "limine_version": "000000012.9.4",                 "limine_version_source": "flag", "visibility_era": "pre-12.9.5", "verdict": "HEALTHY", "findings": [] },
  { "flag": "12.000000009.000000005",        "rc": 0, "limine_version": "12.000000009.000000005",        "limine_version_source": "flag", "visibility_era": "12.9.5+",    "verdict": "HEALTHY", "findings": [] },
  { "flag": "12.9.999999999",                "rc": 0, "limine_version": "12.9.999999999",                "limine_version_source": "flag", "visibility_era": "12.9.5+",    "verdict": "HEALTHY", "findings": [] },
  { "flag": "0.9.999999999",                 "rc": 0, "limine_version": "0.9.999999999",                 "limine_version_source": "flag", "visibility_era": "pre-12.9.5", "verdict": "HEALTHY", "findings": [] },
  { "flag": "12.9.4",                        "rc": 0, "limine_version": "12.9.4",                        "limine_version_source": "flag", "visibility_era": "pre-12.9.5", "verdict": "HEALTHY", "findings": [] },
  { "flag": "12.9.5",                        "rc": 0, "limine_version": "12.9.5",                        "limine_version_source": "flag", "visibility_era": "12.9.5+",    "verdict": "HEALTHY", "findings": [] },
  { "flag": "000000000.000000000.000000000", "rc": 0, "limine_version": "000000000.000000000.000000000", "limine_version_source": "flag", "visibility_era": "pre-12.9.5", "verdict": "HEALTHY", "findings": [] },
  { "flag": "12.9.6",                        "rc": 0, "limine_version": "12.9.6",                        "limine_version_source": "flag", "visibility_era": "12.9.5+",    "verdict": "HEALTHY", "findings": [] }
]
```

Against the S393 row's `teaches` cell — *"An explicit `--limine-version` is echoed in
`limine_version` exactly as the flag spelled it, with source `flag`, and `visibility_era` is
`pre-12.9.5` below 12.9.5 and `12.9.5+` at or above it"*:

| row claim | measured | verdict |
|---|---|---|
| echo = the flag spelling verbatim | every spelling above echoes verbatim (`12.09.4` → `"12.09.4"`, `000000012.9.4` → `"000000012.9.4"`, `12.000000009.000000005` → verbatim, `12.9.999999999` → verbatim, `0.9.999999999` → verbatim, the all-zero member → verbatim) | **PASS** |
| `limine_version_source` = `flag` | `"flag"` in all nine runs (no run used `auto`, so no `probe` source was in play) | **PASS** |
| `visibility_era` = `pre-12.9.5` below 12.9.5, `12.9.5+` at or above | `(12,9,4)`→`pre-12.9.5`; `(12,9,5)`→`12.9.5+`; `(12,9,999999999)`→`12.9.5+`; `(0,9,999999999)`→`pre-12.9.5`; `(0,0,0)`→`pre-12.9.5`; `(12,9,6)`→`12.9.5+` — the label follows the NUMERIC tuple, not the text | **PASS** |

The two spellings the item names are covered: leading-zero `12.09.4` / `000000012.9.4` (era A,
echoed verbatim) and Z `12.9.999999999` / `0.9.999999999` (era B / era A, echoed verbatim).

**PASS — S393's `teaches` cell re-derives from the pinned gate bytes.**

### 2b. Byte offsets re-measured on the pinned gate bytes

```
$ grep -abo '"limine_version": limine_version' tools/check-limine-pins.py
11230:"limine_version": limine_version
16931:"limine_version": limine_version
$ grep -abo '"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"' tools/check-limine-pins.py
11344:"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"
17037:"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"
$ grep -abo 'resolved `limine_version` and `limine_version_source: "probe"`' tools/check-limine-pins.py
4425:resolved `limine_version` and `limine_version_source: "probe"`
```

| anchor | row states | measured | verdict |
|---|---|---|---|
| `"limine_version": limine_version` | BYTE 11230 | BYTE 11230 (first of two occurrences) | **PASS** |
| `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"` | BYTE 11344 | BYTE 11344 (first of two occurrences) | **PASS** |
| docstring ``resolved `limine_version` and `limine_version_source: "probe"` `` | BYTE 4425 | BYTE 4425 | **PASS** |

**Finding (label defect, does not affect the claim).** The S393 row's anchor cell reads
*"emission lines at BYTE 11230 … and BYTE 11344 …, **main return after parsing**"*. Line numbers
derived by counting newlines in the same pinned bytes:

* 11230 → **line 200**, 11344 → **line 202** — the **early (CANNOT-EVALUATE) return** of `check()`,
  the branch that fires when the conf file cannot be read.
* 16931 → **line 316**, 17037 → **line 318** — the **main return** of `check()`, carrying the same
  two field names.

So the two offsets the row cites are the *first* occurrences of those two field names, which sit
in the error branch, not in the "main return after parsing" the row names. The pointer does not
describe the bytes at 11230/11344. The `teaches` cell is unaffected: `era_b` is computed once
(`version >= VISIBILITY_ERA_SPLIT`, line 193) before either return, and both returns emit the same
`limine_version` / `limine_version_source` / `visibility_era` values — which the nine gate runs in
§2a confirm directly. This is the same class as the routed R97-D1/D2 provenance-label defects: a
number is right, its pointer is not. The round-98 report should cite 16931 / 17037 for the main
return, or drop the "main return after parsing" phrase.

## 3. Reject candidate — `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md`

Commands and raw output: `receipts/06-reject-candidate-config-md.txt`.

```
$ curl -sSL -o limine-config-v12.9.6.md -w 'final_url=%{url_effective} http=%{http_code} bytes=%{size_download}\n' https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md
final_url=https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md http=200 bytes=27609
$ sha256sum limine-config-v12.9.6.md
f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763  limine-config-v12.9.6.md
$ wc -c limine-config-v12.9.6.md
27609 limine-config-v12.9.6.md
```

**HTTP status 200; 27,609 bytes; sha256 `f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763`.**

Token counts over those 27,609 bytes (case-insensitive, `grep -o -F`):

```
limine_version         0
limine_version_source  0
visibility_era         0
echo                   0
int(                   0
leading zero           0
version                0
JSON                   0
```

**REJECTED.** Reason, in the two questions the round asks:

1. **Does it state the gate's JSON fields?** No. `limine_version`, `limine_version_source` and
   `visibility_era` occur **0 times each**. The page is upstream's *limine.conf* reference —
   headings `Location of the config file`, `Structure of the config file`, `Options`, `Paths`,
   `Macros`, `Built-in macros` — and says nothing about any JSON report contract. It cannot
   ground S393's `teaches` cell nor any r98 claim about the gate's emitted fields.
2. **Does it state echo semantics?** No. The token `echo` occurs **0 times**; there is no sentence
   anywhere in the page saying a version string is echoed verbatim or normalised. S393's echo
   claim is therefore grounded *only* in the own-work source (the gate bytes) — which is exactly
   where the row places it (kind `own-work`, tier A).

Two further points that make the reject airtight for this round: the token `version` occurs **0
times** in the whole page, so the page cannot ground S392's `int()` leading-zero statement either,
and it never mentions the 12.9.5 era split that C1's `visibility_era` assertion turns on.
Admitting it would support neither C1 nor C2.

Corroborating rejects, measured the same way in the same round:

```
https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/USAGE.md   http=200 10710 bytes  sha256 db32c4e05427322fc5c4be70773a3dacbc2e36ff9a94fdfc862172d993a90329
    limine_version/visibility_era/limine_version_source/echo/int(/leading zero/version = 0/0/0/0/0/0/0
https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/README.md  http=200  2947 bytes  sha256 318ff36ad960adf3fc3d01eb250e1d30753155dd8b5ced92332db5b2f607b0ce
    limine_version/visibility_era/limine_version_source/echo/int(/leading zero = 0/0/0/0/0/0 ; `version` = 2
https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/limine.1    http=404   14 bytes  sha256 d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed
```

(The README's two `version` hits are build/versioning prose, not a version-echo contract.)

## 4. Sweep for the stale statements the round corrects

Raw grep output: `receipts/01-sweep-000000012-9-4.txt` (every hit, file:line).
Classification of every hit: `receipts/07-sweep-classified.txt`.

```
$ grep -rn "000000012.9.4" /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --include='*.py' --include='*.md'
```

**60 hits.** Every one, with file:line (paths relative to the lane root):

| # | file:line | tag |
|---|---|---|
| 1 | `.ufo/plans/round-97.md:38` | neutral |
| 2 | `.ufo/plans/round-98.md:44` | REPORTS-CORRECTED |
| 3 | `.ufo/waves/round-97/after/report-draft.md:12` | neutral |
| 4 | `.ufo/waves/round-97/before/plan-amendments-r97.md:87` | REPORTS-CORRECTED |
| 5 | `.ufo/waves/round-97/before/plan-amendments-r97.md:88` | REPORTS-CORRECTED |
| 6 | `.ufo/waves/round-97/before/plan-frozen.md:38` | neutral |
| 7 | `.ufo/waves/round-97/make-spec.py:50` | neutral |
| 8 | `.ufo/waves/round-97/make-spec.py:159` | neutral |
| 9 | `.ufo/waves/round-97/w1/CriticClaims/report.md:32` | REPORTS-CORRECTED |
| 10 | `.ufo/waves/round-97/w1/ExecBattery.md:69` | neutral |
| 11 | `.ufo/waves/round-97/w1/ExecBattery.md:109` | neutral |
| 12 | `.ufo/waves/round-97/w1/ExecBattery/report.md:69` | neutral |
| 13 | `.ufo/waves/round-97/w1/ExecBattery/report.md:109` | neutral |
| 14 | `.ufo/waves/round-97/w1/ReviewBattery.md:75` | neutral |
| 15 | `.ufo/waves/round-97/w1/ReviewBattery.md:112` | neutral |
| 16 | `.ufo/waves/round-97/w1/ReviewBattery/report.md:75` | neutral |
| 17 | `.ufo/waves/round-97/w1/ReviewBattery/report.md:112` | neutral |
| 18 | `.ufo/waves/round-97/w1/ScoutSources.md:105` | neutral |
| 19 | `.ufo/waves/round-97/w1/ScoutSources/report.md:105` | neutral |
| 20 | `.ufo/waves/round-97/w1/ScribeKnowledge.md:24` | neutral |
| 21 | `.ufo/waves/round-97/w1/ScribeKnowledge.md:28` | neutral |
| 22 | `.ufo/waves/round-97/w1/ScribeKnowledge.md:80` | REPORTS-CORRECTED |
| 23 | `.ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md:120` | neutral |
| 24 | `.ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md:124` | neutral |
| 25 | `.ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md:137` | neutral |
| 26 | `.ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md:141` | neutral |
| 27 | `.ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md:166` | neutral |
| 28 | `.ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md:252` | neutral |
| 29 | `.ufo/waves/round-97/w1/ScribeKnowledge/report.md:101` | neutral |
| 30 | `.ufo/waves/round-97/w1/ScribeKnowledge/report.md:118` | neutral |
| 31 | `.ufo/waves/round-97/w1/ScribeKnowledge/report.md:208` | neutral |
| 32 | `.ufo/waves/round-97/w1/ScribeKnowledge/report.md:352` | neutral |
| 33 | `.ufo/waves/round-97/w1/ScribeKnowledge/report.md:426` | REPORTS-CORRECTED |
| 34 | `.ufo/waves/round-97/w1/ScribeLesson/round-97.md:174` | REPORTS-CORRECTED |
| 35 | `.ufo/waves/round-97/w1/ScribeLesson/round-97.md:175` | neutral |
| 36 | `.ufo/waves/round-97/w1/ScribeLesson/round-97.md:201` | neutral |
| 37 | `.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py:57` | neutral |
| 38 | `.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py:1799` | neutral |
| 39 | `.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py:1817` | **ASSERT-THE-DEFECT** |
| 40 | `.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py:1820` | **ASSERT-THE-DEFECT** |
| 41 | `.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py:2445` | neutral |
| 42 | `.ufo/waves/round-98/before/plan-frozen.md:44` | REPORTS-CORRECTED |
| 43 | `.ufo/waves/round-98/make-spec.py:134` | neutral (this sweep's own spec text) |
| 44 | `SCORECARD.md:7969` | neutral |
| 45 | `corpus/README.md:1195` | neutral |
| 46 | `corpus/knowledge/limine-bound-9digit-z-r97.md:38` | neutral |
| 47 | `corpus/knowledge/limine-metadata-assertions-r98.md:35` | neutral |
| 48 | `corpus/lessons/round-97-verifier-spotcheck.md:53` | neutral |
| 49 | `corpus/lessons/round-97-verifier-spotcheck.md:201` | REPORTS-CORRECTED |
| 50 | `corpus/lessons/round-97.md:51` | REPORTS-CORRECTED |
| 51 | `tools/limine-pin-battery-r97.py:57` | neutral |
| 52 | `tools/limine-pin-battery-r97.py:1799` | neutral |
| 53 | `tools/limine-pin-battery-r97.py:1817` | **ASSERT-THE-DEFECT** |
| 54 | `tools/limine-pin-battery-r97.py:1820` | **ASSERT-THE-DEFECT** |
| 55 | `tools/limine-pin-battery-r97.py:2445` | neutral |
| 56 | `tools/limine-pin-battery-r98.py:57` | neutral |
| 57 | `tools/limine-pin-battery-r98.py:1809` | neutral |
| 58 | `tools/limine-pin-battery-r98.py:1831` | neutral |
| 59 | `tools/limine-pin-battery-r98.py:1836` | REPORTS-CORRECTED |
| 60 | `tools/limine-pin-battery-r98.py:2465` | neutral |

Tag semantics: **ASSERT-THE-DEFECT** = the surrounding text still states that a raw-TEXT comparison
against `12.9.5` orders `000000012.9.4` as era B; **REPORTS-CORRECTED** = the hit sits inside a
sentence that reports the defect together with the measurement that refutes it; **neutral** = the
hit only lists the spelling as a member, or states its correct era, or is this sweep's own spec.

### Does any surviving sentence still claim the text comparer orders `000000012.9.4` as era B?

**Yes — four hit lines, in two files, and both files are the r97 instrument bytes, not a corpus
record:**

* `tools/limine-pin-battery-r97.py:1817` and `:1820` — the **superseded r97 instrument**. The
  round-98 plan states the frozen bytes are not edited this round ("frozen bytes are not edited
  (void clause); the sentence is corrected in the r98 successor with its own manifest (A6)",
  `.ufo/plans/round-98.md:44-45`, `corpus/README.md:1210-1213`). The **successor
  `tools/limine-pin-battery-r98.py:1831-1836` carries the corrected sentence** (the discriminator is
  `12.000000009.000000005`; the text comparer orders it era A while `int()` reads 12.9.5), and it
  adds the r98 echo/era assertion. This is the intended shape, not a missed correction.
* `.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py:1817` and `:1820` — the **frozen
  do-nothing control**, byte-identical to the r97 landed battery *by construction*:
  `sha256 tools/limine-pin-battery-r97.py` = `e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8`
  = `sha256 .ufo/waves/round-98/before/controls/do-nothing-battery-r97.py` (identical, measured).
  The control *must* carry the r97 bytes, so it necessarily carries the r97 docstring sentence;
  editing it would destroy the blindness control.

**Every other hit is either neutral (a member list, or the member's correct era) or a sentence that
reports the defect together with the measurement that refutes it.** No `corpus/` record, plan,
lesson, scorecard or knowledge entry still asserts the defect as true. The refuting measurement is
re-derivable in one line: a text comparison against `"12.9.5"` orders `12.09.4`, `000000012.9.4` and
`000000000.000000000.000000000` as era A and orders `12.000000009.000000005` as era A as well,
while `int()` normalizes it to `(12, 9, 5)` = era B — so `12.000000009.000000005` is the single
discriminating member and the r98 docstring's sentence is the correct one.

**PASS — the sweep finds no stale *corpus* statement of the R97-D3/A6 defect; the four surviving
assertions are the frozen r97 instrument bytes and their byte-identical do-nothing control, and the
r98 successor corrects the sentence.**

## Incidental observation (outside this seat's scope; not claimed, not fixed)

While verifying that a measurement would be citable I ran the lane's own coverage gate read-only,
at the pre-round base the plan names and at the current lane tip:

```
$ python3 tools/check-registry-coverage.py --revision b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a --branch master
{"branch":"master","branch_tip":"1cfeb5d5089097fdffaf761ad0e2b8dfa75a2793",
 "counts":{"findings":0,"missing":0,"registered":157,"rows_total":157,"tools_total":157},
 "findings":[],"revision":"b3be3f90c2e32400d4e2692b2656ec9a1ba14a8a","status":"PASS"}   exit=0

$ python3 tools/check-registry-coverage.py --revision $(git rev-parse HEAD) --branch master
{"branch":"master","branch_tip":"1cfeb5d5089097fdffaf761ad0e2b8dfa75a2793",
 "counts":{"findings":3,"missing":3,"registered":157,"rows_total":157,"tools_total":160},
 "findings":[{"id":"REGISTRY-ROW-MISSING","site":"tools/check-registry-content-r98.py"},
             {"id":"REGISTRY-ROW-MISSING","site":"tools/limine-pin-battery-r98.py"},
             {"id":"REGISTRY-ROW-MISSING","site":"tools/make-r98-bends.py"}],
 "revision":"1cfeb5d5089097fdffaf761ad0e2b8dfa75a2793","status":"FAIL"}   exit_code=1
```

At the pre-round base `b3be3f90` the coverage gate reads `PASS 157/157 findings 0` — the plan's
"no axis is harmed" leg holds there. At the **current** lane tip `1cfeb5d5` it reads `FAIL`: the
three r98 tools are already committed (`git ls-tree HEAD tools/` lists
`check-registry-content-r98.py`, `limine-pin-battery-r98.py`, `make-r98-bends.py`) but the
operative registry table (the round-71 heading, `SKILL.md:5777`) has no **committed** row for
them, so `tools_total 160` vs `registered 157` and three `REGISTRY-ROW-MISSING` findings.

Update, measured a second time after a concurrent (not mine) edit: the three rows now exist in
the **working tree** at `SKILL.md:5944` (`limine-pin-battery-r98`), `:5945` (`make-r98-bends`) and
`:5946` (`check-registry-content-r98`) — `git diff --stat SKILL.md` → `3 insertions(+)` — but they
are uncommitted, and the coverage gate reads a committed revision, so it still reports the three
missing rows. The finding therefore clears when those rows are committed; it is not a defect in the
round's instruments. Reported for the L1's settle only; no file was edited here.

## Receipts (all under this seat dir)

| receipt | content |
|---|---|
| `receipts/01-sweep-000000012-9-4.txt` | raw grep output, all 60 hits |
| `receipts/02-s392-refetch.txt` | S392 HTTP status, byte count, sha256, redirect chain, r97-pin comparison |
| `receipts/03-s392-byte-offsets.txt` | S392 `grep -abo` offsets + located quote with context |
| `receipts/04-s393-gate-reopen.txt` | the nine gate runs on the LZ and Z spellings, read against the row's `teaches` |
| `receipts/05-s393-gate-byte-offsets.txt` | gate `grep -abo` offsets + what each offset is (line numbers from the same bytes) |
| `receipts/06-reject-candidate-config-md.txt` | limine CONFIG.md: status, bytes, sha256, token counts, rejection reason, corroborating rejects |
| `receipts/07-sweep-classified.txt` | every sweep hit classified, and where each surviving assertion lives |

## PASS/FAIL per expected line

| expected line | verdict |
|---|---|
| S392: HTTP status, byte count, sha256 recorded | **PASS** — 200 / 331022 / `d92580dd…` |
| S392: compare with the r97 pin; byte-identical / drifted / unreachable | **PASS** — byte-identical |
| S392: re-measure the quote offsets 157767 / 153202 / 159315 with `grep -abo` | **PASS** — all three match exactly |
| S393: re-run the gate on a leading-zero and a Z spelling | **PASS** — nine runs, leading-zero and Z spellings included |
| S393: echoed `limine_version`, `limine_version_source`, `visibility_era` match the row's `teaches` | **PASS** — verbatim echo, source `flag`, era from the numeric tuple |
| S393: re-measure the emission offsets 11230 and 11344 | **PASS** — both match (see the "main return" pointer finding) |
| S393: re-measure the docstring phrase at 4425 | **PASS** — matches |
| Reject candidate: fetch a plausible page, record why it is rejected; status, bytes, sha256 | **PASS** — limine CONFIG.md v12.9.6: 200 / 27609 / `f44f3a19…`; rejected: 0 occurrences of the gate's JSON fields and of `echo`, 0 of `version` |
| Sweep: every hit with file:line; state whether any surviving sentence still claims the era-B text-comparer defect | **PASS** — 60 hits listed; 4 hit lines still assert it, all in the frozen r97 instrument bytes and their byte-identical do-nothing control; no corpus/plan/lesson/scorecard/knowledge sentence still asserts it |
| No credential material recorded | **PASS** — only public doc/raw-GitHub URLs, digests and counts |

{"seat":"ScoutSources","verdict":"findings","notes":"S392 re-opens byte-identical (HTTP 200, 331022 bytes, sha256 d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7) and all three row offsets re-measure exactly (grep -abo: 157767 / 153202 / 159315). S393 re-derives from the pinned gate bytes: nine runs on the LZ and Z spellings echo the flag verbatim with source 'flag' and report visibility_era from the numeric tuple; offsets 11230 / 11344 / 4425 all match. FINDING (label defect): the S393 anchor cell calls 11230/11344 'main return after parsing', but those bytes are the CANNOT-EVALUATE early return (lines 200/202); the main return's same field text is at 16931/17037 (lines 316/318) - the teaches cell is unaffected because era_b is computed before either return. REJECT: limine CONFIG.md v12.9.6 (HTTP 200, 27609 bytes, sha256 f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763) - 0 occurrences of limine_version / limine_version_source / visibility_era / echo / version, so it states neither the gate's JSON fields nor echo semantics; corroborating rejects USAGE.md and README.md (200) and limine.1 (404). SWEEP: 60 hits listed with file:line; four hit lines still assert the era-B text-comparer defect, all in the frozen r97 instrument bytes (tools/limine-pin-battery-r97.py:1817,1820) and their byte-identical do-nothing control (sha256 e678c34f both) - no corpus/, plan, lesson, scorecard or knowledge sentence still asserts it; the r98 successor carries the corrected sentence. Incidental (not my scope, reported only): the coverage gate reads FAIL at lane tip 1cfeb5d5 with 3 REGISTRY-ROW-MISSING findings for the three r98 tools (tools_total 160 vs registered 157); the three registry rows are present in the working tree at SKILL.md:5944-5946 but uncommitted, so the finding clears on commit."}
