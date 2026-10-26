VERDICT: defect-found

Item C2-8 — single-row mutants of the C2 entry `corpus/knowledge/pacman-hook-order-r38.md` against the frozen counter `tools/check-hook-order-r38.py`. 9 of the 10 assigned mutant kinds are KILLED; 1 kind SURVIVES (dropping an S-id from the entry's `source:` line), characterized below. The declared C2 PASS at `1fe28e7` is not falsified — the entry's rows all match and the baseline reproduces PASS; the survivor is a counter-coverage gap, reported per the mutation-tester contract with no contract or counter change made by me.

## Method

- Counter freeze verified: `git show 1fe28e725be47364fc6033bf81ecabc66ee5fe62:tools/check-hook-order-r38.py | sha256sum` = `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8` = `sha256sum tools/check-hook-order-r38.py` (worktree) — matches the declared `60e3635b…`.
- Scratch clone (tasking command): `git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /fast/scratch/hyaku/tsukuroi-r38/C2MutEntry/clone`; `git -C "$D" remote remove origin`; local fixture identity `C2MutEntry (round-38 mutant probe) <c2mutentry@r38-scratch.invalid>`; `git -C "$D" rev-parse --show-toplevel` = `/fast/scratch/hyaku/tsukuroi-r38/C2MutEntry/clone` (observed `TOPLEVEL-OK`). `TMPDIR=/fast/scratch/hyaku/tsukuroi-r38/C2MutEntry` throughout; no `/tmp` path used for anything.
- Base for every mutant: declared C2 commit `1fe28e725be47364fc6033bf81ecabc66ee5fe62` (clone master `reset --hard` to it). Entry, SOURCES.md and the counter are byte-identical between `1fe28e7` and lane tip `5edb6c2` (`git diff --stat 1fe28e7 5edb6c2 -- corpus/knowledge/pacman-hook-order-r38.md corpus/SOURCES.md tools/check-hook-order-r38.py` → empty, exit 0).
- Baseline (no mutation): `python3 tools/check-hook-order-r38.py --repo <clone> --revision 1fe28e7…` → exit 0, `result PASS`, `rows_expected 69`, `rows_matched 69`, `mismatches 0`, `extra_rows 0`, `source_ok 1`, `source_ids [S208,S209,S210,S211,S212]` (receipt `baseline.json`; `baseline.err` 0 bytes). A baseline failure would have made every mutant inconclusive; it passed.
- Per mutant: one edit in the clone, committed on master, counter run `python3 tools/check-hook-order-r38.py --repo <clone> --revision <mutant sha>` (frozen lane counter executed read-only), then `git -C "$D" reset -q --hard 1fe28e7…`.

## Results

Counter fields quoted: exit / result / mismatches / extra_rows / source_ok.

| # | mutant (exact change) | sha (clone master) | counter output | verdict |
|---|---|---|---|---|
| M1 | swap adjacent rows fontconfig/fontconfig-32 — the two table lines exchanged verbatim | `4f5112e310ef8ea5995bd631656324abc4c2beea` | exit 0 PASS, mism 0, extra 0 | EQUIVALENT (Finding 2) |
| M1b | the same swap as a reversed order claim: pos cells exchanged, rows stay in line order — entry now claims `fontconfig-32.hook` at pos 32 and `fontconfig.hook` at pos 33 | `baea5256aee6d30d2cf23664b4f013276ccbc0d4` | exit 1 FAIL, mism 2, extra 2; missing/extra lists are exactly the two swapped rows | KILLED |
| M2 | `dir` etc→usr on `90-mkinitcpio-install.hook` (Post pos 26) | `ed8b6260aa61d8dff87201532eeecc4f76dc8dc1` | exit 1 FAIL, mism 1, extra 1 | KILLED |
| M3 | `needs` yes→no on `10-limine-snapper-lock.hook` (Pre pos 2) | `83a6466f70479d1f6fbe3b8e5a769dc062154a82` | exit 1 FAIL, mism 1, extra 1 | KILLED |
| M4 | `exec` `/usr/bin/locale-gen`→`/usr/sbin/locale-gen` on `10-glibc-locale-gen.hook` (Post pos 1) | `a37dc8ef5e12ab718ca42684390b4e07b293c94e` | exit 1 FAIL, mism 1, extra 1 | KILLED |
| M5 | `pos` 26→27 on `90-mkinitcpio-install.hook` (off by one) | `b1bbf96b9b22fabb36e5860855b74d080aa8d748` | exit 1 FAIL, mism 1, extra 1 | KILLED |
| M6 | duplicated row: `99-limine.hook` (Post pos 28) inserted twice | `4c224928cc2b991b7360867429a151d7deb1c629` | exit 1 FAIL, mism 0, extra_rows 1 (the dup count; `dups == 0` term of the predicate) | KILLED |
| M7 | dropped row: `walker-restart.hook` (Post pos 52) deleted | `8195234d4f5a4c7ada3ba1636fb8681f835c643c` | exit 1 FAIL, mism 1, extra 0 | KILLED |
| M8 | row moved across phases: `10-glibc-remove-locale-archive.hook` PreTransaction→PostTransaction (pos 1 kept) | `13891c9615db1a45fa0cb1957dfd1252ba95115a` | exit 1 FAIL, mism 1, extra 1 | KILLED |
| M9 | `source:` line without S208 (line 1 becomes `source: S209, S210, S211, S212 …`) | `1d66e6ac2f705628551defa18b98c52954777c22` | exit 0 PASS, mism 0, extra 0, source_ok 1, source_ids [S209,S210,S211,S212] | SURVIVED |
| M9b | characterization of the M9 class: `source:` line without S212 instead | `ebce274177996d85d4658b516058318fc99e3b98` | exit 0 PASS, source_ok 1, source_ids [S208,S209,S210,S211] | SURVIVED |
| M10 | S212 status `mined`→`queued` in `corpus/SOURCES.md` (entry untouched) | `34edc9e8946c2b4adc658da3c31bcc593c0092cc` | exit 1 FAIL, mism 0, extra 0, source_ok 0, source_problems `["S212 status queued"]` | KILLED |

Tally over the 10 assigned kinds: **9 killed, 1 survived** (M9 class). The swap kind was run in both encodings (M1 verbatim exchange = equivalent; M1b semantic order-claim reversal = killed). M9b is one extra bounded run of the M9 class to characterize the survivor's scope.

## Finding 1 (defect): the counter cannot detect the entry dropping a cited source

- `source_check` (tools/check-hook-order-r38.py:157-178) takes the S-ids from the entry's first `source:` line (:158-159) and validates only the ids still present: each must be a `corpus/SOURCES.md` row with status `mined` (:173-174), used-by naming the entry path (:175-176), and at least one cited row opened 2026-10-26 (:177-178). It never requires the full declared set S208-S212 and never cross-checks which S-ids the HO-rule rows cite.
- All five rows satisfy those checks at `1fe28e7` (`corpus/SOURCES.md:217-221`; each ends `… | mined | 2026-10-26 | … | corpus/knowledge/pacman-hook-order-r38.md |`), so removing any one id leaves `source_ok=1`: observed for S208 (M9) and for S212 (M9b), both PASS exit 0.
- Impact: the entry could silently stop citing S208 — `lib/libalpm/hook.c` at pacman `54d9411`, the source behind HO1-HO5 and HO7 (`corpus/knowledge/pacman-hook-order-r38.md:1` source line; rules table :17-27) — and the frozen counter would still PASS. The same holds for any other single id, including S212, the capture source that grounds every expected row.
- Scope: this is a counter-coverage gap, not evidence against the declared C2 claim — the true entry at `1fe28e7` cites all five ids and the baseline reproduces PASS. Per the mutation-tester contract I changed nothing: no counter edit, no lane edit, and a surviving mutant is not permission to change the contract.
- Proposed tightening (draft, for the planner to accept or reject): in `source_check`, require the id set to equal a pinned expected set, e.g. add to the counter `EXPECTED_SIDS = {'S208','S209','S210','S211','S212'}` and append a problem when `set(ids) != EXPECTED_SIDS`; a weaker variant requires every S-id cited in the entry's HO-rule table (:21-27) to also appear on the `source:` line. With either, M9/M9b flip to FAIL (`source_problems ["S208 absent"]` / `["S212 absent"]`).

## Finding 2 (equivalent mutant, documented so it is not misread as a survivor)

Exchanging two adjacent table lines verbatim (M1) is invisible to the counter by construction: `entry_rows` (tools/check-hook-order-r38.py:141-154) parses the section's table into 7-cell tuples and `main` compares them as sets with the explicit `pos` cell (:199-203), so line order inside the table carries no claim — the order claim lives in the `pos` column. The semantic encoding of the same swap (M1b) is killed. No counter change proposed.

## Restoration evidence

- After the final `git reset --hard 1fe28e7…`: clone HEAD = `1fe28e725be47364fc6033bf81ecabc66ee5fe62`; `git rev-parse HEAD:corpus/knowledge/pacman-hook-order-r38.md` = `bd061ab7d8cbc9f1772e0bbd0e0df61399410c4d` and `HEAD:corpus/SOURCES.md` = `a2e3ac1deb6bf2567a770ea07ef2170650f4a5b5` — identical to `git -C <lane> rev-parse '1fe28e7:<path>'` for both files (outputs observed in-session). Clone `status --porcelain` = 0 lines.
- Lane untouched: HEAD `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf` before and after; `git status --porcelain` = 9 lines before and after, all untracked `.ufo/waves/round-38/*` wave artifacts (observed list: `after/`, `assimilation/`, `l1/`, `make-w1-spec.py`, `w1-dispatch.err`, `w1-dispatch.json`, `w1-spec.json`, `w1.ready`, `w1/` — my receipts dir lives under `w1/` per tasking). No tracked lane file edited; no git/jj mutating command run in the lane; no host mutation; no sudo; no pacman transaction; no service touched.
- Scratch `/fast/scratch/hyaku/tsukuroi-r38/C2MutEntry` removed after receipts were copied (observed `SCRATCH-REMOVED`).

## Receipts

All under `.ufo/waves/round-38/w1/C2MutEntry/`: `baseline.json`, `baseline.err` (0 bytes), and per mutant `m1.diff`/`m1.json`, `m1b.diff`/`m1b.json`, `m2.diff`/`m2.json` … `m10.diff`/`m10.json`, `m9b.diff`/`m9b.json` — each `.diff` is the mutant's `git show --format=` body, each `.json` the full counter record.

## Not done / bounds

- I did not judge HO1-HO7 truth against the pinned sources (that is seats C2RevHookC / C2RevOtherSrc / C2CritHO5 / C2CritHO6 / C2RevenConf per the amendment); I ran no live pacman, no journal reads, and no capture re-verification beyond the counter's own MANIFEST pin, which the baseline exercised.
- Mutants are single-row/single-cell only, as assigned; no multi-row, no capture-file, no counter-code mutants were built.
- Tooling: nothing installed or upgraded (operator rule 2026-10-19) — python3 and git were sufficient; no pacman, no uv, no binary installs.
