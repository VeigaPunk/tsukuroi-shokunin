VERDICT: draft

Seat SimplifyEntry, item R-5 (advisory, text only). Target: `corpus/knowledge/pacman-transaction-order-r39.md` at
`4078eb2` (entry bytes at lane HEAD `394e1ba` are identical: `git diff --stat 4078eb2 -- corpus/knowledge/pacman-transaction-order-r39.md`
prints nothing; sha256 `701a462dfe9c3d03fba0366719e772e081d6cb181e25398d78c0f1ebf5b0d74a`). I edited nothing in the lane.
Three cuts/merges are proposed below; each was applied to a scratch clone and the frozen counter re-run: base PASS,
every proposed variant PASS. I judge **no TO row's truth** against the pinned source, so no `TO<n>: holds|partly|fails`
lines are emitted by this seat.

## Method and receipts

Scratch clone `git clone -q --shared <lane>` under `/fast/scratch/hyaku/tsukuroi-r39/SimplifyEntry/`, `remote remove origin`,
variants committed on `master` there; counter `tools/check-transaction-order-r39.py`
(sha256 `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e` = the declared digest, `sha256sum tools/check-transaction-order-r39.py`)
run with `--repo <clone> --revision <variant>`.

| receipt | revision | predicate fields | result |
|---|---|---|---|
| `.ufo/waves/round-39/w1/SimplifyEntry/counter-base-4078eb2.json` | `4078eb2` | 8 / 0 / 0 / 1 / 2 / 0 | PASS exit 0 |
| `…/counter-variantA-3a52105.json` | `3a52105` | 8 / 0 / 0 / 1 / 2 / 0 | PASS exit 0 |
| `…/counter-variantB-5e3a0d7.json` (`--branch b`) | `5e3a0d7` | 8 / 0 / 0 / 1 / 2 / 0 | PASS exit 0 |
| `…/counter-variantC-9ba32be.json` | `9ba32be` | 8 / 0 / 0 / 1 / 2 / 0 | PASS exit 0 |
| `…/counter-variantD-4271dc2c77d6083ec10d392010083613b7db3ba9.json` | `4271dc2` | 8 / 0 / 0 / 1 / 2 / 0 | PASS exit 0 |

Field order: `rules_verified / duplicate_rows / duplicate_headings / source_ok / counts_ok / oracle_violations`.
`variantA.diff`, `variantD.diff` and `proposed-entry-D.md` (the full proposed bytes) sit beside the receipts.
Header gate at the same clone, `python3 tools/check-knowledge-header.py --revision 9ba32be9…` → `complete_count 60,
finding_count 0, clean_count 60` (stdout line 1 of that run; `source:`/`verified-at:`/`recheck:` are untouched by every proposal).

Why the counter cannot see these cuts: it reads only `## ` headings for duplicates (`tools/check-transaction-order-r39.py:176-177`),
the `source:` line (`:178`) and rows matching `^\|\s*(TO\d+)\s*\|` (`:186`), plus the two host-count substrings (`:224-226`).
The intro paragraph, the order section and the Boundaries bullets are never parsed. That is a fact about the counter,
not permission to cut anything; the constraint the item imposes is "keep every TO row and the counter passing", and
that is what the table above measures.

## Axis A — sentences that restate `pacman-hook-order-r38.md`

| # | entry location | text (short) | restates | verdict |
|---|---|---|---|---|
| A1 | `:7-8` | "`…pacman-hook-order-r38.md` holds the order of hooks **within** a phase (HO1–HO7)" | pointer, not a restatement | **keep** — it is the partition that makes two entries admissible instead of one |
| A2 | `:8-11` | six-clause scope enumeration ("where the two hook phases sit…, the order of removals…, the scriptlet arguments, when the hook directories are read, and what the `[ALPM-SCRIPTLET]` log tag…") | not r38: it is a third copy of the eight-proposition list already frozen in `SCORECARD.md:2221` and already carried by TO1–TO8 | **cut** (Block 1) |
| A3 | TO1 rule cell `:24` | "the PostTransaction phase runs after `transaction completed`" | `pacman-hook-order-r38.md:26` (HO6: "PostTransaction hooks run only after `transaction completed`") | **keep, flagged** — this is the seam the entry exists to draw; cutting it moves a declared proposition out of the row a QUALITY 81 reviewer reads. Not cut in any variant |
| A4 | `:36` | "in HO1 order" | pointer | **keep** |
| A5 | `:41` | "(or `transaction interrupted` / `transaction failed`, which end it without Post hooks)" | `pacman-hook-order-r38.md:26` second clause ("a failed or interrupted commit runs none") | **cut** (Block 2) — the parenthetical already sits next to `(TO1, HO6)` two nodes later |
| A6 | `:44` | "Every line any step 2–8 child prints is logged as `[ALPM-SCRIPTLET]` (TO8)." | TO8's own row `:31`, same entry | **cut** (Block 2) — a tag rule has no position in an ordering chain |
| A7 | Boundary bullet `:48` | "It does not say whether a given hook ran on this host; HO7 and the pacman.log `running` lines answer that." | `pacman-hook-order-r38.md:27` host cell (the subsequence test) + r38 `:108` [unk] | **keep, retighten** (Block 3) — it is the only boundary that says something, but "does not say whether a given hook ran" is overbroad: TO5's host cell `:28` already says of 17 named hooks that none ran in the named transaction |
| A8 | Boundary bullet `:49-50` | "TO5's host column is consistency, not proof: the capture cannot separate \"the hook file was absent\" from \"its triggers did not match\"." | TO5 host cell `:28` last sentence ("This is consistent with the rule, not a proof of it: a Pre hook whose triggers did not match would not have run either") | **merge** into the row it qualifies (Block 4) — a caveat belongs on the claim |
| A9 | Boundary bullet `:51` | "It reads no transaction live and runs no pacman command; the host column comes from the frozen copy." | intro `:12-13` ("the host column is read from a frozen copy…"; "Nothing here authorizes a package, hook or transaction action") and r38 `:108` [unk] | **cut** (Block 1 folds the one live fact into the ground sentence) |
| A10 | TO5 host cell `:28` | "17 PreTransaction hook files…" | r38 count (17 Pre / 52 Post) | **keep** — load-bearing for the row's consistency claim; the shared number is a coupling, not a duplicate |

Nothing is cut that is provenance: the `source:`/`verified-at:`/`recheck:` header, the refused-as-staged paragraph
`:15-18` and the QUALITY block `:53-58` are untouched.

## Axis B — the "Order of one transaction" list against the rules table

Measured, base body `:35-44` (heading `:33`) = 778 chars / 105 words / 10 lines; steps 2–8 are each a TO row restated in compressed form
(step 4 = TO2+TO7, step 5 = TO3+TO4, step 6 = TO6, step 7 = TO1+HO6, step 8 = TO1+TO5, line 44 = TO8). Two facts in
it are not in any row: step 1 (the frontend `[PACMAN] Running` line opens the sequence — TO1's host cell `:24`
mentions the 86 windows only as a count) and the alternatives in step 7. Verdict: **merge to a pointer chain**
(Block 2), not delete.

Two shapes were priced (four commits: A = chain, B = delete the section, C = A plus the heading rename, D = C plus Block 4):

- **A/C/D (kept recommendation)** — heading stays, body becomes a four-line arrow chain, 778 → 336 chars.
- **B (rejected)** — the whole section deleted: counter still PASS (`counter-variantB-5e3a0d7.json`), and the entry
  loses the only single-pass artifact plus the frontend's position in the sequence. Rejected because that is a
  teaching loss with no compensating gain over the chain.

## Axis C — boundary bullets that say nothing

- `:48` — says something (no per-hook adjudication), but overbroad against TO5's host cell; **retighten**.
- `:49-50` — says what TO5's host cell already says; **merge into the row**.
- `:51` — both clauses are already in the intro; **cut**.

One structural note on the same axis: the heading is `## Boundaries — what this entry does NOT establish`
(`:46`), while the two entries that carry the section call it `## Boundaries`
(`corpus/knowledge/errno-contract-variance-r37.md:27`, `corpus/knowledge/mount-errno-contract-r37.md:29`; only
three of the 60 entries in `corpus/knowledge/` carry the word at all — `grep -ln Boundaries corpus/knowledge/*.md`). Renaming to the bare form is a 37-character saving
with no loss and removes a one-off name; tested as variant C (PASS).

## Proposed text (Block 1–4, applied together = `proposed-entry-D.md`, counter PASS)

Block 1 — replace `:7-13`:

```
Ground: the update-safety plane (`PROVINCE.md` Core). `corpus/knowledge/pacman-hook-order-r38.md` holds the
order of hooks **within** a phase (HO1–HO7); this entry holds what happens **between** the phases (TO1–TO8).
Every rule is read from libalpm source at the installed commit; the host column is read from a frozen copy of
this host's `/var/log/pacman.log`, no transaction was read live and no pacman command was run. Nothing here
authorizes a package, hook or transaction action.
```

Block 2 — replace `:35-44` (heading `:33` unchanged):

```
`[PACMAN] Running '<command>'` (the frontend) → Pre hooks in HO1 order (TO1, TO5) → `[ALPM] transaction
started` → removals before adds (TO2, TO7) → each target in transaction order (TO3, TO4) → `ldconfig` once
(TO6) → `[ALPM] transaction completed`, or `interrupted`/`failed` (TO1, HO6) → Post hooks, re-read from disk
(TO1, TO5, HO6).
```

Block 3 — heading `:46` becomes `## Boundaries`; the three bullets `:48-51` become:

```
- It gives no per-hook verdict beyond TO5's 17-file check; HO7 and the pacman.log `running` lines answer whether a given hook ran.
```

(one line in `proposed-entry-D.md`; wrapping it at the entry's ~100-column style is cosmetic and does not touch the
counter, which never reads this section)

Block 4 — in TO5's host cell `:28`, replace the trailing sentence
`This is consistent with the rule, not a proof of it: a Pre hook whose triggers did not match would not have run either`
with
`This is consistent with the rule, not a proof of it: the capture cannot separate an absent hook file from a trigger that did not match`
(this is the only substance in the cut bullet `:49-50` that the host cell did not already carry).

Effect: 58 → 47 lines, 8262 → 7343 chars (−919, −11.1%), 1178 → 1044 words (−134, −11.4%), `## ` headings 4 → 4,
`| TO<n> |` rows 8 → 8, all eight TO source cells byte-identical.

## What each cut loses

| cut | loses | still available at |
|---|---|---|
| Block 1 | the six-clause scope list; a reader must read TO1–TO8 (or `SCORECARD.md:2221`) to see the scope | `SCORECARD.md:2221`; TO1–TO8 |
| Block 2 step 4 | the per-removal micro-order `pre_remove → files → removed → post_remove` | TO7 `:30` |
| Block 2 step 5 | the per-package micro-order `pre_install/pre_upgrade → files+db → installed/upgraded → post_install/post_upgrade` | TO3 `:26` |
| Block 2 step 2 | the `running '<name>'` line hint | TO1 host cell `:24`; r38 HO7 `:27` |
| Block 2 `:44` | the tag statement inside the sequence | TO8 `:31` |
| Block 2 step 7 | "which end it without Post hooks" | r38 HO6 `:26`, cited as `(TO1, HO6)` |
| Block 3 bullet 2 | the "absent file vs non-matching trigger" distinction in the Boundaries list | TO5 host cell via Block 4 |
| Block 3 bullet 3 | nothing semantic | intro `:12-13` via Block 1 |
| Option B (not proposed) | the whole sequence and the frontend's position in it | nothing else states the frontend position as an order |

## Tradeoffs left standing

- **TO1 clause 3** stays a duplicate of HO6's first clause (A3). Cutting it is the one deletion this seat considered
  and refused: the C2 kill rule (QUALITY 81, per-row reviewer verdict) makes the row text the judged object, and
  TO1's job is exactly the log-line placement. A pointer would save ~30 chars and cost a declared proposition its row.
- **The chain still names TO ids.** That is intended: it is an index into the table, and the ids are what make the
  table, the declaration and the sequence stay one authority instead of three.
- **TO5's "17"** is r38's count. If a hook file changes, `pacman-hook-order-r38.md` and TO5's host cell must move
  together; no cut removes that coupling.

## Not done

No live transaction read, no pacman command, no host mutation, no mount or sysfs change, no sudo, no package action,
no tool install (nothing needed). No lane file written except this report and the receipts under
`.ufo/waves/round-39/w1/SimplifyEntry/`. No git/jj write in the lane (all commits are in the scratch clone, since
removed). I did not re-judge TO1–TO8 against the snapshots, so this report carries no TO verdict lines.

Shared-tree state at report time, for the record — not my changes: `git -C <lane> status --porcelain` shows
` M PROVINCE.md`, ` M SKILL.md` and the untracked wave-39 paths. The two modifications are the C1 seat's round-39
appends (`git diff --stat` = 14 and 21 inserted lines, 0 deletions; mtimes 03:02:09 and 03:03:26, before this seat's
first write at 03:07:44). The target entry is byte-identical to `4078eb2` and to its own lane HEAD (`git diff --stat
HEAD -- corpus/knowledge/pacman-transaction-order-r39.md` empty).
