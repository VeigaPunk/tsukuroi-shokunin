# Round 85 — verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_zfl)
date: 2026-11-06
lane-round: tsukuroi r85; pre-round tip `3ed94533d581aa542d330ce2c97a798983839348`, landed tip `92be75064a53aec359976eef7af890f7311b47ac`
report: `/home/vgpnk/Projects/shokunin/.ufo/reports/round-85/tsukuroi.md` (fleet commit `b1b9a85ae4205fb2d19727673d66b584cfdc69f8`)
dispatch digest (copied from the mutable `.ufo/watchdog.log`, lines 3029 and 3039):
`2026-11-06T16:45:05-03:00 launch tsukuroi round=85 pgid=2581162 driver=hyaku-inline attempt=1`;
`2026-11-06T17:41:03-03:00 complete tsukuroi round=85; hyaku-inline attempt=1`

Closure verdict: **admitted**. C2 verifies (evidence-verified plus a direct code read); C1 ruled
`unprovable-but-better`; no axis harmed.

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H %ad' -- .ufo/reports/round-85/tsukuroi.md` (fleet root) | `tsukuroi-shokunin tsukuroi@shokunin.local b1b9a85a… Fri Nov 6 17:36:40 2026 -0300` (before the 17:41:03 completion line) | pass |
| `SHONEN` heading, one line per box | `grep -cE '^\s*- \[[ x~]\]' SHONEN.md` → `4`; report `## SHONEN` has 4 `[~]` lines | 4 = 4 | pass |
| Cited commits exist and are ancestors of `master` | `git rev-parse --verify <h>^{commit}` + `git merge-base --is-ancestor <full> master` for 66374a4d, 479d868b, ffae885f, 6a8296f6, 92be7506, 3ed94533 | all six `ok`; `git log 3ed94533..92be7506` = exactly those five commits, author `tsukuroi-shokunin <tsukuroi@shokunin.local>`, graph order freeze → candidate → landing → landing → receipt | pass |
| Pushed, nothing left over | `scripts/hyaku/jj-lane.sh state <lane>`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `92be7506…` | pass |
| Prompt carries the template contract | `grep -nE '^#+ ' .ufo/prompts/tsukuroi-round-85.md` | §1 MISSION/AXES, §2 claims, §2b frontier, §3 L2 floor, §4 report contract, §5 commit/push/L0, §6 hyaku addendum, §7 scratch; committed `6f74198e` (16:44:40, before launch) | pass |
| Gate standard, Self-test clause | registry rows in `SKILL.md` (lines 5917-5921 at `92be7506`) | `hibernate-resume`, `resume-gate-battery-r85` and `nonauthor-label` record their self-test as an external battery / control receipts; none of the three has a self-invocation mode over isolated fixtures asserting rc + finding-id | **defect, status-neutral** (routed 1) |

Not a marker: five landed commits with resolvable evidence. Status `ok`.

## 2. Claims

### C2 — operability 9, measured (evidence-verified; candidate code re-read against the pinned kernel source)

I did not execute the lane's gate or battery (§Gate standard, Closure consequence). Re-measured with plain commands:

- Instrument unchanged: `git show <r>:tools/resume-gate-battery-r85.py | sha256sum` at `66374a4d`, `ffae885f`,
  `92be7506` → `b30a7c1ed8fca5fa9c30fb3f4b221ccae11137f688bffc47844b16f0a117ba21` all three (= declared).
- Candidate measured = candidate landed: `git show 92be7506:tools/check-hibernate-resume.py | sha256sum` →
  `88041b75…83e7`, the gate sha in `.ufo/waves/round-85/after/measured-at-landing.txt`; `git diff --stat
  ffae885f 92be7506 -- tools` is empty, so the `ffae885f` measurement holds at the tip.
- Committed runs: `jq -c '{families_passed,families_total,verdict,cases,failed_families}'` on
  `after/runs/cand-run{1,2,3}.json` → `20, 20, "met", 134, []` ×3. Reported 20/20 ×3 — agrees.
- Before: freeze receipts `before/controls/receipts/*.json` and the tip re-run in `measured-at-landing.txt`:
  K1 (r84 gate, do-nothing) 0/20, best candidate-free control K6 14/20 at tip (14–15 at freeze). Lane seat
  CriticClaims reports K1 at 1/20 in 8 of 24 re-runs (MALFORMED only) — the report's flat "0/20" is a range
  (routed 3); still far below target.
- Pinned sources intact: `sha256sum -c SHA256SUMS` in `.ufo/waves/round-85/before/src` → 4/4 OK.
- Rule conformance, read by me: candidate `availability()` (diff `3ed94533..479d868b`) tests `hibernate=V` as
  `noresume*` → `nocompress*` → `no*`, sets disable on bare `nohibernate`, suppresses `noresume` when disabled,
  and blocks on `integrity`/`confidentiality`. Pinned `kernel_power_hibernate.c` raw 1424-1438
  (`strncmp(str, "noresume", 8)` … `"nocompress", 10` … `"no", 2` → `noresume = 1; nohibernate = 1;`) and
  1461-1465 (`nohibernate_setup`: both flags) match. `arg()` keeps the last occurrence; headroom is
  `sum(...)` over all swaps with strict `<` (tip `:125-129`, `:161-163`).
- Discrimination is partial, reported by the lane (M3/M4, QUALITY 122): six non-conforming near-miss gates
  (`w1/CriticClaims/forgers/f1,f2,f5,f6,f7,f8`) read 20/20; MutGate M26–M28 survive. Those are instrument gaps
  against *other* gates; the candidate itself conforms on each of those clauses (read above), and no
  candidate-free forger reaches the target — unlike r84, where three forgers met it.
- Verdict: **C2 verifies.** The declaration's sentence "a gate that reaches 20/20 must … parse `hibernate=` by
  the kernel's prefix order" is false as a property of the battery (lane-reported, QUALITY 122), not of the
  candidate. Operability **improved** (new runnable availability arm; ordinal stays 9, no uplift claimed).

### C1 — depth 8, exploratory (I am the named non-author reviewer)

- New ground: `git grep -il 'lockdown_hibernation\|nohibernate\|hibernation_available' 3ed94533 -- corpus/knowledge`
  → no output, rc 1; at `92be7506` → the `.md` and `.json` of `hibernation-availability-r85`.
- Quotes re-opened in the pinned snapshots: HA1 raw 109-113, HA2 raw 766-769 (`if (!hibernation_available()) {
  pm_pr_dbg("Hibernation not available.\n"); return -EPERM;`), HA5 raw 1106-1112 (`If the user said
  "noresume".. bail out early.`), HA8 raw 1162-1169 (`return sysfs_emit(buf, "[disabled]\n");`), HA3 S336 raw
  4479, HA4 S336 raw 1962-1969, HA9 S336 raw 3538-3545 — all verbatim.
- Host re-read (read-only): `/sys/kernel/security/lockdown` → `[none] integrity confidentiality` (HA7 agrees);
  `/sys/power/disk` → `[platform] shutdown reboot suspend test_resume` (not `[disabled]`, HA8 agrees);
  `/sys/power/state` → `freeze mem disk`; `/proc/cmdline` carries none of `nohibernate|noresume|hibernate=|lockdown=`
  (grep rc 1); kernel `7.2.11-arch1-1`.
- Ruling: **unprovable-but-better.** Reasons: (1) it is ground no knowledge entry held, and it is the
  precondition the r84 resume-chain plane silently assumed; (2) the non-obvious facts are correct and sourced
  at tier A — `integrity` (not only `confidentiality`) blocks hibernation by enum order + `>=`, and any
  `hibernate=no…` value except `noresume*`/`nocompress*` disables hibernation; (3) Limits disclose the gate's
  false-HEALTHY paths (`noresume=1`, `nohibernate=1`, empty `resume=`) and the two unpinned sources it leans on.
  No count can show depth moved, so depth stays 8.

### Owned axes not harmed

`git diff 3ed94533 92be7506 -- SCORECARD.md` is append-only (+54 lines: declaration + measured outcome) and ends
"Axes now: depth8, coverage9, operability9, freshness9, calibration9, adjacency8 (unchanged) … No axis harmed."
Census at tip: `sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → `tsukuroi ok`, rc 0,
52 W04 (same count as r84 close), no E code. Rows `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`
342 (`3ed94533`) → 345 (`92be7506`). Header-gate repair evidence-verified: `w1/ExecLints/receipts/01-…` rc 1
(two `KNOWLEDGE-HEADER-MISSING`, r84 entry) and `measured-at-landing.txt` rc 0, 101/101 at `ffae885f`.

| Axis | Verdict | Basis |
|---|---|---|
| depth | unprovable-but-better | C1 exploratory, ruled above |
| operability | improved | C2 verified; no ordinal move |
| coverage | unchanged | no claim |
| freshness | unchanged | no claim |
| calibration | unchanged | no claim |
| adjacency | unchanged | no claim; ConnectorOverlap found no sibling conflict |

## 3. Discernment spot-check (`corpus/lessons/round-85.md` ## Gate)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S344 `include/linux/security.h` | ADMIT | live `curl` of the v7.2 raw URL → sha256 `263740c9…cfcf` (= pin); raw 105-108, 133, 149 | agree | quote verbatim, 19 words (`wc -w`); the enum order is the only place the hibernation-is-integrity fact is stated |
| S343 `kernel/power/hibernate.c` | ADMIT | live `curl` → sha256 `ae3dbeb6…86c1` (= pin); raw 109-113, 1424-1438, 1518-1524 | agree | conjunction and prefix order verbatim; tier A code at the host's tag |
| man7 `kernel_lockdown(7)` | REJECT | live `curl` → sha256 `d07ec15a…5e0a`, 9861 B; line 135 `Unencrypted hibernation/suspend to swap are disallowed as the` | agree | `grep -ic 'encrypt\|luks\|dm-crypt'` on the pinned `hibernate.c` → 0: the page's qualifier is not what v7.2 implements, and the page is not version-pinned |
| ArchWiki swap-size sentence | REJECT | live `action=raw` line 111 | agree | no bound or comparison in the sentence; it points at `image_size`, which S340 already holds |

New SOURCES row checked: S344 (`corpus/SOURCES.md` line 355) — URL, tier A, raw 104-110/128-158, pin sha =
live body; key statement "LOCKDOWN_HIBERNATION is an integrity reason, placed before LOCKDOWN_INTEGRITY_MAX"
is supported by raw 105-108 + 133/149. Spot-check result: 4/4 agree (2 admits, 2 rejects).

## 4. Trend verdicts

- **expansion — unprovable-but-better.** One new plane (HA1–HA9) on ground no entry held (grep above), three
  tier-A rows (342 → 345); new ground is a judgment, not a count (same basis as r84).
- **quality — improved.** QUALITY 120–122 land with red evidence (`w1/ExecLints/receipts/01`, `08`); r84 routed
  defect 1 repaired (header gate rc 1 → rc 0, 101/101); `SKILL.md` registry rows for the three new/changed tools.
- **discernment — improved.** Spot-check 4/4 agree; the lane's own critic falsified its declaration's
  discrimination sentence and the lane reported it as M4 + QUALITY 122 instead of smoothing it; all five r84
  routed defects dispositioned (r84 defect 3: K3a–e r84 forgers committed as controls below target at freeze).

## 5. Routed defects (lane fixes next round)

1. Gate standard, Self-test: `hibernate-resume`, `resume-gate-battery-r85` and `nonauthor-label` have no
   self-invocation mode over isolated fixtures asserting rc + finding-id; give each a `--selftest` (or record why
   a battery is a probe) and put the spelling in its registry row.
2. Battery r85 coverage: no case draws a `hibernate=no<x>` value, a duplicate `resume_offset=`, `free ==
   image_size`, a multi-swap base, or a bool where an int is required — the lane's own r84 "Routed to the next
   round" list named three of these. Any later claim on those clauses needs a re-frozen battery with
   CriticClaims f1/f2/f5/f6/f7/f8 and MutGate M26–M28 as committed controls below target.
3. K1 do-nothing reads 0/20 or 1/20 (CriticClaims: 8 of 24 runs pass MALFORMED); report, SCORECARD and the
   registry row state a flat 0/20 — state the range.
4. Gate false-HEALTHY paths disclosed in Limits (ReviewGate L1 `noresume=1`/`nohibernate=1`, L3 empty
   `resume=`): fix in the gate or freeze them as explicit rules.
5. HA8/Limits rest on `kernel/power/main.c` (`state_show`) and `init/main.c` (`obsolete_checksetup`), outside
   the pinned set: pin both at v7.2 before citing them as tier A.

## 6. Operator note

All four SHONEN boxes stay `[~]` with pointers. Box 2 (LOG "Round 85": capture → `--live` HEALTHY →
availability rows → operator actions) and box 4 (`w1/ConnectorOverlap.md`, PROVINCE unchanged) look checkable by
a non-author. Promotion is operator-owned; not checked here.
