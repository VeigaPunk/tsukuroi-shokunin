VERDICT: supports

Item X-2 — sibling-overlap scan (read-only). Judged axis: adjacency.
Scan date 2026-10-26; seat ConnSiblings-2 (L2, tsukuroi lane round 39, w1).

# What was scanned

Every sibling `PROVINCE.md` under `/home/vgpnk/Projects/shokunin/*-shokunin/`
except this lane — 20 files, one per lane, confirmed by
`find /home/vgpnk/Projects/shokunin -maxdepth 3 -name 'PROVINCE.md' -not -path '*/tsukuroi-shokunin/*'`
("20 paths in 20 dirs").

Exact-keyword scan (case-insensitive) for the item's terms
`/proc/self/mounts`, `mountinfo`, `btrfs`, `sysfs`, `scriptlet`, `ALPM`,
`pacman.log`, `hook`:

    grep -rniE '/proc/self/mounts|mountinfo|btrfs|sysfs|scriptlet|ALPM|pacman\.log|hook' \
      /home/vgpnk/Projects/shokunin/*-shokunin/PROVINCE.md | grep -v '/tsukuroi-shokunin/'

→ 9 hits in 4 lanes (kaidoku ×3, kotoba ×4, mado ×1, mori ×1); full output in
receipt `.ufo/waves/round-39/w1/ConnSiblings/raw-hits.txt`.

Broadened scan (to catch surface ownership stated without the exact terms):
`pacman|alpm|libalpm|mount|btrfs|sysfs|scriptlet` → 8 further-or-repeat hits
in kaidoku (4), kengaku (1), mori (2), souji (1); receipt
`.ufo/waves/round-39/w1/ConnSiblings/broad-hits.txt`.

Head pins for cited lanes (read 2026-10-26):
kaidoku `e059ca9391642d5b71b6662cabcbdce0d9308719`,
kotoba `314e4a1a749848fdf3fc61d44c07e356bdaa1c65`,
mado `a35cfdfcdeb3bd42d1a2cd960faf22ceac1bef3f`,
mori `7197160b927f04db294c9553fb48fadcc7a3f4e3`,
kengaku `4d00e6d80e68b7da9af44f391789bf06b333da06`,
souji `9f17a1ef571f3a510a51ac233d7cf50ac0c871fc`.

# Overlap table

| Sibling (HEAD pin) | Keyword hits in their PROVINCE.md | Cross or border? |
|---|---|---|
| audio, chousa, game-dev-2d, game-dev-3d, kagi, kake, kama, kasegi, kotodama, kumitate, lore, revenger, tabi, tameshi (14 lanes) | none | **None.** Domains: SFX, research method, game production, secrets, web, model endpoints, bounty research, prompt-format measurement, worldbuilding, orchestration tooling, fiction, shipped-artifact RE, browser sessions, verification method. No declared surface touches btrfs sysfs, mount tables, ALPM hooks, scriptlets, or pacman transaction order. |
| mori (`7197160b`) | `pacman.log` at PROVINCE.md:111-115 (round-17 "Adjacent tsukuroi handoff, detection only") | **Border, already recorded on their side.** Their Refuses (PROVINCE.md:9-10): "OS package, systemd unit, driver/firmware and boot state (→ tsukuroi) — mori reads journal and cgroup events as fleet evidence and reports them, never owning OS state". Their pacman.log note records transaction evidence and states "Package and boot-chain interpretation/recovery remain tsukuroi/operator-owned." C2's frozen pacman.log statistics are host-log reading inside this lane's Core pacnew plane (PROVINCE.md "Pair pacman-log history"); C1 is refused-to-mori OS state. No cross; no new handoff. |
| kaidoku (`e059ca93`) | `hook` ×3 at :106,:189,:206 — all Frida process hooking ("Frida-style hooking", "attached or hooked", "no … hooking … acquired"); `pacman` at :50 (`.pkg.tar.zst` cache archive inventory), :62 (`pacman` as host fallback reader), :125 (cession), :168 (multi-version pacman pairs exercised) | **Border, already resolved in this lane's favor.** :125: "Full-system upgrades go through tsukuroi-shokunin's update-safety gate first (that ground is tsukuroi's) … pacman stays paused host-wide". C2's corpus doc grounds itself in "the update-safety plane (PROVINCE.md Core)" and reads libalpm *source* at the installed commit plus a frozen host pacman.log — source-level update-safety knowledge, not shipped-artifact reverse engineering, so ADJ-06 (kaidoku/revenger) is not triggered. The Frida "hook" rows are process instrumentation, unrelated to ALPM hooks. No cross. |
| kotoba (`314e4a1a`) | `Hook` files at :24 (round-59 client hook-config map), :25 (round-60 scoped rules), :52 + :75 (round-74 sibling-overlap re-pin) | **Border, already recorded on their side; this lane's side of their split.** PROVINCE.md:75: "tsukuroi owns host package and initramfs hooks and OS state as read-only probes (PROVINCE.md:22); kotoba routes only client hook-config files and cedes host hooks (hook-files-round59.md:20), a split stated on kotoba's side alone." C2's TO1/TO5/TO8 rows document ALPM transaction hooks — host package hooks, i.e. this lane's side of the kotoba split. No cross; no kotoba handoff. |
| mado (`a35cfdfc`) | `hooks/**` at :18 | **None.** Their :18 `hooks/**` are omarchy theme-repo hook bodies, explicitly OUT for mado ("OUT (report, never absorb)"); unrelated to ALPM hooks. |
| kengaku (`4d00e6d8`) | `mount-namespace` at :331 | **Border (topical only).** :331 is kengaku's catalogue row describing *kotodama's* isolation-replay protocol ("Tier A bwrap mount-namespace replay of a filed runner in a disposable clone"). Kengaku owns prompt-format measurement, not sandbox methods. C1's hidden legs run the census under `unshare -rm` with tmpfs over sysfs as per-counter fixture scaffolding in this lane's scratch — not a reusable fleet method, so ADJ-07 (tameshi) is not triggered. No cross. |
| souji (`9f17a1ef`) | `bind mounts` at :107 | **None.** :107 is souji's deletion-safety lesson ("Known namespace checks are not a universal defense against hostile bind mounts, hardlinks or concurrent filesystem replacement"); unrelated to C1's read-only mount guard. |

# Judgment

Round-39 C1 (btrfs-sysfs/mount-table storage guard) and C2 (libalpm
transaction order TO1-TO8) **cross no sibling-owned surface**. Three borders
are topical and already settled in existing records: mori's round-17
pacman.log detection handoff (interpretation stays tsukuroi), kotoba's
round-74 `adjacent` row with explicit cession of host hooks to tsukuroi, and
kaidoku's explicit cession of update-safety ground (PROVINCE.md:125). No
sibling PROVINCE.md declares ownership of `/proc/self/mounts`, mountinfo,
btrfs, sysfs, ALPM scriptlet output, or pacman transaction order — the
C1/C2-specific keywords appear nowhere except mori's `pacman.log` note.

# Proposed handoff text for PROVINCE.md (append-only round-39 register)

    ## Adjacent — round-39 sibling-overlap scan (X-2)

    Append-only; the ADJ-01..ADJ-07 table and prior append-only sections are
    unchanged. On 2026-10-26 seat ConnSiblings-2 scanned all 20 sibling
    PROVINCE.md files for `/proc/self/mounts`, `mountinfo`, `btrfs`, `sysfs`,
    `scriptlet`, `ALPM`, `pacman.log`, `hook` (case-insensitive; broadened to
    `pacman|alpm|mount`): no sibling declares ownership of the round-39
    surfaces — the guarded btrfs-sysfs/mount-table read (round-39 C1) and the
    libalpm transaction-order entry (round-39 C2) cross no sibling surface;
    three topical borders are already recorded: kotoba cedes host hooks to
    this lane (kotoba PROVINCE.md:75 @ 314e4a1a, round-74 pin 8bd001f — C2's
    TO1/TO5/TO8 hook rows are this lane's side of that split); mori's
    round-17 pacman.log note is detection-only with interpretation here (mori
    PROVINCE.md:111-115 @ 7197160b; C2's frozen pacman.log statistics read
    host log history inside the Core pacnew plane); kaidoku cedes
    update-safety ground (kaidoku PROVINCE.md:125 @ e059ca93 — C2 is
    source-level update-safety knowledge, not shipped-artifact RE, so ADJ-06
    is not triggered). C1's `unshare -rm` fixture namespaces are per-counter
    scaffolding, not a reusable method, so ADJ-07 is not triggered. mado
    PROVINCE.md:18 `hooks/**` are omarchy theme hooks and souji
    PROVINCE.md:107 bind-mount mentions are deletion safety; both unrelated.
    Scan receipts: `.ufo/waves/round-39/w1/ConnSiblings/`.

# Notes and limits

- Scope was PROVINCE.md only, per the item; sibling SKILL.md files were not
  scanned. Ownership declarations live in PROVINCE.md, so a keyword miss
  there is strong (not perfect) evidence of no owned-surface overlap.
- Scan was case-insensitive; `hook` matched Frida hooking (kaidoku) and
  omarchy theme hooks (mado) in addition to agent-client hook files (kotoba).
- All work was read-only on lane content; no sibling file was modified. The
  `grep` tool's glob did not expand across the fleet root (gitignore), so the
  scan ran via `grep -rniE` over absolute paths; both receipts are preserved.
- No tools were installed or upgraded; nothing to record under the
  2026-10-19 tooling-authorization rule.
