# FxMutJudge — SURVIVES these bounded attacks

Axes: C2 operability, detector calibration, exact restoration. Target: `68a8ae035fde33360cbbe21dc92ca0eacf0a5b33`. Own no-hardlinks clone: `FxMutJudge.HTur9a/clone`; pinned HEAD verified, origin removed. No production edits.

Detector: `/usr/bin/python3 -B /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/falsify/FxMutJudge.HTur9a/clone/tools/check-revision-binding.py --selftest`. TMPDIR remained inside clone; bytecode disabled. Pristine and four restored runs: **50/50, exit0**. Four mutants: **KILLED, exit1**, assertion failures, empty stderr; no fixture exceptions.

Exact changed lines in `tools/check-revision-binding.py` (original numbering):
```diff
@@ 262
-    return uses, copies
+    return uses or bool(SHARED_IMPORT.search(source)), copies
@@ 344
-            "finding_count": len(findings) if isinstance(findings, list) else None,
+            "finding_count": len(binding_ids(text)) if isinstance(findings, list) else None,
@@ 406
-    must(git(sandbox, "update-ref", "-d", remote), "E-SANDBOX", "origin absent")
@@ 480
-    return (PASS if result["consistent_tools"] == result["total"] else FAIL), result["status"]
+    return (PASS if result["all_consistent_tools"] == result["all_total"] else FAIL), result["status"]
```

Expected detectors actually fired:
- deadimport: **48/50**; `dead-import-not-shared` got `(1,True,0)` versus `(0,False,0)`; `local-copy-census` got `(True,1)` versus `(False,1)`.
- extra-unrelated: **48/50**; `shared-extra-finding-bound-not-consistent` got `(True,True,9,9,0)` versus `(True,False,9,8,1)`; failing-probes empty versus `{'single-id'}`.
- missingorigin: **48/50**; analogous `shared-require-origin-*` failures, empty versus `{'origin-absent'}`.
- discoveredunbound: **49/50**; `discover-unbound-independent` got `(9,9,1,0,1)` versus `(9,9,1,0,0)`.

Restored SHA256 after every mutant: `5a5198951a36bc1e806cd403cccf5c10873741ce67f38ebeb3a2fec162fe780f`, identical to pristine. Full before/mutated/after hashes, actual outputs/exits/argv: [observations](FxMutJudge.HTur9a/observations.json). Exact Git patches: `FxMutJudge.HTur9a/{deadimport,extra-unrelated,missingorigin,discoveredunbound}.diff`.

Unknowns: universal runtime equivalence and final production measurements remain unproven. No tools installed.

Scope: executed=/usr/bin/mktemp -d; /usr/bin/git clone --no-hardlinks --no-checkout, checkout --detach, remote remove origin, rev-parse HEAD, remote, diff --no-ext-diff --no-textconv (4); /usr/bin/mkdir -p; /usr/bin/sha256sum (18); /usr/bin/python3 -B <absolute-clone-judge> --selftest (9), including its sandbox-only fixture Git/stub subprocesses.
