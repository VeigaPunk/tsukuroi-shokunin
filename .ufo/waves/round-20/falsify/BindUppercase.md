# BindUppercase — source-only review

## Scope and axes

Round20 attempt1; registered baseline `0cbc34dd6b20896085a8fb07943e3ea4027d8472`. The binder worktree is `/tmp/tsukuroi-r20-binder-20261021`, as recorded in `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/worktree-bindings.json:2-7`. Axes examined: uppercase object-selector identity, case-preserving branch semantics, and the judge's actual case coverage. This is a recommendation from source inspection, not a claim admission or an executed result.

## Findings, by severity

### High — the judge's acceptance helper has an argument mismatch, so its uppercase case is unreachable on the normal selector-probe path

- `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:393-401` defines `accepted(sandbox, name, rev, expect_sha)` with four parameters. The new `exact_accept()` calls it with five positional arguments, including `branch`, at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:479-482`.
- The first normal acceptance call in `object_selector_probes()` is the real-prefix branch-shadow case at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:590-596`; the uppercase full-object case subsequently uses that same helper at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:615`.
- The canonical judge path invokes these probes for present original tools at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:663-669`. Its top-level exception handler emits `E-INTERNAL` with exit class 2 at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:1108-1118`; the corresponding payload reports `object_selector_tools=0`, `CANNOT_EVALUATE`, and no per-tool cases at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:733-744`.

**Consequence [INFERENCE]:** once normal fixture construction reaches the first acceptance call, Python raises `TypeError` before any uppercase acceptance can be observed. This cannot substantiate the preregistered `object_selector_tools: 0→9` claim (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:13-19`). The judge's own selector-positive selftest calls this same path at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:1021-1030`, while its exception handler only catches `Cannot` at `:1086-1087`.

The caller/definition contract must agree. Merely discarding the fifth argument would also discard the requested branch: `run_tool()` already supports forwarding it at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:359-364`.

### Medium — the judge's positive synthetic consumer rejects uppercase before reaching its lowercase object lookup

- The real binder and independent judge both admit `A-F` in their revision syntax: `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:41` and `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:82`.
- In contrast, the judge's synthetic consumer defines `HEX` as `[0-9a-f]{7,64}` at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:775`. Its unconditional revision gate rejects an uppercase letter at `:810-812`, before object-selector mode performs `rev.lower()` at `:813-818`.
- The positive selector fixture instantiates this `object-selector` mode for every original tool and expects all nine to pass at `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:1021-1030`. Its case set includes `tip.upper()` at `:615`.

**Consequence [INFERENCE]:** after the argument mismatch is repaired, any fixture tip containing `a-f` will make this supposedly positive consumer reject the full uppercase case with `E-REVISION-INVALID`; the new normalization line is unreachable for that input. A digits-only tip would evade the failure only by failing to exercise case conversion. Fixture construction commits ordinary generated content and has no letter-bearing-OID requirement (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:867-883`). This is a concrete mismatch between the synthetic consumer and both actual resolver syntax contracts, not an observed test result.

## Normalization and unchanged nonhex semantics

No source-level mismatch was found in the actual binder versus the judge's own object lookup:

- Binder: `bind()` validates hexadecimal syntax before calling `_object_commit()` (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:172-179`); `_object_commit()` passes `revision.lower()` specifically to `--disambiguate` (`:112-124`). It returns the enumerated commit OID or a peeled tag's commit output, rather than echoing the input selector (`:126-146`).
- Independent judge: its syntax gate likewise precedes `object_commit()` (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:192-199`), which passes `prefix.lower()` to object enumeration (`:139-148`) and returns the selected commit OID or tag peel (`:149-166`). Both full and short valid uppercase hexadecimal inputs therefore enter the same lowercased lookup expression. This conclusion concerns source dataflow, not an exercised Git invocation.
- Lowercasing is not applied to `branch`. Both implementations validate the original branch string and construct literal `refs/heads/{branch}` / `refs/remotes/origin/{branch}` paths (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:84-95,172-192`; `/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:178-208`). The corresponding lane-source validation and branch interpolation have the same case-preserving form (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/_revision.py:83-94,134-154`; `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-revision-binding.py:148-176`). Thus no branch-case folding was introduced in these inspected paths.
- Nonhex strings used as **revision selectors**, including `master`, `MASTER`, and `refs/heads/master`, still fail the hex gate before object normalization. That is distinct from a nonhex **branch parameter**, whose original spelling remains the ref identity. Existing binder negative declarations include `master` and `refs/heads/master` (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:238-243`); judge consumer probes include `master` (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:413-420`), and the judge's own bind checks include the full ref string (`:1045-1049`).

## Exact declared case coverage and residual gaps

| Surface | Full hexadecimal selector | Short hexadecimal selector | Case limitation |
|---|---|---|---|
| Binder selftest | Lowercase `tip`, and uppercase `tip.upper()` with exact expected `tip` (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:233-236`) | Lowercase `tip[:8]` only (`:234`) | No dedicated uppercase-short or mixed-case selector declaration; generated tip has no enforced letter condition (`:222-225`). |
| Judge's original-tool probes | Lowercase `tip` (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:418`), plus `uppercase_object=tip.upper()` (`:615-616`) | Lowercase `tip[:8]` (`:419`); lowercase generated prefix shadows (`:584-599`) | No uppercase-short case. New acceptance cases are blocked by the high-severity finding. |
| Judge's own bind selftest | Lowercase generated `tip5` (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:1043-1049`) | No dedicated uppercase-short bind assertion | No direct uppercase-full assertion of the independent resolver either. |
| Annotated-tag selectors | Generated tag OID | Generated unique tag prefix | Neither is uppercased in the binder (`/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:315-323`) or judge probes (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:576-583,617-618`). |

Additional limits:

- Full uppercase coverage plus lowercase-short coverage is not an uppercase-short test. A length-dependent uppercase regression is not separately exercised by these declarations. No dedicated mixed-case branch identity fixture was found in the inspected binder/judge cases; branch preservation above is a source observation.
- The new helper's name does not mean exact lowercase JSON equality. `accepted()` compares `got.lower() == expect_sha.lower()` (`/tmp/tsukuroi-r20-binder-20261021/tools/check-revision-binding.py:393-401`); `exact_accept()` only adds an exit-code condition (`:479-482`). Consequently, after its arity issue is repaired, uppercase JSON output can still satisfy this comparison. That checks case-insensitive object identity, not canonical lowercase output or how lookup was performed. The existing R20 baseline-only oracle artifact proposed both uppercase-full and uppercase-short inputs, a letter-bearing prefix, and exact lowercase JSON comparison (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/build/BindUpperHex.md:12-24`); those proposals are not the implemented case set. The preregistered `uppercase_object` expectation itself is only “same commit” (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-20/preregister.json:42`), so this distinction is a coverage limit, not evidence that the actual binder returns uppercase.

## Verification limits

Read-only source/artifact inspection only. `read xd://lsp` reported “No such tool” and listed only `ast_edit` and `debug` devices; no LSP server/status, references, definitions, or diagnostics were available through the permitted surface. Literal grep was used only for source-location discovery, not presented as semantic proof. No commands, imports, tests, builds, formatters, external requests, candidate execution, tool installation, or host operations were performed. No execution or measurement result is asserted; conditional runtime consequences are marked `[INFERENCE]`. No Git-state or code edits were made, and this report is the only file written. Boot images remain UNKNOWN; this review grants no host or boot clearance.

Scope: executed=none
