#!/usr/bin/env bash
# Drive each of the seven unclaimed `| head` readers at 18389f44 past the pipe buffer.
# Each site gets a SMALL fixture pair (same logical content as the first rows of the padded
# one, total output below the 64 KiB pipe buffer) and a PAD fixture (same first rows, the
# rest of the output past the pipe buffer), so exit code and read value are directly
# comparable, per site, at one revision.
set -uo pipefail
S=/fast/scratch/hyaku/tsukuroi-r45/C1ExecMaskedSites
. "$S/h.sh"
mkdir -p "$S/out"
summary="$S/out/summary.txt"
: > "$summary"

rec() { # rec LABEL FXPATH
  local label=$1 fx=$2
  run "$fx"
  printf '%s\n' "$OUT" > "$S/out/$label.out"
  printf '%s\n' "$RC" > "$S/out/$label.rc"
  printf 'CASE %-14s rc=%s verdict=%s\n' "$label" "$RC" "$(printf '%s\n' "$OUT" | sed -n 's/^TSUKUROI_CENSUS: \([A-Z]*\).*/\1/p')" >> "$summary"
}

# ---------------- site :707  probe_packages, pacman -Qq sample (process substitution) ------
mkfix "$S/fx/s707-small"
printf 'pkg-01\npkg-02\npkg-03\npkg-04\npkg-05\npkg-06\npkg-07\npkg-08\n' > "$S/fx/s707-small/pq"
mkfix "$S/fx/s707-pad"
{ printf 'pkg-01\npkg-02\npkg-03\npkg-04\npkg-05\npkg-06\npkg-07\npkg-08\n'
  awk 'BEGIN { for (i = 0; i < 2000; i++) printf "zz-pad-package-%05d-with-a-long-suffix-padding\n", i }'; } > "$S/fx/s707-pad/pq"
rec s707-small "$S/fx/s707-small"
rec s707-pad   "$S/fx/s707-pad"
printf '  707 pq bytes small=%s pad=%s\n' "$(wc -c < "$S/fx/s707-small/pq")" "$(wc -c < "$S/fx/s707-pad/pq")" >> "$summary"

# ---------------- site :832  probe_packages, HoldPkg first row (`|| true` assignment) -----
mkfix "$S/fx/s832-small"
printf 'HoldPkg = pacman glibc\n' > "$S/fx/s832-small/pacman.conf"
mkfix "$S/fx/s832-pad"
{ printf 'HoldPkg = pacman glibc\n'
  awk 'BEGIN { for (i = 0; i < 2500; i++) printf "HoldPkg     = pad-hold-%05d pad-hold-%05d-a\n", i, i }'; } > "$S/fx/s832-pad/pacman.conf"
rec s832-small "$S/fx/s832-small"
rec s832-pad   "$S/fx/s832-pad"

# ---------------- site :997  probe_systemd user timers (process substitution) -------------
mkfix "$S/fx/s997-small"
printf 'aa-user-timer.timer enabled enabled\n' > "$S/fx/s997-small/timerlist"
printf 'failed\n' > "$S/fx/s997-small/timerresult"
mkfix "$S/fx/s997-pad"
{ printf 'aa-user-timer.timer enabled enabled\n'
  awk 'BEGIN { for (i = 0; i < 2000; i++) printf "zz-pad-user-timer-%05d-with-a-long-name.timer enabled enabled\n", i }'; } > "$S/fx/s997-pad/timerlist"
printf 'failed\n' > "$S/fx/s997-pad/timerresult"
rec s997-small "$S/fx/s997-small"
rec s997-pad   "$S/fx/s997-pad"

# ---------------- site :1531 probe_journal timer ActiveState (process substitution) ------
mkfix "$S/fx/s1531-small"
printf 'aa-jrn-timer.timer enabled enabled\n' > "$S/fx/s1531-small/timerlist"
printf 'inactive\n' > "$S/fx/s1531-small/timeractivestate"
mkfix "$S/fx/s1531-pad"
{ printf 'aa-jrn-timer.timer enabled enabled\n'
  awk 'BEGIN { for (i = 0; i < 2000; i++) printf "zz-pad-jrn-timer-%05d-with-a-long-name.timer enabled enabled\n", i }'; } > "$S/fx/s1531-pad/timerlist"
printf 'inactive\n' > "$S/fx/s1531-pad/timeractivestate"
rec s1531-small "$S/fx/s1531-small"
rec s1531-pad   "$S/fx/s1531-pad"

# ---------------- site :1196 probe_mem_arm cgroup sweep (find|sort|head -n 4000) ---------
mkfix "$S/fx/s1196-small"
mkfix "$S/fx/s1196-pad-a"     # 1500 pad files: find|sort output past the pipe buffer, cap not hit
i=0; while [ "$i" -lt 1500 ]; do
  d="$S/fx/s1196-pad-a/cgroup/zzz-pad/very-long-cgroup-directory-name-for-the-pipe-buffer-$i"
  mkdir -p "$d"; printf 'oom_kill 0\n' > "$d/memory.events"; i=$((i + 1))
done
mkfix "$S/fx/s1196-pad-b"     # 4200 pad files: the documented 4000 cap is reached
i=0; while [ "$i" -lt 4200 ]; do
  d="$S/fx/s1196-pad-b/cgroup/zzz-pad/very-long-cgroup-directory-name-for-the-pipe-buffer-$i"
  mkdir -p "$d"; printf 'oom_kill 0\n' > "$d/memory.events"; i=$((i + 1))
done
rec s1196-small "$S/fx/s1196-small"
rec s1196-pad-a "$S/fx/s1196-pad-a"
rec s1196-pad-b "$S/fx/s1196-pad-b"

# ---------------- site :1517 probe_journal failed-history names (`|| true`) --------------
names6='aa-fail-01.service aa-fail-02.service aa-fail-03.service aa-fail-04.service aa-fail-05.service aa-fail-06.service'
mkfix "$S/fx/s1517-small"
: > "$S/fx/s1517-small/journal-err.json"
for u in $names6; do printf '{"MESSAGE":"Failed to start %s."}\n' "$u" >> "$S/fx/s1517-small/journal-err.json"; done
mkfix "$S/fx/s1517-pad"
for u in $names6; do printf '{"MESSAGE":"Failed to start %s."}\n' "$u" >> "$S/fx/s1517-pad/journal-err.json"; done
awk 'BEGIN { for (i = 0; i < 3000; i++) printf "{\"MESSAGE\":\"Failed to start zz-pad-unit-%05d-with-a-long-unit-name.service.\"}\n", i }' >> "$S/fx/s1517-pad/journal-err.json"
rec s1517-small "$S/fx/s1517-small"
rec s1517-pad   "$S/fx/s1517-pad"

# ---------------- site :1817 probe_update_safety unknown-provenance (`|| true`) ----------
unk6='zz-unk-01 zz-unk-02 zz-unk-03 zz-unk-04 zz-unk-05 zz-unk-06'
mkfix "$S/fx/s1817-small"
{ for n in $unk6; do printf '%s 1.0-1\n' "$n"; done; } > "$S/fx/s1817-small/pm"
mkfix "$S/fx/s1817-pad"
{ for n in $unk6; do printf '%s 1.0-1\n' "$n"; done
  awk 'BEGIN { for (i = 0; i < 3000; i++) printf "zz-pad-foreign-package-%05d-with-a-long-name 1.0-1\n", i }'; } > "$S/fx/s1817-pad/pm"
rec s1817-small "$S/fx/s1817-small"
rec s1817-pad   "$S/fx/s1817-pad"

printf '== summary ==\n'
cat "$summary"
