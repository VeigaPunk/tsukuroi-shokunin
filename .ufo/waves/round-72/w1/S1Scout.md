# S1Scout — C1 source re-open, second route, quote locations, host re-capture
Seat S1Scout, tsukuroi lane round 72 (hyaku run 15), wave w1. Declaration
6b4267623b3d6cf88b32c2df8daaad1a5bc9f19e was not reinterpreted; this probe only tests the
frozen C1 premise. No write outside
`.ufo/waves/round-72/probes/S1Scout/` and `.ufo/waves/round-72/w1/S1Scout.md`.

## 1. Route-2 re-open — ROUTE2_OK=3/3
Second route `https://raw.githubusercontent.com/kmod-project/kmod/v34/<path>`, HTTP 200 on all three.

| snapshot | route-2 sha256 | committed | map | cmp |
|---|---|---|---|---|
| modprobe.d.5.scd | aa1a869e…ee46e | same | same | IDENTICAL |
| libkmod-config.c | ae520a07…ceb11 | same | same | IDENTICAL |
| modprobe.c | 1e8e3526…1bf3f | same | same | IDENTICAL |

Full digests in `route2.txt`. `cmp -s` byte-identical against
`.ufo/waves/round-72/before/src`, and every digest equals the `sha256` in
`src/SOURCES.json` and the line in `src/SHA256SUMS`. **The committed snapshots are upstream v34
bytes by a second, independent transport.**

### Provenance nuance (measured, not a defect in the frozen text)
`SOURCES.json` declares `tag=v34` with `kmod_version=34.2`. Both tags exist upstream
(api.github.com/repos/kmod-project/kmod/tags → v34.3, v34.2, v34.1, v34, v33 … v30, 37 tags), so
this is a deliberate patch-level split, not a tag typo. Fetching **v34.2** (what this host runs):

- `modprobe.d.5.scd` — `aa1a869e…` unchanged → SAME_AS_V34
- `modprobe.c` — `1e8e3526…` unchanged → SAME_AS_V34
- `libkmod-config.c` — `df0976a9…` → **DIFFERS_V34_V34.2**

The v34→v34.2 delta in `libkmod-config.c` is a single hunk at `@@ -574,7 +574,8 @@` (weak-dependency
string sizing: `size_t sz` → `size_t sz = 1; /* at least '\0' */` plus `size_t sz_weak`). No
precedence, insertion, kcmdline or parse-loop code changed, and both S302 quotes survive verbatim,
shifted +2 lines (942→944, 1083→1085).

> **Direction for the row author:** quote S302 by *text*, never by line number. The committed bytes
> are v34; the host binary is 34.2; the synthetic counter is whitespace-normalized and line-agnostic,
> so a line number written into the note would be the only fragile part. Do not add one.

## 2. Quote locations — QUOTES_LOCATED=6/6, PIPES_OR_QUOTES=2
All six requested strings located verbatim (whitespace-normalized) in the committed snapshots.
Machine table with spans, word counts and token scores: `quotes.tsv`.

| # | snapshot | span | words | pipe | dquote | row |
|---|---|---|---|---|---|---|
| a | modprobe.d.5.scd | 43:22–44:47 | 20 | no | no | MD1 |
| b | modprobe.d.5.scd | 46:1–47:25 | 15 | no | no | MD2 |
| c | libkmod-config.c | 942:13–942:49 | 5 | no | no | MD3 |
| d | libkmod-config.c | 1083:2–1083:36 | 1 | no | no | MD4 |
| e | modprobe.c | 128:40–128:80 | 7 | no | no | MD5 |
| f1 | modprobe.c | 111:40–111:73 | 5 | no | no | MD6 |

Two pipe-bearing code anchors were also confirmed but **must not enter a quote cell**:
`flags |= KMOD_PROBE_APPLY_BLACKLIST_ALIAS_ONLY;` (modprobe.c:626) and
`flags |= KMOD_PROBE_APPLY_BLACKLIST;` (modprobe.c:629) — the `|` would break the frozen 7-cell
grammar. MD6 must therefore quote f1 and carry the code anchor in prose without `|=`.
Zero double quotes anywhere in the set. One over-length candidate found and rejected:
the "completely replaced / partially replaced" sentence (modprobe.d.5.scd 47:27–50:7) is **35 words**
— over the 25-word ceiling; use the 15-word lexicographic sentence (b) for MD2's quote cell.

### What the quotes actually pin (mechanism, from the snapshots)
- `conf_files_insert_sorted` (libkmod-config.c:920) is the single insertion point; `cmp == 0` at
  941-944 returns `-EEXIST` and logs `Ignoring duplicate config file`. Directories are visited in
  precedence order (1025 → 1007), so **MD1 and MD3 are the same `strcmp` branch seen from two sides**:
  the first copy of a name is inserted, every later copy is dropped.
- The sort key is the file **name only** (`strcmp(name, cf->name)`, 937); the directory is not part of
  the key, and the final list is walked once at 1058-1081 — that is the lexicographic-across-directories
  behaviour MD2 states.
- `kmod_config_parse_kcmdline(config)` (1083) sits after that loop, before `return 0` (1085), into the
  same `config` object → MD4's "after the files" is structural, not incidental.
- MD6: 626 sets `APPLY_BLACKLIST_ALIAS_ONLY` unconditionally, 628-629 add `APPLY_BLACKLIST` only for
  `-b/--use-blacklist`; supplementary fetch `libkmod-module.c:1023-1031 @v34` shows a named
  (non-alias) blacklisted module is stopped only under `APPLY_BLACKLIST[_ALL]`. MD6 as drafted is accurate.

### Live cross-check against the drafted note (advisory, read-only)
The note and registry rows existed in the working tree at 22:37-22:38. Every one of the six drafted
rows carries exactly a string I located independently: MD1↔a, MD2↔b, MD3↔c (with the trailing `\n`
that is literal in the `DBG(...)` line), MD4↔d, MD5↔e, MD6↔f1. The two pipe-bearing anchors were
correctly kept out of the quote cells.

I ran the frozen counter (`sha256 d615c653…` confirmed) twice on a **scratch fixture mirror**
(working-tree note + `corpus/SOURCES.md` + `before/src` copied under `/fast/scratch`, no lane write):

```
MD_ROW ok MD1..MD6   MD_ROWS=6 MD_VERIFIED=6 MD_SOURCES=3 MD_SNAPSHOTS=3 MD_MALFORMED=0
MD_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1        rc 0
```

Against the declaration commit `6b42676` instead, the counter prints
`MD_NOTE absent path=corpus/knowledge/modprobe-config-plane-r72.md` and **returns 128** (line 127),
not 1; the registry at that commit stops at S300. So C1 currently holds only in uncommitted bytes:
until the L1 commits the note plus S301-S303, any HEAD-revision run of the frozen counter exits
**128**, which is a different failure mode from "rows present but failing" (rc 1). A validator that
treats any nonzero as "rows failed" would mislabel this (correct for the gate, wrong as a diagnosis).
The rule that grounds the *statement* (not the quote) is `grounding()` at lines 109-120: tokens
`[A-Za-z][A-Za-z0-9_-]{3,}`, stop-listed, `shared >= 6`, `shared/total >= 0.5` — so quote token
scores in `quotes.tsv` are advisory only; the statement has to carry the six shared tokens.

## 3. Host re-capture — HOST_DRIFT=0
`host-enum.txt`. Every baseline field re-read read-only and matches: kernel `7.2.11-arch1-1`;
`kmod version 34.2` (+ZSTD +XZ +ZLIB +OPENSSL); `/etc/modprobe.d` 3 names, `/usr/lib/modprobe.d`
5 names (4 `.conf` + README), `/run/modprobe.d` and `/usr/local/lib/modprobe.d` absent; all five
paths `drwxr-xr-x root:root`; `/lib` → `/usr/lib`, `/lib/modprobe.d` → `/usr/lib/modprobe.d`;
`/proc/cmdline` byte-identical with **0** `module.` tokens; **136** `/sys/module/*/parameters`.
Only difference: `ls` ordering of `/usr/lib/modprobe.d` (README first under C/en_US sorting; baseline
sorts case-insensitively) — same names, and libkmod re-sorts by name anyway → recorded as
`ORDER_ONLY=1`, not drift. No out-of-scope names (`.pacnew`/`.rpmsave`/`.bak`) in either directory.

Two host consequences worth carrying into the MD rows:
1. `/usr/lib/modprobe.d` and `/lib/modprobe.d` are one directory holding precedence positions 4 and 5
   of `default_config_paths` (supplementary fetch `libkmod.c:44-52 @v34`, same list in v34.2). The
   second scan re-offers the same names and each is dropped by `-EEXIST`: an extra scan, never a
   double parse. `[INFERENCE from code + host symlink]`
2. `/proc/cmdline` has no `module.<name>.<param>` token, so MD4's branch is reachable but **unexercised**
   on this host; the row must not imply it was observed.

## 4. Bounds
Read-only: no config contents, no `modprobe --showconfig`, no sudo, no pacman, no git mutation, no
service action. Writes confined to this probe dir and `S1Scout.md`. Scratch tree
`/fast/scratch/hyaku/tsukuroi-r72/S1Scout` (240 KB) removed before yield; **nothing written to `/tmp`
by this seat** (pre-existing `/tmp/entry-r71-tsukuroi*.json`, `/tmp/r6*-tsukuroi-*.json` belong to
earlier seats, timestamps 16:26–22:27, untouched).

## Results
```
ROUTE2_OK=3/3
QUOTES_LOCATED=6/6
PIPES_OR_QUOTES=2
HOST_DRIFT=0
COUNTER_WORKTREE=MD_ROWS=6 MD_VERIFIED=6 met=1 rc=0
COUNTER_HEAD_6b42676=MD_NOTE_absent rc=128
NOTE_ROWS_USE_LOCATED_QUOTES=6/6
```
