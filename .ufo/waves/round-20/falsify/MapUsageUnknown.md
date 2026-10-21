# MapUsageUnknown — C3 usage and no-clearance semantics

## Counterexample / finding

The corrected **verdict-map cell itself** is fail-closed against an altered usage or clearance statement: the candidate constant includes `usage: 2 could-not-evaluate` and `not operator clearance` (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:31-34`), and `_audit_live_map` requires a whitespace-normalized exact match (`:270-288`). The lane's operative row also says `--live (not live-run round20)` and limits live reads to separate authorization, with no host writes (`SKILL.md:2109`). The underlying script documents usage errors as exit 2 (`tools/boot-chain-audit.sh:81-86`) and returns live `UNKNOWN`/2 or `CONSISTENT`/0 from its summary (`:794-806`). I found no way for the required corrected map text alone to assert operator clearance.

However, the candidate does **not** enforce that no-clearance/non-live-run meaning across the whole registry row, and its successful result is not a host check:

- `_audit_live_map` checks the row name, kind, tool path, and verdict cell only (`/tmp/tsukuroi-r20-registry-20261021/tools/check-registry-coverage.py:277-288`). `_coverage` unpacks pinned values, write scope, and owner into unused `_pinned`, `_scope`, and `_owner` variables (`:203-215`); its other checks do not validate those cells (`:216-267`). It checks only that the entry cell names the expected tool path, not the `--live (not live-run round20)` qualification (`:283-285`). **[INFERENCE]** Thus a mutated operative row retaining the exact corrected verdict cell but changing its entry-cell qualification or write-scope text to claim a successful host check or authorization can still satisfy the C3-specific check; the contradictory neighboring text is outside this check's inspected fields.
- The candidate emits the generic top-level `status: PASS` (`:297-302`) after reading committed `SKILL.md` and tool files and checking map metadata (`:344-362`); it does not invoke the audit. Its corrected-map selftest fixture even uses a stub source containing only a comment and a `--selftest` string (`:565-581`). **[INFERENCE]** A detached `PASS`/`audit_live_map_errors=0` receipt could therefore be mistaken for a successful host check unless its checker scope is retained. No host observation or authorization is established by that result.

These are bounded presentation/row-consistency risks, not evidence that the current lane text grants authority or that C3's finite map calibration is wrong. Existing limits expressly disclaim host/boot-safety certification (`.ufo/waves/round-20/build/ConnSourceLimits.md:23-28`); no host or boot check was run here.

## Impacted axes

- **C3 calibration:** the exact usage-2 and no-clearance wording is protected in the verdict cell. Candidate C3 success means only that this map cell matches.
- **Authority / host-check interpretation:** the C3 gate does not police contradictory entry/write-scope cells, and its generic `PASS` needs registry-check context. No impact found to C1/C2.

## Smallest safe correction

Keep C3's result explicitly labeled as a **registry-map check only**, never as an audit/host `PASS`. If the acceptance criterion requires preventing misleading authorization claims anywhere in the operative row, extend the finite C3 check to pin the existing non-live-run entry qualification and separately-authorized/no-host-write scope (or reject contradictory authority language there); checking the verdict cell alone cannot guarantee row-wide semantics. Do not broaden this into a claim of host or boot safety.

Limits: source/artifact inspection only; no candidate or host execution. Findings describe source behavior and the explicitly marked inferences, not observed output.

Scope: executed=none
