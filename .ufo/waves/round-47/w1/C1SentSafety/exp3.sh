#!/bin/bash
set -u
S=/fast/scratch/hyaku/tsukuroi-r47/C1SentSafety
C=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r47.py
D=$S/fx3
rm -rf "$D"
git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D" || { echo CLONE_FAIL; exit 9; }
git -C "$D" remote remove origin
TOP=$(git -C "$D" rev-parse --show-toplevel); [ "$TOP" = "$D" ] || { echo MISMATCH; exit 9; }
R0=$(git -C "$D" rev-parse HEAD); echo "R0=$R0"
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
GR1H=$(python3 "$C" --lane "$D" --revision "$R0" --section-hash | python3 -c 'import json,sys;print(json.load(sys.stdin)["section_sha256"]["GR1"])')

echo "=== F1 wave '..' as the ONLY dispatch for a seat (report outside the wave dir) ==="
git -C "$D" rm -q .ufo/waves/round-47/w1-dispatch.json
python3 - "$D" "$GR1H" <<'EOF'
import json, os, sys
d, h = sys.argv[1], sys.argv[2]
base = os.path.join(d, '.ufo/waves/round-47')
json.dump({'taskCall': {'tasks': [{'name': 'R47RevGR1a', 'agent': 'reviewer'}]}}, open(os.path.join(base, '..-dispatch.json'), 'w'))
json.dump({'results': [{'name': 'R47RevGR1a', 'agent': 'reviewer'}]}, open(os.path.join(base, '..-results.json'), 'w'))
os.makedirs(os.path.join(d, '.ufo/waves/round-47/w1'), exist_ok=True)
open(os.path.join(d, '.ufo/waves/R47RevGR1a.md'), 'w').write(
    'ROW GR1 VERDICT: holds\nSECTION SHA256: ' + h + '\n'
    + 'Anchors cmdline.c:147, vsprintf.c:86, kstrtox.c:29. ' + 'x' * 320 + '\n')
EOF
git -C "$D" add -A; git -C "$D" commit -qm f1; F1=$(git -C "$D" rev-parse HEAD)
python3 "$C" --lane "$D" --revision "$F1" | python3 -c '
import json,sys;d=json.load(sys.stdin)
print("waves_seen=",d["waves_seen"])
print("GR1 seat:",json.dumps(d["per_row"]["GR1"]["seats"]["R47RevGR1a"]),"bound=",d["per_row"]["GR1"]["bound_on_current"])'
echo "--- git cannot read the escaped path ---"
git -C "$D" show "$F1:.ufo/waves/round-47/../R47RevGR1a.md" >/dev/null 2>"$S/f1.err"; echo "rc=$? :: $(cat "$S/f1.err")"
echo "--- write-freedom: fixture tree unchanged by the counter run ---"
git -C "$D" status --porcelain | head -5; echo "porcelain_lines=$(git -C "$D" status --porcelain | wc -l)"

echo "=== G1 negative control: tampered pinned snapshot must invalidate row quotes ==="
git -C "$D" reset -q --hard "$R0" && git -C "$D" clean -qfdx
printf '\n// tampered line appended by C1SentSafety fixture\n' >> "$D/.ufo/waves/round-44/frozen/src/scrub.c"
printf '\n// tampered line appended by C1SentSafety fixture\n' >> "$D/.ufo/waves/round-45/frozen/src/cmdline.c"
git -C "$D" add -A; git -C "$D" commit -qm g1; G1=$(git -C "$D" rev-parse HEAD)
python3 "$C" --lane "$D" --revision "$G1" | python3 -c '
import json,sys;d=json.load(sys.stdin)
print("quotes_ok=",d["quotes_ok"])
for r in ("GR1","GR2","GR3"):
    q=d["per_row"][r]["quotes"]; print(r,"ok=",q["ok"],"/",q["quotes"],"bad0=",(q["bad"][0][:70] if q["bad"] else None))'
echo "=== G2 substitution attack: swap the S242 blob content for the S237 bytes at the S242 path ==="
git -C "$D" reset -q --hard "$R0" && git -C "$D" clean -qfdx
cp "$D/.ufo/waves/round-42/frozen/src/scrub.c" "$D/.ufo/waves/round-44/frozen/src/scrub.c"
git -C "$D" add -A; git -C "$D" commit -qm g2; G2=$(git -C "$D" rev-parse HEAD)
python3 "$C" --lane "$D" --revision "$G2" | python3 -c '
import json,sys;d=json.load(sys.stdin)
print("quotes_ok=",d["quotes_ok"],"GR2 ok=",d["per_row"]["GR2"]["quotes"]["ok"],"/",d["per_row"]["GR2"]["quotes"]["quotes"])
print("GR2 bad0=",d["per_row"]["GR2"]["quotes"]["bad"][:1])'
echo DONE
