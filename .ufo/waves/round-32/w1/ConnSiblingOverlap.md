Verdict: no sibling emits, consumes or specifies tsukuroi's C1 HANDOFF line or C2 environment contract, so neither claim is CONFLICTS on ownership; but C1's planned values use selectors that differ from mori's own classes (a value-meaning CONFLICTS risk), and the frozen grammar's minimum leaves out tsukuroi's own ADJ-04 evidence fields, which the scorer lets the census add at no scoring cost.

Seat: TsukuroiR32.ConnSiblingOverlap (connector, read-only). Sibling HEADs read: mori a45850f05e4f, kumitate bde1086ea727 (moved from 32b7fd5 during the scan; cited lines re-read at bde1086), tameshi 09e4f273dd54, tabi e3cf4e0d30bb, kagi 899c50b42634, kama 1560e4d83f42, souji 4edb25dfe262, chousa 66bf1b930073, kaidoku d210fb8fa62d. Tsukuroi bytes: base 58cc2e0b, declaration fe1ae02c. Paths below are absolute unless prefixed `git show <rev>:`.

## Axes
Adjacency (C1, primary), operability (C2). The move proposed in finding 8 must improve adjacency without touching the frozen `routed` verdict.

## C1 — finding-to-owner HANDOFF, routing contract, kill-event/coredump evidence

1. [obs] **mori owns the evidence classes C1 routes, and accepts tsukuroi's overlap as adjacent rather than contested. Class: AGREES.**
   - /home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md:8-9: "kill/OOM-related catalog-ID records and signal-11 coredump records from independently labeled user/system journals, plus cgroup `memory.events`".
   - /home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md:66 (tsukuroi row): "this is adjacent host diagnosis, not contested fleet ownership."
   - /home/vgpnk/Projects/shokunin/mori-shokunin/PROVINCE.md:71 records the earlier prose packet TSUKUROI-F1-MEM-01 as received: "records the 2026-10-15T04:53:46Z capture as `prepared`; … acknowledgement/acceptance/resolution are unobserved."
   - The `state=prepared` vocabulary in the C1 line matches what mori already reads.
   - Must not absorb: fleet or wave attribution, OOM cause, and victim identity. These belong to mori's FR1 (PROVINCE.md:44, "a host record alone does not prove a fleet-caused kill").

2. [obs] **No sibling tool or document parses a tsukuroi `HANDOFF` line or reads the census's stdout as a routing input. Class: NONE (the consumer side is a LANE-GAP).**
   - Command: `git grep -E 'tsukuroi-census|\^HANDOFF|"HANDOFF|HANDOFF ADJ|kind=dated-event|state=prepared' HEAD` over all 20 siblings, excluding `.ufo` and JSON/JSONL. Exit 0.
   - The only census mentions are mori PROVINCE.md:287 (it reads the same `/proc/pressure/memory` file) and tameshi's mutation leg (finding 5).
   - A fleet-root `rg` for `^HANDOFF`, `'HANDOFF` or `"HANDOFF` outside the lanes printed nothing.
   - [inf] The C1 line is prepared output that nothing yet consumes. That fits ADJ-04's "prepared, not accepted" stance at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:77. C1 must not describe the line as a delivered handoff or as mori's intake.

3. [obs] **mori already emits the mirror-image route toward tsukuroi, in a different grammar. Class: AGREES on direction; LANE-GAP on grammar (no shared fleet routing-line grammar exists).**
   - /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh:1493 emits `FINDING UNIT_FAILURE_OUT_OF_SCOPE info "class=unit_failure_record count=$nonfleetn subject=nonfleet owner=tsukuroi …"`, with the note "a routing hint, not proof of non-fleet ownership".
   - The contract behind it is /home/vgpnk/Projects/shokunin/mori-shokunin/corpus/knowledge/journal-alarm-routing-r14.md:189 (§6 heading at :181).
   - souji uses a third `HANDOFF` grammar, tab-separated `HANDOFF\t<field>\t<value>` (/home/vgpnk/Projects/shokunin/souji-shokunin/tools/impl-37.sh:801-809).
   - Must not absorb: tsukuroi must not declare its `HANDOFF ADJ-04 …` grammar a fleet routing contract. Cross-lane protocol is not tsukuroi's to set. Dispatch and routing semantics belong to kumitate, per tsukuroi's ADJ-05 at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:50.
   - [inf] A future fleet aggregator matching `^HANDOFF` would pick up souji's TSV lines too. The `ADJ-04 mori` tokens separate them, so there is no collision today.

4. [obs] **The values C1 would route are derived differently from mori's classes. Class: CONFLICTS (risk on what the value means; ownership is not disputed).**
   - Coredumps:
     - The base census counts entries in `journalctl -b -p err -o json` whose raw JSON contains `"SYSLOG_IDENTIFIER":"systemd-coredump"`, with no `--user`/`--system` split (`git show 58cc2e0b:tools/tsukuroi-census.sh` :1342, :1360).
     - mori counts by structured MESSAGE_ID per scope and never sums the scopes. /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh:954-955: "coredump_notice MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1 notice" and "segfault_signal11 COREDUMP_SIGNAL=11 (RECORD subset of coredump records)".
   - Kill events:
     - The base oom plane matches MESSAGE text: `CLASS_OOM='Out of memory|oom-kill|oom_reaper'` and `CLASS_SIGKILL="status=9/KILL|Failed with result '(signal|oom-kill)'"` (`git show 58cc2e0b:tools/tsukuroi-census.sh` :428, :433).
     - mori forbids that selector for its own counts. /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh:940-941: "A journal class is counted by a stable STRUCTURED field, never by MESSAGE text".
   - [inf] `class=coredumps value=n` will not in general equal mori's `coredump_notice` or `segfault_signal11` counts for the same boot. This rule binds mori, not tsukuroi.
   - Must not absorb: tsukuroi must not present the value as a mori class count, a signal-11 count, or a per-scope record total, and must not adopt mori's catalog-ID classification.

5. [obs] **tameshi pins the tsukuroi census as a mutation-testing surface but reads only the selftest grammar, not the census's output lines. Class: NONE for C1.**
   - The pin is already stale. /home/vgpnk/Projects/shokunin/tameshi-shokunin/tools/mutate-and-run.sh:90: "bash-tsukuroi-census  tsukuroi-shokunin/tools/tsukuroi-census.sh  6/10 (60 %)".
   - /home/vgpnk/Projects/shokunin/tameshi-shokunin/SKILL.md:1046: "bash-tsukuroi-census     165307fe       aa136d69    stale".
   - What tameshi reads, at /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/mutation-case-tsukuroi-census.md:65: "The suite's grammar: per-case `PASS <label> (exit N, VERDICT)` / `FAIL <label>: exit X wanted".
   - Must not absorb: tameshi owns the mutation method (/home/vgpnk/Projects/shokunin/tameshi-shokunin/PROVINCE.md:7, "Owns: the method"). A changed census only makes tameshi's pin more stale. Re-pinning is tameshi's own action.

6. [obs] **Other siblings (kumitate, tabi, chousa, kotoba, kasegi, kama, kotodama, lore) have no HANDOFF line, packet or routing contract touching tsukuroi, ADJ-04, or kill/coredump evidence. Class: NONE.**
   - Their "handoff packet" and "routing contract" hits are lane-internal: kotodama→lore packets; kasegi role bindings at `.ufo/reports/round-21/kasegi.md:22`; kama handoff lines to kengaku/kumitate/kagi.
   - A per-sibling count of `ADJ-04|TSUKUROI-F1-|adjacency-handoffs-fleet` outside `.ufo` is non-zero only for mori (4).

## C2 — child-process environment contract for lane tools

7. [obs] **Several siblings build allow-listed or scrubbed child environments, but each scopes the contract to its own gates. None owns or specifies one for other lanes' tools, and none of the eleven C2 targets is invoked by a sibling. Class: AGREES (precedent), with no CONFLICTS.**

   C2 targets: the `TARGETS` tuple at `git show fe1ae02c:tools/probe-child-env-allowlist-r32.py` :64-77. Every target is under tsukuroi `tools/`. A sibling `git grep` for `tsukuroi-shokunin/tools/` other than the census finds no caller.

   | Sibling | Evidence (file:line) | Quote (≤25 words) | Scope | Must not absorb |
   |---|---|---|---|---|
   | kumitate | /home/vgpnk/Projects/shokunin/kumitate-shokunin/corpus/knowledge/pinned-evidence.md:99-101 (@bde1086) | "The gates pass an allowlisted child env (`PATH`, `HOME`, `LANG`, `LC_ALL`, `GIT_TERMINAL_PROMPT`, `GIT_OPTIONAL_LOCKS`)" | its own gates; `scripts/gate-mutants.mjs:14` "runs with an allowlisted environment" | kumitate's tooling domain (PROVINCE.md:3 "orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime") is OMP/ufo-fsd, not lane tools. Tsukuroi must not claim to set the env for OMP-spawned seats or run-receipt's harness. |
   | tabi | /home/vgpnk/Projects/shokunin/tabi-shokunin/scripts/check-round-contract.mjs:59 | "Constructed child environment: no inherited GIT_* variable can redirect the" | own gates | none to absorb. AGREES with C2's direction. |
   | tabi | /home/vgpnk/Projects/shokunin/tabi-shokunin/SKILL.md:1824-1825 | "require a trusted, scrubbed process environment: unset inherited `GIT_*`, `BASH_ENV`, `NODE_OPTIONS`" | own historical commands | a deny-list, the same shape as tsukuroi's round-31 one; see the next row. |
   | mori | /home/vgpnk/Projects/shokunin/mori-shokunin/tools/mori-census.sh:568,578 | "ONE scrubbed environment for every Git child" / "MORI_*, PATH, HOME and every other variable are untouched" | own census git children | none. mori deliberately keeps a deny-list; C2's allow-list is a different, compatible choice. |
   | kama | /home/vgpnk/Projects/shokunin/kama-shokunin/tools/kama-llamacpp-live.py:82-84 | "Child process environment allowlist: the server sees only these names when present in the harness env — names are recorded, values never are." | own server child | none. AGREES (the closest pattern to C2: names only, values never). |
   | kagi | /home/vgpnk/Projects/shokunin/kagi-shokunin/corpus/op-ref-probe.sh:259; PROVINCE.md:3 | `env -i PATH=/usr/bin:/bin HOME="$WORK/home"`; "secrets & vault ops — the-janitor flows, credential hygiene evidence" | own `op` probe | Credential values in the environment are kagi's. C2's probe and any allow-list doc must record variable NAMES only, never values, and must not classify a name as a secret. |
   | tameshi | /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/knowledge/hermetic-env-differential.md:2; PROVINCE.md:7,14 | "This is a finite experiment, not a universal hermeticity certificate."; "every lane's gate remains its own" | the method (environment-differential), not any lane's environment | The reusable hermetic-environment method is tameshi's. C2's probe is a lane gate. Tsukuroi must not claim the method as general; tameshi admits a pattern only from two lanes. |

   - [obs] kaidoku has a lane-internal allow-listed child env for its carrier runs (/home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md:537: "allowlisted child env with private `/tmp/kr17-rea-*` `TMPDIR`"). Class: NONE.
   - [inf] Allow-listed child environments now exist in kumitate, kama, kaidoku and tabi. That evidence meets tameshi's two-lane rule, so it could become a tameshi-owned general pattern. C2 should cite these as precedent, not claim the pattern as tsukuroi's.

## 8. Proposed move (one, bounded) — C1 handoff evidence fields via the scorer's trailing-field allowance

- **Evidence.**
  - Tsukuroi's own ADJ-04 row names the minimum evidence a handoff must carry. /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/PROVINCE.md:49: "Capture time, boot/window, exact counter or PSI command/exit and observed value; distinguish presence, cumulative count and dated event".
  - The frozen grammar carries only class, value, kind and state.
  - The frozen scorer explicitly tolerates more fields. `git show fe1ae02c:tools/score-census-handoff-r32.py` :37-39: "trailing `key=value` fields after `state=prepared` are accepted (the census may add a capture time or window) and never compared". HANDOFF_RE at :97-98 ends with `(?:\s+(.*))?$`.
- **Move.** The C1 implementer appends, after `state=prepared`, fields that already exist in the census's own state:
  - `window=` (the oom plane's `boots=… first..last`; base :1281-1283).
  - `selector=` (`journal-err-syslog-id` for coredumps; `oom-plane-C1..C3-message-text` for kill events).
  - `scope=merged` (the census does not split user and system scopes).
  - Optionally `captured=<UTC>`.
- **Axes.** Adjacency improves: the line then satisfies tsukuroi's own ADJ-04 minimum evidence, and it states the selector difference in finding 4 instead of hiding it. This answers mori's no-substitution concern without adopting mori's classes. Operability and C2 are untouched. `routed` is not harmed, because the trailing fields are never compared. PLANE lines, the TSUKUROI_CENSUS line and the exit code are unchanged by construction.
- **Risks.**
  - (a) A `captured=` timestamp makes census stdout non-reproducible across runs. Any repeat-equality check over full stdout, such as a future tameshi env-diff profile, would read it as raw-output-variable. Dropping `captured=` and keeping `window=` avoids this.
  - (b) A trailing field must be `key=value` with no spaces, or the line still matches HANDOFF_RE but a later reader may mis-split it.
  - (c) Rule 79-81 in QUALITY.md, and whether doc lines in PROVINCE/SKILL count as a surface beyond the declared separability, were not checked [unk].
- **Verification.**
  - `python3 tools/score-census-handoff-r32.py --revision <REV>` should still give `routed` 24 of 24 with `harness_errors` 0.
  - `bash tools/tsukuroi-census.sh | grep '^HANDOFF ADJ-04 mori' | grep -c 'window='` should equal the HANDOFF line count.
  - A diff of PLANE and TSUKUROI_CENSUS lines against base 58cc2e0b on one fixture should be empty.

## Unknowns
- [unk] Whether mori will ever read HANDOFF lines: no intake exists (finding 2). Acknowledgement stays unobserved.
- [unk] Whether kumitate or the protocol integrator wants a single fleet routing-line grammar. No document asks for one.

Scope: read=round-32 declaration at fe1ae02c (SCORECARD.md), tsukuroi PROVINCE.md ADJ/OUT rows, base census 58cc2e0b (oom and journal planes), frozen C1 scorer and C2 probe TARGETS at fe1ae02c; PROVINCE/SKILL/tools/corpus of mori, kumitate, tameshi, tabi, kagi, kama, souji, kaidoku, plus git-grep sweeps over all 20 sibling repos at HEAD; fleet-root rg for HANDOFF parsers; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w1/ConnSiblingOverlap.md (and the empty directory /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-32/w1/ConnSiblingOverlap/); executed=read-only `git show`, `git grep HEAD`, `git rev-parse`, `git log -1`, `rg`, `sed` (all exit 0); no git or jj writes, no sandbox clone, no counter run
Model: not exposed
Installs: none
