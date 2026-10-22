# RevSrcS142 — independent re-open of source S142

Verdict: holds. Source S142 re-opens cleanly, the fetched bytes match the anchor hash and the committed snapshot exactly, both Gate quotes are located at the stated lines, and the teaches and scope cells are faithful to the source under QUALITY 66.

## Findings

1. Re-open succeeded. `curl -fsS https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/panic.h` returned bytes without error; 113 lines, sha256 `f9f64576a0aab7ad06c003ba4fffe4729def421a532a50ee36a813c90d37c6a8` (command output at /fast/scratch/hyaku/tsuku27a2/RevSrcS142/panic.h). Agree.

2. Anchor cell agrees with fetched bytes. The S142 row at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md:148 writes `raw bytes sha256 f9f64576a0aab7ad06c003ba4fffe4729def421a532a50ee36a813c90d37c6a8; snapshot .ufo/waves/round-27/sources/S142.h (113 lines)` and cites lines 83 and 84. Fetched sha256 is identical and the file is 113 lines. Agree.

3. Committed snapshot is byte-identical to the freshly fetched source. `sha256sum` of /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/sources/S142.h gives the same `f9f64576a0aab7ad06c003ba4fffe4729def421a532a50ee36a813c90d37c6a8` and `diff -q` reports the files identical. Agree.

4. Gate quote 1 holds. /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-27.md:16 quotes `#define TAINT_OOT_MODULE 12` located at `include/linux/panic.h line 83`. Fetched line 83 is `#define TAINT_OOT_MODULE\t\t12` — same tokens, tab whitespace normalized to a space, which the round-27 declaration explicitly allows (whitespace-normalised substring, SCORECARD.md:1000). Word count 4, at most 25, at the stated line. Agree, with an [obs] that the literal bytes use tabs, not a single space.

5. Gate quote 2 holds. lessons/round-27.md:17 quotes `#define TAINT_UNSIGNED_MODULE 13` at line 84; fetched line 84 is `#define TAINT_UNSIGNED_MODULE\t13`. Same whitespace normalization observation; 4 words, correct line. Agree.

6. Teaches cell is faithful (QUALITY 66, corpus/QUALITY.md:133). SOURCES.md:148 teaches `TAINT_OOT_MODULE is bit 12 and TAINT_UNSIGNED_MODULE is bit 13` — this is exactly what lines 83 and 84 state, no dropped branch and no words like "only" that lack a source sentence. Agree.

7. Scope cell is accurate. `Taint bit numbers for the host kernel 7.2.11` is supported: the file defines bits 0–19 (TAINT_PROPRIETARY_MODULE 0 at line 71 through TAINT_FLAGS_COUNT 20 at line 91), and a drift check of the actually installed release — `curl https://raw.githubusercontent.com/gregkh/linux/v7.2.11/include/linux/panic.h` — returns sha256 `f9f64576a0aab7ad06c003ba4fffe4729def421a532a50ee36a813c90d37c6a8`, identical to the v7.2 tag bytes, so pinning v7.2 describes 7.2.11 without drift. Agree.

8. Downstream use is consistent [obs]. corpus/knowledge/kernel-taint-r27.json rows cite S142 twice with the same quotes and locations (json lines 33–40), matching the KT1 claim `12288 = bit 12 (O) + bit 13 (E)` in kernel-taint-r27.md:18; 2^12 + 2^13 = 12288 checks out.

No actionable defect found on this source. Residual risk: none identified beyond the normalized-whitespace note, which the declaration's own rule permits.

Scope: read=SOURCES.md S142 row, lessons/round-27.md Gate rows, kernel-taint-r27.md/.json KT1, corpus/QUALITY.md:133, SCORECARD.md declaration lines, fetched panic.h (v7.2 and v7.2.11); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w2a2/RevSrcS142.md plus scratch fetches under /fast/scratch/hyaku/tsuku27a2/RevSrcS142/; executed=curl (2 fetches), sha256sum, diff, wc, grep, sed (read-only)
Model: not exposed
Installs: none
