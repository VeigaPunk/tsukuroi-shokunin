VERDICT: defect-found

Seat AsmS201Man, item A-1 (assimilation re-ground, theme pacman hook timing). Read-only on the lane; the only writes are this report and `w1/AsmS201Man/`.

Short result: all five S201 claims are present verbatim, so the staged entry is **supported on content**. The audit found four defects in the staging and in the entry, none of which falsifies a claim:

- **ID collision:** all four staged IDs are already taken in the lane.
- **Section anchor:** the staged S201 row's anchor omits the section that holds the ordering claim.
- **Overreach:** one sentence in the entry says more than the cited sources say.
- **"Non-overlapping" wording:** the row's "non-overlapping complement" wording is true against S008 but false against the lane's own round-38 rows S209 and S210.

## 1. Re-open of staged S201 — https://man.archlinux.org/man/alpm-hooks.5

Access date **2026-10-26** (UTC 05:04). Page header, verified on the fetched page:

- `.TH "ALPM\-HOOKS" "5" "2026\-10\-15" "Pacman 7\&.1\&.0"` (`w1/AsmS201Man/alpm-hooks.5.raw:10`).
- HTML footer: `foot-date 2026-10-15`, `foot-os Pacman 7.1.0`, package `Version: 7.1.0.r9.g54d9411-3` (`alpm-hooks.5.html` lines 208, 209, 233).
- Staged-row metadata (man date 2026-10-15, Pacman 7.1.0, package 7.1.0.r9.g54d9411-3) therefore matches today's page exactly.

Fetch notes, for honesty:

- The first `curl` returned a TLS EOF (exit 35, `curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading`). The `read` tool on the URL failed with ECONNRESET.
- `curl --http1.1 -A Mozilla/5.0` then succeeded for `.../alpm-hooks.5` (HTTP 200, 13365 B), `.../alpm-hooks.5.en` (HTTP 200, 13371 B) and `.../alpm-hooks.5.en.raw` (HTTP 200, 7680 B).
- The quotes below come from the `.5.en.raw` roff. Raw-roff line numbers are `alpm-hooks.5.raw:N`. Receipts and `SHA256SUMS` are in `w1/AsmS201Man/`.

Section order on the page (TOC, `alpm-hooks.5.html`): NAME, SYNOPSIS, DESCRIPTION, TRIGGERS, ACTIONS, OVERRIDING HOOKS, EXAMPLES, CAVEATS, BUGS, AUTHORS.

| # | Claim the staged entry attributes to S201 (`pacman-hook-timing-r25.md`) | Present? | Verbatim quote, section, raw line |
|---|---|---|---|
| 1a | Hooks run in alphabetical order of file name, ignoring the suffix (entry :22-23) | **present** | **DESCRIPTION**, raw:52: "Hooks are run in alphabetical order of their file name, where the ordering ignores the suffix." |
| 1b | Hooks live in `/usr/share/libalpm/hooks` plus a `HookDir`, default `/etc/pacman.d/hooks` (entry :16, row teaches) | **present** | **DESCRIPTION**, raw:52: "Hooks are read from files located in the system hook directory /usr/share/libalpm/hooks, and additional custom directories specified in pacman.conf(5) (the default is /etc/pacman.d/hooks)." |
| 1c | `When=PreTransaction\|PostTransaction` required (entry :16, row teaches) | **present** | **ACTIONS**, raw:89-91: "When = PreTransaction\|PostTransaction / When to run the hook. Required." Also SYNOPSIS raw:42. |
| 2 | `AbortOnFail` aborts on non-zero exit and is PreTransaction only (entry :41-42) | **present** | **ACTIONS**, raw:99-101: "AbortOnFail / Causes the transaction to be aborted if the hook exits non-zero. Only applies to PreTransaction hooks." SYNOPSIS raw:45: "AbortOnFail (Optional, PreTransaction only)". |
| 3 | `NeedsTargets` passes matched trigger targets on stdin (entry :42-43) | **present** | **ACTIONS**, raw:104-107: "NeedsTargets / Causes the list of matched trigger targets to be passed to the running hook on stdin." |
| 4 | PostTransaction hooks do not run if the transaction fails to complete (entry :43-44) | **present** | **CAVEATS**, raw:139: "PostTransaction hooks will not run if the transaction fails to complete for any reason." |
| 5 | A file extracted with `.pacnew` triggers on the original name (entry :44-45) | **present** | **CAVEATS**, raw:137: "When installing or upgrading a file that is extracted with a .pacnew extension, the original file name is used in triggering the hook." |

Result: 5 of 5 claims present. S201 is not absent for any attributed claim.

Unattributed-to-S201 text in the entry, checked against its own cited source (S202 devblog, https://devblog.archlinux.page/2026/on-scripts-and-hooks/, opened 2026-10-26, page dated 2026-08-09; text receipt `devblog-text.txt`):

- "pre-transaction tasks are only available and run once the package is installed, that provides them. A post-transaction task is only available and run as long as the package is installed, that provides it." Present, **The two systems**.
- "First, the pre-transaction tasks of the alpm-hooks(5) in the test package version 0.1.0-1, then the pre- and post-upgrade functions of the alpm-install-scriptlet(5) in the test package version 0.1.0-2 and finally the post-transaction tasks of the alpm-hooks(5) in test package version 0.1.0-2 are run." Present, **Transaction example / Upgrading the package**.
- "we are missing a documented ordering system for alpm-hooks(5) in the distribution to establish ranges of number prefixes for specific tasks." Present, **Notes for package maintainers / Documentation**.

## 2. Defects found

**D1 — Staged IDs collide with live lane IDs (assimilation blocker).**

- The staged rows are S201, S202, S209 and S212 (`SOURCES.append.md:8,9,16,19`).
- In the lane (`corpus/SOURCES.md`, HEAD 5edb6c2e) those IDs already name different sources:
  - S201 = btrfs `ioctl.c` (:210)
  - S202 = errno(3) man7 (:211)
  - S209 = alpm-hooks(5) asciidoc at 54d9411 (:218)
  - S212 = round-38 host hook capture (:221)
- `grep -n -E '^\| S2(1[3-9]|2[0-9]) ' corpus/SOURCES.md` returns no rows, so the lane's highest S2xx ID is S212 and S213 onward is free (observed 2026-10-26; `corpus/SOURCES.md` is 314 lines).
- Appending the staged rows as they are would silently re-bind S201/S202/S209/S212. That would corrupt existing citations in `corpus/knowledge/mount-errno-contract-r37.md:3`, `errno-contract-variance-r37.md:2` and `pacman-hook-order-r38.md:1`, and the round-37 lessons.
- The staged numbering is campaign-local, so the rows need fresh lane IDs (next free) on assimilation, with the entry's `source:` lines renumbered to match.
- Note the staged S209 (alpm-install-scriptlet(5)) is a different source from lane S209 (alpm-hooks asciidoc). Same ID, different document. I did **not** re-open staged S209 or S212; this item scoped S201. A reviewer assuming "S209 = the scriptlet page" in the lane would be wrong.

**D2 — Staged S201 anchor omits the section that holds the ordering claim.**

- Entry header (`pacman-hook-timing-r25.md:2`): `# TRIGGERS` / `# ACTIONS`. Row anchor: `TRIGGERS; ACTIONS; CAVEATS`.
- Ordering (1a) and the directories (1b) are in **DESCRIPTION** (raw:52), not in TRIGGERS, ACTIONS or CAVEATS.
- The TRIGGERS section contributes nothing to the entry's claims; the entry's claims come from DESCRIPTION, ACTIONS and CAVEATS.
- Proposed anchor: `DESCRIPTION; ACTIONS (When, AbortOnFail, NeedsTargets); CAVEATS — Pacman 7.1.0, man date 2026-10-15, package 7.1.0.r9.g54d9411-3`.

**D3 — Overreaching sentence in the entry.**

- `pacman-hook-timing-r25.md:22-27` says: "Ordering is alphabetical, and upstream says that is not a design … So there is no documented precedence scheme to appeal to — the filename is the only lever."
- S201 states the alphabetical rule as a rule (raw:52). S202 says only that there is no documented *ordering system to establish ranges of number prefixes*. Neither says "that is not a design".
- "the filename is the only lever" is also incomplete: the lane's own sources show hook directory precedence (S008 overriding; lane S211 `alpm.c:56-62` for the directory-list head) and the `hook.c` tie-break (lane S208). That is the lane's own HO1-HO3 ground, which post-dates the staged entry.
- Proposed rewording: "Hooks run in alphabetical order of file name ignoring the suffix (S201 DESCRIPTION). The pacman maintainers add that the distribution has no documented number-prefix ordering convention (S202 Documentation), so the file name is the main ordering lever."

**D4 — The row's "non-overlapping complement to S008" is true only against S008.** See section 3.

## 3. Comparison with lane rows

**S008** (`corpus/SOURCES.md:14`): the alpm-hooks(5) man page, anchor `OVERRIDING HOOKS`, Pacman 7.1.0 footer dated 2026-10-15.

- Confirmed today: **OVERRIDING HOOKS**, raw:111: "Hooks may be overridden by placing a file with the same name in a higher priority hook directory. Hooks may be disabled by overriding them with a symlink to /dev/null." This matches S008's `teaches` text.
- S008 and staged S201 cite the same URL, the same man date and the same Pacman version. They hold disjoint sections: S008 holds OVERRIDING HOOKS; S201 would hold DESCRIPTION/ACTIONS/CAVEATS.
- The "complement to S008" claim holds. Because the URL is identical, a lane reader would see two rows for one page. That is acceptable only if the anchors stay disjoint, which D2's correction preserves.

**Lane S209** (`corpus/SOURCES.md:218`): `doc/alpm-hooks.5.asciidoc` at pacman 54d9411, lines 34-39 (ordering) and 87-89 (AbortOnFail).

- I re-fetched `https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/doc/alpm-hooks.5.asciidoc` (HTTP 200, 4351 B). Its sha256 is `2970cb35115a32a5d8a9652dfd795ad535d9354c36039fcc0d25929d9c3493d3`, equal to the row's recorded snapshot hash.
- Lines 35-39 read: "Hooks are read from files located in the system hook directory +{datarootdir}/libalpm/hooks+ … Hooks are run in alphabetical order of their file name, where the ordering ignores the suffix." Lines 87-89 read: "*AbortOnFail*:: Causes the transaction to be aborted if the hook exits non-zero. Only applies to PreTransaction hooks."
- These are the same sentences as S201 claims 1a, 1b and 2. They are the **source** of the rendered S201 page.
- So staged S201 overlaps lane S209 on three of its five attributed claims: ordering, directory list, and AbortOnFail PreTransaction-only. The row's "non-overlapping complement to S008" is right for S008 and wrong with respect to lane S209, since S209 already holds ordering and AbortOnFail, and S210 already holds the post-hook rule.
- The overlap is not harmful, since S201 is the published rendering and S209 the pinned source, and both agree. The honest framing is "S201 = published rendering of S209".

**Lane S210** (`corpus/SOURCES.md:219`): `trans.c` at 54d9411, `_alpm_trans_commit` lines 201-240.

- I re-fetched `.../raw/54d9411/lib/libalpm/trans.c`. Its sha256 is `637c1165790ddd1c9d80bb0bfed9d85b1f5baa9b8e5a2e323243c5764ac4ed07`, equal to the row's recorded hash.
- The code shows `_alpm_hook_run(handle, ALPM_HOOK_POST_TRANSACTION)` only inside the `else` of `if(trans->state == STATE_INTERRUPTED)`, after "transaction completed". The `_alpm_remove_packages` and `_alpm_sync_commit` failure branches `return -1` before it.
- This is the code-level confirmation of S201 claim 4 (CAVEATS raw:139). The man claim is also code-true at 54d9411.

**New to the lane from staged S201.** Searching `corpus/knowledge/pacman-hook-order-r38.md` for `NeedsTargets|pacnew|stdin` finds only a host count line (14 hooks with `NeedsTargets`), and no semantics. The two claims the lane does not already source are:

- claim 3 (`NeedsTargets` → stdin; the lane has the host count but not the semantics);
- claim 5 (`.pacnew` triggers on the original name; no lane hook row, and the lane's `.pacnew` ground is S011).

Claim 5 is directly relevant to the lane's `.pacnew`/`.pacsave` surface and to HO-rule readers asking whether `/etc/*.pacnew` could trigger a Path hook. That is the real incremental value of S201.

## 4. Proposed assimilation text (exact)

Corrected row, with the new lane ID `S213` standing for "next free ID at append time" (the staged S201 ID must not be reused):

`| S213 | alpm-hooks(5) — https://man.archlinux.org/man/alpm-hooks.5 | docs | A | alpm hook file-order, AbortOnFail/NeedsTargets semantics and the PostTransaction-on-failure and .pacnew-trigger caveats, as the published rendering of the pinned source in S209; disjoint from S008, which holds only OVERRIDING HOOKS | DESCRIPTION; ACTIONS (When, AbortOnFail, NeedsTargets); CAVEATS — Pacman 7.1.0, man date 2026-10-15, package 7.1.0.r9.g54d9411-3, opened 2026-10-26 | <keep staged teaches text> | mined | 2026-10-26 | on-release | corpus/knowledge/pacman-hook-timing-r25.md |`

- Renumber the staged S202, S209 and S212 to S214, S215 and S216 (or next free), with the matching `source:` lines in the entry.
- Replace entry :22-27 with the D3 rewording.
- Header line 2 of the entry becomes `source: S213 — … — \`DESCRIPTION\` / \`ACTIONS\` / \`CAVEATS\` — Pacman 7.1.0, man date 2026-10-15`.

## 5. Not done

- Staged S202, S209 (scriptlet page) and S212 (Chinese wiki) were **not** re-opened for their own claims, beyond the three S202 quotes above that the entry uses for its ordering and lifecycle claims. S209 and S212 were only checked for their ID collision with the lane rows.
- No per-HO-row verdicts were requested of this seat; none given. This seat is not one of C2RevHookC, C2RevOtherSrc, C2CritHO5, C2CritHO6 or C2RevenConf.
- No tools installed or upgraded. No pacman or host mutation. No lane tracked file touched.
