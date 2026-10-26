VERDICT: defect-found

Seat C2CritSourced, item C2-15 — attack the sourced-claim requirement (round prompt §2b item 4; `CORPUS.md` SOURCES rule 1). Read-only on the lane: no lane file was modified, no git/jj state touched, no package/hook/service/sysfs/`/etc` change, no `sudo`, no pacman transaction, no registry edit. Writes: this report and `w1/C2CritSourced/` (`receipts.txt`, `quotes.txt`). Scratch `/fast/scratch/hyaku/tsukuroi-r38/C2CritSourced/` removed after receipts were copied.

Result in one line: the sourced-claim requirement is met structurally — `corpus/knowledge/pacman-hook-order-r38.md:1` names `S208, S209, S210, S211, S212`, all five rows are `mined` with `used-by` pointing at that entry, and the after receipt records `source_ok: 1` (`.ufo/waves/round-38/after/c2-after-1fe28e7.json`) — but the rows' recorded URLs are **not** the URLs opened this round, the snapshots match only the `/raw/` form, one own-work row's `teaches` clause is contradicted by its own capture header, and the entry cannot be admitted under QUALITY 14 because it carries no `## QUALITY check`. All four are fixable; none falsifies the hook-order content.

## 1. Are the URLs S208-S211 the opened ones? No — viewer form recorded, `/raw/` form opened

The four registry rows record the GitLab **blob viewer** URL:

- `corpus/SOURCES.md:217` — `https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/hook.c`
- `corpus/SOURCES.md:218` — `.../-/blob/54d9411/doc/alpm-hooks.5.asciidoc`
- `corpus/SOURCES.md:219` — `.../-/blob/54d9411/lib/libalpm/trans.c`
- `corpus/SOURCES.md:220` — `.../-/blob/54d9411/lib/libalpm/alpm.c`

Every recorded fetch this round used the **raw** endpoint:

- `.ufo/waves/round-38/sources/SHA256SUMS:1` — `# fetched 2026-10-26T04:20:21Z from https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/<path>`
- `w1/C2RevHookC.md:7` — `URL: https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/hook.c — accessed 2026-10-26`
- `w1/C2RevOtherSrc.md:4` — re-fetch 04:41-04:57Z against the same `/raw/` digests.

A whole-round grep (`grep -rn "blob/54d9411" .ufo/waves/round-38/ corpus/`) returns the four registry rows, a mutant diff that copies them (`w1/C2MutEntry/m10.diff:6-8`), the C2-15 prompt/dispatch text, and one mention in `w1/C2RevO2Rows.md:30` that quotes the URL rather than opening it. No seat report or receipt records opening the blob URL.

The two endpoints do not serve the same bytes. Re-fetched today (2026-10-26, receipt 05:10:23Z, `receipts.txt`):

| path | `/raw/54d9411/...` | row URL `/-/blob/54d9411/...` |
|---|---|---|
| `lib/libalpm/hook.c` | HTTP 200, sha256 `99f1044b…b199a` (= row anchor) | HTTP 200 `text/html`, 43,313 B, sha256 `b44f3a5c…` |
| `doc/alpm-hooks.5.asciidoc` | HTTP 200, sha256 `2970cb35…493d3` (= row anchor) | HTTP 200 `text/html`, 43,499 B, sha256 `e4139d64…` |
| `lib/libalpm/trans.c` | HTTP 200, sha256 `637c1165…ed07` (= row anchor) | HTTP 200 `text/html`, 43,327 B, sha256 `8a9a21a5…` |
| `lib/libalpm/alpm.c` | HTTP 200, sha256 `8bbb0a3c…834a` (= row anchor) | HTTP 200 `text/html`, 43,313 B, sha256 `e5fb1943…` |

The viewer page is a shell, not the file: `<title>lib/libalpm/hook.c · 54d9411 · Pacman / Pacman · GitLab</title>`, `data-page="projects:blob:show"`, and `grep -c '_alpm_hook_cmp' blob-hook.c` = 0. So a reader who opens the row's URL and runs `sha256sum` against the row's own anchor gets a **mismatch**, and cannot recover the quoted source text without following a further link.

This is not a lane convention, it is the lane's only exception. `grep -c -- '-/blob/' corpus/SOURCES.md` = 4, and all four are S208-S211 (`corpus/SOURCES.md:217-220`). Every other GitLab row at the same commit uses `/raw/`: S099 (`:105`), S191 (`:197`, full commit `54d94116164b…`), S192 (`:198`), S194 (`:200`), S195 (`:201`), S196 (`:202`). Prior review gap: `w1/C2RevO2Rows.md` (§2, §3) pronounced S208-S212 "conformant" and quoted the `/raw/` fetch header while accepting the `/blob/` row URL; it did not compare the two. The finding above is new relative to that seat.

## 2. Do the snapshots match "those URLs" today?

- Against the **opened** (`/raw/`) URLs: yes, exactly. All four re-fetches today are byte-identical to `.ufo/waves/round-38/sources/SHA256SUMS:2-5` and to every row anchor (table above). The 54d9411 pin resolves and the snapshot set is sound.
- Against the **recorded** (`/blob/`) URLs: no. Those return a 43 KB HTML viewer with a different digest (table above). The snapshots do not match the registry URL form.

Consequence for the Gate: rule 1 requires the Gate to record "the URL ... for every new row". Recording the blob URL would record a URL that was not opened and that does not reproduce the digest. The Gate rows proposed in §5 therefore carry the `/raw/` URL with the viewer form named once in the Gate note.

## 3. Is S212 legitimately tier A for its scope?

Scope (`corpus/SOURCES.md:221`): "The 70 hook files present on this host in both hook directories at capture time". Tier A is "primary or authoritative for that scope ... the lane's own re-runnable gate output" (`/home/vgpnk/Projects/shokunin/CORPUS.md`, SOURCES shape); own-work captures are A-tier precedent in this very registry (S031, S032, S040, S051-S056, S066-S069).

Verified today (all output in `w1/C2CritSourced/receipts.txt`):

- `sha256sum -c MANIFEST.sha256` → exit 0, 70 lines, no failure.
- Counts with a command: `grep -c '  usr-share-libalpm-hooks/' MANIFEST.sha256` = 67; `grep -c '  etc-pacman.d-hooks/'` = 3; `wc -l` = 70.
- One same-name pair: `LC_ALL=C comm -12` of the two name lists = `90-mkinitcpio-install.hook` only.
- Capture faithful to the host today: `diff` of the manifest digests against `sha256sum *.hook` in `/usr/share/libalpm/hooks` and `/etc/pacman.d/hooks` is empty for both (67/67 and 3/3); the capture is not a stale or partial copy.
- Anchor digest: `sha256sum MANIFEST.sha256` = `da07f43461fe41794419eb0da8ec88bd832c242abb2972e267df90d1ddd701dd`, equal to the row's anchor cell.

Verdict: **tier A is legitimate for the capture-time scope**, and only for that scope. Three corrections are needed in the Gate/row wording:

1. `teaches` says "read without running pacman" (`corpus/SOURCES.md:221`), but the capture header records a pacman invocation: `capture-meta.txt:2` — `$ pacman -Q pacman`. The true statement is narrower: the hook inventory was read from the two directories, while the header also records one read-only `pacman -Q pacman` version query (and `pacman-conf` at `:4`, `:6`). QUALITY 26 (R17-STEER-SCOPE) is the criterion that governs how a capture header records such an invocation; the clause as written is falsified by the row's own anchor file.
2. The counts 67/3/70 in `teaches` carry no command, contrary to the fleet corpus rule "A count carries its command" (`/home/vgpnk/Projects/shokunin/CORPUS.md`, "Rules added from the round-1/2 corpus audits"). The Gate row below supplies the commands.
3. `capture-meta.txt:6` ends with `$ pacman-conf --verbose 2>/dev/null | grep -i hookdir` and no output; the record does not show whether that command printed anything. The effective HookDir is still evidenced at `:4-5` (`/etc/pacman.d/hooks/`), so the row's scope is not harmed, but the capture tail is incomplete as a record.

## 4. Gate-admission blockers found while checking the sourced-claim chain

These are in scope because §2b item 4 lands through the lesson's `## Gate`, and the Gate cannot admit what the lane's own bar rejects:

1. **No `## QUALITY check` in the entry.** `grep -c "QUALITY" corpus/knowledge/pacman-hook-order-r38.md` = 0, and its headings are `## Rules` (`:17`), `## Effective hook order` (`:29`), `## Observed / inferred / unknown` (`:103`). QUALITY 14 (`corpus/QUALITY.md:19`) requires "its explicit `## QUALITY check`" before an admit; round-37 entries carry one (`corpus/knowledge/mount-errno-contract-r37.md:36-40`, `corpus/knowledge/errno-contract-variance-r37.md:35-40`) and round-37 rejected a candidate for exactly this omission (`corpus/lessons/round-37.md:22`). The C2 after receipt's `source_ok: 1` does not test this: the counter's `source_ok` only checks row status/used-by/opened date (`.ufo/waves/round-38/after/c2-after-1fe28e7.json`; `tools/check-hook-order-r38.py` docstring).
2. **The committed non-author per-row verdicts are split, and the Gate must reconcile them, not average them.** QUALITY 81 requires a committed non-author verdict per row. Recorded: `HO5: holds` in `w1/C2RevHookC.md:66`, `w1/C2RevOtherSrc.md:111`, `w1/C2RevenConf.md:175`, but `HO5: partly` in `w1/C2CritHO5.md:188` (the parenthetical at `hook.c:119-123` and the "one path" consequence at `hook.c:554-562` "are false as written"); `HO6: holds` in `w1/C2RevOtherSrc.md:112` and `w1/C2RevenConf.md:176` (C2RevHookC judged HO1-HO5 and HO7 at `w1/C2RevHookC.md:62-67`, with no HO6 line), but `HO6: partly` in `w1/C2CritHO6.md:203`. `w1/C2RevenConf.md:145` additionally proposes replacement wording for HO2's first sentence. A Gate that says "all rows hold" would be false against the delivered reports; a Gate that admits without naming the split would hide it.
3. **The lesson file does not exist.** `ls corpus/lessons/round-38.md` → `No such file or directory`. The Gate rows below are the proposal that must land there, in the round-37 table shape.

## 5. Proposed exact Gate rows (each quote verified verbatim in the frozen snapshot)

Gate note to precede the table:

> The four upstream rows were opened through the GitLab **raw** endpoint, which is the form the frozen snapshots and the pinned digests belong to. The registry `source` cells for S208-S211 carry the GitLab viewer form `/-/blob/54d9411/...`; opened today (2026-10-26) that form returns `text/html` (about 43 KB, `data-page="projects:blob:show"`) and does not reproduce the anchor sha256. Registry `source` is a canonical viewer link; the Gate and every re-opener must use `/raw/54d9411/...` (precedent: S099, `corpus/SOURCES.md:105`). No registry cell was edited by this seat.

| Row | Source URL/path and opened date | Located quote (≤25 words) | Location | Decision |
|---|---|---|---|---|
| S208 | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/hook.c — opened 2026-10-26 (fetched 04:20:21Z per `sources/SHA256SUMS:1`; re-fetched 2026-10-26, digest `99f1044b…b199a` equal) | “/* exclude the suffixes from comparison */” and “return l1 < l2 ? -1 : 1;” (7 and 8 words) | `_alpm_hook_cmp`, `hook.c:449` and `hook.c:452`, commit 54d9411 (`:588-590` covers "first file seen wins") | admit, mined, tier A |
| S209 | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/alpm-hooks.5.asciidoc — opened 2026-10-26 (digest `2970cb35…493d3` equal) | “Hooks are run in alphabetical order of their file name, where the ordering ignores the suffix.” (16 words) and “Causes the transaction to be aborted if the hook exits non-zero. Only applies to PreTransaction hooks.” (16 words) | `DESCRIPTION`, `alpm-hooks.5.asciidoc:38-39`; `*AbortOnFail*`, `:88-89` (key `:87`), commit 54d9411 | admit, mined, tier A |
| S210 | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/trans.c — opened 2026-10-26 (digest `637c1165…ed07` equal) | “RET_ERR(handle, ALPM_ERR_TRANS_HOOK_FAILED, -1);” (3), “alpm_logaction(handle, ALPM_CALLER_PREFIX, "transaction completed\n");” (4), “_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION);” (2) | `_alpm_trans_commit`, `trans.c:203`, `:235`, `:238`, commit 54d9411 | admit, mined, tier A |
| S211 | https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/alpm.c — opened 2026-10-26 (digest `8bbb0a3c…834a` equal) | “myhandle->hookdirs = alpm_list_add(NULL, hookdir);” (4 words) | `alpm_initialize`, `alpm.c:62`, commit 54d9411 — quote grounds the **list-head placement only**; "HookDir entries searched first override it" is S007's documented precedence, not this row | admit, mined, tier A |
| S212 | `.ufo/waves/round-38/frozen/hooks-capture/` (own-work) — opened 2026-10-26 (captured 04:11:58Z) | “# captured 2026-10-26T04:11:58Z host=plazir27 read-only” (5 words) | `capture-meta.txt:1`; counts `grep -c '  usr-share-libalpm-hooks/' MANIFEST.sha256` = 67, `grep -c '  etc-pacman.d-hooks/'` = 3, `wc -l` = 70; MANIFEST sha256 `da07f434…01dd` | admit, mined, tier A, own-work — scope is the hook set read from the two directories; the header also records `pacman -Q pacman` (`:2`) and `pacman-conf` (`:4`, `:6`), so "read without running pacman" in the row's `teaches` overstates and should be narrowed by erratum |

Every quote above was checked whitespace-normalized against the frozen snapshot (`w1/C2CritSourced/quotes.txt`, all `verbatim=True`; word counts 2-16, all ≤25). The S212 quote is `capture-meta.txt:1` in the frozen capture directory.

## 6. Smallest safe correction (ordered)

1. Gate: land the five rows above with the `/raw/` URLs and the viewer/raw note. This satisfies rule 1 without touching a registry cell (append-only preserved).
2. Entry: add a `## QUALITY check` section to `corpus/knowledge/pacman-hook-order-r38.md` evaluating at least QUALITY 1-3, 7, 14, 81 and the depth criteria 80/82 that the declaration invokes; the Gate admits only after that section exists and resolves its pointers.
3. Gate: record the HO5/HO6 verdict split by seat and the adjudication (or wording change) the L1 adopts; do not write "all rows hold" while `w1/C2CritHO5.md:188` and `w1/C2CritHO6.md:203` say "partly".
4. Erratum in the round-38 lesson (append-only, not an in-place row edit): S212's `teaches` clause "read without running pacman" is narrowed to "the hook set was read from the two directories; the header records one read-only `pacman -Q pacman` query"; add the count commands. Same for S211: its quote grounds list-head placement; the override direction is S007.
5. If the lane wants the registry rows themselves to be digest-reproducible, append correction rows per contract rule 2 — optional and disproportionate for four rows; the Gate note already supplies the reproducible URL.

## 7. What I did not do

- Did not run the lane census (`scripts/sources-census.sh`); only `w1/C2RevO2Rows.md` §1 is cited for its exit-0 result.
- Did not adjudicate HO1-HO7 against the source; that is the assigned per-row seats' judgment and the canonical judge's call. I only recorded that the committed verdicts disagree.
- Did not run pacman or pacman-conf, and did not modify any registry row, entry, counter, capture or host file.
- Did not check the installed pacman binary's behaviour; no boot, hook or transaction was run.

## 8. Impacted axes

- **C2 (sourced depth):** source bytes and digests are sound; the registry locator form is not reproducible (`/-/blob/` returns HTML), and the entry lacks its QUALITY 14 check.
- **QUALITY 7** (exact row, tier, anchor): S211's `teaches` overreaches its cited line; S208-S211 anchors are otherwise exact.
- **QUALITY 14** (performed, not promised, check): missing from the entry.
- **QUALITY 81** (per-row non-author verdict): delivered but split; Gate must reconcile.
- **CORPUS SOURCES rule 1** (URL/access date/located quote per new row): the Gate rows above supply all three in the opened URL form.
