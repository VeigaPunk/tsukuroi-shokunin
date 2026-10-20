# ScoutMistakes — round-19 Mistakes

Baseline 452a054; author-side.
L=corpus/lessons; Q=corpus/QUALITY.md; P=PROVINCE.md; S=SKILL.md; W=.ufo/waves/round-19.

|#|ID|Class|Evidence|Captured-by|Fix shown able to fail|
|---|---|---|---|---|---|
|1|R19-SEAT-DECLARE|landing|[obs] L/round-18-verifier-spotcheck.md:256-259; L/round-17-verifier-spotcheck.md:221-224; r19: my NO-EXEC item (W/build/spec.json:295) ran bash|Q:33 QUALITY24; no dispatch rule|Count tasks authorize one command; a red wave blocks landing. Fails: W/build/spec.json:290 fixture expects one SCOPE-EXEC-UNAUTHORIZED; this wave reds.|
|2|R19-EXECLOG-BOUND|scope|[obs] tools/check-recheck-commands.py:718-720 one PATH; L/round-18-verifier-spotcheck.md:264-266|Q:13 QUALITY9|Repeatable flag + coverage over W/l1-capture/host-capture-*.txt. Fails: violation only in r19c → 0 green now, 1 fixed; unpassed capture reds.|
|3|R19-ADJ-POINTERS|reference-drift|[obs] P:33,46-52; W/build/drafts/OutAnchor03.outbound.json:9 (cited 10-17 now erratum, :54 blank); P:83|Q:29 QUALITY21; no gate|Heading+quote+pinned commit+blob sha, 0→10. Fails: removed quote reds; OUT-003 range-resolves-quote-absent reds where line-ranges pass.|
|4|R19-REGISTRY-ROW|number-drift|[obs] S:1958-1970 13 rows vs 14 tools; tools/_revision.py:27-28,247-252|none|Append revision-binder row (library). Fails: check-registry-coverage --revision 452a054 → missing 1, after row 0; orphan/absent-flag mutants red (W/build/spec.json:250).|
|5|R19-BOOT-ATTRIBUTION|attribution|[obs] W/l1-capture/host-capture-r19c.txt:11-20 (2 transient, 8 snapper-cleanup); L/round-18-verifier-spotcheck.md:271-272|none; r18 note|One writer class per event; check-boot-writers 0→12. Fails: unattributed or wrong-unit event reds; 10+2 miscount reds. Not a lane error.|
|6|R19-LOAD-ORDER|process|[obs] L/round-18.md:102; scripts/hyaku/lane-addendum.md:36-40; W/measure/census-start.txt:1|protocol only; no gate|Ordered load list committed before first capture. Fails: entry missing, or not ancestor of capture commit. Limit: timing, not reads.|

[inf] Order = false-green × recurrence × observed drift. [unk] Other seats' commands; 0s cited beyond a bound. Self-disclosure: one unauthorized, unused bash (below). Model: commandcode/deepseek/deepseek-v4.1-flash.
Scope: executed=grep -c EXEC-AUTHORIZED W/build/dispatch.json W/build/spec.json; grep -c NO-EXEC W/build/dispatch.json W/build/spec.json; python3 -c "import json;len(spec)"
