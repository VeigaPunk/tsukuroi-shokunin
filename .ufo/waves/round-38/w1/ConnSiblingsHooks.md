VERDICT: supports

# Item X-2 — Sibling-overlap scan for C2 (pacman hook semantics / omarchy walker hook)

Seat: ConnSiblingsHooks (L2 connector, tsukuroi lane round 38). Judged axes: adjacency, C2.
Scope of scan, per the item: sibling lanes' `PROVINCE.md` and `SKILL.md` only, read-only.

## Method

Scanned all 20 sibling lanes (`/home/vgpnk/Projects/shokunin/*-shokunin/` minus tsukuroi-shokunin):
38 files (20 `PROVINCE.md`; 18 `SKILL.md` — `audio-shokunin` and `game-dev-2d-shokunin`
have no `SKILL.md`). Two greps: (1) narrow — `alpm|pacman[ -]hook|HookDir|libalpm|mkinitcpio|limine`
(case-insensitive); (2) boundary — `walker-restart|hook[ -]order|alpm-hooks|HO[1-7]|\.hook`.
Full command + output: `.ufo/waves/round-38/w1/ConnSiblingsHooks/sibling-scan.txt`.

## Findings

### 1. Narrow scan: exactly one hit in 38 sibling files — and it is not hook semantics

- `mado-shokunin/SKILL.md:1941` — a round-19 version erratum quoting
  `/var/log/pacman.log:2929`: `[ALPM] upgraded walker (2.17.0-1 -> 2.17.2-1)`. mado uses
  pacman.log as a *version oracle* for its walker pin; it asserts nothing about ALPM hook
  semantics, order, or ownership. (sibling-scan.txt scan 1)

### 2. No sibling names the omarchy walker hook or ALPM hook-order

- Scan 2 (`walker-restart`, `hook order`, `alpm-hooks`, `HO1`–`HO7`, `.hook`) across the same
  38 files: **zero hits** (sibling-scan.txt scan 2). No sibling `PROVINCE.md`/`SKILL.md`
  mentions `walker-restart.hook` at all.

### 3. Ownership as declared by the siblings themselves

- **kotoba-shokunin** routes *client/agent-tooling* hook-config files only and explicitly
  cedes host hooks to tsukuroi:
  - `kotoba-shokunin/SKILL.md:127`: "writing or running hook code is out of scope
    (round-13 census), and host package/initramfs hooks are tsukuroi's."
  - `kotoba-shokunin/PROVINCE.md:75` (round-74 sibling-overlap census, tsukuroi row):
    "tsukuroi owns host package and initramfs hooks and OS state as read-only probes
    (PROVINCE.md:22); kotoba routes only client hook-config files and cedes host hooks
    (hook-files-round59.md:20), **a split stated on kotoba's side alone**."
  - `kotoba-shokunin/corpus/knowledge/hook-files-round59.md:20`: "Host package and
    initramfs hooks are tsukuroi's (`.ufo/waves/round-59/w0/ConnSiblingHooks.md`)."
  - `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round74.md:29-42`: records
    tsukuroi reclassified `none → adjacent` on this basis; round-59 closure verdict
    "FITS (tsukuroi host hooks kept …)" (line 39).
  - Note: the tsukuroi-side report kotoba cites (`.ufo/waves/round-59/w0/ConnSiblingHooks.md`)
    is **not present** in the current tsukuroi tree (`find .ufo/waves/round-59 -name
    ConnSiblingHooks*` → nothing; no round-59 dir). The ruling's record currently lives only
    in kotoba's committed bytes.
- **mado-shokunin** owns the Hyprland/waybar/walker/terminal config plane and the omarchy
  theme plane; hook *bodies* are explicitly out:
  - `mado-shokunin/PROVINCE.md:18`: "OUT (report, never absorb): `hooks/**` bodies, …".
  - `mado-shokunin/SKILL.md:1580`: mentions `omarchy-restart-walker` only as the measured
    restart/apply path for walker config edits ("`omarchy-restart-walker` restarts
    `elephant.service` + `app-walker@autostart.service`").
  - `mado-shokunin/SKILL.md:426` and `:1338` ("hooks flat vs `*.d`") are omarchy *skill
    documentation* drift notes, not pacman/ALPM hooks.
- **mori-shokunin** refuses OS-package state:
  - `mori-shokunin/SKILL.md:143-144`: "Refuses OS-package state — pacman/systemd
    units/drivers/firmware/boot are tsukuroi."
  - `mori-shokunin/PROVINCE.md:111-114`: pacman.log used detection-only, handed to tsukuroi.
- **kaidoku-shokunin** owns binary-artifact/archive forensics (its pacman hits are
  `.pkg.tar.zst` cache inventory, `PROVINCE.md:50` and `:62`) — package artifacts, not
  hook semantics; zero narrow-scan hits.
- All remaining siblings (audio, chousa, game-dev-2d, game-dev-3d, kagi, kake, kama,
  kasegi, kengaku, kotodama, kumitate, lore, souji, tabi, tameshi): zero hits in either scan.

### 4. tsukuroi's side of the boundary (for the crossing question)

- `tsukuroi-shokunin/PROVINCE.md` Core: "Owns … pacman state (`pacman -Qkk` verify loops,
  foreign/AUR census, …). Update-safety questions: what an -Syu would touch, what
  pins/holds exist." (`PROVINCE.md:8-13`)
- `tsukuroi-shokunin/PROVINCE.md:22`: "Initramfs v42 and boot recovery — Inspect effective
  mkinitcpio drop-ins, **hooks** and recovery stages; never rebuild or boot."
- `tsukuroi-shokunin/SKILL.md:427-429`: the `walker-restart.hook` root-exec finding is
  routed cross-domain "→ kagi / operator … reported, never absorbed".

## Answers

**Which sibling owns pacman hook semantics?** None but tsukuroi. ALPM/pacman hook semantics
(order, `HookDir` precedence, masking, `AbortOnFail`, transaction gating) are tsukuroi's
declared Core (pacman state + update-safety, PROVINCE.md:9-13) — a cession kotoba states
explicitly and mori honors by refusal. No sibling contests or duplicates it.

**Which sibling owns the omarchy walker hook?** None. `walker-restart.hook`
(Exec `/home/vgpnk/.local/share/omarchy/bin/omarchy-restart-walker`, the row 52 entry of the
r38 table) is a host package hook in `/etc/pacman.d/hooks/` — tsukuroi's plane by kotoba's
cession; its *target* (walker) is mado's plane, but mado puts `hooks/**` bodies OUT
(PROVINCE.md:18) and never names the hook. tsukuroi already routes the finding's risk to
kagi/operator (SKILL.md:427-429).

**Does `corpus/knowledge/pacman-hook-order-r38.md` cross any sibling? No.**
The file documents the host's effective ALPM hook order (69 rows) plus source-level rules
HO1–HO7 read from the installed pacman's own source at commit `54d9411` (source header,
`pacman-hook-order-r38.md:1-3`), and states its own ground: "Ground: the update-safety
plane (`PROVINCE.md` Core)" (`pacman-hook-order-r38.md:7`). Every content element maps to a
tsukuroi-owned surface: hook order/`HookDir`/mask/`AbortOnFail` → pacman state; HO5/HO6
(broken hook blocks the transaction; a failed transaction runs none of the 52 Post hooks,
including `90-mkinitcpio-install.hook` and `99-limine.hook`) → update-safety and the
already-owned initramfs/limine read-only probes (PROVINCE.md:22). The nearest conceivable
adjacency — kaidoku's shipped-artifact internals (tsukuroi ADJ-06) — is not crossed: the
file reads pacman *source text* at the installed version, not a shipped binary, and kaidoku
claims no ALPM semantics (zero hits). mado is touched only incidentally by one table row
(`walker-restart.hook`) whose semantics are ALPM's, not the launcher's.

## One proposed move (adjacency axis)

Asymmetry recorded by the fleet itself: the host-hooks split is "stated on kotoba's side
alone" (kotoba PROVINCE.md:75), tsukuroi's own bytes carry zero whole-word `kotoba` hits
(sibling-overlap-census-round74.md:31-36), and the tsukuroi report kotoba cites from
round 59 no longer exists in this tree. Propose tsukuroi state the cession bilaterally —
one append-only line, no frozen-claim touch:

> Draft, append to the `Refuses` paragraph of `tsukuroi-shokunin/PROVINCE.md`:
> "Client/agent-tooling hook-config files (Claude Code, Codex, VS Code, Copilot, Gemini
> CLI, Cursor, opencode) are kotoba's; this lane owns host package and initramfs hooks —
> ALPM `.hook` semantics, ordering, masks, abort behavior — as read-only probes."

- Affected axes: adjacency (two-sided record of the tsukuroi↔kotoba hook boundary; the
  round-74 census no longer depends on kotoba's bytes alone). C2 unaffected — the line is
  lane-governance text outside the frozen claims/counters.
- Risks: none identified. PROVINCE.md is append-only governance text; no counter reads it;
  no sibling surface changes. Sole cost: one line at the next non-frozen edit window.
- Verification after landing: (a) re-run the narrow scan (receipt command in
  `ConnSiblingsHooks/sibling-scan.txt`) — expect zero non-tsukuroi hits except mado's
  version-erratum line; (b) the fleet census rule already counts a one-sided split, so the
  bilateral line can only strengthen, never weaken, the recorded boundary.

## Checks not run (stated)

- Sibling `corpus/` directories were not scanned — the item scopes the scan to
  `PROVINCE.md`/`SKILL.md`. Kotoba's cession inside its own corpus
  (`hook-files-round59.md:20`) was read only to confirm the `SKILL.md:127`/`PROVINCE.md:75`
  statements.
- No scratch, clones, fixtures, or installs were used (read-only greps only); nothing
  written outside this seat's report/receipt paths.
