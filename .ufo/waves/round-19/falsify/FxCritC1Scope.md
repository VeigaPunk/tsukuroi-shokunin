## Attack

Test whether C1's outbound count silently implies complete portable coverage of ownership handoffs in `SKILL.md`, beyond the explicitly counted `PROVINCE.md` pointers. I enumerated the latter and separately searched `SKILL.md` for owner-routing language, treating the requested lines 207, 568, 707 and 1504 as craft/method/source pins rather than handoffs.

## Method

- Inspected committed `PROVINCE.md` and `SKILL.md` at `8e5916360f2dfe7bc4eb4ba144081af555900116`; checked the revision resolves.
- Enumerated `PROVINCE.md` pointers with `git show 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md | grep -nE '\.\./[a-z0-9-]+-shokunin/[^ )|]*\.md'`.
- Read the `SKILL.md` pin lines and searched its lane-name, owner/ownership and handoff references; read the counted-scope section and outbound anchor table in `corpus/knowledge/adjacency-anchors-r19.md`.
- Did not run the gate or inspect live sibling state.

## Verdict

**CONFIRM — C1, narrowly as declared.** The scope is explicit and the ten counted `PROVINCE.md` pointers map one-to-one to OUT-001..OUT-010. The finding below does not falsify that bounded count; it does falsify any broader reading that the round-19 anchors cover all ownership handoffs stated in `SKILL.md`.

## Evidence

- The committed scope says outbound means the ten sibling ownership pointers in `PROVINCE.md` (line-range only), and fixes the set to OUT-001..OUT-010: `corpus/knowledge/adjacency-anchors-r19.md:9-19`. Its bounded sweep explicitly says “Scope: `PROVINCE.md` only”: `corpus/knowledge/adjacency-anchors-r19.md:214-218`.
- The committed-pointer search returned exactly these ten locations: `PROVINCE.md:33,46,47,48,49,50` (two), `51` (two), and `52`. They map respectively to OUT-001, OUT-002, OUT-003, OUT-004, OUT-005, OUT-006/OUT-007, OUT-008/OUT-009, and OUT-010 in `corpus/knowledge/adjacency-anchors-r19.md:81-90`. The matching anchor rows are in `PROVINCE.md:121-130`.
- `SKILL.md:173-175` states cross-domain handoffs to kaidoku/revenger, kama, kagi and the owning lane. Its only cited locus is `PROVINCE.md:18`; in the target, line 18 is the “Surface | Boundary | Corpus entry” table header, not that route declaration (`PROVINCE.md:16-28`). This is an ownership-routing statement without a direct sibling declaration anchor in `SKILL.md`.
- A stronger omitted route is `SKILL.md:427-430`: `walker-restart.hook` is routed to “kagi / operator”, but the cited source is the lane's own `corpus/knowledge/update-safety-note.md:471-473`, not a pinned kagi ownership declaration. Other explicit linkage/ABI routes to kaidoku/revenger appear at `SKILL.md:760-761` and `951-952`; the former points to `PROVINCE.md:15-16`, which does not state that route in the target.
- The excluded references are not owner handoffs: `SKILL.md:207` cites kama's skill as a shape model; `:568` cites tameshi's mutation runner; `:707` cites a tameshi plan; `:1504` cites a tameshi ledger. They are craft/method/source pins, not sibling ownership locators.

**Impacted axis:** adjacency (C1) only. This evidence does not bear on C2 depth or C3 calibration.

**Smallest safe correction:** keep C1 explicitly PROVINCE-only (as the current source does). If the intended proposition is repo-wide ownership-handoff coverage, add portable anchors for active `SKILL.md` routes—at minimum the kagi/operator route and the cross-domain routing block—or explicitly disclaim that broader coverage. Do not count the four craft/method/source pins as ownership pointers.

## Residual

I did not independently inspect pinned sibling snapshots or rerun `check-adjacency-anchors.py`; this review establishes the local scope and text-level omission only. The exact completeness of all historical `SKILL.md` routing statements remains untested.

Scope: executed=git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse 8e5916360f2dfe7bc4eb4ba144081af555900116 && git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --short; git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md; git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e5916360f2dfe7bc4eb4ba144081af555900116:SKILL.md; git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md | grep -nE '\.\./[a-z0-9-]+-shokunin/[^ )|]*\.md'