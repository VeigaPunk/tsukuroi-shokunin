captured_utc=2026-11-03T23:19:48Z
seat=S2Scout | round=69 | wave=w1 | role=scout | axes=depth,C1,C2,host
receipt=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-69/probes/S2Scout-host.md
privacy=read-only; no sudo, no pacman transaction, no service action, no git mutation; no lane census/selftest run

## Results

S2_RELEASE=7.2.11-arch1-1
S2_PKG_OWNER=linux 7.2.11.arch1-1
S2_PENDING=NO
S2_TAINT_BITS=12,13
S2_TREES=2
S2_QO_MISSING_RC=1

## Observed facts (each carries its command in the receipt)

1. Running release agrees across both routes: `cat /proc/sys/kernel/osrelease` and `uname -r` both
   print `7.2.11-arch1-1` (rc 0 each).
2. Kernel package of the running tree: `pacman -Q linux` → `linux 7.2.11.arch1-1`;
   `pacman -Qo /usr/lib/modules/7.2.11-arch1-1` → owned by `linux 7.2.11.arch1-1` **and**
   `linux-headers 7.2.11.arch1-1` (two owners, rc 0).
3. Pending predicate: transform the package version by replacing the dot before the arch component
   with a dash — `s/\.(arch[0-9]+)-/-\1-/` maps `7.2.11.arch1-1` → `7.2.11-arch1-1`, which equals
   `uname -r` (comparison printed `equal=YES`). `linux-lts 6.18.57-2` needs no transform and does
   not match the running release. → pending=NO.
4. Two module trees under `/usr/lib/modules/`: `6.18.57-2-lts` and `7.2.11-arch1-1`. Ownership:
   `6.18.57-2-lts` → `linux-lts 6.18.57-2` + `linux-lts-headers 6.18.57-2`. The non-running tree is a
   separately installed kernel package, not stale residue: `pacman -Q linux-lts` reports it installed
   and `pacman -Qo` maps the directory to it.
5. Taint: `/proc/sys/kernel/tainted` = `12288` = `0x3000`; set bits are **12** and **13** only
   (`4096+8192`), verified by a shift loop over bits 0..31. Boot kernel log prints exactly two bracket
   entries (`[O]=OOT_MODULE`, `[E]=UNSIGNED_MODULE`) — count agrees with 2. Letters intentionally not
   assigned; they come from S288's closed table via S1Scout.
6. dkms nvidia module: `modinfo -F vermagic` → `7.2.11-arch1-1 SMP preempt mod_unload` (trailing
   space), which matches the running release, rc 0; the file is `644 root:root`, 12,279,379 bytes,
   zstd-compressed — readable without privilege.
7. Soft-lockup log lines this boot: `journalctl -b -k --no-pager | grep -ciE 'soft lockup'` printed
   `0` at rc 1 (grep no-match; the `0` is grep -c's count).

## C2 field-semantics hazards (for the executor of the `KERNEL` line)

- `pacman -Qo <missing path>` → rc 1, stderr `error: No package owns /usr/lib/modules/does-not-exist`.
  No package name appears; any parser that takes a trailing token yields a false `pkg=`. Rule: rc≠0 →
  `pkg=UNKNOWN`, never a value, and never echo the stderr text into a field.
- `pacman -Qo <tree>` returns **two** owners (kernel and `*-headers`) on this host; take the kernel
  package (`pacman -Q linux` is the unambiguous route) instead of "first line wins".
- `modinfo -F name,license` exits **0 with no output** on kmod 34.2, while `-F name` → `nvidia` and
  `-F license` → `Dual MIT/GPL`. An empty capture at rc 0 from the comma form is not evidence of an
  empty field; emit `UNKNOWN` rather than fabricating a value or a "none".
- `pending=` is computed only from the package owning the running tree (`linux`), not from any tree
  found by listing `/usr/lib/modules/` — the listing contains a second, non-running kernel.

## Confidence

High (direct command output, rc recorded): items 1-7 and every hazard above.
[INFERENCE] Only the causal link between the two logged bracket taints and bits 12/13 is inferred
from the count match plus the nvidia out-of-tree/unsigned messages; bit numbering itself is observed.

## Remaining unknowns

- The letter names for bits 12/13 (deliberately not assigned here; S288 table read is S1Scout's).
- Whether the kernel log's `Tainted:` entries correspond one-to-one to bits 12/13 individually (only
  the count of 2 was checkable on-host).
- Any non-systemd-boot or second-device behaviour: out of scope for this seat (kernel-arm coverage
  debt recorded in the round's planned section).
