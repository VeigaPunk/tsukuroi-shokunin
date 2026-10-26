VERDICT: supports

Seat ConsiderLineageVerify (L2, tsukuroi round 40 w1, item F-6). Independent re-derivation of the lineage of six counters, for the L1 to cross-check the scribe's lineage draft. Lane read at HEAD `f951f288483c1af0cef4afd458488b84cf7a2165` = `master` = `origin/master` (`git rev-parse master HEAD`, `git rev-parse origin/master`); tree clean except an untracked `corpus/lessons/round-40.md` (not mine, untouched). Every command below was run read-only from the lane root; raw outputs are in `.ufo/waves/round-40/w1/ConsiderLineageVerify/lineage-receipts.txt`.

## 1. Lineage table

`git log --format=%h -- <tool>` returns **exactly one hash per tool** — the adding commit; no later commit changed any of the six on master. Cross-checked per tool with `--follow` and `--full-history` (identical single hash each).

| Tool | Added by (full hash) | Commit (date — subject) | sha256 at adding commit | Later commits on master | sha256 at tip f951f288 |
|---|---|---|---|---|---|
| `tools/score-storage-arm-r38.py` | `7cbaeb6317cb9f7323d2619eec02db4e4da29449` | 2026-10-25 — "round-38: freeze C1/C2 counters, hook capture, before receipts and controls" | `e649bfb33ed99161dc3affdacd7fa86fa8d96e2c5bb60b2d22d6fc12a7f82218` | none | identical (`e649bfb3…`) |
| `tools/check-hook-order-r38.py` | `7cbaeb6317cb9f7323d2619eec02db4e4da29449` | same commit | `60e3635b37d5cd92f371800d8e5a22837b540e57c1c50a399bc973d4e21bd1a8` | none | identical (`60e3635b…`) |
| `tools/score-storage-hidden-r39.py` | `6a08925daa30767809eb13bb4b01448ff954d46a` | 2026-10-26 — "round-39: freeze C1/C2 counters, libalpm 54d9411 snapshots and pacman.log capture; registry rows" | `75a9e8abd3f1262e425ce1fde9e3ba4763d08cf21d0b61761719c0ebbae8f973` | none | identical (`75a9e8ab…`) |
| `tools/check-transaction-order-r39.py` | `6a08925daa30767809eb13bb4b01448ff954d46a` | same commit | `f1c97836abb50887231b82d27cd026d05b8083cefcdd713217071648b07c991e` | none | identical (`f1c97836…`) |
| `tools/score-selftest-literals-r40.py` | `a447b67b2502bae1e96fda341ae5ad32243ae524` | 2026-10-26 — "round-40: freeze C1/C2 counters, pinned sources, host capture, registry rows" | `8b06de18ca7eec1d928a0dfac8ca6930bf808bfd1f4250374ec300640f2f0159` | none | identical — **equals the declared sha** (SCORECARD.md:2303; assignment C1) |
| `tools/check-exec-environment-r40.py` | `a447b67b2502bae1e96fda341ae5ad32243ae524` | same commit | `d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d` | none | identical — **equals the declared sha** (SCORECARD.md:2304; assignment C2) |

All three freeze commits are authored by the lane identity `tsukuroi-shokunin` (detailed log output in receipts). Sizes at the adding commit (numstat): score-storage-arm-r38.py 252 lines, check-hook-order-r38.py 218, score-storage-hidden-r39.py 286, check-transaction-order-r39.py 238, score-selftest-literals-r40.py 176, check-exec-environment-r40.py 339.

Independent corroboration already in the lessons (my hashes match theirs exactly):
- round-38-verifier-spotcheck.md:52 — "`e649bfb3…` at all three [7cbaeb63, 9c9bb647, f8b4df2a]; only `7cbaeb6` touches the file. … check-hook-order `60e3635b…` at all three".
- round-39-verifier-spotcheck.md:63 — "`75a9e8ab…` at all four revisions [6a08925d, 49cc53c7, a2d7aad7, a6ca8171]; only `6a08925` touches the file".
- round-39-verifier-spotcheck.md:91 — "`f1c97836…` at both revisions [6a08925d, a2d7aad7]".

Base checks at the round-40 base `53b294a`: the four r38/r39 counters are byte-identical there (`git show 53b294a:<tool> | sha256sum` → the same four hashes); both r40 counters do not exist there (`git cat-file -e 53b294a:tools/score-selftest-literals-r40.py` → `fatal: … not in '53b294a'`, rc=128; same for check-exec-environment-r40.py). This matches "counters frozen at `a447b67b…`".

## 2. Retiring / qualifying defect per counter (corpus/lessons/round-3\*-verifier-spotcheck.md)

A sweep for the six tool names across all ten spotcheck files (rounds 30–39) matches **only** round-38-verifier-spotcheck.md and round-39-verifier-spotcheck.md (grep; rounds 30–37: zero matches). Mapping:

| Tool | Retires (defect → evidence) | Qualified by (spotcheck row) | Defects later found in it |
|---|---|---|---|
| `score-storage-arm-r38.py` | **None named in any round-3\* spotcheck** — it is the round-38 C1 instrument itself; round-37-verifier-spotcheck.md has zero matches for `(?i)storage\|hook\|Q82` (grep run 2026-10-26) | round-38-verifier-spotcheck.md:52 (bytes frozen, "only `7cbaeb6` touches the file") | Its **v1** predicate passed a fixture-gated arm and a 14-line no-open arm — `R38-QUALITY-UNREAD` (round-38.md:84; ID appears only in the round lesson, not the spotcheck); `R38-ABSENT-ROOT` concerns the frozen F06 rule it scores (round-38-verifier-spotcheck.md:63, §6.2 :174); `R38-Q82-LEAK` names the **sibling** `tools/score-storage-arm-r38-q82.py`, not this file (round-38-verifier-spotcheck.md:64, §6.1 :171; both files exist — glob) |
| `check-hook-order-r38.py` | None named (round-38 instrument) | round-38-verifier-spotcheck.md:52 ("check-hook-order `60e3635b…` at all three") | §6.3 round-38-verifier-spotcheck.md:175-178: passes a stripped entry citing only S212; survives an S-id drop from `source:`; cannot see block duplication past the next `## ` → formalized `R38-C2-COUNTER-GAPS` (round-39.md:76, citing :175-180); duplicate-folding detail at round-38.md:94 (tool :200/:205/:209). **Retired by `check-transaction-order-r39.py`** (round-39.md:88) |
| `score-storage-hidden-r39.py` | **Retires `R38-Q82-LEAK`** — round-39.md:86: "fixed-this-round \| Views are tmpfs mounts inside the child namespace, filled from stdin (`tools/score-storage-hidden-r39.py`, frozen `6a08925d`); the four leak arms ported onto `49cc53c7` all FAIL it"; prescription is round-38-verifier-spotcheck.md:171-173. Also carries the `R38-ABSENT-ROOT` hidden legs (absent-root BLOCKED leg, round-39-verifier-spotcheck.md:62; the census-side mounts cross-check landed at `49cc53c7`, round-39.md:87) | round-39-verifier-spotcheck.md:63 (frozen bytes, "only `6a08925` touches the file") and :66 (leak arms all FAIL) | `R39-FIXTURE-MONOCULTURE` (round-39.md:71; spotcheck :69 "fixture literal monoculture", §6.2 :184) and `R39-VIEW-CONTROL-UNREACHABLE` (round-39.md:72, citing the tool's `draw_view` at :97-107; that ID appears only in the round lesson, not the spotcheck) |
| `check-transaction-order-r39.py` | **Retires `R38-C2-COUNTER-GAPS`** — round-39.md:76: "Closed in the round-39 counter's rules and shown by committed controls: E1 (own-work only) 0/8 FAIL, E3 (S213 dropped) 5/8 FAIL, E4 (duplicated block) FAIL"; disposition round-39.md:88; prescription round-38-verifier-spotcheck.md:175-178 ("Any re-claim on this counter must close these gaps") | round-39-verifier-spotcheck.md:91 (frozen bytes at `6a08925d` and `a2d7aad7`) | `R39-CONTENT-UNREAD` (round-39-verifier-spotcheck.md:75 and §6.1 :180; round-39.md:70 — the counter "never reads the rule cell … reads `cells[2]` and `cells[3]` only"); host-column blindness inside `R39-HOSTCELL-INFERRED-AS-SEEN` (round-39.md:73 — `counts_ok` recomputes exactly two cells, tool :223-226; ID named at spotcheck :87) |
| `score-selftest-literals-r40.py` | **Retires `R39-FIXTURE-MONOCULTURE`** — named round-39-verifier-spotcheck.md:184 (§6.2) with the prescription "Vary device, subvolume and option literals across fixtures; freeze a one-literal arm as a should-fail control" (exactly the declared M1–M9/N1–N3 design, SCORECARD.md:2303); defect row round-39.md:71 | none yet — no round-40 spotcheck exists; the tool name has zero matches in all of corpus/lessons (grep) | — |
| `check-exec-environment-r40.py` | **Lands the round-39 spotcheck §6 item 6 debt** (round-39-verifier-spotcheck.md:191): "Residual staged propositions (NeedsTargets→stdin, `.pacnew` trigger target, scriptlet cwd, interpreter): … Land them on new rows from S219 if pursued" — covered by EX6, EX8, EX1, EX4 respectively; that debt carries **no R-id** in the spotcheck | none yet — same grep | — |

## 3. The `--all` nuance (informational, not a defect)

`git log --all --format=%h -- <tool>` shows **4 commits per tool**, not 1: the freeze commit plus three empty-description commits reachable **only** from `refs/jj/keep/*` (1001 refs total; 8 real heads). Characterization (git show -s / --numstat / merge-base / branch -a --contains):

- r39 pair: `374003de1f140fb9873ed73d12451b284e1e507e`, `5569c9ccc333215a56a46e69c16a9fc249d80889` (protocol-shokunin), `b5593f8b7a7da07d6732ebebd85a5785317938e1` (tsukuroi-shokunin) — parent `0eff65b2` (round-39 base), all 2026-10-26 02:47:11 -0300.
- r38 pair: `4d71297870a0154198ebbd554702c32408cd8c53` (tsukuroi), `77d7b8a8fdd289e042481898ceb12f2ce3b494d2`, `c50cc3ba2c434ece27ba6cf4b7e8c433330c8774` (protocol) — parent `8bd001f5` (round-38 base), all 2026-10-26 01:16:08 -0300.
- r40 pair: `689eeabb2ceedf820751db6a8efab82af5008049`, `a8f8df218c5ee6626158a29d587f79ee71821642` (protocol), `c0cb750b2f5a5a115741dc108159555583124164` (tsukuroi) — parent `53b294a` (round-40 base), all 2026-10-26 04:02:00 -0300.

All nine: empty subject, numstat all-added for the pair's files, **content sha256 identical to the frozen bytes**, `git merge-base --is-ancestor <c> master` rc=1 for all nine, `git branch -a --contains` empty for the snapshots (the freeze commits resolve to master + origin/master). I.e. they are jj working-copy snapshots of the pre-freeze state, not divergent counter variants: **no commit anywhere in the repo holds counter bytes other than the frozen ones.** The lessons' "only `<freeze>` touches the file" rows (round-38 spotcheck :52; round-39 spotcheck :63) are master-scoped and remain true; anyone re-deriving with `--all` should expect these three extra hashes per tool and check bytes, not assume divergence.

## 4. Declared-commit topology (cross-check of the frozen claims)

`git merge-base --is-ancestor` (rc 0 = ancestor): `53b294a`→`a447b67` ✓; `a447b67`→`c707e356` ✓ and `a447b67`→`bf238050` ✓ (both r40 counters frozen before the implementation commits, the lane's declared pattern); `c707e356`→`f951f288` ✓, `bf238050`→`f951f288` ✓; `7cbaeb6`→`6a08925`→`53b294a` ✓. Reference commits resolve as declared: `a447b67` "round-40: freeze C1/C2 counters…", `53b294a` "protocol-shokunin round-39 verifier spot-check…", `c707e356` "…C1 census selftest varies mount-table literals (R39-FIXTURE-MONOCULTURE)", `bf238050` "…C2 libalpm exec environment EX1-EX8 on S219-S225", tip `f951f288`.

## 5. Commands for the L1 (all read-only, from the lane root)

```
git log --format=%h -- tools/<tool>                      # one hash per tool: 7cbaeb6 / 6a08925 / a447b67
git log --format='%h %ad %an %s' --date=short -- tools/<tool>
git rev-parse 6a08925 7cbaeb6                            # full hashes
git show <add>:tools/<tool> | sha256sum                  # sha256 at the adding commit
sha256sum tools/<tool>                                   # tip bytes
git show 53b294a:tools/<tool> | sha256sum                # base bytes (r38/r39 only)
git cat-file -e 53b294a:tools/score-selftest-literals-r40.py; echo $?   # 128 = absent at base
git log --follow --format=%h -- tools/<tool>             # same single hash
git log --full-history --format=%h -- tools/<tool>       # same single hash
git log --all --format=%h -- tools/<tool>                # 4 hashes: freeze + 3 jj/keep snapshots
git merge-base --is-ancestor <snapshot> master; echo $?  # 1 for all nine snapshots
git branch -a --contains <snapshot>                      # empty
```

## 6. What I did not do

- I did not run any counter, the census `--selftest`, or the controls (out of F-6 scope; lineage only).
- I did not read the scribe's (`ConsiderLineage`) lineage draft — this derivation is deliberately independent; the L1 cross-checks the two.
- I did not audit the counters' internals beyond what the lessons cite (e.g. I did not re-verify `check-transaction-order-r39.py:223-226` myself).
- No tools were installed or upgraded; no scratch artifacts were created (scratch dir created empty, then removed). No lane file was modified; the only writes are this report and `lineage-receipts.txt` under my seat dir.
