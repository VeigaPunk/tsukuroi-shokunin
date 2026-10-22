# ScribeNotices — round 24, wave 1

Seat: TsukuroiR24.ScribeNotices-2 (scribe, leaf; no delegation, no background jobs).
Date: 2026-10-22. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scope: C2 supersession notices — append-only dated notices for `corpus/README.md`
`## Frontier`, `corpus/knowledge/partial-upgrade-recheck-r15.md`, and `PROVINCE.md`
`## Frontier`.

**Verdict: three notice drafts are written and every factual claim in them is
anchored to the committed round-24 L1 capture; `PROVINCE.md` `## Frontier` carries
no C2-superseded premise, so no supersession notice is owed there, and the one
candidate additive bullet is offered as a draft for the L1 to accept or drop.**

## Findings

1. [obs] The `corpus/README.md` `## Frontier` bullet "Pending `mkinitcpio` 42
   upgrade strands two `/new_root` hooks (`initramfs-v42-sysroot-recovery.md`)"
   is at `corpus/README.md:38-39`; the `## Frontier` section runs from
   `corpus/README.md:28` to the `## Erratum` heading at `corpus/README.md:44`.
   The bullet must not be rewritten — the notice is a new bullet appended at the
   end of that list, after the "Where to learn more" bullet at
   `corpus/README.md:42`.

2. [obs] The half of that bullet that is stale is the "pending upgrade" half:
   `mkinitcpio 42.2-1` is installed
   (`.ufo/waves/round-24/capture/l1/capture.txt:61-63`) and the sync database
   carries the same version (`capture.txt:77-79`); the 2026-10-20 09:15 -03
   upgrade is recorded at `corpus/README.md:150` and by the sync marker
   `2463:` at `capture.txt:132`.

3. [obs] The hooks are unchanged: `/usr/lib/initcpio/hooks/btrfs-overlayfs:4` and
   `/usr/lib/initcpio/hooks/plymouth:11` still name `/new_root`
   (`capture.txt:91-94`); the 42.x build root creates `new_root` as a relative
   symlink to `sysroot` (`/usr/lib/initcpio/functions:1213`, via
   `capture.txt:115-117`); the busybox init mounts root at `/sysroot` and calls
   `switch_root /sysroot` (`capture.txt:104-112`).

4. [obs] Two boots completed after the upgrade — boot `-1` (2026-10-20 09:57
   -03) and boot `0` (2026-10-22 04:55 -03), `capture.txt:11-16` — and Plymouth
   started and terminated in both (`capture.txt:136-151`, `capture.txt:153-167`).
   [inf] Because both boots post-date the 09:15 -03 upgrade, the ordinary boot
   path on a 42.2 image is now observed rather than inferred; `corpus/README.md:151`
   still carries round 17's "not boot-tested" wording, and the round-24 notice
   adds the newer observation without editing that line.

5. [unk] A snapshot boot — the only path where `btrfs-overlayfs` acts — has not
   been exercised on a 42.2 image. This is the residual open item and it is
   recorded as unknown in `corpus/knowledge/pause-lift-gate-r24.md` § P3. The
   notice therefore supersedes the "pending upgrade" wording only and leaves
   the upstream-watch item standing (`corpus/README.md:152-153`).

6. [obs] `corpus/knowledge/partial-upgrade-recheck-r15.md:14` still reads
   `| pending_updates | 413 | 0 / empty | ... |`, and the numeral is repeated at
   `:32` and at `:68-69` (R15-BOUNDARIES 3). The file already records at
   `:176` (R17-FRESH-PARTIAL-02) that 413 was not re-measured and was
   superseded by the 09:15 full upgrade. The round-24 notice adds the missing
   current measurement: `pacman -Qu` returned 3 rows — `1password-beta`,
   `chatgpt-bin`, `claude-code` (`capture.txt:38-42`), count 3
   (`capture.txt:45-47`), repositories `omarchy`, `openai-chatgpt`, `omarchy`
   (`capture.txt:50-54`), so no boot-chain package is pending.

7. [obs] The boot-chain packages read the same installed and sync versions
   (`capture.txt:61-88`), no installed package is newer than its sync-database
   version (`capture.txt:57-59`), and `libinput 1.32.0-1` is installed
   (`capture.txt:73`) and also the sync version (`capture.txt:88`). The
   R15-HANDOFF wording "the pending set crosses the boot chain" therefore
   describes the 2026-10-20 state, not the 2026-10-22 state; the notice says so
   and leaves the decision `BLOCKED_FOR_AGENT_PACKAGE_ACTION` and the
   operator's boot/recovery gate untouched.

8. [obs] During the host-wide pause the pacman log records five installs —
   `zcode`, `tizen-sdb`, `tizen-sdb-debug`, `openssl-1.0`, `openssl-1.0-debug`
   (`capture.txt:120-126`) — plus one `pacman -Sy --noconfirm` at 2026-10-21
   20:32 -03 (`capture.txt:133`), while the core/extra/multilib database mtimes
   remain 2026-10-17 22:37 -03 (`capture.txt:29-33`). The r15 notice cites this
   as [obs] and defers the upgrade-target reading to the gate entry § P4.

9. [obs] `PROVINCE.md` `## Frontier` (`PROVINCE.md:75-106`) holds two bullets
   (`:77-78`, `:79-80`), the "Out of province → report, never absorb." line
   (`:82-83`) and the Round-12/13/14 refinement paragraphs (`:85-106`). A
   search of the whole file for `mkinitcpio`, `new_root`, `413`, `pending`,
   `partial` and `upgrade` returns three hits, none of them in `## Frontier`:
   `PROVINCE.md:20` (Arch News upgrade gate), `:22` (Initramfs v42 and boot
   recovery), `:27` (never installs, upgrades, or removes packages). [inf] No
   C2 premise is stale there and the capture does not contradict any of the
   three hits, so no supersession notice is owed in `PROVINCE.md`.

10. [obs] One round-24 residual is inside this lane's domain and is not yet
    carried by `PROVINCE.md` `## Frontier`: the untested snapshot-boot path on a
    42.2 image. The PROVINCE draft therefore offers one clearly labelled
    **additive** bullet (supersedes nothing) for the L1 to accept or drop.

## Gates and constraints observed

- Read-only. No pacman transaction, no `pacman -Sy/-S/-Syu/-Scc`, no
  `paccache`, no service restart, no initramfs rebuild, no boot, no
  configuration write, no git write command. The host-wide pacman pause was
  not touched.
- No production lane file was edited by this seat. `corpus/README.md`,
  `corpus/knowledge/partial-upgrade-recheck-r15.md` and `PROVINCE.md` are
  unchanged; every notice is a draft under this seat's own directory. [obs] The
  lane working tree also carries in-flight sibling edits — `tools/check-pause-gate.py`,
  `tools/report-red-causes.py`, `.ufo/waves/round-24/capture/capture.sh` and the
  untracked `corpus/knowledge/pause-lift-gate-r24.md`, `capture/l1-3/`,
  `capture/l1-4/` — none of them written by this seat.
- Every notice is append-only by construction: the drafts state the insertion
  point, quote the superseded text, and never propose an edit to an existing
  byte.
- No external source was opened this session, so no `corpus/SOURCES.md` row is
  drafted; the notices cite only lane-internal captures and corpus entries.

## Conflicts and risks for the canonical judge

- The gate entry `corpus/knowledge/pause-lift-gate-r24.md` is, at drafting
  time, an **untracked working-tree file** (`git status` shows it as `??`);
  it was produced in this wave by the sibling gate-entry seat. The notices cite
  its **section headings** (§ P1–§ P5, § Supersedes), not line numbers, so
  later edits of that file do not silently break the citations.
- The schema'd gate JSON `corpus/knowledge/pause-lift-gate-r24.json`, which
  `tools/check-pause-gate.py` reads, does not exist in the working tree at
  drafting time (only the `.md` does). That is the gate-entry seat's and the
  L1's surface, not mine; it is recorded here because the notices quote the
  gate entry as their reference.
- The round-24 capture exists in two committed revisions:
  `capture/l1/capture.txt` (198 lines, committed at `674891d`) and
  `capture/l1-2/capture.txt` (708 lines, committed at `10b45f0`). The gate
  entry cites the `l1-2` line numbers for the mirror, cache and
  sudo-attribution facts. My notices cite `capture/l1/capture.txt` for every
  claim they make, so they stand on the smaller committed capture alone; where
  the notices mention the cache or the mirror they point at the gate entry
  instead.
- Two further capture directories, `capture/l1-3/` and `capture/l1-4/`, are
  untracked in-flight sibling artifacts and are not cited by any notice here;
  if the L1 prefers a newer capture as the citation base, the notice text
  stays valid because every pointer is a command-output locator inside a named
  capture file.

## Out of scope for this seat

- Writing the notices into `corpus/README.md`, `corpus/knowledge/partial-upgrade-recheck-r15.md`
  and `PROVINCE.md` — the L1 is the only integrator and the only VCS writer.
- The gate entry itself, the `pause-lift-gate-r24.json` file, the checker run
  and the `SKILL.md` registry row (sibling seats).
- The C1 per-cause report and the C1/C2 claim measurement (other seats).

## Artifacts

- `.ufo/waves/round-24/w1/ScribeNotices/2026-10-22-corpus-README-frontier-notice.md`
- `.ufo/waves/round-24/w1/ScribeNotices/2026-10-22-partial-upgrade-recheck-r15-notice.md`
- `.ufo/waves/round-24/w1/ScribeNotices/2026-10-22-PROVINCE-frontier-notice.md`
- `.ufo/waves/round-24/w1/ScribeNotices.md` (this report)

Scope: read=corpus/README.md, corpus/knowledge/partial-upgrade-recheck-r15.md, corpus/knowledge/pause-lift-gate-r24.md, PROVINCE.md, corpus/QUALITY.md, tools/check-pause-gate.py, .ufo/waves/round-24/capture/l1/capture.txt, .ufo/waves/round-24/capture/l1-2/capture.txt, .ufo/waves/round-24/w1-assignments.json, .ufo/waves/round-24/w1-spec.json, git log/status of the lane repo; wrote=.ufo/waves/round-24/w1/ScribeNotices/2026-10-22-corpus-README-frontier-notice.md, .ufo/waves/round-24/w1/ScribeNotices/2026-10-22-partial-upgrade-recheck-r15-notice.md, .ufo/waves/round-24/w1/ScribeNotices/2026-10-22-PROVINCE-frontier-notice.md, .ufo/waves/round-24/w1/ScribeNotices.md; executed=read-only file reads, grep/awk line-number verification over the lane repo, git log --oneline, git status --porcelain, ls -la of the capture and knowledge directories — no package-manager, service, boot or VCS write command
Installs: none
