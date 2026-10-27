VERDICT: supports

Seat C1ExecBaseKill — item C1-21: do the six `(R45-C1)` selftest cases discriminate? Yes, exactly as declared.
Grafted the round-45 case block onto the round-45 **base** census and ran `--selftest`: the five reader cases fail
with exit 141 (each reporting the reader's own wanted code) and the foreign-baseline case passes at base — it is a
regression guard, not a base/impl discriminator. Grafting the round-41 `awk ... exit` lookup into that base copy
turns the guard case red at 141. No other outcome appeared.

# Evidence

## Objects under test (lane read-only throughout)

| object | revision / file | sha256 | lines |
|---|---|---|---|
| base census | 5bbd5ff588120fd8e7c744695351a6978b4241c1:tools/tsukuroi-census.sh | 17c82406fe7a7d06261b1fb2ac4be56e7d5498c6712ae90fe8233d2bb0e81a35 | 3441 |
| impl census | 18389f44cf6ce414d7be205998b29c79fb0b490c:tools/tsukuroi-census.sh | 237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc | 3485 |
| grafted base (block on base readers) | `graft-base-v2.sh` | e9af7ea6de24803f0f79872c803bf55d282fb401c0ab744bfd5b93858bf88e28 | 3485 |
| grafted base + round-41 awk exit | `graft-base-awk-v2.sh` | c5dd86490fd2c142422279dfc04a48665842e550d1ebd88b8863e578284c34e9 | 3485 |
| impl, driver reader reverted only | `impl-rev-driver.sh` | e193784f6e0271903cf9f0fd4a450c9f40da0e9b9e12ab234c325e73dbbc6631 | 3485 |

`sha256sum` output kept verbatim in `.ufo/waves/round-45/a2w1/C1ExecBaseKill/scripts.sha256`; all commands in
`commands.txt` beside it.

Block boundaries: in the impl census the block is `tools/tsukuroi-census.sh:3333-3376` — the line
`  # Round 45 (C1; routed since round 42, R43 item 3): ...` through the blank line before
`  check_cli 'cli: unknown argument exits 2 with usage (S10-2)'` at `:3377`. In the base census the same anchor sits
at `:3333`, and base `:3320-3332` is byte-identical to impl `:3320-3332` (`diff` → empty), so the insertion point is
the declared one.

**Isolation.** `diff -u graft-base-v2.sh impl.sh` (`graft-vs-impl.diff`) yields five hunks and nothing else: the five
reader statements. The graft is therefore base-revision readers with the impl's case block and no other delta, so any
case outcome is attributable to the block. The five readers sit at identical line numbers in both revisions —
base/impl `:965` (probe_systemd `state`), `:1003` (timer `Result` `r`), `:1085` (probe_drivers `driver`), `:1460`
(probe_journal `t_word`), `:1535` (timer `ActiveState` `r`):
base `:965` `state=$(printf '%s\n' "$CAP_OUT" | head -n1 | tr -d '\r' | sed -E 's/[[:space:]]+$//')`
impl `:965` `state=${CAP_OUT%%$'\n'*}; state=${state//$'\r'/}; state=${state%"${state##*[![:space:]]}"}   # first line, no early reader (R45-C1)`
(and the same shape at the other four).

## Run 1 — the block on base readers (the discriminating run)

`TMPDIR=$S/tmp2 bash graft-base-v2.sh --selftest` → exit **1**; log `graft-v2.selftest.log` (157 lines, in seat dir).
The six block cases, verbatim (lines 148-153 in file order, i.e. the order the readers appear in the script):

```
FAIL degraded: a large is-system-running output keeps its first line (R45-C1): exit 141 wanted 1; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-27T03:29:48Z — read-only
FAIL degraded: a large timer Result output keeps its first line (R45-C1): exit 141 wanted 1; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-27T03:29:48Z — read-only
FAIL healthy: a large nvidia-smi output keeps the first GPU line (R45-C1): exit 141 wanted 0; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-27T03:29:49Z — read-only
FAIL blocked: a large is-active output keeps its first word, trailing blanks and CR dropped (R45-C1): exit 141 wanted 2; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-27T03:29:49Z — read-only
FAIL degraded: a large timer ActiveState output keeps its first line (R45-C1): exit 141 wanted 1; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-27T03:29:49Z — read-only
PASS degraded: a foreign baseline past the pipe buffer still finds its last row (R45-C1) (exit 1, DEGRADED)
TSUKUROI_CENSUS_SELFTEST: FAIL (154 cases, 149 passed, 5 failed)
```

Five failures, each `exit 141` (SIGPIPE under `set -euo pipefail`), each reporting the wanted code of its own arm
(1/1/0/2/1) — the case fires on the crashed census, not on a wrong verdict. The sixth case passes **at base** with
exit 1 DEGRADED, confirming the seat's premise that the foreign-baseline lookup has been a full read since round 42
and the case is a regression guard: `tools/tsukuroi-census.sh:777` (impl, unchanged from base) carries
`bn=$(printf '%s\n' "$base_txt" | awk -v n="$nm" '$1 == n && !f { print $2; f = 1 }')   # full read (round 42: an awk ``exit`` under pipefail killed the census on a large baseline)`.

149 passed = the base's 148 cases plus the one passing block case, so the graft broke nothing else.

## Run 2 — base control (148) and impl positive control (154)

`TMPDIR=$S/tmp-base bash base.sh --selftest` → exit **0**, `base.selftest.log`:
`TSUKUROI_CENSUS_SELFTEST: PASS (148 cases, 148 passed, 0 failed)` — the frozen "148 -> 154" claim holds at its base end.
`TMPDIR=$S/tmp-impl bash impl.sh --selftest` → exit **0**, `impl.selftest.log`:
`TSUKUROI_CENSUS_SELFTEST: PASS (154 cases, 154 passed, 0 failed)`, with six `PASS ... (R45-C1)` lines and zero FAIL
lines (`grep -c "^PASS.*R45-C1"` = 6, `grep -c "^FAIL"` = 0 — note PASS lines are printed, not inferred from the
summary alone).

So the same six cases: 6/6 pass at impl, 5 fail + 1 pass at base. The block discriminates the shipped change while
staying green on it.

## Run 3 — the guard case is able to fail (round-41 lookup graft)

Replaced `:777` in the grafted base with the round-41 form
`bn=$(printf '%s\n' "$base_txt" | awk -v n="$nm" '$1 == n {print $2; exit}')` (`awk-lookup.diff`, 1 line). The
literal round-41 statement is attested in the lane's own round-42 before-state:
`.ufo/waves/round-42/w1/C1ExecDiffScope/base.sh:740` reads exactly that, and the round-42 commit `44766208`
("[…] :743 lookup full read […]") is the rewrite.
`TMPDIR=$S/tmp3 bash graft-base-awk-v2.sh --selftest` → exit **1**, `graft-v2-awk.selftest.log`:
```
FAIL degraded: a foreign baseline past the pipe buffer still finds its last row (R45-C1): exit 141 wanted 1; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-27T03:30:47Z — read-only
TSUKUROI_CENSUS_SELFTEST: FAIL (154 cases, 148 passed, 6 failed)
```
The guard case turns red, and it does so for the pipefail reason (141), not a verdict mismatch. The sixth case is
therefore not vacuous: it detects the exact round-41 regression class it was written for, at 150 KB of padding.

## Run 4 — per-case attribution (no cross-fire)

Reverted **only** the driver reader at impl (`:1085` back to
`driver=$(printf '%s\n' "$CAP_OUT" | head -n1 | awk -F', *' '{print $NF}')`, `impl-rev-driver.diff`, 1 line):
`TMPDIR=$S/tmp4 bash impl-rev-driver.sh --selftest` → exit **1**, `impl-rev-driver.selftest.log`:
```
FAIL healthy: a large nvidia-smi output keeps the first GPU line (R45-C1): exit 141 wanted 0; output: tsukuroi-census census-v2 — host=fixture-host — 2026-10-27T03:32:01Z — read-only
TSUKUROI_CENSUS_SELFTEST: FAIL (154 cases, 153 passed, 1 failed)
```
Exactly one case flips, and it is that reader's case: the reader cases are individually attributable, and the other
four do not absorb or mask it. Together with run 1 (five failures mapping one-to-one, in script order, onto the five
reader lines in `graft-vs-impl.diff`) this is the discrimination claim in the item's own terms.

# Findings / caveats

1. **No falsification.** Every expected outcome was observed, with the exact exit codes the seat predicted. The one
   asymmetry is by design and matches the seat text: the sixth case cannot discriminate base from impl (it is green on
   both); its discrimination is demonstrated by the round-41 graft in run 3.
2. The block adds **exactly six** cases (148 → 154) and no case other than the five reader ones changes state on either
   side; the base's remaining 148 stay green under the graft (149 passed in run 1 = 148 + the guard case).
3. Cosmetic only: inserting impl `:3333-3375` without the trailing blank (`graft-base.sh`, run kept in the first pass:
   154 cases, 149 passed, 5 failed, identical FAIL set) leaves the blank line above `check_cli` inside the block. The
   reported artifact is the `v2` graft, which includes the blank so that `graft-base-v2.sh` is line-for-line comparable
   to impl (3485 lines, five-hunk diff).

# What I did not do

- Did not run the frozen C1 counter (`score-census-readers-r45.py`) or any of its legs; this item is the base-side
  discrimination question and the counter's legs (lexical / equivalence / revert_killed / adjacency) belong to other
  seats. My runs are the census's own `--selftest`, the instrument the counter counts.
- Did not run the census in live mode, and did not touch `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` beyond
  `git show` reads: no write, no git/jj mutation, no index touch.
- No host mutation: no `systemctl` start/stop, no scrub/replace/sysfs write, no sudo, no pacman (host-wide pause; no
  install was needed, so nothing to record).
- All runs were serialised, one census selftest at a time, each with `TMPDIR` inside
  `/fast/scratch/hyaku/tsukuroi-r45/C1ExecBaseKill`; that scratch dir was removed at seat end after the receipts were
  copied, so no `/tmp` path is cited as evidence. Not verified by me: any post-integration gate (wave rule — the L1
  owns it).

# Receipts

`.ufo/waves/round-45/a2w1/C1ExecBaseKill/` — `base.selftest.log`, `graft-v2.selftest.log`,
`graft-v2-awk.selftest.log`, `impl.selftest.log`, `impl-rev-driver.selftest.log`, `graft-block.diff`,
`graft-vs-impl.diff`, `awk-lookup.diff`, `impl-rev-driver.diff`, `scripts.sha256`, `commands.txt`. Each under 15 KB.
