# Round 86 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-06
lane-round: tsukuroi r86; pre-round tip `3f56789829b84a97b2a8aa786618022195ef53cb`, landed tip `1d4bf1e8a153b383c5b819f2c2dca9dfb9891ded`
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-86/tsukuroi.md` (fleet commits `909fad00bb22e0c0c87e3274232922c060057d52` 18:54:30, `dd58ef82503f1a4b2ceac9ab608a727a73ff4b03` 18:55:55)
dispatch digest (copied from the mutable `.ufo/watchdog.log`, lines 3042 and 3064):
`2026-11-06T17:45:45-03:00 launch tsukuroi round=86 pgid=2714119 driver=hyaku-inline attempt=1`;
`2026-11-06T18:56:23-03:00 complete tsukuroi round=86; hyaku-inline attempt=1`

Closure verdict: **admitted**. C1 verifies under its frozen predicate and kill rule (re-counted from the
committed run logs; discrimination partial, lane-reported); C2 ruled `unprovable-but-better`; no axis harmed.
A host incident (both UKIs rewritten by a wave seat) is confirmed still present and is routed to the operator.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an <%ae> %H %ad' -- .ufo/reports/round-86/tsukuroi.md` (fleet root) | `tsukuroi-shokunin <tsukuroi@shokunin.local>` `909fad00…` 18:54:30 and `dd58ef82…` 18:55:55, both before the 18:56:23 completion line | pass |
| Second report commit | `git diff 909fad00 dd58ef82 -- .ufo/reports/round-86/tsukuroi.md` | one line (ExecSelftests bullet relabelled "(a seat is the lane)") rewritten in place, 85 s after first filing and before completion | **defect, status-neutral** (filed bytes rewritten, not an appended erratum; routed 4) |
| `SHONEN` heading, one line per box | `grep -cE '^\s*- \[[ x~]\]' SHONEN.md` → `4`; report `## SHONEN` has 4 `[~]` lines | 4 = 4 | pass |
| Cited commits exist and are ancestors of `master` | `git cat-file -t <h>` + `git merge-base --is-ancestor <h> refs/heads/master` for 2f67de80, dc884949, 1e1caabc, b96dc4be, 1d4bf1e8, 3f567898 | all six `commit` + ancestor; `git log 3f567898..1d4bf1e8` = exactly those five commits, author `tsukuroi-shokunin <tsukuroi@shokunin.local>`, order freeze → candidate → entry → landing → landing | pass |
| Pushed, nothing left over | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `1d4bf1e8…` | pass |
| Prompt carries the template contract | `grep -nE '^#+ ' .ufo/prompts/tsukuroi-round-86.md`; `git log` on it | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract, §5 commit/push/L0, §6 hyaku addendum, §7 scratch; committed `5f47ed77` 17:45:27, before the 17:45:45 launch | pass |
| Gate standard, Self-test clause | `SKILL.md` rows at `1d4bf1e8`; `w1/ExecSelftests/receipts/02-*`, `04-*`, `06-battery-mut4-selftest-cwd-lane.txt` | `hibernate-resume` (13 cases) and `nonauthor-label` (8 cases) self-tests fail on every committed mutant (rc 1); the battery's `--selftest` PASSes on the never-`met` mutant mut4 (rc 0) and is cwd-dependent — lane-routed R86-R4 | **defect, status-neutral** (routed 2) |
| Report precision | `git show 1d4bf1e8:.ufo/waves/round-86/before/controls/controls-summary.txt` | report and `resume-gate-battery-r86` registry row say near-miss N01–N12 each fail "exactly its own family"; N11 fails 2 (`DECOYS-R86,PREC-DECOYS`), N12 fails 4 — disclosed in `controls-receipt.txt` and CriticClaims §4, not in the report/registry sentence | **defect, status-neutral** (routed 3) |

Not a marker: five landed commits with resolvable evidence. Status `ok`.

## 2. Claims

### C1 — operability 9, measured (re-counted from committed run logs; gate code read against the pinned kernel source)

I did not execute the lane's gate or battery (§Gate standard, Closure consequence). Plain measurements:

- Instrument frozen: `git show <r>:tools/resume-gate-battery-r86.py | sha256sum` at `2f67de80` and `1d4bf1e8` →
  `a49a18aa21322579f723cbddd38f0fcdff686cde85f525a9a81976ef176fbc21` both; = `before/freeze-manifest.sha256:44`.
  Kill rule "void" does not fire.
- Measured candidate = landed candidate: `git diff --stat dc884949 1d4bf1e8 -- tools/` touches only
  `tools/check-nonauthor-label-r85.py`; `git diff --stat b96dc4be 1d4bf1e8 -- tools/ SKILL.md corpus/knowledge` is
  empty, so the measurement at `b96dc4be` holds at the tip.
- Re-count, not quoted totals: for `after/runs/cand-run{1,2,3}.json` I grouped `case_log` by `family` and counted
  families whose every case has `passed: true` and `want == got` → **30, 30, 30** of 30 (231 cases each; header
  `families_passed` 30, `verdict met`). Before, freeze receipts `before/controls/receipts/K1-r85-gate-do-nothing-run{1,2,3}.json`
  → **26, 26, 26**, failing exactly `EMPTY-RESUME, NOHIB-VALUED, NORESUME-VALUED, OFFSET-SSCANF`. Reported
  26/30 → 30/30 ×3 — agrees.
- Gate code read (diff `3f567898..dc884949`): `matches()` compares the first `len(setup)` characters with `-`→`_`;
  `noresume`/`nohibernate` matched by prefix and value-blind; `arg(cmdline,"resume=")` keeps the last token and
  `not arg(...)` treats empty as absent; `resume_offset()` keeps the previous value unless the rest starts with a
  digit. Pinned `init_main.c` raw 207-223 (`int n = strlen(p->str); if (parameqn(line, p->str, n))`, handler gets
  `line + n`, `line[n]` test only under `p->early`), `kernel_params.c` raw 86-95, `kernel_power_hibernate.c` raw
  982-985, 1402-1422, 1440-1466, 1518-1524, `lib_vsprintf.c` raw 3669-3681 — all match.
- Discrimination is partial, reported by the lane (M2, R86-R3): `w1/CriticClaims/runs/f4-shortcut-run{1,2}.json`
  re-count 30/30 too. The committed `counter/transcript.txt` shows the candidate answering the three composed
  counterexamples by the frozen rule set (`HR-SWAP-TOO-SMALL` kept) where f4 drops it. That is an instrument gap
  against other gates, not a candidate defect (same shape as r85 C2, admitted).
- Verdict: **C1 verifies.** Operability **improved** (two r85 false-HEALTHY paths — valued `noresume`/`nohibernate`,
  empty last `resume=` — and the non-digit-offset CANNOT-EVALUATE fixed; ordinal stays 9, no uplift claimed).

### C2 — depth 8, exploratory (I am the named non-author reviewer)

- New ground: `git grep -n -i 'obsolete_checksetup\|parameqn' 3f567898 -- corpus/knowledge` → one Limits line,
  `hibernation-availability-r85.md:56` (a disclosed gap, no row). At `1d4bf1e8`: `git grep -c -E '^\| BP[0-9]'`
  → 8 rows in the `.md`; the `.json` is a list of 8 (`BP1`…`BP8`).
- Rows re-read against the pinned bytes (whose sha256 I matched to live v7.2 fetches, §3): BP1 raw 207-223, BP2
  params.c 86-95, BP3 init/main.c 503-528 (`repair_env_string(param, val);` … `if (obsolete_checksetup(param))`),
  BP4 hibernate.c 1440-1444/1461-1466/1518/1524, BP5 1402-1409, BP6 46 + 982-985, BP7 1411-1422 + vsprintf.c
  3669-3681/79-95, BP8 1106-1112 (`If the user said "noresume".. bail out early.`) — every statement holds.
- Ruling: **unprovable-but-better.** Reasons: (1) it converts the r85 entry's own disclosed gap into sourced,
  tier-A rows pinned at the host's kernel tag; (2) the non-obvious facts are correct — a token reaches a `__setup`
  handler by prefix with no `=`/end check (that check is only for early params), `noresume=0` still sets the flag,
  a trailing bare `resume=` erases the device, `resume_offset=4096k` reads 4096 and `=abc` keeps the old value;
  (3) Operator actions are directly usable, and Limits route the not-modelled tokenizer cases (R86-R1/R2) rather
  than parking them (QUALITY 123). No count can show depth moved; depth stays 8.

### Owned axes not harmed

`git diff 3f567898 1d4bf1e8 -- SCORECARD.md` is append-only (+58 lines: declaration + measured outcome) and ends
"Axes now: depth8, coverage9, operability9, freshness9, calibration9, adjacency8 (unchanged) … No axis harmed."
Census at tip: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → `tsukuroi ok`, rc 0,
52 W04 (same as r85 close), no E code. Rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`
345 (`3f567898`) → 349 (`1d4bf1e8`); the SOURCES diff is +4 rows (S346–S349) and one `used-by` change on S343.

| Axis | Verdict | Basis |
|---|---|---|
| depth | unprovable-but-better | C2 exploratory, ruled above |
| operability | improved | C1 verified; no ordinal move |
| coverage | unchanged | no claim |
| freshness | unchanged | no claim |
| calibration | unchanged | no claim |
| adjacency | unchanged | no claim; ConnectorOverlap found no sibling conflict |

## 3. Discernment spot-check (`corpus/lessons/round-86.md` ## Gate)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S346 `init/main.c` | ADMIT | live fetch of `https://raw.githubusercontent.com/torvalds/linux/v7.2/init/main.c` → HTTP 200, sha256 `e895a643…3516` (= pin); raw 208-209 | agree | quote `int n = strlen(p->str); if (parameqn(line, p->str, n)) {` verbatim at 208-209; the prefix rule is stated nowhere else |
| S348 `lib/vsprintf.c` | ADMIT | live fetch of the v7.2 raw URL → HTTP 200, sha256 `cabb648a…69ca` (= pin); raw 3669-3674, 79-95 | agree | quote `(base == 10 && !isdigit(digit))` verbatim at 3671; with `is_sign` false for `%llu`, a non-digit first char breaks before conversion |
| man7 `bootparam(7)` | REJECT | live fetch `https://man7.org/linux/man-pages/man7/bootparam.7.html` → HTTP 200, body sha256 `6f440e77…2c50` (= the lane's pinned copy) | agree | the page says the kernel "would search the bootsetups array to see if 'foo' was registered" — a whole-name lookup; v7.2 `obsolete_checksetup` matches by prefix (S346). Admitting it would re-teach the r85 gate defect (QUALITY 118) |

New SOURCES rows checked: S346 and S348 (`corpus/SOURCES.md`, `git diff 3f567898 1d4bf1e8`) — URL at tag v7.2,
tier A, anchors (201-228/463-475/503-532; 79-95/3458/3644-3681) cover the cited lines, pinned sha = live body.
Their Gate quotes are 9 and 5 tokens (≤25 words). Spot-check result: 3/3 agree (2 admits, 1 reject).

## 4. Trend verdicts

- **expansion — unprovable-but-better.** One new plane (BP1–BP8) on ground no entry held (grep above), four tier-A
  rows (345 → 349); new ground is a judgment, not a count.
- **quality — improved.** All five r85 routed defects dispositioned; `hibernate-resume` and `nonauthor-label` gained
  self-tests that fail on every committed mutant (`w1/ExecSelftests/receipts/02-*`, `04-*`); the r85 entry's Limits
  now cite pinned S346/S349; two false-HEALTHY paths fixed; QUALITY 123 lands with M1 behind it. Offsets (not
  harms): the battery self-test is weak (R86-R4) and one report line was rewritten in place.
- **discernment — improved.** Spot-check 3/3 agree; the lane's own critic falsified C1's certification breadth
  and the lane reported it (M2, R86-R3) instead of smoothing it; the r85 man7 reject class was applied again.

## 5. Routed defects (lane fixes next round)

1. **Host incident (operator-owned repair; lane owes the prevention).** Read-only re-check at closure:
   `sudo -n b2sum /boot/EFI/Linux/*.efi` → `omarchy_linux.efi 57f5eb94…`, `omarchy_linux-lts.efi eff78d32…`, both
   mtime 2026-11-06 18:11:22; `/boot/limine.conf:30` pins `b990d8c6…`, `:38` pins `a68c281d…` — still mismatched.
   Lane: QUALITY row or wave-context rule that bans `objcopy`/any in-place writer on `/boot` as a probe (M3 has
   "captured-by" to land), and a `/boot` hash receipt before/after any `sudo` seat.
2. Gate standard, Self-test: `resume-gate-battery-r86 --selftest` passes on a never-`met` battery mutant and depends
   on cwd (R86-R4); fix before the next battery is frozen and record it in the registry row.
3. Report/registry wording: "N01–N12 each failing exactly its own family" — N11 fails 2 families and N12 fails 4;
   state the actual sets (the registry row is lane-owned; append a correction).
4. Filed-report discipline: the second commit `dd58ef82` rewrote one filed line of the report; corrections go in an
   appended erratum naming the superseded text.
5. Carry R86-R1..R5 (tokenizer `--`/quotes/bootconfig, unresolved `resume=` device class, composed families N13/N14,
   battery self-test, MutGate survivor M19) into the r87 freeze before any further claim on the r86 parse.

## 6. Operator note

All four SHONEN boxes stay `[~]` with pointers. Box 2 (LOG "Round 86": host cmdline → kernel parse rule → `--live`
HEALTHY) and box 4 (`w1/ConnectorOverlap.md`, PROVINCE unchanged) look checkable by a non-author. Promotion is
operator-owned; not checked here. The UKI/limine pin mismatch is open on the host (L0 line 383); Limine verifies
`#<blake2b>`-pinned paths at load, so both main entries are expected to fail verification (not booted here to
confirm) — the operator should resolve it before the next reboot.
