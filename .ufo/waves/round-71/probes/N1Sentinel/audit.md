# N1Sentinel — round-71 w1 boundary audit

Read-only audit of every artifact under `.ufo/waves/round-71/{w1,probes}` plus both
repositories' working-tree state. Snapshot taken 2026-11-04T01:08Z, after all 14 seats had published; lane HEAD `bdaec573`, fleet HEAD unchanged (pre-existing dirty set only).

Method: command-context scanner (only fenced blocks, inline spans that lead with a command
token, and prompt-led lines are judged as commands — prose that *describes* a prohibition is
not a violation), secret-shape regexes over all text, `git status` in both repos, `/tmp` and
scratch inventory, and byte-hash attribution of every lane-tree write.

## Verdict

| key | value | basis |
|---|---|---|
| WRITES | 73 | files under `w1/` + `probes/` at snapshot |
| SECRETS | 0 | no key/token/session/`op://` shape in any artifact (see F1 for identifiers) |
| SUDO_NONREADONLY | 0 | zero `sudo` occurrences as a command; the two textual hits are "no sudo" statements |
| TMP_EVIDENCE | 0 | no artifact cites `/tmp`; the one mention describes a mutant's temp-file choice |
| LANE_DIRTY | 2 | both lane files are L1-authored; 0 seat-authored writes outside the wave dirs |
| MISROOT | 0 | no realized misroot write; 6 misroot-*shaped* relative invocations (F2) |

## A — host writes, package and service state: none

Every `/sys` occurrence is descriptive: table cells, quoted upstream docs, and the
SKILL/coverage/province prose. No redirect, `tee`, `dd of=`, `cp`/`mv`/`install`/`chmod`
into `/sys`, `/proc`, `/etc` or `/boot`; no `pacman -S/-U/-R`, no `systemctl
start|stop|restart|enable`, no `modprobe`/`insmod`/`rmmod`, no `sysctl -w`, no
`mkinitcpio`/`bootctl`/`grub-*`, no interactive `sudo`.

Scanner hits were examined and cleared:
- `w1/SC4Index.md:41` — `> /sys/` inside a sentence reporting `WRITE_SYNTAX_HITS=0`, a fragment, not a command.
- `w1/SC2Sources/rows.md:38` and two S1Scout lines — `modprobe usbcore blinkenlights=1` is the quoted upstream example in the S300 registry cell, not an invocation.
- `probes/E1Harness/census-*.sh:399,2162` — `systemctl enable ...` lives inside the census's own selftest heredoc fixtures, inherited from the committed tool; those copies are data, not executed lines.

## B — secrets: none; one identifier-minimization finding

No private-key block, `ghp_`/`sk-`/`AKIA`/`xox*`/JWT, `op://` reference, bearer header or
`password=`-style assignment anywhere in `w1/` or `probes/`. `SECRETS=0`. (A rerun of the shape
grep returns three hits — all three are this report and `w1/N1Sentinel.md` naming the patterns
they exclude; they are self-references, not material.)

**F1 (LOW) — host identifiers beyond need.** `probes/S1Scout/host-enum.txt:47` publishes the
live btrfs filesystem UUID (`/sys/fs/btrfs/<uuid>/read_policy`); line 51 publishes the
`PARTUUID=` from `/proc/cmdline`. The PARTUUID is already in the committed
`before/host.txt`; the filesystem UUID is new to this wave. The seat's own report
(`w1/S1Scout.md:61`, `probes/S1Scout/S1Scout.md:66`) correctly redacts to `<uuid>`, so the
leak is confined to the raw capture. The real hostname `plazir27` appears in
`w1/R2Reviewer/live-diff.txt` and in the committed `before/`/`after/` census receipts — it is
emitted by the census tool itself and is therefore pre-existing lane practice, not a seat
departure. Smallest remediation: replace the two raw values with `<uuid>` / `<partuuid>` in
`host-enum.txt`, and redact `host=<name>` in wave-level copies. No credential, no access
granted, no session material.

## C — `/tmp`: not used as evidence or as a seat scratch root

No artifact under `w1/` or `probes/` names a `/tmp` path as evidence. Runtime-only leftovers
exist and are all tiny: `/tmp/r71fact.{1,2}.{out,err}` (700 B each, pre-report gate run by the
orchestrator at 22:03) and the empty pre-wave directory `/tmp/r71-boundary-uvzwghru`
(21:47, before the wave opened). One mutant described in `probes/M1Mutation/score.md:67`
writes `/tmp/out.$$.$RANDOM` as a *deliberate* hermeticity violation; its files are already
gone. `TMP_EVIDENCE=0`.

## D — misroot: no realized write, six misroot-shaped invocations

**F2 (MEDIUM, reporting) — `probes/SC3Lesson/sweep-receipt.txt`.** All six `$`-led lines use
paths relative to the lane root and record no `cd`:

```
python3 .ufo/waves/round-71/probes/SC3Lesson/sweep-selftest-tally.py ...
git show 0fcfca31:SCORECARD.md | grep -n '12 cases: 1 well-formed control'
grep -n '^BATTERY' .ufo/waves/round-71/before/control/battery.txt
```

From the guard-default cwd (the fleet root) these do not resolve to the same bytes: the fleet
root has **no** `.ufo/waves/round-71`, and it *does* have a `SCORECARD.md` of 531 lines whose
line 5467 is empty, whereas the lane's `SCORECARD.md` is 5504 lines and line 5467 carries the
quoted declaration line. The observed output (5467) therefore proves the run happened with
cwd = lane — no misroot was realized — but the receipt is not reproducible as written, and one
of its six paths silently shadows a *different existing file* in the fleet repo. Smallest
remediation: re-emit the six lines with absolute lane paths (or one recorded `cd` line), as
every other seat did.

Every other seat's receipts anchor absolutely (`/home/vgpnk/...`, `$S/...`,
`/fast/scratch/...`). `MISROOT=0`; risk count 6, confined to one file.

## E — writes outside the wave dirs: none by a seat

**F5 (INFO).** No seat wrote the lane tree, the fleet repo, a sibling, `.ufo/state`,
`.scratch`, `MANIFEST.json` or `.watchdog.log`; no `git`/`jj` mutation appears in any
artifact (all git calls are read-only or `-C <clone>`). The fleet repo's dirty set is
identical to the pre-audit baseline.

The lane tree *is* dirty, and every dirty path is attributable to the L1, the only permitted
writer:
- `db58e7c9` (22:02:07) — `tools/tsukuroi-census.sh`, `tools/count-xs-rows-r70.py`, three `after/` receipts;
- `2959254a` (22:03:25) — `corpus/SOURCES.md`, `corpus/knowledge/module-parameter-plane-r71.md`;
- `bdaec573` (22:06:13) — PROVINCE/SKILL/README, tally tool;
- uncommitted at snapshot — `tools/tsukuroi-census.sh` (22:07:35, +16/−7) and `tools/check-selftest-tally.py`.

Attribution evidence: the committed census bytes (`487feeb6…`) are byte-identical to
`/fast/scratch/hyaku/tsukuroi-r71/L1/proto/census.sh`, which no seat scratch contains.

## F3 (HIGH, provenance) — the committed C2 bytes are not reproducible from the seat's artifact

Three distinct byte lineages of `tools/tsukuroi-census.sh` exist for round 71:

| state | sha256 (prefix) | size | time |
|---|---|---|---|
| L1 prototype = committed `db58e7c9` | `487feeb6…` | 281975 | 21:58 / 21:59:50 |
| seat E1Harness `census-r71-c2.patched.sh` | `ebe3ab2d…` | 284918 | 22:06 |
| seat E1Harness `census-on-landed-patched.sh` | `81628076…` | 283362 | 22:06 |
| lane working tree (uncommitted) | `598ae252…` | 282507 | 22:07:35 |

Additional measured facts:
- E1Harness's first scratch `harness.patch` is a **reverse** diff (`--- lane 21:59:50`,
  `+++ census.sh 21:59:35`) and, applied to the HEAD base `042c6b4b…`, **4 of 5 hunks fail**
  and the result is not the lane file. It cannot be the artifact that produced the commit.
- No file under `probes/E1Harness/` predates `db58e7c9`; the directory did not exist until 22:06.
- The seat itself published `harness-vs-landed.diff` and an on-landed patched copy, which is
  the correct response to finding the lane already changed.

Corroboration: E1Harness's own report opens "Independent alternative to the harness the L1
landed at `db58e7c9`. Drafted on the pre-landing base `db58e7c9^` … Nothing here was applied to
the lane tree; the L1 owns it." The seat and the bytes agree.

Consequence: the round cannot claim "the C2 predicate was implemented by E1Harness's patch and
applied by the L1" from local evidence. The committed block's provenance is the L1 prototype,
and the seat's deliverable is byte-different from it. This is a provenance/calibration defect,
not a boundary write; it is reported so the round's receipt language matches the bytes.
Smallest remediation: record the applied artifact's sha256 in the C2 receipt and name the
lineage explicitly (prototype vs seat patch), or apply the seat's on-landed patch and commit
its hash.

## F4 (INFO) — two full census copies published into `probes/`

`probes/E1Harness/census-r71-c2.patched.sh` (284 KB) and `census-on-landed-patched.sh`
(283 KB) are complete copies of the 280 KB tool. They are inside the seat's write scope and
contain no secrets, but they carry the tool's fixture heredocs (`systemctl enable …`), which
any pattern-based scanner will flag; both were inspected and are data, not commands.

## Scratch cleanup

Present at snapshot (22:08Z): `L1/` (orchestrator), `R2Reviewer/` (published, tree not yet
removed), `N1Sentinel/` (this seat, removed at yield). Removed by their seats: `C1Connector`,
`E2CounterAttack`, `E3Repairs`, `E1Harness`, `K1Critic`, `M1Mutation`, `R1Reviewer`, `S1Scout`,
`SC1Entry`, `SC2Sources`, `SC3Lesson`, `SC4Index` — including K1Critic, whose receipt claims
removal before yield and whose 434 MB tree is in fact gone, and E1Harness, whose 434 MB tree
disappeared between 22:07 and 22:08. `R2Reviewer` is the only published seat with a live
scratch tree at snapshot.

## Limits of this audit

Seats were still writing while the scan ran; the numbers are pinned to 22:08Z and the file
list is reproducible with `find .ufo/waves/round-71/{w1,probes} -type f`. The audit reads
artifacts and repository state; it does not execute the wave's harnesses and does not judge
the C1/C2 predicates themselves.
