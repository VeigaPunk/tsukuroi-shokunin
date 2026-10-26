#!/usr/bin/env bash
set -euo pipefail
S=/fast/scratch/hyaku/tsukuroi-r38/C1RevSharedState
H=$S/probe_harness.sh
UUID=11111111-2222-3333-4444-555555555555
mk() { d=$1; rm -rf "$d"; mkdir -p "$d"; }
st_write() { mkdir -p "${1%/*}"; printf 'write_errs %s\nread_errs %s\nflush_errs %s\ncorruption_errs %s\ngeneration_errs %s\n' "$2" "$3" "$4" "$5" "$6" > "$1"; }

echo "== T1: five counters, NO trailing newline on last line =="
mk "$S/t1"; st_write "$S/t1/btrfs/$UUID/devinfo/1/error_stats" 0 0 0 0 0
mkdir -p "$S/t1/btrfs/$UUID/devinfo/2"
printf "write_errs 0\nread_errs 0\nflush_errs 0\ncorruption_errs 0\ngeneration_errs 0" > "$S/t1/btrfs/$UUID/devinfo/2/error_stats"
TSUKUROI_BTRFS_SYSFS="$S/t1/btrfs" bash "$H" || echo "T1 rc=$?"

echo "== T2: root dir present but mode 000 (unsearchable) =="
mk "$S/t2"; st_write "$S/t2/btrfs/$UUID/devinfo/1/error_stats" 1 0 0 0 0
chmod 000 "$S/t2/btrfs/$UUID"
TSUKUROI_BTRFS_SYSFS="$S/t2/btrfs" bash "$H" || echo "T2 rc=$?"
chmod 755 "$S/t2/btrfs/$UUID"

echo "== T2b: root itself mode 000 =="
mk "$S/t2b"; st_write "$S/t2b/btrfs/$UUID/devinfo/1/error_stats" 1 0 0 0 0
chmod 000 "$S/t2b/btrfs"
TSUKUROI_BTRFS_SYSFS="$S/t2b/btrfs" bash "$H" || echo "T2b rc=$?"
chmod 755 "$S/t2b/btrfs"

echo "== T3: root path is a regular file =="
mk "$S/t3"; : > "$S/t3/btrfs"
TSUKUROI_BTRFS_SYSFS="$S/t3/btrfs" bash "$H" || echo "T3 rc=$?"

echo "== T4: empty error_stats file =="
mk "$S/t4"; mkdir -p "$S/t4/btrfs/$UUID/devinfo/1"; : > "$S/t4/btrfs/$UUID/devinfo/1/error_stats"
TSUKUROI_BTRFS_SYSFS="$S/t4/btrfs" bash "$H" || echo "T4 rc=$?"

echo "== T5: duplicate last line WITHOUT trailing newline =="
mk "$S/t5"; st_write "$S/t5/btrfs/$UUID/devinfo/1/error_stats" 0 0 0 0 0
printf 'read_errs 0' >> "$S/t5/btrfs/$UUID/devinfo/1/error_stats"
TSUKUROI_BTRFS_SYSFS="$S/t5/btrfs" bash "$H" || echo "T5 rc=$?"

echo "== T6: blank middle line =="
mk "$S/t6"; mkdir -p "$S/t6/btrfs/$UUID/devinfo/1"
printf 'write_errs 0\n\nread_errs 0\nflush_errs 0\ncorruption_errs 0\ngeneration_errs 0\n' > "$S/t6/btrfs/$UUID/devinfo/1/error_stats"
TSUKUROI_BTRFS_SYSFS="$S/t6/btrfs" bash "$H" || echo "T6 rc=$?"

echo "== T7: uppercase UUID dir =="
mk "$S/t7"; st_write "$S/t7/btrfs/11111111-2222-3333-4444-55555555555A/devinfo/1/error_stats" 5 0 0 0 0
TSUKUROI_BTRFS_SYSFS="$S/t7/btrfs" bash "$H" || echo "T7 rc=$?"

echo "== T8: CRLF line endings =="
mk "$S/t8"; mkdir -p "$S/t8/btrfs/$UUID/devinfo/1"
printf 'write_errs 0\r\nread_errs 0\r\nflush_errs 0\r\ncorruption_errs 0\r\ngeneration_errs 0\r\n' > "$S/t8/btrfs/$UUID/devinfo/1/error_stats"
TSUKUROI_BTRFS_SYSFS="$S/t8/btrfs" bash "$H" || echo "T8 rc=$?"

echo "== T9: read-EOF semantics with three vars (does read clear k on EOF?) =="
printf 'a 1' | { n=0; while IFS=' ' read -r k v extra || [ -n "${k:-}" ]; do n=$((n+1)); echo "iter$n k=[$k] v=[$v] extra=[${extra:-}]"; if [ "$n" -gt 3 ]; then echo LOOP-RUNAWAY; break; fi; done; echo "iterations=$n"; }

echo "== T10: read-EOF leaves k unchanged or clears it =="
k=PREV; printf 'a 1' | { IFS=' ' read -r k v extra; echo "rc-read1 k=[$k]"; IFS=' ' read -r k v extra || true; echo "after-EOF k=[$k] v=[${v:-UNSET}]"; }
