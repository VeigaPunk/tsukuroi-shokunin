# Round 84 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane round: tsukuroi 84. Lane HEAD before `64f45b790f2dbbf63b9b343c47810118a79f7a35`, after
`55de0f8820fecd728f5986ab63bf5d0311e1d615`. Report `.ufo/reports/round-84/tsukuroi.md` (fleet repo).
Driver digest (copied from mutable `.ufo/watchdog.log`):
`2026-11-06T15:39:26-03:00 launch tsukuroi round=84 pgid=1084420 driver=hyaku-inline attempt=1`;
`2026-11-06T16:41:58-03:00 complete tsukuroi round=84; hyaku-inline attempt=1`.

## 1. Conformance (step 1)

| Check | Command | Observed | Result |
|---|---|---|---|
| Report landed by lane | `git log --format='%an %H' -- .ufo/reports/round-84/tsukuroi.md` | `tsukuroi-shokunin 3fd19b0dee6e93d85e0db4501aa4e2b10000c407` (committer 16:41:06 -03, after lane tip 16:40:07) | ok |
| Prompt committed | same, `.ufo/prompts/tsukuroi-round-84.md` | `tsukuroi-shokunin 19fd6303…` | ok |
| SHONEN heading | read report §SHONEN | 4 lines, one per box, all `[~]` with pointers | ok |
| Cited hashes exist and are ancestors of `master` | `git cat-file -t <h>`; `git merge-base --is-ancestor <h> master` for 64f45b79, e0f42051, c6ee78b2, 69915b86, c6941adb, f19e73f3, 2ad4d1ef, 55de0f88, d5b3e134, a8598038 | all `commit`, all ancestors | ok |
| Pushed, no leftovers | `scripts/hyaku/jj-lane.sh state tsukuroi-shokunin`; `git status --porcelain`; `ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote `55de0f88…` | ok |
| Prompt carries template contract | section headers of the prompt | §1 MISSION/AXES binding, §2 claims 1–3, §2b frontier step, §3 L2 floor, §4 report contract (path, SHONEN, hash rule), §5 commit/push scope/L0, §6 hyaku addendum | ok |
| Marker? | report names committed work and hashes | real report | status `ok` |

## 2. Claims

Rule applied: instruments and forgers are the lane's/its seats'; I did not execute the battery or the gate
(§Gate standard, Closure consequence). C2 is **evidence-verified**; C1's new-ground and host facts are
**re-measured** by plain reads; C1's exploratory judgment is mine as named non-author reviewer.

### C2 — operability 9, measured: gate `tools/check-hibernate-resume.py` scored by battery 13/13

- Instrument bytes unchanged from freeze: `git show <rev>:tools/resume-gate-battery-r84.py | sha256sum` →
  `00310ac205f07f39…` at both `e0f42051` and `55de0f88`; counter `cb70d4357ebe2d50…` and capture
  `cec27b9d19e4ac85…` equal at both revisions.
- Before: `.ufo/waves/round-84/before/controls/c2-control-absent.json` → `families_passed 0, families_total 13,
  verdict unmet` (committed at freeze).
- After: `.ufo/waves/round-84/after/measured-at-landing.txt` (measured at `2ad4d1ef`): three candidate runs
  `families_passed 13 verdict met rc=0`; forgers `f2-replay.py`, `f1-signature.py`, `f4-firstfault.py` each
  `families_passed 13 verdict met rc=0`.
- Forger read: `f2-replay.py` (committed, 21 lines) never opens `--facts`; it replays a fixed answer schedule
  keyed on a per-parent counter in `/tmp`. A gate that never reads its input meets the target, so the battery
  cannot distinguish the candidate from a forger.
- Verdict: **C2 does not verify** (agrees with the lane). Operability axis **unchanged** (9 → 9; no ordinal move
  was claimed).

### C1 — depth 8, exploratory: hibernate-resume plane HR1–HR10

- New ground: `git grep -c map-swapfile 64f45b79 -- corpus/knowledge` → exit 1 (absent);
  at `55de0f88` → `hibernate-resume-plane-r84.json:4`, `.md:3`.
- Rows: `corpus/knowledge/hibernate-resume-plane-r84.json` → 10 rows `HR1`…`HR10`.
- Host facts re-read in `.ufo/waves/round-84/before/host/receipt.txt`: :4 cmdline `resume_offset=3795013`;
  :13 `map-swapfile -r` → `3795013`; :24 `filefrag` first extent physical `3530821`; :44
  `/sys/power/resume_offset` → `3795013`. HR1/HR2/HR3/HR8 host values match.
- Source lines re-read in the pinned snapshots (`sha256sum -c SHA256SUMS` OK): `ch-swapfile.rst` :13 NODATACOW
  (HR4), :118 "physical offset … not the same" (HR3), :127 map-swapfile adjusted value (HR2); `sysfs-power`
  :97-98 image_size upper limit (HR10), :307-308 override (HR8); `mkinitcpio-install-resume` :11-12
  `systemd_ver >= 255 … add_binary …systemd-hibernate-resume` (HR9).
- Provenance counter `count-resume-rows-r84 --revision 2ad4d1ef` → met 10/10, 6 snapshots (committed
  evidence); correctly reported as a shape gate that earns nothing (its P1 junk control also reads met).
- Reviewer status: the report names wave seat ReviewEntry as the "named non-author reviewer"; per LEARNING.md
  §Discernment ("A subagent the lane dispatched is still the lane") that seat is the lane. I act as the named
  non-author reviewer for this exploratory claim.
- My judgment: **unprovable-but-better.** Reasons: (1) the entry holds a host-specific, sourced trap no entry
  held — the btrfs `map-swapfile` offset (3795013) versus the `filefrag` physical extent (3530821), measured on
  this host; (2) every row I sampled (HR2, HR3, HR4, HR8, HR9, HR10) quotes text present at the cited raw
  lines of a digest-pinned snapshot; (3) the Limits section is honest (no resume exercised; writer of
  `/sys/power/resume` unknown; gate reads only `/proc/cmdline`); (4) operator actions name the
  update-safety gate before boot-entry regeneration. Not measurable: no counter separates it from junk.
  Depth axis: no ordinal move (8 → 8).

### Owned axes not harmed

`git diff 64f45b79 55de0f88 -- SCORECARD.md` is append-only (declaration, C1 withdrawal, outcome blocks;
no prior row edited). Outcome line: `depth8, coverage9, operability9, freshness9, calibration9, adjacency8
(unchanged)`. Spot reads of the new tools and entry show no change to existing entries.

| Axis | Verdict | Basis |
|---|---|---|
| depth | unprovable-but-better | C1 exploratory, judged above |
| operability | unchanged | C2 not verified; forgers reach 13/13 |
| coverage | unchanged | no claim; SCORECARD append-only |
| freshness | unchanged | no claim |
| calibration | unchanged | no claim |
| adjacency | unchanged | no claim; ConnectorOverlap split swap image-fit (tsukuroi) from swap capacity (mori) |

## 3. Discernment spot-check (`corpus/lessons/round-84.md` `## Gate`)

| Item | Decision | Re-opened source | Agree? | Reason |
|---|---|---|---|---|
| S340 sysfs-power | ADMIT (HR8/HR10) | `curl -sS -L https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/ABI/testing/sysfs-power`, lines 305-309 | agree | live body sha256 `c2be59dd56c9c036…` equals the pinned snapshot; :307-308 read "Using this sysfs file will override any values that were set using the kernel command line for disk offset." — the Gate quote verbatim (19 words) |
| S342 CPython subprocess.py v3.14.8 | ADMIT (corrects r83 reject reason) | `curl -sS https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/subprocess.py`, lines 396-402 | agree | `return p.wait(timeout=timeout)` / `except:  # Including KeyboardInterrupt, wait handled that.` / `p.kill()` / `raise` — `call()` kills the child on timeout; the round-83 reason was false and is now corrected by an appended note |
| swsusp.rst swap-size advice | REJECT | `curl -sS -L https://raw.githubusercontent.com/torvalds/linux/v7.2/Documentation/power/swsusp.rst`; `grep -n 'Just prepare big'` → :382; `grep -n -i 'image_size\|free swap\|…'` | agree | :382 "Just prepare big enough swap partition." names no size rule; no sentence in the file bounds the image against free swap (image_size hits :62-64, :424-432, :499-500 only set or reset the knob); HR10 correctly rests on sysfs-power |
| ArchWiki Suspend_and_hibernate oldid=887184 | REJECT (unreachable) | `curl -sS -L -w '%{http_code} %{size_download}'` same URL | agree | HTTP 200, 7046 bytes, `<title>Making sure you're not a bot!</title>`, 0 `resume_offset` hits — an interstitial, not a source |

SOURCES.md row re-opened: `S340` (line 351) — anchor names tag v7.2, raw lines 91-103 and 296-308, and the
snapshot sha256 `c2be59dd…a102`, matching the re-fetched body; its Gate quote is 19 words (≤25) and located
at :307-308. Status `mined`, used-by the new entry.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → `tsukuroi ok`,
rc 0, 52 W04 (duplicate URL across scopes), no E code. Rows
`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`: 335 at `64f45b79` → 342 now (+7, S336–S342).

Spot-check result: 4/4 agree (2 admits, 2 rejects).

## 4. Trend verdicts

- **expansion — unprovable-but-better.** One new knowledge entry on ground no entry held (map-swapfile
  absent at `64f45b79`), its rows citing mined rows S336–S341; it rests on my exploratory judgment, not a
  count, and the entry lacks the `source:`/`recheck:` header lines (defect 1).
- **quality — improved.** The round-83 false reject reason is corrected from the implementing source (S342,
  re-opened above) by an appended note and QUALITY 118; registry `check-registry-coverage` 4 findings → 0
  (committed evidence in `after/measured-at-landing.txt`); two partial rows reworded before landing. No
  admitted entry failed its re-check.
- **discernment — improved.** The spot-check agrees with the Gate on both admits and both rejects; the
  round-83 disagreement (r83 spot-check, discernment harmed) became lesson M1 plus grounded QUALITY 118, and
  the C2 battery defect became M4 plus QUALITY 119 instead of a re-declared target.

## 5. Routed defects (lane fixes next round)

1. `corpus/knowledge/hibernate-resume-plane-r84.md` opens without `source:` and `recheck:` header lines
   (LEARNING.md §Files the path writes); add them (S336–S341; `tools/check-hibernate-resume.py --live`).
2. The report and entry call wave seat ReviewEntry the "named non-author reviewer"; a lane-dispatched seat
   is the lane (LEARNING.md §Discernment). Correct the wording in the next report/entry; exploratory claims
   get their non-author ruling at closure.
3. C2 battery `tools/resume-gate-battery-r84.py` is replayable (fixed case order, single-fault families);
   any re-run of the C2 claim needs a new frozen battery meeting QUALITY 119 with the f1/f2/f4 forgers as
   committed negative controls reading below target before any candidate is scored.
4. C1 counter is a provenance shape gate (M3); do not cite it as a measurement again.
5. Freeze commit `e0f42051` carries its parent's author date (helper behaviour); chronology rests on commit
   graph order — keep citing graph order, not dates.

## 6. Operator note

All four SHONEN boxes are `[~]` with pointers; box 2 (end-to-end task: host capture → gate `--live` HEALTHY
→ operator actions) and box 4 (ConnectorOverlap H1–H7) look checkable by a non-author. Promotion is
operator-owned; not checked here.
