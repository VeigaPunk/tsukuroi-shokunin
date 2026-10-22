# RevMarkerO08 — attack on C1 marker O08 at 10d5288fc1051364e711203855e7c53710dfcc21

Verdict: **holds** — the O08 marker in `corpus/knowledge/driver-firmware-plane.md:315` passes every check I could run against it: the original statement is unchanged in place, the `corrected` verdict is the right reading of the round-27 capture, and every cited basis line resolves to bytes that name the loaded module, its version and its signer, with the one recomputable number (the capture sha256) matching exactly.

Lane tip verified `10d5288fc1051364e711203855e7c53710dfcc21` (`git rev-parse HEAD`), and `git status --porcelain` on the five files touched below is empty, so lane working-tree bytes are the revision bytes.

## Findings

1. **(a) Original statement unchanged — holds.** The anchor line is `corpus/knowledge/driver-firmware-plane.md:276` ("- Stale: "filename: /lib/modules/7.2.3-arch1-3/updates/dkms/nvidia.ko.zst" — [obs] 7.2.3-arch1-3 dkms row: built modules missing (615.78.08); the loaded module is not re-identified by modinfo [unk]. ..."). sha256 of that line without its newline = `4703768aa5b2ff4bf421fa5de3ada08eef35dad07b55f566fc911b3f37ebde4c`, byte-identical to `BASE_DIGEST['O08']` in `tools/check-owed-statements-r29.py:96`. M1 holds; the anchor is a verbatim substring and the line sits outside the marker. [obs]

2. **(b) Verdict `corrected` is right.** The round-17 statement recorded an unresolved unknown (modinfo could not name the loaded module because the 7.2.3-arch1-3 tree had no built modules). The round-27 capture resolves that unknown with named evidence (finding 3), so the old statement is superseded, not merely narrowed: `corrected` (not `qualified`, not `rebutted`) is the correct token, and it is one of the three M4 tokens. [obs]

3. **(c) Every basis reference resolves and supports the `now` text — holds, numbers recomputed.** The marker cites no `S###` row (counter `sources: []`), so the SOURCES.md/w1-snapshot leg of the assignment is N/A for this item; its bases are repo path:line plus one sha256:
   - `.ufo/waves/round-27/capture/capture.txt:45` is exactly `$ modinfo -F filename nvidia` (the command the parenthetical names); its output line 46 is `/lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst`. [obs]
   - `:49` is exactly `615.78.08` (modinfo -F version nvidia at `:48`). [obs]
   - `:55` is exactly `DKMS module signing key` (modinfo -F signer nvidia at `:54`). [obs]
   - The sha256 I recomputed over `capture.txt` is `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, equal to the marker's value and to `corpus/knowledge/kernel-taint-r27.json` `capture.sha256` (its `capture.path` is this same file). [obs]
   - Loaded module, version, signer all named, per the assignment's basis test: module via `:45-46` plus capture lines 16-20 (`module_taint nvidia OE`, and OE for nvidia_drm/nvidia_modeset/nvidia_uvm — those modules are loaded this boot), version 615.78.08 at `:49`, signer at `:55`, vermagic `7.2.11-arch1-1 SMP preempt mod_unload` at `:58` matching `uname -r` `7.2.11-arch1-1` (capture line 6), journal lines 135-136 "nvidia: module verification failed: signature and/or required key missing - tainting kernel", and `pacman -Qo` at `:65` reporting no package owns the .ko (DKMS-built), with `nvidia-open-dkms 615.78.08-1` installed (capture lines 128-131). All three cited lines exist, are non-blank, non-marker: M6 passes. [obs]

4. **Counter agrees.** `python3 tools/check-owed-statements-r29.py --revision 10d5288fc1051364e711203855e7c53710dfcc21` in the sandbox clone at `/fast/scratch/hyaku/tsukuroi-r29/RevMarkerO08/repo` prints O08 `ok: true` with `basis.paths` resolving all three capture lines and no `unresolved`, and the summary `items: 12, marked: 12`, `counter_sha256 c3f9cfe73e980db948b7ab375c4d2876ba83685171bd53716a576944d69e52ab` — the declared version-2 counter. [obs]

5. **Minor wording compression, not a defect.** [inf] The `now` sentence says "The round-27 capture re-identifies the loaded module: modinfo -F filename nvidia reports ...". modinfo reads the on-disk file; `kernel-taint-r27.json` `corrections_r27_a2` row KT4 itself notes "the loaded version is /sys/module/<name>/version, modinfo reads the file on disk". The loaded-module identity actually rests on the same capture's per-module taint `nvidia OE` plus the journal taint lines plus the vermagic/uname match — evidence the capture contains, so the conclusion stands; only the single-step attribution to modinfo is compressed. Non-blocking.

## Residual risk and verification gaps

- I did not re-run the round-17 capture or the live host; the "loaded" chain inside the round-27 capture (taint/journal → on-disk file) is an inference from consistent capture bytes, as finding 5 records. [unk] whether /sys/module/nvidia/version would have matched byte-for-byte; it was not captured in round 27.
- M2 marker uniqueness across the six target files is verified only through the counter's `ok` flag, not by my own cross-file grep of every target file.

Scope: read=SCORECARD.md:1096-1100; corpus/lessons/round-29.md; corpus/knowledge/driver-firmware-plane.md:276,300-320; tools/check-owed-statements-r29.py:1-96; .ufo/waves/round-27/capture/capture.txt:1-138; corpus/knowledge/kernel-taint-r27.json; wrote=.ufo/waves/round-29/w2/RevMarkerO08.md; executed=git rev-parse/status (read-only, lane); sha256sum line 276 + capture.txt; sandbox clone+checkout at /fast/scratch/hyaku/tsukuroi-r29/RevMarkerO08/repo; check-owed-statements-r29.py --revision 10d5288f in sandbox
Model: zai/glm-5.3-flash
Installs: none
