#!/usr/bin/env python3
"""Round-46 C1: build census variants from the base bytes (candidate K8 and the pre-data controls).
Usage: python3 make_c1_variant.py <variant> <base census file> <out file>
Variants: candidate | K1-constant | K2-pathhash | K3-nocases | K5-stderr | K6-grepc | K7-twolines | K9-noflagcheck
Every edit sits at or after the selftest's last check_cli case (census :3382 at base) or replaces a line in place
(usage :594, :605), so no line at or before :3383 moves (adjacency anchor IN-109 and sibling pins stay put)."""
import sys

USAGE_OLD = 'usage: tsukuroi-census.sh [--selftest] [--sample N] [--help]\n'
USAGE_NEW = 'usage: tsukuroi-census.sh [--selftest] [--sample N] [--identity] [--help]\n'
EXIT_OLD = 'Exit map:     0 HEALTHY | 1 DEGRADED | 2 BLOCKED (worst plane wins; usage errors also 2)\n'
EXIT_NEW = ('Exit map:     0 HEALTHY | 1 DEGRADED | 2 BLOCKED (worst plane wins; usage errors also 2); --identity '
            'alone prints one TSUKUROI_CENSUS_IDENTITY line naming the executed script bytes, exit 0, no host probe\n')
SELF_OLD = 'SELF=${BASH_SOURCE[0]}\n'
SELF_NEW = 'SELF=${BASH_SOURCE[0]:-}  # round 46 (C1): empty when the script is read from stdin (--identity: unverifiable)\n'

CASES_ANCHOR = ("  check_cli 'cli: --help prints usage and exits 0 (S10-2)' 0 \\\n"
                "    '^usage: tsukuroi-census\\.sh' -- --help\n")

CASES = r'''
  # ---- round 46 (C1): --identity, the one-command census identity (routed debt D12) ----
  # Expected values are computed here with sha256sum/md5sum/wc over the same file, never read
  # back from the identity line; the copy, symlink and stdin cases kill a constant writer and a
  # path hasher (a decoy regular file named `bash` sits in the stdin case's cwd).
  id_line() { # id_line FILE-FOR-EXPECTED -> the four byte fields as the identity prints them
    printf 'sha256=%s md5=%s bytes=%s lines=%s' "$(sha256sum < "$1" | cut -d' ' -f1)" \
      "$(md5sum < "$1" | cut -d' ' -f1)" "$(wc -c < "$1")" "$(wc -l < "$1")"
  }
  id_check() { # id_check LABEL WANT-FIELDS OUTPUT RC
    local label=$1 want=$2 out=$3 rc=$4 planes
    planes=$(grep -E "^  printf 'TSUKUROI_CENSUS: %s \(" "$SELF" | head -n1 | grep -oE '[a-z-]+=%s' | sed 's/=%s$//' | paste -sd, -)
    if [ "$rc" -ne 0 ]; then
      bad "$label: exit $rc wanted 0; output: $(printf '%s' "$out" | tr '\n' '|')"
    elif [ "$(printf '%s\n' "$out" | grep -c .)" -ne 1 ]; then
      bad "$label: wanted exactly one line; got: $(printf '%s' "$out" | tr '\n' '|')"
    elif [[ "$out" != "TSUKUROI_CENSUS_IDENTITY: version=$VERSION $want planes=$planes exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified="* ]]; then
      bad "$label: wanted '$want' planes=$planes; got: $out"
    else
      ok "$label (exit $rc)"
    fi
  }
  local idd id_out id_rc id_self_want id_copy_want id_abs
  id_abs=$(readlink -f -- "$SELF")
  idd="$work/identity"
  mkdir -p "$idd/dec"
  cp -- "$SELF" "$idd/copy.sh"
  printf '\n# r46 identity selftest copy\n' >> "$idd/copy.sh"   # the census ends without a newline
  ln -s -- "$id_abs" "$idd/link.sh"
  { cat -- "$SELF"; printf '# decoy\n'; } > "$idd/dec/bash"
  id_self_want=$(id_line "$SELF")
  id_copy_want=$(id_line "$idd/copy.sh")
  set +e
  id_out=$("$BASH" "$SELF" --identity 2>&1); id_rc=$?
  set -e
  id_check 'identity: one line naming this file, digests recomputed here, verified=yes (R46-C1)' \
    "$id_self_want" "$id_out" "$id_rc"
  [[ "$id_out" == *' verified=yes' ]] || bad 'identity: this file must read verified=yes (R46-C1)'
  set +e
  id_out=$("$BASH" "$idd/copy.sh" --identity 2>&1); id_rc=$?
  set -e
  if [ "$id_copy_want" = "$id_self_want" ]; then
    bad 'identity: a one-line copy must change every byte field (R46-C1)'
  else
    id_check 'identity: a copy with one appended line reports its own bytes, not a constant (R46-C1)' \
      "$id_copy_want" "$id_out" "$id_rc"
  fi
  set +e
  id_out=$("$BASH" "$idd/link.sh" --identity 2>&1); id_rc=$?
  set -e
  id_check 'identity: a symlink invocation reports the target file (R46-C1)' "$id_self_want" "$id_out" "$id_rc"
  set +e
  id_out=$(cd "$idd/dec" && "$BASH" -s -- --identity < "$id_abs" 2>&1); id_rc=$?
  set -e
  id_check 'identity: a script read from stdin prints unverifiable, never a decoy file named bash (R46-C1)' \
    'sha256=unverifiable md5=unverifiable bytes=unverifiable lines=unverifiable' "$id_out" "$id_rc"
  [[ "$id_out" == *' verified=no' ]] || bad 'identity: a stdin script must read verified=no (R46-C1)'
  { printf 'mv -f -- "$R46_DECOY" "$R46_PATH"\n'; cat -- "$SELF"; } > "$idd/repl.sh"
  { cat -- "$SELF"; printf '\n# decoy\n'; } > "$idd/repl.decoy"
  set +e
  id_out=$(R46_DECOY="$idd/repl.decoy" R46_PATH="$idd/repl.sh" "$BASH" "$idd/repl.sh" --identity 2>&1); id_rc=$?
  set -e
  id_check 'identity: a file replaced after bash opened it prints unverifiable, never the new bytes (R46-C1)' \
    'sha256=unverifiable md5=unverifiable bytes=unverifiable lines=unverifiable' "$id_out" "$id_rc"
  check_cli 'cli: --identity with another flag exits 2 (R46-C1)' 2 \
    '--identity takes no other argument' -- --identity --selftest
'''

FUNC_ANCHOR = '# ---- main --------------------------------------------------------------------\nmain() {\n'

FUNC = r'''# ---- --identity (round 46, C1): one-command census identity (routed debt D12) ---------
# Prints ONE line naming the bytes this bash process executes, so a reader re-derives the
# census revision with one command (closeout-r11.md D12: identity is by hash, not VERSION).
# The digests are read through the descriptor bash holds open on the script (bash opens the
# script file and moves it to a high descriptor, normally 255), re-opened as /proc/$$/fd/<n>,
# and only when that descriptor resolves to the same file as $SELF. A script read from stdin
# or from a pipe has no such descriptor: the four byte fields then print `unverifiable` and
# verified=no — a path is never hashed on trust. sha256 is taken again after the other
# fields; a change in between also reads unverifiable. Reads /proc and the script only;
# writes nothing; runs no plane probe. Exit 0.
CENSUS_PLANES='packages,systemd,drivers,journal,update-safety,oom'
census_identity() {
  local self_real fdp='' p sha md5 bytes lines sha2
  local f_sha=unverifiable f_md5=unverifiable f_bytes=unverifiable f_lines=unverifiable verified=no
  self_real=$(readlink -f -- "$SELF" 2>/dev/null || true)
  if [ -n "$self_real" ] && [ -f "$self_real" ]; then
    for p in "/proc/$$/fd/255" /proc/$$/fd/*; do
      case "${p##*/}" in '' | *[!0-9]*) continue ;; esac
      [ "${p##*/}" -ge 10 ] || continue
      [ -f "$p" ] || continue
      if [ "$(readlink -- "$p" 2>/dev/null || true)" = "$self_real" ]; then fdp=$p; break; fi
    done
  fi
  if [ -n "$fdp" ]; then
    sha=$(sha256sum < "$fdp" 2>/dev/null | cut -d' ' -f1 || true)
    md5=$(md5sum < "$fdp" 2>/dev/null | cut -d' ' -f1 || true)
    bytes=$(wc -c < "$fdp" 2>/dev/null || true)
    lines=$(wc -l < "$fdp" 2>/dev/null || true)
    sha2=$(sha256sum < "$fdp" 2>/dev/null | cut -d' ' -f1 || true)
    if [[ "$sha" =~ ^[0-9a-f]{64}$ && "$md5" =~ ^[0-9a-f]{32}$ && "$bytes" =~ ^[0-9]+$ \
      && "$lines" =~ ^[0-9]+$ && "$sha2" = "$sha" ]]; then
      f_sha=$sha f_md5=$md5 f_bytes=$bytes f_lines=$lines verified=yes
    fi
  fi
  printf 'TSUKUROI_CENSUS_IDENTITY: version=%s sha256=%s md5=%s bytes=%s lines=%s planes=%s exit_map=%s verified=%s\n' \
    "$VERSION" "$f_sha" "$f_md5" "$f_bytes" "$f_lines" "$CENSUS_PLANES" '0:HEALTHY,1:DEGRADED,2:BLOCKED' "$verified"
}

'''

PARSE_OLD = '''main() {
  local selftest=0
  while [ $# -gt 0 ]; do
    case "$1" in
      --selftest) selftest=1; shift ;;
'''
PARSE_NEW = '''main() {
  local selftest=0 identity=0 nargs=$#
  while [ $# -gt 0 ]; do
    case "$1" in
      --identity) identity=1; shift ;;
      --selftest) selftest=1; shift ;;
'''
DISPATCH_OLD = '''  if [ "$selftest" -eq 1 ]; then
    run_selftest
    return
  fi
'''
DISPATCH_NEW = '''  if [ "$identity" -eq 1 ]; then # round 46 (C1): --identity stands alone, before any probe
    if [ "$nargs" -ne 1 ]; then
      printf 'tsukuroi-census: --identity takes no other argument\\n' >&2; usage >&2; exit 2
    fi
    census_identity
    exit 0
  fi

  if [ "$selftest" -eq 1 ]; then
    run_selftest
    return
  fi
'''


def sub(text, old, new, label):
    if text.count(old) != 1:
        sys.exit(f'anchor {label} found {text.count(old)} times')
    return text.replace(old, new)


def build(variant, base):
    t = base
    t = sub(t, USAGE_OLD, USAGE_NEW, 'usage')
    t = sub(t, EXIT_OLD, EXIT_NEW, 'exitmap')
    t = sub(t, SELF_OLD, SELF_NEW, 'self')
    func = FUNC
    cases = CASES
    parse_new, dispatch_new = PARSE_NEW, DISPATCH_NEW
    if variant == 'K1-constant':  # prints the base file's real digests as constants
        func = func.replace('verified=yes\n    fi\n  fi\n',
                            'verified=yes\n    fi\n  fi\n  f_sha=@SHA@ f_md5=@MD5@ f_bytes=@BYTES@ f_lines=@LINES@ verified=yes\n')
    elif variant == 'K2-pathhash':  # hashes the $SELF path on trust (no descriptor check)
        func = func.replace('  if [ -n "$fdp" ]; then\n', '  [ -n "$self_real" ] && [ -f "$self_real" ] && fdp=$self_real\n  if [ -n "$fdp" ]; then\n')
    elif variant == 'K3-nocases':  # correct identity, no selftest cases
        cases = ''
    elif variant == 'K5-stderr':  # identity line on stderr
        func = func.replace("verified=%s\\n' \\\n", "verified=%s\\n' >&2 \\\n")
    elif variant == 'K6-grepc':  # counts non-empty lines instead of newline bytes
        func = func.replace('lines=$(wc -l < "$fdp" 2>/dev/null || true)', 'lines=$(grep -c . < "$fdp" 2>/dev/null || true)')
    elif variant == 'K7-twolines':  # a banner line before the identity line
        func = func.replace("  printf 'TSUKUROI_CENSUS_IDENTITY:", "  printf 'tsukuroi-census identity\\n'\n  printf 'TSUKUROI_CENSUS_IDENTITY:")
    elif variant == 'K9-noflagcheck':  # --identity silently wins over other flags
        dispatch_new = dispatch_new.replace('    if [ "$nargs" -ne 1 ]; then\n', '    if false; then\n')
    elif variant != 'candidate':
        sys.exit(f'unknown variant {variant}')
    t = sub(t, CASES_ANCHOR, CASES_ANCHOR + cases, 'cases')
    t = sub(t, FUNC_ANCHOR, func + FUNC_ANCHOR, 'func')
    t = sub(t, PARSE_OLD, parse_new, 'parse')
    t = sub(t, DISPATCH_OLD, dispatch_new, 'dispatch')
    return t


if __name__ == '__main__':
    variant, src, out = sys.argv[1:4]
    base = open(src, encoding='utf-8').read()
    text = build(variant, base)
    if variant == 'K1-constant':
        import hashlib
        b = base.encode()
        text = (text.replace('@SHA@', hashlib.sha256(b).hexdigest()).replace('@MD5@', hashlib.md5(b).hexdigest())
                .replace('@BYTES@', str(len(b))).replace('@LINES@', str(b.count(b'\n'))))
    open(out, 'w', encoding='utf-8').write(text)
