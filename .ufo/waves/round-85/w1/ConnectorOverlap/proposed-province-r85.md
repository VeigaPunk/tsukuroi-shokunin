# Proposed patch — PROVINCE.md append-only section (r85, ConnectorOverlap)

Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md`, **append at end of file**
(currently 573 lines; last section `## Round 76` at PROVINCE.md:555). Do **not** touch the
`## Adjacent — finding-to-owner handoffs` table: `check-adjacency-table-r49/r50/r51` require
exactly `ADJ-01..ADJ-07` and an eighth row inside that table fails all three.
Measured at lane master `479d868b2fc8969a19a617cd55ced5c13edd84b6`.

Inert-verified in a `clone --shared` (base `f2797a3b20ceae`, base+row `0478fdb624ac`):
`adj_rows 7` before and after, `adj_exact 1` before and after, `bare_all 0` before and after,
`anchor_rows_exact 1` before and after; `check-adjacency-anchors.py` identical (CANNOT_EVALUATE,
1 finding) at both. See report §6.

---

## Round 85 — hibernation availability enters the province (HA1-HA8)

Append-only. The `## Adjacent — finding-to-owner handoffs` table (ADJ-01..ADJ-07) and the
`## Adjacent — portable ownership anchors (round 19)` table are unchanged; the three rows below
are new and live in this section because the frozen counters of rounds 49-51 predicate on exactly
seven rows in that table.

The surface is the precondition the round-84 resume chain never read: `hibernation_available()`
(`nohibernate == 0 && !security_locked_down(LOCKDOWN_HIBERNATION) && !secretmem_active() &&
!cxl_mem_active()`) and the `nohibernate` / `noresume` / `hibernate=` cmdline parse, read by
`corpus/knowledge/hibernation-availability-r85.md` and reported by the `hibernate-resume` arm
(`SKILL.md:5917`, findings HR-HIBERNATE-DISABLED, HR-LOCKDOWN-BLOCKS, HR-NORESUME-ARG). The
episode half stays where it already is (`corpus/knowledge/journal-boot-plane.md:251-252,402`).
Detection and report only: nothing here authorizes a suspend/hibernate, a `lockdown=` or cmdline
change, a sysctl write or a swap operation.

Three limits travel with these rows. (1) The gate's `HEALTHY` covers the three modeled availability
rules; it reads neither `secretmem_active()` nor `cxl_mem_active()`, and `CONFIG_SECRETMEM=y` on this
host makes the first one live. The whole conjunction has a kernel-side witness the entry already names
(`/sys/power/disk` prints `[disabled]` from `hibernate.c:1168-1169`), and on 2026-11-06 it read
`[platform] shutdown reboot suspend test_resume` — available, so the gate is corroborated here, and
blind rather than wrong. (2) The lockdown string `[none]` was captured 2026-11-06 and answers
`kernel-taint-r27.md` KT3's "lockdown state was not captured" for that capture only, not
retroactively. (3) The sibling quotes below are at the revisions named and carry no blob-sha pin;
re-read the live declaration before any later handoff.

| ID | Finding / boundary trigger | Tsukuroi retains | Next analysis recipient | Minimum handoff evidence | Ownership source |
|---|---|---|---|---|---|
| ADJ-08 | A working-state, idle or uptime figure must be split by sleep/hibernation, or an episode must be confirmed or denied | HA1-HA8 availability facts and the `hibernate-resume` gate findings; the journal episode sweep at `corpus/knowledge/journal-boot-plane.md:251-252,402` | mori | Capture time, the exact counter command/exit and value, and the journal sweep command/exit with its match count; no claim that a counter delta is an episode | mori declaration, `../mori-shokunin/corpus/knowledge/workstate-win-r71.md:64-66` @ `7765969c79e6` ("diagnosing sleep/hibernation or boot state ... are tsukuroi/operator ground") and `uptime-win-r70.md:40-43` @ `7765969c79e6` ("no sleep/hibernation split ... stay unmeasured here"); `../mori-shokunin/PROVINCE.md:13` |
| ADJ-09 | A signed-module load refusal or a hibernation refusal is attributed to kernel lockdown | The live `/sys/kernel/security/lockdown` selection and the `enum lockdown_reason` ordering (`LOCKDOWN_MODULE_SIGNATURE`=1, `LOCKDOWN_HIBERNATION`=5, both < `LOCKDOWN_INTEGRITY_MAX`); one measurement decides both reasons | revenger (ADJ-06 route) for artifact-side signature acceptability | Capture time and the exact sysfs text; kernel tag; the artifact path/digest if one is named. No statement about the artifact's signature from the host mode | `OUT-008`, `OUT-009`; revenger `corpus/knowledge/round-73-re-resource-atlas.md:278` @ `654d09298960` ("acceptance policy depends on kernel config (lockdown, sig_enforce), not on the file") |
| ADJ-10 | A gate returns HEALTHY over a rule set narrower than the predicate it names, while the lane's own entry names a host witness the gate does not read (`/sys/power/disk` `[disabled]`) | The gate, its rule set and the measured host facts (`CONFIG_SECRETMEM=y`; no `/sys/bus/cxl`, no `/dev/cxl`; witness not `[disabled]`) | tameshi (ADJ-07 route) — method advice only, not gate ownership | The gate docstring's rule list with its line numbers, the source predicate and witness ranges, and the measured values; no behavior change proposed | `OUT-010` |

---

## Separate one-field patch — adjacency register IN-109 (pre-existing red)

Not part of the append above; `check-adjacency-anchors.py --revision 479d868b` returns
`status: FAIL` with `INBOUND-CLASSIFICATION-WRONG` at
`corpus/knowledge/adjacency-anchors-r19.json:inbound[108]`. The record's `found_line: 2822` no
longer holds its `evidence_quote`; the quote now sits at `tools/tsukuroi-census.sh:3214`
(`grep -n "kernel ring class counts are evidence" tools/tsukuroi-census.sh` → `3214:`).

Patch: set `inbound[108].found_line` to `3214`, append to `inbound[108].note`:
"Round 85 (ConnectorOverlap): census growth moved the case 2822 -> 3214; quote re-located at
479d868." Do not rewrite the earlier note text; `target_ranges` and `classification` are unchanged.
