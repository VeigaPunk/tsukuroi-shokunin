# ScribeEntry — round 85 w1 (C1 hibernation-availability draft)

Seat: ScribeEntry (scribe, axis depth). Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Lane revision measured: `479d868b2fc8969a19a617cd55ced5c13edd84b6` (`git -C … rev-parse master`, unchanged
from the candidate tip at the start and end of this seat; `git status --porcelain` shows the two modified
files other seats hold, `SKILL.md` and `corpus/knowledge/hibernate-resume-plane-r84.md`, and no change by me).

## Verdict

Drafted the C1 knowledge entry to the seat's shape: 8 rows HA1–HA8, each with a source id, raw-line span and
a quote that is a byte-exact slice of the pinned v7.2 snapshot, plus 9 extra quote blocks in the markdown
(17 total). All 17 pass exactness, uniqueness and the 25-word cap; every row's JSON quote is the first block
of its markdown row. Nothing hibernated, resumed, or wrote to the host; no lane file was edited.

## Deliverables

| path (relative to lane) | bytes | sha256 |
|---|---|---|
| `.ufo/waves/round-85/w1/ScribeEntry/hibernation-availability-r85.md` | 18035 | `ae11bd8209cdd72bfa68edf0712f154d22a54c9ac86c9637334c2d1be5c4b636` |
| `.ufo/waves/round-85/w1/ScribeEntry/hibernation-availability-r85.json` | 7668 | `c68da0ae9c080975fb7dfe7e8959a7c7f855ac0bf6ee449803a1520b3a2c207a` |
| `.ufo/waves/round-85/w1/ScribeEntry/gen_rows.py` (generator, refuses bad quotes) | 25913 | `c9b1d73306bc2c67bfa9c452dc508d9cdcc1fb59e775f2d73ffc9c532b939bf5` |
| `.ufo/waves/round-85/w1/ScribeEntry/receipts/quote-check.txt` | 4200 | `c7cd5ff706d466b1795582fab3b8f31ffa80d5462a27e27a90ae8ceebee7adc7` |

Other receipts: `receipts/host-recheck.txt` (timestamped host read, 17:05:19-03:00),
`receipts/FETCHES.txt` + `receipts/upstream-mm-secretmem.c`, `upstream-cxl-suspend.c`,
`upstream-cxl-mem.c` (the three unpinned referents, HTTP 200 each, sha256 recorded).

## Draft content (row map)

| row | statement (one line) | source, raw lines | quote words |
|---|---|---|---|
| HA1 | `hibernation_available()` is the four-term conjunction; five call sites check it (`hibernate()` 766-769, `software_resume_initcall` 1111-1112, `disk_show` 1168-1169, `disk_store` 1211-1212, `resume_store` 1269-1270) | S343 111-113 | 10 |
| HA2 | `nohibernate` sets `noresume` and `nohibernate` together; not undoable from userspace | S343 1461-1466 | 15 |
| HA3 | `hibernate=` is an ordered prefix parse (`noresume`→`nocompress`→`no`→`protect_image`); `nocompress` does not disable, anything else starting `no` does (incl. `hibernate=non`, `hibernate=noprotect_image`) | S343 1428-1432 | 23 |
| HA4 | `noresume` sets only `noresume`; hibernation stays available, the initcall bails, the image is not read | S343 1440-1444 | 12 |
| HA5 | `LOCKDOWN_HIBERNATION` (5) < `LOCKDOWN_INTEGRITY_MAX` (21); `kernel_locked_down >= what` → `-EPERM`, so `integrity` blocks hibernation | S344 133-149 | 17 |
| HA6 | the documentation mirrors the three tokens and `lockdown=` but not the ordering | S336 1962-1966 | 23 |
| HA7 | this host is not blocked, and the kernel's own witness (`/sys/power/disk` not `[disabled]`) agrees | S343 1168-1169 | 5 |
| HA8 | secretmem/CXL are gate-invisible; measured read-only (CONFIG, VMA scan, modules, sysfs, iomem, dmesg) | S343 113-113 | 3 |

Header (first 12 lines, column 0): `source:` line 3, `recheck:` line 4, `verified-at: 2026-11-06` line 5, plus
`host capture:`, `machine-readable rows:`, `snapshots:`, `gate:` — meets the grammar of
`tools/check-knowledge-header.py` (column 0, ISO date, `30d` cadence) and the round-85 first-12-lines window
of `.ufo/waves/round-85/w1/ExecLints/check-entry-headers-r85.py`. Sections present: What this plane answers,
Rows, Operator actions, Limits, Review record, Provenance.

## Method and checks actually run

Generator (writes all three artifacts from the pinned bytes; refuses on sha256 mismatch, non-exact slice,
non-unique slice, >25 words):

```
$ TMPDIR=/fast/scratch/.../ScribeEntry python3 gen_rows.py
wrote hibernation-availability-r85.json, hibernation-availability-r85.md, receipts/quote-check.txt (8 rows, 17 quote blocks)
rc=0
```

Pinned digests verified against `.ufo/waves/round-85/before/src/SHA256SUMS` (quote-check.txt):

```
S343 kernel_power_hibernate.c sha256=ae3dbeb6…86c1 pinned=yes
S344 include_linux_security.h sha256=263740c9…fcf pinned=yes
S345 security_lockdown_lockdown.c sha256=fec032ce…e00a pinned=yes
S336 Documentation_admin-guide_kernel-parameters.txt sha256=23b1a690…340c pinned=yes
rows=8 quote_blocks=17 all_exact=yes all_unique=yes all_le_25_words=yes
```

Markdown cross-check (a second, independent parse of the generated file):

```
fenced_blocks 17
blocks_equal_json_primary 8
all_blocks_exact_slice True
all_le_25_words True
json_rows 8 all_keys_ok True
primary_quote_is_first_block_of_row: [True, True, True, True, True, True, True, True]
```

JSON shape: bare list of 8 objects, keys exactly `{id, statement, source, raw_lines, quote, host_value}`;
`raw_lines` is `[first, last]` inclusive.

Host (read-only; `receipts/host-recheck.txt`, 2026-11-06T17:05:19-03:00):

```
[none] integrity confidentiality          # /sys/kernel/security/lockdown
[platform] shutdown reboot suspend test_resume   # /sys/power/disk (not [disabled])
freeze mem disk                           # /sys/power/state
15 []                                     # cmdline tokens; matches for nohibernate/noresume/hibernate=
{"findings": [], "verdict": "HEALTHY"}    # python3 tools/check-hibernate-resume.py --live
rc=0
CONFIG_HIBERNATION=y
CONFIG_SECRETMEM=y
CONFIG_CXL_MEM=m
secretmem_vma_hits_root=0
secretmem_maps_files_with_hits=0
dmesg_lines=2162
dmesg_secretmem_or_cxl_lines=0
iomem_cxl_lines=0
lsmod_cxl_lines=0
sys_class_cxl_entries=0
secretmem_active_kallsyms=2
```

## Findings

1. **A competing untracked pair already sits on the landing path.** `corpus/knowledge/hibernation-availability-r85.md`
   (16:58:53) and `.json` (16:59:14) are untracked (`??`), so they are not landed; I did not touch them. They
   do not match the seat's shape and contain concrete defects: `corpus/knowledge/hibernation-availability-r85.json:51,55`
   has row `HA7` with `"quote": null` (the "no row without a located quote" rule), `md:32` likewise quotes
   nothing for HA7 (`—`), `md:29` (HA4) ends its quote mid-`if` at `else if (!strncmp(str, "no", 2))` without
   the branch body, and its quotes are flattened to one line with spaces, so they are not verbatim at the raw
   lines (the snapshot uses tabs and line breaks). It also numbers 9 rows (HA1–HA9) with a different mapping
   (HA2 = callers, HA7 = host, HA9 = lockdown doc) than the seat's frozen HA1–HA8. L1 decision: land my draft
   and drop/replace that pair, or fold it — my draft supersedes it row-for-row.
2. **Rule-vs-kernel gap, now in Limits.** The frozen A1/A3 text tests whole tokens, but the kernel rejoins
   `param=value` (`repair_env_string`, `init/main.c` v7.2 463-472) and matches a parameter-name prefix
   (`parameqn`, `kernel/params.c` 86-95) before calling the setter. So `noresume=1`, `noresumeX`,
   `nohibernate=1`, `nohibernateX` all disable in the kernel while the gate reports no finding; `hibernate=`
   is different because the registered string contains the `=` literally (`hibernateX=` does not match).
   `lockdown` is an `early_param` compared by exact name (`do_early_param`, `init/main.c` 721-730), so the
   gate's sysfs read has no divergence. This is a rule-text limit, not a C2 predicate defect — the gate
   implements the frozen rules; the entry states the gap. No patch to the gate is proposed here.
3. **The kernel's own availability witness is free but unread.** `/sys/power/disk` prints `[disabled]`
   exactly while `hibernation_available()` is false (1168-1169); the gate never reads it (it reads
   `/sys/power/state` only, `tools/check-hibernate-resume.py:165`). HA7/HA8 use it as an independent
   cross-check; the entry marks it as outside the frozen rule set, so it cannot silently become a rule.

## Open questions for the L1

- JSON shape: I used the bare list the seat prompt names (`{id, statement, source, raw_lines, quote,
  host_value}`), which is what the competing draft also used but differs from the r84 object shape
  (`snapshots`/`receipts`/`rows`). If the landing counter expects r84's object, the provenance table in the
  markdown and `receipts/` carry the same data.
- Stable delta: the entry's Limits defer the 7.2 → 7.2.11 delta of the cited regions to `ScoutSources`; when
  landing, cite its result (or drop the sentence if it does not land).
- Two definitions (`mm/secretmem.c`, `drivers/cxl/*`) are outside the pinned set and appear only in HA8's
  statement; the machine rows quote pinned bytes only. If the corpus rule is pinned-only, HA8's statement
  needs those clauses removed (the host measurements stand without them).

## Refused / not done

- No lane file was edited; no `git add|commit|push|stash|checkout|switch|reset|pull`, no `jj` mutation.
- No host write: no hibernate/suspend, no swap, no sysfs, no sysctl, no boot/limine/mkinitcpio/pacman action.
  `sudo -n` used only to read `/proc/*/maps`, `dmesg` and `ls`.
- Not run here (not this seat, and not passes): the C2 battery, the lane header gate on the landed path (my
  draft is untracked; compliance checked by inspection as above), the stable 7.2.11 delta.
- Tool installs/upgrades: none.
- Scope incident, self-reported: one `mkdir -p` was issued with a relative path from the fleet-root cwd and
  created empty `/home/vgpnk/Projects/shokunin/.ufo/waves/round-85/w1/ScribeEntry/receipts`; I removed exactly
  those empty directories with `rmdir` (`/home/vgpnk/Projects/shokunin/.ufo/waves` itself pre-existed and was
  left in place). No file was created there. All later commands used absolute paths.
- Scratch `/fast/scratch/hyaku/tsukuroi-r85/ScribeEntry` removed after the run; no `/tmp` files left.
