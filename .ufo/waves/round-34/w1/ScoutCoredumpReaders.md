# ScoutCoredumpReaders — C2 coverage sweep

Verdict: the two journal phrases are not already distinguished anywhere in the named files, so that split is not existing coverage; the census `coredump=` number is already restated as coredumps, cores or a crash storm in many notes, so a claim that "what the count counts" is uncovered ground would overclaim.

Worktree read: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` as it stood during this sweep (declaration commit `6de666c427ba9aa6b4350561980bde8d0e7c261d` was not checked out here; these are the working-tree files). [obs]

## 1. What the count actually is [obs]

`tools/tsukuroi-census.sh:1403-1410` counts boot-0 `journalctl -b -p err -o json` lines whose JSON text matches `"SYSLOG_IDENTIFIER":"systemd-coredump"`, then publishes that integer twice: `coredump=<n>` inside the PLANE journal note (`:1409`) and `HANDOFF ADJ-04 mori class=coredumps value=<n>` when `JRN_COREDUMPS` is at least 1 (`:2780-2782`). The awk rule does not read `MESSAGE`. [obs]

The header names the same integer "boot-0 coredump entries" (`:67`). The comment above the assignment names it a "coredump count" (`:1401`). [obs]

Fixtures prove message text is irrelevant. The selftest plants `MESSAGE` as the byte array for "godot" and expects `coredump=1` (`:2198-2200`). The handoff selftest and `tools/score-census-handoff-r32.py:390-391` plant `Main process terminated with signal N (Segmentation fault)`, which is neither phrase, and expect `class=coredumps value=` equal to the planted identifier count (`tsukuroi-census.sh:2693-2699`). [obs]

## 2. Commands

Sweep set: `SKILL.md`, `PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/*.md` (53 markdown files), `tools/tsukuroi-census.sh`, `tools/score-census-handoff-r32.py`. 58 files. [obs]

1. Pattern `coredump` over those six roots (search tool). Exit was a hit list, not a shell status.
2. Pattern `class=coredumps|coredumps` over the same roots.
3. Pattern `dumped core|without generating a coredump|terminated abnormally` over the lane, then narrowed to the sweep set.
4. Exhaustive enumerator, exit 0: Python 3.14.8 walk of the 58 files, case-insensitive `coredump|JRN_COREDUMP|class=coredumps|dumped core|without generating|terminated abnormally`. Result: 211 hits, written to `/fast/scratch/hyaku/tsukuroi-r34/ScoutCoredumpReaders/hits.tsv`.
5. Second pass, because "cores" and "crashes" do not contain the substring `coredump`: pattern for cores, crash storm, crash-loop and crashes over the same roots, and a number pass for the capture series 198, 207, 208, 211, 220, 224, 244, 269, 279, 467, 522, 523, 752. The number pass is noisy (package counts, boot monotonic 244.159, line numbers); only hits that restate this class are kept below.

Equivalent commands, from the lane root:

    rg -n -i 'coredump|JRN_COREDUMP|class=coredumps' SKILL.md PROVINCE.md corpus/README.md corpus/knowledge tools/tsukuroi-census.sh tools/score-census-handoff-r32.py
    rg -n -i 'dumped core|without generating|terminated abnormally' SKILL.md PROVINCE.md corpus/README.md corpus/knowledge tools/tsukuroi-census.sh tools/score-census-handoff-r32.py
    rg -n -i 'cores|crash storm|crash-loop|crashes' SKILL.md PROVINCE.md corpus/README.md corpus/knowledge tools/tsukuroi-census.sh tools/score-census-handoff-r32.py

Labels: (a) the hit calls the counted thing an entry or entries; (b) it calls that number coredumps, cores, crashes, or a crash/coredump storm; (c) field name, tool name, class label, disk path, ownership, or a line that says both. A line that only names `coredumpctl` or `/var/lib/systemd/coredump` is (c) and is not a restatement of the census integer.

## 3. Does any note already split the two phrases? [obs]

No. Zero hits for `without generating` in the sweep set. The two phrases are never paired.

Nearest misses, none of which is that split:

- `corpus/knowledge/driver-firmware-plane.md:170` — "191 `dumped core` lines in journal". A raw-line count of one phrase (the same note's 60,941-line trap is at `:171`). It does not mention entries that did not generate a core, and 191 is not the census `coredump=` figure. (b) for "dumped core lines", but a different unit.
- `corpus/knowledge/oom-event-plane.md:45` — pairing key `systemd-coredump … terminated abnormally` against `FatalProcessOutOfMemory`. Not the full "without generating a coredump", and not contrasted with "dumped core". The 15 is a backtrace pairing, not `coredump=`.
- `corpus/knowledge/systemd-user-plane.md:142` — coredumpctl `corefile` "172 present / 19 missing / 7 none" on 198 records. That is stored-versus-absent core files on a tool the census refuses to probe (`tsukuroi-census.sh:264-266`). It is not the journal MESSAGE split.
- `corpus/knowledge/systemd-user-plane.md:166-167` — coredump `MESSAGE` in `-o json` is a byte array, so string pipelines yield `<binary-message>`. Explains why a MESSAGE-text split was not done; it does not do the split.
- `corpus/knowledge/oom-event-plane.md:321` and `corpus/knowledge/kill-event-deep-r8.md:234` — SIGKILL "produces no coredump" / "leaves no coredump". A different absence (signal 9, no core), not the systemd storage message.
- `corpus/knowledge/kill-oom-boundary-r33.md:27` — "this lane counts by `SYSLOG_IDENTIFIER` over merged boot-0" and "Neither is a victim count or an OOM cause". Refuses a victim reading. Still does not split the two phrases.

Outside the sweep set, `LOG.md:1315` already states the 2026-10-23 boot-0 split (1604 `systemd-coredump` error entries, 183 "dumped core", 1348 "terminated abnormally without generating a coredump") and says the census counts all of them as `coredump=`. That sentence is this round's declaration, not a prior knowledge note. [obs]

So the phrase split is not existing coverage. It is also not a blank frontier: the identifier-versus-victim point is already written at `kill-oom-boundary-r33.md:27`, `PROVINCE.md:193`, `SKILL.md:2753` (situation cell) and `tsukuroi-census.sh:67`. [inf]

## 4. (b) Says coredumps, cores, crashes, or a storm

These restate the journal-class integer, or the same capture series (198, 207, 211, 220, 224, 244, 269, 279, 467, 522, 523, 752), as coredumps, cores or a crash.

- `corpus/README.md:8` — "coredump census (198 this boot: godot 142, node 47)". The underlying section 6 is coredumpctl length, which that note equates to the entry count; this row does not say entries.
- `corpus/README.md:13` — "≈207 coredumps". 207 is the class-table cell at `journal-boot-plane.md:96`.
- `corpus/knowledge/journal-boot-plane.md:48` — "of which 207 are coredumps" and "the crash storm".
- `corpus/knowledge/journal-boot-plane.md:8` — "a coredump storm is running".
- `corpus/knowledge/journal-boot-plane.md:332-333` — "during a crash storm" and "coredump 198→208".
- `corpus/knowledge/calibration-synthesis.md:141` — "coredumps 198→208→211→220→224".
- `corpus/knowledge/host-health-report-r3.md:389` — "coredumps 208 → 211" beside "err entries 248 → 251". The class series is coredumps; the err total is entries.
- `corpus/knowledge/host-health-report-r3.md:9` — "a coredump storm is running".
- `corpus/knowledge/host-health-report-r3.md:35` — "the live coredump storm (J1)".
- `corpus/knowledge/host-health-report-r3.md:243` — "coredump storm (the plane's DEGRADED driver)".
- `corpus/knowledge/host-health-report-r3.md:388` — "while the crash storm runs" (next line is the 208→211 coredumps).
- `corpus/knowledge/host-health-report-r3.md:640` — "the live coredump storm (J1)".
- `corpus/knowledge/degraded-triage-r4.md:69` — "244 cores in 3 measured classes". 244 is `coredump=244` on `:45` and `:51`. Missed by a `coredump` grep.
- `corpus/knowledge/degraded-triage-r4.md:80` — "244 cores/2 h".
- `corpus/knowledge/degraded-triage-r4.md:270` — "journal err mass (244/407), 3.9 G cores".
- `corpus/knowledge/degraded-triage-r4.md:427` — "244 cores in ~2 h".
- `corpus/knowledge/degraded-triage-r4.md:431` — "the coredump rate is quiet".
- `corpus/knowledge/oom-event-plane.md:49` — "coredump storm (round-4 count 244, not re-measured here)".
- `corpus/knowledge/census-closeout-receipt-r10.md:183-184` — "the coredump-storm class (its count here — 523 — is a capture)".
- `corpus/knowledge/closeout-r11.md:255-256` — "the coredump storm … 752 this window". 752 is `coredump=752` on `:54`.
- `SKILL.md:1627` — "coredump storm (523 at round 10's capture; 752–781 in the round-11 window's captures".
- `corpus/knowledge/aur-drift-receipt-r9.md:63` — "live coredump storm, moving counts".
- `corpus/knowledge/boot-plane.md:8` — "a coredump storm".
- `tools/tsukuroi-census.sh:270` — "the live coredump storm".
- `tools/tsukuroi-census.sh:1401` — "JRN_COREDUMPS is the boot-0 coredump count".
- `tools/tsukuroi-census.sh:2666` — "the journal plane's own coredump count".
- `tools/tsukuroi-census.sh:2697` — "boot-0 coredumps route one coredumps handoff, value = the boot-0 count".

Related (b) counts that are not the census integer, kept so a later declaration does not treat them as the same unit:

- `SKILL.md:48` second clause — "Coredumps this boot 198: godot 142 SIGABRT, node 47". Same digits as the entry class on that line; the breakdown is the coredumpctl table (`systemd-user-plane.md:128-141`).
- `SKILL.md:174-175` — "fleet-app crashes (`grok-bot`, `chrome_crashpad` coredumps above)".
- `corpus/knowledge/driver-firmware-plane.md:170` — "191 `dumped core` lines".
- `corpus/knowledge/driver-firmware-plane.md:213` — "the 142 godot coredumps".
- `corpus/knowledge/oom-event-plane.md:44` and `:432` — "15 distinct coredumps" (V8 backtrace pairing).
- `corpus/knowledge/systemd-user-plane.md:181-182` — "coredump storms" and "ongoing godot crashes".
- `corpus/knowledge/degraded-triage-r4.md:263` — "node cores show the V8 FatalOOM path".
- `corpus/knowledge/degraded-triage-r4.md:268` — "Class C — app crashes to route".

## 5. (c) Says both, or says "events" for the census number

- `SKILL.md:48` — same line: "60 941 err lines but only 238 entries" and "Entry classes: `systemd-coredump` 198", then "Coredumps this boot 198". (a) and (b) together.
- `SKILL.md:2753` R32-H2 — situation "counted m ≥ 1 systemd-coredump entries" and the handoff grammar `class=coredumps value=<m>`. Decision cell: "Each counted entry is a journal record of one coredump event" and "a core file can outlive its journal entry". Equates one identifier entry with one coredump event. Does not split stored core from no core. This is the operative contract row.
- `corpus/knowledge/systemd-user-plane.md:128` — "198 coredumps this boot (`jq 'length'` = 198; matches §5 coredump entry count)". Equates coredumpctl length with the journal class.
- `corpus/knowledge/systemd-user-plane.md:204-212` — user-journal "199 entries" beside "coredump census 199 (was 198)".
- `corpus/knowledge/journal-boot-plane.md:105-106` — "Journal err coredump entries = 207" and "one crash apart".
- `corpus/knowledge/journal-boot-plane.md:308` — "247 entries … coredump 207 → 211" and "named defect: crash storm".
- `corpus/knowledge/host-health-report-r3.md:49` — "Coredump storm (211 events, live)". 211 is `coredump=211` on `:30` and `:88`. "events" is neither "entries" nor "cores".
- `corpus/knowledge/host-health-report-r3.md:458-459` — "`coredump` +17 (class 211→228" next to a `coredumpctl` window of 232. Field name plus the other tool.
- `tools/tsukuroi-census.sh:263` — "non-kernel classes (coredumps, service messages)" beside the entry rule at `:242-245`.

Bare `coredump=<n>` snapshots, which name the field and do not say entries or crashes. (c). The integer is the identifier count from section 1:

- `SKILL.md:541` coredump=220; `:884` coredump=279; `:1214` coredump=522.
- `tools/tsukuroi-census.sh:268` coredump=211; `:1383` and `:2195` coredump=0; `:2200` coredump=1; `:2698` coredump=3.
- `corpus/knowledge/aur-drift-receipt-r9.md:57` coredump=467; `:188` "coredump 279→467".
- `corpus/knowledge/census-closeout-receipt-r10.md:59` coredump=523; `:140` "798 / 523"; `:143` "coredump 467 → 523".
- `corpus/knowledge/closeout-r11.md:54` coredump=752.
- `corpus/knowledge/degraded-triage-r4.md:45` coredump=244; `:51` "coredump 211→244"; `:55` "244 + 139 + 24 = 407" (the 244 is the class term, no unit word on `:55`).
- `corpus/knowledge/executor-test-sufficiency.md:91` and `:161` coredump=220; `:198` "coredump 211 → 220".
- `corpus/knowledge/host-health-report-r3.md:30`, `:88`, `:245` coredump=211; `:429` "coredump 211→228"; `:438` coredump=228.
- `corpus/knowledge/calibration-synthesis.md:32` and `:327-329` — "the coredump class reads 198 → … → 522". Says "class", not entries or crashes.
- `corpus/knowledge/closeout-r11.md:156-158` — "The coredump class is the standing proof" through 752.
- `SKILL.md:1448-1450` — "The coredump figure's day — 198 → 208 → 211 → 220 → 224 … 523".
- `SKILL.md:490` template `coredump=N`; `:496` "classes disjoint coredump > kernel > other"; `:1512` "`err`/`coredump` were quiet".
- `corpus/knowledge/closeout-r11.md:193` — "a `new=`/coredump jump".

Handoff grammar and scorer, unit not restated on the line (the predicate lines that say "entries" are in section 6):

- `tools/tsukuroi-census.sh:55-56` template `class=coredumps value=<m>`.
- `tools/tsukuroi-census.sh:1409-1410`, `:2780-2782` emit the field and the handoff from `JRN_COREDUMPS`.
- `tools/tsukuroi-census.sh:502`, `:1334` initialize `JRN_COREDUMPS=0`.
- `tools/tsukuroi-census.sh:2691`, `:2699` case name and expected handoff line `value=3`.
- `tools/score-census-handoff-r32.py:10`, `:90`, `:93`, `:427`, `:567`, `:596`, `:598`, `:600`, `:669`, `:680`, `:745`, `:759`, `:766-767`, `:783`, `:792`, `:892` — scenario name, field parse, or "journal plane coredump=%d, planted %d".
- `SKILL.md:2811` and `:2868` — registry scenario type `coredumps`.
- `corpus/knowledge/kill-oom-boundary-r33.md:14`, `:16`, `:17`, `:52` name the prepared class `coredumps` or "boot-0 systemd-coredumps" without a number. (c)
- `corpus/knowledge/kill-oom-boundary-r33.md:16` and `:17` also quote mori's "signal-11 coredump records". That is mori's class, not this count.

Not a restatement of the integer. (c), listed so the 211-hit sweep is closed:

- Tool name `coredumpctl`: `SKILL.md:153`, `:158`, `:204`; `tools/tsukuroi-census.sh:264`; `corpus/knowledge/calibration-synthesis.md:305`, `:338`; `degraded-triage-r4.md:255`, `:281`, `:520`, `:595`; `host-health-report-r3.md:50`, `:97`, `:252`, `:271`, `:459`, `:501`; `journal-boot-plane.md:4`, `:102`, `:302`, `:395`, `:439`; `systemd-user-plane.md:126`, `:144`, `:167`, `:168`, `:227`, `:246`, `:258`, `:268`.
- Section pointers: `SKILL.md:192` "coredump census :126-147"; `tools/tsukuroi-census.sh:361`; `boot-plane.md:252`; `journal-boot-plane.md:376`; `update-safety-v3.md:266`, `:291` "coredump-storm ownership".
- Disk, config, or directory, not the journal class: `degraded-triage-r4.md:70`, `:277-279`, `:605`, `:607`; `host-health-report-r3.md:267`; `closeout-r11.md:257`, `:280`; `degraded-triage-r4.md:98`, `:284` "prune cores" (files, after the 244-core rows); `host-health-report-r3.md:270` "crash owners have the cores"; `PROVINCE.md:51`, `:64` "raw cores" (handoff hygiene); `adjacency-anchors-r19.md:184` quotes that prohibition.
- Ownership, not a number: `PROVINCE.md:125` and `adjacency-anchors-r19.md:85` OUT-005 "signal-11 coredump records"; `host-health-report-r3.md:371` and `journal-boot-plane.md:359` "Coredump root cause"; `kill-oom-boundary-r33.md:19` mori quote only.
- Line-volume explanation, not the class integer: `driver-firmware-plane.md:172`, `:203`; `journal-boot-plane.md:85`, `:75`; `systemd-user-plane.md:107`, `:191`, `:194`.
- One-off events: `oom-event-plane.md:139`, `:208`; `kill-event-deep-r8.md:46`.
- `journal-boot-plane.md:92` heading "coredump cross-count"; `systemd-user-plane.md:156` dedupe rule.

`storage-health-r26.md:85` and `:125` say "host-visible crashes" about NVMe Unexpected Power Losses. That is not this count. Excluded. [obs]

## 6. (a) Says entries

The counted thing is named an entry, and the line does not also call that number cores or crashes:

- `PROVINCE.md:193` — "boot-0 systemd-coredump entries".
- `corpus/README.md:12` — "boot err entries" and "the `systemd-coredump` entry class".
- `tools/tsukuroi-census.sh:67` — "the boot-0 coredump entries whose SYSLOG_IDENTIFIER is `systemd-coredump`".
- `tools/tsukuroi-census.sh:242-245` — "ENTRY count" and "only `-o json` lines (= entries) are ever counted". `:243` names the class; `:245` names the unit. `:245` has no "coredump" substring, so it was not in the 211, but it is the unit rule for the class.
- `tools/tsukuroi-census.sh:266` — "the `systemd-coredump` entry class IS the storm signal".
- `tools/tsukuroi-census.sh:1380` — "boot error entries, counted at ENTRY level". Class order is `:1381`.
- `tools/tsukuroi-census.sh:1404` — the matcher. One identifier hit, one increment, `next`. No MESSAGE test.
- `tools/tsukuroi-census.sh:2665` — "a boot-0 coredump entry routes one coredumps line". The next line (`:2666`) is (b).
- `tools/score-census-handoff-r32.py:16`, `:76-77` — "value equal to the planted coredump entries".
- `tools/score-census-handoff-r32.py:53`, `:784`, `:793` — "no coredump entry".
- `tools/score-census-handoff-r32.py:81`, `:230`, `:379`, `:709`, `:779` — "coredump entries" / "systemd-coredump entries".
- `tools/score-census-handoff-r32.py:388` and `tools/tsukuroi-census.sh:2693-2695` — the planted row is one JSON object with that identifier.
- `corpus/knowledge/executor-test-sufficiency.md:155` — "entry count; classes disjoint coredump > kernel > other".
- `corpus/knowledge/host-health-report-r3.md:98` — "the `systemd-coredump` entry class is the storm signal".
- `corpus/knowledge/host-health-report-r3.md:246-247` — entry `wc -l`, then "same stream by identifier: `systemd-coredump` 208 → 211".
- `corpus/knowledge/journal-boot-plane.md:94-96` — column "entries", row `systemd-coredump` 207.
- `corpus/knowledge/systemd-user-plane.md:111-113` — column "entries", row `systemd-coredump` 198.
- `corpus/knowledge/systemd-user-plane.md:118` — "godot coredump entry".
- `corpus/knowledge/systemd-user-plane.md:151-152` — "198 entries, all `SYSLOG_IDENTIFIER=systemd-coredump`" and "the same 198 coredump entries".
- `corpus/knowledge/kill-oom-boundary-r33.md:27` — row title "coredump journal entries"; "boot-0 `-p err` entries with `SYSLOG_IDENTIFIER=systemd-coredump`"; "Neither is a victim count".
- `corpus/knowledge/kill-oom-boundary-r33.md:51` — "Coredump journal entries row".
- `SKILL.md:503-504` — "`err=` counts entries". No "coredump" on those lines; it is the unit for the journal line that carries `coredump=`.

## 7. What this does to a C2 "new ground" claim [inf]

QUALITY rule 68 (`corpus/QUALITY.md:136`): a declaration that calls ground new has to show this sweep; existing coverage makes the claim deeper ground or a supersession.

- New, relative to these files: no note splits "dumped core" from "terminated abnormally without generating a coredump", and nothing here records 183 versus 1348. The counter and the handoff scorer cannot see that split, because they key only on `SYSLOG_IDENTIFIER` and their fixtures use other MESSAGE text. [obs]
- Already covered, so not a new frontier: the census integer is an entry count of `systemd-coredump` journal records (`tsukuroi-census.sh:67`, `:1404`, `PROVINCE.md:193`, `kill-oom-boundary-r33.md:27`), and R32-H2 already says each such entry "is a journal record of one coredump event" (`SKILL.md:2753`). A note that many of those entries are the no-core message would deepen that row. It would not be the first statement of the counting unit.
- Already over-read, and those sentences are the ones a correction would have to reach: the (b) list in section 4, especially `journal-boot-plane.md:48`, `degraded-triage-r4.md:69`, `host-health-report-r3.md:49` and `:389`, `calibration-synthesis.md:141`, `README.md:13`, `SKILL.md:1627`, `closeout-r11.md:255`, and the census comments at `:1401` and `:2697`. [inf]

Scope: read=SKILL.md, PROVINCE.md, corpus/README.md, corpus/QUALITY.md:136, corpus/knowledge coredump and cores hits, tools/tsukuroi-census.sh journal arm and handoff, tools/score-census-handoff-r32.py plant path; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ScoutCoredumpReaders.md; executed=python hit enumerator and phrase extracts under timeout, no git write
Model: xai-oauth/grok-4.7-build-fast
Installs: none
