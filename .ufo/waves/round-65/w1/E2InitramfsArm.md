# E2InitramfsArm — C2 initramfs arm in tools/tsukuroi-census.sh (round 65, wave w1)

Seat: E2InitramfsArm (executor, EXEC-AUTHORIZED). Claim served: **C2 coverage+operability**
(capability `initramfs-arm`). Lane repo `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
base HEAD `37c74e27`. No mutating git/jj command was run; the change is a working-tree edit.

## 1. What was built

`probe_initramfs_arm()` (`tools/tsukuroi-census.sh:2101-2178`) plus its wiring, mirroring the
round-35/38/44 arms: one verdict-neutral line, printed after `SCRUB` and before the rollup.

```
INITRAMFS initramfs-plane mkinitcpio-conf=PRESENT|ABSENT|UNREADABLE conf_d=N hooks=N
          newroot_latehooks=N presets=N ukify=PRESENT|ABSENT|SKIP unreadable=N [detail=...]
```

| field | reading | seam (default) |
|---|---|---|
| `mkinitcpio-conf` | `stat` + readability test only, the file is never opened; `UNREADABLE` covers a directory, a dangling symlink or an unreadable mode | `TSUKUROI_MKINITCPIO_CONF` (`/etc/mkinitcpio.conf`) |
| `conf_d` | entries under the drop-in dir, name+stat only; absent -> `0` + `detail=confd:absent` | `TSUKUROI_MKINITCPIO_CONFD` (`/etc/mkinitcpio.conf.d`) |
| `hooks` | entries under the initcpio hooks dir; absent -> `0` + `detail=hooks:absent` | `TSUKUROI_MKINITCPIO_HOOKS` (`/usr/lib/initcpio/hooks`) |
| `newroot_latehooks` | regular, readable hook files whose bytes name the literal `/new_root` (`grep -qF`, a plain text state — no binary/decision analysis, no mkinitcpio run) | same dir |
| `presets` | entries under the preset dir; absent -> `0` + `detail=presets:absent` | `TSUKUROI_MKINITCPIO_PRESETS` (`/etc/mkinitcpio.d`) |
| `ukify` | `command -v` on the seam; `SKIP` when `TSUKUROI_UKIFY_PROBE=skip` asks for no lookup | `TSUKUROI_UKIFY` (`ukify`), `TSUKUROI_UKIFY_PROBE` (`probe`) |
| `unreadable` | existing-but-unreadable encounters: the conf, an unlistable dir (counted once, named `confd:/hooks:/presets:unreadable`), or an entry inside one (`…:entry-unreadable`) | — |

Detail tokens never repeat, appear once each, in field order, bytewise (`LC_ALL=C`). No name is
ever echoed (QUALITY 84). The arm invokes no `mkinitcpio`, `dracut`, `ukify` or `bootctl`; it
writes nothing, needs no privilege and no network.

**Verdict-neutrality** is structural, not asserted: `INITRAMFS_LINE` is assigned, appended with
`detail`, and printed — it is read nowhere else, so it cannot enter `worse`, the rollup term or
the exit map (mirrors STORAGE/SCRUB). The new selftest case proves it on one fixture tree (arm
inputs present vs every seam absent: identical lines apart from `INITRAMFS`, identical exit).

## 2. Selftest coverage (168 -> 177, 9 new counted cases)

7 `check` cases + 2 `ok` cases, chronological after the R50 case, using `selftest_base_dir` +
fixture roots as caller overrides and `TMPDIR` as the base (no `/tmp` hardcode):

1. happy path: conf + 2 drop-ins + 3 hooks (exactly 1 naming `/new_root`) + 1 preset + a
   fixture `ukify` executable via `TSUKUROI_UKIFY` -> `…PRESENT conf_d=2 hooks=3
   newroot_latehooks=1 presets=1 ukify=PRESENT unreadable=0`;
2. everything absent -> `mkinitcpio-conf=ABSENT … ukify=ABSENT unreadable=0
   detail=confd:absent,hooks:absent,presets:absent`;
3. mode-000 conf -> `UNREADABLE`, `unreadable=1`, `detail=conf:unreadable,…`;
4. preset dir absent -> `presets=0 detail=presets:absent`;
5. hooks dir absent -> `hooks=0 detail=hooks:absent`;
6. `TSUKUROI_UKIFY_PROBE=skip` with a resolvable stub -> `ukify=SKIP` (never a guess);
7. unlistable hooks dir -> `hooks=0 unreadable=1 detail=…hooks:unreadable…`;
8. verdict-neutral A/B on one tree (the arm's inputs present vs absent): identical non-INITRAMFS
   lines and identical exit code, exactly one `INITRAMFS` line per run;
9. emitted-line shape: every field, in contract order, exactly once.

House-pattern note: the ukify case uses the path-override mechanism the other arms use
(`TSUKUROI_UKIFY=<fixture executable>`), never a PATH mutation or a PATH-stub.

Harness change (the only pre-existing code touched): the 32-line inline `env` invocation inside
`check()` became `env "${ENV_BASE[@]}" "${EXTRA_ENV[@]}"`, with `base_env()` building the same
30 seams plus the five round-65 ones, so the neutrality case re-runs the byte-identical
invocation. No seam was dropped or reordered; later `EXTRA_ENV` entries still win.

## 3. Measured results (all on the patched file in the lane repo)

| check | command | result |
|---|---|---|
| red-before | `grep -c INITRAMFS tools/tsukuroi-census.sh` at HEAD | `0`, rc1 |
| selftest | `bash tools/tsukuroi-census.sh --selftest` | **PASS (177 cases, 177 passed, 0 failed)**, rc0 |
| selftest, dirty TMPDIR | same with `TMPDIR="…/dirty tmpdir"` | PASS 177/177, rc0 (R47/R48 contract intact) |
| live | `bash tools/tsukuroi-census.sh` | rc1, **exactly one** `INITRAMFS` line |
| live line | — | `INITRAMFS initramfs-plane mkinitcpio-conf=PRESENT conf_d=4 hooks=12 newroot_latehooks=2 presets=0 ukify=ABSENT unreadable=0` |
| existing verdicts | diff vs `.ufo/waves/round-65/before/live-census-baseline-prearm.txt` | `DRIFT`, `STORAGE`, `SCRUB`, `TSUKUROI_CENSUS` byte-identical; rc 1 -> 1 |
| declaration metric | `grep -c INITRAMFS tools/tsukuroi-census.sh` | `22` (>= 1) |
| static | `bash -n`, `shellcheck -S error` | rc0, rc0 |
| patch size | `git diff --stat -- tools/tsukuroi-census.sh` | `+279 −34`; the 34 deletions are the 2 rewritten usage lines and the 32 env lines moved verbatim into `ENV_BASE` |

Live values grounded against the round-65 bootstrap probes: `conf_d=4` (`nvidia.conf`,
`omarchy_hooks.conf`, `omarchy_resume.conf`, `thunderbolt_module.conf`), `hooks=12`
(`probes/r65-hooks.txt`), `newroot_latehooks=2` (`btrfs-overlayfs`, `plymouth`), `ukify=ABSENT`
(`probes/r65-ukify.txt` rc1).

**Live operability reading for the L1 (a reading, not a verdict):** `/etc/mkinitcpio.d` exists
and is **empty**, so `presets=0` — no `*.preset` exists on this host, and a preset-driven
`mkinitcpio -P` (the classic UKI producer path the v262 plane leans on) has nothing to build
here. That is the state the C1 note has to place against the requirement plane.

## 4. Files written (all inside the seat's scope)

- `tools/tsukuroi-census.sh` — patched in place (atomic: scratch copy -> `.tmp` in `tools/` ->
  single `mv -f`), mode 755 preserved, sha256 `fe15cc5d…a39f3f`, 4069 lines.
- `.ufo/waves/round-65/w1-artifacts/E2/patch.diff` — full unified diff (byte-identical to the
  repo working-tree diff, verified with `cmp`).
- `.ufo/waves/round-65/w1-artifacts/E2/diff-summary.txt` — hunk/deletion inventory.
- `.ufo/waves/round-65/w1-artifacts/E2/selftest-post.log`, `selftest-dirtytmp.log`,
  `live-post.log` — raw runs.
- `.ufo/waves/round-65/w1-artifacts/E2/live-line.txt`, `receipt.txt` — the live line, the
  before/after identity table, and every command with its rc.
- `.ufo/waves/round-65/w1/E2InitramfsArm.md` — this report.

Not touched: LOG.md, SCORECARD.md, SKILL.md, corpus/SOURCES.md, corpus/knowledge/, PROVINCE.md,
SHONEN.md, AGENTS.md, `.ufo/state/`, MANIFEST.json, any other seat's files, the fleet repo.

## 5. Defects and risks (nothing routed as a defect against another seat)

1. **Root-run sensitivity of the two unreadable cases.** `mode-000` reads `UNREADABLE` only for
   an unprivileged caller (`[ -r ]` is true for root). The pre-existing `drift-unreadable` case
   has the identical dependency, so this is a known suite property, not a regression; noted so a
   root-run selftest failure is read correctly.
2. **`ukify=SKIP` is a third value** beyond the item's `PRESENT|ABSENT`. The mandated
   `TSUKUROI_UKIFY_PROBE=skip` seam has to print something that is neither a claim of presence
   nor of absence; `SKIP` is documented in the header and pinned by a selftest case. Consumers
   must accept the three-value field.
3. **Counting unit is "entries under", by design**: directories inside the three dirs count, and
   `*.preset` selection is left to mkinitcpio's own rule. Documented in the header rather than
   silently narrowed; a future arm can tighten it if the register asks.
4. **The output is additive.** The line is verdict-neutral, but a consumer that diffs the whole
   census output against a *frozen text* of a fixed revision will see one extra line (this is the
   declared C2 form, and why the LINE is printed after SCRUB). Scorers that build their own base
   census at runtime are unaffected.
5. **Inter-run `PLANE drivers` drift** (`C4_sweep` 222→220, `C5_swap_fail` …436→…470, PSI
   0.54→0.71) is host measurement the receipt warns about; that plane is not read by this arm.

## 6. Scratch

All scratch lived under `/fast/scratch/hyaku/tsukuroi-r65/E2InitramfsArm/` (shared clone, selftest
`TMPDIR`, dirty-TMPDIR base). Every receipt needed was copied into the wave dir first, then the
whole scratch tree was removed — confirmation in the message to the L1 and in the final report
(`ls` of the parent path returns nothing).
