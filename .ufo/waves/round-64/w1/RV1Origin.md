# RV1Origin — C1-ORIGIN: the CRLF conversion mechanism (reconstructed contract)

Report: `.ufo/waves/round-64/after/revenger-crlf-origin.md` (full receipt: commands, full outputs,
per-commit tables, byte dumps).
captured_utc=2026-11-03T19:07:05Z

## Reconstructed contract

Committed blobs only (`git show`/`cat-file`; worktree ignored). The three files' LF→CRLF conversion
is a **whole-file byte rewriting, first CR line = 1 in every case**, followed by appends whose new
lines were CRLF. That is the signature of a **text-mode file handle on a Windows host** (CPython
`open(p,'w')` with `newline=None`: every `\n` written becomes `\r\n`), not of `core.autocrlf`
(CR is *in* the blobs; `core.autocrlf` unset at system/global/local; `git check-attr` → all
`unspecified`; the only `.gitattributes` in the tree are fixture clones under `.ufo/waves/`), not
of a checkout filter (`git ls-files --eol`: `i/crlf` SCORECARD, `i/mixed` SKILL, `i/crlf` SOURCES,
`i/lf` LOG), and not a one-shot editor conversion (contiguous LF regions map exactly to
individually-appended sections).

## Evidence chain (all read-only)

- CR counts / first-CR line at `81776bef`, `c5a33d08`, `2913b75d`, `5dd83fa3`, `44fc183b`, `2f3061ef`:
  SCORECARD first CR line **1** @ `c5a33d08`; SKILL first CR line **1** @ `2913b75d`;
  SOURCES first CR line **1** @ `2913b75d`.
- Byte-exact reconstruction: `tip == CRLF-normalise(base) + tail` holds for `c5a33d08:SCORECARD`
  (tail 51 lines, 51 CRLF/0 LF), `2913b75d:SKILL` (tail 123, 104 CRLF/19 LF), `c4aa0f5c:SKILL`
  (4990→5009 CRLF), `2f3061ef:SCORECARD` (tail 22, 22 CRLF); and `tip == base with one line
  inserted` holds exactly for `2913b75d:corpus/SOURCES.md` (insert at line 283, reconstruct == tip
  True) and every later SOURCES commit. Raw `base` byte-prefix holds for the append commits
  (`35c2748f`, `41c18296`, `dd994b92`, `136bfb00`, `541cdaea`, `f47bb0aa`, `e50973da`, `f9eee551`,
  `cdfd8b8c`, `896e3c8b`, `bef165c4`, `abb2a161`, `f3f64812`, `82f0e1a9`).
- Zero `\r\r\n` across 475 first-parent commits → each conversion is a single pass, never a
  round trip over already-CRLF bytes.
- Boundary bytes: `41c18296` base tail `...none.\n` + append head `\r\n## Round 60 ...`;
  `35c2748f` base tail `...rule).\r\n` + append head `\n## Round 59 ...`; SKILL `2913b75d`
  line 4990 ends `\r\n`, lines 4991-5009 (the appended Round-59 section) end `\n`.
- Census differential (why the Windows census passed): canonical gawk keeps the CR in `$0`
  (`len=12`, CR at 12), `trim()` strips only space/tab, so `trim(substr(line,3))=="Registry"` is
  false for `## Registry\r` → `in_registry=0` → **every** row hits the E12 arm. Measured on the
  HEAD blob: CRLF copy → E12=278, W04=0, rc 1; CR-stripped copy → E12=0, W04=42. 278 == the file's
  S-row count. Windows receipts (`35c2748f`, `52d9ba1a`) show the inverse (42 W04, 0 E-code,
  exit 0) over 377/377 and 379/379 CRLF files; the bundled gawk manual §B.3.1.3 documents the
  MinGW default — `\r\n`→`\n` on input unless `BINMODE` — and the census never sets `BINMODE`
  (`grep` rc 1).

## Divergences from the frozen C1 origin statement

1. **SCORECARD.md is already 100 % CRLF at `c5a33d08`** (r59 *declaration*; `81776bef` CR=0 →
   `c5a33d08` CR=4178/4178, delta +51/−0 under `--ignore-cr-at-eol`). "Parent `c5a33d08` is 100 %
   LF" holds only for SKILL.md and corpus/SOURCES.md; SCORECARD's origin commit is `c5a33d08`, not
   `2913b75d`. (Agrees with seat SC2Census's F6; cross-confirmed by both seats independently.)
2. **The class recurs on this Linux host**: at `2f3061ef` SCORECARD was written whole-file again and
   its 47 residual LF-only lines (4179-4225, 4539 at `44fc183b`) came out CRLF (CRLF(base) is again
   a byte prefix; +22 CRLF lines; delta 22/0 under `--ignore-cr-at-eol`), while LOG.md in the same
   commit is a clean LF byte append. So the writer emits CRLF *explicitly*; a CR-strip repair alone
   is undone by the next declaration-class write.

## Mechanism table (per file)

| file | pattern | mechanism | earliest evidence |
|---|---|---|---|
| SCORECARD.md | whole-file @ `c5a33d08` (`+51` lines, all CRLF) | Windows text-mode whole-file write | line 1 |
| SKILL.md | whole-file @ `2913b75d` (4886 LF→CRLF, +104 CRLF) then +19 LF lines from a byte appender; re-CRLF'd @ `c4aa0f5c` | text-mode write + byte-exact append | line 1 |
| corpus/SOURCES.md | whole-file @ `2913b75d` with `S274` inserted in id position (line 283); later rounds = byte-exact one-row inserts | text-mode read→insert→write (append impossible, so the same text-mode write did the conversion) | line 1 |

## Confidence

Whole-file vs append classification: **high** (byte-exact reconstruction, no judgement).
Writer behaviour (text-mode `\n`→`\r\n` on write): **high**. Writer identity (CPython vs PowerShell
`Out-File` vs editor save): **[inf]** — bytes are indistinguishable; CPython is the best fit for a
Python-tooled lane. Census-pass reason: **high**. Machine that authored `2f3061ef`'s SCORECARD
write: **[unk]** (its receipts run Linux paths and LOG.md is LF-clean in that commit, yet SCORECARD
returns all-CRLF).

## Scope note

Read-only throughout; no edit, no commit, no integration. Scratch fixture directory
`/fast/scratch/hyaku/tsukuroi-r64/RV1Origin/` used for the census CRLF/LF comparison and removed
on exit. Parallel-seat coordination: replied to SC2Census with the mechanism facts (heading-anchored
E12, the census-mode silent-zero, and the index `i/crlf` hazard covering all three files).
