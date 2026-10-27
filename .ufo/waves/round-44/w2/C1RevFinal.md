VERDICT: defect-found
Seat: C1RevFinal (L2, tsukuroi r44 w2, hyaku 9) — Item C1-8, final arm review
Reviewed revision: 8eee79db608b5815c325a5af7cbfdeac50eda9f4 (scratch clone at /fast/scratch/hyaku/tsukuroi-r44/C1RevFinal/lane, toplevel asserted, clean). All citations are line numbers of `tools/tsukuroi-census.sh` at that revision. No lane or fixture mutations; selftest run with TMPDIR in my scratch.

## F1 — MEDIUM: the header contract sentence for the scrub arm is truncated at the integrated tip

`tools/tsukuroi-census.sh:404-405` reads:

    # scrub_speed_max is unreadable or not one decimal line (<fsid8>:<devid>:speed-unreadable,
    # NONE. Globs run under LC_ALL=C, so the detail order is bytewise. ...

The parenthetical opens and never closes; the sentence is broken. `git diff ab8aae16..8eee79db -- tools/tsukuroi-census.sh` shows the integration commit 071ab0d1 ("wave-1 integration") deleted exactly two header lines that ab8aae16 (the C1 arm commit) had:

    -# speed-malformed) or whose devid is not decimal (<fsid8>:?:bad-devid), records present with no
    -# sysfs root to judge orphans by (sysfs:absent); else RECORDED when records+tmp+sockets > 0; else

Losses at the reviewed revision, each contradicted by live code:

1. The RECORDED state trigger is now documented nowhere in the header, while the code implements it (`:2038` `elif [ $((rec + tmp + sock)) -gt 0 ]; then state=RECORDED`) and selftests assert it (3313-3314, 3247-3248). The header's state enumeration now reads BLOCKED → NONE with no RECORDED condition.
2. `speed-malformed` (code 1985-1988, selftests 3302-3303, 3260-3261) and `bad-devid` (code 1982) BLOCKED tokens are undocumented.
3. The `sysfs:absent` BLOCKED clause (code 2020, selftest 3288-3289) is undocumented.

This is the normative contract the seat chain reviews against and that C2 sources rows from; at the frozen tip it is corrupt and understates the implemented state machine.

## F2 — LOW: w1-hardened behavior was never added to the header enumeration

Same integration commit added `sysfs:not-directory` (code 2019, selftest 3325-3326) and the timer not-a-directory exclusion (code 2032, selftest 3328-3331, commit 8eee79db "timers case guards plain btrfs-scrub.timer (mutant k)"), but the header sentences at 397-405 document neither: the timers sentence (399-400) names only the bare-template exclusion. Header understates implemented semantics; a reader binding to the header alone would call the extra BLOCKED reasons uncontracted.

## Verified-good (evidence)

- Verdict-neutral placement: `main` prints the SCRUB line between STORAGE and the rollup (3418-3421); the rollup is composed only from PKG/SYS/DRV/JRN/UPD/OOM verdicts (3423-3429) — no PLANE text, rollup term, or exit-code change; `probe_scrub_record` returns 0 (2042).
- `set -euo pipefail`: declared at 451 for the whole script (dispatcher: `set -uo pipefail`, 2058). The probe is errexit-safe: every loop guard is an AND/OR list (`[ -e ... ] || continue` 1977/1981, `[[ =~ ]] || continue` 1979, `[ -d "$e" ] && continue` 2032 — failing non-last command of an AND-list), the only `while read` is a loop condition (1986-1987), and all arithmetic uses `$(( ))` expansion, never `(( ))`.
- QUALITY 84 (echo only validated tokens; corpus/QUALITY.md:165): PASS. Echoed names are enums (state/dir, 2037-2039), integer counters, fixed reason tokens, and host names only in validated form: fsid8 from a regex-matched lowercase UUID (1978-1979), devid validated `^[0-9]+$` with literal `?` substituted when bad (1982), speed_max validated `^[0-9]+$` (1986-1988). Non-conforming names (`scrub.status.NOT-A-UUID`, 3238; a forged newline-suffixed record name, 3280) are ignored and never echoed; the ABSENT assertion holds (3283).
- Timers branch (2024-2034): absent wants dir → timers=0 (2024, case 3232-3233); exists-but-not-listable → BLOCKED `timers:unreadable` (2026-2027); bare template `btrfs-scrub@.timer` excluded (2031); directory-shaped entries excluded (2032); instance symlinks counted by link name. Case 3270-3275: 2 instance links counted, template/`fstrim.timer`/plain `btrfs-scrub.timer` not. Case 3328-3331: directory `btrfs-scrub@x.timer` not counted. Dangling links count (`[ -e ] || [ -L ]`, 2030).
- Not-directory/absent sysfs branch (2017-2020): fires only when a record exists and sysfs was not scannable; listable-dir-with-no-permission already flagged `sysfs:unreadable` (1972-1973) and is not double-reported (2018); existing non-directory root → `sysfs:not-directory` (2019, case 3325-3326, fixture overwrites the root with a regular file at 3323); missing root → `sysfs:absent` (2020, case 3288-3289).
- Selftest re-run at 8eee79db: `TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)`, exit 0, 16/16 `(R44-C1)` cases PASS (37 s). Receipt: `.ufo/waves/round-44/w2/C1RevFinal/selftest-rerun-8eee79db.out`.

## Residual risk / gaps

- `timers:unreadable` (2026-2027) has no selftest case; a mutant in that arm would survive the suite (dir:unreadable is covered at 3266-3267).
- `bad-devid` (1982) has no selftest case and, after F1, no header documentation either.
- `scrub_speed_max` CRLF/whitespace variants are handled by the one-decimal-line rule (1985-1988) but unexercised.

## Proposed text (L1 to integrate)

Replace tip lines 404-405 with:

    # scrub_speed_max is unreadable or not one decimal line (<fsid8>:<devid>:speed-unreadable,
    # speed-malformed) or whose devid is not decimal (<fsid8>:?:bad-devid), records present with no
    # sysfs root to judge orphans by (sysfs:absent, or sysfs:not-directory when the root exists but
    # is not a directory); else RECORDED when records+tmp+sockets > 0; else
    # NONE. Globs run under LC_ALL=C, so the detail order is bytewise. Known limit: an absent sysfs root

and extend the timers sentence at 399-400: "…the bare template name is not an instance and is not
counted, nor is an entry that is a directory)."
