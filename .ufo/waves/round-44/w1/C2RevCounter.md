VERDICT: defect-found

Seat C2RevCounter-6, item C2-8 — line-by-line review of `tools/check-scrub-record-r44.py`
(sha256 `c96aeda99fc53336c7a12c3a492a5745bfbca28e3334d2b98f0547532a4c8059`, re-verified at review
end; 361 lines) against the Round-44 declaration (SCORECARD.md § "Round 44 — declaration" at freeze
`1d2afffeaedbb553d951f53c9edb0190e345b1ab`). All line refs below are `tools/check-scrub-record-r44.py`
unless noted. Receipts: `.ufo/waves/round-44/w1/C2RevCounter/` (counter outputs at both revisions,
c1–c7 fixture outputs, fx2 output, driver `fx1.sh`, novelty greps).

## 1. Runs requested by the item

- `python3 tools/check-scrub-record-r44.py --revision 7e081698d4fc3c4ea944884fd093058de9909de1`
  → exit 1, `verdict: FAIL` with `rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1,
  novelty_base_hits 0, pointer_ok 1, snapshots_ok true, capture_ok true, verdicts_ok 0`
  (receipt `run-impl.json`). The only red axis is `verdicts_ok`: all six w2 seats are unbound
  (`per_row.*.verdicts` all `null`). That is the expected wave-1 state — the declaration binds
  verdicts only from WAVE 2 seats, so this frozen counter cannot PASS at a wave-1 revision by design.
- `--revision 98020ece0674e0b569ee23aed10ffbee355b248e` → exit 1, FAIL with `rows 0, quotes_ok 0,
  props_ok 0, host_ok 0, sources_ok 0, pointer_ok 0, snapshots_ok false, capture_ok false`
  (receipt `run-base.json`): entry and frozen snapshots absent at base — the expected before-state.
- Exit codes: 0 PASS / 1 FAIL / 2 usage error confirmed (`--revision deadbeef…` →
  `{"error": "cannot resolve …"}`, exit 2; receipt `out-bogus.json`).
- Pre-data battery `controls/battery-summary-c2.jsonl` agrees: same counter sha in its header line;
  K0–K2, K4–K18 FAIL, K3 (forged records) and K19 (partly + bound residual holds) PASS; final line
  `{"should_fail_accepted": 0, "control_accepted": 1}`.

## 2. Verified correct (evidence)

- Snapshot pins: all 8 SNAP/CAPTURE digests (:70-84) match `git show 7e081698…:<path>` byte-wise
  (sha256sum over re-extracted copies). Windows bracket the real code: `dev->scrub_ctx`/-EINPROGRESS
  attach (scrub.c 3140-3165), detach NULL (3215-3226), `btrfs_scrub_progress` ternary
  `dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV` (3321-3337), ioctl copy-back only on 0 (ioctl.c 3126-3145);
  `BTRFS_ATTR_RW`→0644 (sysfs.c 70-76), `%llu\n`/memparse/skip_spaces/-EINVAL (2019-2050), attr decl
  (2108-2116); throttle `bwlimit == 0` return (r44 scrub.c 1365-1385); `-B`→do_background=false +
  do_print=true (r42 scrub.c 1286-1296), SIGINT handler → BTRFS_IOC_SCRUB_CANCEL (412-444),
  `stats.canceled = !!ret` (960-972), child handler call (1510-1548). The entry's quotes are true to
  these lines (impl run: 11/9/13 good quotes, 10/9/13 in-window, bad 0).
- Host lines: cited capture.txt lines 1,4,5,6,7,8,9 exist and are substantive (CapEff=0; mode 644
  value 0; wants instances 0; timer disabled; installed unit digests equal the S244 pins; pacman
  owner btrfs-progs 7.1-1) — receipt `snap/capture.txt` content quoted in report §4 of
  `entry-impl.md` copy in receipts.
- Novelty is honestly achievable: independent `git grep -n -F -- <token> 98020ece… -- corpus/knowledge
  SKILL.md` for ENOTCONN / memparse / KillSignal each return nothing (exit 1; receipts
  `novelty-*.txt`). The r43 entry at base does not contain them.
- sources_ok is earned, not accidental: SOURCES.md rows S242/S243/S244/S245 are absent at base
  (base SOURCES.md exists, 239094 bytes), carry kind, `mined`, `2026-10-26`, tag, and used-by naming
  the entry; S237/S240 used-by names the entry; entry line 1 lead-run lists all six ids
  (`source:` regex :335-338 matches exactly this shape).
- Pointer: r43 entry line 4 `extended-by: round 44 — … btrfs-scrub-record-r44.md` is within the
  first 20 lines (:342-343).
- Binding fails closed on every negative I threw at it: contradictory JSON `verdict`
  (`verdict_line` says holds, `verdict` says fails → unbound; :187-203, receipt `out-c2.json`),
  report first line differing from the recorded output line (:222-224, `out-c3.json`), raw output
  with a leading blank line (first line "" → fullmatch fails; :203, :216-218, `out-c4.json`).
  Positive control binds (`out-c1.json`: verdicts_ok 1, SR7 rev+crit holds). Cross-row protection:
  a seat line is rejected for another row (:217 `m.group(1) != row`); dispatch/results entries must
  be unique (:210, :212-214); the residual chain fails closed (:303-308: resid unbound or `fails`
  → row not ok). `transcripts_bound` is reported outside the predicate as declared (impl 0/0;
  fx2 fabricated records 0 of 6 found in host transcripts).

## 3. Findings

- **F1 (medium, not covered by any control) — quote text is bare substring containment, so a gutted
  quote still counts.** :287 `if src and 1 <= n <= len(src) and q in src[n - 1]` with `(.+)` from
  QUOTE_RE (:105-106). Demonstrated: replacing SR8's `sysfs.c:2044: "return -EINVAL;"` quote text
  with `"n"` leaves `quotes_ok 3, good 11, bad 0` (`out-c5.json`). Together with :290/:294 (only one
  good quote must sit in any window of the key; the impl entry itself carries SR7's scrub.c:3081
  quote outside every window), a careless writer can satisfy the whole quote gate with one in-window
  trivial quote plus one token per required file. The docstring's "occurs on its named line" (:22-24)
  is accurate but the gate is much weaker than it reads. K9 (shifted line) and K6 (mention-not-
  assertion) do not cover this.
- **F2 (medium, undeclared) — SOURCES registry is last-duplicate-wins.** :167-175 `rows[cells[0]] =
  cells`: any `^ {0,3}|S\d{3,}|`-shaped line with exactly 11 cells anywhere in SOURCES.md (including
  inside a fenced code block) participates; duplicates are not flagged. Demonstrated both directions:
  appending a doctored S242 duplicate (used-by dropping the entry) flips `sources_ok 1→0`
  (`out-c6.json`) — an innocent re-listing would silently regress a passing lane; appending the
  original row again restores `sources_ok 1` (`out-c7.json`) — a broken row can be resurrected by a
  later corrected duplicate. K12 edits the row in place; no control appends.
- **F3 (medium-low, partially declared) — base-relative checks fail open in a repo without base
  history.** `novelty_hits` ignores the git exit code (:240-243): if BASE is not resolvable
  (shallow/re-rooted clone), grep fails and yields 0 hits = "novel"; `reg_base` is `{}` when
  `show(BASE, 'corpus/SOURCES.md')` returns None (:267), making "absent at the base" (:330) trivially
  true. Demonstrated: an orphan repo with zero shared history — real entry/registry/snapshots +
  self-authored w2 dispatch/results/reports — returns **exit 0, verdict PASS** with all fields green
  (`out-fx2.json`, revision `774732b49f199c5c149ffd276990ccef469867c7`). The declaration names the
  forged-records channel (C2-K3) but not the vacuity of novelty/newness in a baseless repo. On the
  lane itself BASE exists (both runs above), so this is fixture/clone-sensitivity, not a live defect.
- **F4 (low) — prop_ok is satisfied by any occurrence of the token in the statement cell.** :296
  `all(t in st for t in spec['props'])` over raw text between markers (:143-152): a negation
  ("never calls memparse") or a bare mention passes. The K6 fixture fails, but via its particular
  construction; the mechanism cannot separate mention from assertion. Coarse by design (declared
  shape gate, SCORECARD freeze: "C2's lexical checks are shape gates"), recorded here for the
  six-month reader.
- **F5 (low, code-level only, not run) — repeated `## SR7` headers merge.** :127-135
  `out.setdefault(cur, [])` accumulates lines across two `## SR7` sections, so props/quotes may be
  split across separately-placed sections and still pass; `## ` headings inside fenced blocks would
  also cut a row.
- **F6 (info) — window/anchor drift.** Counter SR7 window scrub.c 3140-3165 (:88-89) vs S242's
  SOURCES.md anchor "lines 3140-3162"; SR8 sysfs windows 70-76 / 2019-2050 / 2108-2116 (:92-93) vs
  S243 anchor "72-74, 2021-2049, 2113". Counter windows are supersets; the frozen ROWS are the
  authority and the entry quotes sit inside both. No action needed; noted so a future reader does
  not treat the registry prose as the window source.
- **F7 (info) — used-by is exact-token membership** after splitting on `[,;]` (:323-324, :330-331):
  a cell like "…r44.md and others" would fail a good row. Currently green; brittleness only.

## 4. Residual risk and verification gaps

- The residual-reviewer binding path (K19: partly + bound residual holds) was not rebuilt by this
  seat; I verified its fail-closed logic at :303-308 and rely on the pre-data K19 receipt.
- F5 was established by reading, not by a fixture run.
- `transcript_has` (:228-238) is a host-local substring search; the declaration already records that
  committed bytes cannot distinguish forged orchestrator records (C2-K3), and my F3 shows the
  complement: in a baseless repo the novelty/newness guarantees are vacuous too.
- I did not test QUOTE_RE edge cases beyond F1 (inner quotes, backtick variants).
- No lane tracked file was touched; writes were limited to this report, the receipt directory
  `.ufo/waves/round-44/w1/C2RevCounter/`, and scratch under `/fast/scratch/hyaku/tsukuroi-r44/C2RevCounter-6/`
  (removed after copying receipts). No tools were installed (system python3/git only). Scratch
  fixtures used `user.name=fixture <fixture@invalid>` and `git clone --shared`; toplevel asserted
  before every commit.
