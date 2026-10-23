# RevSourceS171 — wave-2 re-open of source S171 (man-pages 6.19 ld.so(8))

Verdict: **holds** — S171 is a genuine, independently re-openable tier-A source; its pinned bytes, quote, and taught conditions all verify. One registry defect found: the S171 row's `used-by` cell names two files (the probe tool and `corpus/QUALITY.md`) that do not cite S171 at tip f3a5723.

## Findings (severity order)

1. **[obs] `used-by` cell overstates citations (registry defect).** `corpus/SOURCES.md` line 265 lists `tools/probe-git-child-env-r31.py, corpus/QUALITY.md, corpus/lessons/round-31.md` as used-by. All three files exist at f3a5723 (`test -f` rc=0), but only `corpus/lessons/round-31.md` cites S171 (lines 3, 18, 22). `grep -c 'S171'` = 0 for `tools/probe-git-child-env-r31.py` (364 lines) and 0 for `corpus/QUALITY.md` (155 lines); both also contain zero matches for any of `S17`, `ld.so`, `man-pages`, `6.19` (case-insensitive). Repo-wide `grep -rn -l 'S171'` (excluding `.ufo/waves`) finds only `corpus/lessons/round-31.md` and `corpus/SOURCES.md`. Two of three listed used-by files fail the "cite S171" criterion.
2. **[obs] No other registry cell fails.** id, source URL (identical to the fetched URL), kind `docs`, tier A, status `mined`, opened 2026-10-22, recheck `on-release` all match the Gate row (round-31.md line 18) and the registry-changes note (round-31.md line 22: S171 absent → `mined`, recheck `on-release`).

## Evidence per check

- **Re-open fetch**: `curl -sL --fail 'https://git.kernel.org/pub/scm/docs/man-pages/man-pages.git/plain/man/man8/ld.so.8?h=man-pages-6.19'` rc=0; saved bytes `sha256 dbb71df461480514e839669ec3fcecfaa68a2079f8f735df17cdf512d4b792cc`, 937 lines / 28174 bytes. Identical to the row anchor sha256 and to the committed snapshot `.ufo/waves/round-31/w1/ScribeSrcLdSo/ld.so.8` (same digest, same `wc -l -c`). [obs]
- **Gate row quote**: round-31.md line 18 located-quote `"objects to be loaded before all others."` (7 words, one line) — `sed -n '436p' <snapshot> | grep -cF 'objects to be loaded before all others.'` printed `1`. [obs]
- **Installed version**: `pacman -Q man-pages` → `man-pages 6.19-1`, matching the Gate decision's "man-pages release installed on the host, 6.19". [obs]
- **Teaches keeps every condition** (SOURCES.md line 265 teaches cell vs pinned lines):
  - "LD_LIBRARY_PATH adds execution-time shared-library search directories" — lines 396-401 ("A list of directories in which to search for ELF libraries at execution time"); "is ignored in secure-execution mode" — line 403. [obs]
  - "LD_PRELOAD loads user-specified ELF objects before others and can override functions" — lines 435-439 ("A list of additional, user-specified, ELF shared objects to be loaded before all others. This feature can be used to selectively override functions"); secure-mode path/directory restrictions — lines 445-449 ("preload pathnames containing slashes are ignored... preloaded only from the standard search directories and only if they have set-user-ID mode bit enabled"). [obs]
  - "LD_AUDIT loads audit objects before others in a separate linker namespace" — lines 498-501; "is ignored in secure mode" — line 507. [obs]
  - "secure-execution may void or modify and strips these environment variables" — lines 291-296 ("the effects of some environment variables are voided or modified, and furthermore those environment variables are stripped from the environment"); the stripped list at lines 303-317 includes LD_LIBRARY_PATH, LD_PRELOAD, LD_AUDIT; "with AT_SECURE indicating the mode" — lines 322-329 ("A binary is executed in secure-execution mode if the AT_SECURE entry in the auxiliary vector... has a nonzero value"). [obs]
- **Anchor cell**: tag `man-pages-6.19` appears in the fetched URL; cited line ranges (27-28, 291-341, 396-403, 434-450, 497-540) cover exactly the four taught conditions; snapshot path exists at tip with matching byte/line counts and the recorded digest. [obs]

## Residual risk / verification gaps

- [unk] I cannot independently prove the kernel.org cgit tag mapping (`?h=man-pages-6.19`) server-side; strongest available evidence is that my independent fetch from that URL reproduces the pinned sha256 exactly.
- [inf] The teach-cell checks are semantic line-by-line mappings; each condition was located in the cited source lines and quoted above.

Scope: read=corpus/SOURCES.md S171 row, corpus/lessons/round-31.md Gate rows, SKILL.md round31 registry rows, .ufo/waves/round-31/w1/ScribeSrcLdSo/{ld.so.8,S171-row.md,S171-gate.md, ScribeSrcLdSo.md}, fresh fetched ld.so.8 bytes, pacman -Q man-pages; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevSourceS171.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevSourceS171/ld.so.8.fetch; executed=curl -sL --fail (fetched ld.so.8), sha256sum, wc -l -c, sed -n ... | grep -cF, grep -c/-n, pacman -Q man-pages, git clone/checkout (read-only sandbox)
Model: inception/mercury-3
Installs: none
