# C3 duplicate highest-heading/map review
**Impacted axis:** C3 calibration (`audit_live_map_errors`).


## Finding

The candidate fails closed for duplicate **exact-form** highest registry headings and duplicate `boot-chain-audit` rows in the parsed operative table; it does not select first/last. No code defect found on those canonical duplicate shapes.

- Two exact headings with the same greatest round number cause `_operative_rows` to raise `TableError("round{highest} heading is duplicated")` (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:137-150`). This happens before the C3 map audit (`:348-355`). The exact expected result is exit **2**, `status: CANNOT_EVALUATE`, one `E-REGISTRY-TABLE` finding at `SKILL.md` with detail `roundN heading is duplicated`; `audit_live_map_errors` is **absent**, not zero or one. `main` maps `TableError` to that finding and code (`:363-368`), `_emit` names code 2 `CANNOT_EVALUATE` (`:297-303`), and only the successful parse path adds the C3 count (`:348-355`). The canonical ambiguity rule is also stated in `SKILL.md:1997-1999` and preregistration scopes C3 to the highest operative map (`.ufo/waves/round-20/preregister.json:21-27`).
- With one unique highest heading but two parsed rows named `boot-chain-audit`, `_audit_live_map` returns exactly one `REGISTRY-AUDIT-LIVE-MAP` finding, site `SKILL.md`, detail `exactly one operative boot-chain-audit row required` (`:270-280`). Under `--audit-live-map`, the metric is therefore `audit_live_map_errors=1`; with no unrelated findings the expected result is `FAIL`/exit **1** (`:351-361`). This matches the C3 error contract (`SKILL.md:2118`; preregistration’s legacy-map red result at `.ufo/waves/round-20/preregister.json:49-53`).

## Coverage gap / smallest safe correction

The selftest does not exercise duplicate map rows in C3 mode. Its duplicate-highest fixture checks only `CANNOT` and `E-REGISTRY-TABLE` (`:533-538`), and `_invoke` defaults `audit_live_map=False` (`:433-443`). The C3 fixtures cover corrected, live-1, highest-table, and historical-only cases (`:565-613`), but none duplicates `boot-chain-audit`. Add one isolated fixture with two `boot-chain-audit` rows under a unique highest heading, invoke `_invoke(..., audit_live_map=True)`, and assert exit 1, `audit_live_map_errors == 1`, and the C3 finding/detail above. This is a regression-test gap; the inspected implementation already fails closed for that shape.

A boundary to keep explicit: heading discovery uses an exact full-match regex with no optional leading/trailing Markdown syntax (`:23-25,137-149`). Thus a Markdown-equivalent decorated duplicate (for example, a leading-space or closing-`##` variant beside one exact heading) is not counted as a second registry heading. The lane’s operative rule explicitly specifies the exact heading form (`SKILL.md:1999`), so I cannot establish that such a variant is an operative duplicate under the contract. If the intended rule is instead to reject semantically equivalent Markdown headings too, the smallest code correction is to detect and reject those same-round variants rather than silently ignoring them; otherwise keep the exact-form rule and document/test that boundary.

## Limits

Source-only review of the inherited registry candidate and cited R20 lane evidence. No fixture, evaluator, build, or runtime was executed; this does not establish candidate output, host state, or boot safety.

Scope: executed=none
