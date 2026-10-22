# ScribeMarkerDriver — C1 marker O08 draft (round 29, wave 1)

Verdict: done — the O08 marker for `corpus/knowledge/driver-firmware-plane.md` line 276 is drafted, and a sandbox validation shows the round-29 counter accepts it (`"id": "O08", "ok": true, "verdict": "corrected"`, summary `marked 1`, `unresolved` empty). [obs]

1. Target anchor verified verbatim at the revision under attack. [obs]
   `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 81a061a67466c5e1be812814a895a4b5ed89b4ff:corpus/knowledge/driver-firmware-plane.md | grep -nF 'the loaded module is not re-identified by modinfo [unk]'` → `276:…` (exit 0). Anchor text frozen by the counter: `the loaded module is not re-identified by modinfo [unk]` (`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-owed-statements-r29.py:70`).

2. The resolving capture is the round-27 kernel-taint capture, tracked at the revision. [obs]
   `corpus/knowledge/kernel-taint-r27.json` names `.ufo/waves/round-27/capture/capture.txt` with sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`; the working-tree file has exactly that sha256 (`sha256sum` → match) and 138 lines, and `git cat-file -e 81a061a…:.ufo/waves/round-27/capture/capture.txt` succeeds (tracked, so `path:LINE` basis refs resolve in the counter's `git show`).

3. The capture block `### modinfo-nvidia` (lines 44-58 at the revision) holds the modinfo output naming the loaded module, version and signer. [obs]
   Line 45 `$ modinfo -F filename nvidia` → line 46 `/lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst`; line 48/49 → `615.78.08`; line 54/55 → `DKMS module signing key`; line 57/58 → vermagic `7.2.11-arch1-1 SMP preempt mod_unload`. This closes the round-17 `[unk]`: modinfo does re-identify the loaded module. Verdict chosen: `corrected`.

4. S143/S144 checked as the assignment asked and NOT used. [obs]
   Their `corpus/SOURCES.md` rows are `| S143 | … | code | A | … | mined | 2026-10-22 | on-release | corpus/knowledge/kernel-taint-r27.md |` and the same for S144 (cell 11 = `corpus/knowledge/kernel-taint-r27.md`); neither used-by cell names `driver-firmware-plane.md`, so M6 would list them as unresolved. Basis is therefore three `path:LINE` refs only; M7 does not apply to O08 (kernel-mechanism S### is required only for O01-O04).

5. Marker line drafted (the exact line to append, also in `draft.md`). [obs]
   `[R29-OWED-O08] verdict: corrected | original: "the loaded module is not re-identified by modinfo [unk]" | now: The round-27 capture re-identifies the loaded module: modinfo -F filename nvidia reports /lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst, version 615.78.08 and signer DKMS module signing key, so the loaded DKMS build for the running 7.2.11 kernel is named and the round-17 unknown is closed. | basis: .ufo/waves/round-27/capture/capture.txt:45 (the command \`modinfo -F filename nvidia\`), .ufo/waves/round-27/capture/capture.txt:49 (615.78.08), .ufo/waves/round-27/capture/capture.txt:55 (DKMS module signing key), the round-27 kernel-taint capture whose sha256 88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841 matches \`corpus/knowledge/kernel-taint-r27.json\` \`capture.sha256\``
   Placement for the L1: one new line immediately after line 276, original line untouched (M1/M2 require the anchor to remain and exactly one line to carry the id). `now` has 39 words (checker regex group, re-parsed: `original == anchor True`, `anchor in now False`, one id occurrence per line), repeats no anchor substring.

6. Sandbox validation (seat clone under `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkerDriver/repo`, no GIT_* inherited). [obs]
   Baseline at `81a061a67466c5e1be812814a895a4b5ed89b4ff`: `{"revision": "81a061a…", "items": 12, "marked": 0, "unmarked": ["O01"…"O12"], "counter_sha256": "5b6cf227580ff26e47db5888001febc7ff38b97322bd496121a6aa84c2dc6375"}`. After inserting the marker line and committing in the clone (`cf8b31fa4176597a555b13fad2477da1980c5021`): O08 row `{"basis": {"paths": [".ufo/waves/round-27/capture/capture.txt:45", ".ufo/waves/round-27/capture/capture.txt:49", ".ufo/waves/round-27/capture/capture.txt:55"], "sources": [], "unresolved": []}, "file": "corpus/knowledge/driver-firmware-plane.md", "id": "O08", "ok": true, "verdict": "corrected"}`; summary `"marked": 1`, exit 1 (expected: O01-O07 and O09-O12 still unmarked). Raw output: `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkerDriver/counter-o08.jsonl`.

7. The marker quotes only capture bytes; no source was fetched and no quote outside the capture is used. [obs]
   The capture line refs are the whole basis; nothing here asserts a kernel mechanism. [inf] A reviewer may prefer a second basis ref to `corpus/knowledge/kernel-taint-r27.json` (`capture` object) but the checker resolves the capture path directly, so it is not needed.

Out-of-scope items: no other O-item marker was drafted (O01-O07, O09-O12 untouched); no lane file was edited (the only edit was in the seat sandbox clone, used for validation); no counter was rerun to decorate — the two runs were the before/after falsifier of this draft.

Artifact paths:
- Draft line: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeMarkerDriver/draft.md`
- Validation output: `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkerDriver/counter-o08.jsonl`
- Sandbox clone: `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkerDriver/repo` (detached commits `81a061a…` base, `cf8b31fa…` marker)

Scope: read=SCORECARD.md:1097-1109, tools/check-owed-statements-r29.py, corpus/knowledge/driver-firmware-plane.md:276, corpus/knowledge/kernel-taint-r27.json, corpus/SOURCES.md (S140-S147 rows), .ufo/waves/round-27/capture/capture.txt:1-62, git objects at 81a061a67466c5e1be812814a895a4b5ed89b4ff; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeMarkerDriver/draft.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-29/w1/ScribeMarkerDriver.md, /fast/scratch/hyaku/tsukuroi-r29/ScribeMarkerDriver/ (clone, counter-o08.jsonl); executed=git show/cat-file/rev-parse (read-only) in the lane, git clone/checkout/commit in the seat sandbox, python3 tools/check-owed-statements-r29.py (2 runs), grep -nF/grep -cF, sha256sum
Model: opencode-go/deepseek-v4.1-flash
Installs: none
