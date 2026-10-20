# FxCritSemantics — C1 source-arithmetic semantics

Verdict: **FAILS** on "source arithmetic actually executes and fails" (green-unused);
SURVIVES on "restored wrong-now tests execute and fail" and "no unused fixtures".

## Counterexample 1 (strongest): `return True` mutant survives the whole selftest

`correction_source_ok` (tools/check-boot-chain.py:622-651) is invoked only at :736.
`statement_correction_cases` (:1414-1489) mutates only `registry` records and md
text — never `capture`. Every expected FAIL comes from the fixed-string
`expected` dict (:705-716), the missing-id/notice checks, or early registry
rejects; none reaches the arithmetic. Replacing the entire function body with
`return True` still yields 7/7 correction cases passing, so the package-argv
(:609-619), digest-tuple (:626-639) and mtime-regex (:640-650) checks have zero
failing coverage. "Arithmetic executes and fails" is unproven: the gate would
report PASS/`correction_count:4` with the arithmetic dead.

## Counterexample 2: CORR-04 byte-identity clause is never verified

`CORRECTION_SPECS[3].now` asserts "is byte-identical to the 09:29:18 history
copy (B:115, 171, 219)". Its witnesses are capture:171 `sha256 2e9c9bdc…`
(live) vs :219 `sha256 2e9c9bdc…` (history). The `mtime` branch (:640-650)
checks only the mtime string and `startswith("omarchy_linux.efi_sha256_")` on
:115 — it never parses :171/:219 nor the digest embedded in the :115 filename.
A line-115 file named `omarchy_linux.efi_sha256_0000…` (mtime 09:29:18) passes
all arithmetic while `now` claims byte-identity that is false on its face.
This is exactly the CritDepth failure mode ("registry can say the wrong now")
the mode was added to kill; only the mtime-attribution half is armed.

## Evidence

- :1432-1459 wrong-now mutants alter record+notice strings only; capture arg
  is the pristine fixture.
- Capture bytes confirmed: :171/:219 equal `2e9c9bdc…`, :115 filename embeds
  it; :124 mtime 09:26:22 `omarchy_linux.efi` — so real data passes, but the
  digest-equality path is structurally absent, not merely untested.

## Impacted axes

C1 semantic depth; selftest coverage completeness.

## Smallest safe correction

In `mtime` branch: parse `^sha256 ([0-9a-f]{64})$` at :171/:219, require
equality and equality with the digest embedded in :115's filename; add one
capture-side mutant case (flip :219 digest) expecting
CORR-R18-CORR-04-UNRESOLVED.

Scope: executed=none
