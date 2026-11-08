# ScoutSources — round-98 wave w1: S392 / S393 re-opens, one reject candidate, stale-statement sweep

Seat: ScoutSources (scout). No claim rests on this seat; the numbers below are the sources' own
re-opens, the rejection record, and the sweep.

Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
Seat dir: `.ufo/waves/round-98/w1/ScoutSources/` (full report: `ScoutSources/report.md`)
Scratch: `/fast/scratch/hyaku/tsukuroi-r98/ScoutSources` (removed before yield).

Reads first: `.ufo/waves/round-98/claims.json`, `.ufo/plans/round-98.md`,
`.ufo/waves/round-98/before/instruments.sha256`,
`corpus/lessons/round-97-verifier-spotcheck.md`, `corpus/QUALITY.md` 139-141.

No file outside this seat dir and this seat's top-level file was written; no git/jj mutation; no
pacman, no `sudo`, no tool install (host's `curl 8.23.0`, `grep 0.2.0`, `sha256sum 0.8.0`,
`python3 3.14.8` used as found).

## Manifest (before any measurement)

`$ sha256sum -c .ufo/waves/round-98/before/instruments.sha256` → **28/28 OK, 0 FAILED**
(`receipts/` of the seat dir; the raw output is quoted in `ScoutSources/report.md` §0).

## 1. S392 re-open — external — BYTE-IDENTICAL

```
$ curl -sSL -o s392.html -w 'HTTP %{http_code} bytes %{size_download}\n' https://docs.python.org/3/library/functions.html#int
HTTP 200 bytes 331022
$ sha256sum s392.html
d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7  s392.html
```

* URL: `https://docs.python.org/3/library/functions.html#int` → **HTTP 301** to
  `https://docs.python.org/3/builtins/functions.html` → **HTTP 200**, **331022 bytes**,
  sha256 **`d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7`**.
* **r97 pin comparison: BYTE-IDENTICAL** (r97 pin = same sha256, same 331022 bytes). Also
  byte-identical to all three committed r97 snapshots of the page.
* Quote offsets re-measured at BYTE level (`grep -abo`, QUALITY 141), each anchor unique in the file:

| anchor | row states | measured |
|---|---|---|
| `id="int"` | 153202 | **153202** |
| "have leading zeros, be surrounded by whitespace" | 157767 | **157767** |
| "disallows leading zeros" | 159315 | **159315** |

Located quote (7 words, in context): *"…the string can be preceded by + or - (with no space in
between), **have leading zeros, be surrounded by whitespace,** and have single underscores
interspersed between digits…"*; and the base-0 contrast *"Base **0 also disallows leading zeros:**
`int('010', 0)` is not legal…"*.

**PASS.** (Wording note: the row's `teaches` cell says "radix string"; the page says "base-n
integer string" — `radix string` occurs 0 times in the pinned bytes. Faithful in substance.)

Receipts: `receipts/02-s392-refetch.txt`, `receipts/03-s392-byte-offsets.txt`.

## 2. S393 re-open — own-work — re-derives, with one label defect

Nine gate runs on the pinned gate (`tools/check-limine-pins.py`, sha256 `7d79ac29…`), scratch-local
fixture, `--limine-version <SPELLING>`:

| flag | `limine_version` echoed | source | `visibility_era` | rc |
|---|---|---|---|---|
| `12.09.4` (leading-zero) | `12.09.4` | `flag` | `pre-12.9.5` | 0 |
| `000000012.9.4` (leading-zero) | `000000012.9.4` | `flag` | `pre-12.9.5` | 0 |
| `12.000000009.000000005` (LZ) | verbatim | `flag` | `12.9.5+` | 0 |
| `12.9.999999999` (Z) | verbatim | `flag` | `12.9.5+` | 0 |
| `0.9.999999999` (Z) | verbatim | `flag` | `pre-12.9.5` | 0 |
| `000000000.000000000.000000000` | verbatim | `flag` | `pre-12.9.5` | 0 |
| `12.9.4` / `12.9.5` / `12.9.6` | verbatim | `flag` | as the tuple selects | 0 |

Against the row's `teaches` cell (verbatim echo, source `flag`, era from the whole tuple):
**PASS** on all three clauses.

Byte offsets on the pinned gate bytes (`grep -abo`): **11230** (`"limine_version": limine_version`),
**11344** (`"visibility_era": "12.9.5+" if era_b else "pre-12.9.5"`), **4425** (docstring
``resolved `limine_version` and `limine_version_source: "probe"` ``) — all three match the row.

**FINDING (label defect; the claim is unaffected).** The S393 anchor cell calls 11230/11344
*"main return after parsing"*. Counting newlines in the same bytes: 11230 → line 200 and 11344 →
line 202 are the **CANNOT-EVALUATE early return** of `check()`; the main return's identical field
text is at **16931 / 17037** (lines 316/318). The pointer does not describe the bytes it cites.
The `teaches` cell is unaffected — `era_b` is computed once (line 193) before either return and
both emit the same values, which the nine runs above confirm. Same class as the routed R97-D1/D2
provenance-label defects: the number is right, the pointer is not. Recommend the round-98 report
cite 16931/17037 for the main return, or drop the phrase.

Receipts: `receipts/04-s393-gate-reopen.txt`, `receipts/05-s393-gate-byte-offsets.txt`.

## 3. Reject candidate — limine `CONFIG.md` v12.9.6

```
$ curl -sSL -o limine-config-v12.9.6.md -w 'final_url=%{url_effective} http=%{http_code} bytes=%{size_download}\n' https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md
final_url=https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md http=200 bytes=27609
$ sha256sum limine-config-v12.9.6.md
f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763  limine-config-v12.9.6.md
```

**HTTP 200, 27609 bytes, sha256 `f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763`.**

**REJECTED.** Reason: it states **neither** thing this round's claims need.
*Gate's JSON fields:* `limine_version`, `limine_version_source`, `visibility_era` occur **0 times
each** — the page is upstream's *limine.conf* reference (config-file location, structure, options,
paths, macros), with no JSON report contract at all.
*Echo semantics:* `echo` occurs **0 times** — no sentence says a version string is echoed verbatim
or normalised, so it cannot ground S393 (which is an own-work row and is grounded in the gate
bytes). It also cannot ground S392: `version` occurs **0 times** in the page and `leading zero`
**0 times**, and it never mentions the 12.9.5 era split.

Corroborating rejects, measured the same way: `USAGE.md` (HTTP 200, 10710 bytes,
sha256 `db32c4e05427322fc5c4be70773a3dacbc2e36ff9a94fdfc862172d993a90329`; all seven probe tokens
0), `README.md` (HTTP 200, 2947 bytes, sha256
`318ff36ad960adf3fc3d01eb250e1d30753155dd8b5ced92332db5b2f607b0ce`; all probe tokens 0 except two
build-prose `version` hits), `limine.1` (HTTP **404**, 14 bytes, sha256
`d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` — no such path at the tag).

Receipt: `receipts/06-reject-candidate-config-md.txt`.

## 4. Sweep — 60 hits, every one listed

```
$ grep -rn "000000012.9.4" /home/vgpnk/Projects/shokunin/tsukuroi-shokunin --include='*.py' --include='*.md'
```

**60 hits**, each with file:line, in `receipts/01-sweep-000000012-9-4.txt` (raw) and
`receipts/07-sweep-classified.txt` (every hit with a tag). Files hit:
`.ufo/plans/round-97.md:38`, `.ufo/plans/round-98.md:44`,
`.ufo/waves/round-97/after/report-draft.md:12`,
`.ufo/waves/round-97/before/plan-amendments-r97.md:87-88`,
`.ufo/waves/round-97/before/plan-frozen.md:38`, `.ufo/waves/round-97/make-spec.py:50,159`,
`.ufo/waves/round-97/w1/CriticClaims/report.md:32`,
`.ufo/waves/round-97/w1/ExecBattery.md:69,109`, `.ufo/waves/round-97/w1/ExecBattery/report.md:69,109`,
`.ufo/waves/round-97/w1/ReviewBattery.md:75,112`,
`.ufo/waves/round-97/w1/ReviewBattery/report.md:75,112`,
`.ufo/waves/round-97/w1/ScoutSources.md:105`, `.ufo/waves/round-97/w1/ScoutSources/report.md:105`,
`.ufo/waves/round-97/w1/ScribeKnowledge.md:24,28,80`,
`.ufo/waves/round-97/w1/ScribeKnowledge/limine-bound-9digit-z-r97.md:120,124,137,141,166,252`,
`.ufo/waves/round-97/w1/ScribeKnowledge/report.md:101,118,208,352,426`,
`.ufo/waves/round-97/w1/ScribeLesson/round-97.md:174,175,201`,
`.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py:57,1799,1817,1820,2445`,
`.ufo/waves/round-98/before/plan-frozen.md:44`, `.ufo/waves/round-98/make-spec.py:134`,
`SCORECARD.md:7969`, `corpus/README.md:1195`,
`corpus/knowledge/limine-bound-9digit-z-r97.md:38`,
`corpus/knowledge/limine-metadata-assertions-r98.md:35`,
`corpus/lessons/round-97-verifier-spotcheck.md:53,201`, `corpus/lessons/round-97.md:51`,
`tools/limine-pin-battery-r97.py:57,1799,1817,1820,2445`,
`tools/limine-pin-battery-r98.py:57,1809,1831,1836,2465`.

**Does any surviving sentence still claim the text comparer orders `000000012.9.4` as era B
(the R97-D3/A6 defect)?** Yes — **four hit lines, in two files, and both are the r97 instrument
bytes, not a corpus record**:

* `tools/limine-pin-battery-r97.py:1817` and `:1820` — the **superseded r97 instrument**. The
  round-98 plan states the frozen bytes are not edited this round and that the sentence is
  corrected in the r98 successor with its own manifest (A6) — `.ufo/plans/round-98.md:44-45`,
  `corpus/README.md:1210-1213`. The successor `tools/limine-pin-battery-r98.py:1831-1836` carries
  the corrected sentence (discriminator `12.000000009.000000005`; the text comparer orders it era A
  while `int()` reads 12.9.5) and adds the r98 echo/era assertion.
* `.ufo/waves/round-98/before/controls/do-nothing-battery-r97.py:1817` and `:1820` — the **frozen
  do-nothing control**, byte-identical to the r97 landed battery by construction
  (`sha256` `e678c34f0b30a15a5b333d1e4bfb8e414d5f66a923b6a47d55edd5a080e6a1a8` for **both**,
  measured). It must carry the r97 bytes, so it necessarily carries the r97 sentence; editing it
  would destroy the blindness control.

**Every other hit is neutral (a member list, or the member's correct era) or a sentence that
reports the defect together with the measurement that refutes it.** No `corpus/` record, plan,
lesson, scorecard or knowledge entry still asserts the defect as true.

Refuting measurement, re-derived here: a text comparison against `"12.9.5"` orders `12.09.4`,
`000000012.9.4` and `000000000.000000000.000000000` as era A and `12.000000009.000000005` as era A
as well, while `int()` normalizes that last one to `(12, 9, 5)` = era B — so
`12.000000009.000000005` is the single discriminating member and the r98 docstring's sentence is
the correct one.

**PASS.**

## Incidental (reported, not absorbed; outside this seat's scope)

The lane's coverage gate, read-only: at the pre-round base `b3be3f90` it reads `PASS 157/157
findings 0`; at the current lane tip `1cfeb5d5` it reads `FAIL` with three `REGISTRY-ROW-MISSING`
findings for `tools/check-registry-content-r98.py`, `tools/limine-pin-battery-r98.py` and
`tools/make-r98-bends.py` (committed at that tip; `tools_total 160` vs `registered 157`). The
operative registry table is the round-71 heading (`SKILL.md:5777`). Re-measured after a
concurrent (not mine) edit: the three rows now exist in the **working tree** at `SKILL.md:5944-5946`
(`git diff --stat SKILL.md` → `3 insertions(+)`) but are uncommitted, and the gate reads a
committed revision — so the finding clears on commit. Not a defect in the round's instruments.
No file was edited here.

## PASS/FAIL per expected line

| expected line | verdict |
|---|---|
| S392 URL, HTTP status, byte count, sha256 recorded | **PASS** — 200 / 331022 / `d92580dd…` |
| S392 compared with the r97 pin: byte-identical / drifted / unreachable | **PASS** — byte-identical |
| S392 quote offsets 157767 / 153202 / 159315 re-measured with `grep -abo` | **PASS** — all three exact |
| S393 gate re-run on a leading-zero and a Z spelling | **PASS** — nine runs |
| S393 echoed `limine_version`, `limine_version_source`, `visibility_era` match the row's `teaches` | **PASS** |
| S393 emission offsets 11230 and 11344 re-measured | **PASS** — match (pointer finding above) |
| S393 docstring phrase at 4425 re-measured | **PASS** — match |
| one named rejection with its reason, plus status / bytes / sha256 | **PASS** — limine CONFIG.md v12.9.6 |
| sweep: every hit with file:line, and whether any surviving sentence still claims the era-B defect | **PASS** — 60 hits; 4 assert it, all frozen r97 bytes |
| no credential material recorded | **PASS** |

{"seat":"ScoutSources","verdict":"findings","notes":"S392 re-opens BYTE-IDENTICAL (HTTP 200, 331022 bytes, sha256 d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7) and all three row offsets re-measure exactly (grep -abo 157767/153202/159315). S393 re-derives from the pinned gate bytes: nine runs on the LZ and Z spellings echo the flag verbatim with source 'flag' and report visibility_era from the numeric tuple; offsets 11230/11344/4425 match. FINDING (label defect, claim unaffected): the S393 anchor cell calls 11230/11344 'main return after parsing', but those bytes are the CANNOT-EVALUATE early return (lines 200/202); the main return's same text is at 16931/17037 (lines 316/318) - recommend the report cite 16931/17037 or drop the phrase. REJECT: limine CONFIG.md v12.9.6 (HTTP 200, 27609 bytes, sha256 f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763) - 0 occurrences of limine_version/limine_version_source/visibility_era/echo/version, so it states neither the gate's JSON fields nor echo semantics; corroborating rejects USAGE.md (200), README.md (200), limine.1 (404). SWEEP: 60 hits listed with file:line; 4 hit lines still assert the era-B text-comparer defect, all in the frozen r97 instrument bytes (tools/limine-pin-battery-r97.py:1817,1820) and their byte-identical do-nothing control (sha256 e678c34f both) - no corpus/, plan, lesson, scorecard or knowledge sentence still asserts it; the r98 successor carries the corrected sentence. Incidental (reported, not absorbed): coverage gate reads PASS 157/157 at b3be3f90 but FAIL with 3 REGISTRY-ROW-MISSING for the three r98 tools at lane tip 1cfeb5d5 - the three registry rows are present in the working tree at SKILL.md:5944-5946 but uncommitted, so the finding clears on commit."}
