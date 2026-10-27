#!/bin/bash
# C1SentSafety: adversarial probes against the frozen r47 admission counter (fixture clone only).
set -u
S=/fast/scratch/hyaku/tsukuroi-r47/C1SentSafety
C=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r47.py
D=$S/fx
rm -rf "$D"
git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D" || { echo CLONE_FAIL; exit 9; }
git -C "$D" remote remove origin
TOP=$(git -C "$D" rev-parse --show-toplevel)
[ "$TOP" = "$D" ] || { echo "TOPLEVEL_MISMATCH $TOP"; exit 9; }
R0=$(git -C "$D" rev-parse HEAD)
echo "R0=$R0 TOP=$TOP"
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
com() { git -C "$D" add -A && git -C "$D" commit -qm "$1" && git -C "$D" rev-parse HEAD; }
reset0() { git -C "$D" reset -q --hard "$R0" && git -C "$D" clean -qfdx; }
marks() { python3 -c 'import json,sys;d=json.load(sys.stdin);print("marks=",json.dumps(d.get("marks"),sort_keys=True),"marks_ok=",d.get("marks_ok"),"verdict=",d.get("verdict"))'; }

echo "=== A1 README negation, capital N ==="
printf '\n## Gate status \xe2\x80\x94 round 47 (GR1-GR3 admitted)\n' >> "$D/corpus/knowledge/btrfs-scrub-grounding-r45.md"
printf '\n## Scrub grounding \xe2\x80\x94 round 47 admission\n' >> "$D/SKILL.md"
printf '| `knowledge/btrfs-scrub-grounding-r45.md` | Not admitted round 47: still pending |\n' >> "$D/corpus/README.md"
A1=$(com a1); python3 "$C" --lane "$D" --revision "$A1" | marks
reset0
echo "=== A2 README negation, NBSP separator ==="
printf '\n## Gate status \xe2\x80\x94 round 47 (GR1-GR3 admitted)\n' >> "$D/corpus/knowledge/btrfs-scrub-grounding-r45.md"
printf '\n## Scrub grounding \xe2\x80\x94 round 47 admission\n' >> "$D/SKILL.md"
python3 - "$D/corpus/README.md" <<'EOF'
import sys
p = sys.argv[1]
with open(p, 'a', encoding='utf-8') as f:
    f.write('| `knowledge/btrfs-scrub-grounding-r45.md` | not\u00a0admitted round 47; still pending |\n')
EOF
A2=$(com a2); python3 "$C" --lane "$D" --revision "$A2" | marks
reset0
echo "=== A3 CONTROL: plain lowercase negation ==="
printf '\n## Gate status \xe2\x80\x94 round 47 (GR1-GR3 admitted)\n' >> "$D/corpus/knowledge/btrfs-scrub-grounding-r45.md"
printf '\n## Scrub grounding \xe2\x80\x94 round 47 admission\n' >> "$D/SKILL.md"
printf '| `knowledge/btrfs-scrub-grounding-r45.md` | not admitted round 47: still pending |\n' >> "$D/corpus/README.md"
A3=$(com a3); python3 "$C" --lane "$D" --revision "$A3" | marks
reset0
echo "=== A4 README negation by homoglyph negation word alongside grant phrase ==="
printf '\n## Gate status \xe2\x80\x94 round 47 (GR1-GR3 admitted)\n' >> "$D/corpus/knowledge/btrfs-scrub-grounding-r45.md"
printf '\n## Scrub grounding \xe2\x80\x94 round 47 admission\n' >> "$D/SKILL.md"
python3 - "$D/corpus/README.md" <<'EOF'
import sys
with open(sys.argv[1], 'a', encoding='utf-8') as f:
    f.write('| `knowledge/btrfs-scrub-grounding-r45.md` | \u043d\u043e\u0442 admitted round 47 (Cyrillic "not"), row pending |\n')
EOF
A4=$(com a4); python3 "$C" --lane "$D" --revision "$A4" | marks
reset0
echo "=== B1 quote leg: content-free fragment quote ==="
python3 - "$D/corpus/knowledge/btrfs-scrub-grounding-r45.md" <<'EOF'
import sys, re
p = sys.argv[1]
lines = open(p, encoding='utf-8').read().split('\n')
ln = lines[26]
assert ln.startswith('**Quote.** `S246` cmdline.c:147: '), ln
lines[26] = re.sub(r'"(.*)"\s*$', '"."', ln)
open(p, 'w', encoding='utf-8').write('\n'.join(lines))
EOF
B1=$(com b1); python3 "$C" --lane "$D" --revision "$B1" | python3 -c 'import json,sys;d=json.load(sys.stdin);print("quotes_ok=",d["quotes_ok"],"GR1 quotes=",json.dumps(d["per_row"]["GR1"]["quotes"]))'
reset0
echo "=== B2 CONTROL: fabricated quote text ==="
python3 - "$D/corpus/knowledge/btrfs-scrub-grounding-r45.md" <<'EOF'
import sys, re
p = sys.argv[1]
lines = open(p, encoding='utf-8').read().split('\n')
lines[26] = re.sub(r'"(.*)"\s*$', '"this sentence is nowhere in the source file"', lines[26])
open(p, 'w', encoding='utf-8').write('\n'.join(lines))
EOF
B2=$(com b2); python3 "$C" --lane "$D" --revision "$B2" | python3 -c 'import json,sys;d=json.load(sys.stdin);print("quotes_ok=",d["quotes_ok"],"GR1 quotes=",json.dumps(d["per_row"]["GR1"]["quotes"]))'
reset0
echo "=== C1 CITE_RE cost reachable end-to-end (64 KiB single token body) ==="
GR1H=$(python3 "$C" --lane "$D" --revision "$R0" --section-hash | python3 -c 'import json,sys;print(json.load(sys.stdin)["section_sha256"]["GR1"])')
mkdir -p "$D/.ufo/waves/round-47/w1"
python3 - "$D/.ufo/waves/round-47/w1/R47RevGR1a.md" "$GR1H" <<'EOF'
import sys
p, h = sys.argv[1], sys.argv[2]
body = 'cmdline.c:147 resolves here. ' + 'a.' * 32768 + '\n'
open(p, 'w', encoding='utf-8').write(
    'ROW GR1 VERDICT: holds\nSECTION SHA256: ' + h + '\n' + body)
EOF
python3 - "$D/.ufo/waves/round-47/w1-results.json" <<'EOF'
import json, sys
json.dump({'results': [{'name': 'R47RevGR1a', 'agent': 'reviewer'}]}, open(sys.argv[1], 'w'))
EOF
C1=$(com c1); echo "body bytes: $(wc -c < "$D/.ufo/waves/round-47/w1/R47RevGR1a.md")"
/usr/bin/time -f 'counter wall: %e s' python3 "$C" --lane "$D" --revision "$C1" 2>&1 >/dev/null | tail -1
python3 "$C" --lane "$D" --revision "$C1" | python3 -c 'import json,sys;d=json.load(sys.stdin);print("GR1 bound:",d["per_row"]["GR1"]["bound_on_current"],"seats:",json.dumps(d["per_row"]["GR1"]["seats"]["R47RevGR1a"])[:200])'
reset0
echo "=== D1 wave name '..' + NBSP verdict line ==="
python3 - "$D" "$GR1H" <<'EOF'
import json, sys, os
d, h = sys.argv[1], sys.argv[2]
base = os.path.join(d, '.ufo/waves/round-47')
json.dump({'taskCall': {'tasks': [{'name': 'R47RevGR1a', 'agent': 'reviewer'}]}},
          open(os.path.join(base, '..-dispatch.json'), 'w'))
json.dump({'results': [{'name': 'R47RevGR1a', 'agent': 'reviewer'}]},
          open(os.path.join(base, '..-results.json'), 'w'))
os.makedirs(os.path.join(d, '.ufo/waves/round-47/w1'), exist_ok=True)
# report placed OUTSIDE the wave dir, at .ufo/waves/R47RevGR1a.md
open(os.path.join(d, '.ufo/waves/R47RevGR1a.md'), 'w').write(
    'ROW GR1 VERDICT: holds\nSECTION SHA256: ' + h + '\n'
    + 'See cmdline.c:147 and vsprintf.c:86 and kstrtox.c:29 for the parse chain. ' + 'x' * 300 + '\n')
# NBSP in the binding line of a second seat, placed in the real wave dir
json.dump({'taskCall': {'tasks': [{'name': 'R47RevGR1a', 'agent': 'reviewer'},
                                 {'name': 'R47RevGR1b', 'agent': 'reviewer'}]}},
          open(os.path.join(base, 'w1-dispatch.json'), 'w'))
json.dump({'results': [{'name': 'R47RevGR1b', 'agent': 'reviewer'}]},
          open(os.path.join(base, 'w1-results.json'), 'w'))
open(os.path.join(base, 'w1/R47RevGR1b.md'), 'w').write(
    'ROW\u00a0GR1 VERDICT: holds\nSECTION SHA256: ' + h + '\n'
    + 'See cmdline.c:147. ' + 'y' * 320 + '\n')
EOF
D1=$(com d1)
python3 "$C" --lane "$D" --revision "$D1" | python3 -c '
import json,sys;d=json.load(sys.stdin)
print("waves_seen=",d["waves_seen"])
g=d["per_row"]["GR1"]
print("bound_on_current=",g["bound_on_current"])
print("a:",json.dumps(g["seats"]["R47RevGR1a"])[:200])
print("b:",json.dumps(g["seats"]["R47RevGR1b"])[:200])'
echo "=== git show for the escaped report path ==="
git -C "$D" show "$D1:.ufo/waves/round-47/../R47RevGR1a.md" >/dev/null 2>"$S/escape.err"; echo "rc=$? err=$(cat "$S/escape.err")"
reset0
echo DONE
