VERDICT: supports

# C1ExecFinalCounter — C1 final counter re-run (round 44, wave w2, item C1-1)

Seat: `C1ExecFinalCounter` (leaf). Item: run the frozen C1 counter through `tools/run-receipt.py` at the
integrated tip and once at base, report every field including the wrong ids, confirm the counter sha256.
Measured at 2026-10-27T00:54:44Z–00:56:24Z on `plazir27`. No lane mutation, no git/jj command that writes,
no install/update, no service/mount/sysfs action, no btrfs scrub. All scratch under
`/fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalCounter` (removed on exit); `/tmp` never used as evidence.

## 1. Counter identity (sha256 confirmation)

| Where | `tools/score-scrub-arm-r44.py` sha256 |
|---|---|
| working copy, lane | `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388` |
| `git show 1d2afffeaedbb553d951f53c9edb0190e345b1ab:…` (tool revision, freeze commit) | `1409a5fd…9536388` |
| `git show 8eee79db608b5815c325a5af7cbfdeac50eda9f4:…` (measured revision) | `1409a5fd…9536388` |
| `git show 3a1c6b5c958c4f289a8b12551f96d843877b700e:…` (lane master at report time) | `1409a5fd…9536388` |
| `git show 98020ece0674e0b569ee23aed10ffbee355b248e:…` (base) | absent (`e3b0c442…b855`, empty) |

**Confirmed:** the frozen counter is `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388`, and each
receipt's header `tool_sha256` field repeats it. The counter does not exist at base, so the base run is the same
frozen bytes executed from `--tool-revision 1d2afffe` against base's census; the receipt names both revisions.

Census bytes scored: base `98020ece…` → `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9`;
tip `8eee79db…` → `2ef86357c14aec3f4346f7ac9013cdda3b399d38bae67f4ca2e286e5a37c4639` (identical at current
master `3a1c6b5c…`, see §5c).

## 2. Commands run (exact)

Tip (receipt `.ufo/waves/round-44/w2/C1ExecFinalCounter/c1-final.jsonl`):

```
python3 tools/run-receipt.py --revision 8eee79db608b5815c325a5af7cbfdeac50eda9f4 \
  --tool-revision 1d2afffeaedbb553d951f53c9edb0190e345b1ab \
  --out …/w2/C1ExecFinalCounter/c1-final.jsonl \
  -- tools/score-scrub-arm-r44.py --revision '{rev}' --scratch /fast/scratch/hyaku/tsukuroi-r44/C1ExecFinalCounter/s
```

Base (receipt `…/C1ExecFinalCounter/c1-base-final.jsonl`): same, `--revision 98020ece0674e0b569ee23aed10ffbee355b248e`.
Wall: tip 61 s, base 38 s. Receipt sha256: `c1-final.jsonl` `98a2609e7d2985ac0bbe78d3669a42d9c1c4f88fa7fc4f0d841dddeaf04f5b99`;
`c1-base-final.jsonl` `bb70465653cbd598b4bfa7c86c6134d62f5a46677ab7edf49d551c7760faf987`.

## 3. Tip `8eee79db608b5815c325a5af7cbfdeac50eda9f4` — every receipt field

Header: `receipt 1`; `revision 8eee79db608b5815c325a5af7cbfdeac50eda9f4`; `tool_revision 1d2afffeaedbb553d951f53c9edb0190e345b1ab`;
`tool tools/score-scrub-arm-r44.py`; `tool_sha256 1409a5fd…9536388`; `started_utc 2026-10-27T00:54:44Z`;
`argv` = the command in §2; `lane_branches` = 10 refs at run time (`master 0f8c07a5035cc9469f59ae41726335388b1cbcac`,
plus `hyaku/s3-ready66-tsukuroi`, `hyaku/s3-tsukuroi-r24-author`, four `round20-*`, three `round23/*`).

Counter line:

| field | value |
|---|---|
| `counter` | `score-scrub-arm-r44` |
| `revision` | `8eee79db608b5815c325a5af7cbfdeac50eda9f4` |
| `cases` | `16` |
| `correct` | `16` |
| `wrong` | `[]` (no wrong ids) |
| `identity` | `["1000","1000","1000"]` |
| `identity_ok` | `1` |
| `wired.want` | `SCRUB btrfs-scrub-record state=RECORDED dir=present records=2 tmp=2 sockets=1 unreadable=2 orphan=0 limited=4 timers=1 detail=15c955ed:18:speed_max=93723166,15c955ed:8:speed_max=57297228,1d02a454:25:speed_max=20862330,1d02a454:6:speed_max=73132126` |
| `wired.got` | the same single line |
| `wired.rc` | `2` (informational, see §5b) |
| `wired_ok` | `1` |
| `live.want` | `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0` |
| `live.got` | `["SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0"]` |
| `live.wired` | `1` |
| `live_agree` | `1` |
| `selftest_pass` | `1` |
| `selftest_line` | `TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)` |
| `selftest_failures` | `[]` |
| `selftest_r44` | `16` |
| `channels_open` | `["mount table","uid_map","script path /mnt/census-lib.sh"]` |
| `predicate` | `cases == 16 and correct == 16 and identity_ok == 1 and wired_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r44 >= 6` |
| `verdict` | `PASS` |

Footer: `receipt_end 1`; `exit_code 0`; `timed_out false`; `stderr_tail ""`; `finished_utc 2026-10-27T00:55:41Z`.

Every predicate conjunct is met: 16/16, `identity_ok 1`, `wired_ok 1`, `live_agree 1`, `selftest_pass 1`,
`selftest_r44 16 ≥ 6` → exit 0.

## 4. Base `98020ece0674e0b569ee23aed10ffbee355b248e` — every receipt field

Header as §3 with `revision 98020ece…`, `started_utc 2026-10-27T00:55:49Z`, same `tool_sha256`.

| field | value |
|---|---|
| `cases` | `16` |
| `correct` | `0` |
| `identity` | `["1000","1000","1000"]`, `identity_ok 1` |
| `wired.want` | `SCRUB btrfs-scrub-record state=RECORDED dir=present records=1 tmp=1 sockets=2 unreadable=2 orphan=1 limited=2 timers=0 detail=1d02a454:11:speed_max=63932573,1d02a454:29:speed_max=97458595` |
| `wired.got` | `[]`; `wired.rc 2`; `wired_ok 0` |
| `live.want` | `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0` |
| `live.got` | `[]`; `live.wired 0`; `live_agree 0` |
| `selftest_line` | `TSUKUROI_CENSUS_SELFTEST: PASS (132 cases, 132 passed, 0 failed)`; `selftest_pass 1`; `selftest_failures []` |
| `selftest_r44` | `0` |
| `channels_open` | `["mount table","uid_map","script path /mnt/census-lib.sh"]` |
| `verdict` | `FAIL` |

Footer: `exit_code 1`; `timed_out false`; `stderr_tail ""`; `finished_utc 2026-10-27T00:56:24Z`.

Wrong ids — all 16, every one `rc 127`, `got ""` (function absent at base → `probe_scrub_record: command not found`):

| id | want (drawn per run) |
|---|---|
| `none-dir-absent` | `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0` |
| `recorded-readable` | `… state=RECORDED dir=present records=1 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0` |
| `root-records-unreadable` | `… state=RECORDED dir=present records=1 tmp=0 sockets=0 unreadable=1 orphan=0 limited=0 timers=0` |
| `orphan-records` | `… state=RECORDED dir=present records=2 tmp=0 sockets=0 unreadable=0 orphan=1 limited=0 timers=0` |
| `tmp-beside-record` | `… state=RECORDED dir=present records=1 tmp=1 sockets=0 unreadable=1 orphan=0 limited=0 timers=0` |
| `progress-socket` | `… state=RECORDED dir=present records=1 tmp=0 sockets=1 unreadable=1 orphan=0 limited=0 timers=0` |
| `limited-devices` | `… state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=7 timers=0 detail=1bf5a04d:2:speed_max=510,1bf5a04d:28:speed_max=8041272743,1d02a454:17:speed_max=9292154525,1d02a454:23:speed_max=38,1d02a454:7:speed_max=592587961,c42944ab:28:speed_max=8727558984,c42944ab:9:speed_max=7461503661` |
| `speed-malformed` | `… state=BLOCKED … detail=1d02a454:37:speed-malformed` |
| `speed-unreadable` | `… state=BLOCKED … detail=da164c30:10:speed-unreadable` |
| `dir-unreadable` | `… state=BLOCKED dir=unreadable … detail=dir:unreadable` |
| `dir-not-directory` | `… state=BLOCKED dir=unreadable … detail=dir:unreadable` |
| `timers-enabled` | `… state=NONE dir=absent … timers=4` |
| `timers-unreadable` | `… state=BLOCKED … detail=timers:unreadable` |
| `wrong-types` | `… state=BLOCKED dir=present … detail=progress:not-socket,record:not-regular,record:not-regular,tmp:not-regular` |
| `sysfs-unreadable` | `… state=BLOCKED dir=present records=1 … detail=sysfs:unreadable` |
| `mixed` | `… state=RECORDED dir=present records=2 tmp=0 sockets=0 unreadable=0 orphan=1 limited=0 timers=3` |

This is exactly the declared before-state: `correct 0`, `wired_ok 0`, `live_agree 0`, selftest `PASS 132`,
`selftest_r44 0`, exit 1 — and the base census's own selftest passes 132/132, so the base FAIL is the missing arm,
not broken tooling. Base and tip wired `want` values differ (e.g. `records=2 tmp=2 sockets=1` vs
`records=1 tmp=1 sockets=2`) because the counter seeds `random.Random(os.urandom(16))` per run and mixes the host
fsid (`1d02a454-c549-4a35-b567-89d60902af8e`) in; the values are not reused across runs.

## 5. Kill-rule measurement (declared C1 kill rules, measured here)

### 5a. Live census, both revisions, twice each (independent of the counter)

`bash census-<rev>.sh` (bytes extracted with `git show <rev>:tools/tsukuroi-census.sh`, sha256 verified per §1),
`TMPDIR` in scratch, no namespace. Evidence: `live-census-{base,tip}-run{1,2}.txt` (sha256 `fb4689bf…`,
`cc49f273…`, `010321ee…`, `ccc6427e…`).

| revision | exit | lines | `SCRUB ` lines | rollup lines | stderr |
|---|---|---|---|---|---|
| base run1 / run2 | 2 / 2 | 12 / 12 | 0 / 0 | 1 / 1 | empty |
| tip run1 / run2 | 2 / 2 | 13 / 13 | 1 / 1 | 1 / 1 | empty |

- **Exit code unchanged:** 2 at base and 2 at tip, both runs. No change.
- **Rollup byte-identical** at base and tip:
  `TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)`.
- **PLANE lines:** all five verdict words and every field name/order identical. The only differing bytes are the
  header timestamp and, inside `PLANE drivers`, the live counters `C5_pswp` numerator,
  `C6_psi_some_avg300`, `C6_psi_full_avg300`, `C6_psi_full_total_us`, `C6_avail_kb`, `C6_shmem_kb`. These drift
  **between two runs of the same revision** (base-vs-base `C5_pswp` `551431` → `551468`, `C6_avail_kb`
  `17412216` → `18119624`; tip-vs-tip `551443` → `551475`, `17787308` → `17890252`), i.e. host noise, not a
  revision effect. Every other line (`PLANE packages`,
  `systemd`, `journal`, `update-safety`, `oom`, both `HANDOFF`, `DRIFT`, `STORAGE`) is byte-identical base vs tip.
- **New line placement:** exactly one added line, the `SCRUB` line, sitting between `STORAGE btrfs-device-stats`
  and the rollup (`wired_check` enforces `storage < scrub < rollup` and exactly one of each: `wired_ok 1`;
  `wired_check` at `tools/score-scrub-arm-r44.py:503-510`, called with the full census output).
- **Live value:** `state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0`
  (this host has no `/var/lib/btrfs`; the live leg therefore exercises only the absent branch — RECORDED/BLOCKED
  are the 16 namespace cases' job, and they all pass).
- **Arm writes no file in live mode:** `strace -f` over the tip live census
  (`-e trace=openat,open,mkdir,mkdirat,creat,unlink,unlinkat,rename,renameat,symlink,symlinkat,chmod,fchmodat,utimensat`)
  shows the nine accesses to `/var/lib/btrfs`, `/sys/fs/btrfs/…/scrub_speed_max` and
  `timers.target.wants` are **all `O_RDONLY`** (evidence `strace-scrub-paths-tip.txt`, sha256 `939fdb01…`), with no
  `O_WRONLY`/`O_RDWR`/`O_CREAT`/`mkdir`/`creat`/`unlink`/`rename` on any of them. Write-ish opens elsewhere in
  the log belong to pre-existing planes (pacman `-Qkk` gnupg lock attempts, all `EACCES`; nvidia device nodes) and
  to `/proc/self/task/<tid>/comm`, none of them the scrub arm.
- **No host path created:** `ls -la /etc/systemd/system/timers.target.wants` and `ls -la /var/lib/btrfs` snapshot
  before and after are identical (`diff` clean, `SNAPSHOT-UNCHANGED`); `/var/lib/btrfs` is still absent; the
  census runs left `TMPDIR` empty (`find … -mindepth 1` = 0 entries) at both revisions, both runs.

### 5b. `wired.rc 2` is informational, not a signal

`wired_ok` is computed only from the SCRUB line's content, count and position (`wired_check`), not from the
namespace census's exit code; the full census in the fixture view exits 2 because other planes read BLOCKED/DEGRADED
in that view. Base also returns `wired.rc 2` while producing no SCRUB line, so the field does not discriminate base
from tip and must not be read as one. The declared kill rule concerns the **live** exit code, which is 2 at both
revisions (§5a).

### 5c. The lane moved during w2; the scored bytes did not

Each receipt's `lane_branches` records `master 0f8c07a5035cc9469f59ae41726335388b1cbcac` at run time; lane master
is now `3a1c6b5c958c4f289a8b12551f96d843877b700e` (`0f8c07a5` w2 spec → `8728e8bc` docs → `efbffe08` → `3a1c6b5c`
registry). `tools/tsukuroi-census.sh` is byte-identical at `8eee79db…`, `0f8c07a5…` and `3a1c6b5c…`
(`2ef86357…`), and the counter is byte-identical too, so the PASS measured at the named revision describes current
master's census bytes. The measured revision remains the immutable `8eee79db…`.

## 6. Advisories (for the L1 / closure; none blocks the C1 predicate)

1. **Claim-row prose is stale against the shipped selftest.** The frozen C1 row (`SCORECARD.md:2760`) still says
   "plus nine `R44-C1` selftest cases (132 → 141)"; the measured surface is **148 cases with sixteen `(R44-C1)`
   labels** (`selftest_r44 16`), which `SKILL.md:4209` ("148 cases, sixteen `(R44-C1)` labels") and
   `corpus/lessons/round-44.md:46` record, and which this seat's frozen claim summary states as "132 -> 148 after w1
   hardening". No refinement is appended inside the `## Round 44 — declaration` section (grep for
   `148|141|hardening|refinement` over lines 2746-2787 matches only the stale row). The predicate is
   `selftest_r44 >= 6`, so the claim passes; the number mismatch is a documentation matter for closure, and the
   declaration must not be rewritten after data.
2. **`live` leg is weak on this host by construction:** `/var/lib/btrfs` is absent, so live only proves the absent
   branch agrees with the independent Python walk; the rich branches are namespace-only (declared, and consistent
   with the recorded QUALITY-90 open channels `mount table`, `uid_map`, script path).
3. **Channels still open as declared:** `channels_open` reports all three; nothing here narrows them. The base/tip
   paired evidence in §5a is also the cheapest available guard against a cached-answer live leg (a stale cached line
   would have had to be `state=NONE dir=absent` at base too, where the arm does not exist — base printed no line).

## 7. Proposed text (measured outcome for the L1 to place)

> **C1 (coverage), measured at `8eee79db…` (receipt `c1-final.jsonl`):** the frozen counter
> `tools/score-scrub-arm-r44.py` (sha256 `1409a5fd…9536388`) exits 0 — `cases 16`, `correct 16`, `wrong []`,
> `identity_ok 1`, `wired_ok 1` (one SCRUB line, equal to the oracle, between STORAGE and the rollup),
> `live_agree 1`, `selftest_pass 1` (`PASS (148 cases, 148 passed, 0 failed)`), `selftest_r44 16`; the same frozen
> bytes at base `98020ece…` exit 1 with `correct 0`, `wired_ok 0`, `live_agree 0`, `selftest PASS 132`,
> `selftest_r44 0`, and all 16 wrong ids at `rc 127` (no `probe_scrub_record`). Kill rules did not fire: the live
> census exits 2 at both revisions, the rollup line is byte-identical, the five PLANE lines keep their verdicts and
> fields (only live host counters drift, and they also drift base-vs-base), the sole added line is the SCRUB line
> after STORAGE, and strace shows the live arm opens only `O_RDONLY` and creates nothing. Target met by the declared
> command. Disclosed: the claim row's "nine … (132 → 141)" predates the wave-1 hardening (shipped 148/16, recorded
> in `SKILL.md:4209` and `corpus/lessons/round-44.md:46`); the live leg exercises only the absent branch on this
> host.

## 8. Files

Written (only these): `.ufo/waves/round-44/w2/C1ExecFinalCounter.md`;
`.ufo/waves/round-44/w2/C1ExecFinalCounter/{c1-final.jsonl,c1-base-final.jsonl,live-census-base-run1.txt,live-census-base-run2.txt,live-census-tip-run1.txt,live-census-tip-run2.txt,strace-scrub-paths-tip.txt}`.
No lane tracked file touched; no git/jj mutation; scratch removed.
