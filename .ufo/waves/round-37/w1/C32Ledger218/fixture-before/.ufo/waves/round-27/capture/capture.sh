#!/usr/bin/env bash
# Round-27 read-only kernel-taint capture (tsukuroi). No sudo, no writes outside stdout.
set -u
sec() { printf '### %s\n' "$1"; }
run() { printf '$ %s\n' "$*"; "$@" 2>&1; printf '[exit %s]\n' "$?"; }
sec time; run date -u +%Y-%m-%dT%H:%M:%SZ
sec kernel; run uname -r
sec tainted; run cat /proc/sys/kernel/tainted
sec per-module-taint
for f in /sys/module/*/taint; do t=$(cat "$f" 2>/dev/null); [ -n "$t" ] && printf 'module_taint %s %s\n' "$(basename "$(dirname "$f")")" "$t"; done
printf '[exit 0]\n'
sec sig_enforce; run cat /sys/module/module/parameters/sig_enforce
sec kernel-config; printf '$ zgrep -E CONFIG_MODULE_SIG|CONFIG_MODVERSIONS /proc/config.gz\n'; zgrep -E '^(# )?CONFIG_(MODULE_SIG|MODVERSIONS)' /proc/config.gz; printf '[exit %s]\n' "$?"
for m in nvidia nvidia_drm nvidia_modeset nvidia_uvm; do
  sec "modinfo-$m"; run modinfo -F filename "$m"; run modinfo -F version "$m"; run modinfo -F license "$m"; run modinfo -F signer "$m"; run modinfo -F vermagic "$m"
  fn=$(modinfo -F filename "$m" 2>/dev/null); [ -n "$fn" ] && run pacman -Qo "$fn"
done
sec packages; run pacman -Q linux dkms nvidia-open-dkms nvidia-utils
sec cmdline-taint-params; printf '$ grep -oE (panic_on_taint|module.sig_enforce)[^ ]* /proc/cmdline\n'; grep -oE '(panic_on_taint|module\.sig_enforce)[^ ]*' /proc/cmdline; printf '[exit %s]\n' "$?"
sec panic_on_taint-sysctl; run cat /proc/sys/kernel/panic_on_taint
sec kernel-journal-taint; printf '$ journalctl -k -b 0 --no-pager -o short-monotonic | grep -iE taint\n'; journalctl -k -b 0 --no-pager -o short-monotonic 2>&1 | grep -iE 'taint'; printf '[exit %s]\n' "$?"
