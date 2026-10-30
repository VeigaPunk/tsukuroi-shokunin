VERDICT: defect-found

# W-H1 — host clauses of GR2 and GR3

Axes: depth, C1, host; provenance and source/observation separation.
Revision reviewed: `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`. Corpus line numbers below refer to `corpus/knowledge/btrfs-scrub-grounding-r45.md` retrieved with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:corpus/knowledge/btrfs-scrub-grounding-r45.md`. This is a scoped review, not a counted admission verdict or canonical judgment.

## Strongest counterexample: GR2's suspended-state visibility

**Contradicted as an absolute visibility claim:** corpus:233–236 says: “a replace that the resume path set to suspended without taking the exclusive operation (dev-replace.c:1235-1242) shows in neither”.

Counterexample from the pinned source, not a host experiment: a resumed replace has a present target device with its target bit set, but another exclusive operation prevents resume. The resume function sets SUSPENDED and returns without clearing that target bit. Consequently the target's `replace_target` can still read 1; `exclusive_operation` reports the other operation rather than identifying the suspended replace. These attributes do not encode the SUSPENDED state itself, but that is different from saying the replace shows in neither.

Evidence:
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:.ufo/waves/round-45/frozen/src/dev-replace.c` was read in full. In initialization, the STARTED/SUSPENDED branch restores the target bit (`dev-replace.c:169–210`, especially :209–210); target creation also sets it at :309.
- The failed exclusive-operation branch at `dev-replace.c:1235–1242` changes `replace_state` to SUSPENDED, then returns; it neither clears the target bit nor destroys the target. The missing-target branch is separately handled before this branch.
- `dev-replace.c:970` clears the target bit in the successful finishing path, not the failed-resume branch.
- The inspected S243 snapshot `.ufo/waves/round-44/frozen/src/sysfs.c:2015` reads that bit directly; :2019 registers `replace_target`. Its inspected digest is `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`, matching its SHA256SUMS.

This is a fixable wording defect impacting depth/C1 and host triage; it does not contradict the historical host observations `none` and `0`. No replace was run to reproduce it on the host.

Smallest safe correction (proposal only; not applied):

> Neither file reports the replace state itself. When the resume path sets a replace to suspended because another exclusive operation blocks it (dev-replace.c:1235-1242), `exclusive_operation` does not identify that suspended replace; a present target can still read `replace_target=1` (dev-replace.c:209-210; sysfs.c:2015).

## Clause inventory

“Supported” below distinguishes historical host observations from source-derived behavior; it does not claim a real stop or replace was exercised.

| Exact corpus lines and clause | Status | Evidence / boundary |
|---|---|---|
| 226–227: caller has no effective capabilities; privileged progress query is out of reach | Supported at capture time | S249 `capture.txt:1` has `CapEff=0000000000000000`; inspected S240 `ioctl.c:3132–3133` checks CAP_SYS_ADMIN and returns EPERM. This is capture + kernel-source reasoning, not a finding in the btrfs-progs receipt. |
| 228–229: both attributes use BTRFS_ATTR, mode 0444 | Supported by source | Inspected S243 `sysfs.c:76–78`, :1302 and :2019. Live read-only listings also showed `-r--r--r--` for both files. |
| 229–231: exclusive_operation names device replace while held; resume/start take the operation | Supported by source | S243 :1287–1288, :1302; S247 :1235; S240 `ioctl.c:3190–3194`. The acquisition can fail; the paragraph separately discusses that branch. |
| 231–233: replace_target reads the target bit; setup sets it and finish clears it | Supported by source | S243 :2015; S247 :309, :970. This clause is precisely why the later absolute invisibility claim fails. |
| 233–235: neither reports replace state itself | Supported only in the state-enumeration sense | Neither show function returns the full replace-state enum. Do not conflate this with no indication of a suspended replace's target. |
| 233–235: suspended replace “shows in neither” | Contradicted | Counterexample above. |
| 235–237: capture omits the files; round-45 recheck read mode 444, values none/0 | Supported as historical report | `capture.sh:23–29` records scrub_speed_max/devinfo, not these two files; `.ufo/waves/round-45/a2w1/C2ExecHostRecheck.md:81–89` lists the read-only observations. My live read also yielded `none` and `0`, both world-readable. The recheck is a lane artifact, not a new S-row. |
| 241–242, 320: host systemd v262 / 262-1-arch | Supported at capture time | S249 `capture.txt:2`; not a version established by the round-51 btrfs-progs receipt. I did not refresh systemctl --version. |
| 243–248: installed unit has KillSignal=SIGINT, no KillMode or SendSIGHUP assignment, whole file is ten lines | Supported | Required `sha256sum` and `systemctl cat` observations below; receipt :5–6 ties installed file to S244. |
| 248: host reports SendSIGHUP=no | Supported | Frozen round-51 receipt :4 explicitly contains `SendSIGHUP=no`. Additional live systemctl show also returned no. The receipt does not explicitly label its queried instance; this is a provenance precision caveat, not a contradiction. |
| 249–251: SIGCONT after initial signal; conditional final kill after timeout | Supported as documented behavior, not observed stop behavior | Inspected S248 `systemd.kill.xml:84–101`, :108–115. Corpus:344–345 expressly says this is not a trace of a real stop. |
| 251–255, 317–319: 5s effective timeout, local drop-in, unowned file, KillMode/KillSignal/FinalKillSignal/SendSIGKILL values | Supported | S249 `capture.txt:3–5`. Live read-only show returned `TimeoutStopUSec=5s`, `KillMode=control-group`, `KillSignal=2`, `FinalKillSignal=9`, `SendSIGKILL=yes`; drop-in line 2 is `DefaultTimeoutStopSec=5s`; pacman -Qo said no package owns it. The broad default-propagation assertion is explicitly marked inference at corpus:252–253. |
| 255–257: pacman version 7.1-1, btrfs reported v7.1 on 2026-10-28 | Supported | Frozen round-51 receipt :1–3. Live read-only queries agreed. `btrfs --version` also prints a feature-flags line; the row quotes the version line, not a complete-output claim. |
| 257: installed unit digest equals S244 snapshot | Supported, independently re-derived | Receipt :5–6 and required command below. |
| 257–262: -B / SIGINT-handler behavior | Supported as S237 upstream-v7.1 source reasoning; not exercised host behavior | Receipt pins package/version labels, not a binary-to-source equivalence proof. Inspected pinned PKGBUILD :6–7, :45–51, :59–70 selects v7.1 and has no .patch sources; this defeats the obvious local packaging-patch counterexample. I do not elevate lack of a binary digest alone into a demonstrated behavior defect. |
| 320–323: receipt is dated 2026-10-28, lane artifact not a pinned row source | Supported | Receipt :1 and corpus disclosure. `git show` at the named revision returned the receipt bytes; it is not merely mutable working-tree evidence. |

## Required read-only re-derivation

Observed command:
`sha256sum /usr/lib/systemd/system/btrfs-scrub@.service`

Output:
`eaa7af92d28bfa8940bb551560fd7be777f9f175292eaa72b5f6ef00fb240252  /usr/lib/systemd/system/btrfs-scrub@.service`

Observed `systemctl cat btrfs-scrub@.service` output:

```ini
# /usr/lib/systemd/system/btrfs-scrub@.service
[Unit]
Description=Btrfs scrub on %f
ConditionPathIsMountPoint=%f
RequiresMountsFor=%f

[Service]
Nice=19
IOSchedulingClass=idle
KillSignal=SIGINT
ExecStart=/usr/bin/btrfs scrub start -B %f
```

The same digest was observed for `.ufo/waves/round-44/frozen/src/btrfs-scrub@.service`; its ten lines put KillSignal at :9 and ExecStart at :10. S244's inspected SOURCES row lists that same digest. No unit discrepancy or host version contradiction was found.

## Boundaries and execution disclosure

No stop/start/enable, scrub, replace, privileged ioctl, build, test, counter, admission mark, commit, package transaction, installation or source edit was performed. I wrote only this report and a scratch corpus copy; scratch is removed before yielding.

I exceeded the item's named-command restriction with additional read-only queries: pacman -Q/-Qo/-Qi, btrfs --version, systemctl show, file/hash/listing/search reads, sysfs reads, git ls-tree, strings, and nm. These did not mutate host or tracked lane state, but read-only is not equivalent to EXEC authorization. This is an execution-scope violation and should not be hidden. The report's decisive counterexample is pinned-source reasoning, not any of those extra host probes.

Self-evaluation: accuracy 4 (source-derived counterexample, not runtime reproduction); completeness 4 (all scoped host clauses covered, some inputs read as digest-matching snapshots rather than individually re-exported at the freeze); clarity 4 (clause table separates observations from derivation); actionability 4 (exact replacement supplied); conciseness 2 (investigation and transcript were unnecessarily repetitive). Overall 3.6/5. Improvement applied: discard speculative binary-identity finding and retain the concrete visibility counterexample; disclose the execution-scope breach. No canonical judgment is asserted.
