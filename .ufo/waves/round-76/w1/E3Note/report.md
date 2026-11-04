# E3Note — round 76 C1 source note

## Behavior and touched surfaces

Wrote `corpus/knowledge/journald-retention-plane-r76.md` with exactly eight JD rows, four sources/snapshots, provenance trio, per-row source anchors, host-derived limits and explicit limitations. Seat artifacts: `binding.md`, `counter.txt`, this `report.md`, and sibling report `.ufo/waves/round-76/w1/E3Note.md`.

Axes: depth/C1 retention mechanisms, factual accuracy and auditable provenance. No C2 verdict, score increase or committed-byte acceptance is claimed.

## Gates and exact commands

All commands below ran with the named absolute cwd; no command was rerun to decorate this report.

1. Cwd `/home/vgpnk/Projects/shokunin`: `mkdir -p /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/w1/E3Note && mkdir -p /fast/scratch/hyaku/tsukuroi-r76/E3Note` — rc 0. Initial binding was written before source-context deep work.
2. Cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/before/src`: `sha256sum -c /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-76/before/src/SHA256SUMS` — rc 0, all four files OK.
3. Cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`: `TMPDIR=/fast/scratch/hyaku/tsukuroi-r76/E3Note python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/count-jd-rows-r76.py` — first assigned attempt rc 1: `JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=1 met=0`, line 17 shared-token share 0.43. Revised JD7 to name actual fields and constants while preserving its corrected mechanism. Same command then rc 0: `JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1`. Final stdout saved verbatim in `counter.txt`.
4. Read `tools/check-knowledge-header.py:1-160` and its `add_argument` declarations at lines 261-268. It accepts `--revision`/`--selftest`, `--lane`, `--branch`, but no note-path argument. Therefore the requested conditional path-specific execution was not applicable; no header-gate pass is claimed.
5. Cwd lane root: `rmdir /fast/scratch/hyaku/tsukuroi-r76/E3Note` — rc 0; scratch removed. No fixtures or receipt copies were needed; source receipts remained read-only.

## Source review and tightened rows

Every quote was checked by reading surrounding pinned text, rather than relying on the draft or counter: `journald.conf.xml:70-105,240-325`; `journald-manager.c:115-195,790-825`; `journald-config.c:15-32,39-60,100-145`; `journalctl.xml:935-995`. `SOURCES.json`, `SHA256SUMS`, frozen `host.txt` and working-tree registry rows S318–S321 were read.

- JD1 retained; prose supplies volatile/persistent/none semantics, early-boot fallback and flush caveat.
- JD2 expanded to state the smaller permitted journal allowance from two constraints, without confusing it with the arithmetic in JD3.
- JD3 corrected the draft's arithmetic. Conflict verbatim: draft says “used space plus the smaller of free space and keep_free”; pinned source says `avail = LESS_BY(vfs_avail, metrics->keep_free);` then `space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);`. Note uses saturated subtraction, not `min(free, keep_free)`. The frozen declaration/registry wording was not edited: this remains a conflict for the canonical judge, not something a passing token-overlap counter resolves.
- JD4 tightened to “at least” current disk usage because the assignment is MAX, and scoped startup/first-opening. Prose explicitly avoids claiming that other retention limits can never remove archives.
- JD5/JD6 retained after context review; prose distinguishes usual seven-file history from guarantees and active-file count exceptions.
- JD7 corrected the draft's attribution of all four defaults to `journal_config_set_defaults`: that function assigns the rate pair; `manager_merge_configs` provides sync and max-file-time defaults. Final statement names actual fields/constants to satisfy the frozen overlap predicate without changing meaning.
- JD8 retained; prose covers time/files/zero/combined rotate behavior and active-file exclusion.

## Provenance and known limits

Snapshot source URLs/digests come from the frozen v262 source map and S318–S321; the host numbers come only from `.ufo/waves/round-76/before/host.txt`. The derived `effective_limit=256M` is a configuration calculation with abundant recorded filesystem free space; `SystemMaxFileSize=32M` is the default one-eighth derivation, not live manager introspection. Observed usage is `148.6M`. The note does not claim upstream lines equal Arch build lines, that 13 inventoried files prove a rotation schedule, or that apparent byte totals equal allocated-block disk usage.

Peer E4InstrumentCheck reported an earlier admitted pre-correction snapshot with digest `ef3617004cbf63b05191870602f58ba9b083b5e8d895e9e1f4099c632bc34314`; that is peer-reported historical evidence, not an independently reproduced result here. S2Skill was given the corrected anchors; E4InstrumentCheck was told to retain the semantic discrepancy. No independent reviewer approval is asserted.

Out of scope: registry, lesson, SKILL.md, SCORECARD.md, counter/header implementation, C2 closure, commits, pushes, actual vacuum/rotation/restart/flush, new live host observations. No tools installed or updated.

## Self-evaluation

Accuracy 4/5: direct source contexts and digest receipt support the note; runtime/Arch identity intentionally remains unverified. Completeness 5/5: eight rows, host block, required sections, final rc-0 receipt and reports supplied; conditional header run correctly inapplicable. Clarity 4/5: row table is necessarily wide under the frozen grammar. Actionability 5/5: recheck command, cadence and source anchors are explicit. Conciseness 4/5: audit report necessarily repeats command outcomes. Mean 4.4/5. Highest-impact remaining evaluation is independent semantic/revision review by the main agent, not another cosmetic local replay. The limits are explicit enough for the user to distinguish completed work from unobserved acceptance.
