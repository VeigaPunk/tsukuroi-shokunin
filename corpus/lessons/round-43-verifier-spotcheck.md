# Round 43 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_opus)

Lane-round: tsukuroi round 43. Lane tip before the round `6951ead90566b2d74f7c45b4efca29246badad64`, after
`5f8b3c58bbf46128c0d924149bf795bc8199c66b` (branch `master`). Report: `.ufo/reports/round-43/tsukuroi.md` (fleet repo).
Dispatched prompt: `.ufo/prompts/tsukuroi-round-43.md`. Closed 2026-10-26. The closure wrote this file, not the lane,
and the lane must not edit it. No re-check seats were dispatched: the closure session ran every command below. Neither
lane counter (`tools/score-bootinputs-r43.py`, `tools/check-scrub-record-r43.py`), the boot-chain or census selftest,
nor `check-self-assessment.py` was executed (PROTOCOL §Gate standard, Closure consequence): their committed receipts
were verified. C1 was re-measured with an independent plain reproduction of the old and new idiom plus counts over
committed bytes. C2's quotes, snapshots, sources and bound verdicts were re-measured.

Driver digest (copied from `.ufo/watchdog.log`, mutable):

```
2026-10-26T18:37:51-03:00 launch tsukuroi round=43 pgid=1248034 driver=hyaku-inline attempt=1
2026-10-26T20:31:55-03:00 complete tsukuroi round=43; hyaku-inline attempt=1
```

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by the lane identity | `git log --format='%an <%ae> %H %ci' -- .ufo/reports/round-43/tsukuroi.md` (fleet root) | `tsukuroi-shokunin <tsukuroi@shokunin.local> ff846a480fe102ef741910fcfcbfbfe7f1d55c20 2026-10-26 20:31:15 -0300` (after lane tip 20:29:44, before the `complete` line 20:31:55) | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | four boxes, each `[~]` with sub-bullets | pass |
| Cited commits exist and are ancestors of the branch | `git cat-file -t <h>; git merge-base --is-ancestor <h> master` for the 11 cited hashes + base | all `commit`, all `anc=0`; `git log --first-parent 6951ead9..5f8b3c58` = 11 commits, author and committer `tsukuroi-shokunin` | pass |
| Pushed, no leftovers | `scripts/hyaku/jj-lane.sh state …` ; `git status --porcelain` ; `git ls-remote origin refs/heads/master` | `state branch=master local=5f8b3c58… remote=5f8b3c58… ahead=0 behind=0 head=detached tracked=0 untracked=0`; porcelain empty; remote `5f8b3c58…` | pass |
| Prompt carries the template contract | `diff <(sed -n 1,140p templates/round-prompt.md) <(sed -n 1,140p .ufo/prompts/tsukuroi-round-43.md)` | 11 changed lines, all `{{LANE}}`/`{{ROUND}}`/`{{FLEET_ROOT}}`/`{{AXES}}` substitutions; sections 1–5 present; hyaku addendum §6 and §7 appended | pass |
| Prompt committed before dispatch | `git log -- .ufo/prompts/tsukuroi-round-43.md` | `3fc4f25e…` 18:37:49, launch line 18:37:51 | pass |

No step-1 conformance defect found.

## 2. Claims

### C1 — operability (boot-input freshness under pipefail)

- Code delta, committed bytes: `git diff 6951ead9 5f8b3c58 -- tools/boot-chain-audit.sh` replaces
  `find … -print -quit 2>/dev/null | grep -q .` (under `set -uo pipefail`, line 139 at every revision) with
  `inputs_newer_than`, which tests `[ -n "$(find … -print -quit 2>/dev/null)" ]`; plus four `R43-C1` selftest cases.
  Unchanged since `9b974f2a` (`git diff --stat 9b974f2a 5f8b3c58 -- tools/boot-chain-audit.sh` empty).
- Counts over committed bytes (`git show <r>:tools/boot-chain-audit.sh | grep -cE "^\s*st_check '"`, `… 'R43-C1`,
  `… -c -- '-print -quit 2>/dev/null | grep -q \.'`): base 45 / 0 / 1; `717b716a` 48 / 3 / 0; `c3954913` 49 / 4 / 0;
  tip 49 / 4 / 0. Matches the reported totals 45 → 48 → 49 and `selftest_r43` 0 → 3 → 4.
- Independent reproduction (my own bash, not the lane script; scratch fixture with one input at mtime 3000, epoch
  2000, under `set -uo pipefail`): missing start point first → old idiom `0`, new `1`; unreadable (mode 000, old mtime)
  directory first → old `0`, new `1`; all present → old `1`, new `1`; nothing newer with a missing start point → old
  `0`, new `0`. The fail-open is real and the fix closes it without a false positive.
- Committed evidence (evidence-verified, not re-executed): frozen counter sha256 at `fe357001` and at tip both
  `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f` (no commit touches it after `fe357001`);
  `before/c1-before.jsonl` revision `6951ead9…`, `correct 8`, `selftest_r43 0`, `PASS total=45`, `verdict FAIL`,
  exit 1; `after/c1-after-c395491.jsonl` revision `c3954913…`, `correct 16`, `identity_ok 1`, `live_agree 1`,
  `selftest_r43 4`, `PASS total=49 failed=0`, `verdict PASS`, exit 0; control battery
  `controls/battery-summary-c1.jsonl` `should_fail_accepted 0, control_accepted 1`. Receipt timestamps
  (21:57Z, 23:27Z) precede their shipping commits (`717b716a` 21:57:16Z, `a87249c7` 23:29:07Z).
- Verdict: **verified — operability improved.**

### C2 — depth (scrub record re-grounded: SR1, SR3, SR6)

- Rows: `grep -nE '^## SR' corpus/knowledge/btrfs-scrub-record-r43.md` → SR1, SR3, SR6 (3); file absent at base
  (`git show 6951ead9:<path>` → fatal). Provenance trio on lines 1–3.
- Quotes: a script matching every `**Quote.** \`S2xx\` <file>.c:<n>: "<text>"` line against line n of the pinned
  snapshot → `ok 33 bad 0`.
- Snapshots: `sha256sum -c .ufo/waves/round-43/frozen/src/SHA256SUMS` → `ioctl.c: OK`; round-42 `scrub.c`
  `48df2e2f…0801` and `hostcap/capture.txt` `f7ecbe7c…c556` match the entry header.
- Live re-open (2026-10-26): `curl https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/fs/btrfs/ioctl.c?h=v7.2.11`
  → sha256 `7b3488f2…4ba01` (identical to the pin), lines 3132-3133 `if (!capable(CAP_SYS_ADMIN))` /
  `return -EPERM;`; `curl https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/cmds/scrub.c` → `48df2e2f…0801`
  (identical to S237's pin).
- Semantics re-read: SR3's thirteen `_SCRUB_SUM` fields (`sed -n 800,822p scrub.c | grep -c '_SCRUB_SUM('` → 13),
  `last_physical` copied, `canceled`/`finished` from the new run, `t_resumed` ← new `t_start`, `t_start` ← resumed,
  durations summed (scrub.c:803-825); skip condition at :1430-1437 matches the narrowed text. SR6: scrub.c:1197-1205
  returns 1 on the first ioctl returning 0, else 0; `in_progress` assigned only at :1946; `running` printed only from
  `in_progress` (:341).
- Host re-probe (uid 1000): `btrfs scrub status /` → `no stats available`, exit 0; `/var/lib/btrfs` absent. Agrees with
  S241.
- Bound verdicts: first lines of `w2/C2RevSR1.md`, `C2CritSR1.md`, `C2RevSR6.md`, `C2CritSR6.md` → `ROW SR? VERDICT:
  holds`; `C2RevSR3.md` holds, `C2CritSR3.md` `partly`; `residual/C2ResSR3.md` (reading `5647d4ff`) holds. Between the
  counted reads' revision `8acf0b02` and the tip the entry changed in one line only (`git diff -U0 8acf0b02 5f8b3c58`:
  line 60, the SR3 skip narrowing the residual re-read).
- Committed evidence: counter sha256 `b4602c56…9854` unchanged since `fe357001`; `before/c2-before.jsonl` `rows 0`, FAIL;
  `after/c2-after-c395491.jsonl` rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1, verdicts_ok 3,
  novelty_base_hits 0, pointer_ok 1, PASS; `c2-after-c395491-direct.json` `transcripts_bound 7 / 7`. Round-42 entry
  header gains the `superseded-in-part` pointer (one added line).
- Defect (routed below, not a claim failure): the entry contradicts itself on SR1's trailing-bytes consequence —
  line 28 says "reproduced in a scratch harness compiled from the pinned write path, round-43 wave-1 seat
  C2ExecTailRepro", and `w1/C2ExecTailRepro.md:136` shows the tail identical, while `## Limits` line 152 says it
  "was not reproduced". The statement itself is marked [inference] and not observed on the host; the predicate does
  not read Limits.
- Verdict: **verified — depth improved.**

### No-harm

`git diff 6951ead9 5f8b3c58 -- SCORECARD.md` is append-only (declaration, measured outcome, axes table with unchanged
ordinals depth 8, coverage 9, operability 9, freshness 9, calibration 9, adjacency 8, capabilities table, planned row).
`git diff --numstat 6951ead9 5f8b3c58 | awk '$2>0'` → only `tools/boot-chain-audit.sh` (7, the replaced idiom) and
`corpus/SOURCES.md` (1, S237 `used-by` only: field-diff shows column 12 alone changed); no file deleted.
`SKILL.md` +156/-0, `PROVINCE.md` +10/-0, `corpus/README.md` +11/-0, `LOG.md` +27/-0, `QUALITY.md` +2/-0. Capabilities
table header count `awk …(round 43)…` → 1 (round 42's → 2, the recorded red). Self-assessment receipt
`after/self-assessment-final.jsonl`: 27 checks, 0 non-`match`, exit 0. Sources census below exit 0.

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 re-measured (independent reproduction + committed counts) and receipt-verified |
| depth | improved | C2 re-measured (33/33 quotes, live re-fetch, host re-probe, bound verdicts) |
| coverage | unchanged | scrub record stays Frontier; no Core move |
| freshness | unchanged | S237/S240 re-fetched byte-identical (also re-opened by this closure); no ordinal move |
| calibration | unchanged | self-assessment receipt 27/0; ordinals unchanged |
| adjacency | unchanged | sibling pins reported (report §Adjacency), none moved by a sibling-owned file |

## 3. Discernment spot-check

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| SR6 (S240 EPERM gate on scrub progress) | admit | git.kernel.org stable `ioctl.c?h=v7.2.11` (sha256 identical to pin, :3126-3133), scrub.c:1197-1205, :1946, :341, `btrfs scrub status /` as uid 1000 | agree | progress ioctl returns `-EPERM` before any other work without `CAP_SYS_ADMIN`; status's only `running` path is `in_progress` from that ioctl; host prints `no stats available` |
| SR3 narrowed skip condition | admit | scrub.c:803-825, :1425-1440 | agree | resume takes a record that is canceled or unfinished; `skip` is set only for finished-and-not-canceled or no record; 13 summed fields, `t_start`/`t_resumed`/duration as stated |
| "device id is never emitted" (w1 `C2DraftCritSR3.md` F1) | reject | scrub.c:782-792, :864-870 | agree | `scrub_writev` formats and writes its buffer itself (`return scrub_write_buf(fd, buf, ret);`); the following `scrub_write_buf(fd, buf, ret)` uses the outer `ret`, 0 after the `-EOVERFLOW` guard, so it writes 0 bytes |
| `merge/tsukuroi/ext4-journal-guarantee-r32.md` | reject (out of province) | `findmnt -rno TARGET,FSTYPE` (fstype tally: btrfs 4, vfat 1, xfs 2, no ext4); `grep -n ext4 PROVINCE.md` → none | agree | no ext4 filesystem on this host and PROVINCE names none; flip condition stated |

New `corpus/SOURCES.md` row re-opened: **S240** — URL resolves; anchor lines 3066-3075, 3118-3140, 5578-5584 at peeled
`a2de78ee…`; the Gate quote `"if (!capable(CAP_SYS_ADMIN))" / "return -EPERM;"` is located verbatim at :3132-3133
(also :3072-3073, :3120-3121) and is under 25 words. S241's quoted lines match `capture.txt:6, 2, 10`. S237 change is
`used-by` only and logged old→new in the lesson Gate.

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
→ exit 0, `tsukuroi ok`, 40 `W04` (duplicate-URL-across-scopes warnings, unchanged from start); rows 239 → 241
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` at base and tip).

QUALITY 92 (one header row per rendered table) is grounded by lesson row R43-CAP-HEADER-DUP with a red-before count.

## 4. Trend verdicts

- **expansion: unchanged.** The r43 entry deepens an existing Frontier line; no new coverage-map ground and no new
  capability row (the boot-chain-audit row is updated). Agrees with the lane.
- **quality: improved.** The round-42 withdrawn SC1/SC3 and the errno-only running-state note are superseded by rows
  verified at pinned lines (re-measured here), the old entry points to them, and a fail-open in the lane's own audit is
  fixed with red-before evidence. The SR1 Limits contradiction is a provenance inconsistency inside a statement already
  marked [inference], not a false domain fact; it is routed, not graded harm.
- **discernment: improved.** The spot-check agrees with the gate on two admits and two rejects; the one unlearned
  mistake (capabilities header duplication) became QUALITY 92 with its lesson.

## 5. Routed defects (the lane fixes next round)

1. **R43-SR1-LIMITS-CONTRADICTION** — `corpus/knowledge/btrfs-scrub-record-r43.md:152` says SR1's trailing-bytes
   consequence "was not reproduced"; :28 and `w1/C2ExecTailRepro.md:136` record a scratch-harness reproduction. Append a
   correction (not observed on the host; reproduced in a harness compiled from the pinned write path) and sweep
   `SKILL.md` "Scrub record re-grounded — round 43" and `PROVINCE.md` for the same wording.
2. Carried, lane-recorded: the C2 binding accepts padded/blank-prefixed verdict lines and a contradictory JSON
   `verdict` beside `verdict_line` (`w1/C2MutBinding.md`); the C1 counter leaves mount-table, uid_map, script-path and
   cwd channels open and does not exercise the empty-btime branch; no gate reads a `superseded-in-part` pointer.
3. Carried from round 42: the census `:743` lookup selftest case and the five single-line probe readers (planned row
   item 3).

## 6. Notes for the operator

All four SHONEN boxes remain `[~]` in the report. Boxes 1 (SKILL decision tables with cited sources) and 2 (an
end-to-end task logged in `LOG.md`) look checkable by a non-author now: this closure independently reproduced the C1
fail-open and fix and re-opened C2's sources. Boxes 3 (whole-SKILL executability) and 4 (PROVINCE accuracy) need a
dedicated review. Promotion is operator-owned; nothing was promoted or written to `SHONEN.md`.
