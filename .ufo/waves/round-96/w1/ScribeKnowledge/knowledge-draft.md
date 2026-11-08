# A published component bound is per component, and a gate that judges a version must report the version it acted on

`source:` `corpus/SOURCES.md` S389 (Python 3 documentation, integer string conversion length
limitation, version-pinned — opened 2026-11-08) and S390 (`sys.int_info.default_max_str_digits` —
opened 2026-11-08); S382/S383/S384 (Limine v12.9.5 `common/lib/config.c`, `ChangeLog`,
`host/limine.c`); own-work: `tools/check-limine-pins.py` (`parse_limine_version()`,
`VISIBILITY_ERA_SPLIT`, `check()`'s JSON fields) and `tools/limine-pin-battery-r96.py` (the four
families named below). The instruments are pinned in `.ufo/waves/round-96/before/instruments.sha256`
(`check-limine-pins.py` sha256 `7d79ac29…`, `limine-pin-battery-r96.py` sha256 `f06d90ae…`).
`verified-at:` 2026-11-08 (round 96).
`recheck:` `python3 tools/limine-pin-battery-r96.py --gate tools/check-limine-pins.py --runs 3
--work <scratch> --json OUT` (three runs read `verdict met`, `families_passed 103`,
`families_total 103`, `failed_families []`, 0 error rows each) and
`python3 tools/check-limine-pins.py --selftest` (`selftest PASS 39/39`).

## PC1 — the 1-9-digit cap is a bound on every component, not on the value

`tools/check-limine-pins.py` accepts a `--limine-version` only as three ASCII-digit components of
1-9 digits each (`parse_limine_version()`), because an unbounded component handed to `int()` raises
above CPython's decimal-conversion digit limit: S389 states "The default limit is 4300 digits as
provided in sys.int_info.default_max_str_digits." (re-opened 2026-11-08: the pinned page is
**815447 bytes, sha256 `6bf2ce2b…`**, the sentence at byte **785297**, the `ValueError` sentence at
byte **782228**), and S390 names the configured value of the same limit — "The default value for
sys.get_int_max_str_digits() when it is not otherwise explicitly configured." (12 words; the
2026-11-08 pin is **280632 bytes, sha256 `a7e00587…`**, the sentence at byte **157851**).

The bound is therefore **per component**, and only the X position was certified until this round:

| leg | family | sends | expected |
|---|---|---|---|
| accepted, X at the cap | `REFUSAL-VERSIONS-9DIGIT` (r95) | `999999999.9.9` | rc 1 `DEGRADED`, LP-MISMATCH consequence `panic` |
| accepted, Y at the cap | `REFUSAL-VERSIONS-9DIGIT-Y` (r96) | `12.999999999.4` (era B), `0.999999999.0` (era A) | rc 1 `DEGRADED`; `panic` for the era-B member, `prompt` for the era-A member |

The Y family is the per-component leg the r95 Frontier named next ("The accepted leg is
**X-certified only** … A per-component accepted family is next", `corpus/README.md` round-95
Frontier). It is enumerated one member per case, never a draw over the discriminating field
(QUALITY 128): `Y_DIGIT9 = ("12.999999999.4", "0.999999999.0")` (battery `:1719`) and the family
picks `Y_DIGIT9[c.index % len(Y_DIGIT9)]` (battery `:1777`), so the four cases of the family are
two copies of each member.

That the cap really is per component and not on the value is measurable: the gate accepts
`999999999.999999999.999999999` — the cap in all three positions at once — with rc 0 `HEALTHY` and
`visibility_era 12.9.5+` (`receipts/gate-limit-probe.json`, key `cap_member_in_every_position`).

## PC2 — the version a gate acts on is reported with its source and the era it selected

`check()` emits three metadata fields in every JSON answer (`tools/check-limine-pins.py:200-202`
and the parallel block at `:316-318`):

- `limine_version` — the version the gate acted on, echoed verbatim for an explicit flag;
- `limine_version_source` — `flag` when the value came from `--limine-version`, `probe` when the
  installed bootloader answered it;
- `visibility_era` — `pre-12.9.5` or `12.9.5+`, selected by comparing the **whole tuple** against
  `VISIBILITY_ERA_SPLIT = (12, 9, 5)` (gate `:104`, applied at `:193`).

For an explicit flag the gate must echo the flag value and name the source `flag`, and the era
must follow from the tuple. Measured on the landed gate (own-work probe
`receipts/gate-metadata-probe.json`, the era-sensitive fixture whose first physical line is an
entry label, so the era changes the pin's consequence):

| `--limine-version` | echoed `limine_version` | source | `visibility_era` | pin consequence | rc / verdict |
|---|---|---|---|---|---|
| `12.9.4` | `12.9.4` | `flag` | `pre-12.9.5` | `prompt` | 1 `DEGRADED` |
| `12.9.5` | `12.9.5` | `flag` | `12.9.5+` | `panic` | 1 `DEGRADED` |
| `12.9.6` | `12.9.6` | `flag` | `12.9.5+` | `panic` | 1 `DEGRADED` |
| `999999999.9.9` | `999999999.9.9` | `flag` | `12.9.5+` | `panic` | 1 `DEGRADED` |
| `12.999999999.4` | `12.999999999.4` | `flag` | `12.9.5+` | `panic` | 1 `DEGRADED` |
| `0.999999999.0` | `0.999999999.0` | `flag` | `pre-12.9.5` | `prompt` | 1 `DEGRADED` |

The two metadata families are exactly this table, split in two: `EXPLICIT-VERSION-ECHO` asserts the
echo and the source, `EXPLICIT-VERSION-ERA` asserts the era label, and each sends one of the four
`EXPLICIT_VERSION_META` versions per case (`12.9.4`, `12.9.5`, `12.9.6`, `999999999.9.9`; battery
`:1718`, `:1758`, `:1767`). Round 95 never read either field: `grep -c visibility_era
tools/limine-pin-battery-r95.py` → **0**, `grep -c check_echo tools/limine-pin-battery-r95.py` →
**0**, and its `auto_ok` short-circuits on a non-AUTO case (`if c.auto is None or c.auto in
("fail", "shapes"): return True`, battery r95 `:2014`), so the r95 roster compared the echo only
on probe cases — which is why the r95 mutant that echoes `99.9.9` for an explicit flag read
`met 99/99`.

The fields are not decorative: each has a one-clause bend that kills exactly its family
(`receipts/summary-table.txt`, three runs each, canonical lane):

| bend | one-clause change | verdict | passed | `failed_families` | error rows |
|---|---|---|---|---|---|
| `N01-echo-wrong` | `"limine_version": "99.9.9" if limine_version_source == "flag" else …` | `unmet` ×3 | 102/103 | `["EXPLICIT-VERSION-ECHO"]` | 0 |
| `N02-y-cap-8` | Y's cap `<= 9` → `<= 8` | `unmet` ×3 | 102/103 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` | **4** |
| `N03-era-label-flip` | the two `visibility_era` labels swapped | `unmet` ×3 | 102/103 | `["EXPLICIT-VERSION-ERA"]` | 0 |
| `N04-extra-components` | `len(parts) != 3` → `len(parts) < 3` | `unmet` ×3 | 101/103 | `["EXTRA-COMPONENT", "REFUSAL-VERSIONS"]` | 0 |

The N02 error rows are the bend's own refusals (rc 64, empty stdout, no JSON to parse), one per
Y-family case; this is the shape the round's amendment A3 records, and the frozen sentence's "0
error rows" clause does not hold on that leg.

**The era is selected from the whole tuple, not from one position.** Three own-work mutants of
the landed gate (one clause each, `era_b = version >= VISIBILITY_ERA_SPLIT` replaced by a
single-component comparison; sources and clauses in `receipts/mutants/`, results in
`receipts/mut-M-*.json`) read:

| mutant | era rule | verdict | passed | `failed_families` |
|---|---|---|---|---|
| `M-x-only-era` | `version[0] >= 12` | `unmet` | 96/103 | AUTO-ERA-A, ERA-DEFAULT, ERA-FLE-MEASURED-A, ERA-FLE-PANIC-A, EXPLICIT-VERSION-ECHO, EXPLICIT-VERSION-ERA, FIRST-LINE-ENTRY |
| `M-y-only-era` | `version[1] >= 9` | `unmet` | 95/103 | the same seven **plus `REFUSAL-VERSIONS-9DIGIT-Y`** |
| `M-z-only-era` | `version[2] >= 5` | `unmet` | 102/103 | `["REFUSAL-VERSIONS-9DIGIT-Y"]` |

`M-z-only-era` is the cleanest witness: it changes nothing but the era rule and it kills exactly
the Y family — the family is the only one that puts the discriminating weight in the second and
third components. `M-x-only-era` does **not** kill the Y family (it passes 4 of 4): with X alone
`0.999999999.0` reads era A and `12.999999999.4` reads era B, which are the correct answers, so
the Y family is blind to an X-only rule by construction. The battery docstring's claim that "one
that reads the era from X alone answers era B for `0.999999999.0` and fails" (battery `:1774`) is
therefore false as written — an X-only rule gives era A for `0.999999999.0` — and the X-only mutant
is caught by `EXPLICIT-VERSION-ERA` and the ERA families instead, on `12.9.4` (X-only reads era B
for `12.9.4`, whose correct era is A; measured: the family passes 3 of 4, the failing case wants
`prompt` and the mutant answers `panic`). This is a wording defect in a frozen tool docstring of
the same class the round already corrected for r95 (routed 4); it is reported here, not edited.

## PC3 — a fourth component is outside the published `X.Y.Z` grammar, and the class was sampled before

`12.9.6.1`, `12.9.6.1.0`, `12.9.6.99` and `12.9.6.7` are outside the gate's published `X.Y.Z`
grammar and must be refused rc 64 with empty stdout. The `EXTRA-COMPONENT` family sends all four
in one list together with `12.9.6` as the **same-list positive control** (`c.usage =
list(EXTRA_COMPONENT_VALUES) + ["12.9.6"]`, `c.usage_positive = {"12.9.6"}`, battery `:1788-1790`),
so a blanket refuser — one that refuses every value including `12.9.6` — fails the family too. The
positive control's contract is the strict one: it must answer a **verdict** (`json.loads(stdout)`
succeeds and rc is 0), not merely a non-refusal (battery `:2138-2143`).

Measured on the landed gate (own-work probe `receipts/gate-metadata-probe.json`, key
`healthy_fixture`; and the family's own usage rows in `receipts/r3-landed.json`):

| version | rc | stdout bytes | answer |
|---|---|---|---|
| `12.9.6.1` | 64 | 0 | refused (usage error on stderr) |
| `12.9.6.1.0` | 64 | 0 | refused |
| `12.9.6.99` | 64 | 0 | refused |
| `12.9.6.7` | 64 | 0 | refused |
| `12.9.6` (control) | 0 | 922 | `HEALTHY`, echo `12.9.6`, source `flag`, era `12.9.5+` |

**The r95 Frontier correction.** The r95 README's Frontier bullet said the `12.9.6.1`
extra-component shape was "not sent at battery level". That sentence is corrected here: the
**class** was sampled once before this round. The r95 battery's `REFUSAL_VERSIONS` roster
(battery r95 `:1643`) contains `"12.9.5.1"` — a four-component value — so the class reached the
instrument at family level in r95, and the r95 gate refused it rc 64 (the r95 usage row reads
`"12.9.5.1"` rc 64, stdout 0). The r95 `usage_check` also sent `12.9.6.1` (r95 `:2300`), but that
is the instrument's own usage check, not a family. So r96 **broadens** the class — four shapes
plus a same-list positive control, against one pre-existing row — and does not close a first. The
bend shows the same fact from the other side: `N04-extra-components` kills two families, and the
second is `REFUSAL-VERSIONS`, the pre-existing row, not a new one (the failing row is
`"12.9.5.1"`, which the bent gate answers rc 0 with 343 bytes of stdout instead of refusing;
`receipts/bend-N04-extra-components.json`, `receipts/dn-N04-extra-components.json`).

The r95 battery is blind to the three new families and to the correction: on the landed gate and
on N01/N02/N03 it reads `met 99/99` with 0 error rows in all three runs
(`receipts/dn3-landed.json`, `receipts/dn3-N0*.json`); on N04 it reads `unmet 98/99` with
`failed_families ["REFUSAL-VERSIONS"]` in all three runs (`receipts/dn3-N04-extra-components.json`)
— the blindness receipt, and the proof that the pre-existing row is what dies.

## PC4 — the scope of these clauses, and what they do not cover

- **The metadata clauses are the gate's own reporting contract (own-work).** `limine_version`,
  `limine_version_source` and `visibility_era` are fields the lane's gate emits; no upstream
  source states them. The upstream files pinned in S382-S384 state the era split and the
  `--version` line, not this JSON schema: `S382` is the v12.9.5 `config.c` (re-opened 2026-11-08:
  **23351 bytes, sha256 `a940acae…`**, the cut at raw 328-330 and the label-end NUL at 362-365);
  `S383` is its `ChangeLog` (**121313 bytes**, the "Parse the config in linear time" entry at line
  8 under "Noteworthy changes compared to the previous release, 12.9.4:" at line 5); `S384` is
  v12.9.5 `host/limine.c` (**69050 bytes**, `puts("Limine " LIMINE_VERSION)` at raw 2035 and the
  bare `puts(LIMINE_VERSION)` at raw 2031).
- **The four-component refusal is the gate's grammar (own-work).** No upstream Limine row states
  a component count or a version grammar; the sweep `grep -nE 'X\.Y\.Z|three dot-separated|
  component count|three components' corpus/SOURCES.md` returns **no match**, and the only rows that
  mention a component width are S389 and S390, which state CPython's conversion limit and not
  Limine's version shape. Limine's own behaviour on a four-component value is not claimed.
- **No upstream binary is read beyond the versions already sourced.** The round certifies metadata
  the *gate* emits; it reads no upstream Limine binary beyond S382-S384/S389-S390. The upstream
  tags in the corpus are `v12.9.4`, `v12.9.5` and `v12.9.6` only
  (`grep -oE 'limine-bootloader/limine/v[0-9.]+' corpus/SOURCES.md | sort -u`).
- **The AUTO leg is not re-measured here.** The metadata families are explicit-flag families
  (`c.auto` is never set in them); the probe cases still compare the echo through `auto_ok`
  (battery `:2104-2109`), and a probe-failure row emits no JSON to read, so the probe's own
  metadata leg stays where r93/r94 left it.
- **The isolation contract is the r92 one** (private gate copy, `bwrap --unshare-all`,
  `python3 -I`); its residual channels (argv via `/proc`, host fingerprint, writable gate-copy
  parent, `/dev` writes) stay named and open in the r92 A6 and the r93 Frontier.
- **The era mechanism is still the observable, not the mechanism.** This entry certifies the
  reported label and the answer that follows from it. It does not certify *how* the gate reads
  the version, and it does not certify upstream's own parse.

## Limits (declared, not claimed)

- **The Z position of the cap is unsampled at family level.** No family sends a version whose
  third component is at the cap; the sweep
  `grep -oE '999999999\.999999999[^"]*' tools/limine-pin-battery-r96.py` returns **no match**.
  `999999999.999999999.999999999` (the cap in all three positions) is accepted by the gate
  (measured, PC1) but is sent by no family, and a bend of **Z**'s bound to `<= 8` is therefore
  still untested. The Y family's second member carries the second position; the third is open.
- **Four-component shapes beyond the four enumerated stay unsampled at family level.** The gate
  refuses `12.9.6.` (empty fourth component), `12.9.6.1.2` (five components) and `12.9.6.1.2.3`
  rc 64 with empty stdout, and a non-ASCII digit (`12.9.6.０`, full-width zero) is refused too
  (`receipts/gate-limit-probe.json`, key `unsampled_four_component_shapes`) — but the family's
  roster is exactly the four members of `EXTRA_COMPONENT_VALUES` (battery `:1720`), so none of
  those shapes is asserted by a case.
- **The X-only era rule is not killed by the Y family** (measured, PC2): the Y family passes 4 of
  4 under `M-x-only-era`. The whole-tuple rule is certified by the roster as a whole, not by the
  Y family alone.
- **The battery docstring's X-only claim is wrong** (PC2): it says an X-only era rule "answers era
  B for `0.999999999.0`", but X of that value is 0, so an X-only rule answers era A — the correct
  answer. The clause is corrected in the r95 tool docstrings this round (routed 4); this one
  remains standing in the r96 battery's `fam_refusal_versions_9digit_y` docstring (battery
  `:1773-1775`) and is reported, not edited.
- **The per-component bound is the gate's own contract**, not upstream Limine's: S389 and S390
  state CPython's conversion limit and no upstream row states a version grammar (PC4).
- **The r95 do-nothing battery is blind to three of the four new families** (measured, PC3): it
  reads `met 99/99` on the landed gate and on N01/N02/N03. The blindness is the receipt, not a
  defect of the old roster.

## Related ground

- `limine-bound-9digit-r95.md` — the accepted leg of the same bound, X-certified only; this entry
  takes the Y leg and the two metadata fields.
- `limine-auto-default-r94.md` — `auto` became the default version source, and its probe refuses
  rather than defaulting.
- `limine-version-probe-r93.md` — the probe's parse clause ("the first `X.Y.Z` immediately
  following `limine`").
- `limine-r92-oracle-isolation.md` — the battery runs each gate in a private copy under `bwrap`,
  so the numbers this entry cites are results, not borrowed answers.
