# Mutation probe — C1 input pinning (wave 2, seat MutC1Pins)

Verdict: **survives**. The attacked behavior — C1's pinned-input gate on
`.ufo/waves/round-23/falsify/events.json` — detected a one-byte mutation of that
input (exit 1, `pin_mismatches`), and restored to exit 0 with exact bytes. The
claim is not falsified; the kill demonstrates the pinning behavior is real.

Probe: one byte of `.ufo/waves/round-23/falsify/events.json` at the landed
commit `22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0` (tool string `"read"` →
`"rad"` in the first seat event; JSON stays valid). Mutated, committed, detected,
restored byte-exact, committed, re-detected. All in my private clone
`/fast/scratch/hyaku/tsuku24w2-MutC1Pins/lane` (origin remote removed so
`_revision.bind` resolves against the clone's local master only; no lane writes,
no git writes in the fleet repo).

1. Pristine baseline at `22fd1642` in the clone: `python3 tools/report-red-causes.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0` → exit 0, `pin_mismatches: []`, `preserved: true`, `attributed_findings: 268`, `attributed_with_recorded_operation: 267`, `attributed_seat_level: 1`, `checker_exit: 2`, `incomplete_seat_is_frozen: true`, `split_matches: true`. [obs] Output: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/MutC1Pins/baseline-22fd1642.json` (exit captured by runner).

2. Mutant commit `f17f160f88e519732ddbd297cc6e8d14c17f9f8a` (one byte of events.json changed, committed on clone master; worktree clean): `python3 tools/report-red-causes.py --revision f17f160f88e519732ddbd297cc6e8d14c17f9f8a` → **exit 1**, `pin_mismatches: ['.ufo/waves/round-23/falsify/events.json']`, `preserved: false`. [obs] Output: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/MutC1Pins/mutant-f17f160f.json`. The tool's pinned digest for EVENTS is `52a5021b…`; the mutant events blob hashes to `f95a47c9827ae59377efaf398db36612bbcea24e1b1a93c098bbe27b4242f1da`. [obs]

3. Restore: events.json replaced byte-exact from the `22fd1642` blob (`git show 22fd1642…:…events.json`), committed as `d793d7b6469e9e404628279237e871a2db52b150`. sha256 `52a5021bb18647ca868d0814d933dd899f29cdb0a44d2cc78605ee2e38b62b83` equals both the pristine hash and the tool's PINS value; blob id `5ab7db46f607ae225c7db27779f71af3c590848f` matches the pristine blob id. [obs] `python3 tools/report-red-causes.py --revision d793d7b6469e9e404628279237e871a2db52b150` → **exit 0**, `pin_mismatches: []`, `preserved: true`, findings identical to baseline (268/267/1). [obs] Output: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/MutC1Pins/restored-d793d7b.json`.

4. Adjacent observation, not a falsification: the one-byte tool-string rename also shifted the frozen checker's outcome (`total_findings` 268 → 269, `split_matches` false), so the same mutation was detected by the pin gate before any semantic check mattered. `attributed_findings` 269 at the mutant shows the checker's evaluation depends on tool-name values; the C1 claim's 268/267/1 numbers are restored only with the exact pinned bytes. [inf]

The invariant that a changed pinned input is refused (exit 1, `pin_mismatches`) survives at the mutated and restored revisions. Smallest correction: none — the tool behaved as claimed; no contract change is proposed.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md, tools/report-red-causes.py, tools/_revision.py, .ufo/waves/round-24/measure/c1-22fd1642.json, .ufo/waves/round-23/falsify/events.json; clone work at /fast/scratch/hyaku/tsuku24w2-MutC1Pins/lane (commits f17f160f, d793d7b on local master); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/MutC1Pins.md and .ufo/waves/round-24/w2/MutC1Pins/{baseline-22fd1642.json, mutant-f17f160f.json, restored-d793d7b.json, pristine-events-sha256.txt, pristine-events-blob.txt, mutant-events-blob.txt, mutant-commit.txt, restored-commit.txt, restored-events-sha256.txt}; executed=git clone/checkout/remote remove/add/commit (clone only), sha256sum, python3 tools/report-red-causes.py at three revisions.

Installs: none
