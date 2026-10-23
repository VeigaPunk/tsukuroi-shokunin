# RevC2Pointers — re-open every pointer in coredump-count-unit-r34.md @ 879daa95

Verdict: every lane file:line pointer, capture.txt line range, saved-snapshot line number and mori `f2d28711` pointer in the committed note resolves. Four minor defects: one off-by-one finding citation, one capture range that stops three lines before the cited "answer" content, one corefile-field range that shows 'n'-prefix evidence rather than the literal `none`, and one "not a registered row" claim that L1's uncommitted working tree is already correcting via new row S189. No wrong pointer found.

## 1. Lane file:line pointers — all resolve [obs]

- `tools/tsukuroi-census.sh:1403-1410` (assignment says 1398-1410; the note says 1403-1410): `:1403` opens `cls_n=$(printf '%s\n' "$CAP_OUT" | awk '`, `:1404` is `/"SYSLOG_IDENTIFIER":"systemd-coredump"/ { c++; next }`, `:1409` builds `cls="coredump=$cd_n kernel=$kd_n other=$ot_n"`, `:1410` is `JRN_COREDUMPS=$cd_n`. Resolves.
- `tools/tsukuroi-census.sh:2780-2782`: `if [ "$JRN_COREDUMPS" -ge 1 ]; then printf 'HANDOFF ADJ-04 mori class=coredumps value=%s kind=dated-event state=prepared scope=boot0-merged selector=SYSLOG_IDENTIFIER\n' "$JRN_COREDUMPS"`. Same variable, printed twice — resolves.
- `tools/tsukuroi-census.sh:263-267` for "storm signal": `:266-267` reads `` `--json` would add a jq dependency; the `systemd-coredump` entry class IS the / storm signal. `` — resolves (quote lands on 266-267, inside the cited range).
- `SKILL.md:541`: `err=260 (coredump=220 kernel=38 other=2) failedhist=0 timer_drift=0` — snapshot only…`; `SKILL.md:884`: `PLANE journal: DEGRADED (boots=13 current=yes … err=442 (coredump=279 kernel=139 other=24); …`; `SKILL.md:1214`: `… err=797 (coredump=522 kernel=139 other=136); …`. All three present `coredump=N` bare as a coredump count; resolves. [inf] The claim that readers take N as "a number of coredumps" is itself ratified by the appended rule at `SKILL.md:2874-2882`: "Snapshot lines above that read `coredump=N` as N coredumps are read this way."
- `PROVINCE.md:125`: `| OUT-005 | ADJ-04 | `mori-shokunin/PROVINCE.md` @ `91940fa339e3` | … | kill/OOM-related catalog-ID records and signal-11 coredump records | Mori owns kill/OOM catalog-ID and signal-11 coredump classification from separately labeled user/system journals; … |` — resolves verbatim.
- Secondary pointer inside the cited census comment: `systemd-user-plane.md:169` — `corpus/knowledge/systemd-user-plane.md:168-169` is the coredumpctl item ("coredumpctl list table parsing misleads … `-F exe` returned empty … `--json=short` + jq worked"); :169 is inside it. Resolves.

## 2. capture.txt line ranges — resolve, two of four slightly imprecise [obs]

- `:34-67` (round 1): `:34` `arm cls text: coredump=1621 kernel=155 other=1`, `:35` `JRN_COREDUMPS …=1621`, `:36` the would-print HANDOFF line with `value=1621`, `:39-40` jq equality 1621, `:52-57` kind totals `dumped-core=183 / json-null=69 / no-coredump-abnormal=1365 / other=4 / sum=1621`, `:58-67` PRIORITY and MESSAGE_ID splits (`fc2e22bc6ee647b6b90729ab34a250b1` x1617, absent x4). Resolves.
- `:129-162` (round 2): same block for 1635 (`coredump=1635`, kinds 183/69/1379/4, MESSAGE_ID x1631). Resolves.
- `:181-185` (corefile field): `:181` `corefile field: type=string first_char_classes=[{"c":"n","n":1631}]`, `:182` `corefile lengths: min=4 max=4 distinct=1`, `:185` `existing files behind corefile values=0 of 1631`. The literal token `"none"` is stated at `:258` and `:273-275`, not inside the cited range — the range proves a 4-char 'n'-prefixed single distinct value, which only equals "none" together with the later lines. Resolves with a citation-precision caveat (minor).
- `:246-266` (drift table and answer): `:246-258` is the drift table (`coredump= +14`, `dumped core 0`, `no-coredump +14`, `coredumpctl window 1617/1631`, `corefile == "none" 1617/1631`); `:262-266` begins the equality checks. The handler-error explanation (`:267-269`) and the plain "What one counted entry is" answer (`:290-297`) and §E (`:334-345`) sit outside the range — the cited "answer" content runs past the pointer. Resolves with a range-shortfall caveat (minor).
- Round-1 coredumpctl `1617` provenance: the `@epoch` window run at 08:45:32Z is described in `ExecCoredumpReconcile.md:85-87`, not in capture.txt's round-1 section (which shows the failed `-b` argv at `:73-79` and the `--since` wall-clock 1616 at `:95-97`). Consistent, documented elsewhere in the same seat (minor).

## 3. Saved-snapshot line numbers — all resolve [obs]

Snapshot directory `.ufo/waves/round-34/w1/SrcCoredumpCode/` digests re-hashed 2026-10-23 match both capture.txt §D and the S186/S177 rows:

- `coredump-submit.c` sha256 `54ce12400ce7e7c5ec4f8a6acdeac58659780434ed964f9c941f82ec11d0e538` — matches. `:709-711` is exactly `asprintf(&core_message, "Process "PID_FMT" (%s) of user "UID_FMT" %s", …, written ? "dumped core." : "terminated abnormally without generating a coredump.")`; `written` is set at `:646-649` (`written = save_external_coredump(…) >= 0;`, inside the cited 645-650). Removal without resetting `written`: `maybe_remove_external_coredump` body `:452-467` (unlinks at `:464-465`) called at `:655-659` with `filename = mfree(filename)` at `:663` — inside the cited 652-668. Failure branches: `context->rlimit < page_size()` at `:265` and both-limits-zero `process_limit == 0` at `:274-277` (cited 265-277); copy failure `log_error_errno(r, "Cannot store coredump…"` at `:350-353` (cited 350-354). Resolves.
- `coredump-context.c:360-361`: `iovw_put_string_field(&context->iovw, "PRIORITY=", STRINGIFY(LOG_CRIT))` and `"MESSAGE_ID=", SD_MESSAGE_COREDUMP_STR`. Resolves.
- `sd-messages.h:41-42`: `SD_MESSAGE_COREDUMP(_STR)` = `fc,2e,22,bc,6e,e6,47,b6,b9,07,29,ab,34,a2,50,b1` → `fc2e22bc6ee647b6b90729ab34a250b1`. Resolves.
- `coredump.conf.xml:78-80` (w1/SrcCoredumpConf/): "the core dumps may be logged (including the backtrace if possible), but not stored permanently" — verbatim at `:78-79`. Resolves. S187 row cites lines 77-93 — consistent.
- `journalctl.xml:591-593` (w1/SrcJournalctlJson/): "Fields larger than 4096 bytes are encoded as `null` values. (This may be turned off by passing `--all`…" — verbatim at `:591-593`. Resolves. S188 row cites 585-603 — consistent.
- `.ufo/waves/round-34/l1/src/coredump-receive.c:100`: `return log_error_errno(r, "Failed to initialize pidref: %m");` — resolves (`log_error_errno` = LOG_ERR = priority 3; capture.txt:269 records CODE_LINE=100, ERRNO present). File sha256 `48caa3734626c2e44a03caf29234c7e712b2bb16a7d1dd3eec57d0e58bdc1f64` matches capture.txt:217.
- Corroborating implementation for the S188 rule (not cited by the note; checked as saved): `l1/src/logs-show.c:43` `#define JSON_THRESHOLD 4096U`, `:1124` the `!(flags & OUTPUT_SHOW_ALL) && strlen(name)+1+size >= JSON_THRESHOLD` → null branch, `:1219` `sd_journal_set_data_threshold(j, … JSON_THRESHOLD)`. Matches capture.txt:279-282 exactly; sha256 `abc2fc1f…` matches capture.txt:218.
- `systemd-coredump.xml` sha256 `56bed6ed1e1ef3b6b2dc8990455548b152521cef0f4c524d9255f7ccf930bd3f` == S177 row digest — "re-opened … digest unchanged" resolves; also recorded in `SrcCoredumpCode.md` finding 1 (13-22).
- `JOURNAL_EXPORT_FORMATS.md` (S188 companion, saved): `:143-149` states non-UTF8 → byte array and oversized-field `_null_` — consistent with the 69-byte-array/null mechanism.

## 4. Mori pointers at `f2d28711` — resolve; still true at mori HEAD [obs]

- Commit `f2d28711ee723c969b6c2008d32df498192f9e7b` exists in `/home/vgpnk/Projects/shokunin/mori-shokunin` (round-35 freeze commit, 2026-10-23 05:34:43 -0300).
- `PROVINCE.md:8-9` at that commit: "kill/OOM-related catalog-ID records and signal-11 coredump records from independently labeled user/system journals" — resolves verbatim for "signal-11 coredump classification".
- `PROVINCE.md:24` at that commit: "**Kill/OOM classes** — structured, MESSAGE-free journal records carrying catalog IDs for kernel-OOM unit notices, oomd notices, coredumps, unit-process SIGKILL results and unit failures, plus a distinct numeric signal-11 coredump count…" — resolves for "declares its own scoped catalog-ID record counts".
- `SKILL.md:31` at that commit (`## Error patterns` row `journal class counts`): "count records carrying catalog `MESSAGE_ID` (`fe6faa94…` kernel-OOM unit notice, `d989611b…` oomd notice, `fc2e22bc…` coredump, …)". Resolves.
- Drift check: at mori HEAD `cedb0ec4f3a4f672804deac388b7191258f01fcd` (2026-10-23 06:06:42 -0300) the same three passages are unchanged at the same line numbers — no drift.
- "No intake contract for `class=coredumps`": the note cites "CritC2Absorb finding 4"; the bounded negative search producing that proposition is **finding 5** of `CritC2Absorb.md` (evidence `CritC2Absorb/read-only-git-receipts.txt:11`: "no match for HANDOFF, class=coredumps or intake" in the two pinned show outputs). Finding 4 covers only the declared-counts half. Off-by-one citation — minor; the proposition itself resolves via finding 5 and `PROVINCE.md:193` ("mori declares no intake format for it").

## 5. "Not a registered row" — true at the pinned commit, being repaired in flight [obs]

- At `879daa95`, `corpus/SOURCES.md` ends at S188; `git show 879daa95:corpus/SOURCES.md` contains no S189/S190. The note's parenthetical "(`ExecCoredumpReconcile`, v262 `coredump-receive.c:100`, read in that seat; not a registered row)" was accurate at the landed commit — resolves.
- Working tree now (2026-10-23, uncommitted): L1 has added S189 registering exactly `coredump-receive.c` line 100 (snapshot `.ufo/waves/round-34/l1/src/coredump-receive.c`, digest `48caa373…`) and a REJECTED S190 for `logs-show.c`, and is simultaneously editing the note's bullet to "(S189, `coredump-receive.c:100`)". So the claim is stale only in the in-flight edit pair, which corrects it atomically — flag, not defect, provided both land together.
- Note header timestamp "08:44Z and 08:49Z": round-2 capture is 08:48:49Z (capture.txt:112,126); the 08:50:22Z run is the `-a` supplement. Truncated rounding — cosmetic.

## 6. Cross-referenced seat reports — resolve [obs]

- `SrcCoredumpConf.md` finding 5 (`:11-…`): `systemd-analyze cat-config systemd/coredump.conf` drop-ins `/etc/systemd/coredump.conf.d/storage.conf` `Storage=none`, `limit.conf` `MaxUse=512M KeepFree=8G`, `#ProcessSizeMax=32G` commented — resolves for the effective-config paragraph.
- `SrcJournalctlJson.md` finding 3 (`:11`): default JSON `69 null / 4538 string`, `--all` `4607 string / 0 null`, and the >4096-byte recount of 69 — resolves for the note's second [unk].
- `ScoutCoredumpReaders.md`: exists, lists its commands in §2, restates `coredump=` at the same census lines — resolves for the QUALITY-9 negative claim.
- `ExecCoredumpReconcile.md`: findings 5-6 corroborate the 4-entry delta (1621-1617 = handler errors) and one-record-per-crash keys; consistent.

Scope: read=`corpus/knowledge/coredump-count-unit-r34.md` @879daa95, census.sh :263-267/:1398-1410/:2780-2782, SKILL.md :536-544/:880-888/:1210-1218/:2870-2882, PROVINCE.md :118-130/:141/:193, capture.txt (all 345 lines), all six SrcCoredumpCode snapshots + SrcCoredumpConf + SrcJournalctlJson + l1/src files with sha256 re-verification, SOURCES.md HEAD-vs-worktree diff, the four cited w1 seat reports, mori-shokunin @f2d28711 and @cedb0ec4 (read-only git show/log only); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/RevC2Pointers.md; executed=git rev-parse/status/log/show/diff/ls-files/cat-file/ls-tree (read-only), awk/sed/grep reads, sha256sum, wc, mkdir on seat dir
Model: devin/swe-2
Installs: none
