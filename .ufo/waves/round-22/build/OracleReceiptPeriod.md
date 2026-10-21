# OracleReceiptPeriod — source-only oracle for REVIEW-SCOPE-MISMATCH

Seat: leaf, NO-EXEC, NO-FETCH, no subagents. Target read in full:
`.ufo/waves/round-22/snapshot/tools/check-review-snapshots.py` (278 lines, read as
`:1-120`, `:121-270`, `:271-278` in raw form). Nothing below rests on grep snippet
inference; grep was used only to confirm line anchors already seen in the full text.

**LSP availability.** No language-server session is bound to this snapshot path inside the
seat's declared surface (read/grep/glob only, NO-EXEC). Recorded as *unavailable*, not as
absence of a definition. Because the whole file was read, every claim here is a direct
source quote or a mechanical consequence of quoted lines.

**Digest.** The receipt digest is the seat-declared value; it was not recomputed here
(NO-EXEC forbids running a hasher). Digest identity therefore rests on the seat binding.

## 1. Axes named (godspeed)

| Axis | Move this report keeps |
|---|---|
| Fixture minimality | single-char `name`/`report`/`source`/`predicate`, empty source blob, no trailing newline |
| Defect specificity | exactly one finding, so the reported ID cannot be a co-fire artifact |
| Digest literalness | only an empty source has a digest derivable without executing a hasher |
| Exit taxonomy | prove code `1` (FAIL) is disjoint from code `2` (CANNOT_EVALUATE) |
| Pin accounting | prove `pinned_reviews == 0` for this class |
| Boundary honesty | separate derived policy expectation from observed result (none) and from the tool's own disclaimers |
| Report-shape hazard | this build artifact is itself non-registrable as a review report |

## 2. Source facts that decide the outcome

Comparison block (grep-anchored, verbatim):

```
112  scope_lines = [line for line in lines if line.startswith("Scope:")]
117  if scope_lines != ["Scope: executed=none"]:
118      add("REVIEW-SCOPE-MISMATCH", row["name"])
119  if len(findings) == start:
120      pinned += 1
121  code = 2 if report_encoding_error or read_error else (1 if findings else 0)
```

Supporting surface, quoted from the full read:

- `physical_lines` splits **only** at LF and strips **at most one** terminal CR; no other
  normalization. Line 44 is the entire implementation.
- `add(fid, site)` appends `{"id": fid, "site": site}`; at 118 the `site` argument is
  `row["name"]` — the review **name**, never the report path.
- The scope check is inside the `else` branch of the UTF-8 decode (`text = report.decode("utf-8")`
  / `except UnicodeError`). An undecodable report yields `REVIEW-REPORT-ENCODING` and the
  token comparisons are skipped entirely.
- `REVIEW-SCOPE-MISMATCH` has exactly one emission site in the file (line 118). No other
  code path can produce that ID.
- Manifest gate (lines 63-80) must pass first: `schema == "tsukuroi-review-snapshots-v1"`,
  non-empty `reviews` list, unique names, unique reports, `safe_path` on `report` and
  `source`, `sha256` matching `[0-9a-f]{64}`, non-empty control-free `predicate`.
- Payload (lines 125-128): `status` is `("PASS","FAIL","CANNOT_EVALUATE")[code]`,
  plus `distinct_source_files`, `pinned_reviews`, `total_reviews`, `findings`, and a
  `scope` advisory string.
- `DEFAULT = ".ufo/waves/round-21/reviews.json"` (line 18): any invocation that omits
  `--manifest` evaluates round-21's manifest, not the fixture.
- `git_read` (lines 131-142) reads `rev:path` from git; a path absent at `rev` returns
  `None`.

Consequence: the scope test is pure literal equality against the single-element list
`["Scope: executed=none"]`. Any second line beginning `Scope:` — including an identical
duplicate — breaks equality. Any value divergence (one period, two periods, trailing
space, CR retained, lookalike Unicode) breaks equality. There is no trimming, no
case-folding, no NFKC, no period tolerance.

## 3. Smallest literal fixture

The fixture is three literal blobs at the bound revision `894d1e20…`, all under
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.

### 3.1 Manifest `M` (literal JSON, no whitespace)

```json
{"schema":"tsukuroi-review-snapshots-v1","reviews":[{"name":"A","report":"a","source":"s","sha256":"e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855","predicate":"p"}]}
```

### 3.2 Source blob `s` (literal, 0 bytes)

Empty file. Its digest is the standard test vector for the empty byte string,
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. This is the *only*
choice of source content whose 64-hex manifest literal is derivable without executing a
hash function, which is what makes the fixture literal under NO-EXEC. It is also the
smallest legal blob.

### 3.3 Report blob `a` (literal, three physical lines, no trailing newline)

```
Reviewed-SHA256: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
Predicate: p
Scope: executed=none.
```

The final character of the blob is the period that terminates `Scope: executed=none.`.
That one period is the entire defect. It is data, not sentence punctuation.

### 3.4 Why this is minimal

- One review row is the minimum (`reviews` must be non-empty).
- All six row keys are mandatory; `name`, `report`, `source`, `predicate` are at their
  minimum legal length of 1 (name regex `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`, `safe_path`
  accepts `"a"` and `"s"`), and the digest is fixed at 64 hex characters.
- The report is the three compared lines only; the digest line is forced to the row's
  `sha256`, the predicate line to `Predicate: ` + `predicate`, and the scope line carries
  the one-byte deviation.
- A repo-shaped variant (`name:"One"`, `report:"wave/One.md"`, `source:"snapshot/tool.py"`,
  non-empty source) is *not* execution-free literal: its digest is a computed value, as
  the selftest itself demonstrates at line 148 (`sha = hashlib.sha256(b"fixed source\n")`).

### 3.5 One-line mutants that keep the same predicted finding

| Mutant | Report line 3 | Predicted result |
|---|---|---|
| F1 (above) | `Scope: executed=none.` | REVIEW-SCOPE-MISMATCH |
| F2 (mirrors the assignment's literal `executed=none..`) | `Scope: executed=none..` | REVIEW-SCOPE-MISMATCH, identical payload |
| F0 (smallest possible blob) | line omitted entirely | REVIEW-SCOPE-MISMATCH, identical payload (`scope_lines == []`) |

F0 is the smallest *report*; F1 is the smallest *deviation*; F2 is the literal the Work
text displays.

## 4. Exact expected verdict — policy expectation, derived from source

`evaluate(M, read_bytes)` returns code `1` with this payload (as `json.dumps(..., sort_keys=True)`
would serialize it):

```json
{"distinct_source_files": 1, "findings": [{"id": "REVIEW-SCOPE-MISMATCH", "site": "A"}], "pinned_reviews": 0, "scope": "primary snapshot and predicate declarations only; not proof of reading, chronology or command nonexecution", "status": "FAIL", "total_reviews": 1}
```

- **Exit code:** `1` (line 121: no encoding error, no read error, findings non-empty).
- **Status:** `FAIL`.
- **Finding ID:** `REVIEW-SCOPE-MISMATCH`, exactly one.
- **`site`:** `"A"` — the review name. A fixture that reports `"a"` (the report path) as
  the site is wrong.
- **`pinned_reviews`:** `0`. The pin test at 119-120 sees a grown findings list, so the row
  is not counted as pinned. A scope mismatch and `pinned_reviews == total_reviews` are
  mutually exclusive.
- **`total_reviews`:** `1`; **`distinct_source_files`:** `1`.
- **Ordering:** `findings` is in emission order (digest, predicate, scope); with only one
  finding, order is trivially exact.

**CLI-vs-API delta.** `main()` prints the payload after
`payload.update(revision=…, branch=…, branch_tip=…)`, so real stdout carries seven keys.
Asserting that stdout equals the five/six-key `evaluate()` payload is a false oracle. The
finding set and exit code are the stable assertions; the three revision keys are
invocation-dependent.

## 5. Attacking the expectation

Every row below is a **source-derived prediction**, not a run.

### 5.1 Token-shape attacks on line 3

| # | Report line 3 | Derived result | Why |
|---|---|---|---|
| 1 | `Scope: executed=none` | PASS (0), no findings, pinned 1 | exact equality |
| 2 | `Scope: executed=none.` | SCOPE-MISMATCH | list has a trailing period |
| 3 | `Scope: executed=none..` | SCOPE-MISMATCH | same class; assignment literal |
| 4 | line absent | SCOPE-MISMATCH | `scope_lines == []` |
| 5 | `scope: executed=none` | SCOPE-MISMATCH | lowercase never `startswith("Scope:")` |
| 6 | `Scope: executed=none ` (trailing space) | SCOPE-MISMATCH | no trimming |
| 7 | `Scope: executed=none\t` | SCOPE-MISMATCH | no trimming |
| 8 | two identical `Scope: executed=none` lines | SCOPE-MISMATCH | list length 2 ≠ 1 |
| 9 | `Scope: executed=none\r\n` (CRLF) | PASS | `physical_lines` strips one CR |
| 10 | `Scope: executed=none\r\r\n` | SCOPE-MISMATCH | one CR remains in the token |
| 11 | `prefix\vScope: executed=none` | SCOPE-MISMATCH | line starts with `prefix`; VT does not split |
| 12 | `Scope: executed=none\vextra` | SCOPE-MISMATCH | starts correctly, value differs |
| 13 | `Scope: executed\uFF1D none` (fullwidth `=`) | SCOPE-MISMATCH | `unicodedata` is used only for control categories, never normalization |
| 14 | `Scope: executed=none` after a form feed inside the same physical line | SCOPE-MISMATCH | form feed is not a line separator here |

Row 9 matters: the checker is CRLF-tolerant *for this comparison*, so a scope line that
looks byte-different in an editor can still PASS. Rows 11-14 matter because a reviewer
eyeballing a terminal may see two lines where `physical_lines` sees one, and vice versa.

### 5.2 Reachability attacks — where the expected ID is *not* emitted

| # | Surface | Derived result | Why |
|---|---|---|---|
| 15 | report bytes not valid UTF-8 | code 2, `REVIEW-REPORT-ENCODING`, **no** scope check | scope test sits in the decode `else` |
| 16 | report read raises | code 2, `REVIEW-READ-FAILED`, no scope check | `continue` before decode |
| 17 | report read returns `None` | code 1, `REVIEW-REPORT-MISSING`, no scope check | `if report is None` branch |
| 18 | source read raises | code 2, `REVIEW-READ-FAILED` only | `continue` before the report is read |
| 19 | source readable but digest differs | code 1, `REVIEW-SNAPSHOT-MISMATCH`; scope still evaluated | digest test does not short-circuit |
| 20 | manifest absent at revision | code 1, `REVIEW-MANIFEST-MISSING`, `site` = the round-21 default path | `raw is None` branch, line 57 |
| 21 | manifest malformed / duplicate JSON key / bad schema / unsafe path / duplicate report path | code 2, `REVIEW-MANIFEST-SCHEMA` | manifest gate |
| 22 | manifest bytes not UTF-8 | code 2, `REVIEW-MANIFEST-SCHEMA` | `UnicodeError` caught by the outer handler |
| 23 | two rows: row1 scope-bad, row2 unreadable | code 2, **both** findings | `read_error` wins the exit code while findings persist |
| 24 | two rows: row1 scope-bad, row2 clean | code 1, one finding, `pinned_reviews == 1`, `total_reviews == 2` | per-row pin test |

**Key ambiguity:** exit code `1` is shared by `REVIEW-MANIFEST-MISSING`,
`REVIEW-SNAPSHOT-MISMATCH`, `REVIEW-PREDICATE-MISMATCH`, `REVIEW-SCOPE-MISMATCH`, and
`REVIEW-REPORT-MISSING`. The exit code alone never identifies the defect; only the
`findings[].id` does. An invocation that forgets `--manifest` (row 20) or commits only the
working tree (row 20 again, since `git_read` reads `rev:path`) produces code 1 with a
*different* ID and would be misreported as a scope failure.

**Second ambiguity:** a report can satisfy the digest pin and still fail the scope token
(row 19 vs row 2 are independent checks). `Reviewed-SHA256` equality is not evidence about
`Scope:`.

**Third ambiguity:** `status` is a function of the exit code, not of findings. Row 23 shows
`CANNOT_EVALUATE` with findings present.

### 5.3 Attack on the premise itself

The Work text writes the scope as `executed=none..`. The checker has no notion of prose.
If a reader treats the first period as data and the second as sentence punctuation, the
canonical value becomes `executed=none.` and every conforming report — including this
seat's own receipt — flips to `REVIEW-SCOPE-MISMATCH`. If both periods are prose, the
value is `executed=none` and F1/F2 fail while F0/row 1 pass. The byte string supports
opposite verdicts; only the receipt requirement (three literal lines, last one
`Scope: executed=none`, verbatim, no punctuation) resolves it. The checker is fail-closed
on exactly this ambiguity: adding a sentence period to a conforming receipt turns PASS into
FAIL with no other signal.

### 5.4 Shape hazard created by this seat's own deliverable

This artifact necessarily contains extra lines beginning `Reviewed-SHA256:`, `Predicate:`,
and `Scope:` inside the fixture block. If it were registered as a review report for
`check-review-snapshots.py`, all three exact-equality tests would fire
(`REVIEW-SNAPSHOT-MISMATCH`, `REVIEW-PREDICATE-MISMATCH`, `REVIEW-SCOPE-MISMATCH`) because
each list would have more than one element. The wave must not cite this file as a review
report; a registered report must contain exactly one of each token line, and the fixture
must live in a separate blob. (This is a derived consequence of lines 107-118, not an
observed run.)

## 6. Observed runtime result

**None.** The case was not invoked: no `python3`, no subprocess, no hash computation, no
git read. Section 4 is a policy expectation mechanically derived from `evaluate`, and
section 5 is a set of derived predictions.

The closest source-level corroboration is the selftest case `scope-period` (line 161),
whose declared tuple expects exit `1` and finding set `{REVIEW-SCOPE-MISMATCH}` for a report
whose scope value gains one period. That is the tool author's *declared* expectation inside
the file — it is not an observation by this seat and was not executed. Agreement between it
and section 4 is a consistency check between two readings of the same source, not runtime
evidence.

## 7. What this outcome proves and does not prove

A `REVIEW-SCOPE-MISMATCH` proves one thing: the set of physical lines in the report that
begin with `Scope:` is not exactly one line equal to `Scope: executed=none`. It does not
prove the seat read anything, ran nothing, or acted in any particular order. The payload's
own `scope` advisory states this: "primary snapshot and predicate declarations only; not
proof of reading, chronology or command nonexecution". For C1/C2/C3 accounting this means a
PASS across every receipt is not evidence that `executed=none` held; it is evidence that the
declared token matched. Never present this checker as preventive enforcement or as proof of
nonexecution.

## 8. Residual unknowns

1. The empty-byte-string digest literal is recalled as the standard test vector; it was not
   recomputed under NO-EXEC. One `sha256sum` on the empty file confirms the fixture before
   use. If it must be avoided, the alternative requires computing a digest, which leaves
   the execution-free literal regime.
2. Whether the harness tolerates a zero-byte committed blob at the bound revision. The
   checker itself does: only `None` is treated as missing (line 90 compares `source is None`
   before hashing).
3. Which revision L1 binds for the fixture, and whether the manifest path is passed
   explicitly — the default is round-21's manifest (line 18).
4. Whether any round-22 review manifest will cite this build artifact; per 5.4 it must not.

Reviewed-SHA256: b9e6537343464bd63fa0f4719b8c209693580936948a2b8d9d05670e35ad91b8
Predicate: r22-oraclereceiptperiod
Scope: executed=none
