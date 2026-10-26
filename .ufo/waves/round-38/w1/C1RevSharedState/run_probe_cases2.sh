#!/usr/bin/env bash
set -euo pipefail
S=/fast/scratch/hyaku/tsukuroi-r38/C1RevSharedState
H=$S/probe_harness.sh
UUID=11111111-2222-3333-4444-555555555555
mk() { d=$1; rm -rf "$d"; mkdir -p "$d"; }
st_write() { mkdir -p "${1%/*}"; printf 'write_errs %s\nread_errs %s\nflush_errs %s\ncorruption_errs %s\ngeneration_errs %s\n' "$2" "$3" "$4" "$5" "$6" > "$1"; }

echo "== T11: extra third field on a counter line =="
mk "$S/t11"; st_write "$S/t11/btrfs/$UUID/devinfo/1/error_stats" 0 0 0 0 0
printf 'flush_errs 0 junk\n' >> "$S/t11/btrfs/$UUID/devinfo/1/error_stats"
TSUKUROI_BTRFS_SYSFS="$S/t11/btrfs" bash "$H" || echo "T11 rc=$?"

echo "== T12: devinfo dir itself unreadable =="
mk "$S/t12"; st_write "$S/t12/btrfs/$UUID/devinfo/1/error_stats" 0 0 0 0 0
chmod 000 "$S/t12/btrfs/$UUID/devinfo"
TSUKUROI_BTRFS_SYSFS="$S/t12/btrfs" bash "$H" || echo "T12 rc=$?"
chmod 755 "$S/t12/btrfs/$UUID/devinfo"

echo "== T13: error_stats unreadable (mode 000 file) =="
mk "$S/t13"; st_write "$S/t13/btrfs/$UUID/devinfo/1/error_stats" 2 0 0 0 0
chmod 000 "$S/t13/btrfs/$UUID/devinfo/1/error_stats"
TSUKUROI_BTRFS_SYSFS="$S/t13/btrfs" bash "$H" || echo "T13 rc=$?"
chmod 644 "$S/t13/btrfs/$UUID/devinfo/1/error_stats"

echo "== T14: value with leading zeros 007 =="
mk "$S/t14"; st_write "$S/t14/btrfs/$UUID/devinfo/1/error_stats" 007 0 0 0 0
TSUKUROI_BTRFS_SYSFS="$S/t14/btrfs" bash "$H" || echo "T14 rc=$?"

echo "== T15: negative value =="
mk "$S/t15"; st_write "$S/t15/btrfs/$UUID/devinfo/1/error_stats" -1 0 0 0 0
TSUKUROI_BTRFS_SYSFS="$S/t15/btrfs" bash "$H" || echo "T15 rc=$?"

echo "== T16: st_write leak semantics (function-in-function persists) =="
bash -c 'outer(){ inner(){ echo inner-body; }; }; outer; declare -F inner >/dev/null && echo "inner STILL DEFINED after outer returned" || echo "inner gone"'
