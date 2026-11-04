# Round-77 source rows — ScribeSources draft

Draft only, for L1 disposition. The current working registry already contained S324–S326 when read; do not append duplicate IDs. Existing S320 teaches must remain unchanged. This draft independently reopens the sources and makes the replacement of the smaller-of interpretation explicit.

## Registry

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S324 | systemd v262 src/fundamental/macro.h — https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro.h | code | A | LESS_BY saturated subtraction and CLAMP arithmetic for finite journald worked examples, not minimum-of-free-and-keep_free | macro.h at v262, lines 320-350: LESS_BY 320-326 and CLAMP 337-349; sha256 1bd38a180b2cccacf0732e3e5b6388ac3d71e453839236c388501080a11a75b8 | LESS_BY(a,b) returns a-b when a>b, otherwise zero, not min(a,b); CLAMP tests high first, then low, then returns x; use ordered bounds and non-overflowing inputs | mined | 2026-11-04 | on-release | corpus/knowledge/journald-space-arithmetic-r77.md, corpus/knowledge/journald-space-arithmetic-r77.json, corpus/lessons/round-77.md |
| S325 | systemd v262 src/journal/journald-manager.c — https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c | code | A | Corrected cache_space_refresh arithmetic, superseding only S320's smaller-of interpretation | journald-manager.c at v262, lines 143-186: arithmetic 168-171 and patch_min_use 176-186; sha256 428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2 | supersedes S320 — replace smaller-of free space and keep_free with saturated subtraction: avail=max(free-keep_free,0); limit=CLAMP(used+avail,min_use,max_use); available=max(limit-used,0). patch_min_use separately raises min_use to at least current usage; these finite examples do not establish startup-normalized metrics | mined | 2026-11-04 | on-release | corpus/knowledge/journald-space-arithmetic-r77.md, corpus/knowledge/journald-space-arithmetic-r77.json, corpus/lessons/round-77.md |
| S326 | Unavailable systemd v262 src/fundamental/macro-fundamental.h — https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro-fundamental.h | code | A | Screened filename only; no arithmetic support | Opened 2026-11-04; HTTP 404; quote null; no source payload anchor or digest asserted | REJECTED: this exact v262 URL returns HTTP404, so no located source quote supports a rule; flip: the exact version-pinned URL becomes reachable and provides a located relevant quote, followed by fresh review. Actual opened macro.h is S324, not evidence this rejected URL works | rejected | 2026-11-04 | on-release | corpus/lessons/round-77.md |

## Draft Gate

Each admitted quote below is a single exact source line, under 25 whitespace words. Macro LESS_BY and CLAMP are read together at 320-350; the short quote is not a substitute for that full anchor.

| id | URL | opened | disposition | located quote | reason / flip |
|---|---|---|---|---|---|
| S324 | https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro.h | 2026-11-04 | admit, bounded code support | macro.h:325: `UNIQ_T(A, aq) > UNIQ_T(B, bq) ? UNIQ_T(A, aq) - UNIQ_T(B, bq) : 0;` (13 words, trailing continuation omitted) | The positive-difference branch and zero alternative establish saturated subtraction; CLAMP high/low order is at 344-348. Flip: fresh version-pinned bytes contradict these expressions |
| S325 | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c | 2026-11-04 | admit, scoped supersession | journald-manager.c:168: `avail = LESS_BY(vfs_avail, metrics->keep_free);` (4 words) | Together with S324, replaces smaller-of with saturated free-minus-keep_free; limit and remaining allowance are at 170-171. Flip: a source revision actually using minimum |
| S326 | https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro-fundamental.h | 2026-11-04 | reject | null | Independently reopened exact URL returned HTTP 404. No code quote can be located. Flip: exact version-pinned URL becomes reachable with a located relevant quote; review anew |

## Interpretation boundary

The six pinned examples are small non-overflowing uint64 values with min_use <= max_use. A2/A3 exercise exhausted/equal reserve; A4 the upper clamp; A5 the lower clamp; A6 used above max with zero remaining allowance. Reading patch_min_use does not authorize treating arbitrary example inputs as startup-normalized manager state. No live journald state, service action, retention outcome or universal arithmetic proof is claimed. Neither C1 nor C2 was executed by this seat.
