status: done
verdict: GROUND_UNHELD=yes

# C1Connector — sibling overlap + held-corpus restatement check (round 73, w1)

**Axes (godspeed):** adjacency, C1, overlap. The move is a report-only
classification: it improves `overlap` (L1 gets a decision per sibling hit) and
`adjacency` (the C1 note's nearest neighbours are named with quotes) and cannot
harm `C1` because it writes no lane file and edits no instrument.

**Question.** Does any sibling lane own the systemd unit-load merge plane, and
does `corpus/knowledge/` already state a merge/precedence/mask *rule* on it (which
would make C1 a restatement)?

## Verdict

`GROUND_UNHELD=yes`

Evidence that decides it (all commands run from
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, read-only):

```
$ git rev-parse HEAD
8eeadcb92ad5362cae155e1903cdf11b52a5ac5d

$ git ls-tree -r --name-only 749371321c00f04d98c29d2c26b57d75a92d7e37 -- corpus/knowledge/ | grep -c unit-load
0

$ python3 tools/count-ul-rows-r73.py --revision 749371321c00f04d98c29d2c26b57d75a92d7e37
UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md
rc=128
$ python3 tools/count-ul-rows-r73.py --revision HEAD
UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md
rc=128

$ grep -rn 'FragmentPath\|SYSTEMD_UNIT_PATH\|DropInPaths' corpus/ SKILL.md PROVINCE.md
(no output, rc 1)
$ grep -rn 'passim' corpus/ SKILL.md
(no output, rc 1)
$ grep -rn 'src/core/unit\.c\|src/shared/install\.c\|man/systemd\.unit\.xml' corpus/knowledge/*.md
(no output, rc 1)

$ grep -c '^| S[0-9]' corpus/SOURCES.md
303            # last row S303 (kmod v34); no S304–S306, no v262 unit.c/install.c/systemd.unit.xml row

$ sha256sum tools/count-ul-rows-r73.py tools/check-r72-routed-r73.py
542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6  tools/count-ul-rows-r73.py
93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e  tools/check-r72-routed-r73.py
```

Both digests equal the frozen declaration values, so the ground is measured with
the declared instruments. The lane's own declaration already asserts the plane
was never held (`SCORECARD.md:5843`, "the systemd unit-load merge plane this lane
never held"); the commands above are the independent check of that assertion,
not a restatement of it.

Note on scope: the lane *does* hold two **other** merge planes —
`corpus/knowledge/pacman-hook-order-r38.md` (ALPM hooks, HO1–HO7, S208–S211) and
`corpus/knowledge/modprobe-config-plane-r72.md` (kmod config, MD1–MD6, S301–S303).
They are the pattern C1 is shaped like, on different substrates and different
sources; they are **not** the systemd unit-load plane. Their existence is the one
adjacency risk for C1 and is stated under "Contradictions and limits" below.

## 1. Sibling scan

Search run over every sibling lane:
`grep -n -i -E 'drop-in|dropin|\bmask|unit load|systemd/system|FragmentPath|UnitFileState|daemon-reload'`
on each `*/PROVINCE.md` and `*/SKILL.md`, then a second sweep of every sibling
`--include='*.md'` tree for `FragmentPath|UnitFileState|drop-in|DropInPaths|/usr/lib/systemd/system|/etc/systemd/system`
(excluding `.ufo/`) plus `System Unit Search Path|unit-paths|masked unit|LoadState=masked`.

| # | sibling | path:line | quoted boundary sentence | decision | REPORTED, NOT ABSORBED |
|---|---|---|---|---|---|
| S1 | mori | `mori-shokunin/PROVINCE.md:13` | "**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package, systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal and cgroup events as fleet evidence and reports them, never owning OS state;" | **none** (explicit refusal → tsukuroi) | nothing to hand off; mori's own table already routes this ground here |
| S2 | mori | `mori-shokunin/PROVINCE.md:66` | "\| tsukuroi \| Owns host OS, package, systemd-unit, driver, firmware, and boot diagnosis." | **none** (names tsukuroi as owner) | — |
| S3 | mado | `mado-shokunin/PROVINCE.md:35` | "its unit-state rows sit next to tsukuroi's unit-health ground, which stays tsukuroi's" | **none** (nearest neighbour; explicitly cedes unit ground) | report the phrase to L1 as the one place a sibling names this ground from *outside*; mado keeps only desktop-side unit-state probes |
| S4 | mado | `mado-shokunin/corpus/knowledge/walker-deep.md:33` | "(`systemctl --user cat`), with drop-in `~/.config/systemd/user/app-walker@autostart.service.d/restart.conf` (`Restart=always`, `RestartSec=2`) plus the generator's `slice-tweak.conf`." | **none** (observes a named drop-in of its own unit; states no merge rule) | — |
| S5 | kama | `kama-shokunin/PROVINCE.md:10` | "kama governs discovering whatever serves these ports and never claims an installed server" | **none** (serving ports, not unit loading) | — |
| S6 | kama | `kama-shokunin/PROVINCE.md:47-48` | "**Write boundary (hard):** kama never writes to `~/.config`, `~/.omp`, or systemd units." | **none** (write refusal only) | — |
| S7 | kumitate | `kumitate-shokunin/SKILL.md:618` | "the child runs in a transient user scope (`MemoryMax`, `MemorySwapMax=0`, `TasksMax`) launched from `{PATH, XDG_RUNTIME_DIR}`, under `env -i` + `bwrap …`" | **none** (consumes `systemd-run --user` as a dispatch sandbox; states no unit-file load rule) | adjacency worth one line in the report: C1's mask/load rules must not be read as governing transient scopes, which never load from the unit-file search path |
| S8 | tameshi | `tameshi-shokunin/PROVINCE.md:14-17` | "**Refuses:** product domains — every lane's gate remains its own; tameshi owns only the reusable craft … Never edits a sibling's gate code" | **none** (method only; the C1 counter stays tsukuroi's gate) | — |
| S9 | kake | `kake-shokunin/corpus/knowledge/keeper-timer-inert.md:33` | "UnitFileState=disabled" | **none** (property read of kake's own probe timer) | — |
| S10 | kagi | `kagi-shokunin/SKILL.md:378` | "Masking is narrower than its help text reads: only **reference-resolved** values …" | **none** (secret-masking vocabulary — lexical false positive for `mask`) | — |
| S11 | chousa, souji, kaidoku, kengaku, tabi, kotoba, kotodama, revenger, audio, lore, kasegi, game-dev-2d/3d | — | only incidental "drop-in replacement" / "masked field" / `systemd-coredump`-path / `systemd --user` PPID prose; no unit-file load, precedence, mask or drop-in rule | **none** | — |

Sibling lanes owning the ground: **0**. Sibling lanes adjacent-but-ceded: mado (S3/S4), kumitate (S7 — runtime consumer, not load-plane owner).

## 2. Held-corpus restatement check (the twelve `drop-in` files)

`grep -rli -E 'drop-in|dropin' corpus/knowledge/` returns exactly **12** files
(the item's brief count matches). For each, the line judged and the decision:

| # | file:line | line judged (quoted) | states a merge/precedence/mask **rule**? |
|---|---|---|---|
| 1 | `boot-writers-r19.md:15` | "drop-in `/usr/lib/systemd/system/snapper-cleanup.service.d/limine-snapper-override.conf` adds `ExecStartPre=-touch /run/limine-snapper-cleanup.lock` … and `ExecStopPost=limine-snapper-sync`" | **no** — names one drop-in and its directives |
| 2 | `boot-writers-r19.json:34` | "after the service stops the drop-in ExecStopPost runs limine-snapper-sync" | **no** — machine-readable twin of #1 |
| 3 | `btrfs-scrub-grounding-r45.md:251-253` | "the unit's effective stop timeout is 5 s: the drop-in `/etc/systemd/system.conf.d/10-faster-shutdown.conf` sets `DefaultTimeoutStopSec=5s` (that this default reaches every system unit without its own `TimeoutStopSec=` is [inference]: `systemd-system.conf(5)` is not pinned here)" | **no** — the nearest analogue in corpus, and it is *deliberately not ruled*: a `system.conf.d` default-reach claim marked `[inference]`, with its man page unpinned. Not the unit-load merge plane (no search path, no drop-in `.d` merge order, no mask, no fragment, no alias) |
| 4 | `degraded-triage-r4.md:358` | "Measured inputs: `MODULES=()` + drop-ins `nvidia.conf` …, `omarchy_hooks.conf` …, `omarchy_resume.conf`" | **no** — mkinitcpio config inputs, other substrate |
| 5 | `initramfs-v42-sysroot-recovery.md:10` | "The `HOOKS` declarations in `/etc/mkinitcpio.conf` and `/etc/mkinitcpio.conf.d/omarchy_hooks.conf` omit `systemd`; the drop-in includes `plymouth`, `encrypt`, and `btrfs-overlayfs`" | **no** — initramfs inventory |
| 6 | `journal-boot-plane.md:434` | "Correction: that base-file citation is not the effective host configuration; mkinitcpio reads the host's configuration drop-ins." | **no** for systemd units — it *is* an effectiveness rule, but for mkinitcpio config (erratum D5), sourced to the Arch wiki; it names no directory order, no mask, no fragment/alias |
| 7 | `kill-event-deep-r8.md:263` | "stop-time behaviour \| `KillMode=mixed` (unit) + `TimeoutStopSec=5s` drop-in" | **no** — observation of one effective property |
| 8 | `kill-oom-boundary-r33.md:17` | "teardown purge \| `KillMode=mixed` + `TimeoutStopSec=5s` drop-in" | **no** — restates #7 for the ADJ-04 packet |
| 9 | `oom-event-plane.md:352` (also `:190`, `:347`) | "`/etc/systemd/system/user@.service.d/faster-shutdown.conf` → `TimeoutStopSec=5s`"; ":190 … no drop-in dir" | **no** — one positive and one negative observation |
| 10 | `systemd-user-plane.md:29`, `:44`, `:73-74` | "**7 unit files + 1 drop-in + 5 enablement symlinks**"; "drop-in hardening a *generated* xdg-autostart unit"; "`systemd-analyze --user unit-paths` lists 17 roots" | **no** — the closest in-corpus approach to the load path, and it is a **count**: 17 user roots, not an order, not a merge, not a mask rule. (`timer-drift-plane.md:49` counts 18 roots with the same command on a later date; the corpus counts roots and never orders them.) |
| 11 | `systemd262-credentials-boot-policy-r66.md:29` | "/systemd, /usr/lib/systemd and /etc/kernel, no unit file or drop-in references the option" | **no** — negative sweep for a kernel-cmdline option |
| 12 | `systemd262-uki-pcr-r65.md:22` | "4 `/etc/mkinitcpio.conf.d/` drop-ins; 12 hooks …" | **no** — initramfs inventory |

Restatement of a **rule**: **0 of 12**. Every file either names a specific
drop-in and its effective directive, or discusses a different drop-in substrate
(mkinitcpio / journald / system.conf.d). None states: search-path precedence,
same-name override, drop-in merge order, `/etc` > `/run` > `/usr/lib`, drop-in
vs unit-file precedence, `daemon-reload` trigger, mask-by-`/dev/null`, or
`Install` alias parsing.

## 3. Adjacent in-lane ground (reported, not absorbed)

These are same-lane merge-plane entries on other substrates. They are the reason
C1 must be written from its own three v262 snapshots rather than templated, and
the reason the C1 note should cite its substrate boundary explicitly.

| lane entry | what it already rules | why it is not C1 | REPORTED, NOT ABSORBED |
|---|---|---|---|
| `corpus/knowledge/pacman-hook-order-r38.md` HO1–HO7 (S208–S211) | hook name order (bytewise, suffix-stripped), last-directory-wins with first-seen file, triggerless file = mask, phase abort, Post-hook failure ignored | ALPM hooks; `hook.c`/`trans.c` sources; no unit file, no drop-in `.d`, no fragment/alias | L1 may cite it as the lane's merge-plane precedent; no edit |
| `corpus/knowledge/modprobe-config-plane-r72.md` MD1–MD6 (S301–S303) | directory precedence with same-name suppression, lexicographic cross-directory order, duplicate `-EEXIST`, kcmdline into the same object, `-n`, blacklist reach | kmod config; `libkmod-config.c` sources; nothing about unit load | same; also the closest *shape* risk for C1 (see §4) |
| `corpus/knowledge/degraded-triage-r4.md:617-621` (D2 erratum) | `HookDir` precedence, same-name override wins | pacman hook directories | same |
| `corpus/knowledge/timer-drift-plane.md:49`, `systemd-user-plane.md:73-74` | counts of user unit-path roots (18, 17) | counts, not order; user scope only | C1's search-path row must not inherit or contradict these counts without saying which scope/command it uses. If a UL row quotes a system-scope path list, the note should disclose the scope difference once |
| `.ufo/waves/round-44/w1/C2ExecUnitsSR9.md:199-202` (wave evidence, **not** corpus) | names `/etc/systemd/system`, `/run/systemd/system`, `/usr/lib/systemd/system` as the "System Unit Search Path" beside `systemctl enable`/`--runtime` enablement channels, cited to `systemd.unit.5` (online man page) | enablement channels, not same-name load precedence; unabsorbed wave evidence, and cited to the man page, not the v262 `systemd.unit.xml` snapshot | report: C1 will be the first *corpus* statement of any search-path content; the note should either absorb or explicitly not-absorb this prior wave reading |

## 4. Contradictions and limits (stated, not smoothed)

1. **Shape similarity is not restatement.** C1 shares the merge-plane *form* with
   HO (hooks) and MD (modprobe). A reviewer can fairly ask that C1 not be a
   name-substituted copy: the UL rows must be located in `systemd.unit.xml` /
   `unit.c` / `install.c` and must carry mechanisms none of HO/MD has (compiled
   load path + `SYSTEMD_UNIT_PATH` replacement, drop-in merge after the unit file
   with `/etc` > `/run` > `/usr/lib`, `daemon-reload` on drop-in path-list change,
   mask via `/dev/null` symlink and `LoadState=masked` with a non-null
   `FragmentPath`, `Install` alias parsing). If a UL row would still read true with
   `hook.c`/`libkmod-config.c` substituted, it is a template row, not this plane.
2. **r45's `[inference]` is not closed by C1's snapshots.** `btrfs-scrub-grounding-r45.md:252`
   leaves "this default reaches every system unit without its own `TimeoutStopSec=`"
   as inference because `systemd-system.conf(5)` is unpinned. C1 pins
   `systemd.unit.xml`, `unit.c`, `install.c` — not `systemd-system.conf.xml` — so UL
   rows must not be presented as closing that inference; a UL row on drop-in
   precedence (drop-ins beat the unit file) is a *different* claim from a
   `system.conf.d` default reaching units that set no such key.
3. **Sibling declarations drift.** Every decision above is pinned to the sibling
   bytes read today at their working trees; only the quotes are frozen here, not
   the siblings' authority. `mori:PROVINCE.md:66` already discloses such drift
   experience ("sibling declarations can drift" is tsukuroi's own phrasing,
   `PROVINCE.md` Frontier).
4. **Lexical bound.** The restatement check is a grep plus line reading. A rule
   paraphrased without `drop-in|dropin|mask|precedence|lexicographic|beats|wins|
   search path|unit file|LoadState|UnitFileState|FragmentPath` could hide; I
   bounded that by searching rule vocabulary as well as the substrate terms, and
   by reading the rule-bearing entries the vocabulary surfaced (HO, MD, D2, D5).
   Files that never use the word "drop-in" but rule on unit loading would still be
   caught by `LoadState|UnitFileState|FragmentPath|unit file`, which returned only
   inventory/property uses.
5. **No write authority exercised.** Nothing in the lane repo, no sibling lane, no
   registry row, no instrument was touched. Both instrument digests re-measured
   equal to the frozen values above.

## 5. Scratch

Scratch root `/fast/scratch/hyaku/tsukuroi-r73/C1Connector` used only as
`TMPDIR` for the counter; removed before this report was yielded (verified
absent by `ls -d` → rc 2). No tool was installed or upgraded this seat.
