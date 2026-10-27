#!/bin/bash
# C1SentSafety exp4: end-to-end proof that the F2 README-mark bypass can carry a full PASS.
set -u
S=/fast/scratch/hyaku/tsukuroi-r47/C1SentSafety
C=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r47.py
D=$S/fx4
rm -rf "$D"
git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D" || { echo CLONE_FAIL; exit 9; }
git -C "$D" remote remove origin
TOP=$(git -C "$D" rev-parse --show-toplevel); [ "$TOP" = "$D" ] || { echo MISMATCH; exit 9; }
R0=$(git -C "$D" rev-parse HEAD); echo "R0=$R0"
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
H=$(python3 "$C" --lane "$D" --revision "$R0" --section-hash | python3 -c 'import json,sys;d=json.load(sys.stdin)["section_sha256"];print(d["GR1"],d["GR2"],d["GR3"])')
set -- $H; H1=$1 H2=$2 H3=$3
echo "H1=$H1"; echo "H2=$H2"; echo "H3=$H3"

plant(){  # $1 = README line
python3 - "$D" "$H1" "$H2" "$H3" "$1" <<'EOF'
import json, os, sys
d, h1, h2, h3, readme_line = sys.argv[1:6]
E = os.path.join(d, 'corpus/knowledge/btrfs-scrub-grounding-r45.md')
open(E, 'a', encoding='utf-8').write('\n## Gate status \u2014 round 47 (GR1-GR3 admitted)\n')
open(os.path.join(d, 'SKILL.md'), 'a', encoding='utf-8').write('\n## Scrub grounding \u2014 round 47 admission\n')
open(os.path.join(d, 'corpus/README.md'), 'a', encoding='utf-8').write(readme_line + '\n')
W = os.path.join(d, '.ufo/waves/round-47/w1')
os.makedirs(W, exist_ok=True)
rows = {'GR1': (h1, 'cmdline.c:147'), 'GR2': (h2, 'dev-replace.c:700'), 'GR3': (h3, 'systemd-kill:68')}
rows['GR3'] = (h3, 'systemd.kill.xml:68')
seats = {'GR1': ('R47RevGR1a', 'R47CritGR1a'), 'GR2': ('R47RevGR2a', 'R47CritGR2a'),
         'GR3': ('R47RevGR3a', 'R47CritGR3a')}
results = []
for row, (digest, cite) in rows.items():
    for n, seat in enumerate(seats[row]):
        role = 'reviewer' if 'Rev' in seat else 'critic'
        body = (f'{seat} read the row against its pinned snapshot at {cite} and checked the '
                f'ordering of the checks the row states, then re-read the quoted lines one by one '
                f'for the {row} bytes; this body is padded so it clears the three hundred byte floor '
                f'and differs from its sibling by this sentence, filler {row}-{n}-' + 'z' * 200 + '\n')
        open(os.path.join(W, seat + '.md'), 'w', encoding='utf-8').write(
            f'ROW {row} VERDICT: holds\nSECTION SHA256: {digest}\n' + body)
        results.append({'name': seat, 'agent': role})
json.dump({'results': results}, open(os.path.join(d, '.ufo/waves/round-47/w1-results.json'), 'w'))
EOF
}

summ(){ python3 "$C" --lane "$D" --revision "$1" | python3 -c '
import json,sys;d=json.load(sys.stdin)
print("marks=",json.dumps(d.get("marks"),sort_keys=True),"marks_ok=",d.get("marks_ok"),
      "structural_ok=",d.get("structural_ok"),"quotes_ok=",d.get("quotes_ok"),
      "verdicts_ok=",d.get("verdicts_ok"),"VERDICT=",d.get("verdict"))'; }

echo "=== H1 all-green fixture, README says: Not admitted round 47 (capital N) ==="
plant '| `knowledge/btrfs-scrub-grounding-r45.md` | Not admitted round 47: still pending |'
git -C "$D" add -A; git -C "$D" commit -qm h1; H1C=$(git -C "$D" rev-parse HEAD); summ "$H1C"
echo "=== H2 same fixture, README says: not admitted round 47 (control) ==="
git -C "$D" reset -q --hard "$R0"; git -C "$D" clean -qfdx
plant '| `knowledge/btrfs-scrub-grounding-r45.md` | not admitted round 47: still pending |'
git -C "$D" add -A; git -C "$D" commit -qm h2; H2C=$(git -C "$D" rev-parse HEAD); summ "$H2C"
echo "=== H3 same fixture, README says: admitted round 47 (honest grant) ==="
git -C "$D" reset -q --hard "$R0"; git -C "$D" clean -qfdx
plant '| `knowledge/btrfs-scrub-grounding-r45.md` | GR1-GR3 admitted round 47 (all three holds) |'
git -C "$D" add -A; git -C "$D" commit -qm h3; H3C=$(git -C "$D" rev-parse HEAD); summ "$H3C"
echo "=== H4 same fixture, README says: not<NBSP>admitted round 47 ==="
git -C "$D" reset -q --hard "$R0"; git -C "$D" clean -qfdx
plant "$(printf '| `knowledge/btrfs-scrub-grounding-r45.md` | not\xc2\xa0admitted round 47; still pending |')"
git -C "$D" add -A; git -C "$D" commit -qm h4; H4C=$(git -C "$D" rev-parse HEAD); summ "$H4C"
echo DONE
