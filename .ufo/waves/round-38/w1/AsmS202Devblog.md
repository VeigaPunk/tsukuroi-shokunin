VERDICT: defect-found

# AsmS202Devblog — Item A-2: S202 re-open (staged `pacman-hook-timing-r25.md`)

Source: S202 https://devblog.archlinux.page/2026/on-scripts-and-hooks/ — accessed 2026-10-26 (curl 200, 97486 bytes, 2026-10-26T05:04:20Z; receipt `.ufo/waves/round-38/w1/AsmS202Devblog/page.html`, sha256 `ea3085d7191f6cf889d3ff9d0486f51780592d4fd93dbc0bf8a7db56702364ef`). Page front-matter: published 2026-08-09, authors David Runge and Arne Christian Beer, tag alpm-hooks, Zola v0.23.6.
Staged entry: `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/knowledge/corpus/knowledge/pacman-hook-timing-r25.md` (71 lines; S202 header at :3; claims at :22-39). The page was read through the read tool (first 300 lines inline, rest via artifact) and re-checked by a tag-stripped substring search of the raw HTML.

## Verdicts

| item | verdict | summary |
|---|---|---|
| (a) ordering-system statement | **present, with attribution drift and locator drift** | The quoted words are verbatim; the staged text attributes them to the wrong body and cites the wrong section. |
| (b) upgrade order | **present** (faithful) | The order matches the blog's own words. Staged adds one inference. |
| (c) hook exists only while provider is installed | **paraphrase-drift** (semantically faithful, not verbatim) | The exact phrase is absent; two sentences support it. |

## (a) — present; two drifts

Located verbatim (section `### 📓 Notes for package maintainers` → `#### Documentation`; also tag-stripped HTML offset 21904):
> "At the time of writing, we are missing a documented ordering system for alpm-hooks(5) in the distribution to establish ranges of number prefixes for specific tasks."
(24 words of the quoted sentence; the continuation "Having such documentation would allow us to work with alpm-hooks(5) more robustly." follows.)

Staged (`:24-26`): *"missing a documented ordering system for alpm-hooks(5) … to establish ranges of number prefixes for specific tasks"*. The ellipsis elides only "in the distribution" — the quote is verbatim and honestly elided. Present.

Drifts (defects in the staged entry):
1. **Attribution drift.** Staged `:23-24` says "The pacman maintainers state plainly that the distribution is …". The page's authors are David Runge and Arne Christian Beer, writing in the Arch Linux Dev Blog about Arch Linux package-integration research ("we have been doing research on the integration of our official distribution packages"). The phrase "pacman maintainers" is ABSENT from the page (substring search: ABSENT). "we" = the dev-blog authors, not the pacman maintainers.
2. **Locator drift.** The staged S202 header (`:3`) cites `# The two systems` / `# Transaction example`. The quoted sentence lives in `Notes for package maintainers › Documentation`, which is neither. Actual headings are `## 2️⃣ The two systems`, `### ⌨️ Transaction example`, `### 📓 Notes for package maintainers`, `#### Documentation` (levels are ##/###/####, not `#`).
3. **Unsourced adjacent claims in the same paragraph (`:22-23`, `:26-27`).** "Ordering is alphabetical" and "upstream says that is not a design" are NOT in S202: the string "alphabet" is ABSENT from the page. The page's only ordering words about hooks are "alpm-hooks(5) offer a strictly ordered and timed integration" (section `### 🪝 Hooks`, offset 6353) plus the missing-number-prefix-ranges statement. The alphabetical claim must rest on S201 (alpm-hooks(5)), not S202. "The pacman maintainers state … not a design" is a reading of the quote and of the "At the time of writing" caveat (dated 2026-08-09); the blog states only that *documentation of number-prefix ranges is missing*, not that alphabetical order "is not a design". "so there is no documented precedence scheme … the filename is the only lever" is the entry's inference, not blog text.

## (b) — present

Located verbatim (`#### Upgrading the package`, closing paragraph; offset 20318):
> "First, the pre-transaction tasks of the alpm-hooks(5) in the test package version 0.1.0-1, then the pre- and post-upgrade functions of the alpm-install-scriptlet(5) in the test package version 0.1.0-2 and finally the post-transaction tasks of the alpm-hooks(5) in test package version 0.1.0-2 are run."
(Quote 1: "First, the pre-transaction tasks … in the test package version `0.1.0-1`" ; abbreviated, original is one sentence of ~55 words.)

Matches staged `:35-37` ("old pre-transaction hooks first, then new install-scriptlet functions, then new post-transaction hooks"). Supporting evidence in the page's own pacman output for the upgrade: `(1/1) Running the pre-transaction hook for test package 0.1.0-1...` (old), `Running the pre_upgrade function … 0.1.0-2`, `Running the post_upgrade function … 0.1.0-2`, then `(2/2) Running the post-transaction hook for test package 0.1.0-2...` (new).

Caveats (not drift in the quote, but scope limits the staged text does not state):
- The order is observed in ONE worked example (a hook package whose triggers target itself, `Target = test`, `--upgrade` of a local file). The blog presents it as an illustration, not as a general statement of rules.
- The staged sentence "a writer observed after an upgrade may belong to the old version's hook or the new version's scriptlet" (`:38-39`) is the entry's inference for the lane's use, not blog text.
- Corroboration inside the page: first-install output shows no pre-transaction hook line (the hook is not yet on disk), and the removal output shows `(1/1) Arming ConditionNeedsUpdate...` only after removal, i.e. the removed package's post-transaction hook did not run.

## (c) — paraphrase-drift (faithful in meaning)

The staged sentence "A hook exists only while its providing package is installed" (`:29`, bold) does NOT appear in the page as such. The page says, under `### 🪝 Hooks` → "A few things should be noted about alpm-hooks(5):" (offsets 6922 and ~7022):
> "As hooks are read from the target system's filesystem, pre-transaction tasks are only available and run once the package is installed, that provides them."
> "A post-transaction task is only available and run as long as the package is installed, that provides it."

Staged `:29-31` second half repeats these two sentences nearly verbatim ("a pre-transaction task is only available and run once the package that provides it is installed; a post-transaction task is only available while that package remains installed"). The bold headline, however, merges them into a stronger, single claim: the blog says *pre-transaction* tasks are available "once the package is installed" (a start condition) and *post-transaction* tasks "as long as the package is installed" (a duration), and says nothing about hooks "existing". The page's own removal example shows the pre-transaction hook of the package being removed still runs (package still installed at that time), so "exists only while installed" is consistent but loose. Verdict: paraphrase-drift; the headline should quote the two sentences instead of coining one.

## Proposed corrected text for the staged entry (draft; seat made no edit)

Header `:3` replace with:
`source: S202 — https://devblog.archlinux.page/2026/on-scripts-and-hooks/ — "Hooks" (bullets), "Upgrading the package", "Notes for package maintainers › Documentation" — published 2026-08-09, David Runge and Arne Christian Beer`

Replace `:22-27` with:
> **Number-prefix ranges are undocumented.** The Arch Linux Dev Blog authors (not "the pacman maintainers") write, on 2026-08-09: *"At the time of writing, we are missing a documented ordering system for alpm-hooks(5) in the distribution to establish ranges of number prefixes for specific tasks."* (S202, Notes for package maintainers › Documentation.) The claim that hooks run in alphabetical order of file name must be cited to S201 alpm-hooks(5), not S202, which does not contain it.

Replace the bold headline `:29` with: **Hook availability is bound to the providing package's installation (two statements).** and quote both sentences above.

Replace `:35-37` keep, but add: *"(S202 shows this in one worked example, not as a general rule; the inference about writer attribution is the lane's own.)"*

## What I did not do
- I did not compare against S201 (alpm-hooks(5)) or the pacman source; the "alphabetical" claim's own support was not verified here, only its absence from S202.
- Images (package-manager-transaction.svg) were not opened.
- No lane or shokuknow file was edited; no host change. Tools installed: none.
- Scratch dir removed (trap); the only kept receipt is `AsmS202Devblog/page.html`.
