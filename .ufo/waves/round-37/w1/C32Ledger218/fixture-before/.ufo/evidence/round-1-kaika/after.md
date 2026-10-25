# after — fleet round 1 (kaika), measured on the worktree tree being committed

capture: 2026-10-19T22:33:26Z; base 9b70381; cwd = lane worktree root

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
34
```

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
```

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=31 B=1 C=2 
```

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=26 queued=5 rejected=3 
```

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d; echo '(dup check end)'
(dup check end)
```

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md; echo '(enum check end)'
(enum check end)
```

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done; echo '(missing check end)'
(missing check end)
```

```
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;s=$9;gsub(/[[:space:]]/,"",i);gsub(/[[:space:]]/,"",s); if(s=="mined"){n=split($12,a,/[,;]/); for(j=1;j<=n;j++){p=a[j];gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if(p!=""&&p!="—") print i, p}}}' corpus/SOURCES.md | while read -r i p; do grep -qw "$i" "$p" || echo "nocite: $i $p"; done; echo '(reverse-cite check end — supplemental)'
(reverse-cite check end — supplemental)
```

```
$ jq '[.routes[]|select(has("state"))]|length' corpus/knowledge/adjacency-handoffs-fleet-r1.json
7
```

```
$ jq -c '[.routes[]|.id+":"+.state], .source_pin_recheck.current_match_count, .source_pin_recheck.anchors_hold_count' corpus/knowledge/adjacency-handoffs-fleet-r1.json
["ADJ-01:contract-only","ADJ-02:contract-only","ADJ-03:contract-only","ADJ-04:prepared","ADJ-05:contract-only","ADJ-06:contract-only","ADJ-07:contract-only"]
5
8
```

```
$ jq -r '.source_pins|to_entries[]|.key+" "+.value' corpus/knowledge/adjacency-handoffs-fleet-r1.json | while read p h; do l=$(basename $(dirname $p)); c=$(git -C /home/vgpnk/Projects/shokunin/$l show HEAD:PROVINCE.md | sha256sum | cut -c1-64); [ "$h" = "$c" ] && echo MATCH $l || echo DRIFT $l; done
DRIFT kama-shokunin
MATCH kagi-shokunin
MATCH mado-shokunin
MATCH mori-shokunin
MATCH kumitate-shokunin
DRIFT kaidoku-shokunin
DRIFT revenger-shokunin
MATCH tameshi-shokunin
```

```
$ grep -rn 'TSUKUROI-F1-MEM-01' /home/vgpnk/Projects/shokunin/*-shokunin --include=*.md --include=*.json | grep -v '^/home/vgpnk/Projects/shokunin/tsukuroi-shokunin' | wc -l
0
```

```
$ ls corpus/knowledge/*.md | wc -l; grep -cE '^[0-9]+\.' corpus/QUALITY.md; grep -c '^| `' corpus/README.md
30
13
15
```

```
$ for k in source verified-at recheck; do echo "no-$k $(grep -L "^$k:" corpus/knowledge/*.md | wc -l)"; done
no-source 0
no-verified-at 0
no-recheck 0
```

```
$ for f in $(git ls-tree --name-only 9b70381 corpus/knowledge/ | grep '\.md$'); do grep '^recheck:' "$f" | tail -1 | grep -qE '[0-9]{4}-[0-9]{2}-[0-9]{2}|\b[0-9]+d\b|on-release' && echo ok; done | wc -l
25
```

```
$ grep -lE '^## Erratum \(2026-10-19, fleet round 1\) — D[1-5]' corpus/knowledge/*.md | wc -l; grep -hoE '^## Erratum \(2026-10-19, fleet round 1\) — D[1-5]' corpus/knowledge/*.md | sort | uniq -c
7
      6 ## Erratum (2026-10-19, fleet round 1) — D1
      1 ## Erratum (2026-10-19, fleet round 1) — D2
      1 ## Erratum (2026-10-19, fleet round 1) — D3
      1 ## Erratum (2026-10-19, fleet round 1) — D4
      1 ## Erratum (2026-10-19, fleet round 1) — D5
```

```
$ grep -rnE 'sudo pacman -Sy`|[Oo]perator `-Sy`|then `-Sy`|`-Sy` then|`-Sy` and re-run' corpus/knowledge | wc -l
14
```

```
$ grep -rliE 'archlinux\.org/news|arch news|informant' corpus SKILL.md PROVINCE.md | wc -l
5
```

```
$ grep -rliE 'pacnew|pacsave|pacdiff' corpus SKILL.md PROVINCE.md | wc -l
6
```

```
$ grep -rliE 'rescue\.target|emergency\.target|break=premount|rd\.systemd|debug_shell|arch-chroot|init=/bin/sh' corpus SKILL.md PROVINCE.md | wc -l
3
```

```
$ grep -rliE 'archive\.archlinux\.org|Arch Linux Archive' corpus SKILL.md PROVINCE.md | wc -l
1
```

```
$ grep -rliE 'DisableSandbox|Landlock|disable-sandbox' corpus SKILL.md PROVINCE.md | wc -l
1
```

```
$ grep -rlE 'CAP_DAC_OVERRIDE|mode 555|\b555\b' corpus/knowledge | wc -l
2
```

```
$ grep -c '^## Mistakes' corpus/lessons/round-1.md; grep -c '^| [MD][0-9]' corpus/lessons/round-1.md
1
19
```

```
$ wc -l SKILL.md; wc -c SKILL.md
1660 SKILL.md
146784 SKILL.md
```

```
$ awk '/^## Capabilities/{f=1;next} /^## /{f=0} f && /^\| [a-z]/' SCORECARD.md | wc -l
2
```

```
$ for f in $(git diff --name-only 9b70381 -- corpus PROVINCE.md SKILL.md SCORECARD.md LOG.md); do n=$(git show 9b70381:$f | wc -c); cmp -s <(git show 9b70381:$f) <(head -c $n $f) || echo "not-prefix $f"; done; git diff 9b70381 --numstat -- corpus/README.md corpus/knowledge/adjacency-handoffs-fleet-r1.json SCORECARD.md
not-prefix SCORECARD.md
not-prefix corpus/README.md
not-prefix corpus/knowledge/adjacency-handoffs-fleet-r1.json
34	1	SCORECARD.md
19	0	corpus/README.md
34	0	corpus/knowledge/adjacency-handoffs-fleet-r1.json
```

```
$ bash tools/tsukuroi-census.sh --selftest 2>&1 | tail -1; echo rc=${PIPESTATUS[0]}
TSUKUROI_CENSUS_SELFTEST: PASS (80 cases, 80 passed, 0 failed)
rc=0
```

```
$ git status --porcelain tools/ | wc -l
0
```

Note: SCORECARD.md is not a byte-prefix because the 2026-10-16 "— none yet —" capabilities placeholder row was replaced by the two real rows (1 line removed); SCORECARD is the lane ledger, not an append-only corpus file. README rows and JSON keys are insertions (0 deletions).
