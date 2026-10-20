# R18 NoticePackages — package-state-plane.md freshness drafts

Target: `corpus/knowledge/package-state-plane.md` (baseline 842a5312, 337 lines, sha256 e33cf524…; working tree identical).
Capture: `.ufo/waves/round-18/l1-capture/host-capture-r18.txt` (sha256 7e8482c5…; identical at landed 51dd9eea; not present at baseline).

Drafts (no production append):
- `.ufo/waves/round-18/build/drafts/NoticePackages.append.txt`
- `.ufo/waves/round-18/build/drafts/NoticePackages.records.json` (11 records, keys validated)

## Records (all R18-FRESH-NoticePackages-NN, freshness; no corrections)

| ID | Target line | Now (capture) |
|---|---|---|
| 01 | 44 | local DB entries 1188 → 1395 (:25) |
| 02 | 86 | same count, census paragraph (:25) |
| 03 | 75 | sync DBs four → five, incl. openai-chatgpt.db (:53) |
| 04 | 82 | offline.db absent from sync listing (:54) |
| 05 | 90 | local-DB write 2026-10-13 → 2026-10-20 13:23:08 (:41) |
| 06 | 112 | keyring update claim not re-established; filemtime 2026-09-09 ≠ update (:90); last transaction 13:23:09 (:63-65) does not identify a keyring update |
| 07 | 98 | keyring 20260902-1 → 20260909-1 (:28) |
| 08 | 143 | paccache present; pacman-contrib-1.13.1-1 (:83, :36) |
| 09 | 279 | snapper configs root/home present (:80); configuration only, no rollback coverage claimed |
| 10 | 310 | kernel pin 7.2.3 → 7.2.11-arch1-1 (:6) |
| 11 | 49 | elephant 2.21.0-1 → 2.22.1-1 (:30, :72) |

Validation (in-process): every baseline_quote occurs in 842a5312 bytes; every heading absent from baseline and unique; every capture_quote is a substring of its cited line; the `now` and `capture_ref` strings appear in the append text.

## Not refreshed (unmeasured in R18)
207 explicit / 981 derived / 16 foreign counts; pubring and trustdb mtimes; keyring install time; master-key age; sync birth times; cache size 8.6 G; `download-*` dirs; `pacman -Qkk` results.

## Gaps for the planner
- `S060` is not yet a row in `corpus/SOURCES.md` (grep finds none). The notices cite it as instructed; the row must be added before the gate runs.
- Record 06 claims a non-current keyring date only as "not established"; no keyring transaction was measured.
- Line 98's `archlinux-keyring 20260902-1` also needs no further action beyond record 07.

## Tooling
No installs or updates.

Scope: executed=read-only `git show`, `git cat-file -e`, `sha256sum`, `jq` on draft JSON; in-process Python validation and writes limited to `.ufo/waves/round-18/build/drafts/NoticePackages.*`
