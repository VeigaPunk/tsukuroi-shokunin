2026-11-03T23:27:00Z
# N1Sentinel — boundary and side-effect sweep, round 69 wave w1

Lane HEAD 920a9eea3c5c5400567be0e96141014f338973df. Wave dispatched 20:18:43 -0300 (23:18:43Z). Sweep window 23:18:50Z–23:27Z, two snapshots because seats were still writing:
- snapshot A = 23:25:10Z (63 files under `.ufo/waves/round-69/`)
- snapshot B = 23:26:30Z (65 files; `probes/SC1Scribe/quote-check.txt` and `drafts/c1/{note,lesson,sources-rows}.md` were rewritten in between)

Read-only throughout: no sudo, no pacman transaction, no service action, no lane mutation. The only git writes made by this seat were inside `/fast/scratch/hyaku/tsukuroi-r69/N1Sentinel/clone`, always with `-C` on that path.

## 1. Forbidden-action sweep

Scanner (inline, over `w1-spec.json`, `w1-dispatch.json`, `before/`, `drafts/`, `probes/`):

```
sudo|pkexec|doas|\bsu -|pacman -[SRU][a-z]*|systemctl (start|stop|restart|enable|disable|daemon-reload)
|journalctl --(rotate|vacuum)|dmesg -[cC]|snapper (create|rollback|set-config)
|btrfs (scrub|balance|subvolume|device stats)|pkill|killall|kill -9
|git (commit|push|stash|checkout|reset|pull|add|rm|mv|clean|rebase|merge)
|op://|id_rsa|/etc/shadow|var/lib/pacman|os\.system|urllib|requests\.|wget
```

$ python3 <inline scanner>
TOTAL_HIT_LINES 16     # snapshot A
$ python3 <inline scanner>
TOTAL_HIT_LINES 36     # snapshot B, including 24 self-quoted lines of this very receipt
rc=0

Excluding this receipt's own quotations, snapshot B has 13 hit lines. Against A: 4 lines left because `probes/SC1Scribe/quote-check.txt` was rewritten at 23:24:59Z (see "Provenance drift"), and 1 line arrived at 23:27Z in `probes/R1Reviewer/attack.md:810` (a quoted corrected note snapshot, same `recheck:` text as row 5). Snapshot B+ = 23:27Z is the closing cutoff for this sweep; seats were still writing when it closed.

| # | file:line | token(s) | class | disposition |
|---|---|---|---|---|
| 1 | w1-spec.json:5 | sudo, pkexec, pacman -S, systemctl start, journalctl --rotate, dmesg -c, snapper create, btrfs scrub, btrfs device stats, var/lib/pacman, pkill, op:// | DECL | wave-context string: the seat guard prose ("NEVER sudo …"); no invocation |
| 2 | w1-spec.json:155 | sudo, pkexec, pacman -S, journalctl --rotate, dmesg -c, var/lib/pacman, pkill | DECL | this seat's own item text embedded in the spec (prohibition list) |
| 3 | w1-dispatch.json:187 | as row 1 | DECL | same context string, dispatch copy |
| 4 | w1-dispatch.json:252 | as row 2 | DECL | same item string, dispatch copy |
| 5 | drafts/c1/note.md:3 | var/lib/pacman | DECL | `recheck:` prose that steers package readings to *file reads* (`ls -d …/local/linux-*`, the `desc` markers) and states "no package-manager invocation is prescribed" |
| 6 | probes/S2Scout-host.md:3 | sudo | DECL | header line `mode=read-only (no sudo, no pacman transaction, …)` |
| 7 | probes/SC1Scribe/pacman-localdesc.txt:2 | var/lib/pacman | READ | `$ sed -n "1,6p" …/linux-7.2.11.arch1-1/desc` |
| 8 | probes/SC1Scribe/pacman-localdesc.txt:11 | var/lib/pacman | READ | `$ grep -nE "%(NAME|VERSION)%" …/desc` |
| 9 | probes/SC1Scribe/pacman-localdesc.txt:16 | var/lib/pacman | READ | `$ awk "/%NAME%/{getline;print} …" …/desc` — print only, no `-i` |
| 10 | probes/C1Connector/overlap.md:28 | git merge (merge-base) | READ | `$ git merge-base --is-ancestor acce353b 920a9ee` — ancestry query; `-C` absent, cwd unrecorded (nit only, no mutation possible) |
| 11 | probes/R1Reviewer/attack.md:72 | var/lib/pacman | DECL | quotation of the note's `recheck:` line under review |
| 12 | probes/R1Reviewer/attack.md:619 | sudo | DECL | citation of a round-27 capture: "(sha256 …, 2026-10-22T15:55:13Z, no sudo)" — asserts absence |
| 13 | probes/SC1Scribe/quote-check.txt:20 (snapshot A) | var/lib/pacman ×2 | READ | `$ ls -d /var/lib/pacman/local/linux-[0-9]* …` — listing, rc recorded; line removed by the 23:24:59 rewrite |
| 14 | probes/SC1Scribe/quote-check.txt:21 (A) | var/lib/pacman | READ | output line of row 13; removed by the rewrite |
| 15 | probes/SC1Scribe/quote-check.txt:22 (A) | var/lib/pacman | READ | output line of row 13; removed by the rewrite |
| 16 | probes/SC1Scribe/quote-check.txt:25 (A) | var/lib/pacman | READ | `$ grep -E "^(NAME|VERSION)=" …/desc`; removed by the rewrite |
| 17 | probes/R1Reviewer/attack.md:810 (B+) | var/lib/pacman | DECL | "Corrected note snapshot" quoted inside a markdown fence — the note's `recheck:` prose again, with the same "no package-manager invocation is prescribed" clause |

Classes across the window: DECL = 9, READ = 8, INVOCATION = 0.

The pacman-DB reads are readable and immutable to uid 1000 (my own observation, not the seat's):

$ id -u
1000
$ head -2 /var/lib/pacman/local/linux-7.2.11.arch1-1/desc
%NAME%
linux
rc=0
$ test -w /var/lib/pacman/local/linux-7.2.11.arch1-1/desc && echo WRITABLE || echo NOT_WRITABLE
NOT_WRITABLE

Sandbox-only git mutations (`add`/`commit` are forbidden outside a sandbox clone):

$ grep -R -n -E 'git -C /fast/scratch/hyaku/tsukuroi-r69/[A-Za-z0-9]+/clone[^|]*(add|commit|rm|mv|reset|checkout|stash|clean|merge|rebase|push)' probes drafts | wc -l
28
$ grep -R -h -o -E 'git -C [^ ]+' probes drafts | sort | uniq -c | sort -rn
     56 git -C /fast/scratch/hyaku/tsukuroi-r69/E2Counter/clone
     27 git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
      2 git -C tsukuroi-shokunin
      2 git -C "$d"
      1 git -C <sib>
rc=0
$ grep -R -h -o -E 'git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin [a-z-]+' probes drafts | sort | uniq -c | sort -rn
     19 … show
      3 … rev-parse
      3 … cat-file
      2 … ls-tree
rc=0

All 28 mutating lines carry `-C` on the seat's own `--shared` clone under `/fast/scratch/hyaku/tsukuroi-r69/E2Counter/clone`, and the throwaway identity is supplied only by `-c user.name=…E2Counter fixture -c user.email=e2counter@fixture.invalid` inside that clone. Every lane-targeted call is a read verb (`show`, `rev-parse`, `cat-file`, `ls-tree`); the relative calls (`git -C tsukuroi-shokunin rev-parse/grep`, `git -C "$d" rev-parse/grep` in a fixture loop) are read-only; `-C <sib>` is prose. No `jj` command appears anywhere. 0 mutating git/jj calls outside a sandbox clone.

Network reads: 8 `curl` lines, all of the named source or prose — `probes/S1Scout-sources.md:28,34,36` (raw.githubusercontent.com gregkh/linux v7.2.11, rc recorded per file), `probes/E3Hygiene/r68-checklist.txt:23,24,25` and `r69-checklist.txt:30` (checklist rows with `<file>/<url>` placeholders, not executed), `probes/R1Reviewer/attack.md:299` (prose: "method curl -sS --max-time 60"). No other host named.

Committed receipts: `grep -R -n -E '<same alternation>' before/` → 0 matches, rc=1. No forbidden token in any pre-declaration capture.

### Provenance drift (OBSERVATION, not a breach)

`probes/SC1Scribe/quote-check.txt` was rewritten at 23:24:59Z (947 B, 20:24:59 -0300): four pacman-DB lines present at snapshot A are gone, and the file now holds the `sha256sum -c SHA256SUMS` check only. The seat owns the file and the rewrite removes evidence rather than adding claims; the same pacman-DB reads survive in `probes/SC1Scribe/pacman-localdesc.txt:mm 2,11,16`. A receipt that changes after it is first written cannot be treated as a frozen record — the L1 should cite the final bytes and the digest, not line numbers read earlier.

## 2. Misroot list

$ git -C /home/vgpnk/Projects/shokunin status --porcelain
 M .scratch/goal-20261103-hyaku-run15.md
 M .scratch/run15-state.json
 M .ufo/l0-questions.md
?? .scratch/run13-state.json
?? .scratch/run15-kernel.py
?? after
rc=0

$ find /home/vgpnk/Projects/shokunin -maxdepth 6 -path '*/tsukuroi-shokunin/*' -prune -o -path '*/.git/*' -prune -o -type f -newermt '2026-11-03 23:17:00 UTC' -print
(no output)
rc=0
$ find /home/vgpnk/Projects/shokunin -maxdepth 3 -type f -newermt '2026-11-03 23:17:00 UTC' -not -path '*/tsukuroi-shokunin/*' -not -path '*/.git/*' -print
(no output)
rc=0
$ find /home/vgpnk/Projects/shokuknow /home/vgpnk/Projects/shokunin/considerthese -maxdepth 3 -type f -newermt '2026-11-03 23:17:00 UTC' -not -path '*/.git/*' -print
(no output)
rc=0
$ find /home/vgpnk/Projects/shokunin -maxdepth 2 \( -name w1 -o -name drafts -o -name probes -o -name round-69 \) -not -path '*/.git/*'
(no output)
rc=0

Fleet-root untracked files that name the lane (mtime, local -0300):

| path | mtime | what it names | written by a seat this wave? |
|---|---|---|---|
| .scratch/run13-state.json | 2026-10-30 16:05:50 | `"tsukuroi": {`, `"tsukuroi": 53` | no — 4 days before the wave |
| .scratch/run15-kernel.py | 2026-11-03 19:24:49 | orchestrator loader (`%load …run15-kernel.py`) | no — 54 min before dispatch |
| after | 2026-11-03 20:05:14 | `== SCORECARD diff base-` (24 B) | no — before dispatch |
| .scratch/run15-state.json (M) | 2026-11-03 20:16:24 | 2 lane matches | no — orchestrator state, 2 min before dispatch |
| .scratch/goal-…-run15.md (M) | 2026-11-03 16:26:59 | 1 lane match | no |
| .ufo/l0-questions.md (M) | 2026-11-03 20:03:25 | 26 lane matches | no |

Misroot count: 0. No seat-written file exists outside the lane; none in a sibling repo, shokuknow, considerthese, or the fleet root during the wave window; no relative-path artefact (`drafts/`, `w1/`, `probes/`, `round-69/`) exists above the lane.

In-lane surface check (every present file sits inside a path its seat names):
`before/` 10 committed pre-declaration files; wave control `w1-spec.json`, `w1-dispatch.json`, `w1-run.stderr`, `w1.ready`, `w1.ready.dispatched`, `w1/swarm-registry.json`; `drafts/c1/{lesson,note,sources-rows}.md`; `drafts/c2/count-kr-rows-r69.py`; `drafts/hygiene/quality-102.md`; `probes/{S1Scout-sources.md,S1Scout-taint-table.tsv,S2Scout-host.md}` (both S1Scout files named in its item step 7); `probes/SC1Scribe/*.txt`; `probes/E2Counter/**`; `probes/E3Hygiene/{r68,r69}-checklist.txt`; `probes/C1Connector/overlap.md`; `probes/R1Reviewer/attack.md`; `probes/l1/*`; `w1/<Seat>.md`. No seat wrote `corpus/`, `tools/`, `SCORECARD.md`, `LOG.md`, `SKILL.md` or any other tracked file.

Tracked-file change during the round (not by a seat):

$ git status --porcelain -uall | grep -v '^??'
 M .ufo/waves/round-69/before/s243-v73-recheck.txt
$ git diff --stat
 .ufo/waves/round-69/before/s243-v73-recheck.txt | 1 +
 1 file changed, 1 insertion(+)

The added line reads `## correction (appended 2026-11-03 by the L1, no in-place edit): no wave seat re-verifies S243 this round. …` (mtime 23:19:10Z). OBSERVATION: a committed pre-declaration receipt changed inside the round; the change is additive, self-declared, and narrows the claim rather than inflating it.

Second observation: `before/census-live-baseline.txt` (untracked, 19 lines, 23:19:24Z) records a full `bash tools/tsukuroi-census.sh` run at `rc=1`. No seat item names that path; S2Scout's item explicitly forbids it the lane census and no seat claims the file. Attribution evidence: it appeared 14 s after the L1's own self-declared append in the same directory, and `probes/l1/taint-table.txt` (23:20:15Z) shows the L1 writing `probes/` in the same window — most consistent with the L1, unproven from artefacts alone.

## 3. Privilege table (uid 1000; `sudo` never used, never requested)

| instrument | path at sweep | state | command run | rc | output | needs root? |
|---|---|---|---|---|---|---|
| C1 content-sensitive counter | lane `tools/count-kr-rows-r69.py` ABSENT (matches the base control); draft `drafts/c2/count-kr-rows-r69.py` | draft only | `$ python3 tools/count-kr-rows-r69.py --revision HEAD` (copy inside the N1Sentinel clone, note absent) | 1 | `KR_ROWS=0 KR_VERIFIED=0` | NO |
| same, row path exercised | same | draft only | fixture commit `f07859fa` in the clone (S288+S289 appended under `## Registry`; 5-row note copied from `probes/E2Counter/outputs/control.md`), then the same command | 0 | `KR_ROWS=5 KR_VERIFIED=5` and `KR_ROW KR1..KR5 ok` | NO |
| C2 census kernel arm | `drafts/c2/tsukuroi-census.sh`, `drafts/c2/census-kernel-arm.diff` | ABSENT | `$ ls drafts/c2/tsukuroi-census.sh drafts/c2/census-kernel-arm.diff` | 2 | `ls: cannot access 'drafts/c2/tsukuroi-census.sh': No such file or directory` / `…'drafts/c2/census-kernel-arm.diff': No such file or directory` | UNRUN (absent instrument, not a privilege block) |

Counter interface observed in its bytes: read-only `git -C <lane> rev-parse/show/cat-file`, `Path.read_bytes` on the snapshots, `hashlib.sha256`; no temp files, no network, no writes (`subprocess` only for those three git verbs).

C2 data sources the arm must read, exercised here as uid 1000:

$ uname -r → 7.2.11-arch1-1, rc=0
$ cat /proc/sys/kernel/tainted → 12288, rc=0
$ ls -ld /usr/lib/modules/* → `6.18.57-2-lts` and `7.2.11-arch1-1`, both `drwxr-xr-x root root`, rc=0
$ pacman -Q linux linux-lts → `linux 7.2.11.arch1-1`, `linux-lts 6.18.57-2`, rc=0
$ pacman -Qo /usr/lib/modules/7.2.11-arch1-1 → owned by `linux 7.2.11.arch1-1` and `linux-headers 7.2.11.arch1-1`, rc=0
$ modinfo -F vermagic nvidia → `7.2.11-arch1-1 SMP preempt mod_unload`, rc=0
$ test -r /usr/lib/modules/{7.2.11-arch1-1,6.18.57-2-lts}/modules.dep → READABLE / READABLE_LTS
$ journalctl -b -k --no-pager -n 3 → 3 kernel lines, rc=0

Privilege-gated paths recorded (an arm must avoid them; the base census already documents the fallback at `tools/tsukuroi-census.sh:165,1105`):

$ cat /proc/sys/kernel/dmesg_restrict → 1, rc=0
$ ls -ld /sys/kernel/debug → `drwx------ 60 root root … /sys/kernel/debug`, rc=0
$ grep -n -E 'sudo|/sys/kernel/debug|dmesg |pacman -S|systemctl (start|restart|stop)' tools/tsukuroi-census.sh → only comment/fixture lines (152, 165, 1099, 1105, 1720, 1775, 1786, 2346, 2367, 2394, 2611); no privileged invocation.

BLOCKED paths: none needing privilege I lack. 1 instrument (the C2 census arm) was absent at 23:26Z, so its privilege test is UNRUN — exact `ls` error above.

## 4. Credential-shaped names mentioned by the artefacts (names only, no values)

| shape | where | value present? |
|---|---|---|
| `op://` (1Password reference syntax) | `w1-spec.json:5`, `w1-dispatch.json:187` — guard prose "never read or echo … op:// references" | no reference follows |
| `…credentials-boot-policy-r66.md` | corpus note filename referenced in the SC1Scribe item/paths | no — knowledge-file name |
| `/var/lib/pacman/local/<pkg>/desc` | SC1Scribe receipts, note `recheck:` line | no — package metadata (`%NAME%`, `%VERSION%`) |
| `.env`, `.ssh`, `id_rsa`, `id_ed25519`, `.netrc`, keyring | `grep -R -n -E '(/etc/|\.ssh|id_rsa|id_ed25519|\.netrc|\.env\b|op://|token|api[_-]?key|secret|password)' drafts probes` | none of these paths appear; the only "token" hits are prose and `token=` checklist fields |

## 5. What the evidence cannot prove

These artefacts are self-reported text: they cannot prove that a recorded command is the command actually executed, that no command ran whose output was never written, that the `before/census-live-baseline.txt` run came from the L1 rather than a seat, that `probes/SC1Scribe/quote-check.txt`'s pre-rewrite bytes were what the seat really ran, or that the absent C2 census arm needs no privilege — only the harness transcripts and the arm's own bytes could speak to those, and an unrun check has not passed.
