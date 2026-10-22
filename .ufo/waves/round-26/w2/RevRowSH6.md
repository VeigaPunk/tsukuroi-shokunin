# RevRowSH6 review: SH6 (NVMe lifetime counters and Unexpected Power Losses) at 7dfea9244a84a0e2439f0698e54491e5d7b7c467

Verdict: Partly holds. Every cited line number and every quoted string matches its source or the frozen capture, and no SH6 action changes the host. The statement misstates the Unexpected Power Losses trigger, the HEALTHY verdict does not follow for that signal, the "not a count of host-visible crashes" claim is overstated, and the journal method "date abrupt boot ends" is unsupported. The SKILL.md row repeats these faults.

## Findings

1. **The Unexpected Power Losses trigger is misstated, and "only" is contradicted by the source.** [obs]
   - Affected text: `corpus/knowledge/storage-health-r26.md:85` ("increments only when main power is lost while the controller had not reported it was ready to power off"); `corpus/knowledge/storage-health-r26.json:271` (same sentence); `corpus/SOURCES.md:141` (S135 claim column: "increments only when main power is lost before the controller reports it is ready to be powered off").
   - Source: `.ufo/waves/round-26/sources/S135.txt:238-258`. The text reads "This count shall be incremented if, and only if, main power is lost when:" and then gives two clauses. Clause (a): the controller "does not report it is ready to be powered off (i.e., the CSTS.SHST field is not set to 10b)". Clause (b): "shutdown processing was reported as in progress or was reported as complete", and when power was lost "the media was not in a shutdown state as a result of processing an Admin command received via the out-of-band mechanism", with the Ignore Shutdown bit set. The row keeps clause (a) and drops clause (b).
   - Independent check: I fetched the NVMe 2.4 PDF with plain curl. Its sha256 is fe7647532c06859f2952d9db1f90165aa3e9375343d588d5444253f7dbb2c9bd, which matches `SOURCES.md:141`. pdftotext 26.08.0 with no flags gives sha256 c39f3403106ca496dff79a3b2b4860bf1b422a6695e49e7b5d9fef15787fe20e, which also matches. The same two-clause text is at `/fast/scratch/hyaku/tsuku26/w2/RevRowSH6/src/nvme-2.4.txt:21507-21527`. The excerpt slice is byte-identical to `S135.txt` (sha256 0819e59f573ec66617b7f49953e43175a578ff5822f10c7ede2df263c8fc4c81).
   - Fix: quote both clauses, or drop the trigger sentence.
   - [unk] The excerpt does not define "shutdown state" in clause (b). Read literally, clause (b) may also reach power losses after a routine shutdown. The entry should not settle that by assertion.

2. **"So it is not a count of host-visible crashes" is overstated and contradicted by the lane's own wave-1 work.** [inf]
   - Clause (a) counts any main-power loss while SHST is not 10b, whatever the host was doing. A hang that ends in a hard power-off increments the counter.
   - The wave-1 seat wrote exactly that: `.ufo/waves/round-26/w1/ConnSiblingOverlap.md:54` ("A hard power-off after a memory-pressure hang would add to Unsafe Shutdowns: 200").
   - What the source supports: a software crash that keeps power on does not increment the count. A power loss that also crashes the host does.

3. **The HEALTHY verdict does not follow for the Unexpected Power Losses signal.** [obs]
   - The vocabulary (`storage-health-r26.json:20`) defines HEALTHY as "the host reading shows no fault on this signal". The verdict appears at `storage-health-r26.md:89`, `storage-health-r26.json:273` and `SKILL.md:2368`.
   - The zero readings support HEALTHY for media and data integrity errors (capture line 197; nvme-cli line 224) and for error log entries (capture line 198; nvme-cli line 225).
   - The 200 Unsafe Shutdowns (capture line 196; nvme-cli line 223) do not support it. S135 gives no threshold, and `S134.cpp:528` only prints the count. The row's own host reading says "most of the 200 cannot be dated" (`storage-health-r26.md:87`). The action needs "two dated reads" (`:91`), and the row has one.
   - [inf] Split the verdict: HEALTHY for the two zero counters, and UNVERIFIED for the power-loss count. UNVERIFIED is defined as "the evidence needed to judge this signal does not exist on the host" (`storage-health-r26.json:23`), which fits here.

4. **The lifetime sentence drops the source's qualifier.** [obs]
   - `storage-health-r26.md:85` says the log "reports information over the life of the controller, retained across power cycles". The source says "The information provided is over the life of the controller and is retained across power cycles unless otherwise specified." (`S135.txt:13-14`).
   - The spec marks some fields as current state. Critical Warning bits "represent the state at the time the Get Log Page command is processed" (`S135.txt:48-53`). The Endurance Group summary bits "represent the current associated state and are not persistent" (`S135.txt:139-140`).
   - Lifetime is quoted explicitly only for the error log count (`S135.txt:276`). "Not dated events" for Power Cycles and media errors has no quote [inf]; the figure lists no time field for them.
   - The critic seat kept the qualifier (`.ufo/waves/round-26/w1/CritLearningFrontier.md:57`); the landed row dropped it.

5. **"Date abrupt boot ends from the journal" is an unsupported method, and the entry contradicts it.** [obs]
   - Affected text: `SKILL.md:2368` ("how to read it" column). `storage-health-r26.md:102` says the journal-boot plane "dates abrupt boot ends" in the same bullet that says "a missing record is not an unsafe shutdown".
   - My read-only checks on this host: boot -1 ends at 2026-10-22 04:54:50 -03 inside a systemd shutdown sequence ("Stopping Flush Journal to Persistent Storage...", then "Unmounted /var/cache/pacman/pkg.") with no final record (`sudo -n journalctl --no-pager -b -1 -n 14 -o short-iso`, exit 0). Boot -2 ends at 2026-10-20 09:56:15 -03 in ordinary runtime lines (UFW BLOCK, a waybar core dump) with no shutdown sequence (`sudo -n journalctl --no-pager -b -2 -n 8 -o short-iso`, exit 0).
   - Neither end shows whether power dropped. The journal dates the last entry of each boot (the LAST ENTRY column of `journalctl --list-boots`). It does not classify abruptness. `.ufo/waves/round-26/w1/ScoutJournalBoots.md:60-61` makes the same point.
   - Fix: say the journal dates boot end times. Remove "dates abrupt boot ends" from `storage-health-r26.md:102` and from the SKILL.md cell.

6. **The row does not bind its counts to a device, and the limits miss a second NVMe controller.** [obs]
   - The capture reads `/dev/nvme0n1` (smartctl, capture line 176) and `/dev/nvme0` (nvme-cli, line 206). The LUKS root is `nvme0n1p2` (line 32).
   - The kernel names swapped between boots. Boot 0 maps nvme0 to PCI 0000:02:00.0 and nvme1 to 0000:15:00.0. Boot -1 maps nvme0 to 0000:15:00.0 and nvme1 to 0000:02:00.0 (`sudo -n journalctl -k --no-pager -b -1 --grep "pci function" -o short-iso` and `-b 0`, both exit 0).
   - [inf] The 200 counts therefore belong to PCI 0000:02:00.0 in boot 0, the root drive. A "two dated reads" comparison across a reboot could compare two different drives unless it binds the PCI address or the serial. The row binds neither.
   - The limits (`storage-health-r26.md:110`) say "One capture, one host, one device." The journal shows two NVMe controllers, and the second is unmeasured. `.ufo/waves/round-26/w1/ConnSiblingOverlap.md:92-97` proposed this binding and a limit sentence; the landed text has neither.

7. **"A high lifetime ratio alone is not a fault" is an undefined judgment.** [obs]
   - Affected text: `storage-health-r26.md:91`, `storage-health-r26.json:274`, `SKILL.md:2368`.
   - Neither "high" nor "lifetime ratio" is defined. The ratio would be 200 over 325, about 61.5% [inf], and the row never states it. No source gives a threshold. Delete the sentence, or define the ratio and its basis.

8. **Other universal or unsupported words.** [obs]
   - `storage-health-r26.md:102`: "narrow" has no source. "A missing record is not an unsafe shutdown" is universal; the one proof case (boot -1) supports only "does not by itself show".
   - `storage-health-r26.md:87`: "most of the 200 cannot be dated" is an inference from the journal's boot count. The counter carries no timestamps, and that is the sentence to keep.
   - `storage-health-r26.md:87` and `SKILL.md:2368`: "retained". The list-boots count of six is correct. The header is excluded, the `tail -n +2` in capture line 160 is right, and the current list shows boots -5 through 0. But `.ufo/waves/round-26/w1/ScoutJournalBoots.md:5-7` says the three oldest boots (-5, -4, -3) have no system journal left. My check of the last three lines of boots -5 and -3 showed only user-manager lines, which does not settle it [unk]. "Readable" is the more accurate word.

## What holds

- Line numbers. `storage-health-r26.md:87` and `SKILL.md:2368` cite capture lines 194, 196-198, 221 and 223-225. Each matches `.ufo/waves/round-26/capture/capture.txt`, whose sha256 is 002bef16... and matches the pin. The JSON capture pointers 194, 196 and 223 carry the tokens "Power Cycles", "Unsafe Shutdowns" and "unsafe_shutdowns" on those lines.
- Quotes. All four JSON quotes appear verbatim: `S135.txt:14`, `S135.txt:258`, `S135.txt:276` and `S134.cpp:528` (checked by script). The S134 snapshot equals upstream smartmontools RELEASE_7_5 `nvmeprint.cpp` (sha256 4770d985..., fetched from raw.githubusercontent.com).
- Actions do not change the host. Each named command is read-only and on the allow-list: `sudo -n smartctl -H -A`, `sudo -n nvme smart-log`, and `journalctl`.
- Lifetime wording. The general sentence at `S135.txt:13-14` supports "lifetime" for all four listed counters, with the qualifier. Line 276 supports it explicitly for the error log count only.
- The JSON row and the SKILL.md row carry the same numbers and verdict as the markdown.

## What the gate cannot see

`tools/check-storage-health.py` header (lines 9-23): R2 checks only that a verdict and an action exist. R4 checks quote presence, and R5 checks pointer uniqueness. No rule tests a statement or whether a verdict follows. The measure file `.ufo/waves/round-26/measure/c1-7dfea924.json` records SH6 with `"findings": []`. So the 6-of-6 measurement says nothing about findings 1 to 3.

The SKILL.md row (`SKILL.md:2368`) repeats findings 3, 5, 6 (no device binding), 7 and 8. It does not repeat findings 1 or 2. It needs the same fixes.

## Minimal fixes (recommendations; no edits made)

- Replace the trigger sentence with both clauses (a) and (b), or drop it.
- Remove "not a count of host-visible crashes", or rewrite it as in finding 2.
- Split the verdict: HEALTHY for the two zero counters, UNVERIFIED for the power-loss count.
- Restore "unless otherwise specified" and qualify the lifetime claim.
- Replace "date abrupt boot ends from the journal" with "date boot end times from the journal".
- Bind the SH6 counts to PCI 0000:02:00.0 (boot 0) and name the second NVMe controller as unmeasured. Require PCI or serial binding in the two-read action.
- Delete "high lifetime ratio alone", or define the ratio.
- Change "retained" to "readable", and remove "narrow".

## Unknowns and gaps

- [unk] Whether clause (b) reaches routine clean shutdowns.
- [unk] System journal content of boots -5, -4 and -3. I checked only the last three lines of -5 and -3, and did not check -4.
- [unk] The wave-1 "proven orderly reboot" (boot -1, "System is rebooting." at 04:54:48). I did not verify that line.
- [inf] The root drive's PCI address in boot 0. It rests on capture line 32 and the boot 0 kernel mapping.
- Not run: `tools/check-storage-health.py`. Its `--revision` mode reads git history, and my sandbox has none.

Scope: read=lane storage-health-r26.md and .json (SH6); SKILL.md 2357-2375; SOURCES.md 135-145; S134.cpp and S135.txt snapshots; capture.txt; w1 ScoutJournalBoots.md, ConnSiblingOverlap.md, CritLearningFrontier.md, DraftEntry.md; measure/c1-7dfea924.json (grep); checker header lines 1-66 and grep hits; NVMe 2.4 PDF and smartmontools nvmeprint.cpp fetched from public URLs; journal and kernel log via read-only commands; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-26/w2/RevRowSH6.md, /fast/scratch/hyaku/tsuku26/w2/RevRowSH6/sb/, /fast/scratch/hyaku/tsuku26/w2/RevRowSH6/src/; executed=git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive 7dfea9244a84a0e2439f0698e54491e5d7b7c467 | tar -x (sandbox; cmp shows four files identical to the working copy), curl (NVMe 2.4 PDF; nvmeprint.cpp at RELEASE_7_5), sha256sum, pdftotext (no flags), python checks of quotes, pointers and slice hashes, journalctl --list-boots --no-pager, sudo -n journalctl (boots -1, -2, -3, -5; kernel pci-function lines in boots -1 and 0)
Model: anthropic/claude-haiku-5-5 (stated in this session's workstation context)
Installs: none
