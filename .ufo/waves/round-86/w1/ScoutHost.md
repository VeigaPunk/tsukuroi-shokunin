# ScoutHost — round 86 w1 — host re-read through the round-86 parse

Seat: ScoutHost (scout, read-only host re-read; leaf; no subagents dispatched)
Lane measured: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` @ `1e1caabcdd740a6429dd31d7aba3b725ff8c677d`
(`git -C … rev-parse master` → `1e1caabcdd740a6429dd31d7aba3b725ff8c677d`; `git log --oneline -3 master` →
`1e1caabc round-86: C2 entry hibernation-boot-parse-r86 …`, `dc884949 round-86: candidate gate …`,
`2f67de80 round-86: freeze C1 battery r86 …`).
*Lane tip moved during my seat* (L1 landed `b96dc4be round-86: landing — …` at ~18:5x while I was
running); every measurement above was taken against the `1e1caabc` tree (the gate and entry files I ran
are unchanged between the two commits for the paths I exercised — `tools/check-hibernate-resume.py`,
`tools/resume-gate-battery-r86.py`, `corpus/knowledge/hibernation-boot-parse-r86.md`). I did not modify
any lane file: my only writes are `.ufo/waves/round-86/w1/ScoutHost.md` and
`.ufo/waves/round-86/w1/ScoutHost/`.
Scratch (removed on exit): `/fast/scratch/hyaku/tsukuroi-r86/ScoutHost/`.
Receipts: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-86/w1/ScoutHost/`.

## 0. HEADLINE — host-side incident caused by this seat (read this first)

**I modified two boot artifacts on the host.** `objcopy --dump-section` is *not* read-only: with no
output file it rewrites its input in place. Two `sudo -n objcopy --dump-section .cmdline=… /boot/EFI/Linux/<uki>`
calls (18:11:21 and 18:11:22 today) rewrote **both** UKIs in place:

| file | sha256 before (recorded in `/boot/limine.conf`) | sha256 after my objcopy |
|---|---|---|
| `/boot/EFI/Linux/omarchy_linux.efi` | `b990d8c6…` (limine.conf `#` suffix) | `cf6f8782b5d7d502bd2ed42b3f88d9612c15612833b6f6b99372bf0b235d0c37` |
| `/boot/EFI/Linux/omarchy_linux-lts.efi` | `a68c281d…` (limine.conf `#` suffix) | `3af6fbd6df61a53e6ef02bd4737d73e7176bcf53208f6373a5277aef02678711` |

Measured blast radius (controlled reproduction on a pristine copy of the untouched
`/boot/432d02b544a5459ebbff9c42ec68334d/limine_history/omarchy_linux.efi_sha256_2e9c9bdc…`, file
`objtest2/A.efi` → `objtest2/B.efi`, one `objcopy --dump-section`):

```
$ cmp -l A.efi B.efi | wc -l
5
$ cmp -l A.efi B.efi
137   5 206
138 177 107
139 262 356
217 300 175
218 264 175
$ stat -c '%n %s' A.efi B.efi   →  284439552  284439552   (size unchanged)
```

* exactly **5 bytes** change: PE `TimeDateStamp` low 3 bytes (offset 136..138) and 2 bytes of the PE
  optional-header checksum field (offset 216..217); the section table, `.text/.rodata/.data/.sbat/
  .sdmagic/.reloc/.uname/.osrel/.cmdline/.linux/.initrd` payloads and the `.cmdline` content are
  byte-identical (`diff <(objdump -h A) <(objdump -h B)` → only the filename line differs; `.cmdline`
  dumps equal);
* file size and every loadable section are unchanged, so the UKIs still contain the same kernel,
  initramfs and cmdline;
* the **integrity suffix in `/boot/limine.conf` is a BLAKE2b-512 of the whole file** — proved by
  hashing the pristine history copy: `blake2b(full) = 822299bbdaf0d4ede97d341fd5fcfa73fb3ca3942b7dcc597a79e7b46e69ec8f3eaabb194c431112de1c97b15345f1ca64adb0438b94d8fc8100cd393ce98024`
  = the `#` suffix limine.conf records for that exact path (sha256/md5/sha1/sha3/blake2s/blake3 all
  **do not** match). Hence the recorded `#` suffix for the two live UKIs no longer matches the files
  on disk;
* consequence at next boot: limine verifies the `#hash` of the kernel path; with
  `hash_mismatch_panic: no` in `/boot/limine.conf` limine prints a mismatch warning and waits for a
  keypress (`Y` continues) instead of panicking — i.e. an unattended reboot of this host may stall on
  that prompt. Secure Boot is inactive on this host (`/sys/firmware/efi/efivars/SecureBoot-8be4df61…`
  data = `00`), so no firmware-level signature check is in play, and both UKIs carry no PE
  certificate table (`cert_table_off 0`, `cert_size 0`), so the 5 changed bytes cannot invalidate a
  signature.
* **I did not repair it**: restoring byte-exactly requires writing `/boot`, which is outside my seat
  bounds ("never touch /boot"). Proposed repair for the L1/operator (see §6 and §6.1).

Everything else in this report is read-only observation. Nothing else on the host was written by me
(`sudo` was used only for `cat`/`stat`/`ls`/`grep`/`objdump -h`/`objcopy --dump-section`/`cp` to
scratch/`sha256sum`/`filefrag`-free reads; no `pacman`, no `mkinitcpio`, no `limine`, no swap/hibernate
action, no `/sys` or `/proc` write).

### 0.1 Repair procedure for the operator (scratch-verified, NOT executed — writing `/boot` is out of bounds for this seat)

Facts the repair depends on (all measured):

* the only bytes that differ from the pre-incident file are **5**: PE `TimeDateStamp` bytes at file
  offsets **136–138** and PE optional-header `CheckSum` bytes at offsets **216–217**;
* the **payload is bit-identical** — section table and every section payload are unchanged; measured
  sha256 of the section bytes of the current live files:
  `.linux 7ca8265d…` (linux) / `29f1531e…` (lts), `.initrd 279d492e…` / `8c0f611f…`,
  `.cmdline d8cd5382…` (both, identical to the untouched history copy) — see
  `ScoutHost/objcopy-incident/CURRENT-HASHES.txt`;
* the `#<hash>` suffix in `/boot/limine.conf` is **BLAKE2b-512 of the whole file** (proved by hashing the
  pristine history copy: `822299bb…` == the suffix limine.conf records for that path; sha256/md5/sha1/
  sha3/blake2s/blake3 all differ). Current BLAKE2b-512 of the two live files:
  `57f5eb94…` (linux) and `eff78d32…` (lts) — i.e. both now mismatch the recorded `b990d8c6…` / `a68c281d…`;
* `objcopy` is deterministic in the timestamp: `SOURCE_DATE_EPOCH=<ts> objcopy --dump-section …` reproduces
  the identical byte stream (verified: on the pristine history copy, `SOURCE_DATE_EPOCH=1790082821 objcopy`
  yields a file byte-identical to the input, `cmp -l` = 0 differences).

Recommended order (each is a host mutation → operator-owned):

1. **Regenerate the config (smallest change).** Re-run `limine-entry-tool` (the tool that wrote
   `/boot/limine.conf`) so the `#<hash>` suffixes are recomputed from the files actually on disk, i.e.
   `57f5eb94…` for `omarchy_linux.efi` and `eff78d32…` for `omarchy_linux-lts.efi`. This restores
   unattended boot without touching the UKIs.
2. **Rebuild the UKIs** via `kernel-install` (90-uki-copy.install) so the images themselves are pristine
   and the config is regenerated in the same step.
3. **Byte-exact restore** (only if the L1 wants the files themselves unchanged): recover the original
   `TimeDateStamp` of each UKI (the build time of the UKI — the live pair was built when the 7.2.11 /
   6.18.57 UKIs were last regenerated) and the original `CheckSum` field, then patch offsets 136–138 and
   216–217 only. The `CheckSum` field is not a plain sum of the file (I fitted `~fold16(sum16) + filesize`
   and the standard PE 16-bit ones-complement checksum; neither reproduces the stored value for any of the
   four files I had: pristine history copy, its objcopy'd twin, and the two live files), so the operator
   should obtain the two original 4-byte header fields from the build tooling rather than from
   arithmetic. **Unknown to me**: the original timestamps/checksums of the two live UKIs — the pristine
   bytes of the *live* pair are not on the host (the `limine_history` copies are different builds: same
   `.linux`, different `.initrd`).
4. **Do nothing** is safe for the kernel itself (the UKI payload and the `.cmdline` inside it are intact,
   Secure Boot is inactive and the images carry no PE certificate table, so no signature is invalidated) but
   leaves limine's integrity check failing on the two UKI paths.

**Rule to add to the round's tool discipline:** `objcopy --dump-section` is **not** a read-only probe —
with no output file it rewrites its input in place (5 bytes here). Use `objdump -s -j .cmdline <file>`
(read-only; I used it too and it does not modify the input) or copy the file to scratch first.

## 1. Host values read (this seat, 2026-11-06 ~18:00–18:40, read-only)

```
$ uname -r
7.2.11-arch1-1
$ cat /proc/cmdline
resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 systemd.show_status=false rd.udev.log_level=0 vt.global_cursor_default=0 cryptdevice=PARTUUID=cf3d875f-72a4-4468-9795-015c9e953618:root:allow-discards,no-read-workqueue,no-write-workqueue root=/dev/mapper/root zswap.enabled=1 zswap.max_pool_percent=25 rootflags=subvol=@ rw rootfstype=btrfs
$ cat /sys/power/resume
253:0
$ cat /sys/power/resume_offset
3795013
$ cat /sys/power/disk
[platform] shutdown reboot suspend test_resume
$ cat /sys/power/state
freeze mem disk
$ zcat /proc/config.gz | grep -E 'PM_STD_PARTITION|HIBERNATION'
CONFIG_ARCH_HIBERNATION_POSSIBLE=y
CONFIG_ARCH_HIBERNATION_HEADER=y
CONFIG_HIBERNATION=y
CONFIG_HIBERNATION_SNAPSHOT_DEV=y
CONFIG_HIBERNATION_COMP_LZO=y
# CONFIG_HIBERNATION_COMP_LZ4 is not set
CONFIG_HIBERNATION_DEF_COMP="lzo"
CONFIG_PM_STD_PARTITION=""
```

`/sys/power/image_size` = 12835467264; `swap` = `/swap/swapfile`, 31722876 KiB size / 12603956 KiB used;
`btrfs inspect-internal map-swapfile -r /swap/swapfile` = 3795013; `lsattr /swap/swapfile` =
`---------------C------`; lockdown = `[none] integrity confidentiality`; hooks include `resume` after
`encrypt` (full capture receipt in `ScoutHost/capture/receipt.txt`).

## 2. Every host cmdline token classified by the BP1/BP2 rule

Rule applied (kernel `obsolete_checksetup` + `parameqn`, pinned v7.2): a token reaches the
`__setup` handler when its first `strlen(option)` characters equal the option string, `-` read as `_`;
the handler gets the rest of the token. Implemented literally (dash→underscore on both sides, prefix
compare, last-token-wins, empty value distinguished from absent) and applied to `/proc/cmdline` and to
every boot-entry cmdline source.

```
### /proc/cmdline  (15 tokens)
   MATCH 'resume=/dev/mapper/root' -> ['resume=']
   MATCH 'resume_offset=3795013'   -> ['resume_offset=']
   noresume      n=0 vals=[]
   nohibernate   n=0 vals=[]
   hibernate=    n=0 vals=[]
   resume=       n=1 vals=['/dev/mapper/root']
   resume_offset=n=1 vals=['3795013']
```

All other 13 tokens match no hibernation option (`quiet`, `splash`, `loglevel=0`,
`systemd.show_status=false`, `rd.udev.log_level=0`, `vt.global_cursor_default=0`, `cryptdevice=…`,
`root=/dev/mapper/root`, `zswap.enabled=1`, `zswap.max_pool_percent=25`, `rootflags=subvol=@`, `rw`,
`rootfstype=btrfs`). Same classification result for every cmdline line in `/boot/limine.conf` (5
entries) and for both UKIs' embedded `.cmdline` sections (17 tokens each, see §4).

Row-by-row host reading of the round-86 entry (`corpus/knowledge/hibernation-boot-parse-r86.md`):

| Row | host value (measured) | verdict |
|---|---|---|
| BP1 prefix match, value passed through | host has exactly one `resume=` and one `resume_offset=` token | consistent |
| BP2 `-`/`_` equivalence | no dashed token anywhere on the host (`resume-offset=` absent) | consistent (dormant) |
| BP3 dotted names (`x.noresume=1`) | no dotted hibernation token; dotted tokens present are `systemd.*`, `rd.*`, `vt.*`, `zswap.*` | consistent |
| BP4 value-blind `noresume`/`nohibernate` | no `noresume`/`nohibernate` token present → switch not set | consistent |
| BP5 `resume=` copied verbatim, last wins | one token, value `/dev/mapper/root`; `/sys/power/resume` = `253:0` = `stat -L -c '%t %T' /dev/mapper/root` (`fd 0`) → the copied device is the one the kernel picked up | consistent |
| BP6 empty `resume=` ⇒ no resume; default is `CONFIG_PM_STD_PARTITION` | `CONFIG_PM_STD_PARTITION=""` → default empty; the host has a valued `resume=` so the default is irrelevant | consistent |
| BP7 `resume_offset=` digits only | `resume_offset=3795013` → 3795013; `/sys/power/resume_offset` = 3795013; `btrfs map-swapfile -r` = 3795013 → all three agree | consistent |
| BP8 order effect via `noresume` | no `noresume` token → order effect dormant on this host | consistent |

## 3. Boot-entry source: can it introduce a valued or empty form?

Chain on this host: UEFI → **limine** (`/boot/EFI/BOOT/BOOTX64.EFI` is byte-identical to
`/boot/EFI/limine/limine_x64.efi`, sha256 `8a7214bfd8b9a044b780f1e71b2752dc12ecc25c06b9cf39ac6a0a341c802282`
— no systemd-boot, no `/boot/loader/entries`) → `/boot/limine.conf` → UKI
`boot():/EFI/Linux/omarchy_linux.efi`.

Cmdline sources, all read-only:

| source | content | valued/empty form possible? |
|---|---|---|
| `/etc/default/limine` | `KERNEL_CMDLINE[default]+="cryptdevice=… rootfstype=btrfs"`, `+=" quiet splash loglevel=0 …"`, `+=" resume=/dev/mapper/root resume_offset=3795013"` | **valued only**, literal text, no variable expansion, no shell/template → cannot produce an empty `resume=` today |
| `/etc/limine-entry-tool.d/resume.conf` | `KERNEL_CMDLINE[default]+=" resume=/dev/mapper/root resume_offset=3795013"` | valued only, literal |
| `/boot/limine.conf` (generated) | 5 `cmdline:` lines; entries 1–2 = the live cmdline verbatim; entries 3–4 are snapper-snapshot variants (`rootflags=subvol=/@/.snapshots/…`); entry 5 = the 2026-10-20 pre-nvme snapshot | valued only; `resume=`/`resume_offset=` valued in all 5 |
| UKI embedded `.cmdline` (`omarchy_linux.efi`, `omarchy_linux-lts.efi`) | 17 tokens: the live cmdline **plus a trailing duplicate** `resume=/dev/mapper/root resume_offset=3795013` (the `+=` append is applied twice: `/etc/default/limine` *and* the drop-in `resume.conf`) | valued only; duplicate is same value → last-wins is a no-op |
| `/etc/kernel/cmdline`, `/etc/kernel/cmdline.d`, `/usr/lib/kernel/cmdline` | absent | n/a |
| `mkinitcpio` | only `HOOKS+=(resume)` in `/etc/mkinitcpio.conf.d/omarchy_resume.conf`; no cmdline injection | n/a |

No `noresume`, `nohibernate` or `hibernate=` token exists in any of these sources
(`grep -c "noresume\|nohibernate\|hibernate="` → `0` for `/boot/limine.conf`, `/etc/default/limine`,
`/etc/limine-entry-tool.d/resume.conf`), and no source uses shell or template expansion, so today no
valued or empty `noresume=`/`nohibernate=`/`resume=` form can be introduced from the boot entry.
The only way an empty `resume=` could appear is a future edit that writes a bare `resume=` (or an
unexpanded template variable) into one of those `KERNEL_CMDLINE[default]+=` strings — the entry's
operator note about a trailing bare `resume=` is therefore a *latent* hazard on this host, not a
present one.

**Effective cmdline.** `/proc/cmdline` is byte-identical to the `cmdline:` line of limine.conf entries 1
and 2 (15 tokens, `proc == limine entry cmdline: True`), and *not* to the UKIs' embedded `.cmdline`
(17 tokens with the duplicate `resume=`). So on this host the loader-provided cmdline (limine.conf)
wins over the UKI's embedded `.cmdline`, and the effective command line contains exactly one
`resume=/dev/mapper/root` and one `resume_offset=3795013`. The duplicated pair inside the UKI `.cmdline`
is therefore inert here.

## 4. Boot-chain cmdline classification (all sources)

```
### /boot/limine.conf:31,39,51,57,65      → each: MATCH 'resume=/dev/mapper/root' (resume=),
                                             MATCH 'resume_offset=3795013' (resume_offset=);
                                             noresume/nohibernate/hibernate= → 0 matches
### UKI omarchy_linux.efi      .cmdline    → resume= n=2 ['/dev/mapper/root','/dev/mapper/root']
                                             resume_offset= n=2 ['3795013','3795013']
                                             noresume/nohibernate/hibernate= → 0
### UKI omarchy_linux-lts.efi  .cmdline    → identical to the above
```

## 5. Host values vs the frozen host receipt (round-86 `before/host/receipt.txt`)

| value | frozen receipt (2026-11-06T17:55:05-03:00) | live now | same? |
|---|---|---|---|
| `uname -r` | `7.2.11-arch1-1` | `7.2.11-arch1-1` | yes |
| `/proc/cmdline` | 15 tokens | identical string | **yes** (byte-identical) |
| `/sys/power/resume` | `253:0` | `253:0` | yes |
| `/sys/power/resume_offset` | `3795013` | `3795013` | yes |
| `/sys/power/disk` | `[platform] shutdown reboot suspend test_resume` | same | yes |
| `/sys/power/state` | **absent from receipt** | `freeze mem disk` | n/a (gap in the receipt, §6) |
| `CONFIG_HIBERNATION` / `CONFIG_PM_STD_PARTITION` | `=y` / `=""` | `=y` / `=""` | yes |
| gate `--live` | `{"findings": [], "verdict": "HEALTHY"}` rc=0 | `{"findings": [], "verdict": "HEALTHY"}` rc=0 | yes |

The frozen receipt therefore still describes this host; the only missing block is `/sys/power/state`
(the gate reads `sys_power_state` for its `HR-NO-DISK-STATE` rule; live value `freeze mem disk`
contains `disk`, so the rule would not fire).

## 6. Tool runs (this seat)

```
$ python3 tools/check-hibernate-resume.py --live      (cwd lane root, TMPDIR=$S)
{"findings": [], "verdict": "HEALTHY"}
rc=0
$ python3 tools/check-hibernate-resume.py --selftest
… 13 cases, "failed": [], "selftest": "PASS"   (noresume-valued → HR-NORESUME-ARG,
   nohibernate-valued → HR-HIBERNATE-DISABLED, empty-resume-last → HR-NO-RESUME-ARG,
   offset-nondigit-skipped, offset-dash-digit-prefix, offset-last-wins → 2 findings,
   decoys, hibernate-nox, boundary-equal, lockdown-integrity, bool-for-int, schema-v1)
rc=0
$ python3 tools/resume-gate-battery-r86.py --selftest
{"failed": [], "selftest": "PASS"}  (4/4)   rc=0
```

(I did **not** run the C1 counting command — that is the executor's seat; and I did not run the
battery against the 30 families: unrun here, not a pass.)

### 6.1 Tooling installed for this seat (per `/home/vgpnk/.omp/agent/RULES.md`)

| tool | version | channel | reason |
|---|---|---|---|
| `blake3` (python binding) | 1.0.11 | `pip install` into a throwaway venv under my scratch (`$S/.venv`), official PyPI | identify which digest limine's `#<hash>` suffix is, so the incident report could state the exact mismatch and the operator's repair values |

No system package was installed, nothing in `~/.local/bin` or any `PATH` directory was created or
modified, and no pacman transaction was attempted (pacman is paused host-wide). The venv lived only in
`/fast/scratch/hyaku/tsukuroi-r86/ScoutHost/` and was removed with the scratch root.

## 7. Freshness: pinned v7.2 sources vs the kernel actually running (7.2.11-arch1-1)

The round-86 pin is upstream tag **v7.2**; the host runs **7.2.11-arch1-1**. I diffed the parse-relevant
functions of the pinned snapshots against upstream stable **v7.2.11** (fetched read-only from
`git.kernel.org/…/stable/linux.git/plain/<file>?h=v7.2.11`, `ScoutHost/src/`):

| pinned v7.2 | stable v7.2.11 | result |
|---|---|---|
| `init/main.c` `obsolete_checksetup` (raw 201-228) | same function | **IDENTICAL** |
| `kernel/params.c` `dash2underscore`+`parameqn` (raw 79-95) | same | **IDENTICAL** |
| `kernel/power/hibernate.c` `resume_setup`…`nohibernate_setup` (raw 1402-1465) | same | **IDENTICAL** |
| `kernel/power/hibernate.c` `find_resume_device` head (raw 982-985) | same | **IDENTICAL** |
| `kernel/power/hibernate.c` `resume_file[256] = CONFIG_PM_STD_PARTITION` (raw 46) | same | **IDENTICAL** |
| `kernel/power/hibernate.c` `__setup("…")` list (raw 1518-1524) | same 7 registrations, only line numbers +2 | **IDENTICAL** |
| `lib/vsprintf.c` (whole file) | — | **0 diff lines** |

Unrelated drift between the two tags (does not touch the parse): `init/main.c` bootconfig bounds
checks, `kernel/params.c` `param_set_charp` reordering, `kernel/power/hibernate.c`
`hibernate_preallocate_memory` ordering. **The round-86 pinned parse is valid for the running
kernel** — the entry's "Snapshots are tag v7.2; the host runs 7.2.11" caveat is closed in the
direction that matters.

Also checked on the host: the `__setup` strings are `noresume`, `resume_offset=`, `resume=`,
`hibernate=`, `resumewait`, `resumedelay=`, `nohibernate` (7.2.11, same set/order as the pin), and
`next_arg()` (the `=` splitter) lives in `lib/cmdline.c` in v7.2 — a file **not** in the round-86 pin.
It only decides where `param` ends and `val` begins, and `repair_env_string()` (in the pinned
`init/main.c`, raw 463-474) rejoins `param=val` before the `__setup` search, so the pin is sufficient
for the claims; adding `lib/cmdline.c` would close the loop (§8).

## 8. Findings for the L1 (defects / limits, with file:line)

1. **[host incident — my own]** §0. `/boot/EFI/Linux/omarchy_linux.efi` and
   `/boot/EFI/Linux/omarchy_linux-lts.efi` were rewritten in place by `objcopy --dump-section`
   (5 bytes each: PE `TimeDateStamp` low 3 bytes at file offset 136, checksum field bytes at 216-217).
   Repair options, none of which I may execute (writing `/boot` is outside my seat bounds):
   * **(a) byte-exact restore** — needs the original `TimeDateStamp` (build time of the UKI) and the
     original checksum field; the original bytes are **not** recoverable from any copy on the host
     (the `limine_history` copies are different builds: same `.linux` section, different `.initrd`).
   * **(b) regenerate the config** — re-run `limine-entry-tool` under operator control so that
     `/boot/limine.conf` records the BLAKE2b-512 of the *current* files; this is the smallest change
     that restores unattended boot (the UKI payloads are unchanged and still correct).
   * **(c) rebuild the UKIs** via `kernel-install` so that file and config agree again.
   * **(d) do nothing** — the UKIs still contain the right kernel/initramfs/cmdline; only limine's
     integrity check fails, and with `hash_mismatch_panic: no` that is a warning + `Y` prompt at boot.
   * Recommendation: **(b)**, plus (d)-safe because payload bytes are unchanged; (b) is a single
     command the operator already owns. Until then, do **not** rely on an unattended reboot of this
     host. Any of (b)/(c) touches `/boot`, so the L1 must own it.
   * Also worth a rule addition: `objcopy --dump-section` (and `objcopy` in general) is **not** a
     read-only probe; use `objdump -s -j .cmdline <file>` (which I also used, and which does not
     modify the input) or `dd` on a scratch copy.
2. **Receipt coverage gap** — `.ufo/waves/round-86/before/host/receipt.txt` has no `### /sys/power/state`
   block although the gate reads `sys_power_state` (rule `HR-NO-DISK-STATE`) and the capture
   (`tools/capture-resume-facts-r84.py`) reads it. Live value is `freeze mem disk` (contains `disk`),
   so the rule would not fire on this host; a future receipt should include the block so a `DEGRADED`
   from that rule can be distinguished from an unmeasured one.
3. **Pin completeness (C2)** — `corpus/knowledge/hibernation-boot-parse-r86.md` quotes `init/main.c`
   raw 503-532 for the "rejoined before the `__setup` search" claim. That is correct
   (`repair_env_string()` raw 463-474 then `obsolete_checksetup(param)` raw 527), but the *splitting*
   of `param=val` happens in `lib/cmdline.c` (`next_arg()`), which is **not** in the pinned set
   (`.ufo/waves/round-86/before/src/` has 5 files: `init/main.c`, `kernel/params.c`,
   `kernel/power/hibernate.c`, `kernel/power/main.c`, `lib/vsprintf.c`). Proposed: add
   `lib/cmdline.c` to the pin (one more URL in `URLS.txt` + one line in `SHA256SUMS`) and cite
   `next_arg()` for the split in BP1/BP3. No claim in the entry is falsified by this; it closes the
   "where does `param` end" loop.
4. **Latent, not present: valued/empty `noresume=`** — the boot-entry sources are literal strings
   with no expansion, so no valued or empty `noresume=`/`nohibernate=`/`resume=` can appear today
   (§3). If `KERNEL_CMDLINE[default]+=` in `/etc/default/limine` or
   `/etc/limine-entry-tool.d/resume.conf` is ever edited to a template or a bare `resume=`, the
   kernel-side behaviour is as BP4/BP6 describe and the gate's `HR-NORESUME-ARG` /
   `HR-NO-RESUME-ARG` findings are the right signal. Worth one line in the entry's Operator actions:
   *the append is literal, so the operator's edit is the only source of a valued/empty form*.
5. **Duplicate `resume=` inside the UKI `.cmdline`** — both UKIs embed the `resume=`/`resume_offset=`
   pair twice (once from `/etc/default/limine`, once from the drop-in `resume.conf`, both `+=`).
   Harmless today (identical values, last-wins, and the loader cmdline wins anyway), but it means the
   UKI's embedded cmdline is *not* a faithful copy of the effective cmdline. Not a kernel-parse
   defect; noted so the entry's "the UKI .cmdline is the boot source" assumption is not made.

## 9. Unrun / not claimed

* C1 counting command (`python3 tools/resume-gate-battery-r86.py --gate tools/check-hibernate-resume.py`,
  three runs) — **not run by this seat** (executor seat).
* Byte-exact restoration of the two UKIs — **not attempted** (writes `/boot`, outside seat bounds);
  the analysis above is the input for the L1's decision.
* `lib/cmdline.c` content of the **host** kernel — not available on the host (Arch ships
  `linux-headers` only, no `.c` sources under `/usr/src/linux`); the v7.2.11 upstream copy was fetched
  for the diff instead.
