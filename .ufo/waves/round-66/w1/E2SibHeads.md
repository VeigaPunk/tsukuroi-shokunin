# Seat E2SibHeads — C2-LOCATE (round 66, wave w1)

**Verdict: C2 achieved on the location axis — 10/10 ownership anchors located at each sibling's LIVE HEAD, 0 unlocated, 0 unreachable.**

## Files written (relative to `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`)

| path | role |
|---|---|
| `.ufo/waves/round-66/probes/c2-sibling-heads.txt` | receipts (§A HEAD + `cat-file -t`, §B blob sha256, §C per-anchor locate, §D register-vs-live, §E full-quote literal, §F rule) |
| `.ufo/waves/round-66/drafts/c2-anchors-live.tsv` | 10 data rows, header `AR_n OUT_id sibling live_head blob_sha256 status line path` |
| `.ufo/waves/round-66/drafts/e2-summary.md` | counts, counting commands with output, normalisation rule |
| `.ufo/waves/round-66/w1/E2SibHeads.md` | this report |

No tracked file touched; no write into any sibling repo; read-only git verbs only (`rev-parse`, `cat-file`, `show`).

## Behaviour / evidence

Authority read first: `corpus/knowledge/adjacency-anchors-r19.json` (register). All 10 anchors target `PROVINCE.md` across 8 sibling repos (mori ×3: OUT-001/005/007).

Locator procedure per item step 3: `git -C <D> rev-parse HEAD` → `git -C <D> cat-file -t <HEAD>` (all `commit`, rc=0) → `git -C <D> show <HEAD>:PROVINCE.md | sha256sum` → whitespace/marker-normalised whole-quote substring match with the 1-based line of the first matching line.

**Normalisation rule (only `**` and backticks removed, no other folding):** strip `**`, strip backticks, collapse whitespace runs to one space, strip; case-sensitive substring test line-by-line, then across a contiguous span of ≤12 lines as fallback. Probe §E shows OUT-001 and OUT-009 also match *literally* without normalisation, i.e. the rule is not load-bearing for the located verdicts.

### Live results (rows exactly as they appear in `c2-anchors-live.tsv`)

```
AR_n	OUT_id	sibling	live_head	blob_sha256	status	line	path
AR1	OUT-001	mori	84c6cbc3b47c536a504aaee329c77897d389935e	2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838	located	9	PROVINCE.md
AR2	OUT-002	kama	6035e952c2521999e192d6f236331f265ac98392	f0aaae9ccfd0ecb6641ad1646934f4ff5555fcc45d2e397670b2eb5ff083e8a6	located	12	PROVINCE.md
AR3	OUT-003	kagi	91f7752ba551092eef20f6bd43d6dd798dc88ba0	0bbf19b3019e780269259b1acbbd45fcb9a53139fe6337609e7bd6448b364edd	located	3	PROVINCE.md
AR4	OUT-004	mado	524fa1f90b1f2de44b3019bacf833d54e0af13a0	01c55ed921b1eb9ebb571f5801525d6c1b49576bf3a1d9a28ca9a4c083943a17	located	6	PROVINCE.md
AR5	OUT-005	mori	84c6cbc3b47c536a504aaee329c77897d389935e	2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838	located	8	PROVINCE.md
AR6	OUT-006	kumitate	3c369336218329e30248b5d69c41348c02658169	fa9a63a8f62331595858868496c0516df04dfea456b18351d1a01be062ae47ed	located	3	PROVINCE.md
AR7	OUT-007	mori	84c6cbc3b47c536a504aaee329c77897d389935e	2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838	located	12	PROVINCE.md
AR8	OUT-008	kaidoku	c7fe6898e9a8b3ff04486b4a1d672e9db37610c9	50b6c259beb6816e26b3af91e44e5317f82e40eaf94993701781221ef7bb98c4	located	3	PROVINCE.md
AR9	OUT-009	revenger	5915ad8d71c19ad377829d130ba1c35445eb32a4	c49f6d1d11441728a9a9ed9abed7444837cf2cf0ee569681ad48340187c6f502	located	3	PROVINCE.md
AR10	OUT-010	tameshi	f20ba482c7441d4c75818e7cd8a3165fee7821a1	0031aae86d34e39c753ac39ff4daf95a13761f9ba3992f221cc54c6c3bbb5a26	located	7	PROVINCE.md
```

Counts (`$ awk -F'\t' 'NR>1{c[$6]++} END{for(k in c) print k, c[k]}' …/c2-anchors-live.tsv`): `located 10`, rc=0; row count `10`.

### Paste-ready C2 row form (for `corpus/knowledge/adjacency-recheck-r66.md`)

`locator` = `<path>:<line>` from the TSV. Nothing here is a new observation; it is the same 10 rows re-serialised in the frozen predicate's shape.

```
| AR1  | OUT-001 | mori      | 84c6cbc3b47c536a504aaee329c77897d389935e | 2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838 | located | PROVINCE.md:9 |
| AR2  | OUT-002 | kama      | 6035e952c2521999e192d6f236331f265ac98392 | f0aaae9ccfd0ecb6641ad1646934f4ff5555fcc45d2e397670b2eb5ff083e8a6 | located | PROVINCE.md:12 |
| AR3  | OUT-003 | kagi      | 91f7752ba551092eef20f6bd43d6dd798dc88ba0 | 0bbf19b3019e780269259b1acbbd45fcb9a53139fe6337609e7bd6448b364edd | located | PROVINCE.md:3 |
| AR4  | OUT-004 | mado      | 524fa1f90b1f2de44b3019bacf833d54e0af13a0 | 01c55ed921b1eb9ebb571f5801525d6c1b49576bf3a1d9a28ca9a4c083943a17 | located | PROVINCE.md:6 |
| AR5  | OUT-005 | mori      | 84c6cbc3b47c536a504aaee329c77897d389935e | 2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838 | located | PROVINCE.md:8 |
| AR6  | OUT-006 | kumitate  | 3c369336218329e30248b5d69c41348c02658169 | fa9a63a8f62331595858868496c0516df04dfea456b18351d1a01be062ae47ed | located | PROVINCE.md:3 |
| AR7  | OUT-007 | mori      | 84c6cbc3b47c536a504aaee329c77897d389935e | 2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838 | located | PROVINCE.md:12 |
| AR8  | OUT-008 | kaidoku   | c7fe6898e9a8b3ff04486b4a1d672e9db37610c9 | 50b6c259beb6816e26b3af91e44e5317f82e40eaf94993701781221ef7bb98c4 | located | PROVINCE.md:3 |
| AR9  | OUT-009 | revenger  | 5915ad8d71c19ad377829d130ba1c35445eb32a4 | c49f6d1d11441728a9a9ed9abed7444837cf2cf0ee569681ad48340187c6f502 | located | PROVINCE.md:3 |
| AR10 | OUT-010 | tameshi   | f20ba482c7441d4c75818e7cd8a3165fee7821a1 | 0031aae86d34e39c753ac39ff4daf95a13761f9ba3992f221cc54c6c3bbb5a26 | located | PROVINCE.md:7 |
```

## Retained evidence (exact commands, verbatim outputs)

Probe file §A — HEAD and object type, all 8 rc=0, all types `commit`:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin rev-parse HEAD
84c6cbc3b47c536a504aaee329c77897d389935e
rc=0
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin cat-file -t 84c6cbc3b47c536a504aaee329c77897d389935e
commit
rc=0
```

(same shape for kama `6035e95…`, kagi `91f7752…`, mado `524fa1f…`, kumitate `3c36933…`, kaidoku `c7fe689…`, revenger `5915ad8…`, tameshi `f20ba48…` — full text in probe §A.)

Probe file §B — blob sha256, all rc=0, e.g.:

```
$ git -C /home/vgpnk/Projects/shokunin/mori-shokunin show 84c6cbc3b47c536a504aaee329c77897d389935e:PROVINCE.md | sha256sum
2af29312d28727b4dc91236b6f2ce188c0b721a3759e6a8cdaf73f98f4919838  -
rc=0
```

Probe file §C — line numbers, all rc=0, e.g.:

```
$ grep -n -F -- '**Owns (surfaces):** `~/.config/hypr/`' /fast/scratch/hyaku/tsukuroi-r66/E2SibHeads/C-mado.md
6:**Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules,
rc=0   # OUT-004 raw literal incl. bold+backticks
```

```
$ grep -n -F -- '**Refuses:** dispatch and orchestration mechanism' /fast/scratch/hyaku/tsukuroi-r66/E2SibHeads/C-mori.md
12:**Refuses:** dispatch and orchestration mechanism (→ kumitate); OS package,
rc=0   # OUT-007 raw literal incl. bold
```

```
$ grep -n -F -- 'Owns: reverse engineering of shipped artifacts' /fast/scratch/hyaku/tsukuroi-r66/E2SibHeads/C-revenger.md
3:Owns: reverse engineering of shipped artifacts — native binaries, managed
rc=0   # OUT-009
```

## Risks / caveats for the L1

1. **Register commits are stale, register text is not.** Every sibling HEAD differs from `sibling_commit` in `adjacency-anchors-r19.json` and every live `PROVINCE.md` blob sha256 differs from `sibling_blob_sha256` (probe §D). Cite the live HEADs in this report, not the r19 commits; text and line numbers are unchanged.
2. **OUT-009 has no bold markers at HEAD.** Register quote `Owns: reverse engineering of shipped artifacts` matches revenger `PROVINCE.md:3` literally, but that line is *not* a `**Owns:**` line — it reads `Owns: reverse engineering of shipped artifacts — native binaries, managed`. The proposition still holds; do not record a bolded `**Owns:**` locator, it would not grep at HEAD.
3. **OUT-005's register quote is a mid-line fragment.** It begins `pair); kill/OOM-related …` — the live line 8 is preceded by `pair); `, i.e. the quote starts inside a sentence inherited from line 7. Located at line 8 as the first line containing the quote; a locator of `PROVINCE.md:8` is correct for the quote, but a reader expecting a sentence start at that line will not find one.
4. **mori carries 3 of the 10 anchors on one file** (lines 8, 9, 12). AR5/AR1/AR7 are distinct lines, so no collision, but they share HEAD `84c6cbc…` and blob `2af2931…`; row-level uniqueness in the recheck table comes from OUT id, not from head/blob.
5. **This seat verified only location.** No claim is made about whether the quoted text is *true* of the sibling's live behavior, and no lane gate, census, or selftest was run (L1 owns those).
6. **Scratch deleted.** `/fast/scratch/hyaku/tsukuroi-r66/E2SibHeads` is removed before yield; probe §C/§E reference `C-*.md` files that were in it — every matched line and every sha256 is reproduced verbatim in the probe file itself, so the probe is self-contained after scratch removal.
