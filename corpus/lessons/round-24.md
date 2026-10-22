# Round 24 — lesson (tsukuroi, attempt 2, 2026-10-22)

author: TsukuroiR24, the round-24 L1 (planner seat and only integrator). Claim base `f169b3ba9a59abaf3e324c1b591e1e07a4d6003a`; declaration landed at `674891dfbcb853432a863a6eb82e7b2a9bdb3958`.

## Gate

Sources opened this round (all on 2026-10-22, each by the named wave-1 seat, each quote copied from the opened page):

| Row | URL | Located quote (at most 25 words) | Opened by |
|---|---|---|---|
| S087 | https://archlinux.org/news/ | "Arch Linux News Archives"; two rows dated 2026-10-21 (php; ca-certificates-mozilla) | SrcArchNews |
| S088 | https://archlinux.org/news/update-to-ca-certificates-mozilla-31311-1-to-prevent-man-in-the-middle-attacks/ | "The compromised certificates have been removed/invalidated with ca-certificates-mozilla ≥ 3.131.1-1." | SrcArchNews |
| S089 | https://man.archlinux.org/man/pacman.8 | "Only package versions are used to find outdated packages; replacements are not checked here." | SrcPacmanQuery |
| S090 | https://man.archlinux.org/man/pacman.8 | "Use one --clean switch to only remove packages that are no longer installed; use two to remove all files from the cache." | SrcPacmanQuery, SrcPaccache |
| S091 | https://man.archlinux.org/man/paccache.8 | "Specify how many versions of each package are kept in the cache directory, default is 3." | SrcPaccache |
| S092 | https://wiki.archlinux.org/title/System_maintenance?oldid=885170 | "A simple pacman -Syu to a properly synced mirror will fix the problem as long as pacman is not broken." | SrcSystemMaintenance |
| S093 | https://wiki.archlinux.org/title/Downgrading_packages?oldid=887421 | "If a package was installed at an earlier stage, and the pacman cache was not cleaned, install an earlier version from /var/cache/pacman/pkg/." | SrcSystemMaintenance |
| S094 | https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/raw/v42.2/functions | `ln -s "sysroot" "$buildroot/new_root"` (line 1213) | SrcMkinitcpioFunctions |
| S095 | https://gitlab.archlinux.org/archlinux/mkinitcpio/mkinitcpio/-/merge_requests/482 | "To avoid issues (or to at least try to avoid them), /new_root will be kept as a symlink to /sysroot." | SrcMkinitcpioFunctions |
| S096 | https://gitlab.freedesktop.org/plymouth/plymouth/-/raw/26.134.222/src/main.c | "chdir (root_dir); chroot ("."); chdir ("/");" | SrcPlymouthRootFs |
| S097 | https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/26.134.222-3/plymouth.initcpio_hook | "plymouth update-root-fs --new-root-dir=/new_root" | SrcPlymouthPackaging |
| S098 | https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs | `root_mnt="/new_root"` (line 4) | ScoutOverlayHookUpstream |
| S099 | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/dload.c | "/* start from scratch, but only download if our local is out of date. */" | CritMirrorReading |
| S100 | https://raw.githubusercontent.com/omacom/omarchy-mirror/master/README.md | "it serves the Arch snapshot the current Omarchy release was tested against. It changes only when a release ships" | CritMirrorReading, SrcOmarchyMirror |
| S101 | https://stable-mirror.omarchy.org/core/os/x86_64/core.db | "last-modified: Thu, 22 Oct 2026 04:40:03 GMT" (also capture l1-4 line 363) | CritMirrorReading, L1 capture |
| S102 | https://raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-snapshot | "Snapper installed but unconfigured snapshots nothing." | SrcOmarchyUpdate |
| S103 | https://raw.githubusercontent.com/basecamp/omarchy/v3.8.4/install/post-install/pacman.sh | template line "Server = https://stable-mirror.omarchy.org/$repo/os/$arch" | SrcOmarchyMirror |

Registry changes: rows S087-S103 added (17 rows; tier A; kinds docs 9, code 7, dataset 1; status `mined`; used-by the pause-lift gate entry). Rows touched old→new: none. Rows S021, S022 and S058 were re-opened by wave seats (ScoutOverlayHookUpstream, SrcPlymouthPackaging, RevExistingRows) and still hold byte for byte; their cells are unchanged, so no status, recheck or used-by flip is logged. New duplicate-scope warnings (W04) for pacman.8, the btrfs-overlayfs URL and the MR !482 URL are retained as intended narrower scopes.

## Routed defects from the round-23 spot-check

| Spot-check locus | Routed item | Disposition this round |
|---|---|---|
| line 52 | author-written `schema_original_keys` names `replace_all`, not recoverable from retained events | Fixed in output and as criterion: `tools/report-red-causes.py` labels each name absent from the flagged site's retained event as "author recollection, not recoverable from retained events"; QUALITY 54 |
| line 64 | report per-cause observability of the frozen red cohort without widening the grammar, erasing unknown keys or dropping the incomplete seat | C1: per-finding rows with checker-branch subcause, recorded request line and call id; status `CANNOT_EVALUATE`, exit 2, `ConnFxPlanner` and `__unknown_argument__` stay visible; input digests pinned |
| line 64 | if future recording keeps unknown key names, keep values redacted and commit the generator first | Not exercised: this round recorded no new seat traces |
| line 64 | keep early retry, scope and receipt debt visible; native toolset enforcement stays operator-owned | Carried unchanged in the round report; no enforcement claim |
| lines 17, 21 | mode 1 means evaluable, not clean; selftests are capability evidence, not outside reruns | Wording kept in C1 output (`checker_status`, `preserved`) and in SCORECARD |

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix, and how it was shown able to fail |
|---|---|---|---|---|
| R24-STALE-PREMISE | calibration: stale self-assessment | The round-24 declaration (`SCORECARD.md`, section "Round 24 — declaration, attempt 2") said C2 worked "freshness 8 → 8 (tied lowest)" and that "the corpus still records 413 pending upgrades and a pending mkinitcpio 42 upgrade". Freshness was 9 at the base; round-17 notices had already marked both statements historical (wave seats CritClaimSizing, CritLearningFit, ScoutStalePremiseWalk). | none at declaration time; caught by the wave-1 critics | QUALITY 55; the SCORECARD refinement below corrects the axis and before-value without changing either target. The C2 checker pins the capture by sha256 and needs a unique capture pointer per premise; selftest cases `capture-hash-mismatch`, `no-capture-pointer` and `boilerplate-only` fail as designed. |
| R24-REDACTION-OVERWRITE | privacy and evidence labelling | `.ufo/waves/round-24/capture/l1-2/capture.txt` lines 240-697: the second `sed` substitution turned every `PWD=inside-fleet-repo` into `PWD=outside-fleet-repo`, so the inside/outside split was not evidence. | SentinelCapture (wave 1) | `capture.sh` now classifies with one `awk` rule. Synthetic test, run by the L1: a line with PWD inside the fleet repo printed `inside-fleet-repo`, one with `.../Projects/BTVREV` printed `outside-fleet-repo`, the fleet root printed inside, and `.../shokunin-other` printed outside. The old pipeline maps all four to outside, so the test fails on the old rule. QUALITY 56. |
| R24-KEY-RECOLLECTION | evidence provenance | `.ufo/waves/round-23/measure/post-falsify/falsify-limit.json` lists `replace_all`; the retained event at `FxC3Build08:17` keeps `__unknown_argument__` (spot-check line 52). | outside spot-check | QUALITY 54 and the C1 label; selftest case `unknown-key-renamed` fails when the label rule is broken. |
| R24-C1-BY-CONSTRUCTION | claim sizing | The first C1 tool ran from the working tree, so the declared counting command returned 268 of 268 even at `f169b3ba`; the join could not fail; five of nine sandbox mutants still passed (CritC1Construction, CritClaimSizing). | wave-1 critics | The tool now reads itself from the revision (absent at `f169b3ba`: exit 2), pins the four input digests, requires the 266/1/1 split and the incomplete seat by name, and re-runs the frozen checker's classification for every event finding. Selftest case `stub-shifted-sites` fails when sites are shifted. |
| R24-CAPTURE-COUNT | measurement unit | `ls /var/cache/pacman/pkg \| wc -l` printed 4 and the first draft called them "4 files"; all four are empty `download-*` directories (CritPauseEvents, ExecRollbackPaths). | wave-1 critics | `capture.sh` block `cache-package-files` counts `*.pkg.tar*` files (0 at capture time, `l1-4/capture.txt:286`); the P5 falsifier now uses package files. |

## Process notes

- The first dispatch of the 40-seat build wave was refused whole ("Background job limit reached (100)"); nothing spawned (`.ufo/waves/round-24/w1-refusal-1.txt`). Main lowered the seat-gate cap to 85; the unchanged payload was re-acquired through the gate and dispatched once.
- Attempt 1's committed fixtures (`.ufo/waves/round-24/fixtures/`, `fixture-data-D-index.json`, commit `eef0b8e9`) are inherited history; neither claim reads them.
- Installs: none.
