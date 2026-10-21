# FxC1Policy — falsification of C1 source/policy separation

Reviewed-SHA256: 1dc94c5f733a9a0112c5db0e94dda5eca31e4f2d982950bc56e08461040d7dd7
Predicate: C1-source policy separation

Primary: `.ufo/waves/round-21/candidate/corpus/knowledge/selector-contract-r21.json` at candidate revision 0a14952b59d20179e1c813af58befaecd6992a17. The SHA-256 above is the predispatch digest declared in `candidate-files.json`. I read the file and did not recompute the digest, because NO-EXEC rules that out.

Auxiliary snapshot dependencies, all read from the frozen candidate tree with digests taken from `candidate-files.json`:
- `tools/check-selector-contract.py`: 239758b49da4f24415f53adb52cc6833818d0e340f0832d0389416bce50aea50
- `corpus/knowledge/selector-contract-r21.md`: b4966a9bcf4ac124a964718b0ed76104e2f07c41b63050dc8bda618ea5136353
- `tools/_revision.py`: 06b71e8cb4aa541a25c95301106dc4d3ad9566cf18ec834f226ec0708db58cbf
- `corpus/SOURCES.md`: ef697b7c6b60bf0e5b71e1267f30cda678d5de01abc803b24dcc7dce1b93c3e4
- `corpus/QUALITY.md`: 1ac6354185c4685f87fba07c702132b87e8102c44412871e5a13622ea6948596
- `corpus/lessons/round-21.md`: ab841b2562e41fa69f90b63b8444d5ab47670ce2acf0ec1208f71cf7980349c9
- `SCORECARD.md`: 04403120de891fa8eb1c90276da8ea339ec2b0f46442940dbd0fdd5d86ae4e25
- `SKILL.md`: c43477cbb012fe0b0c4170610d4fa034d2e8ae5b09005e3f48a4cccd38f843b3

Unpinned evidence I also read, outside the candidate inventory:
- `.ufo/waves/round-21/sources/git-types.txt`, the retained S081/S082 extract. It is used only for what the sources say.
- `.ufo/waves/round-21/build/ExecDecision.md` and `.ufo/waves/round-21/drafts/ExecDecision/selector-contract-r21.json`. These are advisory only and are not production.

## Axes

- Depth: whether each row is grounded in its source.
- Calibration: whether provenance and attribution are true.
- Operability: whether the gate defends the claim it counts.
- Scope and safety: whether any host certification is made.

## Verdict

The predicate holds in the prose, the source registry and the lesson. It is only weakly represented in the primary JSON, and the checker does not defend it.

I found no counterexample in which any candidate file claims that S081 or S082 defines the landed, pushed or origin-ref policy. I also found no host certification.

There is one fixable defect. The JSON's single per-row `source` field attributes each lane-policy outcome and finding ID to a Git manual. The separation between Git semantics and lane policy survives only in free-text rationale, and the checker never inspects that text. This is a fixable defect, not a tradeoff that the canonical judge would have to reject.

## Observations (read from bytes)

**O1. The explicit lane-policy paragraph exists.** It is in the `.md` file under the heading "Source proposition and lane policy" (lines 9–15):

> "Those object-prefix/ancestry/push restrictions come from the lane's evidence contract, not these manuals."

Line 25 says that "Pushed" means "only the local origin tracking ref when present, as defined by the binder. It does not prove current remote reachability or hosting-service state."

**O2. The prose matches the canonical binder.** I checked each lane-policy statement in the prose against the binder, and none of them introduces a second authority:
- `_revision.py` line 41 (`REV`) requires 7–64 hex characters.
- Lines 112–145 enumerate object IDs and peel only tags with `^{commit}`.
- Lines 180–191 check the local branch for ancestry, and check `refs/remotes/origin/<branch>` only when it exists.
- QUALITY 27 (line 37) says the same, using the phrase "when present".

**O3. The registry separates the policy as well.** In `SOURCES.md`, the S082 row (line 89) has the scope cell "Verification of existing object type, separate from lane object-prefix, landed and pushed policy" and the proposition "a valid object ID alone is not a commit or a landed/pushed certificate". The S081 row (line 88) has the scope cell "not lane branch ancestry or host health". Lesson line 50 names the policy authority as "QUALITY27/36/shared-binder contract, distinct from S081/S082's Git semantics".

**O4. The retained source extract contains no landed, pushed, ancestor or origin wording.** Searching `git-types.txt` for push, landed, ancestor and origin returned nothing. Its only statements are:
- the S081 typed-peel example;
- the S081 statement that `^{}` peels recursively until a non-tag object is found;
- the S082 statement that "you can add the `^{type}` peeling operator".

So nothing in the extract could ground the landed/pushed policy.

**O5. There is no host certification.**
- The JSON contains no host, boot, package or service terms.
- `.md` line 7 says the entry does "not change host state, certify a boot image".
- The checker's docstring says it is "not a consumer-execution or host-health certificate".
- The checker's `scope` string says "not consumer behavior or host health".
- `SKILL.md` line 2125 says "No host or package/service/boot action follows any result."

**O6. Counterexample: the JSON's provenance cannot express the separation.** Each row has exactly one `source` value, and that value is a Git manual:
- `commit` is `accept-if-landed-and-pushed` with source S082.
- `tag-to-commit` is `accept-if-landed-and-pushed` with source S082.
- The three refusal rows carry `E-REVISION-INVALID` with source S081.

The outcome tokens and the finding ID `E-REVISION-INVALID` are lane constructs from QUALITY 27/36 and `_revision.py` lines 44–49. The JSON has no field naming the policy authority, and its top-level `sources` list contains only `["S081","S082"]`. A reader of the structured data, rather than the prose, sees S082 as the source of "landed-and-pushed".

The rationale strings carry the caveat ("lane ancestry and origin tracking checks remain separate", and "must satisfy lane ancestry policy"), but they do so unevenly:
- The `tag-to-commit` rationale mentions ancestry but omits push and origin.
- The refusal rows never say that the finding ID is lane policy.

**O7. Attribution in the JSON and the prose disagree.** In the prose table, the Sources column reads "S081, S082" for every row. In the JSON, each row has a single source, split as S082 or S081. The checker compares neither.

The `tag-to-commit` row attributes "recursively peel" to S082. In the retained extract, recursion is stated only by S081, and only for `^{}`; the S082 extract says nothing about recursion.

**O8. The checker's scope does not cover separation.** `check-selector-contract.py` lines 70–82 verify only these things:
- the `(outcome, finding)` tuple against the hard-coded `EXPECTED`;
- that `source` is either S081 or S082;
- that the rationale is a non-empty string;
- that one prose row starting with `| <class> |` contains the outcome substring, plus the finding substring when the finding is not null.

The checker never reads the lane-policy paragraph, line 25, the rationale content, or the prose Sources column. Its own selftest fixture (lines 101–104) labels all five rows, including both `accept-if-landed-and-pushed` rows, as `"source": "S081"`. This confirms that the source field is checked for membership only.

**O9. The advisory draft diverges from the candidate.** `build/ExecDecision.md` says its draft "refuses acceptance when no `origin/<branch>` tracking ref exists". The candidate did not adopt this, and it keeps the binder's "when present" rule. I count this in the candidate's favour: the draft's rule would have been a second, conflicting "pushed" authority alongside QUALITY 27 and `_revision.py`. The draft rows also had a `proposition` field, and its commit row's proposition separated "acceptance additionally requires landed and pushed ancestry". The candidate dropped that field, leaving the structured rows with less separation than the draft had.

## Source predictions (not executed)

**P1. Separation can be deleted without the gate noticing.** Suppose I delete `.md` lines 13–15 and 25, and change the `commit` rationale to "S082 certifies landed and pushed commits". I predict `--revision` on that commit returns exit 0 with `decision_rows` 5. The reason is that no code path in lines 35–82 reads those bytes. This is a prediction from reading the source, not an execution.

**P2. The prose substring match is weak.** Take the prose row `| commit | ... | refuse | ... accept-if-landed-and-pushed ... |`. I predict it still counts as supported, because the accept rows check only that the outcome substring is present (line 75, with `finding is None`). Similarly, a `tree` prose row that contains "accept-if-landed-and-pushed" in its Git-distinction column, alongside `refuse` and `E-REVISION-INVALID`, passes.

**P3. Swapping source attributions is invisible.** If every row's `source` is changed to S082, including the tree refusal row whose grounding is in S081, I predict the result is still PASS 5/5.

## Limits

- [INFERENCE] The full S081 page probably also states that typed `^{<type>}` peeling is recursive, and the glossary defines commit-ish. Neither is in the retained extract, and I made no network read. So "tree/blob is not commit-ish" and the nested-tag recursion are grounded only partly by retained bytes.
- S082 repeats S077's URL (`SOURCES.md` lines 84 and 89) for a narrower scope. Line 146 discloses this. It is not a policy issue.
- Every statement above is either a reading of bytes or a source prediction. No gate, selftest, mutant or Git command was run.
- I installed no tools; none was needed for this source review.
- Prior source-only reviewers are not outside closure. I claim no non-author closure and no promotion.

## Smallest safe correction (for L1 to decide)

1. In each JSON row, add a policy field, for example `"policy": "QUALITY27/QUALITY36 via tools/_revision.py bind; origin ancestry only when refs/remotes/origin/<branch> exists"`. Narrow `source` to the Git proposition only. Change the `tag-to-commit` source to S081, or allow both sources. The checker's fixed `EXPECTED` tuples and the preregistered outcome tokens stay unchanged, and the checker accepts extra keys.
2. Optionally, have the checker require that the policy field is present and non-empty on every row, and that the `.md` contains the "not these manuals" sentence. Add a selftest mutant that deletes the separation and must fail. This closes P1 without renaming any frozen outcome.

Either change alters the primary bytes, so this receipt's Reviewed-SHA256 would no longer apply and a fresh snapshot would be needed.

Lane bounds: leaf member — no subagent dispatch.
Scope: executed=none
