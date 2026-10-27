VERDICT: defect-found

Item C2-11 — attack the C2 pre-data battery. Every one of K0–K19 is what its docstring says and fails for its intended conjunct (K3/K19 pass as the designed controls). But the battery leaves two cheap writers unscored: a statement that contradicts its own quotes while keeping all proposition tokens, and quotes that are in-window but do not substantiate the claim. I built both as fixture variants; the frozen counter scores both PASS (exit 0). The C2 counter cannot tell a lying row from a true one.

## 1. Battery integrity: every control matches its docstring and fails on its intended conjunct

Controls are built in `run_controls_c2.py` (variants: `main()` lines 150-195; record shapes: `records()` lines 66-96; scripted entry: `scripted_entry()` lines 99-119) and scored by the frozen counter `tools/check-scrub-record-r44.py` (sha256 `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059`, matches the declared pin). Predicate: `check-scrub-record-r44.py:49-51,347-348`; binding: `bound()` lines 206-225; quote/statement/host parsers lines 127-164; sources logic lines 326-339.

Battery result file `controls/battery-summary-c2.jsonl`:2 — `{"should_fail_accepted": 0, "control_accepted": 1}` (all expected-FAIL controls failed; expected-PASS controls passed).

| K | docstring | variant actually built | observed failure conjunct (C2-K*.jsonl) | intended? |
|---|---|---|---|---|
| K0 | do-nothing BASE must FAIL | empty commit on BASE | `rows:0`, per_row present=false | yes (entry absent) |
| K1 | scripted writer, no records | scripted_entry + planted reports | verdict_ok false on all 3 rows (crit/rev null) | yes (unbound) |
| K2 | K1 + results without dispatch | no w2-dispatch.json | verdict_ok false on all rows | yes (dispatch missing) |
| K3 | forged all-holds — control | full forged records | PASS, exit 0 | yes (expected PASS) |
| K4 | one counted `fails` | C2CritSR8=fails | SR8 verdict_ok false; verdicts_ok 2 | yes |
| K5 | one `partly` no residual | C2CritSR7=partly | SR7 verdict_ok false | yes |
| K6 | mention-not-assertion | output/report open with sentence quoting holds line | SR9 unbound (first line fails VERDICT_RE fullmatch) | yes |
| K7 | content-free statements | prop tokens replaced by `X` in statement paragraphs | props_ok 0 (all rows prop_ok false) | yes |
| K8 | SR7 w/o ioctl.c quotes | ioctl.c quote lines dropped | SR7 quote_ok false (`files:["S242:scrub.c"]` only) | yes |
| K9 | one quote line shifted +1 | `sysfs.c:2040:`→`2041:` | SR8 quote_ok false (`bad:1`) | yes |
| K10 | sysfs.c quote labelled S242 | `` `S243` ``→`` `S242` `` at :2044 | SR8 quote_ok false (`bad:1`) | yes |
| K11 | r43 without pointer | base r43 restored | `pointer_ok:0` | yes |
| K12 | S242 status `queued` | registry row edited `mined`→`queued` | `sources_ok:0` | yes |
| K13 | JSON verdict_line vs report first line | report override (K13: `'VERDICT: holds\nROW SR8…'`) | SR8 unbound | yes |
| K14 | padded verdict (two spaces) | output+report first line `  ROW SR7…` | SR7 unbound | yes |
| K15 | blank-line-prefixed verdict | output+report leading `\n` | SR9 unbound | yes |
| K16 | contradictory JSON `verdict` key | `{"verdict_line":"ROW SR8…holds","verdict":"fails"}` | SR8 unbound (declared_line returns None) | yes |
| K17 | S244 dropped from `source:` line | regex `source: … S244` strip | `source_line` false → sources_ok 0 | yes |
| K18 | SR9 without host line | host block removed | SR9 host_ok false (`host_ok:2`) | yes |
| K19 | `partly` + bound residual `holds` — control | residual-dispatch/results/report | PASS, exit 0 | yes (expected PASS) |

I independently re-derived each variant from `run_controls_c2.py` and the K jsonl lines (every `C2-K*.jsonl` first line carries the control's `expect`/`exit`; second line the scored JSON). No control failed for an unintended conjunct.

## 2. Surface drift: the battery scored a stale entry, not the frozen one

Candidate hashes (battery summary line 1) match the lane's frozen files for every surface file except the entry itself:
- `c2-candidate/…/btrfs-scrub-record-r44.md` sha256 `b0f2cc8c…`; lane HEAD `corpus/knowledge/btrfs-scrub-record-r44.md` sha256 `cc9233899…` (verified with `sha256sum`).
- Diff (candidate vs lane): SR7 statement was narrowed by commit `7e081698` ("C2 SR7 narrowed before wave 1 (btrfs_scrub_dev also serves device replace)") — adds a device-replace sentence and one extra quote `**Quote.** `S242` scrub.c:3081: "bool readonly, bool is_dev_replace)"` (outside every SR7 window, so it counts `good` but not `in_window`).
- So K0–K19 exercised the pre-narrowing draft. I re-ran the K3-equivalent control on the LIVE entry surface: forged all-holds + live entry → `PASS, exit 0` (`rows:3 quotes_ok:3 props_ok:3 host_ok:3 sources_ok:1 verdicts_ok:3 pointer_ok:1`). The drift does not change any control outcome, including the new SR7 quote.

## 3. Snapshot quotes: every quote line in the entry verified against the pinned source

All 33 quote texts verified verbatim on their labelled lines (frozen snapshots, digests pinned in `SNAP`):
- sysfs.c 72/74 (BTRFS_ATTR_RW/__INIT_KOBJ_ATTR 0644), 2028 (sysfs_emit "%llu\n"), 2040 (memparse), 2042 (skip_spaces), 2044 (-EINVAL), 2048 (BTRFS_ATTR_RW(devid, scrub_speed_max,…)).
- kernel scrub.c 1380/1381 (bwlimit read, 0 → return), 3147 (`if (dev->scrub_ctx ||`), 3153 (-EINPROGRESS), 3159 (sctx attach), 3222 (NULL), 3321/3331/3333/3336 (progress: 0 iff sctx), 3081 (replace arg, live-added).
- ioctl.c 3139/3141 (progress call, copy_to_user only on 0).
- btrfs-scrub@.timer 5/7/8/11; btrfs-scrub@.service 9/10; PKGBUILD 100/101; progs v7.1 scrub.c 1293/1295/421/1546/969.
- Host capture lines 1/4/5/6/7/8/9 all non-empty and support the SR8/SR9 host readings (value 0 mode 644 root; 0 links; disabled; byte-identical units; pacman owner).

## 4. Missing writers (built, scored — both PASS)

Fixture recipe used exactly as in `run_controls_c2.py`: clone `--shared` of the lane under `/fast/scratch/hyaku/tsukuroi-r44/C2CritControl-5/`, remove origin, assert toplevel == clone, checkout BASE, overlay surface (live entry + frozen files + forged all-holds records), commit with identity `fixture <fixture@invalid>`, run the frozen counter with `--lane <D> --revision <sha> --sessions <no-sessions>`. Counter sha256 checked before runs. Results (JSON receipt in `w1/C2CritControl/missing-controls.json`):

- **Control X — statement contradicts its quotes but keeps the tokens (PASS, exit 0).** SR7's statement was rewritten to assert the exact inverse of its own quotes (0 only while `dev->scrub_ctx` is *unattached*; `-ENOTCONN` *while a scrub runs*; `is_scrub_running_in_kernel` answers 1 when nothing is scrubbed), keeping all five prop tokens (`btrfs_scrub_progress`, `scrub_ctx`, `ENOTCONN`, `ENODEV`, `EINPROGRESS`) and all original quotes. Counter: `prop_ok:true quote_ok:true (good:11 bad:0 in_window:10) host_ok:true verdicts rev/crit holds` → PASS. The quote `scrub.c:3336 "return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;"` directly refutes the rewritten statement; no conjunct sees this.
- **Control Y — quotes in window but irrelevant to the claim (PASS, exit 0).** SR8's statement (unchanged) claims the *write* path (memparse, -EINVAL, suffix handling), but the quotes were reduced to the attribute macro lines (sysfs.c 72/74), the attrs-array line sysfs.c 2113 (`BTRFS_ATTR_PTR(devid, scrub_speed_max),`, inside window 2108-2116) and the throttle read lines (scrub.c 1380/1381). No quote touches memparse/-EINVAL/write parsing; file coverage and window requirements are satisfied. Counter: `quote_ok:true (good:4 in_window:4) prop_ok:true host_ok:true` → PASS.

Both are therefore un-scored cheap writers: they pass the frozen predicate with false or unsubstantiated content. The seed list's third example ("statements copied from another lane file") is *already* guarded: at BASE, none of corpus/knowledge or SKILL.md contains the SR7/SR8/SR9 tokens except a single `ENODEV` in `mount-errno-contract-r37.md:15` (`git grep -F` at base; `novelty_base_hits:0` for ENOTCONN/memparse/KillSignal), so a verbatim cross-file copy fails `prop_ok`.

## 5. Small findings
- K1/K2 fail on the intended conjunct (unbound verdicts) but carry an incidental side effect: `scripted_entry()` drops multi-line `**Host reading.**` continuation lines (they don't start with `**Host reading.**`), so SR8/SR9 host_ok also flip false. Harmless for the verdict; noted for exactness.
- `transcripts_bound` is reported outside the predicate and is 0 in all controls (`--sessions <no-sessions>`); fine.

## What I did not do
Did not run `run_controls_c2.py` itself (the existing `C2-K*.jsonl`/summary files were read as evidence). Did not touch lane tracked files, git state, or the host. Scratch removed after copying receipts.

## Proposed addition (untested against a modified counter — the counter is frozen; this is a suggested future control)
Add to the battery, scoring on the same predicate: `K20` — SR7 statement inverted as in Control X (tokens kept, quotes kept) must FAIL; `K21` — SR8 write-path claims quoted by none of the write-path lines must FAIL. Both would require the counter (or a wave-2 reviewer gate) to gain a semantic check: statement-claim direction vs. quote content (e.g., bind each prop token to a quote line whose text implies the claim direction). Until then, the predicate cannot distinguish a true SR7 from its exact opposite.
