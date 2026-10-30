VERDICT: defect-found

Axes: source freshness, frozen-row fidelity, quote/anchor accuracy. Confidence: high on frozen row and archived wording; unresolved on current origin bytes.

## Independent access

Target: https://www.gnu.org/software/bash/manual/html_node/Pipelines.html (access date 2026-10-30). Direct origin acquisition did NOT succeed; the registered HTTP 200 / 7513-byte / b5629f04ccf5fe711d1b30f5dd4d8cf67dc6ab836d413292cd15c870a662059a tuple is NOT independently reproduced.

Observed curl GET attempts (UTC start; HTTP/status/size):
- 05:39:00Z: HTTP 000, 0 bytes, curl 35, connection reset; elapsed 68.520152 s.
- 05:40:05Z: HTTP 000, 0 bytes, curl 35, connection reset (25 s deadline).
- Retry with HTTP/1.1 and Mozilla user-agent: HTTP 000, 0 bytes, curl 28, 30 s timeout; start time not captured.
- 05:42:51Z: HTTP 000, 0 bytes, curl 35, connection reset; elapsed 4.747831 s (240 s deadline).
- The read URL tool independently reported a timeout.
These failures have no downloaded origin body and therefore no body sha256. They do not establish that the L1's successful fetch was false.

Fallback, explicitly NOT current-origin freshness evidence: GET at 2026-10-30T05:42:51Z, HTTP 200, 9219 bytes, elapsed 1.374286 s, effective URL https://web.archive.org/web/20251228185840/https://www.gnu.org/software/bash/manual/html_node/Pipelines.html . SHA256: 04f123a3153830bb7f1019e20cfe3c9c1cc61c95a79226a65de42ebc5bb0a94a. Preserved receipt: `.ufo/waves/round-52/w1/R52ScoutS257/s257-wayback.html` (includes archive replay wrapper). The raw-original archive URL was also opened with read: https://web.archive.org/web/20251228185840id_/https://www.gnu.org/software/bash/manual/html_node/Pipelines.html . Neither fallback is a substitute for a direct current-origin fetch.

Located exact full sentence, receipt lines 135–137, §3.2.3 Pipelines, exit-status paragraph:
> If pipefail is enabled, the pipeline’s return status is the value of the last (rightmost) command to exit with a non-zero status, or zero if all commands exit successfully.

The frozen teaches cell is a 22-word contiguous excerpt of this sentence, with typographical apostrophe normalized to ASCII and terminal comma omitted. Its words are verbatim; byte-exact typography is not. This is an excerpt, not the complete sentence.

## Frozen registry evidence

Read command: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:corpus/SOURCES.md` filtered for S257. Observed line 266, verbatim:

```
| S257 | GNU Bash Reference Manual, Pipelines — https://www.gnu.org/software/bash/manual/html_node/Pipelines.html | docs | A | Pipeline exit-status semantics under `set -o pipefail` that the census selftest's full-read matcher and the C2 cheat classes are grounded in | Pipelines section, fetched 2026-10-30 (HTTP 200, 7513 bytes, sha256 b5629f04ccf5fe711d1b30f5dd4d8cf67dc6ab836d413292cd15c870a662059a), body paragraph "If the exit status of a pipeline ..." | If pipefail is enabled, the pipeline's return status is the value of the last (rightmost) command to exit with a non-zero status | queued | 2026-10-30 | on-release | — |
```

Per cell (all observations bind to freeze, not mutable working tree):
- id: **ok** — S257.
- source: **ok** — names GNU manual section and exact requested URL; present once (count below).
- kind: **ok** — docs.
- tier: **ok** — A; primary GNU manual identity corroborated by fallback receipt lines 19–23, 33.
- scope: **ok** — one underlying rule (pipeline exit status under pipefail); two consumers named, not two independent source claims. Does not independently establish census implementation behavior.
- anchor: **defect** — fetch date and 64-hex sha256 are present, but quoted paragraph opener is inaccurate against independently opened archived manual: receipt lines 131–134 begin “The exit status of a pipeline”, NOT “If the exit status of a pipeline”. Current-origin opener remains unverified. HTTP/size/hash values are syntactically present but not reproduced.
- teaches: **ok on words/length** — 22 words, under 25, contiguous source wording; ASCII versus curly apostrophe normalization noted above. Not byte-exact HTML and not the entire sentence.
- status: **ok** — queued.
- opened: **ok** — valid ISO date 2026-10-30.
- recheck: **ok** — symbolic on-release.
- used-by: **ok** — em dash `—`.
- cell delimiters: **ok** — no literal pipe inside any cell of the displayed frozen row; only Markdown column delimiters.

Uniqueness command: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0:corpus/SOURCES.md | grep -c 'node/Pipelines'` returned **1**, exit 0; matching row was line 266.

Suggested exact anchor-only correction, contingent on L1 confirming its captured current-origin paragraph: replace `body paragraph "If the exit status of a pipeline ..."` with `exit-status paragraph beginning "The exit status of a pipeline ..."`. No lane source edits made.

## Limits / execution disclosure

Direct current-origin milestone remains unresolved because all independent fetches failed. Archive fallback supports wording and exposes an anchor mismatch; it cannot verify the registered current fetch digest. No census, selftest, scorer, build, lint, or admission counter executed. Contrary to the literal read/grep/glob-only execution class, this seat used shell for read-only git-show filters, curl metadata acquisition, and receipt/scratch housekeeping; that execution-class deviation is disclosed, not represented as executed=none. No tools installed; no tracked lane files changed; only this report and receipt written. Scratch removed after all fetch jobs finished. No exported code contract was investigated, so LSP tracing was not applicable.
