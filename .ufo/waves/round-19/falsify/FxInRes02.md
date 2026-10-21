## Attack

Re-verified the ten RESOLVES records IN-016..IN-025 at lane revision `8e5916360f2dfe7bc4eb4ba144081af555900116`. The attack tests whether each stored quote occurs at its recorded `found_line`, that line lies in `target_ranges`, the pinned sibling line still cites and relies on the lane evidence, and `relied_on` fairly summarizes that evidence.

## Method

- Read the target files from the exact lane revision using `git show <revision>:<target_path>` and read each sibling file at the census-pinned commit using `git -C <sibling-repo> show <sibling_commit>:<sibling_path>`. Compared quote, found line, ranges, sibling line, and `relied_on` for every assigned ID. Also compared the pinned sibling-file blob to the file at sibling `HEAD`.
- Ran `timeout 600 python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116` and `timeout 600 python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116 --registry-from 8e5916360f2dfe7bc4eb4ba144081af555900116`. Both exited 0 and returned `status: PASS`, no findings; counts were RESOLVES 97 / DRIFTED 17 / UNRESOLVABLE 0, with 25 operative / 89 historical.
- The gate result was supplementary: the record-by-record sibling-line checks below were performed separately against pinned sibling commits.

## Verdict

**CONFIRM — C1 adjacency, assigned batch IN-016..IN-025 (10/10).** Each quote is present at the recorded line, every `found_line` is in its recorded target range, and each pinned sibling line still makes the recorded reliance. No REFUTE found.

| ID | Lane evidence: quote at `found_line` (range) | Pinned sibling evidence and reliance check |
|---|---|---|
| IN-016 | `corpus/QUALITY.md:13` (13–13): bounded search/probe sweep requirement; exact quote at 13. | `kama-shokunin` `e75cf680b53484a61709ee1b2787d8dbc6419f74:.ufo/waves/round-17/falsify/advice/ConnectTsukuroi.md:42`; its QUALITY criterion citation supports the recorded paraphrase about bounded sweep command, scope, and date. |
| IN-017 | `PROVINCE.md:27` (27–28): refusal to install, upgrade, or remove packages; exact quote at 27. | `kama-shokunin` `e75cf680b53484a61709ee1b2787d8dbc6419f74:.ufo/waves/round-17/falsify/advice/ConnectTsukuroi.md:50`; line states tsukuroi is not a repair/removal recipient and cites this refusal. |
| IN-018 | `SKILL.md:144` (144–155): “never installs, upgrades, removes, or restarts”; exact quote at 144. | Same pinned kama line 50 cites `SKILL.md:144-155` as reinforcing the diagnostic product/read-only verbs; recorded paraphrase is fair. |
| IN-019 | `PROVINCE.md:8` (8–14): “Owns (surfaces, all read-only probes):”; exact quote at 8. The additional cited boundary text is at `PROVINCE.md:38-42`. | `kama-shokunin` `e75cf680b53484a61709ee1b2787d8dbc6419f74:.ufo/waves/round-17/falsify/advice/ConnectTsukuroi.md:51`; line cites the owned pacman/systemd/driver/update-safety surfaces and the no-repair/unresolved-owner boundary. This supports the recorded scope paraphrase. |
| IN-020 | `PROVINCE.md:66` (65–68): “Acknowledgement is not acceptance; resolution”; exact quote begins at 66 and continues on 67. | `kama-shokunin` `e75cf680b53484a61709ee1b2787d8dbc6419f74:.ufo/waves/round-17/falsify/advice/ConnectTsukuroi.md:59`; line quotes the closure rule and its owner-side evidence requirement. |
| IN-021 | `.ufo/l0-questions.md:1` (1–2): “Only operator/global-routing authority can provide these bindings.”; exact quote at 1. The two lane-local entries occupy the cited range. | `kotoba-shokunin` `c61a973b2e02e1ded169703ddcb06466f4edd8bd:.ufo/round-22/scouts/A6.md:47`; line identifies the tsukuroi lane-local L0 entries as unmirrored questions. The fleet L0 file has no `ROUTE-BINDING` or `RECEIPT-BINDING` hits, consistent with the recorded paraphrase. |
| IN-022 | `PROVINCE.md:3` (3–19): “host operability & system repair”; exact quoted phrase is at 3. | `lore-shokunin` `01306d51252f837909af5252c398ee4e31259f9b:.ufo/waves/round-87/K1.md:28`; line rejects tsukuroi for world-bible records based on its host-operability/system-repair domain. |
| IN-023 | `SKILL.md:755` (755–755): walker version-crossing quote; exact quote at 755. Other cited lines in the same target ranges contain `omarchy-walker` at 101 and `walker-restart.hook` at 404 and 842. | `mado-shokunin` `a4046a8216080d4004de3f268c62cf142095ac07:.ufo/evidence/round-12/l2-connector.md:13`; the row cites all four lines and identifies Walker packaging/hooks. `relied_on` fairly summarizes the cited package/version/hook evidence. |
| IN-024 | `SKILL.md:1707` (1705–1715): exact eight-column gate-registry header at 1707. | `mado-shokunin` `a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-13/w1/RegistryDraft.md:57`; line cites this registry as an eight-column row-shape precedent. The R18 current-use supersession note is at `SKILL.md:1952-1954`, separate from the historical row-shape evidence. |
| IN-025 | `SKILL.md:1705` (1705–1705): exact `### Gate registry` heading at 1705. | `mado-shokunin` `a4046a8216080d4004de3f268c62cf142095ac07:.ufo/waves/round-13/w1/ReviewRegistry.md:15`; line cites the committed heading as a format precedent, matching `relied_on`. |

All ten sibling commits resolve to commits, and their cited sibling-file blobs match the files at the sibling repos' current HEAD. The target quote for IN-024 also occurs in later registry tables, but its recorded occurrence at line 1707 is exact and inside the cited range.

## Residual

The census `sibling_line_text` field truncates lines longer than 600 characters; IN-019 is one such row. I verified the full sibling line directly at its pinned commit, and it still makes the recorded reliance. This did not change any assigned verdict. The attack covers only IN-016..IN-025; it does not re-evaluate other adjacency records or the broader truth of unrelated sibling assertions.

Scope: executed=timeout 600 python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; timeout 600 python3 tools/check-adjacency-anchors.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116 --registry-from 8e5916360f2dfe7bc4eb4ba144081af555900116