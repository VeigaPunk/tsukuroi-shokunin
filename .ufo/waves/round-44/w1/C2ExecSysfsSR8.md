VERDICT: defect-found — SR8's four pinned quotes, the `0644` → inode-mode chain, `memparse`'s suffix set, the trailing-whitespace skip and "0 = no limit" are all CONFIRMED at Linux v7.2.11; but two clauses are wrong at their boundaries ("rejects anything else after the number with `-EINVAL`" fails for bytes after an embedded NUL; "only its owner (root) can write it" ignores `CAP_DAC_OVERRIDE`), and the row says nothing about where the value lives — it is in-memory only, zeroed by `kzalloc_obj`, so it survives `mount -o remount` and is lost on an unmount of a single-device filesystem (this host's). Exact window-by-window narrowings in §2-§8 and proposed replacement text in §10, which keeps all five required proposition tokens (`scrub_speed_max`, `0644`, `memparse`, `EINVAL`, `no limit`).

Seat: C2ExecSysfsSR8 (L2, round 44 / hyaku run 9, wave w1). Item C2-5, milestone "SR8 attribute semantics". Kernel under test: Linux **v7.2.11**, tag `v7.2.11`, peeled commit `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`.

---

## 0. What I read, and the receipts

Receipts (all under `w1/C2ExecSysfsSR8/`): `sr8_harness.c`, `sr8-output.txt`, `kernel-lines.txt`, `capability-grep.txt`, `capability-and-mode-receipt.txt`, `persistence-receipt.txt`, `tree-grep.txt`, `host-probe.txt`, `fetch-receipt.txt`, `FETCH-SHA256SUMS.txt`.

- **Kernel tree.** Sparse clone of the tag (same method as the SR7 seat): `git clone --depth 1 --filter=blob:none --sparse --branch v7.2.11 https://github.com/gregkh/linux linux-v7211`, `git sparse-checkout set fs/btrfs include/linux lib fs/kernfs fs/sysfs kernel`; `git rev-parse HEAD` = `a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea`, `git describe --tags` = `v7.2.11`; 131 entries in `fs/btrfs`. `fetch-receipt.txt:3-4`.
- **Frozen copies are byte-identical to that tree**: `fs/btrfs/scrub.c` = `f347931b795c738db08c5706b5caaabce891c9545309a9f8dff5fab9938ca5b8` = `round-44/frozen/src/scrub.c`; `fs/btrfs/sysfs.c` = `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43` = `round-44/frozen/src/sysfs.c`. `tree-grep.txt` (`sha256sum` of both sides on adjacent lines).
- **Extra plain-file fetches** from the same tag (git.kernel.org `?h=v7.2.11`, `linux.git/plain`, accessed 2026-10-26/27; 26 files, sha256 in `FETCH-SHA256SUMS.txt`): `lib/cmdline.c`, `lib/vsprintf.c`, `lib/kstrtox.c`, `lib/ctype.c`, `lib/string_helpers.c`, `lib/kobject.c`, `include/linux/{ctype.h,sysfs.h,kobject.h,kernfs.h,string.h,overflow.h}`, `fs/kernfs/{file.c,dir.c}`, `fs/sysfs/{file.c,group.c}`, `fs/btrfs/{volumes.c,volumes.h,fs.h,super.c,disk-io.c,dev-replace.c}`, `fs/namei.c`, `kernel/capability.c`, `include/uapi/linux/btrfs_tree.h`.
- **Second, independent whole-tree index**: Bootlin Elixir `https://elixir.bootlin.com/linux/v7.2.11/A/ident/scrub_speed_max` (HTTP 200, accessed 2026-10-26) lists exactly six references — `fs/btrfs/scrub.c#L1380`, `fs/btrfs/sysfs.c#L2028`, `#L2045`, `#L2048`, `#L2113`, `fs/btrfs/volumes.h#L216` (`fetch-receipt.txt:14-21`). Agrees with my tree grep.
- **Executable check.** I extracted `memparse`, `simple_strtoull`/`simple_strntoull`, `_parse_integer_fixup_radix`/`_parse_integer_limit`, `skip_spaces`, the `_ctype` table and the store body verbatim into `sr8_harness.c` (source lines cited inline in that file; one substitution — `check_shl_overflow(ret, shl, &ret)` is expanded to the equivalent inline shift-and-compare of `include/linux/overflow.h:192-202`, and `sysfs_kf_write`'s `!count` early return is modelled as a distinct `-999` result so the zero-length row cannot be mistaken for a store verdict) and ran 39 input/expectation pairs: **`total=39 mismatches=0`**, exit 0 (`sr8-output.txt:50`). This is the only "run" besides read-only host probes.
- Line numbers below are v7.2.11 unless a file name says otherwise; frozen-snapshot line numbers (`S242`, `S243`) are identical to the tree by the hashes above.

---

## 1. Does `0644` reach the file? Yes — full chain, host `stat` agrees

| step | evidence |
|---|---|
| `BTRFS_ATTR_RW(devid, scrub_speed_max, …)` | `sysfs.c:2048-2049` |
| expands to `__INIT_KOBJ_ATTR(_name, 0644, _show, _store)` | `sysfs.c:72-74`; btrfs-local macro `sysfs.c:61-66` |
| attribute registered in the devid group | `sysfs.c:2113` inside `devid_attrs[]` (`sysfs.c:2107-2116`), `ATTRIBUTE_GROUPS(devid)` at `sysfs.c:2117` |
| group attached to the per-device kobject | `.default_groups = devid_groups` in `devid_ktype` (`sysfs.c:2128-2132`), used by `kobject_init_and_add(&device->devid_kobj, &devid_ktype, devinfo_kobj, "%llu", …)` (`sysfs.c:2166-2167`) |
| group creation masks the mode | `mode &= SYSFS_PREALLOC \| 0664` (`fs/sysfs/group.c:81`, WARN at 77-79, call at 82-83); `SYSFS_PREALLOC 010000` (`include/linux/sysfs.h:125`) ⇒ `0644 & 0100664 == 0644` |
| inode mode | `__kernfs_create_file(parent, attr->name, mode & 0777, uid, gid, PAGE_SIZE, …)` (`fs/sysfs/file.c:316`) → `kn->mode = mode` (`fs/kernfs/dir.c:688`) |
| host | `-rw-r--r-- 644 root:root 4096 /sys/fs/btrfs/1d02a454-…/devinfo/1/scrub_speed_max` (`host-probe.txt:4`), and it is the **only** writable attribute in that directory — the other six are `-r--r--r--` (`host-probe.txt:5-13`), which is exactly the `BTRFS_ATTR` (0444) vs `BTRFS_ATTR_RW` (0644) split |

Two details the row does not need but a corpus reader might: btrfs' local `__INIT_KOBJ_ATTR` (`sysfs.c:61-66`) does **not** wrap its mode in `VERIFY_OCTAL_PERMISSIONS`, unlike the fs-level `__ATTR` (`include/linux/sysfs.h:240-245`), so the permission is not compile-checked; and the group path strips everything outside `SYSFS_PREALLOC|0664` (`fs/sysfs/group.c:81`), so a mode with execute or setuid bits could not reach the inode even if a driver asked for it. Neither changes 0644. `st_size` 4096 is the kernfs page size passed at `fs/sysfs/file.c:316`, not a content length.

---

## 2. `memparse` suffixes — six, both cases, one character only

`lib/cmdline.c:160-187` switches on the byte after the number: `E/e`, `P/p`, `T/t`, `G/g`, `M/m`, `K/k`, each adding `shl += 10` with `fallthrough` — so every suffix is a power of 1024, upper and lower case are equivalent, and **exactly one suffix byte is consumed** (`endptr++` at `lib/cmdline.c:193`; only reached when a number preceded the suffix, `lib/cmdline.c:189`).

Harness evidence (`sr8-output.txt`): `1K`→1024, `1k`→1024, `1M`/`1m`→1048576, `2G`→2147483648, `3T`→3·2^40, `4P`→4·2^50, `5E`/`5e`→5·2^60; **`1MiB`, `1MB`, `1 M`, `1M x` → `-EINVAL`**, and bare `K` → `-EINVAL` (suffix without a preceding digit). So SR8's "a size suffix such as `K`, `M` or `G`" is true but understates the set and omits the `iB` rejection, which is the case a human is most likely to write.

---

## 3. The unsuffixed number is base-0, and overflow saturates instead of failing

`memparse` calls `simple_strtoull(ptr, &endptr, 0)` (`lib/cmdline.c:156`); `simple_strtoull` → `simple_strntoull` (`lib/vsprintf.c:79-116`) → `_parse_integer_fixup_radix` (`lib/kstrtox.c:26-39`): base 0 means `0x` + hex digit ⇒ **16**, a leading `0` ⇒ **8**, otherwise **10**. `_parse_integer_fixup_radix` does **not** skip whitespace.

Harness: `0x1000` → **4096**, `010` → **8**, `010M` → **8388608** (octal 10 × 1 MiB), and ` 1M` (leading space) → **`-EINVAL`**. Two consequences for the corpus: a leading zero is *not* decimal, so a value written as `0100` means 64 bytes/s; and leading whitespace is rejected even though trailing whitespace is accepted (§4) — the asymmetry is real, not a typo.

Overflow: `_parse_integer_limit` saturates to `ULLONG_MAX` and only ORs an internal overflow bit (`lib/kstrtox.c:83-88`) which `memparse` ignores; suffix overflow saturates via `check_shl_overflow(ret, shl, &ret) → ret = ULLONG_MAX` (`lib/cmdline.c:191-192`, macro at `include/linux/overflow.h:192-202`). Harness: `18446744073709551615` → `ULLONG_MAX` OK; `18446744073709551616` → `ULLONG_MAX` **OK** (not `-EINVAL`). So a too-large write silently becomes "unthrottled" rather than failing.

---

## 4. `skip_spaces` skips the trailing newline — and five more bytes

Store body, verbatim: `limit = memparse(buf, &endptr); endptr = skip_spaces(endptr); if (*endptr != 0) return -EINVAL; WRITE_ONCE(...); return len;` (`sysfs.c:2040-2046`, comment at 2041: "There could be trailing '\n', also catch any typos after the value.").

`skip_spaces` is `while (isspace(*str)) ++str;` (`lib/string_helpers.c:846-851` — note it lives in `lib/string_helpers.c`, not `lib/string.c` in v7.2.11); `isspace` is `(__ismask(c)&(_S)) != 0` (`include/linux/ctype.h:33`) over the `_ctype` table (`lib/ctype.c:11-38`), which marks bytes **9-13** (`\t \n \v \f \r`, `_C|_S`), **32** (space, `_S|_SP`) and **160** (0xA0, `_S|_SP`). Harness: `1M\n\n` and `1M\t\r\v\f\n` both → 1048576 OK; `1M\xa0` → 1048576 OK. NUL is not space (table index 0 is `_C`), which matters in §5.

---

## 5. "Rejects anything else after the number with `-EINVAL`" — true except after an embedded NUL

- Ordinary trailing junk is rejected: harness `1E1`, `1M x`, `1.5G`, `1\n2`, `1\x01`, `+1`, `-1` → all `-EINVAL`. Note `-1` and `+1` are rejected because `simple_strtoull` has no sign handling (`lib/vsprintf.c:112-116` takes the unsigned path; only `simple_strtol` strips `-`, `lib/vsprintf.c:140-146`).
- **Embedded NUL defeats the check.** kernfs copies the user buffer and writes `buf[len] = '\0';` (`fs/kernfs/file.c:330`), and the store inspects only `*endptr`. A write of `"1M\0junk"` therefore parses `1M`, sees NUL, and **succeeds** with 1048576 while returning the full byte count (harness test `{"1M\0junk", 1, 1048576ULL}` at `sr8_harness.c:261`, whose output row prints the input truncated at the NUL as `1M` → `store=OK value=1048576`, `sr8-output.txt:48`; `sysfs.c:2046 return len`). The clause is a universal ("anything else"), so it needs the NUL carve-out.
- **Zero-length write never reaches the store**: `sysfs_kf_write` returns 0 when `!count` (`fs/sysfs/file.c:142-143`), so a 0-byte write is a silent no-op, whereas `echo 0 >` writes `"0\n"` and `echo >` writes `"\n"` which **succeeds and sets 0** (harness `\n` → OK 0; `""` → store not called, marked `-999` in the harness). SR8's "0 means no limit" therefore also covers "a lone newline was written".
- A sysfs write is capped at `PAGE_SIZE` when the file sets no `atomic_write_len` (`fs/kernfs/file.c:311-315`), so a longer buffer is truncated before the parse.

---

## 6. Capability: the store path checks none — the only gate is file permission at open

- `btrfs_devinfo_scrub_speed_max_store` (`sysfs.c:2031-2047`) contains no capability call; `git grep -n "capable(\|ns_capable\|CAP_DAC\|CAP_SYS" -- fs/btrfs/sysfs.c fs/sysfs fs/kernfs lib/kobject.c fs/namei.c` returns **four** hits in `fs/btrfs/sysfs.c`, all in *other* attributes: `btrfs_chunk_size_store` (775, `CAP_SYS_ADMIN`), `btrfs_force_chunk_alloc_store` (864, `CAP_SYS_ADMIN`), `btrfs_commit_stats_store` (1178, `CAP_SYS_RESOURCE`), `quota_override_store` (1224, `CAP_SYS_RESOURCE`) — `capability-grep.txt:3-6`. None in `fs/sysfs`, `fs/kernfs` or `lib/kobject.c`.
- The write chain is `kernfs_fop_write_iter` (`fs/kernfs/file.c:304-361`, no permission test, copies + NUL-terminates + caps length) → `sysfs_kf_write` (`fs/sysfs/file.c:136-146`, only the `!count` short-circuit) → `kobj_attr_store` (`lib/kobject.c:832-842`, `container_of` + call) → the driver store.
- The permission decision is the VFS inode check: `generic_permission` (`fs/namei.c:521-564`), which after `acl_permission_check` allows a denied writer holding **`CAP_DAC_OVERRIDE`** (540, 560; `CAP_DAC_READ_SEARCH` for read-only at 537, 551) via `capable_wrt_inode_uidgid` (`kernel/capability.c:473-480` = `ns_capable(ns, cap) && privileged_wrt_inode_uidgid(...)`).
- So SR8's "only its owner (root) can write it" is accurate operationally (nothing on this host holds `CAP_DAC_OVERRIDE` at uid 1000: `CapEff=0000000000000000`, `host-probe.txt:1`; `test -w` = denied, `test -r` = readable, `host-probe.txt:16-19`) but false as a universal — and, more importantly for the corpus, **there is no `CAP_SYS_ADMIN` gate here**, unlike the fsid-level attributes three functions above it in the same file.

---

## 7. Where `scrub_speed_max` is initialised, and what that means for persistence

**Whole-tree answer (two independent sources agree).** `git grep -n scrub_speed_max` over `fs/btrfs include/linux lib fs/kernfs fs/sysfs kernel` (`tree-grep.txt`) hits only:

| file:line | kind |
|---|---|
| `fs/btrfs/volumes.h:216` | `u64 scrub_speed_max;` — plain in-memory field of `struct btrfs_device` |
| `fs/btrfs/sysfs.c:2028` | read (`sysfs_emit(buf, "%llu\n", READ_ONCE(...))`) |
| `fs/btrfs/sysfs.c:2045` | **the only write in the tree** (`WRITE_ONCE`) |
| `fs/btrfs/sysfs.c:2048-2049`, `2113` | registration |
| `fs/btrfs/scrub.c:1380` (+ comment 1369) | read in the throttle |

Bootlin's identifier index for v7.2.11 lists the same six sites and nothing else. There is **no on-disk representation**: `git grep -n scrub -- include/uapi/linux/btrfs_tree.h` is empty (`persistence-receipt.txt:9-10`), and no mount option or ioctl sets it.

**Initialisation = zero, by allocation.** `btrfs_alloc_device` does `dev = kzalloc_obj(*dev);` (`volumes.c:7470`), so every new device starts at 0; the field is then never assigned again except by the sysfs store. The five allocation sites that create a device struct are `volumes.c:868` (scan finds a device), `volumes.c:1034` (`clone_fs_devices`), `volumes.c:2900` (device add), `volumes.c:7430` (`add_missing_dev`), `dev-replace.c:285` (`btrfs_init_dev_replace_tgtdev`) — `persistence-receipt.txt:12-20`.

**Persistence, stated precisely:**

1. **`mount -o remount` keeps it.** The remount path is `btrfs_reconfigure` (`super.c:1501`) → `btrfs_remount_ro` (1347) / `btrfs_remount_rw` (1300); `git grep` for `btrfs_alloc_device|free_fs_devices|btrfs_close_devices|btrfs_open_devices` in `fs/btrfs/super.c` returns a **single** line, `super.c:1962` (`btrfs_open_devices` in the mount path), and the remount body never allocates or frees a `btrfs_device` (`persistence-receipt.txt:1-6`). Same `btrfs_device` objects ⇒ same value.
2. **Unmount keeps it only if the struct survives.** `close_ctree` calls `btrfs_close_devices` (`disk-io.c:1230`), which closes the bdev and leaves the devices on the list (`close_fs_devices`, `volumes.c:1191-1208`; `btrfs_close_one_device`, `volumes.c:1140-1189`, never touches the field), then frees the whole `fs_devices` — **only when `fs_devices->num_devices == 1`** (`volumes.c:1210-1243`, the `num_devices == 1` test at 1226-1229 → `free_fs_devices`, `volumes.c:418-431`). So:
   - **single-device filesystem** (this host: one `devinfo` entry, `host-probe.txt:23-24`): unmount frees the struct ⇒ the limit is **lost**; the next mount starts at 0.
   - **multi-device filesystem**: the cached `fs_devices` (and its device structs) survives the unmount, so the limit **survives** a remount if the fsid is mounted again before the cache is purged (`btrfs_free_stale_devices`, `volumes.c:531-578`, and `btrfs_cleanup_fs_uuids`, `volumes.c:433-443`, are the purge paths).
3. **Device lifecycle resets it**: device add (`volumes.c:2900`), a missing device that gets a fresh struct (`volumes.c:7430`), realistic replace (the **target** is a new struct, `dev-replace.c:285`, so the replacement device comes up unthrottled), and reboot.
4. Nothing in the tree copies the value from one device struct to another (the whole-tree grep above is exhaustive for writes).

**Answer to the item's question:** the value is initialised nowhere but `kzalloc_obj` (`volumes.c:7470`) and written nowhere but `sysfs.c:2045`; it is persistent across `mount -o remount` and **not** persistent across unmount of a single-device filesystem, device add/replace, or reboot. It is also per-mount in the weak sense that a reader (the C1 census) sees whatever the current mount's struct holds — an unthrottled device after a reboot reads `0`, which is "no limit", not "never configured".

---

## 8. Throttle semantics: 0 = no limit is exact; a nonzero limit is approximate

`scrub_throttle_dev_io` (`scrub.c:1371-1420`): `bwlimit = READ_ONCE(device->scrub_speed_max); if (bwlimit == 0) return;` (`scrub.c:1380-1382` — value in **bytes per second**, per the comment at `scrub.c:1368-1369`); the slice budget is `div = clamp(bwlimit / (16 * 1024 * 1024), 1, 64)` (`scrub.c:1388`, i.e. limits ≤16 MiB/s use one interval) and a bio is admitted while `sctx->throttle_sent <= div_u64(bwlimit, div)` **after** adding `bio_size` (`scrub.c:1400-1402`) — so a single bio larger than the slice budget is still submitted, and the limit is enforced over 1 s epochs (`time_slice = 1000`, `scrub.c:1374`), not as a hard cap. `READ_ONCE` per call also means the value can be changed **mid-scrub** and takes effect on the next submission. SR8's sentence "reads the value as bytes per second and returns at once when it is 0, so 0 means no limit" is exactly right; "the limit" should be qualified as approximate.

---

## 9. Host reading (read-only; no write, no scrub, no sysfs mutation)

`host-probe.txt`: uid 1000, `CapEff=0000000000000000`; `scrub_speed_max` `-rw-r--r-- 644 root:root 4096`; content **`0`** (one decimal, newline — matches `sysfs.c:2028`); `test -r` = readable, `test -w` = denied; one device (`devinfo` = `1`), root filesystem `/dev/mapper/root[/@] rw,…,subvol=/@`; kernel `7.2.11-arch1-1`, `btrfs-progs 7.1-1`. This reproduces `frozen/hostcap/capture.txt:4` independently. (The environment prints `error: openai-chatgpt: missing required signature` on stderr before `pacman -Q` output; noted in `host-probe.txt:32-35`, the package line itself is the authoritative `btrfs-progs 7.1-1`.)

---

## 10. Proposed replacement text for SR8

Constraints from `tools/check-scrub-record-r44.py`: the statement must contain the tokens `scrub_speed_max`, `0644`, `memparse`, `EINVAL`, `no limit` (all kept below); quote lines must match `^\*\*Quote\.\*\* \`(S\d{3,})\` (scrub\.c|ioctl\.c|sysfs\.c|btrfs-scrub@\.timer|btrfs-scrub@\.service|PKGBUILD):(\d+): "(.+)"$`, quote text must occur on that line of the digest-checked snapshot, at least one quote must land in windows `sysfs.c:70-76 / 2019-2050 / 2108-2116` or `scrub.c:1365-1385`, and the row must quote `sysfs.c` **and** kernel `scrub.c`. I therefore cite the non-pinned files (`lib/cmdline.c`, `lib/string_helpers.c`, `include/linux/ctype.h`, `fs/kernfs/file.c`, `fs/namei.c`, `include/linux/overflow.h`, `volumes.c`) **only in the statement narrative**, never as new `**Quote.**` lines.

**Statement (replacement)** — insert as one physical line starting with `**Statement.**` at column 0 (no blockquote
marker: the counter's `statement()` only collects from a line whose `startswith('**Statement.**')` is true, and a
multi-line cell must not begin a continuation line with `**Quote.**` or `**Host reading.**`):

> **Statement.** Each btrfs device's scrub bandwidth limit is the in-memory `u64 scrub_speed_max` of its `struct btrfs_device`, exposed as the sysfs attribute `devinfo/<devid>/scrub_speed_max` under `/sys/fs/btrfs/<fsid>/`, declared with `BTRFS_ATTR_RW`, which builds the attribute with mode 0644 (`sysfs.c:72-74`, registered at `sysfs.c:2048-2049` and `2113`): every user can read it, and a writer needs either ownership (root) or `CAP_DAC_OVERRIDE` — the store itself tests no capability, the gate is the VFS inode check at open (`fs/namei.c:521-564`, v7.2.11, not pinned here), unlike the fsid-level attributes in the same file that do check `CAP_SYS_ADMIN`/`CAP_SYS_RESOURCE`. Reading prints the value as one decimal number and a newline (`sysfs.c:2028`). Writing parses with `memparse` (`sysfs.c:2040`), which accepts exactly the suffixes `K`, `M`, `G`, `T`, `P`, `E` in either case as powers of 1024 and consumes a single suffix character — so `1MiB` and `1MB` are `-EINVAL` — while the unsuffixed number is read base-0, so `0x…` is hex and a leading zero is octal, and an overflowing number or suffix saturates to `ULLONG_MAX` instead of failing (`lib/cmdline.c:156`, `160-194`; v7.2.11, not pinned here). `skip_spaces` then skips trailing whitespace — space, `\t`, `\n`, `\v`, `\f`, `\r` and byte 0xA0 — and anything else before the terminating NUL gives `-EINVAL` (`sysfs.c:2042-2044`); leading whitespace is not skipped, a zero-length write never reaches the store, and a buffer with an embedded NUL is accepted up to that NUL because kernfs NUL-terminates the write buffer. The value exists only in the device struct: `btrfs_alloc_device` zeroes it with `kzalloc_obj` (`volumes.c:7470`) and nothing else in the tree writes it, so it survives `mount -o remount` but is lost on unmount of a single-device filesystem, on device add or replace, and on reboot. The scrub throttle reads the value as bytes per second and returns at once when it is 0, so 0 means no limit; a nonzero limit is applied in at most 64 one-second slices (`scrub.c:1388`) and a bio that overshoots the slice budget in the same call is still sent (`scrub.c:1400-1402`), so the limit is approximate, per device, and can be changed mid-scrub.

**Quotes:** keep all nine existing ones unchanged (all verified on their frozen lines). Optionally add two, both verified verbatim at the cited frozen lines:

> **Quote.** `S243` sysfs.c:2046: "return len;"
>
> **Quote.** `S242` scrub.c:1388: "div = clamp(bwlimit / (16 * 1024 * 1024), 1, 64);"

(`sysfs.c:2046` sits inside the 2019-2050 window; the `scrub.c:1388` quote supports the approximate-limit clause. Neither is required for `quotes_ok` — the existing nine already satisfy it.)

**Host reading:** keep `capture.txt:4` (mode 644, owner root, value 0) and optionally add `capture.txt:1` (uid 1000, `CapEff=0`), which is what makes the "root or `CAP_DAC_OVERRIDE`" clause observable on this host.

**If the row has a hard length budget**, the minimum edits are: (i) replace "only its owner (root) can write it" with "only root or a holder of `CAP_DAC_OVERRIDE` can write it (the store tests no capability)"; (ii) replace "rejects anything else after the number with `-EINVAL`" with "rejects other trailing text with `-EINVAL` up to the first NUL byte"; (iii) add one sentence: "the value is in-memory only, zeroed at device allocation, kept across `mount -o remount` and lost on unmount of a single-device filesystem". The suffix/base-0/overflow and the "state it is in-memory" details then remain the only unstated refinements.

---

## 11. What I did NOT do

- No host mutation: no sysfs write of any kind (not even a failing one — `test -w` uses `access(2)`), no scrub start/cancel/resume/limit, no mount, no unit/timer/service action, no sudo, no `/etc` or `/var/lib` change, no pacman transaction, no package install (gcc 16.2.1 was already present; **zero tools installed or upgraded this seat**).
- No runtime reproduction on the live kernel: the sysfs mode, the value and the permission split are observed, but `memparse` behaviour is established from source + a userspace harness that copies the kernel functions — I did not attempt a real write to prove `-EINVAL` on the live kernel, by design of the host guard. Consequence: the harness proves the parse/verdict logic, not that this booted Arch kernel is built from these exact files; the "Arch patch touches no `fs/` file" claim is carried from round 43 as stated in the entry's Limits.
- No counter run: `tools/check-scrub-record-r44.py` and `tools/score-scrub-arm-r44.py` were not executed (wave 1 produces no counted verdicts; the C2 counter would also need wave-2 seats to bind). I did read the counter's row spec to keep §10 compatible with it.
- No whole-tree content sweep outside the sparse set: the exhaustiveness claim for `scrub_speed_max` rests on the sparse-set `git grep` (which includes all of `fs/btrfs`, `lib`, `fs/kernfs`, `fs/sysfs`, `kernel`, `include/linux`) **plus** the Bootlin whole-tree identifier index.
- I did not inspect `S237`/`btrfs-progs`, `S240`, `S244` or `S245` beyond the host capture line I re-measured: SR8 is a kernel-side attribute.
- Scratch `/fast/scratch/hyaku/tsukuroi-r44/C2ExecSysfsSR8/` (the sparse clone, the fetched plain files, the harness build) was deleted at seat end; every
  fetched file's sha256 is in `FETCH-SHA256SUMS.txt` and every URL in `fetch-receipt.txt:1`, so the evidence re-fetches even though the copies are gone.

## 12. One-line answer

`0644` does reach the inode (btrfs' `BTRFS_ATTR_RW` → group mask → `mode & 0777` → `kn->mode`, host `stat` = 644 root:root); `memparse` accepts `K/M/G/T/P/E` in either case (one byte, power of 1024), a base-0 number, and skips trailing whitespace via `isspace` (space `\t \n \v \f \r` and 0xA0) but not leading whitespace; trailing junk is `-EINVAL` except after an embedded NUL; the store path checks no capability at all (only the VFS permission check, i.e. root or `CAP_DAC_OVERRIDE`); the value is initialised **only** by `kzalloc_obj` in `btrfs_alloc_device` (`volumes.c:7470`) and written **only** at `sysfs.c:2045`, so it is in-memory, survives `mount -o remount`, and is lost on an unmount of a single-device filesystem, on device add/replace, and on reboot — SR8 must narrow the "rejects anything else" and "only its owner" clauses and add the init/persistence sentence (§10).
