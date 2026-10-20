# NoOralReview — round-12 static review (no executed E2E)

Seat: NoOralReview (reviewer, leaf). Scope: written root-mechanism instructions only; no oral context. Static review; nothing below is an executed end-to-end result. No PASS is claimed. No install, upgrade, sudo, systemd-run, census run, selftest, pacman verify, or host write was performed. No tool was installed or updated (install log: none).

Matrix status: `corpus/knowledge/root-dac-decision-r12.md` and `.json` were **absent** at review time (`ls` → no such file). Matrix-specific checks are therefore **deferred**, not passed. Re-run this review when the Matrix seat lands.

## 1. Inputs read (read-only)

- `PROVINCE.md` (whole; Owns/Refuses/Adjacent/Frontier; lines 8-28, 35-52, 70-80).
- `corpus/QUALITY.md` (whole; items 1-13).
- `corpus/lessons/round-1.md:21-43` (Mistakes table, D1-D6, M3-M13).
- `corpus/knowledge/snapper-eacces-mechanism.md` (whole, 58 lines).
- `corpus/knowledge/degraded-triage-r4.md:312-329, 522, 602, 623-627`.
- `corpus/SOURCES.md` rows S010, S019-S034 and notes at lines 44-54.
- `corpus/README.md:20, 40`.
- `tools/tsukuroi-census.sh:14-56, 286-303, 340-341, 1579-1586, 1662, 2017, 2028`.
- `.ufo/waves/round-12/spec.json` (context and all items' `# Target`/`# Acceptance`; full text read via node slices).
- `/home/vgpnk/.omp/agent/RULES.md` (whole).
- Peer seats' prompts (Census, Matrix) were read as written instructions. `.ufo/waves/round-12/dispatch.json` has zero items; `swarm-registry.json` (mode 0600) was **not opened**.

## 2. Read-only probes run (command → exit → observed)

| Command | rc | Observed |
|---|---|---|
| `stat -c '%a %U:%G %n' /` | 0 | `555 root:root /` |
| `systemctl show limine-snapper-sync.service -p User -p CapabilityBoundingSet -p ProtectSystem -p ProtectHome -p NoNewPrivileges` | 0 | `User=root`, `CapabilityBoundingSet=cap_sys_admin`, `ProtectSystem=no`, `ProtectHome=yes`, `NoNewPrivileges=yes` |
| `findmnt -n -o TARGET,FSTYPE,OPTIONS /` | 0 | `/ btrfs rw,…,subvol=/@` (no `ro`) |
| `pacman -Qo /usr/bin/test` | 0 | owned by `coreutils 9.11-2` |
| `command -v` for stat, systemctl, systemd-analyze, findmnt, getfacl, jq, node, shellcheck, pacman, journalctl, sudo, namei, lsattr, getcap, capsh, getpcaps, snapper, btrfs, zcat, timeout, tac | 0 | all present; `bun`, `bats` absent (bats not required: census has its own `--selftest`) |
| `[ -e ]` on every cited sibling/knowledge/source path | 0 | all present except S030 path (see F5) |
| Web reads of man-pages S027 (capabilities(7)), S028 (systemd.exec(5)), S034 (access(2)) | n/a | quotes re-checked (see F3) |

Not run: `sudo` (any form), `systemd-run`, `sudo -n`, `pacman -Qkk`, census or selftest, any write.

## 3. Tool inventory against the written instructions

- Every command the snapper note and r4 note name is present on this host (`stat`, `getfacl`, `systemctl`, `journalctl`, `findmnt`, `zcat`, `snapper`, `pacman -Qo`, `btrfs`). No missing tool blocks a static or read-only step.
- Missing-tool risk is not a binary absence; it is a **privilege** gap: the runtime-capability and subvolume-layout discriminators need root (see F2, F9).
- `RULES.md` licenses installs via `sudo pacman -S`; this lane's contract forbids package operations (see F1). No install was needed for this review.

## 4. Findings (severity order)

### HIGH

**F1 — Contradictory authority on sudo and package operations (contract vs. operator directive vs. province).**
- Evidence: `spec.json` context Contract: "NO sudo/host mutation, package operations, service restarts or systemd-run." The same paragraph: "Every seat may install or upgrade tools that help the task; read RULES.md first … Prefer no installs." `RULES.md` lines 1-16: any agent "installs or updates any tool … with full privilege, without asking first. Passwordless `sudo` is available." `PROVINCE.md:27-28`: "Never installs, upgrades, or removes packages."
- Risk: a seat reading RULES first can justify `sudo pacman -S` while the contract and province forbid it. No precedence rule is written. Passwordless sudo is an operator assertion; I did not verify it (running `sudo -n` is forbidden by this lane's contract).
- Recommendation for parent: state one rule for round-12 — no installs; RULES' tooling directive does not override the lane contract or PROVINCE for this wave.

**F2 — The only written discriminator for the capability branch is privileged; the read-only substitute cannot exercise runtime caps while the unit is inactive.**
- Evidence: `snapper-eacces-mechanism.md:23-28` falsifier is `sudo systemd-run --wait --pipe -p CapabilityBoundingSet=CAP_SYS_ADMIN test -w /` and `sudo test -w /` (labelled "operator-only … not run"). `degraded-triage-r4.md:522` lists `sudo btrfs subvolume create /.snapshots` as a discriminator — this one **mutates** state. `degraded-triage-r4.md:318` records the unit `is-active` = inactive (oneshot, last ran at boot).
- Read-only substitute observed: `systemctl show … -p CapabilityBoundingSet` → `cap_sys_admin` (rc 0, non-root). This is **configuration**, not the running process's bounding/effective/permitted sets. A running-process read (`/proc/<pid>/status` CapBnd/CapEff) has no PID to read while the unit is inactive.
- Risk for the Matrix ("each discriminator runnable read-only"): the capability and root-DAC branches have no runtime discriminator runnable without privilege right now. Matrix must mark them `not-runnable-read-only` or cite the configuration read as weaker evidence.
- Also: `test -w` run as the invoking non-root user tests vgpnk's authority, not root's. It cannot discriminate the root-DAC branch.

**F3 — Falsifier rationale cites access(2) for a path the cited rule may not govern.**
- Evidence: `snapper-eacces-mechanism.md:30` says "`access(2)` (S034) explains why this `test -w` comparison distinguishes root's permitted capabilities from its effective capabilities." Fetched S034 (`https://man.archlinux.org/man/access.2`): "for the root user, the check uses the set of permitted capabilities rather than the set of effective capabilities" — quote verified. The same page, faccessat `AT_EACCESS`: "Perform access checks using the effective user and group IDs. By default, faccessat() uses the real IDs (like access())." — verified.
- Gap: `/usr/bin/test` is coreutils 9.11-2 (verified). I did **not** verify which syscall coreutils' `test -w` uses. [inf] it uses an effective-ID (`AT_EACCESS`) path, which would make the access(2) permitted-set rule the wrong citation.
- Impact: the predicted rc (1 with bounded set, 0 with full caps) is unaffected, because permitted and effective sets are equal in both cases. The explanation is unsupported. The `Capabilities` seat is already tasked to audit this exact language; cross-reference, not a new owner.
- Also noted: S027 quote "Bypass file read, write, and execute permission checks." verified (capabilities(7) CAP_DAC_OVERRIDE). capabilities(7) also says privileged (effective UID 0) processes "bypass all kernel permission checks" in the traditional model. Matrix must frame root-with-reduced-caps as the discriminating case, not as "root bypasses DAC" (already prohibited by the Matrix spec).
- S028 quote "Capabilities listed will be included in the bounding set, all others are removed." verified (systemd.exec(5) CapabilityBoundingSet=). The note's extension "also affects effective and permitted sets" was **not** verified: the grep window cut at "Note that this option also affects the respective capabilities in".

**F4 — Census C1 changes the live verdict on this host, and its premise is an unproven intent.**
- Evidence: Census spec: "worsen verdict for missing owner write/search as named DEGRADED." Live `/` is `555 root:root` (probe above). `snapper-eacces-mechanism.md:34`: "An operator may determine why `/` is `0555`; if that mode is unintended …". `PROVINCE.md:8-14`: census owns read-only probes only.
- Risk 1: the live `TSUKUROI_CENSUS` verdict will move to packages=DEGRADED and overall exit 1 on this host. The spec does not state the expected live change or add a consumer-visible expectation.
- Risk 2: "missing owner write" is a mode-bit observation. It is not a writability fact: mode bits cannot say whether a root process with CAP_DAC_OVERRIDE can write. Calling it a named defect presumes intent that the note itself says is unknown. That is a default-requirement judgment in disguise, which the spec forbids ("no unsupported default 0755 requirement").
- Recommendation: the spec should record the 0555 result as an observation with a named rule, state the expected live verdict change, and not present it as a defect without intent evidence.

### MEDIUM

**F5 — Unresolved or undefined references.**
- "provenance trio" (Matrix spec): undefined in the repo. QUALITY #8 defines `source:`, `verified-at:`, `recheck:`; that is the likely referent but is not stated.
- "ART K2 candidate" (`snapper-eacces-mechanism.md:34`), "ART K4" (`arch-news-gate-2026.md:44`), "ART K3" (`lessons/round-1.md:71`): the ART ledger is not in this repo. Three hits total (`grep -rn 'ART K[0-9]' corpus LOG.md SKILL.md .ufo/waves/round-12`).
- S030 (`SOURCES.md:36`, tier C) points to `/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/fleet-ledger/.ufo/waves/kaika-w1/tsukuroi-art.md`: **MISSING** (`[ -e ]` → absent; `.tower` directory itself exists). S033 (`SOURCES.md:39`) is a tier-C synthesized answer and notes S030 as its equivalent, so the chain of tier-C support does not resolve on this host.
- `mkdir(2)` (Matrix spec): QUALITY #7 requires a `SOURCES.md` S### row. The spec says "ask parent for new ID" — an unresolved dependency; the Matrix cannot cite it until the parent assigns an ID.
- "update-safety gate" (`RULES.md`, contract): RULES says full-system upgrades go through "tsukuroi-shokunin's update-safety gate first." The only matching surface is the census update-safety plane (SKILL.md row ~50), a read-only verdict. PROVINCE says tsukuroi never upgrades. The gate performs no upgrade gating in any written instruction I found.
- QUALITY #10 says sweep "README.md". There is no root `README.md` (`ls README.md` → absent); the file is `corpus/README.md` (lesson M12 cites `corpus/README.md:13`). The sweep scope is ambiguous.
- Stale text: `snapper-eacces-mechanism.md:1` says "access(2) … (opened lead; no S-id assigned in ART)". `SOURCES.md:40` now assigns S034. QUALITY #10 requires superseded text to be swept.
- Census override contract: `tools/tsukuroi-census.sh:286-303` states "every host path read in live mode has an override below." The spec asks for `TSUKUROI_ROOT_DIR` but does not require adding it to that list (lines 296-302). Without that, the header invariant is violated.

**F6 — Negative claim measured with the wrong probe.**
- Evidence: `snapper-eacces-mechanism.md:3, 10` ("no matching `ProtectSystem` … lines") uses `systemctl cat … | grep`, which reads unit-file text only. The effective property is `ProtectSystem=no` (observed `systemctl show`, rc 0). r4 used `systemctl show -p ProtectSystem` (`degraded-triage-r4.md:602`).
- Impact: the note's absence claim is true but measures the file, not the effective default. QUALITY #9 requires the bounded sweep to be the one that answers the claim. Use `systemctl show -p ProtectSystem` for the effective value.

**F7 — README states an [inf] mechanism as fact.**
- Evidence: `corpus/README.md:20` says "`/` 0555 + `CapabilityBoundingSet=CAP_SYS_ADMIN` drops CAP_DAC_OVERRIDE" with no marker. `snapper-eacces-mechanism.md:14` marks it `[inf]`; `corpus/README.md:40` says it "stays [inf] until the operator runs the falsifier".
- Impact: the index overstates the mechanism. QUALITY #3 separates observation from inference; the README line should carry `[inf]`.

### LOW

**F8 — Scope creep in the snapper note.** `snapper-eacces-mechanism.md:15, 36` adds a `/boot` FAT capacity comparison against a mutable-branch S019 recommendation (4 GiB). It states it is "not a cause." It is outside the EACCES mechanism and should be a separate note or dropped.

**F9 — Matrix existing-layout branch cannot be discriminated read-only as written.** `degraded-triage-r4.md:325`: `btrfs subvolume show/list` as non-root → EPERM. The existing-layout discriminator must use `findmnt -t btrfs -n -o TARGET,OPTIONS`, `stat -c '%F %a %n' /.snapshots`, and `snapper list-configs` (the last two are already used in the note). Matrix should avoid `btrfs subvolume list`.

**F10 — Checked and OK (not findings).**
- Superseded D3 claim is handled: `degraded-triage-r4.md:623-627` erratum supersedes lines 321-325 (append-only, QUALITY #4).
- Lesson D3/MC3, D6, M3, M8, M11, M12, M13 anchors resolve (`lessons/round-1.md:21-43`).
- Sibling PROVINCE refs in `PROVINCE.md` exist: `../mori-shokunin/PROVINCE.md` (81 lines; lines 1-18 read and cited topics match), `../kaidoku`, `../kagi`, `../kama`, `../mado`, `../kumitate`, `../revenger`, `../tameshi` (all present). Their content beyond the reviewed range was not re-read.
- Census anchors cited by the spec resolve: `tools/tsukuroi-census.sh:530-570` early returns (PKG_V=BLOCKED), `fx_default` at `:1662`, selftest packages cases at `:1839-1942`.

## 5. Residual risk and verification gaps

- Matrix not visible: C2 unassessed. Re-run this review against `corpus/knowledge/root-dac-decision-r12.{md,json}` once it lands.
- `test -w` implementation path (coreutils) unverified (F3). The Capabilities seat's audit should settle it with a source read of coreutils `test`/gnulib `euidaccess`, not by running a privileged probe.
- Runtime capability state is unobservable read-only while the unit is inactive (F2). Any claim about running-process caps needs the operator-run falsifier or a future active run.
- `sudo` availability asserted by RULES is unverified (no `sudo -n` run, by contract).
- S028 "effective and permitted sets" extension unverified (F3).
- Live verdict change under C1 (F4) is predicted from the spec text, not measured; no census run was made.

## 6. Verification scope (what this file does NOT claim)

- No E2E execution. No census, selftest, or pacman verify was run. No unit was started or restarted. No sudo or systemd-run was used.
- No PASS is asserted for any seat. Operability and depth are reported as the evidence above, not as scores.
