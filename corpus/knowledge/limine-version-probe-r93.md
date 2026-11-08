# Limine r93 — the 12.9.5 tag itself, and where `limine --version`'s answer comes from

source: S382 (Limine v12.9.5 `common/lib/config.c`), S383 (Limine v12.9.5 ChangeLog), S384 (Limine v12.9.5 `host/limine.c`), all opened 2026-11-08; S379/S380 (v12.9.6 files) re-opened from the pinned copies
recheck: re-open S382-S384 on any `limine` package update (on-release cadence: the V2 boundary and the V3 probe format both live in these three files); re-run `python3 tools/check-limine-pins.py --live --limine-version auto` after an upgrade
verified-at: 2026-11-08

Round 93. Two facts the lane did not hold: (a) the r92 boundary evidence pinned v12.9.6, so "the cut
starts at 12.9.5" was an inference from the ChangeLog and the equality of the two files; the v12.9.5
tag itself is now opened and byte-pinned. (b) The gate's r92 stance was that it never reads the host
version; round 93 adds an explicit probe (`--limine-version auto`) and this entry records what that
probe's input actually is.

## VP — the boundary file and the probe source

VP1. **The v12.9.5 tag carries the cut.** `common/lib/config.c` at tag `v12.9.5`, raw 328-330:
`if (p > config_addr) { *(p - 1) = '\0'; }` inside `create_menu_tree()`; the file's sha256 is
`a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60`, identical to the v12.9.6 file the
r92 entry pinned (S379) — the whole file, `diff` empty (ScoutSource, round 93) — so the two releases are
one rule and the boundary is 12.9.5, not 12.9.6.

VP2. **The release notes date the change to 12.9.5, not later.** v12.9.5 ChangeLog raw 8-9: *"Parse
the config in linear time. Configs with thousands of entries were slow to load."* This is the entry
the r92 gate's `>= 12.9.5` split rests on; the v12.9.6 ChangeLog sentence S380 quotes is the
follow-up that states the visibility consequence.

VP3. **`limine --version` prints a first line of the form `Limine <X.Y.Z>`.** `host/limine.c` raw
2089-2091 dispatches `version`/`--version` to `version()`; raw 2035 is `puts("Limine " LIMINE_VERSION);`
followed by copyright and licence lines (raw 2036-2038), and `--version-only` (raw 2030-2032, print at
2031) prints the bare `LIMINE_VERSION`. The host's answer this round is `Limine 12.9.4` (first line of
`limine --version`, rc 0), so the gate's V3 probe reads the first `X.Y.Z` of that output and records
it with `limine_version_source: "probe"`.

VP4. **The live gate under auto selects the host's era.** `python3 tools/check-limine-pins.py --live
--limine-version auto` (sudo, read-only; `/boot` digest identical before and after) reads
`limine_version 12.9.4`, `visibility_era pre-12.9.5`, `secure_boot_enforced false` (efivar), rc 1, the
two operator-owned pins at `/boot/limine.conf` lines 30 and 38 `LP-MISMATCH`. The era choice is the
installed package's, not a hand-typed default.

## What the r93 families certify, and what they do not

| family | input the case builds | expected gate answer |
|---|---|---|
| ERA-EXACT-125 | `--limine-version 12.9.5`, line 1 an entry, `hash_mismatch_panic: no` after the body | `panic` (era B: key invisible) — a strict `>` split returns `prompt` |
| ERA-B-FIRST-BODY | 12.9.6, line 1 the label, line 2 the key | `panic` — a cut that lands one line late returns `prompt` |
| ERA-B-U1 | 12.9.6, header then an efi entry whose image line has no URI shape | `unverified_image_lines: [image line]` — a pre-cut-only U1 returns `[]` |
| REFUSAL-VERSIONS | ten values outside `X.Y.Z`, each passed to `--limine-version` | rc 64, empty stdout, no verdict |
| AUTO-ERA-A / AUTO-ERA-B | a fake `limine` on the case PATH answering 12.9.4 / 12.9.6, `--limine-version auto` | era A (`prompt`) / era B (`panic`), `limine_version` = the fake's answer, source `probe` |
| AUTO-PROBE-FAIL | a fake `limine` exiting 1, `--limine-version auto` | rc 64, empty stdout |

Limits. The probe takes the first `X.Y.Z` in stdout, so a pre-release answer (`12.9.6-rc1`) reads as
`12.9.6` [inference from the regex, not measured on a release binary]; a two-component answer
(`12.9`) is a probe failure, not a guess. The 5 s timeout is shorter than the battery's 20 s per-case
timeout by design. The probe remains opt-in: `--limine-version` still defaults to `12.9.4`, so a host
whose package moved is answered with the new era only when the flag or a future default says so.
Era-B U1 is a whole-file reporting contract; the family certifies the list's content, not any boot
consequence (U1 changes no pin verdict).

## Gate

Opened 2026-11-08 by the L1 (URL, access date, located quote; ≤25 words each):

| row | URL opened | tier | located quote | verdict |
|---|---|---|---|---|
| S382 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/common/lib/config.c` | A | "if (p > config_addr) { *(p - 1) = '\0'; }" (raw 328-330) | admit — the v12.9.5 tag's own cut |
| S383 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/ChangeLog` | A | "Parse the config in linear time. Configs with thousands of entries were slow to load." (raw 8-9) | admit — dates the change to 12.9.5 |
| S384 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.5/host/limine.c` | A | "puts(\"Limine \" LIMINE_VERSION);" (raw 2035; `--version` dispatch raw 2089-2091) | admit — the probe's input format |
| reject | `https://api.github.com/.../git/trees/v12.9.5?recursive=1` | C | (a listing, not a document) | reject — used to locate S384, not cited as support |
| reject | `common/lib/misc.c` at v12.9.5 | C | (no version print in it) | reject — the print lives in `host/limine.c`; the file is pinned as a negative locator |

The three rows are new; no status or `recheck` change lands this round. Pinned bytes and their
sha256 live in `.ufo/waves/round-93/before/src/` (`SHA256SUMS`), fetched 2026-11-08.
