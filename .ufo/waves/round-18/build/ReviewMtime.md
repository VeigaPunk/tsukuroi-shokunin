# ReviewMtime — falsifier: C1 boot-chain-r17:88 mtime source (B:115 vs B:124)

## Verdict: SURVIVES

The routed correction — at `corpus/knowledge/boot-chain-r17.md:88` the `(mtime 09:26:22)` support must be B:124, not B:115 — is byte-verified. No image-identification confusion found.

## Evidence

Bytes frozen: `boot-chain-r17.md` sha256 `655275a011bd05031ec244f1adcd44eaebb508a0e9529c8b6786462d479433e6` and `boot-chain-capture.txt` `1a05ec2aba4d0dc1a4a336617a432d218f53281b06745ea8adc956334e035868` identical at baseline `842a5312`, prerequisite `51dd9eea`, and working tree; `R18-CORR` count 0 (not yet landed).

- Defect, exact bytes: `:88` `…The image file (mtime 09:26:22) is byte-identical to` → `:89` `the 09:29:18 history copy (B:115, 171, 219).` B:115 = `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:115` `…09:29:18…omarchy_linux.efi_sha256_2e9c9bdc…` — the snapshot-#2 history copy, whose own mtime contradicts the 09:26:22 it would support. B:115/171/219 correctly support the *copy* clause: B:219-220 sha256 `2e9c9bdc…`/b2sum `822299bb…` of the history copy equals B:171-172 of the live image (byte-identity).
- Correct line: `boot-chain-capture.txt:124` `-rwx------ … 284439552 2026-10-20 09:26:22… omarchy_linux.efi` under `/boot/EFI/Linux:` — unique 09:26:22 file line in the capture (grep: only :122 dir, :124 file).

## Image identification (no confusion)

- B:124 names the booted default: `LoaderEntrySelected: Omarchy.linux` / `LimineLastBootedEntry: Omarchy/linux` (`supplement-capture.txt:113,115`); limine.conf `//linux` → `path: …/omarchy_linux.efi#822299bb…` (B:25,30), b2sum matches B:172, uname 7.2.11, VERSION 42.2 (B:173-175).
- Adjacent traps all excluded: :122 is the `/boot/EFI/Linux` directory (09:26:22); :125 is `omarchy_linux-lts.efi` (09:26:16); :114 is snapshot-#1 copy `0f1e3c84…` (09:03:02). Lane's own two-image cite `boot-chain-r17.md:27` already maps 09:26:16/09:26:22 → B:124–125, confirming the 124↔09:26:22 convention. Timing coherent: 09:26:22 < boot 0 (loader dir 09:57:10, B:108).
- `boot-chain-r17.json:112` states the mtime with no B-cite; factually consistent with B:124 — correction scope is the md cite only.

## Residual risk

Off-by-one drift to :122/:125 during drafting is the only failure mode; :124 with filename `omarchy_linux.efi` in the quote discharges it.

Scope: executed=read (files, ranges), grep tool, read-only `git show` + `sha256sum` in lane (no writes, no probes).
