# C3 path-census ledger privacy review

**Severity: Low (residual metadata/linkability risk only).**

**Attacked claim:** C3, path-census ledger retention. **Result:** no concrete sensitive-body or path disclosure falsifier found in the bounded review.

**Exploit path:** A person who can read the ledger could use its stable `call_id` and `site` labels to correlate entries with separately available event records. Because `request_arguments_sha256` is an unkeyed deterministic digest, a person with candidate low-entropy argument encodings could test guesses offline. This is a possible metadata/linkability risk, not an observed recovery of argument contents.

**Evidence:** Inspected both cohorts (378 build rows; 995 falsify rows), their row schemas and value types, retained-path examples, and bounded searches over all string values for secret-like, body-like, environment, URL, and filesystem-path literals. Each row has only these string fields: `call_id`, `disposition`, `request_arguments_sha256`, `rough_category`, `site`, and `tool`. `canonical_bad` and `rough_first_bad` contain numeric indexes (or null), not path strings; `retained_path_count` stores counts only. The cohort totals report 23 build and 29 falsify retained-path cases, but the ledger does not include those path values. No report, command, fetch, or environment bodies, credentials, or filesystem paths surfaced. The string-value search returned no matches; site labels are scenario labels such as `FxC1ReportWrite:6`, not paths.

**Impact:** Direct exposure of secrets, report/command bodies, environment data, or path values is not evidenced. The remaining concern is correlation and possible confirmation of guessed request arguments if an attacker has a suitable external corpus. This does not falsify the ledger's bounded privacy claim; it limits any claim that its metadata is unlinkable.

**Smallest remedy:** No frozen-ledger change is justified by this evidence; the retained identifiers and digest serve the per-event reconciliation record, and removing them would weaken traceability. If the ledger is to be published to a broader audience, replace raw `call_id` values with cohort-local stable row identifiers; keep the argument digest only if the frozen evidence contract requires it.

Reviewed-SHA256: 80ca7015fa187b4a22abd329ab6767849dc9109dc954215dead49d83b8650799
Predicate: r23f-sentfxprivacy
Scope: executed=none
