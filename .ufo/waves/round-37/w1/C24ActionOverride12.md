# C24ActionOverride12 — C2 falsification item 4/8: action-override classification

Seat: `C24ActionOverride12` (scribe, L2 leaf) · round 37 wave 1 · milestone "C2 counter attack" · axes: depth, `C2:action-override classification`.
Assignment: attack the declared C2 correction requirement "action-override classification": read the r36 verifier spot-check and the current r36 note/source; decide whether the target is precise and testable; propose concrete should-pass / should-fail cases; do NOT author the change.

## Method & lane bounds obeyed

- Leaf member: no subagent dispatch, no delegation, no campaign tools.
- No writes to lane/fleet/sibling repos, no git/jj mutation, no pacman/net host changes, no tool installs (`~/.omp/agent/RULES.md` read 2026-10-25; nothing was installed/updated — channel/reason not applicable).
- Live probes are read-only `journalctl` queries on this host (same class as the r36 closure's spot-cells); scratch kept in `/tmp/c24act/` only; the only lane write is this report.

## Sources opened this round (all accessed 2026-10-25)

| # | Source | What was located |
|---|---|---|
| S1 | `/home/vgpnk/.omp/agent/RULES.md` (local) | tooling authorization; no install needed |
| S2 | `.ufo/waves/round-37/w1-spec.json` (local) | seat prompt item 4/8 |
| S3 | `corpus/lessons/round-36-verifier-spotcheck.md` (local) | §2 C2 re-measure; §6 item 2 (line 103): "**C2 note corrections** (W2CritC2Depth blocking items): … action-override classification. Recorded, still unapplied."; line 65: "action-override classification) are recorded but **not yet applied** — routed below" |
| S4 | `.ufo/waves/round-36/w2/W2CritC2Depth/W2CritC2Depth.md` (local) | line 5: "… and `--list-boots` is an action override, not working field enumeration." |
| S5 | `corpus/knowledge/journalctl-v262-field-filter-r36.md` (local) | line 17 (guard description), line 44 (attacked table row), line 126 ("the 16-term limiting-option predicate") |
| S6 | `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json` (local) | cell `live_list_boots` (lines 1017-1032): argv `["journalctl","--no-pager","-F","PRIORITY","--list-boots"]`, exit 0, stdout 541 B, verdict "OK"; `live_show_cursor` (1034-1050), `live_merge` (1051-1067) |
| S7 | systemd v262 `src/journal/journalctl.c` — `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c`, fetched bytes sha256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` (matches the note's pin) | L801-814 option→action map; L953-956 extraneous guard; L958-960 scope-rejection guard; L962-965 `--merge` conflict |
| S8 | systemd v262 `src/journal/journalctl-filter.c` — `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl-filter.c`, fetched bytes sha256 `480f7a03040c0ddc93b1b65c0b49d6f0e8a4a377ee1b94168655132dcfd72f48` (matches the note's pin) | L26-43: `field_list_has_scope_options()` = exactly 15 terms |

No source was cited that was not opened this round.

## The declared correction requirement (verbatim anchors)

- S4 line 5: "… and `--list-boots` is an action override, not working field enumeration. Correct the overbroad prior-state wording as well."
- S3 §6 item 2: "action-override classification" among the three blocking C2 note corrections (15 predicate terms; `-F` vs `-N` under `-n`; action-override classification).
- The attacked note row (S5 line 44):
  `| not a limiter | \`--boot=all\`; \`--list-boots\`; \`--show-cursor\`; \`--merge\` | **WORK** | \`live_boot_all\` …, \`live_list_boots\`, \`live_show_cursor\`, \`live_merge\` |`

## Precision assessment

- The **negative** claim is precise: the note's one "not a limiter" row groups `--list-boots` with options that genuinely modify field enumeration (`--show-cursor`, `--merge`, `--boot=all`) and asserts all of them WORK with `-F`/`-N`. That grouping is false: `--list-boots` selects a different journalctl *action* (`ACTION_LIST_BOOTS`), so `-F`/`-N` combined with it is not field enumeration at all.
- The **positive** requirement is under-specified: the critique does not state (a) the corrected table shape (new "action override" row? which cells?), (b) the expected combined exit codes or output semantics, (c) that behavior is argv-*order-dependent*, (d) the separate `--list-boots` + `--merge` conflict (exit 1, distinct 60-byte message, `journalctl.c:962-965`) that a corrected row must record. A counter built only from the critique text would not know what to assert.
- Conclusion: **target is directionally precise but not yet fully specified; it is fully testable** — deterministic on systemd 262, order-contingent, machine-checkable via exit codes plus stdout byte-equality against baselines.

## Empirical results (live, read-only; systemd 262 (262-1-arch), 2026-10-25)

| probe | argv (all with `--no-pager`) | rc | stdout | stderr | meaning |
|---|---|---|---|---|---|
| A | `-F PRIORITY` | 0 | 12 B sha `97477348840c310c` (values 2 4 5 6 7 3) | 0 | field-value baseline |
| E | `--list-boots` | 0 | 262 B sha `979cd33fdd5af4ec` (boot table) | 0 | boot-list baseline |
| B | `-F PRIORITY --list-boots` | 0 | 262 B, sha IDENTICAL to E | 0 | `-F` silently swallowed → boot list. **Exact argv of matrix cell `live_list_boots`** |
| C | `--list-boots -F PRIORITY` | 0 | 12 B, sha IDENTICAL to A | 0 | `--list-boots` swallowed → field list |
| D | `--list-boots -N` | 0 | 2735 B, sha identical to K (`-N` alone) | 0 | field-names list |
| F | `--list-boots --merge` | 1 | 0 | 60 B: `Using --boot or --list-boots with --merge is not supported.` | third error class |
| G | `--list-boots --merge -F PRIORITY` | 0 | 12 B, sha = A | 0 | `-F` overwrites action; merge conflict masked |
| H | `--merge -F PRIORITY` | 0 | 12 B, sha = A | 0 | true modifier (contrast F/G) |
| I | `-b 0 -F PRIORITY` | 1 | 0 | 84 B scope-rejection line (re-confirmed byte-for-byte) | limiter+`-F` rejects |
| J | `-b 0 -F PRIORITY --list-boots` | 0 | 262 B, sha = E | 0 | limiter+`-F` exits 0 because `--list-boots` wins the action |
| K | `-N` | 0 | 2735 B sha `7991f1df402d9d9a` | 0 | field-names baseline |
| L | `-F PRIORITY --show-cursor` | 0 | 12 B, sha = A | 0 | true modifier |

Key facts established:
1. `-F`/`-N` and `--list-boots` each write `arg_action`; the **last** action option in argv wins (`journalctl.c:801-814`). The scope guard runs once after full parse (`journalctl.c:958-960`), so it sees only the final action → order-dependence.
2. Combined invocations are *silent* overrides: B≡E, C≡A, D≡K byte-identical. Neither the `-F` nor the `--list-boots` semantics survive; the output is whichever action came last.
3. `--list-boots` has its own conflict: +`--merge` → exit 1, 60 stderr bytes (`journalctl.c:962-965`), which `-F` placed after can even mask (G).
4. The matrix's own cell `live_list_boots` (= B) recorded exit 0 with stdout 541 B (content has since changed; shape same) and verdict "OK" — i.e. the note's evidence *is* the misclassified case: it is a boot list, not field enumeration.

## Proposed test vectors

**Should-pass** (a corrected note/counter must satisfy these):
- SP1 `journalctl --no-pager -F PRIORITY --list-boots` exits 0 AND stdout sha256 == `journalctl --no-pager --list-boots` stdout sha256 (proves `-F` overridden; row must not call this "working field enumeration").
- SP2 `journalctl --no-pager --list-boots -F PRIORITY` exits 0 AND stdout sha256 == `journalctl --no-pager -F PRIORITY` stdout sha256 (proves `--list-boots` overridden).
- SP3 `journalctl --no-pager --list-boots -N` exits 0 AND stdout sha256 == `journalctl --no-pager -N` stdout sha256.
- SP4 `journalctl --no-pager --list-boots --merge` exits 1 AND stderr == `Using --boot or --list-boots with --merge is not supported.` (60 bytes) — the action-override row must record this separate interaction.
- SP5 `journalctl --no-pager -F PRIORITY --show-cursor` and `--merge -F PRIORITY` exit 0 with stdout sha256 == plain `-F` (these genuinely are modifiers; discriminates the two classes).
- SP6 (text) the note contains no sentence classifying `--list-boots` as a "limiter" or implying `-F`+`--list-boots` performs field enumeration.

**Should-fail** (would falsify the current note row or any attempted fix):
- SF1 `--list-boots -F PRIORITY` exits non-zero or prints the 84-byte scope-rejection (would mean `--list-boots` IS a limiter — contradicts both note and critique).
- SF2 `-F PRIORITY --list-boots` stdout ≠ boot-list baseline (breaks override model).
- SF3 `--list-boots -F PRIORITY` stdout ≠ field-list baseline (breaks override model).
- SF4 `--list-boots --merge` exits 0, or exits 1 with any other stderr (contradicts `journalctl.c:962-965`).
- SF5 `--list-boots --merge -F PRIORITY` exits non-zero (currently masks; if it started rejecting, the note must document it).
- SF6 `-b 0 -F PRIORITY --list-boots` exits non-zero or stdout ≠ boot-list baseline (a naive "limiter+`-F` ⇒ reject" rule fails here; keep as tripwire).
- SF7 (counter-implementation) a check that only asserts exit codes cannot certify this correction: `--list-boots`±`-F` both exit 0 — the counter must assert output **equality/type**, not exit codes. Vector: run the candidate counter against the current uncorrected note → it MUST fail.

## Exact anchors

- Guard: `journalctl.c:958-960` (IN_SET + `field_list_has_scope_options()`), `journalctl-filter.c:26-43` (15 terms).
- Extraneous-arguments guard: `journalctl.c:953-956`; `--merge` conflict: `journalctl.c:962-965`.
- Option→action map: `journalctl.c:801` (`-N`→`ACTION_LIST_FIELD_NAMES`), `805` (`-F`→`ACTION_LIST_FIELDS`+`arg_field`), `812` (`--list-boots`→`ACTION_LIST_BOOTS`).
- Note row attacked: `journalctl-v262-field-filter-r36.md:44`; note guard text line 17; note "16-term" source line 126 (factually 15).
- Critique: `W2CritC2Depth.md:5`; spot-check §6 item 2 (`round-36-verifier-spotcheck.md:103`) and line 65.
- Declared After-state/counter (not yet built): `SCORECARD.md:1909-1916` — "an action-override classification row"; counter `tools/check-journalctl-v262-corrections.py` **does not exist** at tip (glob: path not found).

## Out-of-scope / limits

- I did not author the correction; no change proposed beyond test vectors.
- The other two C2 corrections (15-vs-16 predicate terms; `-F`/`-N` under `-n`) are out of scope; the 15-term count was verified in passing (S8).
- Byte counts of boot/field lists are journal-content-dependent (r36 matrix's 541 B vs 262 B today); all equality claims are within-run sha256 comparisons.
- Host = systemd 262 (262-1-arch); claims hold for this version only (as in the note).

## Final answer

C2 action-override target: precise as a negative claim (the note's row 44 misclassifies `--list-boots`), under-specified positively (no corrected row shape, no expected semantics), and fully testable — it is order-dependent and silently overrides, proven live: `-F PRIORITY --list-boots` ≡ boot list, `--list-boots -F PRIORITY` ≡ field list (byte-identical stdout), plus a separate 60-byte `--merge` conflict. The note's own evidence cell (`live_list_boots`) is the misclassified case (exit 0, boot-list output, verdict "OK"). Should-pass SP1-SP6 and should-fail SF1-SF7 above define the correction's acceptance; any counter must assert output equality/type, not exit codes. Sources S1-S8 opened this round, all quoted/located; no tool installs, no lane writes beyond this seat report.
