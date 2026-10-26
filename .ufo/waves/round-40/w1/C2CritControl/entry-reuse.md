source: S220, S221, S222, S223 in `corpus/SOURCES.md`
verified-at: 2026-10-26
recheck: counter

# Mechanical entry

## Rules

| id | rule | value | source (file:line and quote) | host |
|---|---|---|---|---|
| EX1 | working directory chroot `/` alpha bravo charlie delta echo foxtrot golf hotel | / | S221 util.c:4-4 “*  Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | mechanical host cell |
| EX2 | stdout stderr stdin end-of-file alpha bravo charlie delta echo foxtrot golf hotel | stdout+stderr: one socket; stdin: second socket | S221 util.c:4-4 “*  Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | mechanical host cell |
| EX3 | SHLVL BASH_ENV umask 0022 alpha bravo charlie delta echo foxtrot golf hotel | SHLVL=1 BASH_ENV=unset umask=0022 | S221 util.c:4-4 “*  Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | mechanical host cell |
| EX4 | /usr/bin/bash /bin/sh -c alpha bravo charlie delta echo foxtrot golf hotel india | /usr/bin/bash | S220 PKGBUILD:1-1 “# Maintainer: Levente Polyak <anthraxx[at]archlinux[dot]org>” | /usr/bin/bash libalpm.so.16.0.1 |
| EX5 | tmp/alpm_XXXXXX .INSTALL 01777 alpha bravo charlie delta echo foxtrot golf hotel india | tmp/alpm_XXXXXX/.INSTALL | S222 trans.c:4-4 “*  Copyright (c) 2006-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | mechanical host cell |
| EX6 | NeedsTargets stdin sorted duplicate alpha bravo charlie delta echo foxtrot golf hotel | sorted, deduplicated, one per line | S223 hook.c:4-4 “*  Copyright (c) 2015-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | 14 of 69 effective hook files |
| EX7 | Depends running AbortOnFail satisfy dependencies alpha bravo charlie delta echo foxtrot golf | could not satisfy dependencies | S223 hook.c:4-4 “*  Copyright (c) 2015-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | mechanical host cell |
| EX8 | file list NoExtract NoUpgrade .pacnew alpha bravo charlie delta echo foxtrot golf | NoExtract | S223 hook.c:4-4 “*  Copyright (c) 2015-2025 Pacman Development Team <pacman-dev@lists.archlinux.org>” | mechanical host cell |
