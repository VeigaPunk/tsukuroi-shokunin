# RevRowQ02 — per-row review of C1 row Q02 at f3a5723a988bf1c2835985880e7a38d477462cd0

Verdict: holds — the Q02 quote is verbatim at its cited line in the re-fetched pinned snapshot, every clause of the JSON statement, the SKILL line and the decision-table/note rows is supported by the cited source lines with no lost branch and no unearned hedge, both parts of the frozen question are answered, and the fact is novel against base 2077e2fa.

All source line numbers below are lines of the re-fetched bytes `btrfs-rescue-v71.rst` (sha256 `838504fe8b00d221e017457e7953717f3ca2a0e886a48a4c457367b8c4063a1d`), saved under `.ufo/waves/round-31/w2/RevRowQ02/`.

## Findings

1. [obs] Pin integrity, re-opened myself: SOURCES row S165 (`corpus/SOURCES.md:259` at f3a5723a) names `https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-rescue.rst` with sha256 `838504fe8b00d221e017457e7953717f3ca2a0e886a48a4c457367b8c4063a1d`, status cell 9 `mined`. `curl -sL` returned HTTP 200 and `sha256sum` of the fetched bytes equals the pin exactly; the committed snapshot `.ufo/waves/round-31/w1/ScribeSrcRescue/btrfs-rescue.rst` at f3a5723a hashes to the same digest (`git show … | sha256sum` → same), and the counter pin agrees (`tools/check-btrfs-repair-r31.py:66` at REV). raw.githubusercontent.com answered directly; no kernel.org fallback needed.

2. [obs] Quote verbatim at the cited line: `sed -n '149p' btrfs-rescue-v71.rst | grep -cF 'If the errors are like above, then :command:`zero-log` should be used to clear'` prints `1`; the line holds 13 words (inside the 6–25 rule). The Q02 row (`corpus/knowledge/btrfs-repair-r31.json`, id Q02) cites line 149 and this exact string.

3. [obs] JSON statement, clause by clause (fetched btrfs-rescue.rst):
   - "mount fails during log replay" ← line 126-127: "This command will clear the filesystem log tree. This may fix a specific / set of problem when the filesystem mount fails during log replay. See below".
   - "kernel backtrace" ← line 136: "One can determine whether :command:`zero-log` is needed according to the kernel"; sample frames lines 141-147, `open_ctree` at 147.
   - "backtrace shows open_ctree plus function names containing replay, recover, or log_tree" ← lines 150-152: "the log and the filesystem may be mounted normally again. The keywords to look / for are 'open_ctree' which says that it's during mount and function names" (continuing "*replay*, *recover* or *log_tree*" on 152). The row keeps open_ctree separate from the three name keywords, as the source does.
   - "zero-log should clear the log" ← line 149 verbatim (finding 2); "should" preserved, no "will"/"always".
   - "may then mount normally" ← line 150: "the log and the filesystem may be mounted normally again."; "may" preserved.
   - "may lose changes made since the last transaction commit—up to 30 seconds at the default commit period, or less when other filesystem activity implied a commit" ← lines 131-134: "Clearing the log may lead to loss of changes that were made / since the last transaction commit. This may be up to 30 seconds / (default commit period) or less if the commit was implied by / other filesystem activity."; "may", "up to" and the less-branch all preserved.
   No lost branch: the only other content in 123-152 (synopsis "Clear the filesystem log tree." at 124, and the sample frames) is carried by the note rows (finding 5). No "only"/"always" the source lacks: the row stays conditional and hedged exactly as the source.

4. [obs] SKILL line (`SKILL.md:2681` at f3a5723a, the only `^| [R31-Q02] ` line at REV, `grep -c` → 1) is supported by the same lines: trigger from 126-127/136/150-152, "Use zero-log to clear the log tree" from 123-124/149, "may mount normally again" from 150, loss bound from 131-134. It answers both parts of the frozen question ("When does btrfs rescue zero-log apply after a failed mount" ← trigger clauses; "and what does it lose" ← loss clause).

5. [obs] Decision-table row (`corpus/knowledge/btrfs-repair-r31.md:13`, cites `btrfs-rescue.rst:123-152` (S165)) and the three error-pattern rows (`btrfs-rescue.rst:141-152` open_ctree/keyword reading; `:136-152` sample-frame decision; `:123-134` clear-plus-loss) each map onto the fetched lines: frames and keywords at 141-152, decision sentence at 136-152, clear-and-loss at 123-134. Frame names `replay_one_dir_item`, `walk_log_tree`, `btrfs_recover_log_trees` named in the note row appear in the fetched code block (141-147).

6. [obs] SOURCES contract: at REV exactly one S165 row, status `mined`, containing the frozen URL and full sha256 (checked at `corpus/SOURCES.md:259`); at BASE 2077e2fa `corpus/SOURCES.md` has no S165 and no btrfs-rescue row at all (grep over the dumped BASE file → no matches).

7. [obs] Novelty at BASE 2077e2fa (`git grep -n -i -F` over SKILL.md, PROVINCE.md, corpus/, 8 synonym groups): `zero-log` 0 hits; `zero log` only `corpus/lessons/round-19-verifier-spotcheck.md:150` "Zero logged events is not proof of zero writes" — an unrelated audit-log idiom that does not contain the hyphenated frozen token; `log tree`/`log-tree`/`log_tree` 0 hits; `log replay`/`open_ctree` 0 hits; broad `recover`/`rescue` hits are initramfs/systemd-rescue-shell/package-recovery contexts (e.g. S026 rescue shell, boot recovery, `omarchy-recover-*` units) holding a different fact; `transaction commit`/`mount fails`/`clear the log` hits are the device-stats plane (S132, `storage-health-r26.*`) — again a different fact. No btrfs log-repair or zero-log knowledge is held anywhere at base; the row's fact is new.

8. [obs] Minor wording notes, not defects: (a) the SKILL line cites "S165 lines 126-152" while the decision row and SOURCES cite 123-152 — both ranges contain every supporting sentence (heading 123-124, body 126-152); (b) the JSON statement reads "zero-log should clear the log" where the source says "should be used to clear the log" (149) — the md decision row keeps the normative form ("the documentation says to use it when the errors are like the sample"), and the JSON retains "should" plus the "may" hedge, so no overclaim.

## Residual risk and verification gaps

- [inf] Novelty is established textually (git grep, 8 synonym groups); a semantically equivalent base fact worded with none of these synonyms would not be caught by grep. The broad recover/rescue/transaction-commit sweeps found no such fact, so the risk is low.
- [unk] Whether the sealed answer-key words are the best possible summary of this source — out of scope for this review; I did not attempt key recovery and printed no keys.
- I did not re-run the frozen counter (per-row judgment scope; the counter's own receipts are separate wave evidence). lsp device not applicable: targets are RST/markdown and git history, no language server; text git grep is the prescribed and used method.

Scope: read=lane f3a5723a corpus/knowledge/btrfs-repair-r31.json + .md + SKILL.md:2681 + corpus/SOURCES.md at REV and 2077e2fa + tools/check-btrfs-repair-r31.py; fetched btrfs-progs v7.1 Documentation/btrfs-rescue.rst (pin-matched, saved under .ufo/waves/round-31/w2/RevRowQ02/); wrote=.ufo/waves/round-31/w2/RevRowQ02.md, .ufo/waves/round-31/w2/RevRowQ02/{btrfs-rescue-v71.rst,rows-r31.json,SOURCES-r31.md,SOURCES-base.md}; executed=curl -sL fetch + sha256sum, sed -n/grep -cF quote checks, git grep -i novelty sweeps at 2077e2fa, read-only git show dumps
Model: zai/glm-5.3-flash
Installs: none
