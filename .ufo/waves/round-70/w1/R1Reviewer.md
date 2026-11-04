# R1Reviewer — C1 falsification round 70 w1

Seat: R1Reviewer (reviewer, leaf). Scratch `/fast/scratch/hyaku/tsukuroi-r70/R1Reviewer` (removed after run). Counter copy sha256 `65065d9d18cea52027619697264de430780e65ff13ab6da2a790c3d2054f6f5c` = frozen. Snapshot digests re-computed, all four match `SHA256SUMS`/`SOURCES.json`. No tool installs (pacman guard respected; nothing needed).

## Finding 1 — row re-derivation: 6/6 reproduce against the committed snapshots; one LOW wording risk

Independent re-implementation of the frozen grammar (derive.py; not the counter's code): for each of the six rows in `.ufo/waves/round-70/w1/SC1Entry-note.md` — sha256 of the named snapshot, quote located whitespace-normalized verbatim, quote/statement word counts, shared non-stopword tokens (len>=4, boundary regex).

```
$ python3 $S/derive.py
XS1: OK stmt_words=19 quote_words=7 tokens(5)=xfs_stats_format,xstats,xstats_entry,endpoint,counter_val src=S291 snap=xfs_stats.c
XS2: OK stmt_words=31 quote_words=8 tokens(7)=counter_val,per_cpu_ptr,xfs_stats_format,extra,precision,defer_relog,debug src=S291 snap=xfs_stats.c
XS3: OK stmt_words=24 quote_words=6 tokens(9)=xfs_stats_ktype,stats,xfs_sysfs_attr_ro,stats_clear,... src=S292 snap=xfs_sysfs.c
XS4: OK stmt_words=23 quote_words=4 tokens(6)=xfs_log_ktype,log_head_lsn,...,grant src=S292 snap=xfs_sysfs.c
XS5: OK stmt_words=21 quote_words=13 tokens(11)=mounted,filesystem,...,write src=S290 snap=xfs.rst
XS6: OK stmt_words=25 quote_words=9 tokens(10)=health_f,health,...,problems src=S293 snap=health.c
DERIVED_OK=6/6
```

Every digest byte-matches the frozen values; quotes XS1 (`/* Loop over all stats groups */`), XS2 (the two joined `xs_xstrat_bytes/xs_write_bytes` accumulation lines), XS3 (`if (val != 1) return -EINVAL;` — two source lines, single line after whitespace normalization), XS4 (the four ATTR_LIST entries), XS5 (hierarchy sentence at xfs.rst:405-406), XS6 (health.c:541-542) are all verbatim. Source-byte factual spot-checks: XS3 `stats_clear_store` (kstrtoint, EINVAL on !=1, then `xfs_stats_clearall`) exact at xfs_sysfs.c:361-380; XS4 `%d:%d` cycle:block and `atomic64_read` `%lld` exact at xfs_sysfs.c:405-455; XS5 "As of 4.9 … metadata: applies metadata buffer write IO" exact at xfs.rst:422-426.
LOW: XS6's trailing clause "…before reporting any health problems" is ambiguous — the notice prints at `if (!reported)` (health.c:539-545), i.e. when the report pass produced nothing, not before reporting. No frozen clause violated; wording risk only.
In-flight: `corpus/SOURCES.md` in the working tree still lacks S290-S293 (grep `'| S29'` → 0 hits at attack time); `SC2Sources.md` §1 carries the draft rows and their source cells contain exactly the four snapshot map URLs, so the binding clause will hold at landing. Until L1 lands them, the frozen counter prints `source-unregistered` for all six rows.

## Finding 2 — counter attack: 11 self-built mutants, 7 refused, 4 survive (one material)

Control: my own six rows over 4 snapshots/4 sources (M6's run = control verbatim): rc 0, `XS_ROWS=6 XS_VERIFIED=6 XS_SOURCES=4 XS_SNAPSHOTS=4 met=1`. Mutants (all distinct from the frozen battery's 8 cases; fixtures under `$S/fixture`, registry + note are mine):

| mutant | construction | verdict |
|---|---|---|
| M1 source-cross-binding | XS1 cites S004 (registered for health.c URL) with snapshot=xfs.rst | REFUSED `source-not-bound`, rc 1 |
| M2 quote-word-order | "both we print series of quota information together" (words all present, order swapped) | REFUSED `quote-absent`, rc 1 |
| M3 stopwords-only | 36-word statement, every WORD_RE token in STOP | REFUSED `statement-tokens=0`, rc 1 |
| M4 chance-tokens | "statistics error unmount qzxwj vhktp lmfrs bqxzd ngvcp hjwlt zsdfk pqvbn wrmjt" (12 words; the 3 named tokens are standalone in xfs.rst) | **SURVIVED** rc 0 met=1 |
| M5 duplicate-snapshot | 6 rows over 4 distinct snapshots, xfs.rst cited 3× (same digest, different statements) | **SURVIVED** rc 0 met=1 |
| M6 anchor-bogus | registry S001 anchor cell `tag v6.12.0-legacy WRONGTAG`, source cell URL correct | **SURVIVED** rc 0 met=1 |
| M7a header+XS7 | valid 7th row appended | REFUSED rows=7≠6, rc 1 |
| M7b header+XS0 | valid XS0 appended | REFUSED `ids-not-contiguous`, rc 1 |
| M8 quote-26-words | 26-word verbatim xfs.rst quote | REFUSED `quote-words=26`, rc 1 |
| M9 pipe-in-statement | `\|` inside statement cell | REFUSED `malformed`, rc 1 |
| M10 digest-uppercase | last digest hex char `A` | REFUSED `malformed`, rc 1 |
| M11 invisible-row | extra row written `\|XS8\|…` (no space after pipe) | **SURVIVED** rc 0 met=1 — not counted at all |

Material finding (M4): the statement-substance clause is satisfiable by a content-free writer — three domain tokens (`statistics`, `error`, `unmount`) plus nine gibberish words pass `grounded()==3`. The frozen battery's `mutant-content-free` only killed zero-token filler. The clause still forces minimal domain contact, so this degrades the claim's "substance" strength, it does not break verifiability. M5: the frozen targets tolerate up to 2 of 6 rows re-citing an already-cited snapshot (only >=4 distinct demanded). M6: `registry_rows()` stores the anchor cell but `evaluate()` never reads it — the binding clause covers the source cell only, anchors are self-policed. M11: the `line.startswith("| XS")` gate makes any number of space-less `|XS<n>|` rows invisible; row-shape/pipe clauses are enforced only on counted rows. Candidate amendment for the already-planned next-round "row-verdict binding" work; no amendment of frozen predicates this round.

## Finding 3 — novelty holds

```
$ for p in sys/fs/xfs stats_clear log_head_lsn reserve_grant_head_bytes fail_at_unmount xfs_spaceman max_retries; do git -C <lane> grep -n -F "$p" b2aa0be068725d23a345616dc9282d00dcaaa835 | wc -l; done
0 0 0 0 0 0 0
```
All seven sysfs/health patterns: 0 hits at base (matches `before/novelty-sweep.txt`). SH1-SH6 (`storage-health-r26.md`) state btrfs per-device error counters, scrub records/repair and NVMe SMART lifetime counters — no statement, quote or claim overlaps XS1-XS6 (xfs sysfs stats/log/error/health plane); the note's Scope section references S128-S139 without restating them. No S-row duplication found. NOVELTY=holds.

## Finding 4 — grammar, pipes, header: clean on the real note, inflation mutants refused

Real note: all six rows have exactly 7 pipes (6 cells, no pipe inside any cell); header `| id | statement | source | snapshot | digest | quote |` and the `|---|` separator do not match `ROW_RE` (`^| XS<digits> |`) and are not counted — no header inflation possible on this note. M7a/M7b/M9/M10 show the counter refuses inflation and shape mutants via the exact-count, contiguity and grammar gates. Residual gap is M11's invisible-row channel (Finding 2).

## Finding 5 — verdict

C1's six rows reproduce in full against the committed snapshots; the frozen counter refuses every mutation class it claims (binding, verbatim quote, substance floor, counts, contiguity, shape). Four survivor channels exist (M4/M5/M6/M11); none lets a fabricated fact through — M4 needs three real domain tokens, M5/M6/M11 inflate or under-check bookkeeping, not content. Attack verdict: **C1 stands**, with Finding-2's four channels recorded for the next-round amendment work.

Final: ROWS_REPRODUCED=6/6 COUNTER_MUTANTS=11 REFUSED=7 SURVIVORS=4 NOVELTY=holds FINDINGS=5
