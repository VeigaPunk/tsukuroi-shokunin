# W2ConnAfter — sibling overlap re-scan at c052bb7

Written: 2026-10-24T04:37:17Z (`date -u +%H:%M:%SZ`). Scan close: 04:37:03Z. Read-only. No installs. No production edits. Pacman not run.

Axes: adjacency, connector. C1 (operability) and C2 (depth) predicates are not this seat's measures.

Change commit under test: `c052bb7d41ced49aa888817069afd804eccfecf1` (HEAD at scan). Freeze named by the wave: `1e926801195e304950e3eb9d2525ef8bbc245089`. Prior scan: `.ufo/waves/round-36/w1/ConnSiblings/ConnSiblings.md` (stamp 02:51:40Z).

## Contradiction (do not collapse)

Two different results:

1. **No new predicate or file collision.** No sibling last-round window, and no landed tsukuroi row, puts the C1 `leaking_pairs` measure or the C2 rejection sentence into another lane's claim.
2. **The landed S198 title is the neighborhood ConnSiblings said not to mint.** Mori `corpus/SOURCES.md` S014 is already titled `journalctl(1)` and already says the systemd 262 man page was opened 2026-10-19. C2's rows must not be read as fleet-novel `journalctl(1)`.

(1) does not erase (2). (2) does not fail C2's depth predicate.

## Method

Twenty sibling checkouts under `/home/vgpnk/Projects/shokunin/*-shokunin` (home lane excluded). Own-round commits: subject matching `^(?:lore\s+)?r(?:ound[- ])?N`. Last three rounds = the three highest such N in `git log -n 800` (same rule as ConnSiblings; not first-seen order).

Re-checked at sibling `HEAD`:

- `git grep -I -F 'cannot be combined with options that limit the journal'` → 0 lanes (04:36:43Z).
- `git grep` for `journalctl now rejects -F`, `probe-child-env-allowlist-r36`, `leaking_pairs`, `journalctl-v262-field-filter-r36` → no hits.
- `git ls-files` for `check-revision-binding`, `check-report-receipts`, `score-census-handoff-r32`, `mutants-btrfs-space-r30`, `run-receipt.py`, `probe-child-env-allowlist` → no path.
- Tool-basename hits that remain are citations of tsukuroi, same class as the 02:51Z table (kama r23, kotodama r50, kumitate r51, tameshi r18/r32/r35).

Diff-scanned every commit in a round that entered the highest-3 set since 02:51Z, plus mori rounds 37–39 and chousa round 38 in full (`git show --unified=0`, binary lines skipped). Keyword set: `journalctl`, `leaking_pairs`, `probe-child-env`, `CHILD_ENV`, `clean_env`, `GIT_CONFIG_NOSYSTEM`, `os.environ`, `pacnew`, `pacsave`, `strace`, `field_list_has_scope`, `cannot be combined`, the five tool basenames, `-F/--field`.

## Windows since ConnSiblings

| Lane | Highest 3 then | Highest 3 now | Tip now | New-round keyword result |
|---|---|---|---|---|
| chousa | 35–37 (`b905217`) | 36–38 | `870074e8aaf0` | Still `env = dict(os.environ)`. Predicate is `ENV_PIN_CAPTURE_MATCH` (7/7), not `leaking_pairs`. `strace` is a network watch. |
| kake | 42–44 (`942fe18`) | 43–45 | `dc7f03e7c8ba` | Cites tsukuroi `run-receipt.py` as "a score harness". `strace` is a network watch. `os.environ` hits are vendored Python HTML. |
| kotoba | 61–63 (`cbbee56`) | 62–64 | `b99fb79c2704` | `c019919c`: `env = os.environ.copy()` in `verifiers/check_r64_routed_repairs.py` and a wave report. Ambient copy, not the five tools. |
| kotodama | 62–64 (`097c21d`) | 62–64 | `17c32302c684` | Same three rounds. `git log -G` on `097c21d..HEAD` for journalctl / leaking_pairs / probe / `GIT_CONFIG_NOSYSTEM` / `clean_env`: empty. |
| kumitate | 49–51 | 50–52 | `042372174ac3` | Production tree: zero `journalctl` lines (`git grep` excluding `.ufo`, rc 1). `GIT_CONFIG_NOSYSTEM` only in round-52 wave sandbox copies. `ConnOverlap.md` cites tsukuroi C1/C2 and says `run-receipt.py` is not `scripts/receipt-attest.mjs`. |
| mori | 36–38 (`b699374`, then `13f3db7`) | 37–39 | `bb1f2457bb8d` | `clean_env()` still pops `GIT_*` off `dict(os.environ)`. No `-F` claim. See neighborhood. |
| revenger | 61–63 | 62–64 | `782bd020c65e` | `git log -G` on round-64 for the rejection sentence / `leaking_pairs` / the probe: empty. |

Unchanged highest-3, not re-diffed: audio 99–101 `7a2fcd4f0883`, game-dev-2d 103–105, game-dev-3d 106–108, kagi 26–28, kaidoku 32–34 `f432c8e3bc58`, kama 29–31, kasegi 20–22, kengaku 27–29, lore 101–103, mado 26–28 `317ff19c6343`, souji 20–22 `4edb25dfe262`, tabi 20–22 `e3cf4e0d30bb`, tameshi 33–35 `34fa5b0cfe90`. Their HEAD greps above still stand.

Kumitate's tip moved during this seat (`ab5dde401b7c` at 04:33:40Z, `042372174ac3` by the window pass). Both are round-52 subjects; the later one is "FINAL receipts", and the production `journalctl` grep was at the later tip.

## C1 — no new collision

Nobody else has the five tools, the probe, or `leaking_pairs`.

New activity is the same neighborhood, different predicates:

- chousa r38 (`504c1d2`, freeze) still builds the child with `dict(os.environ)`. The printed predicate is now `ENV_PIN_CAPTURE_MATCH` (r37's name was `PIN_CAPTURE_ENV_MATCH`). Still not C1. A scoreboard that keys only on "env" will double-count; the predicates do not.
- mori r37–39 `clean_env()` is the C1 before-shape (inherit, then drop `GIT_*`), on mori's own counters. Not a fixed `PATH=/usr/bin:/bin` dict and not the five tools.
- kotoba r64 `os.environ.copy()` is ambient inheritance in `verifiers/check_r64_routed_repairs.py`.
- kumitate r52 and kake r45 only cite tsukuroi. They do not own the tools.

No new `.pacnew` / `.pacsave` claim showed up in the new-round diffs.

## C2 — predicate absent; title neighborhood is real

Exact rejection line `-F/--field= and -N/--fields cannot be combined with options that limit the journal.` :

- 0 sibling HEADs (04:36:43Z).
- 0 hits in mori `HEAD` (whole tree, 04:37:03Z).
- 0 hits for `field_list_has_scope_options` and for `-F/--field` in mori `HEAD`.

Mori's live argv is still `--output-fields`, not `-F`/`-N`: `tools/mori-census.sh:1232` and `:1335`, `tools/mori-journal-window.py:440` and `:844`. C2 does not indict those commands.

Landed rows at `c052bb7` (`corpus/SOURCES.md`):

- S198 title cell: `journalctl(1) at systemd 262 — https://man.archlinux.org/man/journalctl.1`. Quote cell says `-F`/`-N` semantics and that the restriction is **not** on that page.
- S199 title cell: `systemd NEWS pinned at the v262 tag`. Not a `journalctl(1)` title. Quote cell says NEWS has the prose rejection, not the 84-byte runtime line.
- The note `corpus/knowledge/journalctl-v262-field-filter-r36.md` does not mention mori or S014. `corpus/README.md` round-36 row says "S198 journalctl(1) at 262" with no sibling pointer.
- Tsukuroi's own S014 is ArchWiki mkinitcpio. It is not this neighborhood. The collision is **mori's** S014.

### Mori-neighborhood note

Do not read S198/S199, or the note, as fleet-novel `journalctl(1)` against mori.

| Row | What it already holds | What it does not hold |
|---|---|---|
| mori S014 | Title `journalctl(1)`. URL `https://www.freedesktop.org/software/systemd/man/latest/journalctl.html`. Anchor: Source Options; Filtering Options `--after-cursor`; Output Options `--output-fields`; "systemd 262 man page opened 2026-10-19". Used by mori journal knowledge notes. Cell length 714. Counts inside the cell: `-F` 0, `--field` 0, `cannot be combined` 0, `field_list` 0, `--output-fields` 1. | The `-F`/`-N` rejection sentence. The Arch man URL. |
| mori S122 | Same `man/journalctl.xml` sha256 `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` that tsukuroi S188 and S198 cite. Span is JSON encoding and `--output-fields` (`:586-603`, `:667-675`). | `-F`/`-N` (cell count 0). |
| mori S160 | `src/journal/journalctl.c` at tag v262, "option grammar and filter application", companions `journalctl-filter.c` and `journalctl-util.c`. The cell's worked example is `-b`/`-u`, not field listing. | `-F`, `--field`, `field_list`, `cannot be combined` (cell counts 0). A case-folded `-n` count of 1 is not the token `-N` (`find("-N")` is -1). |
| tsukuroi S188 | Same xml sha, scoped to JSON / export. Already in this lane. | The rejection line. |

S198's title is the string ConnSiblings warned against ("a new tsukuroi row titled like S014 (`journalctl(1) at systemd 262`)"). The propositions differ: S014 is cursor and `--output-fields`; S198 is `-N`/`-F` wording plus an explicit absence. Same manual family, different URL, different sentence. S160 is the same `journalctl.c` file the note cites at lines 958-960, and it does not contain that sentence. S199 does not take the `journalctl(1)` title.

The behavior that is still unclaimed outside this lane is the rejection line, exit 1, and the 16-term predicate. That is not a second fleet `journalctl(1)`.

False hits recorded so they are not re-read as the sentence: mori r37 `52d636d` / `e57c58b` "cannot be combined" is `Set-Cookie` HTML in an S225 source copy. mori r38 `b699374` mentions S160 by id only.

## Proposed move (one)

Append one adjacency sentence, in the L1's C2 adjacency note or the note's source list, not in either claim's predicate and not by rewriting S198 (registry in-place edits are status / recheck / used-by only):

> S198 is not a second fleet `journalctl(1)`. Mori S014 already holds that title for source selection, cursor bounds, and `--output-fields` on the systemd 262 man page. Mori S160 already holds v262 `journalctl.c` option grammar and does not contain the rejection line. S198/S199 add the `-N`/`-F` man wording, the pinned NEWS bullet, and the runtime rejection, which those rows do not.

Adjacency improves (the contested title stays reported). Operability and depth predicates stay unchanged, so neither axis is harmed. Do not retitle S198 in this round's close; a title rewrite would touch an immutable cell to fix a label the sentence above already fences.

## Risks

- Treating "no new collision" as the only result hides the title. A later reader of `corpus/README.md` ("S198 journalctl(1) at 262") can credit tsukuroi with mori's manual.
- Treating the title overlap as a failed depth claim would reject a sentence mori does not have.
- chousa r38 `ENV_PIN_CAPTURE_MATCH=7/7` and C1 `leaking == 0` share the word environment only.
- Shared xml sha `d54bbede` (mori S122, tsukuroi S188, tsukuroi S198) is one upstream file with three spans, not three authorities for the rejection line.
- Mori and kumitate tips moved during the scan. The greps named above are at the later tips. A commit after 04:37:03Z is unseen.

## Verification run

- Sibling tips and highest-3 windows, 04:33:40Z and again in the window pass.
- HEAD exact-string greps and `git ls-files` for the five tools.
- Byte-safe diff scan of the new rounds (74 commits considered; 22 keyword-hit commits, classified above).
- Mori S014/S122/S160 cell needle counts; mori whole-tree grep for the rejection line, `-F/--field`, and `field_list_has_scope_options` (all absent, 04:37:03Z).
- Landed S198/S199 title cells via `git show c052bb7:corpus/SOURCES.md`.
- Note/README absence of a mori S014 pointer (the note file has no `mori` / `S014` / `fleet-novel` hit; README mori hits are older adjacency rows, not the round-36 C2 row).
- Mori tool argv lines still `--output-fields`.

Not run: no probe, no live `journalctl` matrix, no re-fetch of the man page, no census. An unrun check has not passed. This seat did not open mori's rendered man-page body beyond the S014 cell and the tree-wide absence of the rejection line.
