# E5MarkerAudit — scoped findings (round 76 w1, C2 item 5 marker audit)

**Verdict:** the seven carried wave markers exist, are regular files, are untracked at base `865b38c9` (`git cat-file -e` fails for each, as required), and contain only wave-runner bookkeeping. **Classification: runtime markers, safe to commit as wave evidence.** No lane file was modified.

| path | bytes | sha256 | regular | absent-at-base |
|---|---|---|---|---|
| .ufo/waves/round-66/w1.ready.dispatched | 345 | b03da1df2522bcb6053a877f87bc5733bf23f69c758117dcf3c1fb5d63b34df2 | yes | OK |
| .ufo/waves/round-67/w1.ready.dispatched | 309 | eef188c54705f382d7343f1f1bd3fb546b5ab5c067a9c137d2ab57e1da334ea5 | yes | OK |
| .ufo/waves/round-73/w1-run.stderr | 0 | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 | yes | OK |
| .ufo/waves/round-73/w1.ready.dispatched | 355 | 9ce3ddf52142cac9707d38e257c5858b32c1a6b090df4c683bc30fc3c63970c5 | yes | OK |
| .ufo/waves/round-74/w1.ready.dispatched | 362 | 52e47c51026c84c05b2cf02ad06de5b262d5e7a087e2242df027e3d8683b4dfd | yes | OK |
| .ufo/waves/round-75/w1.ready | 160 | ba3e6c471eabc17e96a587d86b9e3f7f8a2af4418f247944e618f24c42c9873e | yes | OK |
| .ufo/waves/round-75/w1.ready.dispatched | 363 | bc73b5cd906730b3ab1b437573265c0f707489616a5b285b064f0286801a8863 | yes | OK |

Round-76 runtime markers at audit close: `w1.ready` (169 B, `0f100b89c5338d2a77376d2bb49447be6c6098263dc33448965e314368c9d945`) and `w1.ready.dispatched` (393 B, `d8ea5f8735b25d4c852e582785f331774bbebabba1c5e01f0d4d7472c2f04824`) exist, regular, absent-at-base. `w1-results.json` does **not** exist yet (wave in flight); re-check before the C2 commit.

Safety: contents are timestamp + seat→agent-id maps or `lane/round/wave/dispatch/l1` JSON; no credentials; no absolute path outside the fleet root (the `dispatch` fields point inside the lane root); nothing near 1 MiB.

Surprises: (1) `round-73/w1-run.stderr` is empty — valid to commit, but the C2 checker must not assume non-empty content; (2) `w1.ready` files embed absolute dispatch paths inside the fleet root — compliant with the stated rule, would trip any stricter no-absolute-paths rule; (3) `w1-results.json` absence is expected mid-wave, recorded explicitly.

Full evidence: `.ufo/waves/round-76/w1/E5MarkerAudit/markers.txt` and `.../report.md`.
