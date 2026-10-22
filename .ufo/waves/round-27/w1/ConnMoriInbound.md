# ConnMoriInbound — replay of mori pointers into tsukuroi (round 27, wave 1)

Verdict: done. Every mori pointer into this lane was replayed at mori `ef9dbee1` and at mori HEAD `0becc421`. At the lane tip `db9eecfa` almost all of them resolve. Five drifted: four into lane `PROVINCE.md` and one into `tools/check-seat-scope.py`. None are unresolvable once false positives are removed. The `userspace-oom-killers-r26` entry gives nine candidate OV rows for C2, covering all five classes. Two of them are real CONFLICTS.

Axes touched: adjacency (C2 register content). Depth/C1 not touched.

## Method

1. [obs] Grep, as assigned: `git -C /home/vgpnk/Projects/shokunin/mori-shokunin grep -n -E 'tsukuroi' ef9dbee136d6ed2ef98687f5cb0c0a16506a5155 -- .` exit 0, 6479 lines; the same at `HEAD` (= `0becc4216f97e61f41a472bb6c66d2d781b9d9bb`) exit 0, 6568 lines. Raw output: `/fast/scratch/hyaku/tsuku27/ConnMoriInbound/grep-ef9.txt`, `grep-head.txt`.
2. [obs] A pointer is a grep line that names a lane path, line or commit. Accepted forms: `tsukuroi-shokunin/<path>[:lines]`, `../tsukuroi-shokunin/…`, `tsukuroi-shokunin@<commit>:<path>`, the raw GitHub URL form `tsukuroi-shokunin/<commit>/<path>`, a bare backticked file name on a tsukuroi line that exists only in the lane (not in mori, not under `.ufo/`), and a hex commit next to the word tsukuroi that exists in the lane. Forms like `tsukuroi/operator`, `tsukuroi/kama` and `tsukuroi/sessions` mean "or" or a mori-local directory, and are dropped (they matched no lane top-level name). Tool: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/ConnMoriInbound/resolve.py` (read-only git only).
3. [obs] Reference commit. When the pointer names a commit (for example `157ee255`), it is resolved at that commit. Otherwise it is resolved at the lane commit that was current when mori wrote that line: `git blame --porcelain -L n,n` committer time, then `git rev-list -1 --before=<t> db9eecfa`. The named lines at the reference commit are then compared with the tip:
   - same text at the same lines is RESOLVES;
   - the same text at other lines is DRIFTED, with the new line;
   - text gone, path gone, or range beyond the file length is UNRESOLVABLE.
   Path-only pointers resolve when the path exists.
4. [inf] The era rule approximates "the lane as mori saw it". A pointer that was already stale when written (see finding 4) is caught only by the semantic checks below, not by the mechanical comparison.
5. [unk] Bare `PROVINCE.md`, `SKILL.md` and `SCORECARD.md` mentions are excluded automatically, because both repos have those names. The one in the C2 entry (snapshot line 154) is resolved by hand in finding 9.

## Counts

| mori revision | grep lines | pointer occurrences (explicit / bare / commit) | distinct pointers | RESOLVES | DRIFTED | UNRESOLVABLE |
|---|---|---|---|---|---|---|
| `ef9dbee1` | 6479 | 178 (146 / 29 / 3) | 104 | 173 occ. / 100 distinct | 5 occ. / 4 distinct | 0 |
| HEAD `0becc421` | 6568 | 234 (159 / 70 / 5) | 142 | 229 occ. / 138 distinct | 5 occ. / 4 distinct | 0 |

[obs] The machine verdict was UNRESOLVABLE for `check-seat-scope.py:12-15`. It is counted here as DRIFTED after the hand check in finding 3. In mori's admitted files (outside `.ufo/`) there are 24 occurrences at `ef9dbee1` (20 RESOLVES, 4 DRIFTED) and 26 at HEAD. At HEAD, 56 pointer occurrences are new and none were removed. All 56 resolve at the tip; they come from mori's round-27 wave reports and the new mori entry `corpus/knowledge/oom-victim-selection-r27.md:185`. Full per-occurrence tables (verdict, kind, lane path, lines, named commit, reference commit, detail, mori path:line, token):
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/ConnMoriInbound/pointers-ef9dbee.tsv` (sha256 `466a42d4…6cf9`)
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/ConnMoriInbound/pointers-mori-head-0becc42.tsv` (sha256 `6df03e32…1a85`)

## Findings — every pointer in mori's admitted files (`ef9dbee1`; identical at HEAD unless noted)

1. [obs] `mori:PROVINCE.md:66` "`../tsukuroi-shokunin/PROVINCE.md:21-24,35-44`". Reference commit `343fa0db`: line 21 is "Host memory and kill-event measurements support OS triage" and lines 35-44 are the ADJ table. **DRIFTED.** At the tip they are lines 30-33 and 44-53 (`git -C …/tsukuroi-shokunin show db9eecfa:PROVINCE.md`, lines 30 and 44 print the same text).
2. [obs] `mori:SKILL.md:345` "(`tsukuroi-shokunin/PROVINCE.md:19` "never restarts". **DRIFTED** to tip `PROVINCE.md:28`, "never restarts services. Detection and report; the operator remediates." The quote matches.
3. [obs] `mori:.ufo/waves/round-17/build/SiblingSeatDeathTools.md:91` "`tsukuroi-shokunin/tools/check-seat-scope.py:12-15` audits the `Scope: executed=` trailer". At `f7fb9789`, lines 12-15 held the `^Scope: executed=(.+)$` finding list. At the tip, lines 12-15 list `SCOPE-TRAILER-MALFORMED`, the trailer statement is at line 5, and the regex is at line 44. **DRIFTED** (lines 5 and 44).
4. [obs] `mori:corpus/lessons/round-12.md:28` and `:73` "`tsukuroi/PROVINCE.md:16-17`". The lesson itself records the quote as moved to `:19`. Both `:16-17` and the lesson's `:19` are now at tip `PROVINCE.md:25-28`. **DRIFTED.** [inf] This was already stale when written, so mori's own lesson flags it.
5. [obs] `mori:PROVINCE.md:66` "`oom-event-plane.md:231-257,279-281,301,344-367`" and "`kill-event-deep-r8.md:30-37,97,120-135`". **RESOLVES** at the same lines at `343fa0db` and at the tip. The same holds for `PROVINCE.md:71` (`adjacency-handoffs-fleet-r1.md:74-112`), `:73` (`:94-104`), `:287` (`tools/tsukuroi-census.sh:376,1100-1115`) and `:288` (`PROVINCE.md:30-33`, reference `22fd1642`).
6. [obs] The r12 knowledge entries all **RESOLVE** at the same lines:
   - `kernel-oom-line-attribution-r12.md:8` (`oom-event-plane.md:23–42,359–367`);
   - `kill-classes-by-message-id-r12.md:8` (`kill-event-deep-r8.md:97,120–135`; `oom-event-plane.md:39–41`);
   - `oom-kill-counter-kernel-only-r12.md:8` (`oom-event-plane.md:245–257,359–367`; `kill-event-deep-r8.md:120–135`);
   - `userspace-oom-killers-r12.md:8` (`oom-event-plane.md:344–346,353–367`).
   The last one names lane line 344, which the lane itself has since contradicted for current use: tip `oom-event-plane.md:473` says "Line 344 is contradicted on two points by `corpus/knowledge/memory-pressure-r25.md`". So it resolves as text but is superseded in the lane.
7. [obs] `memory-pressure-r25.md` at named commit `157ee255`. This is cited in mori's `PROVINCE.md:371`, `corpus/SOURCES.md:131` (S125), `corpus/lessons/round-26.md:78` and `userspace-oom-killers-r26.md:1,256`. It **RESOLVES**: `git -C …/tsukuroi-shokunin rev-parse 157ee255:corpus/knowledge/memory-pressure-r25.md` gives `be3065ae512f3fefec115a23c0e8fee2cbca9fc4`, which equals the blob named in mori S125. 157ee255 is an ancestor of the tip, and from it to the tip the file only gained 8 lines appended after line 392 (`git diff 157ee255 db9eecfa -- corpus/knowledge/memory-pressure-r25.md`: 1 file, 8 insertions). Every line mori names therefore sits at the same number at both commits. The round-26 lesson quote `:204 "On this host systemd-oomd is inactive and disabled"` matches line 204 at both.
8. [obs] Commit pointers: `a61db549` (`mori:.ufo/waves/round-23/build/CriticScopeProvince.md:160`), `e9f5356c` (`round-26/w1/ConnSiblingOverlap.md:4,27`) and, at HEAD, `157ee255` (`round-27/w1/ConnSiblingOverlap.md:8,106`). Each exists in the lane and is an ancestor of the tip. **RESOLVES.**
9. [obs] Snapshot line 154 points at "`PROVINCE.md` adjacency row" with no repository. [inf] Mori writes bare paths for its own files (snapshot line 250 "the FR10 row in `PROVINCE.md`" is mori's). So this means `mori:PROVINCE.md:66`, the tsukuroi row, whose lane pointer `PROVINCE.md:21-24` drifted to 30-33 (finding 1). Read the other way, as lane `PROVINCE.md`, the adjacency row is ADJ-04 at tip line 49, which also exists. Classification: **INBOUND-DRIFTED (transitive).**
10. [obs] Contradiction with the lane's own round-19 inbound register (`corpus/knowledge/adjacency-anchors-r19.md`):
    - IN-066 calls `check-seat-scope.py:12-15` RESOLVES at line 13. I call it DRIFTED, because the named statement now sits at lines 5 and 44 while line 13 holds a newer, different finding.
    - IN-067 gives `PROVINCE.md:66 → 21-24,35-44` a drift target of 8. I find 30-33 and 44-53.
    Both are stated, not reconciled. [inf] The r19 register's "match line" appears to be a topical nearest match rather than identity of the named text.
11. [obs] Source-ID collision trap for C2 writers. Mori `S125` is the lane entry `memory-pressure-r25.md@157ee255` (`mori:corpus/SOURCES.md:131`). Lane `S125` is a different row, mori's `system-pressure-r24.md@4f05dd5a`, superseded by lane `S127` (`tsukuroi:corpus/SOURCES.md:131,133`; tip `memory-pressure-r25.md:392` "S127 supersedes S125"). Any OV row must qualify these IDs by lane.
12. [obs] Mori HEAD edits the C2 entry. `git cat-file -p ef9dbee1:corpus/knowledge/userspace-oom-killers-r26.md | sha256sum` gives `a5368ee7…b0a29d`, which equals the committed snapshot. At HEAD it gives `94efb7cf…ee93d` (commit `79ecf58`, "Round-27 corrections" O2, O10, O14, O17 plus an S117 correction). [inf] The C2 checker pins `ef9dbee1`, so this does not break counting. Rows that quote changed lines (145-147 and 196 at `ef9dbee1`) should say mori has since reworded them.

## Candidate OV rows for C2 (userspace-oom-killers-r26 and memory-pressure-r25)

Each sibling quote was machine-checked against the C2 row rule with `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/ConnMoriInbound/verify_ov.py`. The checks:
- at most 25 words;
- normalised substring of snapshot lines `quote_line` to `quote_line + 2`;
- `heading` is the nearest `#` line at or above;
- the lane quote is at most 25 words and is a normalised substring of the lane file at `db9eecfa`.

All nine passed (the run printed `sib_ok=True` for each, and `lane_ok=True` for the eight that have a lane side).

| cand | snapshot `quote_line` / heading | sibling quote | lane side (tip line) | class | owner | why / action |
|---|---|---|---|---|---|---|
| OVc1 | 143 / `## Facts` | "every unit the sibling lane captured — `user@1000.service`, `user-1000.slice`, `user.slice` and `-.slice` —" | `corpus/knowledge/memory-pressure-r25.md` 204-206: "every one of the four captured units — `user@1000.service`, `user-1000.slice`, `user.slice` and `-.slice` — carries `auto` on both properties" | INBOUND-RESOLVES | tsukuroi | Same four units at 157ee255 and at the tip. Record only. |
| OVc2 | 145 / `## Facts` | "so nothing in that chain would be monitored even if the service were started" | `memory-pressure-r25.md` 390: "\"monitors nothing while every unit stays auto\" holds only while no such report arrives." | CONFLICTS | tsukuroi | The qualifier (socket mode 0666; plus `OOMRules=` at line 387) is already present at the commit mori cites (157ee255 has 392 lines). Mori copied the unqualified headline. The lane's own `SKILL.md:2316` MP4 row and `memory-pressure-r25.json` MP4 still carry it unqualified. Report to mori; fixing the lane's SKILL and JSON rows is lane debt outside C2. |
| OVc3 | 146 / `## Facts` | "`auto` is the upstream default and means the cgroup's data is not actively used for monitoring and detection." | `memory-pressure-r25.md` 201-202: "`auto` is the default and means systemd-oomd will not actively use that cgroup's data for monitoring and detection;" | AGREES | tsukuroi | At `ef9dbee1` mori omits the ancestor-kill clause (lane 202-203). Mori HEAD adds it (O2), matching the lane. |
| OVc4 | 153 / `## Facts` | "OS and unit diagnosis is tsukuroi's ground (`PROVINCE.md` adjacency row)" | `PROVINCE.md` 32: "The existing census reports those signals; fleet correlation belongs to mori" | INBOUND-DRIFTED | mori | Transitive through `mori:PROVINCE.md:66`. Lane 21-24 at 343fa0db is now 30-33 (findings 1 and 9). Mori should re-pin. |
| OVc5 | 256 / `## Adjacency` | "`tsukuroi-shokunin/corpus/knowledge/memory-pressure-r25.md` at commit `157ee255` — this host's" | `memory-pressure-r25.md` 209: "**Verdict.** `scoped` — the four captured units and their ancestor chain are `auto` and systemd-oomd is inactive;" | INBOUND-RESOLVES | tsukuroi | The MP4 `scoped` verdict that mori cites (snapshot 258-259) is at 209 at both commits. |
| OVc6 | 128 / `## Facts` | "The delegation exception that the previous entry named does not exist in earlyoom 1.9.0" | `memory-pressure-r25.md` 382: "A userspace killer moves neither kernel counter unless it asks the kernel to kill: earlyoom with `--kernel-oom` does" | CONFLICTS | mori | Lane 382 attributes the exception to mori's `oom-kill-counter-kernel-only-r12.md`. That entry still says "`earlyoom --kernel-oom` delegates to the kernel" (mori lines 21 and 30 at `ef9dbee1` and HEAD), based on README master. Mori r26 F7 says the option was removed in v1.2 and is absent from the installed 1.9.0. The lane appends a current-use notice citing r26 F7; mori is told that its r12 counter entry contradicts its r26 entry. |
| OVc7 | 125 / `## Facts` | "path, which is the only place the kernel increments `count_vm_event(OOM_KILL)` and" | `memory-pressure-r25.md` 326: "an earlyoom kill would not move the kernel counters." | AGREES | mori | Mori r26 snapshot line 260 says `oom-kill-counter-kernel-only-r12.md` owns the kernel-counter semantics. Alternate row. |
| OVc8 | 28 / `## Facts` | "**F1 — the host state, and the one that changed.** `earlyoom.service` is **active** and" | `corpus/knowledge/kill-event-deep-r8.md` 354: "earlyoom is installed (local database `earlyoom-1.9.0-1`), its unit is active and enabled" | AGREES | tsukuroi | Unit and package state is tsukuroi's (`mori:PROVINCE.md:369-371`). Alternate row. |
| OVc9 | 196 / `## Decision table` | "the `user.oomd_ooms` / `user.oomd_kill` cgroup attributes \| systemd-oomd's own accounting of its kill attempts and killed pids" | `null`: no lane file holds `oomd_ooms` or `oomd_kill` (`git grep -n -E 'oomd_ooms\|oomd_kill' db9eecfa -- corpus/knowledge PROVINCE.md SKILL.md` gave no output) | LANE-GAP | mori | Mori HEAD reworded this row (D4/O10: counts, "no pid is stored"). The row must say that the `ef9dbee1` wording is superseded at mori HEAD. |

[inf] A six-row set covering all five classes: OVc1, OVc4, OVc3, OVc2, OVc6 and OVc9. Alternates: OVc5, OVc7 and OVc8.

[obs] HEAD-only, not eligible because it is not in the snapshot. Mori `SOURCES.md` S133 (`0becc421`) teaches "On systemd 262 systemd-oomd monitors only cgroups of units set to `kill`; a unit left at the default `auto` is never monitored itself". The lane withdrew exactly that "monitors only" wording at 157ee255:387 (`OOMRules=` units are also monitored). S133 does not mention `OOMRules` (`grep -c OOMRules` → 0). This is a mori-owned drift for a later packet, not a C2 row.

## Second-order risks

- [inf] **Separability.** C1 is declared a "new PROVINCE frontier area", and C2 reads `PROVINCE.md` (its section, and OVc4's lane quote). If the C1 integration writes a PROVINCE frontier paragraph, C1 changes a file C2 reads. That contradicts the declaration's "C1 changes no file that C2 reads". Choosing OVc5 instead of OVc4 removes the C2 lane-side read of `PROVINCE.md`, but not the section read.
- [inf] **OVc2 action scope.** Correcting the lane's `SKILL.md:2316` MP4 row would touch `SKILL.md`, which C1 reads (its `## Kernel taint — round 27` section). Keep it out of round 27, or make it a separate unclaimed note.
- [inf] **OVc9 window.** The quote contains a table-cell `|`. It passes the normalised-substring rule, but the JSON writer must keep it literal.
- [unk] Whether `tools/check-adjacency-overlap.py` exists yet at the lane tip, and how it treats `null` lane sides, was not read. It is not in the tip tool list I saw: `ls …/tools | grep -i -E 'adjac|anchor'` returned only `check-adjacency-anchors.py`.

## Verification the L1 can rerun

- `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/ConnMoriInbound/resolve.py ef9dbee136d6ed2ef98687f5cb0c0a16506a5155 /tmp/x /fast/scratch/hyaku/tsuku27/ConnMoriInbound/grep-ef9.txt` should print `occurrences 178`. Use `HEAD … grep-head.txt` for 234.
- `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/ConnMoriInbound/verify_ov.py` should print `sib_ok=True` for OVc1 to OVc9.
- `git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -p ef9dbee136d6ed2ef98687f5cb0c0a16506a5155:corpus/knowledge/userspace-oom-killers-r26.md | sha256sum` should give `a5368ee7121d2cbe0929dcb65a13144e5d925f942721b8e6557cf6c612b0a29d`.

Scope: read=mori-shokunin git objects at ef9dbee1 and HEAD 0becc421 (grep, blame, show, diff, log), tsukuroi-shokunin git objects at 157ee255, 343fa0db, f7fb9789, 3beab8dd and db9eecfa, SCORECARD round-27 declaration, round-27 mori snapshot; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/ConnMoriInbound.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-27/w1/ConnMoriInbound/{pointers-ef9dbee.tsv,pointers-mori-head-0becc42.tsv,resolve.py,verify_ov.py}, /fast/scratch/hyaku/tsuku27/ConnMoriInbound/*; executed=git grep/blame/show/diff/log/rev-parse/rev-list/merge-base/cat-file/ls-tree (read-only) on both repos, sha256sum, python3 resolve.py and verify_ov.py (read-only analysis)
Model: not exposed
Installs: none
