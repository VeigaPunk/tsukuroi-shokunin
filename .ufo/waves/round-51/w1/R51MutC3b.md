VERDICT: defect-found

Seat R51MutC3b, item C3-A5 (second mutant set on the round-51 C3 counter). Frozen revision 2732ee6c06108c031c4d8043239b994e0504eb2f; the counter `tools/check-adjacency-table-r51.py` is sha256 3d09a8e94a9075f6de12c03fe1f678d77a3af1f23e18ed887c58a700b44cf380 (matches FROZEN-hashes.txt). The battery is `controls/battery.py` (sha256 12eeffb51e9af7fc..., matches FROZEN-hashes.txt).

## Result

The frozen C3 battery (`c3_battery`, battery.py:211-238: K0, K1, K2, K3, K4, K5, K-pass) does not distinguish any of M5-M8. Every mutant returns the same 7 as-expected rows as the original, so none is killed. Four proposed controls (K6-K9) kill them; the unmutated counter passes all 11 rows.

## Why the battery is blind to these legs (evidence)

1. A forced leg equals the real value on the pinned inputs. Direct run of the unmutated frozen counter, `--revision 2732ee6c… --no-base-check`, returned:
   `verdict PASS; display_bound_ok 10; quote_specific_ok 10; digests_bound_ok 10; display_forge_fails 1; override_blocked 1; r50_blind 1; anchors_ok 7; registry_ok 7; quote_at_pin_ok 9`.
   So M5 (`override_blocked = 1`, counter lines 256-263), M6 (`r50_blind = 1`, line 273), M8 (`display_forge_fails = 1`, line 244) and M7 (heading-section test, lines 133-135, passes on all 10 real quotes) are behaviour-identical on every real-input row. A forced leg SURVIVES unless a control drives that leg's real value to 0.
2. Control-mode short-circuit: line 284 reads `((override_blocked == 1 and r50_blind == 1) or a.control)`. In `--control` mode the two guard legs are never checked, so K0, K2-K5 and K9 cannot see M5 or M6 at all. K1 exits at lines 209-211 before any leg is computed. Only K-pass (battery.py:238, measurement mode) runs the self-run and blind-run legs, and it sees the real value of 1.
3. K0's forge failure is masked: line 282 `bound == 10` already fails on the forged 9-row display, so `display_forge_fails` adds nothing there (M8 survives K0).
4. K4 (registry quote_line moved) fails the `quote_line` check (line 127) before the section test is reached, so it masks M7.

Frozen-row reproduction: the unmutated run of the seven rows matched the frozen receipt `controls/battery-summary-r51-freeze-c3.jsonl` (7/7 as expected; K-pass legs identical).

## Survival table (frozen battery)

| Mutant (single edit, frozen bytes) | Forced leg | Frozen 7 rows | Killed by |
|---|---|---|---|
| M5 self-run skipped, `override_blocked = 1` (lines 256-263 → one line) | override_blocked | all as expected: SURVIVES | none |
| M6 `r50_blind = 1` (line 273) | r50_blind | SURVIVES | none |
| M7a heading-section test dropped (lines 134-135 → `pass`) | quote_specific section leg | SURVIVES | none |
| M7b whole heading block dropped (lines 129-135) | quote_specific heading leg | SURVIVES | none |
| M8 `display_forge_fails = 1` (line 244) | display_forge_fails | SURVIVES | none |

## Proposed missing controls (K6-K9)

Each control is a measurement-mode or control-mode row whose real leg value is 0 on purpose, so only a counter that really evaluates that leg can return the expected verdict. Mechanism is run as a variant copy inside the battery's scratch (`--lane` set to the frozen lane, so no lane write).

| Control | Applied to unmutated counter | Applied to mutant | Killed |
|---|---|---|---|
| K6 self-run child is an accepting stub, measurement must FAIL | FAIL (override_blocked 0) | M5: no self-run line exists, so the counter prints PASS | M5 |
| K7 round-50 child rejects any override, measurement must FAIL | FAIL (r50_blind 0) | M6: PASS (r50_blind forced 1) | M6 |
| K8 display prefix check blinded (line 107 → `if False:`), measurement must FAIL | FAIL (display_forge_fails 0) | M8: PASS (forced 1) | M8 |
| K9 displayed + registry heading of OUT-010 moved to `## Core / Frontier / Adjacent (fleet round 1, appended 2026-10-19)` (PROVINCE.md:22 section; quote at :7; quote_line intact), `--control` must CONTROL-FAIL | CONTROL-FAIL (quote_specific 9) | M7a and M7b: CONTROL-PASS (quote_specific 10) | M7a, M7b |

Validation (prop_run.py, battery_prop.py = battery.py + c3_extra hooked into c3_battery):
- orig: 11/11 rows as expected; killed by: nothing
- M5: 10/11 rows as expected; killed by: K6 accepting self-run child: override leg must FAIL the measurement
- M6: 10/11 rows as expected; killed by: K7 round-50 child not blind to the forgery: r50_blind leg must FAIL the measurement
- M7a: 10/11 rows as expected; killed by: K9 heading moved to a section without the quote: quote_specific leg must FAIL
- M7b: 10/11 rows as expected; killed by: K9 heading moved to a section without the quote: quote_specific leg must FAIL
- M8: 10/11 rows as expected; killed by: K8 display check blind to a forged OUT-009 commit: display_forge leg must FAIL

The original seven rows are unchanged; the battery is still 11 rows and runs in about 6 s per variant.

## Proposed text (exact; apply to controls/battery.py, not applied in the lane)

Replace the final line of `c3_battery` (`    return out`, the one immediately before `def main():`) with `    return out + c3_extra(freeze, scratch)`, and insert the block below before `def main():`. Source: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-51/w1/R51MutC3b/battery_prop.py (the full patched battery is there; sha256 e8332071daaa4b2e...).

```python
STUB_CHILD = ("import json, sys\nprint(json.dumps({'verdict': 'PASS', 'control': 'accepting-child-stub'}))\n"
              "sys.exit(0)\n")
SELF_CHILD_OLD = "[sys.executable, os.path.abspath(__file__), '--revision', rev, '--lane', lane,"
SELF_CHILD_NEW = ("[sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'accepting_child.py'), "
                  "'--revision', rev, '--lane', lane,")
R50_MAIN_OLD = 'def main():\n'
R50_MAIN_NEW = ("def main():\n    if '--province-file' in sys.argv:\n"
                "        print(json.dumps({'verdict': 'FAIL', 'control': 'K7'}))\n        return 1\n")
DISPLAY_OLD = '            if not full_commit.startswith(m.group(2)):'
DISPLAY_NEW = '            if False:'
HEAD_NEW = '## Core / Frontier / Adjacent (fleet round 1, appended 2026-10-19)'


def c3_extra(freeze, scratch):
    """Round-51 mutation controls K6-K9. Each one makes a leg that the existing rows never see fail on purpose,
    so a counter whose leg is forced to 1 (or whose heading section test is dropped) no longer matches."""
    out = []
    base = open(C3, encoding='utf-8').read()
    r50 = open(os.path.join(os.path.dirname(C3), 'check-adjacency-table-r50.py'), encoding='utf-8').read()
    d = os.path.join(scratch, 'c3x')
    os.makedirs(d, exist_ok=True)

    def variant(name, c3_text, r50_text, extra):
        vd = os.path.join(d, name, 'tools')
        os.makedirs(vd, exist_ok=True)
        with open(os.path.join(vd, 'check-adjacency-table-r51.py'), 'w', encoding='utf-8') as fh:
            fh.write(c3_text)
        with open(os.path.join(vd, 'check-adjacency-table-r50.py'), 'w', encoding='utf-8') as fh:
            fh.write(r50_text)
        with open(os.path.join(vd, 'accepting_child.py'), 'w', encoding='utf-8') as fh:
            fh.write(STUB_CHILD)
        cmd = [sys.executable, os.path.join(vd, 'check-adjacency-table-r51.py'), '--revision', freeze,
               '--lane', L, '--no-base-check'] + extra
        return run_json(cmd)

    def add(name, expect, rc, obj):
        out.append({'control': name, 'expected': expect, 'got': obj.get('verdict'), 'rc': rc,
                    'as_expected': obj.get('verdict') == expect,
                    'legs': {k: obj.get(k) for k in ('display_bound_ok', 'quote_specific_ok', 'digests_bound_ok',
                                                     'display_forge_fails', 'override_blocked', 'r50_blind',
                                                     'quote_at_pin_ok', 'stub_fails')}})

    # K6: a self-run child that accepts the override (unguarded) must make the measurement FAIL
    rc, obj = variant('k6', base.replace(SELF_CHILD_OLD, SELF_CHILD_NEW), r50, [])
    add('K6 accepting self-run child: override leg must FAIL the measurement', 'FAIL', rc, obj)
    # K7: a round-50 sensitivity child that rejects overrides (r50 not blind) must make the measurement FAIL
    assert r50.count(R50_MAIN_OLD) == 1
    rc, obj = variant('k7', base, r50.replace(R50_MAIN_OLD, R50_MAIN_NEW), [])
    add('K7 round-50 child not blind to the forgery: r50_blind leg must FAIL the measurement', 'FAIL', rc, obj)
    # K8: a display check blind to the displayed OUT-009 commit must make the measurement FAIL (forge leg)
    rc, obj = variant('k8', base.replace(DISPLAY_OLD, DISPLAY_NEW), r50, [])
    add('K8 display check blind to a forged OUT-009 commit: display_forge leg must FAIL', 'FAIL', rc, obj)
    # K9: a displayed heading and registry heading moved to a section that does not hold the quote
    prov = git_show(freeze, 'PROVINCE.md')
    reg = json.loads(git_show(freeze, 'corpus/knowledge/adjacency-anchors-r19.json'))
    lines = prov.split('\n')
    hit = [i for i, ln in enumerate(lines) if ln.startswith('| OUT-010 |')]
    assert len(hit) == 1 and lines[hit[0]].count('`# tameshi-shokunin — Province`') == 1
    lines[hit[0]] = lines[hit[0]].replace('`# tameshi-shokunin — Province`', '`' + HEAD_NEW + '`')
    for row in reg['outbound']:
        if row['id'] == 'OUT-010':
            row['heading'] = HEAD_NEW
    p9 = os.path.join(d, 'k9-province.md')
    r9 = os.path.join(d, 'k9-registry.json')
    with open(p9, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(lines))
    with open(r9, 'w', encoding='utf-8') as fh:
        fh.write(json.dumps(reg))
    rc, obj = variant('k9', base, r50, ['--control', '--province-file', p9, '--registry-file', r9])
    add('K9 heading moved to a section without the quote: quote_specific leg must FAIL', 'CONTROL-FAIL', rc, obj)
    return out
```

## Limits (named)

- K7 is blunt: the variant rejects every override, so it proves the `r50_blind` branch can fail, not that the round-50 counter detects a forged OUT-009 commit. A display-aware round-50 variant would be stronger.
- K6 on M5 is not a stub run: M5 has removed the self-run line, so the counter's real measurement returns PASS. The kill is the forced leg's PASS, which is the behaviour we want the control to expose, but the proof is the M5 K-pass value, not a stub.
- K9 hard-codes the tameshi OUT-010 heading text and the province row; it is a frozen-round control.
- Mutants are one-line edits. Other forms (e.g. self-run executed with its result ignored) were not measured.
- The lane was not edited. Receipts and proposal text only.

## Receipts (under /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-51/w1/R51MutC3b/)

driver.py (first set + M5-M8 battery and control runs, out-results.json), prop_build.py and prop_run.py (proposed rows and mutant runs), battery_prop.py (patched battery), prop-summary.json, out-results.json, run2.log, stubs/accepting_child.py, frozen counter copies, sha256.txt.

## Tooling and scope

No tools installed. Scratch under /fast/scratch/hyaku/tsukuroi-r51/R51MutC3b (lane clone, shared-git, detached at 2732ee6) removed after copy. The lane was read with `git show` only; no tracked lane file and no fleet file was written. Not run: the C1 and C2 counters, the selftest census, and the lane's own battery (`--tag` writes) — not in this item.
