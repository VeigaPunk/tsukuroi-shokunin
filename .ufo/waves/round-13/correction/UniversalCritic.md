# UniversalCritic — counterexamples to "only strict / ReadOnlyPaths=" (round 13, C1 depth)

Seat: critic, axis **depth** (calibration touched). Read-only; no checks/tests run; no installs (curl, man, systemctl already present).
Not admission authority. Pointers are observed unless tagged `[INFERENCE]`.

## Sources reopened by this seat (2026-10-20)
- **M** = local `systemd.exec(5)`, systemd 261.2-1, `/usr/share/man/man5/systemd.exec.5.gz` sha256 `bb09fd20…6b98`, rendered `MANWIDTH=200` (line numbers below are render lines). Same text family as S028.
- **NS** = systemd `v261` `src/core/namespace.c` (raw.githubusercontent, sha256 `731cde78…dcf3f7`). **LF** = `v261` `src/core/load-fragment.c` (sha256 `16d426f1…e88`).
- **NA** = torvalds/linux `master` `fs/namei.c` (sha256 `f578a73e…31fb0`; master at fetch, not a pinned release). Unregistered: candidates for a SOURCES row if the correction cites them.

## Verdict
The round-12 universal is false and the in-progress notice (`root-dac-decision-r12.md:123-137`) correctly narrows it. The
corrected text still has gaps: it does not separate coverage of the **parent** from coverage of the **target**, it does
not list strict's exceptions or the `+` prefix, and the sibling `BindReadonly.md` report swaps the old universal for
untested existence claims rated "confidence 1.0". One fix is blocking: the parent/target error (CX5).

## Counterexamples
| # | Counterexample | Evidence | Status |
|---|---|---|---|
| CX1 | `BindReadOnlyPaths=` creates read-only bind mounts and does not need `ProtectSystem` or `ReadOnlyPaths=`. | M:264; LF:5159,5184 (source and destination are only checked with `PATH_CHECK_ABSOLUTE`, so `/` parses as a destination) | Mechanism documented. That `X:/` mounts cleanly at runtime is `[INFERENCE]`, untested. |
| CX2 | `TemporaryFileSystem=<p>:ro` mounts a read-only tmpfs. | M:975; LF:5092 (absolute-path check only) | Mechanism documented. `/:ro` would hide the unit's own binary; that it is a viable root view is `[INFERENCE]`. |
| CX3 | `RootImage=` plus `RootImageOptions=` (mount(8) options, e.g. `ro`); `RootDirectory=` on a read-only source mount. | M:99-101; M:264 ("unless the source file system mount is already marked read-only") | These change the root view. Read-only only under these conditions, not inherently. QUALITY #17 draft is right on this. |
| CX4 | `DynamicUser=yes` implies `ProtectSystem=strict` without a `ProtectSystem=` line. | M:427-428, M:766. Host: `systemd-journal-gatewayd`/`-upload` unit files contain `DynamicUser=yes` and no `ProtectSystem` line (`systemctl cat … \| grep`), but `systemctl show` prints `ProtectSystem=strict`. | `show`-based captures do include it. The r11 method `systemctl cat \| grep` (`snapper-eacces-mechanism.md:3,10`) **misses** it. |
| CX5 | **"covering the target" is the wrong condition for creating the target.** For an ordinary `mkdir`, EROFS comes from the **parent's** mount, and an existing target returns EEXIST before EROFS. A read-only view mounted *on* `/.snapshots` (BindReadOnlyPaths/TemporaryFileSystem/ReadOnlyPaths) makes the target exist, which gives EEXIST (B4), not EROFS (B2). `ReadOnlyPaths=` on a target that does not exist fails at namespace setup, or is ignored with the `-` prefix. | NA:5072-5096 (`mnt_want_write(path->mnt)` on the parent; the comment says "don't fail immediately if it's r/o, at least try to report other errors"); NA:1822 (positive dentry with `LOOKUP_EXCL` returns EEXIST); M:941-943 (`-` means ignored when missing); M:2619-2621 (exit 226 `EXIT_NAMESPACE`) | **Blocking for depth.** Hits r12 JSON B2 `expected_signal` ("…covering the target, or TemporaryFileSystem= mounting over it"), fixture `mount` field (`.json:240`), and the draft notice wording. For the Btrfs ioctl, order differs (MatrixCriticR K2: `mnt_want_write_file` first) — do not generalize either way. |
| CX6 | `strict` is not total. It excludes `/dev`, `/proc` and `/sys`, plus `ReadWritePaths=`, `StateDirectory=`/`LogsDirectory=` and similar. With `PrivateTmp=`, `/tmp` and `/var/tmp` stay writable. Writable host mounts propagated later stay writable under read-only paths. The man page says "cannot ensure protection in all cases". | M:762, 765-767, 769, 946-950 | Needed so the replacement "strict covers the hierarchy" is not a new universal. |
| CX7 | A command line prefixed with `+` is not subject to file-system namespacing, `strict` included, for that one line. | `systemd.service(5)` Exec prefix table, `+` row (rendered ~684-692) | Host: `ExecStartEx` `flags=` is empty, and the only Exec line is `7:ExecStart=limine-snapper-watcher`. No `+` on the declared line. This closes the r12 B3 "prefixes not inspected" gap for that line only. |
| CX8 | `ReadOnlyPaths=` per-path exceptions: nested `ReadWritePaths=` re-enables writes; the `+` prefix resolves against `RootDirectory=`/`RootImage=`; a read-only superblock wins over `ReadWritePaths=`. | M:926-930, 941-943 | Write "a `ReadOnlyPaths=` entry covering the parent, not re-enabled by a nested `ReadWritePaths=`". |
| CX9 | Not counterexamples, so do not list them as alternatives for `/`: `ExtensionImages=`/`ExtensionDirectories=` make read-only overlays on `/usr`, `/opt` and `/etc` only; `ProtectHome=` covers `/home`, `/root` and `/run/user`. | M:320, 367, 774-780 | Guards against overcorrecting. |

**Why the false "only" was plausible (origin, not excuse).** NS:2506-2519 `root_read_only()` returns true **iff**
`ProtectSystem=strict` or `ReadOnlyPaths=` contains `/`. That is word-for-word the r12 rule. But systemd uses it only to
decide whether to dissect `RootImage=` read-only (NS:2599-2604), and the sibling helper is commented "this is a bit
sloppy" (NS:2531-2533). It is an internal optimisation heuristic, not a statement that no other mechanism makes `/` read-only. This
belongs in the lesson: an implementation shortcut is not a completeness source.

## Host (read-only, uid 1000, 2026-10-20)
`systemctl show limine-snapper-sync.service` (exit 0) returned all of these:
- Empty: `RootDirectory=`, `RootImage=`, `MountImages=`, `ExtensionImages=`, `ExtensionDirectories=`, `ReadOnlyPaths=`, `InaccessiblePaths=`, `BindPaths=`, `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `StateDirectory=`/`Cache…`/`Logs…`/`Runtime…`/`ConfigurationDirectory=` and `DropInPaths=`.
- Set: `DynamicUser=no`, `PrivateTmp=no`, `ProtectSystem=no`, `ProtectHome=yes`, `ReadWritePaths=/tmp`, `FragmentPath=/usr/lib/systemd/system/limine-snapper-sync.service`.

So the configured text shows no read-only view of `/`. This is current configured text only. It says nothing about the unit's
private namespace at failure time, or about another sandbox or LSM. `BindReadonly.md:49` "all read-only path mechanisms remain unset"
is another exhaustive phrase: it checked six properties.

## Smallest safe correction (narrow ProtectSystem-only comparison)
Replace each r12 exclusivity site in the **new active** entry with:
> Among `ProtectSystem=` values, `true` covers `/usr/`, `/boot/` and `/efi/`; `full` adds `/etc/`; neither covers `/`. Only `strict` covers the whole hierarchy, minus `/dev/`, `/proc/`, `/sys/`, `ReadWritePaths=`, StateDirectory-family paths and `PrivateTmp` temporaries, and it is not applied to `+`-prefixed command lines (S028). `ProtectSystem=no` with empty `ReadOnlyPaths=` excludes **those two** mechanisms only. For create-class EROFS, the read-only view has to cover the **parent directory**; a read-only mount on the target itself yields EEXIST for ordinary `mkdir`. Other unit-side read-only views include `BindReadOnlyPaths=`, `TemporaryFileSystem=…:ro` and a read-only `RootDirectory=`/`RootImage=`. This list is not exhaustive.

Sites to cover (some are not in the closure list):
- md:53, md:64, R13 md:86
- md:41-42: add the "among ProtectSystem values" scope
- JSON B2 `interpretation` (last sentence), `limit` and `expected_signal`
- `decision_procedure[1]` (.json:172)
- fixture `mount` (.json:240)

Keep the r12 bytes unchanged under `superseded_by`.

**Adjacent residual, same error class, out of single-claim scope.** `degraded-triage-r4.md:322-323` says "the tree is not
remounted read-only (`ProtectSystem=no`)". The D3 erratum (`:623-627`) covers errno/DAC, not this inference. Route it
to a later round as an append-only erratum. Do not edit it in place.

## Pitfalls for the "fails old / passes new" check
1. A regex that only checks that the old phrase is gone passes on paraphrases ("solely", "the sole", "nothing but", "no other"). Match exclusivity tokens within ~160 characters of `ProtectSystem|ReadOnlyPaths|read-only`, scoped to the **active** B2 strings and md sections. The r12 historical bytes must stay matchable.
2. Pair it with positive assertions on the active entry:
   - the "Among `ProtectSystem=`" scope is present;
   - each of `BindReadOnlyPaths=`, `TemporaryFileSystem=` and `RootImage=` is named;
   - a parent-coverage condition (CX5) is present;
   - the r12 JSON `superseded_by` resolves to an existing file.

   Otherwise, deleting text passes the check.
3. **Integration hazard, observed now:** `root-dac-decision-r12.json:2` has `"superseded_by": "corpus/knowledge/root-dac-correction-r13.json"`, and `root-dac-decision-r12.md:127-128` names `root-dac-correction-r13.md`. Neither file exists yet (a glob for `corpus/**/*r13*` matched nothing). The supersession pointer dangles until CorrectMatrix lands it.
4. The check must not pass because an exclusivity sentence appears inside a quoted "Rejected:" record. Restrict it to active-claim fields, or whitelist quoted historical text explicitly.

## Impacted axes
- **depth:** blocking (CX5), plus completeness fixes (CX6-CX8).
- **calibration:** remove "confidence 1.0" and runtime existence claims in `BindReadonly.md:24-28,48`, or tag them `[INFERENCE]`.
- **adjacency:** unchanged.

None of this pre-admits the correction.
