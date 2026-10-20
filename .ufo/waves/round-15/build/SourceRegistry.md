# SourceRegistry — round 15

## Changed file
`corpus/SOURCES.md` only: appended S046–S049 after S045 plus two bounded `## Search log` paragraphs. Append-only; S041, S044, S048 and S010 unchanged.

## Rows landed (docs, tier A, mined, opened 2026-10-20)
- **S046** https://man.archlinux.org/man/systemd.exec.5 — SANDBOXING >
  ProtectSystem= first definition, by heading, no rendered lines; systemd 262.1
  footer, core/systemd 262.1-1. Quote, 11 words: “Takes a boolean argument or
  the special values "full" or "strict".”. Domain only; supplements S041/S044.
  used-by `corpus/knowledge/source-locator-clarification-r15.md`.
- **S047** https://wiki.archlinux.org/title/System_maintenance — § Partial
  upgrades are unsupported; oldid 885170, last edited 2026-09-07T06:06:18Z.
  Quote, 8 words: “That is why partial upgrades are not supported.” Anchor
  records the do-not list (`pacman -Sy package`; `pacman -Sy` then `pacman -S
  package`). Doctrine only, not installed-state consistency.
  used-by `corpus/knowledge/partial-upgrade-recheck-r15.md`.
- **S048** https://man.archlinux.org/man/pacman.8 — TRANSACTION OPTIONS
  (APPLY TO -S, -R AND -U), `-p, --print` / `--print-format`; Pacman 7.1.0
  footer 2026-10-15. Quote, 14 words: “Only print the targets instead of
  performing the actual operation (sync, remove or upgrade).”. No host-result
  or sync-freshness claim. used-by `corpus/knowledge/partial-upgrade-recheck-r15.md`.
- **S049** same pacman.8 URL — OPERATIONS > `-Q, --query`; QUERY OPTIONS
  (APPLY TO -Q) > `-u, --upgrades`; TRANSACTION OPTIONS > `--needed`; same
  footer. Quotes: 4 words “Query the package database.”; 14 words “Only
  package versions are used to find outdated packages; replacements are not
  checked here.”; 9 words “Do not reinstall the targets that are already
  up-to-date.”. Version-only filter excludes replacements; `--needed` skips
  same-version targets and is not a no-upgrade result. used-by C2 MD.

## Retained fetch evidence (HTTP 200, 2026-10-20, curl -L)
- systemd.exec.5: sha256 `26f9a1827179b42f534271e5109cd97517eee8e7cfb3579ada8e19b1f5d25043`, 293394 bytes.
- System_maintenance: sha256 `e34c3ae844ab3b88f6c24a31fcdba5343e818632e29af3d655501b3c2092a525`, 86175 bytes; raw wikitext `746637cf8a17c4e3fafb944bf5d23d01efc42297d1703173761d48cf763075c5`, 19152 bytes; revid 885170 at 2026-09-07T06:06:18Z.
- pacman.8: sha256 `531ebf4868faf7674a24ba0d9e4bb8af9ab99511ba86a5df87645ce0403fd495`, 41121 bytes, re-fetched byte-identical for the S049 sections.
All quotes were located in fetched bytes; counts are whitespace tokens. In
total 4 candidates screened, 4 included, 0 newly rejected.

## Histogram (measured over the edited file)
| Measure | Before | After |
|---|---|---|
| Rows | 45 | 49 |
| Tier A/B/C | 37/1/7 | 41/1/7 |
| mined/queued/rejected | 32/5/8 | 36/5/8 |
| Malformed rows (cells != 11) | 0 | 0 |

## Limits and recommendations
- The two used-by targets did not exist at write time (sibling-owned); an
  E11-style existence check fails until they land. Do not edit rows to mask it.
- Reused systemd.exec, System_maintenance and pacman.8 URLs are
  scope-separated: W04 warnings are expected, not failures. S049 adds one
  pacman.8 reuse beyond S048.
- S047 was opened unpinned and served revid 885170; the row pins the revision
  in its anchor. A future pinned URL must be a new row, not a rewrite.
- R15-LOCATOR should cite the stable heading and footer, never bare reader
  lines. R15-POSITIVE-DOMAIN should use the positive sentence above and make
  no exhaustive-absence claim.
- C2: use S049 only for documented query/`--needed` semantics; neither row
  proves replacements were absent or that a preview reflects current sync data.
- No package, service or host-state command ran; source bodies were data and no embedded instruction was executed. Tools installed/updated: **none**. No verification/test/lint was run by this seat.
