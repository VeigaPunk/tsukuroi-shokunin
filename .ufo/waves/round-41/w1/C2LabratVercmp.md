VERDICT: supports

# C2-30 — host `vercmp` against PA8's rule text and the pinned `version.c`

Item: falsifiable hypothesis — host `vercmp` orders epoch first (absent = 0), then version, then
release only when both strings carry one. Boundary matrix + comparison with `parseEVR` /
`alpm_pkg_vercmp` in the frozen snapshot.

Result: the hypothesis holds on every case I could construct, including the whole *legal*
full-version space (193,600 pairs). The host binary and the pinned source agree on 16,000+
differential pairs. Three shape-level gaps were found **in PA8's rule text only**
(empty epoch, empty release, a colon that is not an epoch separator) — none is reachable from a
real PKGBUILD, and none changes the ordering of legal versions. One legal-but-sharp edge is
called out in §5 (leading-zero pkgrel subrelease compares equal).

## 1. Method — a reference built from the frozen source, not from the docs

`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-41/frozen/src/version.c`
was copied byte-for-byte into scratch and compiled standalone:

```
sha256sum version_pinned.c
fa769e3081d25d74132109ca35a1e272a44b1c5674c397f3f2a1acaf3b6ab833  version_pinned.c
grep -i version.c .../frozen/src/SHA256SUMS
fa769e3081d25d74132109ca35a1e272a44b1c5674c397f3f2a1acaf3b6ab833  version.c
gcc -O0 -g -I. -include util.h -o refvercmp main.c version_pinned.c   # exit 0
```

`util.h` is a 5-line stub (`SYMEXPORT`, `<stdlib.h>`, `<string.h>`); `main.c` only calls
`alpm_pkg_vercmp`. No lane file was modified; both are kept in
`.ufo/waves/round-41/w1/C2LabratVercmp/harness/` with `SHA256SUMS`.

Host identity: `pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3`, i.e. built from `54d9411`,
the same commit the snapshot was fetched from (`frozen/src/FETCH.txt` line 2). The empirical
agreement in §4 is what actually establishes that the frozen `version.c` is the comparison code
inside `/usr/bin/vercmp`.

## 2. The requested boundary matrix — host vs `alpm_pkg_vercmp` prediction

Every row was run twice: `vercmp A B` (host, pacman 7.1.0.r9.g54d9411-3) and `./refvercmp A B`
(frozen source). Columns `host`/`ref` are the printed values; "code path" is the line in
`version.c` that produces it. 40/40 identical. Receipt: `vercmp-matrix.tsv.txt`.

| # | case | host | ref | code path (frozen `version.c`) |
|---|---|---|---|---|
| 1 | `vercmp 1.0-1 1.0` | 0 | 0 | rel2 = NULL → `if(ret == 0 && rel1 && rel2)` at :252 fails → 0 |
| 2 | `vercmp 1.0 1.0-1` | 0 | 0 | symmetric, rel1 = NULL |
| 3 | `vercmp 0:1.0 1.0` | 0 | 0 | epoch `"0"` vs `"0"` → :249 equal, then version equal |
| 4 | `vercmp :1.0 1.0` | 0 | 0 | empty epoch rewritten to `"0"` at :57-59 → same as row 3 |
| 5 | `vercmp 1:1.0 1.0-99` | 1 | 1 | epoch `"1"` vs `"0"` at :249 → release never read |
| 6 | `vercmp 2.0 1:1.0` | -1 | -1 | epoch `"0"` vs `"1"`; newer version loses, as PA8 states |
| 7 | `vercmp 1.0-1 1.0-1.1` | -1 | -1 | release `"1"` vs `"1.1"` at :253: shorter remainder loses (:200-212) |
| 8 | `vercmp 1.0-1.1 1.0-1.10` | -1 | -1 | release numeric segment 1 vs 10 → more digits wins (:160-172) |
| 9 | `vercmp 1.0-1.2 1.0-1.10` | -1 | -1 | same, dotted pkgrel is numeric per segment, not decimal |
| 10 | `vercmp 1.0-1.10 1.0-1.9` | 1 | 1 | 10 > 9 (digit-count rule), not 1.10 < 1.9 |
| 11 | `vercmp 1.0-1.1 1.0-1.01` | 0 | 0 | leading zeros stripped, segments identical → 0 (see §5) |
| 12 | `vercmp 0:1.0-1 1.0-2` | -1 | -1 | equal epochs → release decides: `"1"` < `"2"` |
| 13 | `vercmp 1.0- 1.0` | 0 | 0 | trailing dash: rel = `""` non-NULL, other side NULL → skip (:252) |
| 14 | `vercmp 1.0- 1.0-0` | -1 | -1 | `""` vs `"0"`: empty string loses (:200-212 showdown) |
| 15 | `vercmp 1:1.0 1:1.0-1` | 0 | 0 | release skipped although the strings differ |
| 16 | `vercmp 01:1.0 1:1.0` | 0 | 0 | epoch `"01"` vs `"1"`: leading zero stripped → equal |
| 17 | `vercmp 1a:1.0 1.0` | -1 | -1 | `1a:` is **not** an epoch (see §3.2) |
| 18 | `vercmp 1-1 1:1-1` | -1 | -1 | `1-1` has no epoch; `1:` does → epoch 0 vs 1 |
| 19 | `vercmp 1:0 0:99999.99999-99999` | 1 | 1 | epoch decides alone over a huge epoch-0 version |
| 20 | `vercmp '' 1.0` | 1 | 1 | `strcmp("", "1.0") != 0`; version `""` loses |

Full 40-row table (adds leading zeros, `_`/`+`/`a` suffixes, epoch ranges `2:`/`10:`,
stripped-versus-dotted versions): `vercmp-matrix.tsv.txt`. All 40 rows: host == ref.

## 3. Where PA8's *text* alone under-specifies (not a host defect)

I implemented PA8's three sentences literally, parameterised by the ambiguous clause, and
diffed the readings against the host over 8,000 mixed pairs (4,000 drawn from every 1-3 character
string over `{0,1,-,:,.,a}`, 4,000 from a random grammar over version tokens/separators).
`differential-random.txt`:

```
host vs pinned-source ref: 0 / 8000 disagree
PA8 text, release=pointer (code reading): 0 / 8000 disagree
PA8 text, release=nonempty (literal reading): 35 / 8000 disagree
PA8 text, epoch=first_colon (naive reading): 731 / 8000 disagree
```

### 3.1 "release only when both strings carry one" — the code tests pointer presence, not a pkgrel

`version.c:51` is `se = strrchr(s, '-')`; `if(se)` at :65 sets `release` to whatever follows, and
:252 tests `rel1 && rel2` — *non-NULL*, so a trailing dash counts as carrying a release and gets
compared:

```
vercmp 1.0- 1.0    = 0      # other side has no release: skipped
vercmp 1.0- 1.0-0  = -1     # both "carry" one; "" < "0"
vercmp 1.0-1 1.0-  = 1
```

Reading "carry one" as "carry a non-empty pkgrel" predicts 0 for the second row; the host returns
-1. This is the only class of textual misprediction my search found (all 35 diverging pairs have a
trailing dash), and `pkgrel` cannot be empty under PKGBUILD(5), so it is unreachable in practice.

### 3.2 The epoch is a leading run of digits *immediately* followed by `:` — not "text before the colon"

`parseEVR` (`version.c:39-77`) scans `while(*s && isdigit(*s)) s++` and only then tests `*s == ':'`
(:53). A colon after any non-digit is part of the **version**:

```
vercmp 1a:1.0 1.0 = -1      # epoch 0; version "1a:1.0" loses on separator length (:110-114)
vercmp 1.0:2 1.0-2 = 1      # epoch 0 both; "1.0:2" vs "1.0" → extra segment wins
```

Any "epoch = substring before the first `:`" reading is wrong in 731/8,000 random shapes; the
digits-then-colon reading is right in all of them.

### 3.3 An *empty* epoch is folded to 0 by a separate branch

`if(*epoch == '\0') epoch = "0";` (:57-59) handles `:1.0`; the `else` branch (:61) handles the
*absent* epoch. PA8 says "absent epoch counting as 0"; `:1.0` is not absent but returns the same
order (`vercmp :1.0 1.0 = 0`, `vercmp :1.0 0:1.0 = 0`). The text predicts the right *number* by the
wrong rule; harmless, but the text does not cover the shape.

## 4. PA8's three sentences predict the pinned code over the entire legal space

Legal grammar taken from the same frozen snapshot: `pkgver` — "not allowed to contain colons,
forward slashes, hyphens or whitespace" (`PKGBUILD.5.asciidoc:47-49`); `pkgrel` — "a positive
integer, with an optional subrelease level ... in the form x.y" (`:58-66`); `epoch` — "required to
be a positive integer; the default value if left unspecified is '0'" (`:67-73`).

Split with that documented grammar (not with `parseEVR`) and compared with the frozen
`alpm_pkg_vercmp` (`legal-grid.txt`, `legal2.py`):

```
legal versions: 440   pairs: 193600
PA8 text (documented grammar) vs pinned source, 193600 legal pairs: 0 mismatches
A epoch decides alone:                          1200 cases, 0 violations
B equal pkgver, one side lacks pkgrel -> 0:      385 cases, 0 violations
C release decides when both carry one:           294 cases, 0 violations
D pkgrel irrelevant when pkgver differs:          32 cases, 0 violations
host vs pinned source on 8000 sampled legal pairs: 0 mismatches
```

So: "any epoch 1 build outranks every epoch 0 build" (`1:0` vs `0:99999.99999-99999` = 1;
`1:1.0-1` vs `2.0-1` = 1) and "`1.0` equals `1.0-5`" (`:13`, `:15`) both hold, and the release is
never consulted once the version differs. S233's cited window `version.c:39-255` is accurate:
`parseEVR` :39-77, `rpmvercmp` :83-217, `alpm_pkg_vercmp` :219-260, the three steps :249-255 —
the window ends on the release step.

Frozen capture cross-check: all six lines of
`frozen/hostcap/vercmp.txt` reproduce exactly on the host today (`capture-reproduction.txt`),
e.g. `vercmp 1.0-1 1:0.1-1 = -1` and `vercmp 2:0.1 1:9.9 = 1`.

## 5. Legal but sharp — dotted pkgrel is a version, not a number

`vercmp 1.0-1.1 1.0-1.01 = 0` (both host and frozen source). The subrelease is compared with
rpmvercmp numeric segments, so leading zeros vanish: `1.1` and `1.01` are the **same** version and
no upgrade is offered between them. Consistent with PA8 ("the release" compared as a version) but
worth knowing: `1.10 > 1.9` and `1.0.0 > 1.0` (`1.0-1` vs `1.0-1.0.0` = -1) in the same
direction, while `1.01 == 1.1` in the other.

## 6. Optional tightened wording for PA8 (only if the entry is ever revised)

Replacing "the release only when both strings carry one" with:

> "the release only when both strings contain a `-` after the epoch digits (an empty release after
> a trailing `-` counts and compares as the empty string, which loses to any release);"

and adding: "an epoch is a run of digits at the very start directly followed by `:`; an empty
epoch before `:` orders as 0, and a `:` not preceded only by digits is part of the version, not an
epoch."

No change is needed for the C2 counter's predicate — this is a text-precision note, not a defect in
the host behaviour, and PA8 as written is correct for every version a PKGBUILD can produce.

## 7. Not done / limits

- No mutation of the lane, the host, or any counter; no sudo, no pacman transaction, no tool
  install (nothing was needed). Scratch was `/fast/scratch/hyaku/tsukuroi-r41/C2LabratVercmp`
  (removed; receipts copied first).
- I did not run the C2 counter `tools/check-package-anatomy-r41.py`; this item is a host probe, and
  the counter needs the per-row VERDICT files other seats own.
- The exhaustive random grid covers 1-3 character strings plus grammar-random ones; longer
  adversarial strings (nested separators) were sampled only through the grammar, so the
  text-misprediction *classes* in §3 are characterised, not proven exhaustive.
- Two of my own first-pass invariants were wrong (they required "epoch decides" and "release
  skipped" without holding the other component equal) and reported 104 and 1,386 false violations;
  the corrected runs (§4) are the ones of record. Recording this so the numbers are not mistaken
  for host defects.
