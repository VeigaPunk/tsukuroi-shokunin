# C2CritSR8 evidence receipts (round-44 w2, item C2-K8)

Verification performed 2026-10-26, cwd /fast/scratch/hyaku/tsukuroi-r44/C2CritSR8,
read-only against the lane. Counter sha256 confirmed frozen:
c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059.

## 1. Snapshot digests (all match the counter's SNAP table)

```
ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43  src/sysfs.c   (S243)
f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8  src/scrub.c    (S242)
efb523889035cba62235d904b9e254068a7083dd07e7bb338ce2a803a3e84900  hostcap/capture.txt (S245)
```

Entry file identical between integrated tip and HEAD:
`git diff 8eee79db608b5815c325a5af7cbfdeac50eda9f4 HEAD -- corpus/knowledge/btrfs-scrub-record-r44.md` → empty.

## 2. Quote line verification (manual re-read, pinned files)

| KB quote | file:line | source line (verbatim) |
|---|---|---|
| `#define BTRFS_ATTR_RW(...)` | sysfs.c:72 | `#define BTRFS_ATTR_RW(_prefix, _name, _show, _store)` |
| `__INIT_KOBJ_ATTR(...0644...)` | sysfs.c:74 | `__INIT_KOBJ_ATTR(_name, 0644, _show, _store)` |
| `sysfs_emit` show | sysfs.c:2028 | `return sysfs_emit(buf, "%llu\n", READ_ONCE(device->scrub_speed_max));` |
| `memparse` | sysfs.c:2040 | `limit = memparse(buf, &endptr);` |
| `skip_spaces` | sysfs.c:2042 | `endptr = skip_spaces(endptr);` |
| `-EINVAL` | sysfs.c:2044 | `return -EINVAL;` |
| `BTRFS_ATTR_RW(devid, scrub_speed_max,...` | sysfs.c:2048 | `BTRFS_ATTR_RW(devid, scrub_speed_max, btrfs_devinfo_scrub_speed_max_show,` |
| throttle read | scrub.c:1380 | `bwlimit = READ_ONCE(device->scrub_speed_max);` |
| throttle zero-return | scrub.c:1381 | `if (bwlimit == 0)` |

Store body (adjacent, not itself quoted): `sysfs.c:2043-2046`:
```
if (*endptr != 0)
    return -EINVAL;
WRITE_ONCE(device->scrub_speed_max, limit);
return len;
```
Attribute placement: `sysfs.c:2113` in `devid_attrs[]` (2107-2116); ktype at
2128-2132; `kobject_init_and_add(..., devinfo_kobj, "%llu", device->devid)` at
2165-2166 → path `/sys/fs/btrfs/<fsid>/devinfo/<devid>/scrub_speed_max`.
Throttle: `scrub.c:1367-1401` — comment "bandwidth-limit based, the timeslice is
1 second"; `time_slice = 1000`; `throttle_sent += bio_size` vs `div_u64(bwlimit, div)`.

## 3. Independent greps

`grep -n scrub_speed_max` over pinned S243+S242: only the seven lines listed in
the report — no persistence call on the write path; only WRITE_ONCE writes.
`grep -n -F memparse` at BASE 98020ece over corpus/knowledge + SKILL.md → 0 hits
(novelty gate satisfied; counter run confirms novelty_base_hits=0).

## 4. Inference-basis check (fetched source)

`fs/btrfs/volumes.c` @ v7.2.11 (URL from FETCH.txt; sha256 ff93893dedc4df9baf5d62dd3f5da218db705dcd60947e1ea1a8730d878fe4a9):
line 7470 `dev = kzalloc_obj(*dev);` inside `btrfs_alloc_device` → the inference
basis "`kzalloc_obj` zeroes the device allocation" is true at v7.2.11.
btrfs-progs v7.1 (S237 scrub.c): `read_scrub_device_limit`/`write_scrub_device_limit`
at 1208-1231 use the same sysfs path; limit printed with "/s" (2123-2124);
old limit saved/restored (1413-1414, 1598) — consistent with volatile, bytes/sec.

## 5. Host capture

```
captured 2026-10-26T23:53:22Z uid=1000 CapEff=0000000000000000            (line 1)
scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1/scrub_speed_max mode=644 owner=root value=0  (line 4)
```
capture.sh (sha-pinned) stats the mode/owner and `cat`s the value unprivileged;
glob covers every `/sys/fs/btrfs/*/devinfo/*/scrub_speed_max` — single line ⇒
one device total. Host reading in row is exact.

## 6. Counter read-only run

`python3 tools/check-scrub-record-r44.py --revision 8eee79db... --lane ...` →
SR8 per-row: present, quote_ok (good=9 in_window=9 bad=0 files=S242,S243),
prop_ok, host_ok; global rows=3 quotes_ok=3 props_ok=3 host_ok=3 sources_ok=1
novelty_base_hits=0 pointer_ok=1; verdicts_ok=0 — unbound pending w2 reports
(expected). Transcript binding: first line of this seat's output and report is
`ROW SR8 VERDICT: holds`.

## 7. Counter gate weaknesses noted while attacking

- Quote gate needs only ≥1 good quote + file coverage of `requires`; claims may
  hang on unquoted lines (WRITE_ONCE at 2045, `return len` at 2046 here).
- `in_window >= 1` tolerates quotes outside frozen windows (not exploited here;
  SR8 is 9/9 in-window).
- These match w1 C2RevCounter F1/F2 territory; no row impact.
