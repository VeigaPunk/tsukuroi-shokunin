# planner-measures — round 1 (kaika), seat W2RoundTsukuroi-8.TsuR1Planner-3

(Verbatim L2 output persisted by the L1 so the pointer resolves at closure; L2 = author-side advisory seat, not a non-author verifier. Source transcript: history://W2RoundTsukuroi-8.TsuR1Planner-3 — session-scoped, this file is the durable copy.)

Axes: A adjacency; B coverage / `sources-registry`; C freshness. Baseline values were measured from the read-only archive of `9b70381`; subsequent corpus commands run from `<wt>` root: `mkdir -p /tmp/tsu-plan && git -C <wt> archive 9b70381 | tar -x -C /tmp/tsu-plan`.

**A — adjacency.** Valid route states: **0/7 → 7/7**; command: `jq '[.routes[]|select(.state=="prepared" or .state=="reported" or .state=="acknowledged" or .state=="accepted" or .state=="resolved")]|length' corpus/knowledge/adjacency-handoffs-fleet-r1.json`. Falsifier: any route lacks a valid state.

Source pins: **5/8 → 8/8**; command: `jq -r '.source_pins|to_entries[]|[.key,.value]|@tsv' corpus/knowledge/adjacency-handoffs-fleet-r1.json | while IFS="$(printf '\t')" read -r rel want; do lane=${rel#../}; lane=${lane%/PROVINCE.md}; got=$(git -C "/home/vgpnk/Projects/shokunin/$lane" show HEAD:PROVINCE.md | sha256sum | cut -d' ' -f1); printf '%s %s %s\n' "$lane" "$want" "$got"; done | awk '$2==$3 {m++} END {printf "%d/%d\n",m+0,NR}'`.

Report locator baseline: `grep -nF 'TSUKUROI-F1-MEM-01' .ufo/reports/round-1/tsukuroi.md` finds line 70, but that is a negative contrast, not a positive receipt. Falsifier: missing positive packet citation in the round report; a literal hit alone does not establish reporting.

**B — sources census.** `corpus/SOURCES.md` is absent at baseline: **0 rows**. The frozen contract lists seven census commands; check 8 below verifies its four required headings. Run the guarded checks in one shell after `S=corpus/SOURCES.md`:
1. **Rows 0 → 32:** `if test -f "$S"; then grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$S"; else echo 0; fi`
2. **Malformed 0 → 0:** `if test -f "$S"; then awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' "$S"; else echo 0; fi`
3. **Tier histogram baseline A/B/C=0:** `if test -f "$S"; then awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5;gsub(/[[:space:]]/,"",t);n[t]++} END{for(k in n) printf "%s=%d\n",k,n[k]}' "$S" | LC_ALL=C sort; else printf 'A=0\nB=0\nC=0\n'; fi`
4. **Status histogram baseline queued/mined/rejected=0:** `if test -f "$S"; then awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9;gsub(/[[:space:]]/,"",s);n[s]++} END{for(k in n) printf "%s=%d\n",k,n[k]}' "$S" | LC_ALL=C sort; else printf 'queued=0\nmined=0\nrejected=0\n'; fi`
5. **Duplicate IDs baseline none:** `if test -f "$S"; then awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2;gsub(/[[:space:]]/,"",i);print i}' "$S" | LC_ALL=C sort | uniq -d; fi`
6. **Enum violations baseline none:** `if test -f "$S"; then awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9;gsub(/[[:space:]]/,"",i);gsub(/[[:space:]]/,"",k);gsub(/[[:space:]]/,"",t);gsub(/[[:space:]]/,"",s);if(t!~/^[ABC]$/)print "tier",i,t;if(s!~/^(queued|mined|rejected)$/)print "status",i,s;if(k!~/^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/)print "kind",i,k;if(t=="A"&&k=="community")print "tier-inflation",i}' "$S"; fi`
7. **Missing mined paths baseline none:** `if test -f "$S"; then awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9;gsub(/[[:space:]]/,"",s);if(s=="mined"){n=split($12,a,/[,;]/);for(j=1;j<=n;j++){p=a[j];gsub(/^[[:space:]]+|[[:space:]]+$/,"",p);if(p!=""&&p!="—")print p}}}' "$S" | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done; fi`
8. **Required headings baseline 0 → 4:** `if test -f "$S"; then grep -cE '^## (Registry|Paths|Search log|Leads \(unopened\))([[:space:]]|$)' "$S"; else echo 0; fi`

New entries: **0/4 → 4/4**; command: `for f in corpus/knowledge/arch-news-gate-2026.md corpus/knowledge/pacnew-plane.md corpus/knowledge/initramfs-v42-sysroot-recovery.md corpus/knowledge/snapper-eacces-mechanism.md; do test -f "$f" && n=$((n+1)); done; printf '%d/4\n' "${n:-0}"`.

ART §1.2 sweep baselines and commands: news **0**, `grep -rliE 'archlinux\.org/news|arch news|informant' corpus SKILL.md PROVINCE.md | wc -l`; pacnew **0**, `grep -rliE 'pacnew|pacsave|pacdiff' corpus/ SKILL.md PROVINCE.md | wc -l`.

Recovery **0**, `grep -rliE 'rescue\.target|emergency\.target|break=premount|rd\.systemd|debug_shell|arch-chroot|init=/bin/sh' corpus SKILL.md | wc -l`; ALA **0**, `grep -rliE 'archive\.archlinux\.org|Arch Linux Archive' corpus SKILL.md | wc -l`.

Sandbox **0**, `grep -rliE 'DisableSandbox|Landlock|disable-sandbox' corpus SKILL.md | wc -l`; DAC **0**, `grep -rlE 'CAP_DAC_OVERRIDE|mode 555|\b555\b' corpus/knowledge | wc -l`.

Systemd ≥258 **1**, `grep -rliE 'systemd 26[0-9]|v26[0-9]\b|cgroup v1' corpus SKILL.md | wc -l`; mkinitcpio drop-ins **1**, `grep -rliE 'mkinitcpio\.conf\.d|omarchy_hooks' corpus SKILL.md | wc -l`. Claim B falsifier: fewer than 32 registry rows, any census violation, fewer than four entries, or news/pacnew/recovery/DAC sweep still 0.

Coverage-map rows **10 → 14**, `grep -c '^| `' corpus/README.md`; QUALITY criteria **5 → 9**, `grep -cE '^[0-9]+\.' corpus/QUALITY.md`.

**C — freshness.** D1–D5 errata blocks **0 → 5**, `grep -hE '^## Erratum \(2026-10-19, fleet round 1\) — D[1-5]([[:space:]]|$)' corpus/knowledge/*.md | wc -l`. Doctrine-citing errata freshness metric **0 → ≥1**, `awk 'FNR==1{if(inside&&doc)n++;inside=doc=0} /^## Erratum \(2026-10-19, fleet round 1\)/{if(inside&&doc)n++;inside=1;doc=0;next} inside&&/(S010|ArchWiki System maintenance)/{doc=1} END{if(inside&&doc)n++;print n+0}' corpus/knowledge/*.md`. Falsifier: fewer than five D1–D5 blocks or no erratum citing S010/doctrine.

Valid last rechecks **0/25 → 29/29**; command: `for f in corpus/knowledge/*.md; do awk '/^recheck:/ {last=$0} END {if(last!="") print last}' "$f"; done | grep -Ec '[0-9]{4}-[0-9]{2}-[0-9]{2}|\b[0-9]+d\b|on-release' || true`; note count `find corpus/knowledge -maxdepth 1 -type f -name '*.md' -print | wc -l` is **25 → 29**.

Missing-key counts: `grep -L '^source:' corpus/knowledge/*.md | wc -l` **6 → 0**; `grep -L '^verified-at:' corpus/knowledge/*.md | wc -l` **11 → 0**; `grep -L '^recheck:' corpus/knowledge/*.md | wc -l` **11 → 0**. Falsifier: any missing key or fewer than 29 valid last rechecks.

Append-only D1 sweep is a retention floor, **9 → ≥9**, not a reduction target: `grep -rnE 'sudo pacman -Sy`|[Oo]perator `-Sy`|then `-Sy`|`-Sy` then|`-Sy` and re-run' corpus/knowledge | wc -l`.

No-harm checks: selftest run once in `/tmp/tsu-plan`, `bash tools/tsukuroi-census.sh --selftest` → **80/80, rc=0**; SKILL bound `wc -l < SKILL.md` → **1636**, cap **≤1636**; `git -C <wt> diff --numstat 9b70381 -- corpus/knowledge | awk '$2>0'` → **no output**.

Coupling: A’s route/pin counts are separable from B/C, but B’s registry rows must support C’s `source:` metadata and errata citations; B’s four new notes also enter C’s key/recheck denominators. Coverage-map and QUALITY counts are supporting B measures. The seven bare-`-Sy` hits must remain due to append-only history.

Hard blockers: none to measurement. The frozen SOURCES contract publishes seven census checks, so the eighth heading check is explicitly supplemental; a literal packet-name hit alone is not proof of reporting.
