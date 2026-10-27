  fx_default() { # clean fixture: everything passes, dmesg restricted like the measured host
    local d=$1
    mkdir -p "$d/pacmandb" "$d/pci" "$d/dev" "$d/root" "$d/etc"
    # Round-12 C1 fixture root: mode 0755 explicitly — umask 077 makes a bare mkdir 0700,
    # and the healthy-case regexes pin 0755, so an implicit mode would hide a mode leak.
    chmod 0755 "$d/root"
    printf 'alpha\nbeta\ngamma\ndelta\n' > "$d/pq"
    printf 'alpha: 10 total files, 0 altered files\nbeta: 20 total files, 0 altered files\n' > "$d/qkk.out"
    printf 0 > "$d/qkk.rc"
    : > "$d/pm"
    : > "$d/fbase"
    : > "$d/pconf"
    # round 39: the storage arm's mount table; no btrfs mount, so an absent sysfs root stays 0/0/0
    printf 'proc /proc proc rw,nosuid 0 0\n/dev/fx0 / ext4 rw,relatime 0 0\n' > "$d/mounts"
    # update-safety plane fixture (S9-1): a fresh 2-db channel, an empty candidate set at the
    # real `-Qu` rc (1 = none), the plan verbs empty, the joined sources agreeing, and a
    # bounded log window holding one non-refresh command.
    mkdir -p "$d/pacmandb/sync"
    : > "$d/pacmandb/sync/core.db"
    : > "$d/pacmandb/sync/omarchy.db"
    : > "$d/pacmandb/sync/offline.db"
    : > "$d/qu"; printf 1 > "$d/qu.rc"
    : > "$d/sup"; printf 0 > "$d/sup.rc"
    : > "$d/suu"; printf 0 > "$d/suu.rc"
    printf 'alpha 1.0-1\nbeta 2.0-1\n' > "$d/q"
    printf 'fixture alpha 1.0-1\nextra beta 2.0-1\n' > "$d/sl"
    printf 'alpha\t1.0-1\nbeta\t2.0-1\n' > "$d/expacsl"
    printf '%s\n' "[2026-10-13T16:37:58-0300] [PACMAN] Running 'pacman -S --needed --noconfirm fixture-pkg'" > "$d/pacman.log"
    printf 'HoldPkg = pacman glibc\n' > "$d/pacman.conf"
    printf 'running\n' > "$d/sysrunning"
    printf 0 > "$d/sysrunning.rc"
    : > "$d/failedunits"
    printf 'ai-usage.timer enabled enabled\n' > "$d/timerlist"
    printf 'success\n' > "$d/timerresult"
    printf 1 > "$d/dmesg.rc"
    : > "$d/dmesg.out"
    : > "$d/dmesg-all.out"
    printf 0 > "$d/dmesg-all.rc"
    : > "$d/journal-err.json"
    printf '{"MESSAGE":"fixture: kernel line 1"}\n{"MESSAGE":"fixture: kernel line 2"}\n{"MESSAGE":"fixture: kernel line 3"}\n' > "$d/journal-all.json"
    printf 0 > "$d/journal-err.rc"
    printf 0 > "$d/journal-all.rc"
    : > "$d/smi.out"
    printf 1 > "$d/smi.rc"
    : > "$d/lsmod"
    printf 'fixture-host\n' > "$d/hostname"
    printf 1 > "$d/dmesg_restrict"
    printf 'IDX BOOT ID                          FIRST ENTRY                 LAST ENTRY\n' > "$d/listboots"
    printf ' -1 73a8e2fc20cc48749b3cbd24ed5dc7c1 Sun 2026-10-11 19:02:51 -03 Tue 2026-10-13 10:57:30 -03\n' >> "$d/listboots"
    printf '  0 d7f0bc8d938e4249b4a1f250cbfacf58 Tue 2026-10-13 11:02:03 -03 Wed 2026-10-14 11:42:34 -03\n' >> "$d/listboots"
    printf 0 > "$d/listboots.rc"
    printf 'active\n' > "$d/boottarget"
    printf 0 > "$d/boottarget.rc"
    printf '{"MESSAGE":"fixture: journal last entry"}\n' > "$d/journal-last"
    printf 0 > "$d/journal-last.rc"
    printf 'active\n' > "$d/timeractivestate"
    printf 0 > "$d/timeractivestate.rc"
    # memory-pressure arm fixture (S7-2): quiet cgroup tree, PSI, meminfo and the three
    # journal `--grep` arms — the live host's shape (95 memory.events files) in miniature
    mkdir -p "$d/cgroup/user.slice/user-1000.slice/user@1000.service" "$d/pressure"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/memory.events"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/memory.events.local"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/user-1000.slice/memory.events"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/user-1000.slice/memory.events.local"
    printf 'low 0\nhigh 0\nmax 0\noom 0\noom_kill 0\noom_group_kill 0\nsock_throttled 0\n' \
      > "$d/cgroup/user.slice/user-1000.slice/user@1000.service/memory.events"
    printf 'high 0\nmax 0\nfail 0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.swap.events"
    printf '0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.swap.peak"
    printf 'pswpin 0\npswpout 0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.stat"
    printf 'max\n' > "$d/cgroup/user.slice/user-1000.slice/memory.max"
    printf 'max\n' > "$d/cgroup/user.slice/user-1000.slice/memory.high"
    printf '0\n' > "$d/cgroup/user.slice/user-1000.slice/memory.oom.group"
    printf 'some avg10=0.00 avg60=0.00 avg300=0.00 total=0\nfull avg10=0.00 avg60=0.00 avg300=0.00 total=0\n' > "$d/pressure/memory"
    printf 'MemTotal: 1000000 kB\nMemAvailable: 900000 kB\nSwapTotal: 8000000 kB\nSwapFree: 8000000 kB\nShmem: 1000 kB\n' > "$d/meminfo"
    : > "$d/oom-kernel.json"; printf 0 > "$d/oom-kernel.rc"
    : > "$d/oom-attrib.json"; printf 0 > "$d/oom-attrib.rc"
    : > "$d/oom-sigkill.json"; printf 0 > "$d/oom-sigkill.rc"
    # oom watch fixture (S9-2): retained-window stubs — the boot list is the existing
    # listboots fixture; the scans default to "0 entries" (rc 1, the measured --grep
    # no-match semantics) and the kernel-kill ledger reads 0.
    printf 'oom_kill 0\n' > "$d/vmstat"
    : > "$d/obase"
    : > "$d/oomwin-kernel"; printf 1 > "$d/oomwin-kernel.rc"
    : > "$d/oomwin-attrib"; printf 1 > "$d/oomwin-attrib.rc"
    : > "$d/oomwin-sigkill"; printf 1 > "$d/oomwin-sigkill.rc"
  }
