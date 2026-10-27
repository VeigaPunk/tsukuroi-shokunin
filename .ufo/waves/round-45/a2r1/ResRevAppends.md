VERDICT: supports

Item R-5 — the `## Round-45 qualification — the stop outcome` append in `corpus/knowledge/btrfs-scrub-record-r44.md`, the `## Round-45 coverage note` append in `corpus/README.md`, and the S246 `teaches` cell change in `corpus/SOURCES.md`, all judged at 194a4523288759b4b73248d1ebcce53e43d0eec7 against the entry rows `corpus/knowledge/btrfs-scrub-grounding-r45.md` GR1-GR3, the pinned snapshots, and every line number the appends name. Receipts in `.ufo/waves/round-45/a2r1/ResRevAppends/` (full.diff, counter-out.json, census-out.txt).

## Snapshot verification (precondition)

- `sha256sum -c .ufo/waves/round-45/frozen/src/SHA256SUMS` → all 5 OK (cmdline.c, dev-replace.c, systemd.kill.xml, kstrtox.c, vsprintf.c).
- `sha256sum -c .ufo/waves/round-44/frozen/src/SHA256SUMS` → all 5 OK (scrub.c, sysfs.c, btrfs-scrub@.timer, btrfs-scrub@.service, PKGBUILD).
- `sha256sum -c` round-42/frozen/src/SHA256SUMS: scrub.c `48df2e2f…0801` matches; CHANGES also matches.
- `.ufo/waves/round-45/frozen/hostcap/capture.txt` sha256 `f5958a83b7cf1e2e438ac1b543f1c521f3f9370287fc4c4bcea38947c3991e70` — matches S249's pinned value and the `f5958a83…` prefix printed in the README Sources cell.

## Append-only property

- `git diff 18389f44…194a4523 -- corpus/knowledge/btrfs-scrub-record-r44.md corpus/README.md` contains zero removed content lines (the only `^-` lines are the `---` file headers); both files gain one trailing `+` hunk each (`@@ -159,3 +159,15 @@` and `@@ -450,3 +450,17 @@`). Append-only holds, so the README sentence "Append-only; the coverage map, the Frontier bullets and the round-38 to round-44 notes above stay as written" and the r44 append's "Appended; nothing above is rewritten" are both true.
- `corpus/SOURCES.md`: single hunk `@@ -252,7 +252,7 @@`, one line changed — the S246 row (line 255 at both revisions). Not an append but the declared cell edit. Word-level diff of the line: the teaches cell gains exactly `; a shifted value that overflows becomes ULLONG_MAX` (cell 7 of 13, verified by splitting on `|`); all other cells byte-identical.

## Sentence-by-sentence check — record-r44 append (`:164-173`)

1. "the grounding it points at is `corpus/knowledge/btrfs-scrub-grounding-r45.md` row GR3" — true: GR3 (entry `:119-157`) covers the systemd stop outcome; the file exists at 194a4523.
2. "The block above grounds SR9's systemd side; it does not qualify the outcome sentence at `:99-101` or the triage bullet at `:140-142`" — true: the `:159-162` grounding sentence names the three `[inference]` marks (`btrfs_scrub_dev` caller, `memparse` suffixes, `KillSignal=` stop signal); `:99-101` still asserts the cancel→record chain unqualified; `:140-142` still asserts "leaves a canceled, resumable record" unqualified. The appended block then adds exactly that qualification.
3. "SIGINT (`KillSignal=2`), then SIGCONT, and SIGKILL only if a process remains once `TimeoutStopUSec=5s` has passed (GR3; S248 `systemd.kill.xml:68,91,96,101,108,114-115`; S249 `capture.txt:3-5`)" — every named line verified:
   - `systemd.kill.xml:68` KillMode=control-group kills all remaining processes; `:91` the `TimeoutStopSec=` delay (applies to control-group, the applicable mode); `:96` termination repeated with SIGKILL/FinalKillSignal unless SendSIGKILL disabled; `:101` default control-group; `:108` KillSignal= controls the first signal; `:114-115` SIGCONT always sent right after. Consistent with GR3 `:121-129`.
   - `capture.txt:3` `KillSignal=2` (= SIGINT; the packaged unit sets `KillSignal=SIGINT`, S244 btrfs-scrub@.service:9), `KillMode=control-group`, `TimeoutStopUSec=5s`, `FinalKillSignal=9`, `SendSIGKILL=yes`; `:4` the `10-faster-shutdown.conf:2` `DefaultTimeoutStopSec=5s` source; `:5` `dropin_owner … none`. "only if a process remains once 5 s has passed" is accurate for KillMode=control-group (the alternative main-process-exited condition at `:89` applies to `mixed` only).
4. "The SIGINT handler issues `BTRFS_IOC_SCRUB_CANCEL` (S237 `scrub.c:416-424`, installed in the foreground start at `:1546`)" — verified: `scrub.c:417-424` defines `scrub_sigint_record_progress` issuing `ioctl(cancel_fd, BTRFS_IOC_SCRUB_CANCEL, NULL)` at `:421`; `:436-443` `scrub_handle_sigint_child` installs it via `sigaction(SIGINT,…)`; `:1546` `scrub_handle_sigint_child(fdmnt)` runs inside `scrub_start` (`:1233`) on the non-background path (`-B` sets `do_background = false` at `:1293`; the `if (do_background)` fork block at `:1512` is skipped), i.e. the foreground start the packaged service runs.
5. "whether the start then writes its `canceled` record before the SIGKILL is not established [inference]" — consistent with GR3 `:130-132` and README cell's "left undecided"; correctly marked.
6. `"Leaves a canceled, resumable record" therefore holds … otherwise the record stands as it was last written during the run, and `btrfs scrub resume` sees whatever that record says` — the quoted phrase matches the triage bullet text `:141-142` (case differs: source reads "leaves"); the conditional is the honest consequence of the undecided write; resume reading the last record is SR3-consistent.

## Sentence-by-sentence check — README coverage note (`:454-466`)

1. Append-only claim — verified above.
2. Table cell — GR1 ("`memparse`: one letter of `K M G T P E`, 1024 per step, base-0 radix, bare newline = 0 = no limit") matches entry `:16-25` and pinned sysfs.c:2040-2044 (`memparse`, `skip_spaces`, `-EINVAL` on trailing non-space — a bare newline passes, limit 0 = none per SR8). GR2 (two `btrfs_scrub_dev(..., false, true)` call sites; `EINPROGRESS` for a present, writeable non-target device while replace started or suspended, after the `-ENODEV`/`-EROFS`/`-EIO` checks; unprivileged sysfs view) matches entry `:57-71` and pinned dev-replace.c:701-703 & 1265-1268 (both end `false, true`), sysfs.c:1288 (`exclusive_operation` = "device replace") and sysfs.c:2015 (`replace_target` emits `%d`). GR3 (SIGINT from `KillSignal=`, SIGCONT, SIGKILL if a process remains after `TimeoutStopUSec=5s`; `canceled` write undecided) matches entry `:121-132`. Sources cell `S246-S249` lists the round's new rows; the pinned-snapshot path and `hostcap/capture.txt` sha256 prefix check out; `tools/check-scrub-grounding-r45.py --revision <REV>` exists and runs (below). Minor observation (not a defect): the row does not restate re-opened sources S237/S242-S244 — same loose convention as the r44 row's "entry header and rows at the measured revision"; no false statement.
3. "Frontier: nothing moves" paragraph — `:443-444` verified: those lines list "running, canceling, resuming or limiting a scrub, enabling its timer, resetting the error counters, profile changes, firmware, LUKS and any repair stay operator-owned" and the record's content/running state/NVMe SMART staying Frontier sits at `:441-443`; the round-44 promotion sentence sits at `:438-440`. The binding sentence (counted a2w1 seats; `partly` residual of a2r1; `SCORECARD.md` "Round 45 — attempt-2 rebinding") matches the scorecard section at `SCORECARD.md:2892` (`residual, if any, a2r1`; rebound `RESIDUAL_WAVE` constant). "Round 45 bound none of them: the depth gate FAILED (`verdicts_ok` 0) and GR1-GR3 are pending, not admitted (entry section 'Gate status — round 45')" — verified: the counter run below prints `verdicts_ok` 0, and entry `:186-195` is the section titled "Gate status — round 45 (the depth gate FAILED; rows pending)" saying exactly that.

## S246 teaches cell

Appends `; a shifted value that overflows becomes ULLONG_MAX` — verified verbatim against pinned cmdline.c:191-192 (`if (unlikely(check_shl_overflow(ret, shl, &ret))) ret = ULLONG_MAX;`). Consistent with the SCORECARD C2 declaration ("overflow to `ULLONG_MAX`") and entry GR1 `:21`.

## Counter and census runs

- `python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-scrub-grounding-r45.py --revision 194a4523288759b4b73248d1ebcce53e43d0eec7` → exit 1; JSON prints `"pointer_ok": 1`, `"sources_ok": 1` (also `rows` 3, `quotes_ok` 3, `props_ok` 3, `host_ok` 3, `snapshots_ok` true, `novelty_base_hits` 0; `verdicts_ok` 0, `verdict` FAIL — the declared depth-gate failure, consistent with the appended claims). Full output: `.ufo/waves/round-45/a2r1/ResRevAppends/counter-out.json`.
- `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0; output ends `tsukuroi ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md` (W04 duplicate-URL notices are pre-existing, scope-wide warnings). Receipt: `.ufo/waves/round-45/a2r1/ResRevAppends/census-out.txt`.

## Findings with replacement text

None. All sentences in the two appends and the S246 cell edit check out against the entry rows, the digest-verified pinned sources and every named line number; both appends are append-only; both required script outputs hold.

## Not done / out of scope

- I did not re-derive the entry rows themselves (GR1-GR3 verdicts belong to other seats); I checked the appends' paraphrases of them.
- I did not verify live `systemctl show` values; I trusted the pinned `capture.txt` after verifying its sha256.
- No tools installed (pacman paused; nothing needed).
