#!/usr/bin/env bash
# C-experiments under in-situ conditions: -u -o pipefail (as census :423/:1946)
S=/fast/scratch/hyaku/tsukuroi-r42/C1RevIntegration
cd "$S/exp" || exit 9
big_out=$( { printf 'PATTERN-IS-PRESENT on line one\n'; awk 'BEGIN { for (i=0;i<60000;i++) printf "filler line %06d\n", i }'; } )
echo "D0 big_out bytes: ${#big_out}"

export PIPESTATUS_IGNORED=
old_absent() (
  set -u -o pipefail
  local out=$1
  if printf '%s\n' "$out" | grep -qE -- 'PATTERN-IS-PRESENT'; then echo "OLD:present"; else echo "OLD:absent"; fi
)
new_absent() (
  set -u -o pipefail
  local out=$1
  if grep -qE -- 'PATTERN-IS-PRESENT' <<<"$out"; then echo "NEW:present"; else echo "NEW:absent"; fi
)
po=0; pa=0
for k in $(seq 1 20); do r=$(old_absent "$big_out"); [ "$r" = "OLD:absent" ] && pa=$((pa+1)); [ "$r" = "OLD:present" ] && po=$((po+1)); done
echo "D1 old form+pipefail, 20 runs, 1.1MiB out, pattern line 1: present=$po absent=$pa (absent=fail-open)"
echo "D2 new form+pipefail, same input: $(new_absent "$big_out")"

echo "D3 old form+pipefail, pattern truly absent, small out: $(old_absent 'nothing here')"
echo "D4 new form+pipefail, pattern truly absent, small out: $(new_absent 'nothing here')"

echo "--- D5: big here-string WITH pattern, TMPDIR unusable (nonexistent) ---"
cat > d5.sh <<'EOF'
set -u -o pipefail
big=$( { printf 'PATTERN-IS-PRESENT on line one\n'; awk 'BEGIN { for (i=0;i<60000;i++) printf "filler line %06d\n", i }'; } )
export TMPDIR
if grep -qE -- 'PATTERN-IS-PRESENT' <<<"$big"; then echo "VERDICT:present(correct)"; else echo "VERDICT:absent(FAIL-OPEN)"; fi
EOF
TMPDIR=/nonexistent-c1rev bash d5.sh 2>&1 | head -5

echo "--- D6: deterministic — TMPDIR on a 64KiB tmpfs (private unshare -rm), 1.1MiB here-string with pattern ---"
cat > d6-inner.sh <<'EOF'
set -u -o pipefail
mkdir -p /tmp/tiny
mount -t tmpfs -o size=64k tmpfs /tmp/tiny || { echo "mount failed"; exit 9; }
big=$( { printf 'PATTERN-IS-PRESENT on line one\n'; awk 'BEGIN { for (i=0;i<60000;i++) printf "filler line %06d\n", i }'; } )
export TMPDIR=/tmp/tiny
if grep -qE -- 'PATTERN-IS-PRESENT' <<<"$big"; then echo "VERDICT:present(correct)"; else echo "VERDICT:absent(FAIL-OPEN)"; fi
EOF
unshare -rm bash d6-inner.sh 2>&1 | head -6
echo "--- D7: control — same but small here-string on the tiny tmpfs ---"
cat > d7-inner.sh <<'EOF'
set -u -o pipefail
mkdir -p /tmp/tiny
mount -t tmpfs -o size=64k tmpfs /tmp/tiny || { echo "mount failed"; exit 9; }
big='PATTERN-IS-PRESENT small'
export TMPDIR=/tmp/tiny
if grep -qE -- 'PATTERN-IS-PRESENT' <<<"$big"; then echo "VERDICT:present(correct)"; else echo "VERDICT:absent(FAIL-OPEN)"; fi
EOF
unshare -rm bash d7-inner.sh 2>&1 | head -6
echo "--- D8: control — no tmpfs, normal TMPDIR, big here-string with pattern ---"
bash d5.sh 2>&1 | head -3
