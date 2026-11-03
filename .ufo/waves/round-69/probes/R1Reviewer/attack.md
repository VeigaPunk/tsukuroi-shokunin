2026-11-03T23:24:13Z
# R1 adversarial C1 review

Axes: depth, C1 content fidelity, evidence binding; no tracked files changed.

## Findings (severity order)

### High — duplicate propositions cannot honestly score as five new depth rows
KR1 repeats the bitfield/table proposition already held in S140 and KT1; KR2 repeats KT1's exact host value, decoded indices and O/E interpretation. S140's committed raw snapshot and S288's new snapshot have identical independently recomputed SHA256, not merely equal titles. A stable-tag re-pin is re-grounding, not a second authority. Refuse KR1 and KR2 as additive depth evidence.

### Medium — KR5's quote does not establish its timing or falsifier claims
KR5 quotes the reassurance about running a tainted kernel, not timing, retention, or module-tree/vermagic predicates. Limits lines 32-33 assert the earliest retained kernel line is Nov 02 12:07:17; before/host.txt prints filtered nvidia messages, while SC1Scribe/host-read.txt prints only the LAST kernel lines (-n 2). Neither measures the earliest retained kernel line. Refuse KR5 as source-grounded depth evidence. This is not fixed by its valid digest and located quote.

### Medium — numeric shape passes conceal uncaptured operational facts
The note's recheck paragraph states desc marker line positions 1 and 4; Limits states dmesg_restrict=1 and debug mode 0700. Neither cited snapshot nor either capture prints those contextual facts. Four unbound numeric assertions; repeated literal digits elsewhere are not contextual evidence. The note also infers dmesg unavailability without an attempted command: a restriction setting alone does not establish process capability/access.

## Per-row re-derivation

The exact shared Python command below recomputes each digest from bytes independently, normalizes source/quote whitespace, counts quote and statement words, checks unique ids and drafted source registration. It is an independent audit, not the lane counter or selftest. Registered-at-measured-revision remains an integration obligation: S288/S289 are only drafts here.

### KR1 — structural PASS; content true; depth DUPLICATE / refuse
Statement 29 words; quote 19 words, found; digest equals tk-v7211.rst. Table lines 85-104 contain indices 0-19 and endpoint values 1, 524288. Quote establishes bitfield mechanism; other details require the named table. Same proposition is already registered in S140 and held KT1.

### KR2 — structural PASS; content PASS; depth RE-GROUNDING / refuse as new depth
Statement 31 words; quote 7 words, found; digest equals tk-v7211.rst. Independent integer computation returns set bits 12,13 and sum 12288. Pinned table lines 97-98 names O/4096 and E/8192; before/host.txt prints exactly `[O]=OOT_MODULE, [E]=UNSIGNED_MODULE`. No arithmetic or log contradiction. However KT1 already states the same 12288 decomposition on the same release. Current-boot recapture is maintenance, not a new mechanism.

### KR3 — structural PASS; content PASS with quotation limitation; ADDITIVE
Statement 40 words; quote 4 words, found across include lines 9-10; digest equals vm-v7211.h. Actual composition is lines 41-46: UTS_RELEASE, MODULE_VERMAGIC_SMP, MODULE_VERMAGIC_PREEMPT, MODULE_VERMAGIC_MODULE_UNLOAD, MODULE_VERMAGIC_MODVERSIONS, MODULE_ARCH_VERMAGIC, MODULE_RANDSTRUCT. CONFIG_SMP selects SMP; CONFIG_PREEMPT_RT takes priority over CONFIG_PREEMPT_BUILD (preempt_rt versus preempt); CONFIG_MODULE_UNLOAD selects mod_unload; CONFIG_MODVERSIONS selects modversions; RANDSTRUCT selects its hashed-seed suffix. Host string matches SMP/preempt/mod_unload with no modversions. No claim about the running kernel config is proved merely by modinfo on one disk file. The quote itself only establishes includes, not conditionals; full anchored source, not quote alone, supports statement. The held driver note only has an old string, not this conditional derivation.

### KR4 — structural PASS; content PASS as explicitly capture-grounded; RE-GROUNDING plus additive owner binding
Statement 38 words; quote 6 words, found; digest equals vm-v7211.h. Independent pacman -Q linux gives linux 7.2.11.arch1-1; uname -r gives 7.2.11-arch1-1. before/host.txt owner outputs bind that directory to linux and linux-headers. NO is a host-specific package/tree equality inference, not a general Arch version conversion proved by S289. Row explicitly says this, so no false upstream attribution. S289's sanity-stamp comment does not entail the owner/pending proposition. The old driver note has a single tree and older vermagic; current owner binding is new host ground, not new upstream mechanism.

### KR5 — structural PASS; content FAIL as source-grounded row; RE-GROUNDING / refuse
Statement 43 words; quote 19 words, found; digest equals tk-v7211.rst. Quote does not establish a per-bit temporal bound, journal retention, missing-tree behavior, or vermagic mismatch. A taint value of zero can invalidate this host reading but cannot invalidate KR1's general bitfield explanation. Likewise a config-dependent modversions/preempt_rt token is allowed by KR3, not a falsifier of its composition rule. Keep host-state recheck triggers distinct from mechanism falsifiers.

## Round-68 shape-only / number-drift attack

Scope for R1_DECL_UNBOUND: empirical/pre-state numeric assertions and qualitative conjuncts absent from the committed before/ outputs at declaration revision. Count each semantically distinct assertion once; exclude dates, revision hashes, source/row/round identifiers, and declared future thresholds/grammars (they are specifications, not measured facts). Band endpoints are separate numeric assertions.

Unbound numeric assertions:
- D1 depth score 8.
- D2 adjacency score 8.
- D3 saturation line 9.
- D4 stagnation window length 3.
- D5 stagnation current position 1.
- D6 v1 wave band lower endpoint 8.
- D7 v1 wave band upper endpoint 16.
- D8 wave seat count 13.
- D9 sha256sum -c returned rc 0: SHA256SUMS is a manifest, FETCH.txt names URLs and method, neither prints a check invocation/result. Independent rehash here confirms bytes, not the historical rc.
Unbound qualitative conjuncts:
- D10 no axes retired.
- D11 knowledge-source-ref-gate entered r68.
- D12 both source documents were READ before declaration (fetch receipt records fetching, not reading).
- D13 counter frozen before any note exists (before/ prints only its base absence, not code or a frozen instrument hash).
R1_DECL_UNBOUND=13 under this explicit contextual count (9 numeric, 4 qualitative). These are before/ binding gaps, not a claim all are false or unbound elsewhere in the repository.

Bound baseline numbers: package/release values, two module trees and package ownership, mask 12288, two named taints, vermagic, lsmod 132, zero matching soft-lockup lines appear in host.txt; 287 source rows, 177 cases, zero KERNEL occurrences, absent note/counter rc128 and absent S288/S289 appear in absence controls. Pin hashes are printed in SHA256SUMS and match independent recomputation. Canonical census rc0 is printed in census receipt; 287 is corroborated by absence controls rather than census output. S243 recheck receipt PRINTS changed/equal digest and a one-comment/outside-ranges assertion, but provides no raw diff; it also incorrectly claims a w1 scout reread at declaration time. This is assertion-only provenance, not direct line-cited verification; do not confuse printed prose with measured proof.

R1_NOTE_UNBOUND=4 contextual numeric facts: desc NAME marker line 1; desc VERSION marker line 4; dmesg_restrict value 1; debug mode 0700. All row numeric values otherwise appear in table/header/captures or the independent arithmetic receipt. Earlier-held release 7.2.3-arch1-3 is printed in the named held driver note (documented historical comparison, not invented live data). Dates are metadata; literal source hashes are recomputed. Earliest-retained qualifier is an additional qualitative overreach, not another numeric value invented from nothing.

## Held-knowledge overlap conclusion
KR1 DUPLICATE; KR2 RE-GROUNDING of identical KT1 result; KR3 ADDITIVE conditional mechanism; KR4 RE-GROUNDING/current owner binding; KR5 RE-GROUNDING/reporting-limit prose with unsupported timing and falsifier attachment. S288 and S140 are byte-identical. The entry contains one clear new mechanism (KR3) and some new host binding (KR4), but presenting the whole five-row entry as five new depth units re-scores held knowledge. Recommend refusing that aggregate depth claim without changing the frozen predicate. Structural validity alone does not buy novelty or entailment.

## Verification gaps and residual risk
LSP unavailable: reading xd://lsp returned `No such tool: xd://lsp`; there is no mounted LSP status device. Text/source reads are literal evidence, not semantic-callgraph proof. This item is Markdown/header content, not a runtime change; canonical-runtime/rerouting/resume-continuity tests are not applicable to this C1-only review. No census, selftest, git mutations, installs, host privilege changes, or other runtime invoked. Drafts are not integrated; no measured-revision source gate claimed.

## Audited draft (immutable review snapshot)

```markdown
source: S288 S289 — Linux v7.2.11 `Documentation/admin-guide/tainted-kernels.rst` (committed snapshot `.ufo/waves/round-69/before/src/tk-v7211.rst`, sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841) and `include/linux/vermagic.h` at the same tag (snapshot `.ufo/waves/round-69/before/src/vm-v7211.h`, sha256 0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea); both fetched from the stable tree at tag v7.2.11 (`.ufo/waves/round-69/before/src/FETCH.txt`). Host readings: the pre-declaration capture `.ufo/waves/round-69/before/host.txt` and this seat's own read-only probe `.ufo/waves/round-69/probes/SC1Scribe/host-read.txt`.
verified-at: 2026-11-03 (pinned bytes: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-69/before/src/` printed `tk-v7211.rst: OK` and `vm-v7211.h: OK`, rc 0; a live host re-read at 2026-11-03T23:20:43Z agrees with the capture field for field)
recheck: on-release — the next stable kernel tag re-fires this read of the v7.2.11 pins; the fired re-read re-runs `sha256sum -c SHA256SUMS` in `.ufo/waves/round-69/before/src/` (both files must print `OK`) and re-reads `cat /proc/sys/kernel/tainted`, `uname -r`, `ls -1 /usr/lib/modules/`, and `modinfo -F vermagic /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst`. Package readings are steered to file reads (QUALITY 26): `ls -d /var/lib/pacman/local/linux-[0-9]*` names the installed version, and the `desc` file under `linux-7.2.11.arch1-1/` carries the `%NAME%`/`%VERSION%` markers at lines 1 and 4 with their values on the following lines (`linux`, `7.2.11.arch1-1`); no package-manager invocation is prescribed. The same re-read fires sooner if any KR5 falsifier appears.

# The kernel taint mask, vermagic stamp and module-tree binding on this host (round 69)

Scope: the kernel taint mask read as `/proc/sys/kernel/tainted` and decoded with S288's closed bit table 0–19, the vermagic string's composition and `CONFIG` conditionals from S289, and this host's module-tree/package binding with the reboot-pending predicate. It does NOT cover signature verification or keyring internals, DKMS build policy, live patching, the kernel command line, module autoload policy, any remediation, or the `kernel/module.c` load-time comparison that is not inside the pinned bytes.

| row | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| KR1 | The kernel taint value in /proc/sys/kernel/tainted is a bitfield: S288's table assigns bit 0 through bit 19 one reason each, from 1 (proprietary module) to 524288 (fwctl debug write). | source=S288 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint" |
| KR2 | This host reads 12288, which is 4096 plus 8192, so exactly bits 12 and 13 are set and no other index in 0-19 is, matching the boot log's two bracket entries. | source=S288 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="13  _/E    8192  unsigned module was loaded" |
| KR3 | VERMAGIC_STRING concatenates UTS_RELEASE with the pieces chosen by CONFIG_SMP, CONFIG_PREEMPT_RT versus CONFIG_PREEMPT_BUILD, CONFIG_MODULE_UNLOAD, CONFIG_MODVERSIONS and RANDSTRUCT, and this host's nvidia module prints `7.2.11-arch1-1 SMP preempt mod_unload` with no modversions token; the header itself does not source the Arch package-version-to-tree conversion. | source=S289 | snapshot=vm-v7211.h | digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea | quote="#include <generated/utsrelease.h> #include <asm/vermagic.h>" |
| KR4 | Host capture, not the pins: /usr/lib/modules/7.2.11-arch1-1 is owned by linux 7.2.11.arch1-1 and linux-headers, uname reports 7.2.11-arch1-1, so pending is NO; the pkgver-to-tree mapping is host-measured, and the load-time use of the stamp sits in code outside these pins. | source=S289 | snapshot=vm-v7211.h | digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea | quote="Simply sanity version stamp for modules." |
| KR5 | Neither pin decides when the taint was set: the earliest retained journal line for this boot is the only bound, and the named falsifiers are a tainted value of 0, a missing running module tree, or a vermagic that lacks the running release. | source=S288 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="Don't worry too much about this, most of the time it's not a problem to run a tainted kernel" |

Reading. The host numbers are reads, not derivations. `cat /proc/sys/kernel/tainted` printed
`12288`; the bit sweep over indices 0-19 printed `1` at index 12 and at index 13 and `0`
everywhere else; `echo $((4096+8192))` printed `12288`. `ls -1 /usr/lib/modules/` printed two
trees, `6.18.57-2-lts` and `7.2.11-arch1-1`; `pacman -Qo` printed `linux 7.2.11.arch1-1` and
`linux-headers 7.2.11.arch1-1` for the running tree and `linux-lts 6.18.57-2` plus
`linux-lts-headers 6.18.57-2` for the other. `modinfo -F vermagic` on
`/lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst` printed
`7.2.11-arch1-1 SMP preempt mod_unload` (one trailing space in the tool output). The boot log
prints `Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE` twice, at Nov 02 16:49:24 and 16:49:45,
and the two `nvidia:` lines at Nov 02 12:07:17 name the causes: `loading out-of-tree module
taints kernel` and `module verification failed: signature and/or required key missing`. The
letters and the arithmetic agree: two set bits, two named taints.

## Limits

- Timing is not decidable beyond the log. The earliest retained kernel line for this boot is
  Nov 02 12:07:17; the taint print follows at 16:49:24. Whether the journal / ring buffer
  dropped earlier lines this boot cannot be read from this account, and no per-bit timestamp
  exists: assigning bit 12 to the out-of-tree load and bit 13 to the signature failure is
  [inference] from the closed table plus the two `nvidia:` lines, not a logged per-bit event.
- Privileged surfaces were not read. `/proc/sys/kernel/dmesg_restrict` reads `1`, so an
  unprivileged `dmesg` is unavailable, and `/sys/kernel/debug` is `drwx------ root root`
  (mode 0700); a root-only lockup or tracing report was not read and no privileged read was
  attempted. The entry cannot decide whether a soft lockup occurred outside the retained log,
  beyond the measured zero matching lines (`grep -ciE 'soft lockup'` printed `0`, rc 1).
- Vermagic coverage is one module, not the tree. Only the dkms `nvidia` module was probed with
  `modinfo -F vermagic`; the rest of the loaded set was not read one by one, so "every module in
  the running tree carries the running release" is not claimed here.
- The Arch version conversion is host-measured, not upstream-documented. `7.2.11.arch1-1`
  (package field) to `7.2.11-arch1-1` (directory and `uname -r`) is a mapping observed on this
  host twice over (owner output and directory name); neither pin documents it, and S289 only
  shows that `UTS_RELEASE` is the first component of the stamp.
- Overlap with `corpus/knowledge/driver-firmware-plane.md:85`. That line records
  `vermagic: 7.2.3-arch1-3 SMP preempt mod_unload` and `Only kernel tree present:` for the
  round-17 capture on kernel `7.2.3-arch1-3`. It is not re-scored, amended or superseded here:
  the same file already marks the "Only kernel tree present" sentence stale at its line 278,
  and KR3's host string is a later release (`7.2.11-arch1-1`) with two trees installed. The two
  readings are different host states, not a contradiction.
- The `linux-lts` tree is a package fact, not a bootability fact. Whether the `6.18.57-2-lts`
  tree is bootable, and how a boot entry would select it, is out of scope: the boot loader
  configuration was not read.
- Nothing here is a remediation and nothing was run beyond the reads above: no package
  transaction, no service action, no privileged read, no write outside the wave directory.

## Falsifiers

The rows are killed, not weakened, by these observables:

- KR1/KR2: `cat /proc/sys/kernel/tainted` reading `0`, or a non-zero value whose set bits fall
  outside indices 0-19, or a third set index in 0-19 on this host.
- KR2 arithmetic: `echo $((4096+8192))` printing anything but `12288`.
- KR3: `modinfo -F vermagic` on a module in the running tree lacking the `7.2.11-arch1-1`
  prefix, or carrying a `modversions` or `preempt_rt` token that the composition rules would
  then have to explain.
- KR4: `/usr/lib/modules/$(uname -r)` being absent, being owned by a package other than
  `linux`/`linux-headers`, or `pacman -Q linux` mapping to a release different from
  `uname -r` — the last would flip the reboot-pending predicate to YES.

```

## Exact commands, verbatim outputs and rc

```text
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T23:20:52Z
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree -r --name-only 920a9eea3c5c5400567be0e96141014f338973df .ufo/waves/round-69/before
.ufo/waves/round-69/before/absence-controls-receipt.txt
.ufo/waves/round-69/before/census-before-receipt.txt
.ufo/waves/round-69/before/host.txt
.ufo/waves/round-69/before/s243-v73-recheck.txt
.ufo/waves/round-69/before/src/FETCH.txt
.ufo/waves/round-69/before/src/SHA256SUMS
.ufo/waves/round-69/before/src/tk-v7211.rst
.ufo/waves/round-69/before/src/vm-v7211.h
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 920a9eea3c5c5400567be0e96141014f338973df:.ufo/waves/round-69/before/absence-controls-receipt.txt
[excerpt: S140 registered digest]
| S140 | Linux v7.2 Documentation/admin-guide/tainted-kernels.rst — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/tainted-kernels.rst | docs | A | What each kernel taint bit and letter means, how to decode /proc/sys/kernel/tainted, persistence of taint and its effect on bug reports, for the host kernel 7.2.11 | tag v7.2, Documentation/admin-guide/tainted-kernels.rst lines 8, 12, 51, 171; raw bytes sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841; snapshot .ufo/waves/round-27/sources/S140.rst (191 lines) | Taint is a set of bits readable in /proc/sys/kernel/tainted; 0 means untainted, bit 12 (O, 4096) marks an externally-built module and bit 13 (E, 8192) an unsigned module in a kernel supporting module signatures; the kernel stays tainted after the cause is undone; developers often ignore reports from tainted kernels | mined | 2026-10-22 | on-release | corpus/knowledge/kernel-taint-r27.md |
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 920a9eea3c5c5400567be0e96141014f338973df:.ufo/waves/round-69/before/census-before-receipt.txt
+ echo '# canonical source census at round-69 base (acce353bacad74043636018d829e9e9b8e0fdf1c)'
# canonical source census at round-69 base (acce353bacad74043636018d829e9e9b8e0fdf1c)
+ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	W04	S044 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S046 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S049 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S058 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/init across scopes
tsukuroi	W04	S082 duplicate url git-scm.com/docs/git-rev-parse/2.56.0 across scopes
tsukuroi	W04	S087 duplicate url archlinux.org/news across scopes
tsukuroi	W04	S089 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S090 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S092 duplicate url wiki.archlinux.org/title/System_maintenance?oldid=885170 across scopes
tsukuroi	W04	S095 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/merge_requests/482 across scopes
tsukuroi	W04	S098 duplicate url gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs across scopes
tsukuroi	W04	S105 duplicate url archlinux.org/news/update-to-ca-certificates-mozilla-31311-1-to-prevent-man-in-the-middle-attacks across scopes
tsukuroi	W04	S106 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S107 duplicate url man.archlinux.org/man/pacman.8 across scopes
tsukuroi	W04	S108 duplicate url wiki.archlinux.org/title/Downgrading_packages?oldid=887421 across scopes
tsukuroi	W04	S109 duplicate url gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/functions across scopes
tsukuroi	W04	S111 duplicate url gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/26.134.222-3/plymouth.initcpio_hook across scopes
tsukuroi	W04	S126 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/oomd.conf.xml across scopes
tsukuroi	W04	S136 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.resource-control.xml across scopes
tsukuroi	W04	S137 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml across scopes
tsukuroi	W04	S138 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/cgroup-v2.rst across scopes
tsukuroi	W04	S149 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
tsukuroi	W04	S155 duplicate url raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/mkfs.btrfs.rst across scopes
tsukuroi	W04	S158 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c across scopes
tsukuroi	W04	S182 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/mm/oom_kill.c across scopes
tsukuroi	W04	S184 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd-oomd.service.xml across scopes
tsukuroi	W04	S185 duplicate url raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/accounting/psi.rst across scopes
tsukuroi	W04	S203 duplicate url man7.org/linux/man-pages/man3/errno.3.html across scopes
tsukuroi	W04	S204 duplicate url man7.org/linux/man-pages/man3/errno.3.html across scopes
tsukuroi	W04	S217 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c across scopes
tsukuroi	W04	S221 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/util.c across scopes
tsukuroi	W04	S222 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c across scopes
tsukuroi	W04	S223 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/hook.c across scopes
tsukuroi	W04	S224 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc across scopes
tsukuroi	W04	S226 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/doc/alpm-hooks.5.asciidoc across scopes
tsukuroi	W04	S230 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c across scopes
tsukuroi	W04	S260 duplicate url docs.python.org/3.13/using/windows.html across scopes
tsukuroi	W04	S265 duplicate url learn.microsoft.com/en-us/windows-server/administration/windows-commands/sc-query across scopes
tsukuroi	W04	S280 duplicate url gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs across scopes
tsukuroi	W04	S281 duplicate url gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook across scopes
tsukuroi	W04	S283 duplicate url api.github.com/repos/systemd/systemd/releases/tags/v262 across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
+ echo 'census rc=0'
census rc=0
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 920a9eea3c5c5400567be0e96141014f338973df:.ufo/waves/round-69/before/host.txt
+ echo '# host capture 2026-11-03 (round 69 pre-declaration), read-only'
# host capture 2026-11-03 (round 69 pre-declaration), read-only
+ echo '## uname -r'
## uname -r
+ uname -r
7.2.11-arch1-1
+ echo '## /proc/sys/kernel/osrelease'
## /proc/sys/kernel/osrelease
+ cat /proc/sys/kernel/osrelease
7.2.11-arch1-1
+ echo '## pacman -Q linux linux-headers linux-lts'
## pacman -Q linux linux-headers linux-lts
+ pacman -Q linux linux-headers linux-lts
linux 7.2.11.arch1-1
linux-headers 7.2.11.arch1-1
linux-lts 6.18.57-2
+ echo '## pacman -Qo /usr/lib/modules/7.2.11-arch1-1'
## pacman -Qo /usr/lib/modules/7.2.11-arch1-1
+ pacman -Qo /usr/lib/modules/7.2.11-arch1-1
/usr/lib/modules/7.2.11-arch1-1/ is owned by linux 7.2.11.arch1-1
/usr/lib/modules/7.2.11-arch1-1/ is owned by linux-headers 7.2.11.arch1-1
+ echo '## pacman -Qo /usr/lib/modules/6.18.57-2-lts'
## pacman -Qo /usr/lib/modules/6.18.57-2-lts
+ pacman -Qo /usr/lib/modules/6.18.57-2-lts
/usr/lib/modules/6.18.57-2-lts/ is owned by linux-lts 6.18.57-2
/usr/lib/modules/6.18.57-2-lts/ is owned by linux-lts-headers 6.18.57-2
+ echo '## ls /usr/lib/modules/'
## ls /usr/lib/modules/
+ ls /usr/lib/modules/
6.18.57-2-lts
7.2.11-arch1-1
+ echo '## cat /proc/sys/kernel/tainted'
## cat /proc/sys/kernel/tainted
+ cat /proc/sys/kernel/tainted
12288
+ echo '## modinfo -F vermagic dkms nvidia module'
## modinfo -F vermagic dkms nvidia module
++ uname -r
+ modinfo -F vermagic /lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst
7.2.11-arch1-1 SMP preempt mod_unload 
+ echo '## lsmod line count'
## lsmod line count
++ lsmod
++ wc -l
132
+ echo '## journalctl -b -k taint lines'
## journalctl -b -k taint lines
++ grep -m3 'Tainted: \['
Nov 02 16:49:24 plazir27 kernel: Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE
Nov 02 16:49:45 plazir27 kernel: Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE
+ echo '## journalctl -b -k nvidia load lines'
## journalctl -b -k nvidia load lines
++ grep -m2 'nvidia: '
Nov 02 12:07:17 plazir27 kernel: nvidia: loading out-of-tree module taints kernel.
Nov 02 12:07:17 plazir27 kernel: nvidia: module verification failed: signature and/or required key missing - tainting kernel
+ echo '## journalctl -b -k soft lockup lines count'
## journalctl -b -k soft lockup lines count
++ grep -ciE 'soft lockup'
0
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 920a9eea3c5c5400567be0e96141014f338973df:.ufo/waves/round-69/before/s243-v73-recheck.txt
# QUALITY 98 watch — S243 stable-series pin re-read (standing duty, round 69)
S243 pins Linux v7.2.11 fs/btrfs/sysfs.c, raw sha256 ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43
upstream release beyond the pin: v7.3 (stable tree tag; the watch trigger)
## fetch: git.kernel.org stable plain fs/btrfs/sysfs.c?h=v7.3
098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377  /fast/scratch/hyaku/tsukuroi-r69/l1/src/sysfs-v73.c
## verdict: CHANGED (digest differs from the pin); v7.3 digest equals registry S287's torvalds v7.3 pin 098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377
## S243 registered anchor ranges 72-74, 2021-2049, 2113: at v7.3 the only v7.2->v7.3 change is one comment line (S287, round 68), outside those ranges; anchors hold
## affected knowledge entries: corpus/knowledge/btrfs-scrub-record-r44.md, btrfs-scrub-grounding-r45.md -> no contradiction measured this round (line-cited re-read by the w1 scout)
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 920a9eea3c5c5400567be0e96141014f338973df:.ufo/waves/round-69/before/src/FETCH.txt
url https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/tainted-kernels.rst?h=v7.2.11
url https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/include/linux/vermagic.h?h=v7.2.11
fetched 2026-11-03 by tsukuroi L1 round 69; method curl -sS --max-time 60
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 920a9eea3c5c5400567be0e96141014f338973df:.ufo/waves/round-69/before/src/SHA256SUMS
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  tk-v7211.rst
0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea  vm-v7211.h
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 920a9eea3c5c5400567be0e96141014f338973df:.ufo/waves/round-69/before/src/tk-v7211.rst
Tainted kernels
---------------

The kernel will mark itself as 'tainted' when something occurs that might be
relevant later when investigating problems. Don't worry too much about this,
most of the time it's not a problem to run a tainted kernel; the information is
mainly of interest once someone wants to investigate some problem, as its real
cause might be the event that got the kernel tainted. That's why bug reports
from tainted kernels will often be ignored by developers, hence try to reproduce
problems with an untainted kernel.

Note the kernel will remain tainted even after you undo what caused the taint
(i.e. unload a proprietary kernel module), to indicate the kernel remains not
trustworthy. That's also why the kernel will print the tainted state when it
notices an internal problem (a 'kernel bug'), a recoverable error
('kernel oops') or a non-recoverable error ('kernel panic') and writes debug
information about this to the logs ``dmesg`` outputs. It's also possible to
check the tainted state at runtime through a file in ``/proc/``.


Tainted flag in bugs, oops or panics messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You find the tainted state near the top in a line starting with 'CPU:'; if or
why the kernel was tainted is shown after the Process ID ('PID:') and a shortened
name of the command ('Comm:') that triggered the event::

	BUG: unable to handle kernel NULL pointer dereference at 0000000000000000
	Oops: 0002 [#1] SMP PTI
	CPU: 0 PID: 4424 Comm: insmod Tainted: P        W  O      4.20.0-0.rc6.fc30 #1
	Hardware name: Red Hat KVM, BIOS 0.5.1 01/01/2011
	RIP: 0010:my_oops_init+0x13/0x1000 [kpanic]
	[...]

You'll find a 'Not tainted: ' there if the kernel was not tainted at the
time of the event; if it was, then it will print 'Tainted: ' and characters
either letters or blanks. In the example above it looks like this::

	Tainted: P        W  O

The meaning of those characters is explained in the table below. In this case
the kernel got tainted earlier because a proprietary Module (``P``) was loaded,
a warning occurred (``W``), and an externally-built module was loaded (``O``).
To decode other letters use the table below.


Decoding tainted state at runtime
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

At runtime, you can query the tainted state by reading
``cat /proc/sys/kernel/tainted``. If that returns ``0``, the kernel is not
tainted; any other number indicates the reasons why it is. The easiest way to
decode that number is the script ``tools/debugging/kernel-chktaint``, which your
distribution might ship as part of a package called ``linux-tools`` or
``kernel-tools``; if it doesn't, you can download the script from
`git.kernel.org <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/tools/debugging/kernel-chktaint>`_
and execute it with ``sh kernel-chktaint``, which would print something like
this on the machine that had the statements in the logs that were quoted earlier::

	Kernel is Tainted for following reasons:
	 * Proprietary module was loaded (#0)
	 * Kernel issued warning (#9)
	 * Externally-built ('out-of-tree') module was loaded  (#12)
	See Documentation/admin-guide/tainted-kernels.rst in the Linux kernel or
	 https://www.kernel.org/doc/html/latest/admin-guide/tainted-kernels.html for
	 a more details explanation of the various taint flags.
	Raw taint value as int/string: 4609/'P        W  O     '

You can try to decode the number yourself. That's easy if there was only one
reason that got your kernel tainted, as in this case you can find the number
with the table below. If there were multiple reasons you need to decode the
number, as it is a bitfield, where each bit indicates the absence or presence of
a particular type of taint. It's best to leave that to the aforementioned
script, but if you need something quick you can use this shell command to check
which bits are set::

	$ for i in $(seq 20); do echo $(($i-1)) $(($(cat /proc/sys/kernel/tainted)>>($i-1)&1));done

Table for decoding tainted state
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

===  ===  ======  ========================================================
Bit  Log  Number  Reason that got the kernel tainted
===  ===  ======  ========================================================
  0  G/P       1  proprietary module was loaded
  1  _/F       2  module was force loaded
  2  _/S       4  kernel running on an out of specification system
  3  _/R       8  module was force unloaded
  4  _/M      16  processor reported a Machine Check Exception (MCE)
  5  _/B      32  bad page referenced or some unexpected page flags
  6  _/U      64  taint requested by userspace application
  7  _/D     128  kernel died recently, i.e. there was an OOPS or BUG
  8  _/A     256  ACPI table overridden by user
  9  _/W     512  kernel issued warning
 10  _/C    1024  staging driver was loaded
 11  _/I    2048  workaround for bug in platform firmware applied
 12  _/O    4096  externally-built ("out-of-tree") module was loaded
 13  _/E    8192  unsigned module was loaded
 14  _/L   16384  soft lockup occurred
 15  _/K   32768  kernel has been live patched
 16  _/X   65536  auxiliary taint, defined for and used by distros
 17  _/T  131072  kernel was built with the struct randomization plugin
 18  _/N  262144  an in-kernel test has been run
 19  _/J  524288  userspace used a mutating debug operation in fwctl
===  ===  ======  ========================================================

Note: The character ``_`` is representing a blank in this table to make reading
easier.

More detailed explanation for tainting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 0)  ``G`` if all modules loaded have a GPL or compatible license, ``P`` if
     any proprietary module has been loaded.  Modules without a
     MODULE_LICENSE or with a MODULE_LICENSE that is not recognised by
     insmod as GPL compatible are assumed to be proprietary.

 1)  ``F`` if any module was force loaded by ``insmod -f``, ``' '`` if all
     modules were loaded normally.

 2)  ``S`` if the kernel is running on a processor or system that is out of
     specification: hardware has been put into an unsupported configuration,
     therefore proper execution cannot be guaranteed.
     Kernel will be tainted if, for example:

     - on x86: PAE is forced through forcepae on intel CPUs (such as Pentium M)
       which do not report PAE but may have a functional implementation, an SMP
       kernel is running on non officially capable SMP Athlon CPUs, MSRs are
       being poked at from userspace.
     - on arm: kernel running on certain CPUs (such as Keystone 2) without
       having certain kernel features enabled.
     - on arm64: there are mismatched hardware features between CPUs, the
       bootloader has booted CPUs in different modes.
     - certain drivers are being used on non supported architectures (such as
       scsi/snic on something else than x86_64, scsi/ips on non
       x86/x86_64/itanium, have broken firmware settings for the
       irqchip/irq-gic on arm64 ...).
     - x86/x86_64: Microcode late loading is dangerous and will result in
       tainting the kernel. It requires that all CPUs rendezvous to make sure
       the update happens when the system is as quiescent as possible. However,
       a higher priority MCE/SMI/NMI can move control flow away from that
       rendezvous and interrupt the update, which can be detrimental to the
       machine.

 3)  ``R`` if a module was force unloaded by ``rmmod -f``, ``' '`` if all
     modules were unloaded normally.

 4)  ``M`` if any processor has reported a Machine Check Exception,
     ``' '`` if no Machine Check Exceptions have occurred.

 5)  ``B`` If a page-release function has found a bad page reference or some
     unexpected page flags. This indicates a hardware problem or a kernel bug;
     there should be other information in the log indicating why this tainting
     occurred.

 6)  ``U`` if a user or user application specifically requested that the
     Tainted flag be set, ``' '`` otherwise.

 7)  ``D`` if the kernel has died recently, i.e. there was an OOPS or BUG.

 8)  ``A`` if an ACPI table has been overridden.

 9)  ``W`` if a warning has previously been issued by the kernel.
     (Though some warnings may set more specific taint flags.)

 10) ``C`` if a staging driver has been loaded.

 11) ``I`` if the kernel is working around a severe bug in the platform
     firmware (BIOS or similar).

 12) ``O`` if an externally-built ("out-of-tree") module has been loaded.

 13) ``E`` if an unsigned module has been loaded in a kernel supporting
     module signature.

 14) ``L`` if a soft lockup has previously occurred on the system.

 15) ``K`` if the kernel has been live patched.

 16) ``X`` Auxiliary taint, defined for and used by Linux distributors.

 17) ``T`` Kernel was build with the randstruct plugin, which can intentionally
     produce extremely unusual kernel structure layouts (even performance
     pathological ones), which is important to know when debugging. Set at
     build time.

 18) ``N`` if an in-kernel test, such as a KUnit test, has been run.

 19) ``J`` if userspace opened /dev/fwctl/* and performed a FWTCL_RPC_DEBUG_WRITE
     to use the devices debugging features. Device debugging features could
     cause the device to malfunction in undefined ways.
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 920a9eea3c5c5400567be0e96141014f338973df:.ufo/waves/round-69/before/src/vm-v7211.h
/* SPDX-License-Identifier: GPL-2.0 */
#ifndef _LINUX_VERMAGIC_H
#define _LINUX_VERMAGIC_H

#ifndef INCLUDE_VERMAGIC
#error "This header can be included from kernel/module.c or *.mod.c only"
#endif

#include <generated/utsrelease.h>
#include <asm/vermagic.h>

/* Simply sanity version stamp for modules. */
#ifdef CONFIG_SMP
#define MODULE_VERMAGIC_SMP "SMP "
#else
#define MODULE_VERMAGIC_SMP ""
#endif
#ifdef CONFIG_PREEMPT_RT
#define MODULE_VERMAGIC_PREEMPT "preempt_rt "
#elif defined(CONFIG_PREEMPT_BUILD)
#define MODULE_VERMAGIC_PREEMPT "preempt "
#else
#define MODULE_VERMAGIC_PREEMPT ""
#endif
#ifdef CONFIG_MODULE_UNLOAD
#define MODULE_VERMAGIC_MODULE_UNLOAD "mod_unload "
#else
#define MODULE_VERMAGIC_MODULE_UNLOAD ""
#endif
#ifdef CONFIG_MODVERSIONS
#define MODULE_VERMAGIC_MODVERSIONS "modversions "
#else
#define MODULE_VERMAGIC_MODVERSIONS ""
#endif
#ifdef RANDSTRUCT
#define MODULE_RANDSTRUCT "RANDSTRUCT_" RANDSTRUCT_HASHED_SEED
#else
#define MODULE_RANDSTRUCT
#endif

#define VERMAGIC_STRING 						\
	UTS_RELEASE " "							\
	MODULE_VERMAGIC_SMP MODULE_VERMAGIC_PREEMPT 			\
	MODULE_VERMAGIC_MODULE_UNLOAD MODULE_VERMAGIC_MODVERSIONS	\
	MODULE_ARCH_VERMAGIC						\
	MODULE_RANDSTRUCT

#endif /* _LINUX_VERMAGIC_H */
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 920a9eea3c5c5400567be0e96141014f338973df:SCORECARD.md
[excerpt: frozen Round 69 declaration only]
## Round 69 — declaration (2026-11-03, base `acce353b`, written before any after-measurement)

Lowest non-retired axis: **depth (8, tied with adjacency 8)**; saturation line 9 / window 3 unchanged;
none retired. Capability `knowledge-source-ref-gate` entered r68, so the stagnation window is at 1 of 3
and the nudge does not waive the lowest-axis duty. Two claims on two distinct axes (depth; operability).
This round carries the r68 closure routings as work, not as extra claims: the content-sensitive counter is
C1's counting command (R68-SHAPE-ONLY-DECLARED-COUNTER), and the declaration-hygiene criterion is a routed
repair (`corpus/QUALITY.md`, R68 routed item 2).

Pre-declaration receipts, disclosed in order. (a) The two source documents for C1 were fetched and read
before this text and committed as snapshots: Linux v7.2.11 `Documentation/admin-guide/tainted-kernels.rst`
sha256 `727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841` and
`include/linux/vermagic.h` sha256 `0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea`, both
from the stable tree at tag v7.2.11; `sha256sum -c` rc 0 (`.ufo/waves/round-69/before/src/{FETCH.txt,SHA256SUMS}`).
(b) Host capture, read-only (`.ufo/waves/round-69/before/host.txt`): `uname -r` `7.2.11-arch1-1`;
`pacman -Q linux` `7.2.11.arch1-1`; `pacman -Q linux-lts` `6.18.57-2`; `/usr/lib/modules/` holds two trees, each
owned by its package (`pacman -Qo`); `/proc/sys/kernel/tainted` `12288`; the boot's kernel log prints
`Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE`; `modinfo -F vermagic` on the dkms nvidia module
`7.2.11-arch1-1 SMP preempt mod_unload`; `lsmod | wc -l` 132; soft-lockup log lines this boot 0.
(c) QUALITY 98 watch fired on Linux v7.3; S243's v7.2.11 `fs/btrfs/sysfs.c` pin (`ce146120…`) re-read at the
v7.3 stable tag → digest `098cb522…` = **changed**, equal to S287's torvalds-v7.3 pin, the single change being
the comment line outside S243's registered ranges (`.ufo/waves/round-69/before/s243-v73-recheck.txt`).
(d) Canonical census before: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root
/home/vgpnk/Projects/shokunin tsukuroi` → rc 0, 287 rows (`.ufo/waves/round-69/before/census-before-receipt.txt`).
(e) Do-nothing controls at base (`before/absence-controls-receipt.txt`): C1 note `cat-file` rc 128; C1 counter
`cat-file` rc 128; `^| KR[0-9]` rows in the tree 0; `grep -c KERNEL tools/tsukuroi-census.sh` 0; selftest
**177** cases; SOURCES 287 rows; S288 and S289 rows 0.

| # | axis/type | claim | before → after (frozen predicate) | counting command | kill rule |
|---|---|---|---|---|---|
| C1 | depth (lowest tied, 8; SOURCED — S288, S289) | `corpus/knowledge/kernel-taint-plane-r69.md`: the kernel taint, vermagic and module-tree plane measured against this host, rows `KR1`–`KR5`. Each row is `| KR<n> | <statement, ≥ 12 words> | source=S### | snapshot=<file> | digest=<64-hex> | quote="<text>" |`; the round's **content-sensitive** counter `tools/count-kr-rows-r69.py` is frozen before any note exists and verifies per row: unique id, statement ≥ 12 words, the `source=` id present in `corpus/SOURCES.md` at the measured revision, `digest=` equal to the sha256 of the named committed snapshot under `.ufo/waves/round-69/before/src/`, and `quote=` ≤ 25 words located verbatim in that snapshot | note absent (`git cat-file -e <rev>:corpus/knowledge/kernel-taint-plane-r69.md` rc 128) and counter absent (rc 128), SOURCES **287** → note present at the measured revision, counter present, `KR_ROWS=5 KR_VERIFIED=5` rc 0; `corpus/SOURCES.md` rows **≥ 289** with S288 and S289 on the lines directly after S287, `awk -F'|' '/^\| S28[89] /{print NF}'` = 13, 13; Gate quote ≤ 25 words; knowledge-header gate PASS; canonical census validate rc 0 | `python3 tools/count-kr-rows-r69.py --revision <rev> --snapshots .ufo/waves/round-69/before/src` (print `KR_ROWS` / `KR_VERIFIED`); `git show <rev>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3,}'` | any row failing one clause reads `KR_VERIFIED < 5` → honest stop; the counter's pre-data battery must fail all five malformed fixtures (duplicate id, wrong digest, absent quote, unregistered source id, 7-word statement) while the well-formed control reads 5 — a battery that passes any malformed fixture makes the counter vacuous and C1 is not declared verified |
| C2 | operability (9; capability `kernel-arm`) | `probe_kernel_arm` + one verdict-neutral `KERNEL` line in `tools/tsukuroi-census.sh`: `KERNEL kernel-plane release=<uts> pkg=<name> pkgver=<ver> modules_tree=PRESENT\|ABSENT\|UNKNOWN tainted=<int\|UNKNOWN> taint_bits=<csv\|none\|UNKNOWN> pending=NO\|YES\|UNKNOWN unreadable=<n> [detail=...]`, decoded with the closed bit→log table 0–19 of S288; read-only, no privilege, no package transaction, never a rollup term and never an exit-code input | `grep -c 'KERNEL' tools/tsukuroi-census.sh` **0**, selftest **177** → label present (`grep -c 'KERNEL kernel-plane'` ≥ 1), selftest **≥ 185** PASS rc 0 with ≥ 8 new `R69-C2` hermetic cases; live run prints exactly one `KERNEL` line carrying every field exactly once in contract order; the verdict-bearing lines and the exit code identical to the pre-arm baseline; knowledge-header, registry-coverage and line-endings gates PASS | `grep -c 'KERNEL kernel-plane' tools/tsukuroi-census.sh`; `bash tools/tsukuroi-census.sh --selftest`; `bash tools/tsukuroi-census.sh 2>/dev/null \| grep -c '^KERNEL kernel-plane'` | not hermetic under the existing fixture/override pattern → honest stop; a field absent, duplicated or out of contract order on the live line → honest stop; any rollup or exit-code change → honest stop |

Causal separability: C1 touches only its note, its two SOURCES rows, the new counter and receipts; C2 touches
only `tools/tsukuroi-census.sh`. Each verifies without the other. Counter strictness is frozen here, before any
note or selftest case exists; both new table-row predicates are strict from the start (distinct ids, non-empty
evidence cells, no fenced-block or prose row). Routed repairs this round (not claims): the declaration-hygiene
criterion in `corpus/QUALITY.md` with a receipt applying it to the round-68 declaration; the QUALITY 98 S243
re-read above; one considerthese proposal mined; assimilation: none (L0 `tsukuroi | round-64` and its addendum
remain open and unanswered in `.ufo/l0-questions.md`).

Wave w1: one v1 wave, band 8–16, 13 seats; seat shape and counts are fixed in `.ufo/waves/round-69/w1-spec.json`.

**planned (next round):** R66-M3/M4 frozen-counter amendments where still reachable; the AR resolve-then-count
debt; the kernel arm's second-device and non-systemd-boot coverage; no amendment of this round's frozen predicates.

rc=0

$ sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/sources/S140.rst /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/before/src/tk-v7211.rst
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/sources/S140.rst
727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/before/src/tk-v7211.rst
rc=0

$ pacman -Q linux
linux 7.2.11.arch1-1
rc=0

$ uname -r
7.2.11-arch1-1
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show acce353bacad74043636018d829e9e9b8e0fdf1c:corpus/knowledge/kernel-taint-r27.md
# Kernel taint on this host — round 27 entry

source: S140, S141, S142, S143, S144, S145 (Linux v7.2, all `mined`, tier A; Gate in `corpus/lessons/round-27.md`)
capture: `.ufo/waves/round-27/capture/capture.txt` (sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, 2026-10-22T15:55:13Z, no sudo)
verified-at: 2026-10-22 (capture 2026-10-22T15:55:13Z, kernel 7.2.11-arch1-1, nvidia-open-dkms 615.78.08-1, dkms 3.4.4-1; sources Linux v7.2)
recheck: on-release (kernel or nvidia-open-dkms update), and after any boot that changes the loaded module set
companion: `corpus/knowledge/kernel-taint-r27.json` holds the same six rows with their quotes and capture pointers; a correction to a row is appended to both files.

## Scope

What the number in `/proc/sys/kernel/tainted` means on this host, which modules set it and why, whether it can be cleared, and what it means for kernel bug reports. Read-only: no row authorises loading, unloading or signing a module, enrolling a key, or writing a sysctl.

Relation to earlier notes: `corpus/knowledge/driver-firmware-plane.md` lines 101-106 recorded the two taint lines as an observation on 2026-10-13 (driver 610.57.04) with no mechanism. This entry adds the mechanism, the decoding, the per-module reading and the operator actions, re-observed on driver 615.78.08. That note's Secure Boot reading was not re-checked this round.

## Rows

| id | question | host reading (capture) | verdict |
|---|---|---|---|
| KT1 | How the taint number is encoded; what 12288 decodes to | 12288 = bit 12 (O) + bit 13 (E); no other bit, so no warning (W), oops (D) or soft lockup (L) recorded this boot | HEALTHY |
| KT2 | What O means and when it is set | set at module load when modinfo lacks the `intree` tag; nvidia printed `loading out-of-tree module taints kernel.` at 17.5 s of boot 0; DKMS modules are out-of-tree by construction | HEALTHY |
| KT3 | What E means; why a module with a named signer still sets it | the kernel trusts only keys in its built-in and secondary keyrings; in permissive mode (sig_enforce N, CONFIG_MODULE_SIG_FORCE not set) a module whose key is unavailable loads and sets E; `modinfo -F signer` = `DKMS module signing key` shows a signature is attached, not that the kernel trusts the key | UNVERIFIED |
| KT4 | What `/sys/module/<name>/taint` shows; which modules and packages | per-module letters, read-only; nvidia, nvidia_drm, nvidia_modeset, nvidia_uvm print OE; their files under `/lib/modules/7.2.11-arch1-1/updates/dkms/` are owned by no package (built on the host by dkms 3.4.4-1 from nvidia-open-dkms 615.78.08-1) | HEALTHY |
| KT5 | Whether taint can be cleared | not while the kernel runs: unloading the module does not clear it, and a sysctl write only adds bits; the mask starts again at the next boot [inf: static initialiser of tainted_mask] | HEALTHY |
| KT6 | What taint means for bug reports | the `Tainted:` field of every oops on this host will show O and E; reports from tainted kernels are often ignored upstream | HEALTHY (reporting limit, not host damage) |

Full statements, actions, quotes and capture pointers: the JSON companion.

## Operator actions (summary)

- Read `cat /proc/sys/kernel/tainted`; expect 12288 while the nvidia DKMS modules are loaded. Any further bit is a new event: look it up in the tainted-kernels table, and look for W, D or L causes in `journalctl -k -b 0`.
- Name the culprit modules from `/sys/module/*/taint`. An O or E on any module outside the nvidia DKMS set is a finding.
- After a kernel or driver update, compare the loaded nvidia module version with the installed nvidia-open-dkms and nvidia-utils versions; pacman owns no DKMS module file, so pacman checks cannot see a stale build.
- Before enabling `module.sig_enforce=1` or a lockdown mode that requires signatures, the DKMS key must be trusted by the kernel, or the nvidia modules will be refused at load. Trusting it is a key-management decision for the operator; the private key is credential material and is never read (ConnSiblingOverlap: kagi's ground, route under ADJ-02).
- For an upstream kernel report, reproduce in a boot without the nvidia modules, or send the tainted report to the out-of-tree module's maintainer first.

## What this entry does not claim

- Which keyring check failed for the DKMS signature (the trusted keyrings were not read), or whether Secure Boot is on now.
- Anything about the contents of the module files or the GPU firmware (shipped-artifact analysis is contested between kaidoku and revenger, ADJ-06).
- That taint means the host is unhealthy: the kernel documentation says a tainted kernel is usually not a problem.

## Wave-2 corrections (round 27, attempt 2, appended 2026-10-22)

Two in-place edits, disclosed here (QUALITY 60): the KT6 table cell above read `DEGRADED (reporting limit, not host damage)` and now reads `HEALTHY (reporting limit, not host damage)`, so the three renderings agree (JSON and `SKILL.md` already said HEALTHY; the verdict reads the host at capture time, and the row says the host is not harmed; wave-2 CritC1Learning, CritClaimSizingFinal, RevRowKT6). A `verified-at:` header line was inserted (QUALITY 8; wave-2 CritTrendVerdicts). Nothing else above is rewritten; the corrections below are appended, and the JSON companion carries the same items under `corrections_r27_a2`.

- KT1: bit 7 (D) means the kernel died recently from an oops or a BUG (S140 lines 92 and 159), not only an oops. `tools/debugging/kernel-chktaint` is a script in the kernel source tree; it is not installed on this host, so decode with the S140 table (RevRowKT1, CritC1Learning).
- KT2: the one-time message prints while bit 12 is still clear kernel-wide (S143 `if (!test_taint(TAINT_OOT_MODULE))` before the `pr_warn`), not strictly for the boot's first out-of-tree module: a root write to the sysctl can set bit 12 first (S141 lines 127-129), and then no module prints it. "Out-of-tree by construction" and "built outside the kernel tree" are [inf]: the kernel tests only the missing `intree` modinfo tag, and the capture did not read that tag (RevRowKT2).
- KT3: "in permissive mode a module whose key is unavailable loads and sets E" holds only when no signature-requiring lockdown is active: S144 ends `module_sig_check` with `return security_locked_down(LOCKDOWN_MODULE_SIGNATURE);` (line 124). The lockdown state was not captured. S145's registry teaches cell also omits two rejections its source states: an unparsable signature is rejected in either mode, and a known key whose signature does not match is rejected even in permissive mode (S145 lines 66-67, 273-276) (RevRowKT3, RevSrcS145).
- KT4: "built on the host by dkms 3.4.4-1 from nvidia-open-dkms 615.78.08-1" is [inf]: the capture shows the installed package versions and that no package owns the module files, not the build event. The culprit loop prints `No such file or directory` for every module without a `taint` attribute and exits 1; skip absent files with `[ -e "$f" ] || continue` (CritC1Learning, CritClaimSizingFinal, RevSkillKernelTaint).
- KT6: "an oops on this host will show O and E" holds for an oops in a boot after the nvidia modules load (from 17.5 s of boot 0 in the capture); an oops before that shows `Not tainted` (S140 lines 35-36). "Every boot that loads the nvidia DKMS modules is tainted O and E" is [inf] from KT2 and KT5; only boot 0 was captured. The summary advice above "or send the tainted report to the out-of-tree module's maintainer first" has no source sentence and is withdrawn (RevRowKT6, CritC1Learning).
- What `verified_rows` counts: complete evidence links per row (sources, Gate quote equal to the located-quote cell, snapshot digest, capture pointers, SKILL row). It does not test that a verdict is true: KT3 counts with the verdict UNVERIFIED, and a copy with KT6 set to BLOCKED still counts 6. Wave-2 CritC1Tool found rule gaps (a generic one-word quote, a quote from a source the row does not list, any heading containing "gate") that the live rows do not use; MutC1Counter killed 27 of 30 rule mutants.
- KT5: "a sysctl write only adds bits" holds for bits below `TAINT_FLAGS_COUNT`; higher bits in the written value are ignored, and with `panic_on_taint=nousertaint` a write that would add the panic bit is refused with `-EINVAL` (S141 lines 96-133, 120-121). The next-boot value is the kernel's built-in initial value (zero unless `CONFIG_RANDSTRUCT` is set), still [inf]. The unload-trace remark tagged unverified is supported by S143 (`last_unloaded_module`, lines 871-874 and 3972-3975) (RevRowKT5).
- KT4, further (RevRowKT4): per-module and kernel-wide bits are not always set together. S143 sets a module's own bits alone when it inherits P (line 1254), sets kernel-wide bits with no module name for ndiswrapper and forced removal (lines 2620, 747), and an unloaded module's taint outlives it; so `/sys/module/<name>/taint` names the culprit for O and E on this host, not for every letter. S143's teaches cell names only O and E although `add_taint_module` has six more call sites. `nvidia-peermem.ko.zst` also sits unowned in `updates/dkms/` and was not read by the capture. `modinfo` reads the file on disk; the loaded module's version is `/sys/module/<name>/version`.
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show acce353bacad74043636018d829e9e9b8e0fdf1c:corpus/knowledge/driver-firmware-plane.md
[excerpt: lines 82-87]
Loaded module identity (`modinfo nvidia`):
`filename: /lib/modules/7.2.3-arch1-3/updates/dkms/nvidia.ko.zst`
(12,027,573 bytes on disk), `version: 610.57.04`,
`vermagic: 7.2.3-arch1-3 SMP preempt mod_unload`. Only kernel tree present:
`ls /lib/modules/` → `7.2.3-arch1-3` (the 7.1.4 build from the pacman log is
gone).
rc=0

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show acce353bacad74043636018d829e9e9b8e0fdf1c:corpus/SOURCES.md
[excerpt: S140 registered digest]
| S140 | Linux v7.2 Documentation/admin-guide/tainted-kernels.rst — https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/admin-guide/tainted-kernels.rst | docs | A | What each kernel taint bit and letter means, how to decode /proc/sys/kernel/tainted, persistence of taint and its effect on bug reports, for the host kernel 7.2.11 | tag v7.2, Documentation/admin-guide/tainted-kernels.rst lines 8, 12, 51, 171; raw bytes sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841; snapshot .ufo/waves/round-27/sources/S140.rst (191 lines) | Taint is a set of bits readable in /proc/sys/kernel/tainted; 0 means untainted, bit 12 (O, 4096) marks an externally-built module and bit 13 (E, 8192) an unsigned module in a kernel supporting module signatures; the kernel stays tainted after the cause is undone; developers often ignore reports from tainted kernels | mined | 2026-10-22 | on-release | corpus/knowledge/kernel-taint-r27.md |
rc=0

$ python3 -c 'from pathlib import Path
import hashlib,re
b=Path('"'"'/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69'"'"')
n=(b/'"'"'drafts/c1/note.md'"'"').read_text()
s=(b/'"'"'drafts/c1/sources-rows.md'"'"').read_text()
ids=[]
for line in n.splitlines():
 if not re.match(r'"'"'^\| KR[1-5] \|'"'"',line): continue
 c=[x.strip() for x in line.split('"'"'|'"'"')[1:-1]]
 rid,statement,source,snapshot,digest,quote=c
 ids.append(rid)
 p=b/'"'"'before/src'"'"'/snapshot.removeprefix('"'"'snapshot='"'"')
 actual=hashlib.sha256(p.read_bytes()).hexdigest()
 q=quote.removeprefix('"'"'quote="'"'"')[:-1]
 normalized='"'"' '"'"'.join(p.read_text().split())
 found='"'"' '"'"'.join(q.split()) in normalized
 wc=len(q.split()); sc=len(statement.split())
 reg=bool(re.search(r'"'"'^\| '"'"'+re.escape(source.removeprefix('"'"'source='"'"'))+r'"'"' \|'"'"',s,re.M))
 ok=actual==digest.removeprefix('"'"'digest='"'"') and found and wc<=25 and sc>=12 and reg
 print(f'"'"'{rid} digest={actual} digest_match={actual==digest.removeprefix("digest=")} quote_found={found} quote_words={wc} statement_words={sc} source_in_draft={reg} STRUCTURAL={"PASS" if ok else "FAIL"}'"'"')
print('"'"'unique_ids='"'"'+str(len(ids)==len(set(ids))))
for line in s.splitlines():
 if re.match(r'"'"'^\| S28[89] \|'"'"',line): print(line.split('"'"'|'"'"')[1].strip()+'"'"' NF='"'"'+str(len(line.split('"'"'|'"'"'))))
print('"'"'12288_set_bits='"'"'+'"'"','"'"'.join(str(i) for i in range(20) if 12288>>i&1))
print('"'"'4096+8192='"'"'+str(4096+8192))
'
KR1 digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 digest_match=True quote_found=True quote_words=19 statement_words=29 source_in_draft=True STRUCTURAL=PASS
KR2 digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 digest_match=True quote_found=True quote_words=7 statement_words=31 source_in_draft=True STRUCTURAL=PASS
KR3 digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea digest_match=True quote_found=True quote_words=4 statement_words=40 source_in_draft=True STRUCTURAL=PASS
KR4 digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea digest_match=True quote_found=True quote_words=6 statement_words=38 source_in_draft=True STRUCTURAL=PASS
KR5 digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 digest_match=True quote_found=True quote_words=19 statement_words=43 source_in_draft=True STRUCTURAL=PASS
unique_ids=True
S288 NF=13
S289 NF=13
12288_set_bits=12,13
4096+8192=12288
rc=0

$ sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/note.md /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/sources-rows.md
811b647e1d129d1ff6066f64bb3e5061ab099be320a692d69953b2275e76054c  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/note.md
40cbf15f535cd5edd0564c43318f80a0483b653b289bc083f5844deaa3bfeddb  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/sources-rows.md
rc=0

$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T23:24:13Z
rc=0

```

R1_ROWS_PASS=5/5 R1_QUOTES=5/5 R1_DECL_UNBOUND=13 R1_NOTE_UNBOUND=4 R1_VERDICT=refuse
R1_VERDICT=refuse rows=KR1,KR2 (held depth re-scored),KR5 (quote does not support timing/falsifiers); structural row pass count is not a semantic verdict.


# Superseding correction review — 2026-11-03T23:26:00Z

Audited corrected note hash: e2fb6b64d523e2372a1e42d28d1f47f2e698c14a025ef896cd8cfa6f6bc16e4f  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/note.md
The earlier review above is retained as a snapshot, not an assertion that removed text remains. Revised row structural checks still pass; exact new counts and commands follow. KR1/KR2 now honestly acknowledge re-grounding, resolving concealment of overlap but not making them new depth units. KR3 now quotes the composition itself and is the clear additive mechanism.

Resolved: the cited privilege-read.txt now prints dmesg_restrict 1 and debug directory permissions; pacman-localdesc.txt prints marker lines 1 and 4; timing-and-crosschecks.txt prints the first retained boot banner and count 13754. Earlier four numeric binding gaps are closed by the newly explicit capture links.

Remaining/new medium findings:
- KR4's `so that tree cannot serve this kernel` is not entailed by VERMAGIC_STRING composition. The pin does not contain the loader comparison/enforcement path; a different token establishes string mismatch, not universal inability to load. The Limits inference label discloses but does not supply the missing premise. Refuse this unqualified row; retain the directly observed mismatch only.
- KR5 says taint reports a cause `not a fault`; the quoted source says MOST OF THE TIME it is not a problem, and its table explicitly includes kernel oops, machine-check and soft-lockup faults. Diagnostic/non-verdict metadata is reasonable; categorically excluding faults is not. Refuse the categorical wording.
- Revised prose says nothing earlier was emitted because the first retained line is the banner. A retained first line does not establish completeness of emission/retention. It now establishes earliest retained banner, which is sufficient; remove the absolute completeness conclusion.
- dmesg unavailable remains inferred from restriction value without a denied command/capability observation.
- The note now claims a measured LTS module vermagic/release token, but neither named host-read.txt nor timing-and-crosschecks.txt prints an LTS modinfo result. Directory/package release numbers appear in before/host.txt; the module-specific release-token measurement does not. R1_NOTE_UNBOUND=1 under contextual counting (LTS module release token 6.18.57-2-lts). It is a missing measurement receipt, not an asserted false value.

Disposition: KR1 re-grounding/duplicate authority; KR2 re-grounding; KR3 additive; KR4 owner-state re-grounding with new but unsupported enforcement implication; KR5 diagnostic re-grounding with categorical overreach. Recommend refusing KR4/KR5's unsupported assertions and any aggregate claim of five novel depth units. Frozen structural counter clauses are not changed.

New direct inspection evidence: read absolute probes/SC1Scribe/{privilege-read,pacman-localdesc,timing-and-crosschecks,host-read}.txt; full numeric marker outputs are in those files. LTS result absent in those windows and directory list at review time. These are source-file inspection results, not executed host probes by R1.

```text
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T23:26:00Z
rc=0

$ python3 -c 'from pathlib import Path
import hashlib,re
b=Path('"'"'/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69'"'"')
n=(b/'"'"'drafts/c1/note.md'"'"').read_text()
s=(b/'"'"'drafts/c1/sources-rows.md'"'"').read_text()
ids=[]
for line in n.splitlines():
 if not re.match(r'"'"'^\| KR[1-5] \|'"'"',line): continue
 c=[x.strip() for x in line.split('"'"'|'"'"')[1:-1]]
 rid,statement,source,snapshot,digest,quote=c
 ids.append(rid)
 p=b/'"'"'before/src'"'"'/snapshot.removeprefix('"'"'snapshot='"'"')
 actual=hashlib.sha256(p.read_bytes()).hexdigest()
 q=quote.removeprefix('"'"'quote="'"'"')[:-1]
 normalized='"'"' '"'"'.join(p.read_text().split())
 found='"'"' '"'"'.join(q.split()) in normalized
 wc=len(q.split()); sc=len(statement.split())
 reg=bool(re.search(r'"'"'^\| '"'"'+re.escape(source.removeprefix('"'"'source='"'"'))+r'"'"' \|'"'"',s,re.M))
 ok=actual==digest.removeprefix('"'"'digest='"'"') and found and wc<=25 and sc>=12 and reg
 print(f'"'"'{rid} digest={actual} digest_match={actual==digest.removeprefix("digest=")} quote_found={found} quote_words={wc} statement_words={sc} source_in_draft={reg} STRUCTURAL={"PASS" if ok else "FAIL"}'"'"')
print('"'"'unique_ids='"'"'+str(len(ids)==len(set(ids))))
for line in s.splitlines():
 if re.match(r'"'"'^\| S28[89] \|'"'"',line): print(line.split('"'"'|'"'"')[1].strip()+'"'"' NF='"'"'+str(len(line.split('"'"'|'"'"'))))
print('"'"'12288_set_bits='"'"'+'"'"','"'"'.join(str(i) for i in range(20) if 12288>>i&1))
print('"'"'4096+8192='"'"'+str(4096+8192))
'
KR1 digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 digest_match=True quote_found=True quote_words=19 statement_words=39 source_in_draft=True STRUCTURAL=PASS
KR2 digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 digest_match=True quote_found=True quote_words=7 statement_words=31 source_in_draft=True STRUCTURAL=PASS
KR3 digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea digest_match=True quote_found=True quote_words=16 statement_words=31 source_in_draft=True STRUCTURAL=PASS
KR4 digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea digest_match=True quote_found=True quote_words=6 statement_words=69 source_in_draft=True STRUCTURAL=PASS
KR5 digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 digest_match=True quote_found=True quote_words=19 statement_words=60 source_in_draft=True STRUCTURAL=PASS
unique_ids=True
S288 NF=13
S289 NF=13
12288_set_bits=12,13
4096+8192=12288
rc=0

$ sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/note.md
e2fb6b64d523e2372a1e42d28d1f47f2e698c14a025ef896cd8cfa6f6bc16e4f  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/note.md
rc=0

```

Corrected note snapshot:
```markdown
source: S288 S289 — Linux v7.2.11 `Documentation/admin-guide/tainted-kernels.rst` (committed snapshot `.ufo/waves/round-69/before/src/tk-v7211.rst`, sha256 727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841) and `include/linux/vermagic.h` at the same tag (snapshot `.ufo/waves/round-69/before/src/vm-v7211.h`, sha256 0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea); both fetched from the stable tree at tag v7.2.11 (`.ufo/waves/round-69/before/src/FETCH.txt`). Host readings: the pre-declaration capture `.ufo/waves/round-69/before/host.txt`, the host scout `probes/S2Scout-host.md`, and this seat's own read-only probes `probes/SC1Scribe/{host-read,privilege-read,pacman-localdesc,timing-and-crosschecks,quote-check,note-selfcheck}.txt`.
verified-at: 2026-11-03 (pinned bytes: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-69/before/src/` printed `tk-v7211.rst: OK` and `vm-v7211.h: OK`, rc 0; the live host re-read at 2026-11-03T23:20:43Z agrees with the capture field for field; the `6.18.57-2-lts` tree's own module was probed at 23:25Z; `cmp -s` proves S288's snapshot byte-identical to S140's v7.2 copy, rc 0)
recheck: on-release — the next stable kernel tag re-fires this read of the v7.2.11 pins; the fired re-read re-runs `sha256sum -c SHA256SUMS` in `.ufo/waves/round-69/before/src/` (both files must print `OK`) and re-reads `cat /proc/sys/kernel/tainted`, `uname -r`, `ls -1 /usr/lib/modules/`, `modinfo -F vermagic /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst`, and one module from each other tree. Package readings are steered to file reads (QUALITY 26): `ls -d /var/lib/pacman/local/linux-[0-9]*` names the installed version, and the `desc` file under `linux-7.2.11.arch1-1/` carries the `%NAME%`/`%VERSION%` markers at lines 1 and 4 with their values on the following lines (`linux`, `7.2.11.arch1-1`); no package-manager invocation is prescribed. The same re-read fires sooner if any KR5 falsifier appears.

# The taint table at its own tag, the vermagic composition rule, and the release token that binds a module tree (round 69)

Scope: this entry re-grounds the taint decode at the running kernel's own release tag, then spends its depth on what the lane does not hold — the `VERMAGIC_STRING` composition rule of `include/linux/vermagic.h` (S289), that rule's instantiation in this host's dkms `nvidia` module, and the release-token consequence for the two `/usr/lib/modules` trees and their package owners. It does NOT cover module signature or keyring internals, DKMS build policy, live patching, the kernel command line, module load policy, a foreign-module load attempt (operator-owned), or the `kernel/module.c` comparison that is not inside the pinned bytes.

| row | statement | source | snapshot | digest | quote |
|---|---|---|---|---|---|
| KR1 | S288 fixes the closed 0-19 taint table at v7.2.11, the running kernel's own tag, and its bytes are identical to S140's v7.2 copy, so this row re-grounds KT1/KT6 of corpus/knowledge/kernel-taint-r27.md at that tag and claims no new taint mechanism. | source=S288 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="as it is a bitfield, where each bit indicates the absence or presence of a particular type of taint" |
| KR2 | Re-grounding KT1 of corpus/knowledge/kernel-taint-r27.md, this host's 12288 is 4096 plus 8192, so only bits 12 and 13 are set, matching the boot log's [O] and [E]; no new mechanism is claimed. | source=S288 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="13  _/E    8192  unsigned module was loaded" |
| KR3 | S289 composes VERMAGIC_STRING as UTS_RELEASE, one space, then MODULE_VERMAGIC_SMP, MODULE_VERMAGIC_PREEMPT (preempt_rt when CONFIG_PREEMPT_RT is set, else preempt when CONFIG_PREEMPT_BUILD), MODULE_VERMAGIC_MODULE_UNLOAD, MODULE_VERMAGIC_MODVERSIONS, MODULE_ARCH_VERMAGIC and MODULE_RANDSTRUCT, each present only when its condition holds. | source=S289 | snapshot=vm-v7211.h | digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea | quote="#define VERMAGIC_STRING \ UTS_RELEASE " " \ MODULE_VERMAGIC_SMP MODULE_VERMAGIC_PREEMPT \ MODULE_VERMAGIC_MODULE_UNLOAD MODULE_VERMAGIC_MODVERSIONS \ MODULE_ARCH_VERMAGIC \ MODULE_RANDSTRUCT" |
| KR4 | The host dkms nvidia module prints `7.2.11-arch1-1 SMP preempt mod_unload`: SMP, preempt and mod_unload are present while modversions, randstruct and arch magic are absent; a module built for another release carries that release as its first token, the 6.18.57-2-lts tree's module prints `6.18.57-2-lts`, so that tree cannot serve this kernel, and since the running tree is owned by linux 7.2.11.arch1-1 and linux-headers with uname matching, no reboot is pending. | source=S289 | snapshot=vm-v7211.h | digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea | quote="Simply sanity version stamp for modules." |
| KR5 | Applicability is diagnostic: the taint value reports a cause, not a fault, and the composition rule is pinned at v7.2.11 alone; the unknowns are the config symbols, read off the produced string, and the named falsifiers are a running-tree module without the running release token, an ownership change of the running tree, or a taint reading outside the v7.2.11 table. | source=S288 | snapshot=tk-v7211.rst | digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 | quote="Don't worry too much about this, most of the time it's not a problem to run a tainted kernel" |

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
module file cannot cross trees without the token mismatching.

The boot log's extent is measured, not assumed: `journalctl -b -k --no-pager -o short-iso` holds
13754 lines and its first line is the kernel banner at `2026-11-02T12:07:17-03:00`, i.e. the
start of this boot's kernel log, so the two `nvidia:` lines at the same second are within the
retained window and nothing earlier is retained because nothing earlier was emitted.

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
  an operator action and was not taken, so the statement that the other tree cannot serve this
  kernel is [inference] from the header rule plus the observed token identity, not a measured
  load rejection.
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

```

R1_ROWS_PASS=5/5 R1_QUOTES=5/5 R1_DECL_UNBOUND=13 R1_NOTE_UNBOUND=1 R1_VERDICT=refuse
R1_VERDICT=refuse rows=KR4 (enforcement beyond pin),KR5 (categorically excludes faults); KR1/KR2 are transparent re-grounding, not new depth.


# FINAL SUPERSEDING REVIEW — 2026-11-03T23:27:19Z

This section supersedes all earlier row dispositions and note-gap counts; earlier snapshots remain historical evidence of the attack/correction sequence.

Final note hash: 951d77fc333e874779950ca79a6403bcd6b614797231e5533cfd1a3d191745e3  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/note.md

All requested semantic corrections are present: KR1/KR2 explicitly re-ground held knowledge; KR3 quotes actual composition; KR4 confines itself to observed release-token mismatch and disclaims loader enforcement; KR5 says cause rather than verdict and acknowledges benign/severe possibilities; retention prose no longer asserts nothing earlier was emitted. Newly retained lts-module-vermagic.txt prints the missing LTS module token and running module token, each rc0, with its exploratory/rerun provenance disclosed. The prior four contextual numeric gaps are supported by explicit privilege/desc captures; the subsequent LTS-token gap is now also closed.

Per-row final classification:
- KR1 PASS fidelity; RE-GROUNDING of duplicate S140 authority, no new mechanism.
- KR2 PASS fidelity; RE-GROUNDING of held KT1 host decode, independently matches arithmetic/table/boot log.
- KR3 PASS fidelity; ADDITIVE vermagic conditional/composition mechanism. CONFIG_SMP, CONFIG_PREEMPT_RT versus CONFIG_PREEMPT_BUILD, CONFIG_MODULE_UNLOAD, CONFIG_MODVERSIONS and RANDSTRUCT are named and bounded by pinned source; MODULE_ARCH_VERMAGIC remains an included architecture component, not inspected architecture implementation.
- KR4 PASS fidelity; ADDITIVE two-tree stamp/owner instantiation with RE-GROUNDING of old vermagic observation. Package-to-tree conversion is host-specific, measured, not claimed as upstream rule or loader rejection.
- KR5 PASS fidelity as a diagnostic applicability/limit row, RE-GROUNDING of held taint-reporting limits; not another independent mechanism.

The entry as a whole contains a genuine depth move in conditional vermagic construction plus two-tree instantiation, NOT five new independent knowledge mechanisms. Its explicit held-ground disclosures now make that distinction honest. S288 remains byte-identical to S140 and should never be advertised as a second document. Final C1 row-fidelity recommendation is pass; this is not an admission, score award, or integration gate result.

Residual declaration hygiene: R1_DECL_UNBOUND remains 13 under the earlier explicit before/-only contextual count. Those predeclaration binding gaps are not cured by after-the-fact note receipts. R1_NOTE_UNBOUND=0 for the final audited note's contextual numeric claims. Integration must still exercise the frozen counter, measured-revision source registration, canonical source census and lane gates; R1 did not run them.

Supplemental source receipt reviewed: absolute probes/SC1Scribe/lts-module-vermagic.txt, timestamp 2026-11-03T23:26:53Z, commands and verbatim outputs:
```text
$ modinfo -F vermagic /usr/lib/modules/6.18.57-2-lts/kernel/arch/x86/crypto/aegis128-aesni.ko.zst
6.18.57-2-lts SMP preempt mod_unload 
rc=0
$ modinfo -F vermagic /lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst
7.2.11-arch1-1 SMP preempt mod_unload 
rc=0
```
These commands are SC1's retained receipt, not a claim R1 reran them.

Final independent audit commands and outputs:
```text
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T23:27:19Z
rc=0

$ python3 -c 'from pathlib import Path
import hashlib,re
b=Path('"'"'/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69'"'"')
n=(b/'"'"'drafts/c1/note.md'"'"').read_text()
s=(b/'"'"'drafts/c1/sources-rows.md'"'"').read_text()
ids=[]
for line in n.splitlines():
 if not re.match(r'"'"'^\| KR[1-5] \|'"'"',line): continue
 c=[x.strip() for x in line.split('"'"'|'"'"')[1:-1]]
 rid,statement,source,snapshot,digest,quote=c
 ids.append(rid)
 p=b/'"'"'before/src'"'"'/snapshot.removeprefix('"'"'snapshot='"'"')
 actual=hashlib.sha256(p.read_bytes()).hexdigest()
 q=quote.removeprefix('"'"'quote="'"'"')[:-1]
 normalized='"'"' '"'"'.join(p.read_text().split())
 found='"'"' '"'"'.join(q.split()) in normalized
 wc=len(q.split()); sc=len(statement.split())
 reg=bool(re.search(r'"'"'^\| '"'"'+re.escape(source.removeprefix('"'"'source='"'"'))+r'"'"' \|'"'"',s,re.M))
 ok=actual==digest.removeprefix('"'"'digest='"'"') and found and wc<=25 and sc>=12 and reg
 print(f'"'"'{rid} digest={actual} digest_match={actual==digest.removeprefix("digest=")} quote_found={found} quote_words={wc} statement_words={sc} source_in_draft={reg} STRUCTURAL={"PASS" if ok else "FAIL"}'"'"')
print('"'"'unique_ids='"'"'+str(len(ids)==len(set(ids))))
for line in s.splitlines():
 if re.match(r'"'"'^\| S28[89] \|'"'"',line): print(line.split('"'"'|'"'"')[1].strip()+'"'"' NF='"'"'+str(len(line.split('"'"'|'"'"'))))
print('"'"'12288_set_bits='"'"'+'"'"','"'"'.join(str(i) for i in range(20) if 12288>>i&1))
print('"'"'4096+8192='"'"'+str(4096+8192))
'
KR1 digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 digest_match=True quote_found=True quote_words=19 statement_words=39 source_in_draft=True STRUCTURAL=PASS
KR2 digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 digest_match=True quote_found=True quote_words=7 statement_words=31 source_in_draft=True STRUCTURAL=PASS
KR3 digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea digest_match=True quote_found=True quote_words=16 statement_words=31 source_in_draft=True STRUCTURAL=PASS
KR4 digest=0556c28fe7711d0383dbd5e91667560c1b96a9a914d4d15e2fdd85dea3671aea digest_match=True quote_found=True quote_words=6 statement_words=83 source_in_draft=True STRUCTURAL=PASS
KR5 digest=727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841 digest_match=True quote_found=True quote_words=19 statement_words=68 source_in_draft=True STRUCTURAL=PASS
unique_ids=True
S288 NF=13
S289 NF=13
12288_set_bits=12,13
4096+8192=12288
rc=0

$ sha256sum /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/note.md
951d77fc333e874779950ca79a6403bcd6b614797231e5533cfd1a3d191745e3  /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/drafts/c1/note.md
rc=0

```

Final audited note snapshot:
```markdown
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

```

R1_ROWS_PASS=5/5 R1_QUOTES=5/5 R1_DECL_UNBOUND=13 R1_NOTE_UNBOUND=0 R1_VERDICT=pass
R1_VERDICT=pass refused_rows=none; depth novelty limited to KR3 and current KR4 instantiation, not KR1/KR2 re-grounding.
