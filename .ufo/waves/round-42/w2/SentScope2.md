VERDICT: defect-found

Seat SentScope2, item F-22, tsukuroi lane round 42, wave w2 (falsify). Scope/misroot sweep over this wave's writes. One **minor, seat-attributable** scope breach: seat `C1RevIntegration` created a host-visible empty directory `/tmp/tiny` and left it (its mount work itself stayed inside `unshare -rm`). No lane content, Git index, jj state, fleet-repo tracked file, boot path or host mount was written by any w2 seat. Three non-seat observations (two PATH mutations, one fleet-root untracked file) are recorded below with attribution so the L1 does not mistake them for seats.

Marker for every "newer than" filter (the item's): `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-42/w2-context.txt` (4,636 B, mtime 2026-10-26 16:38). Four observations: T0 baseline 17:48:53 local (=20:48:53Z, 10 s after the dispatch receipt), T1 17:54:45, T2 18:05, T3 **18:14:23 local = 21:14:23Z** (25 min 30 s after T0). Every command below is read-only; `GIT_OPTIONAL_LOCKS=0` after T0. Receipts: `.ufo/waves/round-42/w2/SentScope2/` (480 KB, no file over 2 MB): `t1/`, `t2/`, `t3/`, `sweep.sh`, plus the T0 baselines and the attribution files named in each section.

## 1. Fleet root — no w2 misroot; one untracked file belongs to another lane

```
$ git -C /home/vgpnk/Projects/shokunin --no-optional-locks status --porcelain
   (0 lines, T0 and T1)
$ …                                          # T2 and T3
?? .ufo/reports/round-42/kengaku.md
```
`.ufo/reports/round-42/kengaku.md` — 14,874 B, mtime 18:06, owner **kengaku-shokunin's own round 42** (peer `KengakuR42`); its header line 1-3 reads "`# kengaku — round 42 report (hyaku run 9, 2026-10-26)` … Lane `/home/vgpnk/Projects/shokunin/kengaku-shokunin`, branch `master`". Name collision on "round 42", not a tsukuroi write.

Name scan at fleet root, depth 2, excluding the lane, for `*tsukuroi*` / `*r42*` (`t1/fleet-name-scan.txt`, `t2/`, `t3/`): 1 line, the lane directory itself (`tsukuroi-shokunin/`, mtime 15:08). Tracked fleet files: `MANIFEST.json` mtime moved (17:43:24 → 18:05:03, 2,136,087 B) but its worktree blob equalled `HEAD:MANIFEST.json` at every observation (`t1` blob `138de5e0…` = then-HEAD; `t3` blob `0e598dd9…` = current HEAD; `git log -2 -- MANIFEST.json` → `13277204 protocol-shokunin 18:05:03`, `a4a605eb … 17:59:26`). The fleet-repo commits during the window are all **protocol-shokunin** ledger exports (reflog 17:48:10 / 17:58:40 / 17:58:46 / 17:59:26 / 17:59:43, "export from jj"), i.e. the fleet orchestrator, not this wave. No seat wrote a fleet-root tracked file.

## 2. Lane — nothing outside `.ufo/waves/round-42/w2/` was written; no leaf commit

```
$ git -C <lane> --no-optional-locks status --porcelain      # T0 == T1 == T2 == T3, 4 lines
?? .ufo/waves/round-42/w2.ready
?? .ufo/waves/round-42/w2.ready.dispatched
?? .ufo/waves/round-42/w2/
?? corpus/lessons/round-42.md
$ git -C <lane> diff --stat HEAD            → empty
$ git -C <lane> diff --cached --stat HEAD   → empty
```

| path | size | mtime | owner / nature |
|---|---|---|---|
| `.ufo/waves/round-42/w2.ready` | 160 B | 17:20 | L1 dispatch marker (`{"lane":"tsukuroi","round":42,"wave":"w2","l1":"TsukuroiR42"}`) |
| `.ufo/waves/round-42/w2.ready.dispatched` | 1,144 B | 17:48:43 | L1 dispatch receipt (seat→harness-id map) |
| `.ufo/waves/round-42/w2/` | 451 files, 5.3 M | 18:14 | the wave's own report dir — expected |
| `corpus/lessons/round-42.md` | 10,412 B | 17:22 | L1 scribe artifact; its line 3 says "author: tsukuroi L1 (`TsukuroiR42`)" — outside `w2/` by design |

Tip: `a968393c678171f8a5a2907da5015735396da4cc`, i.e. dispatch tip `78abb8b5` + **exactly one** commit — `tsukuroi-shokunin <tsukuroi@shokunin.local> 2026-10-26 17:20:25 "round-42: C1 after receipt at 78abb8b5 (PASS, 132 cases…)"` — the L1's integrator identity, before w2 started; no leaf commit, and `.git/logs/HEAD` ends at that "export from jj" line. Only one file outside `w2/` is newer than 17:20 (`t3/lane-outside-w2-newer.txt`): the L1's `corpus/lessons/round-42.md`. `.jj/` has nothing newer than 17:21. Lane symlinks outside `.jj`/`.git` are 6 (`t3/lane-symlinks.txt`), all relative links inside the round-35 upstream snapshot `.ufo/waves/round-35/w1/ScribeC2Draft/pacman-54d9411/src/…` → `../common/…`; none belongs to w2. `w2/` itself contains 0 symlinks.

**Read this before blaming a seat for `.git` mtime:** `<lane>/.git` mtime moves on every `git status` (lock file created and removed), while `<lane>/.git/index` stayed at 17:22:09 with its size unchanged (1,934,576 B) through T3 — so no seat refreshed or rewrote the index.

## 3. `/tmp` and `/var/tmp`

```
$ find /tmp /var/tmp -maxdepth 5 \( -iname '*tsukuroi*' -o -iname '*r42*' -o -iname '*hyaku*' \)
   (0 lines at T1, T2, T3)
$ find /tmp /var/tmp -maxdepth 1 -newer <marker>      # 86 entries
```
Content attribution of the 86 entries (name scan cannot see content): `grep -l -i -e tsukuroi -e round-42 -e r42` over the 75 small files newer than the marker → 11 hits (`t3/tmp-content-tsukuroi.txt`), every one another lane's own document: `/tmp/sa`, `/tmp/sb`, `/tmp/sbase`, `/tmp/skill_base*.md`, `/tmp/base-skill.md`, `/tmp/T49Read03-skill.md` are tameshi-shokunin scorecards/skills ("`# tameshi-shokunin — Scorecard`", "`--- name: tameshi-shokunin`"), `/tmp/tip.*.txt`, `/tmp/del.*.txt` are kama-shokunin scorecards ("`# kama-shokunin — SCORECARD`"). **No tsukuroi-r42 content exists under `/tmp` or `/var/tmp`.**

**Finding (minor, seat `C1RevIntegration`): host directory `/tmp/tiny` created and left behind.**
- Evidence: `stat /tmp/tiny` → directory, size 6 (empty), mtime 2026-10-26 17:42:54; `ls -A /tmp/tiny | wc -l` → 0.
- Source: `w2/C1RevIntegration/exp2.sh:39` and `:49` `mkdir -p /tmp/tiny`, followed at `:40`/`:50` by `mount -t tmpfs -o size=64k tmpfs /tmp/tiny`; the mount is correctly wrapped — `:45`/`:55` run the inner script as `unshare -rm bash d6-inner.sh` / `d7-inner.sh`, and `exp2.out:8-12` shows the 64 KiB branch and its control.
- No harm: `/tmp/tiny` is **not** a mount now — `findmnt -T /tmp/tiny` → `/tmp /dev/nvme1n1p1 xfs …`; `grep -n tiny /proc/self/mounts` → 0 lines; `findmnt -t tmpfs` shows no leftover tmpfs (`t3/tmpfs-mounts.txt`). The host guard's "no mount outside a private `unshare -rm` namespace" was respected; the breach is only that the namespace's `mkdir` lands on the host filesystem and the directory was not removed (`rmdir` costs nothing; the rule says never build under `/tmp`).
- Not this wave: `/tmp/tmpc1h0ejli/` + `/tmp/c1-4600{1..5}.txt` + `/tmp/c2-{4d22ee…,ee6659…}.txt` + `/tmp/srcs.txt` + `/tmp/vq.txt` are round-45 hyprland work (first lines: `PRED-C1-r45-v2 …`, `PRED-C2-r45-v2 hyprland-monitor-rule-r45.md`, `exists ~/.local/share/omarchy/default/hypr/…`), and `/tmp/d.json`, `/tmp/ecc-metrics-*`, `/tmp/claude-tool-count-*`, `/tmp/org.chromium.*`, `/tmp/pymp-*` are harness/daemon artifacts.

## 4. `~/.local/bin` — two new names and one in-place replacement, none from a w2 seat

```
$ LC_ALL=C comm -13 <w1 t3 names (100)>.sorted <now (102)>.sorted
firefox
geckodriver
$ find /home/vgpnk/.local/bin -mindepth 1 -newer <marker>
2026-10-26 17:48  46        /home/vgpnk/.local/bin/firefox
2026-10-26 18:10  275970224 /home/vgpnk/.local/bin/omp
```
- `firefox` — symlink → `/home/vgpnk/.local/opt/firefox-158.0.1/firefox`, birth 17:48:46.564, 46 B; target reports `Mozilla Firefox 158.0.1`.
- `geckodriver` — regular file, 6,029,440 B, birth 17:48:46.542 (mtime preserved from the release archive, 2026-07-17). Born 22 ms apart from `firefox`, **3 s after the w2 dispatch receipt (17:48:43)**, 7 s before this seat's baseline.
- Attribution: **not tsukuroi** — `grep -rn -i -e firefox -e geckodriver` over `.ufo/waves/round-42/w2/` → 0 lines (`SentScope2/firefox-geckodriver-w2-grep.txt`); no w2 report or receipt mentions a browser stack. The only live work naming these exact two paths is tabi-shokunin round 35, which was writing at the same time (`.ufo/waves/round-35/{baseline,counters,measure.sh}` mtimes 17:52–18:01) and whose counter hardcodes them: `tabi-shokunin/.ufo/waves/round-35/counters/c2-firefox-bidi.mjs:78` `const FIREFOX = '/home/vgpnk/.local/opt/firefox-158.0.1/firefox';` and `:79` `const GECKODRIVER = '/home/vgpnk/.local/bin/geckodriver';`. Most consistent owner: tabi r35's prerequisite install (its own report must carry the tooling record; outside this seat's surface).
- `omp` — **replaced in place**: T0 baseline had a 1,680 B wrapper (`-rwxr-xr-x … 1680 Oct 23 20:47 omp`, with `omp.real` 256,702,432 B at Oct 21 20:37); at 18:10:45 the name `omp` is a 275,970,224 B ELF (birth 18:10:41, `omp/18.13.0`), `omp.real` untouched. That is the harness updating itself mid-run, not a seat; the **name-set check that w1 used (`SET-IDENTICAL`) cannot see it** — a name+mtime check can, which is why this section reports both.
- Shim scan: no entry in `~/.local/bin` is named `pacman`, `btrfs`, `systemctl`, `journalctl`, `mount`, `unshare`, `git`, `awk`, `grep`, `python3` (beyond the long-standing uv `python3.x` symlinks) or `sudo` (`t3/localbin-shim-scan.txt`). Other PATH directories (`~/.local/share/fnm`, `~/.opencode/bin`, `~/.local/share/mise/shims`, `~/.local/share/omarchy/bin`, `/usr/local/bin`, `/usr/local/sbin`, `~/.grok/bin`, `~/.kimi-code/bin`): nothing newer than the marker (`t3/other-path-newer.txt` = 0 lines).

## 5. Scratch under `/fast/scratch/hyaku/tsukuroi-r42` — every delivering seat cleaned up

At T1 six seat dirs and `l1` were live; at T3 only two remain (`t3/scratch-top.txt`, `t3/scratch-du.txt`, `t3/scratch-owner-join.txt`):

| dir | size | report delivered? | owner |
|---|---|---|---|
| `/fast/scratch/hyaku/tsukuroi-r42/l1` | 614 M | n/a | L1 `TsukuroiR42` — its own, not mine to delete |
| `/fast/scratch/hyaku/tsukuroi-r42/SentScope2` | 480 K | this seat | removed before yield (receipts copied into the lane first) |

Join against the report dir: **no seat that delivered a report has a surviving scratch dir**, so the "delete your scratch" rule was honoured by all 32 other seats (T2 intermediate states — `CritNoHarmFinal` 315 M, `MistakesFixFail` 315 M, `SimplifierLesson` 315 M, `NotesPatchOffset` 696 K — were live seats without reports yet; all gone by T3). No symlinks at the top level; nothing of this wave sits under `/fast/scratch/hyaku` outside `tsukuroi-r42`.

## 6. Report-dir hygiene (`.ufo/waves/round-42/w2/`)

At T3 the dir held 451 files, 67 top entries, 5.3 M: **33 reports + 33 receipt dirs + `swarm-registry.json` = 67** (`t3/w2-naming-check.txt`). After this seat's own report and its 102 receipt files landed, the same dir is 554 files / 69 top entries / 34 reports (5.8 M); those two additions are this seat's only lane writes. `reports not a dispatch member: []`, `receipt dirs not a dispatch member: []`; the only member without a report or receipts dir at T3 was `SentScope2` (this seat). No file over 2 MB (`t3/w2-oversize.txt` = 0), no symlinks (`t3/w2-symlinks.txt` = 0), so no seat redirected a receipt path.

Cited-path audit (`SentScope2/cited-path-audit.txt`): every `.ufo/waves/round-42/…` path cited by a w2 report exists. The two "missing" patterns are prose, not paths — `C2PostCritBinding.md:129` `.ufo/waves/round-42/residual/C2RevSC<n>c.md` and `:134` `sha256sum .ufo/waves/round-42/w2/C2*-SC*.md`. Out-of-`w2/` citations are all read-only references to `frozen/src`, `frozen/hostcap`, `w1/…`, `before/`, `after/`, `controls/` — reading, not writing. No report uses a `/tmp` path as evidence (`grep -rn '/tmp/' w2/*.md` → 0); the only `/tmp` references in receipts are the `C1RevIntegration/exp2.sh` lines quoted in §3.

## 7. What I did not do

- Did not run either frozen counter or the census selftest (host-load and one-counter-at-a-time rule); this item is a write-scope sweep, not a claim check.
- Did not verify the *content* of any claim or receipt — only location, scope, ownership and provenance.
- Did not delete, move or chmod anything except my own scratch dir: not `/tmp/tiny`, not `~/.local/bin/{firefox,geckodriver}`, not the kengaku report, not the L1's `l1` scratch, no lane or fleet file. No git/jj mutation anywhere; no `unshare`, `btrfs` or `pacman` command of my own; all processes I started were `sleep`/`grep`/`find`/`stat` in my own scratch.
- Installed or upgraded nothing (tooling record: none); used only `bash`, GNU `find`/`stat`/`grep`, `git --no-optional-locks`, `python3`.

Report: `.ufo/waves/round-42/w2/SentScope2.md`
