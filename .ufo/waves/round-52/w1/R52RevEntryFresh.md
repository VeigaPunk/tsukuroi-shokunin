VERDICT: defect-found

# W-N9 — frozen entry freshness sweep

Axes: freshness, depth. Reviewed revision `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0`, as of 2026-10-30. All entry line references below mean `corpus/knowledge/btrfs-scrub-grounding-r45.md` at that revision (abbreviated E); registry references mean `corpus/SOURCES.md` at that same revision (S). Working-tree bytes were not evidence.

## Findings, ordered by severity

**Medium — carried-forward prose lacks a current, bounded freshness statement.** The header remains verified 2026-10-27 with an undated `on-release` trigger (E:2-3). The Arch patch premise explicitly carries `fs/` from round 43 and says `lib/` was not rechecked (E:340-341), while GR1 relies on this premise for the host reading (E:96-100). This is an acknowledged verification gap, not proof the patch claim is false or that a release occurred. No later reopening of that premise is cited in the entry.

**Low — historical gate/coverage prose can be mistaken for current coverage.** E:350 says “no seat has read that last narrowing”; E:385 says the corrected GR2 has been read by no counted seat; E:418 calls the next amendment unread; E:420-430 still describes the round-49 cohort as unsettled. These are historical round-specific statements, not current-row receipts: E:355-362 describes a subsequent round-51 rewrite and E:434-447 already records the round-50 outcome. Their headings supply historical context, so this is not evidence of a false round-52 admission. Likewise QUALITY 3's “two consequences” (E:393-394) is not a complete inventory of the eleven substantive inference occurrences below.

## Freshness fields

“Symbolic” means no calendar deadline, not automatically overdue. Age alone cannot establish violation of an on-release policy. Amendment baseline: read-only `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show -s --format=fuller 6abef5d0` returned full commit `6abef5d0edd19e0c6d21870b6add3b4c71c5ea68`, subject `round-51: AMENDMENT 1 (pre-w2)`, commit date 2026-10-28 18:30:03 -0300.

| Field | Value | Lapsed as of 2026-10-30? | Evidence |
|---|---|---|---|
| Entry verified-at | 2026-10-27; capture 2026-10-27T02:09:52Z | Older than amendment; expiry not defined | E:2 |
| Entry recheck | on-release; refetch/digest, rerun capture, lint at `<REV>` | Symbolic/undated; trigger occurrence unestablished | E:3 |
| GR1 verified-at / recheck | No row-local fields | Absent; only entry header applies | E:13-101 |
| GR2 verified-at / recheck | No row-local fields | Absent; only entry header applies | E:103-235 |
| GR3 verified-at / recheck | No row-local fields; dated supplemental host receipt in prose | Absent; only entry header applies | E:237-323 |
| S237 opened / recheck | 2026-10-26 / on-release | Symbolic; no calendar lapse established | S:246 |
| S240 opened / recheck | 2026-10-26 / on-release; reopened live 2026-10-28, byte-identical | Symbolic; dated reopening recorded | S:249 |
| S242 opened / recheck | 2026-10-26 / on-release | Symbolic; no calendar lapse established | S:251 |
| S243 opened / recheck | 2026-10-26 / on-release | Symbolic; no calendar lapse established | S:252 |
| S244 opened / recheck | 2026-10-26 / on-release | Symbolic; installed service digest compared 2026-10-28 | S:253; E:255-257,320-323 |
| S246 opened / recheck | 2026-10-27 / on-release | Symbolic; no calendar lapse established | S:255 |
| S247 opened / recheck | 2026-10-27 / on-release | Symbolic; no calendar lapse established | S:256 |
| S248 opened / recheck | 2026-10-27 / on-release | Symbolic; no calendar lapse established | S:257 |
| S249 opened / recheck | 2026-10-27 / 30d | No; 30-day anniversary 2026-11-26 | S:258 |
| Arch patch premise recheck | fs/ carried from round 43; lib/ not rechecked this round | Undated outstanding recheck; not a numeric cadence | E:340-341 |

Registry has `opened`, not `verified-at`, columns (S:5). No explicitly calendared recheck is demonstrably overdue in these fields.

## Every inference mark

The literal bracketed inference family appears **15 times**: eleven substantive occurrences and four contextual mentions. This includes `[inference: …]` and `[inference carried …]`, not only the exact token `[inference]`.

| Field / occurrence | Value | Lapsed? | Evidence |
|---|---|---|---|
| Intro, contextual | Round-44 statements had `[inference]` marks | Historical mention; not a new premise | E:8 |
| GR1 Statement | skip_spaces skips isspace characters, including echo newline | Unresolved/undated, not cadence-based | E:26-28 |
| GR1 Statement | sysfs write buffer NUL-terminated after newline | Unresolved/undated | E:30-32 |
| GR1 Statement | Throttle unit bytes per second; byte comparison outside declared range, unquoted | Unresolved/undated | E:33-34 |
| GR1 Host reading | Arch kernel carries upstream code unchanged | Carried premise, no newer reopening cited | E:98-99; E:340-341 |
| GR1 Host reading | Caller cannot write by ordinary mode checks; ACLs/LSMs unobserved | Unresolved/undated | E:99-100 |
| GR2 Statement | CLI printing of start/status returns not pinned | Unresolved/undated | E:137 |
| GR3 Statement | DefaultTimeoutStopSec reaches units without own override | Unresolved/undated | E:252-253 |
| GR3 Statement | Early SIGINT disposition inherited from systemd | Unresolved/undated | E:262-263 |
| GR3 Statement | Killed before final record write leaves last written record | Unresolved/undated | E:264-265 |
| Triage consequence | Stopped scrub may lack canceled mark | Unresolved/undated; repeats GR3 consequence | E:334-336 |
| Limits premise | Arch patch touches neither fs/ nor lib/ | fs/ carried from round 43; lib/ explicitly unrechecked | E:340-341 |
| QUALITY 3, contextual | Says inference marks two consequences | Historical/incomplete inventory, not a new premise | E:393-394 |
| QUALITY 9, contextual | Patch claim stays `[inference]` | Repeats Limits premise | E:404 |
| Round-46 gate, contextual | DefaultTimeoutStopSec reach marked `[inference]` | Historical mention | E:417 |

## Older dates and reopening receipts

This table exhausts the entry's explicit calendar-date occurrences. A frozen historical observation does not become false merely by aging. “No receipt cited” below is bounded to the inspected entry/registered source fields, not a repository-wide assertion that no artifact exists.

| Field / sentence | Value | Lapsed? / reopening disposition | Evidence |
|---|---|---|---|
| Header verification and capture | 2026-10-27; 2026-10-27T02:09:52Z | Before amendment; no entry-wide post-amendment reopening cited. The original capture is cited, not a fresh observation | E:1-2 |
| GR3 package/version/unit digest sentence | “on 2026-10-28” | Dated receipt cited; not a missing-receipt case. Same-day ordering versus amendment is unspecified | E:255-257; E:320-323 |
| GR3 Host reading receipt sentence | “L1's read-only receipt of 2026-10-28” | Explicit reopening receipt `.ufo/waves/round-51/host/host-btrfs-progs.txt`; scope package/version/SendSIGHUP/digest only | E:320-323 |
| QUALITY 9 package-ownership negative | Capture sweep on 2026-10-27 | Before amendment, but explicitly cites a re-run via `a2w1/C2ExecHostRecheck.md` §4 with pacman -Qo; re-run date not stated here. Not a receipt-free sentence | E:400-404 |

Additional old provenance without a calendar date: GR2's sysfs values `none` and `0` rely on the round-45 `C2ExecHostRecheck.md` §3 (E:231-234); that is a receipt, but no new observation date is supplied. The round-43 fs/ patch premise and unrechecked lib/ premise have no newer reopening cited (E:340-341). Gate sections refer to rounds 45, 46, 49, 50, not calendar dates, and remain historical evidence rather than round-52 receipts (E:376-385,408-447).

## Residual risk and verification gaps

Read-only evidence commands were `git show` of the entry and registry at the freeze, and `git show -s` of amendment metadata; text inspection used read/grep on their returned artifacts. No census, selftest, counter, lint, host capture, external fetch, fixture, runtime, or mutation was executed. No scratch was created, so none needed removal. No tool was installed. The mounted device inventory exposed no LSP device; this Markdown review makes no semantic caller/definition claim.

Release-trigger satisfaction, present host values, actual receipt contents, and patch comparison remain unverified in this NO-EXEC seat. Recommendations are to bound the old gate prose explicitly as historical, reconcile QUALITY 3 with the current inference inventory, and supply a dated reopening of the Arch patch premise if current-host applicability is claimed. No entry edit or admission judgment was made.

Self-evaluation: accuracy 4 (receipt existence beyond cited paths not independently inspected); completeness 4 (all explicit entry dates and bracketed inference occurrences enumerated, external receipt contents outside scope); clarity 4 (symbolic versus expired distinguished, tables necessarily lengthy); actionability 4 (three bounded prose/provenance corrections, no proposed patch requested); conciseness 4 (full inventory retained to satisfy the sweep). Overall 4.0. Highest-impact improvement: inspect the cited reopening artifacts in an authorized follow-on review; do not replace this evidence gap with a claimed fresh host check. User-agreement self-check: scope and unexecuted checks are explicit.
