#!/bin/bash
# tight patterns; case-sensitive unless noted. Siblings at HEAD (all refs not scanned), tsukuroi at base 53b294a2.
cd /home/vgpnk/Projects/shokunin
declare -a K=(alpm_XXXXXX 'tmp/alpm_' 'scriptlet-shell' 'SCRIPTLET_SHELL' 'could not satisfy dependencies' 'unable to run hook' 'NeedsTargets' 'alpm-hooks' 'libalpm' '_alpm_run_chroot' 'BASH_ENV' 'SHLVL=' 'umask\(0022\)|umask 0?022' )
for k in "${K[@]}"; do
  echo "== /$k/"
  printf 'tsukuroi@53b294a2 %s\n' "$(git -C tsukuroi-shokunin grep -c -E "$k" 53b294a274656be6479aadf2ec2fee890ded77ce -- corpus SKILL.md PROVINCE.md 2>/dev/null | awk -F: '{s+=$NF} END{print s+0}')"
  for l in *-shokunin; do [ $l = tsukuroi-shokunin ] && continue
    n=$(git -C $l grep -c -E "$k" HEAD 2>/dev/null | awk -F: '{s+=$NF} END{print s+0}'); [ "$n" -gt 0 ] && echo "$l $n"
  done
done
