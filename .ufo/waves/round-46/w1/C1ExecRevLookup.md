VERDICT: supports

# C1-21 — revision lookup demonstrated end to end (non-author)

Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, HEAD `a44770491eb5ca15ce9f8b3207309d1af683ffaf`
(checked with `git -C … rev-parse HEAD`; `tools/tsukuroi-census.sh` clean in the worktree, so HEAD bytes are
the running bytes). All commands and outputs: `commands.txt`, `identity-run.txt`, `five-commit-digests.txt`,
`lookup-loops-five.txt`, `all24-digests.txt`, `lookup-negative.txt`, `non-author-paths.txt`,
`revision-modes.txt`, `ordering-fixture.txt`, `nowrite-check.txt`, `mutant-local-edit.txt` (this directory).

## 1. The five commits and their independent identity fields

`git -C <lane> log --format=%H -n 5 -- tools/tsukuroi-census.sh` (24 commits touch the census in total):

| commit | sha256 of committed bytes | md5 | bytes | lines |
|---|---|---|---|---|
| a4477049 (identity mode added) | `d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa` | `db08a606ce128da3839457372e91e220` | 209208 | 3598 |
| 18389f44 | `237b21c9d757e339943c29b0f005faf569ff997deca46dd5bce16bc631b5fcdc` | `4f926076f14f04eab3935d40d1be2c64` | 202665 | 3485 |
| fbfef071 | `17c82406fe7a7d06261b1fb2ac4be56e7d5498c6712ae90fe8233d2bb0e81a35` | `7e2343ef214e858635eb4117bf2f3921` | 198992 | 3441 |
| 8eee79db | `2ef86357c14aec3f4346f7ac9013cdda3b399d38bae67f4ca2e286e5a37c4639` | `eceff61fd5c6cf75269f95b905c47e74` | 198952 | 3441 |
| 9608ebc3 | `b2c01812f25d5a3f9964009fd673963c167550c1126579be2e3953876edb92e3` | `5abebdb32aa83173368b01ab156b52c6` | 198917 | 3441 |

Fields were derived exactly as the entry prescribes for pre-identity commits — `git show <h>:tools/tsukuroi-census.sh`
piped to `sha256sum`/`md5sum`/`wc -c`/`wc -l` (`five-commit-digests.txt`); no trailing newline, so `lines` = newlines.

## 2. The documented loop returns the commit, and only commits with identical bytes

The loop from `corpus/knowledge/census-identity-r46.md` §"Re-deriving the revision from the line", seeded once per
commit, run against all 24 census revisions (`lookup-loops-five.txt`):

```
### commit=a4477049… want=d925839c…  wall_ms=214 matches=[a4477049…] first_is_self=yes match_count=1
### commit=18389f44… want=237b21c9…  wall_ms=198 matches=[18389f44…] first_is_self=yes match_count=1
### commit=fbfef071… want=17c82406…  wall_ms=224 matches=[fbfef071…] first_is_self=yes match_count=1
### commit=8eee79db… want=2ef86357…  wall_ms=177 matches=[8eee79db…] first_is_self=yes match_count=1
### commit=9608ebc3… want=b2c01812…  wall_ms=216 matches=[9608ebc3…] first_is_self=yes match_count=1
```

Five of five return exactly their own commit as the first and only line. The uniqueness half of the claim is
independently confirmed: the sha256 of all 24 census revisions has no duplicate
(`awk '{print $2}' all24-digests.txt | sort | uniq -d` → empty, `dup_lines=0`), so no revision shares bytes with
another and "only commits with identical bytes" is exercised as a singleton.

The unexercised-by-real-history clause — "the first hash printed is the newest commit that wrote those bytes" — was
tested positively in a scratch fixture repo (toplevel asserted equal to the fixture dir, identity `fixture
<fixture@invalid>`): census bytes of 9608ebc3 committed at c1, a4477049 bytes at c2, 9608ebc3 bytes again at c3.
The loop printed `35c3344b…` (c3, newest) then `853e0f16…` (c1), and not `0ca73897…` (c2) — newest-first ordering
holds and byte-identical history is listed completely (`ordering-fixture.txt`).

## 3. The live identity line at a4477049, and its lookup

From the lane, HEAD `a4477049`:

```
$ bash tools/tsukuroi-census.sh --identity
TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa md5=db08a606ce128da3839457372e91e220 bytes=209208 lines=3598 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes
exit=0 wall_ms=61 stderr_bytes=0
```

- All four byte fields equal the independent `git show` derivation in §1 (`all24-digests.txt` row a4477049:
  `d925839c… 209208 3598`; md5 re-derived: `db08a606…`).
- Same line from a foreign cwd via absolute path, 41 ms, exit 0 (`non-author-paths.txt`) — the fields do not depend
  on cwd or on a relative invocation.
- Feeding that sha256 to the loop prints `a4477049…` and nothing else (§2, first row). So one line plus one loop
  names the revision, with **no author knowledge**: the line's `version=census-v2` alone would not (documented as
  constant since round 3), the hash does.

## 4. Discriminating controls (the loop must not over-claim)

| input sha256 | loop output |
|---|---|
| `d925839c…12cf0` (last hex digit changed) | empty, count 0 |
| random 32 bytes / sha256 | empty, count 0 |
| worktree copy with one byte appended (`b1afd670…`) | empty, count 0 |
| fresh local-edit mutant, trailing comment line added (`ab676ae3…`) | empty, count 0 |

The local-edit mutant is the sharp end-to-end case: its own `--identity` line reports
`sha256=ab676ae3f0bf1f8fb408b7348cdc0652bdc2b32a06099e933bdd859b4849350d`, which equals `sha256sum mut2.sh`, is
`verified=yes`, and the loop returns nothing — i.e. the entry's stated conclusion "no output means the bytes were
never committed (a local edit)" is reachable from one line and one loop (`mutant-local-edit.txt`).

## 5. Mode availability across the five commits (anticipated asymmetry confirmed)

At `a4477049` in a shared clone (`revision-modes.txt`): identical identity line, exit 0.
At `18389f44` in the same clone: `grep -c -- --identity tools/tsukuroi-census.sh` = **0** and
`bash tools/tsukuroi-census.sh --identity` → `tsukuroi-census: unknown argument: --identity`, usage to stderr,
exit 2. The earlier four commits therefore must be fed `git show`-derived fields, exactly as the item instructs;
the loop still identifies them, so the capability covers pre-identity history.

## 6. Cost and side effects

- Lookup cost: 177–224 ms per revision over 24 census commits (`git log` + 24 × `git show | sha256sum`); the
  identity line itself 41–61 ms. Full attribution of a line: under a second, no network, read-only.
- Identity mode wrote nothing: run inside an empty cwd → `files_before=0 files_after=0 exit=0`; lane
  `git status --porcelain` byte-identical before/after an identity run (`nowrite-check.txt`).

## Limits of this item

- I did not run `tools/score-census-identity-r46.py` (the frozen C1 counter) or the census selftest — not this
  item's assignment, and the per-seat cost rule reserves them for the counted seats. What is shown here is the
  operator-facing capability, not the counter verdict.
- The five commits tested are those the item names (`-n 5`); the other 19 census revisions were digested in the
  duplicate scan but their loops were not seeded individually.
- Two scratch fixture repos and a copy of the census were used; the scratch tree was removed after receipts were
  copied. No tool installs were needed.
