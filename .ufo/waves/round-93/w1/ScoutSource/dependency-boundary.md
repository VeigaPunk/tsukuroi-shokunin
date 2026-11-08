# Dependency boundary — what invalidates V2 and V3, and the host trigger

## V2 — the `create_menu_tree()` cut (`common/lib/config.c`)

**Rule V2 encodes:** from 12.9.5 on, a config whose first line is an entry has no global options
visible; from 12.9.5 on, `config_get_value` reads only the text before the first entry.

**Pinned evidence (all byte-verified this round):**

| tag | `common/lib/config.c` sha256 | cut present? | mechanism |
|---|---|---|---|
| v12.9.4 | `aafc9c410a250efc9674e3c93e839d32ae2731ba2ca60bb7f5edd7ad5828fba8` | no | `init_config()` cuts with `c[-1] = 0` after `config_get_entry(&s, 0)` (raw 642-651); no `create_menu_tree()` exists in this file |
| v12.9.5 | `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60` | yes | `create_menu_tree()` raw 298-407; cut raw 328-330; label-end NUL raw 362-365 |
| v12.9.6 | `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60` | yes | **byte-identical to v12.9.5** (`diff -u` empty) |

The v12.9.5 ChangeLog (raw 8-9) dates the in-place parse to 12.9.5; the v12.9.6 ChangeLog
(raw 13-16) states upstream's own reading: `A config whose first line is an entry has had no
global options since 12.9.5`. So the V2 era split at `(12, 9, 5)` is sourced, not assumed, and
the battery's claim that the 12.9.5 and 12.9.6 files are identical in the cut region is
**stronger than claimed: the whole files are byte-identical** (same sha256 `a940acae…`).

**What would invalidate V2:** any upstream release **after v12.9.6** that changes
`common/lib/config.c` — specifically `create_menu_tree()` (raw 298-407) or the cut at 328-330 /
label-end NUL at 362-365 — or a v12.9.7+ ChangeLog entry that changes the global-option rule
upstream states at 12.9.6 (raw 13-16). Concretely: the first tag whose
`common/lib/config.c` sha256 differs from `a940acae…`. Note that the era split would also move
if upstream ever made global options after the first entry work again (the issue #700 /
PR #702 outcome was documentation-only: PR #702 `docs: clarify positioning of global options`,
merged 2026-10-27T22:41:28Z, changed `CONFIG.md` — v12.9.5 `CONFIG.md` raw 76 says
`Global options can appear anywhere in the file`, v12.9.6 `CONFIG.md` raw 76 says
`Global options must come before the first menu entry`).

## V3 — the `limine --version` output format

**Rule V3 encodes:** `--limine-version auto` runs `limine --version` read-only and takes the
first parsable `X.Y.Z` from it, then selects the era from it.

**Pinned evidence:** the print is in **`host/limine.c`** (not `common/lib/misc.c`, which contains
zero occurrences of `Limine `, `--version` or `LIMINE_VERSION`):

- raw 2002 `#define LIMINE_VERSION "%VERSION%"` — substituted at build time
  (`GNUmakefile.in` raw 170: `s/%VERSION%/@PACKAGE_VERSION@/g`), so the printed number is the
  **package** version;
- raw 2089-2091 dispatch: `strcmp(argv[1], "version") == 0 || strcmp(argv[1], "--version") == 0`
  → `return version(argc - 1, &argv[1]);`;
- raw 2035 `puts("Limine " LIMINE_VERSION);` — the first stdout line of `--version`;
- raw 2031 `puts(LIMINE_VERSION);` — the `--version-only` form, **bare number, no `Limine ` prefix**.

**What would invalidate V3:** an upstream release **after v12.9.6** that changes
`host/limine.c`'s version print — dropping the `Limine ` prefix, moving the print to stderr,
or changing the `--version`/`version` dispatch — **or** a distro packaging change that puts a
non-`X.Y.Z` string in `@PACKAGE_VERSION@` (the gate's regex
`(?i)\blimine\s+v?(\d+\.\d+\.\d+)\b` needs the literal word `limine` before the number, so a
bare `12.9.6` first line — the `--version-only` shape — would **not** match; and a version like
`12.9.6.r1.gabc` would silently parse as `12.9.6`). `host/limine.c` is byte-identical across
v12.9.4, v12.9.5 and v12.9.6 (all `4da21c7c…`), so the format is currently stable across the
era boundary.

## The host trigger that must re-run the battery

**A `limine` package upgrade on this host.** The probe's input is the *installed* bootloader
version, so the trigger is the installed package changing, not a source re-read.

- installed now: `limine 12.9.4-1` (`pacman -Qi limine`), whose `limine --version` first stdout
  line is `Limine 12.9.4` (measured);
- Arch `extra` upstream now ships `limine 12.9.6-1` (archlinux.org package JSON,
  `last_update 2026-10-28T08:00:46Z`; `geo.mirror.pkgbuild.com/extra/os/x86_64/` carries
  `limine-12.9.6-1-x86_64.pkg.tar.zst`);
- so the **next `pacman -Syu` that pulls limine 12.9.6-1 flips the probe's answer from 12.9.4
  to 12.9.6**, which flips the selected era from pre-12.9.5 to 12.9.5+, and every era- and
  refusal-sensitive family in the battery must be re-measured.

Two freshness notes on that trigger, both measured:

1. **The host's own package database is stale.** `/var/lib/pacman/sync/extra.db` has mtime
   2026-10-22 01:40 -0300, so `pacman -Si limine` reports `12.9.4-1` and `checkupdates` lists
   6 pending packages, **none of them limine** — the pending 12.9.6 upgrade is invisible to the
   host's current tooling. `checkupdates` against the live upstream (archlinux.org JSON) shows
   12.9.6 exists. So the era flip can arrive without the host's own update check naming it.
2. **A mirror skew exists.** `mirror.rackspace.com/archlinux/extra/os/x86_64/` still lists only
   `limine-12.9.4-1`, while `geo.mirror.pkgbuild.com` lists `limine-12.9.6-1`. Any host reading
   a skewed mirror sees the old version.

Second trigger, independent of the package: **`/boot/limine.conf` changing** (the live run's
input). It is root-only on this host (`ls /boot/limine.conf` → `Permission denied`; not
elevated by this seat), so the live receipt in `.ufo/waves/round-93/after/live-c2.json`
(`limine_version 12.9.4`, `limine_version_source "probe"`, two `LP-MISMATCH` findings at lines
30 and 38) is a point-in-time reading of a file this seat cannot read.

## Branch-tip state at the time of this check (2026-11-08)

The upstream default branch is **`v12.x`** (not `main`; `main` returns HTTP 404). At the tip of
`v12.x` (fetched 2026-11-08 06:21Z):

| file on `v12.x` | sha256 | vs the pinned tag |
|---|---|---|
| `common/lib/config.c` | `a940acae3a0a9c4d1c716f8132f688c4bcdced2b092769bc1becad466e944e60` | **identical to v12.9.5 and v12.9.6** |
| `host/limine.c` | `4da21c7cceae238075612643b845cb63e06cc184977e950d5e6374329bc31ec0` | **identical to v12.9.4/5/6** |
| `ChangeLog` | `ab280b451ee6f56bad5684d44eda5c94bf43d2c17e9e651b8e84b433584d03ba` | **identical to v12.9.6**; its head is still `*** Release 12.9.6 ***` — no unreleased section above it |

So neither V2's cut nor V3's print has moved on the branch tip: the boundary is "the next tag
whose `common/lib/config.c` or `host/limine.c` sha256 changes", and today that has not happened.
The upstream releases list ends at **v12.9.6** (published 2026-10-27T23:16:30Z); tags in order:
v12.9.6 `89a9512c623a`, v12.9.5 `55a93085435a`, v12.9.4 `8ad14430bc9f`, v12.9.3 `e3aa138d383c`,
v12.9.2 `69792f200e90`, v12.9.1 `c82c3708b330`.
