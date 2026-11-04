# E5MarkerAudit — binding report (round 76 wave w1, seat E5MarkerAudit)

## Classification
All nine existing inventoried files are **runtime markers, safe to commit as wave evidence**; the tenth path, `w1-results.json`, is absent and has no content verdict. Every one of the seven carried markers exists as a regular file and `git cat-file -e 865b38c96c23ec0bcace8ca3ee884f860693ce43:<path>` fails for each. This establishes absence from that base tree, not current index status or freedom from history conflicts. Per the assignment, the C2 checker requires those seven paths in the committed revision; the checker was not run by this seat.

## Inventory
Full table (path, bytes, sha256, regular, absent-at-base, content verdict): `markers.txt` beside this file.

## Safety findings (acceptance item 2)
- Content of all seven carried markers plus both round-76 markers is wave-runner bookkeeping only: either a timestamp line without a timezone designation followed by a seat→agent-id JSON map (`*.dispatched`), or a `lane/round/wave/dispatch/l1` JSON object (`w1.ready`). `round-73/w1-run.stderr` is empty (0 bytes).
- No credentials, tokens, or session material in any file.
- No absolute path outside the fleet root: the only absolute paths are the `dispatch` fields in `round-75/w1.ready` and `round-76/w1.ready`, both pointing under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/` — inside the fleet root, therefore passing the stated rule.
- No file approaches 1 MiB; largest is 393 bytes.

## Round-76 state at audit close (acceptance item 3)
- `.ufo/waves/round-76/w1.ready` — exists, 169 B, sha256 `0f100b89c5338d2a77376d2bb49447be6c6098263dc33448965e314368c9d945`, regular, absent-at-base.
- `.ufo/waves/round-76/w1.ready.dispatched` — exists, 393 B, sha256 `d8ea5f8735b25d4c852e582785f331774bbebabba1c5e01f0d4d7472c2f04824`, regular, absent-at-base.
- `.ufo/waves/round-76/w1-results.json` — **does not exist** at audit close (re-checked via directory listing); wave results not yet gathered. Expected later in the wave; L1 should re-check existence immediately before the C2 commit and inventory it with the same fields if present.

## Surprises
1. `round-73/w1-run.stderr` is a 0-byte regular file. Its sha256 is the empty-string hash `e3b0c442…b855`; committing an empty file is valid and it still satisfies "exists in revision", but the C2 checker must not assume non-empty content.
2. The `w1.ready` markers embed absolute dispatch paths inside the lane — within the fleet root, so compliant with the stated rule, but any future rule against absolute paths *at all* would flag these two files.
3. `round-76/w1-results.json` absent at audit time is expected mid-wave, not a defect; noted only so the absence is explicit.

## Method and evidence
- `stat -c '%n|%F|%s|%y'`, `sha256sum`, and `git cat-file -e 865b38c96c23ec0bcace8ca3ee884f860693ce43:<path>` were exercised; all nine existing files were content-read. Exact byte counts and hashes are retained in `markers.txt`; all ten base lookups failed. No build, test, formatter, or C2 checker was run.
- No source marker was modified; only the assigned reports were written: `markers.txt`, `report.md`, and `../E5MarkerAudit.md`. No tools were installed. LSP tools are unavailable in this seat; this file-inventory task required no symbol operations.

## Audit axes
Freshness: observed round-76 readiness files and explicitly recorded missing results. C2 coverage: all seven carried paths inventoried. Safety: regular-file type, size, content, and absolute-path scope checked.
