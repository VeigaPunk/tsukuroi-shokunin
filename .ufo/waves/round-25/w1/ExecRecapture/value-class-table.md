| Value | Class | Frozen | Re-capture |
|---|---|---|---|
| `header|date -u +%Y-%m-%dT%H:%M:%SZ` | changed (counter or gauge moves) | 2026-10-22T10:06:23Z | 2026-10-22T10:21:15Z |
| kernel release (`uname -r`) | same | 7.2.11-arch1-1 | 7.2.11-arch1-1 |
| systemd version (`systemctl --version`) | same | systemd 262 (262-1-arch)<br>+PAM +AUDIT -SELINUX +APPARMOR -IMA +IPE +SMACK +SECCOMP +GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 +KMOD +LIBCRYPTSETUP +LIBCRYPTSETUP_PLUGINS +LIBFDISK +PCRE2 +PWQUALITY +P... | systemd 262 (262-1-arch)<br>+PAM +AUDIT -SELINUX +APPARMOR -IMA +IPE +SMACK +SECCOMP +GNUTLS +OPENSSL +ACL +BLKID +CURL +ELFUTILS +FIDO2 +IDN2 +KMOD +LIBCRYPTSETUP +LIBCRYPTSETUP_PLUGINS +LIBFDISK +PCRE2 +PWQUALITY +P... |
| system memory PSI, read 1 (`/proc/pressure/memory`) | changed (counter or gauge moves) | some avg10=0.02 avg60=0.02 avg300=0.06 total=41385384<br>full avg10=0.02 avg60=0.02 avg300=0.06 total=40856373 | some avg10=0.04 avg60=0.02 avg300=0.07 total=44447250<br>full avg10=0.04 avg60=0.02 avg300=0.07 total=43886898 |
| `system-memory-psi-read-1|sleep` | same | _(not captured)_ | _(not captured)_ |
| system memory PSI, read 2 (`/proc/pressure/memory`, 10 s later) | changed (counter or gauge moves) | some avg10=0.00 avg60=0.02 avg300=0.06 total=41389485<br>full avg10=0.00 avg60=0.02 avg300=0.06 total=40860452 | some avg10=0.01 avg60=0.02 avg300=0.07 total=44462024<br>full avg10=0.01 avg60=0.02 avg300=0.06 total=43901244 |
| wall clock at second PSI read | changed (counter or gauge moves) | 2026-10-22T10:06:33Z | 2026-10-22T10:21:25Z |
| root cgroup `memory.pressure` | changed (counter or gauge moves) | some avg10=0.00 avg60=0.02 avg300=0.06 total=41389485<br>full avg10=0.00 avg60=0.02 avg300=0.06 total=40860452 | some avg10=0.01 avg60=0.02 avg300=0.07 total=44462024<br>full avg10=0.01 avg60=0.02 avg300=0.06 total=43901244 |
| `user.slice` `memory.pressure` | changed (counter or gauge moves) | some avg10=0.00 avg60=0.00 avg300=0.00 total=3150158<br>full avg10=0.00 avg60=0.00 avg300=0.00 total=3125148 | some avg10=0.00 avg60=0.00 avg300=0.00 total=3251943<br>full avg10=0.00 avg60=0.00 avg300=0.00 total=3226500 |
| `user-1000.slice` `memory.pressure` | changed (counter or gauge moves) | some avg10=0.00 avg60=0.00 avg300=0.00 total=3158801<br>full avg10=0.00 avg60=0.00 avg300=0.00 total=3133751 | some avg10=0.00 avg60=0.00 avg300=0.00 total=3258387<br>full avg10=0.00 avg60=0.00 avg300=0.00 total=3232854 |
| `user@1000.service` `memory.pressure` | changed (counter or gauge moves) | some avg10=0.00 avg60=0.00 avg300=0.00 total=3161820<br>full avg10=0.00 avg60=0.00 avg300=0.00 total=3136771 | some avg10=0.00 avg60=0.00 avg300=0.00 total=3261639<br>full avg10=0.00 avg60=0.00 avg300=0.00 total=3236112 |
| `user-1000.slice` `memory.events` | changed (counter or gauge moves) | low 0<br>high 0<br>max 0<br>oom 0<br>oom_kill 0<br>oom_group_kill 0<br>sock_throttled 13763 | low 0<br>high 0<br>max 0<br>oom 0<br>oom_kill 0<br>oom_group_kill 0<br>sock_throttled 16092 |
| `user-1000.slice` `memory.swap.events` | changed (counter or gauge moves) | high 0<br>max 0<br>fail 510 | high 0<br>max 0<br>fail 602 |
| kernel `oom_kill` counter (`/proc/vmstat`) | same | oom_kill 0 | oom_kill 0 |
| `/proc/meminfo` memory and swap gauges | changed (counter or gauge moves) | MemTotal:       31721800 kB<br>MemAvailable:   23863792 kB<br>SwapTotal:      31722876 kB<br>SwapFree:       30005224 kB | MemTotal:       31721800 kB<br>MemAvailable:   23698520 kB<br>SwapTotal:      31722876 kB<br>SwapFree:       28993240 kB |
| `systemctl is-active systemd-oomd.service` | same | inactive | inactive |
| `systemctl is-enabled systemd-oomd.service` | same | disabled | disabled |
| `systemctl is-enabled systemd-oomd.socket` | same | disabled | disabled |
| `systemctl is-active systemd-oomd.socket` | new in the re-capture | _(not captured)_ | inactive |
| `oomd-config|cat-config|lines)` | same | 1 | 1 |
| `systemd-analyze cat-config systemd/oomd.conf` body | same | # /etc/systemd/oomd.conf<br>#  This file is part of systemd.<br>#<br>#  systemd is free software; you can redistribute it and/or modify it under the<br>#  terms of the GNU Lesser General Public License as published by... | # /etc/systemd/oomd.conf<br>#  This file is part of systemd.<br>#<br>#  systemd is free software; you can redistribute it and/or modify it under the<br>#  terms of the GNU Lesser General Public License as published by... |
| `oomd-config|ls|/etc/systemd/system/oomd.conf.d` | new in the re-capture | _(not captured)_ | ls: cannot access '/etc/systemd/system/oomd.conf.d': No such file or directory |
| `systemctl show` ManagedOOM*/MemoryPressure* on `user@1000.service` | same | ManagedOOMSwap=auto<br>ManagedOOMMemoryPressure=auto<br>ManagedOOMMemoryPressureLimit=0<br>ManagedOOMMemoryPressureDurationUSec=[not set]<br>ManagedOOMPreference=none<br>MemoryPressureWatch=skip<br>MemoryPressureThres... | ManagedOOMSwap=auto<br>ManagedOOMMemoryPressure=auto<br>ManagedOOMMemoryPressureLimit=0<br>ManagedOOMMemoryPressureDurationUSec=[not set]<br>ManagedOOMPreference=none<br>MemoryPressureWatch=skip<br>MemoryPressureThres... |
| `systemctl show` ManagedOOM*/MemoryPressure* on `user-1000.slice` | same | ManagedOOMSwap=auto<br>ManagedOOMMemoryPressure=auto<br>ManagedOOMMemoryPressureLimit=0<br>ManagedOOMMemoryPressureDurationUSec=[not set]<br>ManagedOOMPreference=none<br>MemoryPressureWatch=auto<br>MemoryPressureThres... | ManagedOOMSwap=auto<br>ManagedOOMMemoryPressure=auto<br>ManagedOOMMemoryPressureLimit=0<br>ManagedOOMMemoryPressureDurationUSec=[not set]<br>ManagedOOMPreference=none<br>MemoryPressureWatch=auto<br>MemoryPressureThres... |
| `systemctl show` ManagedOOM*/MemoryPressure* on `user.slice` | same | ManagedOOMSwap=auto<br>ManagedOOMMemoryPressure=auto<br>ManagedOOMMemoryPressureLimit=0<br>ManagedOOMMemoryPressureDurationUSec=[not set]<br>ManagedOOMPreference=none<br>MemoryPressureWatch=auto<br>MemoryPressureThres... | ManagedOOMSwap=auto<br>ManagedOOMMemoryPressure=auto<br>ManagedOOMMemoryPressureLimit=0<br>ManagedOOMMemoryPressureDurationUSec=[not set]<br>ManagedOOMPreference=none<br>MemoryPressureWatch=auto<br>MemoryPressureThres... |
| `systemctl show` ManagedOOM*/MemoryPressure* on `-.slice` | same | ManagedOOMSwap=auto<br>ManagedOOMMemoryPressure=auto<br>ManagedOOMMemoryPressureLimit=0<br>ManagedOOMMemoryPressureDurationUSec=[not set]<br>ManagedOOMPreference=none<br>MemoryPressureWatch=auto<br>MemoryPressureThres... | ManagedOOMSwap=auto<br>ManagedOOMMemoryPressure=auto<br>ManagedOOMMemoryPressureLimit=0<br>ManagedOOMMemoryPressureDurationUSec=[not set]<br>ManagedOOMPreference=none<br>MemoryPressureWatch=auto<br>MemoryPressureThres... |
| manager defaults `DefaultMemoryPressureWatch`/`DefaultMemoryPressureThresholdUSec` | same | DefaultMemoryPressureThresholdUSec=200ms<br>DefaultMemoryPressureWatch=auto | DefaultMemoryPressureThresholdUSec=200ms<br>DefaultMemoryPressureWatch=auto |
| `end|date -u +%Y-%m-%dT%H:%M:%SZ` | changed (counter or gauge moves) | 2026-10-22T10:06:33Z | 2026-10-22T10:21:25Z |
| `managed-oom-dropin-dirs|ls|/usr/lib/systemd/system/user@.service.d` | new in the re-capture | _(not captured)_ | 10-login-barrier.conf |
| `managed-oom-dropin-dirs|ls|/etc/systemd/system/user@.service.d` | new in the re-capture | _(not captured)_ | faster-shutdown.conf |
| `managed-oom-dropin-dirs|ls|/usr/lib/systemd/system/user-.slice.d` | new in the re-capture | _(not captured)_ | 10-defaults.conf |
| `managed-oom-dropin-dirs|ls|/etc/systemd/system/user-.slice.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-dirs|ls|/usr/lib/systemd/system/-.slice.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-dirs|ls|/etc/systemd/system/-.slice.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-dirs|ls|/usr/lib/systemd/system/user.slice.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-dirs|ls|/etc/systemd/system/user.slice.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-dirs|ls|/usr/lib/systemd/system/user@1000.service.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-dirs|ls|/etc/systemd/system/user@1000.service.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-dirs|ls|/usr/lib/systemd/system/user-1000.slice.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-dirs|ls|/etc/systemd/system/user-1000.slice.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-dirs|ls|/etc/systemd/system/systemd-oomd.service.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-dirs|ls|/etc/systemd/system/systemd-oomd.socket.d` | new in the re-capture | _(not captured)_ | (absent) |
| `managed-oom-dropin-contents|cat|user@1000.service` | new in the re-capture | _(not captured)_ | # /usr/lib/systemd/system/user@.service<br># /usr/lib/systemd/system/user@.service.d/10-login-barrier.conf<br># /etc/systemd/system/user@.service.d/faster-shutdown.conf |
| `managed-oom-dropin-contents|dropin-grep|user@1000.service` | new in the re-capture | _(not captured)_ | MemoryPressureWatch=skip |
| `managed-oom-dropin-contents|cat|user-1000.slice` | new in the re-capture | _(not captured)_ | # /usr/lib/systemd/system/user-.slice.d/10-defaults.conf |
| `managed-oom-dropin-contents|dropin-grep|user-1000.slice` | new in the re-capture | _(not captured)_ | _(not captured)_ |
| `managed-oom-dropin-contents|cat|user.slice` | new in the re-capture | _(not captured)_ | # /usr/lib/systemd/system/user.slice |
| `managed-oom-dropin-contents|dropin-grep|user.slice` | new in the re-capture | _(not captured)_ | _(not captured)_ |
| `managed-oom-dropin-contents|cat|-.slice` | new in the re-capture | _(not captured)_ | _(not captured)_ |
| `managed-oom-dropin-contents|dropin-grep|-.slice` | new in the re-capture | _(not captured)_ | (no resolvable unit or drop-in file) |
| `managed-oom-kill-search|kill-search` | new in the re-capture | _(not captured)_ | _(not captured)_ |
