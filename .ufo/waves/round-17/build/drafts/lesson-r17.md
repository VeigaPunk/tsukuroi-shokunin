# Round 17 — next-boot safety after the 2026-10-20 mkinitcpio 42.2 upgrade

Author: tsukuroi L1; scribe skeleton (TsukuroiR17.LessonDraft-2), 2026-10-20. Baseline `6923fe0bd3add04fc90f3bc3522895b27cf44bbe`. Every `<L1 fills>` is a placeholder; L1 replaces it with a command result or path:line before commit. Nothing in this skeleton is verified.

## Declared claim

- **C1/depth (lowest axis):** per-limine-entry next-boot verdicts from extracted boot images, new `corpus/knowledge/boot-chain-r17.{md,json}`. Kernel entries with a derived verdict 0→5 (`<L1 fills: count from boot-chain-r17.json>`). Verdict rules and entries: `corpus/knowledge/boot-chain-r17.md` § Decision table (lines 60–67).
- **C2/freshness:** dated R17 notices on current-use host observations invalidated by the 09:15 upgrade, plus `corpus/knowledge/freshness-recheck-r17.json`. Resolved records 0→`<L1 fills: N>`.
- **C3/operability:** revision-taking gates bind `--revision` to the landed branch; reject HEAD/`@`-style and unlanded commits. Bound tools 0→`<L1 fills: N, target 5>`.
- **Frontier:** SOURCES rows opened this round: S051, S052 (own-work, A), S053, S054 (docs/code, A); `corpus/SOURCES.md` lines 57–60.
- **Mined mistake:** steer-scope violation (see `## Mistakes`).
- **Depth unchanged-by-design axis note:** C1 works depth; other axes move only where the Gate shows evidence.

## Gate

Admission table. Candidates from this round; verdict column is L1's.

| candidate | kind | evidence pointer | verdict |
|---|---|---|---|
| `corpus/knowledge/boot-chain-r17.md` + `.json` (C1) | knowledge entry, own-work sources S051/S052 | capture lines 31–41 (ls -d local dirs, no pacman), 62–67 decision table; `fresh-capture.txt:2` "no pacman invocation" | `<L1 fills: admit / reject + reason>` |
| Blocker: recheck names `tools/boot-chain-audit.sh --live` (boot-chain-r17.md:3) | dependency | `ls tools/` at baseline shows no `boot-chain-audit.sh`; BootAuditTool seat owns it | `<L1 fills: admit only after tool lands at landed rev, or reject recheck line>` |
| R17 freshness notices + `freshness-recheck-r17.json` (C2) | appended notices + registry | notices append-only; no prior bytes changed | `<L1 fills: count resolved records, byte-prefix check>` |
| Steer-safe recheck append in `corpus/knowledge/initramfs-v42-sysroot-recovery.md` (`## R17-RECHECK`) | appended notice | header `recheck:` at line 3 still names `pacman -Q` (live, unfixed) | `<L1 fills: appended block present; line 3 status>` |
| Revision-binding gates (C3): `check-section-citations.py` and the five R17 revision tools | tools | `<L1 fills: bound tool count; --revision HEAD rejected with E-REVISION-INVALID exit 2>` | `<L1 fills>` |
| `tools/check-recheck-commands.py` (mined-mistake fix, QUALITY26) | tool | absent at baseline (`tools/` glob); must be red on `initramfs-v42-sysroot-recovery.md:3` at baseline | `<L1 fills: baseline exit code and finding id; landed-rev result>` |
| `tools/check-seat-scope.py` (QUALITY24 demonstrability) | tool | absent at baseline | `<L1 fills: red fixture result>` |
| S051–S054 rows in `corpus/SOURCES.md` | registry | present lines 57–60; row count `<L1 fills: grep -cE count, command + date>` | `<L1 fills>` |

Rejected readings (kept per CORPUS and QUALITY 5):

- "linux-lts protects against the mkinitcpio 42 hook mismatch." Rejected: identical `init` and hook bytes (`boot-chain-r17.md` lines 131–132).
- "The 42.x image's empty `/new_root` directory keeps the overlay hook working." Rejected: `findmnt --mountpoint` needs a real mountpoint; nothing mounts there under v42 `init` (boot-chain-r17.md lines 133–135).
- "The successful 09:57 boot proves snapshot rollback works." Rejected: default root is a writable subvolume (boot-chain-r17.md lines 136–137).
- "No pacman.log rebuild after 09:18 means the booted UKI is the 09:18 build." Rejected: `limine-update` at 09:26:11 rebuilt it (boot-chain-r17.md lines 138–139).
- "The mkinitcpio ≥42 TPM2 manual-intervention news applies here." N/A: HOOKS omit `systemd` (`initramfs-v42-sysroot-recovery.md` line 28).
- "A clean gate verdict grants package or service action." Rejected: both R17 notices state no package or service action is authorized (`<L1 fills: notice line numbers>`).
- "A recheck gate that greps a header line proves the procedure is steer-safe." Open: `<L1 fills: critic outcome from CritNextBootChecklist / recheck critic seat>`.

Spot-check: `<L1 fills: non-author spot-check result, or "none this round">`.

Source census — start: `<L1 fills: scripts/sources-census.sh validate output and exit>`.
Source census — end: `<L1 fills: same command at landed revision>`.

## Mistakes

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| scope (steer-scope violation) | Steer forbids pacman. `corpus/knowledge/initramfs-v42-sysroot-recovery.md:3` `recheck:` prescribes `pacman -Q mkinitcpio …`; the same command's 2026-10-19 output is recorded at `:9`. Round-17 instance: L1 ran `pacman -Q mkinitcpio …` at round start, before re-reading the steer. `<L1 fills: transcript or shell-history path:line for that run; UNVERIFIED — no pacman -Q appears in .ufo/waves/round-17/l1-capture/>` | none. QUALITY24 (`corpus/QUALITY.md` item 24) covers wave seats only, not lane-author recheck prose | QUALITY26 (proposed in the build spec, not yet in `corpus/QUALITY.md`, which ends at item 24) plus `tools/check-recheck-commands.py`, shown red at baseline on `initramfs-v42-sysroot-recovery.md:3` (`<L1 fills: exit code and finding id>`). Design decision for L1: correction is append-only (CORPUS), but a green gate needs the header line or a newest-block rule. Choose one and record it; do not rewrite history silently. |

## Routed debts — r16 verifier spot-check § 5

Source: `corpus/lessons/round-16-verifier-spotcheck.md` § 5 (lines 127–137).

| item | r16 routed text (short) | r17 disposition | evidence |
|---|---|---|---|
| 1 | R16-FALSIFY unexercised; falsify32 wave owed or operator waiver recorded | `<L1 fills: wave-2 falsify dispatch registry path, or operator ruling quoted>` | `<L1 fills>` |
| 2 | Godspeed bytes: carry verbatim `/skill:godspeed` directive in dispatch payload | Build spec prompts begin with the directive bytes (`spec.json` prompt field, e.g. line 355 region). Confirm against `dispatch.json` payload | `<L1 fills: byte-compare command and result>` |
| 3 | Seat-scope deviations (SafetyHost, ConnectMistakes, ConnectAdjacency, DraftIndex); QUALITY24 not shown able to fail | `tools/check-seat-scope.py` (SeatScopeGate). Absent at baseline | `<L1 fills: red fixture result and finding ids>` |
| 4 | Advisory `frozen-cases.json` drift (nonexistent worktree mode; count prose contradicts MD-missing vector) | File still present at `.ufo/waves/round-16/build/frozen-cases.json`. Reconcile or mark superseded | `<L1 fills: reconciled or superseded marker, path:line>` |
| 5 | Census W04 x7 cross-scope duplicate-URL warnings | Carried, not new | `<L1 fills: census output at landed rev>` |

## Operator and scope notes

- No pacman transaction was invoked by this lesson or its seats; the steer keeps all transactions paused. Recovery, boot-hook compatibility and package/service decisions stay operator-owned (boot-chain-r17.md lines 9–11).
- Tools installed or updated this round: `<L1 fills: none, or tool/version/channel/reason>`.
- Known unknowns carried: plymouth handling of the unmounted `/new_root` (boot-chain-r17.md line 87); origin of the empty `new_root` directory in 42.x images (line 45); snapshot login reachability (line 150).
