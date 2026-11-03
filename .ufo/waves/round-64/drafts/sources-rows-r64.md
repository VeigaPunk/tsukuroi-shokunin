# Round 64 / w1 — S279–S281 registry rows + Gate blocks (draft, seat S1Scribe)

Draft written 2026-11-03T18:58Z by seat **S1Scribe** (scribe; the L1 integrates, nothing here is
landed text). Target file: `corpus/SOURCES.md` — the **single** `## Registry` section, rows inserted
at id position directly after **S278** (the R58-SOURCES-APPEND-POSITION rule), so the file reads
S277 → S278 → **S279 → S280 → S281** → `## Paths`.

All three sources were fetched **live on 2026-11-03** (before the L1's integration; the fetch
receipts are cited below and were re-run a second time at 18:55:36Z for the record). Every URL
returned HTTP 200. All three rows are **11 columns** (`awk -F'|' NF == 13` verified, leading and
trailing `|`), single-line, **no `|` inside any cell**, no escaped pipes.

## 1. The three registry rows (paste-ready, one line each)

```text
| S279 | mkinitcpio v42.2 release notes — https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2 | docs | A | The installed mkinitcpio 42.2-1's own release body, read for the hook changes this release carries: the systemd v262 TPM2/PCR unit additions and the UKI failing-units note; not a summary of the release list | CHANGES WITH v42.2 - Changes in hooks; release v42.2, released_at 2026-10-01T07:10:00.872Z; description body lines 1-11, raw JSON bytes sha256 9ebec7b1c8a1fdccd246282fd868e36acbcc1805917d564b41a0a946516c0bc2, fetched 2026-11-03 | v42.2's only hook change is systemd-only - install/systemd adds systemd-tpm2-setup-early.service and systemd-pcrnvdone.service because of systemd v262, required to initialize NvPCRs and to measure a separator into PCR 9 - and the release states this does not fix failing units with UKIs built by mkinitcpio itself, because systemd v262 requires the UKI to be signed with a PCR policy and there is still no solution for that without using ukify; a busybox-hook host gains nothing from v42.2 | mined | 2026-11-03 | on-release | corpus/knowledge/mkinitcpio42-onrelease-r64.md |
| S280 | limine-entry-tool btrfs-overlayfs hook, master re-pin — https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs | code | A | The upstream master overlay runtime hook's root mount path on 2026-11-03, re-pinned after the mkinitcpio v42 /sysroot change - upstream master bytes against the installed limine-mkinitcpio-hook 1.40.0-2 file | run_latehook line 4, fetched 2026-11-03; raw bytes sha256 eeac1ed326f5c6fed2e47bbb596d76c9c4b0020be30c3b3c58f6b3a4fa093dcf, byte-identical to the installed /usr/lib/initcpio/hooks/btrfs-overlayfs | opens: supersedes S021 - re-pin: the hook still hardcodes /new_root after the v42 /sysroot change; master byte-identical to installed limine-mkinitcpio-hook 1.40.0-2 | mined | 2026-11-03 | on-release | corpus/knowledge/mkinitcpio42-onrelease-r64.md |
| S281 | Arch plymouth packaging initcpio hook, main re-pin — https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook | code | A | The packaged Plymouth busybox late hook's root-path argument on 2026-11-03, re-pinned after the mkinitcpio v42 /sysroot change - packaging main branch bytes against the installed plymouth 26.134.222-3 file | run_latehook line 11, fetched 2026-11-03; raw bytes sha256 de852646e615e06d4125eb2e646d0528d1e349bd9e9877c08c5d32c43d288b6f, byte-identical to the installed /usr/lib/initcpio/hooks/plymouth | opens: supersedes S022 - re-pin: the late hook still passes --new-root-dir=/new_root; fetched bytes identical to installed plymouth 26.134.222-3's hook | mined | 2026-11-03 | on-release | corpus/knowledge/mkinitcpio42-onrelease-r64.md |
```

### Column-by-column shape check (against `scripts/sources-census.sh`)

| # | column | S279 | S280 | S281 |
|---|---|---|---|---|
| 1 | id | `S279` | `S280` | `S281` |
| 2 | source | `docs`/`code` values below | | |
| 3 | kind | `docs` | `code` | `code` |
| 4 | tier | `A` | `A` | `A` |
| 5 | scope | release-body scoped | master-hook scoped | main-branch-hook scoped |
| 6 | anchor | `CHANGES WITH v42.2 - Changes in hooks` + `released_at` + sha256 | `run_latehook line 4` + sha256 | `run_latehook line 11` + sha256 |
| 7 | teaches | one grounded learner benefit, no host claim | `opens: supersedes S021 - re-pin: …` | `opens: supersedes S022 - re-pin: …` |
| 8 | status | `mined` | `mined` | `mined` |
| 9 | opened | `2026-11-03` | `2026-11-03` | `2026-11-03` |
| 10 | recheck | `on-release` | `on-release` | `on-release` |
| 11 | used-by | `corpus/knowledge/mkinitcpio42-onrelease-r64.md` (×3) | | |

### Live census proof of the row shape (scratch rig, read-only, LF-normalized copy)

The rig is a **scratch copy** of the lane tree under
`/fast/scratch/hyaku/tsukuroi-r64/S1Scribe/fakeroot/` (the lane's own `corpus/SOURCES.md` was
CR-stripped into a copy; the lane file itself was never written by this seat). The three rows were
inserted at the S278 id position in the rig copy and the canonical census run against it:

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <rig>/fakeroot tsukuroi
rc=0
E-codes: 0        (E01/E02/E03/E04/E05/E06/E07/E08/E09/E10/E11/E12 all absent)
W04-count: 44     (baseline 42 + 2 new, see "Schema notes" below)
rows: 281         (baseline 278 + 3)
tier.A 265 / tier.B 5 / tier.C 11 ; status.mined 253 / queued 5 / rejected 23
```

```
$ awk -F'|' '{print NR": NF="NF}' rows-test.txt
1: NF=13
2: NF=13
3: NF=13
```

The census's own `E04` rule ("duplicate url **within** scope" is an error) does **not** fire for
S280/S281: their URLs duplicate S021/S022 (and S098/S111) but in a **different scope**, which is the
`W04` "duplicate url across scopes" warning class — the same class the register already carries 42
times and the same shape as the 25 existing `supersedes Sxxx` rows. Exit code is 0 either way.

## 2. The three Gate blocks (round lesson `## Gate`)

Each block: URL, access date, and a located quote of ≤ 25 words **with its location**, plus the
`printf '%s' "<quote>" | wc -w` count printed next to the quote.

### S279 — mkinitcpio v42.2 release notes

- **URL**: https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2
- **Accessed**: 2026-11-03 (live fetch, HTTP 200, 3905 bytes; raw JSON sha256
  `9ebec7b1c8a1fdccd246282fd868e36acbcc1805917d564b41a0a946516c0bc2`; release `v42.2`,
  `released_at 2026-10-01T07:10:00.872Z`, changelog commit `e5433c2e3cb8f80dc77708b01d841a7f4dc864a0`).
- **Located quote** (release JSON `description` field, body lines 5–6, the `* install/systemd …`
  bullet under `Changes in hooks:`) — **11 words** by `printf '%s' "<quote>" | wc -w`:

  > install/systemd includes systemd-tpm2-setup-early.service and systemd-pcrnvdone.service because of changes in systemd v262.

- **Supporting located text** (same `description` field, body line 7) — **14 words**:

  > They are required to initialize NvPCRs and to measure a separator into PCR 9.

- **Supporting located text** (same `description` field, body lines 8–9) — **17 words**:

  > Note that this does not fix the issue of failing units with UKIs built by mkinitcpio itself.

- **Supporting located text** (same `description` field, body lines 9–11) — **24 words**:

  > systemd v262 requires that the UKI must be signed with a PCR policy and there is still no solution for that without using ukify.

  (Quote word counts: the three supporting quotes are contiguous in the source **as a run of
  whitespace-normalized text**; each is verbatim modulo the source's own line wrapping. The
  verbatim single-line check was run on the whitespace-normalized `description` value:
  `VERBATIM_IN_DESC: True` for all three, offsets 57 / 191 / 289 in the decoded description.)

### S280 — limine-entry-tool `btrfs-overlayfs` hook (master)

- **URL**: https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs
- **Accessed**: 2026-11-03 (live fetch, HTTP 200, 1519 bytes; raw bytes sha256
  `eeac1ed326f5c6fed2e47bbb596d76c9c4b0020be30c3b3c58f6b3a4fa093dcf`; byte-identical to the
  installed `/usr/lib/initcpio/hooks/btrfs-overlayfs`, owned by `limine-mkinitcpio-hook 1.40.0-2`).
- **Located quote** (file **line 4**, the `root_mnt` assignment inside `run_latehook()`) — **1 word**
  by `printf '%s' "<quote>" | wc -w`:

  > root_mnt="/new_root"

- **Supporting located text** (file **line 6**, the Btrfs check comment) — **7 words**:

  > # Check: Is $root_mnt mounted on Btrfs?

- **Supporting located text** (file **line 21**, the overlay-setup message) — **12 words**:

  > echo "[OverlayFS setup] ${root_mnt} is a read-only Btrfs subvolume. Setting up OverlayFS..."

### S281 — Arch plymouth packaging initcpio hook (`main`)

- **URL**: https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook
- **Accessed**: 2026-11-03 (live fetch, HTTP 200, 336 bytes; raw bytes sha256
  `de852646e615e06d4125eb2e646d0528d1e349bd9e9877c08c5d32c43d288b6f`; byte-identical to the
  installed `/usr/lib/initcpio/hooks/plymouth`, owned by `plymouth 26.134.222-3`).
- **Located quote** (file **line 11**, the `run_latehook()` body) — **3 words** by
  `printf '%s' "<quote>" | wc -w`:

  > plymouth update-root-fs --new-root-dir=/new_root

- **Supporting located text** (file **line 10**, the `run_latehook` opener) — **1 word**:

  > run_latehook(){

### Gate counts summary

| row | primary quote words | supporting quote words | all ≤ 25 |
|---|---|---|---|
| S279 | 11 | 14, 17, 24 | yes |
| S280 | 1 | 7, 12 | yes |
| S281 | 3 | 1 | yes |

## 3. Fetch receipts (the three live opens)

```
2026-11-03T18:55:36Z
$ curl -sS -L --max-time 60 -o /dev/null -w "rc_http=%{http_code} bytes=%{size_download} url=%{url_effective}\n" 'https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2'
rc_http=200 bytes=3905 url=https://gitlab.archlinux.org/api/v4/projects/archlinux%2Fmkinitcpio%2Fmkinitcpio/releases/v42.2
curl_rc=0
$ curl -sS -L --max-time 60 -o /dev/null -w "rc_http=%{http_code} bytes=%{size_download} url=%{url_effective}\n" 'https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs'
rc_http=200 bytes=1519 url=https://gitlab.com/Zesko/limine-entry-tool/-/raw/master/install/arch-linux/limine-mkinitcpio-hook/usr/lib/initcpio/hooks/btrfs-overlayfs
curl_rc=0
$ curl -sS -L --max-time 60 -o /dev/null -w "rc_http=%{http_code} bytes=%{size_download} url=%{url_effective}\n" 'https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook'
rc_http=200 bytes=336 url=https://gitlab.archlinux.org/archlinux/packaging/packages/plymouth/-/raw/main/plymouth.initcpio_hook
curl_rc=0
$ sha256sum mkinitcpio-v42.2.json limine-btrfs-overlayfs-hook plymouth.initcpio_hook
9ebec7b1c8a1fdccd246282fd868e36acbcc1805917d564b41a0a946516c0bc2  mkinitcpio-v42.2.json
eeac1ed326f5c6fed2e47bbb596d76c9c4b0020be30c3b3c58f6b3a4fa093dcf  limine-btrfs-overlayfs-hook
de852646e615e06d4125eb2e646d0528d1e349bd9e9877c08c5d32c43d288b6f  plymouth.initcpio_hook
$ cmp /usr/lib/initcpio/hooks/btrfs-overlayfs limine-btrfs-overlayfs-hook
limine_cmp_rc=0
$ cmp /usr/lib/initcpio/hooks/plymouth plymouth.initcpio_hook
plymouth_cmp_rc=0
$ pacman -Qo /usr/lib/initcpio/hooks/btrfs-overlayfs /usr/lib/initcpio/hooks/plymouth
/usr/lib/initcpio/hooks/btrfs-overlayfs is owned by limine-mkinitcpio-hook 1.40.0-2
/usr/lib/initcpio/hooks/plymouth is owned by plymouth 26.134.222-3
rc=0
$ pacman -Q mkinitcpio limine-mkinitcpio-hook plymouth
mkinitcpio 42.2-1
limine-mkinitcpio-hook 1.40.0-2
plymouth 26.134.222-3
```

## 4. Schema notes for the L1 (flagged, not fixed)

1. **W04 count moves 42 → 44, and the C1 after-predicate text says 42.** The declaration's C1
   predicate (a) says the same census command must exit 0 with "the 42 W04 duplicate-url-across-scope
   warnings reappear". After S279–S281 land, the count is **44**: S280 re-pins the limine master hook
   URL already carried by S021 and S098, and S281 re-pins the plymouth `main` hook URL already carried
   by S022 — each in a new scope, so each is one `W04` (warning class), not `E04` (error). The exit
   code stays 0 and the E-code count stays 0. The predicate's **exit-0 and zero-E-code** halves are
   unaffected; only the stated W04 figure needs restating as 42 before the rows and 44 after. (Flagged
   to SC2Census; folded into `.ufo/waves/round-64/after/gates-recon.md`.)
2. **`E11` until the knowledge note exists.** All three rows carry
   `used-by = corpus/knowledge/mkinitcpio42-onrelease-r64.md`. That file does not exist on disk yet, so
   the census reports **three `E11` findings** (missing used-by) for the rows until the MK note lands.
   The census **END** receipt must therefore be taken after the note is written, or the end receipt
   carries three landing-order artifacts instead of a clean rc 0. (Also folded into `gates-recon.md`.)
3. **The `supersedes` wording — seat-spec text, flagged as a house-form observation.** The row text
   for S280/S281 is verbatim from this seat's specification (`opens: supersedes S021 - re-pin: …` /
   `opens: supersedes S022 - re-pin: …`) and is reproduced unchanged above. For the record: the
   register's established pattern for a re-pin row is `supersedes S0NN — …` at the head of the
   **teaches** cell (25 existing rows, e.g. S094→S109, S098→S112), and the `opens: ` prefix appears
   **nowhere** in the current 278-row register (`grep -c 'opens:' corpus/SOURCES.md` → 0 at the
   base). The census's `E04` exemption only tests `teaches !~ /supersedes S[0-9]{3}/` (a substring
   test), so `opens: supersedes S021 …` passes it and the exit code is unaffected either way.
   **Nothing changed here** — this is the L1's wording call, not a silent fix by the scribe.
4. **S279's anchor carries the API's exact `released_at`, not a rounded value.** The seat spec wrote
   `released_at 2026-10-01T07:10:00Z`; the live JSON says `2026-10-01T07:10:00.872Z`
   (`created_at` identical). The row above carries the exact value, because the row's own claim is
   that this release body was fetched and read today; a rounded timestamp would misstate the anchor
   it is standing on. The `CHANGES WITH v42.2` / `Changes in hooks:` heading text is reproduced
   verbatim from the `description` field.
5. **`teaches` cell must not carry a host claim.** The census does not police this, but QUALITY 1–3
   do: S280/S281's `teaches` cells assert only what the fetched bytes show (the hardcoded
   `/new_root`; the `--new-root-dir=/new_root` argument) plus the byte-identity to the installed
   package file, which the receipt above proves. The host-level consequence (the v42 compatibility
   symlink, the mechanism refutation, the boot-level unknown) belongs to the MK rows in the note
   (E3Mk42's draft), **not** to these registry rows. S279's `teaches` cell likewise stays inside the
   release body (systemd-only change; the UKI failing-units note) and makes no busybox-hook
   consequence claim beyond what the text supports.
6. **The installed-file byte-identity claims are proved, not assumed.** `cmp` rc 0 against
   `/usr/lib/initcpio/hooks/btrfs-overlayfs` and `/usr/lib/initcpio/hooks/plymouth`, with the owning
   packages identified by `pacman -Qo` — so "master byte-identical to installed" and "fetched bytes
   identical to installed" are measured facts, not inferences.
7. **Line endings of the pasted rows.** The three rows above are LF-terminated single lines. The
   lane's `corpus/SOURCES.md` is CRLF at the base (`381/381` CR lines) and E1LineEnd owns the
   CR-normalization; the rows must be pasted into the **CR-normalized** file (the L1's C1 repair),
   otherwise the registry's own line-ending convention is re-broken. The guard
   `tools/check-line-endings-r64.py --check` covers this.
