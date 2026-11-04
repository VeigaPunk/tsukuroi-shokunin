# Round 81 — non-author closure spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed 2026-11-04. Base `96ad75b84160da58efaee4997576ce718fd72e2b`; declaration
`8023711867eaa788f68af09d7f29d24db749cca7`; hyaku "before" head
`e8e5d5b39b25a83f705dc3aa760df21c6a2af508`; measured work
`c6fd99493820947d16a3a1a4978efdf01ba20def`; delivered tip
`4ffcbbd5c036718dc6ecec0e212901430c2c3fa3`.
Status **ok**, admitted **false**, verdict **rejected-honest-stop**.
All three finite after-values re-measure as reported, but none of the three claims was
declared before data: the lane's own declaration (`80237118`, SCORECARD "Round 81 —
declaration") states the L1 authored *and scored* candidate files before freezing the
predicates. The binding round contract (dispatched prompt §6: "The claim is judged on the
counter, kill rule and predicate declared before data") and the run-15 rule that procedural
misses "must not be … retroactively repaired by later controls" make green final counters
insufficient for admission. No owned axis is harmed. No promotion, capability, scope transfer
or ordinal uplift is awarded.

Dispatch/completion digest, copied from the mutable watchdog log:

```text
2026-11-04T17:52:19-03:00 launch tsukuroi round=81 pgid=3648537 driver=hyaku-inline attempt=1
2026-11-04T18:02:51-03:00 lane-dead-no-report tsukuroi round=81; retry same round (attempt=1)
2026-11-04T18:02:53-03:00 launch tsukuroi round=81 pgid=36255 driver=hyaku-inline attempt=2
2026-11-04T18:03:31-03:00 lane-dead-no-report tsukuroi round=81; retry same round (attempt=2)
2026-11-04T18:03:33-03:00 launch tsukuroi round=81 pgid=49539 driver=hyaku-inline attempt=3
2026-11-04T18:04:12-03:00 lane-dead-no-report tsukuroi round=81; retry same round (attempt=3)
2026-11-04T18:25:31-03:00 launch tsukuroi round=81 pgid=737095 driver=hyaku-inline attempt=1
2026-11-04T18:25:49-03:00 lane-dead-no-report tsukuroi round=81; retry same round (attempt=1)
2026-11-04T18:25:51-03:00 launch tsukuroi round=81 pgid=757374 driver=hyaku-inline attempt=2
2026-11-04T18:53:40-03:00 complete tsukuroi round=81; hyaku-inline attempt=2
```

(Each lane-dead line's reason was `FAIL report_of (missing, unchanged, no SHONEN heading, or
< 400B)`.)

## Step-1 conformance

- `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-81/tsukuroi.md`
  → three commits, all `tsukuroi-shokunin`: `df1528e0…` (18:51:09), `e0e258f3…` (18:53:05),
  `15995ee32f09f216f5729b68cc7821ef520ddafc` (18:53:10). All after the delivered tip
  (`4ffcbbd5`, 18:50:51 -03:00): no report filed before its commit.
- `grep '^## SHONEN'` → one heading; four `[~]` lines; `SHONEN.md` holds four boxes
  (`grep -cE '^\s*- \['` → 4). No self-awarded `[x]`.
- Cited hashes `4ffcbbd5`, `c6fd9949`, `96ad75b8`, `80237118`, `9e723336`, `c63511b4`,
  `53d1cece`, `e8e5d5b3`: each resolves (`git rev-parse --verify <h>^{commit}`) and
  `git merge-base --is-ancestor <full> master` holds for all eight. All seven round commits
  `80237118..4ffcbbd5` are authored `tsukuroi-shokunin <tsukuroi@shokunin.local>`.
- `scripts/hyaku/jj-lane.sh state …` → `branch=master local=4ffcbbd5… remote=4ffcbbd5…
  ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` → empty;
  `git ls-remote origin refs/heads/master` → `4ffcbbd5c036718dc6ecec0e212901430c2c3fa3`.
- Prompt `.ufo/prompts/tsukuroi-round-81.md` (84 495 B) carries the template sections 1–5
  (MISSION/AXES binding, claims, frontier step, L2 floor, report contract, commit/push/L0)
  plus the §6 hyaku addendum and §7 scratch discipline.
- Status-neutral conformance defects: (a) chronology — predicates frozen after author
  scoring (lane-disclosed); (b) attack floor met only nominally (reviewer and critic seats
  died with no artifact; effective 1/12); (c) two concurrent writers committed to the lane
  within two minutes (lane-disclosed), leaving two "Round 81 — measured outcome" SCORECARD
  blocks that disagree on the depth ordinal (see R81-V1); (d) four driver attempts died
  without a report before the completing attempt, and attempt 1 had already landed
  `e8e5d5b3` and `c6fd9949` (18:01–18:02) before its lane-dead line.

## Per-claim re-check (against `4ffcbbd5`)

Re-measured = a plain grep/jq/git/sha256sum command I ran; evidence-verified = a lane gate's
committed evidence I checked without executing that gate (§Gate standard, Closure
consequence).

| Claim | Reported | My command | Observed | Mode |
|---|---|---|---|---|
| C1 depth | count 0→8, met | `git show 4ffcbbd5:corpus/knowledge/mount-unit-fstab-plane-r81.json \| jq '.. \| objects \| select(has("id")) \| .id'`; `… .md \| grep -cE '^\| *MT[0-9]'`; `git cat-file -e 80237118:corpus/knowledge/mount-unit-fstab-plane-r81.md` | MT1–MT8 distinct (8); md table rows 8; absent at `80237118` and `e8e5d5b3`; knowledge `.md` 98→99; rows with `measured` = MT2 `[136,145]`, MT5 `[69,70]`, MT6 `[124,127]` (3 legs) | re-measured |
| C1 source pin | snapshot SHA `afbf3be6…2394` | `curl … v262/man/systemd.mount.xml \| sha256sum` | `afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394`, 707 lines | re-measured |
| C1 measured leg MT5 | `tmp.mount` :69-70 | `git show 4ffcbbd5:.ufo/waves/round-81/before/host/generator.txt \| sed -n 66,78p` (sha256 `8e1bb73b…e4f8`) | `Before=local-fs.target` at :70 in the unit whose `Where=/tmp`, `Options=…nofail,x-systemd.before=local-fs.target` at :77 | re-measured |
| C2 operability | 3/6 → 6/6, met | `git show <r>:tools/measure-round80.py \| grep -nE 'CannotEvaluate\|snapshot_(tampered\|absent)\|return 2'`; `grep -cE "^\s+run\('"`; `sha256sum` of committed counter | base `96ad75b8`: `return 0, 'snapshot_tampered'` path, no `CannotEvaluate`; tip: `CannotEvaluate` raises for absent/tampered, `return 2`, six public-CLI `run(...)` cases (met, matrix-mismatch, expected-tampered rc2, snapshot-absent rc2, note-absent, c2-gate-standard) spawning `sys.executable __file__`; committed counter SHA `ca2c8be9…6af3` = ExecGate's candidate SHA | evidence-verified (`after/measurements.txt` 6/6 rc0; `w1/ExecGate.md` §2 base 3/6 A/D/E fail, candidate 6/6; `measure-round81.py` committed at `80237118`, unchanged since: `git log 96ad75b8..4ffcbbd5 -- tools/measure-round81.py` → `80237118` only) |
| C3 freshness | findings 2→0 | for every `corpus/knowledge/*.md` at each rev: last `^verified-at:` line contains `YYYY-MM-DD`? | base 98 notes, 2 without a dated last line (`modprobe-config-plane-r72.md`, `module-parameter-plane-r71.md`); tip 99 notes, 0. Appended lines r72 :99 and r71 :75 read `verified-at: 2026-11-04 — snapshots re-verified at round 81`; filed line 4 unchanged in both | re-measured (plain); gate result evidence-verified |
| C3 premise | 7 snapshots re-verify | `(cd .ufo/waves/round-71/before/src && sha256sum -c SHA256SUMS)`; same for round-72; `git diff --stat 96ad75b8 4ffcbbd5 -- .ufo/waves/round-71 .ufo/waves/round-72` | 4/4 OK, 3/3 OK; no diff | re-measured |
| Census | 330→332, rc0 | `git show <r>:corpus/SOURCES.md \| grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`; `git diff --numstat … -- corpus/SOURCES.md`; `sources-census.sh validate --root … tsukuroi` | 330 → 332; `2 0` (append-only); `tsukuroi ok …`, rc 0 (W04 warnings only) | re-measured |
| SCORECARD | append-only | `git diff --numstat 96ad75b8 4ffcbbd5 -- SCORECARD.md` | `162 0` vs base: no line removed | re-measured |

Every finite number in the report reproduces. The admission failure is procedural (predicates
not declared before data), not numeric.

## Per-axis verdicts

| Axis | Verdict | Reason |
|---|---|---|
| depth | improved | a new eight-row mount-unit decision plane with three measured host legs, sources re-opened and agreeing; the self-assessed ordinal 8→9 is **not** endorsed by this closure (the lane's own second outcome block says "depth 8 → 8 … no uplift claimed") |
| operability | improved | could-not-evaluate now exits 2 through the public CLI; selftest drives six public-path cases (base 3/6 → 6/6 evidence-verified); ordinal unchanged |
| freshness | improved | two undated `verified-at` findings closed by appended dated lines backed by 7/7 snapshot re-checks I re-ran |
| coverage | unchanged | no frontier row moved (`corpus/README.md` "PROVINCE and the coverage frontier are unchanged") |
| calibration | unchanged | honest errata (chronology, dead seats, mutation survivors) offset by a new SCORECARD self-contradiction on depth (R81-V1); no net measured change |
| adjacency | unchanged | unworked this round |

## Discernment spot-check (`corpus/lessons/round-81.md` `## Gate`)

| Item | Gate decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S331 `nofail` quote | ADMIT (docs/A) | `curl https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml` (SHA matches pin); whole-file tag strip → lines 500-501 | agree | quote "With nofail, this mount will be only wanted, not required, by local-fs.target or remote-fs.target." present verbatim (14 words, ≤25); at stripped :500-501 as cited; raw XML places it two lines later (:502-503), matching the disclosed stripping convention |
| S331 `x-systemd.before=` quote | ADMIT | same file, stripped :232-234 | agree | "In the created mount unit, configures a Before= or After= dependency on another systemd unit, such as a mount unit." present (20 words) |
| S332 generator capture | ADMIT WITH CORRECTION (own-work/A) | `git show 4ffcbbd5:.ufo/waves/round-81/before/host/generator.txt` | agree | :77 holds the quoted `Options=` line; :141-145 list five `.requires` mounts, confirming the "four → five" correction; :1 header 2026-11-04T17:54:25-03:00 |
| ArchWiki "Fstab" | REJECT (no row) | `curl 'https://wiki.archlinux.org/index.php?title=Fstab&action=raw'` | agree | :175 carries `{{Accuracy|the nofail option does not work as described here.|section=3.2 External Device options}}`; :183 holds the 90-second quote; community page, no oldid pin, self-disputed — a correct reject |
| Reading "nofail guarantees no waiting even with Before=" | REJECT | S331 stripped :229-241 + S332 :70,:77 | agree | the manual documents `x-systemd.before=` ordering and `tmp.mount` carries `Before=local-fs.target` with `nofail` |

SOURCES row re-opened: `corpus/SOURCES.md` S331 (line 342) — anchor `nofail :498-504` is the
stripped span holding the gate quote above (≤25 words), raw SHA in the row equals my fetch.
Census validate rc 0.

## Trend verdicts

- **expansion — improved.** `corpus/knowledge/` 98→99 with `mount-unit-fstab-plane-r81.md` on
  ground the coverage map did not hold, citing new mined rows S331/S332 (330→332), both
  re-opened and agreeing.
- **quality — improved.** Two stale entries re-verify (dated `verified-at` appended over 7/7
  re-checked snapshots); the round-80 gate-standard defect is repaired; no admitted entry
  failed my re-check.
- **discernment — improved.** The outside spot-check agrees with the gate on three admits and
  two rejects; the wave's falsification of the author draft is visible in the landed entry.

## Routed defects (tsukuroi, owed round 82)

- **R81-V1 SCORECARD depth contradiction.** Two appended "Round 81 — measured outcome" blocks
  disagree: one says "Axes now: depth9 …", the other "depth 8 → 8 … no ordinal moves". Append a
  named correction stating one ordinal; this closure awards no uplift.
- **R81-V2 chronology.** Candidate scoring preceded the declaration; next round must commit
  declaration, no-work/forgery controls and instrument hashes before any candidate is scored.
  Round-81 claims are not retroactively admissible by later re-measurement.
- **R81-V3 attack seats.** Reviewer and critic died with no artifact (effective attack 1/12);
  replace dead attack seats in-round or report the floor as unmet.
- **R81-V4 counter coverage debt.** C1 13 behaviour-bearing mutant survivors of 18; C2 4 of 8
  plus the answer-key selftest class (`SKILL.md` counter-attack scoreboard).
- **R81-V5 anchor convention.** S331 row says the raw file is "two lines later above line 84";
  the offset applies to lines after raw 85 (one line after raw 3). Land the per-line strip
  (R81-CITED-LINES-STRIPPED) and restate the anchor rule unambiguously.

## Operator notes

SHONEN boxes are not fully checkable by a non-author this pass: box 3 still states "no
non-author has replayed it", and this closure did not replay the host task. No promotion.
