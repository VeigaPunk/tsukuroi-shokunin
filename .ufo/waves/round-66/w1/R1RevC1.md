# R1RevC1 — C1-ATTACK scoped findings (round 66, w1)

Timestamp: 2026-11-03T21:01:32Z · Full evidence: .ufo/waves/round-66/drafts/rev-c1.md

## Scope
Independent re-derivation of claim C1 (SOURCED, S283): re-fetch + hash of the systemd v262 release JSON, bullet location/text, quote budget, SOURCES counter semantics, and the base do-nothing control. Lane base c68bfe97. No tracked file touched.

## Findings (severity: none critical)

1. AGREE (A1, source identity) — `curl https://api.github.com/repos/systemd/systemd/releases/tags/v262` → HTTP 200, rc 0, sha256 `008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b` — exact match to the frozen S283 hash and to scout-s283-scope.md's independent fetch.
2. AGREE (A2, bullet) — body line 248 (wraps to 253) under section header at body line 155 `## Changes in the system and service manager:`; verbatim values strict=never / tofu=first boot or no TPM2 / relaxed=SecureBoot disabled or no TPM2, default and previous behavior / off=always; scope = "null"-key boot credentials only (lines 249, 252–253). Matches the frozen predicate clause-for-clause. published_at 2026-09-22T13:19:16Z matches S282 (SOURCES.md:292).
3. AGREE (A3, quote budget) — cited values sentence counts 24 words (`wc -w`), <= 25.
4. AGREE (A4, counters) — header line 5 has 11 columns; `awk -F'|'` NF=13 for header, S282 row (SOURCES.md:292), and an S283-shaped simulated row; `grep -cE '^\| S[0-9]{3,}'` counts the simulated row and the S282+S283 pair (2). Live count 282 = exactly the frozen floor minus S283.
5. AGREE (A5, do-nothing control) — at base c68bfe97: `git cat-file -e c68bfe97:corpus/knowledge/systemd262-credentials-boot-policy-r66.md` → rc 128 "does not exist"; `git show c68bfe97:corpus/SOURCES.md | grep -cE ...` → 282. Predicate fails at base as required.
6. PENDING-LAND (A6, no defect) — `corpus/knowledge/systemd262-credentials-boot-policy-r66.md` not yet in the working tree (ls rc 2), so `grep -c '^| CB' >= 5` is unrunnable right now; it is the C1 scribe's in-flight deliverable. L1 should expect this file at integration and run the CB-row count then.

## Verdict
C1-PREDICATE-SOUND
