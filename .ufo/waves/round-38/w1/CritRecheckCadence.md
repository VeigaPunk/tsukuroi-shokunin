VERDICT: defect-found

# R-8 — freshness design of the C2 recheck line (`pacman-hook-order-r38.md:3`)

Seat: CritRecheckCadence (leaf, read-only on lane content; no host mutation, no package action,
no sudo). Item judged: is the live-drift command in the C2 entry's `recheck:` line sufficient and
runnable as written; how soon the table goes stale; the minimal recheck sentence and cadence.

## Counterexample (the one that decides the item)

The live-drift command, *as written and as an operator would use it against the MANIFEST* (i.e. as
a set, sorted), is blind to a same-name override swap between the two hook directories — the exact
situation the table's headline host consequence encodes (HO2, `pacman-hook-order-r38.md:22`; row 26,
`:69`, `90-mkinitcpio-install.hook` dir `etc`, exec `limine-mkinitcpio-install`).

Fixture: byte copies of both capture directories (70 files), MANIFEST = `sort -k2 MANIFEST.sha256`;
then swap the contents of `usr-share-libalpm-hooks/90-mkinitcpio-install.hook` and
`etc-pacman.d-hooks/90-mkinitcpio-install.hook` (the effective hook changes: the distro script now
wins the `etc` search, the operator override now sits in the shadowed directory):

```
live, unprefixed sorted (as written)  : 8784dcee8f58bceb1ecf13197659a1aad359985efe51673f0504062de5b52dba
fx3 swapped, unprefixed   (as written): 8784dcee8f58bceb1ecf13197659a1aad359985efe51673f0504062de5b52dba   <- IDENTICAL
live, dir-prefixed sorted             : 54225ca997acd2b4b9c8965c68f8325592d0bdc387b673a4c69270bfc7ccee43
fx3 swapped, dir-prefixed             : c2af86f1e908b2d19066ddb745d5a651e39e1c2ba191af4c00bc964c0dd94800   <- drift seen
```
(`.ufo/waves/round-38/w1/CritRecheckCadence/r2-drift-and-swap.txt`)

Cause: `sha256sum *.hook` prints bare basenames and the two globs are concatenated with no directory
label, while the MANIFEST is directory-prefixed (`etc-pacman.d-hooks/…`, `usr-share-libalpm-hooks/…`).
So (a) the command's output cannot be diffed against the MANIFEST at all as written — 142 diff lines
for a file set that is byte-identical — and (b) `90-mkinitcpio-install.hook` appears twice in the
output (verbatim lines 37 and 68, hashes `9fc607e8…` and `a0689d02…`) with nothing saying which
directory each hash came from. Any hash-only comparison therefore loses exactly the HO2 fact.

## Evidence

### 1. The counter cannot turn red from host drift (structural, and run)
- `tools/check-hook-order-r38.py:48` `CAPTURE = Path('.ufo/waves/round-38/frozen/hooks-capture')`,
  `:99 def expected_rows(repo)` reads only `repo / CAPTURE`, `:193 exp = expected_rows(repo)`.
  `grep -n 'usr/share/libalpm\|pacman.d/hooks' tools/check-hook-order-r38.py` → one hit, the docstring
  at `:15`. Nothing in the counter opens a live hook directory.
- Runs (`…/CritRecheckCadence/r1-counter-revisions.txt`): `--revision 1fe28e725be47364fc6033bf81ecabc66ee5fe62`
  → `rows_expected 69, rows_matched 69, result PASS`; `--revision 5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf`
  (wave tip) → PASS; `--revision 8bd001f58bfda29c92d90d2a7a413825c0ca9fcb` (base) → `entry_present false,
  result FAIL`. So the counter red-lights entry-vs-capture mismatch only: a pacman upgrade that adds,
  removes or rewrites a hook leaves it green forever. Freshness therefore rests entirely on the
  `recheck:` line and on S212's `30d` (`corpus/SOURCES.md:221`).

### 2. The recheck line is not runnable as written
`corpus/knowledge/pacman-hook-order-r38.md:3` says `--revision <REV>`. Run literally:
```
$ python3 tools/check-hook-order-r38.py --revision '<REV>'
{"counter": "check-hook-order-r38", "error": "E-REVISION-INVALID revision: 7-64 hex commit required", "exit": 2}
$ python3 tools/check-hook-order-r38.py --revision HEAD
{"counter": "check-hook-order-r38", "error": "E-REVISION-INVALID revision: 7-64 hex commit required", "exit": 2}
```
The lane convention is a concrete binding — `btrfs-repair-r31.md:3` uses
`--revision "$(git rev-parse HEAD)"`, `adjacency-anchors-r19.md:3` defines `<REV>` in-line. The
obvious expansions (`HEAD`, a branch, a tag) are rejected by `tools/_revision.py`; only 7–64 hex works,
which the line does not say.

### 3. Live drift today: none — the capture is current (so this is prospective, not a live error)
```
$ { (cd /usr/share/libalpm/hooks && sha256sum *.hook | sed 's|  |  usr-share-libalpm-hooks/|'); \
    (cd /etc/pacman.d/hooks && sha256sum *.hook | sed 's|  |  etc-pacman.d-hooks/|'); } | sort -k2 | sha256sum
54225ca997acd2b4b9c8965c68f8325592d0bdc387b673a4c69270bfc7ccee43
$ sort -k2 .ufo/waves/round-38/frozen/hooks-capture/MANIFEST.sha256 | sha256sum
54225ca997acd2b4b9c8965c68f8325592d0bdc387b673a4c69270bfc7ccee43
```
70/70 files, byte-identical; `find … -newermt '2026-10-26 04:11:58'` → 0 hook files; MANIFEST sha256
`da07f434…` matches `tools/check-hook-order-r38.py:49`. Credit where due: the line *does* use hashes,
which is the right signal (see 5).

### 4. No HookDir surface in the line
HO2's consequence depends on `HookDir=/etc/pacman.d/hooks/` only. `grep -n HookDir /etc/pacman.conf` →
no line (compiled default); `pacman-conf HookDir` → `/etc/pacman.d/hooks/`. Adding a second `HookDir`
or repointing it changes the effective set and the row order with zero bytes changing in either
checked directory — and the `recheck:` line has no command that re-reads that surface.

### 5. How soon the table goes stale (measured 2026-10-26)
(`…/CritRecheckCadence/r3-churn.txt`)
- Ages of the 70 hook files: **min 13 d, q25 20 d, median 28 d, q75 63 d, max 859 d**; 35/70 rewritten
  within 30 d, 54/70 within 90 d, 64/70 within 365 d; 0 within 7 d.
- The 35 files touched in 30 d carry **10 distinct mtime dates** (2026-09-27, 09-29, 10-01, 10-02,
  10-03, 10-05, 10-06, 10-08, 10-09, 10-12) — a hook rewrite roughly every third day.
- Name-set change inside the same window: `[2026-10-03T17:44:23-0300] [ALPM] installed kernel-modules-hook (0.1.7-3)`,
  `[2026-10-03T17:45:33-0300] [ALPM] installed limine-mkinitcpio-hook (1.36.0-1)`; the latter is what
  supplies `10-limine-snapper-lock`, `60-limine-mkinitcpio-remove-pre`, `80-limine-efi-deploy`,
  `90-limine-mkinitcpio-remove-post` and the `etc` `90-mkinitcpio-install.hook`. An entry captured a
  month before 2026-10-26 would have missed ≥5 rows and shifted every later `pos` in both phases.
- mtime is not a usable staleness signal: `/etc/pacman.d/hooks` has dir mtime `2026-10-20 09:16:42.046312437`
  (same second as `[2026-10-20T09:16:42-0300] [ALPM] upgraded limine-mkinitcpio-hook (1.38.0-1.1 -> 1.40.0-2)`),
  while `90-mkinitcpio-install.hook` keeps `2026-10-08 11:51:33.000000000` — an entry was created/renamed
  in the operator hook dir six days before the capture, leaving no file-mtime trace.

**Staleness horizon:** the table's content columns (`exec`, `needs`, `abort`) and its `pos` column are
the fragile part; with a rewrite event ≈ every 3 days, a 30-day recheck alone allows up to ~10
drift-inducing upgrades before anyone looks. The *order* columns move only on install/remove (≈ monthly
here). `30d` for S212 is the right *re-mine* period — it matches the measured rewrite timescale
(median age 28 d) — but it cannot be the only guard.

### 6. The cadence is not stated in the line, so the lane's cadence count cannot see it
Lane convention puts the cadence first (`boot-writers-r19.md:3`, `boot-plane.md:317`,
`adjacency-anchors-r19.md:3`: `recheck: 30d; procedure: …`), and `SCORECARD.md:193` measures freshness
as "per-note last `^recheck:` date/cadence count". `pacman-hook-order-r38.md:3` carries no `30d` and no
date, so the note is invisible to that count and the 30 d trigger survives only in `corpus/SOURCES.md:221`.

## Impacted axes

- **freshness (primary).** The recheck is unusable as written (2), the drift comparison is blind to the
  override swap (counterexample), the HookDir surface is unchecked (4), and the cadence the freshness
  count reads is absent (6). No measured value is wrong today (3).
- **C2 (secondary).** The 69 rows, the predicates and the after-receipt stand — this is a repair of the
  entry's line 3 only. It must **not** be "fixed" by making the counter read live state: that would make
  a frozen-capture depth counter host-dependent and non-reproducible, and would convert a depth claim
  into a freshness claim it does not make.

## Smallest safe correction

Replace **only** `corpus/knowledge/pacman-hook-order-r38.md:3`. No row, no SOURCES row, no counter
change; the capture and its MANIFEST stay as they are. Exact text proposed:

```
recheck: 30d (S212) and on-release of pacman 54d9411 (S208-S211); procedure: from the lane root `python3 tools/check-hook-order-r38.py --revision "$(git rev-parse HEAD)"` re-derives the 69 rows from the frozen capture; freshness: `{ (cd /usr/share/libalpm/hooks && sha256sum *.hook | sed 's|  |  usr-share-libalpm-hooks/|'); (cd /etc/pacman.d/hooks && sha256sum *.hook | sed 's|  |  etc-pacman.d-hooks/|'); } | sort -k2 | sha256sum` must print `54225ca997acd2b4b9c8965c68f8325592d0bdc387b673a4c69270bfc7ccee43` and `pacman-conf HookDir` must stay `/etc/pacman.d/hooks/`; any other hash, a changed HookDir, or a pacman release means re-capture, update the MANIFEST and re-run the counter before citing a row.
```

Why this text and nothing more:
- One command, one constant, no judgement call: run it, compare 64 hex digits. Verified today: prints
  `54225ca997ac…ccee43`; on the swapped fixture prints `c2af86f1…` (drift caught).
- The prefixing is what restores the HO2 signal; `sort -k2` before hashing makes directory order
  irrelevant, so the result does not depend on which glob ran first.
- `--revision "$(git rev-parse HEAD)"` replaces the non-runnable `<REV>` with the form already in
  `btrfs-repair-r31.md:3`; `<REV>` stays free for the `30d`/`on-release` cadence tokens, matching the
  lane's `recheck: <cadence>; procedure: …` shape measured by `SCORECARD.md:193`.
- Gate-clean: `tools/check-recheck-commands.py`'s own `invocations()` with `DEFAULT_FORBID`
  (`pacman, checkupdates, yay, paru, mkinitcpio, limine-update`, `:62`) returns `[]` for this line, it
  parses as a procedure line, and the control line `pacman -Q pacman` + `mkinitcpio -P` returns
  `['pacman', 'mkinitcpio']` — receipt `r4-proposed-line-gate.txt`. No `pacman` binary is invoked
  (`pacman-conf` is a read-only query and is not in the forbidden set).
- Cadence recommendation, stated explicitly because the item asks: keep **S212 at 30 d** as the re-mine
  period, and make the hash check a **cheap at-citation gate** — any wave that cites a row of this table
  runs the one command first; if it does not print the constant, the table is stale and the capture (and
  hence the counter's fixture) must be regenerated before citation. That is proportionate to the measured
  churn (rewrite event ≈ every 3 d, median file age 28 d) and costs nothing between upgrades.

## What I did not do

- Did not mutate the host, run a package transaction, or reset anything; no `/etc` change; no sudo.
  One read-only query `pacman -Q pacman` (→ `7.1.0.r9.g54d9411-3`) was run only to confirm the capture's
  version line, and the proposed recheck line deliberately does not use `pacman`.
- Could not observe real post-capture drift, because there is none (3); the swap counterexample was
  therefore built from the capture's own bytes in a scratch fixture, not from the live host.
- Did not run `tools/check-recheck-commands.py` against the lane's entry: it needs the repaired line to
  exist at a revision, and I may not edit lane content. I verified my proposed line against that tool's
  own matcher instead (receipt above).
- No tools installed or upgraded; nothing to record.

## Receipts
`.ufo/waves/round-38/w1/CritRecheckCadence/`: `r1-counter-revisions.txt` (counter at entry commit, tip,
base, literal `<REV>`, `HEAD`), `r2-drift-and-swap.txt` (verbatim drift output, 142-line false diff,
duplicate basename, sorted-hash comparison, swap fixture), `r3-churn.txt` (ages, windows, mtime dates,
pacman.log events, `/etc/pacman.d/hooks` mtimes, HookDir surface), `r4-proposed-line-gate.txt` (proposed
line, forbidden-invocation matcher result, control).
