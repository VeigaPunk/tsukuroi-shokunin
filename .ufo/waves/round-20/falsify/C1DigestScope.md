# C1DigestScope — R20 attempt 1 source/digest provenance

## Scope and finding severity

**Axes:** C1 adjacency; exact source identity; raw-byte digest commitment; fidelity of the attributed declaration.

**No actionable digest-scope finding identified.** The candidate does not accept an arbitrary snapshot merely because it carries an OUT-009 label, matching quote, or a newly supplied digest. Its C1 path fixes the complete source identity and hashes the loaded snapshot's raw bytes against a fixed expected SHA-256. This is a static review conclusion, not a measured `ownership_corrections=1` result, claim admission, or host/boot clearance.

Reviewed candidate root: `/tmp/tsukuroi-r20-adjacency-20261021` (`A` below). Production lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` (`L` below). Both abbreviations are exact path prefixes. The declared baseline is `0cbc34dd6b20896085a8fb07943e3ea4027d8472` (`L/.ufo/waves/round-20/preregister.json:2-11`); Git history/working-tree identity was not independently authenticated.

## Exact evidence and attack result

### 1. Expected identity matches the retained source row, not a convenient label

- `A/tools/check-adjacency-anchors.py:77-90` fixes OUT-009's pointer `../revenger-shokunin/PROVINCE.md:3-7,19-25`, sibling `revenger`, source path `PROVINCE.md`, full sibling commit `cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97`, SHA-256 `63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f`, snapshot `.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md`, heading `# revenger province`, quote `Owns: reverse engineering of shipped artifacts`, quote line 3, and original proposition.
- These values agree with the actual OUT-009 registry row in **both** `A/corpus/knowledge/adjacency-anchors-r19.json:113-123` and `L/corpus/knowledge/adjacency-anchors-r19.json:113-123`.
- `A/tools/check-adjacency-anchors.py:91-100` separately fixes the census identity and exact ranges `[[3, 7], [19, 25]]`. The lane's captured row records those ranges and the same commit/digest/snapshot at `L/.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json:2981-3003`.
- The correction helper requires exactly one OUT-009 registry record, compares every fixed registry value, and similarly rejects a nonunique or mismatched census record (`A/tools/check-adjacency-anchors.py:140-154`). Thus changing the registry digest together with replacement snapshot bytes is not a supported escape from the C1 commitment. The enclosing evaluator also requires the exact outbound field set (`A/tools/check-adjacency-anchors.py:524-529`).

### 2. The commitment covers the whole raw snapshot, before text interpretation

- The decisive check reads the **fixed snapshot path**, not a path discovered from the quote or a report label, and compares `hashlib.sha256(loaded.data).hexdigest()` to the fixed expected digest. Missing/unsafe data or a mismatch produces `OWNERSHIP-CORRECTION-INVALID` with count zero (`A/tools/check-adjacency-anchors.py:135-139,178-181`).
- Only after that byte check does the helper strictly decode UTF-8, require the pinned heading's section, and require the pinned quote at line 3 (`A/tools/check-adjacency-anchors.py:182-190`). The quote comparison is an exact **substring**, not whole-line equality; the full-blob digest is what additionally commits to the rest of the declaration, its surrounding text, and byte-level differences.
- `GitReader.read` keys reads by revision/path, rejects unsafe paths and nonregular/nonblob entries, and returns the committed blob's raw `git show` stdout (`A/tools/check-adjacency-anchors.py:264-296`). The main entry binds the evaluated and registry revisions and passes that reader into `evaluate` (`A/tools/check-adjacency-anchors.py:819-839`). The production correction call receives `registry_revision` and the same reader (`A/tools/check-adjacency-anchors.py:761-766`). These inspected source paths do not substitute the working-tree snapshot or the selftest fixture for the production snapshot.

### 3. Exact declaration content supports the R20 attribution

- The retained declaration is headed `# revenger province` at line 1. Lines 3-7 enumerate native binaries, managed assemblies, **Electron/JavaScript packages**, Android APKs, archives, firmware, browser/Electron runtime evidence, and the observation/inference/unknown evidence ledger. This wording is present in both `A/.ufo/waves/round-19/l1-capture/siblings/revenger/cf02419276e5/PROVINCE.md:1-7` and the same lane-relative file under `L:1-7`.
- The source's refusal and write-boundary text remains at that snapshot's lines 19-29; the captured census excerpt agrees with the declared ranges (`L/.ufo/waves/round-19/l1-capture/adjacency-pointers-r19.json:3001-3003`).
- `L/.ufo/waves/round-20/ownership-correction.txt:1` uses that precise package category, calls the text Revenger's sibling declaration rather than a tsukuroi ownership grant, preserves unresolved arbitration, and authorizes no configuration/service/package/boot/sibling-file write. The candidate's correction constant contains the same wording (`A/tools/check-adjacency-anchors.py:43-50`). The lane publishes it at `L/PROVINCE.md:148-152`, alongside the retained full source commit/digest at `L/PROVINCE.md:145`.
- The helper requires the exact appended section rather than accepting a digest label somewhere in arbitrary replacement prose (`A/tools/check-adjacency-anchors.py:156-175`). Its explanation explicitly retains the original quoted declaration and pinned bytes as historical evidence (`A/tools/check-adjacency-anchors.py:51-59`).

## Residual risk and verification gaps

1. **Recorded provenance is not fresh origin authentication.** The source row, candidate constants, and lane publication agree on the full commit/digest, but this seat did not recompute the snapshot SHA-256 or inspect the sibling Git object. The existing source review likewise explicitly calls its hash recorded metadata, not recomputed (`L/.ufo/waves/round-20/build/SrcRevengerScope.md:9,24`). The optional sibling-object comparison returns a hash or `None` and only updates counters; it does not reject a mismatch (`A/tools/check-adjacency-anchors.py:430-447,630-635`). Consequently this review does not claim that the gate freshly authenticates the original sibling commit. That is distinct from the fixed raw-byte commitment verified in the source above.
2. **No measured claim result.** The retained measurement script selects this gate and `--ownership-corrections` for before/after evaluation (`L/.ufo/waves/round-20/measure/run.py:70-78`), but no command, gate, test, build, formatter, or smoke run was performed. No claim is made that candidate documents are landed/pushed or that the entire C1 evaluation succeeds.
3. **No semantic-service evidence.** A read of `xd://lsp/status` reported no LSP doc topics; `xd://lsp` then reported no such mounted tool (only `ast_edit` and `debug` were mounted). References, definitions, and diagnostics could not be queried. File/line reads and literal searches were the permitted fallback; they are not presented as LSP-derived proof of caller completeness.
4. This seat examined only C1 source/digest provenance, not other C1 mutation classes, C2/C3, resume continuity, runtime routing, saturation, or any live system. No external requests, host/service/package/boot operations, code edits, delegation, or tool installation occurred. Boot images remain **UNKNOWN**; no clearance.

Scope: executed=none.
