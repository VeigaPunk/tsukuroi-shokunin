## Round 84 — hibernate-resume plane

| Note | Holds | Sources |
|---|---|---|
| `knowledge/hibernate-resume-plane-r84.md` and `.json` | Ten sourced rows (HR1–HR10) on the chain that decides whether this host returns from hibernation to the image it wrote: `resume_offset=` is the swap header's place inside the `resume=` partition in PAGE_SIZE units and is needed only for swap files; on btrfs that offset is `btrfs inspect-internal map-swapfile -r` (host `3795013`), never `filefrag`, whose first extent physical column reads `3530821` here; the swap file must be NODATACOW (`lsattr` → `---------------C------` on a `compress=zstd:3` mount) and active in `/proc/swaps`; recreating it can move its header, so birth time `1791060333` (2026-10-03 17:45:33 -03) is the recheck trigger; `systemd-hibernate-resume` writes the device's major:minor to `/sys/power/resume` (`253:0` here, `fd 0` for `/dev/mapper/root`); `/sys/power/resume_offset` overrides the command line (`3795013`); mkinitcpio v42.2's `install/resume` adds that binary at systemd ≥ 255 (`systemd 262` here) and the booted UKI initramfs carries it; `/sys/power/image_size` is an upper limit in bytes (`12835467264`) against (31722876 − 11942400) KiB of free swap. Host values are from the pinned capture of 2026-11-06T15:44:21-03:00. Limits: the plane is read-only, no resume was exercised, and HR7 reads the value the kernel holds without showing which writer set it | S336–S341; `lessons/round-84.md` Gate |

This deepens an existing `PROVINCE.md` area rather than opening a new one: the plane sits on the Core
boot-health surface and on the owned "Initramfs v42 and boot recovery" surface, whose boundary already
covers reading effective mkinitcpio hooks and recovery stages. `PROVINCE.md` and the coverage frontier are
unchanged. It is new ground in the corpus, though. At the pre-round tip `64f45b79`,
`git grep -c 'map-swapfile' 64f45b79 -- corpus/knowledge` exits 1 with no output, and the two entries that
had already printed the token (`journal-boot-plane.md:62`, `systemd-user-plane.md:218`) read out
`resume_offset=3795013` without asking whether it points at the swap header and held no rule separating
`map-swapfile` from `filefrag` (HR3: `3530821` against `3795013` on this host). C1 is exploratory, not
measured: it was withdrawn before the wave because the frozen counter's own positive control P1 builds seven
boilerplate rows from random snapshot spans and reads `met`, so `tools/count-resume-rows-r84.py` measures
provenance shape and its 10/10 reading earns nothing (`SCORECARD.md`, "Round 84 — C1 withdrawn as a measured
claim"). The entry verifies only as `unprovable-but-better` on a named non-author reviewer's per-row judgment
(wave seat `ReviewEntry`), otherwise `unprovable`, and claims no ordinal move. The round's measured claim is
the gate `tools/check-hibernate-resume.py`, scored by `tools/resume-gate-battery-r84.py` over 13 families
(POSITIVE, MALFORMED and the eleven finding IDs) on the committed host base plus five unseeded random bases
per run, target 13 of 13, with the four candidate-free controls committed under `before/controls/` reading
gate absent 0/13, blanket HEALTHY 1/13, all-IDs 0/13 and committed-base memoriser 0/13. Its measured outcome
is owned by `SCORECARD.md`, not by this row.

### Frontier (round-84 addition)

- No resume was exercised. The chain's only runtime trace is the kernel's per-boot image lookup, which fails
  on every retained boot: `journalctl -b -g 'Image not found'` prints
  `Nov 02 12:07:17 plazir27 kernel: PM: Image not found (code -22)`, and
  `journalctl --no-pager -g 'hibernation entry|hibernation exit'` prints two boot separators and
  `-- No entries --`; `knowledge/journal-boot-plane.md:64` and `:249-252` hold the same pair. The plane is
  therefore verified against a chain that has never carried an image. <from ScoutHost: independent
  re-capture, and any retained-boot resume evidence beyond the −22 lookup>
- Which writer sets `/sys/power/resume`: the entry reads `253:0` at `before/host/receipt.txt:40` but cannot
  say whether kernel `resume=` parsing or the initramfs `systemd-hibernate-resume` binary wrote it (entry
  Limits and HR7). <from ScoutHost>
- Preconditions the gate does not read, to be named with their evidence before any rule joins the frozen
  eight: <from ScoutHost> — candidate surfaces are the existence and timing of the `resume=` device node
  inside the initramfs, the LUKS unlock ordering beyond the `HOOKS` position rule, and the `[platform]`
  default in `/sys/power/disk` (`before/host/receipt.txt:52`).
- `HR-OFFSET-MISMATCH` is silent when `map_swapfile_offset` is null: the gate's `validate()` accepts null
  and `gate()` guards the comparison on non-null, so a capture that could not run
  `btrfs inspect-internal map-swapfile -r` leaves the offset agreement unchecked without a finding.
- `HR-SWAP-TOO-SMALL` compares free swap with `image_size`, an upper limit on the image; the image's actual
  size is unknown until a hibernation is attempted, so the finding is a bound, not a prediction.
- The round-82 frontier item on swap-unit ordering (`/run/systemd/generator/swap-swapfile.swap`,
  `fstab-generator.c:217`/`:254`) is untouched: this plane reads `/proc/swaps` and the btrfs swap file, not
  the generated unit.
