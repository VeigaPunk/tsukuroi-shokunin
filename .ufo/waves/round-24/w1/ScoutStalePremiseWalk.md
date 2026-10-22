# Planner data walk — statements that present as current at the round-24 declaration

Verdict: the five probed premise families are all present, but only two sites read as current
without any adjacent correction — `corpus/README.md:38` (pending mkinitcpio 42) and
`corpus/README.md:10` (sync dbs born 2026-10-11, `-Sy` never run since) — and the single most
authoritative-looking current-use pointer, `SKILL.md:1805-1814`, predates the 2026-10-20 09:15
full upgrade; the round-24 declaration row itself (`SCORECARD.md:749`) repeats 413 and the pending
mkinitcpio 42 upgrade in the present tense while describing the corpus, not the host.

## Method and revision boundary

I grepped the working tree at `HEAD 10b45f050c16f5f1d4f7e15a285d9f5294f7a486` for `413`,
`mkinitcpio`, `1.31.3`, `sync db`, `sync DB`, `sync database`, `-Syu`, and read the cited ranges.
I then re-checked the key loci with `git show f169b3ba:<file>`: `corpus/README.md:10` and `:38`,
`SKILL.md:50`, `:99`, `:377`, `:1658`, `:1833`, `:1927`, and `SCORECARD.md:425`, `:461`, `:526`
are byte-identical at the claim base. The round-24 declaration rows at `SCORECARD.md:748-751`
are not at `f169b3ba`; they landed with the declaration at `674891d`. All line numbers below are
working-tree numbers, and the base check above covers every line I rank as a hazard.

`pause-lift-gate-r24.md` is untracked (`?? corpus/knowledge/pause-lift-gate-r24.md`); the declared
gate file `corpus/knowledge/pause-lift-gate-r24.json` does not exist at this read. Statements
from the untracked draft are marked as draft, not corpus.

Exact-string negatives: `libinput-1.31.3` occurs nowhere; `-Syu would` (hyphen, no backtick)
occurs nowhere; `413` occurs in no `SKILL.md` or `PROVINCE.md` line. The `413` at
`corpus/knowledge/update-safety-v2.md:115` (`SKILL.md:408-413`) is a line-range citation, not a
pending count, and is excluded below.

## 1. `413`

| Site | Exact phrase | Class |
|---|---|---|
| `SCORECARD.md:425` | `pending/version state tied to capture rather than historical413 context` | Dated historical: round-15 declaration row; the word itself labels 413 historical. |
| `SCORECARD.md:461` | `installed libinput1.32.0-1, pending413 against October18 sync metadata` | Dated historical: round-15 appendix under `C2 snapshot captured2026-10-20T07:44:39Z`. |
| `SCORECARD.md:749` | `the corpus still records 413 pending upgrades and a pending mkinitcpio 42 upgrade` | Dated to the round-24 declaration, but present tense and used as the "Before" baseline; reads as a host claim although grammatically about the corpus. |
| `corpus/knowledge/host-health-report-r3.md:591` | `It records `pacman -Qu` exit 0 with 413 pending rows against sync DBs born` | Dated snapshot (R15 banner, 2026-10-20T07:44:39Z); reads current at the locus. Corrected 37 lines below at `:628`. |
| `corpus/knowledge/host-health-report-r3.md:628` | `neither 413 nor zero is current` | The correction itself: dated R18 notice, reads current. |
| `corpus/knowledge/partial-upgrade-recheck-r15.md:14` | `| `pending_updates` | `413` |` | Dated historical: snapshot table row, `verified-at: 2026-10-20`. |
| `corpus/knowledge/partial-upgrade-recheck-r15.md:32` | `empty stderr returned **413** rows` | Dated historical: same 2026-10-20 section. |
| `corpus/knowledge/partial-upgrade-recheck-r15.md:43` | `The numeral 413 matches the pending-413 numeral stated in the round context` | Dated historical: explicitly refuses to treat the round context as a measured source. |
| `corpus/knowledge/partial-upgrade-recheck-r15.md:68` | `413 is the delta against the 2026-10-18 local` | Dated historical. |
| `corpus/knowledge/partial-upgrade-recheck-r15.md:138` | `the 413 count and 1.32.0-1 are re-readable from the snapshot` | Dated historical: falsifiability bullet bound to the snapshot. |
| `corpus/knowledge/partial-upgrade-recheck-r15.md:173` | `The 413 pending count was NOT re-measured` | Dated historical: explicitly not refreshed. |
| `corpus/knowledge/partial-upgrade-recheck-r15.md:176` | `the pending set was consumed by that transaction, so 413 is not a current-use value` | Dated historical: explicit anti-current statement. |
| `corpus/knowledge/update-safety-note.md:510` | `It records `pacman -Qu` exit 0 with 413 pending rows against sync DBs born` | Dated current-use pointer (`## R15-UPDATE-STATE (2026-10-20)`, "For current use on 2026-10-20 read"); reads current at the locus. Superseded 15 lines below at `:525`. |
| `corpus/knowledge/update-safety-note.md:525` | `the413 pending count remains a dated R15 snapshot` | Correction, dated R18. |
| `corpus/knowledge/update-safety-v2.md:380` | `It records `pacman -Qu` exit 0 with 413 pending rows against sync DBs born` | Dated current-use pointer; reads current at the locus. Superseded at `:395`. |
| `corpus/knowledge/update-safety-v2.md:395` | `the413 pending count remains a dated R15 snapshot` | Correction, dated R18. |
| `corpus/knowledge/update-safety-v3.md:407` | `It records `pacman -Qu` exit 0 with 413 pending rows against sync DBs born` | Dated current-use pointer; reads current at the locus. Superseded at `:461`. |
| `corpus/knowledge/update-safety-v3.md:461` | `the413 pending count remains a dated R15 snapshot` | Correction, dated R18. |
| `corpus/knowledge/pause-lift-gate-r24.md:17` | `## P1 — pending upgrades (the corpus says 413)` | Untracked draft; attributes 413 to the corpus, not the host. Reads current only for the draft. |
| `corpus/knowledge/pause-lift-gate-r24.md:21` | `The 413-row figure of 2026-10-20T07:44Z` | Untracked draft; treats 413 as discharged by the 09:15 upgrade. |

No `413` in `SKILL.md`, `PROVINCE.md`, or `corpus/README.md`.

## 2. `pending` together with mkinitcpio

| Site | Exact phrase | Class |
|---|---|---|
| `corpus/README.md:38` | `Pending `mkinitcpio` 42 upgrade strands two `/new_root` hooks` | Reads current: Frontier bullet, no date, no inline notice. Superseded only at `corpus/README.md:144-151` (106 lines below), and `:164` says Frontier bullets "remain superseded by their explicit later entries, not silently rewritten". |
| `corpus/README.md:144-151` | `superseded for this host: the upgrade ran on 2026-10-20` | Dated historical correction. |
| `corpus/README.md:19` | `mkinitcpio v42 `/sysroot` change vs two `/new_root`-hardcoding hooks` | Descriptive index cell of the recovery note, not a pending-upgrade claim; reads current but is not a state assertion. |
| `SKILL.md:1658` | `busybox hooks hardcode `/new_root` and `mkinitcpio` ≥42 is the candidate` | Reads current: row in the "Check before `-Syu`" table, no date, no notice. 42.2-1 has been installed since 2026-10-20 (`SKILL.md:1927`; capture line 63), so "is the candidate" is stale. |
| `SKILL.md:1833` | `Installed `mkinitcpio 41.1-1` with 42.2-1 pending` | Dated 2026-10-20 by its Round 15 section, but present tense; reads current at the locus. Explicitly superseded at `:1927` (94 lines below). |
| `SKILL.md:1927` | `The "Installed `mkinitcpio 41.1-1` with 42.2-1 pending" reading is superseded` | Correction, dated R18. |
| `SCORECARD.md:749` | `a pending mkinitcpio 42 upgrade` | Dated to the declaration, present tense; reads as the host baseline. |
| `corpus/knowledge/host-health-report-r3.md:594` | ``mkinitcpio 41.1-1` installed with 42.2-1 pending` | Dated snapshot; reads current at the locus. Corrected 35 lines below at `:629` (42.2-1 installed, pending newer row unknown). |
| `corpus/knowledge/update-safety-note.md:513` | ``mkinitcpio 41.1-1` installed with 42.2-1 pending` | Dated current-use pointer; superseded at `:527`. |
| `corpus/knowledge/update-safety-v2.md:383` | ``mkinitcpio 41.1-1` installed with 42.2-1 pending` | Dated current-use pointer; superseded at `:397`. |
| `corpus/knowledge/update-safety-v3.md:410` | ``mkinitcpio 41.1-1` installed with 42.2-1 pending` | Dated current-use pointer; superseded at `:463`. |
| `corpus/knowledge/partial-upgrade-recheck-r15.md:13` | `mkinitcpio 41.1-1; systemd 261.2-1` | Dated historical snapshot row; corrected at `:175`. |
| `corpus/knowledge/arch-news-gate-2026.md:21` | `Current package is below the article's version threshold.` | Table row keyed by the 2026-09-22 article; reads as a host-state claim. Corrected 68 lines below at `:89` (42.2-1 installed, TPM2 condition still unmet). |
| `PROVINCE.md:22` | `Initramfs v42 and boot recovery` | Scope row only; no pending claim. |

## 3. `libinput-1.31.3` cache revert

| Site | Exact phrase | Class |
|---|---|---|
| `corpus/knowledge/partial-upgrade-recheck-r15.md:23` | `(1.31.3-1 -> 1.32.0-1)` | Dated historical: quoted `upgraded libinput` log line at `2026-10-20T04:25:17-0300`. |
| `corpus/knowledge/partial-upgrade-recheck-r15.md:67` | `1.31.3 versus 1.32.0 in memory is `[unknown]`` | Bounded unknown from the 2026-10-20 measurement; not a cache claim and not asserted as known. |
| `corpus/knowledge/pause-lift-gate-r24.md:51` | `The libinput 1.31.3 cache file named as a revert option in the L0 question is gone` | Untracked draft; reads current and asserts a negative about the package cache. Not in the committed corpus. |

No committed lane file claims a `libinput 1.31.3` cache revert option exists. The only committed
mentions of 1.31.3 are the historical log quote and the running-version unknown above, so a
planner cannot source the "cache revert" premise from the corpus; it exists only in the untracked
draft and the round question.

## 4. `sync DB` age

| Site | Exact phrase | Class |
|---|---|---|
| `corpus/README.md:10` | `sync dbs born 2026-10-11, `-Sy` never run since` | Reads current: index row with no date or notice. Contradicted by the R15 measurement (all five dbs born 2026-10-18, `partial-upgrade-recheck-r15.md:15,32-33`) and by later refresh activity. |
| `SKILL.md:50` | `sync dbs born **2026-10-11 12:54:13.542**` | Dated cell: the table heading is "Measured 2026-10-14". The adjacent criterion "snapshot recent (≤7 days by `%w`)" reads as current guidance. No notice at this line; R15/R18 supersession does not cover it. |
| `SKILL.md:99` | ``pacman -Qu` → empty here, **rc=1**` | Reads current: checklist step 2, no date, no notice. Contradicted by the round-24 capture (`pacman -Qu` exit 0, 3 rows). |
| `SKILL.md:201-202` | `Re-derived in-lane (TSUKUROI-4, 2026-10-14)` … `stat '%w'` sync dbs (birth 2026-10-11 12:54:13.542)` | Dated historical. |
| `SKILL.md:218-220` | `birth (`%w`) = 2026-10-11 12:54:13 (3 days)` | Dated historical correction block (2026-10-14). |
| `SKILL.md:956-957` | `db births 2026-10-11 12:54:13.542` | Dated historical receipt (round-6 ledger). |
| `SKILL.md:1646-1648` | `[obs] This host ran bare `-Sy` twice` | Dated historical (2026-10-19). The "twice" completeness is superseded by later refresh and full-upgrade activity, which the sentence does not know about [inf from the C2 context]. |
| `SKILL.md:1805-1814` | `Current-use update state on 2026-10-20 is` … `The dated decision is `BLOCKED_FOR_AGENT_PACKAGE_ACTION`` | Dated current-use pointer (2026-10-20 07:44 snapshot), but reads as the lane's authoritative current-use answer; it predates the 09:15 full upgrade. |
| `corpus/knowledge/package-state-plane.md:71` | `pacman -Qu` = 0 rows vs sync db` | Dated historical (2026-10-14 note); R18 supplement at `:435` says the zero-pending readings are not current. |
| `corpus/knowledge/package-state-plane.md:75-78` | `All four configured sync dbs were **born** 2026-10-11 12:54:13.542` | Dated historical; superseded at `:360` (five `.db` files observed, not four). |
| `corpus/knowledge/driver-firmware-plane.md:183-185` | `Local sync DB snapshot` (core/extra/multilib mtimes 2026-09-08; omarchy 2026-10-11) | Dated historical (2026-10-14 probes). |
| `corpus/knowledge/host-health-report-r3.md:310-312` | `core/extra/multilib carry **2026-09-08** content stamps (36 days at measurement)` | Dated historical (2026-10-14). |
| `corpus/knowledge/partial-upgrade-recheck-r15.md:15` | `shared birth (`%w`) of all five `.db` files` | Dated historical; `:178` withdraws the all-five shared-birth claim for current use. |
| `SCORECARD.md:26` | `births 2026-10-11 12:54:13.542` | Dated historical: round-1 measured-outcome table (2026-10-14 re-run). |
| `SCORECARD.md:461` | `against October18 sync metadata` | Dated historical snapshot. |
| `corpus/knowledge/pause-lift-gate-r24.md:43` | `The core and extra database files carry mtimes 2026-10-17 22:37 -03` | Untracked draft; reads current. |

## 5. `-Syu would`

The literal string does not occur. The nearest counterfactual statements are:

| Site | Exact phrase | Class |
|---|---|---|
| `corpus/knowledge/update-safety-note.md:39` | `An `-Syu` started right now would perform 0 package actions.` | Dated 2026-10-14, but "right now" reads current; superseded at `:501-503` (462 lines below). |
| `corpus/knowledge/update-safety-note.md:360-361` | ``-Syu` right now, as measured: `INERT`` | Dated 2026-10-14 capture; reads current at the locus; same notice at `:501`. |
| `corpus/knowledge/update-safety-note.md:281-282` | ``pacman -Suu` would downgrade it to an older beta` | Dated 2026-10-14; the premise (installed ahead of channel) is reversed by the round-24 capture [obs]. |
| `SKILL.md:377` | ``-Syu` right now: `INERT` — 0 candidates` | Date is in the preceding line ("Composed verdicts (measured 2026-10-14)") but the bullet reads current; superseded only at `:1805-1814`, 1428 lines below. |
| `SKILL.md:382` | ``-Suu` would downgrade `1password-beta` (installed BETA-32 ahead of channel BETA-1)` | Dated parenthetical; premise reversed by the round-24 capture [obs]. |
| `corpus/knowledge/update-safety-v2.md:253` | ``-Syu` would be INERT: 0 actions` | Dated 2026-10-14 table row; round-15 notice at `:370-371`. |
| `corpus/knowledge/update-safety-v3.md:216` | ``-Syu` would be INERT: 0 candidates by three probes` | Dated 2026-10-14 table row; notices at `:397-400` and `:441`. |
| `corpus/knowledge/update-safety-v3.md:183` | `the single action a `-Suu` would perform today` | Dated 2026-10-14 but says "today"; premise reversed by the round-24 capture [obs]. |
| `corpus/knowledge/degraded-triage-r4.md:77` | `plain `-Syu` ignores, `-Suu` downgrades` | Dated note (round 4), reads as a standing behavior claim; premise reversed by the round-24 capture [obs]. |
| `corpus/knowledge/degraded-triage-r4.md:393-395` | `keeps the installed BETA-32 during plain `-Syu`; `-Suu` explicitly downgrades` | Dated note, reads as a standing behavior claim; same premise. |
| `PROVINCE.md:13-14` | `what an -Syu would touch` | Scope description, not a state claim; no stale premise. |

## Highest-risk reads for the planner

1. `corpus/README.md:38` is the only pending-mkinitcpio statement with no correction in its
   immediate neighbourhood. The correction is at `corpus/README.md:144-151`, beyond the Frontier
   section an index reader stops at. [obs]
2. `corpus/README.md:10` and `SKILL.md:50` both carry the 2026-10-11 birth stamp as if current;
   the R15 measurement says all five dbs were born 2026-10-18 14:11 -03, and the R18 notice says
   core.db mtime is 2026-10-17 22:37 -03. [obs at the cited lines]
3. `SKILL.md:99` says `pacman -Qu` is empty with rc=1. The round-24 capture shows exit 0 with
   three rows (`1password-beta`, `chatgpt-bin`, `claude-code`), so a planner copying the
   checklist value gets the opposite sign. [obs: `.ufo/waves/round-24/capture/l1/capture.txt:40-43`]
4. `SKILL.md:1658` still calls mkinitcpio 42 a candidate; 42.2-1 is installed
   (`SKILL.md:1927`, capture line 63). [obs]
5. `SKILL.md:1805-1814` presents `BLOCKED_FOR_AGENT_PACKAGE_ACTION` as the current-use update
   state. It is bound to the 2026-10-20 07:44 snapshot, which the 09:15 full upgrade and the
   round-24 capture supersede; no later SKILL notice corrects this pointer. [obs]
6. The `1password-beta` downgrade trap has reversed. The corpus says installed BETA-32 is ahead
   of channel BETA-1 (`update-safety-note.md:281-282`, `SKILL.md:382`, `degraded-triage-r4.md:77`).
   The round-24 capture lists `1password-beta 8.12.42_34.BETA-1 -> 8.12.44_25.BETA-1` as pending,
   so plain `-Syu` now updates it and the "one ahead" join is not current. [obs: capture lines 40-42]
7. `SCORECARD.md:749` is this round's own "Before" cell and repeats 413 and a pending
   mkinitcpio 42 upgrade in the present tense. It is true as a statement about the corpus text,
   but it is not a host measurement and it contradicts the capture; the gate should quote the
   capture, not this row. [obs/inf]
8. `pause-lift-gate-r24.md` is untracked and its P1 heading and P5 cache statement read as
   current, while the declared JSON gate file is absent. The gate artifact must be written at
   `corpus/knowledge/pause-lift-gate-r24.json`, not inferred from this draft. [obs]
9. Live-capture caveat: `.ufo/waves/round-24/capture/l1/capture.txt` is 198 lines at this read,
   while the draft and the C2 description cite lines up to 706. The gate's "every evidence line
   exists" condition has to be re-checked after the committed capture lands; a citation to a
   line number that does not exist would make the premise not count. [obs/unk]

Scope: read=SKILL.md, PROVINCE.md, corpus/README.md, corpus/knowledge/*.md (grep plus targeted ranges), SCORECARD.md, .ufo/waves/round-24/capture/l1/capture.txt (lines 35-63), pause-lift-gate-r24.md, git objects at f169b3ba; wrote=.ufo/waves/round-24/w1/ScoutStalePremiseWalk.md; executed=read/grep/glob tool calls, git status, git ls-files, git show f169b3ba:<file>, git rev-parse HEAD, wc -l, ls
Installs: none
