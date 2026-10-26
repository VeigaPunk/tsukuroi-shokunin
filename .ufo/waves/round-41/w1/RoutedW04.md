VERDICT: supports

# RoutedW04 — W04 delta (item R-4, round-40 closure §6.5)

Seat: leaf, item R-4. Claim measured: W04 advisories of the fleet census `validate` for lane `tsukuroi`,
now vs the wave's start capture (39 W04 at start). Result: **39 → 40, one new W04 — `S230` — and its
scope is a declared distinct scope**; the live run still exits 0 with no E-codes.

Nothing in the lane, the fleet repo or the host was written. Working files lived in
`/fast/scratch/hyaku/tsukuroi-r41/RoutedW04/` (removed at the end); receipts are in
`.ufo/waves/round-41/w1/RoutedW04/`.

## 1. Measurement now

Command (the item's command, verbatim; `TMPDIR` under the scratch dir):

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

Observed: **exit 0**; 41 stdout lines = **40 W04** + `tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`;
no `E01`-`E12` line of any kind (0 lines matching `\tE[0-9]+\t`).
Receipt `RoutedW04/census-now.txt`, sha256 `29ae7e9dac9d3d0085f0534ce8243119717f0327c882ab082b21ff514fd37732`.

Content measured: lane HEAD `71851d636ab1bffaf8fee5016617c88878a666f1` (`git log -1 --format='%H %cI %s'`),
and `git status --porcelain -- corpus/SOURCES.md` printed nothing, so the census read the committed corpus.

Tool identity (why the delta cannot be a tool change): `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, fleet path clean
(`git -C /home/vgpnk/Projects/shokunin status --porcelain -- scripts/sources-census.sh` empty) at fleet commit
`f47ad6ba8d306f8125597401cb2ce45c1297a593`.

## 2. Delta: exactly one new W04, none removed

`diff` of the W04 lines only (before → now), receipt `RoutedW04/w04-delta.diff`:

```
39a40
> tsukuroi	W04	S230 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c across scopes
```

New W04 list (complete — one entry):

| row | W04 line | earlier row with the same normalized URL |
|---|---|---|
| `S230` | `tsukuroi	W04	S230 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c across scopes` | `S213`, `corpus/SOURCES.md:222` |

No W04 line was removed or re-identified: all 39 start lines are byte-identical in the live run
(`diff` above shows one `a`-side hunk, no `d`/`c`).

## 3. Declared distinct scope: yes

Four independent reads agree that the duplicate is two questions on one file, not two citations of one
question:

1. **The row declares it.** `corpus/SOURCES.md:239`, scope cell (field 5) of `S230`:
   "Which package root members libalpm keeps in the local database at install, **distinct from S213's commit
   order scope**". The compared row, `corpus/SOURCES.md:222` `S213`, scope cell: "Per-package add/upgrade order
   inside the commit: scriptlets, extraction, log line, ldconfig".
2. **The source windows are disjoint in the same pinned revision.** Both rows name snapshot sha256
   `fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1`, which is
   `.ufo/waves/round-41/frozen/src/SHA256SUMS:2` (`sha256sum add.c` re-ran to the same digest, 695 lines).
   `S230` cites `extract_db_file` 168-189 and dot-file dispatch 204-206 — read at
   `.ufo/waves/round-41/frozen/src/add.c:168-189` (`static int extract_db_file(…)` … `.INSTALL`/`.CHANGELOG`/
   `.MTREE` mapping … `reserve all files starting with '.'`) and `add.c:204-206` (`if(*entryname == '.')` →
   `return extract_db_file(…)`). `S213` cites `add.c:466-474` (pre_install/pre_upgrade block),
   `616-648` (`alpm_logaction(… "installed %s (%s)\n")` band) and `655-695` (`_alpm_upgrade_packages`) —
   disjoint from 168-206.
3. **Different consumers.** `S230` used-by `corpus/knowledge/alpm-package-anatomy-r41.md` (this round's entry,
   rule PA4, which quotes `S230 add.c:168-189`); `S213` used-by `corpus/knowledge/pacman-transaction-order-r39.md`.
4. **It is this round's declared prose.** `S230` is one of the ten rows the round-41 declaration names
   (`SCORECARD.md:2454`, claim C2: "rows S227-S236 opened this round"; PA4 is "the three members install keeps in
   the local database"). `git show 9cc9aa77:corpus/SOURCES.md | grep -c '^| S230 '` = 1;
   `git show 0e5805a:corpus/SOURCES.md | grep -c '^| S230 '` = 0.

W04 is by construction a scope-column difference, not a URL-only accident: the census emits W04 when the URL
was seen before under a *different* scope key and E04 when the same URL repeats *inside* the same scope
(`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:644-651`), and its own header calls W04 a warning
that "do not affect clean lanes" (`:33`). The live run's exit 0 agrees.

## 4. Attribution controls (scratch copy of the corpus, no lane writes)

Three `validate` runs against a scratch copy, receipt `RoutedW04/attribution-controls.txt`:

| variant | change to the copy | W04 | E04 |
|---|---|---|---|
| `base` | verbatim copy of the live corpus (236 rows) | **40** | 0 |
| `noS230` | `S230` row deleted | **39** | 0 |
| `noscope` | `S230` kept, its scope cell replaced by `S213`'s exact scope text | **39** | **1** |

- `base` reproduces the live W04 set exactly (diff after relabelling the lane column: identical), so the copy is
  a faithful instrument.
- `noS230` returns the start count, so **the whole delta is `S230`**.
- `noscope` replaces the W04 with
  `E04 S230 duplicate url gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c within scope Per-package add/upgrade order inside the commit: scriptlets, extraction, log line, ldconfig` —
  i.e. the warning exists **because the scopes differ**; identified scopes collapse it into a within-scope error.
- The copies also print 381 `E11` lines each (used-by paths resolved against the copied root). That is a copy
  artifact and is absent from the live run; it is recorded in the receipt so the control is not misread as a
  corpus defect.

## 5. Exact line for the report's Sources & frontier section

Use this (one line, W04 delta included rather than "W04 advisories only", which was round-40 routed defect §6.5):

```
Sources & frontier: `corpus/SOURCES.md` 226 → 236 rows (S227-S236 added, all tier A / mined; tiers A211/B5/C10 → A221/B5/C10, mined 200/queued 5/rejected 21 → 210/5/21, no old row edited — `scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin tsukuroi`, row set from `git diff 0e5805a 71851d6 -- corpus/SOURCES.md`); `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` exits 0 with W04 39 → 40 — the one new same-URL row is S230 (`libalpm/add.c` beside S213), a declared distinct scope (database-member retention `add.c:168-189`/`204-206` vs commit order `add.c:466-474`/`616-648`/`655-695` in the same pinned snapshot `fd313629…`), and no new E-codes.
```

If the line carries only the census clause, drop the leading `corpus/SOURCES.md` parenthesis and keep:
"`… validate … exits 0 with W04 39 → 40 — the one new same-URL row is S230 (libalpm/add.c beside S213), a
declared distinct scope (database-member retention add.c:168-189/204-206 vs commit order
add.c:466-474/616-648/655-695 in the same pinned snapshot fd313629…), and no new E-codes."

## 6. Limits / not done

- The start capture `.ufo/waves/round-41/before/sources-census-start.txt` carries no command header and no tool
  digest (41 lines, 39 W04 + `ok` + `exit=0`) — the same shape note the scorecard already records
  (`SCORECARD.md:2394`). I did not re-run the census at the base commit (that would need a checkout/copy of the
  lane at `0e5805a`; a clone would only re-derive the row set, which `git show` already gives). The comparison
  therefore rests on the tool being unchanged, which I verified only for *now* (clean fleet path, recorded sha256).
- I ran no C1 or C2 counter, no selftest, no build/lint/test; those belong to other seats and to the parent's gate.
- Row-level correctness of `S230` beyond its scope distinctness (that `add.c:168-189` really supports PA4) is the
  C2 reviewer's read; I checked the cited lines exist and say what the row quotes, nothing further.

## 7. Tool installs

None. No package, service or host change; the census is an existing fleet script used read-only
(`validate`/`census` only, no `--out`).

## 8. Files written

- `.ufo/waves/round-41/w1/RoutedW04.md` (this report)
- `.ufo/waves/round-41/w1/RoutedW04/census-now.txt` (sha256 `29ae7e9d…`, exact live stdout)
- `.ufo/waves/round-41/w1/RoutedW04/w04-delta.diff` (sha256 `27dc8432…`, W04-line diff vs the start capture)
- `.ufo/waves/round-41/w1/RoutedW04/attribution-controls.txt` (sha256 `cc9dcbc6…`, the three control runs)
