# ScoutSources — round-95 w1 — the new SOURCES row (S389), the Limine re-open, host freshness

Seat: SCOUT (leaf member; no subagent dispatch). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
@ `884ed06bdc7681ad73e757cf8a02bee21de2c480` (HEAD detached; `refs/heads/master` at the same commit).
Axis: **freshness**. Date: 2026-11-08. Scratch: `/fast/scratch/hyaku/tsukuroi-r95/ScoutSources/`
(created before the first command, removed on exit).
Files written by this seat: **only** `.ufo/waves/round-95/w1/ScoutSources/` (this report + `receipts/`
+ `pins/`) and the wave-level report `.ufo/waves/round-95/w1/ScoutSources.md`. No lane file outside
that seat dir was edited. No git/jj mutation was run in the lane (`git rev-parse`, `git status`,
`git symbolic-ref` only — all read-only).
No tool was installed, upgraded or removed: every command used a preinstalled `curl`, `python3`,
`sha256sum`, `wc`, `cmp`, `pacman` (query only). **No installs, no updates, no channel.**

Receipts (all under `.ufo/waves/round-95/w1/ScoutSources/`):

| receipt | content |
|---|---|
| `receipts/pin-table.tsv` | URL, HTTP status, bytes, sha256, access date, local copy for every fetch (9 rows) |
| `receipts/receipt-01-python-stdtypes.txt` | the new source: both URL forms, the pin's sha256/size, page title, the two quoted sentences with raw byte offsets, and the host-side confirmation of the documented behaviour |
| `receipts/receipt-02-limine-reopen.txt` | S386/S387/S388 re-opened: HTTP status, sha256, ≤25-word quote, locator, and the three-tag byte comparison that dates the cut |
| `receipts/receipt-03-freshness.txt` | `pacman -Si limine`, `limine --version`, the upstream package index, and the era-impact analysis |
| `receipts/receipt-04-sources-row-draft.txt` | the drafted S389 row, the S389-is-free check, and the census validation of the drafted row |
| `receipts/receipt-05-lesson-gate-draft.txt` | the `## Gate` draft lines for the round-95 lesson |
| `pins/` | the fetched bytes themselves (9 files) |

---

## 1. The new row's source — the Python docs page, fetched, hashed, pinned

Fetched (read-only GET), the URL the brief named:

```
$ curl -sSL -w '\nHTTP_STATUS:%{http_code}\nSIZE:%{size_download}\nURL_EFFECTIVE:%{url_effective}\n' \
    -o pins/python-3-stdtypes.html \
    'https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation'
HTTP_STATUS:200
SIZE:815447
URL_EFFECTIVE:https://docs.python.org/3/builtins/stdtypes.html      (1 redirect)

$ sha256sum pins/python-3-stdtypes.html
6bf2ce2ba49d30974485266d70aecd4c4eb89334eb73367f3f99bfa036c7e9a8
$ wc -c pins/python-3-stdtypes.html
815447
```

**Access date: 2026-11-08.** The version-pinned form of the same page was fetched as a cross-check
and is **byte-identical** (`cmp` → identical, same sha256, same 815447 bytes):
`https://docs.python.org/3.15/library/stdtypes.html#integer-string-conversion-length-limitation` →
`https://docs.python.org/3.15/builtins/stdtypes.html`, HTTP 200.

Page identity: `<title>Built-in Types — Python 3.15.2 documentation</title>`, build stamp
`Last updated on Nov 08, 2026 (07:53 UTC)`. The anchor the brief names **exists**:
`<section id="integer-string-conversion-length-limitation">` at byte 780197 of the pin, with the
inner span `id="int-max-str-digits"` at byte 780256.

### The two sentences the brief asked for — located, with raw offsets

| # | sentence (rendered) | words | raw byte offset in the 815447-byte pin |
|---|---|---|---|
| Q1 (contains `4300`) | "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits." | 10 | **785297** |
| Q2 (contains `ValueError`) | "When an operation would exceed the limit, a ValueError is raised:" | 11 | **782228** |

Both live in the section `id="integer-string-conversion-length-limitation"`. The exception's own
message is at byte **783329**: "ValueError: Exceeds the limit (4300 digits) for integer string
conversion: value has 5432 digits" (the page's first example; the second example at the same
message shape names 5432 vs 4300). Supporting sentence recorded for the L1: "The lowest limit that
can be configured is 640 digits as provided in sys.int_info.str_digits_check_threshold." (byte
785568). The page also states the limit applies only to non-power-of-two bases (hex/octal/binary are
unlimited) and that "Underscores and the sign are not counted towards the limit" — scope notes the
knowledge entry should not drop.

Host-side confirmation of the documented behaviour (read-only, no install):
`python3 -c "import sys; print(sys.int_info.default_max_str_digits)"` → **4300**, threshold **640**
on this host's CPython 3.14.8; `int('9'*9)` and `int('9'*10)` succeed, `int('2'*4300)` succeeds,
`int('2'*4301)` raises `ValueError: Exceeds the limit (4300 digits) for integer string conversion`.
So the documented `ValueError` is observable here, and the 9- and 10-digit versions that C1's family
turns on are **far below** the CPython limit — the gate's 9-digit cap is a published contract of the
gate, not a consequence of CPython's 4300. The Python page documents *why a component is length-
checked before `int()`* (the gate's own docstring at `tools/check-limine-pins.py:92-95` cites exactly
that: "A component longer than 9 digits is refused rather than handed to int(), which raises above
4300 digits (round-92 ReviewGate F1)"); it does not and cannot certify that nine digits is the
right design.

**PASS** — page fetched (HTTP 200), pinned with sha256 `6bf2ce2b…` and byte size 815447, and both
requested sentences located with raw offsets.

---

## 2. The re-opened Limine sources — still resolve, still agree

All three re-opened 2026-11-08 with HTTP 200, and **every sha256 reproduces the lane's own r94
frozen copy byte-for-byte** (`sha256sum .ufo/waves/round-94/before/src/limine-v12.9.6-*`):

| row | URL | HTTP | bytes | sha256 | matches r94 freeze copy |
|---|---|---|---|---|---|
| S386 | `…/limine/v12.9.6/common/lib/config.c` | 200 | 23351 | `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60` | **yes** |
| S387 | `…/limine/v12.9.6/ChangeLog` | 200 | 122099 | `ab280b451ee6f56bad5684d44eda5c94bf43d2c17e9e651b8e84b433584d03ba` | **yes** |
| S388 | `…/limine/v12.9.6/host/limine.c` | 200 | 69050 | `4da21c7cceae238075612643b845cb63e06cc184977e950d5e6374329bc31ec0` | **yes** |

The ≤25-word located quotes that support the entry's two claims:

**"the cut applies from 12.9.5 on"** — corroborated twice, once per source:

- S386 (`common/lib/config.c`), raw 328-330, inside `create_menu_tree()`:
  > `if (p > config_addr) { *(p - 1) = '\0'; }`

  The cut is present at the v12.9.6 tag. To date it, three tags were fetched today:
  v12.9.6 `config.c` = `a940acae…` (23351 B) and v12.9.5 `config.c` = `a940acae…` (23351 B) are the
  **same bytes**; v12.9.4 `config.c` = `aafc9c41…` (24554 B) **differs** and `grep -n 'p > config_addr'`
  on it returns **no match** — the cut does not exist one tag earlier. So the cut is a 12.9.5 change.

- S387 (`ChangeLog`), raw 13-16, the 12.9.6 release block's `Miscellaneous:` subsection:
  > "A config whose first line is an entry has had no global options since 12.9.5."

  (15 words; the upstream sentence continues "whereas every option in it used to count as global.
  Fixes #700." The 25-word full form is also available in receipt-02.)

**"the version prints as `Limine X.Y.Z`"** — S388 (`host/limine.c`), raw 2035:

> `puts("Limine " LIMINE_VERSION);`

with the bare version at raw 2031 (`puts(LIMINE_VERSION);`, the `--version-only` line), the macro at
raw 2002 (`#define LIMINE_VERSION "%VERSION%"`, substituted at build time), and the `--version`
dispatch at raw 2089-2091. `host/limine.c` at v12.9.5 is byte-identical (`4da21c7c…`), so the
version-print code did not change between the tags. On this host the binary prints `Limine 12.9.4`,
matching the shape upstream's code produces.

**PASS** — all three sources resolve (HTTP 200), all three digests reproduce the lane's own frozen
copies, and the quotes support both claims.

---

## 3. Freshness — packaged vs installed, and the era question

```
$ pacman -Si limine            (read-only query; NO -Sy, no transaction)
Repository      : extra
Version         : 12.9.4-1
Build Date      : Tue 20 Oct 2026 04:34:10 AM -03
...
$ stat -c '%y' /var/lib/pacman/sync/extra.db
2026-10-22 01:40:04 -0300

$ limine --version
Limine 12.9.4
(exit 0; /usr/bin/limine)

$ pacman -Qi limine   ->   Version: 12.9.4-1
```

- **Packaged Version/Release: 12.9.4-1** (pkgver 12.9.4, pkgrel 1), from the local sync database
  dated 2026-10-22.
- **Installed binary's answer: `Limine 12.9.4`** (`limine --version`, rc 0). Installed == packaged.
- **Is the host behind the packaged version?** No, by `pacman -Si`'s own reading: the local database
  advertises 12.9.4-1 and 12.9.4-1 is installed. But that database is 17 days stale: a read-only GET
  of `https://archlinux.org/packages/extra/x86_64/limine/json/` (HTTP 200) reports upstream's current
  `extra/limine` as **12.9.6-1**, built 2026-10-28 — so the host is **two releases behind upstream**,
  and `pacman -Si` under-reports because no `-Sy` was run. (GitHub's latest release API answers
  `v12.9.6`, published 2026-10-27 — the pinned tag is still upstream's current release, so the pins
  are not behind.) This is the same standing observation the r94 scout recorded; unchanged today.
- **Does the host lag change any era answer? No.** The era split is a constant in the instruments,
  not a host reading: `tools/check-limine-pins.py:104` `VISIBILITY_ERA_SPLIT = (12, 9, 5)`, used at
  line 193 (`era_b = version >= VISIBILITY_ERA_SPLIT`) and 202 (`"visibility_era": "12.9.5+" if era_b
  else "pre-12.9.5"`); the battery mirrors it at `tools/limine-pin-battery-r95.py:321-326`.
  - The **r95 family does not depend on the host at all**: it sets the version explicitly —
    `REFUSAL_DIGIT9 = "9" * 9 + ".9.9"` (battery 1694), used at battery 1715, and `pass_version` stays
    True, so the battery passes `--limine-version 999999999.9.9` (battery 1981-1982) instead of
    probing. (999999999, 9, 9) ≥ (12, 9, 5) is True → **era B**, the first-line key is invisible, the
    expected answer is `panic`. A host upgrade to 12.9.6 changes nothing here.
  - The **host-coupled leg is r94's `ERA-DEFAULT`** (battery 1637: `_era_first_line_panic(c, "12.9.4",
    pass_version=False)`; the comment at 1983-1986), which omits the flag so the gate probes the host.
    Today the host answers 12.9.4 → era A → the key is visible → `prompt` is expected. **If limine
    were upgraded to 12.9.6, that family would probe era B and expect `panic`** — it would need
    re-baselining. That is a recheck trigger, not a present error.
  - Nothing in C1's or C2's frozen sentences depends on the host's installed limine version: C1's
    predicate names the version the fixture carries; C2's names the SKILL.md registry table and the
    gate's counts.

**PASS** — packaged version, installed answer, and the era-impact analysis are all recorded with
their artifacts.

---

## 4. The drafted SOURCES row (S389) — and its census validation

**S389 is free.** The registry's highest id is S388, the row count is 388, and `grep -rn 'S389'`
finds no registry row (the only hits are this round's own dispatch files quoting the seat brief).

The drafted row, in the lane's schema (11 columns; the census parses NF==13) — **the exact bytes are
in `receipts/receipt-04-sources-row-draft.txt`**; the URL is the version-pinned `/3.15/` form because
the two forms serve byte-identical content today and the pinned form does not drift with the next
Python release (the reason S385's own cell records).

| column | value (abridged; full text in the receipt) |
|---|---|
| id | `S389` |
| source | Python 3 documentation — integer string conversion length limitation, version-pinned — `https://docs.python.org/3.15/library/stdtypes.html#integer-string-conversion-length-limitation` |
| kind | `docs` |
| tier | `A` |
| scope | The CPython int↔str decimal-conversion digit limit and the ValueError it raises past it — the upstream reason a version component is length-checked before it is handed to `int()` |
| anchor | § "Integer string conversion length limitation" (`<section id="integer-string-conversion-length-limitation">`, byte 780197; inner span `id="int-max-str-digits"` byte 780256); the `4300` sentence at byte 785297, the `ValueError` sentence at byte 782228; page title "Built-in Types — Python 3.15.2 documentation"; fetched 2026-11-08, 815447 bytes, sha256 `6bf2ce2b…` |
| teaches | the default conversion limit is 4300 digits — "The default limit is 4300 digits as provided in sys.int_info.default_max_str_digits." — and a conversion past it raises `ValueError` ("When an operation would exceed the limit, a ValueError is raised:"), which is why a version component is refused on its digit count rather than parsed |
| status | `mined` |
| opened | `2026-11-08` |
| recheck | `on-release` |
| used-by | `corpus/knowledge/limine-bound-9digit-r95.md, corpus/lessons/round-95.md` |

**Census validation of the drafted row** (measured on a lane-shaped COPY of the tree under scratch —
`corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/`, `corpus/QUALITY.md`, `SKILL.md`,
`tools/` all copied, the row inserted right after S388, the two used-by targets stubbed):

```
$ bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin \
      --file .../lanetest/corpus/SOURCES.md --today 2026-11-08
EXIT=0
$ ... | grep 'S389'   ->  (no output)     # S389 draws NO finding of any code
$ ... | grep -c 'W04' ->  57              # identical to the lane's own baseline (57 W04 + 1 W01)
$ ... | tail -1
file	ok	.../lanetest/corpus/SOURCES.md
```

No E01/E02/E03/E04/E05/E06/E07/E08/E09/E10/E11/E12 and no W01/W03/W04 raised by the new row. The
lane's **real** registry, unchanged, still validates clean (`validate --root … tsukuroi` → EXIT=0,
57 W04 + the pre-existing W01 on S381).

**Ordering dependency the L1 must honour:** the census's E11 rule requires each used-by path to
exist on disk. The two paths this row names do **not** exist yet
(`ls corpus/knowledge/limine-bound-9digit-r95.md corpus/lessons/round-95.md` → "No such file or
directory") — they are the files the ScribeKnowledge and ScribeLesson seats draft this wave. The row
becomes E11-clean once the L1 lands those two files; integrate the row together with (or after)
them and re-run `sources-census.sh validate` to confirm zero E11. (Same ordering already governs
S386-S388, whose used-by paths are the r94 entry and lesson.)

**`corpus/SOURCES.md` was NOT edited** — the row above is a draft for the L1 to integrate, as the
seat brief requires.

---

## 5. The `## Gate` draft for the round-95 lesson

Drafted in `receipts/receipt-05-lesson-gate-draft.txt`, in the shape of `corpus/lessons/round-94.md`
§ Gate (table `row | URL opened | tier | located quote (≤25 words)`, then "Admitted:", then
"Rejected / refused this round:"). The five rows are S389 (two quotes: the `4300` sentence and the
`ValueError` sentence) and the three re-opened Limine rows (S386/S387/S388), all with access date
2026-11-08; the draft states that nothing was rejected this round (every URL opened returned 200),
that S386-S388 are re-opens rather than new rows (their used-by cells are unchanged), and carries the
host-freshness note (packaged 12.9.4-1 vs upstream 12.9.6-1; the host lag does not touch this
round's era answers).

---

## 6. What I did not do

No claim adjudication (the claim seats own C1/C2); no battery, gate, bend or registry run (other
seats). No edit to `corpus/SOURCES.md`, `corpus/knowledge/`, `corpus/lessons/`, `SKILL.md`, the
instruments, `tools/make-r95-bends.py`, the freeze manifest, `claims.json` or the plan. No
`sudo`, no pacman transaction, no `limine` invocation other than `limine --version`, no
`/boot/limine.conf` access. No git/jj mutation in the lane.

**One incident, disclosed in full.** While validating the drafted row I built a lane-shaped scratch
tree whose `corpus/knowledge` and `corpus/lessons` were **symlinks** into the real lane, and my
`touch` of the two used-by placeholder files therefore created two empty files in the live lane:
`corpus/knowledge/limine-bound-9digit-r95.md` and `corpus/lessons/round-95.md`. Both were detected
immediately (`git status --porcelain` showed them as untracked) and **removed with `rm -f`** in the
next command; the lane was re-verified clean immediately afterwards
(`git status --porcelain` → only `.ufo/waves/round-95/**` untracked entries, no tracked file
modified). The scratch tree was rebuilt with **copies** instead of symlinks and re-measured, giving
the census result quoted above. No byte of any tracked lane file was ever modified, and no corpus
knowledge or lesson file survives from that touch.

---

## Verdict

**Freshness: SUPPORTED, with two carryable notes.**
The round's new source resolves and is pinned: `https://docs.python.org/3/library/stdtypes.html#integer-string-conversion-length-limitation`
→ HTTP 200 → `https://docs.python.org/3/builtins/stdtypes.html`, 815447 bytes, sha256
`6bf2ce2ba49d30974485266d70aecd4c4eb89334eb73367f3f99bfa036c7e9a8`, access date 2026-11-08; the
`4300` sentence is at raw byte 785297 and the `ValueError` sentence at raw byte 782228 of the pin,
and the version-pinned `/3.15/` form serves byte-identical content. The three Limine sources the
entry cites still resolve (HTTP 200 ×3) and their digests still reproduce the lane's own r94 frozen
copies byte-for-byte, and the re-opened quotes still support both claims — "the cut applies from
12.9.5 on" (ChangeLog sentence + the cut's absence at v12.9.4 and byte-identity at v12.9.5) and
"the version prints as `Limine X.Y.Z`" (`puts("Limine " LIMINE_VERSION);`). The drafted row S389 is
census-clean on a scratch copy (EXIT=0, zero findings for the row). Host freshness: packaged
`limine` is **12.9.4-1** from a 2026-10-22 sync database, the installed binary answers
**`Limine 12.9.4`**, upstream's live `extra/limine` is **12.9.6-1** — the host is two releases behind
upstream but not behind its own database, and that lag changes **no** era answer in C1 or C2 (the
r95 family pins its own version; only r94's `ERA-DEFAULT` is host-coupled and would need
re-baselining after a limine upgrade). Two notes for the L1: (1) the S389 row's used-by paths
(`corpus/knowledge/limine-bound-9digit-r95.md`, `corpus/lessons/round-95.md`) must land together with
it or the census reports E11; (2) the pin's digest is Sphinx-stamp dependent, so re-verify by the
title/version string and the two sentence offsets, never by the digest — the same caveat S385
already records.

Receipts: `.ufo/waves/round-95/w1/ScoutSources/{receipts/pin-table.tsv, receipts/receipt-01-python-stdtypes.txt, receipts/receipt-02-limine-reopen.txt, receipts/receipt-03-freshness.txt, receipts/receipt-04-sources-row-draft.txt, receipts/receipt-05-lesson-gate-draft.txt, pins/}`.

{"seat":"ScoutSources","verdict":"met","notes":"New source pinned: docs.python.org stdtypes 4300/ValueError section, HTTP 200, 815447 B, sha256 6bf2ce2b..., quotes at raw offsets 785297 (4300) and 782228 (ValueError), access 2026-11-08; /3.15/ form byte-identical. S386/S387/S388 re-opened HTTP 200 and byte-identical to the r94 frozen copies (a940acae/ab280b45/4da21c7c); cut dated to 12.9.5 by ChangeLog sentence + absence at v12.9.4; version print puts(\"Limine \" LIMINE_VERSION) at raw 2035. Freshness: packaged limine 12.9.4-1 (sync db 2026-10-22), installed answers 'Limine 12.9.4', upstream extra/limine 12.9.6-1 - host two releases behind upstream, not behind its own db; no era answer changes (r95 family pins 999999999.9.9, only r94 ERA-DEFAULT is host-coupled). S389 drafted (id free, max S388, 388 rows), census-clean on a scratch copy (EXIT=0, no finding for S389); corpus/SOURCES.md NOT edited - L1 integrates, and must land the two used-by files with the row or E11 fires. Disclosed incident: two empty files briefly created in the live corpus via scratch symlinks, removed in the next command, lane re-verified clean."}
