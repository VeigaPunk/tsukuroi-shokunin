# BindGhostTag — C2 independent edge-case design

## Finding / proposed fixture

The frozen C2 oracle already requires `ghost_hex_tag` to return `E-REVISION-INVALID; exit=2` (`.ufo/waves/round-20/preregister.json:37-41`). The baseline selftest and independent judge do not currently exercise a ref with a hex-shaped tag name: `_revision.py:200-205` tests an unknown `"0" * 40` selector, while `check-revision-binding.py:380-435` covers ordinary IDs and a blob, but no tag-name collision.

In the judge's isolated sandbox, use the already landed `tip` as the target and add two distinct 40-hex tag names (assert each name is not already an object ID before creating its ref):

- lightweight: `deadbeefdeadbeefdeadbeefdeadbeefdeadbeef` → `refs/tags/<name>` points directly to `tip`;
- annotated: `cafebabecafebabecafebabecafebabecafebabe` → `refs/tags/<name>` is an annotated tag pointing to `tip`.

For each case, call the consumer with only the bare 40-hex tag name as `--revision` (not `refs/tags/<name>` and not an object-prefix expression). The judge sandbox setup makes `tip` both `refs/heads/master` and `refs/remotes/origin/master` (`check-revision-binding.py:201-210`), so erroneous resolution to the tag target cannot be masked by branch ancestry or push checks.

Expected helper result for each: `RevisionError(E-REVISION-INVALID, site="revision", ...)`. Expected `refused(...)` observation per consumer: `exit=2`, `finding=E-REVISION-INVALID`, `binding_ids=["E-REVISION-INVALID"]`, `finding_count=1`, `ok=true`. Keep the preregistered `ghost_hex_tag` oracle satisfied only when **both** lightweight and annotated variants refuse; these can be separate per-tool cases aggregated under that oracle label. The judge's strict-refusal check already enforces exactly one binding finding (`check-revision-binding.py:424-430`).

## Source justification and kill condition

The shared binder's documented selector contract requires 7–64 hex and classifies an unresolved/non-commit revision as invalid (`tools/_revision.py:14-21`). `bind()` checks only that the input is hex-shaped, then passes the raw string to `_commit()` (`tools/_revision.py:134-141`); `_commit()` asks `git rev-parse` to resolve `<raw>^{commit}` (`tools/_revision.py:97-108`). Thus the missing edge is distinguishing an object-ID selector from a same-named ref. The independent judge intentionally keeps a separate implementation (`tools/_revision.py:8-9`); its `bind()` likewise applies the hex regex then calls `rev_parse(repo, rev)` (`check-revision-binding.py:130-136,162-176`), and its current probe matrix lacks this tag fixture (`check-revision-binding.py:380-435`).

Smallest wrong implementation killed: accept a selector merely because `rev-parse <raw-hex>^{commit}` resolves it, without establishing that the bare selector names an object ID. If Git resolves either raw name through its same-named tag ref, that implementation returns the landed `tip` (exit 0) instead of the preregistered invalid result (exit 2). **[INFERENCE]** The fixture's intended discrimination depends on Git's raw-name resolution of the synthetic tag; no command was run to observe that resolution under this NO-EXEC assignment.

## Scope and limitations

Read-only source/oracle inspection only; no candidate edits and no fixture execution. Baseline identity was taken from the task's pinned baseline context, not independently checked with Git. No LSP device/status was exposed in the allowed read-only tool set. No claim about host or boot safety.

Scope: executed=none