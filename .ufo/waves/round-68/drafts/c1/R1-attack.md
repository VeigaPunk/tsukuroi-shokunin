2026-11-03T22:31:37Z (seat start; all commands below run 22:31-22:47Z)
Seat: R1Reviewer (L2, round 68 w1, lane base 42400ec6, declaration commit 3f6edcc9). Item: attack the C1 predicates and facts. Independent attacker; no fixes proposed.

A1 - The frozen SHA-256 pairs vs the pinned bytes: SURVIVES
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-68/before/src && sha256sum ./*
11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692  ./v72-Documentation_accounting_psi.rst
a9433bb0e16a67f07a93424c7bf842f47616e9b0a27b51e17d7b34cff246b7ad  ./v72-Documentation_admin-guide_cgroup-v2.rst
ce146120f29ac29c0bc1859f21e4b84da91a536df2ec9fd2fa5649144f731c43  ./v72-fs_btrfs_sysfs.c
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  ./v72-mm_oom_kill.c
11c6b7129103b4547c31895cb1cfc0ff75b741c95a24bfcaeb01dece37b82692  ./v73-Documentation_accounting_psi.rst
2750c11a6324e18f4d3a9bb63032b55f3268bd7077b80897af2f15a712611b68  ./v73-Documentation_admin-guide_cgroup-v2.rst
098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377  ./v73-fs_btrfs_sysfs.c
452f1348e79c252ee89215d55fb104591412bbcea4a3ee965e873a401f756b4e  ./v73-mm_oom_kill.c   (rc 0)
All 8 lines are byte-for-byte equal to SHA256SUMS (8/8 MATCH), and to the declaration's frozen values (SCORECARD.md:5107-5110).

A1b - The same bytes are the committed bytes (not just worktree files):
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file blob 3f6edcc9:.ufo/waves/round-68/before/src/v73-fs_btrfs_sysfs.c | sha256sum
098cb522131501deabde61ffcdc56138a8516098f4e980f9c34cb9e62b467377 ... (all 8 committed blobs hash to the same 8 values; rc 0). The 10 files were added by commit 3f6edcc9 (git show --stat), so the pins are committed evidence, not worktree-only.

A2 - Upstream freshness of the pins: SURVIVES (bytes real), with one channel caveat
$ curl -fsS --max-time 60 "https://raw.githubusercontent.com/torvalds/linux/<tag>/<path>"   (all 8 FETCH.txt URLs)
curl: (22) The requested URL returned error: 404  (rc 22, all 8) - the FETCH.txt URL channel does not reproduce from this seat today.
Control: $ curl -fsS -o master-README https://raw.githubusercontent.com/torvalds/linux/master/README -> rc 0, 6034 bytes (raw CDN works for master).
$ curl -fsS "https://api.github.com/repos/torvalds/linux/tags?per_page=15" -> v7.4-rc1, v7.3, ..., v7.2 (tags exist, rc 0).
$ curl -fsS "https://api.github.com/repos/torvalds/linux/contents/<path>?ref=<tag>" | python3 -c 'decode base64, sha256'  (8 requests, all rc 0)
a9433bb0... 133236 cgroup-v2.rst (v7.2) / 2750c11a... 135851 (v7.3); 452f1348... 34311 twice (oom_kill.c);
ce146120... 72925 sysfs.c (v7.2) / 098cb522... 72926 (v7.3); 11c6b712... 6792 twice (psi.rst).
All 8 live-upstream hashes+sizes equal the pins. The pins are not fabricated; only the raw.githubusercontent.com channel 404s from here (environmental; recorded, not remediated).

A3 - Verdict column derivable from a single command over committed bytes: SURVIVES
$ cmp <(git -C $L cat-file blob 3f6edcc9:$R/v72-F) <(git -C $L cat-file blob 3f6edcc9:$R/v73-F)
Documentation_admin-guide_cgroup-v2.rst: DIFFER rc=1  -> S138 CHANGED reproduces
fs_btrfs_sysfs.c:                        DIFFER rc=1  -> S158 CHANGED reproduces
mm_oom_kill.c:                           IDENTICAL rc=0 -> S149 and S182 UNCHANGED reproduce (one command covers both rows: same file, same bytes)
Documentation_accounting_psi.rst:        IDENTICAL rc=0 -> S185 UNCHANGED reproduces
Every declared verdict is the rc of one cmp over the committed pair. S182's "same bytes as S149" is literal: both registry rows cite sha 452f1348 (SOURCES.md:155,188).

A4 - Predicate attack: 'grep -cE RW rows >= 6' accepts boilerplate: FALSIFIED
Declared counting command (SCORECARD.md:5119, counting-command column): git show <rev>:corpus/knowledge/linux-v73-pinwatch-r68.md | grep -cE '^\| RW[0-9]+ \| ' >= 6. Declared strictness (SCORECARD.md, Counter strictness paragraph): "distinct ids, a non-empty evidence cell, no fenced-block or prose row".
Fixture (boilerplate-only; copied generic text, no located anchor, no command in any evidence cell):
| RW1 | S138 | changed | v7.3 bytes differ from v7.2 bytes per SHA256SUMS |
| RW2 | S158 | changed | v7.3 bytes differ from v7.2 bytes per SHA256SUMS |
| RW3 | S149 | unchanged | v7.3 bytes identical to v7.2 bytes per SHA256SUMS |
| RW4 | S182 | unchanged | same bytes as S149 per SHA256SUMS |
| RW5 | S185 | unchanged | v7.3 bytes identical to v7.2 bytes per SHA256SUMS |
| RW6 | host | open | installed kernel stays 7.2.11 per uname -r |
$ grep -cE '^\| RW[0-9]+ \| ' boilerplate-note.md -> 6 (rc 0). ACCEPTS.
Duplicate-id variant (six identical '| RW1 |' rows): grep -cE -> 6 (rc 0). The declared command cannot see id distinctness at all; it counts matching lines. No declared command (cat-file -e; the grep; the SOURCES grep; sources-census validate) implements "non-empty evidence" beyond text presence or id distinctness. Only the prose kill rule ("any do-nothing control reaches the after-state") could catch this, and no command executes it. Verdict: the declared predicate ACCEPTS a boilerplate-only six-row fixture. This is a falsifier for the predicate, not a fix.

A5 - Declaration anchor-drift fact 'oom_kill 1507 -> 1533': FALSIFIED (off-by-one)
$ diff <(sed -n '1507p' v72-Documentation_admin-guide_cgroup-v2.rst) <(sed -n '1533p' v73-Documentation_admin-guide_cgroup-v2.rst)
1c1 < 		The number of processes belonging to this cgroup  ---  > 	  oom_kill   (NOT byte-identical)
$ diff <(sed -n '1507p' v72-...) <(sed -n '1534p' v73-...) -> IDENTICAL; $ diff <(sed -n '1506p' v72-...) <(sed -n '1533p' v73-...) -> IDENTICAL.
The v7.2 oom_kill label sits at line 1506 (description 1507-1508); the v7.3 label sits at 1533 (description 1534-1535). SCORECARD.md:5112 writes "oom_kill 1507 -> 1533": that pair mixes a v7.2 description line with the v7.3 label line and does not reproduce byte-identity. Correct pairs: 1506 -> 1533 (label, exactly what grep -n 'oom_kill$' prints) or 1507 -> 1534. The other two declared pairs reproduce: 1468==1495 (memory.events) and 1517==1544 (memory.events.local), both rc 0 IDENTICAL. The note draft avoids the error (sentence anchors 1474->1501, 1508->1535, 1518->1545, all verified IDENTICAL; heading cells 1468/1506/1517 -> 1495/1533/1544 reproduce exactly).

A6 - Declaration RW1 sub-claim 'the changed hunks ... outside the memory-controller section': FALSIFIED
Memory controller section in cgroup-v2.rst v7.2: heading 'Memory' at line 1267, next heading 'IO' at 1982 (awk heading scan).
$ diff v72-Documentation_admin-guide_cgroup-v2.rst v73-Documentation_admin-guide_cgroup-v2.rst | grep -E '^[0-9]'  (17 change groups; 16 unified hunks: $ diff -u ... | grep -c '^@@' -> 16)
1912c1939 sits inside 1267-1981: $ sed -n '1912p' v72-... -> '	A read-only nested-keyed file.' ; $ sed -n '1939p' v73-... -> '	A read-write nested-keyed file.'
That is the memory.pressure access-mode line (read-only -> read-write), a semantic change INSIDE the memory-controller section, in a file area the pinned rows document. The declaration text (SCORECARD.md:5119) asserting the hunks are outside the section is false; the note draft itself reports the true map 'CPU 6, Memory 1, IO 3, Cpuset 1, RDMA 3, DMEM 1, Misc 1' and '1 sits inside it'. I re-derived the map myself: 6/1/3/1/3/1/1 over v72 ranges CPU 1094-1266, Memory 1267-1981, IO 1982-2403, Cpuset 2464-2749, RDMA 2774-2865, DMEM 2866-2908, Misc 2942-3032. Total 16 = the note's count.

A7 - Declaration fact 'The five v7.2-pinned registry rows': FALSIFIED as a definite description
$ grep -cE 'a9433bb0...|452f1348...|ce146120...|11c6b712...' corpus/SOURCES.md -> 11
Eleven rows pin v7.2-family bytes of exactly these four files: S115 (:121), S118 (:124), S119 (:125), S133 (:139), S138 (:144), S149 (:155), S158 (:164, 'Same URL and bytes as S133', ce146120 present on the row), S178 (:184, rejected), S182 (:188), S185 (:191, rejected), S243 (:252, stable v7.2.11, ce146120). QUALITY.md:192 scopes the watch to 'a SOURCES.md row whose recheck: is on-release ... names the upstream tag it pins' - not to a named five. Six of the eleven (S115, S118, S119, S133, S178, S243) get no RW verdict row. Substance is intact: all four files were re-read, so every one of the eleven rows' bytes was re-read and their verdicts are derivable from the same pairs (A3); but the declaration sentence counts the trigger surface as five. RW6's host applicability also does not cover S243's stable-series trigger (a newer stable 7.2.x would change those bytes while tag v7.2 bytes stay frozen); re-checking the stable series needs kernel.org, which is outside this seat's allowed fetch sources - BLOCKED, not run.

A8 - C2's S999 red-before claim ('source: S999 passes the header gate'): CORRECT
tools/check-knowledge-header.py never reads the registry. Exact lines: :56 KEYS = ("source", "verified-at", "recheck"); :202 RULES = {"source": None, "verified-at": date_problem, "recheck": cadence_problem}; :218-220 in evaluate(): rule = RULES[key]; if rule is None: continue. grep for 'SOURCES' in the tool: 0 hits. The only file the gate reads is corpus/knowledge/*.md at the bound revision (notes_at, :131-146).
Empirical (sandbox shared clone under my scratch; git writes only there):
$ git clone --shared <lane> $S/sb; fixture corpus/knowledge/zz-s999-fixture.md with 'source: S999'; commit 2b7e053; update-ref refs/remotes/origin/master HEAD (bind requires E-REVISION-NOT-PUSHED clearance, _revision.py:186-190)
$ python3 tools/check-knowledge-header.py --revision 2b7e053... --lane $S/sb -> rc 0, status PASS, 86 notes, 0 findings, fixture note {source: 3, verified-at: 4, recheck: 5} problems []
Control at the lane: --revision 3f6edcc9 -> rc 0, PASS, 85 notes, 0 findings.
So the claim is CORRECT and the proving line is :202 (source has no value rule) with :219-220 (None -> continue).

A9 - Note draft evidence cells (step 6; note appeared at 19:36Z): CHECKED - every named command re-run once over the pinned bytes, all reproduce
RW1: sha256sum pair prints a9433bb0/2750c11a rc 0; diff -u | grep -c '^@@' -> 16 rc 0; sentence greps: v72=1/v73=1 for the sentences at 1474, 1508, 1518; heading greps: '^  memory.events' -> 1468,1517 (v72) / 1495,1544 (v73); 'oom_kill$' -> 1506 (v72) / 1533 (v73); sed 1912p 'A read-only nested-keyed file.' vs 1939p 'A read-write nested-keyed file.' - all as the cell states.
RW2: sha pair ce146120/098cb522 rc 0; diff -u hunk count 1; 1339c1339 comment-only ('parameter' -> 'parameters'); cmp -s of ranges 37,40 / 68,78 / 672,688 -> rc 0 three times.
RW3/RW4: sha256sum prints 452f1348 twice rc 0; cmp -s rc 0; wc -l 1257/1257.
RW5: sha 11c6b712 twice; cmp -s rc 0; 188/188 lines; grep -n '^| S185 ' corpus/SOURCES.md -> 191; awk -F'|' NR==191 field 9 = ' rejected '.
RW6: sed -n '2,3p' before/host.txt -> '7.2.11-arch1-1' / 'linux 7.2.11.arch1-1'; host.txt:6 'pacman -Qu rc=1'.
One internal inconsistency: the Limits bullet still says the controller attribution is BLOCKED ('S1Scout-verify.md did not exist at draft time, ls rc 2 at 2026-11-03T22:35:44Z') while the RW1 fact cell now cites that receipt's attribution. The stale bullet should be dropped or rewritten before landing; the evidence cells themselves all reproduce.

Residual risk / verification gaps
- The FETCH.txt raw.githubusercontent.com channel 404s from this seat (A2): the declared reproduction path for the pins does not currently reproduce; verification had to go through api.github.com contents. Whether this is egress filtering or CDN state was not determined.
- S243's stable-series (v7.2.11) trigger was not re-checked (kernel.org outside allowed sources): BLOCKED.
- The C2 gate tools/check-knowledge-refs-r68.py is not present at HEAD or in the worktree (expected mid-wave; L1 lands it). Its declared red-before depends only on A8, which was verified.
- A4 shows the declared counting command cannot fail on boilerplate; the R67-COUNTER-SHAPE-ONLY battery under probes/ was not present when I looked (probes/ dir empty at 22:31Z) and is the L1's to land.
