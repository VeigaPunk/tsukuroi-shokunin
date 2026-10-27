VERDICT: supports

# C1-K2 — kill rule: live census output digits-stripped byte-identical base vs final

Scope read only. Base = `916019057147d7e9ba6b137647b2cee26decf4b8` (round-46 tip), final =
lane worktree `tools/tsukuroi-census.sh` (blob `eb62e3dd883505ab0e1b73b739378f9bda7b74ba`,
identical to `HEAD:tools/tsukuroi-census.sh`; worktree clean for this path — `git diff --stat HEAD
-- tools/tsukuroi-census.sh` printed nothing). No lane file was created, edited or deleted by this
seat; no host mutation, no service/package/sysfs action.

## 1. Bytes under test

    $ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 91601905...:tools/tsukuroi-census.sh | sha256sum
    ac4e38ff99df044bf17410722b253965402afa1556fd105dde181e19e048f48e  -
    $ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show HEAD:tools/tsukuroi-census.sh | sha256sum
    adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41  -

Base materialized to `/fast/scratch/hyaku/tsukuroi-r47/C1ExecKillLive/base-census.sh`
(sha256 `ac4e38ff…`, 3622 lines); final at
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh`
(sha256 `adb1b4ce…`, 3644 lines).

The base→final diff touches only the hermetic selftest fixture base and two comment blocks — no
live-mode code path:

    tools/tsukuroi-census.sh | 28 +++++++++++++++++++++++++---
    $ git -C ... diff 91601905... -- tools/tsukuroi-census.sh
    +  local st_base=${TMPDIR:-/tmp}
    +  case "$st_base" in
    +    *[!A-Za-z0-9._/+-]*) st_base=/tmp ;;
    +  esac
    +  work=$(mktemp -d "$st_base/tsukuroi-r3-2-selftest.XXXXXX")
    (plus the two R47-C2 pin cases at the end of run_selftest and 3 comment hunks)

Anchor: `tools/tsukuroi-census.sh:2055-2059` (final) — the R47-C2 `st_base` fallback;
`tools/tsukuroi-census.sh:2050` `run_selftest()` entry. Live mode is untouched.

## 2. Live census, base vs final — DIGITS-STRIPPED BYTE-IDENTICAL

Command form exactly as the item states, run from
`/fast/scratch/hyaku/tsukuroi-r47/C1ExecKillLive/` with `TMPDIR` pointed inside the seat scratch
(`$S/tmp`) so nothing lands under `/tmp`:

    env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$TMPDIR" bash <(git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 916019057147d7e9ba6b137647b2cee26decf4b8:tools/tsukuroi-census.sh) > procsub-base.out 2> procsub-base.err
    env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR="$TMPDIR" bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh > procsub-final.out 2> procsub-final.err

    base rc=2   final rc=2   (stdout 7583 B each, stderr 0 B each)

    $ sed 's/[0-9]//g' procsub-base.out > p1 ; sed 's/[0-9]//g' procsub-final.out > p2 ; diff -u p1 p2
    (no output)  stripped_diff_rc=0
    $ sha256sum p1 p2
    09547ccfb23be73533042b2db6adf6d07fc77e08bf48f487ce311b5fe5612d1a  p1
    09547ccfb23be73533042b2db6adf6d07fc77e08bf48f487ce311b5fe5612d1a  p2

**Kill rule holds: digits-stripped live output is byte-identical (sha256 `09547ccf…` both sides).**
Receipts: `.ufo/waves/round-47/w1/C1ExecKillLive/procsub-base.out`,
`procsub-final.out`, `base-live.out`, `final-live.out`, `base-live.stripped`, `final-live.stripped`.

### Unstripped diff (for the record) — 2 lines, both host-volatile, both digit-only

    $ diff base-live.out final-live.out
    1c1
    < tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T08:53:40Z — read-only
    ---
    > tsukuroi-census census-v2 — host=plazir27 — 2026-10-27T08:53:43Z — read-only
    4c4
    < … C6_avail_kb=21046660 …
    ---
    > … C6_avail_kb=20413572 …

Token-level diff of line 4 confirms exactly one token differs:
`diff <(sed -n '4p' base-live.out | tr ' ' '\n') <(sed -n '4p' final-live.out | tr ' ' '\n')`
→ `34c34 < C6_avail_kb=21046660 --- > C6_avail_kb=20413572`. No field name, no plane id, no verdict,
no HANDOFF/DRIFT/STORAGE/SCRUB token changed.

### Every real difference

1. **Run timestamp** (line 1): `2026-10-27T08:53:40Z` vs `…:43Z` — the two runs are 3 s apart.
2. **`C6_avail_kb`** (line 4): `21046660` vs `20413572` — free-memory reading that moves between
   two consecutive probes of the *same* script.

No other difference exists. To show these two are host volatility and not a code-path effect, the
same two scripts were each run a second time (final → `rep1.out`, base → `rep2.out`):

    $ diff final-live.out rep1.out
    1c1   (timestamp)
    4c4   C6_avail_kb=20413572 → 22057644
    $ diff base-live.out rep2.out
    1c1
    4c4

Digits-stripped sha256 of **all six** live captures (base, final, procsub-base, procsub-final,
rep1, rep2) is one single value:

    $ sha256sum base-live.stripped final-live.stripped p1 p2 r1s r2s | awk '{print $1}' | sort -u | wc -l
    1
    09547ccfb23be73533042b2db6adf6d07fc77e08bf48f487ce311b5fe5612d1a

So the "digit-stripped identical" property is stable across four process invocations, and the two
unstripped deltas reproduce *within* a single script revision — i.e. they are ambient host state,
not base-vs-final behaviour.

### Exit map and verdict unchanged

    base-live.out  line 13: TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=BLOCKED drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)
    final-live.out line 13: TSUKUROI_CENSUS: BLOCKED (packages=BLOCKED systemd=BLOCKED drivers=DEGRADED journal=DEGRADED update-safety=BLOCKED oom=DEGRADED)

Identical; rc 2 (BLOCKED) on both sides — the exit map
(`0:HEALTHY,1:DEGRADED,2:BLOCKED`, `tools/tsukuroi-census.sh:3533`) is unchanged. Line count 13 on
both. Both live runs produced **zero** bytes on stderr.

### Live mode wrote nothing

    $ ls /tmp | wc -l   -> before 1487, after 1487

and the census created no file in the seat scratch other than my redirected captures.

## 3. `--identity` — line shape unchanged; only the digests differ

    $ env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=… bash base-census.sh --identity   -> rc 0, 1 line
    $ env -i PATH=/usr/bin:/bin LC_ALL=C TMPDIR=… bash tools/tsukuroi-census.sh --identity -> rc 0, 1 line

base (`base-id.out`):

    TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=ac4e38ff99df044bf17410722b253965402afa1556fd105dde181e19e048f48e md5=15e26889f9196617231eaa672d3b9752 bytes=210762 lines=3622 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes

final (`final-id.out`):

    TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41 md5=cf005e9a946e0a37c96f81d443d520d8 bytes=212252 lines=3644 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes

Shape comparison (digests and counts masked):

    $ sed -E 's/sha256=[0-9a-f]+/sha256=<HEX64>/; s/md5=[0-9a-f]+/md5=<HEX32>/; s/bytes=[0-9]+/bytes=<N>/; s/lines=[0-9]+/lines=<N>/' <id>.out
    $ diff -u base-id.shape final-id.shape
    (no output)  shape_diff_rc=0
    a0887392c41295fc4c37e18697bc18c6d91e6ebfcd161d12949682590cb21274  base-id.shape
    a0887392c41295fc4c37e18697bc18c6d91e6ebfcd161d12949682590cb21274  final-id.shape

Identical field order, identical `version=census-v2`, identical `planes=` list and order
(`packages,systemd,drivers,journal,update-safety,oom`), identical `exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED`,
identical trailing `verified=yes`. Receipts: `base-id.out`, `final-id.out`, `base-id.shape`,
`final-id.shape`.

**Real differences in the identity line (all expected):** `sha256=`, `md5=`, `bytes=`, `lines=` —
the identity line reports the *executed script's* bytes, and the base and final scripts genuinely
differ (3622 → 3644 lines, 210762 → 212252 bytes). The base digest `ac4e38ff…` equals the sha256 of
the base blob computed above, and the final digest `adb1b4ce…` equals the sha256 of
`HEAD:tools/tsukuroi-census.sh` — the identity line is self-consistent on both sides.

**Note on a naive digit-strip of the identity line:** it does **not** come out identical, because the
hex digests contain letters (`a`–`f`) that survive `sed 's/[0-9]//g'` (only the numeric bytes/lines
fields are stripped). The item's requirement for `--identity` is shape, not digit-stripped
identity — and shape is identical (`shape_diff_rc=0`, sha256 `a0887392…` both sides). The digit-strip
kill rule is satisfied on the **live census** output, which is where the item states it.

## 4. What this falsifies / risks

- No falsification of the C1/C2 claims from this item. The R47-C2 edit is confined to the selftest
  fixture base (`tools/tsukuroi-census.sh:2055-2059`); the live-mode path, the plane vocabulary, the
  verdict line, the exit map and the `--identity` shape are all unchanged.
- Residual risk (host-side, not a code defect): the live census output is not reproducible
  byte-for-byte between two runs of the *same* revision — line 1 timestamp and `C6_avail_kb` move.
  A kill rule that compared live output without digit-stripping would fail even against an
  unmodified script. Recorded as an observation for the L1; it does not affect the round's declared
  claims.
- The live verdict on this host is `BLOCKED` (packages BLOCKED on a `pacman -Qkk` missing-signature
  error, systemd-user BLOCKED with no session bus, update-safety BLOCKED with `pacman -Qu` rc=1).
  That is the ambient host state of the seat's machine, not a round-47 regression.

## 5. Commands not run / limits of this seat

- Not run here: the `--selftest` battery (164 cases) and the R47-C2 TMPDIR-with-space census run —
  they belong to the C2 seat and would contend for the ~6-CPU budget; this seat's cost rule allows
  one heavy run at a time and this item needed none.
- Not run: the R47 admission counter (`check-scrub-admission-r47.py`) and the battery — those bind
  C1 rows, not the C2 kill rule.
- No tool was installed or upgraded by this seat (no pacman, uv, npx or `~/.local/bin` write).

## 6. Receipts

All under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-47/w1/C1ExecKillLive/`:

    base-live.out / base-live.err / base-live.rc      base census live (materialized base blob)
    final-live.out / final-live.err / final-live.rc    final census live
    procsub-base.out / procsub-final.out               live runs via the item's exact `bash <(git show …)` form
    base-live.stripped / final-live.stripped           digits-stripped live captures
    base-id.out / base-id.rc / final-id.out / final-id.rc   --identity captures
    base-id.shape / final-id.shape                     --identity with digests/counts masked

Scratch `/fast/scratch/hyaku/tsukuroi-r47/C1ExecKillLive/` removed after copying these receipts.
