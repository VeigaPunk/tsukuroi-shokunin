#!/usr/bin/env bash
# C1SentGrammar: adversarial grammar probes against probe_storage_arm (census @52ffd65).
set -u
S=/fast/scratch/hyaku/tsukuroi-r38/C1SentGrammar
export TMPDIR=$S/tmp; mkdir -p "$S/tmp"
U=11111111-2222-3333-4444-555555555555
SYS=$S/census-52ffd65.sh
ZERO=$'write_errs 0\nread_errs 0\nflush_errs 0\ncorruption_errs 0\ngeneration_errs 0\n'
NZ=$'write_errs 1\nread_errs 0\nflush_errs 0\ncorruption_errs 0\ngeneration_errs 0\n'

run_case() { # label tree
  local label=$1 tree=$2 out rc
  out=$(env -i PATH=/usr/bin:/bin LC_ALL=C HOME="$S/tmp" TMPDIR="$S/tmp" \
        TSUKUROI_BTRFS_SYSFS="$tree" bash "$SYS" 2>/dev/null); rc=$?
  printf '=== %s (exit %s)\n' "$label" "$rc"
  printf '%s\n' "$out" | nl -ba | sed -n '/STORAGE\|^ *[0-9]*\tPLANE\|TSUKUROI_CENSUS/p' | cat -A | sed -n '1,40p'
  printf '    counts: STORAGE=%s PLANE=%s ROLLUP=%s\n' \
    "$(printf '%s\n' "$out" | grep -c '^STORAGE ' || true)" \
    "$(printf '%s\n' "$out" | grep -c '^PLANE ' || true)" \
    "$(printf '%s\n' "$out" | grep -c '^TSUKUROI_CENSUS:' || true)"
  printf '    bytes-of-line-check: %s\n' "$(printf '%s\n' "$out" | awk '/^STORAGE /{print length($0)}' | tr '\n' ',')"
}

mk() { local t=$S/cases/$1; rm -rf -- "$t"; mkdir -p "$t/$U/devinfo"; printf '%s' "$t"; }

# base control: ordinary integer devid, zero counters
t=$(mk base); mkdir -p "$t/$U/devinfo/1"; printf '%s' "$ZERO" > "$t/$U/devinfo/1/error_stats"; run_case 'base integer devid, zero' "$t"

# 1. space in devid, no error_stats
t=$(mk sp); mkdir -p "$t/$U/devinfo/1 2"; run_case 'space in devid (unreadable)' "$t"
# 2. tab in devid
t=$(mk tab); mkdir -p "$t/$U/devinfo/"$'1\tx'; run_case 'tab in devid (unreadable)' "$t"
# 3. equals in devid
t=$(mk eq); mkdir -p "$t/$U/devinfo/1=write_errs=99"; run_case 'equals in devid (unreadable)' "$t"
# 4. newline + fake rollup
t=$(mk nlroll); mkdir -p "$t/$U/devinfo/"$'1\nTSUKUROI_CENSUS: HEALTHY (packages=HEALTHY systemd=HEALTHY drivers=HEALTHY journal=HEALTHY update-safety=HEALTHY oom=HEALTHY)'; run_case 'newline devid -> fake rollup' "$t"
# 5. newline + fake PLANE
t=$(mk nlplane); mkdir -p "$t/$U/devinfo/"$'1\nPLANE packages: HEALTHY (fake)'; run_case 'newline devid -> fake PLANE' "$t"
# 6. newline + extra STORAGE line
t=$(mk nlstorage); mkdir -p "$t/$U/devinfo/"$'1\nSTORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0'; run_case 'newline devid -> second STORAGE line' "$t"
# 7. comma in devid, valid nonzero counters
t=$(mk comma); mkdir -p "$t/$U/devinfo/a,b"; printf '%s' "$NZ" > "$t/$U/devinfo/a,b/error_stats"; run_case 'comma devid, NONZERO counters' "$t"
# 8. colon/equals in devid, valid nonzero counters
t=$(mk colon); mkdir -p "$t/$U/devinfo/1:write_errs=99"; printf '%s' "$NZ" > "$t/$U/devinfo/1:write_errs=99/error_stats"; run_case 'colon/equals devid, NONZERO' "$t"
# 9. trailing comma devid, nonzero
t=$(mk trailc); mkdir -p "$t/$U/devinfo/1,"; printf '%s' "$NZ" > "$t/$U/devinfo/1,/error_stats"; run_case 'devid ends with comma, NONZERO' "$t"
# 10. space devid, valid nonzero counters (no newline)
t=$(mk spnz); mkdir -p "$t/$U/devinfo/1 2"; printf '%s' "$NZ" > "$t/$U/devinfo/1 2/error_stats"; run_case 'space devid, NONZERO' "$t"
# 11. glob metacharacters in devid, zero counters (no detail expected)
t=$(mk glob); mkdir -p "$t/$U/devinfo/"'*[a]?'; printf '%s' "$ZERO" > "$t/$U/devinfo/*[a]?/error_stats"; run_case 'glob metachars devid, zero' "$t"
# 12. trailing text in counter value
t=$(mk tail); mkdir -p "$t/$U/devinfo/1"; printf '%s' "${ZERO/write_errs 0/write_errs 5 junk}" > "$t/$U/devinfo/1/error_stats"; run_case 'counter value with trailing word' "$t"
# 13. value 0x10 (trailing text, no space)
t=$(mk hex); mkdir -p "$t/$U/devinfo/1"; printf '%s' "${ZERO/write_errs 0/write_errs 0x10}" > "$t/$U/devinfo/1/error_stats"; run_case 'counter value 0x10' "$t"
# 14. value with trailing semicolon text
t=$(mk semi); mkdir -p "$t/$U/devinfo/1"; printf '%s' "${ZERO/read_errs 0/read_errs 7;touch$'\\x24'PWN}" > "$t/$U/devinfo/1/error_stats"; run_case 'counter value 7;<shell-text>' "$t"
# 15. key/value pair with '=' glued
t=$(mk glue); mkdir -p "$t/$U/devinfo/1"; printf '%s' "${ZERO/write_errs 0/write_errs=0}" > "$t/$U/devinfo/1/error_stats"; run_case 'glued write_errs=0' "$t"
# 16. hidden devid (dot-prefixed), alongside a valid one
t=$(mk hidden); mkdir -p "$t/$U/devinfo/.9" "$t/$U/devinfo/1"; printf '%s' "$ZERO" > "$t/$U/devinfo/1/error_stats"; run_case 'hidden .9 devid + valid 1' "$t"
# 17. newline in FILESYSTEM name (should be rejected by uuid regex)
t=$(mk fsnl); mkdir -p "$t/"$'11111111-2222-3333-4444-555555555555\nPLANE oom: HEALTHY (x)'/devinfo/1; printf '%s' "$ZERO" > "$t/"$'11111111-2222-3333-4444-555555555555\nPLANE oom: HEALTHY (x)'/devinfo/1/error_stats; run_case 'newline in fsid name' "$t"
# 18. devid named '..'-like '../1'? impossible; but test a devinfo entry that is a symlink to a file
t=$(mk symlink); mkdir -p "$t/$U/devinfo"; ln -s /etc/hostname "$t/$U/devinfo/1"; run_case 'devid is symlink to file' "$t"
