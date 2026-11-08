# A published component bound is per component, and a gate must report the version it acted on

source: `corpus/SOURCES.md` S389 (CPython docs, integer string conversion length limitation,
opened 2026-11-08) and S390 (CPython docs, `sys.int_info.default_max_str_digits`, opened
2026-11-08); own-work: `tools/check-limine-pins.py` `parse_limine_version()`/
`--selftest` and `tools/limine-pin-battery-r96.py` (families named below).
verified-at: 2026-11-08 (round 96; the instruments are pinned in
`.ufo/waves/round-96/before/instruments.sha256`).
recheck: `python3 tools/limine-pin-battery-r96.py --gate tools/check-limine-pins.py --runs 3
--json OUT` (verdict `met`, `families_total 103`); `python3 tools/check-limine-pins.py --selftest`
(`PASS 39/39`).

## PC1 — the 1-9-digit cap is a bound on every component, not on the value

`tools/check-limine-pins.py` accepts a `--limine-version` only as three ASCII-digit components of
1-9 digits each (`parse_limine_version()`), because handing an unbounded component to `int()` raises
above CPython's decimal-conversion digit limit — the 4300-digit default S389 states, whose
configured value S390 names (`sys.int_info.default_max_str_digits`, "The default value for
sys.get_int_max_str_digits() when it is not otherwise explicitly configured.", byte 157653 of the
2026-11-08 pin, sha256 `a7e00587…`). The bound is therefore **per component**: `999999999.9.9` (X at
the cap) and `12.999999999.4` (Y at the cap) are both in-bound versions, and `0.999999999.0` is the
same cap below the era split. Round 95 certified only the X member; the r96 family
`REFUSAL-VERSIONS-9DIGIT-Y` sends the Y members (both eras), and a gate that applies `<= 8` to Y
refuses them and reads `unmet` (`N02-y-cap-8`).

## PC2 — the version a gate acts on is reported with its source and the era it selected

`check()` emits `limine_version`, `limine_version_source` (`flag` or `probe`) and `visibility_era`
(`pre-12.9.5` / `12.9.5+`). For an explicit `--limine-version` the JSON must echo the flag value and
name the source `flag`; the era follows from the whole tuple, so `12.9.4` reads `pre-12.9.5` and
`12.9.5`, `12.9.6`, `999999999.9.9` read `12.9.5+`. Round 95's battery compared the echo only on
probe cases, so a gate that echoed `99.9.9` for an explicit flag survived 99/99 (M06). The r96
families `EXPLICIT-VERSION-ECHO` and `EXPLICIT-VERSION-ERA` send one explicit version per case and
fail both a wrong echo (`N01-echo-wrong`) and an inverted era label (`N03-era-label-flip`).

## PC3 — a fourth component is outside the published `X.Y.Z` grammar

`12.9.6.1`, `12.9.6.1.0`, `12.9.6.99` and `12.9.6.7` are refused rc 64 with empty stdout, while
`12.9.6` is the same-list positive control (rc 0 on a healthy fixture) so a blanket refuser fails
too (`EXTRA-COMPONENT`; bend `N04-extra-components`, which accepts only the first three components,
reads `unmet`). The class **was** sampled before this round — twice: the r95 family roster carries
`12.9.5.1` (it alone kills the bend, 98/99 unmet) and the r95 instrument's `--usage-check` mode
already sends `12.9.6.1`. The r95 Frontier's "not sent at battery level" is therefore corrected here
for both the roster and the instrument; r96 broadens the class (four shapes plus a positive control)
and the family is a **twin** under QUALITY 136 — the round's measured discrimination delta is the
three families `EXPLICIT-VERSION-ECHO`, `EXPLICIT-VERSION-ERA`, `REFUSAL-VERSIONS-9DIGIT-Y`
(A4; `w1/CriticClaims` F-2).

## PC4 — what the scope does not cover

- The metadata clauses are the gate's own reporting contract (own-work), not Limine behaviour; the
  upstream files pinned in S382-S384 and S386-S388 state the era split and the `--version` line, not
  this JSON schema.
- The four-component refusal is the gate's grammar (own-work); Limine's own parser behaviour on a
  four-component value is not claimed.
- The battery's isolation is the r92 contract (private gate copy, `bwrap --unshare-all`,
  `python3 -I`); its residual channels (argv via `/proc`, host fingerprint, writable gate-copy
  parent, `/dev` writes) stay named and open in the r92 A6 and the r93 Frontier.
- The Z component's 9-digit boundary and a 9-digit component with leading zeros are **unsent**:
  `MutBound`'s `M06-z-cap-8` and `M08-refusal-9digit-below-1e8` survive 103/103 (the landed gate
  accepts `12.9.999999999` and `000000001.0.0`; the mutants refuse them), so QUALITY 139's boundary
  rule is certified at family level for X and Y only (r96 Frontier).
- The probe reads the first `X.Y.Z` of `limine --version`; a pre-release answer would read as the
  release (r93 Frontier, not re-measured here).
