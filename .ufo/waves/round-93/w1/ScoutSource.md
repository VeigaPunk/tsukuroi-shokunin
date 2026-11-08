# ScoutSource — round 93, wave w1 (freshness axis)

Seat: SCOUT (leaf member — no subagent dispatch). Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
(branch `master`, jj-colocated), read-only throughout. Freeze commit `c633f49aa512e1c8a0e0464b7fb5d354c70096cf`.
Scratch: `/fast/scratch/hyaku/tsukuroi-r93/ScoutSource/` — **deleted on exit** (see §6).

Receipts (this seat's dir): `.ufo/waves/round-93/w1/ScoutSource/`
— `pin-table.tsv`, `quotes.md`, `r92-rows-freshness.md`, `s377-correction.md`,
`dependency-boundary.md`, `locator-discrepancy-S384.md`, `pins/` (11 pinned byte files +
`SHA256SUMS`).

No instrument was edited. `sha256sum -c .ufo/waves/round-93/before/freeze-manifest.sha256` was run
read-only from the lane root: **12 of 13 lines OK**, the one FAILED line being
`.ufo/plans/round-93.md` — the lane's own working-tree amendment A1 (the `## Amendment A1` block
appended after the freeze), not a mutation by this seat. Every byte this seat re-fetched or
compared is upstream or the lane's own committed pins.

---

## 1. Pin table (all fetched 2026-11-08, 06:10–06:12Z)

| # | URL | HTTP | bytes | sha256 | local copy |
|---|---|---|---|---|---|
| 1 | `raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/common/lib/config.c` | 200 | 23351 | `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60` | `pins/limine-v12.9.5-common_lib_config.c` |
| 2 | `…/v12.9.5/ChangeLog` | 200 | 121313 | `d2e08cc4a4bffc4b598b9baf43435cbf05f2c76edcaf89f9ba18f35c42b51779` | `pins/limine-v12.9.5-ChangeLog` |
| 3 | `…/v12.9.5/host/limine.c` | 200 | 69050 | `4da21c7cceae238075612643b845cb63e06cc184977e950d5e6374329bc31ec0` | `pins/limine-v12.9.5-host_limine.c` |
| 4 | `…/v12.9.5/common/lib/misc.c` | 200 | 18196 | `3b81e321992a903071681281a3e2fd12429897b6dca65843bbba2f3a3475bcb5` | `pins/limine-v12.9.5-common_lib_misc.c` |
| 5 | `…/v12.9.6/common/lib/config.c` | 200 | 23351 | `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60` | `pins/limine-v12.9.6-common_lib_config.c` |
| 6 | `…/v12.9.6/ChangeLog` | 200 | 122099 | `ab280b451ee6f56bad5684d44eda5c94bf43d2c17e9e651b8e84b433584d03ba` | `pins/limine-v12.9.6-ChangeLog` |
| 7 | `…/v12.9.4/common/lib/config.c` | 200 | 24554 | `aafc9c410a250efc9674e3c93e839d32ae2731ba2ca60bb7f5edd7ad5828fba8` | `pins/limine-v12.9.4-common_lib_config.c` |
| 8 | `docs.python.org/3/using/cmdline.html` | 200 | 171073 | `2371db30c8f4dfbb8118f990ebd6aed2203c719ed0194d2c46e3325098477aba` | `pins/python-3-cmdline.html` |
| 9 | `raw.githubusercontent.com/containers/bubblewrap/main/bwrap.xml` | 200 | 33289 | `2cb77df2f4be0b2a0302bb2f0a260fdb4d9e1299b76481ea66ed34c40f5be1da` | `pins/bubblewrap-bwrap.xml` |
| 10 | `api.github.com/repos/Limine-Bootloader/Limine/issues/700` | 200 | 5780 | `7c7ac6e0f9330da89cad4bc999a0a3239a39ff57f33629b557b41109499f1049` | `pins/issue-700.json` |

Full table with per-row dates: `ScoutSource/pin-table.tsv`.

**The v12.9.5 / v12.9.6 diff the battery claims.** `diff -u v12.9.5_common_lib_config.c
v12.9.6_common_lib_config.c` → **empty**; the two files are byte-identical, same sha256
`a940acae…`. The battery's claim is **stronger than stated**: not "identical in the cut region"
but identical in the **whole file**. `diff -u` v12.9.4 → v12.9.5 is large and shows the rewrite
from `config_get_entry()`/`is_child()` to `create_menu_tree()`.

---

## 2. The four located quotes (raw line numbers, ≤25 words each)

Full table with word counts and the verification method: `ScoutSource/quotes.md`.

| what | file (tag) | raw lines | quote |
|---|---|---|---|
| **(a) the cut** | `common/lib/config.c` (v12.9.5) | **328-330** | `if (p > config_addr) { *(p - 1) = '\0'; }` |
| **(b) the label-end NUL** | `common/lib/config.c` (v12.9.5) | **362-365** | `if (*p == '\n') { *p = '\0'; p++; }` |
| **(c) the ChangeLog line naming the parser change** | `ChangeLog` (v12.9.5) | **8-9** | `Parse the config in linear time. Configs with thousands of entries were slow to load.` |
| **(d) the version print line** | `host/limine.c` (v12.9.5) | **2035** | `puts("Limine " LIMINE_VERSION);` |

Supporting: `create_menu_tree()` opens at raw **298**; the `--version` dispatch is raw **2089-2091**
(`strcmp(argv[1], "version") == 0 || strcmp(argv[1], "--version") == 0` → `return version(argc - 1, &argv[1]);`);
the `--version-only` print is raw **2031** (`puts(LIMINE_VERSION);`); `#define LIMINE_VERSION "%VERSION%"`
is raw **2002**.

**The file that prints the version is `host/limine.c`, not `common/lib/misc.c`.** Negative locator,
recorded as such: over the pinned v12.9.5 `common/lib/misc.c`, `grep -c 'Limine '` → **0**,
`grep -c -- '--version'` → **0**, `grep -c 'LIMINE_VERSION'` → **0**. `LIMINE_VERSION` is a
build-time placeholder substituted by `GNUmakefile.in` raw **170**
(`s/%VERSION%/@PACKAGE_VERSION@/g`), so the printed number is the **package** version.

**v12.9.6 upstream statement of the same rule** (v12.9.6 `ChangeLog` raw **13-16**):
`Document that global options must come before the first entry, as has been the case since 4.0.` /
`A config whose first line is an entry has had no global options since 12.9.5, whereas every option in it used to count as global.` / `Fixes #700.`

---

## 3. r92 row freshness (S377, S378, S379, S380, S381)

Full detail: `ScoutSource/r92-rows-freshness.md`.

| row | result |
|---|---|
| S378 (bwrap `bwrap.xml`) | live `main` **byte-identical** to the r92 pin (`2cb77df2…`). The anchor's `bwrap 0.13.1` still holds: latest upstream release **v0.13.1** (2026-10-14T12:21:00Z), `main` head `1fb0aa26…` (2026-10-14T12:26:03Z), and the file at tag `v0.13.1` is byte-identical to `main`'s copy. Quoted options still at raw 158-160 / 232-235 / 587. |
| S379 (v12.9.6 `config.c`) | **byte-identical** to the r92 pin. Anchor's line numbers re-checked against the refetch: `create_menu_tree()` 298-407 ✓, cut 328-330 ✓, label-end NUL 362-365 ✓, `menu_tree = create_menu_tree();` at 668 ✓, `config_get_value` at 727 ✓. |
| S380 (v12.9.6 `ChangeLog`) | **byte-identical** to the r92 pin; the `Miscellaneous:` block at raw 13-16 still carries both upstream sentences. |
| S381 (issue #700) | **byte-identical** (JSON sha256 and `body`). `closed`, created 2026-10-27T18:52:23Z, closed 22:43:43Z; the timeline's one `cross-referenced` event points at **#702 "docs: clarify positioning of global options"** (`merged_at` 2026-10-27T22:41:28Z, merge commit `23cae029…`, body `Resolves #700 by correcting the incorrect documentation`). **Freshness note the row does not carry:** the outcome was **documentation-only** — PR #702 changed `CONFIG.md` (v12.9.5 `CONFIG.md` raw 76: `Global options can appear anywhere in the file and are not part of an entry`; v12.9.6 `CONFIG.md` raw 76: `Global options must come before the first menu entry`), while the code cut is unchanged between the tags. S379/S380, not #700, are what carry the behaviour. |
| S377 (Python `-P`/`-I` docs) | The **anchor's version string is wrong**; the quote is right. See §4. |

---

## 4. S377 — the routed defect 3, reproduced, and the proposed correction

Full text: `ScoutSource/s377-correction.md`.

**Measured version strings, 2026-11-08:**

- live page `https://docs.python.org/3/using/cmdline.html` → **`Python 3.15.2 documentation`**
  (3 occurrences; `<title>1. Command line and environment — Python 3.15.2 documentation</title>`);
- the r92 pinned snapshot `.ufo/waves/round-92/before/src/python-3-cmdline.txt` line 1 →
  **`1. Command line and environment — Python 3.15.2 documentation`**;
- the S377 anchor at the freeze commit `c633f49a` → **`Python 3.14 docs`**.

Both the pinned text and the live page already carried 3.15.2 when the row was written: the anchor
was wrong at write time, not stale since. The ≤25-word quote cell is correct and unchanged.

**Two freshness facts the row does not carry:**

1. **The URL is a rolling "latest stable" URL** (`/3/` follows Python's current stable), so the
   version string in the anchor drifts again on the next Python release. The version-pinned URL
   `https://docs.python.org/3.15/using/cmdline.html` (HTTP 200, 171073 bytes, sha256
   `d3c503060ebf18e5a807ba35d8527cfde49f8322373b9111e5c26d657b658cf6`) carries the **same docs
   content**: `diff` against the `/3/` copy is exactly one line — the Sphinx build stamp
   (`Last updated on Nov 08, 2026 (00:12 UTC)` vs `(06:12 UTC)`). The recheck cadence should
   follow Python's release, not a fixed `180d`.
2. **The r93 lesson's parenthetical is false.** `corpus/lessons/round-93.md` line 28 says the
   page's `3.17` mentions "are the development banner". Measured: `3.17` occurs **2** times, both
   inside the `-b`/`-bb` deprecation note (`…schedule them to become no-op in Python 3.17.` /
   `Starting with Python 3.17, no BytesWarning will be raised for these cases; use a type checker
   instead.`). The live page has **no** development banner (`development version` → 0,
   `pre-release` → 0) and `https://docs.python.org/3.17/using/cmdline.html` is **HTTP 404**. The
   pinned r92 snapshot carries the same two `3.17` occurrences at its lines 182 and 184, in the
   same note. The conclusion ("the page is 3.15.2") is right; the stated reason is not, and a
   reader who took "3.17 banner" for a page version would infer the wrong docs version.

**Proposed appended-row correction** (never a silent rewrite) — full 11-cell row text in
`s377-correction.md`; shape:

```
| S385 | Python 3 documentation — command line and environment (`-P`, `-I`), version-pinned — https://docs.python.org/3.15/using/cmdline.html#cmdoption-P | docs | A | … | tag `3.15` docs (docs version string `Python 3.15.2 documentation`), `-P` entry `cmdoption-P`, `-I` entry `cmdoption-I`; fetched 2026-11-08, sha256 `d3c50306…` | supersedes S377 — the anchor named `Python 3.14 docs`; the pinned snapshot and the live page both carry `Python 3.15.2`, and the version-pinned URL keeps the locator from drifting with the next Python release; the `-I`/`-P` quote is unchanged | mined | 2026-11-08 | on-release | corpus/knowledge/limine-r92-oracle-isolation.md, corpus/lessons/round-92.md, corpus/lessons/round-93.md |
```

`corpus/CORPUS.md` §SOURCES.md contract v1 rule 2 — *"Append-only. Only `status`, `recheck` and
`used-by` change in place … A correction is a new row whose `teaches` opens `supersedes S0NN —`"* —
and the next unused id after S384 is **S385**.

**Lane-state discrepancy this seat must report.** The working tree already performs an **in-place**
S377 anchor edit (`git diff corpus/SOURCES.md`: `Python 3.14 docs` → `Python 3.15.2 docs`), the
QUALITY-60 sweep `git diff -U0 c633f49a -- corpus/SOURCES.md | grep -E '^-[^-]'` prints exactly
**1** changed line, and `corpus/lessons/round-93.md` lines 26-29 log the change with the sweep
receipt `.ufo/waves/round-93/after/q127-s377-pre.txt` (present). That route is explicitly allowed
by the r92 spot-check's routed defect 3 (*"by an appended row **or** a logged anchor change"*).
**But** `corpus/lessons/round-93.md` line 38 states the disposition as *"corrected by an appended
row (S385)"*, and **no S385 row exists** (`grep -c '^| S385'` → 0; `S385` occurs in the whole lane
only in that sentence). The lesson claims a mechanism it did not use, and the claim is a dangling
id in prose. The lane must pick one route — appended row S385 (then revert the in-place edit and
log that revert, which the sweep must then show as 2 changed lines), or keep the logged anchor
change and correct line 38's sentence to name the logged anchor change rather than a
non-existent S385.

---

## 5. A second locator defect found: the working-tree S384 row

Full text: `ScoutSource/locator-discrepancy-S384.md`.

`corpus/SOURCES.md` S384's anchor (working tree, uncommitted) says the version print is at
**raw 2029**, and `corpus/lessons/round-93.md`'s Gate table repeats *"raw 2029"*. **Raw 2029 is a
blank line.** The print `puts("Limine " LIMINE_VERSION);` is at raw **2035**; the `--version-only`
print `puts(LIMINE_VERSION);` is at raw **2031**, outside the cited `2022-2026` range. Measured on
three copies with one sha256 (`4da21c7c…`: upstream raw, the lane's own r93 pin
`.ufo/waves/round-93/before/src/limine-v12.9.5-host_limine.c`, and my refetch), no CRLF, 2096
lines; `grep -n` → `2035` and `2031`. The same line numbers hold at v12.9.4 and v12.9.6
(`host/limine.c` is byte-identical across all three tags). The row's *quote* is verbatim-correct;
only the line locator is off by six, and the anchor is the row's own verification handle.

Proposed appended-row correction (**S386**, because the r93 lesson already claims **S385** for the
S377 correction — the two must not collide on one id): full 11-cell row text in
`locator-discrepancy-S384.md`.

---

## 6. Dependency boundary

Full text: `ScoutSource/dependency-boundary.md`.

**V2 — the `create_menu_tree()` cut.** Encodes: from 12.9.5 on, a config whose first line is an
entry has no global options visible.

| tag | `common/lib/config.c` sha256 | cut present? | mechanism |
|---|---|---|---|
| v12.9.4 | `aafc9c41…` | no | `init_config()` cuts with `c[-1] = 0` after `config_get_entry(&s, 0)` (raw 642-651); no `create_menu_tree()` in this file |
| v12.9.5 | `a940acae…` | yes | `create_menu_tree()` raw 298-407; cut 328-330; label-end NUL 362-365 |
| v12.9.6 | `a940acae…` | yes | **byte-identical to v12.9.5** |

The era split at `(12, 9, 5)` is **sourced**, not assumed: v12.9.5 `ChangeLog` raw 8-9 dates the
in-place parse to 12.9.5, and v12.9.6 `ChangeLog` raw 13-16 states upstream's own reading
(`A config whose first line is an entry has had no global options since 12.9.5`).

**What would invalidate V2:** any upstream release **after v12.9.6** whose
`common/lib/config.c` changes — specifically `create_menu_tree()` (298-407), the cut (328-330)
or the label-end NUL (362-365) — or a v12.9.7+ `ChangeLog` entry that changes the global-option
rule upstream states at 12.9.6 (13-16). Concretely: the first tag whose
`common/lib/config.c` sha256 differs from `a940acae…`. The era split would also move if upstream
ever made global options after the first entry work again (the #700 / PR #702 outcome was
documentation-only).

**V3 — the `limine --version` output format.** Encodes: `auto` runs `limine --version` read-only
and takes the first parsable `X.Y.Z`.

**What would invalidate V3:** an upstream release **after v12.9.6** that changes
`host/limine.c`'s version print (dropping the `Limine ` prefix, moving the print to stderr, or
changing the `--version`/`version` dispatch) — **or** a distro packaging change that puts a
non-`X.Y.Z` string in `@PACKAGE_VERSION@`. The gate's regex
`(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b` requires the literal word `limine` before the number, so a
bare `12.9.6` first line — the `--version-only` shape at raw 2031 — would **not** match; and a
version like `12.9.6.r1.gabc` would silently parse as `12.9.6`. `host/limine.c` is byte-identical
across v12.9.4/12.9.5/12.9.6 (`4da21c7c…`), so the format is stable across the era boundary.

**Branch-tip state (2026-11-08 06:21Z).** The upstream default branch is **`v12.x`** (`main`
returns HTTP 404 — a re-open of the wrong URL is a false negative). At the tip of `v12.x`,
`common/lib/config.c` = `a940acae…`, `host/limine.c` = `4da21c7c…`, `ChangeLog` = `ab280b45…` —
**all identical to the pinned tags**, and the `ChangeLog` head is still `*** Release 12.9.6 ***`
with no unreleased section above it. Neither V2's cut nor V3's print has moved. Upstream releases
end at **v12.9.6** (2026-10-27T23:16:30Z); tags: v12.9.6 `89a9512c623a`, v12.9.5 `55a93085435a`,
v12.9.4 `8ad14430bc9f`, v12.9.3 `e3aa138d383c`, v12.9.2 `69792f200e90`, v12.9.1 `c82c3708b330`.

**The host trigger that must re-run the battery: a `limine` package upgrade on this host.** The
probe's input is the *installed* bootloader's version, so the trigger is the installed package
changing, not a source re-read.

- installed now: `limine 12.9.4-1` (`pacman -Qi limine`), whose `limine --version` first stdout
  line is `Limine 12.9.4` (measured; the gate's regex extracts `12.9.4`);
- Arch `extra` upstream now ships `limine 12.9.6-1` (archlinux.org package JSON,
  `last_update 2026-10-28T08:00:46Z`; `geo.mirror.pkgbuild.com/extra/os/x86_64/` carries
  `limine-12.9.6-1-x86_64.pkg.tar.zst`);
- therefore the **next `pacman -Syu` that pulls limine 12.9.6-1 flips the probe's answer from
  12.9.4 to 12.9.6**, which flips the selected era from pre-12.9.5 to 12.9.5+, and every
  era-sensitive and refusal-sensitive battery family must be re-measured.

Two measured freshness notes on that trigger:

1. **The host's own package database is stale.** `/var/lib/pacman/sync/extra.db` has mtime
   2026-10-22 01:40 -0300, so `pacman -Si limine` reports `12.9.4-1` and `checkupdates` lists
   6 pending packages, **none of them limine** — the pending 12.9.6 upgrade is invisible to the
   host's current tooling even though upstream carries it.
2. **A mirror skew exists.** The host's configured mirror
   (`/etc/pacman.d/mirrorlist`: `https://stable-mirror.omarchy.org/$repo/os/$arch`) serves an
   `extra.db` with `Last-Modified: Thu, 22 Oct 2026 04:40:04 GMT` whose only limine entry is
   `limine-12.9.4-1/` (verified by listing the db's entries); `mirror.rackspace.com` likewise
   lists only `12.9.4-1`; `geo.mirror.pkgbuild.com` lists `12.9.6-1`. So the era flip can
   arrive without the host's own update check naming it, and a host reading a skewed mirror sees
   the old version.

**Second trigger, independent of the package: `/boot/limine.conf` changing** (the live run's
input). It is root-only on this host (`ls /boot/limine.conf` → `Permission denied`; this seat
did not elevate), so the live receipt `.ufo/waves/round-93/after/live-c2.json`
(`limine_version 12.9.4`, `limine_version_source "probe"`, two `LP-MISMATCH` findings at lines
30 and 38) is a point-in-time reading of a file this seat cannot read.

---

## 7. Notes on the two claims under attack (freshness axis only)

- **C1** — the battery's premise that the v12.9.5 and v12.9.6 files are identical in the cut
  region is **confirmed and understated**: the files are byte-identical in full
  (`a940acae…`), the cut is at raw 328-330 and the label-end NUL at 362-365 **in the v12.9.5 tag
  itself**, and upstream's own `ChangeLog` (v12.9.5 raw 8-9; v12.9.6 raw 13-16) dates the
  behaviour to 12.9.5. The era boundary the families sample (12.9.5 exactly, 12.9.6) is sourced
  at the tag, not inferred from 12.9.6 plus the ChangeLog.
- **C2** — the probe's input format is confirmed at the tag: `host/limine.c` raw 2089-2091
  dispatch, raw 2035 print, raw 2002 substituted constant, and the same bytes across
  v12.9.4/5/6. On this host `limine --version` prints `Limine 12.9.4` and the landed gate's
  regex extracts `12.9.4`; the lane's own live receipt
  `.ufo/waves/round-93/after/live-c2.json` records `limine_version 12.9.4`,
  `limine_version_source "probe"` — consistent with the claim's stated live value. The
  freshness caveat is the host trigger in §6: the installed package is 12.9.4 while upstream
  `extra` already ships 12.9.6-1, so this host's live value is one upgrade away from flipping
  the era, and the host's own mirror and sync db still hide that upgrade.

---

## 8. Tooling

No tool was installed or upgraded by this seat: the task needed only `curl`, `sha256sum`,
`diff`, `grep`, `awk`/`sed` and read-only `pacman -Q*`/`checkupdates`, all already present.
`/home/vgpnk/.omp/agent/RULES.md` was read first; its update-safety gate was not engaged because
no install was required. (pacman transactions are paused host-wide in any case.)

## 9. Scratch hygiene

`/fast/scratch/hyaku/tsukuroi-r93/ScoutSource/` was created before the first command and
**deleted on exit** (this seat's own tree; nothing under `/tmp` was written by this seat; the
fixtures were read-only upstream fetches, no git/jj mutation was performed anywhere).

## Verdict

**Supports C1 and C2 on the freshness axis; falsifies one landed locator and one landed
prose claim; proposes two appended-row corrections (S385, S386) rather than a rewrite.**

- C1 supported: the v12.9.5 and v12.9.6 `common/lib/config.c` are **byte-identical**
  (`a940acae…`, `diff -u` empty — stronger than the claimed "identical in the cut region"), the
  cut is at raw 328-330 and the label-end NUL at 362-365 **in the v12.9.5 tag**, and upstream's
  `ChangeLog` (v12.9.5 raw 8-9; v12.9.6 raw 13-16, `Fixes #700`) dates the behaviour to 12.9.5.
  Receipts: `ScoutSource/pins/` + `ScoutSource/pin-table.tsv` + `ScoutSource/quotes.md`.
- C2 supported: the `limine --version` input format is pinned at the tag — `host/limine.c` raw
  2089-2091 dispatch, raw 2035 `puts("Limine " LIMINE_VERSION);`, raw 2002 substituted constant
  (identical bytes at v12.9.4/5/6); the host prints `Limine 12.9.4` and the lane's live receipt
  records `limine_version 12.9.4` / `limine_version_source "probe"`. Receipts:
  `ScoutSource/quotes.md`, `ScoutSource/pins/limine-v12.9.5-host_limine.c`.
- Falsified (landed working tree): **S384's locator** — the version print is at raw **2035**, not
  raw 2029 (raw 2029 is a blank line), and the `--version-only` print is at raw **2031**, outside
  the cited 2022-2026. Receipt: `ScoutSource/locator-discrepancy-S384.md`.
- Falsified (landed working tree): the r93 lesson's routed-3 disposition names an **appended row
  S385 that does not exist** while the tree does an in-place S377 edit; and the lesson's
  "3.17 … development banner" parenthetical is false (the two `3.17` occurrences are the `-b`/`-bb`
  deprecation note; the page has no dev banner and `docs.python.org/3.17/…` is HTTP 404).
  Receipts: `ScoutSource/s377-correction.md`, `ScoutSource/r92-rows-freshness.md`.
- Proposed corrections (append-only, never a rewrite): **S385** = S377 anchor correction,
  version-pinned URL `docs.python.org/3.15/using/cmdline.html`, `teaches` opening
  `supersedes S377 —`; **S386** = S384 locator correction. Full row texts in the two receipts.
- Boundary: **V2** is invalidated by the first upstream tag after v12.9.6 whose
  `common/lib/config.c` sha256 differs from `a940acae…` (the branch tip `v12.x` is still
  identical); **V3** by the first change to `host/limine.c`'s version print or to
  `@PACKAGE_VERSION@`'s shape; **the host trigger** is a `limine` package upgrade — installed
  12.9.4-1, upstream `extra` already at 12.9.6-1, while this host's sync db (2026-10-22) and its
  configured omarchy mirror still carry only 12.9.4-1, so the era flip can arrive unannounced.
  Receipt: `ScoutSource/dependency-boundary.md`.
