# E4InstrumentCheck binding

Verdict: frozen instrument digests, selftests, negative controls, reachable draft, working-tree predicates, and host-deletion rejection match their declared mechanical contracts. Semantic limitation found: the accepted draft/JD3 says “smaller of free space and keep_free” although the pinned code subtracts keep_free.
Unchecked: post-sibling-correction final note bytes and final committed closure. Source-reference CLI cannot inspect an uncommitted note; its existing evaluation functions were additionally applied to a copied working-tree note (0 dangling ids), explicitly not revision-bound admission.

Axes: depth, freshness, instruments. Read-only executor; changed only this seat's reports/receipts. No tools installed, git mutations, external substrate changes, or subagents. No LSP endpoint is exposed in this seat's tool inventory; inspected definitions by file reads instead. The note already existed on first discovery; no polling was needed.

## Frozen digests

Compared independent `sha256sum` output against SCORECARD.md:6292–6299:

| Instrument | Observed and declared sha256 | Match |
|---|---|---|
| count-jd-rows-r76.py | `549f6ba352284d44d7462954d1de36d2134bab73b0440e4e011b9017ec58fe4f` | yes |
| check-r75-routed-r76.py | `01e12e6a57211f80d2f9e042a336cf7ebe933b0560fecedef0411fe158ffe3d7` | yes |

Receipt: `instrument-digests.json` alongside this report.

## Exact execution results

Commands used absolute tool paths, cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, `TMPDIR=/fast/scratch/hyaku/tsukuroi-r76/E4InstrumentCheck`, and `PYTHONDONTWRITEBYTECODE=1`. JSON receipts retain full argv, cwd, TMPDIR, stdout, stderr and rc.

| Receipt stem | Exact stdout summary | rc |
|---|---|---|
| counter-selftest | `SELFTEST: PASS (14 cases, 14 passed, 0 failed)` | 0 |
| routed-selftest | `SELFTEST: PASS (10 cases, 10 passed, 0 failed)` | 0 |
| counter-base | `JD_MAP absent` | 128 |
| routed-base | `ROUTED_STALE=8 ROUTED_OK=0/8` | 1 |
| counter-declaration | `JD_NOTE absent` | 128 |
| draft-control | `JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1` | 0 |
| counter-working-tree | `JD_ROWS=8 JD_VERIFIED=8 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=1 JD_MALFORMED=0 met=1` | 0 |
| routed-working-tree | `ROUTED_STALE=0 ROUTED_OK=8/8` | 0 |
| copy-host-deletion | `JD_ROWS=8 JD_VERIFIED=0 JD_SOURCES=4 JD_SNAPSHOTS=4 JD_HOST=0 JD_MALFORMED=1 met=0` | 1 |

Base = `865b38c96c23ec0bcace8ca3ee884f860693ce43`; declaration = `d5f0565bfb42a405ec024d8a5b0796514fb92002`. Revision reads were the instruments' git plumbing reads; no stash or checkout.

Draft replay copied the frozen four snapshots/map and current registry into scratch, then installed `before/draft-rows-validated.md` at the counter's expected note path. It reproduced `before/draft-row-control.txt` exactly. Registry digest of the copied fixture: `e7b7b71e95e2b43d023eaceee754e5926c1862120ff33db9ee1e4e76fbe16693`.

## Reference and line-ending gates

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-knowledge-refs-r68.py --revision d5f0565bfb42a405ec024d8a5b0796514fb92002 --lane /home/vgpnk/Projects/shokunin/tsukuroi-shokunin` returned PASS, rc 0, 93 notes, 0 findings and 0 dangling ids (`refs-declaration.json`). This revision predates the new note: that CLI result does NOT admit the working-tree note.

The documented CLI supports only immutable revisions, not individual paths/worktrees. Without creating a commit, imported that same gate with bytecode disabled, used its `registry_ids_at()` parser against the copied registry (read_blob supplied fixture bytes), and its unmodified `evaluate()` on the copied note. Operative header line 3 resolves S318, S319, S320, S321; dangling ids = `[]`, findings = `[]`, rc-equivalent 0 (`refs-note-working-copy.json`). This is a working-copy evaluation, not a successful revision-bound CLI run over the note.

`python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-line-endings-r64.py --check` returned rc 0:

```text
CHECK_LINE_ENDINGS: PASS (380 file(s) checked, 0 violation(s))
check-line-endings-r64: 23642 allow-listed .ufo path(s) skipped (upstream captures)
```

Receipt: `line-endings.json`; tally is a point-in-time tracked-set lane gate, not a claim about concurrently changing or untracked files.

## Independent attack and semantic discrepancy

Removed the entire `## Effective limits on this host` section from a scratch-only copy of the real note, keeping the row table, registry and pinned snapshots intact. Counter stderr, exactly:

```text
  line 0: host block missing heading ## Effective limits on this host
```

It rejected the copy with rc 1 and JD_HOST=0. Receipt: `copy-host-deletion.json`; preserved input files: `checked-note.md`, `host-deletion-mutant.md`. Checked real-note sha256 was `ef3617004cbf63b05191870602f58ba9b083b5e8d895e9e1f4099c632bc34314`.

Semantic discrepancy (both values): the accepted draft and original note JD3 say “used space plus the smaller of free space and keep_free”; pinned `journald-manager.c:168` actually says `avail = LESS_BY(vfs_avail, metrics->keep_free);`, followed at :170 by `space->limit = CLAMP(vfs_used + avail, metrics->min_use, metrics->max_use);`. Thus token overlap/quote validity can admit an incorrect arithmetic paraphrase; `JD_VERIFIED=8` is structural grounding, not semantic verification. The frozen declaration repeats the incorrect paraphrase. E3Note notified this seat that corrected note bytes were subsequently written and that its specifically assigned final counter was running; that is coordination evidence, not a check performed here. This seat intentionally preserves the pre-correction result rather than presenting it as verification of corrected bytes. Parent should bind final admission to the corrected committed bytes and resolve the frozen-declaration discrepancy explicitly.

## Scope and handoff

All assigned executable controls completed; no instrument, note, registry or shared document edits. Scratch was removed before terminal yield. Parent owns post-integration committed-revision counter/reference gates and closure; no committed freshness claim is inferred from a working-tree `ROUTED_OK=8/8`.

Self-evaluation: accuracy 4 (semantic and revision limits explicitly bounded); completeness 4 (all executable requests covered, but official refs CLI cannot admit an uncommitted note); clarity 4 (raw JSON separated from summary); actionability 4 (final revision binding explicitly owed); conciseness 4 (retained full receipts avoid embedding long JSON). Overall 4.0/5. Improvement: parent runs final immutable-revision admission after integration; this seat cannot supply that without prohibited commits.
