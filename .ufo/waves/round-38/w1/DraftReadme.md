VERDICT: draft

# P-2 — append-only README section for round 38 (storage arm in the census; effective ALPM hook order)

Draft only. I wrote no lane content: `corpus/README.md` is unmodified (`git status --porcelain`
shows no `corpus/` entry; the only paths I created are this report and
`.ufo/waves/round-38/w1/DraftReadme/receipts.txt`). No counter was run, no `--selftest` was run, no
package/write/service/host action was taken, nothing installed. Lane HEAD at drafting:
`5edb6c2` (`git log --oneline -1`, 2026-10-26).

## What the draft rests on (claims I checked myself)

| Fact in the draft | Command / path | Observed |
|---|---|---|
| arm function and line | `grep -n "probe_storage_arm" tools/tsukuroi-census.sh` | `1848:probe_storage_arm() {`, call `3007`, print `3008` |
| line position (after DRIFT, before rollup) | `sed -n '3000,3010p' tools/tsukuroi-census.sh` | DRIFT `printf` :3005, then the round-38 comment :3006, `probe_storage_arm` :3007, `printf … "$STORAGE_LINE"` :3008, `local roll=HEALTHY` :3010 |
| grammar and verdict rules | `tools/tsukuroi-census.sh:1847-1887` (header contract :350-369) | `STORAGE btrfs-device-stats state=… filesystems=… devices=… nonzero=…`; five keys; BLOCKED/DEGRADED/HEALTHY as drafted; sysfs 0444; `TSUKUROI_BTRFS_SYSFS` default `/sys/fs/btrfs` (:392) |
| six selftest cases | `grep -n "case_home='storage" tools/tsukuroi-census.sh \| wc -l` → `6`; names at :2889-2922 | `storage-absent`, `-zero`, `-nonzero`, `-malformed`, `-duplicate`, `-no-devinfo` |
| verdict-neutrality | header :366-368 ("no PLANE text, rollup term or exit code changes"); receipt `six_planes_all: 1` per case | unchanged rollup terms; six PLANE lines every run |
| arm bytes identical at the measured commit and HEAD | `git show 52ffd65:tools/tsukuroi-census.sh \| sha256sum` vs `sha256sum tools/tsukuroi-census.sh` | both `8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c` |
| counter digests cited | `sha256sum tools/score-storage-arm-r38.py tools/score-storage-arm-r38-q82.py tools/check-hook-order-r38.py` | `e649bfb3…f82218`, `a183ff58…d99e3`, `60e3635b…bd1a8` — equal to the frozen values in SCORECARD `:2107,2133` |
| C1 predicate sentence | `tools/score-storage-arm-r38.py:7` | `fixtures_matched == FIXTURES_EXPECTED and live_match == 1 and six_planes_all == 1` |
| q82 predicate sentence | `tools/score-storage-arm-r38-q82.py:18` | `ns_views_matched == VIEWS and ns_available == 1`; `VIEWS = 3`, no override, `unshare -rm`, bind over `/sys/fs/btrfs`, random per run (:46-53 header) |
| C1 measured state | `.ufo/waves/round-38/after/c1-after-52ffd65.json` | `fixtures_matched 10`, `live_match 1`, `six_planes_all 1`, `result PASS`, `exit 0`, `euid_root false` |
| C2 measured state | `.ufo/waves/round-38/after/c2-after-1fe28e7.json` | `rows_expected 69`, `rows_matched 69`, `mismatches 0`, `extra_rows 0`, `source_ok 1`, `source_ids S208-S212`, PASS |
| v1 counter is fixture-gameable | `.ufo/waves/round-38/controls/controls-q82.jsonl` line 1 | fixture-gated arm: v1 `fixtures_matched 10, live_match 1 → PASS`; q82 `ns_views_matched 0/3 → FAIL` |
| q82 controls behave as drafted | same file lines 2-3 | cached-live `1/3 FAIL`; real arm `3/3 PASS` |
| live reading `HEALTHY 1/1/0` | `cat /sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/error_stats` (read-only, my own read) | five counters, all `0`; `ls -d /sys/fs/btrfs/*/` → one UUID dir plus `features` |
| counts in the C2 row | `corpus/knowledge/pacman-hook-order-r38.md:13-14`; S212 row `corpus/SOURCES.md:221` | 69 effective / 70 files / 17 Pre / 52 Post / 1 override / 0 masks / 0 AbortOnFail / 14 NeedsTargets; 67 system + 3 operator files |
| HO1-HO7 wording | `corpus/knowledge/pacman-hook-order-r38.md:21-27` | each rule read; my one-line summaries track the row text |
| cited line ranges hold in the pinned snapshots | `.ufo/waves/round-38/sources/hook.c:443-455` (`strncmp`, "exclude the suffixes from comparison" :449), `:540` (`alpm_list_last(handle->hookdirs)`), `:588-590` (`skipping overridden hook`), `:118-122` (triggerless mask), `:629-631` (`ret != 0 && … PRE_TRANSACTION → cleanup`), `:636-641` (msort + triggered), `:660-669` (`abort_on_fail`); `trans.c:201-204` (`ALPM_ERR_TRANS_HOOK_FAILED`), `:237-239` (Post after `transaction completed`); `alpm-hooks.5.asciidoc:35-39` (custom dirs, default `{sysconfdir}/pacman.d/hooks`, "ordering ignores the suffix"), `:87-89` (AbortOnFail PreTransaction only); `alpm.c:56-62` (hookdirs list head) | all present at the cited lines |
| round-19 `[inf]` target line | `sed -n '37p' corpus/knowledge/boot-writers-r19.md` | `- Shadowing: … [inf] The /etc copy is the operative one (S008; precedence per S007; pacman.conf HookDir not captured [unk]).` |
| round-26 promotion condition line | `sed -n '243p' corpus/README.md` | `- Storage integrity is a frontier area, not Core: it becomes Core only after a read-only census arm reads it (shape proposed in …` |

## Findings

1. **The authored after-receipts are not committed.** `git status --porcelain` lists
   `?? .ufo/waves/round-38/after/` at HEAD `5edb6c2`, so both receipts the draft cites
   (`c1-after-52ffd65.json`, `c2-after-1fe28e7.json`) exist on disk but are untracked. The draft cites
   the paths as receipts, not as commits; if the index must only cite tracked bytes, those two rows
   need the receipts committed first.
2. **No author after-receipt exists for the QUALITY-82 conjunct.** `.ufo/waves/round-38/after/`
   contains only the two v1 receipts, and the amendment (`SCORECARD.md:2133`, bullet `:2142-2152`)
   itself says the q82 counter was added after them. Every q82 receipt in the tree is a wave/seat artifact
   (`.ufo/waves/round-38/w1/…`, untracked) or a control. The draft therefore records the conjunct as
   required and states, dated, that no q82 author receipt is committed — it does not claim a q82 pass.
3. **The round-19 `[unk]` is now answerable, not just the `[inf]`.** The line records "pacman.conf
   HookDir not captured [unk]"; `/etc/pacman.conf` carries no `HookDir` directive
   (`grep -n HookDir /etc/pacman.conf` → no match, my read), and the pinned S209 text supplies the
   default: `alpm-hooks.5.asciidoc:35-37` — "additional custom directories specified in
   linkman:pacman.conf[5] (the default is +{sysconfdir}/pacman.d/hooks+)". The installed
   pacman.conf(5) agrees: `/usr/share/man/man5/pacman.conf.5.gz` — "The default is
   /etc/pacman.d/hooks". I put this in the draft as a narrowing, with the S209 lines.
4. **The census exit code is not evidence for this arm.** Every receipt leg shows `census_exit 2`
   (fixture and live alike), so the host rollup is `BLOCKED` on some other plane at the measured
   revision. Verdict-neutrality is what `six_planes_all == 1` and the unchanged rollup terms establish;
   I phrased the draft that way and did not cite exit 0. I did not investigate the exit-2 cause (out of
   item scope, and rerunning the census is not my job).

## Not done (limits)

- No counter run, no `--selftest`, no mutation of any artifact: all numbers above are read from
  committed tools/receipts or, where stated, from my own read-only reads.
- No live `pacman`/transaction behaviour measured; HO6's boot consequence stays `[inf]` inside the entry
  and the draft does not upgrade it.
- No review verdict on HO1-HO7 (that is the amendment's separate reviewer obligation); the draft cites
  those rows as content.
- No scratch directory was needed: no clone, fixture or mutant was made, so nothing under
  `/fast/scratch/hyaku/tsukuroi-r38/DraftReadme/` was created or left behind.

## Proposed text (exact; append at end of `corpus/README.md`)

```markdown
## Round 38 — storage arm in the census; effective ALPM hook order

Append-only; the coverage map and Frontier bullets above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `../tools/tsukuroi-census.sh` (round-38 addition, C1 `probe_storage_arm`) | The verdict-neutral storage-integrity arm that the round-26 Frontier bullet made the condition for Core: one `STORAGE btrfs-device-stats state=HEALTHY/DEGRADED/BLOCKED filesystems=N devices=N nonzero=N [detail=…]` line, printed after the DRIFT line and before the rollup, built from the five counters (`write_errs`, `read_errs`, `flush_errs`, `corruption_errs`, `generation_errs`) of every `<fsid>/devinfo/<devid>/error_stats` under `TSUKUROI_BTRFS_SYSFS` (default `/sys/fs/btrfs`, sysfs 0444, no privilege); BLOCKED on a filesystem without `devinfo` or an unreadable or malformed `error_stats`, DEGRADED when a stored lifetime total is non-zero, HEALTHY otherwise and for an absent sysfs (0/0/0); `nonzero` counts (device, counter) pairs above zero; six hermetic selftest cases (`storage-absent`, `storage-zero`, `storage-nonzero`, `storage-malformed`, `storage-duplicate`, `storage-no-devinfo`); no PLANE text, rollup term or exit code changes | `../tools/score-storage-arm-r38.py` (sha256 `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218`, predicate `fixtures_matched == 10 and live_match == 1 and six_planes_all == 1`, PASS at `52ffd65`, receipt `.ufo/waves/round-38/after/c1-after-52ffd65.json`); verdict rules SH1/SH2 of `knowledge/storage-health-r26.md` (S128, S133); required QUALITY-82 conjunct `../tools/score-storage-arm-r38-q82.py` (sha256 `a183ff580cb92cdd276a5720adb54336e7e247c9bd7c81058065e706d62d99e3`) |
| `knowledge/pacman-hook-order-r38.md` | The host's effective ALPM hook order at pacman `54d9411`: 69 effective hooks from 70 files — 17 PreTransaction, 52 PostTransaction, one same-name override, 0 triggerless masks, 0 `AbortOnFail`, 14 `NeedsTargets` — plus rules HO1-HO7: suffix-ignoring bytewise name order with the shorter name first on a tie (HO1), last-directory-first search where the first file seen per name wins and the system directory is the list head (HO2), a triggerless file as the supported mask (HO3), `AbortOnFail` as the only Pre-phase abort with the remaining Pre hooks skipped (HO4), a parse or validate failure stopping the transaction before any Pre hook runs (HO5), Post hooks only after a completed commit with their result ignored (HO6), and a phase's order as the candidate subset whose triggers matched (HO7) | S208 `hook.c` (`_alpm_hook_cmp` :443-455, `_alpm_hook_run` :532-683), S209 `alpm-hooks.5.asciidoc` :35-39 and AbortOnFail :87-89, S210 `trans.c` :201-204 and :212-240, S211 `alpm.c` :56-62, all at pacman commit `54d9411`; S212 own-work capture `.ufo/waves/round-38/frozen/hooks-capture/` (70 files, MANIFEST sha256 `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`); `../tools/check-hook-order-r38.py` (sha256 `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8`, 69/69 rows, `source_ok 1`, receipt `.ufo/waves/round-38/after/c2-after-1fe28e7.json`) |

### Frontier notice — round 38

The round-26 condition at `corpus/README.md:243` ("it becomes Core only after a read-only census arm
reads it") is met. `probe_storage_arm` (`../tools/tsukuroi-census.sh:1848`) reads the btrfs per-device
error counters on every census run and prints the verdict-neutral `STORAGE` line (`:3007-3008`; the arm's
bytes are one file at `52ffd65` and at HEAD, sha256
`8e0084f67ad4783a980d5c2eaba453f51f1fc5d75408a1c9021a7249ac9aba1c`), and
`../tools/score-storage-arm-r38.py` scores that arm under its frozen predicate: 10/10 fixtures matched,
`live_match 1`, `six_planes_all 1`, PASS (`.ufo/waves/round-38/after/c1-after-52ffd65.json`). Storage
integrity therefore joins the coverage map as Core ground.

The promotion is coverage, not health. On this host the arm currently reads `STORAGE
btrfs-device-stats state=HEALTHY filesystems=1 devices=1 nonzero=0`
(`/sys/fs/btrfs/1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/error_stats`, five zeros, read
2026-10-26), a stored lifetime total that dates nothing (SH2); disk-space runway stays with mori, and
scrub runs, counter resets, profile changes and firmware updates stay operator-owned.

Two counter conditions bound the claim, and the second is the stronger. The v1 counter drives the arm
through its `TSUKUROI_BTRFS_SYSFS` override and its live leg has one constant answer here, so a
fixture-gated arm scores it PASS 10/10 (control `.ufo/waves/round-38/controls/controls-q82.jsonl`). The
pre-seat amendment's QUALITY-82 conjunct `../tools/score-storage-arm-r38-q82.py` must therefore pass
too: it runs the census with no override inside `unshare -rm` with a per-run random tree bind-mounted
over `/sys/fs/btrfs` (predicate `ns_views_matched == VIEWS and ns_available == 1`), under which the
fixture-gated (0/3) and cached-live (1/3) controls fail and the real arm passes 3/3. C1 counts as
verified only with that conjunct's receipt at the measured revision; at drafting (2026-10-26, HEAD
`5edb6c2`) no q82 author receipt is committed under `.ufo/waves/round-38/after/`, so this section
records the conjunct, not its pass.

The same wave source-backs the round-19 override reading. `boot-writers-r19.md:37` keeps its `[inf]`
("The /etc copy is the operative one") as written; HO2 supplies the rule it inferred — hook directories
are searched from the last list entry to the first, the first file seen per name wins, and the system
directory is the list head (S208 `hook.c:540`, `:588-590`; S211 `alpm.c:56-62`) — so
`/etc/pacman.d/hooks/90-mkinitcpio-install.hook` replaces the `/usr` copy of that name. The `[unk]` in
the same line narrows as well: `/etc/pacman.conf` carries no `HookDir` directive, and S209 makes custom
directories those specified in pacman.conf with `{sysconfdir}/pacman.d/hooks` as the default
(`alpm-hooks.5.asciidoc:35-37`). Nothing in this section authorizes a package, hook or transaction
action: the entry's rows are read from files and source, never from a run, and the per-row HO1-HO7
reviewer verdicts required by the amendment are a separate, wave-side condition.
```

Artifacts: this report; `.ufo/waves/round-38/w1/DraftReadme/receipts.txt` (the commands and their
outputs quoted above).
