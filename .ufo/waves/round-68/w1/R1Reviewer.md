2026-11-03T22:31:37Z — R1Reviewer (round 68 w1, C1 attacker). Full receipt with every command and output: .ufo/waves/round-68/drafts/c1/R1-attack.md

FINDINGS BY SEVERITY

F1 (declaration fact, FALSIFIED): SCORECARD.md:5112 anchor drift "oom_kill 1507 → 1533" does not reproduce. v72:1507 is "The number of processes belonging to this cgroup"; v73:1533 is the label "	  oom_kill". Byte-identical pairs: 1506→1533 (label) or 1507→1534 (description). The other two declared pairs (1468→1495, 1517→1544) reproduce. The note draft's sentence anchors (1474→1501, 1508→1535, 1518→1545) all reproduce.

F2 (declaration sub-claim, FALSIFIED): SCORECARD.md:5119 "the changed hunks named and shown outside the memory-controller section". Hunk 1912c1939 sits inside the Memory section (heading at v72:1267, next heading IO at v72:1982): v72:1912 "A read-only nested-keyed file." → v73:1939 "A read-write nested-keyed file." (memory.pressure access mode). The note draft itself reports the true map (CPU 6, Memory 1, IO 3, Cpuset 1, RDMA 3, DMEM 1, Misc 1; 16 unified hunks) — the frozen declaration text contradicts its own evidence.

F3 (predicate falsifier): the declared counting command `git show <rev>:…pinwatch-r68.md | grep -cE '^\| RW[0-9]+ \| '` ≥ 6 accepts a boilerplate-only six-row fixture (copied text, no located anchor, no command: grep prints 6) and even six identical duplicate-id rows (prints 6). The declared strictness ("distinct ids, a non-empty evidence cell") is enforced by no declared command; only the prose kill rule could catch it.

F4 (declaration wording, FALSIFIED as definite description): "The five v7.2-pinned registry rows" — the registry holds 11 rows pinning v7.2-family bytes of the same four files (SOURCES.md :121,124,125,139,144,155,164,184,188,191,252 = S115,S118,S119,S133,S138,S149,S158,S178,S182,S185,S243); QUALITY.md:192 scopes the watch to any on-release row pinning the tag. All four files were re-read, so the six unmentioned rows' verdicts are derivable from the same pairs and none flips; the count wording is wrong. S243's stable-series trigger additionally unaddressed (kernel.org outside allowed sources: BLOCKED).

VERIFIED SURVIVORS
- SHA pairs: 8/8 recomputed from pinned bytes = SHA256SUMS = committed blobs at 3f6edcc9 = live upstream via api.github.com contents (sizes match too). Raw.githubusercontent.com FETCH.txt URLs 404 from this seat today (control: master README rc 0; tags API lists v7.2/v7.3) — channel caveat, facts hold.
- Verdict column: each verdict is one `cmp` rc over the committed pair (S138 DIFFER, S158 DIFFER, S149/S182 IDENTICAL, S185 IDENTICAL) — all reproduce.
- S158: exactly one hunk, comment-only at :1339 ("parameter"→"parameters"), anchor ranges 37-40/68-78/672-688 byte-identical (cmp -s rc 0 ×3).
- S999 red-before (C2): CORRECT. Header gate reads no registry (check-knowledge-header.py:56, :202 `RULES = {"source": None, …}`, :218-220 `if rule is None: continue`; zero SOURCES references). Empirical: sandbox shared clone + fixture `source: S999` → gate rc 0 PASS, 86 notes, 0 findings; base control 3f6edcc9 PASS 85/0.
- Note draft (step 6): NOTE=CHECKED. Every evidence-cell command re-run once over the pinned bytes; all reproduce (sha/cmp/wc/grep -cF/heading greps/diff -u counts/host.txt). One stale Limits bullet (BLOCKED wording superseded by the updated RW1 row citing S1Scout-verify.md) should be cleaned before landing.

KEYS: SHA_PAIRS_MATCH=8/8 A_FALSIFIERS=4 RW_BOILERPLATE_ACCEPTED=yes S999_CLAIM=CORRECT NOTE=CHECKED
