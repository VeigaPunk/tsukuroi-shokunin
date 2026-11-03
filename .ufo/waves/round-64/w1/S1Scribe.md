2026-11-03T19:05:00Z

# S1Scribe — wave report (round 64 / w1), item C3-DOCS

Seat: **S1Scribe** (scribe). Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Scope: draft only — the L1 (TsukuroiR64) integrates and lands. No commit, no push, no mutating
git/jj command, no product-code edit. Two files written, both under my named wave dir
`.ufo/waves/round-64/drafts/`. `corpus/`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, `MANIFEST.json` and
every sibling file were **read-only** to this seat.

## Deliverables (both draft paths)

| artifact | path | bytes | CR lines |
|---|---|---|---|
| S279–S281 registry rows + Gate blocks | `.ufo/waves/round-64/drafts/sources-rows-r64.md` | 16063 | 0 / 217 |
| round-64 lesson skeleton | `.ufo/waves/round-64/drafts/lesson-skeleton-r64.md` | 12432 | 0 / 169 |
| this wave report | `.ufo/waves/round-64/w1/S1Scribe.md` | — | 0 |

## Behavior — what I did

1. **Read the form first**: `corpus/SOURCES.md` (registry header + row shape + `## Paths`),
   `corpus/lessons/round-63.md` (lesson shape, `## Gate` and `## Mistakes` rows), `corpus/lessons/
   round-61.md`/`round-62.md` (older `## Gate` shapes), `corpus/lessons/round-17.md`/`round-18.md`
   (the `author:` header line convention), `LOG.md` "Round 64 — declaration" (`2f3061ef`), and
   `scripts/sources-census.sh` (the row validator: 11 columns ⇒ NF 13, `E01`–`E12`, `W04`, the
   `E04` "duplicate url within scope" rule and its `supersedes S\d{3}` exemption).
2. **Opened the three sources live** (network reads only; HTTP 200 on all three; a second re-run at
   18:55:36Z for the record).
3. **Drafted the three registry rows** and the **three Gate blocks** (URL, access date, located quote
   ≤ 25 words with its location, and the `wc -w` count next to every quote).
4. **Drafted the lesson skeleton** with the `## Gate` (candidates / admitted / rejected / spot-check),
   the fully written `## Mistakes` row `R64-CRLF-HOST-DRIFT`, and the `## No-further-mistakes sweep`
   placeholder.
5. **Proved the row shape against the real census** in a read-only scratch rig (an LF-normalized
   copy of the lane tree — the lane's own files were never written), rather than asserting it.

## The three quotes and their `wc -w` counts

`printf '%s' "<quote>" | wc -w` — every count below is that command's output, printed next to its
quote in the draft.

**S279** — mkinitcpio v42.2 release notes,
https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2
(accessed 2026-11-03; HTTP 200, 3905 bytes; raw JSON sha256 `9ebec7b1c8a1fdccd246282fd868e36acbcc1805917d564b41a0a946516c0bc2`;
`released_at 2026-10-01T07:10:00.872Z`; changelog commit `e5433c2e3cb8f80dc77708b01d841a7f4dc864a0`).

> install/systemd includes systemd-tpm2-setup-early.service and systemd-pcrnvdone.service because of changes in systemd v262.

**11 words** — location: the `description` field, `CHANGES WITH v42.2` → `Changes in hooks:` →
the `* install/systemd …` bullet (body lines 5–6). Supporting located quotes, same field:
"They are required to initialize NvPCRs and to measure a separator into PCR 9." — **14 words**
(line 7); "Note that this does not fix the issue of failing units with UKIs built by mkinitcpio
itself." — **17 words** (lines 8–9); "systemd v262 requires that the UKI must be signed with a PCR
policy and there is still no solution for that without using ukify." — **24 words** (lines 9–11).

**S280** — limine-entry-tool `btrfs-overlayfs` hook, master,
https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs
(accessed 2026-11-03; HTTP 200, 1519 bytes; sha256 `eeac1ed326f5c6fed2e47bbb596d76c9c4b0020be30c3b3c58f6b3a4fa093dcf`;
`cmp` rc 0 vs the installed `/usr/lib/initcpio/hooks/btrfs-overlayfs`, owned by
`limine-mkinitcpio-hook 1.40.0-2`).

> root_mnt="/new_root"

**1 word** — location: file **line 4**, the `root_mnt` assignment inside `run_latehook()`. Supporting
located quotes: "# Check: Is $root_mnt mounted on Btrfs?" — **7 words** (line 6); `echo "[OverlayFS
setup] ${root_mnt} is a read-only Btrfs subvolume. Setting up OverlayFS..."` — **12 words** (line 21).

**S281** — Arch plymouth packaging initcpio hook, `main`,
https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook
(accessed 2026-11-03; HTTP 200, 336 bytes; sha256 `de852646e615e06d4125eb2e646d0528d1e349bd9e9877c08c5d32c43d288b6f`;
`cmp` rc 0 vs the installed `/usr/lib/initcpio/hooks/plymouth`, owned by `plymouth 26.134.222-3`).

> plymouth update-root-fs --new-root-dir=/new_root

**3 words** — location: file **line 11**, the `run_latehook()` body. Supporting located quote:
"run_latehook(){" — **1 word** (line 10).

No quote exceeds 25 words; no cell contains a pipe. The S279 quotes are verbatim modulo the
release body's own line wrapping — checked on the whitespace-normalized `description` value
(`VERBATIM_IN_DESC: True` at decoded-description offsets 57 / 191 / 289).

## Gates the drafts satisfy

- **Row shape**: all three rows are single lines, 11 columns (`awk -F'|'` → **NF = 13** on each,
  re-verified after extracting them back out of the finished draft), leading `|`, trailing `|`,
  **no `|` inside any cell**, no escaped pipes, LF-terminated.
- **Live census (read-only scratch rig)**: `sources-census.sh validate --root <rig> tsukuroi` →
  **rc 0**, **0 E-codes**, **W04 44**, rows **281** (tier.A 265 / B 5 / C 11; mined 253 / queued 5 /
  rejected 23), S279 inserted at the id position directly after S278.
- **Gate quote lengths**: 11 / 14 / 17 / 24 (S279), 1 / 7 / 12 (S280), 3 / 1 (S281) — all ≤ 25.
- **Byte-identity claims are measured, not assumed**: `cmp` rc 0 for both hooks against the
  installed files, `pacman -Qo` naming the owning packages, `pacman -Q` naming the installed
  versions (`mkinitcpio 42.2-1`, `limine-mkinitcpio-hook 1.40.0-2`, `plymouth 26.134.222-3`).

## Touched surfaces

- **Written**: `.ufo/waves/round-64/drafts/sources-rows-r64.md`,
  `.ufo/waves/round-64/drafts/lesson-skeleton-r64.md`, `.ufo/waves/round-64/w1/S1Scribe.md`.
- **Read only**: `corpus/SOURCES.md`, `corpus/lessons/round-{17,18,61,62,63}.md`,
  `corpus/QUALITY.md`, `LOG.md`, `scripts/sources-census.sh`, `tools/check-knowledge-header.py`,
  `.ufo/waves/round-64/before/*`, `.ufo/waves/round-64/probes/mk42/*`,
  `.ufo/waves/round-64/after/mk42-rows-draft.md`, `tools/check-line-endings-r64.py` (existence only).
- **Scratch**: `/fast/scratch/hyaku/tsukuroi-r64/S1Scribe/` (raw fetches + the census rig), deleted
  before this report was written.

## Findings — schema problems flagged, not fixed

1. **The W04 figure in the C1 after-predicate moves 42 → 44.** The declaration's C1 predicate (a)
   says the same census command must exit 0 with "the 42 W04 duplicate-url-across-scope warnings
   reappear". After S279–S281 land, the count is **44**: S280 re-pins the limine master hook URL
   (already carried by S021 and S098) and S281 re-pins the plymouth `main` hook URL (already carried
   by S022), each in a **new scope**. That is the `W04` "across scopes" warning class, **not** the
   `E04` "within scope" error (whose `teaches !~ /supersedes S[0-9]{3}/` exemption the rows also
   satisfy). The exit-0 and zero-E-code halves of the predicate are unaffected; only the stated
   warning count needs restating as 42 before the rows and 44 after. Raised with **SC2Census** and
   folded into `.ufo/waves/round-64/after/gates-recon.md` with attribution.
2. **Three `E11` findings until the knowledge note exists.** All three rows carry `used-by
   corpus/knowledge/mkinitcpio42-onrelease-r64.md`, which is not on disk yet, so the census reports
   E11 (missing used-by) for each row until the MK note lands. The census **END** receipt must be
   taken **after** the note exists, or the end receipt carries three landing-order artifacts instead
   of a clean rc 0. Also folded into `gates-recon.md`.
3. **`opens: ` prefix is not house form.** The seat spec's S280/S281 `teaches` text begins
   `opens: supersedes S021 - re-pin: …`. The register's 25 existing superseding rows start the
   `teaches` cell with `supersedes S0NN — …`, and `grep -c 'opens:' corpus/SOURCES.md` is **0** at
   the base. The census does not care (substring test), so I reproduced the spec text **unchanged**
   and flagged it as the L1's wording call.
4. **S279's `released_at`: the spec rounded it.** The seat spec wrote `released_at
   2026-10-01T07:10:00Z`; the live API says `2026-10-01T07:10:00.872Z` (`created_at` identical). The
   row carries the exact value, because the row's claim is that this release body was read today.
   Flagged in the draft's schema notes.
5. **One nuance in the declared blob archaeology — the "parent is 100% LF" clause does not hold for
   `SCORECARD.md`.** Measured from the lane's git objects (`git show <c>:F | grep -c $'\r'`):

   | commit | meaning | `corpus/SOURCES.md` | `SKILL.md` | `SCORECARD.md` |
   |---|---|---|---|---|
   | `81776bef` | r58 carry-in | 0/376 CR | 0/4886 CR | 0/4127 CR |
   | `c5a33d08` | r59 **declaration** | 0/376 CR | 0/4886 CR | **4178/4178 CR** |
   | `2913b75d` | r59 **work** | **377/377 CR** | **4990/5009 CR** | 4178/4178 CR |

   So `c5a33d08` is 100% LF for `corpus/SOURCES.md` and `SKILL.md` (and `2913b75d` is the first CR
   commit for those two), but `SCORECARD.md` was **already fully CRLF at `c5a33d08`** — its first CR
   commit is the round-59 *declaration*, one commit earlier than the round-59 *work* commit. The
   class, the file set, the counts (381/381, 5452/5489, 4654/4701) and the fix are unchanged; only
   the "which commit first carried CR in SCORECARD.md" detail needs the per-file form. I wrote the
   declared row text as specified **and** added a scribe's archaeology note with this measurement,
   flagged for the L1 — I did not silently rewrite the declared claim.
6. **E12's blast radius is heading-anchored, and one CR is enough.** Reproduced in the scratch rig:
   with the whole file LF-clean and **one** CR injected into the `## Registry` heading line, the
   census reports **E12 = 278** (every row) and 0 W04 — i.e. the 278 E12s in the round-start receipt
   are caused by the heading match, not by 278 damaged rows. This is the same finding SC2Census
   reported; it independently confirms that the CR-strip repair (not per-row surgery) is the
   correct fix, and that the C1 byte-identity proof (`git show <pre>:F | tr -d '\r' | cmp - F`) is
   the right acceptance test.

## Out of scope — explicitly not done

- No edit to `corpus/SOURCES.md`, `corpus/lessons/round-64.md`, `SKILL.md`, `SCORECARD.md`,
  `LOG.md`, `corpus/QUALITY.md`, `corpus/README.md`, `MANIFEST.json`, or any `.ufo/state/` path.
- No commit, push, or any mutating git/jj command (no `add`/`commit`/`stash`/`checkout`/`reset`/
  `pull`/`push`).
- No `pacman` transaction of any kind, no `systemctl` action, no `journalctl --rotate/--vacuum`, no
  write to `/etc`, `/boot` or `/var/lib/pacman`, no privileged probe, no secret read.
- No new source opened beyond the three the item named; no lead retired.
- No `## Gate` "admitted" list filled in — those are the L1's placeholders
  (`<<<L1: fill after integration>>>`), deliberately left open.
- No rejection row written: none of the three sources was rejected, and the zero-rejection statement
  in the skeleton is scoped to exactly those three rows plus the CRLF criterion candidate.

## Checks the main agent should run

1. `awk -F'|' 'NF!=13' corpus/SOURCES.md` → 0 rows; `grep -c '^| S27[89] ' corpus/SOURCES.md` → 3;
   `grep -n '^| S279 ' corpus/SOURCES.md` → directly after the S278 row.
2. `bash <fleet-root>/scripts/sources-census.sh validate --root <fleet-root> tsukuroi` → rc 0, 0
   E-codes, **W04 = 44** (42 before the rows), rows 281 — **taken after
   `corpus/knowledge/mkinitcpio42-onrelease-r64.md` exists**, or three E11s appear.
3. `python3 tools/check-line-endings-r64.py --check` → rc 0 over the lane tree; `--selftest` → PASS.
4. `python3 tools/check-knowledge-header.py --revision <work> --round 64` → PASS, the new MK note
   listed with no problems.
5. Re-measure the three Gate quote word counts with `printf '%s' "<quote>" | wc -w` on the landed
   text: 11 / 14 / 17 / 24 (S279), 1 / 7 / 12 (S280), 3 / 1 (S281).

## Scratch cleanup

`/fast/scratch/hyaku/tsukuroi-r64/S1Scribe/` removed after the drafts were written (raw fetch
copies and the census rig). Every receipt needed downstream is reproduced inside
`.ufo/waves/round-64/drafts/sources-rows-r64.md` §3 (fetch receipts with UTC stamp, `$ command`,
output and `rc`) and in this report — no `/tmp` or scratch path is cited as evidence.

**Report**: `.ufo/waves/round-64/w1/S1Scribe.md`
