# C1 marker O08 — draft for `corpus/knowledge/driver-firmware-plane.md`

Target file: `corpus/knowledge/driver-firmware-plane.md`, anchor at line 276 (verified verbatim at revision 81a061a67466c5e1be812814a895a4b5ed89b4ff):

```
- Stale: "filename: /lib/modules/7.2.3-arch1-3/updates/dkms/nvidia.ko.zst" — [obs] 7.2.3-arch1-3 dkms row: built modules missing (615.78.08); the loaded module is not re-identified by modinfo [unk]. Capture `.ufo/waves/round-17/l1-capture/fresh-capture.txt:38`.
```

## The exact line to append

Append this as one new line immediately after line 276 (append-only; the original line stays untouched):

[R29-OWED-O08] verdict: corrected | original: "the loaded module is not re-identified by modinfo [unk]" | now: The round-27 capture re-identifies the loaded module: modinfo -F filename nvidia reports /lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst, version 615.78.08 and signer DKMS module signing key, so the loaded DKMS build for the running 7.2.11 kernel is named and the round-17 unknown is closed. | basis: .ufo/waves/round-27/capture/capture.txt:45 (the command `modinfo -F filename nvidia`), .ufo/waves/round-27/capture/capture.txt:49 (615.78.08), .ufo/waves/round-27/capture/capture.txt:55 (DKMS module signing key), the round-27 kernel-taint capture whose sha256 88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841 matches `corpus/knowledge/kernel-taint-r27.json` `capture.sha256`

## Evidence for the resolution

- `.ufo/waves/round-27/capture/capture.txt:44-55` (tracked at the revision; sha256 `88d02d98cbb5fd4633ff83cacb2256ac57af1d740c7c57b6ac7a98fceb067841`, 138 lines), block `### modinfo-nvidia`:
  - line 45 `$ modinfo -F filename nvidia` → line 46 `/lib/modules/7.2.11-arch1-1/updates/dkms/nvidia.ko.zst`
  - line 48 `$ modinfo -F version nvidia` → line 49 `615.78.08`
  - line 54 `$ modinfo -F signer nvidia` → line 55 `DKMS module signing key`
  - line 57 `$ modinfo -F vermagic nvidia` → line 58 `7.2.11-arch1-1 SMP preempt mod_unload`
- `corpus/knowledge/kernel-taint-r27.json:6-8` names that capture path and the same sha256.
- `S143` and `S144` were checked and are NOT usable as basis here: their `corpus/SOURCES.md` used-by cell (cell 11) is `corpus/knowledge/kernel-taint-r27.md`, not `driver-firmware-plane.md`, so M6 would reject them for O08. Basis is therefore path refs only (M7 does not apply to O08).

## Validation run in the seat sandbox

`/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkerDriver/repo` (clone of the lane at `81a061a67466c5e1be812814a895a4b5ed89b4ff`), marker inserted after line 276, committed there, then:

```
python3 tools/check-owed-statements-r29.py --revision <sandbox-commit> --lane /fast/scratch/hyaku/tsukuroi-r29/ScribeMarkerDriver/repo
```

Baseline before the insert at `81a061a67466c5e1be812814a895a4b5ed89b4ff`: `{"revision": "81a061a67466c5e1be812814a895a4b5ed89b4ff", "items": 12, "marked": 0, "unmarked": ["O01", ..., "O12"], "counter_sha256": "5b6cf227580ff26e47db5888001febc7ff38b97322bd496121a6aa84c2dc6375"}`.
