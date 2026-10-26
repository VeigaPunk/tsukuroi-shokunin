#!/bin/bash
# usage: sweep.sh ; runs in fleet root. tsukuroi at base 53b294a2 (pathspecs), siblings at HEAD
declare -A P=(
 [scriptlet_shell]='scriptlet.{0,40}(shell|/bin/sh|/usr/bin/bash)|(shell|/bin/sh|/usr/bin/bash).{0,40}scriptlet'
 [SHLVL]='SHLVL'
 [BASH_ENV]='BASH_ENV'
 [umask_0022]='umask.{0,20}0?022|0?022.{0,20}umask'
 [alpm_XXXXXX]='alpm_(XXXXXX|[A-Za-z0-9]{6})|\.INSTALL'
 [NeedsTargets]='NeedsTargets'
 [could_not_satisfy]='could not satisfy dependencies'
 [NoExtract_trigger]='NoExtract'
 [chroot_cwd]='(chroot|cwd|working directory).{0,60}(hook|scriptlet|install)|(hook|scriptlet|install).{0,60}(chroot|cwd|working directory)'
)
for k in scriptlet_shell SHLVL BASH_ENV umask_0022 alpm_XXXXXX NeedsTargets could_not_satisfy NoExtract_trigger chroot_cwd; do
  echo "== $k  /$(echo ${P[$k]})/"
  echo "-- tsukuroi @53b294a2 (corpus SKILL.md PROVINCE.md)"
  git -C tsukuroi-shokunin grep -n -i -E "${P[$k]}" 53b294a274656be6479aadf2ec2fee890ded77ce -- corpus SKILL.md PROVINCE.md | wc -l
  for l in *-shokunin; do
    [ $l = tsukuroi-shokunin ] && continue
    n=$(git -C $l grep -n -i -E "${P[$k]}" HEAD 2>/dev/null | wc -l)
    echo "$l $n"
  done | awk '$2>0'
done
