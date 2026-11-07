# ScoutDrift — upstream drift of the r90 rule set (Limine v12.9.4 → v12.9.6)

Seat: SCOUT (read-only). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Lane revision measured (`git rev-parse master`): `ce89df93e5f576c5c236d4547299e9ea954e8853`
(candidate commit; freeze commit `6511437e7d86d3f1e7e39a45df91ade1d8293612`).
**Note:** while this seat was running, other seats landed C1/C2 on `master` and the tip moved to
`b380483e2a1d8edc97556fdd021794f619b6e1a6` (`58723499` C1 measured, `b380483e` C2 entry). That
advance is other seats' work, not mine; every measurement below was taken against
`ce89df93`, which is the r90 candidate the round-90 declaration is written against.
Host Limine: `limine 12.9.4-1` (matches the pinned r90 sources).
Receipts: `.ufo/waves/round-90/w1/ScoutDrift/` (`drift-evidence.txt`, `upstream-tags.txt`,
`arch-package.txt`, `harness/`).
No lane file was edited. No host write of any kind: no `pacman` transaction, no `sudo`, no
`/boot` access; every upstream clone and every compiled harness lived in
`/fast/scratch/hyaku/tsukuroi-r90/ScoutDrift` and was removed on exit.
Tools used, all preinstalled, **no installs performed**: git 2.56.0, gcc 16.2.1, python3 3.14.8.

## 1. Upstream state

```
$ git ls-remote --symref https://github.com/limine-bootloader/limine.git HEAD
ref: refs/heads/v12.x	HEAD
89a9512c623a4779cc73e3869383876d54264b28	HEAD

$ git ls-remote --heads https://github.com/limine-bootloader/limine.git v12.x trunk
31e8865c9545c337982f05415c30a8bc80055d07	refs/heads/trunk
89a9512c623a4779cc73e3869383876d54264b28	refs/heads/v12.x

$ git ls-remote --tags ... | sort -V | tail -8
12.9.0 12.9.1 12.9.2 12.9.3 12.9.4 12.9.5 12.9.6
```

- Tags newer than the pinned **v12.9.4** (commit `8ad14430bc9f2c24679cda558981ef53e6e3b18c`,
  2026-10-19): **v12.9.5** (`55a93085435aa1b8f91054df3794b2a43fb7984a`, 2026-10-27) and
  **v12.9.6** (`89a9512c623a4779cc73e3869383876d54264b28`, 2026-10-28).
- The repo's **default branch is `v12.x`**, whose tip is exactly the v12.9.6 tag commit
  `89a9512` — so "default branch" and "newest release tag" are the same tree here.
- `trunk` (`31e8865`) is **not** a descendant of v12.9.6: it diverged at
  `8c2ffdf9` ("docs/ChangeLog: Add notes for v12.5.0"), 838 commits ahead / 804 behind.
  Trunk is unreleased; I treat it as forward-risk only (see §4).
- **All seven r90-clause files are byte-identical between v12.9.5 and v12.9.6** (sha256
  equal for each). Every upstream change below therefore landed in **v12.9.5**.
- Arch: the local sync DB (`/var/lib/pacman/sync/extra.db`, mtime **Oct 22 01:40**) is stale
  and still lists 12.9.4-1, but the upstream Arch PKGBUILD on gitlab now says
  `pkgver=12.9.6` / `pkgrel=1`, and `archlinux.org/packages/extra/x86_64/limine/` shows
  **limine 12.9.6-1**. So `pacman -Si limine` under-reports: a `pacman -Sy` would reveal
  12.9.6-1 available. (Not installed — pacman transactions are paused host-wide.)

## 2. Per-file table: v12.9.4 → v12.9.6

| file | changed? | r90 clause touched | what changed, and whether an r90 rule moves |
|---|---|---|---|
| `common/lib/uri.c` | **CHANGED** (56 lines) | R4, R2/R3 | R4 dispatch block (`349-366`→`375-392`) **byte-identical**. R2/R3 `uri_resolve` (`32-104`→`33-105`) **byte-identical**. `URI_ERROR` macro **identical**. Changes: `if (resource == NULL) URI_ERROR("No resource specified…")` **deleted** (12.9.4 `340`); `uri_guid_dispatch` refactored into `volume_by_guid_str` + `connect_all()` (UEFI Fast Boot: connect all disks before giving up on a volume); `uri_fslabel_dispatch`/`uri_hdd_dispatch`/`uri_odd_dispatch` retry after `connect_all()`. **R4 rule text does not move**; the deleted branch was dead code (§3-D). The `connect_all()` retry changes *which volumes resolve*, which is upstream R4/R5 resolution behaviour but is outside the r90 modelled scope (r90 only models `boot()` with empty root as resolvable). |
| `common/lib/config.c` | **CHANGED** (427 lines) | **R1**, R9 | **R1's strip loop is rewritten** (`528-551`→`551-580`): the old in-place loop becomes a single-pass copy that drops every CR and trims leading/trailing blanks per line. Behaviour differs: see §3-A. R1's `config_get_value` (`778-818`→`727-767`) is **byte-identical**. R9's entry model is rewritten: `config_get_entry`/`config_get_entry_name`/`is_child` **deleted**, replaced by a single `create_menu_tree()` (`298-…`) that NUL-terminates inside `config_addr`; the r90 R9 "entry body runs to the next `/` line" rule is **unchanged in effect** but its source citation moves from `686-720` to `create_menu_tree`. |
| `common/menu.c` | **CHANGED** (159 lines) | R6, R9, R10 | R6/R10 block `hash_mismatch_panic`+`measured_boot` (`1711-1730`→`1789-1808`) **byte-identical**. R9 protocol dispatch (`2429-2468`→`2498-2537`) **byte-identical**. Other changes are UI (`display_width`, editor, `efi_boot_entry` GUID) — outside r90 clauses. |
| `common/protos/chainload.c` | **CHANGED** (29 lines) | R9 | The `PATH`→`IMAGE_PATH`→`uri_open`→panic block (`414-437`→`429-452`) is **byte-identical**. Elsewhere: EBR partition handling (`p->backing_dev->ebr_part`→`p->extended`), and the EFI device path is now built with a `\` root prefix. Neither touches an r90 rule. |
| `common/lib/panic.s2.c` | **CHANGED** (8 lines) | R10 | `measured_boot`→`allow_menu=false` (`26-28`) **byte-identical**. Added: under UEFI with the fallback terminal, `print("\e[2J\e[H")` before the panic banner (cosmetic). `menu(false)` `78`→`86`, `"System halted."` `98`→`106` — line numbers move, **rule text unchanged**. |
| `common/lib/gterm.c` | **CHANGED** (10 lines) | R6 | Only `colour_blend()` alpha arithmetic (`256`→`255` divisor) changes. The two `uri_open_optional` call sites (wallpaper `625`→`627`, term_font `706`→`708`) are **unchanged in behaviour** — R6's "optional resource ⇒ skip" is unaffected. |
| `common/lib/tpm.c` | **CHANGED** (24 lines) | (C2) | `tpm_present()` (`113-115`) **byte-identical** ⇒ C2's TPM answer is stable. Added: `EFI_VOLUME_FULL` is now counted as measured with one warning instead of a prompt. Changed: the TPM measurement path/hash split now uses `strrchr('#')` (last `#`) instead of `strchr` (first `#`), aligning with `uri.c`. |

## 3. Two behavioural divergences, proven at C level

I compiled the **verbatim** upstream functions (not paraphrases) and drove them with upstream's
own buffer layout (`config_size = f->size + 2`; `config_addr[config_size-2]='\n'`).
Harness sources are in `harness/`; full output in `drift-evidence.txt`.

### A. R1's strip loop: v12.9.4 vs v12.9.6 differ on CRLF lines — **and the r90 model already matches v12.9.6, not v12.9.4**

`12.9.4 raw 528-551` vs `12.9.6 raw 551-580`, verbatim, 300 000 random buffers:

```
TRIALS 300000  DIFF 11182  class=12.9.4-keeps-trailing-blanks-before-CR 11182  class=other 0
```

The **only** difference between the two loops is this: v12.9.4's in-place loop removes a
trailing blank run only when the run is *immediately* followed by `'\n'`; a `'\r'` sitting
between the blanks and the newline blocks that removal. v12.9.6's single pass removes every
CR first, then trims trailing blanks, so blanks before a CRLF **are** removed.

Measured on the key-line **value** (what r90 actually compares), 200 000 trials:

```
  LF  lines : 100383   model!=12.9.4 : 0 (0.000%)   model!=12.9.6 : 0 (0.000%)
  CRLF lines:  99617   model!=12.9.4 : 74780 (75.068%)   model!=12.9.6 : 0 (0.000%)
```

The r90 R1 model (`raw.replace("\r","").strip(" \t")` per physical line — battery line 138,
gate `split_key` line 63) agrees with **v12.9.6 on 100 % of lines** and with **v12.9.4 on 0 % of
CRLF lines** that carry trailing blanks.

Consequence for the r90 rule set as frozen: the r90 model is *already* v12.9.6-shaped for R1.
On the r90 battery's own `WHITESPACE-CRLF` family — the one family that draws CRLF and a
trailing-blank pin line — the model and the gate report the pin as `OK`/`LP-MISMATCH`, and so
does upstream v12.9.6, while upstream **v12.9.4** would compute a 131-character hash and hit
`URI_ERROR("Blake2b hash must be 128 characters long")` → panic. On the real battery fixture
bytes:

```
upstream v12.9.4 : PATH value hash-length = 131  => URI_ERROR 'hash must be 128 characters long' -> PANIC
upstream v12.9.6 : PATH value hash-length = 128  => hash OK (LP-MISMATCH/OK)
gate/battery model: PATH value hash-length = 128  => hash OK (LP-MISMATCH/OK)
```

So R1's frozen *text* ("remove EVERY CR anywhere in the file and the leading/trailing blanks of
each line") is a faithful description of **v12.9.6**, and is **not** a faithful description of
the pinned v12.9.4 for CRLF lines with trailing blanks. The host's own `/boot/limine.conf`
(per the r90 host receipt) is LF, so the divergence does not affect the host today; but the
r90 *rule text* and the r90 *pin* disagree on that corner. **This is a re-pin question, not a
battery change**: re-pinning to v12.9.6 would make the rule text and the pin agree.

### B. R6/R8/R10 global-option scope changed between v12.9.4 and v12.9.6

Upstream reads `hash_mismatch_panic` and `measured_boot` with `config_get_value(NULL, 0, KEY)`,
i.e. over the whole `config_addr`. What "the whole file" *means* changed:

| config shape | r90 model (whole file) | upstream v12.9.4 | upstream v12.9.6 |
|---|---|---|---|
| A) global option before the first entry | `no` | `no` | `no` — same |
| B) **first line is an entry**, option inside that entry | `no` | `no` | **(absent)** — **changed** |
| C) global line first, option only inside an entry | `no` | **(absent)** | **(absent)** — same |

```
B) FIRST LINE IS an entry; the option sits inside that entry
    r90 model (whole file)      : no
    upstream v12.9.4 (global)   : no
    upstream v12.9.6 (global)   : (absent)
    model==12.9.4: YES   model==12.9.6: NO    upstream12.9.4==12.9.6: NO
C) option ONLY inside an entry (a global line precedes it)
    r90 model (whole file)      : no
    upstream v12.9.4 (global)   : (absent)
    upstream v12.9.6 (global)   : (absent)
    model==12.9.4: NO   model==12.9.6: NO    upstream12.9.4==12.9.6: YES
```

Upstream's own changelog for v12.9.6 states the change: *"Document that global options must
come before the first entry, as has been the case since 4.0. A config whose first line is an
entry has had no global options since 12.9.5, whereas every option in it used to count as
global."* `CONFIG.md` changed accordingly (raw `76-77`): *"Global options can appear anywhere in
the file"* → *"Global options must come before the first menu entry. Any that come after it are
part of an entry, where they are ignored."*

So the r90 model ("first key line **in the whole file**", battery `r1_panic` line 216, gate
`check()` line 138) is:
- **v12.9.6-shaped** on shape B (upstream 12.9.6 ignores an in-entry option that v12.9.4
  honoured) — wait, no: on B the model says `no` (found), 12.9.4 says `no` (found), 12.9.6 says
  absent. So the model matches **12.9.4**, not 12.9.6, on B.
- **neither** upstream version's shape on C: both upstreams ignore an in-entry option when a
  global line precedes it, because v12.9.4 truncates `config_addr` at the first entry
  (byte-level: `config_addr` after init_config = `"timeout:_5"`), and v12.9.6 NULs the entry
  label line inside `config_addr`.

The r90 model's shape-C behaviour is thus a pre-existing divergence from the pinned v12.9.4, and
shape B is a divergence that **appears on upgrade to v12.9.6**. Both are *outside* the r90
battery's exercised shapes (every r90 family that puts an option inside an entry — e.g.
`fam_measured_in_entry` line 1210, `fam_panic_first` line 506, `fam_measured_first` line 1184
— does so *after* a global `timeout:` line, i.e. shape C) but they matter for the rule text's
accuracy. Note this is a *documentation/rule-text* drift, not a battery defect: the battery's
own expected values are computed by the same whole-file model the gate implements, so battery
and gate agree with each other and the frozen battery stays self-consistent (73/73 met, §5).

### C. R9's entry-body rule survives the rewrite, but its citation does not

v12.9.4's `config_get_entry()` and v12.9.6's `create_menu_tree()` compute the body by
different means (copy of a byte range vs. an in-place NUL-terminated slice), yet both end the
body at the next `/`-at-line-start, so r90 R9's *"an entry's body is the physical lines after
it up to the next entry line"* still holds. What changed is where a reader must look:
`config.c raw 686-720` (`config_get_entry`) → `config.c raw 298-…` (`create_menu_tree`).
The R9 *protocol dispatch* and *chainload image* blocks are byte-identical, so R9's
"first `path` key line, else first `image_path`" rule is unaffected.

### D. R4's deleted `URI_ERROR("No resource specified for URI")` branch was dead code

Driving upstream v12.9.4's verbatim `uri_resolve` with a valid 128-hex hash:

```
  uri_resolve("boot():/x#H") -> true   resource="boot"
  uri_resolve("():/x#H")     -> true   resource=""
  uri_resolve("bogus:/x#H")  -> false  resource=(NULL)
  => successful resolves: 9 ; resource==NULL among them: 0  => branch UNREACHABLE (dead code) in v12.9.4
```

`uri_resolve` only returns true when it has set `*resource`, so `resource == NULL` could never
be observed at the deleted branch. Its removal in v12.9.6 changes no r90 answer. Note that
`resource == ""` (empty name) *is* reachable and still reaches the R4 `else` branch
(`URI_ERROR("Resource \`%s\` not valid.")`) → LP-BAD-RESOURCE, in both versions.

### E. C2's two anchors are stable

`common/lib/tpm.c` `tpm_present()` is **byte-identical** at raw `113-115` in v12.9.4 and
v12.9.6 (`return tcg2 != NULL || cc != NULL;`), so C2's TPM-interface answer and R10's
`--tpm-present` modelling are unaffected by the upgrade. `uri_boot_dispatch` (`220-242` →
`251-273`) and `parse_bios_partition` (`107-…` → `108-…`) are behaviourally identical, so C2's
"how `boot(N)` finds a volume" and "which name would denote this host's ESP" hold; note the
v12.9.5 addition that `guid()`/`uuid()`/`fslabel()` retry after `connect_all()` (UEFI Fast
Boot connecting all disks), which can make a volume resolve where v12.9.4 would not — the one
C2-relevant behavioural change I found upstream.

## 4. Forward risk: `trunk` breaks R3/R5 outright

`trunk` (`31e8865`, unreleased) rewrites hashing: `uri_resolve` now accepts **64 / 128 / 256**
hex characters (`hash_type_from_hex_length`) instead of exactly 128, and `common/crypt/hash.{c,h}`
plus `blake3.c` add BLAKE3 and a long-digest algorithm. r90's **R3** ("exactly 128 characters")
and **R5** ("BLAKE2b-512 of the file's raw bytes") are both invalidated by that work. `trunk`
also carries the "global options must precede the first entry" documentation change. No r90
pin should target `trunk`; it is a v-next re-design, not a v12.9.6 bump.

## 5. Does the frozen r90 battery still pass? (context, not my claim)

```
$ python3 tools/limine-pin-battery-r90.py --gate tools/check-limine-pins.py --runs 1 --work $S/battery
families_passed 73/73 verdict met failed -
battery rc=0
```

The frozen battery and gate are mutually consistent (73/73) at the measured lane revision —
upstream drift does not by itself break them, because the battery's expectations are computed
from the same whole-file model the gate implements. What upstream drift changes is the
**accuracy of the r90 rule text relative to the pinned sources** (§3-A, §3-B) and the
**validity of the pinned raw-line citations** (§2, §6).

## 6. Re-pin verdict: is a re-pin needed on upgrade?

**Yes — a re-pin is needed the moment the host moves off v12.9.4, and it is mechanical except
for one wording change.** Concretely, if/when Arch delivers limine 12.9.6-1 (PKGBUILD already
says `pkgver=12.9.6`; archlinux.org lists 12.9.6-1) the r90 pin set must be re-fetched at
v12.9.6 and the docstring's raw-line citations re-pointed. Because the seven clause files are
byte-identical between v12.9.5 and v12.9.6, **v12.9.6 is the correct single re-pin target**;
v12.9.5 would pin the same bytes but leave the changelog one release behind.

Citation moves required (v12.9.4 → v12.9.6 raw):

| r90 citation | v12.9.4 | v12.9.6 | status |
|---|---|---|---|
| R1 strip loop | 528 | 551 | moved |
| R1 `config_get_value` | 778 | 727 | moved (text identical) |
| R9 entry body | 686 | 298 (`create_menu_tree`) | moved + symbol changed |
| R2 `uri_resolve` | 32 | 33 | moved (text identical) |
| R3 hash length | 89 | 90 | moved (text identical) |
| R4 resource dispatch | 349 | 375 | moved (text identical) |
| R4 "not valid" error | 364 | 390 | moved |
| R4 "No resource specified" error | 340 | — | **deleted (dead code)** |
| R6 `URI_ERROR` macro | 21 | 22 | moved (text identical) |
| R6 `uri_hash_mismatch` | 301 | 332 | moved (text identical) |
| R6 `uri_open_optional` | 696 | 722 | moved |
| R6 `hash_mismatch_panic` (menu.c) | 1711 | 1789 | moved (text identical) |
| R10 `measured_boot` (menu.c) | 1720 | 1798 | moved (text identical) |
| R10 `tpm_present()` call (menu.c) | 1726 | 1804 | moved |
| R9 protocol dispatch (menu.c) | 2429 | 2498 | moved (text identical) |
| R9 chainload `PATH` | 415 | 430 | moved (text identical) |
| R9 chainload panic | 435 | 450 | moved (text identical) |
| R10 `measured_boot`→`allow_menu` (panic.s2.c) | 26 | 26 | **same** |
| R10 `menu(false)` (panic.s2.c) | 78 | 86 | moved |
| R10 `"System halted."` (panic.s2.c) | 98 | 106 | moved |
| R6 gterm wallpaper caller | 625 | 627 | moved |
| R6 gterm term_font caller | 706 | 708 | moved |
| C2 `tpm_present()` (tpm.c) | 113 | 113 | **same** |

**The one substantive wording change** the upgrade forces is in R1: the frozen sentence
*"common/lib/config.c raw 527-551 remove EVERY CR anywhere in the file and the leading/trailing
blanks of each line"* is not what v12.9.4 does to a CRLF line with trailing blanks (§3-A).
Re-pinning at v12.9.6 makes the sentence true of the pin. If the lane instead wants to keep
describing v12.9.4 exactly, R1 must gain the qualifier "…and trailing blanks are removed only
when the line ends with LF", and the battery's `WHITESPACE-CRLF` family expectation would
then be describing v12.9.6, not v12.9.4. Either way the pin and the rule text must agree; today
they do not.

Second, smaller: R6/R8/R10's *"the FIRST … key line in the whole file"* describes v12.9.4 and
not v12.9.6 (upstream 12.9.6 requires global options to precede the first entry). A re-pin at
v12.9.6 should either say "before the first entry" or acknowledge the divergence.

Neither change alters the frozen battery's 73 families or their expected values, so this is
**not** a battery re-scope; it is a pin/rule-text refresh plus two clause sentences.

## 7. What I did not do / open items

- I did not touch the lane, the battery, the gate, the pin set, or `SCORECARD.md`.
- `/boot/limine.conf` is unreadable without privilege (permission denied); the r90 host receipt
  is my source for host facts, and it shows the host conf is LF, so §3-A does not affect the host
  today. A read-only command the L1 could run to confirm CRLF-ness of the live conf:
  `sudo -n grep -c $'\r' /boot/limine.conf` (rc 0 = no CR).
- `common/lib/tpm.c` is **not** in the r90 pin set (`.ufo/waves/round-90/before/src/` holds six
  files: config.c, gterm.c, panic.s2.c, uri.c, menu.c, chainload.c). C2's TPM answer therefore
  rests on an unpinned source. Worth pinning `tpm.c` (v12.9.6 sha256
  `c91734237cb2583f33d8beddf9fc0bd87392cc5c684f8a51c79fe367ac127898`) if C2 is to cite it.
- `CONFIG.md` is cited by r90 R2/R5/R6 but is likewise unpinned at r90 (it is pinned at r87 as
  `limine-v12.9.4-CONFIG.md`). Its global-options paragraph changes between the two versions.
- `trunk` is unreleased and diverged; I did not build or boot it.
