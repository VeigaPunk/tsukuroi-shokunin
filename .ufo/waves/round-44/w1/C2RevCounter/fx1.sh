#!/bin/bash
# C2RevCounter-6 fixture experiments on check-scrub-record-r44.py
set -u
S=/fast/scratch/hyaku/tsukuroi-r44/C2RevCounter-6
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
IMPL=7e081698d4fc3c4ea944884fd093058de9909de1
C="$L/tools/check-scrub-record-r44.py"
D="$S/fx1"

rm -rf "$D"
git clone -q --shared "$L" "$D" || exit 1
git -C "$D" remote remove origin
[ "$(git -C "$D" rev-parse --show-toplevel)" = "$D" ] || { echo FATAL-top; exit 1; }
git -C "$D" checkout -q --detach "$IMPL"

cm() { git -C "$D" add -A >/dev/null; git -C "$D" -c user.name=fixture -c user.email=fixture@invalid commit -q -m "$1"; git -C "$D" rev-parse --short=12 HEAD; }

run() {
  python3 "$C" --lane "$D" --revision "$2" > "$S/out-$1.json"
  local ec=$?
  echo "== $1 exit=$ec rev=$2"
  python3 -c '
import json,sys
d=json.load(open(sys.argv[1]))
keys=("rows","quotes_ok","props_ok","host_ok","sources_ok","verdicts_ok","novelty_base_hits","pointer_ok","verdict")
print(" ", {k:d[k] for k in keys})
r=d["per_row"]["SR7"]; s=d["sources"]
print("  SR7:", r.get("verdicts"), "verdict_ok" if r.get("verdict_ok") else "NOT-OK", r.get("quotes"))
print("  srcS242:", s.get("S242"), "srcS245:", s.get("S245"))
' "$S/out-$1.json"
}

W="$D/.ufo/waves/round-44"
mkdir -p "$W/w2"

# c1: positive binding — both SR7 seats hold, critic output is JSON verdict_line+verdict agreeing
printf '%s\n' '{"taskCall":{"tasks":[{"name":"C2RevSR7","agent":"reviewer"},{"name":"C2CritSR7","agent":"critic"},{"name":"C2RevSR8","agent":"reviewer"},{"name":"C2CritSR8","agent":"critic"},{"name":"C2RevSR9","agent":"reviewer"},{"name":"C2CritSR9","agent":"critic"}]}}' > "$W/w2-dispatch.json"
printf '%s\n' '{"results":[{"name":"C2RevSR7","agent":"reviewer","output":"ROW SR7 VERDICT: holds"},{"name":"C2CritSR7","agent":"critic","output":"{\"verdict_line\": \"ROW SR7 VERDICT: holds\", \"verdict\": \"holds\"}"}]}' > "$W/w2-results.json"
printf '%s\n' 'ROW SR7 VERDICT: holds' > "$W/w2/C2RevSR7.md"
printf '%s\n' 'ROW SR7 VERDICT: holds' > "$W/w2/C2CritSR7.md"
R1=$(cm "c1 positive binding SR7")
run c1 "$R1"

# c2: contradictory JSON verdict (verdict_line says holds, verdict says fails)
printf '%s\n' '{"results":[{"name":"C2RevSR7","agent":"reviewer","output":"ROW SR7 VERDICT: holds"},{"name":"C2CritSR7","agent":"critic","output":"{\"verdict_line\": \"ROW SR7 VERDICT: holds\", \"verdict\": \"fails\"}"}]}' > "$W/w2-results.json"
R2=$(cm "c2 contradictory verdict key")
run c2 "$R2"

# c3: report first line differs from bound output line
printf '%s\n' '{"results":[{"name":"C2RevSR7","agent":"reviewer","output":"ROW SR7 VERDICT: holds"},{"name":"C2CritSR7","agent":"critic","output":"{\"verdict_line\": \"ROW SR7 VERDICT: holds\", \"verdict\": \"holds\"}"}]}' > "$W/w2-results.json"
printf '%s\n' 'ROW SR7 VERDICT: partly' > "$W/w2/C2CritSR7.md"
R3=$(cm "c3 report first line differs")
run c3 "$R3"

# c4: raw output with leading blank line (JSON-unparseable, first line empty)
printf '%s\n' 'ROW SR7 VERDICT: holds' > "$W/w2/C2CritSR7.md"
printf '%s\n' '{"results":[{"name":"C2RevSR7","agent":"reviewer","output":"\nROW SR7 VERDICT: holds"},{"name":"C2CritSR7","agent":"critic","output":"{\"verdict_line\": \"ROW SR7 VERDICT: holds\", \"verdict\": \"holds\"}"}]}' > "$W/w2-results.json"
R4=$(cm "c4 blank-line-prefixed raw output")
run c4 "$R4"

# c5: quote text gutted to a substring still on the same snapshot line
printf '%s\n' '{"results":[{"name":"C2RevSR7","agent":"reviewer","output":"ROW SR7 VERDICT: holds"},{"name":"C2CritSR7","agent":"critic","output":"{\"verdict_line\": \"ROW SR7 VERDICT: holds\", \"verdict\": \"holds\"}"}]}' > "$W/w2-results.json"
python3 - "$D/corpus/knowledge/btrfs-scrub-record-r44.md" <<'PYEOF'
import sys
p = sys.argv[1]
s = open(p).read()
old = '**Quote.** `S243` sysfs.c:2044: "return -EINVAL;"'
new = '**Quote.** `S243` sysfs.c:2044: "n"'
assert old in s, "marker not found"
open(p, "w").write(s.replace(old, new))
PYEOF
R5=$(cm "c5 gutted quote substring")
run c5 "$R5"
git -C "$D" checkout -q HEAD~1 -- corpus/knowledge/btrfs-scrub-record-r44.md

# c6: doctored duplicate S242 row appended (used-by drops the entry)
python3 - "$D/corpus/SOURCES.md" <<'PYEOF'
import sys
p = sys.argv[1]
lines = open(p).read().splitlines(keepends=True)
rows = [l for l in lines if l.startswith('| S242 ')]
assert len(rows) == 1, len(rows)
row = rows[0]
parts = row.split('|')
assert len(parts) == 13, len(parts)
assert 'btrfs-scrub-record-r44.md' in parts[11], parts[11]
parts[11] = ' corpus/knowledge/btrfs-scrub-record-r43.md '
new = '|' + '|'.join(parts[1:]).rstrip('\n') + '\n'
open(p, "a").write(new)
open(p + '.orig-row', 'w').write(row)
PYEOF
R6=$(cm "c6 doctored duplicate S242 row")
run c6 "$R6"

# c7: append the ORIGINAL row again — last duplicate wins
cat "$D/corpus/SOURCES.md.orig-row" >> "$D/corpus/SOURCES.md"
R7=$(cm "c7 original row appended last")
run c7 "$R7"

# bogus revision on the real lane
python3 "$C" --revision deadbeef00deadbeef00deadbeef00deadbeef00 --lane "$L" > "$S/out-bogus.json" 2>&1
echo "bogus_exit=$?"
cat "$S/out-bogus.json"
echo

# fx2: orphan repo with no shared history — fabricated wave-2 records for all rows
F="$S/fx2"
rm -rf "$F"
git init -q "$F"
[ "$(git -C "$F" rev-parse --show-toplevel)" = "$F" ] || { echo FATAL-top2; exit 1; }
mkdir -p "$F/corpus/knowledge" "$F/.ufo/waves/round-42/frozen/src" "$F/.ufo/waves/round-43/frozen/src" "$F/.ufo/waves/round-44/frozen/src" "$F/.ufo/waves/round-44/frozen/hostcap" "$F/.ufo/waves/round-44/w2"
cp "$S/entry-impl.md" "$F/corpus/knowledge/btrfs-scrub-record-r44.md"
cp "$S/old-impl.md" "$F/corpus/knowledge/btrfs-scrub-record-r43.md"
cp "$S/sources-impl.md" "$F/corpus/SOURCES.md"
cp "$S/snap-r42/scrub.c" "$F/.ufo/waves/round-42/frozen/src/scrub.c"
cp "$S/snap/ioctl.c" "$F/.ufo/waves/round-43/frozen/src/ioctl.c"
cp "$S/snap/scrub.c" "$S/snap/sysfs.c" "$S/snap/btrfs-scrub@.timer" "$S/snap/btrfs-scrub@.service" "$S/snap/PKGBUILD" "$F/.ufo/waves/round-44/frozen/src/"
cp "$S/snap/capture.txt" "$F/.ufo/waves/round-44/frozen/hostcap/"
python3 - "$F/.ufo/waves/round-44" <<'PYEOF'
import json, sys, os
w = sys.argv[1]
tasks, results = [], []
for n in ("7", "8", "9"):
    for nm, role in ((f"C2RevSR{n}", "reviewer"), (f"C2CritSR{n}", "critic")):
        tasks.append({"name": nm, "agent": role})
        results.append({"name": nm, "agent": role, "output": f"ROW SR{n} VERDICT: holds"})
    open(os.path.join(w, "w2", f"C2RevSR{n}.md"), "w").write(f"ROW SR{n} VERDICT: holds\n")
    open(os.path.join(w, "w2", f"C2CritSR{n}.md"), "w").write(f"ROW SR{n} VERDICT: holds\n")
json.dump({"taskCall": {"tasks": tasks}}, open(os.path.join(w, "w2-dispatch.json"), "w"))
json.dump({"results": results}, open(os.path.join(w, "w2-results.json"), "w"))
PYEOF
git -C "$F" add -A
git -C "$F" -c user.name=fixture -c user.email=fixture@invalid commit -q -m "orphan fabricated round-44 lane"
python3 "$C" --lane "$F" --revision HEAD > "$S/out-fx2.json"
echo "fx2_exit=$?"
cat "$S/out-fx2.json"
echo
echo DONE
