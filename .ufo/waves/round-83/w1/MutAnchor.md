# Round 83 · wave w1 · seat MutAnchor — mutation probe of the anchor counter (C1, depth)

Scope: `tools/check-anchor-coordinates-r83.py` at frozen declaration `d78b3b3982b5df62286dd65b0a42ae8a91847608`
(sha256 `b1e208af…343e21`). Scratch clone only; the real lane was not written. The frozen instrument, battery,
predicates, legs and targets were not changed. Scratch is removed after this report (all material needed to
reproduce is below and in the frozen wave fixtures).

## Baseline (unmutated counter, scratch clone at the declaration)

```
$ python3 tools/check-anchor-coordinates-r83.py --selftest      -> SELFTEST total=16 passed=16 failed=0   rc=0
$ python3 tools/round83-battery.py --instrument r83 --revision d78b3b3982b5df62286dd65b0a42ae8a91847608   rc=0
  C1_depth      3/3 met   C1.a rc2 pass · C1.b rc0 pass · C1.c rc0 pass
  C2_calibration 4/4 met  C2.a rc1 pass · C2.b rc0 pass · C2.c rc0 pass · C2.d rc2 pass
```

## Mutants (13; each is one clause; each in its own copy of the scratch clone)

Diff is `lane → mutant`. Mutant file sha256 prefixes in brackets.

| id | clause mutated | diff |
|---|---|---|
| M01 | drop `len(digest)==64` | `if not isinstance(digest, str) or len(digest) != 64 \` → `if not isinstance(digest, str) \` [5cdb8a7f] |
| M02 | drop hex-character check | drop `or any(c not in "0123456789abcdef" …)` line [ea34c430] |
| M03 | drop `.lower()` on declared digest (compare) | `if actual != digest.lower():` → `if actual != digest:` [8e657d67] |
| M04 | digest over decoded text, not bytes | `actual = sha256(snap_bytes)` → `sha256(snap_bytes.decode("utf-8","replace").encode("utf-8"))` [9df0aa22] |
| M05 | skip `bind_digest` on revision path only | delete `bind_digest(entry, snap_bytes)` in the `revision is not None` branch [d13be5f0] |
| M06 | skip `bind_digest` on fixture path only | delete `bind_digest(entry, snap_bytes)` in the fixture branch [e00cffca] |
| M07 | `norm()` skips `html.unescape` | `" ".join(html.unescape(str(text)).split())` → `" ".join(str(text).split())` [18c836f5] |
| M08 | `locate()` returns first-word line for both ends | `return lines[first], lines[last]` → `return lines[first], lines[first]` [b08c9686] |
| M09 | exact-span test `==` → `>=` (tuple) | `(found[0], found[1]) == (span[0], span[1])` → `>=` [5257ba2f] |
| M10 | finding met when count ≥ target−1 | `count == target` → `count >= target - 1` [10784ace] |
| M11 | `strip_line()` skips tag removal | `norm(TAG.sub("", line))` → `norm(line)` [eb1aaaa3] |
| M12 | `locate()` first-span `bisect_right` → `bisect_left` | `bisect_right(starts, pos) - 1` → `bisect_left(starts, pos) - 1` [b3010f4f] |
| M13 | last-span probe `pos+len-1` → `pos+len` | `bisect_right(starts, pos + len(want) - 1)` → `bisect_right(starts, pos + len(want))` [75f5f264] |

## Scoring

Way 1: the mutant's own `--selftest` (rc≠0 = kill). Way 2: the mutant installed as the counter in the scratch
clone and `round83-battery.py --instrument r83 --revision d78b…` (a C1.a/b/c miss = kill).

| id | selftest rc (FAILs) | battery C1.a / C1.b / C1.c | killed? |
|---|---|---|---|
| M01 | 0 (0) | pass / pass / pass | no — EQUIVALENT on verdict (see below) |
| M02 | 0 (0) | pass / pass / pass | no — EQUIVALENT on verdict |
| M03 | 0 (0) | pass / pass / pass | no — **GAP** |
| M04 | 0 (0) | pass / pass / pass | no — **GAP** |
| M05 | 0 (0) | pass / pass / pass | no — **GAP** |
| M06 | 3 (digest-mismatch-refuses, digest-undeclared-refuses, digest-malformed-refuses) | **miss** (rc0, expect 2) / pass / pass; battery rc1 | yes — both arms |
| M07 | 3 (entity-decode) | pass / pass / pass; battery rc0 | yes — selftest only |
| M08 | 3 (correct-span, range-too-short, entity-decode, digest-updated-decides) | pass / **miss** (rc1) / **miss** (rc1); battery rc1 | yes — both arms |
| M09 | 3 (shifted-two-lines, range-too-short) | pass / pass / pass; battery rc0 | yes — selftest only |
| M10 | 0 (0) | pass / pass / pass | no — **GAP** |
| M11 | 3 (correct-span, digest-updated-decides) | pass / **miss** (rc1) / **miss** (rc1); battery rc1 | yes — both arms |
| M12 | 3 (correct-span, entity-decode, digest-updated-decides) | pass / **miss** (rc1) / **miss** (rc1); battery rc1 | yes — both arms |
| M13 | 0 (0) | pass / pass / pass | no — EQUIVALENT |

**Killed 6/13** (M06, M07, M08, M09, M11, M12). Survived 7: **3 EQUIVALENT** (M01, M02, M13) and **4 GAP** (M03, M04, M05, M10).
Non-equivalent mutants killed: 6/10.

### Survivors

**EQUIVALENT**
- **M13** (last-span `pos+len`). Proof: `want` is whitespace-normalised, so `text[pos+len-1]` is a non-space; `text[pos+len]` is
  a space or end-of-text; word starts are non-space positions; so no `starts[k]` lies in `(pos+len-1, pos+len]`, and the
  `bisect_right` results are identical. Empirical: 200 000 random views/quotes (`locate` original vs M13), 135 036 located,
  **0 differences**.
- **M01** (drop len==64) and **M02** (drop hex check). `hashlib.sha256(...).hexdigest()` is always 64 lowercase hex, so any
  declared digest that is not exactly that string is refused (rc2) whether or not these clauses exist. Verdict/rc/finding/count
  are identical. The only observable difference is the `problems` message, which no selftest case or battery leg reads:
  - `f63` (63-hex declared digest): lane `snapshot-digest-undeclared` → M01 `snapshot-digest-mismatch:declared-c718576fcce8:…`; both rc2.
  - `fz64` (64 non-hex declared digest): lane `snapshot-digest-undeclared` → M02 `snapshot-digest-mismatch:declared-zzzzzzzzzzzz:…`; both rc2.
  Treated as EQUIVALENT for the verdict; a message-only difference with no leg behind it.

**GAP** (each has a separating input, verified by running the lane counter and the mutant on the same input)

- **M03** (`.lower()` dropped from the compare). Input `c3`: honest snapshot, `snapshot_sha256` written in UPPERCASE hex.
  Lane: `rc0 count 8/8 met`. M03: `rc2 cannot-evaluate snapshot-digest-mismatch`. The lane's own hex check accepts uppercase
  (it lowercases first), so the intended contract accepts it; no selftest case or battery leg uses an uppercase digest.
- **M04** (digest over decoded text, not bytes). Input `m04b`: the frozen `anchor-fixture-digestfixed` with a raw `0xff`
  byte appended to the snapshot; `snapshot_sha256` set to `25c214d27e5552f52aa9ac2edd7b80edb73434b88e1d0f6380302579f0c12166`
  (= sha256 of the snapshot with `0xff` replaced by U+FFFD). Lane: `rc2 snapshot-digest-mismatch` (correct: the declared
  digest does not bind these bytes). M04: `rc0 count 8/8 met` — it accepts a snapshot whose bytes are not the declared bytes.
  The real tree and both battery fixtures are valid UTF-8, so no leg reaches this.
- **M05** (no `bind_digest` on the `--revision` path). Input `fx-m05`: a fresh git repo (`git init -q -b master`) whose tree is
  the frozen `anchor-fixture-doctored` (declared digest `194c…`, snapshot bytes `c718…`), committed; run with
  `--repo <repo> --branch master --revision <HEAD>`. Lane: `rc2 cannot-evaluate snapshot-digest-mismatch`. M05: `rc0 count 8/8 met`.
  The same tree in `--fixture` mode is rc2 under both (control). The battery exercises `--revision` only on the real tree (C1.c),
  and the selftest never calls the revision path.
- **M10** (finding met at `count ≥ target−1`). Input `g10`: the frozen `anchor-fixture-digestfixed` with row MT1's cited range
  changed `[135,138]` → `[135,137]` (7/8 exact; located `[135,138]`). Lane: `rc1 unmet count 7/8`. M10: `rc0 met`.
  The selftest passes `target=want_count`, so a case with `rows==target` and `count==target−1` never occurs; the battery only
  sees 8/8 and the real tree.

## Other observation (not a mutant; no verdict effect)

`tools/check-anchor-coordinates-r83.py` labels itself as C2: line 2 of the docstring (`"""C2 counter, round 83 …`) and line 51
`CLAIM = "C2"`; its JSON output carries `"claim": "C2"`. The anchor counter is the C1 depth instrument. No battery leg reads
`claim`, so verdicts are unaffected. Proposed patch (for the L1 to decide): `CLAIM = "C1"` at line 51 and line 2 → `"""C1 counter`.

## Proposed separating legs (for the L1; not applied, instrument frozen)

Each one closes one GAP. Expected verdicts are the lane counter's.
- G-M03: `snapshot_sha256` uppercase of the honest digest → expect rc0 8/8.
- G-M04: snapshot with a raw `0xff` byte, digest of the U+FFFD-substituted bytes → expect rc2 cannot-evaluate.
- G-M05: git-revision fixture with the doctored tree committed → expect rc2 cannot-evaluate.
- G-M10: 8 rows with exactly one off-by-one cited range → expect rc1 unmet, count 7.

## Exact commands

```
S=$HYAKU_SCRATCH/tsukuroi-r83/MutAnchor        # HYAKU_SCRATCH=/fast/scratch/hyaku
git clone -q --shared /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$S/lane"
git -C "$S/lane" checkout -q d78b3b3982b5df62286dd65b0a42ae8a91847608
for id in M01 … M13: cp -a "$S/lane" "$S/m/$id"; apply the one-clause edit above to "$S/m/$id/tools/check-anchor-coordinates-r83.py"
  (cd "$S/m/$id" && TMPDIR=$S/tmp/$id python3 tools/check-anchor-coordinates-r83.py --selftest; echo $?)
  (cd "$S/m/$id" && TMPDIR=$S/tmp/$id python3 tools/round83-battery.py --instrument r83 --revision d78b3b3982b5df62286dd65b0a42ae8a91847608; echo $?)
GAP probes (run with cwd = $S/lane or $S/m/<id>, TMPDIR set):
  python3 tools/check-anchor-coordinates-r83.py --fixture $S/in/g10     # lane rc1 7/8; M10 rc0
  python3 tools/check-anchor-coordinates-r83.py --fixture $S/in/c3      # lane rc0 8/8; M03 rc2
  python3 tools/check-anchor-coordinates-r83.py --fixture $S/in/m04b    # lane rc2; M04 rc0 8/8
  python3 tools/check-anchor-coordinates-r83.py --repo $S/in/fx-m05 --branch master --revision <HEAD>   # lane rc2; M05 rc0 8/8
EQUIVALENCE probe: python3 fuzz of locate() lane vs M13, 200 000 trials, 0 diffs.
```

Tools installed: none. Lane edits: none (`tools/check-anchor-coordinates-r83.py` in the real lane is untouched; its committed
blob hash equals the scratch file, `b1e208af…343e21`). Scratch removed after this report.
