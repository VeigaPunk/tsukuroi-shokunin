# PredicateReview — round-14 repair (TsukuroiR14.PredicateReview)

Scope: read-only review of the r13 gate and its inputs; no gate execution, no tests, no verification commands. Only write is this file.

## 1. Why MD:97 passes the current gate

Defect (observed): `corpus/knowledge/root-dac-correction-r13.md:97`, replacement cell for `r12 MD:41-42`, says "the value set is not exhaustive" after naming ProtectSystem values. S041 defines the option as "a boolean argument or the special values full or strict" (outside-lesson reopen, round-13-verifier-spotcheck.md:143-153). Non-exhaustiveness belongs to unit-side mechanisms; the same entry says so at MD:31 and in `replaced_b2_claims[0]` of the JSON.

Gate blind spots in `tools/check-root-dac-correction.py`:
- L28-30 `OLD` and L31 `OVER` match only "only strict ... would make ... read-only" and "proves ... general ... correctness". MD:97 ("is the only value that covers") matches neither, so `active-exclusive` cannot fire.
- L112 `nonexhaustive` is whole-text substring: `"non-exhaustive" in low or "not the only" in low`. It is satisfied by MD:31 regardless of MD:97. MD:97's phrasing ("not exhaustive", no hyphen) matches neither token, and no negative predicate exists for it.
- L100-104 heading chain lists 5 headings. "## Replaced round-12 B2 statements", where MD:97 lives, is not in the list. No predicate is section-scoped.
- L256-262 selftest `MD13` fixture contains no replacement section, so no case exercises it.
- L124-157 `json13_issues` reads only named keys. It never reads `replaced_b2_claims`, `protect_system_values` or `preserved_exceptions` for scope, so no MD-vs-JSON cross-check exists.
- All checks are presence-based. A passing count shows tokens exist somewhere, not that a sentence is correctly scoped. QUALITY #17 states this rule; the gate does not implement it.
- gate_contract JSON lists 10 headings; the checker enforces 5 (already routed as lesson item 4).

## 2. Why attribution has zero gate coverage

- The gate reads four files only (L20-23: r12 MD/JSON, r13 MD/JSON). It never reads `corpus/SOURCES.md`, `corpus/lessons/round-13.md`, `LOG.md` or `corpus/QUALITY.md`.
- Defect surfaces: S042 row `corpus/SOURCES.md:48` and S043 row `:49` both say "self-described model-generated automated triage"; `corpus/lessons/round-13.md:68-70` repeats it for all bot comments.
- Captured #8047 body (`.ufo/waves/round-13/correction/IssueBot8047.md:10-37`) contains no "model-generated" or "self-described". It contains "Codex Medium reviewed..." (L27, L34) and the reported VM attempt (L39). The live API fetch of `comments/6071740243` returned HTTP 403 from this seat, so the capture is the only body evidence here.
- Captured #6629 body (`IssueBot6629.md:26-28`) does contain "This review is by Claude Opus 5.5 alone." and "Nothing was run on a machine." The self-description is real for S043 and is being transferred to S042. Transfer is the defect.
- `corpus/QUALITY.md` #20 (working tree at read time) already forbids calling #8047 self-described model-generated triage. The S042 row contradicts it and no check enforces QUALITY.

## 3. Proposed bounded predicates (new checker, e.g. `tools/check-source-scope-r14.py`; not written, not run)

Active surfaces: the new MD/JSON pair, active (non-superseded) `corpus/SOURCES.md` rows, `corpus/lessons/round-14.md`. Historical blobs at baseline `8606bad4` are exempt only by pinned blob hash, never by a marker in the text (a marker-based exemption would hide defects).

Value domain (VD):
- VD1 open-domain unit: split active text into units (table cells and sentences on `. ` / `; `). FAIL `VALUE-DOMAIN-OPEN` when a unit contains `exhaust|not the only|open set|closed` AND `ProtectSystem|value`, AND lacks `mechanism`. Red fixture: MD:97 cell verbatim, must FAIL. Green fixture: "the unit-side mechanism set is not exhaustive", must PASS.
- VD2 finite domain: every token following `ProtectSystem=` in active surfaces must be in `{no,yes,true,false,full,strict}` (case-folded). Basis: S041 quote. Boolean synonyms (`on/off/1/0/y/n`) come from systemd parse-boolean semantics, not S041; they stay out of the set until a source row exists. [INFERENCE] until then.
- VD3 cross-file scope agreement: for each pointer present in both the MD replacement table and JSON `replaced_b2_claims`, both must use the same scope noun ("mechanism" or "option"); mismatch FAILs. This would have flagged MD:97 against JSON `replaced_b2_claims[0]`.
- VD4 "only" scoping (QUALITY #17): a unit containing `only` + a mechanism name (`ReadOnlyPaths=|BindReadOnlyPaths=|TemporaryFileSystem=|RootDirectory=|RootImage=`) + `read-only|EROFS`, without `among ProtectSystem`, FAILs. Known false-positive risk on prose that negates ("not the only").
- VD5 section coverage: scan every `## ` section for VD1-VD4, not a fixed heading list. Minimum: add "## Replaced round-12 B2 statements" and "## Preserved exceptions" to the required list, with a fixture that deletes each.

Attribution (AT):
- AT1 comment binding: any sentence naming comment ID N must match ID, login, `user.type` and `author_association` exactly against a committed JSON snapshot of that comment (not the markdown summary). Equality check.
- AT2 anti-transfer (the key predicate): a self-description phrase (`self-described`, `model-generated`, `generated by`, `Claude`, `LLM`) attributed to comment N must be backed by a verbatim quote of at most 25 words located in N's own body snapshot. Red: S042 row against the `6071740243` snapshot (no such quote) must FAIL. Green: S043 against `6234472369` snapshot ("This review is by Claude Opus 5.5 alone.", 8 words) must PASS.
- AT3 reported execution: sentences quoting VM-execution or restore claims ("worker VM", "I tried", "restore completed") must contain `reported|claimed|unverified` in the same cell.
- AT4 quote budget: every `quote` field is at most 25 whitespace words and is verbatim in its snapshot.
- AT5 immutable rows: for each S-row present at baseline `8606bad4`, the candidate row bytes must equal baseline bytes. Supersession requires a new row carrying `supersedes: S042` (new ID). Implement with the existing `read_git` pattern (L231-241).

Acceptance (for L1, not run here): every predicate needs a red fixture from the defective r13 bytes (MD:97; S042 row) that FAILs, and a green fixture from corrected text that PASSes. Per QUALITY #19, the fixed correction does not count until the checker fails the preserved defects.

## 4. Limitations to state in the new checker header and the round-14 lesson

- Lexical and presence-based. It does not establish source truth or semantic scope, and misses paraphrases outside the token lists (for example "other values may exist" needs an added token).
- Depends on committed snapshots from 2026-10-20 (man page footer systemd 262.1; host 261.2-1). It cannot recheck live GitHub or the man page at run time; this seat's API read was 403.
- Scope is a fixed file list. Anything not listed (LOG, QUALITY, lessons) is invisible unless added explicitly.
- Passing is conformance only. Fresh non-author review is still required before admission.
- Old r13 gate stays a historical narrow checker, as the contract requires; the new checker must not reinterpret its counts.

## 5. Recommendations (ranked)

1. Commit MD:97 verbatim as a red fixture before drafting the fix; VD1 and VD5 must fail it.
2. Put the new checker in its own file. Do not extend the r13 gate's 4-file scope or its presence-only checks.
3. Commit the #8047 and #6629 body snapshots as JSON with sha256 so AT1-AT4 read bytes, not summaries.
4. Use AT5 to keep S042/S043 byte-identical and add S045 as a superseding row.
5. Do not treat lesson or LOG prose as source evidence in any predicate.

## 6. Tooling record

- Tools installed or updated: none. Reads and grep only. No package transactions.
- One GitHub API fetch (`comments/6071740243`) returned HTTP 403; not retried, no auth attempted.
- No gate was executed; no tests, builds, lint or smoke runs.
