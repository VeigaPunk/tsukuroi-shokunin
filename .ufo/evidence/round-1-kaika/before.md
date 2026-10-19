# BEFORE measurements — lane `tsukuroi`, fleet round 1 (kaika)

- Base commit (full): `9b70381c54a040e8775b43a61245b088acefb65f`
- Commit date: `2026-10-17T00:28:34-03:00`
- Lane worktree: `/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/tsukuroi-shokunin`
- Worktree HEAD at capture: `9b70381c54a040e8775b43a61245b088acefb65f`; `git status --porcelain` = 0 lines (clean)
- UTC capture window: `2026-10-19T22:03:02Z` → `2026-10-19T22:03:37Z`
- Immunity to concurrent writers: every measurement below ran with bash `cwd=/tmp/tsu-base`, a `git archive 9b70381` extraction. No command read the live worktree. `/tmp/tsu-base` is scratch and is not evidence; the re-runnable evidence is the lane-repo commit plus the extraction command.

## 0. Extraction and identity

Command (run in `/tmp`):

```bash
rm -rf /tmp/tsu-base && mkdir -p /tmp/tsu-base && git -C /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/tsukuroi-shokunin archive 9b70381 | tar -x -C /tmp/tsu-base && echo EXTRACT_OK && ls /tmp/tsu-base | wc -l
```

stdout:

```text
EXTRACT_OK
11
```

Command:

```bash
git -C /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/tsukuroi-shokunin rev-parse 9b70381; date -u +%Y-%m-%dT%H:%M:%SZ
```

stdout:

```text
9b70381c54a040e8775b43a61245b088acefb65f
2026-10-19T22:03:02Z
```

Command:

```bash
git -C /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/tsukuroi-shokunin log -1 --format='%H %cI' 9b70381; git -C /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/tsukuroi-shokunin rev-parse --show-toplevel; git -C /home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/tsukuroi-shokunin status --porcelain | head -5
```

stdout:

```text
9b70381c54a040e8775b43a61245b088acefb65f 2026-10-17T00:28:34-03:00
/home/vgpnk/Projects/shokunin/.tower/worktrees/kaika/tsukuroi-shokunin
```

(no status lines: clean)

## 1. SOURCES registry absence

Command (cwd=/tmp/tsu-base):

```bash
set +e; ls corpus/SOURCES.md; echo "rc=$?"
```

stdout+stderr:

```text
ls: cannot access 'corpus/SOURCES.md': No such file or directory
rc=2
```

## 2. Corpus holdings

Command (cwd=/tmp/tsu-base):

```bash
ls corpus/knowledge/*.md | wc -l; ls corpus/lessons/*.md | wc -l; grep -cE '^[0-9]+\.' corpus/QUALITY.md; grep -c '^| `' corpus/README.md
```

stdout (4 lines, in order):

```text
25
1
5
10
```

## 3. Contract keys `source:` / `verified-at:` / `recheck:`

Command (cwd=/tmp/tsu-base):

```bash
echo -n 'nosource '; grep -L '^source:' corpus/knowledge/*.md | wc -l; echo -n 'noverified '; grep -L '^verified-at:' corpus/knowledge/*.md | wc -l; echo -n 'norecheck '; grep -L '^recheck:' corpus/knowledge/*.md | wc -l
```

stdout:

```text
nosource 6
noverified 11
norecheck 11
```

Command (cwd=/tmp/tsu-base):

```bash
for f in corpus/knowledge/*.md; do grep '^recheck:' "$f" | tail -1 | grep -qE '[0-9]{4}-[0-9]{2}-[0-9]{2}|\b[0-9]+d\b|on-release' && echo ok; done | wc -l
```

stdout:

```text
0
```

## 4. Adjacency ledger lifecycle instantiation

Command (cwd=/tmp/tsu-base):

```bash
jq '[.routes[]|select(has("state"))]|length' corpus/knowledge/adjacency-handoffs-fleet-r1.json; jq '.routes|length' corpus/knowledge/adjacency-handoffs-fleet-r1.json; jq -r '.source_pins|keys[]' corpus/knowledge/adjacency-handoffs-fleet-r1.json
```

stdout:

```text
0
7
../kagi-shokunin/PROVINCE.md
../kaidoku-shokunin/PROVINCE.md
../kama-shokunin/PROVINCE.md
../kumitate-shokunin/PROVINCE.md
../mado-shokunin/PROVINCE.md
../mori-shokunin/PROVINCE.md
../revenger-shokunin/PROVINCE.md
../tameshi-shokunin/PROVINCE.md
```

## 5. PROVINCE source-pin currency

Command (cwd=/tmp/tsu-base):

```bash
jq -r '.source_pins|to_entries[]|.key+" "+.value' corpus/knowledge/adjacency-handoffs-fleet-r1.json | while read p h; do l=$(basename $(dirname $p)); c=$(git -C /home/vgpnk/Projects/shokunin/$l show HEAD:PROVINCE.md | sha256sum | cut -c1-64); [ "$h" = "$c" ] && echo MATCH $l || echo DRIFT $l; done
```

stdout:

```text
DRIFT kama-shokunin
MATCH kagi-shokunin
MATCH mado-shokunin
MATCH mori-shokunin
MATCH kumitate-shokunin
DRIFT kaidoku-shokunin
DRIFT revenger-shokunin
MATCH tameshi-shokunin
```

Command (same pipeline, `grep -c MATCH`):

```bash
jq -r '.source_pins|to_entries[]|.key+" "+.value' corpus/knowledge/adjacency-handoffs-fleet-r1.json | while read p h; do l=$(basename $(dirname $p)); c=$(git -C /home/vgpnk/Projects/shokunin/$l show HEAD:PROVINCE.md | sha256sum | cut -c1-64); [ "$h" = "$c" ] && echo MATCH $l || echo DRIFT $l; done | grep -c MATCH
```

stdout:

```text
5
```

Sibling HEADs at capture (command run cwd=/tmp/tsu-base):

```bash
for l in kagi kaidoku kama kumitate mado mori revenger tameshi; do printf '%s ' "$l"; git -C /home/vgpnk/Projects/shokunin/$l-shokunin rev-parse --short HEAD; done
```

stdout:

```text
kagi aea7a43
kaidoku de77d75
kama 35e9175
kumitate 16a5441
mado e1d81d4
mori 20e2255
revenger 8bbcb4e
tameshi 4eb4cf3
```

## 6. ART dossier §1.2 coverage sweeps (0-hit baseline)

Command (cwd=/tmp/tsu-base):

```bash
echo -n 'news '; grep -rliE 'archlinux\.org/news|arch news|informant' corpus SKILL.md PROVINCE.md | wc -l; echo -n 'pacnew '; grep -rliE 'pacnew|pacsave|pacdiff' corpus/ SKILL.md PROVINCE.md | wc -l; echo -n 'recovery '; grep -rliE 'rescue\.target|emergency\.target|break=premount|rd\.systemd|debug_shell|arch-chroot|init=/bin/sh' corpus SKILL.md | wc -l
```

stdout:

```text
news 0
pacnew 0
recovery 0
```

Command (cwd=/tmp/tsu-base):

```bash
echo -n 'ala '; grep -rliE 'archive\.archlinux\.org|Arch Linux Archive' corpus SKILL.md | wc -l; echo -n 'sandbox '; grep -rliE 'DisableSandbox|Landlock|disable-sandbox' corpus SKILL.md | wc -l; echo -n 'dac '; grep -rlE 'CAP_DAC_OVERRIDE|mode 555|\b555\b' corpus/knowledge | wc -l
```

stdout:

```text
ala 0
sandbox 0
dac 0
```

## 7. Errata, D1 doctrine sweep, mistakes

Command (cwd=/tmp/tsu-base):

```bash
grep -rc '^## Erratum (2026-10-19' corpus/knowledge | awk -F: '{s+=$2} END{print s+0}'; echo -n 'd1 '; grep -rnE 'sudo pacman -Sy|[Oo]perator `-Sy`|then `-Sy`|`-Sy` then|`-Sy` and re-run' corpus/knowledge | wc -l; echo -n 'mistakes '; grep -c '^## Mistakes' corpus/lessons/round-1.md
```

stdout (command exit code 1, from the final `grep -c` finding no match):

```text
0
d1 9
mistakes 0
```

## 8. SKILL size and capability rows

Command (cwd=/tmp/tsu-base):

```bash
wc -l SKILL.md; wc -c SKILL.md; awk '/^## Capabilities/{f=1;next} /^## /{f=0} f && /^\| [a-z]/' SCORECARD.md | wc -l
```

stdout:

```text
1636 SKILL.md
144943 SKILL.md
0
```

Observation for the capability sweep: `SCORECARD.md:157-166` at this commit holds `## Capabilities`, its header row, separator, and the placeholder row `| — none yet — |`; no lowercase-leading capability row exists, so the sweep's 0 is the intended count (placeholder, not capability).

## 9. Census self-test

Command (cwd=/tmp/tsu-base; output piped through `tail -2`, rc read from `PIPESTATUS`):

```bash
set +e; bash tools/tsukuroi-census.sh --selftest 2>&1 | tail -2; echo "rc=${PIPESTATUS[0]}"
```

stdout:

```text
PASS cli: --help prints usage and exits 0 (S10-2) (exit 0)
TSUKUROI_CENSUS_SELFTEST: PASS (80 cases, 80 passed, 0 failed)
rc=0
```

## 10. Metric summary (all at `9b70381`, 2026-10-19T22:03Z)

| metric | command (all cwd=/tmp/tsu-base) | value |
|---|---|---|
| SOURCES.md present | `ls corpus/SOURCES.md` | absent, rc=2 |
| knowledge notes | `ls corpus/knowledge/*.md \| wc -l` | 25 |
| lesson files | `ls corpus/lessons/*.md \| wc -l` | 1 |
| QUALITY criteria | `grep -cE '^[0-9]+\.' corpus/QUALITY.md` | 5 |
| README coverage rows | `grep -c '^| `' corpus/README.md` | 10 |
| notes lacking `source:` | `grep -L '^source:' corpus/knowledge/*.md \| wc -l` | 6 |
| notes lacking `verified-at:` | `grep -L '^verified-at:' corpus/knowledge/*.md \| wc -l` | 11 |
| notes lacking `recheck:` | `grep -L '^recheck:' corpus/knowledge/*.md \| wc -l` | 11 |
| date/cadence recheck lines | cadence loop over notes | 0 |
| routes with `state` | `jq '[.routes[]\|select(has("state"))]\|length' …` | 0 (of 7) |
| PROVINCE pins matching HEAD | pin-currency loop `\| grep -c MATCH` | 5 (of 8) |
| pins drifted | same loop | 3 (kama, kaidoku, revenger) |
| news sweep | `grep -rliE 'archlinux\.org/news\|arch news\|informant' …` | 0 |
| pacnew sweep | `grep -rliE 'pacnew\|pacsave\|pacdiff' …` | 0 |
| recovery sweep | `grep -rliE 'rescue\.target\|…\|init=/bin/sh' …` | 0 |
| ALA sweep | `grep -rliE 'archive\.archlinux\.org\|Arch Linux Archive' …` | 0 |
| sandbox sweep | `grep -rliE 'DisableSandbox\|Landlock\|disable-sandbox' …` | 0 |
| DAC sweep | `grep -rlE 'CAP_DAC_OVERRIDE\|mode 555\|\b555\b' corpus/knowledge` | 0 |
| errata blocks dated 2026-10-19 | `grep -rc '^## Erratum (2026-10-19' corpus/knowledge \| awk …` | 0 |
| D1 bare-`-Sy` advice lines | `grep -rnE 'sudo pacman -Sy\|…' corpus/knowledge \| wc -l` | 9 |
| `## Mistakes` section | `grep -c '^## Mistakes' corpus/lessons/round-1.md` | 0 |
| SKILL.md lines / bytes | `wc -l SKILL.md`; `wc -c SKILL.md` | 1636 / 144943 |
| capability rows | `awk '/^## Capabilities/{…}' SCORECARD.md \| wc -l` | 0 |
| census self-test | `bash tools/tsukuroi-census.sh --selftest` (tail -2) | PASS 80/80, rc=0 |

## Limits

- These are point-in-time reads of commit `9b70381` only; they do not observe the live worktree, so later round-1 edits cannot affect them.
- The pin-currency check resolves sibling repositories at their own `HEAD`, which is mutable; the exact sibling HEADs used are recorded in §5.
- The census self-test is hermetic per its own report; the last-2-lines capture is an intentional truncation of that command's output.
