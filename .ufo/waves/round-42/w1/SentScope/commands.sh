# SentScope-5 (item G-5) — commands executed, verbatim (read-only except own scratch and this seat dir)
date -Is; ls -la tsukuroi-shokunin/.ufo/waves/round-42/
git -C /home/vgpnk/Projects/shokunin rev-parse --show-toplevel
git -C /home/vgpnk/Projects/shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain --untracked-files=no
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --oneline --stat f50c28d83e1832ecd7eba765caace531f45d6b27..HEAD
find /tmp /var/tmp -maxdepth 5 -newer <marker> \( -name '*tsukuroi*r42*' -o -name '*tsukuroi-r42*' -o -name '*size-inv-r42*' \)
find /tmp /var/tmp -maxdepth 3 -newer <marker> -user vgpnk -printf '%s\t%TY-%Tm-%TdT%TH:%TM:%TS\t%p\n'
ls -la /home/vgpnk/.local/bin ; ls /home/vgpnk/.local/bin
find /fast/scratch/hyaku/tsukuroi-r42 -maxdepth 1 -mindepth 1 -printf '%TY-%Tm-%TdT%TH:%TM\t%u\t%p\n'
du -sh /fast/scratch/hyaku/tsukuroi-r42/*
find <lane>/.ufo/waves/round-42/w1 -type f -printf '%s\t%TY-%Tm-%TdT%TH:%TM\t%p\n'
find /home/vgpnk/.local/bin -maxdepth 1 -newer <marker> -mindepth 1
for d in $PATH dirs; do find "$d" -maxdepth 1 -newer <marker> -mindepth 1; done
for p in /proc/[0-9]*; do tr '\0' ' ' < $p/cmdline | grep tsukuroi-r42 -> pid/cwd
git -C <lane> diff --stat -- tools/tsukuroi-census.sh
git -C <lane> diff -- tools/tsukuroi-census.sh | head -80
sha256sum <lane>/tools/tsukuroi-census.sh   -> 7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9
git -C <lane> cat-file -p HEAD:tools/tsukuroi-census.sh | sha256sum -> 46d62a24709ece8efbcd231f4c269bd5b3791237e3c78ac7433fb0115494f1b1
stat -c '%s bytes mtime=%y ctime=%z' <lane>/tools/tsukuroi-census.sh <lane>/corpus/knowledge/btrfs-scrub-record-r42.md
git -C <lane> diff -- corpus/knowledge/btrfs-scrub-record-r42.md
grep -rn -F '$1 == n && !f' <lane>/.ufo/waves/round-42/w1
grep -rn -F 'ABSENT' <lane>/.ufo/waves/round-42/w1 --include='*.md' | grep -F '<<<'
find <lane>/.ufo/waves/round-42/w1 -type l
find /fast/scratch/hyaku -maxdepth 1 -newer <marker> -mindepth 1
# marker = tsukuroi-shokunin/.ufo/waves/round-42/make-w1-spec.py (mtime 2026-10-26T16:36)
