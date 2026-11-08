# Limine r94 — `auto` becomes the default, and the ten-digit enumeration closes

source: S386 (Limine v12.9.6 `common/lib/config.c`), S387 (Limine v12.9.6 ChangeLog), S388 (Limine v12.9.6 `host/limine.c`), all opened 2026-11-08; S382-S385 re-opened from the pinned copies; S385's missing rule-1 row is supplied in the round-94 lesson `## Gate`
verified-at: 2026-11-08 (freeze `HEAD` set in the wave receipts; live `limine --version` reads `12.9.4`)
recheck: re-open S386-S388 on any `limine` package update (cadence on-release, the V4 default and the not-word-char guard both live in these files); re-run `python3 tools/check-limine-pins.py --live` after an upgrade (the era flips with the binary, never with the flag)

Round 94. Three things the lane's USER guide did not hold in one place until this round: (a) the
gate's era-selection input is the installed binary by default, not a hand-typed `12.9.4`; (b) the two
v12.9.6 files the downgrade path depends on are byte-identical to their v12.9.5 counterparts; and
(c) the version refusal's 9-digit boundary has a live boundary member (`999,999,999` accepted) and
a ten-digit enumeration above it.

## `auto` by default (V4)

`tools/check-limine-pins.py --limine-version` defaults to `auto` since round 94 (was `12.9.4` in
r93 V3). `--live` therefore probes the installed bootloader unless an explicit `X.Y.Z` is passed;
the JSON records `limine_version` and `limine_version_source: probe`; a failed probe is rc 64 with
empty stdout — never a silent substitution of the packaged default (QUALITY 138). The battery's
`ERA-DEFAULT` family (omits the flag) still expects the `12.9.4` answers, because the host's real
`limine` answers `12.9.4` inside the sandbox; a gate whose default is a newer era answers `panic`
and fails. This is the user-guide requirement made executable: the seeded-gate for a FRESH install on
12.9.6 reads the era from the binary, whichever release is installed.

## The two era rules at v12.9.6 are byte-identical to v12.9.5

- `common/lib/config.c` at tag `v12.9.6` is byte-identical (sha256 `a940acae…`) to the v12.9.5 file
  (S382, pinned in round 93): the `create_menu_tree` cut (`if (p > config_addr) { *(p - 1) = '\0'; }`,
  raw 328-330) and the label-end NUL (raw 362-365) are the same bytes. The v12.9.5 tag's own cut is
  therefore the boundary and 12.9.6 adds nothing to it.
- `host/limine.c` at tag `v12.9.6` is byte-identical (sha256 `4da21c7c…`) to its v12.9.5 copy
  (S384): `--version` prints `"Limine " + LIMINE_VERSION` at raw 2035, `--version-only` prints the
  bare version at raw 2031. The probe's input format did not move.

## The rules follow to 12.9.6 only up to what upstream changed

The v12.9.6 ChangeLog (release 12.9.6, 2026-10-28) changes the visibility story in exactly one
sentence, quoted by S387 ("Document that global options must come before the first entry, as has been
the case since 4.0. A config whose first line is an entry has had no global options since 12.9.5,
whereas every option in it used to count as global. Fixes #700.") — a documentation sentence, not a
code change. The gate's `>= 12.9.5` rule is therefore unchanged at 12.9.6: the boundary is the v12.9.5
tag's code, and no code bytes after that tag alter the two clauses this battery certifies.

## Family map

| family | inputs | expected |
|---|---|---|
| REFUSAL-VERSIONS-10DIGIT | `1234567890.0.0`, `0.1234567890.0`, `0.0.1234567890`, `1234567890.1234567890.1234567890` (each exits 64 with empty stdout); the healthy `12.9.4` control inside the same family reads a verdict | `REFUSAL-VERSIONS-10DIGIT` passed 4/4 on the landed gate; a `<= 10` bound bends it to `unmet` with the family in `failed_families` |
| AUTO-PROBE-SHAPES | a fake `limine` printing `no version here`, then `Limine 12.9.6-rc1`, then `Limine 12.9.6` on stderr (exit 0) | refused rc 64, empty stdout; without the not-word-char guard the suffixed answer reads `12.9.6` and the family fails |
| ERA-DEFAULT (r93, unchanged) | omits `--limine-version` | the `12.9.4` answers, because the host's `limine` answers `12.9.4` in the sandbox; a newer-era default answers `panic` |

Limits. The probe is still not total: the r92 launcher residuals (argv via `/proc`, host fingerprint,
writable gate-copy parent, `/dev` writes) are recorded, not claimed; the stderr shape belongs to the
gate's selftest, not the family; a release-format change is a re-pin of S384.

## Gate

| row | URL opened | tier | located quote (≤25 words) |
|---|---|---|---|
| S386 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/common/lib/config.c` | A | "if (p > config_addr) { *(p - 1) = '\0'; }" (raw 328-330, `create_menu_tree()`) |
| S387 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/ChangeLog` | A | "A config whose first line is an entry has had no global options since 12.9.5." (12.9.6 Miscellaneous) |
| S388 | `https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.6/host/limine.c` | A | "puts(\"Limine \" LIMINE_VERSION);" (raw 2035; `--version-only` at raw 2031) |

Admitted: all three, `used-by corpus/knowledge/limine-auto-default-r94.md, corpus/lessons/round-94.md`.

Rejected: the host-stable 12.9.6 documentation pages (`https://man.archlinux.org/man/limine.8`,
HTTP 404 this round — not a source); the GitHub release-API JSON (a listing, not a document;
kept as a locator in the wave directory).

S385 note (r93 routed 2): the version-pinned Python docs supersession of S377 now carries its
rule-1 row in `corpus/lessons/round-94.md` `## Gate` (URL, 2026-11-08, located quote).
