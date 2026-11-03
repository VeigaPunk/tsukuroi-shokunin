source: S288 S289 — Linux v7.2.11 `Documentation/admin-guide/tainted-kernels.rst` (committed snapshot `.ufo/waves/round-69/before/src/tk-v7211.rst`, sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841) and `include/linux/vermagic.h` at the same tag (snapshot `.ufo/waves/round-69/before/src/vm-v7211.h`, sha256 0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea); both fetched from the stable tree at tag v7.2.11 (`.ufo/waves/round-69/before/src/FETCH.txt`). Host readings: the pre-declaration capture `.ufo/waves/round-69/before/host.txt`, the host scout `probes/S2Scout-host.md`, and this seat's own read-only probes `probes/SC1Scribe/{host-read,privilege-read,pacman-localdesc,timing-and-crosschecks,lts-module-vermagic,quote-check,note-selfcheck}.txt`.
verified-at: 2026-11-03 (pinned bytes: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-69/before/src/` printed `tk-v7211.rst: OK` and `vm-v7211.h: OK`, rc 0; the live host re-read at 2026-11-03T23:20:43Z agrees with the capture field for field; the `6.18.57-2-lts` tree's own module was probed at 2026-11-03T23:26:53Z (`probes/SC1Scribe/lts-module-vermagic.txt`); `cmp -s` proves S288's snapshot byte-identical to S140's v7.2 copy, rc 0)
recheck: on-release — the next stable kernel tag re-fires this read of the v7.2.11 pins; the fired re-read re-runs `sha256sum -c SHA256SUMS` in `.ufo/waves/round-69/before/src/` (both files must print `OK`) and re-reads `cat /proc/sys/kernel/tainted`, `uname -r`, `ls -1 /usr/lib/modules/`, `modinfo -F vermagic /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst`, and one module from each other tree. Package readings are steered to file reads (QUALITY 26): `ls -d /var/lib/pacman/local/linux-[0-9]*` names the installed version, and the `desc` file under `linux-7.2.11.arch1-1/` carries the `%NAME%`/`%VERSION%` markers at lines 1 and 4 with their values on the following lines (`linux`, `7.2.11.arch1-1`); no package-manager invocation is prescribed. The same re-read fires sooner if any KR5 falsifier appears.

# The taint table at its own tag, the vermagic composition rule, and the release token that binds a module tree (round 69)

Scope: this entry re-grounds the taint decode at the running kernel's own release tag, then spends its depth on what the lane does not hold — the `VERMAGIC_STRING` composition rule of `include/linux/vermagic.h` (S289), that rule's instantiation in this host's dkms `nvidia` module, and the release-token consequence for the two `/usr/lib/modules` trees and their package owners. It does NOT cover module signature or keyring internals, DKMS build policy, live patching, the kernel command line, module load policy, a foreign-module load attempt (operator-owned), or the `kernel/module.c` comparison that is not inside the pinned bytes.

| row | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| KR1 | S288 fixes the closed 0-19 taint table at v7.2.11, the running kernel's own tag, and its bytes are identical to S140's v7.2 copy, so this row re-grounds KT1/KT6 of corpus/knowledge/kernel-taint-r27.md at that tag and claims no new taint mechanism. | source=S288 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint" |
| KR2 | Re-grounding KT1 of corpus/knowledge/kernel-taint-r27.md, this host's 12288 is 4096 plus 8192, so only bits 12 and 13 are set, matching the boot log's [O] and [E]; no new mechanism is claimed. | source=S288 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="13  _/E    8192  unsigned module was loaded" |
| KR3 | S289 composes VERMAGIC_STRING as UTS_RELEASE, one space, then MODULE_VERMAGIC_SMP, MODULE_VERMAGIC_PREEMPT (preempt_rt when CONFIG_PREEMPT_RT is set, else preempt when CONFIG_PREEMPT_BUILD), MODULE_VERMAGIC_MODULE_UNLOAD, MODULE_VERMAGIC_MODVERSIONS, MODULE_ARCH_VERMAGIC and MODULE_RANDSTRUCT, each present only when its condition holds. | source=S289 | snapshot=vm-v7211.h | digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea | quote="#define VERMAGIC_STRING \ UTS_RELEASE " " \ MODULE_VERMAGIC_SMP MODULE_VERMAGIC_PREEMPT \ MODULE_VERMAGIC_MODULE_UNLOAD MODULE_VERMAGIC_MODVERSIONS \ MODULE_ARCH_VERMAGIC \ MODULE_RANDSTRUCT" |
| KR4 | The host dkms nvidia module prints `7.2.11-arch1-1 SMP preempt mod_unload`: SMP, preempt and mod_unload are present while modversions, randstruct and arch magic are absent; a module built for another release carries that release as its first token, the 6.18.57-2-lts tree's module prints `6.18.57-2-lts`, so its stamp differs from the one this kernel composes, though whether the loader refuses that mismatch is not in the pins; the running tree is owned by linux 7.2.11.arch1-1 and linux-headers with uname matching, so no reboot is pending. | source=S289 | snapshot=vm-v7211.h | digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea | quote="Simply sanity version stamp for modules." |
| KR5 | Applicability is diagnostic: the taint value names a cause rather than a verdict, and the pinned table spans benign and severe causes alike, so severity must be read from the set bit; the composition rule is pinned at v7.2.11 alone, and the named falsifiers are a running-tree module without the running release token, an ownership change of the running tree, or a taint reading outside the v7.2.11 table. | source=S288 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="Don't worry too much about this, most of the time it's not a problem to run a tainted kernel" |

Reading. The host numbers are reads, not derivations. `cat /proc/sys/kernel/tainted` printed
`12288`; a bit sweep over indices 0-19 printed `1` at 12 and at 13 and `0` everywhere else;
`echo $((4096+8192))` printed `12288`. `ls -1 /usr/lib/modules/` printed two trees,
`6.18.57-2-lts` and `7.2.11-arch1-1`. `modinfo -F vermagic` printed
`7.2.11-arch1-1 SMP preempt mod_unload` for `/lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst`
(one trailing space in the tool output) and `6.18.57-2-lts SMP preempt mod_unload` for
`/usr/lib/modules/6.18.57-2-lts/kernel/arch/x86/crypto/aegis128-aesni.ko.zst`. `pacman -Qo`
printed `linux 7.2.11.arch1-1` and `linux-headers 7.2.11.arch1-1` for the running tree, and
`linux-lts 6.18.57-2` plus `linux-lts-headers 6.18.57-2` for the other. The boot log prints
`Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE` twice, at Nov 02 16:49:24 and 16:49:45, and the
two `nvidia:` lines at Nov 02 12:07:17 name the causes.

The composition check is token by token: the rule's conditionals give `SMP ` from `CONFIG_SMP`,
`preempt ` from the `CONFIG_PREEMPT_BUILD` branch (not `preempt_rt `), `mod_unload ` from
`CONFIG_MODULE_UNLOAD`, and empty strings for `CONFIG_MODVERSIONS`, randstruct and arch magic;
concatenated behind `7.2.11-arch1-1 ` that is exactly the observed string, trailing space
included. The boot banner's `#1 SMP PREEMPT_DYNAMIC` (the log's first line) agrees with the SMP
and preempt tokens without naming either config symbol. The `6.18.57-2-lts` module shows the
same rule instantiated by a different build: the release token is the tree's own name, so a
module file built in one tree carries a different first token than the other tree's modules, and
the loader's comparison of that token is outside the pinned bytes.

The boot log's extent is measured, not assumed: `journalctl -b -k --no-pager -o short-iso` holds
13754 lines and its first line is the kernel banner at `2026-11-02T12:07:17-03:00`, i.e. the
start of this boot's kernel log, so the two `nvidia:` lines at the same second are inside the
retained window; whether the journal discarded any line before retention cannot be decided from
the journal alone.

## Relation to held ground

- `corpus/knowledge/kernel-taint-r27.md` (rows KT1-KT6, S140-S145) already holds the taint
  mechanism, the per-module reading, the clearing rule and the reporting consequence. KR1 and
  KR2 here re-ground its KT1/KT6 decode at the running kernel's own tag — S288's bytes are
  byte-identical to S140's v7.2 snapshot (`cmp -s` rc 0, same sha256), so those two rows record
  tag stability and the host reading, not a second mechanism. KT2-KT5 are not restated.
- `corpus/knowledge/driver-firmware-plane.md:85` holds an older `vermagic:
  7.2.3-arch1-3 SMP preempt mod_unload` string with an "Only kernel tree present" reading from
  the round-17 capture. That observation is not re-scored here; KR3 and KR4 are about a later
  kernel release and a two-tree layout.

## Limits

- Timing is bounded by the log itself. The first retained kernel line is the boot banner at
  `2026-11-02T12:07:17-03:00` (13754 lines this boot, `probes/SC1Scribe/timing-and-crosschecks.txt`),
  and the taint print follows at 16:49:24. No per-bit timestamp exists, so assigning bit 12 to
  the out-of-tree load and bit 13 to the signature failure is [inference] from the closed table
  plus the two `nvidia:` lines, not a logged per-bit event.
- Privileged surfaces were not read. `/proc/sys/kernel/dmesg_restrict` reads `1`, so an
  unprivileged `dmesg` is unavailable, and `/sys/kernel/debug` is `drwx------ root root`
  (`probes/SC1Scribe/privilege-read.txt`); a root-only lockup or tracing report was not read and
  no privileged read was attempted. Beyond the measured zero soft-lockup lines
  (`grep -ciE 'soft lockup'` printed `0`, rc 1), the entry cannot decide whether a soft lockup
  occurred outside the retained log.
- The config symbols are inferred, not observed. No `/boot/config-*` or `/proc/config.gz` was
  read: `CONFIG_SMP`, `CONFIG_PREEMPT_BUILD`, `CONFIG_MODULE_UNLOAD` and the absence of
  `CONFIG_PREEMPT_RT`, `CONFIG_MODVERSIONS`, `RANDSTRUCT` and non-empty arch magic are read off
  the produced string and the banner, which over-determine them but are not the config file.
- No foreign-module load was attempted. Loading the `6.18.57-2-lts` modules into this kernel is
  an operator action and was not taken, so the mismatch between their first token and this
  kernel's composed stamp is observed but a load rejection is not: the comparison and its force
  modes live in code outside the pins.
- Vermagic coverage is two module files, not the trees. Only the dkms `nvidia` module (running
  tree) and one `6.18.57-2-lts` module were probed with `modinfo -F vermagic`; the rest were not
  read one by one, so "every module in either tree carries its tree's release" is not claimed.
- The Arch version conversion is host-measured, not upstream-documented. `7.2.11.arch1-1`
  (package field) to `7.2.11-arch1-1` (directory and `uname -r`) is a mapping observed on this
  host twice over (owner output and directory name); neither pin documents it.
- The `linux-lts` tree is a package fact, not a bootability fact. Whether the `6.18.57-2-lts`
  tree is bootable, and how a boot entry would select it, is out of scope: the boot loader
  configuration was not read.
- Nothing here is a remediation and nothing was run beyond the reads above: no package
  transaction, no service action, no privileged read, no module load, no write outside the wave
  directory.

## Falsifiers

Each bullet names the row it kills and the observable that does it:

- KR1: a documented taint reason outside bits 0-19, or a second meaning attached to one bit,
  would falsify the closed-table claim; so would S288's bytes differing from S140's copy at the
  same tag.
- KR2: a different tainted reading on this host (0, or a third set index in 0-19) or
  `echo $((4096+8192))` printing anything but `12288` falsifies the host decode; it does not
  touch the table's meaning, which is KR1's claim.
- KR3/KR4: `modinfo -F vermagic` on a module in the running tree lacking the `7.2.11-arch1-1`
  first token, carrying a `modversions` token while the rule's branch is clear, or a
  `6.18.57-2-lts` module whose first token is not `6.18.57-2-lts`.
- KR4 binding: `/usr/lib/modules/$(uname -r)` being absent, being owned by a package other than
  `linux`/`linux-headers`, or `pacman -Q linux` mapping to a release different from `uname -r` —
  the last would flip the reboot-pending predicate to YES.
