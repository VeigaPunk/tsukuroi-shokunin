# ClaimSeparation — round 14 C1/depth repair review (report only)

Lane: TsukuroiR14.ClaimSeparation. Baseline 8606bad4cbc6451ac2890c9f8e2548a36c386db6. Observed 2026-10-20. No tests, builds, gate runs, or writes outside this report.

## Verdict

C1 (depth) is a repair, not a new capability. Keep its two defects separate, each with its own quoted source and its own notice:

- **R14-VALUE-DOMAIN** repairs `corpus/knowledge/root-dac-correction-r13.md:97`.
- **R14-COMMENT-ATTRIBUTION** repairs the S042 self-description in `corpus/SOURCES.md:48`, the matching r13 lesson sentence (`corpus/lessons/round-13-verifier-spotcheck.md:155-163`), and the QUALITY criterion 20 cross-reference.

Depth is not scored higher by this round. The repair removes source-inconsistent prose; it does not add a new ordinal point. Any gate pass is structural conformance, not source truth.

## Evidence

E1. ProtectSystem definition (systemd.exec(5), https://man.archlinux.org/man/systemd.exec.5, fetched 2026-10-20, § ProtectSystem=): "Takes a boolean argument or the special values "full" or "strict"." That is 11 whitespace words. The same paragraph says "This setting cannot ensure protection in all cases." That sentence limits the setting's efficacy; it does not enumerate a mechanism set. The source never says "non-exhaustive".

E2. r13 MD:97 says "the value set is not exhaustive" about ProtectSystem values. That contradicts E1 as a description of the option's domain. The correct non-exhaustive claim is about unit-side mechanisms (S041: BindReadOnlyPaths=, TemporaryFileSystem=, RootDirectory=, RootImage=, ReadOnlyPaths=). Other active "exhaustive"/"non-exhaustive" uses are mechanism-scoped and correct: r13 MD:31, :84, :102; r13 JSON `alternatives_scope`, :120, :157; snapper-eacces-mechanism.md:101. Do not treat them as defects.

E3. #8047 comment 6071740243 (author login omarchybot). Fetched through the github.com issue page's embedded JSON, because the API endpoint returned HTTP 403 and then a rate-limit message to this IP. Body length 2980 characters. Negative sweep of the body for model, generated, automated, triage, AI, LLM, Claude, bot: **0 hits each**. Body propositions, each separable:
- VM execution assertion (unverified; reported action): "I tried this on a stock Omarchy worker VM and could not reproduce the central claim" — 16 words.
- Second opinion: "Codex Medium reviewed the same evidence and upstream files and reached the same conclusion." — 13 words. Followed by "It may have seen this analysis first, so its agreement is not guaranteed to be independent."
- Maintainer deferral: "The remount failure is #6634, which is waiting on the maintainer to decide whether snapshot boots should keep the overlay." — 20 words.
- Reporter request: "This now waits on your answer." — 6 words. This defers to the reporter, not the maintainer.

E4. Account fields (API user type User, association COLLABORATOR, login omarchybot) come from the existing S042 row. I did not re-verify them through the API this session. The HTML embedded JSON shows author `__typename` User, login omarchybot, createdAt 2026-10-09T00:27:22Z, databaseId 6071740243, matching the row.

E5. #6629 disclaimer ("This review is by Claude Opus 5.5 alone.", 23 words; "Nothing was run on a machine.", 6 words) is comment 6234472369 under S043. It is not in #8047 and cannot be transferred.

## Separation rules for the new pair

R14-VALUE-DOMAIN:
- Append a notice after the provenance trio in r13 MD, naming line 97's phrase "the value set is not exhaustive" as retired. Do not edit line 97's bytes.
- Domain proposition: quote E1 (11 words) and cite S044. Do not cite S044 for non-exhaustiveness.
- Mechanism proposition: cite S041 for each named alternative and mark "the mechanism set is not closed" as [INFERENCE] from those alternatives.
- Do not add boolean spellings (yes/no/on/off) to the domain claim unless citing systemd.syntax(7). That page lists "1, yes," and "0, no, false and off" as equivalent; I did not read the full positive list.

R14-COMMENT-ATTRIBUTION:
- Keep S042 bytes unchanged. S045 supersedes S042 with a "supersedes S042 — REJECTED:" teaches. Its three propositions are: verified account fields; unverified VM assertion (E3, 16-word quote); Codex Medium second opinion (E3, 13-word quote); maintainer deferral (E3, 20-word quote).
- Host-cause rejection stays. Maintainer acceptance is rejected. No "self-described", "model-generated", or "automated triage" wording for #8047.
- Append a notice in the r13 lesson before lines 155-163. Keep the historical text.
- Wave-local copies (SourceRegistry.md, IssueBot8047.md, SourceContractReview.md:64, round-13.md:68-71) repeat the same wording. They are historical and out of scope; do not cite them as evidence.

## Harm checks for other axes

- **Coverage:** S041–S043 must stay. S044 uses the same URL as S041, and S045 may use the same URL as S042. Expect census W04 duplicate-URL warnings and disclose them; they are not census failures. Re-measure tier and status counts after landing; do not predict them.
- **Operability:** the checker must be read-only, network-free in selftest, and must key on replacement sentences and the domain construction ("value set" or "value domain" near ProtectSystem). A bare "not exhaustive" match would false-fail the correct mechanism-scope sentences in E2. A check that only looks for the word "boolean" would false-pass a sentence that still claims exhaustiveness. Conformance is not truth.
- **Freshness:** the API returned HTTP 403 and a rate-limit message on 2026-10-20. State the access route used for S045 (HTML embedded JSON, or API when it works). I did not verify the systemd 262.1 footer in this session; carry it as the existing S041 anchor, not as a fresh observation.
- **Calibration:** keep #8047 in tier C and rejected. "I tried" is a reported action, not a reproduction. "Waits on your answer" is not a maintainer decision.
- **Adjacency:** QUALITY.md criteria 19 and 20 already state R14-SOURCE-SCOPE and the #8047 attribution rule. Cite them; do not duplicate. No other lane, fleet, MANIFEST, or routing file is touched.

## Recommendations

1. Land R14-VALUE-DOMAIN as an appended notice plus a new MD/JSON pair. Keep line 97 bytes; name it as retired.
2. Land R14-COMMENT-ATTRIBUTION as an S045 row plus a lesson notice. Keep S042 bytes; cite the three body quotes with their word counts.
3. Gate: assert the notice exists, each quote is ≤25 words and appears in the stored literal snapshot, and no active replacement pairs "value set" with "exhaustive". Name the output "bounded conformance" in the summary.
4. Report S045's access route. Note the API 403 and rate-limit observed today.

## Limitations

- No verification commands were run, per contract.
- The #8047 API fields are carried from the existing row, not re-fetched.
- The systemd 262.1 footer and the full systemd.syntax(7) positive boolean list were not re-read.
- No checker was built or run.

## Tooling record

- Installed or updated: none.
- Used: curl and python3 (stdlib) for read-only fetches and a body sweep. Scratch files in /tmp were created and removed; no repo writes other than this report.
- Privileged probes, package transactions, services, snapper, commits: none.
