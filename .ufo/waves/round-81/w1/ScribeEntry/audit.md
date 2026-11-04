# ScribeEntry audit — corpus/knowledge/mount-unit-fstab-plane-r81.md (C1)

Receipts: `receipts.txt` in this directory (R1–R14, verbatim outputs). Capture line numbers are
`.ufo/waves/round-81/before/host/generator.txt` unless stated; `capture.txt` is named where used.
Verdicts: SUPPORTED / PARTIAL / CONTRADICTED / UNSUPPORTED. "Live-only" = true on this host but the
underlying bytes are in no persisted receipt.

## 1. "What this host does with it" — sentence → line-range table

| # | Sentence (abridged, in entry order) | Verdict | Support (line ranges / receipt) |
|---|---|---|---|
| 1 | `/etc/fstab` carries six local file systems; four are required and two are not | CONTRADICTED | fstab has 7 local rows (R8: lines 6, 9, 12, 15, 18 required; 26, 27 nofail). Generator required set holds 5 units (`local-fs.target.requires` 140–145, R10). Count is 7 with 5 required + 2 nofail, not 6 with 4 + 2. |
| 2 | required: `/` (btrfs), `/home`, `/var/cache/pacman/pkg`, `/var/log` (btrfs subvolumes), `/boot` (vfat) | SUPPORTED (fstab side live-only) | `-.mount` 3–16 (btrfs, `subvol=/@` at 16); `boot.mount` 18–33 (vfat at 32); `home.mount` 49–62; `var-cache-pacman-pkg.mount` 79–92; `var-log.mount` 94–107; `requires` dir 140–145 (R10). fstab rows: R8. |
| 3 | `nofail`: `/tmp` and `/fast` (both xfs on the second NVMe) | SUPPORTED; NVMe part uncited | nofail + xfs: fast 46–47, tmp 76–77. Second-NVMe devices are in `capture.txt` 5 (`dev-nvme1n1p1`, tmp) and 16 (`dev-nvme1n1p2`, fast) — not cited by the entry (R11). |
| 4 | `/tmp` alone also carries `x-systemd.before=local-fs.target` | SUPPORTED (fstab side live-only) | tmp Options 77 carries it; fast Options 47 does not; device.d header 131 records it; fstab 26 vs 27 (R8). |
| 5 | The generator output matches the documentation row for row | PARTIAL — overclaimed | Host instances exist only for MT1 (partly), MT2, MT5, MT6. fstab has no noauto, auto, x-systemd.automount, requires/wants, wanted-by or required-by (R8), and no `.automount` unit appears in the generator listing (R10). MT3, MT4, MT7, MT8 are not exercised on this host. |
| 6 | `local-fs.target.requires` holds the five required mounts; `local-fs.target.wants` holds `fast.mount`, `tmp.mount` (S332 :135–145) | PARTIAL (omission) | requires 140–145 ✓ (all five). wants 136–139 holds `fast.mount`, `systemd-remount-fs.service` (138), `tmp.mount`. The entry omits `systemd-remount-fs.service`. Range 135–145 covers both. |
| 7 | "That is MT2's wanted-not-required split, measured on this boot rather than quoted." | split SUPPORTED (136–145); "on this boot" CONTRADICTED | Split: 136–145. Timing: generator files stat 2026-11-04 17:34:49 (R7); system booted 2026-11-02 12:07:17 (R7). The output is a post-boot regeneration, not this boot's generation. Cause of the 17:34:49 regeneration: UNKNOWN. [INFERENCE] Content is probably unchanged since boot because `/etc/fstab` mtime is 2026-10-20 09:48:47 (R8). |
| 8 | `tmp.mount` is generated with `Before=local-fs.target`; `fast.mount` is not (S332 :35–47 vs :95–107) | claim SUPPORTED; **citation WRONG** | tmp `Before=` at line 70 (tmp block 64–77). fast block 35–47 has no `Before=` ✓. Range 95–107 is `var-log.mount`, not fast or tmp (R10). The tmp block is not cited. |
| 9 | The two fstab lines differ in exactly one option; `/tmp` names `x-systemd.before=`, `/fast` does not, so the ordering difference is MT5's, not a generator quirk | SUPPORTED (generator side); fstab side live-only | Generator: fast Options 47 vs tmp Options 77 differ only by `,x-systemd.before=local-fs.target`. fstab 26 vs 27 differ only by that token (R8). MT5 doc: S331 229–241 (stripped numbering). "Not a generator quirk" is [INFERENCE] supported by the documentation. |
| 10 | `x-systemd.device-timeout=10s` on both xfs entries becomes `JobRunningTimeoutSec=10s` in a `dev-disk-by-…device.d/50-device-timeout.conf` drop-in; option text recorded in its header (S332 :120–134) | SUPPORTED | Drop-ins 121–127 (header 123–124, `JobRunningTimeoutSec=10s` 127) and 128–134 (header 130–131, value 134). fstab 26–27 carry the option (R8). |
| 11 | The generated `Options=` line keeps `nofail` but drops the `x-systemd.*` tokens, which is the consumption MT6 describes | CONTRADICTED for `/tmp` | fast 47: keeps nofail, no `x-systemd` tokens ✓. tmp 77: keeps nofail **and keeps `x-systemd.before=local-fs.target`**. The device-timeout token is dropped in both. |
| 12 | `nofail` bounds waiting and failure, not ordering; a nofail entry naming `x-systemd.before=local-fs.target` "still delays `local-fs.target` by up to the device timeout"; one without it is only wanted and unordered | UNSUPPORTED (delay claim unmeasured and not marked) | Supported: wanted-not-ordered (S331 498–505, stripped 500–503); `x-systemd.before` adds Before= (S331 229–241). Unsupported: the delay itself. Only `JobRunningTimeoutSec=10s` (127, 134) is observed, which is a property, not a measured delay. Limits says no boot test. "Bounds waiting" also conflicts with S331's "boot will continue without waiting". Needs [INFERENCE] marking. |
| 13 | "The boot cost of a missing second NVMe is therefore up to ten seconds for `/tmp` and nothing for `/fast`." | UNSUPPORTED (unmeasured, unmarked) | Same basis as row 12. No device-removal or boot test (Limits). "Nothing for `/fast`" is also unmeasured. |

## 2. Limits section

| Check | Verdict | Evidence |
|---|---|---|
| Names the no-boot-test limit | PRESENT | "No boot test, no device removal test, no `systemctl daemon-reload`, no unit start or stop." |
| Names the upstream-vs-host-build line-number limit | PRESENT, but mis-described | Says the anchors are "v262 upstream lines". They are tag-stripped token numbering (R12; the lane's r79 entry discloses this at `systemd-dependency-propagation-r79.md:25-29`). Against raw upstream lines, MT1's quote sits at 135–138 and MT4's at 491–492, outside the cited windows. |
| "one boot's generator output" | CONTRADICTED | Output written 2026-11-04 17:34:49, not at the 2026-11-02 12:07 boot (R7). |
| Declined: x-initrd.mount, x-systemd.mount-timeout=, x-systemd.graceful-option=, makefs/growfs/pcrfs/validatefs, SloppyOptions=, LazyUnmount=, ForceUnmount=, DirectoryMode= | PRESENT | Named as declined. |
| Declined but NOT named: `x-systemd.wants-mounts-for=`/`requires-mounts-for=` (raw 273–282), `x-systemd.device-bound=` (301), `x-systemd.idle-timeout=` (326), `x-systemd.rw-only` (452), `_netdev` (465), `ReadWriteOnly=` (~630), `TimeoutSec=` (~667), unit-file keys `What=`/`Where=`/`Type=`/`Options=` (558–593) | MISSING | Documented in the same page and not held by the entry. |
| fstab rows the count and decision never mention: swap (`/swap/swapfile`, fstab 22; generated `swap-swapfile.swap` 109–118) and tmpfs `/dev/shm` (fstab 30) | MISSING | The `/dev/shm` row produced no generated unit (R10 grep = 0). The "six local file systems" wording silently excludes both. |
| Host does not exercise MT3, MT4, MT7, MT8 | MISSING | See row 5 above. |

## 3. Provenance trio and recheck

| Field | Verdict | Evidence |
|---|---|---|
| `source:` S331 / S332 | PARTIAL (not committed) | Both S-ids exist only in the uncommitted worktree `corpus/SOURCES.md`; HEAD has 0 (R5). The entry `.md` and `.json` are untracked (R4). |
| `verified-at:` snapshot re-fetched at v262 and digest-checked, SHA `afbf3be6…2394` | SUPPORTED | Upstream fetch today, sha matches snapshot and SHA256SUMS (R6). Capture taken 2026-11-04 17:54 (before/host/generator.txt header). |
| `verified-at:` host systemd "262.1-1-arch" (in recheck) | SUPPORTED | `systemctl --version` → systemd 262 (262.1-1-arch); `pacman -Q` → 262.1-1 (R9, read-only query). |
| `recheck:` command exactly runnable | NOT RUNNABLE at any landed revision today | `--revision <REV>` is undefined in the entry (other lane entries define REV as a landed hex commit per QUALITY 27). At HEAD `e8e5d5b3` and at `8023711` the counter prints `note-absent` and exits 1 (R3). The entry is untracked and S331/S332 are uncommitted (R4, R5). |
| Recheck's expected output `"count": 8, "target": 8, "finding": "met"` rc 0 | MATCHES counter output format | Fixture run prints `{"claim": "C1", "revision": "fixture", "count": 8, "target": 8, "finding": "met", "problems": []}` rc 0 (R2). Selftest 6/6 (R1). |
| Recheck detects change on release of the systemd tag | NOT ACHIEVED by the procedure | The counter reads only the local snapshot and its `SHA256SUMS`, and never re-fetches upstream (`verify()` reads `SNAPDIR` and `SUMS`). A new upstream release would not change the printed result. The procedure as written cannot detect the trigger it names. |

## 4. Defects

Severity: H = a stated fact is wrong or unsupported in a way a reader would act on; M = wrong citation, wrong
attribution, or overclaim; L = omission. "Fix" is a suggestion only; no production file was edited.

- **D1 (H, depth)** Row 1 and the registry row S332 both give the wrong counts. The entry says "six local file systems; four required"; the real figures are 7 local rows with 5 required and 2 nofail. S332 also says "four required mounts land in .requires" (SOURCES.md, R10 shows five). Fix: "seven local file systems (five required, two nofail)" and correct S332.
- **D2 (H, depth)** Row 11 says `Options=` "drops the `x-systemd.*` tokens". `/tmp` keeps `x-systemd.before=local-fs.target` (generator 77). Fix: state that device-timeout is dropped and x-systemd.before is kept on tmp.
- **D3 (H, freshness)** Row 7 and Limits say the output was measured "on this boot" / is "one boot's output". Generator files were written 2026-11-04 17:34:49; boot was 2026-11-02 12:07 (R7). Cause of the regeneration is unknown and must be stated as unknown. Fix: "generator output regenerated 2026-11-04 17:34:49, after the 2026-11-02 boot."
- **D4 (M, depth)** Row 8's citation "S332 :95–107" is `var-log.mount`. The tmp block is 64–77 with the Before= at 70. Fix: cite 64–77 and 35–47.
- **D5 (M, depth)** The MT5 measured leg (S332 99–100) is `var-log.mount`'s default `Before=local-fs.target`, not the x-systemd.before effect. It does not evidence MT5 (R13). The counter's R7 check is substring-only and does not catch this. Fix: cite the tmp block (70 and 77) for MT5. Counter gap noted for its owner, not this seat.
- **D6 (M, depth)** Rows 12–13 state a delay bound ("up to the device timeout", "up to ten seconds") as fact. No test or measurement supports it, and it is not marked [INFERENCE]. "Nofail bounds waiting" also conflicts with S331's "boot continues without waiting". Fix: mark as inference or remove.
- **D7 (M, depth)** Row 5 "matches the documentation row for row" overclaims. MT3, MT4, MT7, MT8 have no host instance (R8, R10). Fix: say which rows the host exercises.
- **D8 (M, depth/provenance)** Every MT anchor uses tag-stripped token numbering (R12), but the entry and the S331 registry row call them "v262 upstream lines", and a reader opening the raw XML at those numbers lands on different text (MT1 raw 135–138, MT4 raw 491–492). The r79 entry discloses this convention; r81 does not. Fix: add the same disclosure as `systemd-dependency-propagation-r79.md:25-29`, or renumber to raw lines.
- **D9 (M, operability)** The fstab side of every host claim is live-only. `/etc/fstab` is not in `before/host/capture.txt` or `generator.txt`, and the entry cites no fstab receipt (R8). Fix: persist `/etc/fstab` lines 6–30 into the capture, or cite them.
- **D10 (M, operability)** Nothing is committed. The entry `.md`/`.json` are untracked, and S331/S332 exist only in the worktree (R4, R5). The recheck therefore fails at every landed revision today (R3). Fix: commit the entry, JSON and registry rows together.
- **D11 (M, freshness)** The recheck's "on-release of the systemd tag" trigger cannot fire the check: the counter never re-fetches upstream (R6, R3 counter source). Fix: add a re-fetch and digest-compare step to the procedure, or make the cadence "on-snapshot-change".
- **D12 (L, depth)** Row 6 omits `systemd-remount-fs.service` from `local-fs.target.wants` (generator 138).
- **D13 (L, depth)** Limits omits: swap row (fstab 22; generator 109–118), tmpfs `/dev/shm` (fstab 30; no unit, R10), and the documented-but-unnamed options listed in §2.
- **D14 (L, depth)** The MT2 measured leg (140–143) shows the requires list, not the nofail/wants side (136–139) that MT2 is about.
- **D15 (L, operability)** `<REV>` is not defined in the entry.

## 5. Not verified / unknown

- The cause of the 2026-11-04 17:34:49 generator regeneration is UNKNOWN. I did not run `daemon-reload`, `systemctl` reload or any unit operation.
- Whether the 17:34:49 output equals what the 2026-11-02 boot generated is [INFERENCE] (fstab mtime 2026-10-20 suggests yes). Not measured.
- Whether `systemd-fsck`/`blockdev` ordering the entry does not discuss affects its delay claims: not examined.
- Knowledge-header gate and registry-coverage gate were not run (entry untracked; they read committed revisions).
- No boot, device-removal or unit test was run (none is in scope).
