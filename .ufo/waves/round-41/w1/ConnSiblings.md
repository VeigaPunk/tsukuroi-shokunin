# ConnSiblings — Item X-2 sibling-overlap scan (round-41 surfaces)

VERDICT: draft

Scan deliverable (no round-41 claim verified here; read-only lanes, no counter run).
Scope: 20 sibling lanes under `/home/vgpnk/Projects/shokunin/*-shokunin` (tsukuroi excluded), files `PROVINCE.md` (+ `SKILL.md` where present) — 38 files. `audio-shokunin` and `game-dev-2d-shokunin` have no SKILL.md.

## Commands (as executed)

```sh
# 1. enumerate sibling files
for d in /home/vgpnk/Projects/shokunin/*-shokunin; do
  [ "$d" = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin" ] && continue
  for f in PROVINCE.md SKILL.md; do [ -f "$d/$f" ] && printf '%s\n' "$d/$f"; done
done | sort

# 2. broad keyword scan over all 38 files (case-insensitive, gitignore off)
# pattern:
#   \.PKGINFO|\.MTREE|BUILDINFO|package database|Qkk|vercmp|epoch|PKGBUILD|makepkg|mount[ -]?table|selftest|self[ -]test|mutat

# 3. tight ALPM-keyword re-scan (same path list)
# pattern:
#   PKGINFO|MTREE|BUILDINFO|Qkk|vercmp|PKGBUILD|makepkg

# 4. tsukuroi reference scan (same path list)
# pattern: tsukuroi

# 5. mount-related scan (same path list)
# pattern: \bmount(s)?\b|fstab|mnt|subvol
```

## Keyword hit matrix (literal hits per keyword)

| Keyword | Hits in sibling PROVINCE/SKILL |
|---|---|
| `.PKGINFO` | none |
| `.MTREE` | kaidoku PROVINCE.md:50 |
| `BUILDINFO` | none |
| `local package database` | none (closest: kaidoku pacman cache inventory; mori /var/log/pacman.log observation) |
| `pacman -Qkk` | kaidoku PROVINCE.md:50; mado SKILL.md:1637 (dated) and :2019 (supersession) |
| `vercmp` / `epoch` | no `vercmp` anywhere; every `epoch` hit is semantically unrelated (see false positives) |
| `PKGBUILD` | none |
| `makepkg` | none |
| `mount table` | no literal hit; all `mount`/`fstab` hits are bind-mount/namespace/sandbox contexts (see false positives) |
| `selftest` | near-universal, self-referential per lane; the only tsukuroi-targeting hit is tameshi SKILL.md:681 |
| `selftest mutation` | tameshi (tsukuroi-census leg); kengaku reports-out (method); kumitate gate-mutants (own gates) |

## Findings (lane, file:line, quote, contested-scope assessment)

### A. tameshi-shokunin — adjacency on C1 surface (census selftest), method-only, stale pins
- `PROVINCE.md:32-35`: `"tsukuroi \`tools/tsukuroi-census.sh\`, mado \`tools/mado-verify.sh\` (\`tools/mutate-and-run.sh:84-89\`; ... the tsukuroi and mado gates entered through the round-5/6 service runs)"` — tsukuroi-census.sh is a recorded read-only "primary surface" for tameshi's mutation-testing legs.
- `SKILL.md:674-685`: `"Round 5 moves the author axis: the third gate is \`tsukuroi-shokunin/tools/tsukuroi-census.sh\` — a four-plane host-health census (bash, 977 lines, sha256 \`084951be…c78c5\` at measurement) ... summary \`TSUKUROI_CENSUS_SELFTEST: PASS (26 cases, 26 passed, 0 failed)\` ... It diverged: 6/10 killed (60%)"` — the only sibling file naming tsukuroi's census selftest.
- `SKILL.md:687-694` (incident): `"the substrate moved mid-run — a concurrent lane (tsukuroi's own S5-1) hardened the tool at 14:06:23 (+56 lines, 0 deletions, 9 new selftest cases, 26 → 35)"` — both lanes have co-evolved this exact file; measured cells sit on a frozen pre-hardening copy.
- `SKILL.md:1045-1046`, `:1174-1175`, `:1183-1187`: ledger pins for `bash-tsukuroi-census` are recorded stale: `084951be…` → `bba6cdf6…` (HEAD `72b038da`), "stale cell ... no drift at this read".
- Assessment: not contested ownership — tameshi's province claims the reusable mutation *method*; each lane's gate stays its own (kotoba PROVINCE.md:74: "tameshi owns the reusable fixture and mutation method while each lane's gate stays its own"). But the pinned case doc/pins predate round-41's census change (four new mount-table selftest cases); any leg re-run after round-41 would need re-pin/re-measure. Report; do not absorb.

### B. kaidoku-shokunin — contested-scope candidate on C2 surface (.MTREE + `pacman -Qkk`)
- `PROVINCE.md:50` (Core table): `"Archive/package inventory | ... pacman \`.pkg.tar.zst\` cache: 1,556 signed archives (2026-10-13 snapshot); current cache: 1,350 archive files ... \`.MTREE\` per-file sha256; \`pacman -Qkk\` verify"` — same artifact/command pair as C2 PA5 (mtree listing) and PA6 (`pacman -Qkk` → check_pkg_full / "no mtree file").
- Kaidoku credits tsukuroi's update-safety ground (`PROVINCE.md:125`: "Full-system upgrades go through tsukuroi-shokunin's update-safety gate first (that ground is tsukuroi's)") but declares no split with tsukuroi on `.MTREE`/`-Qkk` semantics. Claim shape differs (byte-integrity inventory of signed cache archives for REA analysis vs libalpm load/profile semantics), yet the surface is literal. Flag for integrator; absorb nothing.

### C. mado-shokunin — non-contested (ceded package state); dated `-Qkk` reuse
- `PROVINCE.md:20,24,34`: `"package state stays with tsukuroi"`; `"its unit-state rows sit next to tsukuroi's unit-health ground, which stays tsukuroi's"`.
- `SKILL.md:1636-1639`: `"package \`walker 2.17.0-1\` with \`pacman -Qkk\` 29 files / 0 altered"` — dated round-9 evidence pin; `SKILL.md:2018-2019` supersedes it (2.17.2, `-Qkk` not re-run due to host pacman pause → `[UNK]`). Reuse of the command as evidence, no claim over package semantics.

### D. mori-shokunin — non-contested (ceded OS state); observes pacman log only
- `PROVINCE.md:12-15`: refuses `"OS package, systemd unit, driver/firmware and boot state (→ tsukuroi)"`; reads journal/cgroup events as fleet evidence only.
- `PROVINCE.md:111-117`: observes today's `pacman -Syu`/`-U` in `/var/log/pacman.log` but `"Package and boot-chain interpretation/recovery remain tsukuroi/operator-owned"`. `SKILL.md:143-145,375-376`: same split; actuation for "mounts" is operator-owned.

### E. kagi-shokunin — adjacent explicit split on packages
- `PROVINCE.md:67`: `"kaidoku reads 1Password binaries statically and tsukuroi tracks the 1Password packages — kagi owns runtime auth and credential custody"` — non-contested.

### F. kotoba-shokunin — adjacent explicit split on host hooks/OS state
- `PROVINCE.md:33,52,75`: tsukuroi `none` → `adjacent`; `"tsukuroi owns host package and initramfs hooks and OS state as read-only probes"; kotoba routes only client hook-config files and cedes host hooks` — split stated on kotoba's side alone; non-contested.

### G. kengaku-shokunin — reports out the mutation-testing method
- `PROVINCE.md:282-284`: `"mutation testing of a lane's own gate is a fleet-wide pattern, not kengaku ground — tameshi's \`tools/mutate-and-run.sh\` and kumitate's \`gate-mutants.mjs\` are the precedents"`; `:461-467` (R40 adjacency): method stays tameshi's. Reaches tsukuroi only transitively through tameshi's leg; non-contested.

### H. souji-shokunin — complementary split
- `PROVINCE.md:52-54`: `"tsukuroi-shokunin repairs host operability and never removes packages; souji removes files and never touches the OS"` — non-contested.

### I. False positives recorded (keyword present, meaning unrelated)
- `epoch`: kagi SKILL.md:121 (`session_context_epoch.baseline`, DB column); kumitate SKILL.md:122/231/351 (`park epoch`, `Epoch receipt`); tabi SKILL.md:1466 (`epoch 1792022400`, Unix ts); mado SKILL.md:437 (epoch-varying PIDs); kaidoku PROVINCE.md:58 (retention epoch-scoped). None concern vercmp/version ordering (C2 PA8).
- `mount`/`fstab`: kumitate SKILL.md:622 (bind-oracle mounts `--bind /etc /etc`); chousa SKILL.md:158/731 (bind-mount/nlink refusal and userns PATH-pin in research-gate); souji PROVINCE.md:107, SKILL.md:336 (hostile bind-mount warning); mori SKILL.md:376/380 (operator actuation incl. mounts); mado SKILL.md:677 (harness setup `mount … || exit 125`); kengaku PROVINCE.md:331 (Tier-A bwrap mount-namespace replay). None parse a mount table (C1 surface).
- `selftest`/`self-test`/`mutation`: chousa, kake, kama, kasegi, kotodama, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi all refer to their own gates/instruments; game-dev-3d's "actor mutation" and `'s "engine source mutation" are engine/capability wording. No other lane targets tsukuroi's census or ALPM anatomy.

## Conclusion
For the round-41 surfaces, zero sibling provinces/skills contain `.PKGINFO`, `BUILDINFO`, `PKGBUILD`, `makepkg`, `vercmp`, "local package database", or "mount table". Two real adjacencies found: kaidoku (C2: `.MTREE` + `pacman -Qkk` inventory — contested-scope candidate, no declared split) and tameshi (C1: census selftest mutation leg — method-only, pins stale pre-round-41, non-contested). mado/mori/kagi/kotoba/souji explicitly cede the package/OS ground; kengaku reports the method out.

Not done: no tsukuroi counter or census run (out of seat scope); no lane file modified except this report; no tools installed.
