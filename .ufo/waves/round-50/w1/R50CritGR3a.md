ROW GR3 VERDICT: partly
SECTION SHA256: 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c

# GR3, counted critic (R50CritGR3a)

## Section hash, re-derived

`python3 tools/check-scrub-admission-r50.py --revision 8029cdba1049df25632c91a23c8db4eefb54be5f --section-hash`
printed `GR3 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` with `"problems": []` and
`structural_ok: 1`. I also recomputed it myself from the extracted entry: lines 153-198 (from `## GR3` up to the line
before `## How this changes OS triage` at 199, the final element being the empty line 198), joined with LF, no trailing
LF -> `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c`. The row bytes I judged are exactly the
frozen bytes.

## Snapshot digests (checked before reading any clause)

`sha256sum -c SHA256SUMS` -> all OK in `.ufo/waves/round-45/frozen/src` (cmdline.c, dev-replace.c, systemd.kill.xml,
kstrtox.c, vsprintf.c), `.ufo/waves/round-44/frozen/src` (scrub.c, sysfs.c, btrfs-scrub@.timer,
btrfs-scrub@.service, PKGBUILD) and `.ufo/waves/round-42/frozen/src` (scrub.c, CHANGES). S-row mapping:
S248 = round-45 `systemd.kill.xml` (FETCH.txt records `GET .../systemd/v262/man/systemd.kill.xml`), S249 = round-45
`hostcap/capture.txt` (sha256 f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70, as stated),
S244 = round-44 `btrfs-scrub@.service`, S237 = round-42 `scrub.c` (FETCH.txt: btrfs-progs v7.1, peeled
4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b). `hostcap/capture.sh` hashes to c6d2c448c83de3326109a29638d55d7083ee93edd4242a845b050bc180a751fc, the value registered at
corpus/SOURCES.md:258.

## Every quote is exact on its cited line

All 12 **Quote.** lines resolve and match byte-for-byte:
- `btrfs-scrub@.service:9` = `KillSignal=SIGINT`; `:10` = `ExecStart=/usr/bin/btrfs scrub start -B %f`.
- `systemd.kill.xml:68` = `<para>If set to <option>control-group</option>, all remaining processes in the control group of this`
- `systemd.kill.xml:91` = `<listitem><para>the delay configured via the <varname>TimeoutStopSec=</varname> has passed`
- `systemd.kill.xml:96` = `the termination request is repeated with the <constant>SIGKILL</constant> signal or the signal specified via`
- `systemd.kill.xml:101` = `<para>Defaults to <option>control-group</option>.</para>`
- `systemd.kill.xml:108` = `<listitem><para>Specifies which signal to use when stopping a service. This controls the signal that`
- `systemd.kill.xml:114` = `<para>Note that, right after sending the signal specified in this setting, systemd will always send`
- `systemd.kill.xml:115` = `<constant>SIGCONT</constant>, to ensure that even suspended tasks can be terminated cleanly.</para>`
- `scrub.c:421` = `	ret = ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL);`
- `scrub.c:1546` = `	scrub_handle_sigint_child(fdmnt);`
- `scrub.c:439` = `		.sa_handler = fd == -1 ? SIG_DFL : scrub_sigint_record_progress,`

## Clause-by-clause against the pinned bytes

1. `KillSignal=` = SIGINT instead of the SIGTERM default: btrfs-scrub@.service:9 plus systemd.kill.xml:108 (and
   `Defaults to <constant>SIGTERM</constant>` at :112). Holds.
2. No `KillMode=` in the unit: btrfs-scrub@.service:1-10 sets only Description/ConditionPathIsMountPoint/
   RequiresMountsFor/Nice/IOSchedulingClass/KillSignal/ExecStart; default `control-group` at systemd.kill.xml:101,
   "all remaining processes ... will be killed" at :68. Holds.
3. SIGCONT right after the stop signal: systemd.kill.xml:114-115. Holds.
4. Repeat with SIGKILL after `TimeoutStopSec=`, honouring `FinalKillSignal=` unless `SendSIGKILL=no`:
   systemd.kill.xml:91-93 (applies to `control-group`) and :96-97. Holds.
5. Effective 5 s stop timeout on this host: capture.txt:4 (`stop_default /etc/systemd/system.conf.d/10-faster-shutdown.conf:2:DefaultTimeoutStopSec=5s`)
   and, independently, capture.txt:3 (`TimeoutStopUSec=5s`). Holds.
6. The `[inference]` on "this default reaches every system unit" is justified: no `systemd-system.conf(5)` snapshot
   exists under any of the three `frozen/src` dirs (`ls` and `find .ufo/waves -name '*system.conf*'` -> none), so the
   mark is correctly placed and correctly scoped.
7. "no package owns that drop-in": capture.txt:5 (`dropin_owner /etc/systemd/system.conf.d/10-faster-shutdown.conf none`),
   produced by the bounded pacman-db sweep at capture.sh:16-21. Holds.
8. `systemctl show` values: capture.txt:3 gives exactly `FinalKillSignal=9 ... KillMode=control-group KillSignal=2
   SendSIGKILL=yes TimeoutStopUSec=5s`. The attribution to `btrfs-scrub@-.service` is decided, not guessed: capture.sh:11
   runs `systemctl show 'btrfs-scrub@-.service'` with those `-p` properties. Holds.
9. "`-B` does not fork into the background (scrub.c:1512)": `scrub.c:1292-1294` is `case 'B': do_background = false;`
   and `:1512` is `if (do_background) {`. The cited line is the fork guard and the option parse confirms it. Holds.
10. "installs its SIGINT handler on the mount's descriptor (scrub.c:1546, :439)": `fdmnt = btrfs_open_mnt(path)` at
    `scrub.c:1343`, passed at `:1546`, handler selected at `:439` (`fd == -1 ? SIG_DFL : scrub_sigint_record_progress`).
    Holds.
11. "which issues `BTRFS_IOC_SCRUB_CANCEL` (SR9)": the ioctl is `scrub.c:421` inside `scrub_sigint_record_progress`
    (function `scrub_sigint_record_progress` defined at `:417`). The `(SR9)` pointer resolves: the round-44 row `## SR9` states the foreground start
    "installs a SIGINT handler that issues `BTRFS_IOC_SCRUB_CANCEL`" (btrfs-scrub-record-r44.md:99). Not a defect.
12. `SR3` pointer: defined in the round-44 entry (btrfs-scrub-record-r44.md:8, :101, `canceled` set resumed later).
    The 5 s-vs-SIGKILL write question is properly left `[inference: ...]`. Holds.
13. "No unit was started or stopped": capture.sh:4 declares `systemctl --version/show (no start, stop or enable)` and
    capture.txt:1 records `uid=1000 CapEff=0000000000000000`. Holds.
14. No errno/order-of-errno clause and no multi-line range exist in GR3 (the row cites only single lines), so the
    "range runs into the next function" test has nothing to bite on. Universal words: "every remaining process" is
    backed by :68 "all remaining processes"; "always" occurs only inside the verbatim quote at :114.

Counterexample tested and rejected: systemd.kill.xml:84-87 documents an *optional* SIGHUP immediately after the
KillSignal, which the row's "in this order" omits. But :138 says `SendSIGHUP=` "Defaults to <literal>no</literal>" and
btrfs-scrub@.service sets none, so no SIGHUP intervenes and the order is complete for this unit. Not a defect.

## Defect (1): two S237 citations fall outside the registered ranges and are undeclared

S237's registration (corpus/SOURCES.md:246) declares `cmds/scrub.c lines 67-70, 280-330, 446-535, 826-895, 1110-1125,
1186-1220, 1330-1340, 1498-1512, 1925-1945`. GR3 cites `scrub.c:1512` (inside 1498-1512, fine), `:421` (outside, but
declared at entry line 227: "S237's do not list `scrub.c:421`"), and then `:439` and `:1546` — both outside every
registered range, with no declaration anywhere in the entry (`grep -n '439\|1546'` finds only the row body, the two
Quote lines, and a round-46 history note at :281; the sole S237 gap sentence at :227 names `:421` alone). This is the
same defect class the round-49 counted critic named as defect 4 for S247, and which round 50 applied to S247 and S240
(entry:229-235) but not to S237. Content is not in doubt — S237's raw bytes are digest-pinned whole-file
(sha256 48df2e2f468f7db79a3611ae2f3b1b794d330e8d02cc91f9ce386de8ed8f0801, SOURCES.md:246) — so this is a provenance
gap, not an unsupported claim.

Smallest safe correction, exact replacement at entry line 227:

  `S237's do not list \`scrub.c:421\`.`  ->  `S237's do not list \`scrub.c:421\`, \`:439\` or \`:1546\`.`

(Alternative: widen the registration at corpus/SOURCES.md:246 by adding `330-446` and `1513-1560`.)

The round-50 counter does not catch this: its `CORR49_REQ` (tools/check-scrub-admission-r50.py:107-112) requires only
`the widened S247 ranges still do not list`, so `quotes_ok`/`corr_ok` can be 1 while this gap is undeclared.

## GR2's four round-49 corrections (checked, because C1 depends on them)

All four are present in the frozen bytes, contrary to nothing: (1) the `[inference]` bracket is scoped to "how
`btrfs scrub start` and `btrfs scrub status` print these returns is not pinned here" (entry:75-79) and the forbidden
ioctl-conjunct string is absent (`grep` -> ABSENT); (2) `S240` is named in the `source:` line with its sha256 and
cited ranges (entry:1); (3) the dev-replace.c:1128 quote carries the prefix — the line reads
`	 * Scrub doing the replace isn't running so we need to do the`; (4) the S247 and S240 gaps are declared
(entry:229-235). These are GR2 facts, not my verdict line.

## What I verified but did not re-derive

- The counter's full predicate (`structural_ok/corr_ok/quotes_ok/verdicts_ok/seats_ok/marks_ok`): I ran only
  `--section-hash`. C1's predicate is not re-derived here.
- Upstream fetches: no network re-fetch. Digests were checked against the recorded `SHA256SUMS` and the SOURCES.md
  sha256 values only.
- GR1's row: not read (out of scope). S242/S243/S240 citations: not checked (GR3 cites none).
- The round-44 SR9/SR3 statements were read only far enough to resolve the two pointers, not audited against their own
  quotes.

## What I did not do

No unit was started, stopped or enabled; no privileged ioctl, no sysfs write. No lane file was modified; the only
writes were this report and the scratch extraction under /fast/scratch/hyaku/tsukuroi-r50/R50CritGR3a/ (removed).
No tool installs were needed.
