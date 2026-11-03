# C1 attack review — seat R1C1Rev — round 64 w1

UTC stamps inline per section (host local time is UTC-3). Reviewer attack on the frozen C1
predicates (a)–(d), LOG.md "Round 64 — declaration", base commit 2f3061ef725abebd8cd157b778203f1cf5c0cb0c
(parent 44fc183b). Every command below was run by this seat; nothing was trusted from E1's receipts.
Environment: Python 3.14.8, git 2.56.0, lane HEAD = 2f3061ef (pinned via `git rev-parse HEAD`, rc 0).
Scratch: /fast/scratch/hyaku/tsukuroi-r64/R1C1Rev (one `git clone --shared` clone; deleted after this
receipt was written). Tools installed by this seat: none.

Precondition poll (2026-11-03T18:38:34Z) — met on the FIRST check, no 60 s waits consumed:
- `ls -la tools/check-line-endings-r64.py` → `-rwxr-xr-x 1 vgpnk vgpnk 11859 Nov  3 15:38 ...`
- CR counts (`tr -cd '\r' | wc -c`): corpus/SOURCES.md 0, SKILL.md 0, SCORECARD.md 0.

## 1. Predicate (a) — census exits 0, zero E-code, 42 W04 (2026-11-03T18:38:49Z)

$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi

tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
[… 40 further W04 rows, S042–S265, elided here; full stream captured in the seat scratch receipt, counts below …]
tsukuroi	W04	S265 duplicate url learn.microsoft.com/.../sc-query across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
rc=0

- E-code lines: `grep -c 'E[0-9][0-9]' census.out` → **0** (required 0)
- W04 lines: `grep -c 'W04' census.out` → **42** (disclosed exactly; the declaration predicted the
  42 W04 duplicate-url warnings reappear — they do, same count as the r63 receipts entry)
- exit rc = 0

**Verdict (a): PASS.**

## 2. Predicate (b) — identity: CR removal only + attack on the proof itself (2026-11-03T18:38:49Z, re-verified 18:40:53Z)

Per file F ∈ {corpus/SOURCES.md, SKILL.md, SCORECARD.md}:

$ git show 2f3061ef:F | tr -d '\r' | cmp - F
rc=0   (silent) for all three files

Attack on the proof: `tr -d '\r'` deletes EVERY 0x0D byte, so a mid-file CR in the blob would be
invisible to cmp while surviving in the worktree. Independent byte-level counts (python3, 0x0D/0x0A
census over the blob and the worktree file):

| file               | blob@2f3061ef size | blob CR | blob stray-CR-not-before-LF | blob CRLF pairs | worktree size | worktree CR | size delta == CR? |
|--------------------|--------------------|---------|------------------------------|-----------------|---------------|-------------|-------------------|
| corpus/SOURCES.md  | 279287             | 381     | 0                            | 381             | 278906        | 0           | 381 == 381 ✓      |
| SKILL.md           | 1356990            | 5452    | 0                            | 5452            | 1351538       | 0           | 5452 == 5452 ✓    |
| SCORECARD.md       | 773314             | 4723    | 0                            | 4723            | 768591        | 0           | 4723 == 4723 ✓    |

- Worktree CR bytes: **0 / 0 / 0** — no CR of any kind survived anywhere in any of the three files.
- Blob stray CR (mid-file / CR not before LF): **0 / 0 / 0** — the pre-state was trailing-CR-only
  (pure CRLF line endings), matching the declaration's description; normalization removed exactly
  those bytes (size delta equals CR count per file).
- Byte-exact confirmation (2026-11-03T18:40:53Z): sha256(`git show 2f3061ef:F | tr -d '\r'`) ==
  sha256(worktree F) for all three:
  - corpus/SOURCES.md e1558e4b3eeef8857e27a64299e08c50e52c3b9f5f2160a09cd6647e90c3df77
  - SKILL.md          bda5249b161e7442f056e924c9091331ac091a6d38e49bbcd762a93ad331c85d
  - SCORECARD.md      1304750516c86ab17a1cdb0ee0df956e26aed25ae7e5f73bb2130b2e2c89df66
- Kill rule not triggered: no content change beyond CR removal was needed to reach rc 0.

Reconciliation of the before-numbers: `crlf-inventory-receipt.txt` (2026-11-03T18:00:04Z) ends with
`SCORECARD.md 4654/4701`, and I reproduce exactly 4654 CR / 4701 LF at **44fc183b**. The declaration
commit 2f3061ef itself then added 69 more CRLF lines to SCORECARD.md (4723/4723 at the fix base);
SOURCES.md and SKILL.md are byte-identical at both revs. LOG.md quoted the receipt faithfully for its
measurement moment; the fix normalized the later, larger state. Disclosure nuance only — see §6 F3.

**Verdict (b): PASS.**

## 3. Predicate (c) — guard selftest + full-tree check (2026-11-03T18:39:06Z)

$ python3 tools/check-line-endings-r64.py --selftest     (cwd = lane repo)

check-line-endings-r64 selftest (fixtures under /fast/scratch/hyaku)
  lf-file-passes                       PASS
  crlf-file-fails-naming-path          PASS
  allowlisted-ufo-path-ignored         PASS
  cr-at-eof-without-newline-flagged    PASS
  cr-midline-flagged                   PASS
CHECK_LINE_ENDINGS_SELFTEST: PASS (5 cases, 5 passed, 0 failed)
rc=0

(The required case mix is present: a CRLF-fixture kill and the allowlisted `.ufo/**` capture.)

$ python3 tools/check-line-endings-r64.py --check         (cwd = lane repo)
CHECK_LINE_ENDINGS: PASS (326 file(s) checked, 0 violation(s))
rc=0

**Verdict (c): PASS.**

## 4. Predicate (d) — mutant with a DIFFERENT injection point (2026-11-03T18:40:18Z)

Scratch clone: `git clone --shared <lane> <scratch>/clone` (rc 0; `git rev-parse --show-toplevel`
printed the clone dir). The clone's checked-out HEAD state is the CRLF state, so the three files
were first replaced with the LF worktree copies (cp; CR counts re-checked 0/0/0) and the guard run
clean: `CHECK_LINE_ENDINGS: PASS (326 file(s) checked, 0 violation(s))` rc 0 — clean baseline.

$ printf '\r' >> SCORECARD.md            (CR as the LAST byte, no trailing newline)
$ tail -c 4 SCORECARD.md | od -c
0000000   d   .  \n  \r
$ python3 tools/check-line-endings-r64.py --check --root <clone>

check-line-endings-r64: 1 violation(s)
  SCORECARD.md:4724: CR byte at offset 768591
CHECK_LINE_ENDINGS: FAIL (326 file(s) checked, 1 violation(s))
rc=1

Named path, line, and byte offset; exit 1 as required.

**Verdict (d): PASS.**

## 5. Adversarial edges against the guard

**(a) CRLF under an allowlisted path** — guard-verdict: DISCLOSED BEHAVIOR, not a silent hole.
Header docs state it outright: allow-list = "any path under a `.ufo/` directory is skipped and
NEVER flagged", with the rationale (upstream captures legitimately carry CRLF). Live:
`--check <attack>/.ufo/capture.headers --root <attack>` (file contains `x\r\n`) →
`CHECK_LINE_ENDINGS: PASS (0 file(s) checked, 0 violation(s), 1 allow-listed)` rc 0 — the skip is
counted and named in the summary. Matters for C1: no (intended design).

**(b) Guarded file that is a symlink into .ufo/** — guard-verdict: the GUARD side wins, which is
the safe direction. Setup in the clone: tracked guarded path `corpus/SOURCES.md` replaced by
symlink `../.ufo/crlf-target.md` (target holds `HTTP/1.1 200 OK\r\n...`):
$ python3 tools/check-line-endings-r64.py --check --root <clone>
check-line-endings-r64: 1 violation(s)
  corpus/SOURCES.md:1: CR byte at offset 15
CHECK_LINE_ENDINGS: FAIL (326 file(s) checked, 1 violation(s))
rc=1
The allowlist is name-based on the TRACKED path (`corpus/SOURCES.md` carries no `.ufo` component),
so the target's `.ufo` location grants no shield; bytes are read THROUGH the link and the CR is
flagged. Corollary edge (found en route): a BROKEN symlink at a guarded tracked path is counted
`, 1 missing` and is not a violation (rc can stay 0 with the missing count visible — disclosed
branch; code comment: counting it clean or failing it would both lie). Matters for C1: no.

**(c) Empty file / binary** — guard-verdict: clean pass, no crash.
- empty file → `PASS (1 file(s) checked, 0 violation(s))` rc 0
- binary with NUL bytes, no CR (`bin\0ary\0data`) → `PASS (1 ...)` rc 0
- binary with NUL and CR (`bin\0ary\r\0x`) → `binary-nul-cr.md:1: CR byte at offset 7` FAIL rc 1
The tool is a byte scanner with no NUL/text sniffing: a guarded BINARY carrying CR would FAIL
(false-positive class). Matters for C1: currently no — mime sweep of today's guarded set
(`git ls-files -- corpus plans` + `file --mime-type`): 197 text/plain, 24 application/json,
1 text/html, 1 text/javascript, 3 text/x-script.python; no binary. Note for the future, not a defect.

## 6. Guard findings (routed to E1/L1; none block C1)

- **F1 LOW — doc/code divergence in the allowlist rule.** The module docstring says a path is
  allow-listed "if `.ufo` is a **leading** component of its repo-relative form", but the code
  `is_allowlisted` implements `ALLOW_DIR in parts` (ANY component). Demonstrated:
  `--check <attack>/corpus/.ufo/inner.md --root <attack>` (inner.md = `row\r\n`) →
  `CHECK_LINE_ENDINGS: PASS (0 file(s) checked, 0 violation(s), 1 allow-listed)` rc 0.
  So a CRLF file dropped at `corpus/.ufo/x.md`, `plans/.ufo/…`, or `tools/.ufo/…` silently
  bypasses the guard in explicit mode, and in default mode `guarded_set` pre-filters it away
  entirely (the summary's allow-listed count stays 0 — cosmetic sub-issue, F2). Exposure today:
  `git ls-files | grep -E '^(corpus|plans)/' | grep -E '(^|/)\.ufo/'` → **0 rows**. Suggested fix
  (one line): anchor to `parts[0] == ALLOW_DIR` (or fix the docstring to match the code).
  — FIXED by E1LineEnd post-review; re-verified by this seat against the final tool sha (§9).
- **F2 INFO** — in default guarded-set mode the summary always reports "0 allow-listed" because
  allowlisted tracked files are excluded before counting; harmless, weakens that field's disclosure.
  — FIXED by E1LineEnd post-review; re-verified by this seat against the final tool sha (§9).
- **F3 INFO** — the declaration's before-count for SCORECARD.md (4654/4701) is the 44fc183b figure;
  at the fix base 2f3061ef it was 4723/4723 (the declaration commit itself landed 69 CRLF lines).
  Receipt-accurate at its measurement time; predicate (b) is defined against 2f3061ef and holds.
- **F4 INFO (accidental positive control)** — while restoring the clone worktree I used
  `git -C <clone> checkout-index -f`, which rewrote the CLONE's corpus/SOURCES.md from the clone
  index (the CRLF HEAD blob, 279287 B). The guard flagged `corpus/SOURCES.md:1: CR byte at offset 35`,
  FAIL rc 1 — independent
  confirmation that it catches the real pre-fix committed state, not just synthetic fixtures.
  Clone-targeting proof: §7.

## 7. Addendum (2026-11-03T18:44Z) — lane-write clearance for this seat

E1LineEnd reported (18:43Z) that the LANE worktree corpus/SOURCES.md carried 381 CR bytes at
18:43:21Z and was CR-free again at mtime 15:43:24-0300, asking whether my `checkout-index` restore
had run against the lane. It did not; evidence:

1. The command was `git -C "$C" checkout-index -f -- corpus/SOURCES.md` with $C = the absolute
   clone path (the bash call's cwd was the fleet root); `git -C` overrides any cwd.
2. The write demonstrably landed in the CLONE: my immediately following guard run
   `--check --root <clone>` flagged the clone's corpus/SOURCES.md with the CRLF blob (279287 B,
   confirmed by `ls -l` of the clone file).
3. My lane re-measurement at 2026-11-03T18:40:53Z — 35 s AFTER that checkout-index — shows the
   lane file untouched: mtime 15:37:05 (E1's normalization time), CR_count=0, cmp rc 0.
4. My last command of the session was the scratch deletion at ~18:42Z; the 18:43:21Z lane touch
   post-dates it by over a minute. Nothing pending, scratch deleted.

Re-verification at 2026-11-03T18:44:01Z (this seat, read-only): all three files CR_count=0,
`git show 2f3061ef:F | tr -d '\r' | cmp - F` rc 0 ×3; corpus/SOURCES.md mtime 15:43:24-0300,
size 278906 (LF state, byte-identical). The 18:43:21Z CR state (381 CR) existed for ~3 s and was
restored by another party — not this seat. Candidate: one of the wave's mutation-testing seats
(they probe the guard); the wave coordinator can check which seat was active at 18:43:21Z.

## 8. Frozen predicate verdicts (my own runs)

| predicate | requirement (frozen) | my evidence | verdict |
|---|---|---|---|
| (a) | census exits 0, zero E-code, 42 W04 disclosed | §1: rc 0, E=0, W04=42 | **PASS** |
| (b) | three files differ from base ONLY by removed CR bytes; per-file cmp identical | §2: cmp rc 0 ×3; CR-attack: 0 surviving CR; sha256 equality | **PASS** |
| (c) | guard exists, --selftest PASS, --check rc 0 | §3: 5/5 PASS rc 0; 326 files PASS rc 0 | **PASS** |
| (d) | one CR injected into a guarded file in a scratch copy → --check non-zero | §4: EOF-CR mutant, rc 1, path/line/offset named | **PASS** |

**Claim C1: all four predicates PASS; no routed defect found in the claim itself.**

Residual risk / verification gaps:
- The fix is worktree-only (`git status --porcelain`: M on the three files; the guard tool is
  untracked). L1 must land it; a post-integration re-run of §1–§4 should reproduce verbatim.
- F1 is live code behavior with zero exposure today; it narrows guard coverage only if the lane
  ever stores captures under a nested `corpus/.ufo/`-style path.
- W04=42 is the disclosed duplicate-url warning class, unchanged by this repair (not an error).

## 9. Addendum (2026-11-03T18:46:05Z) — re-verification against the FINAL tool

E1LineEnd fixed F1 and F2 after my review and named the final tool sha. This seat re-ran (c)/(d)
and both probes against exactly those bytes — sha256sum matches E1's statement:

$ sha256sum tools/check-line-endings-r64.py
15f0e65c889acc3b591ca44c7e52fe16fa14d79c367e743ebcc905b17d50c030  tools/check-line-endings-r64.py
(350 lines — matches E1's stated 350)

- **(c) selftest**: `--selftest` → 5/5 cases PASS,
  `CHECK_LINE_ENDINGS_SELFTEST: PASS (5 cases, 5 passed, 0 failed)`, rc 0.
- **(c) check**: `--check` (lane, default mode) →
  `CHECK_LINE_ENDINGS: PASS (326 file(s) checked, 0 violation(s))` rc 0, followed by the new F2
  disclosure line `check-line-endings-r64: 22370 allow-listed .ufo path(s) skipped (upstream captures)`.
- **(d) mutant re-run** (fresh `git clone --shared` scratch clone, three files re-copied LF,
  baseline `PASS (326 file(s) checked, 0 violation(s))` + disclosure line, rc 0; then
  `printf '\r' >> SCORECARD.md`, od -c tail `d . \n \r`) →
  `SCORECARD.md:4724: CR byte at offset 768591`, `FAIL (326 file(s) checked, 1 violation(s))`,
  disclosure line, **rc 1**.
- **F1 fix verified by this seat**: explicit check of a nested `corpus/.ufo/inner.md` holding
  `row\r\n` → `corpus/.ufo/inner.md:1: CR byte at offset 3`, `FAIL (1 file(s) checked,
  1 violation(s))`, **rc 1** — the nested path is no longer shielded; the allowlist is now
  anchored to a leading `.ufo` component as documented.
- **Leading `.ufo` still allowlisted**: explicit check of `.ufo/capture.headers` (`x\r\n`) →
  `PASS (0 file(s) checked, 0 violation(s), 1 allow-listed)` rc 0.

All four predicate verdicts in §8 stand UNCHANGED on the final tool: **C1 = 4/4 PASS**.
Lane corpus bytes at this timestamp: unchanged (digest e1558e4b… for corpus/SOURCES.md, CR 0/0/0;
see §7 for the 18:43–18:44Z transient attribution note). Scratch dir for this addendum:
/fast/scratch/hyaku/tsukuroi-r64/R1C1Rev2 — deleted after this section was written.
