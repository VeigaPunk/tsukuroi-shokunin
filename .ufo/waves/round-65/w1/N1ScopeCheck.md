# N1ScopeCheck — sentinel scope-check report (tsukuroi lane, round 65 / hyaku run 15 / wave w1)

Seat: **N1ScopeCheck** (sentinel, READ-ONLY). Item: **SCOPE-CHECK** — the wave's security/scope
audit. Lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. Audited window 2026-11-03
~19:38Z → ~20:20Z. Verdict draft: `.ufo/waves/round-65/drafts/sentinel-scope.md`.

## VERDICT: CLEAN

All five audited axes pass. No host mutation, no unauthorized privilege, no secret captured, no
foreign write path, no write outside the lane repo. Two incomplete-wave gaps (C1SiblingScan silent;
the L1's own cited-receipts gate currently FAIL) and four low-severity documentation/resource
observations are recorded below for the L1 — none is a routed scope violation.

## Axes (godspeed)

1. **Host mutation** — no seat executed a mutating verb.
2. **Privilege** — every `sudo -n` is the authorized `/boot` cat/ls/stat class.
3. **Secrets** — no credential-shaped content captured.
4. **Write scope** — every modified/untracked path is a wave path, E2's census file, or an L1 landing.
5. **Containment** — nothing written outside the lane repo; no sibling-lane pollution.

## What I did

1. Enumerated the wave tree (98 files at close) and every seat's report/artifact set.
2. Swept the whole wave tree for mutating verbs, `sudo`, credential shapes and mutating git/jj verbs.
3. Cross-read each seat's receipt for its privilege class, its file writes, and its scratch cleanup.
4. Diffed the lane's `git status --porcelain --untracked-files=all` against the allowed-path set,
   with file mtimes to separate seat writes from L1 landings.
5. Swept the fleet root and all 17 sibling lane repos for this round's unique content strings and
   for stray `*r65*` files newer than the wave start.
6. Polled the wave read-only for the other seats' outputs (≈30 min of sleeps; stopped on the L1's
   instruction not to wait further on C1SiblingScan).
7. Cross-checked the L1's own gate output (`after/cited-receipts-r65.txt`) against the tree.

## Findings, axis by axis

### 1. Host mutation — CLEAN

Every regex hit over the wave tree (mutating verbs: `pacman -S/-R/-U/-Sy/-Fy/-Syu`,
`systemctl start/stop/restart/enable/disable`, `journalctl --rotate/--vacuum`,
`coredumpctl dump/delete`, `nvidia-smi -r`, `bootctl install/update`, `tee` into `/etc|/boot|/usr`,
redirection into system paths) is **prose in a third-party or historical document**, never an
executed command. Full table with file:line is in the draft. The three highest-risk hits:

- `after/work-F:503` — ``pacman -Syu`` — `work-F` is a byte-copy of the r64-era SCORECARD body
  (768 591 B, `cmp` vs `git show 431f0c9:SCORECARD.md` = 0); it narrates the host's 2026-10-20
  upgrade, it is not a transcript.
- `before/s282-v262-body.md:376` — `coredumpctl dump` — upstream systemd v262 release notes.
- `w1/S1Scribe.md:121` — `pacman transaction`, `systemctl start/stop/…` — a **negative attestation**.

The E2 census patch contains only `stat`/glob/`grep -qF`/`command -v`; no `mkinitcpio`, `dracut`,
`ukify` or `bootctl` call was added. Package state is unchanged (systemd 262.1-1, mkinitcpio 42.2-1,
limine 12.9.4-1, linux 7.2.11.arch1-1, nvidia-utils 615.78.08-1 — identical to the pre-arm reading).

### 2. `sudo -n` — CLEAN (exactly the authorized class)

Three privileged commands exist in the entire wave, all from E1HostProbes, all named in E1's item:

| file:line | command |
|---|---|
| `probes/r65-limine-conf.txt:2` | `sudo -n cat /boot/limine.conf` |
| `probes/r65-boot-inventory.txt:2` | `sudo -n ls -laR /boot` (depth ≤ 3) |
| `probes/r65-boot-inventory.txt:69` | `sudo -n stat -c …` on the UKI/EFI images |

No other seat used `sudo`; each states "no sudo" and its receipts contain none. All remaining
`sudo` strings are historical lane prose (r17/r26/r27 boot-chain-audit tool descriptions) or upstream
text. **No UKI content was read or extracted** — the inventory is names/sizes/mtimes only, and
unprivileged `stat` on a `/boot/EFI/Linux/*.efi` returns `Permission denied (os error 13)` here
(measured), so the 0700 root-only `/boot` would have blocked it regardless.

### 3. Secrets — CLEAN

Zero credential-shaped hits (`AKIA…`, `ghp_…`, `-----BEGIN … PRIVATE KEY-----`, `session=`,
`token=`, `cookie:`, `password=`) in any receipt, probe, draft, seat report or artifact. The only
matching files are `w1-spec.json` / `w1-dispatch.json`, which embed the item prompt text (my own
rule string), not captured data.

`/boot/loader/boot-secret-mixin` (32 B) and `/boot/loader/random-seed` (32 B) are **named/sized
only** (`probes/r65-boot-inventory.txt:65-66`); `probes/r65-bootctl.txt:64` shows the seed was never
accessible ("Permission denied"). E1 discloses this at `w1/seats/E1HostProbes.md:95`. Non-secret host
identifiers (machine-id `432d02b5…`, PARTUUID `b80445be-…`, root cmdline, uname) are present and
flagged by E1 as public-ish.

### 4. Write scope — CLEAN, no foreign path

Every `git status --porcelain --untracked-files=all` path is in an allowed bucket:
`.ufo/waves/round-65/**` (all seats + L1), `tools/tsukuroi-census.sh` (**E2 only**, as its item
names), and the L1's own landings (`corpus/SOURCES.md`, `corpus/QUALITY.md`,
`corpus/knowledge/systemd262-uki-pcr-r65.md`, `corpus/lessons/round-65.md`, `LOG.md`, `SCORECARD.md`,
`SKILL.md`) plus the L1's deletion of its own `drafts/log-outcome-skeleton.md`.

Seat-vs-L1 attribution is proven by mtime: the last seat-authored file is 16:54:36 local, every L1
landing is ≥ 16:58:47 (`knowledge/…` 16:58:47 → `SOURCES.md` 17:03:37 → `lessons/round-65.md`
17:04:10 → `QUALITY.md` 17:09:21). The L1 committed the work at `2ddd5e79`.

No seat wrote to `LOG.md` / `SCORECARD.md` / `SKILL.md` / `corpus/SOURCES.md` / `corpus/knowledge/` /
`PROVINCE.md` / `SHONEN.md` / `AGENTS.md` / `.ufo/state/` / `MANIFEST.json` / `.ufo/l0-questions.md` /
`.scratch/`. Exactly **one** erratum block landed for the single routed id `R64-SPOTCHECK-C1-PROOF`
(`SCORECARD.md:4872`), which closes R2RevRepair's D2 (two drafts existed for one id).

### 5. Containment — CLEAN

`find /home/vgpnk/Projects/shokunin -maxdepth 4 -newermt '2026-11-03 16:40' -iname '*r65*'` outside
the lane wave dir → **empty**. The only new fleet-root files are the orchestrator's own
`.scratch/run15-state.json` (16:53) and `.scratch/run15-kernel.py` (16:26) — L0's, not a seat's.
Grepping every sibling lane repo for this round's unique strings (`probe_initramfs_arm`,
`systemd262-uki-pcr-r65`, `initramfs-plane`, `r65-bootctl`, `r65-double-census`, `r65-uki-producer`,
`r65-limine-conf`) → **zero hits outside tsukuroi**. Dirty siblings (kengaku 18, kasegi 15, kake 15,
tabi 8, kagi 28) hold their **own lanes'** rounds (kengaku r64/65, kasegi r57, kake r70, tabi r57,
kagi r31) — concurrent other-lane work, not tsukuroi r65 output. `chousa-shokunin/.ufo/waves/round-65/`
is chousa's own round-65; its `tsukuroi` mentions are adjacency prose, not writes into this lane.

## Gaps and observations for the L1 (not scope violations)

**G1 — C1SiblingScan landed at the last minute; one trailer path still missing.** At audit close
(20:20Z, ~42 min after dispatch) the seat had produced **nothing**; it then landed
`drafts/overlap-scan.md` (17 568 B, 17:25 local) and `w1/C1SiblingScan.md` (11 702 B, 17:27). It
**never wrote `w1/seats/C1SiblingScan.md`**, the path its item names. Its content is scope-clean:
no mutating verb, no `sudo`, zero credential shapes, and it states "No sibling repo was written" —
independently re-verified (all 17 sibling repos re-checked; `kengaku`/`kasegi`/`souji`/`tabi`/`kagi`
dirt is their own concurrent rounds; grepping siblings for `C1SiblingScan|overlap-scan` outside
tsukuroi returns only their own historical r21/r25/r29/r32 files). The adjacency duty has its
evidence.

**G2 — resource-hygiene deviation (LOW), C1SiblingScan (self-resolved).** The lane bound allows
**one live clone per seat**; that scratch held **6** concurrent lane clones peaking at **2.6 GB**
(all `--shared` with alternates → no full object mirror). Under `/fast` (397 G of 804 G used) this was
not host pressure. The seat **did** clean up: its scratch dir is gone at close and
`/fast/scratch/hyaku/tsukuroi-r65/` holds only `drafts`, `l1`, `probes` and this seat's dir.

**G3 — the L1's own cited-receipts gate is FAIL right now.** `after/cited-receipts-r65.txt`
(gate `check-cited-receipts-r62`, rev `2ddd5e79`, round 65) records `verdict: FAIL`, 4 findings:
- `after/counting-battery-at-work.txt` — written 17:18, **after** the `2ddd5e79` commit, so absent
  from that revision (it exists on disk now).
- `after/gates-at-work-rev.txt` — **does not exist anywhere** (`ls` rc 2, `git cat-file -e` rc 128).
  The landed LOG.md outcome no longer cites it; only the draft the L1 deleted did → self-clearing
  once that deletion is committed.
- `w1/C1SiblingScan.md` — **now exists** (landed 17:27) → cleared.
- `w1/N1ScopeCheck.md` — **this seat's own report path**; both `w1/N1ScopeCheck.md` and
  `w1/seats/N1ScopeCheck.md` now exist (written after the gate ran), so this finding is closed by my
  landing. **Findings 1 and 2 remain for the L1**: commit the seven `after/` receipts with the
  outcome commit (the landed LOG.md cites two of them), produce `after/gates-at-work-rev.txt` or drop
  its citation, then re-run the gate.

**Observation 1 (LOW) — E1's privilege inventory overstates escalation on an `/etc` path.**
`w1/seats/E1HostProbes.md:7` lists "`stat` on `/etc/limine-entry-tool.conf`" as privileged; the
receipt carrying that read (`probes/r65-mkinitcpio-conf.txt:76-77`) shows `ls -la` **unprivileged**
(the file is `-rw-r--r--` world-readable). No unauthorized privileged read occurred; the wording
should be corrected so the sudo inventory matches the receipts.

**Observation 2 (LOW) — receipt labelling.** `probes/r65-boot-inventory.txt:96-100` and `:107-113`
(the `limine_history` UKI-snapshot `stat` blocks) omit the `sudo -n` prefix although `/boot` is
0700 root-only, so those reads were necessarily privileged; the class is still the authorized
`stat`-on-`/boot`, but the command label is missing, and the block mixes `ls -la` and `stat` output
shapes.

**Observation 3 (LOW) — three seats wrote only the `w1/` copy of their report.**
`w1/seats/E2InitramfsArm.md`, `w1/seats/M1MutBattery.md` and `w1/seats/C1SiblingScan.md` are
absent; all three `w1/<seat>.md` copies exist, so no evidence is lost, but the dispatch names both
paths and the trailer contract is half-met for three seats.

**Observation 4 (LOW) — the wave's `after/` receipts are not in the work commit.** All seven
`after/` files written at 17:18 (`census-end.txt`, `census-postarm-live.txt`, `cited-receipts-r65.txt`,
`counting-battery-at-work.txt`, `knowledge-header-at-work.json`, `prearm-vs-postarm-live.diff`,
`registry-coverage-at-work.json`) are still untracked. The landed LOG.md outcome cites two of them
(`after/census-postarm-live.txt`, `after/counting-battery-at-work.txt`) — they must be committed with
the outcome, or the cited-receipts gate will keep reporting them missing at the landed revision.

## Files written by this seat

- `.ufo/waves/round-65/drafts/sentinel-scope.md` — the full verdict + evidence index (the item's
  required output).
- `.ufo/waves/round-65/w1/seats/N1ScopeCheck.md` — this report (the item's named path).
- `.ufo/waves/round-65/w1/N1ScopeCheck.md` — this report at the item's Report-trailer path
  (the path `w1-dispatch.json` cites, which the cited-receipts gate checks).

Nothing else was written. No other seat's file was modified.

## Commands run (all read-only, with rc)

```
mkdir -p /fast/scratch/hyaku/tsukuroi-r65/N1ScopeCheck                                rc 0
ls -la .ufo/waves/round-65/{,before,after,drafts,probes,w1,w1/seats,w1-artifacts}    rc 0
find .ufo/waves/round-65 -type f -printf '%T@ %s %p\n' | sort -n                      rc 0  (98 files)
git -C <lane> status --porcelain                                                      rc 0
git -C <lane> status --porcelain --untracked-files=all                                 rc 0
git -C <lane> log --oneline -1                                                        rc 0  (2ddd5e79)
git -C <lane> reflog --date=iso -8                                                     rc 0
git -C <lane> diff --stat ; git -C <lane> diff --summary ; git -C <lane> diff --raw    rc 0
git -C <lane> show --stat --name-only 2ddd5e79 | grep -E 'after/|drafts/'              rc 0
git -C <lane> cat-file -e 2ddd5e79:.ufo/waves/round-65/after/gates-at-work-rev.txt      rc 128 (absent)
git -C <lane> cat-file -e 2ddd5e79:.ufo/waves/round-65/after/counting-battery-at-work.txt rc 128 (absent)
git -C <lane> diff corpus/SOURCES.md ; git -C <lane> diff corpus/QUALITY.md             rc 0
git -C <lane> show 2ddd5e79:.ufo/waves/round-65/drafts/log-outcome-skeleton.md         rc 0
grep -rnE '<mutating verbs>' .ufo/waves/round-65/   (excl. w1-spec/w1-dispatch)       rc 0  (7 hits, all prose)
grep -rn 'sudo' .ufo/waves/round-65/                 (excl. w1-spec/w1-dispatch)       rc 0  (3 privileged cmds)
grep -rn 'sudo -n (cat|ls|head|stat)' .ufo/waves/round-65/                            rc 0
grep -rlE '<secret shapes>' .ufo/waves/round-65/     (excl. w1-spec/w1-dispatch)       rc 0  (0 files)
grep -rnE '\bgit +(add|commit|stash|checkout|switch|reset|restore|push|pull|merge|rebase|cherry-pick)\b|\bjj +(commit|describe|new|restore|abandon)\b'  rc 0
grep -rn 'git clone' .ufo/waves/round-65/                                             rc 0  (E2 receipt only)
sha256sum + cmp .ufo/waves/round-65/w1/seats/R1RevC1-s282-live.json  vs  before/s282-v262-release.json  rc 0 (identical)
find /home/vgpnk/Projects/shokunin -maxdepth 4 -newermt '2026-11-03 16:40' -iname '*r65*'  (excl. lane wave)  rc 0 (empty)
find /home/vgpnk/Projects/shokunin -maxdepth 3 -newermt '2026-11-03 16:40' -not -path '*/tsukuroi-shokunin/*'  rc 0
grep -rl '<round-65 unique strings>' /home/vgpnk/Projects/shokunin/*-shokunin/  (excl. tsukuroi)  rc 0 (0)
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do git -C "$d" status --porcelain; done   rc 0
git -C <lane> grep -n 'R64-SPOTCHECK-C1-PROOF' SCORECARD.md ; grep -c '<erratum header>' SCORECARD.md  rc 0 (1)
python3 -c '<dispatch path existence check>'                                              rc 0
stat -c '%y %n' <each L1-landed file>                                                    rc 0
ls -d /fast/scratch/hyaku/tsukuroi-r65/C1SiblingScan/laneclone* | wc -l                 rc 0  (6)
du -sh /fast/scratch/hyaku/tsukuroi-r65/* ; df -h /fast                                rc 0
stat -c '%y %n' /home/vgpnk/Projects/shokunin/.scratch/run15-state.json /…/run15-kernel.py  rc 0
```

## Scratch-clean confirmation

Scratch dir `/fast/scratch/hyaku/tsukuroi-r65/N1ScopeCheck/` — created for this seat, used only for
inspection (no fixture, no clone, no receipt written there), and **removed** at seat end:

```
rm -rf -- /fast/scratch/hyaku/tsukuroi-r65/N1ScopeCheck                                rc 0
test -e /fast/scratch/hyaku/tsukuroi-r65/N1ScopeCheck                                  -> absent
```

Parent `/fast/scratch/hyaku/tsukuroi-r65/` still holds only the other seats' dirs
(`C1SiblingScan`, `drafts`, `l1`, `probes`) — none touched by this seat. No `/tmp` path was used as
citable evidence. No tool was installed (no pacman / uv / npx / release-binary action); no git/jj
mutation was run anywhere (read-only verbs only: log/show/diff/status/rev-parse/cat-file/
merge-base/rev-list/ls-files).
