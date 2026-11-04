# Round 73 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)
round: tsukuroi 73 — report `.ufo/reports/round-73/tsukuroi.md` (commit `53e452c5ecf256268e94df6cae6bdecffbece941`,
lane identity); lane `eb1057575d5d8b940c4846e21611674cf5571aea..8985a81733289905040e2e889c9d7b99369804e4`;
measured revision `3cfa23ac4da7129fa8a614909af52fdfeae5c143`; declaration
`749371321c00f04d98c29d2c26b57d75a92d7e37`.
Digest (`.ufo/watchdog.log`, mutable — copied verbatim): `2026-11-03T22:57:20-03:00 launch tsukuroi round=73
pgid=1857750 driver=hyaku-inline attempt=1`; `2026-11-03T23:26:41-03:00 complete tsukuroi round=73;
hyaku-inline attempt=1`.

## 1. Step-1 conformance

- **Report attribution and landing.** `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H' --
  .ufo/reports/round-73/tsukuroi.md` → `tsukuroi-shokunin <tsukuroi@shokunin.local>
  53e452c5ecf256268e94df6cae6bdecffbece941`; author `2026-11-03 23:25:39 -0300` (committer 23:25:56), 10 s
  after the lane tip `8985a817` (`23:25:29`) — commit-then-report holds. `git merge-base --is-ancestor
  53e452c5 origin/master` → rc 0 and `git cat-file -e origin/master:.ufo/reports/round-73/tsukuroi.md` →
  present, so the report is pushed. The commit adds exactly one file, 142 lines (`git show --stat`).
- **SHONEN.** `grep -c '^## SHONEN' .ufo/reports/round-73/tsukuroi.md` → **1**, followed by **four**
  `- [~]` lines = the four `SHONEN.md` boxes, each with a pointer; `[x]` count → **0**; `SHONEN.md` is
  untouched (`git diff --stat eb105757 8985a817 -- SHONEN.md` → empty; `git show 8985a817:SHONEN.md |
  grep -c '\[x\]'` → 0).
- **Cited lane commits.** Nine hashes in "Landed changes" (`74937132 8eeadcb9 09dac09f 583eea87 3efb9b24
  b15f5167 65cc1f17 3cfa23ac 8985a817`) plus the base `eb105757`; each resolves (`git cat-file -e`) and
  `git merge-base --is-ancestor <h> refs/heads/master` → **ANCESTOR-OK** for all ten (git HEAD is detached
  in the jj-colocated repo, so ancestry was tested against the branch ref as required). The report's
  statement that the tip's only delta over `3cfa23ac` is the after-receipt checks out:
  `git diff --name-status 3cfa23ac 8985a817` → one added file
  (`.ufo/waves/round-73/after/measure-3cfa23ac.txt`, 36 lines).
- **Lane state.** `/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state
  …/tsukuroi-shokunin` → `branch=master local=8985a81733289905040e2e889c9d7b99369804e4
  remote=8985a81733289905040e2e889c9d7b99369804e4 ahead=0 behind=0 head=detached tracked=0 untracked=4`.
  `git status --porcelain` lists only four untracked dispatch/runtime markers
  (`.ufo/waves/round-66,w1.ready.dispatched`, `round-67/w1.ready.dispatched`,
  `round-73/w1.ready.dispatched`, `round-73/w1-run.stderr`); no tracked round work is uncommitted, and
  `git ls-remote origin refs/heads/master` reads `8985a817…`.
- **Prompt fidelity.** `.ufo/prompts/tsukuroi-round-73.md` is committed (author `tsukuroi-shokunin`,
  `22:56:39`, before the `22:57:20` launch line). Its §1–§5 head (lines 1–140, up to the §6 addendum) is
  the rendered `templates/round-prompt.md`: `diff` against the template shows placeholder substitutions
  only (`{{LANE}}`, `{{ROUND}}`, `{{FLEET_ROOT}}`, `{{AXES}}`, and the literal `<{{LANE}}-repo>` resolved
  to `tsukuroi-shokunin`). Five child-lane items present: report path/filename (§4), commit-then-report
  ordering (§5 first sentence + §6 item 4 "landed = committed and pushed"), the `SHONEN` heading with one
  mark per box (§4), cite-only-`landed <hash>` / the commit-hash citation rule (§4 Landed changes and
  measurement commits; §6 item 4), lane write scope (§6 item 3). Round-level items: MISSION/AXES §1,
  claims 1–3 §2, frontier §2b, L2 floor ≥8 in one batched call §3, commit-then-push §5, push scope §5, L0
  side channel §5. The quoted L2 route map matches `MISSION.md`'s role-class buckets (the table there is
  advisory to host routing; the run-15 operator map is quoted verbatim, no lane-repo model alias).
- **Wave.** `.ufo/waves/round-73/w1-results.json` → `seats=12`, `results=12`, no empty outputs; roster
  scout 1 / executor 3 / scribe 3 / connector 1 / reviewer 2 / critic 1 / mutation-tester 1 (L1 held
  planner) = strict attack 4/12 = 33 % (≥25 %), connector 1 (≤2), residual 0; `w1-spec.json`,
  `w1-dispatch.json`, `w1.ready` committed.
- **Report body.** All six required sections present with commands and commit pointers: not a marker.
- **Misroot.** `git -C /home/vgpnk/Projects/shokunin status --porcelain` shows only `.scratch/` (operator
  run state) and the pre-existing 24-byte `after` redirect file; no round-73 seat file sits in the fleet
  root. Nothing moved.
- **Conformance defects (status-neutral).** (1) two Gate-quote line anchors drift from the committed
  snapshot bytes — S306's `path = path_make_absolute(*name, config_path);` is cited `install.c:2387` but
  sits at `:2383` (2387 is the `create_symlink` call), and the S304 anchors each carry one extra edge line
  (`:367-370` actual 368-370; `:236-238` actual 237-238; `:238-240` actual 238-239); every quote itself is
  grounded, and the note's own `anchor` ranges contain them. (2) `LOG.md`'s Round 73 entry states the
  mid-wave counts ("a twelfth selftest case", "growing to eleven cases") while the final committed
  instruments print 13 and 14 cases; the lesson's `## Correction 2` and the SCORECARD "instruments at wave
  close" block carry the final values, but the append-only LOG carries no correction entry.
- **Step-1 result: ok.** No marker predicate; the report names real committed work.

## 2. Claim re-checks (non-author; commands run in this session)

I did not execute any lane gate or selftest (§Gate standard, Closure consequence). *Re-measured* means my
own grep/git/census count over committed bytes; *evidence-verified* means the claim rests on a committed
lane receipt whose values I read and cross-checked against the committed tool digest.

### C1 — depth (lowest tied, 8; SOURCED — S304–S306)

| Check | Command | Observed |
|---|---|---|
| note absent at base / present at tip | `git cat-file -e eb105757:corpus/knowledge/systemd-unit-load-plane-r73.md`; same at `8985a817` | rc **128** (`exists on disk, but not in 'eb105757'`); rc **0** |
| UL rows | `git show 8985a817:corpus/knowledge/systemd-unit-load-plane-r73.md \| grep -cE '^\| UL[0-9]+ \|'` | **6** (UL1–UL6) |
| distinct sources / snapshots | row `source=` / `snapshot=` cells | **3** (S304/S305/S306) / **3** (systemd.unit.xml, unit.c, install.c); reuse 2 each (≤2 as the counter pins) |
| registry rows | `git show <rev>:corpus/SOURCES.md \| grep -cE '^ {0,3}\| *S[0-9]{3,}'` | **303** base → **308** tip |
| knowledge notes | `git ls-tree --name-only <rev>:corpus/knowledge \| grep -c '\.md$'` | **90** base → **91** tip |
| new-row schema | `awk -F'\|' … NF!=13` over S304–S308; `grep -cE '^\| *S30[4-8] '` | 5 rows, malformed **0**; statuses S304–S306 `mined` with `used-by corpus/knowledge/systemd-unit-load-plane-r73.md`, S307/S308 `rejected` |
| snapshot digests (committed) | `git show 8985a817:.ufo/waves/round-73/before/src/<f> \| sha256sum` | `eb9479be…14c6` (systemd.unit.xml), `47e98d39…efcb7` (unit.c), `c11cd575…ef4d` (install.c) — all equal the note's `digest=` cells and `before/src/SHA256SUMS` |
| snapshot digests (live) | `curl -sS …/raw.githubusercontent.com/systemd/systemd/v262/<path> \| sha256sum` | HTTP 200 on all three; byte-identical to the committed snapshots |
| quotes grounded | whitespace-normalized token match of each UL `quote=` against its own snapshot | **6/6** found: UL1/UL2 in the XML (span 368-370 / 237-238 / 238-239), UL3 `unit.c:3908`, UL4 `unit.c:3875`, UL5 `install.c:2383`, UL6 `install.c:351`; every quote 4–19 words |
| lane counter receipt | `git show 8985a817:.ufo/waves/round-73/after/measure-3cfa23ac.txt` | `UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `UL_TARGET … met=1`, `rc=0`; header names tool sha256 `1f22c26b…` = the committed `tools/count-ul-rows-r73.py` bytes (evidence-verified) |
| selftest tally | same receipt + `after/wave-close-instruments.txt` | `SELFTEST: PASS (13 cases, 13 passed, 0 failed)` (evidence-verified) |
| census | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` | rc **0** (W04 duplicate-URL warnings only, all pre-existing) |
| ground unheld at base | `git grep -cE 'FragmentPath\|DropInPaths\|SYSTEMD_UNIT_PATH\|unit load path\|unit_need_daemon_reload\|unit_file_mask' eb105757 -- corpus/knowledge SKILL.md PROVINCE.md` | **0 matches** (rc 1); 12 knowledge files mention `drop-in` as host/mkinitcpio context, none a merge rule |

**Verdict: verified.** Every element of the before→after is reproduced by my own counts and digests; the
counter's `met=1` is the lane instrument's summary over those same facts.

### C2 — freshness (9)

| Check | Command | Observed |
|---|---|---|
| repair 1 — r72 lesson correction | `git show <rev>:corpus/lessons/round-72.md \| grep -c 'Correction (round 73'` | **0** at base → **1** at tip; block names both superseded sentences ("No capability row enters this round", "nine hermetic cases") and the ten-case landed state with the receipt pointer |
| repair 2 — instrument-digest erratum | `git show <rev>:SCORECARD.md \| grep -c 'R72-C3-INSTRUMENT-DIGEST-DRIFT'` | **0** → **2** (heading + body); names `df8a59c7…` → `2610ff43…` with the intermediates `123e1c57`/`53bcddef` and the same-instrument before/after receipt |
| repair 3 — capability refresh | `git show <rev>:SCORECARD.md \| grep -c 'Capability refresh — round 73'` | **0** → **1**; restates `gate-selftest` as ten cases with receipt `.ufo/waves/round-72/after/selftest-selftest-after.txt` (present at the tip; last line `SELFTEST: PASS (10 cases, 10 passed, 0 failed)`) |
| same-instrument before control | `after/c2-before-final-instrument.txt` | `--revision eb105757` → `ROUTED_STALE=3 ROUTED_OK=0/3` rc 1; `--revision a7015d27` → `ROUTED_STALE=3` rc 1 (final bytes, tool sha256 `71931c1c…` named in the receipt) |
| after verdict | `after/measure-3cfa23ac.txt` | `ROUTED_ITEM LESSON ok / DIGEST ok / CAPABILITY ok`, `ROUTED_STALE=0 ROUTED_OK=3/3`, `rc=0`; header names the committed checker sha256 `ad853877…` (= `git show 8985a817:tools/check-r72-routed-r73.py \| sha256sum`) |
| selftest tally | `after/wave-close-instruments.txt` | `SELFTEST: PASS (14 cases, 14 passed, 0 failed)` (evidence-verified) |
| t2 deletes nothing | `git diff --numstat eb105757 8985a817 -- SCORECARD.md SKILL.md PROVINCE.md LOG.md corpus/SOURCES.md corpus/README.md` | 44/0, 41/0, 255/0, 39/0, 5/0, 21/0 — insertions only |

**Verdict: verified (re-measured repairs + evidence-verified gate verdict).** The checker was not executed
by me; its committed receipts, its committed bytes, the tool digest named in each receipt, and the three
repairs in committed bytes were cross-checked.

## 3. Axis verdicts

| Axis | Before | After | Verdict | Evidence |
|---|---|---|---|---|
| depth | 8; no unit-load merge-plane note | 8; note UL1–UL6 on three tier-A snapshots, T1–T6 decision table, hosts readings + named limits | **improved** (content added on 0-hit ground; ordinal held at 8 as declared) | C1 table above; `SKILL.md:5974`; `PROVINCE.md:482`; `corpus/README.md:680` |
| coverage | 9 | 9 | unchanged | no new measured surface beyond the depth claim; the `PROVINCE.md` frontier→Core wording is documentation of the same note |
| operability | 9 | 9 | unchanged | no capability row entered (the report says so); both instruments are per-round gates over this round's objects |
| freshness | 9 | 9; three r72 routed defects closed | **improved** (stale statements fixed in committed bytes; ordinal held) | C2 table; `ROUTED_STALE=3` → 0 |
| calibration | 9 | 9 | unchanged | the report's SHONEN stays `[~]` with named limits (counter is a form instrument, answer-key risk, C2 denial leg, mid-wave instrument drift); no `[x]` written |
| adjacency | 8 | 8 | unchanged | `w1/C1Connector/report.md` (`GROUND_UNHELD=yes`); the note/skill/registry name the boundary; contested kaidoku/revenger ownership still reported, not absorbed |

No axis is harmed: the base→tip numstat over `SCORECARD.md`, `SKILL.md`, `PROVINCE.md`, `LOG.md`,
`corpus/SOURCES.md`, `corpus/README.md` is insertions-only; no axis text or row was deleted.

## 4. Discernment spot-check (LEARNING.md, checked from outside)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S304 systemd v262 `man/systemd.unit.xml` | admit (docs, tier A, mined) | `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml` | **agree** | HTTP 200, 165445 bytes, sha256 `eb9479be…14c6` = the committed snapshot = the note cell. The load-path override sentence is at `:368-370`, the drop-in precedence sentence at `:237-238`, the lexicographic sentence at `:238-239`; all are ≤25 words and within the row's anchor `:233-248`/`:364-378`. |
| S305 systemd v262 `src/core/unit.c` | admit (code, tier A, mined) | `https://raw.githubusercontent.com/systemd/systemd/v262/src/core/unit.c` | **agree** | HTTP 200, 263849 bytes, sha256 `47e98d39…efcb7` = committed snapshot = note cell. `any drop-ins that are masked are simply omitted from the list` at `:3908` and `For masked files check if they are still so` at `:3875`, both inside the row's `:3859-3915`/`:1439-1451` anchors. |
| S306 systemd v262 `src/shared/install.c` | admit (code, tier A, mined) | `https://raw.githubusercontent.com/systemd/systemd/v262/src/shared/install.c` | **agree** | HTTP 200, 140296 bytes, sha256 `c11cd575…ef4d` = committed snapshot = note cell. `path = path_make_absolute(*name, config_path);` at `:2383` and the dangling-alias message at `:351` ground UL5/UL6; the mask write (`create_symlink(&lp, "/dev/null", …)`) is at `:2387`. |
| S307 Arch rendered systemd.unit(5) | reject (same upstream text as S304, no divergence) | `https://man.archlinux.org/man/systemd.unit.5` | **agree** | HTTP 200, 135978 bytes, sha256 `69dba097…7916` = the recorded digest. After markup stripping the page carries the same load-path override, drop-in precedence and lexicographic sentences; no Arch patch sentence changes them, so the refusal ("grounds no rule S304 does not") and its flip condition are right. |
| S308 Arch core/systemd package page | reject (build provenance only) | `https://archlinux.org/packages/core/x86_64/systemd/` | **agree** | HTTP 200, 101009 bytes; body names `systemd 262.1-1`, `Last Packager Christian Hesse`, `Build Date`; `grep -icE 'lexicographic\|take precedence\|unit load path\|drop-in'` → **0**. Two consecutive fetches now differ at one line only — a per-response CSP `nonce=` (`…nonce="ySOIPCAOZaXR5U/wtNsCrQ=="` vs `…nonce="UcvSpYPJc51XUK45ewyf+g=="`), diff = 4 lines — so the row's "no content digest claimed, nonce-only divergence" is accurate (line 2962 in this fetch vs 2966 recorded; the nonce-only substance reproduces). |

The round recorded two real refusals with reason and flip after opened, measured fetches, closing
R72-GATE-NO-REJECT. The newly written rows' ≤25-word Gate quotes were re-opened against the sources above
(S304–S306), all locating correctly.

## 5. Trend verdicts (non-author)

- **expansion: improved.** Three admitted tier-A rows (S304–S306) on ground my own base sweep reads as
  unheld (0 matches for `FragmentPath`/`DropInPaths`/`SYSTEMD_UNIT_PATH`/`unit load path`/the six code
  anchors across `corpus/knowledge`, `SKILL.md`, `PROVINCE.md`; the 12 `drop-in` knowledge mentions are
  host/mkinitcpio context); one admitted entry (UL1–UL6) whose `source:` cites all three `mined` rows;
  registry **303 → 308**, notes **90 → 91**; two opened refusals kept as taste evidence.
- **quality: improved.** The three round-72 routed defects close in committed bytes (re-measured above)
  with a same-instrument `3 → 0` pair; both round-73 instruments were hardened by the wave's own attacks
  and their final bytes carry thirteen and fourteen named selftest cases with matching receipts; four
  overreaching note rows were rewritten to the reviewer's corrected sentences before landing
  (`ROWS_HOLD 2/6 → 6/6`, `w1/R1Reviewer/report.md`); no admitted entry was found false and left unmarked.
  The Gate-quote line drift and the LOG mid-wave counts are conformance defects routed in §6, not
  admitted-entry failures.
- **discernment: improved.** The outside spot-check agrees with the gate on all three admits and both
  rejects (the previous round's zero-rejection gap is now exercised with two measured refusals that keep
  reason and flip). No disagreement is left unlearned; no new QUALITY criterion was required.

## 6. Routed defects (lane owes these next round; status-neutral)

1. **R73-GATE-QUOTE-LINE-DRIFT (P3, quote location).** In `corpus/lessons/round-73.md` §Gate the S306
   quote is attributed to `install.c:2387` but the committed v262 snapshot carries
   `path = path_make_absolute(*name, config_path);` at `install.c:2383` (2387 is the
   `create_symlink(…, "/dev/null", …)` call), and the S304 anchors carry one extra edge line each
   (`:367-370` → 368-370, `:236-238` → 237-238, `:238-240` → 238-239). Quotes are grounded; append a
   corrected-anchor line naming these four citations (CORPUS "a quote names its location").
2. **R73-LOG-COUNT-STALE (P3, corrections sweep).** `LOG.md`'s Round 73 entry reads "a twelfth selftest
   case" and the checker "growing to eleven cases"; the final committed instruments are thirteen and
   fourteen cases (`tools/count-ul-rows-r73.py` sha256 `1f22c26b…`, `tools/check-r72-routed-r73.py` sha256
   `ad853877…`, `after/wave-close-instruments.txt`, lesson `## Correction 2`). The lesson and the SCORECARD
   wave-close block carry the final values; the append-only LOG has no correction entry. Append one
   naming the superseded counts.

## 7. Verdict

Both claims verify: C1 re-measured over committed bytes and live sources (digests, rows, quotes, counts),
C2 re-measured on the three repair blocks plus evidence-verified on the committed checker receipts and the
final instrument bytes. No axis is harmed. Conformance defects are status-neutral and routed above.
**admitted** — status `ok`.
