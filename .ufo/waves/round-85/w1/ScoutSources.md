# ScoutSources — round 85, wave w1 — upstream sources re-opened and registry rows drafted

Seat: `ScoutSources` (scout, leaf). Lane revision measured:
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` → `479d868b2fc8969a19a617cd55ced5c13edd84b6`
(the candidate commit; the freeze commit is `66374a4db963e5c655506e64cb0fea2d67ec9d0d`).

Axes named: **source freshness** (do the pinned upstream snapshots still say what the round cites?)
and **registry depth** (are the availability sources registered with locatable quotes?).

No lane file was edited. Every `git` call was read-only. No host state was written; the host was only
read (`/sys`, `/proc`, `/proc/config.gz`).

---

## Check 1 — upstream URL re-fetch vs the pinned snapshot — **PASS (4/4 MATCH)**

`curl -sS -L -w '%{http_code} %{size_download}'` into scratch, then `sha256sum` and `cmp` against
`.ufo/waves/round-85/before/src/SHA256SUMS`.

```
FILE                                           HTTP   RC           SHA256   VERDICT
kernel_power_hibernate.c                       200    rc=0         ae3dbeb6 MATCH
include_linux_security.h                       200    rc=0         263740c9 MATCH
security_lockdown_lockdown.c                  200    rc=0         fec032ce MATCH
Documentation_admin-guide_kernel-parameters.txt 200   rc=0         23b1a690 MATCH
```

All four are byte-identical to the pinned snapshots (`cmp` silent). Full per-file detail:
`.ufo/waves/round-85/w1/ScoutSources/receipt-1-url-fetch.txt`.

## Check 2 — v7.2 snapshot vs stable v7.2.11 (the host's kernel) — **PASS, with one recorded drift**

Fetched from the stable tree at the host's own tag
(`https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/<path>?h=v7.2.11`), all
HTTP 200:

| path | v7.2.11 sha256 | bytes |
|---|---|---|
| kernel/power/hibernate.c | `dac50a26672fcb0d1ab96f9d93465a97380cbda0a8a6d03adc75c7cd134eaab0` | 35318 |
| include/linux/security.h | `263740c965f34f9363fc8d2a673b0826e27a21376e896ac2ed5b8859f4fecfcf` | 67333 |
| security/lockdown/lockdown.c | `fec032ce5ae3a85f66db28a4454a819d70abfe5cbbecfe4f1a115276fc04e00a` | 4344 |
| Documentation/admin-guide/kernel-parameters.txt | `209f7cd9bfb6150bacc0076cdc31116c3d211a8c4057b5e5e4145d44d2155825` | 316764 |

**Every region the round cites is identical on the host's own 7.2.11.** Line numbers shift by **+2**
after line 472 because of one unrelated upstream commit inside `hibernation_snapshot()`:

```
hibernate.c 109-113    v7.2 == v7.2.11 109-113     : SAME
hibernate.c 760-766    v7.2 == v7.2.11 762-768     : SAME
hibernate.c 1106-1111  v7.2 == v7.2.11 1108-1113   : SAME
hibernate.c 1424-1465  v7.2 == v7.2.11 1426-1467   : SAME
hibernate.c 1518-1524  v7.2 == v7.2.11 1520-1526   : SAME
security.h 128-158     whole-file sha256 identical : SAME
lockdown.c 59-73       whole-file sha256 identical : SAME
```

The v7.2 → v7.2.11 `hibernate.c` diff is **only** this hunk, all inside `hibernation_snapshot()`
(the `dpm_prepare`/`hibernate_preallocate_memory` reorder and a new `Cleanup:` label):

```
410a411,419
413c422
424,432d432
466a467,470
469,470d472
```

None of the cited availability lines fall in it. `security.h` and `lockdown.c` are byte-identical
across the two tags.

**One drift worth recording (does not affect any cited region):** in
`kernel-parameters.txt` the `pata_legacy.*` options were dropped upstream, so the `resume=` block
moves **6574 → 6537** between v7.2 and v7.2.11. The four availability parameter blocks do **not**
move:

```
^	hibernate=    v7.2:1962  v7.2.11:1962
^	lockdown=     v7.2:3538  v7.2.11:3538
^	nohibernate   v7.2:4479  v7.2.11:4479
^	noresume      v7.2:4593  v7.2.11:4593
^	resume=       v7.2:6574  v7.2.11:6537
```

The S336 registry row anchors `resume=`/`resume_offset=` at **tag v7.2** raw 6574-6583 — correct for
that tag, and it now names a different line number on the host's 7.2.11. The anchor is tag-scoped,
so the row stays true as written; the recheck note below records the drift. Full diff:
`.ufo/waves/round-85/w1/ScoutSources/receipt-2-v7211-diff.txt`.

## Check 3 — S336 snapshot verification at the four required raw ranges — **PASS**

`kernel-parameters.txt` in the r85 pin is byte-identical to the r84 pin:

```
23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c  .ufo/waves/round-85/before/src/Documentation_admin-guide_kernel-parameters.txt
23b1a690210b6884f040a6b1e5baf1fc18856e844d30d4784470bd210953340c  .ufo/waves/round-84/before/src/kernel-parameters.txt
```

Each range holds the claimed text, with a ≤25-word quote:

| raw range | holds | quote (word count) |
|---|---|---|
| 1962-1969 | `hibernate= [HIBERNATION]` with sub-options `noresume`, `nocompress`, `no`, `protect_image` | 1965-1966: "nocompress Don't compress/decompress hibernation images. no Disable hibernation and resume." (13 w) |
| 3538-3545 | `lockdown= [SECURITY,EARLY]` `{ integrity \| confidentiality }` | 3540-3542: "Enable the kernel lockdown feature. If set to integrity, kernel features that allow userland to modify the running kernel are disabled." (24 w) |
| 4479 | `nohibernate [HIBERNATION] Disable hibernation and resume.` | same line (6 w) |
| 4593 | `noresume [SWSUSP] Disables resume and restores original swap space.` | 4593-4594 (9 w) |

S336's own anchor (raw 6574-6583, `resume=` / `resume_offset=`) also verified present and correct.

## Check 4 — three registry rows drafted, census-clean — **PASS**

Rows S343 (hibernate.c), S344 (security.h), S345 (lockdown.c) drafted in the exact `## Registry`
column order, `kind=code`, `tier=A`, `status=mined`, `opened 2026-11-06`, `recheck on-release`,
`used-by corpus/knowledge/hibernation-availability-r85.md`. Anchors name **tag v7.2**, the raw line
ranges and the **snapshot sha256**. No literal `|` inside any cell; `NF=13` for all three.

Mirror census (full lane copy so E11 used-by paths resolve; registry reset to the pre-round `HEAD`
state; my three rows appended right after S342):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file $S/v/corpus/SOURCES.md
...
file	ok	/fast/scratch/hyaku/tsukuroi-r85/ScoutSources/v/corpus/SOURCES.md
rc=0
```

```
## per-code summary
      1 ok
      52 W04
## no finding mentions S343/S344/S345:
(no line mentions S343/S344/S345)
```

The 52 `W04` are the pre-existing same-URL-different-scope warnings, byte-identical to the baseline
run on the untouched lane registry (`rc(baseline)=0`, same 52 W04); the only diff between the two
finding sets is the file path inside the `ok` line. So **my three rows add no E-code and no W-code**.

Rows and their quotes: `.ufo/waves/round-85/w1/ScoutSources/rows.md`.
Mirrors: `SOURCES.mirror-with-rows.md` (my rows) and `SOURCES.mirror-with-S346.md` (appendix).
Census receipt: `receipt-4-census-validate.txt`.

## Concurrent landing observed (no conflict to resolve, but the L1 must know)

While this seat worked, **a sibling seat landed its own S343/S344/S345** into the lane's
`corpus/SOURCES.md` working tree (lines 354-356; `git show HEAD:corpus/SOURCES.md` has 0 such rows,
so the landing is uncommitted). I checked those landed rows against my independent upstream evidence:
they **agree on every anchor range, every snapshot sha256 and every teaching** — including the
`disk_show`/`disk_store`/`resume_store` caller ranges, the `lockdown_levels` mapping at raw 20-22,
and the `kernel_locked_down >= what` comparison at raw 65. The two sets are compatible; the L1
should land one set, not both (two sets of the same three ids would trip `E03 duplicate id`).

## Appendix — one uncovered gap, offered for the L1's decision (not landed by me)

The r85 pin's `kernel-parameters.txt` carries the four **availability** parameter blocks
(1962-1969, 3538-3545, 4479, 4593), but the registry only carries that file as **S336**, whose scope
is "`resume=` and `resume_offset=`" at raw 6574-6583. A fourth row closing that gap is drafted in
`rows.md`; it repeats the kernel-parameters.txt URL, so the census raises `W04` for it
(`rc=0`, no E-code). The L1 may land it as S346 with a distinct scope, or fold the four ranges into
S336's anchor. I did not land it.

## Host read-only facts measured (support the C1 entry's rows)

```
uname -r                                   -> 7.2.11-arch1-1
cat /sys/kernel/security/lockdown          -> [none] integrity confidentiality
grep -oE "nohibernate|noresume|hibernate=[^ ]*" /proc/cmdline -> (none present)
ls /sys/kernel/mm/secretmem                -> No such file or directory
ls /sys/bus/cxl                           -> No such file or directory
cat /sys/power/state                       -> freeze mem disk
/proc/config.gz: CONFIG_HIBERNATION=y CONFIG_PM_SLEEP=y CONFIG_SECRETMEM=y
                CONFIG_SECURITY_LOCKDOWN_LSM=y CONFIG_STRICT_KERNEL_RWX=y
                CONFIG_CXL_BUS=m CONFIG_CXL_MEM=m
```

Upstream definitions fetched for the two blockers named in `hibernation_available()`:
`mm/secretmem.c` raw 45-48 `bool secretmem_active(void) { return !!atomic_read(&secretmem_users); }`
and `drivers/cxl/core/suspend.c` raw 9-12 `bool cxl_mem_active(void) { return atomic_read(&mem_active) != 0; }`.
Receipt: `receipt-5-host-facts.txt`.

## Freshness defects proposed for the L1 (file:line + patch)

1. **`corpus/SOURCES.md:347` (S336 anchor) — line drift on the host's own kernel.**
   The row anchors `resume=`/`resume_offset=` at "tag v7.2, raw lines 6574-6583". Verified: on
   v7.2.11 the same block is at raw **6537-6546** (the `pata_legacy.*` options were dropped upstream,
   `diff_lines=40`, and `resume=` moved `6574 → 6537`; the four availability blocks do not move).
   The row as written is true *for tag v7.2*, which is what it claims, so this is not an error —
   but the C1 entry's recheck line should note the drift. Proposed patch (L1 decides):

   ```
   - tag v7.2, raw lines 6574-6583 (resume=, resume_offset=); pinned snapshot .ufo/waves/round-84/before/src/kernel-parameters.txt sha256 23b1a690…340c
   + tag v7.2, raw lines 6574-6583 (resume=, resume_offset=) — on stable v7.2.11 the same block is at raw 6537-6546; pinned snapshot .ufo/waves/round-84/before/src/kernel-parameters.txt sha256 23b1a690…340c
   ```

2. **`corpus/SOURCES.md:354` (S343 anchor) — same +2 line shift applies to `hibernate.c` on the host.**
   Verified: v7.2 raw 760-766 is v7.2.11 raw 762-768, 1106-1111 → 1108-1113, 1424-1465 → 1426-1467,
   1518-1524 → 1520-1526. The content is identical, only the numbers move. The row says "tag v7.2",
   so it stands; the recheck line should carry the same note as (1).

No patch was applied — per the seat's bounds, the L1 decides what lands.

## Unrun / refused

- **No patch was applied** to any lane file, by instruction. The two items above are proposals.
- **No `git add|commit|push|stash|checkout|switch|reset|pull` and no mutating `jj` command was run.**
  Only `rev-parse`, `status`, `show` (read-only) were used.
- **No host mutation**: no hibernate/suspend/swap, nothing written to `/sys` or `/proc`, no sysctl
  change, no `/boot` touch, no `mkinitcpio`, no pacman transaction. `sudo -n` was not needed at all.
- **No tool was installed** for this seat — `curl`, `sha256sum`, `diff`, `awk`, `python3` and
  `sources-census.sh` (already in the fleet root) covered the task. Nothing to record under the
  2026-10-19 tooling authorization.
- **The `cxl_mem_active` / `secretmem_active` upstream definitions are outside the pinned set**; they
  were fetched live from tag v7.2 and are recorded in `receipt-5-host-facts.txt` as supporting
  context, not as a registry source.
- Scratch root `/fast/scratch/hyaku/tsukuroi-r85/ScoutSources` is removed on exit; all receipts were
  copied into the wave dir first.

## File index

| path | what |
|---|---|
| `.ufo/waves/round-85/w1/ScoutSources.md` | this report |
| `.ufo/waves/round-85/w1/ScoutSources/rows.md` | the three drafted rows, their quotes, the S336 quotes, the appendix row |
| `.ufo/waves/round-85/w1/ScoutSources/rows.raw` | the three rows as machine-readable lines |
| `.ufo/waves/round-85/w1/ScoutSources/receipt-1-url-fetch.txt` | check 1, per-file HTTP code, rc, sha256, verdict |
| `.ufo/waves/round-85/w1/ScoutSources/receipt-2-v7211-diff.txt` | check 2, full v7.2 vs v7.2.11 diffs |
| `.ufo/waves/round-85/w1/ScoutSources/receipt-3-quotes.txt` | check 3 + every cited raw range printed by `sed -n` |
| `.ufo/waves/round-85/w1/ScoutSources/receipt-4-census-validate.txt` | check 4, full census output + rc |
| `.ufo/waves/round-85/w1/ScoutSources/receipt-5-host-facts.txt` | host read-only facts |
| `.ufo/waves/round-85/w1/ScoutSources/receipt-6-final-outputs.txt` | consolidated tables |
| `.ufo/waves/round-85/w1/ScoutSources/SOURCES.mirror-with-rows.md` | corpus mirror with my three rows appended |
| `.ufo/waves/round-85/w1/ScoutSources/SOURCES.mirror-with-S346.md` | corpus mirror with the appendix row |
