VERDICT: draft

Seat: RoutedDisposition (A-3), tsukuroi lane round 39 (hyaku run 8), leaf. Item: draft the round-39 lesson
section `## Round-38 routed defects — round-39 disposition` for the seven routed items of
`corpus/lessons/round-38-verifier-spotcheck.md` §6, and verify each disposition against the lane bytes.
Read-only: no lane file, index, jj state, host mount, service or package was touched; no scratch tree was
created (nothing to clone, copy or mutate for a read-only disposition); no counter, census or selftest was
rerun — every number below is a committed receipt or committed code read at HEAD (`2e1c2a4`).

## 1. The seven routed items, verbatim anchors

`corpus/lessons/round-38-verifier-spotcheck.md:169-184` (§6) was read in full. Item line numbers used below:
Q82 leak `:171-173`, absent root `:174`, C2 counter gaps `:175-180`, S210 anchor `:181`, receipt binding
`:182`, historical probe `:183`, lesson cross-reference `:184`.

## 2. Round-39 product surface (what could cover a debt at all)

```
$ git diff --name-only 0eff65b..HEAD | grep -v '^\.ufo/waves/round-39/'
SCORECARD.md
SKILL.md
corpus/SOURCES.md
corpus/knowledge/adjacency-anchors-r19.json
corpus/knowledge/pacman-transaction-order-r39.md
tools/check-transaction-order-r39.py
tools/score-storage-hidden-r39.py
tools/tsukuroi-census.sh
```
56 files, +14996 −4 in total (`git diff --stat 0eff65b..HEAD`). No `corpus/lessons/` path and no
`tools/score-pacnew-arm-r35b.py` change exists in that range, which fixes the disposition of items 6 and 7
below. `tools/run-receipt.py` is unchanged too (last touched `c052bb7`, round 36).

## 3. Verification of each disposition (observed, not inferred)

| # | Routed item | Observed at HEAD | State |
|---|---|---|---|
| 1 | Q82 leak | views drawn in the parent, sent as JSON on stdin, written into a tmpfs mounted over `/sys/fs/btrfs` inside `unshare -rm` (`tools/score-storage-hidden-r39.py:6-9`, `:80-91`, `:196`); before receipt already `views_matched 3` (`.ufo/waves/round-39/before/c1-before.jsonl:9`) — i.e. the views leg does not move with the hidden-root defect [INFERENCE from that reading, not a declared fact]; `grep -rn Q82Attack .ufo/waves/round-39/` → no hit | views **fixed**; arms **partly** |
| 2 | Absent root | `tools/tsukuroi-census.sh:1903` guard `fsn -eq 0 && blocked -eq 0`; `:1910` `mounts:btrfs-without-sysfs`, `:1912` `mounts:unreadable`; four selftest cases `:2974,2979,2984,2989`; before `hidden_matched 0`, `fixtures_matched 2`, FAIL (`before/c1-before.jsonl:8,10,13`); after `2`/`5`, PASS (`after/c1-after-49cc53c.jsonl:8,10,13`) | **fixed-this-round** |
| 3 | C2 counter gaps | `tools/check-transaction-order-r39.py:7-11` states all three closure rules; controls `C2-E1-no-upstream-row` rules 0, `C2-E3-sid-dropped` rules 5, `C2-E4-block-duplicated` `duplicate_rows 8`/`duplicate_headings 1`, all FAIL (`controls/controls.jsonl:7,9,10`); after receipt `rules_verified 8 … PASS` (`after/c2-after-4078eb2.jsonl:15-19,63`) | **fixed-this-round** (new counter; the round-38 counter is untouched and carries no round-39 claim) |
| 4 | S210 anchor | `corpus/SOURCES.md:226` (S217) teaches cell opens `supersedes S210 —`, anchor `alpm_trans_commit` `trans.c:167`; snapshot `sed -n 167p` = `int SYMEXPORT alpm_trans_commit(alpm_handle_t *handle, alpm_list_t **data)`; `sha256sum` of the snapshot = `637c1165…` = S217's pin; S210 unchanged (`:219`) | **fixed-this-round** |
| 5 | Receipt binding | runner header layout names `tool_sha256` (`tools/run-receipt.py:14-16`, written at `:105`); before receipts carry `revision 0eff65b…`, `tool_revision 6a08925d…`, `tool_sha256 75a9e8ab…` / `f1c97836…` (`before/c1-before.jsonl:1`, `before/c2-before.jsonl:1`; declaration `SCORECARD.md:2215`); every `controls.jsonl` line carries `counter_sha256` + `revision` | **answered** (procedural; runner unchanged) |
| 6 | Historical probe | `git diff 0eff65b..HEAD -- SKILL.md` = +2 lines (the round-39 rows `SKILL.md:3116-3117` only); registry rows for r35b still read `SKILL.md:3005` and `:3110` with no historical mark; counter sha `7517af92…` unchanged and `--revision` still free while only `CLAIM_BASE` is pinned (`tools/score-pacnew-arm-r35b.py:59`); the only guard remains the round-38 consumer note `SKILL.md:3147-3149` | **carried** |
| 7 | Lesson cross-reference | `corpus/lessons/round-38.md:75-77` still reads "Non-author closure pending." with no pointer and is unchanged since base; `ls corpus/lessons/` has no `round-39.md`; the C2 entry already forward-references one (`corpus/knowledge/pacman-transaction-order-r39.md:18`) | **carried to this lesson** |

Note on item 1's arms clause: of the four arms named at `.ufo/waves/round-38/w1/Q82Attack.md:30-33`
(`home-sibling-leak`, `features-empty-leak`, `fsid-shape-leak`, `mountinfo-leak`) exactly one shape is a
round-39 should-fail control — `C1-K3-mountinfo-keyed` (`controls.jsonl:4`, FAIL with `hidden_matched 2`,
`fixtures_matched 2`), and in its detect-the-counter form, not its leaked-path form. The other three shapes
are dead by construction because no view byte is ever written to a host path
(`tools/score-storage-hidden-r39.py:80-91`); that is an argument from code, not a committed arm. The item is
therefore reported as partly met, not met.

## 4. Proposed text (exact) — for `corpus/lessons/round-39.md`

Insert as its own section; it assumes the round-39 lesson's Gate section exists above it and that the tip
citation is updated to the measured revision if the L1 lands it after a further commit.

```markdown
## Round-38 routed defects — round-39 disposition

Round-38 closure routed seven debts (`corpus/lessons/round-38-verifier-spotcheck.md:169-184`, §6). Each one is
disposed here at base `2e1c2a4` and the commits it cites; a row names the bytes that cover it and claims
nothing those bytes do not show.

| # | Routed item (r38 §6) | Disposition | Covering commit / file | Evidence pointer |
|---|---|---|---|---|
| 1 | **R38-Q82-LEAK** — the Q82 counter admits four leak-reading arms; build the views in a tmpfs inside the child namespace, commit the four arms as should-fail controls (`:171-173`) | **fixed-this-round** for the views; **partly** for the arms (note 1) | `6a08925` `tools/score-storage-hidden-r39.py`; registry row `SKILL.md:3116` | Views are drawn in the parent, sent as JSON on stdin and written into a tmpfs mounted over `/sys/fs/btrfs` inside `unshare -rm` (`tools/score-storage-hidden-r39.py:6-9`, `:80-91`, `:196`), so no view byte lives at a host path for the `$HOME`/`$TMPDIR`-sibling or fixture-shape arms of `.ufo/waves/round-38/w1/Q82Attack.md:30-33` to read. The mountinfo shape is committed: `C1-K3-mountinfo-keyed` FAILs (`.ufo/waves/round-39/controls/controls.jsonl:4`: hidden 2/2, fixtures 2/5). |
| 2 | **R38-ABSENT-ROOT** — an absent `/sys/fs/btrfs` read HEALTHY 0/0/0; add a mounts cross-check (`:174`) | **fixed-this-round** | `49cc53c` `tools/tsukuroi-census.sh` | The cross-check runs only when the root yielded no fsid and nothing else blocked (`:1903`); a btrfs mount in `TSUKUROI_PROC_MOUNTS` gives `detail=mounts:btrfs-without-sysfs` (`:1910`), an unreadable table `detail=mounts:unreadable` (`:1912`), and a root with fsid entries never reads the table. Four selftest cases `:2974-2996`. Before `hidden_matched 0`, `fixtures_matched 2`, FAIL (`.ufo/waves/round-39/before/c1-before.jsonl:8,10,13`); after `hidden_matched 2`, `fixtures_matched 5`, PASS (`.ufo/waves/round-39/after/c1-after-49cc53c.jsonl:8,10,13`). |
| 3 | **C2 counter gaps** — a stripped entry citing only S212 passes; an S-id dropped from `source:` survives; block duplication past the next `## ` is invisible (`:175-180`) | **fixed-this-round**, in the new counter (the round-38 counter is unchanged and carries no round-39 claim) | `6a08925` `tools/check-transaction-order-r39.py`; entry `4078eb2` | `tools/check-transaction-order-r39.py:7-11`: a row verifies only on an upstream SOURCES row (`54d9411`, `lib/libalpm/<file>`, status `mined`, used-by naming the entry); every S-id in a source cell must appear on the entry's first `source:` line; duplicated rule rows and `## ` headings are counted anywhere in the file. Controls `C2-E1-no-upstream-row` 0/8, `C2-E3-sid-dropped` 5/8, `C2-E4-block-duplicated` (`duplicate_rows 8`, `duplicate_headings 1`) all FAIL (`.ufo/waves/round-39/controls/controls.jsonl:7,9,10`). After: `rules_verified 8`, `source_ok 1`, `counts_ok 2`, PASS (`.ufo/waves/round-39/after/c2-after-4078eb2.jsonl:15-19,63`). |
| 4 | **S210 anchor** — the anchor names the non-existent `_alpm_trans_commit`; land a row opening `supersedes S210 —` with anchor `alpm_trans_commit` (`trans.c:167`, 201-240) (`:181`) | **fixed-this-round** | `4078eb2` `corpus/SOURCES.md` | `corpus/SOURCES.md:226` (S217) opens its teaches cell `supersedes S210 —` and anchors `alpm_trans_commit` at `trans.c:167`; the frozen snapshot carries `int SYMEXPORT alpm_trans_commit(...)` at `.ufo/waves/round-39/frozen/src/trans.c:167` (sha256 `637c1165…`, the row's pin), and the TO1 row cites S217 (`corpus/knowledge/pacman-transaction-order-r39.md:24`). S210 is unrewritten (`corpus/SOURCES.md:219`). |
| 5 | **Receipt binding** — before receipts and `controls.jsonl` carry no `tool_sha256` or revision (`:182`) | **answered** | `tools/run-receipt.py` (unchanged this round); `93fddb2` before receipts | The runner's header names `revision`, `tool`, `tool_sha256` (`tools/run-receipt.py:14-16`, written at `:105`), and round 39 used it at the base with `--tool-revision 6a08925d` (`SCORECARD.md:2215`): `.ufo/waves/round-39/before/c1-before.jsonl:1` and `before/c2-before.jsonl:1` carry `revision 0eff65b…`, `tool_revision 6a08925d…` and the tool's sha (`75a9e8ab…`, `f1c97836…`). Every `controls.jsonl` line carries `counter_sha256` and `revision`. |
| 6 | **Historical probe** — `score-pacnew-arm-r35b.py` reads base-parity failures past `52ffd65`; mark it historical in the registry or pin its census input (`:183`) | **carried** (note 2) | `SKILL.md` registry tables; `tools/score-pacnew-arm-r35b.py` | Nothing landed this round: `git diff 0eff65b..HEAD -- SKILL.md` adds only the round-39 rows (`SKILL.md:3116-3117`), the two r35b rows (`SKILL.md:3005`, `:3110`) are byte-unchanged, the counter is unchanged (`sha256 7517af92…`) and its `--revision` input is still free while only `CLAIM_BASE` is pinned (`tools/score-pacnew-arm-r35b.py:59`). The only guard remains the round-38 consumer note (`SKILL.md:3147-3149`). |
| 7 | **Lesson cross-reference** — "Spot-check: Non-author closure pending" (`corpus/lessons/round-38.md`) is answered by the spot-check file; cross-reference it next round (`:184`) | **carried to this lesson** (note 3) | `corpus/lessons/round-38.md:75-77`; this section | The lesson still reads "Non-author closure pending." with no pointer (`corpus/lessons/round-38.md:75-77`, unchanged since the base), and this is the round that must carry the cross-reference: the Gate sentence in note 3 does it. |

Notes.

1. **Item 1, the arms clause.** Of the four arms `Q82Attack.md:30-33` names, one shape is committed as a
   round-39 control (`C1-K3-mountinfo-keyed`, in its detect-the-counter form); the sibling-path and
   fixture-shape arms are dead by construction because the view bytes never reach a host path
   (`tools/score-storage-hidden-r39.py:80-91`) — an argument from the counter's code, not a committed
   should-fail arm. If a later counter ever writes view bytes outside the namespace, commit those three arms
   before scoring it.
2. **Item 6 stays open until a registry mark lands.** Proposed note, to be appended under the *Gate and probe
   registry* table on the `SKILL.md:3147-3149` precedent:

   > Historical probe note (round 39, routed defect §6.6): `score-pacnew-arm-r35b.py` is a **round-35
   > instrument only**. Its claim base is pinned in code (`CLAIM_BASE`, `tools/score-pacnew-arm-r35b.py:59`)
   > but its `--revision` input is not, so at any census revision after `52ffd65` its base-parity leg reads
   > failures for lines that postdate round 35. Cite it only with a round-35 revision; it is not a claim
   > counter at any later revision.

3. **Item 7, the cross-reference sentence** for this lesson's Gate (precedent:
   `corpus/lessons/round-38.md:107`): "The round-38 Gate's 'Spot-check: Non-author closure pending'
   (`corpus/lessons/round-38.md:75-77`) is answered by `corpus/lessons/round-38-verifier-spotcheck.md`: its §3
   re-opened three admits (S208, S209, S210/S211) and both rejects with agree/disagree and reasons
   (`:113-121`), its §6 routed the seven debts dispositioned in this lesson's *Round-38 routed defects —
   round-39 disposition* section, and no round-38 debt remains undispositioned."
```

## 5. Findings and limits

- **The draft is not uniform "fixed".** Items 2, 3, 4 are fully covered by committed bytes; item 1 is partly
  covered (views fixed, one of four arms committed); item 5 is answered by procedure with an unchanged
  runner; items 6 and 7 are carried, and item 7 is discharged by this very section plus the note-3 sentence.
  Writing all seven as "fixed" would overstate the round.
- **Item 6 needs an owner outside this seat.** It requires a `SKILL.md` edit; seats are read-only on lane
  content, so the registry note in note 2 is proposed text, not landed text.
- **The C2 entry forward-references an unwritten file** (`corpus/knowledge/pacman-transaction-order-r39.md:18`
  points at `corpus/lessons/round-39.md`); once this section lands, that reference resolves. It is worth
  flagging because a committed entry currently names a file that does not exist (`ls corpus/lessons/`).
- **Not rerun, by design:** `tools/score-storage-hidden-r39.py`, `tools/check-transaction-order-r39.py`,
  `tools/tsukuroi-census.sh --selftest`, and every other lane gate. The before/after and control numbers cited
  above are the committed receipts, and the second-tier facts (line numbers, sha256s, diff sizes) were read
  directly. I did not verify the TO1-TO8 rule *text* against the pinned source — that is the C2 reviewer
  seats' duty under the QUALITY 81 kill rule, not the scribe's.
- **Seat outputs not consulted:** `C1LeakArms`, `C2MutEntry`-era seats and the other live peer reports are
  in flight; nothing in this disposition rests on them.
- **Tooling:** no package, tool or binary was installed or upgraded this round by this seat (pacman is paused
  host-wide regardless); no sudo, no mount outside a namespace (none at all), no service, no `/etc` write.
- **Scratch:** none created; nothing to remove. The only writes are this report and the verification log
  below, both under the seat's own `w1/` path.

## 6. Artifacts

- Report: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/w1/RoutedDisposition.md`
- Verification log (commands and observed outputs): `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-39/w1/RoutedDisposition/verif.txt`
