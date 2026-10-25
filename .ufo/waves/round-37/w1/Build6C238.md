# Build6C238 — C2 `-n` three-state fixture

## Axes and deliverable
- **Operability:** standalone Python stdlib check, lane root argument, no subprocess/live-journal dependency, no lane writes.
- **C2 depth:** validates the measured distinction between rejection, normal work, and allowed-but-output-altered behavior.
- **Calibration:** receipt metrics are checked against the note's named cells rather than accepting a generic success claim.

Runnable check: `.ufo/waves/round-37/w1/Build6C238/check-c2-n-three-state.py`.

Run from a checkout with its round-36 files available:

```sh
python3 .ufo/waves/round-37/w1/Build6C238/check-c2-n-three-state.py /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
```

Exit 1 means either required matrix cells are absent/inconsistent or the note does not classify and cite the three-state evidence. Exit 0 means note and captured evidence satisfy the fixture. It does not contact journalctl or mutate any path.

## Exact retained evidence
Opened this round:
- `.ufo/waves/round-36/w1/ScribeC2Draft/journalctl-v262-field-filter-r36.md:19-48`. It defines only `REJECT` / `WORK` at lines 21-23; line 41 classifies `-n` as `WORK`, and line 48 says `-F -n 1` succeeds without stating the field-list truncation.
- `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json:24-47`: `core_plain` runs `journalctl --no-pager -F PRIORITY`, exit 0, stderr 0, stdout 12 bytes, six values.
- Same matrix `:170-194`: `ext_plain_N` runs `journalctl --no-pager -N`, exit 0, stdout 2882 bytes, SHA-256 `3480f2aac48ee794f741dfd7dbffa31c86d933df70482db14adf5e57dfc2f20a`.
- Same matrix `:486-504`: `ext_lines1_F` runs `journalctl --no-pager -n 1 -F PRIORITY`, exit 0, stderr 0, stdout 2 bytes, one value (`5`), SHA-256 `f0b5c2c2211c8d67ed15e75e656c7862d086e9245420892a7de62cd9ec582a06`.
- Same matrix `:507-533`: `ext_lines1_N` runs `journalctl --no-pager -n 1 -N`, exit 0, stdout 2882 bytes, same SHA-256 as `ext_plain_N`.
- `.ufo/waves/round-36/w2/W2RevC2/review.md:34-62` independently describes the missing third state and recommends `WORK-ALTERED`, while distinguishing `-F` truncation from unchanged `-N` output.

## Expected baseline failure and after-state
**Unchanged baseline:** this check is expected to exit 1 on the opened round-36 note, because it has no `WORK-ALTERED` verdict and does not state the 12-byte versus 2-byte `-F` comparison. Even if the table is described elsewhere, it must cite all four cells and retain the equal 2882-byte/SHA `-N` control. This expected failure is a static prediction from the inspected note and check predicates; I did not execute the check.

**After state measured:** the same lane's immutable matrix remains source of measurements; a corrected note must distinctly identify `REJECT`, `WORK`, and `WORK-ALTERED`, cite `core_plain`, `ext_lines1_F`, `ext_plain_N`, `ext_lines1_N`, and state the measured counts: six values/12 bytes to one value/2 bytes for `-F`; 2882 bytes with identical digest for both `-N` runs. The fixture validates those criteria and fails closed on missing cells or altered receipt metrics. It does not verify journalctl behavior beyond these saved receipts.

## Scope / checks
Only the assigned seat script and this report were written. No lane/source/fleet/sibling file or VCS state was changed; no git/jj writes, package manager, tool installs, live journal commands, or verification runs were performed. No external sources were needed or cited.

**Risks:** note-only checks can be satisfied by placing required terms/cell names outside the relevant table unless maintained carefully. Current fixture checks presence and receipt consistency but does not parse Markdown table row semantics. Matrix input is a frozen receipt and cannot show that current host behavior still matches it.
