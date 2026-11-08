# ScoutSources — round 99 wave w1 — source anchors for the proposed own-work row

Full report: `.ufo/waves/round-99/w1/ScoutSources/report.md`.
Receipts: `.ufo/waves/round-99/w1/ScoutSources/receipts/`.
Row candidate: `.ufo/waves/round-99/w1/ScoutSources/sources-row-candidate.md`.

Verdict: **met**. `corpus/SOURCES.md` was NOT edited.

## Anchors (byte-level, on the pinned bytes — QUALITY 141)

Instrument integrity first: `sha256sum -c .ufo/waves/round-99/before/instruments.sha256` → 17 files
OK, exit 0. Gate `7d79ac29…`, r99 battery `c2e8c8fc…`.

| site | byte | line | quote |
|---|---|---|---|
| gate MAIN return `"limine_version"` | 16931 | 316 | `"limine_version": limine_version,` |
| gate MAIN return `"visibility_era"` | 17037 | 318 | `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5",` |
| gate EARLY (CANNOT-EVALUATE) `"limine_version"` | 11230 | 200 | `"limine_version": limine_version,` |
| gate EARLY (CANNOT-EVALUATE) `"visibility_era"` | 11344 | 202 | `"visibility_era": "12.9.5+" if era_b else "pre-12.9.5",` |
| battery `def meta_ok(c, got):` | 99305 | 2179 | `def meta_ok(c, got):` |
| battery echo assertion | 99430 | 2181 | `if c.check_echo and not (got[8] == c.version and got[9] == "flag"):` |
| battery era assertion | 99523 | 2183 | `if c.check_era and got[10] != ("12.9.5+" if c.era_b() else "pre-12.9.5"):` |

`c.check_echo = True` / `c.check_era = True` sites, one per family (every line text is exactly
`    c.check_echo = True` / `    c.check_era = True`):

| roster family | echo byte/line | era byte/line |
|---|---|---|
| `REFUSAL-VERSIONS-9DIGIT` (X cap, r99) | 79015 / 1775 | 79039 / 1776 |
| `EXPLICIT-VERSION-ECHO` | 79893 / 1792 | — |
| `EXPLICIT-VERSION-ERA` | — | 80414 / 1801 |
| `REFUSAL-VERSIONS-9DIGIT-Y` (Y cap, r99) | 81666 / 1817 | 81690 / 1818 |
| `REFUSAL-VERSIONS-9DIGIT-Z` | 83173 / 1840 | 83197 / 1841 |
| `LEADING-ZERO-NORMALIZE` | 84390 / 1857 | 84414 / 1858 |

New lie kinds: `LIE_KINDS = (` at 108277 (line 2369); `"limine-version"` at **108455** and
`"visibility-era"` at **108473** (both line 2370). The pinned r98 battery's `LIE_KINDS` (BYTE 106583,
line 2345) holds 12 members, none of them those two — the r98 structural gap, closed.

Commands used (exact):

```
grep -abo '"limine_version"' tools/check-limine-pins.py
grep -abo '"visibility_era"' tools/check-limine-pins.py
grep -abo 'def meta_ok' tools/limine-pin-battery-r99.py
grep -abo 'check_echo' tools/limine-pin-battery-r99.py
grep -abo 'check_era' tools/limine-pin-battery-r99.py
python3 -c "b=open('<path>','rb').read(); off=b.find(b'<needle>'); line=b[:off].count(b'\n')+1; ls=b.rfind(b'\n',0,off)+1; le=b.find(b'\n',off); print(off,line,b[ls:le].decode())"
```

## S392 re-open — identical, no drift

`https://docs.python.org/3/library/functions.html#int` → 301 → `https://docs.python.org/3/builtins/functions.html`;
HTTP 200, **331022 bytes**, sha256 `d92580dd0e7a02aab9b51fe30885ae59fd924c639324c7e07a90799e8bc721d7`
= the r98 pin exactly. Offsets re-measured: `have leading zeros, be surrounded by whitespace`
**157767**, `id="int"` **153202**, `disallows leading zeros` **159315** — the row's three offsets.

## CONFIG.md rejection candidate — reject

`https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/CONFIG.md` → HTTP 200,
**27609 bytes**, sha256 `f44f3a19133cb3dc14d6d8b402ed585feb98a36bc4b263c37aa92f621f603763`.
`grep -c` for `limine_version` / `visibility_era` / `echo` / `version` → **0 / 0 / 0 / 0** (sanity:
495 lines; `timeout` 7, `protocol` 17 — the zeros are real absences, not a failed fetch). The page
documents Limine's config keys, not the gate's JSON fields; it grounds none of this round's
propositions, so it stays a rejection (evidence of taste).

## Finding for the L1

**`S395` is already taken in the working tree** — `corpus/SOURCES.md:406` carries an `S395` row for
this round's subject (`git show HEAD:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S395[[:space:]]*\|'`
→ 0, so it is new in the round's uncommitted tree). Every anchor that row claims reproduces
byte-exactly on the pinned bytes (99305 / 99430 / 99523; 79015, 79893, 81666, 83173, 84390;
79039, 80414, 81690, 83197, 84414; 108455; 16931 / 17037), so the landed row is **grounded**. A
wider-scope row must take **S396** with `supersedes S395 — ` (contract v1 rule 2: ids are never
reused; only `status`, `recheck`, `used-by` change in place). Also: that row names the two new
`LIE_KINDS` members with one offset (108455); the second member's own offset is 108473 — a
superseding row would name both.

## Scope note

Source anchors only. This seat did not re-run the gate, battery, bends, lie wrappers or checker, so
it neither confirms nor contradicts the L1's run readings. Two read-only public-document fetches;
no network write, no credential material, nothing quoted from the environment. Scratch
`/fast/scratch/hyaku/tsukuroi-r99/ScoutSources` deleted before yield.

```json
{"seat":"ScoutSources","verdict":"met","notes":"Byte anchors located on pinned bytes: gate MAIN 16931/17037 (lines 316/318), EARLY 11230/11344 (lines 200/202); r99 battery meta_ok 99305 (2179), echo assertion 99430 (2181), era assertion 99523 (2183); ten c.check_*=True sites over six families (X cap 79015/79039, Y cap 81666/81690); LIE_KINDS 108277 (2369) with new members 108455/108473 (2370). S392 re-opened identical (331022 bytes, sha256 d92580dd...; offsets 157767/153202/159315). CONFIG.md reject (200, 27609 bytes, sha256 f44f3a19...; counts 0/0/0/0). FINDING: S395 id already taken at corpus/SOURCES.md:406 in the working tree; all its anchors reproduce byte-exactly; a wider row must take S396. corpus/SOURCES.md not edited."}
```
