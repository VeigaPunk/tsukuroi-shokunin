# Kernel taint on this host — round 27 entry

source: S140, S141, S142, S143, S144, S145 (Linux v7.2, all `mined`, tier A; Gate in `corpus/lessons/round-27.md`)
capture: `.ufo/waves/round-27/capture/capture.txt` (sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, 2026-10-22T15:55:13Z, no sudo)
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
| KT6 | What taint means for bug reports | the `Tainted:` field of every oops on this host will show O and E; reports from tainted kernels are often ignored upstream | DEGRADED (reporting limit, not host damage) |

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
