# RevGateSchema-2: C2 counting rule and gate schema, re-review at landed HEAD 22fd164 (2026-10-22)

Verdict: the landed gate counts 5 of 5 at HEAD 22fd164, but the count measures well-formed anchors, not supported verdicts. An irrelevant source, an anchor unrelated to its premise, and an unused duplicate registry row all still pass, and a value-section rule gives 4 of 5 on the same committed bytes.

Labels: [obs] observed in a file or command output, [inf] inference, [unk] unknown. Probe labels M0–M9 name the mutation runs in section 3; finding labels N1–N13 name the findings in section 4.

## 1. Round-1 findings, status at HEAD 22fd164

| # | Round-1 attack | Status now | Evidence |
|---|---|---|---|
| 1 | Verdict `unverified` counted | Closed | `tools/check-pause-gate.py:35` (COUNTED = cleared, still-holds, changed); `:112` rejects other verdicts; probe M7 exits 1 with 4 of 5 [obs] |
| 2 | Generic evidence substring | Closed for anchors; anchor role still open | `:36` (BOILERPLATE), `:122-126` (an anchor must be a non-boilerplate capture needle occurring exactly once), `:144` (needle of at least 3 characters) [obs]; see N1 and N4 |
| 3 | Source opened today but irrelevant; rejected or duplicate rows | Status, used-by and duplicate checks closed (`:151-158`; probes M5 and M6 exit 1); relevance still open | probe M2 passes; see N2 |
| 4 | `premise` and `limits` unvalidated | Presence and a length of at least 10 characters closed (`:113-115`); content still open | probe M4 passes; see N8 |
| 5 | Section fit | Open: the committed checker has no section check | probe M3 passes; see N1(a) |
| 6 | Content contradicted by the capture | Fixed in the landed JSON: P1 now carries 3 pending rows and 134 checkupdates rows; P5 says the cache holds no package files | `corpus/knowledge/pause-lift-gate-r24.json` P1 and P5 limits [obs]; new items in N9 |
| 7 | Exit code conflates malformed with an honest short count | Open: status derives from the exit code only (`tools/check-pause-gate.py:250`), and findings do not change the exit code (`:166`) | probe M8; see N5 |
| 8 | After-value 5 unreachable | Superseded: HEAD reaches 5 of 5 | official run in section 2 [obs] |

## 2. Official evidence at HEAD 22fd164

- `python3 -B tools/check-pause-gate.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0`: exit 0, status PASS, premises_verified 5, premises_total 5, findings empty [obs].
- `python3 -B tools/check-pause-gate.py --selftest`: status PASS, 24 cases, 0 failed, exit 0 [obs].
- Tracked at HEAD [obs from `git ls-files`]: `corpus/knowledge/pause-lift-gate-r24.json`; `corpus/SOURCES.md` with 17 new rows S087 to S103 at lines 93 to 109, all status `mined`, opened `2026-10-22`, and used-by naming the gate file; `.ufo/waves/round-24/capture/l1-4/capture.txt` (378 lines, sha256 `87f70f82f05956ce5de60abe8bfdd748f38d716483a491cfe7c183939884a56f`); its sidecar `capture.sha256`, which names `capture.txt` only; and `.ufo/waves/round-24/capture/l1-4/checkupdates.out`.
- The ScribeGateEntry draft at `.ufo/waves/round-24/w1/ScribeGateEntry/pause-lift-gate-r24.json` has 53 pointers, placeholder ids `S0NN-…` and list-valued limits. On the same checker it exits 1 with 0 of 5 [obs]. It must not replace the landed file.

## 3. Mutation probes on committed bytes

Each probe changes one field of the landed gate in memory and runs the committed `evaluate()` against committed bytes. No file was written [obs].

| Probe | Change | Exit | Verified | Reading |
|---|---|---|---|---|
| M0 | none | 0 | 5/5 | landed state |
| M1 | P2 evidence reduced to capture line 74 (`libinput-tools 1.32.0-1`) | 0 | 5/5 | P2 "cleared" passes with no pointer to its zero result |
| M2 | P2 sources replaced by S098 (btrfs-overlayfs hook; mined, opened today, used-by the gate) | 0 | 5/5 | an irrelevant source passes |
| M3 | P2 anchored on capture line 277 (a foreign-package line from the P5 section) | 0 | 5/5 | no section fit |
| M4 | P5 limits replaced by `limits text` (11 characters) | 0 | 5/5 | the length rule is a floor, not content |
| M5 | duplicate S092 row, opened 2026-10-19, placed before the original | 1 | 4/5 | caught |
| M6 | S092 status flipped to `rejected` | 1 | 4/5 | caught |
| M7 | P1 verdict `unverified` | 1 | 4/5 | caught |
| M8 | duplicate S001 row (stale copy first); no premise cites S001 | 0 | 5/5 | exit 0 with `GATE-SOURCE-DUPLICATE:S001` in findings; status is derived from the exit code, so the printed status is PASS [obs; the status derivation is read from `tools/check-pause-gate.py:250`] |
| M9 | P2 anchored on the command echo at capture line 58, with the `$ ` prefix removed from the needle | 0 | 5/5 | an instrument line anchors a verdict |

Value-section rule on the same bytes [analysis, using the committed BOILERPLATE list and uniqueness rule]: eligible anchors are P1 lines 40, 53, 374, 375, 376; P3 lines 93, 94, 117, 328, 340, 349; P4 lines 194, 221, 354, 363; P5 lines 122, 270, 281, 297, 317. P2 has none. Four of five premises have an eligible anchor.

Selftest status: the committed checker's own 24 cases pass, including `unverified-not-counted`, `empty-limits`, `boilerplate-only`, `source-rejected` and `source-other-entry` [obs].

## 4. New findings

**N1 (HIGH). Anchors are checked for existence, not for role.** The committed rule requires one unique, non-boilerplate capture line per premise (`:122-126`), but nothing ties that line to the premise's claim. P2 claims a zero: no installed package is newer than its sync entry. Its probe is capture lines 57 to 59, which print nothing: line 57 is the section header, line 58 the command echo, line 59 `exit=0` [obs]. The committed P2 pointers are lines 57, 73, 74 and 88. None is the probe's command or exit line, so no pointer shows the empty output, and line 74 (`libinput-tools 1.32.0-1`) passes as the anchor (M1). The same gap affects other zero claims. P5's "the cache holds 0 package files" rests on the header at line 284 and the directory name at line 297. The zero itself is line 286, and the length rule blocks anchoring a one-character value. The `total 0` at line 291 is the block total printed by `ls -la`, not a file count [inf].
 Required: (a) a per-premise value-section set, with at least one eligible anchor from it. Suggested sets: P1 {pending, pending-count, pending-repos, checkupdates-temp-db}; P2 {local-newer-than-sync}; P3 {hooks-new-root, buildroot-symlink, init-root, boots, boot0-root-mount, plymouth-boot0, plymouth-boot-1, loader-entry, cmdline-boot-flags, boot-chain-installed}; P4 {sync-db-mtime, sync-db-ctime-birth, stable-mirror-headers, mirror-servers, repo-servers, pacman-log-last-sync, pacman-commands-since-pause}; P5 {cache-entries, cache-package-files, sudo-package-commands-since-pause, paccache-runs-since-pause, pacman-log-since-pause, pacman-commands-since-pause, foreign-new, snap-pac, snapper-list}. (b) A zero form: a command echo line N beginning `$ ` and an `exit=` line at N+1, with no lines between. For P2 that is lines 58 and 59. (c) An exact-line form for one-token values: the pointed line must equal the value, and the line two or fewer lines above it must be a command echo. Under (a) alone the committed count is 4 of 5. Under (a) with (b) it is 5 of 5, and P2 is evidenced by transcript adjacency, which is the honest form of an absence claim [inf on fidelity of the transcript].

**N2 (HIGH). Source relevance is not bound to the premise.** A registry row that is mined, opened 2026-10-22 and lists a gate file in used-by passes for any premise that cites it (M2). The 17 used-by cells name the gate's `.json` and `.md` files and no premise id (`corpus/SOURCES.md:93-109` [obs]).
 Required: used-by names the premise id (for example `pause-lift-gate-r24#P2`), and the checker verifies that each premise citing a source appears in that source's used-by cell. Until the cells are edited this rule drops the landed count to 0. Whether a row's teaching supports its premise remains reviewer judgement.

**N3.** Folded into N1(a). Section fit is absent (M3).

**N4 (MEDIUM). Boilerplate is tested on the needle, not on the captured line** (`tools/check-pause-gate.py:36`, `:123`). Removing `$ ` from the needle lets a command echo anchor a verdict (M9).
 Required: test the captured line's prefix, `lines[line-1].startswith(BOILERPLATE)`, and reject any such line as an anchor.

**N5 (MEDIUM). Findings do not change the exit code or the status.** `ok` ignores findings (`:166`), and `main()` derives status from the exit code (`:250`). M8 returns PASS with a finding.
 Required: any finding forces exit 1 and status FAIL. The claim's comparison must read status, premises_verified and findings together, not premises_verified alone.

**N6 (MEDIUM). Non-capture evidence is accepted and unpinned.** P1's ca-certificates limit points at `.ufo/waves/round-24/capture/l1-4/checkupdates.out` line 6 (`ca-certificates-mozilla 3.131-1 -> 3.131.1-1`) [obs]. The sidecar pins `capture.txt` only [obs], so this file's bytes can change without the gate noticing.
 Required: reject non-capture pointers, or pin each referenced file's sha256 in the gate.

**N7 (MEDIUM). Counts in the text are only partly enumerated.** P5 says "six paccache -r runs"; the capture has six such lines (241, 246, 266, 267, 268, 269) and the gate cites one, line 266 [obs]. P5 says "two pacman -Scc runs"; it cites line 270 and not 271. P1 says "3 pending"; it cites line 40 of the three pending rows (40 to 42) and line 53 of the three repository lines (52 to 54).
 Required: cite every counted line, or reword to the count the pointers show.

**N8 (LOW). The length rule accepts filler.** `limits text` passes (M4). Content is reviewer judgement, and the claim wording should say so.

**N9 (LOW, content). Landed text that the capture does not support as written.**
- P5 limits say "no -S or -Su" in the same sentence family as "two pacman -Scc runs (04:10)" (capture lines 270 and 271). `-Scc` is an -S-family run, so the sentence needs "no -S <package> install" [obs].
- P3 limits say plymouthd "wrote boot.log into the real root at 04:55:44". Capture line 321 shows the boot.log mtime and line 142 shows the plymouthd PID, but no pointer attributes the write to plymouthd [inf].
- P5 limits say "4 empty download directories". Emptiness is inferred from size 0 on btrfs and no line lists the directory contents [inf].
- P1 and P4 contain absence claims (no mkinitcpio, linux or plymouth change pending; core, extra and multilib not rewritten). They are bracketed by output, not pointed to, and need N1(b) if kept [obs].

**N10 (LOW). One number hides the verdict mix.** Four of five verdicts are `changed`, and the checker cannot tell `changed` from `still-holds`. The claim output should print the verdict histogram beside premises_verified.

**N11 (LOW). Reproducibility and quote checks.** Three registry rows use mutable `master` URLs: S098 (`gitlab.com/Zesko/limine-entry-tool/-/raw/master/...`, `corpus/SOURCES.md:104`), S100 (`raw.githubusercontent.com/omacom/omarchy-mirror/master/README.md`, line 106) and S102 (`raw.githubusercontent.com/basecamp/omarchy/master/bin/omarchy-snapshot`, line 108). The `opened` cells are self-attested; no tool records access. The lane's located-quote requirement (at most 25 words, copied exactly) has no mechanical check [unk for each quote].

**N12 (BOUNDARY, needs an L1 ruling). The 134-row figure comes from a network sync into a scratch database.** Capture lines 372 to 377 run `checkupdates` with `CHECKUPDATES_DB` under `/fast/scratch`. The SOURCES row S009 says checkupdates syncs a separate temporary database [obs from `corpus/SOURCES.md`]. The contract's read-only list names `pacman -Q*`, `-Si` and `-Sl` against existing databases, and `curl`; it does not name checkupdates, and it forbids `pacman -Sy` [obs]. The host database is not touched [inf]. The L1 must rule whether this is inside the boundary and record the ruling, because P1's `changed` verdict and the limine and systemd findings depend on it.

**N13 (PROCESS). The draft and the landed text disagree.** The ScribeGateEntry draft says the three pending rows are counted "against the host's 2026-10-17 sync DBs". That is wrong for two of the three repositories: `omarchy.db` is dated 2026-10-21 19:44:39 (capture line 34) and `openai-chatgpt.db` 2026-10-20 23:22:02 (line 35). Only core, extra and multilib (lines 31 to 33) carry 2026-10-17 [obs]. The landed text does not repeat the error.

## 5. What the checker must reject so the after-value 5 means something

1. A premise with no eligible value anchor (N1a), and a zero or none claim without the echo-and-exit adjacency form (N1b).
2. An anchor whose captured line begins with `$ `, `### ` or `exit=` (N4).
3. A source not bound to the premise that cites it (N2).
4. Any finding, including a duplicate row for an unused id (N5).
5. Non-capture evidence, unless its sha256 is pinned in the gate (N6).
6. A count in the text that the pointers do not enumerate (N7).
7. The verdict histogram printed beside the count (N10).

Expected results on the committed bytes [analysis]: rules 2 and 4 change nothing for the landed JSON. Rule 5 changes nothing once the checkupdates.out sha is added. Rule 3 drops the count to 0 until the used-by cells are edited. Rule 1(a) alone gives 4 of 5. Rule 1(a) with the P2 echo-and-exit pair gives 5 of 5, with P2 evidenced by absence. Only the last outcome means that each verdict has a value-bearing capture line.

## 6. Corrections to my round-1 report

- Round-1 finding 2 demanded that every pointer be unique. That was too strict. Only anchors need uniqueness, and the committed checker enforces that. The real gap is anchor role (N1, N4).
- Round-1 finding 6 said the three pending rows were counted against the 2026-10-17 databases. Only three of the five databases carry that date (N13).
- Round-1 finding 8 is superseded: HEAD 22fd164 reaches 5 of 5.

## 7. Verification gaps and residual risk

- I ran no host probe. Every host fact comes from the committed capture. The sha256 pins those bytes, not the host state at capture time [inf].
- I spot-checked one source. `curl -s` of the S099 raw file (libalpm dload.c at commit 54d9411, exit 0) shows the If-Modified-Since request built from the local file's mtime (lines 419 to 425) and the downloaded file's mtime set to the server's time (line 704). That supports the P4 mechanism. I did not re-open the other 16 rows.
- The ScribeGateEntry draft and the ExecPauseGateChecker draft report their own results. The ExecPauseGateChecker integration run uses fixture premise text ("P1 fixture premise on real capture"), so it does not exercise the landed gate's text [obs].
- Mutation results show what the rules accept on committed bytes. They do not show what a future commit would produce.
- Residual risk after N1 to N5 are fixed: the count measures well-formed anchors plus a reviewer's judgement of role. The checker cannot judge whether a `changed` verdict is correct.

## 8. Draft implementation check (ExecPauseGateChecker draft, 2026-10-22)

I ran the draft at `.ufo/waves/round-24/w1/ExecPauseGateChecker/check-pause-gate.py` in memory against working-tree bytes. Confirmed working: the pins map verifies P1 once `checkupdates.out` is pinned; per-premise used-by binding flags every row without `#Px`; the value-section rule rejects P2's committed pointers (`no-value-anchor`); a needle with the `$ ` prefix stripped is rejected through the captured-line test (`evidence-line-boilerplate`, probe V3); the echo-and-exit pair is accepted when it is the pointer set (probe V2b: P2's only remaining problems were two source rows my synthetic registry had not bound); the verdict histogram is printed.

Two defects:

- **D1 (HIGH). Non-anchor pointers are held to anchor-grade uniqueness and line purity** (draft `:337-349`). Every pointer with a needle occurring more than once in the file, or sitting on a `$ `-prefixed line, is a premise failure, not merely anchor-ineligible. Identical twin lines then become uncitable: capture lines 63 and 79 are both exactly `mkinitcpio 42.2-1`, and 139/152 are both `Started Show Plymouth Boot Screen.`, so no substring can cite either twin. On the current gate text this fails P3 (two twin needles plus the `$ stat` pointer at line 321), P4 (`/var/lib/pacman/sync/core.db` occurs at lines 31 and 354) and P5 (the `### cache-package-files` pointer and the paccache line occurring at 266 and 302). Required: uniqueness and line purity must gate only anchor eligibility and the zero pair, as in the landed checker; a non-anchor pointer needs only to resolve. A section-scoped uniqueness (count within the pointer's own section) would be an acceptable alternative.
- **D2 (LOW). The draft's `CAPTURE_PATH` constant names `capture/l1/capture.txt` while `evaluate` pins `capture/l1-4/capture.txt`.** The stale constant misled my first probe and will misdirect any importer. Derive both from one constant.

Tree drift during this check [obs]: `corpus/` is modified uncommitted on HEAD `22fd164`; the registry now ends at S114 (114 rows), and the working-tree gate JSON cites S104–S114. The probes above ran on those working-tree bytes.

Messages sent: a short pointer to this file went to ScribeGateEntry-2 and ExecPauseGateChecker-2. No production file was edited, and no git write was run.

Scope: read=SCORECARD.md round-24 declaration; corpus/lessons/round-23-verifier-spotcheck.md:52,64; corpus/SOURCES.md:93-109 and the registry rules; corpus/knowledge/pause-lift-gate-r24.json and .md (HEAD); .ufo/waves/round-24/w1/ScribeGateEntry/pause-lift-gate-r24.json; .ufo/waves/round-24/capture/l1-4/capture.txt, capture.sha256 and checkupdates.out; tools/check-pause-gate.py and tools/_revision.py at HEAD; .ufo/waves/round-24/w1/ExecPauseGateChecker/integration-pass.json; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w1/RevGateSchema.md (rewritten), and deleted tools/__pycache__/check-pause-gate.cpython-314.pyc (a bytecode cache left by my earlier in-process import; untracked and gitignored); executed=git rev-parse, git log, git ls-files and git status (read-only); sha256sum; wc -l; python3 -B tools/check-pause-gate.py --revision 22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0 (exit 0, PASS 5/5); python3 -B tools/check-pause-gate.py --selftest (exit 0, 24/24); in-memory importlib evaluation of tools/check-pause-gate.py against committed bytes (probes M0 to M9, no writes); curl -s of the S099 raw file (exit 0), grep and jq; importlib evaluation of the ExecPauseGateChecker draft against working-tree bytes (probes V-real, V0, V1, V2a, V2b, V3; no writes)
Installs: none
