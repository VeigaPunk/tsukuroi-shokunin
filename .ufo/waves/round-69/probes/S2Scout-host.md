captured_utc=2026-11-03T23:19:48Z
seat=S2Scout round=69 wave=w1 host=canonical-linux-arch base=acce353bacad74043636018d829e9e9b8e0fdf1c
mode=read-only (no sudo, no pacman transaction, no service action, no git mutation)
scratch=/fast/scratch/hyaku/tsukuroi-r69/S2Scout (deleted at exit; nothing below depends on it)

Every block below is `$ command`, then the command's combined stdout+stderr verbatim, then its
exit status. `(no output)` marks an empty capture; it is not an omission.

## A. Named probes

$ cat /proc/sys/kernel/osrelease
7.2.11-arch1-1
[rc=0]

$ uname -r
7.2.11-arch1-1
[rc=0]

$ cat /proc/sys/kernel/tainted
12288
[rc=0]

$ pacman -Q linux
linux 7.2.11.arch1-1
[rc=0]

$ pacman -Q linux-lts
linux-lts 6.18.57-2
[rc=0]

$ pacman -Qo /usr/lib/modules/7.2.11-arch1-1
/usr/lib/modules/7.2.11-arch1-1/ is owned by linux 7.2.11.arch1-1
/usr/lib/modules/7.2.11-arch1-1/ is owned by linux-headers 7.2.11.arch1-1
[rc=0]

$ pacman -Qo /usr/lib/modules/6.18.57-2-lts
/usr/lib/modules/6.18.57-2-lts/ is owned by linux-lts 6.18.57-2
/usr/lib/modules/6.18.57-2-lts/ is owned by linux-lts-headers 6.18.57-2
[rc=0]

$ ls -1 /usr/lib/modules/
6.18.57-2-lts
7.2.11-arch1-1
[rc=0]

$ modinfo -F vermagic /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst
7.2.11-arch1-1 SMP preempt mod_unload 
[rc=0]
(trailing space after `mod_unload` is present in the output)

$ modinfo -F name,license /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst
(no output)
[rc=0]

$ journalctl -b -k --no-pager | grep -m3 'Tainted: \['
Nov 02 16:49:24 plazir27 kernel: Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE
Nov 02 16:49:45 plazir27 kernel: Tainted: [O]=OOT_MODULE, [E]=UNSIGNED_MODULE
[rc=0]

$ journalctl -b -k --no-pager | grep -m2 'nvidia: '
Nov 02 12:07:17 plazir27 kernel: nvidia: loading out-of-tree module taints kernel.
Nov 02 12:07:17 plazir27 kernel: nvidia: module verification failed: signature and/or required key missing - tainting kernel
[rc=0]

$ journalctl -b -k --no-pager | grep -ciE 'soft lockup'
0
[rc=1]
(rc=1 is grep's "no line selected": zero soft-lockup lines this boot. The printed `0` is grep -c's
own count line, not a match.)

## B. Supplementary probes (field semantics / path resolution; same read-only posture)

Named probe `modinfo -F name,license` printed nothing at rc 0, which is ambiguous between "no such
field" and "unsupported field list". These disambiguate it:

$ modinfo --version
kmod version 34.2
+ZSTD +XZ +ZLIB +OPENSSL
[rc=0]

$ modinfo -F name /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst
nvidia
[rc=0]

$ modinfo -F license /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst
Dual MIT/GPL
[rc=0]

$ modinfo /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst | grep -E "^(name|license):"
license:        Dual MIT/GPL
name:           nvidia
[rc=0]

$ modinfo -F name,license /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst; echo "arg_rc=$?"
arg_rc=0
[rc=0]

$ ls -l /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst
-rw-r--r-- 1 root root 12279379 Oct 20 09:17 /lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst
[rc=0]

$ stat -c "%a %U:%G %s %n" /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst
644 root:root 12279379 /lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst
[rc=0]

$ file /lib/modules/$(uname -r)/updates/dkms/nvidia.ko.zst
/lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst: Zstandard compressed data (v0.8+), Dictionary ID: None
[rc=0]

$ test -d /usr/lib/modules/$(uname -r); echo "tree_present_rc=$?"
tree_present_rc=0
[rc=0]

$ pacman -Qo /lib/modules/7.2.11-arch1-1
/usr/lib/modules/7.2.11-arch1-1/ is owned by linux 7.2.11.arch1-1
/usr/lib/modules/7.2.11-arch1-1/ is owned by linux-headers 7.2.11.arch1-1
[rc=0]

$ pacman -Qo /lib/modules/6.18.57-2-lts
/usr/lib/modules/6.18.57-2-lts/ is owned by linux-lts 6.18.57-2
/usr/lib/modules/6.18.57-2-lts/ is owned by linux-lts-headers 6.18.57-2
[rc=0]

$ ls -ld /usr/lib/modules/7.2.11-arch1-1 /usr/lib/modules/6.18.57-2-lts
drwxr-xr-x 1 root root 532 Oct 20 09:18 /usr/lib/modules/6.18.57-2-lts
drwxr-xr-x 1 root root 532 Oct 20 09:18 /usr/lib/modules/7.2.11-arch1-1
[rc=0]

## C. Derivation machinery

$ pacman -Q linux | awk "{print \$2}" | sed -E "s/\.(arch[0-9]+)-/-\1-/"
7.2.11-arch1-1
[rc=0]

$ running=$(uname -r); owner=$(pacman -Q linux | awk "{print \$2}" | sed -E "s/\.(arch[0-9]+)-/-\1-/"); printf "running=%s\nowner_mapped=%s\nequal=%s\n" "$running" "$owner" "$([ "$running" = "$owner" ] && echo YES || echo NO)"
running=7.2.11-arch1-1
owner_mapped=7.2.11-arch1-1
equal=YES
[rc=0]

$ n=$(cat /proc/sys/kernel/tainted); echo "tainted=$n"; printf "hex=%d(0x%x)\n" "$n" "$n"; for i in $(seq 0 31); do if (( (n>>i)&1 )); then echo "bit $i set"; fi; done
tainted=12288
hex=12288(0x3000)
bit 12 set
bit 13 set
[rc=0]

$ echo $((4096+8192))
12288
[rc=0]

## D. Missing-path behaviour of the ownership probe (C2 hazard)

$ pacman -Qo /usr/lib/modules/does-not-exist
error: No package owns /usr/lib/modules/does-not-exist
[rc=1]

`pacman -Qo` on a nonexistent path: rc=1, one stderr line beginning `error: No package owns`.
The path is named back verbatim; no package name appears. A parser that takes "the last word" or
"the token after `error:`" produces the literal string `does-not-exist` or `owns` — a false `pkg=`.

## E. Derived statements

E1. Reboot-pending predicate. Running release `7.2.11-arch1-1` (from `cat /proc/sys/kernel/osrelease`
and `uname -r`). Owning kernel package `linux 7.2.11.arch1-1` (from `pacman -Q linux` and
`pacman -Qo /usr/lib/modules/7.2.11-arch1-1`). Exact transformation: the package version has the form
`<kernelver>.<archtag>-<pkgrel>`, i.e. `7.2.11` `.` `arch1` `-` `1`; replacing the dot that precedes
the arch component with a dash yields `7.2.11-arch1-1` — sed expression `s/\.(arch[0-9]+)-/-\1-/`.
Comparison `[ "$running" = "$owner_mapped" ]` → YES. Therefore pending=NO. The same mapping applied
to `linux-lts 6.18.57-2` (`6.18.57-2` carries no `.archN-` component, so the expression is a no-op)
gives `6.18.57-2`, which is not the running release; the running tree is the `linux` one.

E2. Module tree ownership. Two trees under `/usr/lib/modules/`:
- `7.2.11-arch1-1` → owned by `linux 7.2.11.arch1-1` (also `linux-headers 7.2.11.arch1-1`) — this is
  the RUNNING tree (`test -d /usr/lib/modules/$(uname -r)` rc 0).
- `6.18.57-2-lts` → owned by `linux-lts 6.18.57-2` (also `linux-lts-headers 6.18.57-2`).
The non-running tree is not residue: `pacman -Q linux-lts` reports the package installed at
`6.18.57-2`, and `pacman -Qo` maps the directory to it. It is a separately installed kernel package
whose headers companion is present too. A census that reports `pkg=` from `pacman -Qo <tree>` must
select the kernel package and not the `*-headers` owner (two owners per tree on this host).

E3. Taint mask. `/proc/sys/kernel/tainted` = `12288` decimal = `0x3000`. Set bit numbers: 12 and 13
(`4096 + 8192 = 12288`). No other bits are set in the 0..31 range. Bit letters are deliberately not
assigned here; the letter mapping belongs to S288's closed table as read by S1Scout. Cross-check
available on the host without the table: the boot kernel log prints exactly two bracket entries,
`[O]=OOT_MODULE` and `[E]=UNSIGNED_MODULE` (section A), i.e. two taints set, consistent with two bits.
Note the log also names the cause on the nvidia lines (`out-of-tree module`, `module verification
failed`), which is why bits 12 and 13 are the plausible reading — [INFERENCE] beyond the count match.

E4. Field-semantics hazards for the C2 line, stated from the blocks above:
- `modinfo -F <a>,<b>` is not a field list: with kmod 34.2 it exits 0 and prints nothing, while each
  field alone prints a value. So `(no output, rc 0)` from that form proves nothing about the module
  and MUST NOT be recorded as an empty/absent value; a census needing two fields must call twice or
  parse `modinfo` full output.
- The dkms module is world-readable (`644 root:root`, 12,279,379 bytes), so the read needs no
  privilege; `file` confirms it is zstd-compressed and `modinfo` reads it directly.
- `/lib/modules/...` and `/usr/lib/modules/...` resolve to the same trees for `pacman -Qo` on this
  host (identical owner output for both spellings); either spelling works for the ownership probe.

## F. Seat results

S2_RELEASE=7.2.11-arch1-1 S2_PKG_OWNER="linux 7.2.11.arch1-1" S2_PENDING=NO S2_TAINT_BITS=12,13 S2_TREES=2 S2_QO_MISSING_RC=1
