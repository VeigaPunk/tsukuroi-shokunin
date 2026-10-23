# RevSourceS173 — wave-2 source review of S173 (strace v7.2 doc/strace.1.in)

Verdict: **holds** — the S173 fetched bytes, committed snapshot, anchor and Gate row all agree, and every condition in the teaches cell is grounded in the pinned manual lines. One minor finding: the used-by cell lists `tools/probe-git-child-env-r31.py`, which exists at the revision but never cites the string `S173`, unlike the used-by convention observed in other rows (knowledge files cite the id literally).

Reviewed at lane revision f3a5723a988bf1c2835985880e7a38d477462cd0 (sandbox `/fast/scratch/hyaku/tsukuroi-r31/RevSourceS173/repo`).

## Findings

1. [obs] Fetched bytes match the anchor and the committed snapshot exactly.
   - Command: `curl -sL -o .../w2/RevSourceS173/strace-v7.2-doc-strace.1.in https://raw.githubusercontent.com/strace/strace/v7.2/doc/strace.1.in`; `sha256sum` gives `c16859e07dacc5cda882c7ab5f2e353803645a6ca449a0ac41eda1034e67ae9a`, `wc -c` = 60347, `wc -l` = 2242.
   - Committed snapshot `/fast/scratch/hyaku/tsukuroi-r31/RevSourceS173/repo/.ufo/waves/round-31/w1/ScribeSrcStrace/strace-v7.2-doc-strace.1.in` has the identical sha256 and 60347 bytes; `git ls-files --error-unmatch` confirms it is tracked at the revision.
   - Anchor row (SOURCES.md:267) claims sha256 `c16859e07dacc5cda882c7ab5f2e353803645a6ca449a0ac41eda1034e67ae9a`, 60347 bytes, 2242 lines — all three match the fetched bytes. `curl -sL -o /dev/null -w "%{http_code}"` returned `200`.
2. [obs] Gate row quote verified verbatim at the claimed line in both the fetched bytes and the committed snapshot.
   - Gate row: `corpus/lessons/round-31.md:20`, quote (13 words <= 25): "Prints unabbreviated versions of environment, stat, termios, etc. calls." at manual line 1278, sha256 `c16859e07dacc5cda882c7ab5f2e353803645a6ca449a0ac41eda1034e67ae9a`.
   - `sed -n '1278p' <fetched> | grep -cF 'Prints unabbreviated versions of environment, stat, termios, etc. calls.'` → `1`; same against the committed snapshot → `1`.
3. [obs] Installed-version anchor claim reproduced: `strace -V` prints `strace -- version 7.2` (also `curl -sL -w` HTTP 200 on the tagged URL).
4. [obs] Teaches cell keeps every condition; each is grounded in the anchor line ranges (fetched bytes, verified by `sed -n` extraction):
   - `-f` traces fork/vfork/clone children — lines 437-446 ("Traces child processes … as a result of the fork(2), vfork(2) and clone(2) system calls.").
   - `-qq` suppresses attach, detach, personality-change, exit-status messages — lines 1171-1175 ("Suppresses messages about attaching, detaching, personality changes, and process exit status.").
   - `-v` prints environment calls unabbreviated — lines 1275-1281 ("Prints unabbreviated versions of environment, stat, termios, etc. calls.").
   - `-v` disables default structure abbreviation — lines 837-853 ("The default is --abbrev=all. The -v option has the effect of --abbrev=none.").
   - `-s` bounds each printed string — lines 1204-1208 ("Specifies the maximum string size to print (the default is 32).").
   - strings beyond the limit are followed by an ellipsis — lines 220-226 ("Only the first strsize (32 by default) bytes of strings are printed; longer strings have an ellipsis appended following the closing quote.").
   - filenames are exempt — lines 1204-1208 ("Note that filenames are not considered strings and are always printed in full.").
   - Verdict per cell: id/source/kind/tier/scope/anchor/teaches/status/opened/recheck all hold against the Gate row and the fetched manual.
5. [obs] Used-by cell: `corpus/lessons/round-31.md` exists at the revision and cites S173 (line 20 Gate row; line 3: "its observation method S173"). `tools/probe-git-child-env-r31.py` exists at the revision (tracked, executable) but contains no `S173` citation: `grep -n "S173" tools/probe-git-child-env-r31.py` → no output (exit 1); `grep -rn "S17" tools/` → no hits.
   - [inf] The used-by convention in this registry is literal id citation: `corpus/knowledge/closeout-r11.md` cites `S031` (1 hit), `corpus/knowledge/snapper-eacces-mechanism.md` cites `S034` (5 hits), `corpus/knowledge/root-dac-decision-r12.md` cites `S038` (8 hits). The probe tool names `strace` flags (docstring lines 13, and invocation `-f -qq -v -s 65536` at line 220) but never the id, so it deviates from the convention.
   - Note: the probe tool is a substantive user of the source's semantics (`strace -f -qq -v -s 65536` at `tools/probe-git-child-env-r31.py:220` matches the taught flags), so this is a citation/hygiene gap, not a falsification of the claim. No other used-by citation site for S173 is missing: `grep -rn "S173"` across `.py`/`.md`/`.json`/`.sh` (excluding `corpus/SOURCES.md` and `corpus/lessons/round-31.md`) finds only the wave-1 scribe drafts under `.ufo/waves/round-31/w1/ScribeSrcStrace/`.

## Residual risk / verification gaps

- [unk] The host-install claim "strace -- version 7.2" was verified on this host today; the row's `-V` observation predates the fetch but matches.
- [unk] I did not exercise the probe tool itself (read-only review; no probe run was requested for this seat).

Scope: read=strace v7.2 manual (fetched bytes + committed snapshot), corpus/SOURCES.md S173 row, corpus/lessons/round-31.md Gate row, tools/probe-git-child-env-r31.py, wave-1 scribe report, used-by citation convention samples; wrote=.ufo/waves/round-31/w2/RevSourceS173.md, .ufo/waves/round-31/w2/RevSourceS173/strace-v7.2-doc-strace.1.in (fetched bytes); executed=curl -sL, sha256sum, wc -c/-l, sed -n '1278p' | grep -cF, grep -n/-rn, git ls-files --error-unmatch, strace -V
Model: not exposed
Installs: none
