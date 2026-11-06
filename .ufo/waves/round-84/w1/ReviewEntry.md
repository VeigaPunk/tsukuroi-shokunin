# ReviewEntry — non-author per-row review of C1 `hibernate-resume-plane-r84` (round 84 w1)

Reviewer: ReviewEntry (leaf, no subagents). Not an author of the entry.
Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` →
`c6941adbcd972de8ad1b93ce5f796e16ea630858`. Master moved past the declared tip `69915b86` by two registry
commits (`c6941adb`, `f19e73f3`); `git diff 69915b86..master --stat` → `SKILL.md | 8 ++++++ 1 file changed`
— the reviewed entry files (`corpus/knowledge/hibernate-resume-plane-r84.{md,json}`) are byte-identical at
`c6ee78b2`, `69915b86`, and master.

## What I ran (all read-only)

- `sha256sum -c SHA256SUMS` in `before/src/` → 8/8 OK, `src_rc=0`; in `before/host/` → 2/2 OK, `host_rc=0`.
- `python3 tools/count-resume-rows-r84.py --revision master` → `{"verdict": "met", "counted": 10, "failed": 0,
  "distinct_snapshots": 6, ...}`, `rc=0` — independently reproduces the frozen shape-gate reading. This is a
  provenance gate, not a measurement; the judgment below is mine, per row.
- Line-numbered greps of every quoted span in the pinned snapshots: every cited quote is verbatim in the
  snapshot at exactly the cited lines (HR1 :6581-6582, HR2 :127, HR3 :118, HR4 :13, HR5 :57-58, HR6 :61,
  HR7 :38, HR8 :307-308, HR9 :11-12, HR10 :97-98). No off-by-one, no widened span.
- Line-numbered grep of `before/host/receipt.txt`: every cited host line matches (:4, :9, :13, :17, :24, :32,
  :36, :40, :44, :56, :71, :75, :79).
- `date -d @1791060333` → `2026-10-03 17:45:33 -0300` (HR6 conversion exact).
- `cmp` of `before/src/mkinitcpio-{hooks,install}-resume` vs `/usr/lib/initcpio/{hooks,install}/resume` →
  identical both (supports the .md's byte-identity claim, which I verified independently).
- Prior-state scan at `64f45b79`: `git grep -n 'map-swapfile' 64f45b79 -- corpus/knowledge` → no output,
  exit 1; `git grep -n 'resume_offset' 64f45b79 -- corpus/knowledge` → exactly two hits,
  `journal-boot-plane.md:62` and `systemd-user-plane.md:218`, both printing the cmdline value
  `resume_offset=3795013` without deriving or checking it.

## Per-row verdicts

| Row | Verdict | Reason (one line) |
|---|---|---|
| HR1 | supports | Quote (:6581-6582) is the kernel-parameters definition (offset of swap header in the `resume=` partition, PAGE_SIZE units, swap-files-only); receipt :4 carries `resume_offset=3795013`; :9 shows the only swap area is the file. |
| HR2 | supports | :127 (+ :128 "divided by page size") supports the rule; receipt :13 `3795013` equals cmdline :4 — the entry's key new claim (the configured offset points at the current swap header) is measured on this host. |
| HR3 | supports | :118-119 says the device physical offset is not filefrag's number; receipt :24 `3530821` ≠ :13/:4 `3795013` — the filefrag trap is real and measured here. "btrfs logical address" is a fair paraphrase of :121-123. |
| HR4 | partial | Rule (:13 NODATACOW ⇒ NODATASUM, no compression) and host `C` attribute (:17) support the core; but the statement's "even on a compress=zstd mount" (and .md status "compress=zstd:3 mount") has no pinned evidence — receipt.txt and facts.json capture no mount options. |
| HR5 | supports | Quote (:57-58 "has to be active (ie. be present in /proc/swaps)") supports the rule; receipt :9 lists the file as active; the "fails if swapped off" phrasing is honest. |
| HR6 | supports | Quote (:61, with :62-63 "resume_offset= … has to be updated") supports the rule; birth `1791060333` verified as 2026-10-03 17:45:33 -03; the trigger is one-directional (different birth ⇒ re-derive), which is the safe direction. |
| HR7 | supports | Quote (:38) states the binary writes major:minor to /sys/power/resume; receipt :40 `253:0` = `fd:0` (:36) = /dev/mapper/root, so the value is in the kernel and matches the resume device. Writer attribution is not shown by the capture, but the row's own Limits section discloses exactly this. |
| HR8 | supports | Quote (:307-308) literally says the sysfs write overrides the cmdline value; receipt :44 `3795013` equals :4 and :13. Minor caveat: three-way equality cannot distinguish "never written" from "rewritten with the same value". |
| HR9 | partial | Quote (:11-12) and systemd 262 (:79) support "adds the binary when systemd ≥ 255", and `after/uki-initrd-contents.txt` shows `usr/lib/systemd/systemd-hibernate-resume` in the booted UKI's initrd. Over-claims: (1) "into a busybox initramfs" mislabels — the snippet adds the binary regardless of flavor and this initramfs is systemd-based; (2) "so resume runs through that binary, not the hook's own resume= parser" is not evidenced: the kernel's own `resume=`/`resume_offset=` parsing (S336) writes the same sysfs values, no hibernation was ever exercised (journal shows `PM: Image not found (code -22)` per boot), and with a systemd flavor there is no busybox resume= parser to exclude; (3) the supporting artifact is unpinned (captured 15:50:19 by a sibling seat, no manifest digest). |
| HR10 | supports | Quote (:97-98 "upper limit of the image size, in bytes") supports the rule; :56 `12835467264` B vs free swap (31722876−11942400) KiB = 19780476 KiB × 1024 = 20,255,127,424 B ≈ 20.3 GB (decimal) — arithmetic checks; "shrinks as swap use grows" is honest. |

Counts: **8 supports, 2 partial, 0 does-not-support.** All 10 rows pass the provenance shape gate; the two
partials are wording/over-claim issues, not provenance or measurement defects.

## Prompted over-claim checks

- HR7 "did reach the kernel": reading `/sys/power/resume` is reading kernel-held state, so the value-side
  claim is supported; the writer-side attribution is not shown — disclosed in the .md's Limits, so not a
  silent over-claim at row level. Keep the Limits paragraph.
- HR9 "resume runs through that binary": over-claimed as runtime attribution; nothing in the capture shows
  the binary executed, and the kernel cmdline parser is an sufficient alternative writer. Suggested wording:
  "so the binary is present in the initramfs the kernel booted; the capture does not show which writer
  (kernel `resume=` parsing or the initramfs binary) set `/sys/power/resume`." Also drop "busybox".
- HR10 "≈20.3 GB free": correct as decimal GB (20.26 GB); would be wrong if read as GiB (18.9). No change
  needed; "GB" is the unit written.

## Claim-level judgment: `unprovable-but-better`

1. The ground is genuinely new: at `64f45b79` `corpus/knowledge/` had zero `map-swapfile` coverage (grep
   exit 1) and exactly two `resume_offset` mentions, both printing the cmdline value (`journal-boot-plane.md:62`,
   `systemd-user-plane.md:218`) without reading whether it points at the swap header.
2. The entry's rules are sourced and check out: all quotes verbatim at exactly the cited spans in sha256-pinned
   snapshots (8/8 OK), all host values at exactly the cited receipt lines (2/2 OK), and the load-bearing new
   rule (HR3: filefrag 3530821 vs map-swapfile 3795013) is measured on this host — the prior state could not
   have warned an operator away from a filefrag-derived `resume_offset=`, a wrong value by 264,192 pages.
3. It is unprovable in the absolute sense the round already concedes: nothing hibernated or resumed the host,
   the journal shows no hibernation, and the .md's Limits say "holds" means configured values agree, not that a
   resume succeeded. So it can never verify as measured.
4. Against the prior state (no entry, cmdline printed twice, filefrag trap unrecorded), the plane adds a
   correct, host-grounded, machine-gated operational surface; the residual defects (HR4/HR9 wording, unpinned
   UKI artifact) are localized and do not touch HR1-HR3/HR5-HR8/HR10.

Therefore: **unprovable-but-better** (8/10 rows support outright, 2 partial with proposed rewording below).

## Proposed patches (NOT applied — lane files untouched per wave bounds; L1 decides)

- `corpus/knowledge/hibernate-resume-plane-r84.json` HR4 `statement`: delete "even on a compress=zstd mount"
  (uncited), or capture `mount -v`/`findmnt -no OPTIONS` options in a future pinned receipt and cite it.
  Same clause in the .md row HR4 status.
- HR9 `statement`: replace "into a busybox initramfs" with "into the initramfs"; replace "so resume runs
  through that binary, not the hook's own resume= parser" with "so the binary is present in the initramfs the
  kernel booted; the capture does not show which writer set /sys/power/resume".
- Optionally promote `.ufo/waves/round-84/after/uki-initrd-contents.txt` into the pinned set (sha256 into the
  host manifest) if HR9 is to keep citing it as row evidence.

## Residual risk / verification gaps

- No hibernation was exercised (host is read-only this round by rule); the plane's "holds" is configuration
  agreement, as its Limits state. The first real resume remains untested ground.
- HR6's birth-time trigger is one-directional; a reflink/clone-preserved birth time after recreation would not
  trigger a re-derive. Gate HR-SWAP checks and the operator action already mandate map-swapfile after any
  recreation, which covers it operationally.
- The UKI initrd artifact carries HR9 weight but is unpinned (see patch proposal).
- I did not re-run the C2 battery or the counter's selftest (other seats own those); I re-ran only the C1
  counter to reproduce 10/10.

## Tooling record

No tools installed or upgraded (nothing beyond `python3`, `git`, `sha256sum`, `date`, `cmp`, `grep` was
needed). Pacman untouched. Scratch `/fast/scratch/hyaku/tsukuroi-r84/ReviewEntry/` removed at exit; no
receipts produced outside this wave dir. Refusals: none.
