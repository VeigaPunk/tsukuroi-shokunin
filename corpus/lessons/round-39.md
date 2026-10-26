# Round 39 — lesson (tsukuroi, hyaku run 8)

author: tsukuroi L1 (`TsukuroiR39`), 2026-10-26. Base `0eff65b21bb81195ee06c96a83afbd7a07e52eef`. Claims, controls and
outcome: `SCORECARD.md` sections "Round 39 — declaration" and "Round 39 — measured outcome". Wave: one v2 wave `w1`,
70 seats (`.ufo/waves/round-39/w1-spec.json`, `w1-results.json`; reports in `.ufo/waves/round-39/w1/`). Seats are the
lane, not outside reviewers (LEARNING.md); this round's non-author closure is pending.

The round-38 Gate's "Spot-check: Non-author closure pending" (`corpus/lessons/round-38.md:75-77`) is answered by
`corpus/lessons/round-38-verifier-spotcheck.md`: its §3 re-opened the admits S208–S211 and both rejects with
agree/disagree and reasons (`:113-121`), and its §6 routed the seven debts dispositioned below (wave seat
RevLessonXref; census re-run there exit 0).

## Gate

### New SOURCES rows (all opened 2026-10-26 by this round; each quote located with `grep -n` in the committed
snapshot `.ufo/waves/round-39/frozen/src/` or capture `.ufo/waves/round-39/frozen/txcapture/`)

| Row | Source URL/path and opened date | Located quote (≤25 words) | Location | Decision |
|---|---|---|---|---|
| S213 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/add.c — opened 2026-10-26 (raw fetched 2026-10-26T05:30Z, sha256 `fd313629…`) | “/* run the post-install script if it exists */” | `commit_single_pkg`, add.c:638 (pre scriptlet :466-474; `upgraded` log line :630; ldconfig :676-692) | admit, mined, tier A |
| S214 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/sync.c — opened 2026-10-26 (sha256 `6b297364…`) | “/* remove conflicting and to-be-replaced packages */” | `_alpm_sync_commit`, sync.c:1340 (`_alpm_remove_packages` :1345 before `_alpm_upgrade_packages` :1354) | admit, mined, tier A |
| S215 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/remove.c — opened 2026-10-26 (sha256 `a052d455…`) | “_alpm_runscriptlet(handle, scriptlet, "pre_remove", pkgver, NULL, 0);” | `_alpm_remove_single_package`, remove.c:711 (`removed` log :722, `post_remove` :731) | admit, mined, tier A |
| S216 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/util.c — opened 2026-10-26 (sha256 `381618b6…`) | “alpm_logaction(handle, "ALPM-SCRIPTLET", "%s", line);” | `_alpm_chroot_process_output`, util.c:527 (called from `_alpm_chroot_read_from_child` :544-570 under `_alpm_run_chroot` :610) | admit, mined, tier A |
| S217 | https://gitlab.archlinux.org/pacman/pacman/-/blob/54d9411/lib/libalpm/trans.c — opened 2026-10-26 (sha256 `637c1165…`, equal to S210's snapshot) | “alpm_logaction(handle, ALPM_CALLER_PREFIX, "transaction started\n");” | `alpm_trans_commit` (trans.c:167), trans.c:208 (Pre phase :201-204; Post after `transaction completed` :235-239) | admit, mined, tier A; correction row — teaches opens `supersedes S210 —` (round-38 closure §6.4) |
| S218 | `.ufo/waves/round-39/frozen/txcapture/` (own-work) — opened 2026-10-26 | “# captured 2026-10-26T05:42:12Z host=plazir27 read-only by TsukuroiR39” | capture-meta.txt:1; MANIFEST.sha256 (sha256 `cb5cb4f4…`) over capture-meta.txt, hook-owners.tsv, hook-when.tsv, pacman.log | admit, mined, tier A, own-work |

Status/recheck/used-by changes to existing rows: **S208** used-by
`corpus/knowledge/pacman-hook-order-r38.md` → `corpus/knowledge/pacman-hook-order-r38.md, corpus/knowledge/pacman-transaction-order-r39.md`
(TO5 cites hook.c:532-560). S210 is not rewritten (CORPUS.md rule 2); S217 carries the correction.

### Assimilation — collision check, quarantine slice

Collision check (scratch `.ufo/waves/round-39/assimilation/`, commands of the round prompt §10): registry ids before
this round's appends 212, staged ids 147, collisions 13 (S200–S212, `collisions`); after S213–S218 the collisions are
**19** (S200–S218, `collisions-after-s218`, re-derived independently by wave seat AsmCollision at `2e1c2a40`). Every
colliding staged id names a different document than the lane row at that id, so any future adoption is
document-keyed from **S219**. Guard proof: an indented `  | S200 |` fixture row is caught by the 0–3-space pattern
and missed by the column-zero pattern (`guard-proof/`); AsmCollision repeated it on census-valid registries
(`w1/AsmCollision/guard/`). Quarantine slice: 12 rows (S211, S213, S225, S230, S231, S242–S244, S249–S252 in campaign
numbering, `quarantine-slice`), re-derived byte-identical by ScoutQuarantine; intersection with the ids the round-39
entry cites (lane S208, S213–S218): none adopted — no staged row, id or text enters the corpus this round.

### Assimilation (theme: pacman hook timing, `merge/tsukuroi/`) — core re-grounded, interpretive sentences rejected

Candidate `pacman-hook-timing-r25.md` (sha256 `e18c146e733d3cab4bcc82c2ba30b9a571791ec132f7988cd93481b079f09324`,
the same bytes round 38 refused). Round 39's depth entry re-grounds its transaction-order propositions in libalpm at
`54d9411`; the per-proposition map (26 rows) is `.ufo/waves/round-39/w1/C2RevenStaged.md` §2.

| Candidate / proposition set | Decision | Reason; flip condition |
|---|---|---|
| `pacman-hook-timing-r25.md` — transaction-order core (staged `:17`, `:29-37`, `:48-49`, `:56-59`) | admit, as re-grounded by `pacman-transaction-order-r39.md` TO1–TO7 | Every stage is now read from the installed commit: Pre before `transaction started` (`trans.c:201-208`), removals before adds (`sync.c:1340-1357`), per-package pre-scriptlet → files → log line → post-scriptlet (`add.c:467-474`, `:599`, `:616-647`), new-version-first arguments (`add.c:472-473`, `trans.c:400-406`), removal order (`remove.c:690-733`), one `ldconfig` (`add.c:677-692`). The candidate's own document ids are not carried, so no staged id binds a lane row. Flip: a staged re-issue that cites these TO rows by document instead of restating them. |
| — owner cell (staged `:16`) | admit-with-correction | "the package that ships the file" is incomplete: 2 of the 70 captured hook files are owned by no package (`.ufo/waves/round-39/frozen/txcapture/hook-owners.tsv:69-70`); the cell must read "the package that ships the file, or no package for an operator-placed file". Flip: an ownership capture in which every hook file is package-owned. |
| — availability headline (staged `:29`) | admit-with-correction | "exists only while its providing package is installed" is an availability window, not existence: `Depends =` gates execution independently (`hook.c:509-517`) and an operator file outlives any author; TO5 already states the corrected form. Flip: not available — the "existence" form is contradicted by the two unowned files. |
| — interpretive sentences (staged `:22`, `:26-27`) | reject | "upstream says that is not a design" has no source (`grep alphabet` over the frozen devblog page → absent; byline David Runge / Arne Christian Beer), and the order *is* documented (`.ufo/waves/round-38/sources/alpm-hooks.5.asciidoc:38-39`); "no documented precedence scheme … the filename is the only lever" is contradicted by that line, by `OVERRIDING HOOKS` (`:98-100`) and by HO1's tie-break (`hook.c:451-452`). Flip: a source sentence stating that no ordering rule and no override mechanism exist. |
| — "independent confirmation" sentence (staged `:59-61`) | reject | A page the entry itself calls a translation of `en:Pacman` (staged `:61-63`) cannot independently confirm the English page it translates, and the order is now held at tier-A source (TO1–TO3), which makes the tier-B rendering redundant. Flip: an independent tier-A text in another language stating the same order at its own anchor. |
| — residual mechanism propositions: `NeedsTargets`→stdin (`:42-43`), `.pacnew` trigger target (`:44-45`), scriptlet cwd `/` (`:47-48`), global interpreter (`:49-51`) | not carried — defer, no decision on the candidate | No TO or HO row states them; each is re-groundable in the pinned snapshots (`hook.c:519-529`, `hook.c:258-279`, `util.c:677-683` with `trans.c:397-410`, `trans.c:357-358`). `alpm-hooks.5.asciidoc:91-93` and `:126-129` lie outside S209's declared anchor/scope cell, so stating them needs new rows (next free S219), not an in-place edit. Flip: a round-40 entry, or an appended section in r39, that states each with its line. |

Assimilation result: the candidate is admitted **by re-grounding, not as a document** — no staged row, no staged id,
no staged text enters the corpus.

### Spot-check

Non-author closure pending. Suggested sample: admit S216 (re-open `util.c` at 54d9411, line 527) and the reject of
the staged interpretive sentences (`pacman-hook-timing-r25.md:22`, `:26-27`) against `alpm-hooks.5.asciidoc:38-39`.

## Mistakes

| ID | Class | Evidence pointer | Captured-by | Fix, and how it is shown able to fail |
|---|---|---|---|---|
| R39-CONTENT-UNREAD | vacuous | The frozen C2 counter never reads the rule cell (`tools/check-transaction-order-r39.py` reads `cells[2]` and `cells[3]` only); an entry whose eight rule cells say "RULE NOT SUPPLIED", or the opposite of the source, scores 8/8 PASS (`.ufo/waves/round-39/w1/C2CritAxis.md` §A, X-empty / X-false; `C2CritControl.md` V1–V3, V7). The pre-data controls (`controls/c2-entries/E1`–`E6`) all kept the candidate's rule cells, so the shape was never scored before data | claim-sizing rule "build the cheapest control that skips the claimed work" (round prompt :448-452) — not applied to the rule cell | QUALITY 87 (new): a content counter reads the content it credits, and the frozen controls include a content-free entry. Shown able to fail: X-empty passes the round-39 counter (receipt `C2CritAxis/controls.jsonl`), so any counter that meets QUALITY 87 must fail that committed fixture |
| R39-FIXTURE-MONOCULTURE | vacuous | Every "btrfs mounted" fixture in the C1 counter and the census selftest is the same string (`/dev/mapper/root / btrfs … subvolid=256`), so arms keyed on `subvolid=256`, `/dev/mapper/root`, `" / btrfs "` or the substring `btrfs` PASS the counter 11/11 and the selftest 117/117 (`.ufo/waves/round-39/w1/C1CritControl.md`, VA–VC, VG); `grep -c btrfs` and case-insensitive fstype mutants survive (`C1MutParse.md` (a), (b)); guard mutants on `devn` or without `blocked -eq 0` survive (`C1MutCrossCheck.md` (d), (e)) | QUALITY 82 (fixture-gateable counters) — covers override detection, not literal monoculture | QUALITY 87 (b): vary the literal shape across fixtures and freeze a one-literal arm as a should-fail control. Shown able to fail: VG passes the round-39 counter (`C1CritControl/` receipts), so a counter meeting 87 (b) must fail it |
| R39-VIEW-CONTROL-UNREACHABLE | vacuous | The C1 predicate's third conjunct `views_matched == 3` reads 3 in every committed C1 run this round — `before/c1-before.jsonl`, `after/c1-after-49cc53c.jsonl` and `controls/controls.jsonl:1-5` (seven runs, `grep -o '"views_matched": [0-9]*'`; `hidden_matched` varies 0/2 across the same runs) — so no artifact shows it can move; the only control named for that channel, `C1-K3-mountinfo-keyed` (`controls/controls.jsonl:4`), rewrites `tools/tsukuroi-census.sh:1906`, inside the `if [ "$fsn" -eq 0 ]` guard at `:1903`, which every view skips (`draw_view` always emits 1-3 fsids, `tools/score-storage-hidden-r39.py:97-107`), and its kill arrives from `fixtures_matched 2`; round 38 shipped the arm QUALITY 82 names (`C1-cached-live`, `.ufo/waves/round-38/controls/controls-q82.jsonl:2`, q82 `ns_views_matched 1`) and round 39 ships none. Measured: an arm that does what the label says — `/proc/self/mountinfo` at `/sys/fs/btrfs`, outside the guard — reads hidden 2/2, views 0/3, fixtures 5/5, live 1 (`w1/MistakeMiner/e3b-view-arm-score.json`, variant sha256 `af0cee4e…`) | QUALITY 82 (second half: "the pre-data controls include a fixture-gated variant and a cached-live variant, each of which must read below the target") | Commit it as `C1-K5-view-keyed` with its line required to read `views_matched <= 2` (controls are not frozen; the counter needs no change). Shown able to fail: it reads `views_matched 0` while every other leg stays at target, and the candidate reads 3/3 on the same three legs (`after/c1-after-49cc53c.jsonl`), so the pair discriminates |
| R39-HOSTCELL-INFERRED-AS-SEEN | attribution | `corpus/knowledge/pacman-transaction-order-r39.md:29` (TO6) states "An interrupted transaction logs `transaction interrupted`, runs no `ldconfig` and no Post hook" for a class with zero instances in the round's own capture — 60 `[ALPM] transaction started`, 60 `transaction completed`, 0 `transaction interrupted`, 0 `transaction failed` (`.ufo/waves/round-39/frozen/txcapture/pacman.log`); the same table marks the analogous case honestly at `:25` ("has no host instance yet") and `## Boundaries` (`:46-51`) omits it; no conjunct reaches the host column — `counts_ok` recomputes exactly two cells (`tools/check-transaction-order-r39.py:223-226`, receipt `counts_ok: 2`), so the QUALITY sentence at `:55-56` ("host counts are reproduced from the frozen capture by the same tool") holds for 2 of 8 cells, and the declared kill rule judges rule text, which is source-true here | QUALITY 3 ("Observation, inference, and unknown stay separate", `corpus/QUALITY.md:6`) | Bind the column: `host_cells_inferred == 0`, where a cell must carry a recomputed capture quantity, a `pacman.log:NNN` citation, or begin `[inf] `. Shown able to fail: it reads 2 at `4078eb2` (TO4 `:27`, TO6 `:29`) and 0 after the marks plus the 17/28/0-of-60 recomputations; a digit grep is not the fix (`grep -c '[0-9]'` on both cells prints 1 from `(TO1, HO6)` and `$1`/`$2`) |
| R39-SEAT-PKILL | landing | Wave seat C1SentMounts ran `pkill -f 'tsukuroi-census\.sh'` at about 03:05 local, which sent SIGTERM to every census process on the host, including other seats' runs (`.ufo/waves/round-39/w1/C1SentMounts.md:208`; orchestrator notice to the L1). `C1ExecR38Counters` recorded an 8/10 run whose F03 died of the external SIGTERM | none — the wave context forbade host mutation but said nothing about signalling processes the seat did not start | Wave contexts from round 40 say: "signal only processes you started (by PID); never `pkill`/`killall` by pattern". Census numbers from C1ExecSelftest, C1LabratProcAbsent, LabratSelftestEnv and C1ExecR38Counters are cited below only from runs those reports mark clean or made after 03:05; the L1's own final receipts (`after/*-final-*`) re-measure every claim number |
| R39-ROLE-REFUSED | landing | The first two validator runs refused the spec: `items[8].role "labrat" is not a swarm role`, then `items[63].role "sonic" …` (`.ufo/waves/round-39/w1-dispatch.err` history; the run-8 routing table lists both as routed roles) | the wave validator (it refused; nothing spawned) | Labrat and sonic items were re-cast as executor items (same prompts) before dispatch; the validator is the check, and it fired. Recorded so the next spec is built from the validator's role list, not the routing table |
| R38-C2-COUNTER-GAPS | vacuous | The round-38 C2 counter passed a stripped entry citing only the own-work row S212 and survived an S-id drop from `source:` (`corpus/lessons/round-38-verifier-spotcheck.md:175-180`) | round-38 closure §6.3 | Closed in the round-39 counter's rules and shown by committed controls: E1 (own-work only) 0/8 FAIL, E3 (S213 dropped) 5/8 FAIL, E4 (duplicated block) FAIL (`.ufo/waves/round-39/controls/controls.jsonl`); QUALITY 86. Residual: dropping an *uncited* S-id (S218) from `source:` survives (`w1/C2MutEntry.md`) |

Not a mistake but recorded: the controls script's first two runs died on a shell defect (a here-string and a heredoc
both on stdin; then a quoting error in an inline transform) before scoring anything; both runs aborted rather than
writing wrong rows, and the committed `run-controls.sh` + `c1_variant.py` are the fixed form.

## Round-38 routed defects — round-39 disposition

| # | Routed defect (r38 §6) | r39 disposition | Covered by | Evidence |
|---|---|---|---|---|
| 1 | R38-Q82-LEAK | fixed-this-round | Views are tmpfs mounts inside the child namespace, filled from stdin (`tools/score-storage-hidden-r39.py`, frozen `6a08925d`); the four leak arms ported onto `49cc53c7` all FAIL it (views 0/3, 1/3, 0/3, 0/3) | `.ufo/waves/round-39/w1/C1LeakArms.md`, `C1LeakArms/scores.jsonl` and the four `.diff` files (committed should-fail controls) |
| 2 | R38-ABSENT-ROOT | fixed-this-round | Mount-table cross-check in `probe_storage_arm` (`49cc53c7`; wave hardening for FIFO and empty tables) | SCORECARD "Round 39 — measured outcome"; `PROVINCE.md` "Round-39 limit closure" |
| 3 | C2 counter gaps | fixed-this-round for the new counter | `tools/check-transaction-order-r39.py` rules; controls E1, E3, E4 | row R38-C2-COUNTER-GAPS above |
| 4 | S210 anchor | fixed-this-round | S217 `supersedes S210 —`, anchor `alpm_trans_commit` (trans.c:167); S210 bytes unchanged | `corpus/SOURCES.md` S217; `w1/C2RevS217.md` |
| 5 | Receipt binding | fixed-this-round | Before and after receipts written by `tools/run-receipt.py` (header names revision, tool, tool_sha256, tool_revision); `controls.jsonl` rows carry `counter_sha256`. Two receipt-class texts were unbound (`before/sources-census-start.txt`, `after/selftest-49cc53c.txt`; `w1/RevReceiptBinding.md`); the final receipts name their revision | `.ufo/waves/round-39/before/`, `after/` |
| 6 | Historical probe r35b | fixed-this-round | `SKILL.md` "Historical instrument pins — round 39" pins `score-pacnew-arm-r35b.py` and the round-38 v1 counter's F06 to the census blobs they must be read at | `w1/RoutedHistorical.md` (measured pins) |
| 7 | Lesson cross-reference | fixed-this-round | the cross-reference paragraph at the top of this lesson | `w1/RevLessonXref.md` |

## considerthese — evidence-weight watch (`considerthese/2026-10-25.md`, proposal "Evidence-weight watch")

Mined as a measurement and a lesson, not as a tool (`.ufo/waves/round-39/w1/ConsiderWeight.md`, commands in §1). Rounds
30–38: only four committed evidence files exceed 2 MB, all in round 36 (45,594,475 / 42,058,597 / 3,692,706 /
2,359,003 B — two strace capture pairs, about 87.7 MB of every working tree); round 31 had already stored its heavy
traces gzipped. Lesson: price evidence by checkout weight, not by commit size — no committed evidence file above
2 MB (a larger capture lands gzipped or reduced to the lines that carry the claim, with its sha256), and each
measured-outcome row names the round's evidence weight. Round 39's own weight is dominated by six copies of
`corpus/SOURCES.md` in the C2 control fixtures (`controls/c2-entries/*/SOURCES.md`, about 1.35 MB together).

## Sources census

Round start (`.ufo/waves/round-39/before/sources-census-start.txt`): `tsukuroi ok`, exit 0, 212 rows. Round end:
`.ufo/waves/round-39/after/sources-census-final.txt`.
