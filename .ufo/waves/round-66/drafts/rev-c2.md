# C2-ATTACK — independent locator re-derivation (seat R2RevC2)

UTC: 2026-11-03T21:02:58Z (scratch created: `S=/fast/scratch/hyaku/tsukuroi-r66/R2RevC2; mkdir -p "$S"` → rc=0)
Seat: R2RevC2 (reviewer), tsukuroi lane round 66 w1, base c68bfe97. Item: C2-ATTACK (targets claim C2, SCORECARD.md "Round 66 — declaration" C2 row, :4917).
Method: different from E2SibHeads (`git show <HEAD> | grep`) — here `git -C <sibling> grep -n -F -e '<fragment>' HEAD -- <path>` runs inside each sibling repo at its live HEAD; `git rev-parse HEAD` binds head identity. Read-only git only; no clone; no writes to any sibling repo.
Scratch /fast/scratch/hyaku/tsukuroi-r66/R2RevC2 deleted after these receipts were written.

## Register entries read (corpus/knowledge/adjacency-anchors-r19.json)

- OUT-004 (json lines 48–59): sibling `mado`, sibling_path `PROVINCE.md`, r19 `sibling_commit` a4046a8216080d4004de3f268c62cf142095ac07, quote `**Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules,`, quote_line 6.
- OUT-006 (json lines 74–85): sibling `kumitate`, r19 commit 1770305fae20826b39905a8251ddeca6b4957ac4, quote `**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime`, quote_line 3.
- OUT-008 (json lines 100–111): sibling `kaidoku`, r19 commit d1d981d2cc041dda4656c5b01d2c8445d8d17124, quote `**Domain:** reverse engineering of shipped artifacts with REA on this Linux`, quote_line 3.

## Attack 1 — OUT-004 (mado) locator at live HEAD

```
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin rev-parse HEAD
524fa1f90b1f2de44b3019bacf833d54e0af13a0
rc=0
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin grep -n -F -e '**Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules,' HEAD -- PROVINCE.md
HEAD:PROVINCE.md:6:**Owns (surfaces):** `~/.config/hypr/` (hyprland.conf, keybinds, rules,
rc=0
```

Comparison vs `drafts/c2-anchors-live.tsv` row `AR4` (live_head 524fa1f90b1f2de44b3019bacf833d54e0af13a0, status located, line 6, PROVINCE.md): head identical, line 6 == 6, path identical. Register quote_line 6 matches the live line too.
**AGREE** (item C2).

## Attack 2 — OUT-006 (kumitate) locator at live HEAD

```
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin rev-parse HEAD
3c369336218329e30248b5d69c41348c02658169
rc=0
$ git -C /home/vgpnk/Projects/shokunin/kumitate-shokunin grep -n -F -e 'scopes OMP task/hub, ufo-fsd scripts &' HEAD -- PROVINCE.md
HEAD:PROVINCE.md:3:**Domain:** orchestration & tooling — scopes OMP task/hub, ufo-fsd scripts & runtime
rc=0
```

Comparison vs TSV row `AR6` (live_head 3c369336218329e30248b5d69c41348c02658169, located, line 3, PROVINCE.md): head identical, line 3 == 3. Register quote_line 3 matches the live line too.
**AGREE** (item C2).

## Attack 3 — OUT-008 (kaidoku) locator at live HEAD

```
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD
c7fe6898e9a8b3ff04486b4a1d672e9db37610c9
rc=0
$ git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin grep -n -F -e 'reverse engineering of shipped artifacts with' HEAD -- PROVINCE.md
HEAD:PROVINCE.md:3:**Domain:** reverse engineering of shipped artifacts with REA on this Linux
rc=0
```

Comparison vs TSV row `AR8` (live_head c7fe6898e9a8b3ff04486b4a1d672e9db37610c9, located, line 3, PROVINCE.md): head identical, line 3 == 3. Register quote_line 3 matches the live line too.
**AGREE** (item C2).

Note: register r19 commits differ from the live heads (mado a4046a82… → 524fa1f9…; kumitate 1770305f… → 3c369336…; kaidoku d1d981d2… → c7fe6898…) — expected r19→r66 drift; the TSV pins the live head, as the C2 predicate ("40-hex live HEAD") requires.

## Attack 4 — frozen row-shape regex is shape-only (fabricated HEAD passes)

Fixture (scratch `fab-rows.md`, 3 fabricated rows, verbatim):

```
| AR04 | OUT-004 | mado | 1111111111111111111111111111111111111111 | aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa | located | PROVINCE.md:6 |
| AR06 | OUT-006 | kumitate | 0000000000000000000000000000000000000000 | bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb | located | PROVINCE.md:3 |
| AR08 | OUT-008 | kaidoku | 1234567890abcdef1234567890abcdef12345678 | cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc | located | PROVINCE.md:3 |
```

```
$ grep -nE '^\| AR[0-9]+ \| OUT-0[0-9]{2} \| [a-z]+ \| [0-9a-f]{40} \| [0-9a-f]{64} \| located \|' /fast/scratch/hyaku/tsukuroi-r66/R2RevC2/fab-rows.md; echo "grep -E rc=$?"
1:| AR04 | OUT-004 | mado | 1111111111111111111111111111111111111111 | aaaa…64a | located | PROVINCE.md:6 |
2:| AR06 | OUT-006 | kumitate | 0000000000000000000000000000000000000000 | bbbb…64b | located | PROVINCE.md:3 |
3:| AR08 | OUT-008 | kaidoku | 1234567890abcdef1234567890abcdef12345678 | cccc…64c | located | PROVINCE.md:3 |
grep -E rc=0
$ grep -cE '<same regex>' /fast/scratch/hyaku/tsukuroi-r66/R2RevC2/fab-rows.md
3
```

All 3 fabricated rows match, including rows whose 40-hex HEAD (1111…1, 0000…0, 1234567890abcdef1234567890abcdef12345678) is not a real commit in any sibling repo. Recorded finding: the frozen row regex alone cannot catch a fabricated HEAD — shape-validity is necessary, not sufficient; every row additionally needs an object-existence check.

## Attack 5 — head reality check: `git cat-file -e` per row

```
$ for pair in 'mori 84c6cbc3b47c536a504aaee329c77897d389935e' 'kama 6035e952c2521999e192d6f236331f265ac98392' 'kagi 91f7752ba551092eef20f6bd43d6dd798dc88ba0' 'mado 524fa1f90b1f2de44b3019bacf833d54e0af13a0' 'kumitate 3c369336218329e30248b5d69c41348c02658169' 'kaidoku c7fe6898e9a8b3ff04486b4a1d672e9db37610c9' 'revenger 5915ad8d71c19ad377829d130ba1c35445eb32a4' 'tameshi f20ba482c7441d4c75818e7cd8a3165fee7821a1'; do set -- $pair; git -C "/home/vgpnk/Projects/shokunin/$1-shokunin" cat-file -e "$2" && echo "$1 $2 rc=0 exists" || echo "$1 $2 rc=$? MISSING"; done
mori 84c6cbc3b47c536a504aaee329c77897d389935e rc=0 exists
kama 6035e952c2521999e192d6f236331f265ac98392 rc=0 exists
kagi 91f7752ba551092eef20f6bd43d6dd798dc88ba0 rc=0 exists
mado 524fa1f90b1f2de44b3019bacf833d54e0af13a0 rc=0 exists
kumitate 3c369336218329e30248b5d69c41348c02658169 rc=0 exists
kaidoku c7fe6898e9a8b3ff04486b4a1d672e9db37610c9 rc=0 exists
revenger 5915ad8d71c19ad377829d130ba1c35445eb32a4 rc=0 exists
tameshi f20ba482c7441d4c75818e7cd8a3165fee7821a1 rc=0 exists
```

All 8 distinct heads across the 10 TSV rows (AR1/AR5/AR7 share the mori head) exist as objects → all 10 rows' HEAD columns are real objects.

```
$ git -C /home/vgpnk/Projects/shokunin/mado-shokunin cat-file -e 1111111111111111111111111111111111111111; echo "fabricated-HEAD cat-file -e rc=$?"
fabricated-HEAD cat-file -e rc=1
```

The fabricated head fails (`rc=1`), the real TSV heads pass (`rc=0`): `cat-file -e` is the discriminator the regex lacks.

## Disagreements

None. No DISAGREE found in any of the three re-derived locators, their head identities, or the 10-row head-existence check.

## Verdict

C2-LOCATORS-AGREE
