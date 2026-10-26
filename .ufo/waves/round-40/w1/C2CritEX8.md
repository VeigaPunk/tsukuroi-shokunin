VERDICT: defect-found

Item C2-21, seat C2CritEX8. Lane tip at start and end of review: `f951f288483c1af0cef4afd458488b84cf7a2165` (`git -C . rev-parse HEAD`, read-only). Read-only on lane content: no lane file edited, no git/jj mutation in the lane; every fixture lives in `/fast/scratch/hyaku/tsukuroi-r40/C2CritEX8/` and is removed at the end.

## What is confirmed (the claim's mechanism holds)

**Q1 — how a NoUpgrade file becomes `.pacnew`.** `add.c` at 54d9411, fetched fresh (`curl -sS https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/add.c`, sha256 `fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1`, 695 lines — byte-identical to the S191 snapshot `.ufo/waves/round-35/w1/SrcAddC/add.c`, same digest):

- `add.c:205-210` — an archive entry whose name is absent from `newpkg->files` is skipped, so everything pacman extracts is named by the package file list.
- `add.c:227-233` — NoExtract returns before any backup logic: a NoExtract path produces no `.pacnew` at all.
- `add.c:302-304` — `/* if file is in NoUpgrade, don't touch it */` → `notouch = 1`, in the file-over-file branch only (so a path that does not yet exist is extracted normally).
- `add.c:317-324` — `if(notouch || needbackup)` appends `".pacnew"` to the destination `filename` (root + entry name) and extracts there.
- `add.c:338-350` — `notouch` branch: event `from_noupgrade = 1`, then `filename[filename_len] = '\0'` strips the suffix and `add.c:350` logs `"warning: %s installed as %s.pacnew\n"`. The old file is left in place.
- `add.c:351-408` — backup file with local changes (all three MD5s differ, `add.c:390-404`): the unpacked file stays as `.pacnew`, event `from_noupgrade = 0`. Same on-disk outcome, same matched name.

**Q2 — the trigger match uses the package file-list name and never the `.pacnew` name.** `hook.c` frozen copy (sha256 `99f1044b…`, matches `SHA256SUMS`): the three collection loops read `pkg->files` and pass `filelist.files[f].name` to `_alpm_fnmatch_patterns` — `hook.c:268` + `:274` (install), `:286` + `:289` (upgrade-removal from `spkg->oldpkg->files`), `:300` + `:303` (removal). `grep -ci pacnew hook.c` = **0**; `grep -ci backup hook.c` = **0**. Upstream documents exactly this at `alpm-hooks.5.asciidoc:126-127`: “When installing or upgrading a file that is extracted with a '.pacnew' extension, the original file name is used in triggering the hook.”

**Q3 — NoUpgrade is not consulted anywhere in `hook.c`.** `grep -ci noupgrade hook.c` = **0**. The complete set of handle fields `hook.c` touches is `handle->trans` (×6), `handle->db_local`, `handle->hookdirs` (`grep -o 'handle->[a-z_]*' hook.c | sort | uniq -c`); the only option lookup is `alpm_option_match_noextract` at `hook.c:271`. So NoUpgrade cannot enter the match, on any side.

**Q4 — on upgrade, a path in both old and new packages is an `upgrade` match.** `hook.c:310-311` sorts both lists; `hook.c:312-337` walks them and for every path present in both does `upgrade = alpm_list_add(upgrade, path)` (`:321`), then **removes** that path from `install` (`:324`) and from `remove` (`:328-333`). The operation test is `hook.c:339-341`. Consequence, which the item asks for explicitly: an `Operation = Install` trigger does **not** fire for an upgraded NoUpgrade `.pacnew` whose path the old package owned; `Operation = Upgrade` fires. An `Install` trigger fires only when the path exists on disk but sits outside the old package's file list (unowned file), where `oldpkg->files` yields no `remove` entry and the path stays in `install`.

## The defect

EX8's rule cell (`corpus/knowledge/pacman-exec-environment-r40.md:28`) reads:

> … on the install side a path that NoExtract excludes is skipped, and matching ignores NoUpgrade, so a protected file that pacman writes as `.pacnew` still matches under its listed name

Each clause is literally true, but the operation is unstated, and the only operation named in the sentence is *install* — the one operation that does not fire in the ordinary upgrade case. The same row's counterfactual cell then says the hook “fires on an upgrade that leaves `<file>.pacnew`”. Prose says install side, counterfactual says upgrade, and the code says the two are mutually exclusive per path (`hook.c:324` removes the path from `install`). A hook author writing `Operation = Install` from the prose gets a hook that never runs on the upgrade it was written for. That is a fixable precision defect, not a tradeoff.

Second, narrower defect: the sentence's decisive authorities are outside the citation cell. The cell cites `S223 hook.c:258-279` and `S224 alpm-hooks.5.asciidoc:61-67`; the install/upgrade split that decides the operation lives at `hook.c:310-337` and `:339-341`, and the documented `.pacnew`-name rule lives at `alpm-hooks.5.asciidoc:121-129`, both uncited.

## Counter depth (C2 axis): the frozen counter cannot see either defect

`tools/check-exec-environment-r40.py:178-179` derives EX8 as `'NoExtract'` from two facts only — the `alpm_option_match_noextract(...)` string inside `_alpm_hook_trigger_match_file`, and `'noupgrade' not in hook.c.lower()` — and `:93` requires the rule cell to carry the tokens `file list, NoExtract, NoUpgrade, .pacnew`. Nothing checks the operation split or the matched-name identity. Measured on a scratch clone (`fixture.log`, receipts `counter-*.json`):

| revision | EX8 rule cell | counter |
|---|---|---|
| `f951f28…` (declared) | as shipped | **PASS** |
| `050f808…` | rule cell corrected only | **PASS** |
| `ced996e…` | rule + source + host cells corrected (set 1–3) | **PASS** |
| `8a596d8…` | deliberately wrong: “still matches under its listed name as an install trigger” | **PASS** |
| `5933b64…` | deliberately wrong: “matches under the `.pacnew` name” | **PASS** |

Both wrong cells — one misattributing the operation, one contradicting the very fact this item verifies — survive. Adding one token fixes it: with `TOKENS['EX8'] = ['file list', 'NoExtract', 'NoUpgrade', '.pacnew', 'upgrade']`, the declared text **FAILs** (`rule lacks tokens: upgrade`) and both corrected texts **PASS** (`counter-T1-token-*.json`).

## Smallest safe correction

**(1) Rule cell** — replace the EX8 rule text with (keeps all four tokens, no negation word, 71 words, verified PASS at `050f808…` and `ced996e…`):

> A `Path` trigger matches file paths as the package's file list names them, relative to the installation root; a path that NoExtract excludes is skipped on the install side, and matching ignores NoUpgrade, so a protected file that pacman writes as `.pacnew` still matches under its listed name: an `upgrade` match when the replaced path sits in the old package's file list, an `install` match when that path sits outside it

**(2) Source cell** — append the two uncited anchors:

> … (`alpm_option_match_noextract` :271; upgrade and removal sides :281-306; the install/upgrade split :310-337, `upgrade = alpm_list_add(upgrade, path)` :321 and `install = alpm_list_remove_item(install, i)` :324; operation test :339-341); target semantics in S224 alpm-hooks.5.asciidoc:61-67, and the `.pacnew` caveat at S224 alpm-hooks.5.asciidoc:121-129

**(3) Host cell** — append: “an `Operation = Install` trigger fires only when the old package lacks the path”.

**(4) SOURCES S224** — extend its line list from `61-67, 83-85, 91-93` to `61-67, 83-85, 91-93, 121-129`, so the citation in (2) stays inside the row's declared scope.

**(5) Counter** — `TOKENS['EX8'] += 'upgrade'` (`tools/check-exec-environment-r40.py:93`). Measured effect above; it is the only cheap check that rejects the shipped wording and both wrong variants.

## Provenance gap the L1 has to decide (not fixable by a seat)

The `.pacnew` half of EX8 is not backed by any source this entry cites. `S195` is pacman.conf(5) (`corpus/SOURCES.md:201`, scope “`NoUpgrade` … not evidence of host state”), not add.c — the assignment's wording attributes the backup-file-with-local-changes mechanism to S195, which it does not carry; the code row is `S191` (add.c, sha256 `fd313629…`, my fetch matches it) and `S213`. But `.ufo/waves/round-40/frozen/src/` holds no `add.c` (`ls`, `SHA256SUMS`), the doc's `source:` line lists only `S219–S225` (`pacman-exec-environment-r40.md:1`), and the counter's `source_ok` rule (`:258-261`, `:295`) requires every cited S-id to be on that line, mined, and to name this entry in `used_by`; `awk -F'|'` over `corpus/SOURCES.md` shows `S191 used_by: pacman-backup-files-r35.md, tools/score-pacnew-arm-r35b.py, tools/tsukuroi-census.sh` and `S213 used_by: pacman-transaction-order-r39.md`. Citing either today turns the counter red. So the choice is: (a) accept the man-page CAVEATS as the documentation authority and apply (1)–(5), or (b) add add.c to the round-40 frozen set with a row naming this entry. I recommend (a) for this round — it is one documentation edit plus one row-scope edit, and the CAVEATS sentence states the matched-name rule more directly than the code does.

## Not done / not claimed

- I did not run a real pacman transaction to observe a `.pacnew` hook fire (host is frozen; pacman transactions paused host-wide). The mechanism is established from source and the upstream manual, not from a live trace.
- `[INFERENCE]` The `install`-match case for an unowned pre-existing NoUpgrade file follows from `add.c:243-250` (`isnewfile` false) plus `hook.c:281-295` yielding no `remove` entry; I did not reproduce it against a package database.
- I did not touch `tools/tsukuroi-census.sh`, `probe_storage_arm`, or any C1 material; no tool installs were needed for this item.
