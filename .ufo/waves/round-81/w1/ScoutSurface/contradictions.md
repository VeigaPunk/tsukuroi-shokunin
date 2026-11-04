# Contradictions — ScoutSurface, round 81

Subject: `corpus/knowledge/mount-unit-fstab-plane-r81.md` (sentences) and `corpus/knowledge/mount-unit-fstab-plane-r81.json` (rows MT1–MT8), checked against the live mount surface in `surface.txt` (sections §1–§13, read-only, captured 2026-11-04 ~18:40 -03).

Observation = command output. Inference = marked `[INFERENCE]`. Unknown = stated.

## Contradictions (live surface disagrees with a sentence or number of the entry)

### C1 — "The generated `Options=` line keeps `nofail` but drops the `x-systemd.*` tokens"
- Entry: `mount-unit-fstab-plane-r81.md`, section "What this host does with it", the paragraph beginning "The generated output matches the documentation row for row".
- Observed: `/run/systemd/generator/tmp.mount` line `Options=rw,noatime,nosuid,nodev,logbsize=256k,nofail,x-systemd.before=local-fs.target` (surface.txt:152). `systemctl show -p Options -- tmp.mount` returns the same string including `x-systemd.before=local-fs.target` (surface.txt §7).
- Source: `.ufo/waves/round-81/before/src/fstab-generator.c:645` calls `generator_write_device_timeout(dest, what, opts, &filtered)` and `:663` calls `write_options(f, filtered)`. Only the device-timeout token is removed on that path; `x-systemd.before` is not. `[INFERENCE]` that the helper strips only `x-systemd.device-timeout`; its body is not in the snapshot.
- Verdict: the sentence is false for `/tmp`. It is true for `/fast` (`Options=rw,noatime,nosuid,nodev,logbsize=256k,nofail`, surface §4).

### C2 — "carries six local file systems; four are required and two are not"
- Entry: same section, first bullet list.
- Observed `/etc/fstab` (surface §1): non-comment block-backed rows are `/`, `/home`, `/var/cache/pacman/pkg`, `/var/log`, `/boot` (five, required), `/tmp` and `/fast` (two, `nofail`). Plus `none swap` and `tmpfs /dev/shm`, which are not local block file systems.
- The entry's own next line lists five required mounts, so "four" and "six" both conflict with the entry itself and with the file. Count is seven local file systems: five required, two `nofail`.

### C3 — "`x-systemd.device-timeout=10s` … the boot cost of a missing second NVMe is therefore up to ten seconds for `/tmp`"
- Entry: section "What this host does with it", the penultimate bullet and the sentence beginning "The boot cost of a missing second NVMe".
- Observed (surface §9):
  - `dev-disk-by\x2duuid-1f8a5361…device` and `dev-disk-by\x2duuid-070be1ea…device` carry `JobRunningTimeoutUSec=10s` and the drop-ins under `/run/systemd/generator/…device.d/50-device-timeout.conf`. Each has `Following=` the kernel-name unit (`…nvme1n1p1.device` / `…nvme1n1p2.device`).
  - `dev-nvme1n1p1.device` and `dev-nvme1n1p2.device` report `JobRunningTimeoutUSec=1min 30s` and empty `DropInPaths=`.
  - `tmp.mount` `Requires=system.slice dev-nvme1n1p1.device -.mount` (surface §7). `fast.mount` `Requires=system.slice -.mount dev-nvme1n1p2.device`.
- So the unit the mount actually requires reports 1min 30s, not 10s. The 10s bound sits on an alias unit that the mount does not name in `Requires=` or `After=`. `[INFERENCE]` systemd does not apply the alias's job timeout to a start job queued through the followed unit. Unknown: no device-removal or boot-timing test was run, so the real boot delay is not measured.
- Verdict: the "up to ten seconds" consequence is not supported by the live surface and conflicts with the reported `Requires=` target's own timeout. The `Options=`/drop-in mechanism sentences stand as observed.

### C4 — Measured-leg citations point at the wrong unit blocks
- Entry prose: "`tmp.mount` is generated with `Before=local-fs.target`; `fast.mount` is not (S332 :35-47 vs :95-107)".
- Observed in `.ufo/waves/round-81/before/host/generator.txt` (line numbers via `grep -n "^### /run"`):
  - `:35-47` is the `fast.mount` block (header at :35).
  - `:95-107` is the `var-log.mount` block (header at :94).
  - `tmp.mount` is at `:64-78`; its `Before=local-fs.target` is at `:70`.
- JSON row MT5, measured leg, cites `lines 99-100`, quote `SourcePath=/etc/fstab Before=local-fs.target`. Those lines are `var-log.mount` (plain required mount, no `nofail`, no `x-systemd.before`). They do not evidence MT5's claim that `x-systemd.before=` re-acquires ordering for a `nofail` entry. The correct anchor is `:70` (tmp.mount).
- The quoted text is located verbatim, so the counter's R7 clause would pass; the substance of the citation is wrong.

## Checked, no contradiction (sweep results)

| Check | Observed | Evidence |
|---|---|---|
| A `nofail` mount required by a target | None. `local-fs.target` `Requires=` lists `-.mount boot.mount home.mount var-cache-pacman-pkg.mount var-log.mount` only. `tmp.mount`/`fast.mount` `RequiredBy=` is `tmp-.mount_alma.AFFvYd1.mount` (a mount) and empty. | surface §7, §8, §12 |
| Generated mount unit whose `Options=` carries `x-systemd.*` | One: `tmp.mount` (`x-systemd.before=`). `fast.mount`, `home.mount`, `boot.mount`, `-.mount`, `var-*` carry none. | surface §4, §7 (see C1) |
| Mount unit with no generator file | None hand-written. No `*.mount` or `*.mount.d` under `/etc/systemd/system`, `/run/systemd/system` or `/usr/lib/systemd/system`. Units with empty `FragmentPath` and `SourcePath=/proc/self/mountinfo` are runtime units: `tmp-.mount_alma.AFFvYd1.mount`, `run-user-1000*.mount`. | surface §6, §10 |
| Vendor unit shadowed by generator | `/usr/lib/systemd/system/tmp.mount` exists; live `FragmentPath=/run/systemd/generator/tmp.mount`. The fstab entry wins. | surface §6, §7 |
| Generator files vs capture | 18 of 22 generator files occur verbatim (whitespace-normalized) inside `host/generator.txt`. The 4 that do not are non-fstab (`sshd-unix-local.socket`, `sshd-unix-local@.service`, its `sockets.target.wants` link, `systemd-remount-fs.service` in `local-fs.target.wants`); the capture lists their names only. | receipts/gen-diff-vs-capture.txt, receipts/live-generator-dump.txt |
| Freshness | `/etc/fstab` mtime `2026-10-20 09:48:47`; generator files mtime `2026-11-04 17:34:49`; `uptime -s` `2026-11-02 12:07:17`. Generated output post-dates the last fstab write. `[INFERENCE]` generator re-ran at 17:34 today (boot predates it). | surface §1, §2 |
| Digests of pinned snapshots | `systemd.mount.xml` `afbf3be6…`, `systemd-fstab-generator.xml` `8de8acb8…`, `fstab-generator.c` `537e5f0f…` match `SHA256SUMS` and the JSON. | sha256sum run in the lane `before/src/` (read-only) |
| `x-systemd.device-timeout` drop-in shape | Both drop-ins exist, header comment records the option, body `JobRunningTimeoutSec=10s`. | surface §5 |
| `local-fs.target.wants/requires` anchors | `:135-145` holds the wants/requires listing in the capture. | surface §3, generator.txt:136-145 |

## Gaps (entry silent or incomplete; not contradictions)

- G1 MT1 statement says the `Before=` leg "is dropped when nofail … is present". Live `tmp.mount` has `nofail` and `Before=local-fs.target` (from `x-systemd.before`, MT5). The entry's prose covers this, the MT1 row does not.
- G2 `tmpfs /dev/shm` in fstab produces no generator unit (`dev-shm.mount` `LoadState=not-found`). Entry silent. `[INFERENCE]` consistent with `mount_point_is_api`, whose body is not in the snapshot (`grep -c mount_point_is_api` returns 1, the call only).
- G3 Vendor `tmp.mount` is shadowed (above). Entry silent.
- G4 `tmp.mount` is `RequiredBy=tmp-.mount_alma.AFFvYd1.mount`, a runtime AppImage mount under `/tmp`. Entry silent. A `nofail` mount has a required dependent here.
- G5 `local-fs.target.wants` also holds `systemd-remount-fs.service` (not fstab-derived); entry lists only `fast`, `tmp`.
- G6 `x-systemd.before=` on the `/tmp` entry is operator-chosen (entry says so). Not a contradiction.

## Not evaluated

- `tools/count-mount-rows-r81.py --revision <REV>` was not run (read-only seat; the counter is the lane's gate, not this surface). The counter's R7 would still pass for MT5 because the quote is verbatim at `:99-100`; C4 is a citation-substance defect the counter does not detect.
- No `systemctl start/stop/reload/daemon-reload`, no device removal, no boot test.
