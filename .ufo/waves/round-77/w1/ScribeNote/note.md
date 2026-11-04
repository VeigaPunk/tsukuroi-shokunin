# Journald space arithmetic: six pinned examples (draft)

Sources: S324, S325. Verified-at: 2026-11-04. Recheck: on-release.

This companion to data.json deepens existing JD3; it adds no new coverage. It works six finite byte-valued examples against pinned systemd v262 source, not live journald manager observations. Production integration belongs solely to L1. Depth is the lowest tied axis (8); freshness is 9. Neither score is raised by this draft.

## Source provenance

- **S324**: https://raw.githubusercontent.com/systemd/systemd/v262/src/fundamental/macro.h#L320-L350 — LESS_BY at lines 320–326 and CLAMP at 337–350. Frozen snapshot: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/before/src/macro.h. Recorded SHA-256: `1bd38a180b2cccacf0732e3e5b6388ac3d71e453839236c388501080a11a75b8`.
- **S325**: https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c#L143-L186 — cache_space_refresh at 143–174, arithmetic at 168–171, patch_min_use at 176–186. Frozen snapshot: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/before/src/journald-manager.c. Recorded SHA-256: `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2`.

These digests are transcribed from the frozen SHA256SUMS and expected.json, not independently rehashed by this seat. Line numbers refer to these upstream v262 snapshots, not Arch-patched installed sources. No network refetch is claimed.

Short source quotes (each under 25 words): manager line 168, `avail = LESS_BY(vfs_avail, metrics->keep_free);`; line 170, `space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);`; line 171, `space->available = LESS_BY(space->limit, vfs_used);`.

## Formula and interpretation

Every numeric field is in **bytes**. In these examples, `used` corresponds to `vfs_used` and `free` to `vfs_avail`. The local intermediate `avail` is not the final `available` allowance.

S324 LESS_BY subtracts only when its first operand strictly exceeds its second; otherwise it returns zero. This avoids unsigned subtraction underflow for these calls. S324 CLAMP tests the upper bound first, then the lower bound, otherwise retaining the input. With `min_use <= max_use`, the three steps in S325 are:

1. `avail = max(free - keep_free, 0)` (saturated subtraction, not a minimum of free and keep_free).
2. `sum = used + avail`; `limit = min(max(sum, min_use), max_use)`.
3. `available = max(limit - used, 0)` (again saturated subtraction).

All six vectors satisfy `min_use <= max_use`. Inputs are small, non-overflowing uint64 values: the largest `used + avail` here is 1000 bytes, far below 2^64−1. No general overflow-safety claim about arbitrary uint64 additions follows.

## Six examples

The rows in data.json are exactly the frozen A1–A6 objects, in order, from /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-77/before/expected.json. `sum` is explained here but deliberately not added to those row objects.

| Vector | used | free | keep_free | min_use | max_use | avail | sum | limit | available |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A1 | 100 | 1000 | 100 | 0 | 2000 | 900 | 1000 | 1000 | 900 |
| A2 | 100 | 50 | 100 | 0 | 2000 | 0 | 100 | 100 | 0 |
| A3 | 100 | 100 | 100 | 0 | 2000 | 0 | 100 | 100 | 0 |
| A4 | 100 | 1000 | 100 | 0 | 500 | 900 | 1000 | 500 | 400 |
| A5 | 100 | 50 | 100 | 300 | 2000 | 0 | 100 | 300 | 200 |
| A6 | 700 | 50 | 100 | 0 | 500 | 0 | 700 | 500 | 0 |

- **A1:** free-minus-keep_free is 900; adding used yields 1000, inside the bounds. The limit is 1000 and remaining allowance is 900.
- **A2:** free is below keep_free, so avail saturates to zero. The sum and limit are 100; subtracting used leaves zero.
- **A3:** equality also selects zero in LESS_BY. The sum and limit stay 100, leaving zero available.
- **A4:** avail remains 900 and the sum is 1000, but max_use caps the limit at 500; remaining allowance is 400.
- **A5:** avail is zero and the sum is 100, but min_use raises the limit to 300; remaining allowance is 200 despite free being below keep_free. This is the supplied arithmetic, not a guarantee of successful allocation or actual free space.
- **A6:** avail is zero and the sum is 700, above max_use. CLAMP yields 500; LESS_BY(500,700) yields zero, never a negative result or unsigned wraparound.

## A6 and the startup boundary

A6 is a **hypothetical arithmetic input**, not a claim of a reachable startup-normalized manager state. S325 lines 179–185 explain the startup patch and set min_use to the maximum of its previous value and observed usage. Applying that assignment to A6's supplied min_use=0 and used=700 would raise min_use to 700; retaining max_use=500 would then violate this exercise's precondition `min_use <= max_use`. That different tuple is not A6 and is not evaluated here. No conclusion about the complete metrics-normalization lifecycle follows from the two pinned excerpts.

There is no live manager claim, startup-normalized metrics claim, host effective-setting measurement, vacuum/rotation action, service restart, universal arithmetic oracle, source-reading proof from a matching JSON object, admission, or ordinal uplift. The frozen C1 predicate is exactly “six pinned arithmetic vectors match”; C2 is exactly “three exact corrective blocks exist” and is outside this draft. Predicates, expected tuples, and instrument are unchanged. Reviewer source interpretation and non-author closure remain separate from mechanical object matching.
