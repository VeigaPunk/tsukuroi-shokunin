2026-11-03T22:38:19Z
# K1Critic — falsification of the round-68 declaration (SCORECARD.md "Round 68 — declaration", L5099–L5136)

Base 42400ec6; lane HEAD 3f6edcc9 (one commit, the declaration itself; `git rev-list --count 42400ec6..HEAD` → 1).
Declaration lines cited as L####. Evidence receipts: refetch of the 8 pinned files and sha256sum -c (run this round, rc 0).

## Attacks

**A1 — C1 do-nothing control (six RW rows copying the table text, no v7.3 line). FALSIFIED.**
Frozen predicate (L5119 before→after cell): `note present; grep -cE '^\| RW[0-9]+ \|' ≥ 6; SOURCES ≥ 287 …; awk NF==13 on both new rows; each Gate quote ≤ 25 words; receipt before/src/SHA256SUMS committed; knowledge-header PASS; census validate rc 0`.
Counting command (L5119 counting cell): `git show <rev>:…linux-v73-pinwatch-r68.md | grep -cE '^\| RW[0-9]+ \| '`, the SOURCES count, the census command.
Reasoning: the do-nothing note passes every clause. Six RW rows satisfy the count; a copied row has 13 fields; a copied quote is ≤ 25 words; `knowledge-header PASS` checks only `source:` presence (tools/check-knowledge-header.py at base, RULES line 202: `"source": None`); census rc 0 does not inspect RW content. No clause tests for a v7.3 line number, a v7.3 sha string, or the applicability line. The only rejector is the claim-cell text ("each with a verdict, a located v7.3 anchor and an applicability line", L5119), and no command in the counting column enumerates it. Smallest correction: add a counting command that requires, per RW row, a `v7\.3` token plus a `:<digits>` line anchor and the full 64-hex sha of the v7.3 file, e.g. `grep -cE '^\| RW[0-9]+ \|.*v7\.3.*:[0-9]+'` ≥ 6, and grep the full sha strings from SHA256SUMS in the note.

**A2 — C1 counting-command gaps. FALSIFIED.**
(a) "S286 directly after S285; S287 directly after S286" (L5119 predicate) is counted only as `grep -cE '^\| S[0-9]{3,}'` ≥ 287; adjacency is not tested.
(b) `awk -F'|' 'NF==13'` (L5119 counting cell) is not a count, has no threshold, and is not scoped to the two new rows; it prints a result and does not produce a pass/fail value.
(c) "receipt before/src/SHA256SUMS committed" and "knowledge-header PASS" have no command in the counting column.
Smallest correction: state the command, the expected count, and the scope for each clause.

**A3 — C2 always-exit-0, no-findings tool, judged on the conjunction. SURVIVES.**
Declared clauses (L5120 before→after cell): `--selftest PASS rc 0`; `on a fixture note citing source: S999: header gate rc 0 (passes) and new gate rc 1 with finding KNOWLEDGE-REF-DANGLING`; `live corpus at the work revision: rc 0, 0 findings`.
The stub passes the live clause and can pass the selftest clause only if the selftest is also a stub. It fails the S999 clause because it returns rc 0 where rc 1 is required. The S999 red clause is the one that kills it, and it is conjunctive (`and`), so the stub cannot satisfy the declared predicate. Caveat recorded in A4.

**A4 — C2 selftest clause alone (no case count enumerated). FALSIFIED as a standalone clause.**
L5120: `--selftest PASS rc 0`; the claim text asks for ≥ 8 cases, but the counting command (`python3 tools/check-knowledge-refs-r68.py --selftest`) is not tied to a count. A selftest that asserts nothing and prints PASS passes that clause alone. The conjunction in A3 rescues the predicate only if the S999 fixture is pinned. L5120 does not pin it: the fixture is "a fixture note citing source: S999" with no committed path or content, so the seat authors the red case. Smallest correction: name the committed fixture path and require `--selftest` to report a case count ≥ 8.

**A5 — C2 base pre-scan reproduces. SURVIVES.**
`$ git ls-tree -r --name-only 42400ec6 corpus/knowledge/ | grep -c '\.md$'` → 85. Registry ids `git show 42400ec6:corpus/SOURCES.md | grep -oE '^\| S[0-9]{3,}' | sort -u | wc -l` → 285. Non-fenced `source:` lines across the 85 notes: 110; distinct S-ids cited: 188; `comm -23 cited registry` → empty, rc 0 → 0 dangling. Matches L5114–L5115 ("85 notes, 285 registry ids, 0 dangling").

**A6 — Kill-rule wiring for sha pairs. FALSIFIED.**
Kill rule (L5119 kill cell): `a sha pair does not reproduce → honest stop`. No command in the counting column reproduces a sha. The only sha-adjacent counting item is the existence check "receipt before/src/SHA256SUMS committed". The reproduction command (`curl -s --max-time 60 -o <file> <url>; sha256sum`) is in before/src/FETCH.txt (method line), not in the declaration. The kill rule is therefore not executable from the declared commands. Smallest correction: add `(cd …/before/src && sha256sum -c SHA256SUMS)` and the FETCH.txt refetch loop to the counting column, and require 64-hex shas in the note.

**A7 — sha pairs reproduce; no pair is absent from the declaration. SURVIVES.**
`$ cd …/round-68/before/src && sha256sum -c SHA256SUMS` → 8 × OK, rc 0.
Independent refetch of the 8 URLs in FETCH.txt (curl, rc 0 each) into a scratch dir, `sha256sum` → identical to SHA256SUMS for all 8 (diff of sorted hash lists, empty).
Pairs: S138 a9433bb0…→2750c11a… (L5108); S158 ce146120…→098cb522… (L5108); S149/S182 452f1348… both tags (L5109); S185 11c6b712… both tags (L5109). S286 (cgroup-v2 v7.3) and S287 (sysfs v7.3) hashes are the v7.3 halves of the S138 and S158 pairs, so no pair is missing. Caveat: the declaration cites 8-hex prefixes only (`a9433bb0…`); the 64-hex strings exist only in SHA256SUMS. A note that cites a prefix passes any prefix check.

**A8 — Universal-clause check on the two predicates. FALSIFIED (1 unenumerated).**
Universal words in the frozen predicate cells (L5119, L5120):
- C1 predicate: `each Gate quote ≤ 25 words` ×1. No counting command. UNENUMERATED.
- C2 predicate: no all/every/each/no/complete; "0 findings" is a count over the corpus that the tool itself performs (`--revision <rev>`), enumerated only once the tool lands (see A9).
Claim-cell universals (not predicates): C1 `each with a verdict, a located v7.3 anchor and an applicability line` (no command); C2 `reads every corpus/knowledge/*.md` and `for any id absent` (delegated to the tool, unverifiable before landing).
Predicate-scoped count of unenumerated universals: **1**.

**A9 — C2 universals and live-corpus enumeration. INCONCLUSIVE.**
Whether `check-knowledge-refs-r68.py --revision <rev>` enumerates every `corpus/knowledge/*.md` cannot be tested: the tool is absent at base (`git cat-file -e 42400ec6:tools/check-knowledge-refs-r68.py` → rc 128). Re-test after landing: count the notes the tool reads and compare with 85 (base) plus the new note.

**A10 — S138 pre-declaration anchor line numbers. FALSIFIED (minor).**
`$ grep -n "oom_kill" before/src/v72-Documentation_admin-guide_cgroup-v2.rst` → line 1506 (`\t  oom_kill`); `sed -n '1505,1508p'` shows the same. Declaration L5110–L5111 states `oom_kill 1507 → 1533`. v7.2 line is 1506; v7.3 line 1533 is correct. The byte quote is identical; the declared v7.2 line number is wrong by one.
memory.events 1468 → 1495 (confirmed); memory.events.local 1517 → 1544 (confirmed).

**A11 — S158 comment-only hunk at :1339. SURVIVES.**
`$ diff v72-fs_btrfs_sysfs.c v73-fs_btrfs_sysfs.c` → one hunk, `1339c1339`, the only change is `parameter` → `parameters` in a comment. Matches L5111. S138 diff has 17 hunks; the declared "changed hunks named and shown outside the memory-controller section" (L5119) is not verified (INCONCLUSIVE, not counted).
S149/S182 (oom_kill.c) and S185 (psi.rst): `cmp` v7.2 vs v7.3 → rc 0 identical.

**A12 — Do-nothing controls at base. SURVIVES.**
`$ git cat-file -e 42400ec6:corpus/knowledge/linux-v73-pinwatch-r68.md` → rc 128 (note absent).
`$ git cat-file -e 42400ec6:tools/check-knowledge-refs-r68.py` → rc 128 (tool absent).
`$ git show 42400ec6:corpus/SOURCES.md | grep -cE '^\| S28[67] '` → 0 (rc 1).
Each control fails the claim's before-state, so the after-state is not reached by doing nothing.

**A13 — Window claim: "r66 and r67 entered none; window at 2 of 3". SURVIVES (TRUE).**
Window rule: SCORECARD L180 `stagnation window N = 3 rounds without a new capability row`.
Last entry: L4870 `| initramfs-arm | … | round 65 |`; L4905 "capability initramfs-arm entered r65".
r66 measured outcome: section L4949–L5013; L4994 `Capabilities: none entered this round.`
r67 measured outcome: section L5043–L5097; L5087 `Capabilities: none entered this round (…)`.
Capability tables: `grep -n '| Capability |'` lists 11 headers; the only row under any r65–r67 header is L4870 (initramfs-arm, round 65). No r66 or r67 row exists.
Count: r66 and r67 with no entry = 2 of 3; r68 with no entry would reach N=3. Declaration L5101–L5103 is consistent with this.

## Summary
ATTACKS=13 · FALSIFIED=6 (A1, A2, A4, A6, A8, A10) · SURVIVES=6 (A3, A5, A7, A11, A12, A13) · INCONCLUSIVE=1 (A9)
UNENUMERATED_UNIVERSALS=1 (predicate cells; plus 2 claim-cell universals without a command: C1 "each with a verdict…", C2 "every corpus/knowledge/*.md")
WINDOW_CLAIM=TRUE

## Installs / tooling
None. Read-only git, sha256sum, curl (GET to raw.githubusercontent.com only), grep, awk, comm, diff, cmp. Scratch under /fast/scratch/hyaku/tsukuroi-r68/K1Critic, removed.
