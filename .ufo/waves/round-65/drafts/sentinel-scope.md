# Sentinel scope-check — round 65 / wave w1 (N1ScopeCheck)

Seat: N1ScopeCheck (sentinel, READ-ONLY). Lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Audited window: 2026-11-03 ~19:38Z (wave dispatch) → 2026-11-03 ~20:20Z (audit close).
Audited tree: `.ufo/waves/round-65/` (98 files at close: `before/` 9, `after/` 9, `probes/` 12,
`drafts/` 11, `w1/` 13 + `w1/seats/` 9, `w1-artifacts/` 26, dispatch/spec/ready markers 6) plus the
lane's `git status --porcelain --untracked-files=all` and the fleet root `/home/vgpnk/Projects/shokunin`.

## VERDICT: CLEAN on all five audited axes — no host mutation, no unauthorized privilege, no
## secret captured, no foreign write path, no write outside the lane repo.

Two **incomplete-wave** gaps (not scope violations) and three **low-severity documentation
observations** are recorded below, plus one **resource-hygiene deviation** by a still-running seat.

---

## Axis 1 — Host-mutation audit: CLEAN

Regex swept over the whole wave tree (excluding `w1-spec.json` / `w1-dispatch.json`, which embed the
item prompt text itself):

```
(pacman +(-[a-zA-Z]+ +)*(-S|-R|-U|-Sy|-Fy|-Syu))
| systemctl +(start|stop|restart|enable|disable)
| journalctl[^|]*(--rotate|--vacuum)
| coredumpctl +(dump|delete)
| nvidia-smi +-r
| bootctl +(install|update)
| tee +(-a +)?(/etc|/boot|/usr)
| >>? +"?(/etc|/boot|/usr)/
```

**Every hit is prose in a third-party or historical document, never an executed command:**

| file:line | hit | why it is not a mutation |
|---|---|---|
| `after/work-F:503` | ``pacman -Syu`` | `work-F` is a byte-copy of the r64-era SCORECARD body (768 591 B, sha-identical to the r64 blob; `cmp` against `git show 431f0c9:SCORECARD.md` = 0). It *narrates* the host's 2026-10-20 upgrade. It is a document, not a transcript. |
| `after/work-F:2850` | `systemctl stop` | same historical SCORECARD narrative (r45 btrfs-scrub row) |
| `before/s282-v262-body.md:376` | `coredumpctl dump` | upstream systemd v262 release notes (third-party text) |
| `before/s282-v262-release.json:43` | `systemctl reboot` | same upstream body, JSON-escaped |
| `w1/seats/R1RevC1-s282-live.json:43` | `systemctl reboot` | same upstream body; file is **byte-identical** to `before/s282-v262-release.json` (sha256 `008e1265…babce0b`, `cmp` rc 0) |
| `w1/S1Scribe.md:121`, `w1/seats/S1Scribe.md:121` | `pacman transaction`, `systemctl start/stop/…`, `journalctl --rotate` | a **negative attestation** ("Host reads only: no pacman transaction, no `systemctl start/stop/…`") |

No seat receipt contains an executed mutating verb. The E2 patch to `tools/tsukuroi-census.sh` adds
only `stat`/glob/`grep -qF`/`command -v` calls; the census diff carries no `mkinitcpio`, `dracut`,
`ukify` or `bootctl` invocation (verified by grep over `git diff tools/tsukuroi-census.sh`).
Package state is unchanged: `pacman -Q systemd mkinitcpio limine linux nvidia-utils` →
`262.1-1 / 42.2-1 / 12.9.4-1 / 7.2.11.arch1-1 / 615.78.08-1`, identical to the pre-arm reading.

## Axis 2 — sudo `-n` usage audit: CLEAN (privileged reads are exactly the authorized class)

The only privileged command forms anywhere in the wave are three, all from seat E1HostProbes, all
named in E1's item:

| file:line | command | authorized by |
|---|---|---|
| `probes/r65-limine-conf.txt:2` | `sudo -n cat /boot/limine.conf` | E1 item line 2 (verbatim) |
| `probes/r65-boot-inventory.txt:2` | `sudo -n ls -laR /boot` (depth ≤ 3) | E1 item line 3 (verbatim) |
| `probes/r65-boot-inventory.txt:69` | `sudo -n stat -c '%n\|%s\|%y\|%a\|U:%G'` on UKI/EFI images | E1 item line 3 ("plus stat -c on any UKI/nlm/efi files found") |

No other seat used `sudo` at all. S2Considerthese, C1SiblingScan, R1RevC1, R2RevRepair, K1CritClaims,
M1MutBattery, L1DoubleCensus, S1Scout, S1Scribe, E2, E3 each state "no sudo" and their receipts
contain none. Every `sudo` string in `after/work-F`, `before/s282-v262-body.md`,
`before/s282-v262-release.json` and `w1-artifacts/R2RevRepair/step2b-scorecard-divergence.txt` is
historical lane prose describing the r17/r26/r27 boot-chain-audit tool, not a wave command.

**No UKI content was read or extracted.** The inventory receipt lists names/sizes/mtimes only; the
`stat` block is explicitly labelled "metadata only, no content read". Unprivileged `stat` on a
`/boot/EFI/Linux/*.efi` returns `Permission denied (os error 13)` on this host (measured), i.e. the
0700 root-only `/boot` would have blocked content reads by an unprivileged seat anyway.

**Observation 1 (LOW, documentation only):** `w1/seats/E1HostProbes.md:7` states privilege was also
used for "`stat` on `/etc/limine-entry-tool.conf`". The receipt that carries that read
(`probes/r65-mkinitcpio-conf.txt:76-77`) shows `ls -la /etc/limine-entry-tool.conf` — **unprivileged**
(the file is `-rw-r--r-- root root`, world-readable). The report's privilege inventory therefore
overstates what was escalated on an `/etc` path (outside the item's `/boot`-only sudo class). No
unauthorized privileged read occurred; the discrepancy is in the report's wording only.

**Observation 2 (LOW, receipt labelling):** `probes/r65-boot-inventory.txt:96-100` and `:107-113`
(the `limine_history` UKI-snapshot `stat` blocks) omit the `sudo -n` prefix in their headers, while
`/boot` is `0700 root:root` — those reads must have been privileged. The command class is still
`stat` on `/boot` (authorized); only the receipt's command label is missing. Two of the three
`stat` lines in the block are also formatted as `stat`-output (`name|size|mtime|mode|owner`) while
being attributed to an `ls -la` in the adjacent line, so the block mixes two tools' output shapes.

## Axis 3 — Secret audit: CLEAN

Pattern set `AKIA[0-9A-Z]{16}`, `ghp_[A-Za-z0-9]{20,}`, `-----BEGIN … PRIVATE KEY-----`,
`session=<8+>`, `token=<8+>`, `cookie:`, `password=` swept over every wave file.

**Zero hits in any receipt, probe, draft, seat report or artifact.** The only files matching are
`w1-spec.json` and `w1-dispatch.json`, which contain the *item prompt text* (my own audit rule
string) — not captured secrets.

Boot-secret material was named/sized but never read:
- `probes/r65-boot-inventory.txt:65-66` — `/boot/loader/boot-secret-mixin` (32 B) and
  `/boot/loader/random-seed` (32 B) appear as `ls -laR` directory-listing lines.
- `probes/r65-bootctl.txt:64` — `Exists: Can't access /boot/loader/random-seed (Permission denied)`.
- E1 discloses this explicitly (`w1/seats/E1HostProbes.md:95`): "named/sized only".

Non-secret host identifiers **are** present and are disclosed as such by E1: machine-id
`432d02b544a5459ebbff9c42ec68334d` (`probes/r65-limine-conf.txt:28`, `probes/r65-boot-inventory.txt:9`),
PARTUUID `b80445be-18ee-45e6-9a30-14339ea785a7`, root cmdline, `linux 7.2.11.arch1-1` uname. These are
public-ish identifiers, not credentials, and E1 flags them explicitly.

## Axis 4 — Write-scope audit: CLEAN

`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain --untracked-files=all`.
Every path falls into an allowed bucket; **no foreign path exists**:

| bucket | paths | owner |
|---|---|---|
| wave dir | `.ufo/waves/round-65/**` (before/, after/, probes/, drafts/, w1/, w1/seats/, w1-artifacts/, dispatch/spec/ready markers) | seats + L1 — allowed |
| census tool | `tools/tsukuroi-census.sh` | **E2 only**, as its item names — allowed |
| L1 landings | `corpus/SOURCES.md`, `corpus/QUALITY.md`, `corpus/knowledge/systemd262-uki-pcr-r65.md`, `corpus/lessons/round-65.md`, `LOG.md`, `SCORECARD.md`, `SKILL.md` | **L1 (TsukuroiR65)** — the L1's declared remit ("the L1 lands those") |
| L1's own draft deletion | `.ufo/waves/round-65/drafts/log-outcome-skeleton.md` (`D`) | L1 removed its own skeleton after folding it into LOG.md; inside the wave dir |

Landing timing confirms the split (all seat-authored files are ≤ 16:54:36 local; every L1 landing is
≥ 16:58:47): `corpus/knowledge/systemd262-uki-pcr-r65.md` 16:58:47 · `corpus/lessons/round-65.md`
17:04:10 · `corpus/SOURCES.md` 17:03:37 · `corpus/QUALITY.md` 17:09:21. The L1 committed the work at
`2ddd5e79` ("round-65: work … + wave evidence .ufo/waves/round-65"); LOG.md/SCORECARD.md/SKILL.md
remain as L1 working-tree edits for the outcome commit.

No seat wrote to `LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/SOURCES.md`, `corpus/knowledge/`,
`PROVINCE.md`, `SHONEN.md`, `AGENTS.md`, `.ufo/state/`, `MANIFEST.json`, `.ufo/l0-questions.md` or
`.scratch/` — all verified by each seat's own receipt and by the final `git status`.
**Exactly one erratum block landed** for the single routed defect id `R64-SPOTCHECK-C1-PROOF`
(`SCORECARD.md:4872`), resolving R2RevRepair's D2 (two drafts existed for one id; the L1 landed one).

## Axis 5 — No write outside the lane repo: CLEAN

- Fleet root `/home/vgpnk/Projects/shokunin`: `find … -maxdepth 4 -newermt '2026-11-03 16:40' -iname '*r65*'`
  outside the lane wave dir → **empty**. The only new fleet-root files are the orchestrator's own
  `.scratch/run15-state.json` (16:53) and `.scratch/run15-kernel.py` (16:26) — L0's, not a seat's.
- Sibling lane repos: `grep -rl` for this round's unique content strings (`probe_initramfs_arm`,
  `systemd262-uki-pcr-r65`, `initramfs-plane`, `r65-bootctl`, `r65-double-census`,
  `r65-uki-producer`, `r65-limine-conf`) across `/home/vgpnk/Projects/shokunin/*-shokunin/` →
  **zero hits outside the tsukuroi lane**. Dirty sibling repos (kengaku 18, kasegi 15, kake 15,
  tabi 8, kagi 28 entries) carry **their own lanes'** round content (kengaku r64/65, kasegi r57,
  kake r70, tabi r57, kagi r31), mtimes from other lanes' concurrent runs — not tsukuroi r65 output.
  `chousa-shokunin/.ufo/waves/round-65/` is chousa's own round-65, and its `tsukuroi` mentions are
  adjacency prose about this lane, not writes into it.

---

## Incomplete-wave gaps (NOT scope violations — reported to the L1)

**G1 — seat C1SiblingScan: outputs landed at the last moment; one trailer path still missing.**
At audit close (20:20Z, ~42 min after dispatch) C1SiblingScan had produced **nothing**. It then
landed within the final minutes: `drafts/overlap-scan.md` at 17:25 local (17 568 B) and
`w1/C1SiblingScan.md` at 17:27 (11 702 B). **It never wrote `w1/seats/C1SiblingScan.md`**, the
path its item names ("write your report at …/w1/seats/C1SiblingScan.md"), although it wrote the
`w1/` trailer copy. The scan itself is scope-clean: its draft states "No sibling repo was written;
every command below is a read", its content carries **no** mutating verb, no `sudo` and no
credential shape, and an independent re-check of all 17 sibling repos confirms C1 wrote nothing
into any of them (the `kengaku`/`kasegi`/`souji`/`tabi`/`kagi` dirt is their own concurrent
rounds; grepping every sibling for `C1SiblingScan|overlap-scan` outside tsukuroi returns only
their own historical r21/r25/r29/r32 files).
Impact: the adjacency duty now has its evidence, but the `w1/seats/` copy is absent — same
half-met trailer pattern as Observation 3 below.

**G2 — resource-hygiene deviation (LOW) by C1SiblingScan (self-resolved).** The lane bound allows
**one live clone per seat**. C1SiblingScan's scratch held **6** concurrent lane clones
(`laneclone`, `laneclone2..4`, `lanecloneH`, +1), peaking at **2.6 GB** — all `git clone --shared`
(alternates → the lane's `.git/objects`, so no full object mirror, but 6 working trees). Under
`/fast` (397 G of 804 G used) this was not host pressure. The seat **did** clean up: at close its
scratch dir is gone and `/fast/scratch/hyaku/tsukuroi-r65/` holds only `drafts`, `l1`, `probes`
and this seat's dir. Reported as a bound deviation in progress, self-corrected at the end.

**G3 — the L1's own cited-receipts gate is currently FAIL.** `after/cited-receipts-r65.txt`
(gate `check-cited-receipts-r62`, revision `2ddd5e79`, round 65) records `verdict: FAIL`,
`findings: 4`:
1. `.ufo/waves/round-65/after/counting-battery-at-work.txt` cited in `drafts/log-outcome-skeleton.md`
   — the file was written at 17:18, **after** the `2ddd5e79` commit, so it is not in that revision.
2. `.ufo/waves/round-65/after/gates-at-work-rev.txt` cited in the same draft — **this file does not
   exist anywhere** in the tree (`ls` rc 2; `git cat-file -e 2ddd5e79:…` rc 128). The landed
   `LOG.md` outcome text no longer cites it (it cites `after/census-postarm-live.txt` and
   `after/counting-battery-at-work.txt`, both of which now exist), and the draft that did cite it is
   the one the L1 deleted — so this finding is self-clearing once the deletion is committed.
3. `.ufo/waves/round-65/w1/C1SiblingScan.md` cited in `w1-dispatch.json` — **now exists**
   (landed 17:27) → cleared.
4. `.ufo/waves/round-65/w1/N1ScopeCheck.md` cited in `w1-dispatch.json` — **this seat's own report
   path**; both `w1/N1ScopeCheck.md` and `w1/seats/N1ScopeCheck.md` were written after the gate ran,
   so this finding is closed by this seat's own landing.

Findings 1 and 2 remain for the L1: the `after/` receipts cited by the landed LOG.md outcome must be
committed with the outcome commit, and `after/gates-at-work-rev.txt` must either be produced or its
citation dropped. **Re-run the gate after the outcome commit.**

**Observation 3 (LOW):** `w1/seats/E2InitramfsArm.md`, `w1/seats/M1MutBattery.md` and
`w1/seats/C1SiblingScan.md` are absent — those three seats wrote only the `w1/` copy, while the
dispatch names both paths. The `w1/` copies exist, so no evidence is lost, but the trailer-path
contract is half-met for three seats.

---

## Evidence index (commands run, all read-only, with rc)

```
mkdir -p /fast/scratch/hyaku/tsukuroi-r65/N1ScopeCheck                      rc 0
ls -la .ufo/waves/round-65/{,before,after,drafts,probes,w1,w1/seats,w1-artifacts}   rc 0
find .ufo/waves/round-65 -type f -printf '%T@ %s %p\n' | sort -n            rc 0   (98 files at close)
git -C <lane> status --porcelain [--untracked-files=all]                    rc 0
git -C <lane> log --oneline -1 ; git -C <lane> diff --stat                 rc 0   (HEAD 2ddd5e79)
git -C <lane> status --porcelain -uno                                       rc 0
git -C <lane> show --stat --name-only 2ddd5e79 | grep after/ drafts/       rc 0
git -C <lane> cat-file -e 2ddd5e79:.ufo/waves/round-65/after/gates-at-work-rev.txt   rc 128 (absent)
git -C <lane> diff corpus/SOURCES.md corpus/QUALITY.md                      rc 0
grep -rnE '<mutating verbs>' .ufo/waves/round-65/  (excl. spec/dispatch)    rc 0   (7 hits, all prose)
grep -rn 'sudo' .ufo/waves/round-65/            (excl. spec/dispatch)        rc 0   (3 privileged cmds)
grep -rlE '<secret shapes>' .ufo/waves/round-65/  (excl. spec/dispatch)      rc 0   (0 files)
grep -rnE '\bgit +(add|commit|stash|checkout|switch|reset|restore|push|pull|merge|rebase)\b|\bjj +(commit|describe|new|restore)\b'  rc 0
                                                                             (only `git checkout -q 37c74e27` in
                                                                              E2's scratch clone receipt —
                                                                              inside the fixture clone,
                                                                              `git rev-parse --show-toplevel`
                                                                              asserted first per the host guard)
grep -rn 'git clone' .ufo/waves/round-65/                                    rc 0   (E2 receipt: `git clone --shared`)
sha256sum / cmp .ufo/waves/round-65/w1/seats/R1RevC1-s282-live.json  vs  before/s282-v262-release.json   rc 0 (identical)
find /home/vgpnk/Projects/shokunin -maxdepth 4 -newermt '2026-11-03 16:40' -iname '*r65*'  (excl. lane wave)  rc 0 (empty)
grep -rl '<round-65 unique strings>' /home/vgpnk/Projects/shokunin/*-shokunin/  (excl. tsukuroi)            rc 0 (0)
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do git -C $d status --porcelain; done   rc 0
du -sh /fast/scratch/hyaku/tsukuroi-r65/*                                     rc 0
df -h /fast                                                                 rc 0
ls -d /fast/scratch/hyaku/tsukuroi-r65/C1SiblingScan/laneclone* | wc -l      rc 0   (6)
stat -c '%y %n' <each L1-landed file>                                         rc 0
```

Scratch: `/fast/scratch/hyaku/tsukuroi-r65/N1ScopeCheck/` — created, used for nothing beyond
inspection, **removed** at seat end (confirmation below). No `/tmp` file was used as citable evidence.
No tool was installed (no pacman / uv / npx / release-binary action).
