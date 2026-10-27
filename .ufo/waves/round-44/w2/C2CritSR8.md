ROW SR8 VERDICT: holds

Seat C2CritSR8 — item C2-K8, adversarial falsification of row SR8 in
`corpus/knowledge/btrfs-scrub-record-r44.md` at integrated tip
8eee79db608b5815c325a5af7cbfdeac50eda9f4 (entry identical at HEAD
0f8c07a5035cc9469f59ae41726335388b1cbcac; `git diff 8eee79db HEAD -- <entry>`
is empty). Counter `tools/check-scrub-record-r44.py` sha256
c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059 (frozen).
All snapshot digests re-verified locally: S243 sysfs.c
ce146120…, S242 scrub.c f347931b…, S245 capture.txt efb52388… — match SNAP/CAPTURE.

## Attack plan executed

Adversarial reading of every SR8 sentence against its deciding source line in the
digest-verified snapshots; independent re-grep of all `scrub_speed_max` uses in the
pinned files; fetch of v7.2.11 `fs/btrfs/volumes.c` (the inference basis names
`kzalloc_obj` there); cross-check of the unit claim against btrfs-progs v7.1 (S237);
host-reading claims re-checked against capture.txt and capture.sh semantics.

## Sentence-by-sentence outcome

S1 "Each btrfs device's scrub bandwidth limit is the sysfs attribute
`devinfo/<devid>/scrub_speed_max` under `/sys/fs/btrfs/<fsid>/`" — HOLDS.
`sysfs.c:2113` `BTRFS_ATTR_PTR(devid, scrub_speed_max)` inside `devid_attrs[]`
(2107–2116); `devid_ktype.default_groups = devid_groups` (2130); kobject created
under `devinfo_kobj` at `sysfs.c:2165-2166`. btrfs-progs itself uses the same path
(S237 scrub.c:1214-1215, 1227-1228), confirming this is the limit, not an alias.
"declared with `BTRFS_ATTR_RW`, which builds the attribute with mode 0644" — HOLDS:
`sysfs.c:72-74` `__INIT_KOBJ_ATTR(_name, 0644, _show, _store)`; declared at 2048.
"any user can read it" — HOLDS: 0644 world-read + empirically cat'ed by uid 1000,
CapEff=0 (capture.txt:1,4). "only its owner (root) can write it" — HOLDS as DAC
shorthand; see caveat C2 below (CAP_DAC_OVERRIDE caveat, not a contradiction).

S2 "Reading prints the device's in-memory `scrub_speed_max` as one decimal number
followed by a newline." — HOLDS: `sysfs.c:2028` `sysfs_emit(buf, "%llu\n",
READ_ONCE(device->scrub_speed_max))`.

S3 "Writing parses the text with `memparse`, so a size suffix such as `K`, `M` or
`G` is accepted, skips trailing whitespace including the newline, and rejects
anything else after the number with `-EINVAL`." — HOLDS: `sysfs.c:2040-2044`
`memparse` → `skip_spaces` → `if (*endptr != 0) return -EINVAL;` — exactly "after
the (number+suffix) token, whitespace is skipped and any remaining character
rejects". Suffix is consumed as part of the token, so "10 K" rejects while "10K "
accepts — the sentence's phrasing is precisely right. See caveat C3 (memparse
permissiveness elsewhere does not falsify this clause).

S4 "The scrub throttle reads the value as bytes per second and returns at once
when it is 0, so 0 means no limit." — HOLDS: `scrub.c:1380-1382`
`bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0) return;`
Unit corroborated three ways: comment "bandwidth-limit based, the timeslice is 1
second" (`scrub.c:1367-1369`); `throttle_sent += bio_size` (bytes) compared with
`div_u64(bwlimit, div)` per `time_slice/div` (`scrub.c:1388-1401`); btrfs-progs
prints the attribute with a `/s` suffix (S237 scrub.c:2123-2124).

S5 (the new w1-integrated sentence; least-reviewed surface — main attack target)
"The value is in-memory only: written with `WRITE_ONCE` into `struct
btrfs_device` and read with `READ_ONCE`; nothing on this write path persists it,
so a single-device filesystem loses it on unmount and the device's `kzalloc`
initialisation restores 0 [inference: no persistence site was found in `fs/btrfs`
at v7.2.11; `kzalloc_obj` zeroes the device allocation]." — HOLDS.
- All writes to the field: `WRITE_ONCE` at sysfs.c:2045 only (re-grep: the only
  other `scrub_speed_max` references are READ_ONCE at 2028 and scrub.c:1380 —
  no persistence call on the write path; `struct btrfs_device` is not a
  serialised disk item).
- Inference basis verified: `btrfs_alloc_device` in v7.2.11 `volumes.c:7470` is
  `dev = kzalloc_obj(*dev);` — `kzalloc_obj` zeroes, so a fresh device starts at
  0 = no limit (sha256 of fetched volumes.c ff93893d…; URL per FETCH.txt, tag
  v7.2.11 / a2de78ee).
- Userspace behaviour agrees: btrfs-progs treats the value as volatile — it
  saves `old_limit` before imposing a temporary one and writes it back
  (S237 scrub.c:1413-1414, 1598).
- Corner-case imprecision (recorded, not overreach): "on unmount" means the
  fs's last unmount — a btrfs fs mounted at two places keeps `fs_devices` and
  the `struct btrfs_device` alive until the last umount; likewise `btrfs device
  remove` frees the device (and the value) mid-mount. "single-device" is
  superfluous — every device loses its value when its object dies. The clause
  sits inside the row's own `[inference]` marker, so the reader is already
  warned it is softer than the pinned claims; the mechanism it asserts (no
  persistence) is correct. Proposed tightening below.

## Quotes — all nine verified verbatim

`sysfs.c:72,74,2028,2040,2042,2044,2048`, `scrub.c:1380,1381` — each quoted
string is a substring of the cited line in the digest-verified snapshots
(counter run: SR8 good=9, bad=0, in_window=9/9, files={S242,S243}).

## Host reading — matches capture

capture.txt:4 `scrub_speed_max 1d02a454-…/devinfo/1/scrub_speed_max mode=644
owner=root value=0` — the row's "mode 644, owner root, value 0: no limit" is
verbatim; "read as uid 1000 with no effective capabilities" = capture.txt:1
(uid=1000 CapEff=0, and capture.sh cats the file unprivileged). "The root
filesystem's only device (devid 1)" — capture.sh globs every
`/sys/fs/btrfs/*/devinfo/*/scrub_speed_max`; one line means one device across all
mounted btrfs filesystems, consistent with the claim. No overclaim.

## Counter's own gates (read-only run at 8eee79db)

rows=3, quotes_ok=3, props_ok=3, host_ok=3, novelty_base_hits=0
(`memparse` absent from BASE corpus/knowledge and SKILL.md), sources_ok=1,
pointer_ok=1; only `verdicts_ok`/`transcripts` unbound — expected, those bind
from this wave's results and reports.

Counter gaps observed while attacking (row unaffected): (a) the quote gate
requires ≥1 good quote plus coverage of `requires` files, so a claim may ride on
unquoted lines — here `WRITE_ONCE` at sysfs.c:2045 and `return len` at 2046 are
asserted but not among the row's quotes (all row quotes are still true and
in-window); (b) `in_window ≥ 1` tolerates some quotes outside the frozen windows
(not the case here: 9/9 in-window). Consistent with w1 C2RevCounter findings.

## Caveats recorded (none rise to `partly`/`fails`)

C1 "only its owner (root) can write it": strict DAC reading of 0644 + root
owner; a CAP_DAC_OVERRIDE/CAP_FOWNER process writes regardless — standard
shorthand for every mode-bit claim, not a misstatement.

C2 `memparse` permissiveness: inputs that yield no digits ("", whitespace-only,
"K") are accepted as 0 (i.e. a limit-erasing write, not -EINVAL); base-0 parsing
means "0x…" hex and leading-0 octal parse; >ULLONG_MAX saturates; suffixes T/P/E
also accepted. The row's sentence only claims suffix-acceptance, whitespace-skip,
and trailing-garbage rejection — all true — so this is additive knowledge, not
contradiction.

C3 unmount/multi-mount nuance in the bracketed inference — detailed under S5.

## Proposed text (tightening only; preserves all five props tokens)

**Statement.** … (sentences S1–S4 unchanged) … The value is in-memory only:
written with `WRITE_ONCE` into `struct btrfs_device` and read with `READ_ONCE`;
nothing on this write path persists it, so the limit dies with the device
object — at device removal or the filesystem's last unmount — and the device's
`kzalloc` initialisation restores 0 [inference: no persistence site was found in
`fs/btrfs` at v7.2.11; `kzalloc_obj` zeroes the device allocation].

## Verdict

No sentence contradicts a pinned quote; every deciding claim has its source line;
the inference-marked additions check out in v7.2.11 volumes.c; the host reading
means what capture.txt says. Adversarial falsification found only shorthand-level
imprecision inside an explicit inference marker. `ROW SR8 VERDICT: holds`.

Evidence receipts: `.ufo/waves/round-44/w2/C2CritSR8/evidence.md`.
No git mutations, no sysfs writes, no unit operations; scratch at
/fast/scratch/hyaku/tsukuroi-r44/C2CritSR8 (removed on exit).
