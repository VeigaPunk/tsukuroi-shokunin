source: S288 S289 — Linux v7.2.11 `Documentation/admin-guide/tainted-kernels.rst` (committed snapshot `.ufo/waves/round-69/before/src/tk-v7211.rst`, sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841) and `include/linux/vermagic.h` at the same tag (snapshot `.ufo/waves/round-69/before/src/vm-v7211.h`, sha256 0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea); both fetched from the stable tree at tag v7.2.11 (`.ufo/waves/round-69/before/src/FETCH.txt`) and re-fetched by a second route byte-for-byte (`.ufo/waves/round-69/probes/S1Scout-sources.md` §2). Host readings: `.ufo/waves/round-69/before/host.txt`, `.ufo/waves/round-69/probes/S2Scout-host.md`, and the scribe's read-only probes under `.ufo/waves/round-69/probes/SC1Scribe/`.
verified-at: 2026-11-03 (pinned bytes: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-69/before/src/` printed `tk-v7211.rst: OK` and `vm-v7211.h: OK`, rc 0; host re-read at 2026-11-03T23:20:43Z agrees field for field with the pre-declaration capture)
recheck: on-release — the next stable kernel tag re-fires this read; the fired re-read re-runs `sha256sum -c SHA256SUMS` in `.ufo/waves/round-69/before/src/` (both files must print `OK`) and re-reads `cat /proc/sys/kernel/tainted`, `uname -r`, `ls -1 /usr/lib/modules/`, `pacman -Qo /usr/lib/modules/$(uname -r)` and `modinfo -F vermagic /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst`. It fires sooner if any falsifier below fires.

# The vermagic stamp and the module-tree binding, with the taint table re-grounded at the running tag (round 69)

Scope: the `VERMAGIC_STRING` composition rule of `include/linux/vermagic.h` (S289), that rule's
instantiation in this host's dkms `nvidia` module and in one module of the other on-disk tree, the
release-token consequence for a module tree, and — as re-grounding only — the taint table at the
running kernel's own tag (S288). It does NOT cover module signature or keyring internals, DKMS build
policy, live patching, the kernel command line, module autoload policy, any remediation, or the
load-time comparison in `kernel/module.c` that is not inside the pinned bytes.

| row | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| KR1 | `VERMAGIC_STRING` is composed in one fixed order: the build's `UTS_RELEASE`, one space, then the SMP, preempt, mod_unload, modversions, arch-magic and randstruct token macros, each concatenated by the preprocessor. | source=S289 | snapshot=vm-v7211.h | digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea | quote="#define VERMAGIC_STRING \ UTS_RELEASE " " \ MODULE_VERMAGIC_SMP MODULE_VERMAGIC_PREEMPT \ MODULE_VERMAGIC_MODULE_UNLOAD MODULE_VERMAGIC_MODVERSIONS \ MODULE_ARCH_VERMAGIC \ MODULE_RANDSTRUCT" |
| KR2 | Every token after the release is a compile-time conditional, and `preempt_rt` takes precedence over `preempt`: `CONFIG_PREEMPT_RT` selects the real-time spelling while `CONFIG_PREEMPT_BUILD` selects the plain one, so one config change alters the stamp's middle tokens. | source=S289 | snapshot=vm-v7211.h | digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea | quote="#ifdef CONFIG_PREEMPT_RT #define MODULE_VERMAGIC_PREEMPT "preempt_rt " #elif defined(CONFIG_PREEMPT_BUILD) #define MODULE_VERMAGIC_PREEMPT "preempt "" |
| KR3 | This host's dkms `nvidia` module prints `7.2.11-arch1-1 SMP preempt mod_unload` with a trailing space, which is the composition instantiated with SMP, preempt and mod_unload non-empty and the modversions and randstruct tokens empty. | source=S289 | snapshot=vm-v7211.h | digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea | quote="MODULE_VERMAGIC_SMP MODULE_VERMAGIC_PREEMPT \ MODULE_VERMAGIC_MODULE_UNLOAD MODULE_VERMAGIC_MODVERSIONS" |
| KR4 | Because the release is the stamp's first token, a module built for another release carries that release there; one module of the `6.18.57-2-lts` tree prints `6.18.57-2-lts SMP preempt mod_unload`, so that tree cannot serve the running `7.2.11-arch1-1` kernel (inference: no foreign-module load was attempted). | source=S289 | snapshot=vm-v7211.h | digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea | quote="UTS_RELEASE " " \ MODULE_VERMAGIC_SMP MODULE_VERMAGIC_PREEMPT" |
| KR5 | Re-grounding only: S288's closed 0-19 taint table at v7.2.11 is byte-identical to S140's v7.2 copy, so the r27 entries KT1 and KT6 keep their decode at the running tag and this entry claims no new taint mechanism. | source=S288 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint" |

Reading. The host numbers are reads, not derivations. `cat /proc/sys/kernel/tainted` printed
`12288`; a bit sweep over indices 0-19 printed `1` at 12 and 13 and `0` elsewhere;
`echo $((4096+8192))` printed `12288`. `ls -1 /usr/lib/modules/` printed two trees,
`6.18.57-2-lts` and `7.2.11-arch1-1`. `modinfo -F vermagic` printed
`7.2.11-arch1-1 SMP preempt mod_unload` for
`/lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst` (one trailing space in the tool output)
and `6.18.57-2-lts SMP preempt mod_unload` for
`/usr/lib/modules/6.18.57-2-lts/kernel/arch/x86/crypto/aegis128-aesni.ko.zst`. `pacman -Qo` printed
`linux 7.2.11.arch1-1` and `linux-headers 7.2.11.arch1-1` for the running tree, and
`linux-lts 6.18.57-2` plus `linux-lts-headers 6.18.57-2` for the other; `uname -r` printed
`7.2.11-arch1-1`. The boot log prints `Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE` twice
(Nov 02 16:49:24 and 16:49:45), and the two `nvidia:` lines at Nov 02 12:07:17 name the causes.
The composition check is token by token: `SMP ` from `CONFIG_SMP`, `preempt ` from the
`CONFIG_PREEMPT_BUILD` branch (not `preempt_rt `), `mod_unload ` from `CONFIG_MODULE_UNLOAD`, and
empty strings for the modversions and randstruct tokens; concatenated behind `7.2.11-arch1-1 ` that
is exactly the observed string, trailing space included. The boot banner's `#1 SMP PREEMPT_DYNAMIC`
agrees with the SMP and preempt tokens without naming either config symbol.

The reboot-pending predicate measured, not assumed: the package field `7.2.11.arch1-1` maps to the
release `7.2.11-arch1-1` by replacing the dot before the arch component with a dash
(`s/\.(arch[0-9]+)-/-\1-/`, `.ufo/waves/round-69/probes/S2Scout-host.md` §C), the running release
equals that mapping, and the running tree is owned by the `linux` package — so no kernel reboot is
pending. Both trees are owned by installed packages; the non-running tree is a separately installed
`linux-lts`, not residue. The round-69 census arm reports this reading as a verdict-neutral
`KERNEL ... pending=NO` line.

## Relation to held ground

- `corpus/knowledge/kernel-taint-r27.md` (rows KT1-KT6, sources S140-S145) already holds the taint
  mechanism, the per-module reading, the clearing rule and the reporting consequence. KR5 here
  re-grounds KT1/KT6 at the running kernel's own tag — S288's bytes are byte-identical to S140's
  v7.2 snapshot (`cmp -s` rc 0, same sha256) — and claims no second mechanism. KT2-KT5 are not
  restated.
- `corpus/knowledge/driver-firmware-plane.md:85` holds an older `vermagic:
  7.2.3-arch1-3 SMP preempt mod_unload` string with an "Only kernel tree present" reading from the
  round-17 capture. That observation is not re-scored here; KR1-KR4 are about the composition rule
  and a later kernel release with a two-tree layout.
- `corpus/knowledge/boot-chain-r17.md` already lists both module trees as boot-input paths; this
  entry adds the ownership binding of each tree, not the fact that two trees exist.

## Limits

- Timing is bounded by the log itself. The two taint prints are at 16:49:24 and 16:49:45 of one
  boot; no per-bit timestamp exists, so assigning bit 12 to the out-of-tree load and bit 13 to the
  signature failure is [inference] from the closed table plus the two `nvidia:` lines, not a logged
  per-bit event.
- Privileged surfaces were not read. `/proc/sys/kernel/dmesg_restrict` reads `1` and
  `/sys/kernel/debug` is `drwx------ root root` (`.ufo/waves/round-69/probes/SC1Scribe/privilege-read.txt`);
  no unprivileged `dmesg` or debugfs read was attempted, and no privileged read was taken. Beyond
  the measured zero soft-lockup log lines (`grep -ciE 'soft lockup'` printed `0`, rc 1), the entry
  cannot decide whether a soft lockup occurred outside the retained log.
- The config symbols are inferred, not observed. No `/boot/config-*` or `/proc/config.gz` was
  read: `CONFIG_SMP`, `CONFIG_PREEMPT_BUILD`, `CONFIG_MODULE_UNLOAD` and the absence of
  `CONFIG_PREEMPT_RT`, `CONFIG_MODVERSIONS` and `RANDSTRUCT` are read off the produced string,
  which over-determines them but is not the config file. `MODULE_ARCH_VERMAGIC` comes from
  `<asm/vermagic.h>` (S289 line 10); its value is not inside the pinned bytes.
- No foreign-module load was attempted. Loading a `6.18.57-2-lts` module into this kernel is an
  operator action and was not taken, so the statement that the other tree cannot serve this kernel
  is [inference] from the header rule plus the observed token identity, not a measured load
  rejection.
- Vermagic coverage is two module files, not the trees. Only the dkms `nvidia` module and one
  `6.18.57-2-lts` module were probed with `modinfo -F vermagic`; "every module in either tree
  carries its tree's release" is not claimed.
- The Arch version conversion is host-measured, not upstream-documented: `7.2.11.arch1-1` (package
  field) to `7.2.11-arch1-1` (directory and `uname -r`) is a mapping observed on this host twice
  over (owner output and directory name); neither pin documents it.
- The `linux-lts` tree is a package fact, not a bootability fact: whether that tree is bootable,
  and how a boot entry selects it, is out of scope — the boot loader configuration was not read.
- Nothing here is a remediation: no package transaction, service action, privileged read, module
  load or write outside the wave directory was performed.

## Falsifiers

- KR1: a `VERMAGIC_STRING` definition whose order differs from S289's macro block, or a second
  composition site, falsifies the order claim.
- KR2: a build where `CONFIG_PREEMPT_RT` is set but the stamp carries `preempt ` instead of
  `preempt_rt ` falsifies the precedence claim.
- KR3/KR4: `modinfo -F vermagic` on a module in the running tree lacking the `7.2.11-arch1-1`
  first token, or a `6.18.57-2-lts` module whose first token is not `6.18.57-2-lts`, falsifies the
  instantiation and release-token rows.
- KR5: a taint reason documented outside bits 0-19 at v7.2.11, a second meaning attached to one
  bit, or S288's bytes differing from S140's copy, falsifies the closed-table claim.
- Binding: `/usr/lib/modules/$(uname -r)` being absent or owned by a package other than
  `linux`/`linux-headers`, or `pacman -Q linux` mapping to a release different from `uname -r`,
  would flip `pending` to YES.

## Erratum (2026-11-03, round 69) — the pending transform also covers an `-lts` package

Append-only; the Reading paragraph stays as written. Its transform (replace the dot before the arch
component) is the `linux` package's rule; an `-lts` package's tree name appends `-lts`
(`linux-lts 6.18.57-2` → tree `6.18.57-2-lts`), so the same-build test is not one string rewrite but
a candidate set: the package version itself, every single-dot rewrite of it, and `version-lts` for an
`-lts` package. The census arm implements that set (critic K1 A5 measured that the single-rewrite
rule read `pending=YES` on the installed LTS pair, which is false; the repaired arm reads
`pending=NO` there, `.ufo/waves/round-69/after/census-live-postrepair.txt`). The running tree's
`pending=NO` is unchanged.
