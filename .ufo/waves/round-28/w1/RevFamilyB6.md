# RevFamilyB6 — rule B6 mutants at f8e3a8f

Verdict: holds. Both B6-family mutants (six-lane-gap, lanegap-class-with-lane-side) are refused by
rule B6 itself; sandboxed variants that strip the incidental `province-disagrees` (B7) reason are
still refused by B6 reasons alone.

## Evidence

Rule under attack (docstring, counter blob sha256 `450b020b0bae5e1f43e77303f4e726f6c3a7e15e5d7e9b34b9d9a21bc0faf25e`):
"B6 LANE-GAP needs a null lane side; at most one LANE-GAP row counts"
(`tools/check-adjacency-overlap.py` at f8e3a8f2, docstring lines ~30-31; enforced at lines
`if klass == 'LANE-GAP': lane_gap_rows += 1` → `lane-gap-over-cap`, and
`elif ... if klass == 'LANE-GAP': reasons.append('lane-gap-with-lane-side')`).

Battery command (from a read-only export, sandbox kept with `--keep`):
`python3 tools/mutants-adjacency-overlap.py --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
 --base f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 --counter-rev f8e3a8f2960b26ba5027d2298e50d5c9d6564cc0 --keep`
Summary line: `should_fail_accepted` 0 of 24, `accepted_mutants` [],
`control_live_anchored_rows` 6, `control_live_exit` 0. Declared C1 values hold.

1. six-lane-gap — refused by B6 itself, not only incidentally.
   Per-row `failing` (live-mori run, identical under no-sibling): OV1 `["province-disagrees"]`;
   OV2–OV5 `["lane-gap-over-cap", "province-disagrees"]`; OV6 `["lane-gap-over-cap"]`.
   `lane-gap-over-cap` is the B6 at-most-one-LANE-GAP cap on five rows; `province-disagrees`
   is the incidental B7 hit (PROVINCE class cells still read the original classes).

2. lanegap-class-with-lane-side — refused by B6 itself, not only incidentally.
   `failing`: OV3 `["lane-gap-with-lane-side", "province-disagrees"]`,
   OV6 `["lane-gap-over-cap"]`. Both are B6 reasons (clause 1: LANE-GAP with a non-null lane
   side; clause 2: OV6 becomes the second LANE-GAP row); `province-disagrees` on OV3 is B7 incidental.

3. Variant A (B6 alone on six-lane-gap) — still refused.
   Sandbox `/fast/scratch/hyaku/tsuku28/RevFamilyB6/variant-a` (copy of kept sandbox
   `/tmp/mut-adj-uofj0w9d`), commit `45991bcf86005de7e2689cb7e48f340c1d986638`: same mutant plus
   all six PROVINCE class cells changed to `LANE-GAP` so B7 agrees.
   `python3 .../variant-a/counter/check-adjacency-overlap.py --repo .../variant-a/sbx --revision HEAD
   --siblings-root /home/vgpnk/Projects/shokunin` → exit 1, `anchored_rows` 1, `rows`:
   OV1 `[]`; OV2–OV6 `["lane-gap-over-cap"]` only. No non-B6 reason remains. B6 alone refuses. [obs]

4. Variant B (B6 alone on lanegap-class-with-lane-side) — still refused.
   Sandbox `/fast/scratch/hyaku/tsuku28/RevFamilyB6/variant-b`, commit
   `a18b9fbf2aeb44cfcf7d0d1d7502e1193a7deeee`: same mutant plus PROVINCE OV3 class cell set to
   `LANE-GAP`. Counter run → exit 1, `anchored_rows` 4, `rows`: OV3 `["lane-gap-with-lane-side"]`,
   OV6 `["lane-gap-over-cap"]`, all others `[]`. Both remaining reasons are B6. B6 alone refuses. [obs]

5. Note [obs]: neither original mutant relies solely on an incidental rule; each already carries a
   B6 reason. The variants were built anyway to confirm B6 self-sufficiency — they show refusals
   with a strictly B6-only reason set, so an attacker stripping the B7 surface still loses.

6. Note [unk]: `lane-gap-over-cap` fires on the second and later LANE-GAP rows in register order,
   so which rows report it depends on row order; the cap logic itself is order-dependent only in
   reporting, not in refusal (any ≥2 LANE-GAP rows refuse). No defect.

Report: .ufo/waves/round-28/w1/RevFamilyB6.md
Scope: read=SCORECARD round-28 declaration, check-adjacency-overlap.py, mutants-adjacency-overlap.py, register JSON, PROVINCE.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-28/w1/RevFamilyB6.md, sandboxes under /fast/scratch/hyaku/tsuku28/RevFamilyB6/ (variant-a, variant-b, tree export); executed=battery with --keep, two counter runs on variant commits
Model: devin/swe-2
Installs: none
