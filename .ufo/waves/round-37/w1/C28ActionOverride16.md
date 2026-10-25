# C28ActionOverride16 — C2 falsification item 8/8: action-override classification

Seat: `C28ActionOverride16` (scout, L2 leaf) · round 37 wave 1 · tsukuroi lane · milestone "C2 counter attack"
Axes: depth, `C2:action-override classification`. Date: 2026-10-25.

**Assignment:** attack the declared C2 correction requirement specifically the *action-override classification*; read the r36 verifier spot-check and the current r36 note/source; decide whether its target is precise and testable; propose concrete should-pass / should-fail cases; **do not author the change**.

**Lane bounds honoured.** No lane/fleet/sibling/sibling-repo write. No `git`/`jj` write in any repo (only `git log`/`git show`/`git status`/`git ls-files` reads). No pacman, no host install, no delegation, no background jobs, no campaign tools. Only artifact written: this file. `/home/vgpnk/Projects/shokuknow` never touched. Fixture git: not needed — this seat produced no fixture; all probes ran read-only in `/tmp` (shell redirections only).

**Concurrent-change note.** At the end of this seat's work `git status --porcelain` showed `M SCORECARD.md` (4 appended lines, mtime 16:30:02, ~20 s before this report was written). Its content is a "Round-37 source-pointer erratum" about S200/S201 and C1 — **not mine**; this seat issued exactly one write, to this report file, and never opened `SCORECARD.md` for writing. The modification is a sibling seat's append-only edit, recorded here so the parent does not attribute it to C28ActionOverride16.

**Tooling record.** `/home/vgpnk/.omp/agent/RULES.md` read first (lines 1–14). Channel order is pacman → uv tool → official release binary → cargo/npm; **no install or update was performed or needed** (all evidence needed was `curl`, `python3` 3.14.8 stdlib, `git` 2.56.0 read-only, `sha256sum`, `journalctl` 8.x already present). Host-wide pacman transactions are paused per the assignment, so no pacman command was run at all.

---

## 0. Verdict (short)

**The declared C2 correction target is precise enough to be testable, but as *landed* it is not yet a correct correction of the action-override classification.** Three findings, in descending severity:

1. **The landed note still carries the mis-classified rows.** The correction was shipped as an *addendum* (a second `## Round 37 correction` block at note line 158) that says the r36 rows are "superseded", but the r36 decision table at note lines 42 and 44 — the rows that say `--disk-usage`/`--header`/`--sync`/`--list-boots` are **WORK** — are still present, unedited, and still assert the false classification. There is no `action override` row anywhere in the note's decision table. A reader of the table alone still gets the wrong answer.
2. **The landed counter cannot detect that.** `tools/check-journalctl-v262-corrections.py` is a *prose-token* gate: it splits the note on the addendum header and requires 13 literal substrings plus a 15-term regex. It never inspects the decision table. I proved by mutation: strengthening note row 42 to read `**WORK — field enumeration works**` still exits **0**.
3. **The addendum is duplicated**, with the two copies differing in exactly one load-bearing phrase (`-N` field-name output is unchanged *from plain `-N`* vs *unchanged*). The counter passes only because it reads the region after the *first* header occurrence; a de-duplicated note carrying the second copy's wording exits **1**. The landed note's PASS is partly an artifact of the duplication.

Separately, my own probes found **one behaviour the r36 critic and the landed note both miss**: `--boot=all` **cancels a previously-set boot filter**, so `-b 0 --boot=all -F PRIORITY` exits **0** while `-b 0 -F PRIORITY` exits **1**. That is a *scope-scope* override, not an *action* override, and it is a second, distinct last-wins axis.

Full evidence below.

---

## 1. Anchors opened this round

| # | Artifact | Locator | What it gives |
|---|---|---|---|
| A1 | `corpus/lessons/round-36-verifier-spotcheck.md` | lines 65, 103 | The routed defect: "action-override classification" is one of three C2 corrections, "Recorded, still unapplied". Closure ruling at line 66: `unprovable-but-better`. |
| A2 | `.ufo/waves/round-36/w2/W2CritC2Depth/c2-depth-ruling.md` | §5, lines 87–101 | The defining ruling: "`--list-boots` is an action override, not working field enumeration"; "separate **action overwritten / last action selected** from genuine accepted field-enumeration scope selectors. Preserve exact argv order." Smallest correction at line 99. |
| A3 | `SCORECARD.md` | lines 1906–1919 | The declared C2 after-state: "the note carries … an action-override classification row"; counter `tools/check-journalctl-v262-corrections.py --revision <REV>`, exit 0/1/2. |
| A4 | `corpus/knowledge/journalctl-v262-field-filter-r36.md` | **at tip** `dedb5c2f…1483b`; at r36 base `0077b6cf…a8a8bf` | The note under correction. Decision table lines 23–46. **Addendum appears twice: lines 129 and 158.** |
| A5 | `.ufo/waves/round-36/w1/ScribeC2Draft/matrix-mini.json` | cells `core_plain` (:25), `ext_diskusage_N` (:536), `ext_header_F` (:564), `ext_sync_F` (:589), `live_list_boots` (:1018), `live_namespace` (:1069) | The r36 saved evidence the note's cells point at. 54 cells. |
| A6 | `tools/check-journalctl-v262-corrections.py` | landed at `d621b71` (introduced `543a7ce`) | The declared counter. `BLOCK`/`TERMS` at lines 22–30, `evaluate()` lines 33–78, `required` tuple lines 49–64, `_fixture()`/`selftest()` lines 106–131. |
| A7 | systemd v262 `src/journal/journalctl.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c`, fetched 2026-10-25, sha256 `285b3d0c1217b9a3be90dca2ed4591eb8cf0192e2d3c75f303df3c5f18d5d0ab` (matches the note's pin and the r36 tracked copy) | Option→action map; guard `:958-960`; merge guard `:962-964`; extraneous guard `:953-956`. |
| A8 | systemd v262 `src/journal/journalctl-filter.c` | `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl-filter.c`, fetched 2026-10-25, sha256 `480f7a03040c0ddc93b1b65c0b49d6f0e8a4a377ee1b94168655132dcfd72f48` (matches) | `field_list_has_scope_options()` lines 26–43, 15 OR terms. |
| A9 | systemd v262 `NEWS` | `https://raw.githubusercontent.com/systemd/systemd/v262/NEWS`, fetched 2026-10-25, sha256 `a494f0389edd09702a90d1540c7e21c0af5a4d29a4d020855ca3062d885a7657` (matches S199 pin) | Quote located at lines 129–133: "journalctl now rejects -F/--field together with filters such as unit, boot, time, cursor or grep filters." (accessed 2026-10-25). |
| A10 | `journalctl(1)` at 262.1 | `https://man.archlinux.org/man/journalctl.1` — **fetch FAILED this round**: `curl: (35) TLS connect error: error:0A000126:SSL routines::unexpected eof while reading` on two attempts (default and `--tlsv1.2`). **Not cited as opened.** The lane's tracked local copy `.ufo/waves/round-36/w1/SrcSystemdNews/journalctl.1.local-manpage` (sha256 `1e737294…b62d54`) was read instead; its `-F, --field=` entry carries "Print all possible data values the specified field can take in all entries of the journal." (line 885). This is a **source-availability gap**, not a claim of re-opening S198. |

Sibling seats on the same target (not to be duplicated): `C24ActionOverride12.md` (item 4/8, same "action-override classification" prompt) and `Build7C239` (item 7/12, the fixture). My independent contribution beyond both is §4 (the `--boot=all` scope-cancellation axis), §5 (the counter's table-blindness proof), and §6 (the duplicate-addendum defect).

---

## 2. The target as declared, and its precision

**Declared (SCORECARD.md:1909–1916, verbatim):** "Routed defect: round-36 verifier spot-check §6 item 2 (W2CritC2Depth): 15 not 16 predicate terms; `-F` truncation vs unchanged `-N` output under `-n`; action-override classification. Before: `corpus/knowledge/journalctl-v262-field-filter-r36.md` carries the 16-term table and lacks the two rows. After: the note carries exactly the corrected 15-term predicate table, the third-state (`-n`) row distinguishing `-F` truncation from unchanged `-N` output under `-n`, and an action-override classification row; the rejection line stays verbatim."

**Precision assessment — targeted at the action-override slice only:**

- **The negative claim is precise and correct.** Note line 44 reads: `| not a limiter | --boot=all; --list-boots; --show-cursor; --merge | **WORK** | live_boot_all …, live_list_boots, live_show_cursor, live_merge |`. Grouping `--list-boots` with options that genuinely preserve field enumeration is false: `--list-boots` assigns `arg_action = ACTION_LIST_BOOTS` (A7 `:813`), replacing `ACTION_LIST_FIELDS` assigned by `-F` (A7 `:806`). The guard at A7 `:958` is `IN_SET(arg_action, ACTION_LIST_FIELDS, ACTION_LIST_FIELD_NAMES) && field_list_has_scope_options()`, evaluated **once after the whole parse**, so it sees only the final action.
- **The positive requirement is under-specified in three ways that a counter author cannot resolve from the text alone:**
  1. **"a row" — one row or a row set?** The critic (A2 line 95) names *four* action flags to be separated (`--list-boots`, `--disk-usage`, `--header`, `--sync`), and A7 shows **22 options assign `arg_action`** (`-N`, `-F`, `--list-boots`, `--list-invocations`, `--list-namespaces`, `--disk-usage`, `--vacuum-size/-files/-time`, `--verify`, `--sync`, `--relinquish-var`, `--smart-relinquish-var`, `--flush`, `--rotate`, `--header`, `--list-catalog`, `--dump-catalog`, `--update-catalog`, `--setup-keys`, `--new-id128`, `--verify-key`). The declaration says "an action-override classification row" (singular) with no enumeration and no closure criterion ("all action-assigning options" vs "the four the critic named").
  2. **Where does the row live?** The declaration says "the note carries … an action-override classification row" but does not say whether that row must be *in the decision table* (the thing that is wrong) or may be an append-only addendum (which is what landed). A2's "Smallest correction" says "separate … from genuine accepted field-enumeration scope selectors" — i.e. a change to the *table's classification*, not a prose note elsewhere.
  3. **What is the observable that distinguishes the classes?** Both `--list-boots -F PRIORITY` and `-F PRIORITY --list-boots` exit **0**. Exit code cannot discriminate; only stdout **identity** against a same-run baseline does (§3). The declaration does not say the counter must compare output identity, and the landed counter does not (§5).
- **Testable: yes.** Deterministic on systemd 262, order-contingent, machine-checkable by exit code + stdout sha256 equality against within-run baselines. It is **not** testable by a counter that only greps for phrases — that is precisely the defect in §5.

**Verdict on the declared target: directionally precise, mechanically testable, but under-specified in scope (which flags), placement (table vs addendum), and observable (output identity vs exit code).** All three gaps are live in the landed artifact.

---

## 3. Empirical ground truth (live, read-only, this host)

Host: `systemd 262 (262-1-arch)` (`journalctl --version` first line, 2026-10-25). All probes prefixed `--no-pager`. Digests are truncated to 16 hex chars.

### 3.1 The action-override axis (last action wins)

| argv | rc | stdout bytes | stdout sha256 | meaning |
|---|---|---|---|---|
| `-F PRIORITY` | 0 | 12 | `97477348840c310c` | field-value baseline (**A**) |
| `--list-boots` | 0 | 262 | `3ea80f5652bbfdcb` | boot-table baseline (**E**) |
| `-F PRIORITY --list-boots` | 0 | 262 | `3ea80f5652bbfdcb` | **≡ E** — `-F` swallowed; this is the r36 cell `live_list_boots` |
| `--list-boots -F PRIORITY` | 0 | 12 | `97477348840c310c` | **≡ A** — `--list-boots` swallowed |
| `--list-boots -N` | 0 | 2734 | `879e9c6ab656…` | ≡ plain `-N` |
| `-N --list-boots` | 0 | 261 | `41511e75b148…` | ≡ boot table |
| `-F PRIORITY --disk-usage` | 0 | 61 | `88e9ac46a764d562` | ≡ plain `--disk-usage` ("Archived and active journals take up 56M…") |
| `-F PRIORITY --header` | 0 | 5199 | `caf868a12c3c8ea9` | ≡ plain `--header` (journal header dump) |
| `-F PRIORITY --show-cursor` | 0 | 12 | `97477348840c310c` | ≡ **A** — true modifier |
| `-F PRIORITY --merge` | 0 | 12 | `97477348840c310c` | ≡ **A** — true modifier (contrast the merge *guard*, below) |
| `-b 0 -F PRIORITY` | 1 | 0 | — | 84-byte scope rejection, sha `e8185af7add613e2` |
| `-b 0 -F PRIORITY --list-boots` | 0 | 262 | `3ea80f5652bbfdcb` | **the guard never fires** — action override suppressed the rejection |
| `--list-boots -b 0 -F PRIORITY` | 1 | 0 | — | 84-byte scope rejection — same options, different order, opposite verdict |

The last two rows are the sharpest vector: **the same option set, reordered, flips between exit 1 (scope rejection) and exit 0 (boot table)**. Any counter that keys on "does it reject?" without pinning argv order is wrong.

### 3.2 The third error class the note never records

| argv | rc | stderr bytes | stderr sha256 | text |
|---|---|---|---|---|
| `--list-boots --merge` | 1 | 60 | `83e17587301b7e27` | `Using --boot or --list-boots with --merge is not supported.` |
| `-b 0 --merge` | 1 | 60 | `83e17587301b7e27` | same (A7 `:962-964`) |
| `-F PRIORITY --list-boots --merge` | 1 | 60 | `83e17587301b7e27` | same — the merge conflict **survives** a `-F` override |
| `--list-boots --merge -F PRIORITY` | 0 | 12 | — | **masked** — `-F` last ⇒ `arg_action = ACTION_LIST_FIELDS`, so A7 `:962` does not fire |
| `-N PRIORITY,MESSAGE` | 1 | 54 | `5458e6e1e72122eb` | `Extraneous arguments starting with 'PRIORITY,MESSAGE'` (A7 `:953-956`) |
| `-F PRIORITY --list-invocations` | 1 | 99 | `7cf39cffc7dfdde7` | `Using --list-invocations requires a unit. …` |
| `-F PRIORITY --list-namespaces` | 0 | 21 | `c661c77b64382b28` | `No namespaces found.` — **exit 0 with stderr and empty stdout** |
| `-F PRIORITY --namespace=x` | 0 | 29 | `a9e685546c257573` | `No journal files were found.` — **exit 0, empty stdout**; this is r36 cell `live_namespace` (A5 :1069), recorded `stdout_bytes: 0, stderr_bytes: 29` |

Note the last two: the r36 note calls `--namespace=` **WORK** (note line 43) on the strength of cell `live_namespace`, whose own recorded stdout is **0 bytes**. `WORK` in the note's legend means "exit 0" (line 21), but the cell it points at produced **no field list at all** and printed a diagnostic to stderr. That is a third mis-classification of the same family, in the same table, uncorrected by the landed addendum.

### 3.3 The `--boot=all` scope-cancellation axis (not previously reported)

| argv | rc | stdout | meaning |
|---|---|---|---|
| `-b 0 -F PRIORITY` | 1 | — | rejects |
| `-b 0 --boot=all -F PRIORITY` | **0** | 12 B, sha `97477348840c310c` ≡ **A** | **`--boot=all` cancelled the `-b 0` boot filter** |
| `--boot=all -b 0 -F PRIORITY` | 1 | — | rejects — order matters |
| `--this-boot --boot=all -F PRIORITY` | **0** | 12 B ≡ **A** | ditto for `--this-boot` |
| `--boot=all --this-boot -F PRIORITY` | 1 | — | rejects |

Mechanism (A7): `journalctl.c:520-525` — `parse_id_descriptor("all")` returns **0** for the literal `all` (A7 `:163-168`: `if (streq(x, "all")) { … return 0; }`), and the handler then does `arg_boot = r;` / `arg_boot_filter = r > 0;` — so `--boot=all` sets `arg_boot_filter = (0 > 0) = **false**`, **clearing** a boot filter set by an earlier `-b`/`--boot=`/`--this-boot`. `field_list_has_scope_options()` (A8 `:26-43`) reads `arg_boot_filter`, so the predicate term goes false and the guard cannot fire.

Observable consequence beyond the exit code — the **scope widens**: the PRIORITY value set for boot 0 is `{3,4,5,6,7}` (5 values); for all boots it is `{2,3,4,5,6,7}` (6 values). Measured via `journalctl --no-pager <args> -o json --output-fields=PRIORITY`:

- `-b 0` → `['3','4','5','6','7']`
- `-b 0 --boot=all` → `['2','3','4','5','6','7']`
- `--boot=all` → `['2','3','4','5','6','7']`

So `--boot=all` is **not** merely "sets no boot filter" (the note's parenthetical at line 44). It is a **scope-scope last-wins override** on the `arg_boot_filter` term — the same class of defect as the action override, on the *predicate* axis instead of the *action* axis, and it is **not** mentioned by the r36 critic, the r36 note, the landed addendum, or the landed counter. It is also the *only* scope term with this property: every other term I probed (`-p`, `--facility=`, `-t`, `--user-unit=`, `--exclude-identifier=`, `--invocation=`, `-k`, `-u`, `--cursor=`, `--after-cursor=`, `--cursor-file=`) still rejects when `--boot=all` follows it.

---

## 4. What the landed artifact actually says, and what it misses

**Landed addendum (note lines 129–157 and 158–185, near-duplicate):** "### Action replacement is not field enumeration — The saved `live_list_boots` cell uses `journalctl --no-pager -F PRIORITY --list-boots`, exits 0 and prints 541 bytes of boot-list output; it does not produce the field-value list. In the pinned v262 parser, `-F` sets `arg_action = ACTION_LIST_FIELDS` at `journalctl.c:805-809`, then `--list-boots` replaces it with `ACTION_LIST_BOOTS` at `:812-814`. … Do not classify `--list-boots` as a successful field-enumeration exception."

**Defect D1 — the mis-classifying rows are still live.** Note line 42 still reads `| not a limiter | --output-fields=; --disk-usage; --header; --sync | **WORK** | live_output_fields, ext_diskusage_N, ext_header_F, ext_sync_F |` and line 44 still reads `| not a limiter | --boot=all; --list-boots; --show-cursor; --merge | **WORK** | … |`. The addendum's "supersedes" sentence is prose about the rows; the rows themselves are unchanged. A reader of the table alone is still told `--disk-usage`, `--header`, `--sync` and `--list-boots` are WORK — i.e. exactly the false classification the correction was routed to remove. **The landed note contains no row whose text contains "action override"** (verified by scanning every `|`-prefixed line).

**Defect D2 — the addendum covers one of the four flags the critic named.** A2 line 95 names `--disk-usage`, `--header`, `--sync` alongside `--list-boots`. The addendum's "Action replacement" section discusses only `--list-boots`. `--disk-usage`, `--header` and `--sync` remain in the WORK row with no correction — and my probes show all three override exactly like `--list-boots` (§3.1). `--sync` is the worst of the three: `--sync` assigned last performs a **journal sync** (`ACTION_SYNC` → `action_sync()`, A7 `:857`, `:1122`) — a *state-changing* action that a WORK-labelled row would invite a consumer to run.

**Defect D3 — the "541 bytes" figure is a stale snapshot.** The addendum repeats the r36 cell's 541 bytes as if current. Today the same argv yields 262 bytes (the retained-boot set changed). The addendum does say "the saved `live_list_boots` cell", which is honest, but a counter that ever asserts a byte count here would be host-state-dependent. Compare the r36 `core_plain` cell (12 bytes, sha `d0f6353ae541a724`, order `5 6 2 4 7 3`) with today (12 bytes, sha `97477348840c310c`, order `2 4 5 6 7 3`): same **value set** `{2,3,4,5,6,7}`, different **order** ⇒ different sha. **Any counter must compare output identity against a same-run baseline, never against a pinned sha or a pinned byte count.** This also invalidates the r36 matrix's own sha values as ground truth for the field list.

**Defect D4 — the duplicate addendum.** The heading `## Round 37 correction — predicate count, output states, action precedence and prior teaching` occurs **twice** (lines 129 and 158). The two copies differ in exactly one phrase: copy 1 has `` `-N` field-name output is unchanged from plain `-N` `` (with `` `-N` `` backticked), copy 2 has `field-name output is unchanged from plain `-N` `` (no backticks). Everything else is byte-identical (3528 vs 3522 chars — the 6-char delta is exactly that phrase). The counter requires the copy-1 wording (`required` tuple, A6 line 60: `` "`-N` field-name output is unchanged from plain `-N`" ``). Consequences measured:
- landed note (both copies) → **exit 0**
- de-duplicated to one copy with **copy-1** wording → **exit 0**
- de-duplicated to one copy with **copy-2** wording → **exit 1**, finding `C2-CLAIM-MISSING: -N field-name output is unchanged from plain -N`

So the landed PASS is partly an artifact of a duplicated block: a de-duplicated note that keeps the second copy's (equally correct) wording would fail the declared counter. And the duplication is itself a lane-content defect (two "superseding" addenda with conflicting wording in one file).

---

## 5. The landed counter is table-blind — proven by mutation

`tools/check-journalctl-v262-corrections.py` `evaluate()` (A6 :33-78) does exactly three things: (a) require the `## Round 37 correction` header; (b) regex the 15 `arg_*` names out of one sentence; (c) require 13 literal substrings inside `block = note.split(BLOCK, 1)[1]`. It **never reads the decision table**. `block` starts *after* the addendum, so note lines 23–46 are outside the checked region entirely.

Mutations I ran against a copy of the landed tool + the landed note (no lane write; copy in `/tmp/c2probe`):

| # | Mutation | Counter exit |
|---|---|---|
| 0 | landed note, unmodified | **0 (PASS)** |
| A | note row 42 strengthened to `**WORK — field enumeration works**` | **0 (PASS)** ← the false classification is *not* detected |
| B | addendum removed entirely | 1 (FAIL) — correct |
| C | keep only the first copy of the addendum | 0 (PASS) |
| D | keep only the second copy's wording | **1 (FAIL)** — see §4 D4 |

Run at the real revisions: `--revision 543a7ce` → **0**; `--revision 564db0b614` (r37 base, note uncorrected) → **1** with 14 findings; `--selftest` → **0**, 7/7 cases pass.

**Consequence:** the declared after-state "the note carries … an action-override classification row" is satisfied by the landed artifact **in letter but not in substance**, and the declared counter cannot tell the difference. A note whose table still calls `--list-boots`/`--disk-usage`/`--header`/`--sync` WORK, whose `--namespace=` row points at a 0-byte stdout cell, and which carries a duplicated addendum, passes the counter cleanly. This is exactly the "token/notice-presence guard" failure the lane already diagnosed in round 13 (`.ufo/waves/round-13/correction/AdmissionCritic.md:10-14`: "Every falsifier below **passes a token/notice-presence guard**").

---

## 6. Proposed test vectors

Concrete, machine-decidable, and each tied to a source anchor. "Counter" = `tools/check-journalctl-v262-corrections.py` (the declared C2 counter) unless stated.

### 6.1 Should-pass (the corrected note + counter must satisfy these)

- **SP1 — table-level action-override classification exists.** The note's decision table contains a row whose verdict column distinguishes the action-override class from the scope-selector class, and that row names `--list-boots`. *(Currently absent — D1.)* Anchor: A7 `:806`, `:813`, `:958`.
- **SP2 — no blanket WORK verdict for any action-assigning option.** For each of `--list-boots`, `--disk-usage`, `--header`, `--sync` (the four the critic named, A2 :95): the note must not classify it as WORK for `-F`/`-N` enumeration. *(Currently violated at note lines 42 and 44.)*
- **SP3 — order-sensitive reverse case is recorded.** The note states that `-F`/`-N` **after** an action flag yields genuine field enumeration (exit 0 **and** stdout ≡ the plain field-list baseline), and that the action flag **after** `-F`/`-N` yields that action's own output. *(Absent; the addendum gives only the first direction.)* Vector: `--list-boots -F PRIORITY` → rc 0, stdout sha ≡ `-F PRIORITY` alone (today `97477348840c310c`, 12 B); `-F PRIORITY --list-boots` → rc 0, stdout sha ≡ `--list-boots` alone (today `3ea80f5652bbfdcb`, 262 B).
- **SP4 — guard-suppression case is recorded.** The note states that an action override **after** `-F`/`-N` can *suppress the scope rejection entirely*, so `limiter + -F + action-flag` exits 0 rather than 1. Vector: `-b 0 -F PRIORITY --list-boots` → rc **0**, stdout ≡ `--list-boots` alone, stderr 0 bytes. *(Absent — the addendum implies the guard still governs; it does not.)*
- **SP5 — the third error class is recorded.** The note records the `--merge` conflict as a distinct failure text with its own exit code and byte count, distinct from both the scope rejection and the extraneous-argument error. Vector: `--list-boots --merge` → rc 1, stderr exactly 60 bytes, sha `83e17587301b7e27`, text `Using --boot or --list-boots with --merge is not supported.` *(Absent.)* Anchor A7 `:962-964`.
- **SP6 — the `--namespace=` WORK row is reconciled.** Either the note drops `--namespace=` from the WORK row, or it qualifies it: cell `live_namespace` (A5 :1069) records `stdout_bytes: 0, stderr_bytes: 29` — exit 0 with **no** field list and a stderr diagnostic. Today: `-F PRIORITY --namespace=x` → rc 0, stdout 0 bytes, stderr 29 bytes `No journal files were found.`. *(Currently violated: note line 43 says WORK on that cell.)*
- **SP7 — the `--boot=all` scope-cancellation is recorded.** The note states that `--boot=all` after `-b`/`--boot=`/`--this-boot` **clears** the boot filter term (`arg_boot_filter = r > 0` with `parse_id_descriptor("all") == 0`, A7 `:520-525`, `:163-168`), so the guard does not fire and the enumerated scope widens. Vector: `-b 0 --boot=all -F PRIORITY` → rc 0, stdout sha ≡ plain `-F PRIORITY`; and the PRIORITY value set widens from `{3,4,5,6,7}` (boot 0) to `{2,3,4,5,6,7}` (all boots). *(Absent everywhere — my finding.)*
- **SP8 — the counter asserts table state, not phrases.** The counter must fail when the decision table still classifies an action-assigning option as WORK. Concretely, mutation A above (row 42 → `**WORK — field enumeration works**`) must exit 1. *(Currently exits 0 — §5.)*
- **SP9 — the counter asserts output identity, not exit code.** The counter must compare a candidate invocation's stdout sha256 against a **same-run** baseline invocation, never against a pinned sha or byte count. Rationale: the field-list sha changed between r36 and today (`d0f6353ae541a724` → `97477348840c310c`) with the same value set `{2,3,4,5,6,7}` merely reordered, and the boot-table size changed 541 → 262 B. *(The landed counter asserts neither, so it is vacuous on this axis; but any future counter must not pin hashes.)*
- **SP10 — the addendum appears exactly once.** The note contains exactly one `## Round 37 correction` heading, and the counter must fail on a note containing two. *(Currently 2 — D4.)*
- **SP11 — no stale byte counts asserted as current.** The note must not present 541 (or any host-specific byte count) as a current measurement without marking it a dated snapshot; and any counter asserting byte counts must derive them from the bound revision's recorded cells, not from the host.

### 6.2 Should-fail (each must make the counter exit non-zero)

- **SF1 — base note.** `--revision 564db0b614` (note without the addendum) → exit 1. *Observed: exit 1 with 14 findings.* ✅ already satisfied.
- **SF2 — table still WORK.** Note with the addendum present but decision-table row 42 reading `**WORK — field enumeration works**` → exit 1. *Currently exits 0 — §5 mutation A.*
- **SF3 — action override described as WORK.** Addendum text that says the override "selects the field enumeration action" instead of "replaces it with `ACTION_LIST_BOOTS`" → exit 1. *Already in the landed selftest as `action-overwrite-called-work`.* ✅
- **SF4 — reverse order missing.** Addendum that documents only the `-F … --list-boots` direction and not the `--list-boots -F PRIORITY` reverse → exit 1. *(Not in the landed selftest; the landed selftest has 7 cases, none for order.)*
- **SF5 — guard-suppression missing.** Addendum that omits the `limiter + -F + action-flag → exit 0` case → exit 1. *(Not covered.)*
- **SF6 — merge-conflict class missing.** Addendum that omits the 60-byte `--merge` conflict → exit 1. *(Not covered.)*
- **SF7 — `--boot=all` cancellation missing.** Addendum that still asserts `--boot=all` merely "sets no boot filter" without the cancellation → exit 1. *(Not covered.)*
- **SF8 — duplicate addendum.** Note containing two `## Round 37 correction` blocks → exit 1. *(Currently passes — §4 D4.)*
- **SF9 — counter only greps phrases.** A counter implementation that greps for the 13 required substrings and never inspects the decision table must **not** pass SF2 — i.e. the selftest must include a "table-still-WORK" case and fail it. *Currently absent: the landed selftest's 7 cases are all phrase mutations; none touches the table.*
- **SF10 — counter pins a sha/byte count.** A counter that asserts `stdout_sha256 == d0f6353ae541a724…` or `stdout_bytes == 541` must fail its own selftest on a same-day re-run, because the field list is reordered and the boot table resized. *The landed counter correctly pins only the *r36-recorded* `-N` sha `3480f2aa…` (2882 B, identical across r36 and today) — that one is stable because the field-name list is sorted; the `-F` value list is not.*
- **SF11 — wrong term count / missing `-n` states / missing prior-teaching acknowledgement.** Already covered by the landed selftest (`wrong-term-count`, `missing-f-truncation`, `missing-n-unchanged`, `prior-teaching-omitted`). ✅

---

## 7. Limits, gaps, and what I did not do

- **I did not author the change.** No edit to the note, the counter, `SCORECARD.md`, or any tracked file. The corrections in §6 are specifications for the authoring seat.
- **I did not run the C1/C3 counters, the census, or any gate.** I ran only: `tools/check-journalctl-v262-corrections.py --revision <rev>` and `--selftest` (read-only, exit codes observed), plus `git log`/`show`/`status`/`ls-files` reads.
- **Mutation experiments** were run on copies in `/tmp/c2probe` (tool + note copied out); the lane tree was not modified. `git status --porcelain` after all work shows only pre-existing untracked wave artifacts and `tools/probe-child-env-allowlist-r37.py` — none mine.
- **S198 (`journalctl(1)` at 262.1) could not be re-opened this round**: `https://man.archlinux.org/man/journalctl.1` failed with a TLS error on two attempts. I therefore do **not** claim the S198 quote was re-verified; the lane's tracked local copy was read instead and is cited as such. This is a source-availability gap for the round, not a claim.
- **Byte counts and shas are host- and time-dependent.** The boot-table size moved 541 B (r36) → 262 B (today); the field-list sha moved `d0f6353ae541a724` → `97477348840c310c` on the same value set reordered. Every equality claim above is a **within-run** comparison against a same-run baseline; none is a pinned constant.
- **Not verified**: behaviour on any systemd build other than this host's `262 (262-1-arch)`; whether upstream changed the option→action map after v262 (the note's `recheck: on-release` stands); whether `--boot=all` cancellation is intended upstream behaviour or a bug in v262 (source-level fact only; I make no upstream-causality claim — consistent with the round's "errno discrimination without inflating novelty or historical causality" theme).
- **Sibling overlap**: `C24ActionOverride12.md` (item 4/8) and `Build7C239` (item 7/12) attack the same action-override target. My independent contributions are §3.3 (`--boot=all` cancellation — not in either), §5 (the counter's table-blindness mutation proof — not in either), and §4-D4 (the duplicated addendum). Their SP/SF sets are not restated.
- **The lane's own r36 matrix (`matrix-mini.json`) is retained as history** and must not be edited; where its recorded shas are now stale I say so rather than correcting it.

---

## 8. Bottom line for the parent

1. The C2 **action-override classification** requirement is testable but was under-specified (flag set, placement in the table vs addendum, observable), and the landed artifact does not satisfy it in substance: **the WORK rows for `--list-boots`, `--disk-usage`, `--header`, `--sync` are still in the note's decision table (lines 42, 44)**, and there is **no action-override row in that table**.
2. The declared counter `tools/check-journalctl-v262-corrections.py` **cannot detect this** — it is a prose-token gate; mutation A (row 42 strengthened to "WORK — field enumeration works") still exits 0.
3. The landed note contains the addendum **twice** (lines 129 and 158) with a one-phrase divergence; the counter's PASS depends on the first copy's wording, so a de-duplicated note with the second copy's wording would fail.
4. **New, unreported behaviour:** `--boot=all` **cancels** a previously-set boot filter (`arg_boot_filter = r > 0` with `parse_id_descriptor("all") == 0`), so `-b 0 --boot=all -F PRIORITY` exits 0 and enumerates *all* boots (`{2,3,4,5,6,7}` vs boot-0's `{3,4,5,6,7}`). It is a scope-axis override, not an action-axis one, and appears in neither the critic nor the landed note nor the counter. It also shows `--boot=all` is not merely "sets no boot filter".
5. Also still uncorrected: the `--namespace=` WORK row points at a cell whose recorded stdout is **0 bytes** with a 29-byte stderr diagnostic; and the `--merge` conflict (60-byte, `83e17587301b7e27`) is a third error class the note never records.

**Verification owed by the main agent after integration (not run here):** the C2 counter at the bound revision (exit 0) and at the r37 base (exit 1); the counter's selftest with the new SF2/SF4/SF5/SF6/SF7/SF8 cases; and a table-level re-read of note lines 42/44/43 confirming the WORK rows are gone or qualified.

Report: .ufo/waves/round-37/w1/C28ActionOverride16.md
