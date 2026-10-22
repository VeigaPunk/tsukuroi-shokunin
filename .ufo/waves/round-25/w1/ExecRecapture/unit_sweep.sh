#!/usr/bin/env bash
# Round 25 C2 cross-check, supplementary sweep: every unit systemd knows about,
# and what it reports for ManagedOOMMemoryPressure / ManagedOOMSwap.
# Read-only. No sudo. Writes only to the output file given as $1.
set -u
out=${1:?usage: unit_sweep.sh <output-file>}
{
  printf '### unit-count\n'
  printf '$ systemctl list-units --all --no-legend --no-pager | wc -l\n'
  systemctl list-units --all --no-legend --no-pager 2>/dev/null | wc -l
  printf '[exit %s]\n' "$?"
  printf '### per-unit-managed-oom\n'
  printf '$ for each unit: systemctl show -p ManagedOOMMemoryPressure -p ManagedOOMSwap --value\n'
  systemctl list-units --all --no-legend --no-pager 2>/dev/null | awk '{print $1}' | while read -r u; do
    mp=$(systemctl show -p ManagedOOMMemoryPressure --value -- "$u" 2>/dev/null)
    ms=$(systemctl show -p ManagedOOMSwap --value -- "$u" 2>/dev/null)
    if [ -n "$mp" ] || [ -n "$ms" ]; then
      printf '%s ManagedOOMMemoryPressure=%s ManagedOOMSwap=%s\n' "$u" "$mp" "$ms"
    fi
  done | sort -u
  printf '[exit %s]\n' "$?"
  printf '### non-auto-units\n'
  printf '$ the same sweep filtered to units whose value is not auto\n'
  systemctl list-units --all --no-legend --no-pager 2>/dev/null | awk '{print $1}' | while read -r u; do
    mp=$(systemctl show -p ManagedOOMMemoryPressure --value -- "$u" 2>/dev/null)
    ms=$(systemctl show -p ManagedOOMSwap --value -- "$u" 2>/dev/null)
    if [ -n "$mp" ] && { [ "$mp" != "auto" ] || { [ -n "$ms" ] && [ "$ms" != "auto" ]; }; }; then
      printf '%s ManagedOOMMemoryPressure=%s ManagedOOMSwap=%s\n' "$u" "$mp" "$ms"
    fi
  done
  printf '[exit %s]\n' "$?"
  printf '### distinct-values\n'
  printf '$ cut -d" " -f2,3 over the per-unit table | sort -u\n'
  systemctl list-units --all --no-legend --no-pager 2>/dev/null | awk '{print $1}' | while read -r u; do
    mp=$(systemctl show -p ManagedOOMMemoryPressure --value -- "$u" 2>/dev/null)
    ms=$(systemctl show -p ManagedOOMSwap --value -- "$u" 2>/dev/null)
    if [ -n "$mp" ] || [ -n "$ms" ]; then
      printf 'ManagedOOMMemoryPressure=%s ManagedOOMSwap=%s\n' "$mp" "$ms"
    fi
  done | sort | uniq -c
  printf '[exit %s]\n' "$?"
} > "$out"
sha256sum "$out"
