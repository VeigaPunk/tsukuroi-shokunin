VERDICT: defect-found

# C2-15 — GR3 host stop-timeout claims

**Counterexample:** the host-wide `DefaultTimeoutStopSec=5s` is not unconditionally the stop timeout for every system unit. A unit-level `TimeoutStopSec=` overrides the manager default; an instantiated-unit drop-in can set it too. In addition, a configured `ExecStop=` runs as part of stopping, and its own `TimeoutStopSec=` semantics/budget mean a blanket statement that SIGKILL follows precisely five seconds after initial signal is too strong without checking the stop command path. Here the concrete `btrfs-scrub@-.service` has no `ExecStop`, no unit drop-in, and no unit-specific timeout, so the effective 5s timeout reported for this instance is supported.

## Read-only re-derivation

- `systemd-analyze cat-config systemd/system.conf` displayed `/etc/systemd/system.conf.d/10-faster-shutdown.conf` with `[Manager] DefaultTimeoutStopSec=5s`; the only other manager drop-in shown was `99-omarchy-nofile.conf`, setting only `DefaultLimitNOFILE`. Thus the claim that this manager default applies to system units *without their own value* is accurately qualified.
- `systemctl show 'btrfs-scrub@-.service' -p TimeoutStopUSec -p ExecStop -p FragmentPath -p DropInPaths -p KillSignal -p KillMode -p FinalKillSignal` returned `TimeoutStopUSec=5s`, `FragmentPath=/usr/lib/systemd/system/btrfs-scrub@.service`, empty `DropInPaths=`, `KillSignal=2`, `KillMode=control-group`, `FinalKillSignal=9`; `ExecStop` was not printed (unset). Note: querying the template name `btrfs-scrub@.service` failed as invalid invocation/unit name; the concrete `@-.service` instance query succeeded.
- `systemctl cat 'btrfs-scrub@-.service'` showed the shipped unit with only `Nice=19`, `IOSchedulingClass=idle`, `KillSignal=SIGINT`, and `ExecStart=/usr/bin/btrfs scrub start -B %f`; no `ExecStop=` or unit-level `TimeoutStopSec=`.
- Enumerating regular files under `/usr/lib/systemd/system` and `/run/systemd/system` matching `*/btrfs-scrub@.service.d/*` or `*/system.conf.d/*` returned no paths. Consequently the requested package ownership query on those directories had no files to query; this is not evidence about `/etc` ownership.
- The independent frozen capture at `.ufo/waves/round-45/frozen/hostcap/capture.txt:3-7` records the concrete unit's effective `TimeoutStopUSec=5s`, `FragmentPath`, and empty unit drop-ins; lines 4-6 record the manager default and the capture's `none` ownership findings. The current re-derivation confirms the timeout and config source. (The assignment additionally requested pacman local-db file-list checking; I did not enumerate those lists in this seat.)

## Scope and smallest safe correction

GR3's precise host statement — “On this host the unit's effective stop timeout is 5 s” — is correct for the inspected concrete instance at the observed time. The text already says the manager default applies to system units “without its own value,” which appropriately avoids claiming that every unit uses five seconds. “No package owns that drop-in” is consistent with frozen capture lines 5-6 but was not independently re-derived via local package file lists in this seat. Avoid broadening either claim to all instances or all system units.

The sentence “If processes remain once `TimeoutStopSec=` has passed, the request is repeated with SIGKILL” is systemd's documented sequencing, not a claim that every stop operation finishes exactly five seconds after the first signal. No `ExecStop` is configured for this inspected instance, so it does not alter this concrete example. Recommended narrow replacement for the host paragraph's unconditional-looking timing implication:

> On this host, `btrfs-scrub@-.service` has an effective `TimeoutStopUSec=5s` (`systemctl show`; capture.txt:3). Its unit has no `ExecStop=`, no unit drop-ins, and no unit-specific timeout, so that value comes from `/etc/systemd/system.conf.d/10-faster-shutdown.conf` setting the manager's `DefaultTimeoutStopSec=5s` for units without their own value (capture.txt:4,7; `systemd-analyze cat-config systemd/system.conf`). This is the configured timeout for this inspected instance, not a universal stop duration for other instances or units.

## Evidence / limits

Target text: `corpus/knowledge/btrfs-scrub-grounding-r45.md:94-104,124-127` at the assigned implementation revision. Read-only commands and outputs are recorded above. No unit was started/stopped; no host state was mutated. I did not independently verify package ownership against `/var/lib/pacman/local/*/files`, and did not inspect every possible per-instance drop-in for every other mount instance; the concrete systemd query reports this selected instance's empty `DropInPaths`. No tools installed or upgraded.