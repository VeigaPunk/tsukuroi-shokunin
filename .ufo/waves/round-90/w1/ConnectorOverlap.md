# ConnectorOverlap — Tsukuroi Round 90 Wave w1 Report

Seat: ConnectorOverlap (connector).  
Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (branch `master`).  
Measured lane revision: `ce89df93e5f576c5c236d4547299e9ea954e8853` (HEAD; pre-round tip `c0f91856`, freeze `6511437e`).  
Receipts: `.ufo/waves/round-90/w1/ConnectorOverlap/` (absolute path `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-90/w1/ConnectorOverlap/`).  
Scope: Read-only scan of 20 sibling repos (`/home/vgpnk/Projects/shokunin/*-shokunin`, excluding tsukuroi) and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/considerthese/`. No lane or sibling file was edited; no `sudo` or host write was attempted.

---

## 1. Commands and Measured Revision

```bash
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master
ce89df93e5f576c5c236d4547299e9ea954e8853
[exit 0]
```

```bash
$ for r in /home/vgpnk/Projects/shokunin/*-shokunin; do
    [ "$r" = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin" ] && continue
    name=$(basename "$r")
    echo "=== $name ==="
    git -C "$r" grep -n -i -e limine -e measured_boot -e tpm2 -e LoaderTpm2 -- corpus tools 2>&1
  done
[exit 0]
```

Full scan receipts are recorded in:
- `.ufo/waves/round-90/w1/ConnectorOverlap/sibling-grep-exact.txt`
- `.ufo/waves/round-90/w1/ConnectorOverlap/sibling-grep-broad.txt`
- `.ufo/waves/round-90/w1/ConnectorOverlap/sibling-grep-secureboot.txt`
- `.ufo/waves/round-90/w1/ConnectorOverlap/sibling-grep-guid-uuid.txt`
- `.ufo/waves/round-90/w1/ConnectorOverlap/considerthese-survey.txt`
- `.ufo/waves/round-90/w1/ConnectorOverlap/commands.txt`

---

## 2. Sibling Overlap Scan

The exact command `git -C <repo> grep -n -i -e limine -e measured_boot -e tpm2 -e LoaderTpm2 -- corpus tools` was executed across all 20 sibling lanes. 18 sibling lanes yielded zero matches (`audio-shokunin`, `chousa-shokunin`, `game-dev-2d-shokunin`, `game-dev-3d-shokunin`, `kagi-shokunin`, `kaidoku-shokunin`, `kake-shokunin`, `kama-shokunin`, `kasegi-shokunin`, `kengaku-shokunin`, `kotoba-shokunin`, `kotodama-shokunin`, `kumitate-shokunin`, `lore-shokunin`, `mado-shokunin`, `revenger-shokunin`, `souji-shokunin`, `tameshi-shokunin`).

Hits were returned only by `mori-shokunin` (5 hits) and `tabi-shokunin` (2 hits). Additional broad queries across `corpus` and `tools` for `/sys/class/tpm`, `LoaderTpm2ActivePcrBanks`, `has-tpm2`, `measured_boot`, `limine.conf`, and `fslabel` returned 0 hits across all sibling repos.

### Table of Hits (Conflicts First)

| Sibling repo : file:line | Matched text | Classification | Evaluation against R1–R10 and C2 |
|---|---|---|---|
| `mori-shokunin:corpus/evidence/.ufo/waves/round-25/capture/capture.txt:10` | `+PAM ... +TPM2 ... +LIBARCHIVE` | **POTENTIAL CONFLICT** (Semantic trap / False positive) | Line captures systemd compile-time feature flags (`systemctl --version`). If an operator or automated gate probe uses `systemctl --version` or systemd feature tokens (`+TPM2`) to answer `--tpm-present`, it directly CONFLICTS with host reality. On this host, `/sys/class/tpm` is empty, ACPI tables lack TCPA/TPM entries, efivar `LoaderTpm2ActivePcrBanks` has `0x00000000` (zero banks), and no TPM module is loaded (`host/receipt.txt`). Answering `--tpm-present 1` based on `+TPM2` would cause the gate to model `on_panic: "halt"` (R10) when Limine v12.9.4 firmware actually forces measured boot off and reverts to `on_panic: "menu"`. Must be recognized as userspace library support, not hardware/firmware presence. |
| `mori-shokunin:corpus/evidence/sources-r34/S191.src:262` | `add_uevent_var(env, "PARTUUID=%s", part->bd_meta_info->uuid);` | **POTENTIAL CONFLICT** (Concept trap / Volume naming) | Kernel uevent source shows Linux `PARTUUID` is formatted from the partition's 128-bit GUID (`part->bd_meta_info->uuid`). In Limine v12.9.4 (`uri.c:355-358`), both `guid(...)` and `uuid(...)` dispatch to `uri_guid_dispatch`, resolving against the GPT partition GUID (Linux `PARTUUID`), NOT against the filesystem UUID (FAT 32-bit serial `86D8-C3F6`). Conflating Linux filesystem UUID with Limine's `uuid(...)` would cause URI resolution failure. On this host, the ESP is identified by `guid(b80445be-18ee-45e6-9a30-14339ea785a7)` or `uuid(b80445be-18ee-45e6-9a30-14339ea785a7)`, never by filesystem UUID. |
| `tabi-shokunin:corpus/evidence/w4-t4-3-sweep/forensics.log:57` | `Oct 14 13:11:07 ... Failed to create unit file ... /app-limine\x2dsnapper\x2dnotify@autostart.service: File exists` | **DUPLICATE** | Background forensic journal log of a transient systemd autostart generator collision. Duplicates historical host evidence of installed Arch package `limine-entry-tool` / userland desktop notification daemons. Orthogonal to bootloader-level limine.conf syntax, URI pins, and consequence modelling. |
| `tabi-shokunin:corpus/evidence/w4-t4-3-sweep/forensics.log:59` | `Oct 14 13:11:07 ... Failed to create unit file ... /app-limine\x2drestore\x2dnotify@autostart.service: File exists` | **DUPLICATE** | Same as above (`app-limine-restore-notify`). Duplicates background host service state. |
| `mori-shokunin:corpus/evidence/sources-r55/Documentation_admin-guide_kernel-parameters.txt.v7.2:7606` | `TPM2_PCR_Extend command. Consider this in a situation` | **COMPLEMENTS** | Kernel documentation for command-line parameter `tpm.disable_pcr_integrity=`. Complements C2 by documenting post-boot Linux kernel interaction with TPM2 PCR extension, but orthogonal to Limine v12.9.4 pre-boot UEFI TCG2 protocol checks. |
| `mori-shokunin:corpus/evidence/sources-r55/Documentation_admin-guide_kernel-parameters.txt.v7.3:7640` | `TPM2_PCR_Extend command. Consider this in a situation` | **COMPLEMENTS** | Identical documentation in kernel v7.3 sources. Complements post-boot PCR knowledge. |
| `mori-shokunin:corpus/evidence/sources-r61/kernel-parameters.txt:7640` | `TPM2_PCR_Extend command. Consider this in a situation` | **COMPLEMENTS** | Identical documentation in r61 source snapshot. |
| `mori-shokunin:corpus/evidence/sources-r61/v7.2/kernel-parameters.txt:7606` | `TPM2_PCR_Extend command. Consider this in a situation` | **COMPLEMENTS** | Identical documentation in r61 v7.2 source snapshot. |

---

## 3. Considerthese Review

Directory: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/considerthese/`  
Latest file: `considerthese/2026-10-26.md` (modified 2026-10-26 14:08).  
Section surveyed: `## Self-improvement ideas (proposed only, not acted on)`, lines 15–21.

### Inventory of the 5 Proposals in `2026-10-26.md`

1. **Burst-aware reading** (`considerthese/2026-10-26.md:17`):
   - Proposal: `"Four rounds in about 13 hours is more than a commit-by-commit read can cover well. In a burst, I could read each round's LOG entry and verifier spot-check first, then sample commits only where the two disagree..."`
   - Lane status: **IMPLEMENTED** (adopted in round 46, codified as **QUALITY criterion 112** in `corpus/QUALITY.md:112`: *"Burst-aware reading starts with outcomes, not volume: when recent rounds arrive in a burst, read each selected round's LOG and outside verifier result before drilling into its commits..."*).
2. **Counter-attack scoreboard** (`considerthese/2026-10-26.md:18`):
   - Proposal: `"For each frozen counter, track how many attack arms the wave fielded, how many survived, and which class beat it (leak read, fixture literal, answer-key read)..."`
   - Lane status: **IMPLEMENTED** (adopted in round 41 `corpus/lessons/round-41.md:99`, `SKILL.md:3833`, and codified as **QUALITY criterion 115** in `corpus/QUALITY.md:231`).
3. **Seat-harm incident log** (`considerthese/2026-10-26.md:19`):
   - Proposal: `"Seat-to-seat damage on the shared host (pkill, /tmp misroot, the round-37 fleet-root misroot) is now a recurring class separate from seat loss. A running tally per round would show whether isolation fixes are actually landing."`
   - Lane status: **IMPLEMENTED** (adopted in round 45 `corpus/lessons/round-45.md:124`, standing ledger continued in round 73 `corpus/lessons/round-73.md:120`, codified as **QUALITY criterion 110** in `corpus/QUALITY.md:218`).
4. **Downstream patch-offset check** (`considerthese/2026-10-26.md:20`):
   - Proposal: `"Round 40 found an Arch patch shifts util.c lines after :675 by +5. I could flag any knowledge anchor that cites upstream line numbers for code the host runs as a patched Arch build, so line pins don't silently drift."`
   - Lane status: **PARTIAL / RULE ADOPTED** (rule formally codified as **QUALITY criterion 103** in `corpus/QUALITY.md:201`: *"A line pin taken from an upstream tag is not a host-build line number, and an entry that cites upstream lines for code the host runs says so (R69-PATCH-OFFSET)... This is the lane's adoption of the considerthese/2026-10-26.md proposal 'Downstream patch-offset check'"*; no standing automated detector script in `tools/`).
5. **Cross-note correction propagation map** (`considerthese/2026-10-26.md:21`):
   - Proposal: `"The TO1/TO8 corrections had to be appended to seven older notes and three SKILL sections by hand (a2d7aad). A map of which notes depend on which propositions would let me check that a correction reached every dependent note."`
   - Lane status: **IMPLEMENTED** (adopted in round 43 `corpus/lessons/round-43.md:83`, formalized in round 75 as **QUALITY criterion 108** in `corpus/QUALITY.md:211`: *"A correction set names every companion that carries the corrected proposition, before it lands (R75-CORRECTION-PROPAGATION)..."*).

### Verdict: "None fits" (with detailed rationale)

Strictly, **none fits** because all 5 proposals in the latest file `considerthese/2026-10-26.md` have already been formally mined, adopted, and codified into tsukuroi lane rules and QUALITY criteria (QUALITY 103, 108, 110, 112, 115). Prior rounds (r78, r80, r83) have consistently recognized this closure.

### Evaluation of the Single Open Tooling Gap (Proposal 4)

If evaluated under the narrower standard of "unimplemented standalone tool" (where a rule exists but a standalone detector script in `tools/` is absent):

- **Quoted proposal:**
  > `- **Downstream patch-offset check.** Round 40 found an Arch patch shifts util.c lines after :675 by +5. I could flag any knowledge anchor that cites upstream line numbers for code the host runs as a patched Arch build, so line pins don't silently drift.`
- **What landing it would take:** Authoring a tool (e.g. `tools/check-downstream-patch-offset.py`) that fetches or reads the host's installed package sources/PKGBUILD patches (e.g. comparing the distribution's build against the upstream Git tag) and diffs line coordinates for files cited in `corpus/knowledge/` or `tools/check-limine-pins.py` line pins, raising an error when a downstream distribution patch introduces line shifts.
- **Why it does not fit Round 90:** In Round 90, C1 and C2 evaluate consequence modelling and volume discernment against pinned upstream Limine v12.9.4 source code committed directly in `.ufo/waves/round-90/before/src/`. The battery `limine-pin-battery-r90.py` is frozen, and its line anchors (R1: `config.c:527-551`, R2: `uri.c:28-104`, R9: `chainload.c:414-435`, R10: `panic.s2.c:24-28, 70-78`) bind directly to those pinned upstream bytes. Adding a downstream patch detector would exceed the round's frozen battery and scope boundaries.

---

## 4. UFO-FSD Connector Synthesis: One Non-Obvious Move

### Evidence
1. **Host State (`host/receipt.txt`):** The host ESP is `/dev/nvme0n1p1` (`FSTYPE=vfat`, `PARTUUID=b80445be-18ee-45e6-9a30-14339ea785a7`, `UUID=86D8-C3F6`, `LABEL=` empty). The host has no active TPM (`/sys/class/tpm` empty, `LoaderTpm2ActivePcrBanks` has zero active banks `0x00000000`, SecureBoot disabled `00`).
2. **Limine Source Semantics (`uri.c:355-360`, `panic.s2.c:70-78`, `menu.c:1719-1728`):**
   - Limine's `uuid(...)` and `guid(...)` both invoke `uri_guid_dispatch`, which matches GPT partition GUIDs (Linux `PARTUUID`), NOT filesystem serial numbers (Linux `UUID`).
   - Limine's `fslabel(...)` matches filesystem labels; on this host, `fslabel(...)` cannot resolve the ESP because the ESP filesystem label is empty.
   - Limine's `on_panic` logic (R10) requires active EFI TCG2 protocol presence at boot. If TPM is absent (`--tpm-present 0`), Limine overrides `measured_boot: yes` and defaults to returning to the menu (`on_panic: "menu"`).
3. **Sibling Overlap (`mori-shokunin`):** Systemd's feature banner contains `+TPM2`, which creates a false-positive trap if inspected in place of hardware/firmware device state.

### Affected Axes
- **Operability (9):** Eliminates operational misclassification of `--tpm-present` and volume naming in `tools/check-limine-pins.py`.
- **Freshness (9):** Grounds C2 (`limine-tpm-volume-r90.md`) in authoritative host substrate observations rather than stale userspace assumptions.

### Proposed Move
Synthesize the boundary between pre-boot UEFI firmware state and Linux userland diagnostic state into an authoritative, unprivileged two-signal operational contract for C2 and gate operators:

1. **Autoritative `--tpm-present` Derivation:** An unprivileged userland gate invocation must evaluate `--tpm-present` strictly via `/sys/class/tpm/tpm*` (or `/sys/firmware/efi/efivars/LoaderTpm2ActivePcrBanks*` when accessible), and MUST NOT evaluate `systemctl --version` (`+TPM2`) or kernel build configurations (`CONFIG_TCG_TPM=y`). On this host, `/sys/class/tpm` is empty, confirming `--tpm-present 0`.
2. **Authoritative Volume Naming Map for Host ESP:** Document in C2 that the host ESP (`/dev/nvme0n1p1`) is resolvable by Limine v12.9.4 via:
   - `boot()` (default empty root)
   - `boot(1)` (1-based partition on boot drive)
   - `hdd(1:1)` (drive 1, partition 1)
   - `guid(b80445be-18ee-45e6-9a30-14339ea785a7)` (GPT partition GUID)
   - `uuid(b80445be-18ee-45e6-9a30-14339ea785a7)` (synonym for guid)
   - But **NEVER** `fslabel()` (ESP label is empty) and **NEVER** `uuid(86D8-C3F6)` (FAT volume ID is not a GPT partition GUID).

### Risks
Operators might assume `/sys/class/tpm` is empty due to a missing kernel driver rather than firmware TPM absence. This is mitigated by `host/receipt.txt` confirming `CONFIG_TCG_TPM=y` is built into the kernel, ACPI has no TCPA/TPM tables, and efivar `LoaderTpm2ActivePcrBanks` records zero active banks.

### Verification
Grounded in `host/receipt.txt` lines 4–35, `limine-v12.9.4-common_lib_uri.c:355-360`, and `limine-pin-battery-r90.py` R4, R10.
EOF