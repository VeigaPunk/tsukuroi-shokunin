# WWKD plan — tsukuroi round 11 (final: the closeout) (ufo-round-plan-v1)

Draft lane: PREP-S11 (2026-10-14, drafted during the round-10 wave, 32 lanes at
width). Design-time state read by this lane, not taken from a record: HEAD
`fac745b2813980014125390ff63defe0420b16d7` ("probation round 9 (training r8)")
with `git status --short` **0 lines at 20:50:48Z and again at 20:52:57Z** — the
round-9 landing is committed and the tree was clean at this draft's freeze
(20:50:48Z). The round-10 wave then began landing inside this lane's window:
at 20:53:53Z one untracked file was present —
`?? corpus/knowledge/census-closeout-receipt-r10.md` — and it was **moving**
(shape/hash only; **no content of it is cited as landed state below**): md5
`c1c4ee71…` / 178 `wc -l` at ~20:54Z → `c5041b5d03e38c774637f47a24304ca8` /
183 `wc -l` / 15 506 B / mtime 17:54:47 -03, that last reading stable across
two reads at ~20:55:5xZ and 20:56:03Z. **No pin below is taken from that
revision**, and no gate run was made against it. `plans/round-10.plan.md` (md5
`c905a263e7a343d2c84afb21262ec465`, 321 `wc -l`) is cited as a **plan**, never
as landed state; every round-10 statement below is a draft-time reading that
Step 0 resolves. Scratch: `/tmp/w10-preps11-tsukuroi/` (`live.out`,
`live.err`, `status-before.txt`). Write scope: **this file only**.

Post-freeze shape observation (20:57:15Z; **names only, no content read, no pin
taken**): the tree then carried **three** round-10 artifacts — the receipt
above, `corpus/knowledge/calibration-synthesis.md`, and
`plans/round-10-record-draft.md`. The round-10 wave is landing as this draft is
written; Step 0 resolves all three, and **the landed names govern** over any
name this plan proposes.

Round 11 is the arc's final round. Nothing in it presumes a round 12: every
item still open at this round's close is carried by the handoff's own
*what-is-not-here* section with its owner, never by a future plan.
Fleet-frame note, measured not smoothed: at 20:55Z the sibling lanes
`mado`/`tabi`/`tameshi` carried **no `plans/round-11*` file**, their round-10
plans' own text frames round 10 as the final training round, and the fleet's
train-ladder commits read `all lanes 8/10` at wave 9 — while this lane's
dispatch names round 10 the penultimate and round 11 the closeout. Recorded as
a fleet-level **[unknown] the dispatcher settles**; this plan is written to
stand as the lane's closeout on its own dispatch frame, and it claims nothing
about sibling arcs.

Axis move: **operability, terminal — the closeout: the lane's product handed
to its one remaining reader as one runbook, with the lane's own contracts
closed or named in the same artifact set.** ONE move, one subject (the
terminal state), three ordered legs: (1) the runbook; (2) the contracts it
closes (province, promotion checklist, lesson, coverage map, the gate's final
pin); (3) the non-author execution that tests the runbook. The round opens no
new ground: no new plane, no new gate arm beyond what round 10 lands, no
re-opening of any deferred class. The move's proof is not that the lane is
"done" — it is that a **non-author with no oral context can run the lane's
product from the runbook alone and reach the same verdicts**, and that every
unclosed item sits where the reader will look.

## Candidate decision (why this one)

Candidates considered at this draft: (A) the terminal handoff + closing
contracts (operability, terminal); (B) the coredump-storm watch (deferred
three times already); (C) the one-command identity re-derivation (round 10's
D12 proposal); (D) any round-10 claim that did not land; (E) an executable
update-safety go/no-go.

- (B) is real and measured, and it is deferred a **fourth** time, not
  rejected, with the sharpest anchors yet. One is **this lane's own capture**
  [obs]: live gate `coredump=523` this boot at 20:52:57Z, and
  `/var/lib/systemd/coredump` **484 files / 3.5 G** at ~20:56Z. The rest are
  cited captures, each with its source, none re-run here: 467 (round-9 plan's
  capture, 19:58:48Z, same boot), 269 (round-6 capture), 224 (round-3 report),
  and **443 files / 4.0 G** (round-10 plan's capture, 20:00:17Z). Against that
  last row the dir **shrank while the boot count grew** [unknown:
  retention/prune — the probe that would settle it is a `systemd-coredump`
  retention reading, not taken here]. The class still needs an app-level vocabulary and a second
  baseline before a watch can mean anything; ownership stays godot/node/LOVE
  app lanes + the journal workstream (boundary `oom-event-plane.md:43-52`).
- (C) is measured **absent at this pin** (`grep -n identity tools/tsukuroi-census.sh`
  hits comments only; `usage()` `:439-450` lists `--selftest`, `--sample N`,
  `--help`), so it is round 10's to land or leave — Step-0 debt, never this
  round's move.
- (D) is Step 0, not a candidate: a round-10 claim that did not land is
  finished first against the plan that specified it, never re-designed.
- (E) is declined for the final round: the `-Syu` go/no-go decision table is
  landed (`update-safety-v3.md`, md5 `2ac0c21d…`, 387 `wc -l`), the gate
  carries the plane as a live emitter (`:2328`), and the last round's job is
  to hand over, not to open ground.
- (A) is the move. The reader who is left when the lanes stop has no entry
  point today: `SKILL.md` is 1374 `wc -l` of append-only blocks, the corpus is
  21 landed notes, the gate's contract is scattered (`:249-306`, `:458-528`,
  `:855-930`), and the operator-facing action list is a round-3 snapshot
  (`host-health-report-r3.md`, md5 `98a0f263…`, 563 `wc -l`). The lane's own
  contracts are visibly open at HEAD, all measured here: `corpus/lessons/`
  **0 files** (`ls -A corpus/lessons/ | wc -l` = 0); `PROVINCE.md` unchanged
  since round 0 (`git log --follow -- PROVINCE.md` = `aea5fa2` only; no
  Core/Frontier/Adjacent rows); `SHONEN.md` unchanged since round 3
  (`git log -- SHONEN.md` = `9bcd162` + `aea5fa2`; md5 `9cf1d450…`, 51
  `wc -l`); `corpus/README.md` unchanged since round 3 (md5 `98bd0066…`, 20
  `wc -l`, rows stop at round 3, no `## Frontier` heading — headings measured
  `:1`, `:3`, `:17`); `SCORECARD.md` carries no `planned`/`retired`/axis-score
  rows at all (`grep` empty) while two of its move rows are malformed. A final
  round that leaves those to a round 12 that will not exist is not a record.

## Claim

(a) **The runbook lands.** Proposal: `HANDOFF.md` at the repo root — the
    operator's entry point, sibling of `SKILL.md`/`PROVINCE.md` (the realized
    name and placement are adjudicated at landing; measured: `PROTOCOL.md:406-417`
    enumerates the lane's file set and does not forbid an eighth file, while a
    `corpus/knowledge/` placement would bury the one reader this artifact
    exists for — if the landing lane relocates it, the coverage row moves with
    it). Six sections, every row citing a landed artifact re-hashed at
    dispatch, and **no row making a new host claim**:
    - §Run — the one command (`bash tools/tsukuroi-census.sh`), the final
      revision's identity (md5/sha256/`wc -l`/bytes **with the convention
      stated** — the census carries an unterminated final line, `main "$@"`),
      the declared case count, the read-only contract, the exit map
      (0/1/2, worst plane wins), and — only if round 10 landed the identity
      mode — its one-line form; otherwise the three classic commands.
    - §Read — one row per **emitted** plane (the realized set governs; 6 at
      this pin, `:2324-2329`, rollup `:2339`): what `DEGRADED` means there,
      the operator action, and the note that owns it. A row with no operator
      action is a finding, not a paragraph.
    - §Rules — the standing discipline as the reader's rules, citing the
      round-10 rows where they landed (or, if round 10 left them unlanded,
      the distilled copy with its own citations — never a new claim).
    - §Open — the debt register with owners (list in Step 0's carried ledger).
    - §Not here — the boundaries (detection never remediation, no install, no
      restart, secrets shape-only, no external sites), the deferred classes
      (coredump storm, V8 heap-OOM, hook/root-exec surfaces), and the register
      debts (below) — named, not glossed.
    - §Closing state — the promotion dossier (SHONEN box ↔ evidence pointer),
      the gate-arc table (each row a landed pin), and the re-derivation
      recipe any reader can execute.
(b) **The terminal contracts are closed or honestly named.**
    - `PROVINCE.md` gains **Core / Frontier / Adjacent** (`LEARNING.md:64-71`;
      `PROTOCOL.md:411` — declared surfaces must resolve): Core = the six
      probed surfaces (packages, systemd-user, journal/boot, drivers/firmware,
      update-safety, oom/kill-event), each citing a landed artifact; Frontier
      = measured-but-unheld (coredump attribution, V8 heap-OOM, hook/root-exec
      surfaces, root `-Qkk` delta); Adjacent = sibling-owned, report-only
      (kagi secrets, kaidoku/revenger RE, the journal workstream, the app
      lanes). Every declared Core surface is checked with a resolving command
      at landing.
    - `SHONEN.md`: the mechanical diff against the canonical seed
      (`PROTOCOL.md:419-431`, modulo `<name>` = `tsukuroi-shokunin`) is **run
      and its result recorded**; if non-conformant, the file is regenerated to
      the canonical form with one evidence line per box. `[~]` marks carry
      resolvable pointers; **`[x]` stays with the named non-author review** —
      no self-promotion.
    - `corpus/lessons/round-11.md` lands with the `## Gate` section (candidates
      considered / admitted / rejected with reasons) + the outside spot-check
      (**≥1 admit, ≥1 reject**, `LEARNING.md:37-43`), the spot-check run by a
      non-author seat. The never-written lessons for rounds 1–10
      (`corpus/lessons/` measured 0 files at HEAD; round 10 lands its own at
      most) are **named as a register debt** in the handoff §Not here and in
      this round's lesson — **never fabricated retroactively**: a retroactive
      Gate section would be a new claim about rounds already closed.
    - `corpus/README.md`: the final coverage rows (the round-4…10 back-rows
      verified, not assumed) **plus the `## Frontier` section owed since
      round 1** (`LEARNING.md:57-58`).
    - `SCORECARD.md`: the malformed move rows repaired **with their original
      text preserved verbatim** (the unescaped `|` escaped only; rows 16 and
      21 are both malformed at HEAD — row 16 reads `| 4 | freshness + depth |
      round-3 state | boot plane (299 L | wave-4 32-lane; VER-S1 |`, row 21
      truncates mid-parenthesis and still says "5-plane" against the realized
      six-emitter gate), the repair recorded in the LOG; plus the
      `AXES.md:33-39` contract's missing rows (axis scores with their counting
      commands, `planned`, `retired`) landed as the final self-assessment —
      or, where a score cannot carry its command, named in the handoff instead
      of scored [adjudicated at landing].
    - `SKILL.md`: the terminal append — the handoff pointer, the final identity
      pin, every live count restatement **moved together**, the closing
      errata. `LOG.md`: the closing entry (append-only; the round-9 line's
      "5-plane" wording is corrected by a new entry, never rewritten).
(c) **The runbook is tested by a non-author.** The executor seat — this is the
    post-append no-oral-context re-test owed since round 3 (`LOG.md:153-154`;
    `SHONEN.md:32-38`) — executes the gate with `HANDOFF.md` as the only entry
    point: run §Run's command, reproduce the identity pin and the plane
    set/rollup, walk **≥3 §Read action rows** to their owning notes, and record
    a per-step tally `SUFFICIENT`/`PARTIAL`/`MISSING` — whatever it is; the
    tally is the round's honest output either way (the round-3 precedent: 3
    MISSING landed as fixes, kept in the record). **D13**: the author's suite
    is author evidence and a self-identity is not a non-author check — this
    execution plus a non-author re-hash of the pins is the handoff's
    verification; any plane arm round 10 left unverified stays a **named open
    item**, never absorbed.

## Step 0 (mechanical, before any edit)

Round-10 landing check against its own measure — census revision (md5/sha256/
`wc -l`/bytes, **selftest count from an executed run**, emitted plane set ==
rollup keys, the identity mode's realized shape if landed), the synthesis note
(**the landed name governs**, not the plan's proposal), the standing-discipline
block in `SKILL.md`, README back-rows + `## Frontier`, the SCORECARD repair +
round-10 move row, `corpus/lessons/round-10.md`, the LOG entry, the SHONEN
state, the `update-safety-v2.md` append-only errata pointer (md5 `92803aea…`,
353 `wc -l` at HEAD — owed since round 9), and whether round 9's two planes got
their non-author verification (D13). An unlanded part is named debt finished
first against the plan that specified it, never re-designed. Then the carried
ledger item by item, each re-measured at dispatch: root `-Qkk` delta; the
18/19 sweep-summary split; `1password-beta` provenance (operator); the
`omarchy/1password-beta 8.12.42_32.BETA-1` `-Suu` trap row; `walker-restart.hook`
(kagi/operator); dkms stale `7.1.4-arch1-1`; `snapper` empty (no rollback net);
`offline.db` coverage (birth 2026-10-03 17:41:33, stale 85 d at this pin);
the "20-min cap" item (integrator); E4–E8 proposed-but-unapplied errata on
`oom-event-plane.md` (that note's owner applies them); round-6 H1–H3; the
OOM-counter lifecycle Q2; the round-2 wave-1 errata merge; the coredump-storm
and V8 heap-OOM classes; the AUR-drift watch's own receipt
(`aur-drift-receipt-r9.md`, md5 `e7d6f70b…`, 248 `wc -l`); and the never-written
lessons register. Then re-measure every pin below; a mismatch is recorded, not
smoothed.

## Anti-claim

No row makes a new host claim — every handoff row and every repaired record
cites a landed artifact re-hashed at dispatch, never quoted from this draft.
No host mutation: `-Qu`, `-Su* --print*`, `stat`, bounded reads only; `-Sy`/
`-Syu` never run; no transaction, no download, no db write, no service action,
no root; `db.lck` absent after every probe here and expected absent at landing.
No external site, no AUR RPC; secrets/session material shape-only. No
self-promotion (no `[x]` anywhere in this round's writes); no round-12
presumption; the runbook is **not** a remediation trigger and does not re-open
any deferred class; the coredump/OOM/hook/GSP/AUR classes stay with their
owners; the closeout does not re-design a round-10 unlanded item — it finishes
it against round 10's own plan. No artifact is re-measured from memory.

## Measure

`--selftest` rc=0 with `PASS (N cases)` from the **executed** run; N equals
every live restatement in `SKILL.md` (grep-checked, moved together); the live
run's emitted `PLANE` set equals the rollup keys of the same invocation; zero
mutation (fixture byte-unchanged + `git status` byte-identical before/after +
no `db.lck`); `HANDOFF.md` landed with md5/`wc -l` pinned, and **every command
in it executed** by the non-author seat; ≥3 handoff action rows and ≥2 pins
re-derived by a non-author; `PROVINCE.md`'s three sections present with every
declared Core surface resolving; the `SHONEN.md` mechanical-diff result
recorded; `corpus/lessons/round-11.md` landed with the spot-check verdicts
(≥1 admit, ≥1 reject); `corpus/README.md` `## Frontier` present; malformed
SCORECARD rows repaired with original text preserved; the terminal `SKILL.md`
append and the `LOG.md` closing entry landed; the closing SHONEN state recorded
with evidence, `[x]` left to the non-author review; the "what is not here"
section admits **every** open debt (grep-checked against Step 0's ledger).

Suggested seats: runbook seat (`HANDOFF.md`); province/coverage seat
(`PROVINCE.md` + `corpus/README.md`); record seat (`SKILL.md` append +
`SCORECARD.md` + `corpus/lessons/round-11.md`); executor seat (the no-oral-context
re-test); non-author verifier (rows + pins + the lesson's spot-check); scribe
(`LOG.md` + commit).

## Draft-time pins (this lane, 2026-10-14 20:50:48–20:56:03Z, read-only,
non-root, scratch `/tmp/w10-preps11-tsukuroi/`; re-run, never quote)

Line counts are `wc -l`; the census and `SKILL.md` carry an **unterminated
final line** (census ends `main "$@"`; `SKILL.md` Read 1375 vs 1374), so a pin
states its convention. HEAD `fac745b`; tree **0 entries at 20:50:48Z and
20:52:57Z**, **1 entry** at 20:53:53Z–20:56:03Z
(`?? corpus/knowledge/census-closeout-receipt-r10.md`, shape-only, moving —
no pin taken from it).

Census (HEAD blob, re-hashed): md5 `e32aac98c6b54f9d7fb8bc4f348cd467`, sha256
`c396662eeb5f435d841b0c1863903dba807aa9dcbc6a67b2439fdfb13670c650`, 2349
`wc -l`, 123 410 B, mtime 17:17:50 -03; `--selftest` rc=0 in 11.4 s `PASS (74
cases, 74 passed, 0 failed)` (74 `check` calls in source); live rc=1 in 2.78 s,
stderr empty, **6** `PLANE` emitters (`:2324-2329`), rollup
`TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED
journal=DEGRADED update-safety=DEGRADED oom=HEALTHY)` (`:2339`); zero mutation
(`git status` 0 lines before/after; no `db.lck`). Live captures 20:52:57Z:
`err=798 (coredump=523 kernel=139 other=136)`; `kerr=139 (oom=1 io=70 gpu=0
other=68)`; `drift=2[1password-beta,1password-cli]`; `foreign=16(known=16
new=0 drift=0 gone=0)`; `holds=pacman glibc`; update-safety `join=equal=1171
behind=0 ahead=1 src=sl+expac; chan=dbs=4 fetch=3d stamp=36d;
offline.db=present(stamp=85d birth=11d); trap=-Suu:1[omarchy/1password-beta
8.12.42_32.BETA-1]`; oom `window=boots=13 2026-10-03..2026-10-14; known=2[A,B]
new=0`; systemd `running failed=0`. Independent cross-probes (20:56Z):
`journalctl --list-boots | wc -l` = 14 (13 boots + header); `uptime -s`
2026-10-13 10:57:58; `/var/lib/systemd/coredump` 484 files / 3.5 G.

Artifact pins (full md5): `SKILL.md` `d276ecea1b1abaf5d6bbf6a6d7e31746` 1374
(109 322 B; restatements: 74 at `:1359`, `:1373`; history 49 at `:867`/`:928`/
`:1150`, 63 at `:1197`/`:1314`; round-9 append `:1172+`, addendum `:1345-1374`),
`SCORECARD.md` `da962e185f874e4686d92ab21a58572a` 21 (rows 16 and 21 malformed;
no `planned`/`retired`/axis-score rows), `LOG.md`
`68413998f6770e8b85ed88e5d8c693d3` 172 (last entry = round 9), `SHONEN.md`
`9cf1d450685ae0ed0d15dee1b54e8fd5` 51, `MINT.md`
`1d75fce9ed65ac6a22be115cc0c84055` 19, `PROVINCE.md`
`f1722b163a5c433b003de362ab93ee11` 19, `AGENTS.md`
`390017cff803cc8798dd3b51d48a82f0` 6, `corpus/README.md`
`98bd00668e84f18cf6781718c4d09ea0` 20 (9113 B; headings `:1`,`:3`,`:17`; no
Frontier), `corpus/QUALITY.md` `e31cef8e56f3666406ab9314d3de3f0e` 8,
`corpus/lessons/` **0 files**, `git ls-files` 46 files (21 under
`corpus/knowledge/`). Census anchors at this pin: `VERSION='census-v2'` `:323`,
`usage()` `:439` (no `--identity`; `grep -n identity` hits comments only),
probes `:530/:688/:754/:876/:1012/:1153/:1303`, `run_selftest()` `:1571`,
`main()` `:2286`, emitters `:2324-2329`, rollup `:2339`. Plans (md5 prefix /
`wc -l`): `round-2` `3563bd41…`/10, `round-3` `160a0272…`/13, `round-4`
`63c26bb1…`/10, `round-5` `0e9e8640…`/11, `round-6` `81a9be07…`/38, `round-7`
`bb915954…`/160, `round-8` `0bef822d…`/216, `round-9` `3a59d2ed…`/270,
`round-10` `c905a263…`/321; records `round-4-record-draft` `a44f15db…`/300,
`-5-` `899db964…`/453, `-6-` `4e9708ab…`/424, `-7-` `c1eed63a…`/425, `-8-`
`9e7399c3…`/448, `-9-` `b5d6681e…`/536; **no round-1 plan file** (`git log
--all -- plans/round-1.plan.md` empty). Corpus notes at this pin (md5 prefix /
`wc -l`): `aur-drift-receipt-r9` `e7d6f70b…`/248 · `aur-risk-plane`
`1a584300…`/341 · `aur-risk-plane-ver-s6` `b0de352d…`/133 · `-s7`
`4608743d…`/184 · `boot-plane` `e722b7a9…`/312 · `degraded-triage-r4`
`d57ae2d4…`/607 · `driver-firmware-plane` `518eda8f…`/256 ·
`executor-test-sufficiency` `4b2c1d36…`/219 · `foreign-provenance-r6`
`1b8f47a2…`/307 · `host-health-report-r3` `98a0f263…`/563 ·
`journal-boot-plane` `e5ca40da…`/430 · `kill-event-deep-r8` `6685e1da…`/340 ·
`memory-arm-mutants-s8` `a09e5604…`/181 · `memory-arm-ver-s8`
`861d83ad…`/251 · `oom-event-plane` `7e99d712…`/433 · `package-state-plane`
`ef93f1b7…`/323 · `systemd-user-plane` `af07a829…`/265 · `timer-drift-plane`
`fc0760c8…`/332 · `update-safety-note` `5cc3067f…`/478 · `update-safety-v2`
`92803aea…`/353 · `update-safety-v3` `2ac0c21d…`/387.

Deferred candidate (B) anchors for any later slot: live `coredump=523`
(20:52:57Z; 467 at 19:58:48Z same boot; 269 round-6 capture; 224 round-3
report); `/var/lib/systemd/coredump` 484 files / 3.5 G (20:56Z) vs 443 / 4.0 G
(20:00:17Z) — count up, size down [unknown mechanism]; per-app attribution
exists in notes (systemd-user-plane r1: godot 142 + node 47 in a 198-coredump
boot) but not in the gate; ownership godot/node/LOVE app lanes + the journal
workstream.

## Bounds & unknowns

Round-10 landing state at dispatch **[unknown — Step 0]**: the gate revision's
md5/count/case set and whether the identity mode landed; the synthesis note's
realized name and row set; the README back-rows, the SCORECARD repair, the
round-10 lesson, the LOG entry **[all unknown — Step 0]**; whether round 9's
two planes got their non-author verification **[unknown — Step 0]**; the
handoff's realized name/placement and section set **[design — adjudicated at
landing]**; the SHONEN mechanical-diff result **[unrun here — design; the diff
is the landing seat's first action]**; whether an axis score can carry its
counting command for all six axes **[design]**; whether the training ladder
ends at round 11 for every lane **[unknown — the dispatcher's frame; this
plan claims nothing about siblings]**; the promotion review outcome
**[non-author]**; the upstream Arch/omarchy delta since 2026-09-08 — **the**
real update gate — stays **[unknown] read-only** (the 36 d stamp is a
capture); `pacman.log` rotation window at dispatch **[unknown — the
`cmd=unknown` row is built for the miss]**; the coredump dir's shrink
mechanism **[unknown]**; carried: root `-Qkk` delta, `1password-beta`
provenance, `walker-restart.hook`, dkms stale `7.1.4-arch1-1`, `snapper` empty,
`offline.db` coverage, the "20-min cap", E4–E8 unapplied errata, H1–H3, the
OOM-counter Q2, the V8 heap-OOM and coredump-storm boundaries, the
`omarchy-walker`↔`walker` linkage (kaidoku/revenger), and the never-written
lessons register for rounds 1–10.

## Discipline (round 11 — final)

Host read-only (`PROVINCE.md:16-17`); no external sites; secrets shape-only;
one move; append-only errata (repairs preserve original text verbatim);
observation / inference / unknown separated; measured anchors only; no pin
from a moving revision (concurrent seats observed shape-only, as this draft
did with the round-10 receipt); nothing presumed beyond this round; no
self-issued promotion; write scope = the named artifacts only.