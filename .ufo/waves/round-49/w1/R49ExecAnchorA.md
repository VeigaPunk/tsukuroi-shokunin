VERDICT: supports

# R49ExecAnchorA — independent re-derivation of OUT-002..OUT-010 (item C2-B1)

Freeze under test: `55c07cd3f8bff2e12117c34d57b4c618de74d85c` (lane `tsukuroi-shokunin`, branch master).
All lane bytes read with `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show <REV>:<path>`;
all sibling bytes read with `git -C /home/vgpnk/Projects/shokunin/<sib>-shokunin show <commit>:PROVINCE.md`.
Siblings were read-only; nothing was written in any sibling repo, in the fleet repo, or in the lane.

## What was re-derived (independently of `tools/check-adjacency-table-r49.py`)

For each OUT id named in the frozen ADJ table (`PROVINCE.md:46-52`, 7 rows) and defined in the
frozen anchors table (`PROVINCE.md:110-130`, OUT-001..OUT-010; OUT-002..010 are the ADJ-cited nine):

1. registry row read from `corpus/knowledge/adjacency-anchors-r19.json` at the freeze (`outbound`, 10 rows, exact key set `id,province_pointer,sibling,sibling_path,sibling_commit,sibling_blob_sha256,snapshot,heading,quote,quote_line,proposition`);
2. `git cat-file -e <commit>^{commit}` in the sibling repo;
3. `git show <commit>:PROVINCE.md | sha256sum` compared to `sibling_blob_sha256`;
4. heading literal present in that blob (and at line 1 of it);
5. quote literal present verbatim in that blob, and on line `quote_line` exactly (delta 0); quote occurrence count in the blob = 1 for all nine; `quote_line` also inside the registry `province_pointer` range set;
6. ADJ class symmetry: the anchor row's `ADJ row` cell equals the ADJ row whose **Ownership source** cell names that OUT id, in both directions, and the map is a bijection (each of the nine cited by exactly one ADJ row; no OUT-001 citation);
7. the table's abbreviated commit resolves unambiguously (`git rev-parse --verify <12hex>^{commit}` = the full registry commit);
8. table cells equal the registry fields byte-for-byte (sibling path, heading, quote, proposition);
9. the lane's own committed snapshot `record.snapshot` at the freeze hashes to the same sha256 as the live sibling blob.

## 9-row PASS/FAIL table (digests I computed)

| # | Anchor | Sibling | Pinned commit | Computed blob sha256 | commit exists | sha256 match | heading (line) | quote@quote_line | ADJ class symmetric | snapshot@freeze | verdict |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | OUT-002 | kama | `e75cf680b53484a61709ee1b2787d8dbc6419f74` | `799432d748bd40bcf859de806cc2ef90df069da14c8e5c07bf72250ac411c7a6` | PASS | PASS | PASS (1) | PASS (12) | ADJ-01 ⇄ PASS | PASS | **PASS** |
| 2 | OUT-003 | kagi | `c2cab35bc92e57e39e5489bac3386db078345b3f` | `4a346e2df81f7b2e649914d0d99da974d6c484caf12fed1c6bd530d106a78523` | PASS | PASS | PASS (1) | PASS (3) | ADJ-02 ⇄ PASS | PASS | **PASS** |
| 3 | OUT-004 | mado | `a4046a8216080d4004de3f268c62cf142095ac07` | `1b25bb1e980925b356663602d002c1c15307a0dfac8bfafd9988bd4d8df7464b` | PASS | PASS | PASS (1) | PASS (6) | ADJ-03 ⇄ PASS | PASS | **PASS** |
| 4 | OUT-005 | mori | `91940fa339e38006f8db5bd7d78bb6f037f4d016` | `73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130` | PASS | PASS | PASS (1) | PASS (8) | ADJ-04 ⇄ PASS | PASS | **PASS** |
| 5 | OUT-006 | kumitate | `1770305fae20826b39905a8251ddeca6b4957ac4` | `fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f` | PASS | PASS | PASS (1) | PASS (3) | ADJ-05 ⇄ PASS | PASS | **PASS** |
| 6 | OUT-007 | mori | `91940fa339e38006f8db5bd7d78bb6f037f4d016` | `73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130` | PASS | PASS | PASS (1) | PASS (12) | ADJ-05 ⇄ PASS (note 1) | PASS | **PASS** |
| 7 | OUT-008 | kaidoku | `d1d981d2cc041dda4656c5b01d2c8445d8d17124` | `63920930b77f9604c6ff7f5db8859344ef97fa50de9e4d0028897da4288859ac` | PASS | PASS | PASS (1) | PASS (3) | ADJ-06 ⇄ PASS | PASS | **PASS** |
| 8 | OUT-009 | revenger | `cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97` | `63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f` | PASS | PASS | PASS (1) | PASS (3) | ADJ-06 ⇄ PASS | PASS | **PASS** |
| 9 | OUT-010 | tameshi | `01d586ddbc5fcd78659557c4e93a6ee8517b87d1` | `8006da5db27d2188ff2f3fc20ae402d0d30c7b5c5fcf9ca26c6793d2ff7e080f` | PASS | PASS | PASS (1) | PASS (7) | ADJ-07 ⇄ PASS | PASS | **PASS** |

Note 1 (OUT-007): the ADJ-05 **Next analysis recipient** cell is `kumitate`, while OUT-007's sibling is
`mori`. This is not a class mismatch: OUT-007 is mori's own `**Refuses:** dispatch and orchestration
mechanism (→ kumitate)` declaration, and the anchors-table proposition states exactly that
(`PROVINCE.md:127`). The ADJ class cell is `ADJ-05` on both sides (PASS); the sibling/recipient
divergence is the declared routing the anchor exists to show.

## Raw observed evidence (verbatim, `anchor-raw.txt` in the receipt dir)

```
kama e75cf680b534: exists=yes sha256=799432d748bd40bcf859de806cc2ef90df069da14c8e5c07bf72250ac411c7a6 line12=| served-model-id reconciliation | `GET /v1/models` vs `--alias` vs the configured model id |
kagi c2cab35bc92e: exists=yes sha256=4a346e2df81f7b2e649914d0d99da974d6c484caf12fed1c6bd530d106a78523 line3=**Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence
mado a4046a821608: exists=yes sha256=1b25bb1e980925b356663602d002c1c15307a0dfac8bfafd9988bd4d8df7464b line6=**Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules,
mori 91940fa339e3: exists=yes sha256=73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130 line8=pair); kill/OOM-related catalog-ID records and signal-11 coredump records from
kumitate 1770305fae20: exists=yes sha256=fcd69667a1027d5edd07a8ff0390a716a467aff92719071e33cb6157673b665f line3=**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime
mori 91940fa339e3: exists=yes sha256=73abda79bcb3ab26a069dcba1284cf62a0f257149b2ad39e5fb72ebe24bed130 line12=**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package,
kaidoku d1d981d2cc04: exists=yes sha256=63920930b77f9604c6ff7f5db8859344ef97fa50de9e4d0028897da4288859ac line3=**Domain:** reverse engineering of shipped artifacts with REA on this Linux
revenger cf02419276e5: exists=yes sha256=63acc3d033869f93f3e13da79e35023d86baa60b3f1d3b52861b019183b4b19f line3=Owns: reverse engineering of shipped artifacts — native binaries, managed
tameshi 01d586ddbc5f: exists=yes sha256=8006da5db27d2188ff2f3fc20ae402d0d30c7b5c5fcf9ca26c6793d2ff7e080f line7=**Owns:** the method, documented from the fleet's existing gates as primary
```

Note the qualifier on row 1 (OUT-002): the registry quote is `` `GET /v1/models` vs `--alias` vs the configured model id ``
(9 words, 56 chars) and the anchors-table cell carries that literal unchanged; line 12 of the kama blob
contains it as a substring. Nothing in the table is a paraphrase.

## Additional cross-checks (all PASS, all against frozen bytes)

- **ADJ table has 7 rows and 7 linked rows** (`PROVINCE.md:46-52`); every **Ownership source** cell is a
  backticked `OUT-0NN` id and none carries a `*.md:N[-M]` bare range (checked by regex over cells[5]:
  `ADJ-01`→`OUT-002`, `ADJ-02`→`OUT-003`, `ADJ-03`→`OUT-004`, `ADJ-04`→`OUT-005`,
  `ADJ-05`→`OUT-006`,`OUT-007`, `ADJ-06`→`OUT-008`,`OUT-009`, `ADJ-07`→`OUT-010`; bare_range=False for all).
- **Round-49 note** (`PROVINCE.md:297-320`) names the same nine-id mapping and preserves the old ranges
  only as history; each registry `province_pointer` literal is present in the frozen PROVINCE.md at
  lines 301 (`../kama-shokunin/PROVINCE.md:3-24`, `../kagi-shokunin/PROVINCE.md:3-6,10-17,32-34,54`),
  302 (`../mado-shokunin/PROVINCE.md:3-16`, `../mori-shokunin/PROVINCE.md:3-16`), 303
  (`../kumitate-shokunin/PROVINCE.md:3-6`, `../mori-shokunin/PROVINCE.md:12-16`), 304
  (`../kaidoku-shokunin/PROVINCE.md:3-6,88-100`, `../revenger-shokunin/PROVINCE.md:3-7,19-25`), 305
  (`../tameshi-shokunin/PROVINCE.md:3-18`).
- **Portable digest block** (`PROVINCE.md:137-146`): each `- OUT-0NN … @ <40-hex> sha256 <64-hex>` line
  carries the full pinned commit and exactly the sha256 I computed from the live sibling blob (9/9).
- **Quote/proposition length**: quote words 6–12 (max 25), proposition words 12–20 (max 25),
  `PROVINCE.md:311` claims "≤25-word quote" — holds.
- **Table locator path** equals `<sibling>-shokunin/PROVINCE.md` in all nine rows and the abbreviated
  commit is a 12-hex prefix of the pinned full commit; `git rev-parse --verify` resolved each prefix to
  exactly that full commit in its sibling repo (no ambiguity).

## What I did NOT do

- I did **not** run `tools/check-adjacency-table-r49.py` or `tools/check-adjacency-anchors.py`. The item
  asks for a re-derivation "independently of the counter", and both are selftest-bearing (5–10 CPU-minutes
  each); every dimension the counter's `anchors_ok`/`registry_ok` and the anchors checker's
  `evaluate()` test (commit exists via `git show`, live-blob sha256, heading section contains quote_line,
  exact quote substring, ≤25 words, pointer literal present, four publication fields id+quote/id+commit/
  id+sha256/heading in the anchors region) was reproduced here by hand from the frozen bytes and the live
  sibling objects, and all of them pass. `anchors_checker_rc == 0` therefore remains an unrun claim in
  this seat, not a claim I corroborated by execution.
- I did not run any census `--selftest`; no tool was installed or upgraded (nothing needed).

## Risks / residual notes

- **Pins are stale by design** (`PROVINCE.md:132`): every sibling repo HEAD has moved past its pinned
  commit (kama `7ee8cbdf160f…`, kagi `69b61db46be4…`, mado `3b55b6e91e40f…`, mori `325f7e639916…`,
  kumitate `14057f3e3899…`, kaidoku `c0112995817b…`, revenger `6defe31e4af9…`, tameshi `9cf0146b94dd…`).
  The anchors resolve because the pinned commits are still reachable; if a sibling ever garbage-collects
  or force-rewrites them, `git cat-file -e` fails and the anchor dies. The lane's `snapshot` files under
  `.ufo/waves/round-19/l1-capture/siblings/` are byte-identical copies (H PASS for all nine) so the
  quoted text survives even then, but the "read the live declaration before a handoff" rule stands.
- **ADJ-06 remains unresolved** (kaidoku vs revenger, `PROVINCE.md:51`, `:314-315`). Both OUT-008 and
  OUT-009 resolve as anchors; the recipient arbitration is still the integrator's call — an anchor
  resolving does not settle ownership.
- OUT-005 and OUT-007 share the same mori blob and digest (two different quotes in one pinned file); that
  is consistent, not a duplicate-id defect (ids differ, quotes differ, `quote_line` 8 vs 12).

## Receipts

`.ufo/waves/round-49/w1/R49ExecAnchorA/`: `verify2.py`, `verify2.out` (per-anchor JSON, all booleans),
`final.json` (enriched matrix incl. owner-lane and pointer fields), `anchor-raw.txt` (raw shell run
quoted above), `PROVINCE.frozen.md`, `adj-r19.json`, `verify.py`/`verify.out` (first pass, parser-bug
run retained only as provenance — its two `False` cells were my cell-parsing bug on the double-backticked
locator and the backtick-led OUT-002 quote cell, both re-derived PASS with the corrected parser).

Scratch `/fast/scratch/hyaku/tsukuroi-r49/R49ExecAnchorA/` removed after the copy.
