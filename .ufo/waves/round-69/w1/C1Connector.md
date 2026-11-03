2026-11-03T23:22:17Z

# Seat C1Connector — report (round 69, w1)

Assignment: sibling-overlap and duplication scan for C1 (depth, kernel taint/vermagic note)
and C2 (operability, kernel-arm census line). Read-only; no tracked file, no sibling repo,
no scratch left behind. Full evidence, quotes and commands:
`.ufo/waves/round-69/probes/C1Connector/overlap.md`.

```
C1_SIBLINGS=20 C1_OWNED=0 C1_CONTESTED=0 C1_LANE_DUP=19
C1_BOUNDARY_RISK=B1-vermagic-loader-inference,B2-pending-token-collision,B3-pending-as-remediation,B4-taint-bits-past-19
```

## Findings

1. **No sibling claims any of the five surfaces.** `git -C <sib> grep -n -i … HEAD --
   PROVINCE.md` returns no match for `taint|tainted|/proc/sys/kernel|vermagic|module tree|
   modules_tree|kernel release|uname -r|reboot pending` in all 20 siblings. Near misses are
   adjacent, not owned: mori `PROVINCE.md:24,44` (kernel **OOM event** records and FR1
   event-time attribution), kaidoku `:32-34,132` (REA artifact "module identity"; nvidia GSP
   blob regions), revenger `:10` (`corpus/training/bounty-triage/MODULE.md`). kama, souji and
   tameshi contain no kernel/module line at all. One regex false positive, disclosed: kasegi
   `:205` matched `taint` inside "certainty". No handoff row is needed for this round's claims.

2. **The lane owns all five surfaces, but `PROVINCE.md` never says so.** `grep -c -i` gives
   taint 0, vermagic 0, reboot 0, uname 0; the only kernel claim is `PROVINCE.md:12-13`
   ("driver/firmware plane (kernel modules, nvidia driver + GSP firmware presence, nvidia-smi
   shape)"). The taint plane is registered in `SKILL.md:2422` (KT1-KT6) and
   `corpus/knowledge/kernel-taint-r27.md`, not in PROVINCE — an append-only registration gap.

3. **19 duplication loci in 15 lane files** (counting rule: one `file:line` asserting a
   surface with a host reading or mechanism; lessons/tools/SCORECARD excluded). Most load-bearing:
   `kernel-taint-r27.md:19` (KT1 decodes 12288 = bits 12+13; the r69 KR rows are deeper ground
   over the same bytes, and QUALITY 68 wording applies), `driver-firmware-plane.md:85`
   (vermagic 7.2.3, stale), `driver-firmware-plane.md:278` and `boot-chain-r17.md:92` (two module
   trees — identical to `before/host.txt`), and two **stale contradictions**:
   `update-safety-note.md:296-298` ("`ls /usr/lib/modules/` = `7.2.3-arch1-3` only; `uname -r` =
   `7.2.3-arch1-3` ⇒ no kernel reboot is pending today", no in-file correction) and
   `host-health-report-r3.md:320` ("`uname -r` = `pacman -Q linux` = `7.2.3` → no reboot
   pending today"). C2's `pending=` reproduces exactly that derivation; at 7.2.11/two trees it
   supersedes both by measurement, and neither may be cited as the current basis.
   `host-drift-recheck-r64.md:36,38` still cites the one-tree listing in a round-64 row.

4. **S288 is a re-pin of S140, not new authority.** `sha256sum` gives
   `727ddb82bc042e4c5777592128bc8ca0dd640376af515efa8cba2dff5f9a0841` for both
   `.ufo/waves/round-69/before/src/tk-v7211.rst` and `.ufo/waves/round-27/sources/S140.rst`;
   `cmp -s` rc 0. `corpus/SOURCES.md:146` registers that digest for S140 (v7.2 URL), and
   `SCORECARD.md:5196` declares the same hex for S288 (v7.2.11 URL). Registry convention for a
   re-pin is a supersede cell inside the teaches column — S280 `supersedes S021 — re-pin: …`,
   S281 `supersedes S022 — re-pin: …` (`SOURCES.md:290-291`), earlier S104/S109/S199. Without
   `supersedes S140 — re-pin: …` the S288 row is a second unlinked registration of identical
   bytes. **S289 (`include/linux/vermagic.h`) has no prior row** (`grep -i vermagic
   corpus/SOURCES.md` → no output) and is genuinely new source ground.

5. **Boundary risks** (each against a named line): B1, a KR row concluding loader
   compatibility from the vermagic string or reading `.modinfo` from the `.ko` crosses
   `PROVINCE.md:26-28` + ADJ-06 (`:46`, "no binary-internals inference"); B2, C2's `pending=`
   collides token-for-token with `PLANE update-safety: … pending=` (`tools/tsukuroi-census.sh:1904`);
   B3, `pending=YES`/`detail=` must stay state, not an instruction to reboot
   (`PROVINCE.md:30-32`); B4, `taint_bits` decoded only against the closed 0–19 table
   (`before/src/tk-v7211.rst:189` ends at `19) ``J```) must read UNKNOWN or name the out-of-table bit
   rather than drop it. Read-side `pacman -Q linux` and the upstream source reads are within
   the declared surfaces.

## Defect in the seat spec (not a blocker)

The spec's base string `acce353bacad74043636018d829e9e9b8e0fdf1c9` is 41 hex characters;
`git cat-file` → `fatal: Not a valid object name …`, rc 128. The real revision is the 40-hex
`acce353bacad74043636018d829e9e9b8e0fdf1c` (`git rev-parse acce353b`, rc 0; subject "round-68
verifier spot-check (integrator, hyaku): non-author admit/reject"), and
`git merge-base --is-ancestor acce353b 920a9ee` rc 0. No seat should report the base unreachable.

## Commands run (all read-only)

`rev-parse HEAD`, `cat-file -t/-e`, `log -1`, `merge-base --is-ancestor`, sibling
`rev-parse HEAD`, sibling-and-lane `grep -n` (working tree and `git grep` at
`920a9eea3c5c5400567be0e96141014f338973df`), `sha256sum`, `cmp -s`, `sed -n` ranges,
`grep -c`. No git mutation, no pacman, no privilege, no install, no network.
