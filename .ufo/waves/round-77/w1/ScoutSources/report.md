# ScoutSources — independent upstream re-open

## Scope and axes

Depth (8, lowest tied) and freshness (9). Read the frozen SCORECARD declaration at eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5 (git show, exit 0) and `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/before/expected.json`. C1 remains exactly “six pinned arithmetic vectors match”; C2 remains exactly “three exact corrective blocks exist”. No predicate, instrument, expected data, source, registry or production edits were made. No integration or arithmetic-checker run was performed by this seat.

An honest preliminary report was written before the fetches; this report deepens it with completed observations. Tooling rules were read from `/home/vgpnk/.omp/agent/RULES.md`; no tool was installed or upgraded. No package transactions, privileged mutations, service actions, journal reads, commits, pushes or delegation occurred.

## Commands, exits and durable receipts

Directory creation command, exit 0:

```sh
mkdir -p /fast/scratch/hyaku/tsukuroi-r77/ScoutSources /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/w1/ScoutSources
```

The following three independent GETs ran concurrently. Each curl command exited 0. curl was deliberately not given `--fail`: HTTP status is recorded separately from transport exit.

```sh
env TMPDIR=/fast/scratch/hyaku/tsukuroi-r77/ScoutSources curl --silent --show-error --location --max-time 60 --output /fast/scratch/hyaku/tsukuroi-r77/ScoutSources/macro.h --write-out 'http_code=%{http_code}\nurl_effective=%{url_effective}\n' https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro.h
# http_code=200
# url_effective=https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro.h

env TMPDIR=/fast/scratch/hyaku/tsukuroi-r77/ScoutSources curl --silent --show-error --location --max-time 60 --output /fast/scratch/hyaku/tsukuroi-r77/ScoutSources/journald-manager.c --write-out 'http_code=%{http_code}\nurl_effective=%{url_effective}\n' https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c
# http_code=200
# url_effective=https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c

env TMPDIR=/fast/scratch/hyaku/tsukuroi-r77/ScoutSources curl --silent --show-error --location --max-time 60 --output /fast/scratch/hyaku/tsukuroi-r77/ScoutSources/macro-fundamental.h --write-out 'http_code=%{http_code}\nurl_effective=%{url_effective}\n' https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro-fundamental.h
# http_code=404
# url_effective=https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro-fundamental.h
```

The guessed endpoint response body was exactly `404: Not Found`. Classification: **unreachable at that guessed URL (HTTP 404), not fabrication**. It is not the actual header path and supplies no implementation evidence. The actual header GET succeeded, HTTP 200.

Digest command, cwd `/fast/scratch/hyaku/tsukuroi-r77/ScoutSources`, exit 0:

```sh
env TMPDIR=/fast/scratch/hyaku/tsukuroi-r77/ScoutSources sha256sum --check /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/before/src/SHA256SUMS
# macro.h: OK
# journald-manager.c: OK
```

Thus both independently fetched bodies match the frozen SHA256SUMS byte-for-byte:

| File | SHA-256 |
|---|---|
| macro.h | 1bd38a180b2cccacf0732e3e5b6388ac3d71e453839236c388501080a11a75b8 |
| journald-manager.c | 428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2 |

## Exact located quotes (each at most 25 words)

Line numbers below were read from the freshly downloaded bodies, not inferred from a search snippet. Since digests match, they also locate the frozen snapshots. Actual upstream macro path is `src/fundamental/macro.h`, stored locally as `before/src/macro.h`.

| Symbol/site | Actual v262 lines | Exact quote |
|---|---|---|
| LESS_BY wrapper | macro.h:320 | `#define LESS_BY(a, b) __LESS_BY(UNIQ, (a), UNIQ, (b))` |
| __LESS_BY result | macro.h:325 | `UNIQ_T(A, aq) > UNIQ_T(B, bq) ? UNIQ_T(A, aq) - UNIQ_T(B, bq) : 0;` |
| CLAMP wrapper | macro.h:338 | `#define CLAMP(x, low, high) __CLAMP(UNIQ, x, UNIQ, low, UNIQ, high)` |
| __CLAMP high test | macro.h:344 | `UNIQ_T(X, xq) > UNIQ_T(HIGH, highq) ?` |
| __CLAMP low test | macro.h:346 | `UNIQ_T(X, xq) < UNIQ_T(LOW, lowq) ?` |
| __CLAMP unchanged result | macro.h:348 | `UNIQ_T(X, xq);` |
| cache_space_refresh allowance | journald-manager.c:168 | `avail = LESS_BY(vfs_avail, metrics->keep_free);` |
| cache_space_refresh limit | journald-manager.c:170 | `space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);` |
| cache_space_refresh remaining | journald-manager.c:171 | `space->available = LESS_BY(space->limit, vfs_used);` |
| patch_min_use | journald-manager.c:185 | `storage->metrics.min_use = MAX(storage->metrics.min_use, storage->space.vfs_used);` |

The full LESS_BY implementation spans 320–326: temporaries capture both arguments, then line 325 returns their positive difference or zero. CLAMP spans 337–349: temporaries capture input/low/high (341–343); high is tested first (344), high returned (345), low tested (346), low returned (347), otherwise input returned (348). These are textual implementation and call-site observations; they do not claim a semantic references census.

## Interpretation, contradictions and limits

**Observed:** the raw v262 implementation and the frozen round-77 source statements agree. LESS_BY is saturated subtraction, not minimum. For the stated small non-overflowing uint64 inputs and ordered bounds, the source reading gives `avail = max(free - keep_free, 0)`, `limit = clamp(used + avail, min_use, max_use)`, and `available = max(limit - used, 0)`.

**Contradiction:** the older round-76 declaration's phrase “smaller of free space and keep_free” (visible in frozen SCORECARD, with its later erratum) conflicts with manager:168 plus macro:325. For example, free=1000 and keep_free=100 yield 900 by the located implementation, not 100 by minimum. This corroborates the round-77 rejection/correction premise; it does not amend its frozen predicates. No contradiction was found in the specified round-77 source-line claims.

**Boundary:** manager:176–186 contains the startup `patch_min_use` adjustment, including line 185 above. The finite examples are arithmetic exercises on provided metrics, not claims about startup-normalized metrics, actual disk state, runtime reachability, Arch-patched line numbering, universal overflow behavior, or eventual vacuum actions. No service was restarted to inspect these matters.

**Semantic tooling unavailable:** `read xd://lsp` returned “No such tool” and no mounted language-server device. Literal grep located LESS_BY/CLAMP and the specified manager calls; direct relevant-range reads established their text. No grep result is offered as semantic definition/reference proof, and no exhaustive caller claim is made.

**Confidence:** high for HTTP statuses, byte identity, actual snapshot locations and the bounded source interpretation. Missing endpoint evidence establishes only that specific path returned 404 during this re-open. Production semantic admission and C1/C2 acceptance remain with L1/reviewers; this seat does not judge or ship them.

## Output-scope note

The final `Report:` trailer also names `.ufo/waves/round-77/w1/ScoutSources.md`, outside the explicitly sole permitted seat evidence directory. To honor the narrower sole-write scope, no sibling-level file is written; the full requested report is this acceptance path inside `ScoutSources/`.

Scratch cleanup completed after preserving these durable receipts: `rm -r -- /fast/scratch/hyaku/tsukuroi-r77/ScoutSources`, exit 0. No scratch fixture remains from this seat.
