# Sibling-overlap scan — the modprobe / kernel-module configuration ground

Seat `C1Connector`, L2, round 72 w1 (the round's only wave). Lane `tsukuroi-shokunin`, declaration commit
`6b4267623b3d6cf88b32c2df8daaad1a5bc9f19e` (lane `HEAD` at scan time). Date 2026-11-03.
Read-only throughout: every sibling byte was read with `git -C <repo> show HEAD:<file>`; no mutating git
verb ran anywhere; nothing was written outside
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-72/{probes,w1}/C1Connector*`.

## 1. Question

Does any sibling lane already claim module loading or modprobe configuration as its ground, and does this
round's Core statement (claim C1: `corpus/knowledge/modprobe-config-plane-r72.md`, rows MD1-MD6) absorb a
sibling surface? If contested, name the arbitration; never absorb.

## 2. Method

1. **Population.** 21 lane repositories under `/home/vgpnk/Projects/shokunin/*-shokunin`, each with a
   `.git` (audio, chousa, game-dev-2d, game-dev-3d, kagi, kaidoku, kake, kama, kasegi, kengaku, kotoba,
   kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi). Non-lane roots
   (`research`, `scripts`, `templates`, `tools`) hold no declaration and were not counted.
2. **Declaration bytes.** For each lane, `PROVINCE.md`, `SKILL.md`, `README.md`, `CORPUS.md` at `HEAD`
   (skipped where absent). Committed bytes, not the working tree, so an uncommitted draft is not evidence.
3. **Terms** (case-insensitive): `modprobe`, `modprobe.d`, `module load`, `blacklist`, `softdep`,
   `kernel module`, `kernel-parameters`, `kmod`, `/sys/module`, `module_param`, `insmod`, `rmmod`,
   `depmod`, `modules-load`.
4. **Second passes.** `corpus/knowledge/**` at `HEAD` for every lane (a lane can hold the plane without
   declaring it), then a whole-repository committed `modprobe` grep to catch staging/registry files.
5. **Third pass.** Fleet-root `merge/tsukuroi/` index (`/home/vgpnk/Projects/shokunin/merge`),
   read-only, ids only, no adoption.
6. **Quote discipline.** Every candidate line was re-read from `git show HEAD` and its quote verified as a
   whitespace-normalised substring of that line (script `build.py`, `QUOTE_FAILS: none`), each quote
   <= 25 words. A located quote proves presence, not agreement (round-66 rule).

### Lane pins at scan time

| lane | HEAD | `PROVINCE.md` sha256 |
|---|---|---|
| tsukuroi | 6b4267623b3d6cf88b32c2df8daaad1a5bc9f19e | 8ca301c8ee2a4bd30bffe65cc05658171a6368023ab9cd372cb181b5dd87689d |
| mori | 84c6cbc3b47c536a504aaee329c77897d389935e | 2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838 |
| kotoba | 1c8f37edf2e5ac0fb3c2be1c88e32406313fe47b | 0d7f862e5187619665ba6fbed2ddf8d09bfd0505ea1ac5093c4a2e49eeb0fa99 |
| kaidoku | fcbe200f6739c38939e0dabf3f251de2cc6bd727 | d5dba65bbeb7dfa53781481afdc2537c7667c78dba4b51f5aef2f07ee55d1e6c |
| revenger | 5915ad8d71c19ad377829d130ba1c35445eb32a4 | c49f6d1d11441728a9a9ed9abed7444837cf2cf0ee569681ad48340187c6f502 |
| mado | 04093b83f73a841117d3b31dbb2a6063f4f2a454 | a1cd50dd4a61e36b32db7b7b21885763d243e9526e35d74440db0cce46c4c185 |
| kama | 090a0b25a71298ed1a58e1f81315d850f4932e74 | 7fa09fab3cb5179519a878d54b204322daab9f01e5c859965cb4bce52f78a592 |

kama committed between two measurements of this scan (`d30a86960814` -> `090a0b25a71298`); its
`PROVINCE.md` blob digest is identical at both (`7fa09fab3cb51795`), so the retained kama quote is stable.

## 3. Census

- **Raw term hits: 45**, in **2 of 21 lanes** — tsukuroi `PROVINCE.md` 13 + `SKILL.md` 31 = 44, kaidoku
  `PROVINCE.md` 1. The other **19 lanes read 0** across all four declaration files.
- Of tsukuroi's 44, most are the r71 module-parameter decision table (SKILL rows S1, S3, S4, S8, S9), the
  r27 kernel-taint rows (KT3/KT4), and one repeated gate row (`owed-statements-r29`) whose hit is the
  unrelated phrase "one private temporary HOME directory created at module load". **14 evidence lines**
  survive as surface-bearing and are tabled below.
- **`corpus/knowledge` pass:** tsukuroi 7 files; siblings 4 files in 3 lanes, all incidental:
  chousa `hardening-r10.md:231` and `sweeps-rejections-r5.md:121` ("placeholder blacklist" in research-
  method prose), kotodama `verification/naming-collision-gate.md:149` ("unsourced blacklist"), revenger
  `round-73-re-resource-atlas.md:139` (the token `blacklist` inside an unrelated resource-table row).
  No sibling knowledge note states the modprobe plane.
- **Whole-repository `modprobe` grep, siblings only:** kaidoku 116 files (28 outside `.ufo/`, all under
  `corpus/evidence/round-*/` RE receipts), mado 7 (all `.ufo/waves/**` reports/receipts), mori 3 (1
  outside `.ufo/`: `corpus/evidence/sources-r31/S173.src`), kengaku 1 and kumitate 1 (both `.ufo/`
  artifacts). No lane-root corpus note, no registry row, no staged file names the surface.
- **Ambiguity recorded:** the term `module load` collides with Python/tool-loading prose. A scanner that
  greps raw terms over manifests will over-count; the declaration gate above is what removes the noise.

## 4. Overlap table

`overlap.tsv` in this directory is the machine form (28 rows: 14 evidence + 14 none, tab-separated, quotes
verbatim and <= 25 words).

| sibling lane | surface it claims | exact line | quote (<= 25 words) | class | owner of the new plane |
|---|---|---|---|---|---|
| tsukuroi | driver/firmware plane incl. kernel modules; r71 parameter plane; r72 config note | `PROVINCE.md:12` | driver/firmware plane (kernel modules, nvidia driver + GSP firmware | owned | tsukuroi |
| tsukuroi | operator-owned: fragment edit, module load/unload, blacklist change | `PROVINCE.md:409` | `modprobe.d` edit, module load and unload, and any blacklist change. The lane reads and records; it never | owned | tsukuroi |
| tsukuroi | fragment contents never read — paths and modes only | `PROVINCE.md:412` | and `/usr/lib/modprobe.d` are not read — only their paths and modes. | owned | tsukuroi |
| tsukuroi | MP6 route row (r71 table the r72 note refines) | `SKILL.md:5921` | ROUTE: the command-line route is attributable by token presence; modprobe is the documented alternative | owned | tsukuroi |
| mori | cedes driver/firmware and boot state | `PROVINCE.md:13` | systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal | adjacent | tsukuroi |
| mori | records tsukuroi as owner of driver/firmware/boot diagnosis | `PROVINCE.md:66` | Owns host OS, package, systemd-unit, driver, firmware, and boot diagnosis. | adjacent | tsukuroi |
| mori | holds the kernel-side autoload doc as source S173, not as a surface | `corpus/evidence/sources-r31/S173.src:604` | The full path to the usermode helper for autoloading kernel modules, by default ``CONFIG_MODPROBE_PATH`` | adjacent | tsukuroi (`kernel.modprobe` is a different layer) |
| kotoba | cedes host package and initramfs hooks; keeps client hook files | `PROVINCE.md:78` | tsukuroi owns host package and initramfs hooks and OS state as read-only probes | adjacent | tsukuroi |
| kaidoku | module load failure as an RE tool-subject observation | `PROVINCE.md:236` | is a tool-subject observation with a signature-module load failure; no | adjacent | tsukuroi (config); kaidoku/revenger unresolved (internals) |
| kaidoku | module identity attribution inside an `analyze_function` probe | `PROVINCE.md:32` | When module identity matters for an `analyze_function` probe, pin request bytes | adjacent | tsukuroi (config); kaidoku/revenger unresolved (internals) |
| revenger | shipped-artifact RE incl. firmware and adjacent binaries | `PROVINCE.md:4` | assemblies, Electron/JavaScript packages, Android APKs, archives, firmware, | adjacent | tsukuroi (config); kaidoku/revenger unresolved (internals) |
| mado | mutation-class observation of `sudo modprobe -r` in a desktop script | `mado-shokunin/.ufo/waves/round-16/w1/reports/SafetyService.md:48` | `sudo modprobe -r intel_quicki2c` — a kernel-driver and input mutation behind a name that is | adjacent | tsukuroi (driver/config); mado keeps the desktop symptom |
| mado | explicit refuse: no initramfs rebuild, no `modprobe` of drivers, no reinstall | `mado-shokunin/.ufo/waves/round-13/w1/SiblingOverlap.md:93` | never attempts to rebuild initramfs, modprobe drivers, or reinstall packages | adjacent | tsukuroi |
| kama | served-model identity and endpoint health only; no driver-config surface | `PROVINCE.md:12` | `GET /v1/models` vs `--alias` vs the configured model id | adjacent | tsukuroi (driver/config); kama (endpoint effect) |

The 14 zero-hit lanes — audio, chousa, game-dev-2d, game-dev-3d, kagi, kake, kasegi, kengaku, kotodama,
kumitate, lore, souji, tabi, tameshi — have no declaration line to quote; each row in `overlap.tsv` is
`-`/`none` with the same 0-hit observation.

## 5. Answer

**Does any lane claim module loading or modprobe configuration as its ground?** No. Two siblings *touch*
the word and neither claims the plane: kaidoku observes a module-load failure as an RE tool subject and
pins module identity for a probe; mado classifies `sudo modprobe -r` as a driver/input *mutation* inside a
desktop script body and elsewhere refuses to modprobe drivers at all. Three siblings cede the ground to
tsukuroi in their own bytes — mori twice (driver/firmware/boot → tsukuroi) and kotoba once (host package
and initramfs hooks → tsukuroi). kama declares endpoints only; ADJ-01 explicitly leaves kernel and driver
state with tsukuroi.

**Does this round's Core statement absorb it?** No. Claim C1 adds six rule rows to a lane-internal note
sourced from upstream kmod v34 (`man/modprobe.d.5.scd`, `libkmod/libkmod-config.c`, `tools/modprobe.c`).
It reads no sibling artifact, quotes no sibling corpus and asserts nothing about another lane's surface.
It extends the r71 area from *parameter visibility* to *configuration-file semantics*, still read-only,
still without reading host fragment contents (`PROVINCE.md:412`). `ABSORBED=0`.

**Contested:** none pairwise. `CONTESTED=0`. Three adjacency seams exist and are named in §6; an overlap
class of `contested` is not assigned to any row.

## 6. Second-order effects and risks

1. **`kernel.modprobe` is not the modprobe.d plane.** mori already holds
   `Documentation/admin-guide/sysctl/kernel.rst` as source S173; its `modprobe` section documents the
   kernel's usermode-helper path for autoloading *(`CONFIG_MODPROBE_PATH`)*. That is a kernel-side sysctl,
   not the userspace config assembly the r72 note describes. A later tsukuroi row that cited it would
   need its own registered snapshot and a source kind the frozen counter accepts — a sibling's registered
   source cannot be reused as this lane's own. **Integrator note, not a contest.**
2. **The kaidoku/revenger seam is internals-only.** r72 reads published kmod source, which is
   documentation grounding, not RE of a shipped artifact. If a later round wants the *installed* kmod
   34.2 binary's behaviour against v34 source, that is ADJ-06, whose recipient is still explicitly
   unresolved (`PROVINCE.md:51`). Doing it silently as "just source reading" would absorb an arbitrated
   scope; the integrator should rule before any such read.
3. **The desktop/driver seam has live host instances.** The three `/etc/modprobe.d` names on this host are
   all hardware-behaviour fragments: `hid_apple.conf` (input), `nvidia.conf` (GPU), and
   `disable-usb-autosuspend.conf` (USB power). Under ADJ-01/ADJ-03 the split is by question: tsukuroi owns
   the fragment's rule semantics and the module's parameter visibility, kama owns the endpoint effect,
   mado owns the observed binding/rendering symptom. No fragment contents are read by this lane
   (`PROVINCE.md:412`), so no packet is raised this round; a future Fn-key or GPU-config symptom trace
   will land exactly on this seam and should cite ADJ-01/ADJ-03 rather than answer locally.
4. **Method hazard for the next scan.** kaidoku's 28 non-`.ufo` `modprobe` files sit under
   `corpus/evidence/`, not `corpus/knowledge/`; a scan that treats evidence trees as claims will produce
   false ownership rows. Declarations plus `corpus/knowledge` are the claim surface; evidence trees are
   receipts of runs.
5. **Cross-document figure, flagged without editing.** The r71 note (`module-parameter-plane-r71.md:43`)
   records "three `/etc/modprobe.d` plus four `/usr/lib/modprobe.d` paths"; the round-72 host capture
   counts **five** `/usr/lib/modprobe.d` names (README + four `.conf`). That is the freshness axis (C3,
   another seat) and not sibling overlap; named here only so the integrator does not read the pair as a
   cross-lane contradiction.

## 7. Limits

- Measurements are of committed sibling bytes at each `HEAD` on 2026-11-03; a lane that commits later is
  not covered, and kama moved once during the scan (PROVINCE blob unchanged; §2).
- A term-regex scan cannot find a claim phrased without these terms. The 0-hit rows are "no hit by this
  method", not "the lane has never written the word".
- No sibling was asked, messaged or woken: a located quote is presence, not acknowledgement, acceptance or
  agreement. The register's round-19/round-66 rule governs.
- mado's two strongest statements are round-13/round-16 wave artifacts, not its declaration; they are
  observations/refusals in a lane-local report, so their authority is that of a report, not of a province.

## 8. Merge index / staged entries

`/home/vgpnk/Projects/shokunin/merge` **does not exist** (`ls -d` rc 2), and the fleet repository's `HEAD`
tree lists no `merge` entry (`git ls-tree -d --name-only HEAD` -> `.devin .omp .scratch .ufo research
scripts templates`; `merge` count 0). No staged entry naming this surface could be read, so no id is
recorded: `STAGED_IDS=none`. The `shokuknow/merge/tsukuroi/` tree was **not** read — assimilation is
closed this round — and nothing was adopted. This is an absence observation about the fleet root, not a
claim that nothing is staged anywhere.

## 9. Receipts

```
git -C /home/vgpnk/Projects/shokunin/<lane> rev-parse HEAD
git -C /home/vgpnk/Projects/shokunin/<lane> show HEAD:PROVINCE.md | sha256sum
git -C /home/vgpnk/Projects/shokunin/<lane> show HEAD:{PROVINCE.md,SKILL.md,README.md,CORPUS.md}
git -C /home/vgpnk/Projects/shokunin/<lane> grep -l -iE 'modprobe|softdep|blacklist|/sys/module|module_param' HEAD -- 'corpus/knowledge'
git -C /home/vgpnk/Projects/shokunin/<lane> grep -l -iE 'modprobe' HEAD
git -C /home/vgpnk/Projects/shokunin ls-tree -d --name-only HEAD
```

Scan/verification script: `/fast/scratch/hyaku/tsukuroi-r72/C1Connector/{scan.py,build.py}` (deleted with
the scratch tree before yield). Term-hit census: 45 raw lines; table rows: 28; quote verification:
`QUOTE_FAILS: none`. **Tools installed or updated: none** (no pacman, `uv tool`, `npx` or binary install;
the scan used host `git` and `python3` as found).

KEY=VALUE: LANES_SCANNED=21 CONTESTED=0 ABSORBED=0 STAGED_IDS=none
