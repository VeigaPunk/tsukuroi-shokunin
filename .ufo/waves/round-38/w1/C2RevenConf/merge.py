#!/usr/bin/env python3
# C2RevenConf — replay of hook.c:540 enumeration semantics over the live dirs.
# handle->hookdirs as observed: ["/usr/share/libalpm/hooks/", "/etc/pacman.d/hooks/"]
import os
dirs = ["/usr/share/libalpm/hooks/", "/etc/pacman.d/hooks/"]
seen, order = {}, []
for d in reversed(dirs):                      # alpm_list_last() then alpm_list_previous()
    for n in sorted(os.listdir(d)):           # readdir order; sorted only to make output stable
        if not n.endswith(".hook"):
            continue
        if n in seen:                         # hook.c:588 find_hook() -> "skipping overridden hook"
            continue
        seen[n] = d
        order.append(n)
print("dirs (list order):", dirs)
print("files: usr=%d etc=%d total=%d" % (
    len([x for x in os.listdir(dirs[0]) if x.endswith(".hook")]),
    len([x for x in os.listdir(dirs[1]) if x.endswith(".hook")]),
    sum(len([x for x in os.listdir(d) if x.endswith(".hook")]) for d in dirs)))
print("effective hooks:", len(order))
print("etc winners:", [n for n in order if seen[n] == dirs[1]])
order.sort(key=lambda n: (n[:-5], len(n[:-5])))   # hook.c:443-455 _alpm_hook_cmp
for a, b in [("fontconfig.hook", "fontconfig-32.hook"),
             ("gio-querymodules.hook", "gio-querymodules-32.hook"),
             ("gio-remove-module-cache.hook", "gio-remove-module-cache-32.hook")]:
    print("HO1 %-32s before %-32s : %s" % (a, b, order.index(a) < order.index(b)))
print("merged candidate order (both phases):")
for i, n in enumerate(order, 1):
    print("  %2d %s  [%s]" % (i, n, "etc" if seen[n] == dirs[1] else "usr"))
