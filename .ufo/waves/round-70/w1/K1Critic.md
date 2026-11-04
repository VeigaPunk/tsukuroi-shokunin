# K1Critic — round 70, wave w1 (falsification only)

Seat: K1Critic, L2 critic, hyaku run 15. Declaration read at frozen commit `1710bd74`
(SCORECARD.md "Round 70 — declaration"); base `b2aa0be0`; HEAD at the time of this review
`84e013a7`. Host facts re-read live, read-only. Every command below names an absolute path or
runs from an extracted base archive under
`/fast/scratch/hyaku/tsukuroi-r70/K1Critic/` (tree deleted before yield). No lane write, no
git mutation, no pacman, no service action. Nothing from
`/home/vgpnk/Projects/shokuknow/merge/tsukuroi/` was read.

Summary: six receipts re-run, **three reproduce in full** (c, e, f); three carry a value that
cannot be reproduced (a, b, d). C1 is reachable on the real four snapshots, but its
statement-substance clause verifies vacuous and host-opinion sentences. C2's frozen predicate
admits a line that reads nothing — that is the fatal defect. Two axis harms.

---

## 1. Premise recheck — receipts (a)-(f)

### (a) Four snapshots committed byte-exact before the declaration text — **NOT REPRODUCED**

Premise: ".ufo/waves/round-70/before/src" holds four snapshots + `SHA256SUMS` + `SOURCES.json`
before the declaration text (SCORECARD "Round 70 — declaration" (a)).

Command:
```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 1710bd74 \
    .ufo/waves/round-70/before/src | tar -x -C "$S/src1710"
cd "$S/src1710/.ufo/waves/round-70/before/src" && sha256sum -c SHA256SUMS
python3 -c 'import json;print(sorted(json.load(open("SOURCES.json"))["snapshots"]))'
```

Observed at `1710bd74`:
```
<dir>: FETCH.txt SHA256SUMS SOURCES.json xfs.rst xfs_stats.c xfs_sysfs.c     # no health.c
sha256sum -c SHA256SUMS -> xfs.rst OK / xfs_stats.c OK / xfs_sysfs.c OK, rc 0   # 3 files, 230-byte manifest
SOURCES.json keys -> ['xfs.rst','xfs_stats.c','xfs_sysfs.c']                    # 3, no health.c
FETCH.txt -> route 1 for the three kernel files only; no xfsprogs/health.c URL
```
`git show 1710bd74:.../src/SHA256SUMS` is a 3-line file. The 4-snapshot `SHA256SUMS`
(305 bytes) and the `health.c` map entry arrive only in `84e013a7` ("the declaration cited four
snapshots; three were committed"). At HEAD the fourth file and map entry exist and
`sha256sum -c` is rc 0 for all four, and `grep -c health FETCH.txt` is **0** at HEAD as well:
the fourth snapshot's first-route fetch is recorded nowhere (`SOURCES.json` only).

Consequence: **serious (provenance/freeze).** Receipt (a) is false at its own frozen revision:
at `1710bd74` a health.c row could not verify (`snapshot-absent`), and the receipt's
"`sha256sum -c` rc 0" is true only because the manifest had quietly lost the fourth file.
The round-69 D4 freeze-ordering defect is answered for the counter/predicate, not for the
source bytes.

### (b) Host capture values — **ONE VALUE NOT REPRODUCED**

Premise (declaration (b), and the frozen claim context): "error subtree 7 regular files per
filesystem with `-1` retry values"; two xfs mounts; per-fs `stats/stats` 34 lines 0444;
`stats_clear` 0200 per fs and globally; `/proc/fs/xfs/stat` a symlink to the global stats;
four log files per fs; `xfs_spaceman -c health` prints the not-collected message.

Command (read-only; same commands `before/capture.sh` uses):
```
uname -r; pacman -Q linux xfsprogs; findmnt -t xfs -o TARGET,SOURCE,FSTYPE
awk '$3=="xfs"' /proc/self/mounts; readlink /proc/fs/xfs/stat
for d in /sys/fs/xfs/*/; do wc -l < "$d/stats/stats"; stat -c %a "$d/stats/stats"; done
stat -c '%a %n' /sys/fs/xfs/*/stats/stats_clear /sys/fs/xfs/stats/stats_clear
for d in /sys/fs/xfs/*/log/;    do find "$d" -maxdepth 1 -type f | wc -l; done
for d in /sys/fs/xfs/*/error/;  do find "$d" -type f | wc -l; done
xfs_spaceman -c health /tmp; xfs_spaceman -c health /fast
```
and from the committed bytes:
```
python3 - (parse before/host.txt "## error subtree" block)
```

Observed: kernel `7.2.11-arch1-1`, `xfsprogs 7.2.0-1`; `findmnt` 2 rows
(`/dev/nvme1n1p1 /tmp`, `/dev/nvme1n1p2 /fast`); mount table identical; `/proc/fs/xfs/stat ->
/sys/fs/xfs/stats/stats`; per-fs stats 34 lines, mode 444; `stats_clear` 200 on both fs and on
`/sys/fs/xfs/stats/stats_clear`; log files **4 / 4**; error subtree **9 / 9**; health message
on both mounts.

The committed `before/host.txt` itself lists **9** regular files per error subtree
(`fail_at_unmount` + `metadata/{default,EIO,ENODEV,ENOSPC}/{max_retries,retry_timeout_seconds}`),
and the live host reads **9 / 9**. The declaration's "7" matches neither.

Consequence: **serious.** The frozen C2 field `error=<n>` is pinned in the claim context to a
number the claim's own committed capture contradicts. A verifier holding "7" rejects a correct
census printing 9; a verifier holding 9 must contradict the frozen context. The predicate's
phrase "equal to the enumerated regular-file counts" does not say whether `default/` is
enumerated, so 7 and 9 are both defensible — the predicate is under-specified on a field it
measures.

### (c) Held-ground sweep — **REPRODUCED**

Command: `git grep -c -i xfs b2aa0be0 -- 'corpus/*' PROVINCE.md SKILL.md`; the seven
`git grep -F -c` patterns; `git ls-tree -r --name-only b2aa0be0 | grep -i knowledge.*xfs`;
`git show b2aa0be0:corpus/knowledge/storage-health-r26.md | grep -c '^## SH'`.

Observed: 18 lines / 14 files; `sys/fs/xfs`, `stats_clear`, `log_head_lsn`,
`reserve_grant_head_bytes`, `fail_at_unmount`, `xfs_spaceman`, `max_retries` each **0**;
xfs knowledge notes **0**; SH1-SH6 present. No xfs row in `corpus/SOURCES.md` at base
(`git show b2aa0be0:corpus/SOURCES.md | grep -ci xfs` -> 0). Ground is new by the lane's own
sweep.

Consequence: none.

### (d) Do-nothing controls — **ONE VALUE NOT REPRODUCED**

Command: `git cat-file -e b2aa0be0:<path>`; `git grep -c '^| XS[0-9]'`; `git show
b2aa0be0:tools/tsukuroi-census.sh | grep -c 'XFS xfs-stats'`; `git grep -c probe_xfs`;
`git archive b2aa0be0 | tar -x -C "$S/base"` then
`cd "$S/base" && TMPDIR="$S/selftest-tmp" bash tools/tsukuroi-census.sh --selftest`;
registry row count; knowledge-note count; `git show b2aa0be0:tools/tsukuroi-census.sh | grep -c validate`.

Observed: note `cat-file` rc **128**, counter rc **128**; `^| XS` rows **0**; `XFS xfs-stats`
**0**; `probe_xfs` **0**; selftest `PASS (196 cases, 196 passed, 0 failed)` rc **0**; registry
**289**; knowledge notes **87**; `validate` occurrences in the base census **0**.

The receipt's last value, "census validate rc 0", has no named entry point in
`tools/tsukuroi-census.sh` at `b2aa0be0` (grep 0; the phrase also appears in LOG.md:2801 as a
historical summary). It cannot be replayed from the committed bytes.

Consequence: **minor.** Everything else reproduces exactly; one receipt value is unlabeled and
unreplayable.

### (e) Frozen counter + pre-data battery — **REPRODUCED**

Command:
```
git show 1710bd74:tools/count-xs-rows-r70.py | sha256sum        # 65065d9d…4f6f5c == frozen
git show 1710bd74:.ufo/waves/round-70/before/control/build_battery.py > $S/counter/build_battery.py
# only the hardcoded COUNTER path was repointed at the extracted committed counter
XS_BATTERY_SCRATCH="$S/battery" python3 "$S/counter/build_battery.py"
```
Observed: counter sha256 `65065d9d18cea52027619697264de430780e65ff13ab6da2a790c3d2054f6f5c`
(identical at `1710bd74` and HEAD); battery `PASS (8 cases, 8 passed, 0 failed)`, rc 0; every
mutant rc 1, `met=0`; control `6/6 met=1`.

Consequence: none for the literal kill rule. The battery's coverage gap is finding C1-5/6.

### (f) Base live census — **REPRODUCED**

Command: `cd "$S/base" && TMPDIR="$S/census-tmp" bash tools/tsukuroi-census.sh` (base archive,
read-only).
Observed: rc **1**; 15 lines; the rollup line is byte-identical to
`before/census-live-base.txt` (`diff` empty), and the `KERNEL kernel-plane …` line is
byte-identical. `TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=DEGRADED drivers=DEGRADED
journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)`.

Consequence: none. The neutrality baseline is real and replayable.

---

## 2. C1 attacks

### C1-1 Is the ground new? — yes (own sweep)

Premise: "the XFS sysfs storage plane the lane never held". Evidence: receipt (c) reproduced;
registry has 0 xfs rows at base; 0 knowledge notes matching xfs; the seven plane tokens 0 hits.
The C1 note itself was absent at base (`cat-file` 128) and at the declaration commit.

Consequence: none.

### C1-2 Are the six rows rules rather than host opinions? — **the counter cannot tell**

Premise: "rows `XS1`–`XS6`" state the storage plane; the frozen counter's statement-substance
clause is ">= 3 distinct non-stopword tokens (len >= 4)" shared with the row's snapshot text
(counter lines 94-103, 160-161).

I built four fixture mirrors around the **real** four snapshots (real hashes, real
`SOURCES.json` URLs, synthetic binding rows S901-S904), then ran the frozen counter:

| fixture statement (row XS2 on real `xfs_stats.c`) | counter |
|---|---|
| "The xfs_stats_format function walks the xstats table and sums per_cpu_ptr counters for every named group." (5 shared) | ok |
| "The stats file prints one summary line per named counter group with summed per-CPU counters." (natural, 15 words) | ok |
| "The stats file prints one summary line for every named counter group, with each column a summed per-CPU value." (natural, 19 words) | **fail statement-tokens=2** |
| "The stats group and the xstats group are described in the stats table source line." (vacuous, 15 words) | ok |
| "On this host the xstats xfs_stats_format output reports thirty four group lines per mounted filesystem." (host opinion) | ok |

Two full mirrors:
```
realfix-substantive: XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4 met=1 rc 0
realfix-opinion    : XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4 met=1 rc 0
    (XS1/XS2 are host claims: "thirty four group lines per mounted filesystem",
     "counters unchanged since boot on both filesystems"; the other four rows are rules)
realfix-vacuous    : 6/6 met=1 rc 0  (XS2 is the content-free token-reuse sentence above)
```

Observed: the clause is a lexical-overlap test, not a rule test. A vacuous sentence and a
host-fact sentence verify exactly like a rule; a correct 19-word prose sentence fails while a
near-identical 15-word variant passes. The declaration's own description ("one summary line per
named counter group with summed per-CPU counters") sits between these two outcomes depending on
incidental words ("counters", "precision").

Consequence: **serious.** The C1 claim's "six rules" is prose-only; the counting command can be
met by six non-rules. The declaration itself defers "the XS rows are rules, not admitted
propositions" to the next round (`planned`), which is honest — but then the frozen predicate
must not be presented as measuring rule content.

### C1-3 Is the target reachable without the note (do-nothing)? — no

Premise: "the note's ground" must be actual. At `b2aa0be0` and at `1710bd74` the counter prints
`XS_NOTE absent` and exits **128**; `git cat-file -e` rc 128. No note, no target.

Consequence: none. (The do-nothing control is real.)

### C1-4 Does the statement-substance clause have a control that fails it? — yes, but it is not sound

Premise: the battery's `mutant-content-free` claims "statement-substance clause kills filler
prose". Battery output: `PASS mutant-content-free: rc=1 … XS_VERIFIED=0`. So a control exists.

But that filler ("This fixture row records a general claim measured on an earlier occasion.")
shares 1 token with every fixture snapshot. A filler that reuses snapshot vocabulary ("The stats
group and the xstats group are described in the stats table source line.") passes (C1-2 table).
The control therefore proves only that the token threshold rejects a sentence with no source
vocabulary; it does not prove the clause distinguishes rules from filler or host opinion.

Consequence: **minor** as a control-design finding (the clause is disclosed as lexical by its
own text), folding into C1-2's serious consequence.

### C1-5 Score the declaration's kill rule against the battery — **no mutant meets the target**

Premise: "a mutant meeting the target falsifies the counter". Battery: 8 cases, 8 PASS, every
mutant rc 1 / `met=0` (`content-free` 6 rows/0 verified; `any-registered-id`, `digest-swap`,
`quote-absent`, `short-statement`, `duplicate-id` 6/5; `five-rows` 5/5). No mutant meets 6/6.
The literal kill rule does not fire.

However, a ninth mutant class not in the battery — the host-opinion mirror and the vacuous
mirror above — **meets the target** (`6/6 met=1 rc 0`). Under the declaration's own words
("a mutant meeting the target falsifies the counter"), this falsifies the counter's ability to
enforce the row's substantive content, though not the eight enumerated mutants.

Consequence: **serious** (same root as C1-2).

### C1-6 Does the battery's control prove the target reachable with the REAL snapshots? — **no; reachability proved separately**

Premise: "the pre-data battery's control must read 6/6 rc 0" as evidence the target is
reachable. `build_battery.py` lines 19-54 build four **synthetic** snapshots
(`s_stats.c`, `s_sysfs.c`, `s_docs.rst`, `s_health.c`) whose text embeds the English words the
control rows use ("fixture documentation", "the metadata class applies…", "each filesystem
exposes an error handler class directory"). Those bytes are not the real four.

Therefore the control is a fixture-only proof. The sharp test — a plausible row per real
snapshot — I ran myself (C1-2): a deliberate substantive 6-row mirror reads
`6/6 met=1 rc 0` on the real snapshots. So reachability is real, but it is **not** what the
battery's control establishes; and the real C files are terse enough that a natural prose row
failed with `statement-tokens=2`.

Consequence: **minor** (the counter is reachable; the battery overstates what its control
proves).

### C1-7 The second-route admission gate is outside the predicate

Premise: "a second route is required from the wave's scout before any row is admitted".
`grep -E 'fetch|route|FETCH' tools/count-xs-rows-r70.py` -> **none**; the counter never reads
`FETCH.txt` or the scout report. The gate is met in practice (`w1/S1Scout.md`:
`ROUTE2_OK=4/4, MATCHED=4/4`, including the xfsprogs tarball for `health.c`), but a note with
one route would verify 6/6 identically.

Consequence: **minor.** An admission gate the counting command cannot see is a promise, not a
predicate.

---

## 3. C2 attacks

### C2-1 Can the enumerated counts be satisfied WITHOUT reading the host? — **yes (fatal)**

Premise: the line must report distinct xfs mount sources, their `/sys/fs/xfs/<dev>` presence,
readable `stats/stats` files, regular files under `error/` and `log/`, and a closed detail
vocabulary.

The frozen predicate binds only: label present; one live line; every field once in contract
order; `mounts == distinct xfs source count findmnt -t xfs reports`; `stats <= present`;
`error`/`log` "equal to the enumerated regular-file counts"; rollup/exit identical to base;
selftest PASS N>=206 with >=10 `R70-C2`.

It contains **no** invariant tying `present`/`absent`/`unreadable` to the host, no
`present + absent + unreadable == mounts`, and no named independent enumerator for `error`/`log`
("enumerated" is passive; the counting command is the census itself). A script that reads
nothing satisfies every literal field on this host:

```
$ cat $S/zero-arm.sh
#!/usr/bin/env bash
echo "XFS xfs-stats mounts=2 present=0 absent=0 unreadable=0 stats=0 error=0 log=0 detail=none"
$ bash $S/zero-arm.sh
XFS xfs-stats mounts=2 present=0 absent=0 unreadable=0 stats=0 error=0 log=0 detail=none
$ findmnt -t xfs -o SOURCE -n | sort -u | wc -l
2
```

Check: label 1; fields in order; `mounts=2` equals findmnt today; `stats 0 <= present 0`;
`error`/`log` equal the zero files this "census" enumerated; detail is in vocabulary; it cannot
change the rollup or rc. The declared kill rules — echo an unvalidated name, change rollup/exit,
`mounts` disagree with the mount table, fewer than 10 labelled cases — none fire.

The hole also admits an **overcount**: `for d in /sys/fs/xfs/*/` yields three directories on this
host (`nvme1n1p1`, `nvme1n1p2`, and the global `stats` kobject). A census that counts `stats` as
a "present" device reports `present=3` with `mounts=2`; no clause rejects it, and
`/sys/fs/xfs/stats/stats` also matches the first-line regex, so a naive stats glob reads
`stats=3` — that one is caught by `stats <= present`, but `present=3` itself is not.

A genuinely **fixture-only** census (overrides set to synthetic fixtures) is caught only by the
`mounts` field, because `findmnt` sees 2; that is the single real external binding.

Consequence: **fatal.** The C2 claim ("reads their presence, stats, error and log enumerations")
is not falsifiable by the frozen predicate: a constant line that reads nothing meets it. The
smallest safe correction is to bind `present` to an independent count of
`/sys/fs/xfs/<dev>` directories for the mount sources (excluding the global `stats` kobject),
require `present + absent + unreadable == mounts`, require `error`/`log` to equal a
verifier-side `find`, and make `detail` non-`none` whenever `present < mounts` or any count is
zero while the host has files. If in-round predicate amendment is barred, the verifier must
adopt and state the independent enumeration; the literal predicate text as frozen does not.

### C2-2 Is `mounts == findmnt` a real invariant under LUKS / symlinked sources? — the COUNT holds, the PRESENCE does not

Premise: "distinct xfs mount sources from the mount table" and "`mounts` equal to the distinct
xfs source count `findmnt -t xfs` reports in the same capture".

On this host both are 2 (`/dev/nvme1n1p1`, `/dev/nvme1n1p2`) and the census's source of truth
(`TSUKUROI_PROC_MOUNTS`, default `/proc/self/mounts`) agrees with `findmnt`. Count equality
survives a LUKS mapper or a by-uuid source because both sides count distinct sources; what does
not survive is the per-source `<dev>` lookup: for a dm-crypt mount `findmnt` prints
`/dev/mapper/<name>` while the xfs sysfs kobject is named from `sb->s_id` (`dm-N`), and a
by-uuid/by-label source can differ from the kernel device name. The line would then read
`present=0 absent=<mounts>`, which C2-1's predicate accepts without a detail token. No LUKS
device exists on this host, so this is [INFERENCE] from the naming rule, not a live failure.
A same-source-two-targets mount also makes "rows findmnt reports" (2) differ from "distinct
sources" (1) — again a count-vs-distinct ambiguity, not exercised here.

Consequence: **minor** (no local evidence; but the invariant does not protect the field the
claim is about).

### C2-3 Can the line be all zeros and pass? — not literally on this host; every field but `mounts` can be zero

`mounts` is pinned by `findmnt` (2 here), so a live run cannot print `mounts=0` and pass. But
`present=absent=unreadable=stats=error=log=0` with `mounts=2` passes (C2-1), because there is no
sum invariant and the only count compared to anything else is `stats <= present`. A run with an
empty `TSUKUROI_PROC_MOUNTS` would fail `mounts == findmnt`; that is the one guard.

### C2-4 Does adding the line risk the rollup/exit neutrality clause? — **yes, one concrete path**

Premise: "never a rollup term and never an exit-code input"; rollup and rc identical to (f).
The live census runs under `set -euo pipefail` (`tools/tsukuroi-census.sh:539`). Existing arms
guard every probe whose target may be absent. A new XFS arm that runs `find`/`ls`/`awk` on an
absent `TSUKUROI_XFS_SYSFS` (or an unreadable mount table) without `|| true`/a `cap`-style
wrapper aborts the script **before** the rollup, changing both the rollup presence and rc — the
base run is rc 1 with 15 lines. A plain unconditional `echo` before the rollup does not change
the rollup text; the R65/R69-style neutrality case compares rollup, exit code and non-KERNEL
line count with the arm inputs present vs absent, and one constant extra line is equal in both
runs, so that case alone will not catch an absent-path abort unless the new `R70-C2` cases
exercise the absent override. The predicate's live run catches it, but only at verification.

Consequence: **minor** (implementation hazard, detectable at the live check; no predicate
defect).

### C2-5 What the predicate does bind

`stats <= present` is a real bound: a naive `/sys/fs/xfs/*/stats/stats` glob includes the global
`stats` kobject, giving `stats=3` against mount-derived `present=2`, and fails. `mounts ==
findmnt` is real today. Those two clauses are the predicate's only teeth; the rest is
self-reported.

---

## 4. Axis harm

- **Surface PROVINCE.md does not declare — yes (1).** `PROVINCE.md` Core (lines 6-30) owns
  pacman, systemd, journal/boot, driver/firmware, update-safety, Arch News, pacnew, initramfs,
  snapper; no XFS storage plane. Lines 214 and 280 say the xfs device "(xfs on `/tmp`, `/fast`)
  still has no btrfs counters and stays unread." C2 adds a read of `/sys/fs/xfs` presence,
  stats content, `error/` and `log/`, and no claim in the declaration appends a PROVINCE
  section. The r65 INITRAMFS arm is declared (PROVINCE line 22); this one is not.
  **serious** (governance/ownership: the province calls the surface unread).
- **Sibling ground absorbed — no.** ADJ-01..07 cover endpoint (kama), credentials (kagi), UI
  (mado), OOM/fleet correlation (mori), dispatch (kumitate), RE (kaidoku/revenger), census
  blind spots (tameshi); none owns XFS storage. The note claims no disk-space runway (Mori's),
  no free-capacity measurement. **0.**
- **Health grade the counters cannot produce — no.** C2 is explicitly verdict-neutral; C1 states
  the health reader's "not collected" state, not a grade. **0.**
- **Quality traded for expansion — yes (1).** C2 adds an arm whose predicate a constant line
  meets (C2-1), and C1's six rows can be six host opinions (C1-2), inside a 13-seat single
  wave. **serious.**

→ `HARMS=2` (undeclared surface; quality-for-expansion).

---

## 5. Smallest safe corrections

1. **C2 (fatal):** bind `present` to an independent enumeration of `/sys/fs/xfs/<dev>` for the
   mount sources (exclude the global `stats` kobject), require
   `present+absent+unreadable == mounts`, require `error`/`log` to equal a verifier-side
   regular-file count, and require a detail token when `present < mounts` or any count is zero
   while the host has files. Name the enumerator in the predicate.
2. **C2 (serious):** pin `error` to **9** per filesystem (or define the enumeration excluding
   `default/`); reconcile `before/host.txt` with the declaration's "7".
3. **C1 (serious):** add a battery mutant whose statement reuses source vocabulary but is
   vacuous or a host fact (the two fixtures above are the seed); if the counter stays lexical,
   say so in the claim and verify the six rows by read.
4. **(a) (serious):** cite `84e013a7` as the health.c landing and record its route-1 fetch in
   `FETCH.txt`; do not claim four snapshots at `1710bd74`.
5. **PROVINCE (serious):** append the XFS read surface (or drop C2); "stays unread" is currently
   contradicted by the arm.

---

PREMISES_RECHECKED=3/6 C1_REACHABLE_ON_REAL_SNAPSHOTS=1 C2_NONREAD_SURVIVOR=1 HARMS=2 FATAL=1
