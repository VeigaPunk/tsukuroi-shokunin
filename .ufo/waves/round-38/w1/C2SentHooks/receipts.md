# C2SentHooks — receipts (read-only, capture 2026-10-26)

All commands read-only. No transaction run, no sudo, no host mutation, no scratch clone.

## 1. Hook file identity

```
$ sha256sum /etc/pacman.d/hooks/walker-restart.hook \
    .ufo/waves/round-38/frozen/hooks-capture/etc-pacman.d-hooks/walker-restart.hook
658171771949d8bc633faf79432cf78f42734423594f57eca695fb70d02888b9  /etc/pacman.d/hooks/walker-restart.hook
658171771949d8bc633faf79432cf78f42734423594f57eca695fb70d02888b9  .../etc-pacman.d-hooks/walker-restart.hook

$ stat -c '%n %U:%G %a' /etc/pacman.d/hooks /etc/pacman.d/hooks/walker-restart.hook
/etc/pacman.d/hooks root:root 755
/etc/pacman.d/hooks/walker-restart.hook root:root 644
```

Hook body (11 lines, live == captured):

```
[Trigger]
Type = Package
Operation = Upgrade
Target = walker
Target = walker-debug
Target = elephant*

[Action]
Description = Restarting Walker services after system update
When = PostTransaction
Exec = /home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker
```

## 2. Exec target: writer set

```
$ stat -c '%n %U:%G %a %s' /home/vgpnk /home/vgpnk/.local/share/omarchy \
    /home/vgpnk/.local/share/omarchy/bin /home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker
/home/vgpnk 700 vgpnk
/home/vgpnk/.local/share/omarchy vgpnk:vgpnk 755
/home/vgpnk/.local/share/omarchy/bin vgpnk:vgpnk 755
/home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker vgpnk:vgpnk 755 709

$ getfacl -p .../omarchy-restart-walker
user::rwx  group::r-x  other::r-x        # no named ACL

$ id -u vgpnk
1000

$ pacman -Qo /home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker
error: No package owns /home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker
```

Git provenance of the same file (user-owned checkout):

```
$ git -C /home/vgpnk/.local/share/omarchy remote -v
origin  https://github.com/basecamp/omarchy.git (fetch)
$ git -C ... log -1 --format='%H %ci %s' -- bin/omarchy-restart-walker
d2a4cc0c4d60cd3bce866f65643f89f7d2978d5e 2026-05-01 17:40:22 +0200 Add omarchy CLI (#5477)
$ git -C ... status --porcelain | wc -l
0
$ git -C ... cat-file -p HEAD:bin/omarchy-restart-walker | sha256sum
9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174  -
$ sha256sum bin/omarchy-restart-walker
9ac82d0c1370ec19f59c8347716036765d3335d348feaec4c9581e2ca3bf8174  bin/omarchy-restart-walker
```

Script body (709 B): EUID==0 branch resolves `stat -c '%U' "$0"`, then
`systemd-run --uid="$SCRIPT_OWNER" --setenv=XDG_RUNTIME_DIR=/run/user/$USER_UID bash -c ...`.
`systemd-run --uid=<other user>` needs privilege, so the `Running as unit:` line is
root-branch evidence.

## 3. Trigger set

```
$ pacman -Qq | grep '^elephant'
elephant elephant-bluetooth elephant-calc elephant-clipboard elephant-desktopapplications
elephant-files elephant-menus elephant-providerlist elephant-runner elephant-symbols
elephant-todo elephant-unicode elephant-websearch            # 13
$ pacman -Q walker walker-debug elephant
walker 2.17.2-1
error: package 'walker-debug' was not found
elephant 2.22.1-1
```

## 4. Observed firings (root branch taken each time)

```
/var/log/pacman.log:2034  [2026-10-11T16:16:37-0300] [ALPM] running 'walker-restart.hook'...
/var/log/pacman.log:2035  [ALPM-SCRIPTLET] Running as unit: run-p180026-i69093.service; ...
/var/log/pacman.log:3062  [2026-10-20T09:18:25-0300] [ALPM] running 'walker-restart.hook'...
/var/log/pacman.log:3063  [ALPM-SCRIPTLET] Running as unit: run-p236822-i284703.service; ...
/var/log/pacman.log:3123  [2026-10-20T09:31:04-0300] [ALPM] running 'walker-restart.hook'...
/var/log/pacman.log:3124  [ALPM-SCRIPTLET] Running as unit: run-p371567-i306456.service; ...
```

09:31 transaction (contiguous): elephant-unicode/-todo/-menus upgraded from 2.21.0-1 to
2.22.1-1 and the `-debug` variants installed (`pacman.log:3115-3122`), then
`transaction completed`, then the hook (`:3123-3124`).

## 5. libalpm source (pinned snapshot, .ufo/waves/round-38/sources/, sha256 in SHA256SUMS)

- `hook.c:372` — Package trigger matched by `_alpm_fnmatch_patterns(t->targets, pkg->name)` (glob).
- `hook.c:239` — `hook->cmd = wordsplit(value)`: argv from whitespace/quote splitting, no shell.
- `hook.c:131-135` — validate checks only `hook->cmd == NULL` ("Missing Exec option").
- `hook.c:593` — the only `stat()` in the load path is on the `.hook` file, not on the Exec target.
- `hook.c:525-528` — `_alpm_run_chroot(handle, hook->cmd[0], hook->cmd, ...)`, path executed as given.
- `trans.c:202` — Pre-phase result checked → `ALPM_ERR_TRANS_HOOK_FAILED`.
- `trans.c:238` — `_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION);` return value not used.
- `alpm-hooks.5.asciidoc:61-67` — Target: "Shell-style glob patterns are allowed".

## 6. Comparison rows (package-owned Exec targets)

```
$ pacman -Qo /usr/share/libalpm/scripts/limine-mkinitcpio-install /usr/bin/locale-gen
/usr/share/libalpm/scripts/limine-mkinitcpio-install is owned by limine-mkinitcpio-hook 1.40.0-2
/usr/bin/locale-gen is owned by glibc 2.44+r50+g1848099f063e-1
```

Of the 69 rows in `corpus/knowledge/pacman-hook-order-r38.md:31-101`, exactly one `exec`
cell is outside `/usr/`|`/bin/` (`:101`, the home path):

```
$ awk -F'|' '/^\| (Pre|Post)Transaction \|/ {gsub(/`/,"",$8); gsub(/^ +| +$/,"",$8);
    if ($8 !~ /^\/(usr|bin)\//) print NR": "$8}' corpus/knowledge/pacman-hook-order-r38.md
101: /home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker
```

## 7. Counter parsing (why the proposed note cannot move C2's predicate)

`tools/check-hook-order-r38.py:141-154` (`entry_rows`) collects table lines only between
`SECTION` ("## Effective hook order (r38 capture)") and the next `## ` heading; it `break`s at
that heading. `source_check` (`:157-158`) reads only the first `source:` line. A bullet appended
under "## Observed / inferred / unknown" (`corpus/knowledge/pacman-hook-order-r38.md:103-109`)
is therefore outside `rows_expected`/`rows_matched`/`extra_rows` and outside `source_ok`.
Editing the row-52 cells instead would change the 7-tuple compared by the counter.
