VERDICT: supports

# F-13 — re-open S239 (own-work host capture)

Seat SrcReopenS239, tsukuroi lane round 42, wave w2. Scope: sha256 of
`.ufo/waves/round-42/frozen/hostcap/capture.txt` vs the row, re-run of `capture.sh` into scratch
with diff, the S239 `teaches` cell vs the capture lines, and whether any C2 rule row rests on
S239 alone (QUALITY 86). No tools were installed or upgraded (none needed; operator rule
2026-10-19 record: zero installs). Lane untouched except this report and the receipts named at
the end; all work in `/fast/scratch/hyaku/tsukuroi-r42/SrcReopenS239/` (removed at finish).

## 1. sha256 of capture.txt vs the row — MATCH

- `sha256sum .ufo/waves/round-42/frozen/hostcap/capture.txt` →
  `942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c` (340 bytes, 10 lines;
  `wc -l` = 10).
- The row pins the same digest: `corpus/SOURCES.md:248` — "capture.txt (sha256
  942edc91a6b8fcda3ef29e88c3d54e7a9a48ec4cce302b8c1edcc89c8710643c), captured
  2026-10-26T19:13:44Z, unprivileged".
- The entry pins it too: `corpus/knowledge/btrfs-scrub-record-r42.md:1`; and the counter:
  `tools/check-scrub-record-r42.py:52-53` (`CAPTURE` tuple, same digest).
- Frozen file is the committed content: `git -C <lane> status --porcelain -- .ufo/waves/round-42/frozen/hostcap/`
  → empty (clean); `git log --format='%h %H' -1 -- .ufo/waves/round-42/frozen/hostcap/capture.txt`
  → `a84fc9de a84fc9dec860f8bea516dff7ddfdc98223cdae52`, i.e. last touched by the declared freeze
  commit itself.

## 2. Re-run capture.sh into scratch — reproduces modulo the timestamp line

- Command: `bash .ufo/waves/round-42/frozen/hostcap/capture.sh $S/rerun.txt` (scratch
  `/fast/scratch/hyaku/tsukuroi-r42/SrcReopenS239`, TMPDIR set there), exit 0.
- `diff frozen/capture.txt rerun.txt` → exactly one hunk, line 1 only:
  `captured_utc 2026-10-26T19:13:44Z` vs `captured_utc 2026-10-26T20:47:21Z` (diff exit 1).
  Lines 2–10 are byte-identical; rerun sha256
  `d19259ac7a1bcbaba0cb2b4440f16738a2866d47f9cbb7afb3a7ee3d3804068b` differs solely because of
  that line (receipt `receipt-reopen.txt`).
- The nine substantive readings reproduce: kernel `7.2.11-arch1-1`, btrfs-progs `7.1-1`,
  root btrfs / fsid `1d02a454-c549-4a35-b567-89d60902af8e`, `/var/lib/btrfs` absent, 0 scrub
  timers listed, `btrfs-scrub@.timer disabled disabled`, `scrub_speed_max …/devinfo/1 0`,
  `journal_scrub_lines 0`.
- Script is unprivileged and read-only by inspection (capture.sh:1-23): writes only its `$1`
  output; queries `pacman -Q`, `findmnt`, `systemctl list-timers/list-unit-files`, a sysfs
  `cat`, and `journalctl -k -b 0 --no-pager`; no scrub start/cancel, no write outside `$1`.

## 3. `teaches` cell vs the capture lines — all four claims backed

`corpus/SOURCES.md:248` teaches cell: "No /var/lib/btrfs directory, the scrub timer disabled,
the root device limit 0 and no kernel scrub line in the current boot". Frozen capture lines
(numbered from `read` of the file, 10 lines total):

| teaches claim | capture line | content |
|---|---|---|
| No /var/lib/btrfs directory | capture.txt:6 | `var_lib_btrfs absent` |
| the scrub timer disabled | capture.txt:8 | `scrub_timer_unit_file btrfs-scrub@.timer disabled disabled` (state column `disabled`; corroborated by :7 `scrub_timers_listed 0`) |
| the root device limit 0 | capture.txt:9 | `scrub_speed_max 1d02a454-c549-4a35-b567-89d60902af8e/devinfo/1 0` — devid 1 of the root fsid, which matches :5 `root_fsid …` |
| no kernel scrub line in the current boot | capture.txt:10 | `journal_scrub_lines 0` (grep `'scrub: (started|finished)'` over `journalctl -k -b 0`, capture.sh:20) |

No overclaim found: the row's scope column says "at capture time" (SOURCES.md:248), and the
entry's own Limits section concedes the readings "cannot show that no scrub ever ran"
(btrfs-scrub-record-r42.md:160, SC3 limit).

## 4. QUALITY 86 — no C2 rule row rests on S239 alone

- Mechanical tally over `corpus/knowledge/btrfs-scrub-record-r42.md`:
  `grep -c '^\*\*Quote\.\*\* `S237`'` → 25; `` `S238` `` → 3; `` `S239` `` → 0; total Quote
  lines 28. Per row: SC1 6×S237 (:30-35), SC2 5×S237 (:53-57), SC3 5×S237 (:72-76), SC4
  7×S237 (:104-110,110-112), SC5 2×S237 + 3×S238 (:132-136,136-138). S239 never appears as a
  quote source; it appears only in the five `**Host reading.**` paragraphs (:39-40, :62, :86-88,
  :118, :140), citing capture.txt lines 5-10 — all within 1..10 and each content-correct
  against the frozen capture (section 3 mapping).
- Kinds agree: S237 `code` (SOURCES.md:246), S238 `docs` (SOURCES.md:247), S239 `own-work`
  (SOURCES.md:248) — exactly the QUALITY 86 wording ("every row cites S237 or S238
  (kind `code`/`docs`); S239 (`own-work`) carries only the host readings",
  btrfs-scrub-record-r42.md:165-166).
- The counter structurally forbids a S239-only rule row: `QUOTE_RE`
  (check-scrub-record-r42.py:62) accepts only `scrub\.c|CHANGES` files, and snapshots are
  loaded only for `scrub.c`/`CHANGES` (:46-49), so a row quoting only S239 would score
  `quotes_ok` false; the predicate needs `quotes_ok == 5` (:240). S239's only channel is
  `host_ok >= 3`.
- The capture digest is enforced transitively: on sha mismatch `cap = None` (:137-139), and
  `h_ok` conjoins `cap` (:195), so `host_ok` drops to 0 → FAIL. `capture_ok` reported true at
  HEAD (section 5).

## 5. Counter cross-check at HEAD (read-only, no writes to the lane)

`python3 tools/check-scrub-record-r42.py --revision HEAD` (exit 1, receipt
`SrcReopenS239/counter-at-HEAD.json`): revision `a968393c678171f8a5a2907da5015735396da4cc`,
`capture_ok: true`, `snapshots_ok: true`, `rows: 5`, `quotes_ok: 5`, `novelty_ok: 5`,
`host_ok: 5`, `sources_ok: 1` (`S237: true, S238: true`), `verdicts_ok: 0`, `verdict: FAIL`.
The FAIL leg is `verdicts_ok` only: the ten row-verdict seats' binding records
(`w2-dispatch.json`/`w2-results.json` + committed reports) are not committed at HEAD yet —
expected mid-wave; every content leg relevant to S239 passes.

## What I did not do

- Did not re-fetch or re-verify the S237/S238 upstream snapshots against github.com (other
  seats' scope, QUALITY 79); `snapshots_ok: true` above is sha-vs-pin only.
- Did not re-run the live `btrfs scrub status /` check that SC4's host paragraph cites
  (wave-1 `.ufo/waves/round-42/w1/C2ExecHostRecheck.md` §2); I verified only that the frozen
  capture supports the rest of that paragraph.
- Did not judge the ten row verdicts or the binding (the C2RevSC<n>/C2CritSC<n> seats).
- The re-run is one observation at 2026-10-26T20:47:21Z; it shows the volatile legs (journal,
  timers) still match at that instant, not stability at all future times.

## Residual risk

- The counter's host check is a declared shape gate (btrfs-scrub-record-r42.md:167, QUALITY 87
  "the lexical checks are shape gates only"): it checks the cited capture line exists and is
  non-empty (check-scrub-record-r42.py:195-196), not that the row's host sentence matches the
  line's content. All 9 references are content-correct today (section 4), but a future edit
  could renumber a reference and still pass the counter; that gap is covered only by the bound
  non-author verdicts. Declared, not a hidden defect — no action required this round.

Receipts (this seat dir): `rerun.txt`, `receipt-reopen.txt` (hashes + diff + tally),
`counter-at-HEAD.json`, `counter-at-HEAD.err` (empty, no stderr).
