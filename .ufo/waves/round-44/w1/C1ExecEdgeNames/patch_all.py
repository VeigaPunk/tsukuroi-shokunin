import sys
src = open(sys.argv[1]).read()
def rep(old, new):
    global src
    assert src.count(old) == 1, (src.count(old), old[:60])
    src = src.replace(old, new)

# local list: nd for the devinfo count
rep('  local dir=$SCRUB_DIR root=$BTRFS_SYSFS tw=$TIMER_WANTS fsd dev f v line nl e n fs8',
    '  local dir=$SCRUB_DIR root=$BTRFS_SYSFS tw=$TIMER_WANTS fsd dev f v rest e n fs8 nd')
# per-fsid devinfo counter
rep('      fsids+="${fsd##*/} "; fs8=${fsd##*/}; fs8=${fs8:0:8}',
    '      fsids+="${fsd##*/} "; fs8=${fsd##*/}; fs8=${fs8:0:8}; nd=0')
rep('''        [ -e "$dev" ] || continue
        if ! [[ ${dev##*/} =~ ^[0-9]+$ ]]; then''',
    '''        [ -e "$dev" ] || continue
        nd=$((nd + 1))
        if ! [[ ${dev##*/} =~ ^[0-9]+$ ]]; then''')
# gap 3: reject a symlink at the attribute path
rep('        if [ ! -f "$f" ] || [ ! -r "$f" ]; then blocked=1; detail+="$fs8:${dev##*/}:speed-unreadable,"; continue; fi',
    '        if [ -L "$f" ] || [ ! -f "$f" ] || [ ! -r "$f" ]; then blocked=1; detail+="$fs8:${dev##*/}:speed-unreadable,"; continue; fi')
# gap 5: bounded single-line read
rep('''        v=\'\' nl=0
        while IFS= read -r line || [ -n "$line" ]; do nl=$((nl + 1)); v=$line; done < "$f"
        if [ "$nl" -ne 1 ] || ! [[ $v =~ ^[0-9]+$ ]]; then
          blocked=1; detail+="$fs8:${dev##*/}:speed-malformed,"; continue
        fi
''',
'''        v=\'\' rest=\'\'
        { IFS= read -r -n 33 v || [ -n "$v" ] || true
          IFS= read -r -N 1 rest || [ -n "$rest" ] || true; } < "$f"
        if [ "${#v}" -ge 33 ] || [ -n "$rest" ] || ! [[ $v =~ ^[0-9]+$ ]]; then
          blocked=1; detail+="$fs8:${dev##*/}:speed-malformed,"; continue
        fi
''')
# gap 4: fsid with no devinfo subtree (non-blocking detail)
rep('''        if ! [[ $v =~ ^0+$ ]]; then lim=$((lim + 1)); info+="$fs8:${dev##*/}:speed_max=$v,"; fi
      done
    done''',
'''        if ! [[ $v =~ ^0+$ ]]; then lim=$((lim + 1)); info+="$fs8:${dev##*/}:speed_max=$v,"; fi
      done
      [ "$nd" -gt 0 ] || detail+="$fs8:?:no-devinfo,"
    done''')
# gap 1: a sysfs root that exists but is not a directory
rep('      if [ "$rec" -gt 0 ] && [ "$sysok" -eq 0 ] && [ ! -e "$root" ]; then blocked=1; detail+=\'sysfs:absent,\'; fi',
'''      if [ "$rec" -gt 0 ] && [ "$sysok" -eq 0 ]; then
        blocked=1
        if [ -e "$root" ]; then detail+='sysfs:not-directory,'; else detail+='sysfs:absent,'; fi
      fi''')
# gap 2: a timer entry that is not an enable-link
rep('''        [ "${e##*/}" != 'btrfs-scrub@.timer' ] || continue
        tim=$((tim + 1))
      done''',
'''        [ "${e##*/}" != 'btrfs-scrub@.timer' ] || continue
        if [ ! -L "$e" ]; then blocked=1; detail+='timers:not-link,'; continue; fi
        tim=$((tim + 1))
        [ -e "$e" ] || detail+='timers:dangling,'
      done''')
open(sys.argv[2], 'w').write(src)
print("patched all five")
