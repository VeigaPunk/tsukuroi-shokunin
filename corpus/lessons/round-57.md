# Round 57 — lesson (Windows host, base `a36bfaaf`; declaration `0555a010`, work `19f6b5c8`)

Shape: single-session inline round (no wave/AgentSwarm dispatch surface on this host; the L0
question `tsukuroi | round-53` stands unanswered and was routed around, never treated as answered;
the round-1 contested kaidoku/revenger scope question likewise stands). The r56 closure's one
routed carry-in landed FIRST as a plumbing repair, not a claim: the 14 round-56 receipt files
under `.ufo/waves/round-56/{after,receipts,services-probes}/` that the r56 report/SCORECARD/LOG
cited as committed but that only existed on disk (closure defect R56-RECEIPTS-UNCOMMITTED,
spot-check `b1ca23a0` §5.1) were landed as commit **`a36bfaaf`** (explicit file paths through the
plumbing helper — the helper silently no-ops directory paths; 14 files, 312 insertions) after
their contents were verified against every reported value (T1-T12 12/12 drift 0, D7 420 s rc-124
partial 18 PASS/0 FAIL, selftest 25/25, receipt-run 7/7, gates 94/94/0 + 72/0, census 42 W04 exit
0 both passes, sources 267 rows 0 malformed). The round's base IS that landing; the defect is
mined below as R57-CITED-UNCOMMITTED. Claims declared before any measurement (SCORECARD "Round 57
— declaration"): C1 depth (sourced SDDL/metadata plane), C2 operability (receipt-write +
`--raw-dir`), C3 freshness (dated recheck cadence). The FRESH-START ruled-out set (r50/r51/r52
re-spot-checked from committed bytes: r50 c1-final.json FAIL/verdicts_ok 0/marks_ok 0/seats_ok 18;
r51 `c2-cheats-at-amend1.json` absent at `c0ad548a` rc 128; r52 c1-final.json FAIL/verdicts_ok 1/
seats_ok 16, predicate binds == 18) is in the SCORECARD declaration.

## Gate

Source records for rows opened this round (CORPUS.md contract v1):

- **S268** — Microsoft Learn ARCHIVE, `Sc sdshow` (Windows Server 2012 R2 library),
  https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc742133(v=ws.11) .
  Opened 2026-11-01 by the L1 (HTTP fetch of the live page). Located quote (12 words, counted by
  `wc -w` before landing): "Displays a service's security descriptor, using the Security Descriptor
  Definition Language (SDDL)" — the page's function sentence, title heading. Supporting located
  text: the syntax line `sc [<ServerName>] sdshow <ServiceName>`, the Remarks SDDL pointer (a
  go.microsoft/fwlink redirect — dead-end, so the grammar grounding comes from S269), and the
  frontmatter identity (`is_archived: true`, `ms.date` 2016-08-31, archive `git_commit_id
  c0efbd18045caa47da59db9e0e986b2b22ff7204` — a DIFFERENT archive commit from S263/S264/S267's
  `5327995a…`). The current Windows Server commands reference carries NO sc-sdshow page: the URL
  `…/windows-commands/sc-sdshow` returned HTTP 404 on 2026-11-01 while `sc-query`/`sc-config`
  returned 200 in the same session (the S267 precedent, now twice). The tool's own usage text
  (receipt `t26-sdshow-usage-gate.txt`) matches the function sentence and adds an optional
  `<showrights>` argument the page omits (doc-vs-tool gap, the S266 `userown|usershare` class).
  Used by `corpus/knowledge/windows-services-sddl-plane-r57.md` — C1's sourced ground.
- **S269** — Microsoft Learn, `Security Descriptor String Format` (Win32 secauthz, current),
  https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptor-string-format .
  Opened 2026-11-01 by the L1 (HTTP fetch). Located quote (10 words, counted by `wc -w` before
  landing): "Unneeded components can be omitted from the security descriptor string" — body,
  after the components list. Supporting located text: the format block `O:owner_sid G:group_sid
  D:dacl_flags(string_ace1)...`, "To denote an empty ACL, the security descriptor string includes
  the D: or S: token with no additional string information", the worked example
  `"O:AOG:DAD:(A;;RPWPCCDCLCSWRCWDWOGA;;;S-1-0-0)"` (the ACE-field order used to read the T19
  string), and the frontmatter identity (`ms.date` 2025-07-08, `updated_at` 2025-07-10,
  `git_commit_id 804c358a9c4bce679f7de9c1ef714669cb168959`). Used by
  `corpus/knowledge/windows-services-sddl-plane-r57.md`.
- **S270** — Microsoft Learn, `Service Security and Access Rights` (Win32 services, current),
  https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights .
  Opened 2026-11-01 by the L1 (HTTP fetch). Located quote (23 words, counted by `wc -w` before
  landing): "Granting certain access rights to untrusted users (such as SERVICE_CHANGE_CONFIG or
  SERVICE_STOP) can allow them to interfere with the execution of your service" — closing
  paragraph of "Access Rights for a Service". Supporting located text: the nine specific rights
  with hex values (SERVICE_QUERY_CONFIG 0x0001 … SERVICE_USER_DEFINED_CONTROL 0x0100), the
  standard-rights table, the generic-rights mapping, and the DEFAULT service security-descriptor
  grants table (local authenticated users: READ_CONTROL SERVICE_ENUMERATE_DEPENDENTS
  SERVICE_INTERROGATE SERVICE_QUERY_CONFIG SERVICE_QUERY_STATUS SERVICE_USER_DEFINED_CONTROL;
  Administrators: DELETE READ_CONTROL SERVICE_ALL_ACCESS WRITE_DAC WRITE_OWNER) — the cross-check
  table for T19's measured DACL. The page documents NO SDDL letter table. Frontmatter: `ms.date`
  2018-05-31, `updated_at` 2025-03-11, `git_commit_id c4f4976e377740ff8bb51988e34aeec7f1634dfc`.
  Used by `corpus/knowledge/windows-services-sddl-plane-r57.md`.
- **S271** — Microsoft Learn, `ACE Strings` (Win32 secauthz, current),
  https://learn.microsoft.com/en-us/windows/win32/secauthz/ace-strings — **opened 2026-11-01 and
  REJECTED** as the service-rights anchor (kept as a row: a rejection is evidence of taste).
  Located grounding for the rejection: its rights tables cover ONLY generic (GA/GR/GW/GX),
  standard (RC/SD/WD/WO), directory-service (RP=ADS_RIGHT_DS_READ_PROP, CC=ADS_RIGHT_DS_CREATE_CHILD,
  LC, SW, LO, DT, CR), file (FA/FR/FW/FX), registry (KA/KR/KW/KX) and mandatory-label classes —
  NO service-object table exists on the page, and the directory-service letters collide
  letter-for-letter with service usage while naming DIFFERENT rights. Flip: a Microsoft-published
  table of the Sddl.h service-rights letter constants would make an opened page admissible as the
  mapping anchor. Frontmatter: `ms.date` 2023-02-21, `updated_at` 2025-03-12, `git_commit_id
  85aabcb32ecc444e04519aae583de223682188e9`. Referenced (as the named trap) by
  `corpus/knowledge/windows-services-sddl-plane-r57.md` Limits.

Leads that never became rows: a web-search-provided archive asset id (`cc742070`) was fetched
BEFORE the title was checked and returned "Wbadmin start recovery", not sdshow — re-located by
title-verified search to `cc742133` (S268); the wrong page was never cited. The current-reference
`sc-sdshow` URL's 404 is recorded inside S268's anchor, not as a rejection (nothing was opened —
the S267 precedent).

Header-line changes logged old→new (C3; the SOURCES in-place-change discipline applied to the
knowledge notes' `recheck:` headers — each note's operative line is its LAST `recheck:` line, the
journal-boot-plane convention the header gate implements):

- `windows-services-plane-r54.md` and `windows-services-plane-r55.md`: old `recheck: 30d — re-run
  the probe commands of rows T1-T8|T9-T12 …` (cadence-only) → an appended operative line
  `recheck: 30d from day 0 2026-11-01 (the r56 first executable pass, receipt
  .ufo/waves/round-56/receipts/recheck-services-t1t12.txt: rows=12 matched=12 drift=0; instrument
  tools/recheck-services-r56.sh [--receipt PATH] [--raw-dir DIR]) — next pass due 2026-11-30; a
  late pass is observable from this line (operative; appended r57, supersedes the cadence-only
  line above, which stays)`. Old lines byte-unchanged in place.
- `windows-services-config-plane-r56.md`: same append; the operative line additionally names
  T13-T16's receipt-compared re-check duty (the executable instrument covers T1-T12).
- `windows-services-sddl-plane-r57.md` (new note): born with the dated line (day 0 = 2026-11-01,
  due 2026-11-30).

Census: `bash <fleet-root>/scripts/sources-census.sh validate --root <fleet-root> tsukuroi` exit 0
at round start and round end (42 W04 warnings at BOTH passes — all duplicate-URL warning class, no
E-code either pass; the four new rows carry fresh URLs; receipts committed at the outcome commit:
`.ufo/waves/round-57/before/sources-census-start.txt` and the end receipt from scratch). Gates at
the work tip `19f6b5c8`: knowledge-header PASS **73 notes / 0 findings**; registry-coverage PASS
**95 tools / 95 rows / 0 findings** (`receipt-write-r57` registered, `recheck-services-r56` row
annotated); SCORECARD uniqueness ok rc 0; `RECEIPT_WRITE_SELFTEST: PASS (5 cases, 5 passed, 0
failed)`; `RECEIPT_RUN_SELFTEST: PASS (7 cases, 7 passed, 0 failed)` (unchanged).

Rejections this round: **1 — stated explicitly**: S271 (ACE Strings), opened-then-rejected with
reason and flip in the row itself (a rights-table name collision across object classes). One
further lead (the `cc742070` wrong-page fetch) never became a row (see above).

Assimilation: `considerthese/` mined (latest 2026-10-26; seven notes): the five self-improvement
ideas are aggregator/wave-class or Linux-host-class on this host, and the cross-note correction
propagation map was partially applied in r54 — none clears this round's bar; nothing adopted. The
shokuknow register is not reachable from this host. Assimilation: none — shokuknow unreachable.

## Mistakes

- **R57-CITED-UNCOMMITTED** (class: `landing` — evidence cited as committed was never plumbed;
  this is the r56 closure's routed defect R56-RECEIPTS-UNCOMMITTED, mined here per the closure's
  routing) — the r56 report, SCORECARD and LOG cited 14 receipt files under
  `.ufo/waves/round-56/{after,receipts,services-probes}/` "across all three commits" while the
  committed tree held only `before/` (2 files); the pointers resolved only on this host's disk.
  Evidence: `git ls-tree -r --name-only HEAD | grep round-56` at `ed26680d` (2 files) vs
  `find .ufo/waves/round-56 -type f` (16 files); spot-check `b1ca23a0` §5.1. Captured-by: the
  non-author closure's changed-file-set comparison (and, once known, the same tree-presence sweep
  this round ran before its own outcome commit). Fix: landed via the plumbing helper with 14
  EXPLICIT file paths (`a36bfaaf`; directory paths silently no-op) after verifying every reported
  value against the on-disk contents; the repeatable capture is
  `git ls-tree -r --name-only HEAD | grep "round-<N>"` vs `find .ufo/waves/round-<N> -type f`
  run BEFORE the outcome commit names any receipt as committed.
- **R57-SDSET-ASSUMED-ABSENCE** (class: a probe designed from the ASSUMED failure order of a tool
  — the same class as r56's R56-USAGE-GATE-ASSUMED-ABSENCE, recurring on a new surface) — the T24
  probe assumed `sc sdset <nonexistent> <sddl>` would fail at OpenService with the 1060/rc-36
  absence family; measured: it fails EARLIER, at the SCM — `[SC] OpenSCManager FAILED 5:` Access
  is denied, rc **5** (`t28-sdset-nonexistent-refused.txt`) — because sdset requests SCM write
  access and the read-only session's token is denied BEFORE any service name is resolved. The
  assumed 1060 refusal never fires here. Captured-by: the probe's own receipt (rc 5 with the
  OpenSCManager function line). Fix: the note records the BLOCKED class (privilege gate) instead
  of the assumed refusal, and the gates-now-come-first order is stated explicitly: usage
  validation → SCM access check (rc 5) → OpenService (rc 36); a probe design must name which gate
  it expects to fire and treat a different gate as a finding, not reinterpret it.
- **R57-SELFTEST-WRITTEN-THEN-PASSED** (class: a claimed checker that failed its own first run;
  the honest direction — caught BEFORE landing, not after) — receipt-write.py's first selftest
  run read `RECEIPT_WRITE_SELFTEST: FAIL (5 cases, 1 passed, 4 failed)`: the file was missing the
  shared `_check` helper (NameError × 4) and one case compared two unrelated constants (an
  always-false assertion) — two real defects in the round's own new instrument. Captured-by: the
  selftest's own FAIL lines in the shell transcript, before any commit. Fix: the helper defined
  once and the assertion rewritten to check the actual `stdout_bytes=<len>` line; re-run 5/5 rc 0
  — the registry row's "selftest PASS" claim is now about the FIXED tool, and the FAIL run stays
  reported here rather than being silently discarded.
- **R57-UGREP-XARGS-ARGS** (class: this host's grep is ugrep and an `xargs`-piped multi-file
  count mangled its arguments — the r55/r56 ugrep family, new shape) — the after-battery's
  `grep -l '^command=' raw-t1t12/*.txt | xargs grep -l '^rc='` printed `grep: …t<k>-raw.txt: No
  such file or directory` for all twelve EXISTING files and counted 0. Captured-by: the shell
  transcript (the failed line plus the twelve errors); the committed after-receipt carries the
  REPLACEMENT line naming the failure class — and names a second defect honestly: the failed line
  itself was deleted from the receipt by an in-place sed before staging, so the committed evidence
  is the correction note, not the failure. Fix: per-file loops for multi-file key checks on this
  host (`for f in …; do grep -q … && …; done` → 12/12); deleting a failure line from a receipt
  under commit is wrong — append the correction beside the preserved failure, never substitute.

Sweep that found no further mistakes this round: before the outcome commit the round's files were
re-read against the declared predicates — C1's receipt headers re-checked key by key (t19-t28 rc
values 0/36/0/103/0/0/0/103/0/5 against the note rows), the three Gate quotes re-counted with
`wc -w` (12/10/23), the SOURCES table re-run through the malformed-row awk (0) and the enum awk
(clean), C3's old `recheck:` lines diffed byte-identical against `19f6b5c8^`, C2's summary receipt
header re-read (rows=12 matched=12 drift=0), and the tree-to-tree sweep re-run in its r56
R56-STALE-DRAFT discipline — this round in its tree-to-tree form: the declaration set
(`diff-tree a36bfaaf..0555a010` = 3 files) and the work set (`diff-tree 0555a010..19f6b5c8` =
32 files) listed, then every on-disk copy of those 32 files plus the two r56-repaired tools
(`recheck-drift-r54.sh`, `win-host-census-r53.py`) byte-compared against its committed blob —
all clean. (The r56 full-tree worktree-vs-HEAD form was abandoned this round: two commits landed
while the sweep ran, so `HEAD:` kept re-resolving under it; the tree-to-tree form is the
repeatable replacement.) The four mistakes above are the complete defect set observed this round.
