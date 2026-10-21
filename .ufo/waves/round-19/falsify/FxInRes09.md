## Attack

Re-verified the ten requested `RESOLVES` inbound anchors against lane revision `8e5916360f2dfe7bc4eb4ba144081af555900116`: quote placement, recorded range, pinned sibling reliance, and whether the recorded paraphrase remains supported. The falsifiable point was whether any sibling reliance overstates or contradicts the cited lane evidence.

## Method

- Loaded the requested IDs from `corpus/knowledge/adjacency-anchors-r19.json` and resolved their sibling commit pins and `sibling_line_text` in `.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json` with read-only Python JSON inspection.
- For each record, read the lane target using `git show 8e5916360f2dfe7bc4eb4ba144081af555900116:<target_path>` and checked the 1-based `found_line`, exact quote inclusion, and membership in `target_ranges`.
- Read each sibling source using `git -C <sibling-repo> show <pinned-commit>:<sibling_path>`, then compared the pinned line to the census line text. Both pinned commits resolve; all selected sibling lines remain unchanged at those sibling repositories' HEADs.
- For IN-096, checked the cited round-5 draft in the attacked revision and traced the exact census-tool blob through Git history using `git log --all --format=%H -- tools/tsukuroi-census.sh`, `git merge-base --is-ancestor`, and `git show <commit>:tools/tsukuroi-census.sh | sha256sum` / `wc -l`.
- No gate, host probe, or host action was run.

## Verdict

- **IN-092 — CONFIRM.** Quote is at `PROVINCE.md:8`, within `8-14`; sibling line 29 still cites that ownership range and separately cites `:27` for the no-install clause. The paraphrase is supported by the lane text.
- **IN-093 — CONFIRM.** Quote is at `PROVINCE.md:27`, within `8-14,27`; sibling line 71 still makes the same package-state/no-package-action and report-to-L1 reliance. The paraphrase is fair to the lane text.
- **IN-094 — CONFIRM.** Quote is at `plans/round-5.plan.md:3`, within `3-11`; sibling line 77 still identifies the round-5 plan as the self-service election. The plan's own-gate application supports the paraphrase.
- **IN-095 — CONFIRM.** Quote is at `plans/round-5.plan.md:4`, within `3-11`; sibling line 192 still treats the plan as a historical self-service reference. The paraphrase is fair.
- **IN-096 — REFUTE.** Quote is at `plans/round-5-record-draft.md:445`, within `445`, and sibling line 78 still says the `aae45531` revision was “never committed.” That unqualified reliance is false: the exact `aae45531…` census-tool blob is committed at `da952909584bcad9c643e842c41d6025d732fb56`, an ancestor of the attacked revision, before the sibling's pinned commit on 2026-10-20. The draft records an earlier worktree state, not that the bytes were never committed.
- **IN-098 — CONFIRM.** Quote is at `plans/round-5.plan.md:4`, within `3-11`; sibling line 44 still relies on the lane's own-gate/read-only/temp-copy/kill-rate plan. The paraphrase is fair.
- **IN-099 — CONFIRM.** Quote is at `SKILL.md:569`, within `568-570`; sibling line 106 still identifies the r4-2 md5/sha256 pin as a historical record. The paraphrase is fair.
- **IN-100 — CONFIRM.** Quote is at `SKILL.md:568`, within `565-570`; sibling line 82 still records the r4-2 md5/sha256 pin and runner-method reliance. The paraphrase is fair.
- **IN-101 — CONFIRM.** Quote is at `tools/_revision.py:62`, within `62-72`; sibling line 44 still identifies the prefix-dropping helper as the canonical helper to port. The implementation at the attacked revision retains that `GIT_*` environment filter.
- **IN-103 — CONFIRM.** Quote is at `plans/round-5.plan.md:5`, within `3-9`; sibling line 304 still says the plan schedules its measurement as the third data point. The cited claim describes the lane measuring its own kill-rate; explicit `Measure:` wording is at line 11, outside the range, but the in-range claim fairly supports the paraphrase.

## Evidence

All target quotes were present on the recorded `found_line`; every `found_line` was inside its recorded range:

| ID | Lane target at attacked revision | Range | Pinned sibling line |
|---|---|---:|---|
| IN-092 | `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:8` | 8-14 | `c0aff2364b49b21c41669f050e03800138589fa7:.ufo/waves/round-16/drafts/DraftAdjacency.md:29` |
| IN-093 | `8e5916360f2dfe7bc4eb4ba144081af555900116:PROVINCE.md:27` | 8-14, 27 | `c0aff2364b49b21c41669f050e03800138589fa7:.ufo/waves/round-16/w1/ConnSiblings.md:71` |
| IN-094 | `8e5916360f2dfe7bc4eb4ba144081af555900116:plans/round-5.plan.md:3` | 3-11 | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1:.ufo/waves/round-14/w1/FreshnessIntake.md:77` |
| IN-095 | `8e5916360f2dfe7bc4eb4ba144081af555900116:plans/round-5.plan.md:4` | 3-11 | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1:.ufo/waves/round-14/w1/FreshnessIntake.md:192` |
| IN-096 | `8e5916360f2dfe7bc4eb4ba144081af555900116:plans/round-5-record-draft.md:445` | 445 | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1:.ufo/waves/round-16/w1/CR13.md:78` |
| IN-098 | `8e5916360f2dfe7bc4eb4ba144081af555900116:plans/round-5.plan.md:4` | 3-11 | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1:.ufo/waves/round-16/w2/ProvinceAppend.md:44` |
| IN-099 | `8e5916360f2dfe7bc4eb4ba144081af555900116:SKILL.md:569` | 568-570 | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1:.ufo/waves/round-16/w2/RunnerDiff.md:106` |
| IN-100 | `8e5916360f2dfe7bc4eb4ba144081af555900116:SKILL.md:568` | 565-570 | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1:.ufo/waves/round-17/w2/SiblingImpact.md:82` |
| IN-101 | `8e5916360f2dfe7bc4eb4ba144081af555900116:tools/_revision.py:62` | 62-72 | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1:.ufo/waves/round-18/w1/C04GitEnvPriorArt.md:44` |
| IN-103 | `8e5916360f2dfe7bc4eb4ba144081af555900116:plans/round-5.plan.md:5` | 3-9 | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1:corpus/knowledge/fleet-suite-census.md:304` |

Specific falsification evidence for IN-096:

- `8e5916360f2dfe7bc4eb4ba144081af555900116:plans/round-5-record-draft.md:438-446` records the earlier 26-to-35-case worktree state, and line 445 gives the `aae45531…` worktree SHA.
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show da952909584bcad9c643e842c41d6025d732fb56:tools/tsukuroi-census.sh | sha256sum` produced `aae45531fc393579b9e575683eaca0e7f337004c19713eb9a6a213e961207df6  -`; the same command piped to `wc -l` produced `1032`.
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show da952909584bcad9c643e842c41d6025d732fb56^:tools/tsukuroi-census.sh | sha256sum` produced `084951be50bcbfee5e3f22de3c270d87131550ea1ce8264a557a34c5809c78c5  -`; `wc -l` produced `976`.
- `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin merge-base --is-ancestor da952909584bcad9c643e842c41d6025d732fb56 8e5916360f2dfe7bc4eb4ba144081af555900116` succeeded. The commit timestamp is `2026-10-14T14:33:30-03:00`; the sibling pin is `2026-10-20T17:24:26-03:00`.

## Residual

The attack confirms quote/range placement and pinned sibling-line preservation for all ten records. IN-096's sibling statement is historically understandable as a description of the earlier worktree capture, but its stronger “never committed” wording is falsified by the later committed exact blob. No unrelated sibling claims or host state were investigated.

Scope: executed=read-only Python Eval JSON/line checks; `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --all --format=%H -- tools/tsukuroi-census.sh`; `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin merge-base --is-ancestor da952909584bcad9c643e842c41d6025d732fb56 8e5916360f2dfe7bc4eb4ba144081af555900116`; `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show da952909584bcad9c643e842c41d6025d732fb56:tools/tsukuroi-census.sh | sha256sum`; same exact `git show` piped to `wc -l`; `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show da952909584bcad9c643e842c41d6025d732fb56^:tools/tsukuroi-census.sh | sha256sum`; same parent `git show` piped to `wc -l`; `git -C /home/vgpnk/Projects/shokunin/tameshi-shokunin show -s --format=%H%n%ad%n%s --date=iso-strict 01d586ddbc5fcd78659557c4e93a6ee8517b87d1`