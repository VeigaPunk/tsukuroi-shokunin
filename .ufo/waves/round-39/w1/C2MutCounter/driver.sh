#!/usr/bin/env bash
# C2MutCounter (round 39 w1) — mutation test of the frozen C2 counter
# tools/check-transaction-order-r39.py against the committed controls
# .ufo/waves/round-39/controls/c2-entries/*/, rebuilt as fixture commits on the
# counters-freeze revision 6a08925d exactly the way controls/run-controls.sh builds them.
# Lane repo is only ever read; every write lands in the seat dir or this scratch dir.
set -euo pipefail
SEAT=C2MutCounter
LANE=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
CTL=$LANE/.ufo/waves/round-39/controls
SEATDIR=$LANE/.ufo/waves/round-39/w1/$SEAT
S=/fast/scratch/hyaku/tsukuroi-r39/$SEAT
FREEZE=6a08925daa30767809eb13bb4b01448ff954d46a
COUNTER=tools/check-transaction-order-r39.py
ENTRIES=(E1-no-upstream-row E2-lines-shifted E3-sid-dropped E4-block-duplicated E5-host-counts-wrong E6-candidate E7-opened-stale)

mkdir -p "$S" "$SEATDIR/mutants" "$SEATDIR/runs"
export TMPDIR="$S"
trap 'rm -rf -- "$S"' EXIT
cp "$0" "$SEATDIR/driver.sh"

# ---- 0. pristine bytes + sha ------------------------------------------------
cp "$LANE/$COUNTER" "$SEATDIR/mutants/pristine.py"
sha256sum "$LANE/$COUNTER" | tee "$SEATDIR/mutants/pristine.sha256"

# ---- 1. generate the five single-point mutants (assert: pattern found once) --
python3 - "$LANE/$COUNTER" "$SEATDIR/mutants" <<'PYEOF'
import difflib, pathlib, py_compile, sys
src_p, outdir = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
text = src_p.read_bytes().decode()

def mutate(name, pairs):
    m = text
    for old, new in pairs:
        n = m.count(old)
        assert n == 1, f'{name}: pattern count {n} for {old[:60]!r}'
        m = m.replace(old, new)
    p = outdir / f'{name}.py'
    p.write_text(m)
    py_compile.compile(str(p), doraise=True)
    d = difflib.unified_diff(text.splitlines(), m.splitlines(), 'pristine', name, lineterm='', n=2)
    (outdir / f'{name}.diff').write_text('\n'.join(d) + '\n')
    print(f'{name}: generated, py_compile ok')

mutate('M1-drop-missing-sid', [(
    "r['verified'] = not missing and bool(upstream) and quote_ok",
    "r['verified'] = bool(upstream) and quote_ok")])

mutate('M2-ownwork-upstream', [(
    """upstream = [i for i in ids if i in srows and srows[i]['status'] == 'mined'
                        and ENTRY_NAME in srows[i]['used_by'] and '54d9411' in srows[i]['title']
                        and re.search(r'lib/libalpm/' + re.escape(want) + r'(\\s|$)', srows[i]['title'])]""",
    """upstream = [i for i in ids if i in srows and srows[i]['status'] == 'mined'
                        and ENTRY_NAME in srows[i]['used_by']]""")])

mutate('M3-ignore-line-range', [(
    "body = collapse(' '.join(src[want][lo - 1:hi]))",
    "body = collapse(' '.join(src[want]))")])

mutate('M4-skip-dup-count', [
    ("dup_rows = sum(len(v) - 1 for v in seen.values())", "dup_rows = 0"),
    ("dup_heads = len(heads) - len(set(heads))", "dup_heads = 0")])

mutate('M5-drop-opened-date', [(
    """source_ok = int(bool(header_ids) and len(good) == len(header_ids)
                        and any(srows[i]['opened'] == OPENED for i in good))""",
    "source_ok = int(bool(header_ids) and len(good) == len(header_ids))")])
PYEOF

# ---- E7 generator: E6 candidate with the seven cited rows' opened dates flipped
cat > "$SEATDIR/mutants/e7_gen.py" <<'PYEOF'
"""Build the proposed missing control E7-opened-stale: the E6 candidate entry
verbatim, but in SOURCES.md the `opened` cell of every row the entry cites
(S208, S213-S218) is 2026-10-25 instead of 2026-10-26, so the counter's
opened-date term is the only failing source_ok conjunct."""
import pathlib, re, sys
src = pathlib.Path(sys.argv[1]).read_text()
ids = {'S208', 'S213', 'S214', 'S215', 'S216', 'S217', 'S218'}
out, changed = [], 0
for line in src.splitlines():
    m = re.match(r'^\| (S\d{3,}) \|', line)
    if m and m.group(1) in ids:
        parts = line.split('|')
        assert parts[9].strip() == '2026-10-26', (m.group(1), parts[9])
        parts[9] = parts[9].replace('2026-10-26', '2026-10-25')
        line = '|'.join(parts)
        changed += 1
    out.append(line)
assert changed == 7, f'expected 7 cited rows, changed {changed}'
pathlib.Path(sys.argv[2]).write_text('\n'.join(out) + '\n')
print(f'E7 SOURCES.md written, {changed} opened cells flipped')
PYEOF

# ---- 2. scratch clone of the lane at the counters-freeze revision ------------
D=$S/clone
git clone -q --no-local "$LANE" "$D"
git -C "$D" remote remove origin
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo "FATAL toplevel mismatch" >&2; exit 2; }
git -C "$D" checkout -q -B master "$FREEZE"
gc() { git -C "$D" -c user.name=mut -c user.email=mut@scratch.invalid commit -q -m "$1"; }

# ---- 3. build fixture branches once (corpus-only commits on FREEZE) ----------
for e in "${ENTRIES[@]}"; do
  git -C "$D" checkout -q -B "e-$e" "$FREEZE"
  if [ "$e" = E7-opened-stale ]; then
    python3 "$SEATDIR/mutants/e7_gen.py" "$CTL/c2-entries/E6-candidate/SOURCES.md" "$D/corpus/SOURCES.md"
    cp "$CTL/c2-entries/E6-candidate/entry.md" "$D/corpus/knowledge/pacman-transaction-order-r39.md"
  else
    cp "$CTL/c2-entries/$e/entry.md"   "$D/corpus/knowledge/pacman-transaction-order-r39.md"
    cp "$CTL/c2-entries/$e/SOURCES.md" "$D/corpus/SOURCES.md"
  fi
  git -C "$D" add corpus
  gc "control $e"
done
git -C "$D" checkout -q -B runner "$FREEZE"   # working tree parked at FREEZE; master free to move

# ---- 4. run one counter variant over all controls ----------------------------
run_variant() { # <label>; counter bytes already in place at $D/$COUNTER
  local label=$1 out="$SEATDIR/runs/$1" rev c
  mkdir -p "$out"
  sha256sum "$D/$COUNTER" | cut -d' ' -f1 > "$out/counter.sha256"
  for c in K0-do-nothing "${ENTRIES[@]}"; do
    if [ "$c" = K0-do-nothing ]; then git -C "$D" branch -f master "$FREEZE";
    else git -C "$D" branch -f master "refs/heads/e-$c"; fi
    rev=$(git -C "$D" rev-parse master)
    set +e
    TMPDIR=$S python3 "$D/$COUNTER" --repo "$D" --revision "$rev" \
      > "$out/$c.json" 2> "$out/$c.err"
    echo $? > "$out/$c.exit"
    set -e
  done
}

# ---- 5. pristine baseline ----------------------------------------------------
cp "$SEATDIR/mutants/pristine.py" "$D/$COUNTER"
run_variant pristine

# ---- 6. mutants --------------------------------------------------------------
for m in M1-drop-missing-sid M2-ownwork-upstream M3-ignore-line-range M4-skip-dup-count M5-drop-opened-date; do
  cp "$SEATDIR/mutants/$m.py" "$D/$COUNTER"
  run_variant "$m"
done

# ---- 7. restore pristine bytes; re-run as restoration evidence ---------------
cp "$SEATDIR/mutants/pristine.py" "$D/$COUNTER"
sha256sum "$D/$COUNTER" | cut -d' ' -f1 > "$SEATDIR/runs/restored-counter.sha256"
run_variant restored
sha256sum "$LANE/$COUNTER" | cut -d' ' -f1 > "$SEATDIR/runs/lane-counter-after.sha256"

# ---- 8. compare against recorded controls and the pristine run ---------------
python3 - "$CTL/controls.jsonl" "$SEATDIR/runs" "$SEATDIR" <<'PYEOF'
import json, pathlib, sys
ctl, runs, seat = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3])
KEYS = ('rules_verified', 'duplicate_rows', 'duplicate_headings', 'source_ok',
        'counts_ok', 'oracle_violations', 'result', 'exit')
CONTROLS = ['K0-do-nothing', 'E1-no-upstream-row', 'E2-lines-shifted',
            'E3-sid-dropped', 'E4-block-duplicated', 'E5-host-counts-wrong',
            'E6-candidate', 'E7-opened-stale']
recs = {}
for line in pathlib.Path(ctl).read_text().splitlines():
    r = json.loads(line)
    if r.get('counter', '').endswith('check-transaction-order-r39.py'):
        recs[r['control']] = r

def load(p):
    try:
        return json.loads(pathlib.Path(p).read_text())
    except Exception as e:
        return {'_parse_error': str(e)}

def metrics(o):
    return {k: o.get(k, '<missing>') for k in KEYS}

pristine = {c: metrics(load(runs / 'pristine' / f'{c}.json')) for c in CONTROLS}
rows = []
for v in sorted(d.name for d in runs.iterdir() if d.is_dir()):
    for c in CONTROLS:
        obs = metrics(load(runs / v / f'{c}.json'))
        rec = recs.get('C2-' + c)
        vs_rec = ('no-recorded-row' if rec is None else
                  ('MATCH' if metrics(rec) == obs else 'DIFFERS:' + ','.join(
                      k for k in KEYS if metrics(rec)[k] != obs[k])))
        vs_pri = ('self' if v == 'pristine' else
                  ('MATCH' if pristine[c] == obs else 'DIFFERS:' + ','.join(
                      k for k in KEYS if pristine[c][k] != obs[k])))
        rows.append({'variant': v, 'control': c, 'vs_recorded': vs_rec,
                     'vs_pristine_run': vs_pri, 'observed': obs})
        print(f'{v:22s} {c:20s} vs_recorded={vs_rec:60s} vs_pristine={vs_pri}')
json.dump(rows, (seat / 'verdicts.json').open('w'), indent=1)

# verdict per mutant: killed by every control whose observed metrics differ from
# the pristine run (equivalently from the recorded row, since pristine==recorded).
print('\n=== MUTANT VERDICTS ===')
for m in ['M1-drop-missing-sid', 'M2-ownwork-upstream', 'M3-ignore-line-range',
          'M4-skip-dup-count', 'M5-drop-opened-date']:
    killers = [r['control'] for r in rows if r['variant'] == m and r['vs_pristine_run'].startswith('DIFFERS')]
    v = 'SURVIVES' if not killers else 'KILLED by ' + ', '.join(killers)
    print(f'{m:22s} {v}')
PYEOF

echo DONE
