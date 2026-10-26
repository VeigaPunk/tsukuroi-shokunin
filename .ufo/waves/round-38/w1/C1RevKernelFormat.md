VERDICT: defect-found
Item C1-13 — kernel source behind probe_storage_arm's parse (v7.2 fs/btrfs/sysfs.c, btrfs_devinfo_error_stats_show). The arm's five-key grammar matches the kernel's loaded-stats emission exactly, but the pinned source has a second, S133-documented emission — the single word `invalid` — that the census contract does not mention, the arm relabels as `malformed`, and no selftest fixture covers. Minor: fail-closed, no wrong-HEALTHY path.

## 1. What I opened and how it is pinned

- Tag `v7.2` exists; `git ls-remote https://github.com/torvalds/linux "refs/tags/v7.2" "refs/tags/v7.2^{}"` returned `237a1c39e8dfd3e1c6f1f023eea37a48ec04cc63` (tag) / `8d3ae59288f1e7d58d76558a6ee96d533bc5019f` (peeled commit) (observed 2026-10-26).
- `curl -fsSL` of https://raw.githubusercontent.com/torvalds/linux/v7.2/fs/btrfs/sysfs.c (2026-10-26) → sha256 `ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43`, 2702 lines. Byte-identical to S133's pin (corpus/SOURCES.md:139 "raw bytes sha256 ce146120…"). One transient 404 on first fetch; 200 on retry (`curl -sS -o /dev/null -w "%{http_code}\n"` → `v7.2/fs/btrfs/sysfs.c -> 200`).
- Cross-checks while I was there: fs/btrfs/volumes.c @ v7.2 → sha256 `f3400af8…` (8976 lines), equals S132's pin (SOURCES.md:138); kdave/btrfs-progs v7.1 Documentation/btrfs-device.rst → sha256 `0d4f425a…` (284 lines), equals S128's pin (SOURCES.md:134). All copies retained in `receipts/` (see receipts.txt).

## 2. The exact print format and key names (the requested quote)

Function `btrfs_devinfo_error_stats_show`, fs/btrfs/sysfs.c:2074-2100, attr registered read-only at :2100 (`BTRFS_ATTR(devid, error_stats, …)` — no store op).

- Early exit, sysfs.c:2080-2081 (accessed 2026-10-26): `if (!device->dev_stats_valid) return sysfs_emit(buf, "invalid\n");`
- Format, sysfs.c:2088-2093 (accessed 2026-10-26): `"write_errs %d\n" "read_errs %d\n" "flush_errs %d\n" "corruption_errs %d\n" "generation_errs %d\n"`
- Order is fixed by enum definition order, per the source comment sysfs.c:2083-2086 ("Keep them in sync and in order of definition of btrfs_dev_stat_values") and include/uapi/linux/btrfs.h:735-752 (WRITE, READ, FLUSH, CORRUPTION, GENERATION). Exactly five lines, one space per line, trailing newline, no header/footer.
- ABI doc: `Documentation/ABI/testing/sysfs-fs-btrfs` is NOT present at v7.2 (curl status `v7.2/Documentation/ABI/testing/sysfs-fs-btrfs -> 404`, same 404 at `master/…`; the v7.2 tree page for Documentation/ABI/testing contains no btrfs file — grep for `btrfs` over the fetched listing → No matches found). `Documentation/filesystems/btrfs.rst` @ v7.2 contains no `error` mention (grep → No matches found). So the item's "if present" clause resolves to: absent upstream at v7.2.

## 3. Decision — does the arm's grammar match the source?

Arm grammar under review: five keys, `<key> <int>` per line, nothing else (tools/tsukuroi-census.sh:1863-1864 comment; key list :1851; parse loop :1866-1873; `nk -ne 5` gate :1874-1876).

- For a device with loaded stats: MATCH, exactly. Names identical and in kernel order (write_errs, read_errs, flush_errs, corruption_errs, generation_errs); each line `<key> <decimal int>`; exactly five lines. The arm is order-insensitive (:1867-1871 tracks `seen`, not position) — a harmless superset of the kernel's fixed order. It also enforces "each once, nothing else": unknown key, extra tokens, duplicate, or missing counter → reject (:1867-1869), `nk != 5` → BLOCKED with detail label `malformed` (:1874-1875).
- BUT the source has one more legal emission: `invalid\n` (sysfs.c:2080-2081) whenever `dev_stats_valid` is 0. The arm parses that line as key `invalid` with no value → not in the key list (:1867) → `nk=-1` → BLOCKED, detail `…:malformed` (:1874-1875). Three consequences:
  1. The census header contract (:353-363, esp. :357-359 "must carry exactly the five counters … as non-negative integers, each once" and :360-361 BLOCKED on "unreadable or malformed") does not mention `invalid`, although the contract cites S133 — and S133 itself discloses it (SOURCES.md:139 quote cell: "…or the word invalid when the stats were not loaded"). The contract is therefore inconsistent with its own pinned source row.
  2. The detail label is misleading for diagnosis: a stats-never-loaded device is not malformed; it is uninitialized. A reader of `detail=<fsid8>:<devid>:malformed` cannot distinguish a corrupt file from a not-yet-valid device.
  3. Reachability is transient, which caps severity: `dev_stats_valid` is set to 1 for every device at mount whether the on-disk item is absent (fs/btrfs/volumes.c:8204-8205 zero + valid) or present (:8219-8223), and at device add (:2941); the ioctl path treats not-yet-valid as `-ENODEV` "get dev_stats failed, not yet valid" (volumes.c:8474-8476). So a steady-state mounted filesystem prints the five keys (the lane's own SH1 host capture shows exactly that); `invalid` is a race/transient state. Fail-closed BLOCKED is safe — no false HEALTHY, no false DEGRADED — but the label and the contract omission stand.
- Proposed text (exact, one sentence to append to the census header after tools/tsukuroi-census.sh:359): `# The kernel can also print the single word \`invalid\` when device stats were never loaded (sysfs.c:2080-2081, S133); such a file counts as malformed and BLOCKED, detailed as \`malformed\`.` A matching selftest fixture (one error_stats file containing only `invalid\n`, expecting state=BLOCKED and `detail=…:malformed`) would close the same gap in the tests.

## 4. Can values be negative or non-decimal?

- Non-decimal: never. `%d` emits signed decimal only — no hex, no leading zeros, no padding (sysfs.c:2089-2093). The selftest's `010` case (census :2901, :2903 "010 is ten, not octal") is parser hardening beyond kernel behavior; the kernel never emits leading zeros, so there is no source/arm conflict there.
- Negative: only via signed-int wraparound. The counters are `atomic_t dev_stat_values[BTRFS_DEV_STAT_VALUES_MAX]` (fs/btrfs/volumes.h:201), read by `btrfs_dev_stat_read` → `atomic_read` returning plain `int` (volumes.h:831-835), printed with `%d`. The kernel only increments (`btrfs_dev_stat_inc`, volumes.c:8422-8424) or resets to zero (`btrfs_dev_stat_set(device, i, 0)` at mount-init :8204/:8220 and explicit logged reset :8483-8485); there is no decrement. A negative decimal would therefore require >2^31−1 increments — theoretically expressible in the format, practically unreachable on this host. The arm's `^[0-9]+$` rejects any sign (census :1867-1871) → BLOCKED, which is fail-closed and consistent with the contract's declared "non-negative integers" (:359). (Side note, outside the sysfs surface: the ioctl ABI widens to `__u64 values[…]` at include/uapi/linux/btrfs.h:763 via the signed int at volumes.c:8490 — a wrap would sign-extend there. Not a sysfs-arm concern.)

## 5. Comparison with the lane rows

- S133 (corpus/SOURCES.md:139): CORRECT and current. Pinned sha256 matches my fetch byte-for-byte; cited lines "2074-2100 (btrfs_devinfo_error_stats_show and its BTRFS_ATTR)" match exactly (function at :2074, attr at :2100); its quote cell's "or the word invalid when the stats were not loaded" is verified at sysfs.c:2080-2081. The row is the only lane place that carries the `invalid` fact — the census contract and SH1 do not.
- S128 (corpus/SOURCES.md:134): CORRECT. btrfs-progs v7.1 btrfs-device.rst is byte-identical to the pinned sha256, and SH1's three quotes land on the cited lines: "corruption_errs" at :254, "A block checksum mismatched or a corrupted metadata header was found." at :255, "Since kernel 5.14 the device stats are also available in textual form in" at :260 (raw reads of the fetched file, 2026-10-26). Its "sysfs error_stats mirror" teaching agrees with sysfs.c:2100.
- SH1 (corpus/knowledge/storage-health-r26.md:15): CONSISTENT. The five sysfs names match sysfs.c:2089-2093 exactly; "read by the same kernel function" holds — both paths call `btrfs_dev_stat_read` (sysfs.c:2094-2098; ioctl at volumes.c:8490, quote verified at exactly :8490). The naming nuance (only write/read/flush shortened vs write_io_errs/read_io_errs/flush_io_errs; corruption_errs/generation_errs identical) is already carried by the recorded correction at :128. SH1 does not mention `invalid`; minor, since S133 carries it and the host device prints the five keys.

## 6. Findings summary

- F1 (minor defect): census header contract (tools/tsukuroi-census.sh:353-363) omits the kernel's documented `invalid` emission that its own source row S133 records; the arm relabels it `malformed` (:1875), which is diagnostically wrong and contract-inconsistent. Proposed text in §3. Fail-closed, transient-only (volumes.c:8205/8223/2941) — no verdict-correctness impact.
- F2 (minor test gap): no selftest fixture for `invalid` (nor for a single unknown-key line) among the six storage fixtures (:2889-2891 absent, :2893-2897 zero, :2899-2904 nonzero+010, :2906-2911 missing-counter, :2913-2917 duplicate/extra, :2919-2922 no-devinfo). Same proposed fixture closes it.
- F3 (info, no defect): negatives and non-decimals are unreachable from the kernel format; the arm's stricter grammar is fail-closed and matches the declared contract. Order-insensitivity and the `010` case are harmless supersets/hardening.

## 7. What I did not do

- Did not run tsukuroi-census.sh, its selftest, or the r38 counters (not asked; review of source text and fixtures only). Did not read the live host sysfs (no host reads needed; SH1's capture covers the live format; host must not be touched). Did not verify kernel versions other than v7.2 (item pins v7.2). Did not check btrfs-progs sources beyond Documentation/btrfs-device.rst (S128's cited artifact).

Housekeeping: receipts (fetched files + provenance sha256/commands) in .ufo/waves/round-38/w1/C1RevKernelFormat/; scratch /fast/scratch/hyaku/tsukuroi-r38/C1RevKernelFormat removed after copying. No tools installed (curl/git/sha256sum preexisting); no sudo, no pacman, no host or lane mutation.
