# ConnSiblingPatterns — sibling-overlap and shortcut-pattern scan (round 33, a3w1)

Scope: read-only. Lane: tsukuroi-shokunin @ 9c89ff4f. No lane files edited.

## Verdict
Scan complete: 8 sibling lanes carry child-environment allow-list/env builders (kaidoku, kotodama, mori, tameshi plus four tsukuroi-internal probes); 13 sibling verifier spot-check lessons name shortcut shapes, of which the shapes listed in §A.2 are not covered by this wave's C1 control set (C02–C17). For C2, mori at 24603186 declares kill/OOM/PSI/memory-pressure scope in `PROVINCE.md` and `SKILL.md` but declares no intake format for an ADJ-04 tsukuroi handoff (state remains `prepared`).

## A. Sibling child-environment builders and env probes

Builders found (top-level tools only; `.ufo/` and worktrees excluded):

- `kaidoku-shokunin/tools/round-25/ruler.py:25` `clean_environment()` — `{k:v for k,v in os.environ.items() if not k.startswith('GIT_')}` (ambient minus GIT_*, i.e. the round-32 defect shape).
- `kaidoku-shokunin/tools/round-32/c1-arm64x-positive.py:90` `clean_env()` — ambient minus only `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` (leaves other GIT_*).
- `kotodama-shokunin/tools/check-claim-separability.py:110` `_clean_env()` — `dict(os.environ)` (full ambient copy).
- `kotodama-shokunin/tools/check-judged-object.py:97` `_clean_env()` — `dict(os.environ)` (full ambient copy).
- `mori-shokunin/tools/mori-round19-regressions.py:103` `clean_env(home,tmpdir)` — allow-list builder (PATH from ambient, HOME/TMPDIR from args); `:177` `tool_environment()` wraps it.
- `tameshi-shokunin/tools/bash-witness-study.py:333` `git_clean_env()` — ambient minus GIT_* plus extra removals (THE_JANITOR_BIN, SQLITE3_BIN, CENSUS_BREAK, …).
- `tameshi-shokunin/tools/receipt-measure.py:47` `clean_env()` — `os.environ.copy()` (full ambient copy).
- `tameshi-shokunin/tools/round21-measure.py:26` `clean_env()` — ambient minus `GIT_*`.

Env probes present in tsukuroi itself: `tools/probe-child-env-allowlist-r32.py`, `tools/probe-child-env-allowlist-r33.py` (frozen at 9c89ff4f). No other sibling lane has a dedicated child-env allowlist probe; the builders above are the only cross-lane analogues.

## A.2 Shortcut shapes named in sibling verifier spot-check lessons not covered by C1's control set

C1 control set (this wave) covers: C02 JunkBytes, C03 LabelOnlyAllowlist, C04 DenyInjectFixed, C05 DenyValueNames, C06 HostSnapshotNames, C07 ArgvKeyed, C08 ScratchLocationKeyed, C09 BashEnvKeyed, C10 TracerPlain, C11 InheritNoEnv, C12 SkipWorkSelftest, C13 PathOnlyContentFree, C14 PostDataDeny, C15 HalfFix, C16 PositiveAllowlist, C17 ValueKeyedFilter. (X01/X02 not present in the wave directory at scan time.)

Shortcut shapes named in sibling lessons that are NOT among the above:

- kaidoku `corpus/lessons/round-31-verifier-spotcheck.md`: do-nothing, junk-row, all-false, no-reader, id-rotated, copied-predictions, Core-placement shortcut (real envelopes).
- kotodama `corpus/lessons/round-56-verifier-spotcheck.md`: sidcheat / S-id cheat, path- and line-keyed shortcuts, double decoding, stop-at-first-bad-file, CLI class-label rename. Round-57: `hexonly` (bare-hex arm deleted). Round-59: label-keyed (ids/labels) (never scored, held on cyber_policy).
- mori `corpus/lessons/round-31-verifier-spotcheck.md`: shortcut1, shortcut2, answer-key oracle, junk table, HTML-commented duplicate rows / renumbered ids.
- tameshi `corpus/lessons/round-29-verifier-spotcheck.md`: forged reports plus registry members (syntactic binding check).
- kake `corpus/lessons/round-36/37/38-verifier-spotcheck.md`: cheapest-wrapper shortcut, label shortcut, stdlib shortcut, base wrapper, label-shortcut delegate_ceiling, CriticPredicate rulepatch / rulepatch_pct.
- kumitate `corpus/lessons/round-44-verifier-spotcheck.md`: label shortcut (L1 analysis).
- kotoba `corpus/lessons/round-55-verifier-spotcheck.md`: D (exit remap 1→2), P (entry-only preflight), S (argparse shadow).
- kama `corpus/lessons/round-26-verifier-spotcheck.md`: shortcut classes F1/F3 (warning lines, file-content echo) not re-tested.
- tsukuroi itself `corpus/lessons/round-32-verifier-spotcheck.md`: rounds 30–32 rejected counters met by content-free/post-data shortcuts (depth twice, adjacency once).

Observation [obs]: none of the sibling lessons name a shortcut keyed on an ambient environment variable value or name; the env-builder shortcuts they imply are the builder-level ones (ambient copy minus GIT_*, full copy, strip-only-three). The C1 set's env-specific shapes (C04/C05/C09/C11/C13/C17) cover value/name/tracer/inheritance but not the sibling builder variants (full ambient copy, strip-only-three, extra-removals), which are closer to C11/C04 but not identical.

## B. C2 — mori kill/OOM/PSI/memory-pressure scope at 24603186

Files and lines declaring scope (ownership, not implementation):

- `mori-shokunin/PROVINCE.md:8` — "kill/OOM-related catalog-ID records and signal-11 coredump records".
- `mori-shokunin/PROVINCE.md:10` — "resource runway (disk … /tmp, memory pressure)".
- `mori-shokunin/PROVINCE.md:24` — Kill/OOM classes (kernel-OOM unit notices, oomd notices, coredumps, unit-process SIGKILL, unit failures, signal-11 coredump count; fleet/non-fleet routing).
- `mori-shokunin/PROVINCE.md:25` — Same-boot journal window since anchor (four positive_* subsets: kernel OOM, unit OOM, unit signal, process SIGKILL).
- `mori-shokunin/PROVINCE.md:26` — Resource runway (df, since-boot write average, memory PSI/fill/avail, scope high-watermark).
- `mori-shokunin/PROVINCE.md:31` — individually validated current-boot OOM/user-signal evidence.
- `mori-shokunin/PROVINCE.md:44` — FR1 Kernel OOM event-time attribution and fleet correlation (frontier).
- `mori-shokunin/PROVINCE.md:53` — FR10 Userspace OOM killers (systemd-oomd, earlyoom).
- `mori-shokunin/PROVINCE.md:55` — FR12 Event-driven pressure and CPU/IRQ PSI.
- `mori-shokunin/PROVINCE.md:56` — FR13 eBPF kill/OOM tracing.
- `mori-shokunin/PROVINCE.md:66` — tsukuroi adjacency row: mori cites tsukuroi's oom-event-plane / kill-event-deep entries, absorbs none.
- `mori-shokunin/PROVINCE.md:71` — "Received packet TSUKUROI-F1-MEM-01 (ADJ-04): … records … as prepared; … acknowledgement/acceptance/resolution are unobserved."
- `mori-shokunin/PROVINCE.md:73` — count-only kill sweep for the packet second (0 kernel OOM / notices).
- `mori-shokunin/PROVINCE.md:76` — journalctl query (0).
- `mori-shokunin/PROVINCE.md:88` — no retained kernel OOM/notice overlaps; correlation is not causation.
- `mori-shokunin/PROVINCE.md:250–259` — PSI probe (read-only, no trigger registration).
- `mori-shokunin/PROVINCE.md:268,276,286` — PSI accounting limits / system CPU full=0 note / adjacency (wave-2 finding).
- `mori-shokunin/PROVINCE.md:359–371` — Core one-shot userspace OOM killer read (mori-oom-killers.py); adjacency unchanged, mori absorbs none of tsukuroi's memory-pressure.
- `mori-shokunin/PROVINCE.md:375–384` — OOM victim selection knowledge; adjacency unchanged, corrects tsukuroi's "+200 band first" model without absorbing.
- `mori-shokunin/PROVINCE.md:392` — adjacency evidence pointer.
- `mori-shokunin/SKILL.md:3` — frontmatter: "kill/OOM events" in scope.
- `mori-shokunin/SKILL.md:15` — liveness vs kill remediation boundary.
- `mori-shokunin/SKILL.md:17` — "Did something get killed?" (MESSAGE-free catalog-ID records).
- `mori-shokunin/SKILL.md:19` — resource runway (PSI + fill/avail).
- `mori-shokunin/SKILL.md:20` — tmux relevance (not kill, adjacent).
- `mori-shokunin/SKILL.md:29–37` — OOM counters / journal class counts / positive OOM notice / kill-signal warn.
- `mori-shokunin/SKILL.md:41` — PSI threshold grading.
- `mori-shokunin/SKILL.md:45` — tmux freshness (adjacent).
- `mori-shokunin/SKILL.md:53–83` — per-scope evidence tokens and alarm rule (OOM_KILL_JOURNAL, KILL_SIGNAL_JOURNAL).
- `mori-shokunin/SKILL.md:132–133` — positive tokens reused.
- `mori-shokunin/SKILL.md:211–253` — journal probe / OOM crit / selftest gates.
- `mori-shokunin/SKILL.md:367,386` — OOM crit row / PSI reader.
- `mori-shokunin/SKILL.md:481,490` — never conclude dead/failed/killed.
- `mori-shokunin/SKILL.md:538` — cutover pointer.
- `mori-shokunin/SKILL.md:615–635` — system pressure (PSI) table and error patterns.
- `mori-shokunin/SKILL.md:664–665` — detection/report only, no kill.
- `mori-shokunin/SKILL.md:676–755` — userspace OOM killers, OOM victim selection, earlyoom invocation scope.

ADJ-04 intake: mori declares no intake format for a tsukuroi handoff. At 24603186, `PROVINCE.md:71` records the tsukuroi packet as `state=prepared` with "acknowledgement/acceptance/resolution are unobserved"; `PROVINCE.md:369` and `:383–384` state mori "absorbs none of it" and keeps OS diagnosis with tsukuroi/operator. Inference [inf]: mori's scope is detection/report and knowledge; fleet attribution of a kill remains tsukuroi's, and no intake schema is declared (consistent with tsukuroi's own PROVINCE.md round-32 note that "mori declares no intake format for it").

## Scope
read=.ufo/waves/round-33/a3w1/* (this report's peer dirs listing), sibling lane repos read-only (kaidoku,kotodama,mori,tameshi,kake,kumitate,kotoba,kama) top-level tools/corpus/lessons; mori git show at 24603186; tsukuroi SKILL.md/PROVINCE.md; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-33/a3w1/ConnSiblingPatterns/ConnSiblingPatterns.md; executed=grep/find/sed/git show (read-only)
Model: not exposed
Installs: none