# C2 /boot writer boundary review

Axes: owned-surface fit; operator safety; attribution/evidence limits.

- [obs] PROVINCE Core owns read-only systemd unit/timer and journal/boot triage; its added boot-recovery and Snapper/rollback surfaces forbid rebuild/boot and restore/config changes. (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:8-14,22-23`)
- [obs] The assigned scope is 10 journal events plus two ALPM-SCRIPTLET `/boot/limine.conf` updates. (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:11-20`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19.txt:578,597`)
- [inf] Classifying those captured events by writer and source mechanism is inside existing boot/rollback diagnostics; no new PROVINCE Core row is needed. This remains read-only reporting, not authorization. The captured snapper plugin source includes a `limine-snapper-restore` call on `set-default-snapshot-pre`, so static source review must not become plugin/action execution. (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1199-1245`)
- [obs] Boot-chain authority is observation, namespace emulation and source-grounded inference only; no package, service, initramfs, bootloader or `/boot` changes are authorized. Its recheck says sudo is used only to read `/boot`. (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/boot-chain-r17.md:3,10-11`) `/boot` resizing or boot-file changes remain operator work. (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/snapper-eacces-mechanism.md:36`)

**Exact limits text for the knowledge entry:** “This entry attributes only the 12 captured `/boot/limine.conf` write events to observed writer classes and source-grounded mechanisms; writer/service attribution is not human-operator attribution absent independent evidence. It uses existing read-only captures and opened source files, not live `/boot` inspection or sudo. If evidence would require privileged/live access, mark it [unk] and leave that observation to the operator. It does not authorize or perform `/boot` or Limine restoration/configuration, package transactions, writer-unit/timer/hook execution or restart, rebuild, or boot; remediation remains operator-owned.”

Rejected: a new ownership surface, or treating event attribution as authorization to inspect or repair `/boot`. Model: openai-codex/gpt-6-luna.

Scope: executed=none