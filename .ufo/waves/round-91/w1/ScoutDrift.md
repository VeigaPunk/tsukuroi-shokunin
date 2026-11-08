# ScoutDrift — upstream drift of the r91 rule set (Limine v12.9.4 → newest upstream)

Seat: ScoutDrift (scout, read-only). Lane revision measured at the start of this seat:
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` → **b516d6ae13ec0bba3ef89589ac1cac86f73a9632**
(pre-round tip 40efa4ea2862ab39da02430cada68f6dff230e86; freeze commit d3b0987d68364ccf8b781a755cbcd9563f939468).
By the end of the wave the lane tip had moved to `2d7e09e101996cc1ac5836c6d635f3f608453ac5` (other seats committed);
this seat made **no** commit, so the drift analysis is against the same tree it read — the frozen battery
`sha256 655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9` and the six pinned v12.9.4 sources were
verified unchanged at both revisions (see §0).

## 0. Method and provenance

Upstream clones (read-only, in scratch, deleted at exit):

```
$ git ls-remote --tags https://github.com/limine-bootloader/limine.git | grep -v '\^{}' \
    | awk '{print $2}' | sed 's|refs/tags/||' | grep -E '^v[0-9]+\.[0-9]+\.[0-9]+$' | sort -V | tail -6
v12.9.1
v12.9.2
v12.9.3
v12.9.4
v12.9.5
v12.9.6
```

Tags newer than v12.9.4: **v12.9.5 (2026-10-27) and v12.9.6 (2026-10-28)**. Newest release tag = **v12.9.6**,
commit `89a9512c623a4779cc73e3869383876d54264b28`. The default branch HEAD is the *same* commit
(`git ls-remote … HEAD` → `89a9512c623a4779cc73e3869383876d54264b28`), so **the newest upstream tree is exactly tag v12.9.6** —
there is no unreleased drift beyond the tag.

```
$ git -C <clone v12.9.4> rev-parse HEAD   → 8ad14430bc9f2c24679cda558981ef53e6e3b18c
$ git -C <clone v12.9.5> rev-parse HEAD   → 55a93085435aa1b8f91054df3794b2a43fb7984a
$ git -C <clone v12.9.6> rev-parse HEAD   → 89a9512c623a4779cc73e3869383876d54264b28
```

**The r91 pin is byte-exact and still valid for v12.9.4** (re-verified here, independently of `cmp-pins.txt`):

```
$ cd .ufo/waves/round-91/before/src && sha256sum -c SHA256SUMS
limine-v12.9.4-common_lib_config.c: OK
limine-v12.9.4-common_lib_gterm.c: OK
limine-v12.9.4-common_lib_panic.s2.c: OK
limine-v12.9.4-common_lib_uri.c: OK
limine-v12.9.4-common_menu.c: OK
limine-v12.9.4-common_protos_chainload.c: OK
```

and each pinned file is byte-identical to the freshly cloned upstream v12.9.4 file
(`diff -q` → identical for all six). The r91 freeze manifest is untouched; the frozen battery still hashes
`655ee8f3d0942e958cc853deb2d16abcd2d16ae2823ca6548f2a53991b4901b9`, matching the round-91 declaration.

## 1. HEADLINE: the r91 V1 clause is INVERTED upstream in v12.9.5 — re-pin is required, and the change is
semantic, not cosmetic.

Upstream v12.9.5 rewrote `common/lib/config.c`'s entry parser (`create_menu_tree`) to be linear-time
(ChangeLog 12.9.5: *"Parse the config in linear time. Configs with thousands of entries were slow to load."*).
The r91 V1 rule is anchored on **v12.9.4's** `init_config` cut (`common/lib/config.c` raw 642-650). In v12.9.5/12.9.6
that cut lives in the new `create_menu_tree()` and — critically — the *observable* global-section semantics change.

I did not settle this by reading alone. I compiled the **upstream bytes verbatim** (mechanically extracted
`common/lib/config.c` raw 298-407 of tag v12.9.6 and of v12.9.5, plus v12.9.4 raw 339-396 + 656-722 + 778-822,
with only the allocator/`panic` stubs filled in) and ran both parsers on the same configs, then asked each
version's own `config_get_value(NULL, 0, "HASH_MISMATCH_PANIC")` what it can see.

**v12.9.4 (r91 baseline) vs v12.9.6, upstream file compiled verbatim** (receipt: `w1/ScoutDrift/harness-output.txt`):

| config | v12.9.4 sees | v12.9.6 sees |
|---|---|---|
| A: `hash_mismatch_panic: no` **before** `/Shell` | `hash_mismatch_panic=no` | `hash_mismatch_panic=no` — same |
| **B: `/Shell` first, `hash_mismatch_panic: no` after the entry body** | **`hash_mismatch_panic=no`** (whole file visible) | **`(null)`** — invisible |
| **D: `/Shell` first, `measured_boot: yes` after the entry body** | **`measured_boot=yes`** | **`(null)`** — invisible |
| E: `/Shell` first, no global keys at all | `(null)` / `(null)` | `(null)` / `(null)` — same |
| N: no entry line anywhere | `no` / `yes` | `no` / `yes` — same |

v12.9.5 behaves **identically to v12.9.6** on every case (harness3 in the same receipt): the change landed in
**12.9.5**, not 12.9.6.

**Reading of the two code paths (why B/D differ).** v12.9.4 `init_config` (raw 640-651):

```c
    config_ready = true;
    menu_tree = create_menu_tree(NULL, 1, 0);
    size_t s;
    char *c = config_get_entry(&s, 0);
    if (c != NULL) {
        while (*c != '/' && c > config_addr) {
            c--;
        }
        if (*c == '/' && c > config_addr) {
            c[-1] = 0;
        }
    }
```

v12.9.4's `create_menu_tree` copies each entry body into a *fresh* allocation (`entry->body = ext_mem_alloc(...)`,
`memcpy`), so the global `config_addr` buffer is left intact by the tree builder; only `init_config`'s tail NULs
`c[-1]`. When the first physical line is an entry line, `config_get_entry(&s,0)` returns the position of that
entry's `'/'`, the backward walk stops immediately at `config_addr + 0`, the guard `c > config_addr` is **false**, and
**no NUL is written** — the whole file stays visible to `config_get_value`. That is exactly the r91 V1
"first-line-is-entry exception".

v12.9.5/12.9.6 `create_menu_tree` (raw 298-407) instead *rewrites the buffer in place*: it finds the first
line-initial `'/'` by scanning forward (`*p == '/' && (p == config_addr || *(p-1) == '\n')`), then, if
`p > config_addr`, NULs `*(p-1)` (raw 328-330) — and then it **NULs the newline that ends every entry label line
and the newline before the next entry** (raw ~366 and ~381: `*p = '\0'` / `*(p - 1) = '\0'`). Those in-place NULs
truncate `config_addr` at the first entry's label line, so `config_get_value(NULL, 0, …)` — which scans the raw
`config_addr` text — can no longer see anything past it. The v12.9.4 "whole file stays visible" exception is gone.

**Upstream confirms this is intended behaviour, and confirms it is the 12.9.4 behaviour that was the bug.**
ChangeLog 12.9.6:

```
    Miscellaneous:
        - Document that global options must come before the first entry, as
          has been the case since 4.0. A config whose first line is an entry
          has had no global options since 12.9.5, whereas every option in it
          used to count as global. Fixes #700.
```

and upstream issue **#700** ("Global options after the first entry are ignored, unless the file starts with an
entry", LeeeeT, 2026-10-27, closed by #702) states the same cause and marks the old behaviour as the defect:

> "After Limine builds the menu tree, it ends the config text at the first entry. On `v12.x`, `create_menu_tree()` in
> `common/lib/config.c` does this: `if (p > config_addr) { *(p - 1) = '\0'; }` — In 12.9.4, `init_config()` does the
> same with `c[-1] = 0`. … If the file starts with an entry, `p == config_addr`, so nothing is cut. Then global
> options work in all positions. Thus the result depends on whether one line comes before that first entry."
> Real-world effect: "NixOS adds `boot.loader.limine.extraConfig` above the global options that it makes. If a user
> puts an entry in `extraConfig` … Limine ignores all the generated global options: `timeout`, `editor_enabled`,
> `default_entry`, `hash_mismatch_panic`, the wallpaper and others."

Upstream's own words — *"A config whose first line is an entry has had no global options since 12.9.5, whereas
every option in it used to count as global"* — are a precise description of the V1 flip I measured.

**Consequence for the r91 rule set.** The frozen V1 clause says: *"when that first '/'-line is ALSO the first physical
line of the file (no bytes precede it), no cut happens and the WHOLE file stays visible to config_get_value."* That is
**true of v12.9.4 and false of v12.9.5+**. The r91 battery's `FIRST-LINE-ENTRY` family
(`tools/limine-pin-battery-r91.py` raw 1367-1385) is built exactly on that exception: it puts the entry line first,
then `set_panic(c, "no", indent="")` and `measured(c, "yes", indent="")` after the entry body, and expects
`prompt` + `halt-if-tpm`/`halt`. Against a v12.9.5+ Limine those two keys are invisible, so the correct answers become
`panic` + `menu` — the family as frozen **must be inverted** on re-pin, and the near-miss controls that bend V1 would
need to bend the *opposite* way. `PANIC-GLOBAL-ONLY`, `MEASURED-GLOBAL-ONLY`, `GLOBAL-VS-ENTRY`, `MEASURED-IN-ENTRY`
and `PANIC-AFTER-PIN` are all built with a leading global header, so they are unaffected by the flip (their global
section is non-empty in both versions and the visible text is identical) — but `FIRST-LINE-ENTRY` is not.

**Note on the r91 declaration's own wording.** The round-91 declaration cites *"common/lib/config.c raw 642-650"* for
the cut. Those raw line numbers are v12.9.4 line numbers and are **stale for any re-pin**: in v12.9.6 the cut is at
`common/lib/config.c` raw **328-330** inside `create_menu_tree()` (raw 298-407), and v12.9.6's `init_config` is raw
511-671 with `config_ready = true` at raw 666 and `menu_tree = create_menu_tree();` at raw 668. The V1 text also
attributes the cut to `init_config`, which no longer exists as a separate step upstream.

**Verdict: the frozen V1 clause is correct for the host (limine 12.9.4-1) and would be wrong for limine ≥ 12.9.5.**

## 2. Per-file diff table (v12.9.4 → v12.9.6), against the r91 clauses

Line numbers are raw-file byte offsets. "unchanged" means the cited region is byte-identical after accounting for
the shift; I verified by `diff -u` of the aligned regions, and by compiling the upstream files where the semantics
could not be settled by reading.

| file | r91 clause → cited region | v12.9.4 raw | v12.9.6 raw | verdict | clause impact |
|---|---|---|---|---|---|
| `common/lib/uri.c` | **R2** pins — `uri_resolve` | 28-104 | 33-108 | **unchanged** (whole function byte-identical; `diff` of the function body → identical) | none |
| `common/lib/uri.c` | **R3** hash format | 89-101 | 91-101 | **unchanged** (identical text; `URI_ERROR("Blake2b hash must be 128 characters long")` raw 91, `"…invalid character at position %d"` raw 99) | none |
| `common/lib/uri.c` | **R4** resolution — resource dispatch | 344-366 | 370-392 | **unchanged** in the dispatch itself: the same seven `strcmp` resource names (`hdd, odd, boot, guid, uuid, fslabel, tftp`) at raw 375-388, same `"Resource `%s` not valid."` URI_ERROR at raw 390. **Changed around it:** the `if (resource == NULL) { URI_ERROR("No resource specified for URI `%#`.", uri); return NULL; }` guard at 12.9.4 raw 339-342 was **deleted** in 12.9.5+, and `connect_all()` / `volume_by_coord()` / `volume_by_guid_str()` were added (Fast-Boot disk connect, GUID-BE fallback). | **no r91 clause change** — the deleted guard was unreachable (`uri_resolve` returns false for a NULL resource), and the new helpers only widen *which volumes* resolve, which R5 already models as "no regular file at ESP/path → LP-MISSING". R4's seven-name list and the `"Resource ... not valid"` message are untouched. |
| `common/lib/uri.c` | **R5** comparison | 378-383, 403-470, 483-487, 662-664 | 404-409, 429-496, 509-513, 689-691 | **unchanged** (aligned regions diff-identical; `blake2b_check_hash` raw 468 / 689) | none |
| `common/lib/uri.c` | **R6** consequence — `URI_ERROR` macro + optional resources | 18-26 | 19-27 | **unchanged** (the `#define URI_ERROR` block is identical; only `static bool optional_resource = false;` moved from raw 18 to raw 19) | none |
| `common/lib/uri.c` | **R6** — `uri_hash_mismatch` | 301-319 | 327-345 | **unchanged** (identical `panic`/`menu(false)` behaviour) | none |
| `common/lib/uri.c` | **U1** no-URI-shape → `uri_resolve` returns false without a message | 46-63 | 47-64 | **unchanged** — the three `return false;` sites with no `URI_ERROR` (no `'('`, no `):/`, empty path) are byte-identical | none |
| `common/lib/uri.c` | **R10** secure-boot unhashed | 372-375 | 398-401 | **unchanged** (`if (secure_boot_active && hash == NULL) { URI_ERROR("Secure Boot is active and URI `%#` has no associated hash!", uri); fclose(raw); return NULL; }`) | none |
| `common/lib/config.c` | **V1** global-section cut | `init_config` raw 640-651 | `create_menu_tree()` raw 298-407, cut at **328-330** | **CHANGED — SEMANTIC INVERSION** (see §1). 12.9.4: whole file visible when line 1 is an entry line. 12.9.5/12.9.6: the buffer is NUL-truncated at the first entry's label line, so nothing past it is visible to `config_get_value`. | **V1 must be re-pinned.** `FIRST-LINE-ENTRY` family inverts. |
| `common/lib/config.c` | **R1** CR/blank stripping | 527-551 | 551-580 | **rewritten but semantically equivalent** — 12.9.6 uses a single in-place `read`/`write` compaction; 12.9.4 used an in-place `skip`/memmove loop. I compiled both loops verbatim and compared 19 adversarial inputs (CR at EOL, CR internal, CR+blanks, CR+newline+blanks, leading blanks, trailing blanks, both, blank-only line, tab blank, vertical-tab trailing, form-feed trailing, no trailing newline, CR-only line, multiple CR, CR+blank line, blank+CR, entry-slash line, hash-at-end): **all 19 outputs byte-identical** (receipt `harness-output.txt`). | none — R1 survives |
| `common/lib/config.c` | **R9** entry body | 686-720 (`config_get_entry`) | **deleted** (folded into `create_menu_tree`) | **CHANGED (structural only)** — 12.9.6 has no `config_get_entry`/`config_get_entry_name`; the tree builder writes `entry->body` in place. The *observable* body content is the same span of text, and 12.9.6 additionally NUL-terminates it, which is what causes the V1 flip. | none directly, but the R9 citation must be re-anchored |
| `common/lib/config.c` | **R9** first matching key wins — `config_get_value` | 778-818 | 727-771 | **unchanged** (whole function byte-identical) | none |
| `common/menu.c` | **R6** `hash_mismatch_panic` | 1711-1717 | 1789-1795 | **unchanged** (region diff-identical) | none |
| `common/menu.c` | **R10** `measured_boot` + `tpm_present()` | 1719-1728 | 1798-1805 | **unchanged** (region diff-identical) | none |
| `common/menu.c` | **R9** protocol dispatch | 2429-2468 | 2498-2537 | **unchanged** (region diff-identical; `efi`/`uefi`/`efi_chainload` → `chainload`, `efi_boot_entry` → `efi_boot_entry`, all preserved) | none |
| `common/protos/chainload.c` | **R9** PATH→IMAGE_PATH, panic on NULL | 414-437 | 430-451 | **unchanged** (region diff-identical; also `efi_boot_entry` still present at menu.c raw 2532) | none |
| `common/lib/panic.s2.c` | **R10** `menu(false)` / `"System halted."` | 24-28, 70-78, 98 | 32-36, 78-86, 106 | **unchanged** in the cited regions (aligned regions diff-identical). A UEFI-only screen-clear was added at raw 55-62 (cosmetic). | none |
| `common/lib/tpm.c` | **R10** `tpm_present()` | 113-115 | 113-115 | **unchanged** (`return tcg2 != NULL || cc != NULL;`) | none |
| `common/lib/tpm.c` | (adjacent to R2/R5) hash split in `tpm_measure_path` | 219 (`strchr`) | 237 (`strrchr`) | **CHANGED** — `strchr(path, '#')` → `strrchr(path, '#')`, comment: *"The hash follows the last '#', as uri.c reads it; the path may hold more."* | **none for the clauses as written** — R2 already freezes *"the hash is the text after the LAST '#'"* (uri.c's own behaviour); this change makes `tpm.c` *match* the already-frozen R2 rule rather than contradicting it. Worth a note in the C2 entry, not a rule change. |
| `common/lib/gterm.c` | (R6) `uri_open_optional` callers | 625, 706 | 627, 708 | **unchanged** (call sites diff-identical; only `colour_blend` alpha math changed) | none |
| `CONFIG.md` | **R2** path-valued key names | 111-113, 134, 210, 295-308, 330-350 | same | **unchanged** (all cited regions diff-identical; `kernel_path`, `image_path`, `module_path`, `dtb_path`, `global_dtb`, `wallpaper`, `term_font` counts identical). **Changed at 73-78**: the global-options paragraph now says global options *"must come before the first menu entry"*. | none for R2's key list; the doc change corroborates §1 |

## 3. Arch package: the host is one upgrade behind, and the upgrade flips V1

```
$ pacman -Q limine
limine 12.9.4-1

$ pacman -Si limine
Repository      : extra
Version         : 12.9.4-1
Build Date      : Tue 20 Oct 2026 04:34:10 AM -03
```

The **local sync DB is stale** (`/var/lib/pacman/sync/extra.db` dated Oct 22 2026, i.e. it predates both new
releases). The **upstream Arch package page** for `extra/x86_64/limine` reports:

> ## limine 12.9.6-1
> Package Size: 909.9 KB · Installed Size: 5.3 MB · Build Date: 2026-10-28 07:52 UTC · Last Updated: 2026-10-28 08:00 UTC

So Arch `extra` already carries **limine 12.9.6-1**; the host's 12.9.4-1 is what is *installed*, and the next
`sync` will offer 12.9.6-1. I did not install anything (pacman transactions are paused host-wide; the seat brief
also forbids it) and I did not touch `/boot`, which is `drwx------ root root` and unreadable to this seat anyway.

**Operational consequence.** The r91 rule set is currently *correct for the host as it stands* (limine 12.9.4-1, whose
`/boot/limine.conf` the r91 receipt already characterised). But the moment the host takes 12.9.5 or 12.9.6, the
V1 first-line exception is inverted, and any gate still implementing the frozen v12.9.4 V1 clause will **mis-report
`hash_mismatch_panic` and `measured_boot` for a config whose first physical line is an entry line** — it will read
keys that upstream no longer reads. The host's own config (`/boot/limine.conf`, per the r91 host receipt) has
`protocol: efi` / `path:` entries at lines 29-72; I could not read the file (permission denied) so I cannot certify
whether its first physical line is an entry line — **the L1's host receipt does not record the first line either**.
This is the one host fact I would want run read-only if it matters:

```
$ head -3 /boot/limine.conf          # read-only; needs root; NOT run by me
$ grep -n '^/' /boot/limine.conf | head -3   # first entry line and its line number
```

If the first entry line is line 1, the host config is directly exposed to the flip. If not, the host config is
unaffected (its global section is non-empty and identical under both versions) — but the *gate's rule set* still
needs re-pinning for correctness on any future config.

## 4. "Re-pin needed on upgrade?" — verdict

**Yes, and the re-pin is a semantic change, not a line-number refresh.**

- **v12.9.4 → v12.9.5 (2026-10-27)** is the breaking release for r91. It rewrote `common/lib/config.c`'s parser
  (linear-time `create_menu_tree`), which changed the *global-section visibility* that V1 freezes. Measured with
  upstream bytes compiled verbatim (§1); upstream's own ChangeLog and issue #700 confirm the change and its
  12.9.5 date.
- **v12.9.5 → v12.9.6 (2026-10-28)** changed *nothing* in the r91 clauses: `common/lib/config.c` is byte-identical
  between the two tags (`diff -q` → identical), `common/lib/uri.c` is byte-identical, `common/menu.c` is byte-identical.
  12.9.6 only *documents* the new rule (CONFIG.md 73-78, ChangeLog 12.9.6) and fixes unrelated UEFI/menu issues.
- **Everything else in the r91 clause set (R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, U1) survives both upgrades
  unchanged**, with one citation refresh: the raw line numbers cited in the battery docstring for `config.c`
  (raw 642-650, 527-551, 686-720, 778-818), `uri.c` (18-26, 344-366, 46-63, 378-383, 403-470, 483-487, 662-664,
  693-710), `menu.c` (1711-1717, 1719-1728, 2429-2468), `chainload.c` (414-437) and `panic.s2.c` (24-28, 70-78, 98)
  all shift. New v12.9.6 offsets are in the table in §2.
- The only *behavioural* clause edit needed is **V1's first-line-is-entry exception**, which must be **inverted**:
  under ≥12.9.5 a config whose first physical line is an entry line has **no** global options at all (the buffer is
  truncated at that entry's label line), so `hash_mismatch_panic`/`measured_boot` written after it are invisible.
  `FIRST-LINE-ENTRY` must then expect `panic` + `menu` instead of `prompt` + `halt-if-tpm`/`halt`, and the V1
  near-miss controls must bend the opposite way.

**Recommended sequencing (for the L1, not acted on by me):** keep the r91 round pinned to v12.9.4 (the host's
installed version, and the version the frozen battery and the r91 host receipt describe) and open the V1 inversion
as a **round-92** item gated on the host's limine version — do not silently re-pin inside r91, whose freeze manifest
and 12 controls are already committed and hashed.

## 5. What I did NOT change / could not determine

- **No lane file was edited.** No git/jj mutation was run in the lane or anywhere outside my own scratch and my own
  wave subdir. No commit, no push.
- **No host mutation.** `/boot` was never written (it is root-only and I did not attempt it); no `objcopy`,
  `strip`, `sbsign`, `ukify`, `patchelf`, `mkinitcpio`, `limine*`, `snapper`, `bootctl`, `efibootmgr`, `pacman`,
  no sysctl, no `/sys` or `/proc` write, no `sudo` at all.
- **The host's `/boot/limine.conf` first line is unknown to me** (permission denied, and I will not use `sudo`). The
  read-only commands I would want are in §3.
- **The upstream issue/PR pair (#700 / #702) was read via the GitHub API as read-only web reads**, and upstream
  `ChangeLog` + `CONFIG.md` were read from the clones. I did not clone or run any upstream build; the harness compiles
  only the extracted parser functions with stubbed allocators — it is a *semantic* probe of the upstream bytes, not a
  Limine build, so it establishes config-parsing semantics only.
- **Tooling:** no tool was installed or upgraded this wave (git, gcc, pacman were already present; gcc used only to
  compile my own harness). Channel/version/reason: `gcc` (system, `/usr/bin/gcc`), `git` (system) — used to compile
  the read-only upstream-bytes harness and to clone upstream tags; reason: measure the v12.9.4 vs v12.9.5/12.9.6
  config-parsing semantics empirically rather than by reading alone. No pacman transaction was performed or attempted.
- **Scratch** `/fast/scratch/hyaku/tsukuroi-r91/ScoutDrift/` was removed on exit (`rm -rf`); the harness sources and
  its output are copied into `.ufo/waves/round-91/w1/ScoutDrift/` as receipts.

## 6. Receipts (in this seat's subdir)

| file | what it is |
|---|---|
| `w1/ScoutDrift/harness-output.txt` | the measured output: 12.9.4 vs 12.9.6 and 12.9.4 vs 12.9.5 on the same configs (upstream `config.c` bytes compiled verbatim), plus the 19-case R1 strip-loop equivalence table |
| `w1/ScoutDrift/harness.c` | probe: 12.9.4 parser + 12.9.6 parser transcribed; strip-loop equivalence cases |
| `w1/ScoutDrift/harness2.c` | probe: 12.9.4 vs **v12.9.6 upstream `config.c` raw 298-407 included verbatim** |
| `w1/ScoutDrift/harness3.c` | probe: 12.9.4 vs **v12.9.5 upstream `config.c` raw 298-407 included verbatim** |
| `w1/ScoutDrift/part_*.c` | the mechanically extracted upstream regions (94/95/96) the probes include |

`harness2`/`harness3` include the upstream file text itself, so the receipt is re-runnable and self-evidencing:

```
$ cd w1/ScoutDrift && gcc -std=gnu11 -w -o harness2 harness2.c && ./harness2
```

## 7. Confidence

- **High** for the V1 inversion: measured on upstream bytes (three independent harnesses), corroborated by upstream's
  own ChangeLog text and issue #700, and the release boundary (12.9.5) is pinned by the byte-identical `config.c`
  of tags v12.9.5 and v12.9.6 plus the 12.9.4↔12.9.5 diff.
- **High** for "the rest of the clause set is unchanged": every cited region was diffed byte-for-byte at aligned
  offsets, and the two regions where reading could not settle the semantics (R1 stripping, V1 visibility) were
  settled by compiling and running the upstream code.
- **Medium** on the host's practical exposure: it depends on the first line of `/boot/limine.conf`, which this seat
  cannot read (§3) and which the r91 host receipt does not record.
- **Low/uncertain, deliberately not claimed:** whether upstream will make any further change to `config.c` after
  12.9.6. The default branch HEAD equals the v12.9.6 tag today, so there is no unreleased drift to answer this.

## 8. Note for the L1 on C2 (adjacent, not my claim)

C2's subject is the *host's* line 72, `path: boot():/EFI/BOOT/BOOTX64.EFI` (no `#`). The upstream code paths C2
relies on are **unchanged** across v12.9.4 → v12.9.6: `uri_resolve`'s three silent `return false;` sites (no `'('`,
no `):/`, empty path) are byte-identical, `chainload.c`'s PATH→IMAGE_PATH read and its `"efi: Failed to open image"`
panic are byte-identical, and `uri_open`'s `secure_boot_active && hash == NULL` rejection is byte-identical. So C2's
sourced rows remain valid at v12.9.6. Two updates worth folding in: (a) `tpm.c` raw 237 now uses `strrchr` so the
TPM path/hash split matches uri.c's last-`'#'` rule (this *confirms* R2's "LAST '#'" wording against a second
upstream site); (b) `uri.c` raw 339-342's `"No resource specified for URI"` guard is gone upstream, and the
`"Resource `%s` not valid."` message that R4 maps to LP-BAD-RESOURCE is at v12.9.6 raw 390.

---

**Seat verdict (freshness, operability):** the r91 rule set is *correct for the host today* (limine 12.9.4-1) but
**stale for upstream ≥ 12.9.5**, where the V1 global-section exception it freezes has been inverted by upstream's
linear-time config-parser rewrite. Re-pin required before the host takes limine 12.9.6-1 (already in Arch `extra`);
every other r91 clause survives both upgrades unchanged, modulo raw-line citation refresh.
