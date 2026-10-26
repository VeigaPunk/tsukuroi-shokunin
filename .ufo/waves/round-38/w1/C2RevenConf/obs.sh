#!/bin/bash
# C2RevenConf observation replay — read-only pacman/libalpm queries, no mutation.
S=/fast/scratch/hyaku/tsukuroi-r38/C2RevenConf
cd "$S" || exit 1
echo "# C2RevenConf receipts — replayed $(date -u +%FT%TZ)"
echo "# pacman: $(pacman --version | sed -n '3p' | tr -s ' ')"
echo
echo '$ pacman-conf HookDir'; pacman-conf HookDir
echo
echo '$ grep -n -i hookdir /etc/pacman.conf'; grep -n -i 'hookdir' /etc/pacman.conf; echo "(grep exit=$?)"
echo
echo '$ pacman -Q --verbose | grep "Hook Dirs"'; pacman -Q --verbose 2>&1 | grep 'Hook Dirs'
echo
echo '$ pacman-conf --config t1.conf HookDir    # two explicit HookDir lines'
pacman-conf --config "$S/t1.conf" HookDir
echo
echo '$ pacman-conf --config t2.conf HookDir    # [options] only'
pacman-conf --config "$S/t2.conf" HookDir
echo
echo '$ pacman-conf --config t3.conf HookDir    # system dir listed explicitly'
pacman-conf --config "$S/t3.conf" HookDir
echo
echo '$ pacman -Q --verbose --config t1.conf | grep "Hook Dirs"'
pacman -Q --verbose --config "$S/t1.conf" 2>&1 | grep 'Hook Dirs'
echo
echo '$ pacman -Q --verbose --config t3.conf | grep "Hook Dirs"    # duplicate system dir'
pacman -Q --verbose --config "$S/t3.conf" 2>&1 | grep 'Hook Dirs'
echo
echo '$ pacman -Q --verbose --config t4.conf | grep "Hook Dirs"    # relative HookDir'
pacman -Q --verbose --config "$S/t4.conf" 2>&1 | grep 'Hook Dirs'
echo
echo '$ pacman -Q --verbose --hookdir /var/lib/pacman | grep "Hook Dirs"'
pacman -Q --verbose --hookdir /var/lib/pacman 2>&1 | grep 'Hook Dirs'
echo
echo '$ pacman -Q --verbose --hookdir /custom/z     # nonexistent CLI path'
pacman -Q --verbose --hookdir /custom/z 2>&1; echo "exit=$?"
echo
echo '$ pacman -Q --debug 2>&1 | grep -i hookdir   # the only logged hookdir add'
pacman -Q --debug 2>&1 | grep -i hookdir
echo
echo '$ ./probe'; ./probe
echo
echo '$ ./probe add /etc/pacman.d/hooks'; ./probe add /etc/pacman.d/hooks
echo
echo '$ ./probe add hooks'; ./probe add hooks
echo
echo '$ pacman-conf --sysroot <scratch>/sys --config /etc/pacman.conf HookDir'
pacman-conf --sysroot "$S/sys" --config /etc/pacman.conf HookDir
echo
echo '# live hook dirs'
ls -1 /etc/pacman.d/hooks/*.hook | xargs -n1 basename
echo "usr .hook count: $(ls -1 /usr/share/libalpm/hooks/*.hook | wc -l)"
echo "etc .hook count: $(ls -1 /etc/pacman.d/hooks/*.hook | wc -l)"
echo
echo '# same-name collision across the two dirs'
for f in /etc/pacman.d/hooks/*.hook; do b=$(basename "$f"); [ -e "/usr/share/libalpm/hooks/$b" ] && echo "COLLIDE $b"; done
echo
echo '# Exec of the overridden pair'
grep -H '^Exec' /etc/pacman.d/hooks/90-mkinitcpio-install.hook /usr/share/libalpm/hooks/90-mkinitcpio-install.hook
