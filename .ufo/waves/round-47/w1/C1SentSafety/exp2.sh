#!/bin/bash
set -u
S=/fast/scratch/hyaku/tsukuroi-r47/C1SentSafety
C=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-admission-r47.py
D=$S/fx
rm -rf "$D"
git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$D" || { echo CLONE_FAIL; exit 9; }
git -C "$D" remote remove origin
TOP=$(git -C "$D" rev-parse --show-toplevel); [ "$TOP" = "$D" ] || { echo MISMATCH; exit 9; }
R0=$(git -C "$D" rev-parse HEAD); echo "R0=$R0"
export GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid
export GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
GR1H=$(python3 "$C" --lane "$D" --revision "$R0" --section-hash | python3 -c 'import json,sys;print(json.load(sys.stdin)["section_sha256"]["GR1"])')
echo "GR1H=$GR1H"
reset0() { git -C "$D" reset -q --hard "$R0" && git -C "$D" clean -qfdx; }

echo "=== C1a timing: 64 KiB single-token body through the counter ==="
mkdir -p "$D/.ufo/waves/round-47/w1"
python3 - "$D/.ufo/waves/round-47/w1/R47RevGR1a.md" "$GR1H" <<'EOF'
import sys
p, h = sys.argv[1], sys.argv[2]
open(p, 'w', encoding='utf-8').write('ROW GR1 VERDICT: holds\nSECTION SHA256: ' + h + '\n'
    + 'cmdline.c:147 cited. ' + 'a.' * 32768 + '\n')
EOF
python3 -c 'import json,sys;json.dump({"results":[{"name":"R47RevGR1a","agent":"reviewer"}]},open(sys.argv[1],"w"))' "$D/.ufo/waves/round-47/w1-results.json"
git -C "$D" add -A; git -C "$D" commit -qm c1a; C1=$(git -C "$D" rev-parse HEAD)
python3 - "$C" "$D" "$C1" <<'EOF'
import subprocess, sys, time
c, d, rev = sys.argv[1:4]
t = time.perf_counter()
p = subprocess.run(['python3', c, '--lane', d, '--revision', rev], capture_output=True, text=True)
print(f'64KiB-token body: wall {time.perf_counter()-t:.2f}s rc={p.returncode}')
print('GR1 bound:', __import__('json').loads(p.stdout)['per_row']['GR1']['bound_on_current'])
EOF
reset0
echo "=== C1b timing: same body, 8 KiB token (scaling control) ==="
python3 - "$D/.ufo/waves/round-47/w1/R47RevGR1a.md" "$GR1H" <<'EOF'
import sys
p, h = sys.argv[1], sys.argv[2]
open(p, 'w', encoding='utf-8').write('ROW GR1 VERDICT: holds\nSECTION SHA256: ' + h + '\n'
    + 'cmdline.c:147 cited. ' + 'a.' * 4096 + '\n')
EOF
python3 -c 'import json,sys;json.dump({"results":[{"name":"R47RevGR1a","agent":"reviewer"}]},open(sys.argv[1],"w"))' "$D/.ufo/waves/round-47/w1-results.json"
git -C "$D" add -A; git -C "$D" commit -qm c1b; C1B=$(git -C "$D" rev-parse HEAD)
python3 - "$C" "$D" "$C1B" <<'EOF'
import subprocess, sys, time
c, d, rev = sys.argv[1:4]
t = time.perf_counter()
p = subprocess.run(['python3', c, '--lane', d, '--revision', rev], capture_output=True, text=True)
print(f'8KiB-token body: wall {time.perf_counter()-t:.2f}s rc={p.returncode}')
EOF
reset0
echo "=== D1 wave named '..' only (report outside the wave dir) ==="
python3 - "$D" "$GR1H" <<'EOF'
import json, os, sys
d, h = sys.argv[1], sys.argv[2]
base = os.path.join(d, '.ufo/waves/round-47')
json.dump({'taskCall': {'tasks': [{'name': 'R47RevGR1a', 'agent': 'reviewer'}]}}, open(os.path.join(base, '..-dispatch.json'), 'w'))
json.dump({'results': [{'name': 'R47RevGR1a', 'agent': 'reviewer'}]}, open(os.path.join(base, '..-results.json'), 'w'))
open(os.path.join(d, '.ufo/waves/R47RevGR1a.md'), 'w').write(
    'ROW GR1 VERDICT: holds\nSECTION SHA256: ' + h + '\n'
    + 'Points at cmdline.c:147, vsprintf.c:86, kstrtox.c:29. ' + 'x' * 300 + '\n')
EOF
git -C "$D" add -A; git -C "$D" commit -qm d1; D1=$(git -C "$D" rev-parse HEAD)
python3 "$C" --lane "$D" --revision "$D1" | python3 -c '
import json,sys;d=json.load(sys.stdin)
print("waves_seen=",d["waves_seen"],"structural_ok=",d["structural_ok"])
print("GR1:",json.dumps(d["per_row"]["GR1"]["seats"]["R47RevGR1a"]))'
echo "--- does git resolve the escaped path at all? ---"
git -C "$D" show "$D1:.ufo/waves/round-47/../R47RevGR1a.md" >/dev/null 2>"$S/e.err"; echo "show rc=$? :: $(cat "$S/e.err")"
git -C "$D" show "$D1:.ufo/waves/round-47/x/R47RevGR1a.md" >/dev/null 2>&1; echo "control nested-path show rc=$?"
reset0
echo "=== E1 lane config cannot execute: core.fsmonitor canary ==="
rm -f "$S/canary.fired"
printf '#!/bin/sh\ntouch %s/canary.fired\nexit 0\n' "$S" > "$S/canary.sh"; chmod +x "$S/canary.sh"
git -C "$D" config core.fsmonitor "$S/canary.sh"
git -C "$D" config core.hooksPath "$S/hooks"
python3 "$C" --lane "$D" --revision "$R0" --section-hash >/dev/null 2>&1; echo "counter rc=$?"
[ -e "$S/canary.fired" ] && echo "CANARY FIRED (code execution)" || echo "canary not fired"
git -C "$D" config --unset core.fsmonitor; git -C "$D" config --unset core.hooksPath
echo "=== E2 repo identity is not pinned by -C: GIT_DIR override ==="
python3 "$C" --lane "$D" --revision "$R0" --section-hash | python3 -c 'import json,sys;print("clean env:",json.load(sys.stdin)["revision"])'
GIT_DIR=$S/probe/.git python3 "$C" --lane "$D" --revision "$R0" --section-hash 2>&1 | head -c 260; echo
echo "=== E3 subdir lane silently resolves to the enclosing repo toplevel ==="
python3 "$C" --lane "$D/.ufo/waves" --revision "$R0" --section-hash | python3 -c 'import json,sys;d=json.load(sys.stdin);print("revision",d["revision"],"structural_ok",d.get("structural_ok"))'
echo "=== E4 duplicate-key dispatch JSON (F3) ==="
python3 - "$D" <<'EOF'
import os, sys
d = sys.argv[1]
p = os.path.join(d, '.ufo/waves/round-47/w9-dispatch.json')
open(p, 'w').write('{"taskCall": {"tasks": [], "tasks": [{"name": "R47RevGR1a", "agent": "reviewer"}]}}')
EOF
git -C "$D" add -A; git -C "$D" commit -qm e4; E4=$(git -C "$D" rev-parse HEAD)
python3 "$C" --lane "$D" --revision "$E4" | python3 -c 'import json,sys;d=json.load(sys.stdin);print("waves_seen=",d["waves_seen"],"verdict=",d["verdict"])'
reset0
echo DONE
