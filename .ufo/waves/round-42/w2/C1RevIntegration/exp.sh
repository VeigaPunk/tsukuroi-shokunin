#!/usr/bin/env bash
# C1RevIntegration micro-experiments for F-7 (round 42 w2). Run under bash.
S=/fast/scratch/hyaku/tsukuroi-r42/C1RevIntegration
mkdir -p "$S/exp"
cd "$S/exp" || exit 9

echo "=== A. hunk-1: awk error test vs old grep form (both under set -euo pipefail) ==="
# OLD condition+note (as at 447662088), NEW condition+note (as at 78abb8b)
old_eval() { # -> prints "BLOCK <note>" or "PASS"
  local s_out=$1
  if grep -q '^error:' <<<"$s_out"; then
    printf 'BLOCK %s' "$(grep -m1 '^error:' <<<"$s_out")"
  else
    printf 'PASS'
  fi
}
new_eval() {
  local s_out=$1 err_line=''
  set -euo pipefail
  if err_line=$(printf '%s\n' "$s_out" | awk '/^error:/ { if (!p) { print; p = 1 } } END { if (!p) exit 1 }'); then
    printf 'BLOCK %s' "$err_line"
  else
    printf 'PASS'
  fi
}
mk_noise() { awk -v n="$1" 'BEGIN { for (i=0;i<n;i++) printf "package/foo %d total files, 0 altered\n", i }'; }

i=0
run_case() { # label, input-string
  local label=$1 input=$2 o n
  i=$((i+1))
  o=$(old_eval "$input"); n=$(new_eval "$input")
  if [ "$o" = "$n" ]; then echo "A$i $label: SAME [$o]"; else echo "A$i $label: DIFF old=[$o] new=[$n]"; fi
}
run_case "no-error"            "$(printf 'foo: 1 total files, 0 altered\nbar: 2 total files, 0 altered\n')"
run_case "empty"               ""
run_case "error-first"         "$(printf 'error: package x is damaged\nfoo: 1 total files\n')"
run_case "error-mid"           "$(printf 'ok line\nerror: second thing\nmore\n')"
run_case "error-last-of-two"   "$(printf 'x\nerror: one\ntail\nerror: two\n')"
run_case "only-newline"        "$(printf '\n')"
# CR form AFTER the census' own tr '\r' '\n' normalization (that tr is at :686, pre-existing)
run_case "post-tr CR-prefixed" "$(printf '\r\nerror: after CR split\n')"
run_case "long-then-error"     "$(printf 'error: deep one\n'; mk_noise 12000)"   # error first + ~350KB noise
run_case "noise-then-error"    "$(mk_noise 12000; printf 'error: late one\n')"   # ~350KB noise, error at end
# NUL input — known mechanism difference between grep and awk, verdict must still agree
inp=$'error: nul\x00here\n'
o=$(old_eval "$inp"); n=$(new_eval "$inp")
echo "A9 NUL: old=[$o]"; echo "A9 NUL: new=[$n]"

echo
echo "=== B. hunk-2: bn lookup — duplicate names and the big-baseline SIGPIPE kill ==="
# B1 duplicate-name first-wins equivalence
base_dup=$(printf 'alpha 1.0-1\nbeta 2.0-1\nalpha 9.9-9\n')
ob=$(printf '%s\n' "$base_dup" | awk -v n="alpha" '$1 == n {print $2; exit}')
nb=$(printf '%s\n' "$base_dup" | awk -v n="alpha" '$1 == n && !f { print $2; f = 1 }')
echo "B1 dup-first-wins: old=[$ob] new=[$nb] same=$([ "$ob" = "$nb" ] && echo yes || echo NO)"
# B2 no-match: both empty
ob=$(printf '%s\n' "$base_dup" | awk -v n="ghost" '$1 == n {print $2; exit}')
nb=$(printf '%s\n' "$base_dup" | awk -v n="ghost" '$1 == n && !f { print $2; f = 1 }')
echo "B2 nomatch: old=[$ob] new=[$nb] same=$([ "$ob" = "$nb" ] && echo yes || echo NO)"
# B3 large baseline, early match: does the OLD form kill a set -euo pipefail script?
{ printf 'alpha 1.1-1\n'; awk 'BEGIN { for (i=0;i<4000;i++) printf "extra/pad%05d 1.0-2\n", i }'; } > big_base.txt
wc -c big_base.txt
cat > b3old.sh <<'EOF'
set -euo pipefail
base_txt=$(cat big_base.txt)
bn=$(printf '%s\n' "$base_txt" | awk -v n="alpha" '$1 == n {print $2; exit}')
echo "survived bn=[$bn]"
EOF
cat > b3new.sh <<'EOF'
set -euo pipefail
base_txt=$(cat big_base.txt)
bn=$(printf '%s\n' "$base_txt" | awk -v n="alpha" '$1 == n && !f { print $2; f = 1 }')
echo "survived bn=[$bn]"
EOF
for v in old new; do
  if out=$(bash "b3$v.sh" 2>&1); then st=0; else st=$?; fi
  echo "B3 $v: exit=$st out=[$out]"
done
# B4 late match on the big baseline (worst case for the NEW form: full read, correct value)
bn=$(printf '%s\n' "$(cat big_base.txt)" | awk -v n="extra/pad03999" '$1 == n && !f { print $2; f = 1 }')
echo "B4 new late-match: bn=[$bn]"

echo
echo "=== C. hunk-3: ABSENT arm — old pipe vs new here-string ==="
big_out=$( { printf 'PATTERN-IS-PRESENT on line one\n'; awk 'BEGIN { for (i=0;i<60000;i++) printf "filler line %06d\n", i }'; } )
echo "C0 big_out bytes: ${#big_out}"
old_absent() { # returns 0 (and prints OLD:absent) when the old form reports absent
  local out=$1
  if printf '%s\n' "$out" | grep -qE -- 'PATTERN-IS-PRESENT'; then echo "OLD:present"; else echo "OLD:absent"; fi
}
new_absent() {
  local out=$1
  if grep -qE -- 'PATTERN-IS-PRESENT' <<<"$out"; then echo "NEW:present"; else echo "NEW:absent"; fi
}
po=0; pa=0
for k in $(seq 1 20); do r=$(old_absent "$big_out"); [ "$r" = "OLD:absent" ] && pa=$((pa+1)); [ "$r" = "OLD:present" ] && po=$((po+1)); done
echo "C1 old form over 20 runs (1MiB, pattern line 1): present=$po absent=$pa (absent = fail-open)"
echo "C2 new form same input: $(new_absent "$big_out")"
small_out='nothing to see here'
echo "C3 small out, pattern truly absent: old=$(old_absent "$small_out") new=$(new_absent "$small_out")"
echo
echo "--- C4: TMPDIR failure (bash temp file for >64KiB here-strings) ---"
cat > c4.sh <<'EOF'
out=$(awk 'BEGIN { for (i=0;i<60000;i++) printf "filler line %06d\n", i }')
export TMPDIR
if grep -qE -- 'NEVER-PRESENT' <<<"$out"; then echo "NEW:present"; else echo "NEW:absent"; fi
echo "grep-status=$?"
EOF
echo "C4 big here-string, TMPDIR=/nonexistent-c1rev:"
TMPDIR=/nonexistent-c1rev bash c4.sh 2>&1 | head -4
cat > c4s.sh <<'EOF'
out='small buffer'
export TMPDIR
if grep -qE -- 'NEVER-PRESENT' <<<"$out"; then echo "SMALL:present"; else echo "SMALL:absent"; fi
EOF
echo "C5 small here-string, same broken TMPDIR:"
TMPDIR=/nonexistent-c1rev bash c4s.sh 2>&1 | head -4
echo "C6 old pipe form, big buffer, same broken TMPDIR (no temp file needed for a pipe):"
cat > c6.sh <<'EOF'
out=$(awk 'BEGIN { for (i=0;i<60000;i++) printf "filler line %06d\n", i }')
export TMPDIR
if printf '%s\n' "$out" | grep -qE -- 'NEVER-PRESENT'; then echo "OLDPIPE:present"; else echo "OLDPIPE:absent"; fi
EOF
TMPDIR=/nonexistent-c1rev bash c6.sh 2>&1 | head -4
