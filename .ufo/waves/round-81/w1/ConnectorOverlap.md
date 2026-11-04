# Seat ConnectorOverlap — Binding Report

- **Seat:** ConnectorOverlap
- **Role:** connector (Godspeed-enabled subagent, UFO-FSD connector)
- **Wave:** round-81 w1
- **Lane Root:** `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
- **Base Revision:** `96ad75b84160da58efaee4997576ce718fd72e2b`
- **Declaration-Only Commit:** `8023711867eaa788f68af09d7f29d24db749cca7` (author trials preceded it; not a compliant pre-data freeze)
- **Report Path:** `.ufo/waves/round-81/w1/ConnectorOverlap.md`
- **Detailed Findings:** `.ufo/waves/round-81/w1/ConnectorOverlap/overlap.md`

---

## 1. Declared Axes

The round's declared axes are:
1. **`depth`**: Sourced technical depth on the fstab-to-mount unit translation plane (C1: rows MT1–MT8 in `corpus/knowledge/mount-unit-fstab-plane-r81.json`, counter `tools/count-mount-rows-r81.py`, 8 verified rows, 8 distinct settings, >=2 measured legs from S332).
2. **`operability`**: Protocol gate-standard compliance and CLI exit code discipline (C2: 0 met, 1 unmet, 2 could-not-evaluate, 3 selftest failed across 6 exported cases in `tools/measure-round81.py` scoring `tools/measure-round80.py` against `before/gate-standard-r81.json`).
3. **`freshness`**: Pinned provenance and snapshot re-verification (C3: zero knowledge-header findings via `tools/check-knowledge-header.py` after appending operative `verified-at: 2026-11-04` lines to `modprobe-config-plane-r72.md` and `module-parameter-plane-r71.md` with re-verified `SHA256SUMS`).

---

## 2. Sibling-Overlap Scan

### Question
Does any sibling lane already own the `fstab` → `mount unit` ground claimed in Round 81?

### Methodology
Every sibling lane repository under `/home/vgpnk/Projects/shokunin/*-shokunin/` was scanned read-only across `PROVINCE.md`, `SKILL.md`, and all files in `corpus/knowledge/` using the specified regex patterns:
`fstab`, `automount`, `x-systemd\.`, `mount unit`, `local-fs\.target`.

```bash
python3 -c "
import glob, os, re, subprocess
siblings = sorted([d for d in glob.glob('/home/vgpnk/Projects/shokunin/*-shokunin') if not d.endswith('tsukuroi-shokunin')])
cmd = ['grep', '-n', '-E', '-i', 'fstab|automount|x-systemd\\.|mount unit|local-fs\\.target']
# executed over PROVINCE.md, SKILL.md, and corpus/knowledge/** for each sibling
"
```

### Lane-by-Lane Results

| Sibling Lane | Target Files Scanned | Hits (file:line) | Classification | Analysis / Ownership |
|---|---|---|---|---|
| `audio-shokunin` | 19 | None | unrelated | No ownership; domain is sound, pipewire, audio sinks. |
| `chousa-shokunin` | 94 | None | unrelated | No ownership; domain is fleet investigation & log scraping. |
| `game-dev-2d-shokunin` | 6 | None | unrelated | No ownership; domain is Godot 2D assets & mechanics. |
| `game-dev-3d-shokunin` | 49 | None | unrelated | No ownership; domain is Godot 3D shaders & assets. |
| `kagi-shokunin` | 37 | None | unrelated | No ownership; domain is secret hygiene & credentials. |
| `kaidoku-shokunin` | 172 | None | unrelated | No ownership; owns binary RE & squashfs decompression, not mount unit plane. |
| `kake-shokunin` | 85 | None | unrelated | No ownership; domain is financial ledger & bounty accounting. |
| `kama-shokunin` | 61 | None | unrelated | No ownership; PROVINCE explicitly refuses systemd writes; checks model port liveness. |
| `kasegi-shokunin` | 85 | None | unrelated | No ownership; domain is task execution & telemetry. |
| `kengaku-shokunin` | 79 | None | unrelated | No ownership; domain is local LLM inspection & evaluation. |
| `kotoba-shokunin` | 68 | None | unrelated | No ownership; domain is natural language processing & corpus linguistics. |
| `kotodama-shokunin` | 262 | None | unrelated | No ownership; owns bwrap container isolation replay, not host fstab/mount units. |
| `kumitate-shokunin` | 82 | None | unrelated | No ownership; owns swarm runner orchestration & task dispatch semantics. |
| `lore-shokunin` | 28 | None | unrelated | No ownership; domain is history, repository lore, and conventions. |
| `mado-shokunin` | 108 | None | unrelated | No ownership; domain is window management, Hyprland, and desktop UI. |
| `mori-shokunin` | 70+ files (694 lines in PROVINCE) | `corpus/knowledge/observability-census-r1.md:217` | incident mention | Mentions `automount` as threat-model debt under unquoted `df` argument overrides (`MORI_*_BIN`). **mori PROVINCE.md:12-14 explicitly refuses systemd units and boot state in favor of tsukuroi**. |
| `revenger-shokunin` | 25 | None | unrelated | No ownership; domain is disassembly & decompilation. |
| `souji-shokunin` | 43 | None | unrelated | No ownership; domain is hygiene, cleanup, and garbage collection. |
| `tabi-shokunin` | 77 | None | unrelated | No ownership; domain is host migration & network routes. |
| `tameshi-shokunin` | 72 | None | unrelated | No ownership; domain is mutation testing & verification methodologies. |

### Ownership Conclusion
**No sibling lane owns the `fstab` → `mount unit` ground.** Out of 20 sibling repositories, 19 have zero matches. `mori-shokunin` carries a single incidental threat-model mention in `observability-census-r1.md:217` regarding `df` automount side-effects, and `mori-shokunin/PROVINCE.md:12-14` explicitly refuses systemd unit and boot state, assigning them directly to `tsukuroi`.

---

## 3. Adjacency Note Assessment for PROVINCE.md

**Adjacency Verdict (One Line):**
No adjacency note is required in `PROVINCE.md` because no sibling lane owns or claims fstab→mount-unit translation, and the ground falls directly within `tsukuroi-shokunin`'s owned OS/systemd substrate domain (with mori explicitly refusing systemd/boot state in favor of tsukuroi).

---

## 4. Held-Ground Sweep in tsukuroi-shokunin (QUALITY 102)

### Command
```bash
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin grep -n -i -E \
  'fstab|automount|systemd\.mount|x-systemd' 96ad75b84160da58efaee4997576ce718fd72e2b -- corpus/
```

### Observed Matches at Base `96ad75b8`
1. `corpus/SOURCES.md:62`: S056 source registry description mentions snapshot-2 fstab diff during round-17 Limine boot chain investigation.
2. `corpus/knowledge/boot-chain-r17.md:32`: Notes `/etc/fstab` package install timestamp (`09:19:40`).
3. `corpus/knowledge/boot-chain-r17.md:90`: Lists `/etc/fstab` in a list of root configuration paths.
4. `corpus/knowledge/boot-chain-r17.md:102-103`: Observes that snapshot #2 `/etc/fstab` predates edits and lacks `/tmp` and `/fast` XFS lines (both `nofail`).
5. `corpus/knowledge/boot-chain-r17.md:184`: Summarizes S056 capture contents.
6. `corpus/knowledge/degraded-triage-r4.md:400`: Mentions `/etc/fstab:18` mounting the ESP (`UUID=86D8-C3F6 /boot vfat`) during permission triage.
7. `corpus/lessons/round-18.md:94`: Retrospective text mentioning S056 fstab scope.

A secondary search for generator terms (`systemd-fstab-generator`, `fstab-generator`, `mount-unit`) at base `96ad75b8` returned **0 matches** (exit code 1).

### QUALITY 102 Finding
No prior entry in `tsukuroi-shokunin` holds rows MT1–MT8 or the fstab→mount-unit translation plane. The references in `boot-chain-r17.md` and `degraded-triage-r4.md` are incidental triage observations regarding file modification timestamps and the ESP mount point. The ground claimed in Round 81 is verified unheld prior ground, satisfying QUALITY 102(b).

---

## 5. Non-Obvious Move — UFO-FSD Connector Synthesis

### Evidence
1. **Ground Evidence:** `mori-shokunin/corpus/knowledge/observability-census-r1.md:217` documents that executing `df` against paths declared in `/etc/fstab` can inadvertently trigger automounts when `x-systemd.automount` is active.
2. **Substrate Evidence:** Host generator output (`.ufo/waves/round-81/before/host/generator.txt:120-134`) proves that `systemd-fstab-generator` generates `.device.d/50-device-timeout.conf` drop-ins with `JobRunningTimeoutSec=10s` for `x-systemd.device-timeout=10s`, while stripping `x-systemd.*` options from the emitted mount unit's `Options=` parameter.
3. **Runtime Evidence:** In `mount-unit-fstab-plane-r81.json`, rows MT2 (`nofail`), MT5 (`x-systemd.before=`), and MT6 (`x-systemd.device-timeout=`) prove that a `nofail` entry without `x-systemd.before=` (`/fast`) imposes zero delay at boot, whereas a `nofail` entry with `x-systemd.before=local-fs.target` (`/tmp`) blocks `local-fs.target` for up to 10 seconds waiting for the device unit.
4. **Tooling & Contract Evidence:** `tsukuroi-shokunin/PROVINCE.md:229-233` mandates that tsukuroi's own storage probe reads `/proc/self/mounts` directly to inspect mounts without interpretation, avoiding path resolution.

### Affected Axes
- **`depth` (Improved):** Deepens the operational understanding of the fstab translation plane by synthesizing the distinction between **boot-latency waiting** (`nofail` + `x-systemd.before` waiting on device units) and **access-latency activation** (`x-systemd.automount`), tying upstream documentation directly to host failure behavior.
- **`operability` (Improved):** Establishes an explicit probe invariant: OS triage probes must inspect `/proc/self/mounts` and `/run/systemd/generator/` unit files rather than path-statting (`df`, `stat`), preventing triage tooling from accidentally inducing 10-second device stalls or triggering unmounted filesystems.
- **`freshness` (Neutral):** Reuses the pinned, digest-verified snapshots (`systemd.mount.xml` S331, generator capture S332) without introducing unverified assumptions or drifting dates.

### Proposed Move
Formulate and record in the companion knowledge analysis (`mount-unit-fstab-plane-r81.md`) and future probe guidance an explicit **Boot-Delay vs. Access-Delay Triage Invariant**:
- A mount configured with `nofail` + `x-systemd.before=local-fs.target` delays boot sequencing by up to the device timeout (10s in `/tmp`) when a drive fails to appear, despite being non-fatal.
- Conversely, `x-systemd.automount` (MT4) defers device timeouts and filesystem activation entirely to first userspace access, eliminating boot latency at the cost of potential run-time stalls.
- Consequently, host observability and triage probes (in both tsukuroi and mori) MUST query `/proc/self/mounts` or read generated unit drop-ins under `/run/systemd/generator/`, never issuing commands like `df` that touch mount paths and trigger automount delays.

### Risks
- *Contradiction with Frozen Predicates:* Modifying the frozen 8 rows in `mount-unit-fstab-plane-r81.json` would trip counter clauses R1–R7 in `count-mount-rows-r81.py`. This synthesis must remain strictly in analytical prose and provincial probe contracts, preserving the exact frozen JSON structure.
- *Cross-Lane Province Creep:* Mori refuses OS/systemd remediation. This invariant must be communicated as probe safety guidance (read-only query discipline), not as service or mount configuration changes.

### Verification
1. `count-mount-rows-r81.py --fixture <lane>` continues to pass with `"count": 8, "target": 8, "finding": "met"`, rc 0.
2. `measure-round81.py --fixture <lane>` continues to pass with `"count": 6, "target": 6, "finding": "met"`, rc 0.
3. Probes inspecting storage state execute strictly via `/proc/self/mounts` without issuing stat calls against automounted targets.

---

## 6. Subagent Hygiene & Host Accounting

- **Tool Authorizations:** No tools installed or upgraded (pacman paused host-wide).
- **Git / jj Mutations:** Zero mutations performed. No commits, branch modifications, or staging changes executed.
- **Scratch Directory:** `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r81/ConnectorOverlap/` was verified and removed before completion.
