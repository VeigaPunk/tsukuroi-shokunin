# Decision row — foreign package absent from `pacman -Qu` (R15-DEC-FOREIGN-NOT-IN-QU)

Report-only fragment for L1. No docs edits, host-state commands, package action, or child dispatch.
Consumes `.ufo/waves/round-15/build/host-snapshot.json`; sole added read is the shipped static pacman(8) page.

## Row

| Field | Value |
|---|---|
| Trigger | installed `p` has no `pacman -Qu` line and is foreign (`pacman -Qm`: absent from every configured sync DB) |
| Naive inference (reject) | no `-Qu` row ⇒ `p` current / safe / nothing to do |
| Verdict | `FOREIGN_INDETERMINATE` — **not current, not safe**: no currency or safety credit is earned |
| Clarification | "not safe" = *not certified*, not *proven unsafe*; absence supports neither polarity |
| Action | keep installed state and provenance; no upgrade, rebuild, re-source, signature relaxation, or removal on `-Qu` silence |
| Gate effect | cannot clear a package decision; class-specific provenance review remains owed |

## Why it is structural

S049 (pacman(8), docs/A, mined) quotes `-u` as “Only package versions are used to find outdated packages; replacements are not checked here.” (14 words). The shipped pacman(8) (Pacman Manual 7.1.0, man date 2026-05-06, QUERY OPTIONS) defines `-m, --foreign` as “Restrict or filter output to packages that were not found in the sync database(s).” (15 words).

With `L` installed and `S` configured sync, `-Qu` compares versions only for `L ∩ S`; for `p ∈ L \ S` no sync-side version term exists, so `p ∉ -Qu` for every upstream version. The absence is invariant and carries zero bits about currency or safety. Corpus restatements: “invisible to the upgrade resolver, not merely unchanged” (`aur-risk-plane.md` §0), “never in `-Qu` by construction” (`update-safety-v2.md` §2.2), “not a claim that the foreign set is correct, current, or safe” (`aur-drift-receipt-r9.md` §0).

## Fresh retained evidence (consumed)

- `captured_at` 2026-10-20T07:44:39Z; `pending_updates` = `pacman -Qu`, exit 0, **413 lines**; parsing all 413 for the 16 registry foreign names → **0 hits**. A non-empty candidate set omitting every foreign row is sharper than empty-`-Qu` vacuity.
- `sync_metadata`: five `.db` files born 2026-10-18 14:11:00.026 -0300; sync-dir presence ≠ configured repo (`offline.db` counterexample), so the channel set must come from `pacman-conf`.
- Limit: the snapshot did not run `pacman -Qm` or `pacman -Si`; it neither re-enumerates nor re-classifies foreign rows. Bounds: these 16 names, this capture.

## Provenance envelope that must survive

`-Qm` means only "absent from configured sync DBs"; it is not proof of AUR origin (`arch-news-gate-2026.md`, 2026-06-12 AUR item). Carry name@version, reason/date, class, supplying artifact/db, validation/signer, channel liveness, upstream state, dependency edge.

- `aur-local` (2): `android-apktool-bin` 3.0.3-1, `obsidian-cli-inspector` 1.0.3-1; yay clones, `Validated By: None`; yay→AUR is external and never `-Qu`; review-on-update: diff PKGBUILD vs retained clone, confirm sha256 pins with `pkgver`, never blind `yay -Syu`.
- `offline-exile` (14): 13 `elephant*` 2.21.0-1 + `omarchy-walker` 1.0.0-2; `offline.db` chain, `SHA-256 Sum Signature` GOODSIG, `pacman -Si` rc=1; preserve `offline.db`, 14 `.zst` + 14 `.sig`, yay trees; do not improvise a source.
- `unknown-provenance` (0): rule, never guessed; probe order pacman.log `-U` → yay cache → `Validated By` → `offline.db`.

Membership is the 2026-10-14 receipt set (`foreign-provenance-r6.md` §5), still 16 on 2026-10-19; it is row shape, not a 2026-10-20 census.

## Guards

- Do not collapse three silences: native equal-version (`DecisionAlreadyCurrent`), native shadowed-newer repo (channel listing; separate row), foreign (no comparison at all: this row).
- Do not convert this row into "unsafe" evidence; a safety judgment needs its own source and probe. `FOREIGN_INDETERMINATE` blocks a clearance, not mints a finding.
- If a configured repo later supplies the name, foreign status ends; re-derive with `pacman -Qm`/`pacman -Si`, then hand to native rows.

## Limits and tools

No host command run by this seat: no pacman query, `stat`, `journalctl`, sudo, service, snapper, credential, or agent-db read. Sources: repo corpus, retained snapshot, S049, shipped pacman(8); no network. No current foreign count or AUR upstream state claimed; `-m` is cited from the shipped page, not S049 (scope `-Q`/`-u`). Tools installed/updated: **none**.
