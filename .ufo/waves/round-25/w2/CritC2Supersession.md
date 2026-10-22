Verdict: partly holds. The central contradiction of oom-event-plane.md line 344 is true: `auto` is the default and is not monitored, so "oomd would likely have acted before the kernel" does not follow. The marking still has five defects. The same claim at kill-event-deep-r8.md lines 255 and 266 is left unmarked, even though a wave-1 seat drafted notices for both. The swap-conjunction point is labelled a contradiction in the notice but "narrows" in the entry, and the entry's supersedes span for it points at the wrong text. The MP6 supersession of line 344 gives a reason that does not bear on that text. The notice leaves out line 274, which the entry narrows three times. SOURCES S120 and the SKILL.md rows carry a mistyped sha256 for the oomd.conf(5) source that the notice relies on.

Seat: CritC2Supersession, FALSIFY wave 2, round 25 attempt 1. Measured revision 5e7c04ecb02735491456de2b8bc44550d0db4609. The files I read (oom-event-plane.md, memory-pressure-r25.{md,json}, kill-event-deep-r8.md, SKILL.md, SOURCES.md) show no working-tree changes against that revision (`git status --short` lists only .ufo files).

## Findings

1. [obs] **The main contradiction holds, and the version gap does not weaken it.** Two points are at issue: that `auto` is the default, and that `auto` means systemd-oomd "will not actively use this cgroup's data for monitoring and detection".
   - Both are stated in systemd v262 `man/systemd.resource-control.xml` lines 1529 ("Defaults to <option>auto</option>") and 1545-1546.
   - The events of 2026-10-13 and 2026-10-14 ran under systemd 261.2-1, not 262. The record is `/var/log/pacman.log`: "upgraded systemd (261.1-1 -> 261.2-1)" on 2026-10-11 and "(261.2-1 -> 262-1)" on 2026-10-20.
   - I fetched tag v261 of both manual sources. `curl https://raw.githubusercontent.com/systemd/systemd/v261/man/systemd.resource-control.xml` and the same path at v262 both hash to sha256 `d57641df40e45811403de91e55059b6a8f7506c6812a85cbe9c6ba22900587d8`. The two `man/oomd.conf.xml` files also hash the same (`36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`). The copies are at /fast/scratch/hyaku/tsukuroi-r25/w2/CritC2Supersession/.
   - So the notice's v262 citation also covers the host as it was at the events. The notice could say this once.
   - The "already set" wording is also correctly marked. Wave-1 ExecRecapture found no fragment or drop-in that sets `ManagedOOM*=` on the four units (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ExecRecapture.md:39). My read-only grep of `/usr/lib/systemd/{system,user}`, `/etc/systemd/{system,user}` and `~/.config/systemd/user` for `ManagedOOM` (exit 0) matches only `systemd-oomd.socket:22` (`ListenStream=/run/systemd/oom/io.systemd.ManagedOOM`).

2. [obs] **kill-event-deep-r8.md lines 255 and 266 carry the same superseded claim and have no R25 marking.**
   - Line 255 (/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/kill-event-deep-r8.md:255) says "`ManagedOOMSwap=auto` **and** `ManagedOOMMemoryPressure=auto` are already set on `user-1000.slice`, `user@1000.service` and sampled app scopes". It then infers "the swap rule (90 %) is below event A's measured 99.9999 % saturation, so oomd would have had a trigger; ... policy kills before the kernel needs to act". That has both defects the notice names: the armed reading and the swap-only rule.
   - Line 266 (row 12, "oomd kill selection") says "if oomd is enabled, `ManagedOOMPreference=avoid/omit` ... is the steering knob — measured as available, not configured". With every unit `auto`, enabling oomd monitors nothing, so the knob does nothing.
   - The search finds no R25 marking in the file. `git show 5e7c04ec:corpus/knowledge/kill-event-deep-r8.md | grep -c R25` returns 0, and the file's only appended notices are the four R18-FRESHNESS sections (lines 350-376).
   - No `supersedes` entry in memory-pressure-r25.json names this file. Every `"file"` value is `corpus/knowledge/oom-event-plane.md` (json lines 72, 149, 156, 227, 308, 315, 392, 470, 477).
   - Wave 1 had already found both lines. /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ScribeSupersession.md:49 ("F2 — `kill-event-deep-r8.md:255` ... CONTRADICTED") and :105 ("F8 — `kill-event-deep-r8.md:266` ... NARROWED") include drafted Notice B (:216) and Notice G (:355). The L1 integrated only a single combined notice on oom-event-plane.md.
   - [inf] A reader who reaches the round-8 deep note through SKILL.md:1080-1135, which summarises it, still meets the "oomd would have had a trigger" reading with nothing pointing to the correction.

3. [obs] **The notice and the entry disagree on the relation of the swap point, and the entry's quoted span is the wrong text.**
   - The notice says "Line 344 is contradicted on two points" and makes the swap conjunction the second point (oom-event-plane.md:473).
   - The entry records that point as MP5 `"relation": "narrows"` (memory-pressure-r25.json:394).
   - MP5's `earlier_text` is "`oomd.conf` all-commented (defaults `SwapUsedLimit=90%`, `DefaultMemoryPressureLimit=60%`, `DefaultMemoryPressureDurationSec=30s`)" (json:395). That is the measured-state cell, and MP5 itself rates it `verified`.
   - The swap-only reading actually sits in the mechanism cell of the same line: "event B met a swap plane at ≈99.9 % and event A at 100 % — above oomd's 90 % swap rule" (oom-event-plane.md:344). So the entry marks a true statement and leaves the defective clause unquoted.
   - [inf] "Narrows" is the right label, not "contradicts". In v262 the memory arm is `mem_used = mem_total - mem_available` (src/oom/oomd-util.c:791), tested next to the swap arm in oomd-manager.c:478-479. Event A's own dump shows free memory "below the min watermark" and `Free swap 44kB` (oom-event-plane.md:81-82). So the memory arm was very likely above 90 percent too. The conjunction fixes the reasoning but not the trigger premise for event A. Only the MP4 point turns the conclusion.

4. [obs] **The MP6 supersession of line 344 is wrongly marked.**
   - memory-pressure-r25.json:477-481 marks "oomd would likely have acted *before* the kernel, at the cost of policy-driven kills (it kills the pressured cgroup's processes)" as `supersedes`. The stated reason is "A userspace killer's SIGKILL is not kernel OOM-kill accounting; the two are counted separately".
   - Line 344 says nothing about counters or accounting. The reason is true but does not contradict the quoted text.
   - The notice cites only "rows MP4 and MP5" for line 344, so the notice and the JSON also disagree on which rows bear on that line.
   - [inf] The parenthetical "it kills the pressured cgroup's processes" is in fact imprecise. The monitored unit is not itself a candidate, and oomd kills a descendant leaf or `memory.oom.group=1` cgroup (v262 `man/systemd-oomd.service.xml` lines 48-51, sha256 `4b29be2e41ef309beb9f9a9fcc9a84f18cd7f9f3540f094b0b5717891ef8651d`: "only descendant cgroups are eligible candidates for killing"). That would be a valid MP4 narrowing, but MP6 does not make it.

5. [obs] **Line 274 is narrowed three times in the entry but is missing from the notice.**
   - The JSON narrows oom-event-plane.md:274 in MP2 (json:149-153), MP3 (json:227-231) and MP6 (json:470-474).
   - The notice mentions lines 344, 301 and 347 only.
   - It also says "Line 301 is narrowed by row MP2", but the JSON narrows line 301 in both MP1 (json:72-77) and MP2 (json:156-160).
   - A reader at line 274 ("the pressure signals in this plane are `memory.swap.peak`, `memory.swap.events.fail`, `pswpin/pswpout`, PSI, and the kernel/systemd records") gets no pointer.
   - Every JSON `earlier_text` does match its cited line. A substring check on each `...`-separated fragment returned True for all 9 entries.
   - tools/check-memory-pressure.py checks only that `supersedes` is a list (line 631). Neither defect above, nor the notice's coverage, is gated.

6. [obs] **The sha256 recorded for source S120 (the oomd.conf(5) source behind the notice's second point) is mistyped in committed files.**
   - SOURCES.md:126 and SKILL.md:2307, 2313 and 2317 give `36ae3e474a6e5632d4a61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`.
   - The fetched bytes hash to `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`; positions 17-19 read `d4a` where they should be `a4d`.
   - memory-pressure-r25.md:85 and every wave-1 source seat (SrcOomdConf.md:21, :68; SrcSystemdCode.md:23; CritC2Learning.md:44) carry the correct hash. The typo first appears in .ufo/waves/round-25/w1/DraftSkillTable.md:21, 40, 46 and 50. Command: `grep -rnoE "36ae3e474a6e5632[0-9a-f]{48}" SKILL.md corpus .ufo/waves/round-25`.

7. [obs] **The entry's supersession reason says more than MP4's verdict allows; the notice itself stays in scope.**
   - MP4's verdict says "a unit outside those four was not read by the capture, so no host-wide statement is made" (memory-pressure-r25.md:209-211).
   - Its supersedes reason then says "on this host systemd-oomd would have had no monitored cgroup even if it had been running" (memory-pressure-r25.md:253-254; json:312). That is both host-wide and about 2026-10-14.
   - The notice's own wording, "an enabled systemd-oomd would have monitored none of them", is scoped to the four units and is fine.
   - My live read today closes the user-manager side: `systemctl --user show -p ManagedOOMSwap -p ManagedOOMMemoryPressure app.slice session.slice background.slice` shows `auto` on all three.
   - [unk] For 2026-10-14, user.slice, -.slice and user-manager units were never read. A drop-in removed before 2026-10-22 cannot be ruled out from retained state. `pacman -Ql systemd` (262-1) ships no `ManagedOOM` drop-in, and the remaining drop-ins have old mtimes (`/usr/lib/systemd/system/user@.service.d/10-login-barrier.conf` Sep 22; `/etc/systemd/system/user@.service.d/faster-shutdown.conf` Oct 3).

8. [obs] **The notice does not mark line 344's action cell.**
   - Line 344's operator action is "`systemctl enable --now systemd-oomd`". Under all-`auto`, that action alone monitors nothing (MP4 action: "Enabling the unit would still monitor nothing while every unit stays `auto`", memory-pressure-r25.md:214-215).
   - The R25 notice implies this but does not say the action cell is superseded as current-use guidance.
   - The R18 notices in the same file set the precedent of naming action cells explicitly ("Its install action is superseded as current-use guidance only", oom-event-plane.md:452; "Its 'enable zswap' action is superseded", :460).

9. [obs] **These statements are correctly left unmarked:**
   - oom-event-plane.md:237 and :422 are a measurement cell and a probe-ledger line with no inference.
   - Lines 280-281 ("Nothing was configured to act before the kernel") agree with all-`auto`. Its earlyoom part is already covered by R18-PRECISION (:468).
   - SKILL.md:809-812 is the same no-guard bullet and is already R18-noticed at SKILL.md:1938.
   - adjacency-anchors-r19.md:163 and :171 quote line 344 only up to "`is-enabled`=disabled;", which is still true.
   - The mori citations of 344-346 (`mori-shokunin/PROVINCE.md:66`, `mori-shokunin/corpus/knowledge/userspace-oom-killers-r12.md:8`) rely on service state, not on the inference.
   - PROVINCE.md and corpus/lessons contain no "already set", "would likely have acted" or ManagedOOM claim.
   - The notice's earlyoom sentence checks out: capture-earlyoom.txt lines 6, 9 and 12 show `active`, `enabled` and `earlyoom 1.9.0-1`, and its sha256 `7adbe069...` matches the declaration.

10. [inf] **Caution for whoever integrates the drafted Notice B.** ScribeSupersession.md:57 says that `memory.oom.group` = 0 means "the eligible-candidate set would have been empty even if `kill` had been set". The manual says "only leaf cgroups and cgroups with memory.oom.group set to 1 are eligible candidates" (systemd-oomd.service.xml:50-51). Leaf app scopes are eligible whatever `memory.oom.group` says, so that sentence must not be copied into a notice.

## Impacted axes

Depth and calibration of C2 (supersession correctness), freshness (current-use marking of kill-event-deep-r8.md) and source provenance (S120 hash). The verified-row count of 6 is not affected: none of these defects is a counting input of `tools/check-memory-pressure.py`.

## Smallest safe correction

All append-only; L1 only:
- Append one R25 current-use notice to kill-event-deep-r8.md covering line 255 (the armed reading and the swap-only trigger, with the event-A memory arm as [inf]) and line 266 (the knob is inert while every unit is `auto`). Add matching `supersedes` entries to MP4 and MP5.
- In the oom-event-plane.md notice, either append a precision line or carry it in the next record:
  - the second point is a narrowing, not a contradiction;
  - the action cell is superseded;
  - line 274 is narrowed by MP2, MP3 and MP6;
  - line 301 is narrowed by MP1 as well as MP2.
- Fix MP5's `earlier_text` to quote the mechanism cell ("above oomd's 90 % swap rule"). Drop the MP6 entry for line 344, or replace its reason with the descendant-candidate narrowing.
- Scope the MP4 reason to "the four captured units".
- Correct the S120 sha256 in SOURCES.md:126 and SKILL.md:2307, 2313 and 2317 to `36ae3e474a6e5632a4d61ae91b4d930bc9c3657ebf9f9081db5b7ba4cc926617`.

Scope: read=SCORECARD.md round-25 sections, oom-event-plane.md, memory-pressure-r25.md and .json, kill-event-deep-r8.md, SKILL.md, SOURCES.md, PROVINCE.md and corpus grep, tools/check-memory-pressure.py, round-25 capture and capture-earlyoom, w1 ScribeSupersession and other w1 reports by grep, mori PROVINCE.md:66 and userspace-oom-killers-r12.md:8, systemd v261/v262 manual and source files over public HTTPS; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w2/CritC2Supersession.md, /fast/scratch/hyaku/tsukuroi-r25/w2/CritC2Supersession/ (fetched xml and c files); executed=git log/status/show (read-only), pacman -Q and -Ql systemd, grep of /var/log/pacman.log, ls of unit drop-in directories, grep of unit directories, systemctl show and is-active and is-enabled (system and --user), curl of raw.githubusercontent.com systemd v261 and v262 files, sha256sum, diff, a read-only python3 substring check of the JSON supersedes entries
Model: not exposed
Installs: none
