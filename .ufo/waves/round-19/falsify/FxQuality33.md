# FxQuality33 — /boot writer attribution gate (QUALITY criterion 33 / claim C2, axis R19-BOOT-ATTRIBUTION)

Revision under attack: `8e5916360f2dfe7bc4eb4ba144081af555900116` (registry/captures/SOURCES read here); baseline: `452a054677f6b18284917d7c08c45361f91c25ac`. Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin (worktree HEAD `2fd1e676…`, gate binds revisions via git objects, not the worktree).

## Attack

Criterion 33 (`corpus/QUALITY.md:64-76`, last criterion in the file) declares /boot writes attributable only with writer class, mechanism file:line, unit/hook identity and event timestamp, and the round-19 lessons row pins the falsification receipt: "baseline with the target registry is red, 13 EVENT-UNPUBLISHED + 7 WRITER-UNPUBLISHED; selftest extra-unclaimed-line and wrong-signature fixtures red" (`corpus/lessons/round-19.md:55`). This seat attacks whether that receipt is real: (a) does the documented baseline comparison actually exit red with exactly those finding counts, (b) do the two named negative fixtures exist in the selftest and fail by design, (c) does the criterion state its claim boundary (attribution of writers, not proof of boot safety), and (d) does the target actually pass with 13/13 attributed across 7 named writer classes.

## Method

All commands run in the lane root with `python3` + system `git` only; no tools installed (tooling directive: nothing needed, nothing installed). Gate git surface is read-only for `--revision` runs (`tools/check-boot-writers.py:96-99`, `GitReader` docstring `:105` "Read regular committed blobs only; never read the working tree"); `--selftest` builds its fixture repo inside `tempfile.TemporaryDirectory` and commits only into that fixture's own `.git` (`:592-595`, `:664-672`).

1. Baseline-with-target-registry: `python3 tools/check-boot-writers.py --revision 452a054677f6b18284917d7c08c45361f91c25ac --registry-from 8e5916360f2dfe7bc4eb4ba144081af555900116` (output to /tmp/fxq33-baseline.json).
2. Target: `python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116`.
3. Selftest: `python3 tools/check-boot-writers.py --selftest`.
4. Finding census: `python3 -c` Counter over the baseline JSON findings by id/site.
5. Fixture presence: grep of `tools/check-boot-writers.py` for the fixture names and finding ids; source read `:659-733`.
6. Boundary wording: grep `corpus/QUALITY.md`, `corpus/`, `PROVINCE.md` for safety/boundary phrasing; read of `corpus/knowledge/boot-writers-r19.md` (target revision) `## Limits` and `## QUALITY check` sections.
7. Completeness cross-check: `git show 8e591636…:.ufo/waves/round-19/l1-capture/host-capture-r19{,b,c}.txt | grep -c "Updated: /boot/limine.conf"` and writer-class headers `grep -n "^### W-"` on the knowledge file.

Note: the first gate invocations were piped through `tail`, so an initially observed `EXIT=0` was `tail`'s status; re-runs captured the real exit codes (baseline 1, target 0, selftest 0).

## Verdict

**CONFIRM** (claim C2 / criterion 33; attack did not falsify — the gate reproduces every documented expectation).

- Baseline-with-target-registry is red: exit 1, `status: FAIL`, `counts = {attributed_events: 0, events_total: 13, unattributed: 13, writer_classes: 0, writers_with_events: 3}`, findings exactly `EVENT-UNPUBLISHED ×13` (EV-01…EV-13) + `WRITER-UNPUBLISHED ×7` (W-KERNEL-REMOVE, W-LIMINE-EFI-COPY, W-LIMINE-EFI-DEPLOY, W-MKINITCPIO-HOOK, W-SNAPPER-CLEANUP, W-SNAPPER-PLUGIN, W-WATCHER), no other findings — matching `corpus/lessons/round-19.md:55` verbatim.
- Target is green: exit 0, `status: PASS`, 13/13 attributed, `writer_classes: 7`, zero findings; all seven `### W-*` classes present in `corpus/knowledge/boot-writers-r19.md` (file lines 13-57 at `8e591636…`).
- Both named negative fixtures exist and fail by design inside a passing 11/11 selftest: `extra unclaimed event line` → expects FAIL + `EVENT-UNATTRIBUTED` (`tools/check-boot-writers.py:698-702`); `wrong signature` → expects FAIL + `EVENT-SIGNATURE-MISMATCH` (`:716-720`). The suite additionally mirrors this seat's baseline case (`registry-from with unpublished baseline`, FAIL + `WRITER-UNPUBLISHED`, `:730-732`).
- Claim boundary is stated. Criterion 33: "known writer is expected automation, not evidence of interference; an unattributed unit, a failed run, or a write without a matching timer or hook remains a finding" (`corpus/QUALITY.md:71-72`). Knowledge-file Limits: "No current-state certification", "reads no /boot file and states no /boot mtime, hash or content", "The content change is not verified" (`boot-writers-r19.md` `## Limits`), plus "Nothing here authorizes a package, service, hook, initramfs, bootloader or /boot change" (header) and QUALITY-check item "25. Not applicable. No next-boot verdict or image-derived claim is made."
- 13-event completeness cross-checks: EV-01…EV-13 = 3 ALPM rows (r19b:1695,1700,1702) + 10 journal rows (r19c:11-20); r19c contains exactly those 10 full rows plus the two add events repeated in short form at :25/:42 (duplicates of :11/:12), and the knowledge file documents the probe blocks and the r19:562-563 count-10 cross-check. Raw `grep -c` across all three captures (39) over-counts because captures repeat events in multiple output formats; the gate requires one claim per probe-block line, which is the correct denominator.

## Evidence

- Baseline run (real exit code): exit 1; JSON at /tmp/fxq33-baseline.json; id census `{'EVENT-UNPUBLISHED': 13, 'WRITER-UNPUBLISHED': 7}`; sites EV-01…EV-13 and the 7 `W-*` ids listed above.
- Target run: exit 0; `{"revision":"8e591636…","status":"PASS","counts":{"attributed_events":13,"events_total":13,"unattributed":0,"writer_classes":7,"writers_with_events":3},"findings":[]}` (/tmp/fxq33-target.json).
- Selftest: exit 0; `PASS (11 cases, 11 passed, 0 failed)` (/tmp/fxq33-selftest.txt).
- `tools/check-boot-writers.py:702` (`check("extra unclaimed event line", extra, FAIL, "EVENT-UNATTRIBUTED")`), `:717-720` (`wrong_signature` fixture with `journal-unit` value `different.service` → `EVENT-SIGNATURE-MISMATCH`), `:730-732` (registry-from baseline red case).
- `corpus/QUALITY.md:64-76` (criterion 33, boundary at :71-72); `corpus/lessons/round-19.md:55` (documented expected receipt, matched exactly).
- `corpus/knowledge/boot-writers-r19.md` @ `8e591636…`: header boundary line, `## Writer classes` (7 classes, lines 13-57), `## Event table` (EV-01…EV-13, lines 66-80), `## Operator decision rule` (:86-93), `## Limits` (:95-105).
- Registry default `corpus/knowledge/boot-writers-r19.json` (`tools/check-boot-writers.py:27`); `--registry-from` documented in `--help` ("read registry, captures and SOURCES.md at this bound revision").

## Residual

- I did not independently re-verify each of the 13 events byte-for-byte against the capture blobs; the gate does this with capture digests (tamper case `CAPTURE-TAMPERED` in the selftest), and I verified gate behavior + counts, not every blob citation.
- "Landed and pushed" branch binding was checked locally only (`git branch --contains 8e591636…` → master); no remote probe was in scope.
- The literal phrase "boot safety proven" appears nowhere; the boundary is stated in interference/certification terms (QUALITY.md:71-72 and the knowledge-file Limits). Substantively satisfied; wording differs from the seat prompt's paraphrase.
- Selftest hygiene: the fixture `TemporaryDirectory` is created with `dir=<repo root>` (`tools/check-boot-writers.py:29,664-665`), i.e. a transient untracked dir inside the lane worktree while the selftest runs (git writes confined to the fixture's own `.git`; auto-removed; verified no `check-boot-writers-*` residue and lane `.git` untouched). A `/tmp` default would be cleaner; no residue or state change resulted.
- Working tree had concurrent sibling edits (plan.json, dispatch.json, etc.); none were touched by this seat. No pacman transaction, no host probe, no /boot access; read-only git verbs only.

Scope: executed=python3 tools/check-boot-writers.py --revision 452a054677f6b18284917d7c08c45361f91c25ac --registry-from 8e5916360f2dfe7bc4eb4ba144081af555900116; python3 tools/check-boot-writers.py --revision 8e5916360f2dfe7bc4eb4ba144081af555900116; python3 tools/check-boot-writers.py --selftest