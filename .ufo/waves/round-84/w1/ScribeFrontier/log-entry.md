## Round 84 — hibernate-resume gate and plane (fresh start, 2026-11-06)

**Motivating evidence.** Round-83 non-author closure `corpus/lessons/round-83-verifier-spotcheck.md`
(committed `64f45b79`, 99 lines) and the three rejected closures in the fleet `MANIFEST.json`
`rounds[]` at indices 1276 (round 81), 1297 (round 82) and 1319 (round 83), each `type: closure`,
`lane: tsukuroi`, `ok`. The three failures were procedural or instrumental: round 81 scored candidates
before the freeze, round 82 froze a target its own recipes could not reach, and round 83 froze a battery
that a four-line fixture-path sniff passed in full marks (`.ufo/waves/round-83/w1/CriticClaims.md` F1).
All three were also meta-rounds whose claimed surface was the lane's own instruments. This round returns
to host ground. Before it, no corpus entry had read the hibernate-resume chain:
`git grep -c 'map-swapfile' 64f45b79 -- corpus/knowledge` exits 1 with no output, and the two entries
that had printed the token (`knowledge/journal-boot-plane.md:62`, `knowledge/systemd-user-plane.md:218`)
read `resume_offset=3795013` without asking whether it points at the swap header.

**Freeze before data.** `e0f42051bf9b01af5857c28562ca0247a8fef367` commits the instruments, the pinned
inputs and the candidate-free controls before any candidate file of the round exists (QUALITY 114):
`tools/count-resume-rows-r84.py` sha256 `cb70d4357ebe2d50f360dbbc2079f3a35756a79fc785280cf9d4312268ac8309`,
`tools/resume-gate-battery-r84.py` sha256 `00310ac205f07f396bc4a7a0406f1c0d4baf74c7ab30e27245bbc89d8ce00964`,
`tools/capture-resume-facts-r84.py` sha256 `cec27b9d19e4ac85ccaa513b94e37f568b51979c546133c3d4bc5f62cd6cea23`;
eight upstream snapshots under `.ufo/waves/round-84/before/src/` (eight lines in `SHA256SUMS`, sha256
`5d1673de7f893f035cb2808e9579bcdd292339a32dad605c6e3a53d6561f7eef`) and the read-only host capture
`.ufo/waves/round-84/before/host/{receipt.txt,facts.json}` taken 2026-11-06T15:44:21-03:00
(`SHA256SUMS` sha256 `4ca3e20939eadff71c190f5e2d27a5f453479d0133321ebd118eb7eef624fde6`). The controls
read: gate absent 0/13, blanket HEALTHY 1/13, blanket all-IDs 0/13, committed-base memoriser 0/13
(`.ufo/waves/round-84/before/controls/c2-control-{absent,healthy,allids,basediff}.json`), and the C1
counter selftest `PASS (12 cases, 12 passed, 0 failed)` on three runs (`c1-controls.txt`).

**C2 — hibernate-resume gate (operability, measured).** `c6ee78b2d4184ace3c6d01116190729f0f7c2c31`
authors `tools/check-hibernate-resume.py`, which implements the frozen eight-rule set with eleven finding
IDs and a `--live` path, and prints one JSON object with exit 0 HEALTHY, 1 DEGRADED or 2 CANNOT-EVALUATE.
The counting command is `python3 tools/resume-gate-battery-r84.py --gate tools/check-hibernate-resume.py`;
the battery scores 13 families (POSITIVE, MALFORMED and one per finding ID) on the committed host base and
on five unseeded random bases per run, each case within 20 s, target 13 of 13, kill rule: a timeout,
non-JSON stdout, an extra or missing finding ID or a wrong exit code is a failed case. Operability stays 9:
this is a new runnable arm, not an ordinal move. Measured outcome: `<from ExecBatteryC2 and SCORECARD.md>`.

**C1 — hibernate-resume plane (exploratory, depth, sourced S336–S341).** The candidate commit authors
`corpus/knowledge/hibernate-resume-plane-r84.md` and `.json`: ten rows HR1–HR10 covering the `resume=` and
`resume_offset=` parameters, `btrfs inspect-internal map-swapfile -r` against `filefrag` (3795013 against
3530821 on this host), the NODATACOW requirement, `/proc/swaps` activity, the swap-file recreation trigger,
what `systemd-hibernate-resume` writes to `/sys/power/resume`, the sysfs offset override, the mkinitcpio
`resume` hook at systemd ≥ 255, and `/sys/power/image_size` against free swap. The frozen provenance
counter reads 10/10 with `met` and six distinct snapshots cited, against a declared target of at least 7
rows, no failures and at least 4 distinct snapshots. That reading earns nothing: the same commit's positive
control P1 builds seven boilerplate rows from random snapshot spans and also reads `met`, so the counter is
a shape gate. `69915b8603d9e443f2e1c0021d7c34509186bd9e` withdraws C1 as a measured claim and re-declares it
exploratory before any seat runs; it verifies only as `unprovable-but-better` on a named non-author
reviewer's per-row judgment with reasons (wave seat `ReviewEntry`), otherwise it lands `unprovable`. Depth
stays 8; no ordinal move.

**Sources, lesson and registry.** `corpus/SOURCES.md` gains S336–S342, all status `mined`, opened
2026-11-06, recheck `on-release`; S342 (CPython v3.14.8 `Lib/subprocess.py` raw 397-400) corrects the
round-83 `call()` reject reason, and QUALITY 118 makes that correction a criterion: a reject reason about
code behaviour cites the code at the host's version. `corpus/lessons/round-84.md` carries the Gate table and
three mined mistakes: M1 the docs-only reject reason, M2 three consecutive meta-rounds, M3 a positive
control that needs no domain work and met the target read as a passing selftest case. Registry repairs land
outside the claims: `c6941adb` registers the four round-84 tools and four orphaned round-83 tools in the
operative registry, and `f19e73f3` refines those rows to one tool per row with the code-2 maps (SKILL.md,
3 lines changed). Neither is credited as a claim.

**Wave.** `<from the L1 at landing: seat count, settled seats, durable reports, attack share, residual
call, and any seat that died without a report>`.
