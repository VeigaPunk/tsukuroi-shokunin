# C1Connector — sibling overlap & held-ground scan (round 71, w1)

Seat: C1Connector. Read-only. Lane tree at `0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e`
(the round-71 declaration commit; `git rev-parse HEAD` printed that id).
Question: does the kernel module-parameter surface (sysfs `parameters/`, `modprobe.d`,
`module_blacklist=`, kernel cmdline `mod.param=` tokens) belong to tsukuroi or to a sibling?
Second question: do the declaration's novelty claims still hold at this revision?
Third: does the r70 D1 stale-tally class recur in the files this round will touch?

## 1. Ownership decision — tsukuroi, with four quoted sentences

**Decision: tsukuroi owns the surface.** No sibling claims it; one sibling cedes it
explicitly; the two RE lanes' claim is scoped to shipped artifacts, not published kernel
source; the gate-method lane refuses product domains.

| # | Lane | Quoted ownership sentence (verbatim) | Site |
|---|---|---|---|
| O1 | tsukuroi | "**Owns (surfaces, all read-only probes):** pacman state (`pacman -Qkk` verify loops, foreign/AUR census, `.pkg.tar.zst` receipt discipline), systemd user units & timers (`systemctl --user`, unit files, failed states), journal/boot triage (`journalctl -b`, dmesg error classes), driver/firmware plane (kernel modules, nvidia driver + GSP firmware presence, `nvidia-smi` shape)." | `PROVINCE.md:8-13` |
| O2 | mori | "**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package, systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal and cgroup events as fleet evidence and reports them, never owning OS state; endpoint and model-serving health (→ kama); credential material (→ kagi)." | `../mori-shokunin/PROVINCE.md:12-15` |
| O3 | kama | "**Refuses:** model quality/eval (kengaku), credential material & auth flows (kagi), dispatch/route mechanism (kumitate), remote web surfaces (kake). Boundary rule: kama answers *\"is the thing at this baseURL the model this config believes it is, right now\"* — never *\"is the model good\"* or *\"is the request safe\"*." | `../kama-shokunin/PROVINCE.md:42-45` |
| O4 | revenger | "Owns: reverse engineering of shipped artifacts — native binaries, managed assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, browser/Electron runtime evidence — using the REA skill and its toolset, with an evidence-ledger discipline" | `../revenger-shokunin/PROVINCE.md:3-6` |
| O5 | kaidoku | "**Domain:** reverse engineering of shipped artifacts with REA on this Linux host — native ELF through the Ghidra 12.1.4 provider, Electron/ASAR/JavaScript bundles, archives and packages; evidence-first static analysis that keeps observation, inference and unknowns separate." | `../kaidoku-shokunin/PROVINCE.md:3-6` |
| O6 | tameshi | "**Refuses:** product domains — every lane's gate remains its own; tameshi owns only the reusable craft … Never edits a sibling's gate code (read-only probes; recommendations travel in round reports)." | `../tameshi-shokunin/PROVINCE.md:14-17` |
| O7 | kotoba | "tsukuroi owns host package and initramfs hooks and OS state as read-only probes (PROVINCE.md:22); kotoba routes only client hook-config files and cedes host hooks (hook-files-round59.md:20), a split stated on kotoba's side alone." | `../kotoba-shokunin/PROVINCE.md:78` |

Row-by-row application to the four C1 components:

| Component | Owner | Basis |
|---|---|---|
| `/sys/module/<name>/parameters/*` presence, mode/`perm`, store-handler presence | tsukuroi | O1 "driver/firmware plane (kernel modules …)"; O2 cedes "driver/firmware and boot state (→ tsukuroi)" |
| `modprobe.d` file presence (paths/modes only) | tsukuroi | O1 driver/firmware plane; package-adjacent config under `/etc`/`/usr/lib` is OS state; O7 confirms host-side hooks/OS state are tsukuroi's |
| `module_blacklist=` cmdline token, unknown-parameter warn-and-ignore | tsukuroi | O1 "journal/boot triage"; O2 cedes boot state; tsukuroi `PROVINCE.md:21` already holds "Initramfs v42 and boot recovery" |
| `kernel_param_ops` / `param_attr_store` contract (specification reading) | tsukuroi | published upstream source, not a shipped binary (see §2 contradiction R2) |

Sibling by sibling, the surface is not theirs:
- **kama** — endpoint/serving question only (O3); a module parameter's mode says nothing
  about whether a served model is the one a config names.
- **mori** — fleet capacity, watchdog, journal/OOM correlation; cedes driver/firmware and
  boot state (O2). Its "kernel OOM" rows are journal *records*, not module parameters.
- **revenger / kaidoku** — "shipped artifacts" and native binaries (O4, O5). Kernel
  `params.c`/`moduleparam.h` at tag `v7.2.11` are published upstream source, the same class
  of evidence the lane already mined for S208–S212 (pacman source) and S290–S293
  (`fs/xfs/xfs_stats.c`, `fs/xfs/xfs_sysfs.c`).
- **tameshi** — method only, and it refuses product domains (O6); C2's census change stays
  tsukuroi's gate.
- **kumitate / kengaku / mado / kagi / kake / others** — no mention of the surface (see §3).

## 2. Contradictions stated, not smoothed

**R1 — `PROVINCE.md:25-27` vs. C1's source reading.**
"**Refuses:** endpoint/model serving health (→ kama), secrets (→ kagi), binary RE of drivers
(→ kaidoku/revenger — tsukuroi tracks *state and health*, not internals)." C1 reads kernel
source to state the *plane's contract* (`kernel_param_ops` set/get return conventions, the
warn-and-ignore path for an unknown parameter). This is not a contradiction of R1 as written —
"binary RE of drivers" is about reversing shipped driver binaries, and R1's own parenthetical
reserves *state and health* to tsukuroi — but it is a live tension the note must respect:
MP1–MP6 may state the generic kernel contract and the observed `perm` values, and must not
state nvidia-internal semantics (what `NVreg_*` does inside the driver). Reading published
source for an owned surface is the lane's established practice (S208–S212, S290–S293), not a
new claim class.

**R2 — `ADJ-06` vs. C1.** `PROVINCE.md:49` routes "Driver/firmware/package mechanism requires
shipped-artifact reverse engineering beyond health inventory" to "protocol integrator —
kaidoku/revenger ownership unresolved". ADJ-06 fires only where the question needs
*shipped-artifact RE*; C1's question is answered from published source and sysfs modes, so
ADJ-06 is not triggered. If a later round wants driver-internal NVreg semantics, that is
ADJ-06 work, not C1.

**R3 — false friend, `cmdline`.** `../kengaku-shokunin/PROVINCE.md:14` matches "cmdline"
("`/proc/1299/cmdline` == `~/.config/systemd/user/qwen-coder.service` ExecStart"). That is a
*process argv* pin, not the kernel boot cmdline. A later sweep grepping bare "cmdline" across
siblings will hit kengaku and must not read it as either a sibling claim on
`/proc/cmdline` or a novelty counterexample.

**R4 — no snapshot-content overlap with a sibling.** Sibling corpora hold zero hits for
`module_blacklist|kernel_param_ops|param_attr_store|/sys/module/<name>/parameters`, so the
four committed snapshots cannot duplicate a sibling's held ground either.

## 3. Held-ground check at the declaration revision — holds

Command shape (read-only, lane tree): `grep -rIl -- "<term>" corpus/ SKILL.md PROVINCE.md`.

| Term | File hits | Declaration claim |
|---|---|---|
| `modprobe.d` | 0 | 0 — holds |
| `kernel-parameters` | 0 | 0 — holds |
| `module_blacklist` | 0 | 0 — holds |
| `NVreg` | 0 | 0 — holds |
| `module_param` | 0 | 0 — holds |
| `kernel_param_ops` | 0 | 0 — holds |
| `param_attr_store` | 0 | 0 — holds |

`NOVELTY_COUNTEREXAMPLES=0`. Cross-check on the sibling side (all 21 sibling
`PROVINCE.md`, `grep` tool, pattern `modprobe|module_blacklist|module_param|/sys/module|NVreg|kernel-parameters`):
**no matches**. Sibling corpora, pattern `module_blacklist|kernel_param_ops|param_attr_store|/sys/module/[a-z_]+/parameters`:
**no matches**. The surface is unheld fleet-wide, not merely lane-wide — which raises the
adjacency value of C1 but also means no sibling can corroborate the note's statements; the
four committed snapshots are the only evidence, and that is what the frozen counter enforces.

## 4. Residual overlap risks for the round

1. **Registry ids S297–S300 must be free.** Declaration plans four ids; the base registry
   holds 296 rows (`before/absence-controls.txt`). A sibling lane has its own registry, so
   the risk is intra-lane only — but the ids are the round's most collision-prone token.
2. **`modprobe.d` mode-only boundary.** `before/host.txt` records paths and modes and never
   contents; the note must not cite file contents it never read (secrets shape-only rule,
   `PROVINCE.md:25` "secrets (→ kagi)").
3. **C2 touches `tools/tsukuroi-census.sh` only** — tameshi refuses product-domain gates
   (O6), so no handoff is owed; the case-timeout harness is a tsukuroi gate change.
