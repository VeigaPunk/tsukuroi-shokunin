# R2Reviewer — round-74 w1 — C2 routed-repair + instrument-digest attacks (scoped summary)

Basis: declaration `e51fb49d`, base `d749a625`, tip read `810daf13`. Full report + receipts:
`.ufo/waves/round-74/w1/R2Reviewer/report.md` (battery.py, battery-out.txt, fixtures/cli-g1-append-eof,
fixtures/cli-g2-insert-before, selftest-counter.txt, selftest-checker.txt). No repo bytes mutated.

## Findings by severity

1. **HIGH — the prescribed C2 repair shape cannot close LOG item 2.** `check_r73_log_count` takes the
   FIRST block matching the id or the fallback ("Round 73"+"correction"+"selftest"); LOG.md's Round 73
   entry block already matches the fallback, lacks `14`, and is the file's last block — so a headed
   correction appended at EOF (the spot-check §6.2 shape: "Append one naming the superseded counts") is
   never read. CLI receipt: appended-at-EOF fixture → `ROUTED_STALE=1 ROUTED_OK=1/2` rc 1. Only
   non-append shapes pass: block inserted immediately before the Round 73 entry (CLI fixture →
   `ROUTED_STALE=0 ROUTED_OK=2/2` rc 0) or an unheaded correction paragraph appended inside that block.
   Frozen C2 target is unreachable by the prescribed shape; land G3/G2 or amend the instrument with an
   erratum written before the repair commit.
2. **MEDIUM — LOG item passes without naming R73-LOG-COUNT-STALE** (fallback clause suffices); C2 wording
   requires the name.
3. **MEDIUM — bare-substring tokens:** `install.c:23831`/`12387`/`:368-3700`/`:237-2380`/`:238-2390` pass
   item 1; finals written as `1314` pass item 2's `13` and `14`. The r73 checker's whole-token bar did
   not carry over.
4. **MEDIUM — no direction/verb/attribution check:** a block stating the correction is REJECTED (tokens
   as rejected claims) passes; "final counts are 12 and 11; 13 and 14 were wrong" passes; attributing
   13/14 to the round-74 instruments passes — counts are never bound to tool names or digests
   `1f22c26b…`/`ad853877…` by this instrument.
5. **MEDIUM — first-match shadowing also falsifies item 1:** an earlier lesson block merely mentioning
   the id makes a later valid appended correction fail (L8, stale=1). EOF append works today (control
   0/2); do not mention the id above the correction.
6. **LOW — placement/sentence-ness unenforced (item 1):** id+tokens inside the unrelated Gate section
   pass with no correction block; a bare comma token list passes (r73 F1/F6 vacuity class regressed).

Omission semantics hold (negative results): drafts omitting `install.c:2383`, the superseded `2387`,
S304 anchors, superseded 12/11, or finals 13/14 all FAIL as claimed; absent blocks are stale.

## Instrument-digest claim — VERIFIED
`count-ul-rows-r73.py` `1f22c26b95c52be745a8cdd97ec52ebf06a362f697daf2a8e1e0d77e28f3e643` (tip =
declaration), selftest PASS 13 cases rc 0 (fresh TMPDIR; refuses /tmp by design, rc 2);
`check-r72-routed-r73.py` `ad853877bd4d5117d0ee356f346f3bf515c0b064fd1e9ed8bc670ac97295a281`,
selftest PASS 14 cases rc 0. Both round-74 instruments byte-frozen mid-wave (`2da4ff1f…`,
`94d46a5e…`). SCORECARD.md:6039-6040 and corpus/README.md:685-686 digests match committed bytes.

## Live state
`ROUTED_STALE=2 ROUTED_OK=0/2` rc 1 at tip and at the declaration commit; both corrections still owed.
