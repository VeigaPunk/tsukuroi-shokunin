# C1Connector — sibling-overlap & held-ground scan (round 71, w1)

Read-only. Lane tree at `0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e` (round-71 declaration;
`git rev-parse HEAD` printed it). No lane-tree write, no git/jj mutation, no scratch retained.

## Verdict

1. **Ownership: the kernel module-parameter surface is tsukuroi's.** No sibling claims it and
   one cedes it explicitly. tsukuroi `PROVINCE.md:8-13` owns the "driver/firmware plane (kernel
   modules, nvidia driver + GSP firmware presence, `nvidia-smi` shape)"; mori
   (`../mori-shokunin/PROVINCE.md:12-15`) refuses "OS package, systemd unit, driver/firmware and
   boot state (→ tsukuroi)". kama's boundary is the endpoint question only
   (`../kama-shokunin/PROVINCE.md:42-45`); revenger and kaidoku own RE of *shipped artifacts*
   (`../revenger-shokunin/PROVINCE.md:3-6`, `../kaidoku-shokunin/PROVINCE.md:3-6`), and the four
   C1 snapshots are published upstream source at tag `v7.2.11` — the same evidence class as the
   lane's S208–S212 (pacman source) and S290–S293 (xfs source). tameshi refuses product domains
   (`../tameshi-shokunin/PROVINCE.md:14-17`), so C2's census change needs no handoff.
   Full quote table and component-by-component mapping: `probes/C1Connector/overlap.md` §1.

2. **Two boundary tensions are live and must be respected, not smoothed.**
   - `PROVINCE.md:25-27` refuses "binary RE of drivers (→ kaidoku/revenger — tsukuroi tracks
     *state and health*, not internals)". C1 reads *source* for the plane's contract. That is not
     the refused class, but the note must not state nvidia-internal `NVreg_*` semantics; only the
     generic kernel contract and the observed `perm` values.
   - `ADJ-06` (`PROVINCE.md:49`) routes "driver/firmware/package mechanism requires
     shipped-artifact reverse engineering" to kaidoku/revenger. C1's question needs no shipped-
     artifact RE, so ADJ-06 does not fire. Driver-internal NVreg semantics would be ADJ-06 work.
   - False friend: `../kengaku-shokunin/PROVINCE.md:14` matches "cmdline" but pins
     `/proc/1299/cmdline` (process argv), not the kernel boot cmdline. Do not count it as a
     sibling claim or as a novelty counterexample.

3. **Held ground holds.** At the declaration revision, `modprobe.d`, `kernel-parameters`,
   `module_blacklist`, `NVreg`, `module_param`, `kernel_param_ops`, `param_attr_store` each read
   **0** file hits across `corpus/ SKILL.md PROVINCE.md` — every declaration figure reproduced, no
   counterexample. Fleet-wide cross-check: 0 matches for those terms across all 21 sibling
   `PROVINCE.md`, and 0 for `module_blacklist|kernel_param_ops|param_attr_store|/sys/module/<name>/parameters`
   across sibling corpora. The surface is unheld fleet-wide.

4. **D1 recurrence: 3 files, 5 stale figure tokens, all r70.** Final receipt figure is
   **214 cases, 214 passed, 0 failed**, with **18** `R70-C2` case lines (all 18 are PASS lines):
   `.ufo/waves/round-70/after/selftest-after.txt:217`, corroborated at
   `.ufo/waves/round-70/after/gates-at-40c35ee7.txt:26` and `SCORECARD.md:5344`.

   | Site | Stated | Correct |
   |---|---|---|
   | `PROVINCE.md:372` | "212 cases, 16 labelled `R70-C2`" | 214 cases, 18 labelled |
   | `corpus/README.md:613` | "selftest 196 -> 212" | 196 -> 214 |
   | `SKILL.md:5773-5774` | "196 → 212 cases, 16 of them labelled `R70-C2`" | 196 → 214, 18 labelled |

5. **Four false positives a naive sweep will hit — do not "correct" them.** `corpus/lessons/round-70.md:141`
   ("212/214 pre-repair, 214/214 post-repair") is the correct pre/post-repair history;
   `PROVINCE.md:293` (r44 "148 cases, sixteen labelled (R44-C1)") and `PROVINCE.md:329` (r53 Windows
   host "40 of 168 cases in 90 s and in 420 s, rc 124") are correct at their own revisions;
   `corpus/README.md:600` (r69 "selftest 177 → 192 cases") is correct at r69. The sweep must compare
   against the *round-70 final* receipt only, and must not rewrite historical rows.

6. **Residual risks.** S297–S300 must be free above the 296-row base registry; `modprobe.d` may be
   cited as paths and modes only (contents were never read — secrets stay shape-only, `PROVINCE.md:25`).

Evidence tables: `probes/C1Connector/overlap.md`, `probes/C1Connector/recurrence.tsv`.

KEY=VALUE: SIBLING_OWNERS=0 NOVELTY_COUNTEREXAMPLES=0 STALE_SITES=3
