source: tools/make-r100-bends.py and tools/check-registry-content-r100.py at commit 743ce449 (S396); the `re` primitives the label tokeniser relies on at S397
verified-at: 2026-11-08 (round 100; pre-round tip ce73ccaf, freeze 743ce449)
recheck: `python3 tools/limine-pin-battery-r99.py --gate .ufo/waves/round-100/before/controls/bends/N13-y-echo.py --runs 1 --work <scratch>` must print `104/105 unmet failed REFUSAL-VERSIONS-9DIGIT-Y` rc 1; `python3 tools/check-registry-content-r100.py --selftest` must print `selftest PASS 26/26` rc 0.

# The echo legs, component-keyed bends, and a registry cell's label set

Round 100 closes the last two limits the round-99 Frontier named by name. It adds no family to any
battery: the instrument that measures the echo legs is the round-99 battery, byte-unchanged, and
what is new is the *article* that exercises two flags it already set.

## 1. What a component-keyed echo bend proves

`tools/check-limine-pins.py` reports the flag's `limine_version` verbatim in its JSON
(`"limine_version": limine_version` at BYTE 16931 of the gate at `7d79ac29…`). A bend that changes
only that line, keyed on one version component, asks a single question of the battery: *does the
family that sends this spelling actually read the field it certifies?*

| bend | key | lie only for | changed lines vs the gate |
|---|---|---|---|
| `N12-x-echo` | first component | `999999999` | one (`limine_version` emission), BYTE 2615 of `tools/make-r100-bends.py` |
| `N13-y-echo` | second component | `999999999` | one, BYTE 3384 |

The generator refuses a substitution that matches zero or more than one site, so a bend cannot be a
no-op dressed as a control. Both bends keep pins, rc and `visibility_era` computed from the true
value: the only family whose expected answer can move is one that asserts the echo.

## 2. Measured readings (round 100; each cell is one `--runs` aggregate over the same three runs)

Counting command: `python3 tools/limine-pin-battery-r99.py --gate <ARTICLE> --runs 3 --work <scratch>
--json <out>`, then `.ufo/waves/round-95/before/controls/count-runs.py <out> --family
REFUSAL-VERSIONS-9DIGIT --family REFUSAL-VERSIONS-9DIGIT-Y --family EXPLICIT-VERSION-ECHO`.

| article | instrument | families_passed | failed_families (exact) | error rows |
|---|---|---|---|---|
| landed gate | r99 battery | 105/105 met | `[]` | 0 |
| `N12-x-echo` | r99 battery | 103/105 unmet | `[EXPLICIT-VERSION-ECHO, REFUSAL-VERSIONS-9DIGIT]` | 0 |
| `N13-y-echo` | r99 battery | 104/105 unmet | `[REFUSAL-VERSIONS-9DIGIT-Y]` | 0 |
| `N12-x-echo` | r98 battery (control) | 104/105 unmet | `[EXPLICIT-VERSION-ECHO]` | 0 |
| `N13-y-echo` | r98 battery (control) | 105/105 met | `[]` | 0 |

The Y leg is a met→unmet closure: no r96–r98 family sent `12.999999999.4` or `0.999999999.0` with
an echo assertion, so the control is blind. The X leg is a **delta**, not a flip: the r96
`EXPLICIT-VERSION-ECHO` family sends the same `999999999.9.9` spelling and already reads the echo,
so the control catches the lie through that one member; the X family's own assertion adds exactly
one failed family (104/105 → 103/105). Reading the X leg as a met→unmet closure would overstate it.

## 3. What this does not prove (named limits)

- It does not prove the X-cap family is the *only* reader of the X spelling: the delta is one extra
  family, and a battery that dropped the X assertion would still read 104/105 on this article.
- It does not exercise the selftest's `--reference` leg (the blanket `lie-limine-version` wrapper),
  which stays the owed r99 item A6a; the wrapper proves the battery sees the field, and these bends
  prove a *named family* asserts it.
- A blanket echo lie (any version, any component) is a different article: it moves every echo-reading
  family at once and cannot attribute the failure.

## 4. Registry label sets

`tools/check-registry-content-r99.py` bound `VARIANTS` cells with a span regex whose alphabet had no
space token, and raised `RC-CELL-AMBIGUOUS` on any second mention. Two consequences were fail-closed
but wrong for a legitimate cell: `VARIANTS N01 N02 N03` read `RC-CELL-MISSING`, and a cell stating a
union of two spans had to be rewritten to one span.

`tools/check-registry-content-r100.py` binds the cell as a **set**:

- one `VARIANTS` mention (counted with `\bVARIANTS\b`; a second mention is `RC-CELL-AMBIGUOUS`);
- tokens are `N<digits>` or `N<digits>-N<digits>`, matched with `re.fullmatch` so a letter or
  extra-digit suffix cannot ride along (S397: "If the whole string matches the regular expression
  pattern, return a corresponding match object");
- tokens joined only by `,`, whitespace, `;`, `+`, `/` or the word `and`; a range expands to its
  members; any other token (`through`, `...`, a descending range) is `RC-CELL-MISSING`;
- the declared set must equal the set of N-labels in the tool's `VARIANTS` keys; an extra or missing
  label is `RC-VALUE-MISMATCH` naming both sides.

Six cells that the r99 control rejects now bind: `VARIANTS N01 N02 N03`, `N01; N02; N03`,
`N01 + N02 + N03`, `N01/N02/N03`, `N01-N02 and N03`, and a union (`N01-N02 and N04-N05` against a
tool whose keys are `N01,N02,N04,N05`). Five forged shapes stay closed: a letter suffix and a prose
connector read `RC-CELL-MISSING`, an extra label and the hybrid comma cell read `RC-VALUE-MISMATCH`,
and a restated mention reads `RC-CELL-AMBIGUOUS`.

## 5. Why this matters to the lane

The two instruments answer different questions. The bends answer "does the family assert the field
its spelling selects?", and their control is a predecessor battery that cannot. The label-set binder
answers "does the registry row still state the tool's whole label set at the granularity a reader can
write?", and its control is the predecessor checker that cannot. Both keep their predecessors' bytes
as controls, so a later round can re-run the same article against the do-nothing instrument and
re-derive the difference.
