VERDICT: supports

# Seat CritSeparability — Item X-4: causal separability attack + no-harm plan

Scope: attack the declaration's separability sentence (`SCORECARD.md:2683-2684` — "C1 touches
`tools/boot-chain-audit.sh` only; C2 touches the r43 entry, the r42 entry's header line,
`corpus/SOURCES.md` and frozen snapshots. Neither counter reads the other's surface."), name every harm
risk in `717b716a8943151ace8657e0ca23d7d9b8434f26` (impl) vs `6951ead90566b2d74f7c45b4efca29246badad64`
(base), and draft the six-axis no-harm checklist at the final tip. Read-only on lane content; no repo
mutation; no guest; the only heavy run was the single required self-assessment run at 717b716a
(27.8 s, exit 1, reported below). Scratch: `/fast/scratch/hyaku/tsukuroi-r43/CritSeparability/`
(removed at finish). Receipts: `.ufo/waves/round-43/w1/CritSeparability/`.

## 1. Separability attack — the frozen counters read disjoint surfaces

**C1 counter `tools/score-bootinputs-r43.py` input surface (full source read, 348 lines).**
- Repo input: exactly `tools/boot-chain-audit.sh` at the revision (`SCRIPT = 'tools/boot-chain-audit.sh'`,
  `:61`, `git show <rev>:<SCRIPT>` at `:263-266`; last line must be `main "$@"`).
- Host inputs: `/proc/stat` btime (`:130-135`), `/etc/subuid`, `/etc/subgid` (`:138-147`), the caller's
  environment minus `TSUKUROI_*/BOOTCHAIN_*/UFO_*/TMPDIR` (`:150-151`), and the live `/etc`,
  `/usr/lib/initcpio`, `/usr/lib/modules` trees for the oracle (`:218-234`).
- No corpus file, no SCORECARD, no `.ufo/waves/round-43/frozen/*`, no dispatch/results JSON is read.
  `grep -nE 'SOURCES|knowledge|scrub|btrfs' tools/score-bootinputs-r43.py` → no hits.

**C2 counter `tools/check-scrub-record-r43.py` input surface (full source read, 339 lines).**
- Repo inputs: `corpus/knowledge/btrfs-scrub-record-r43.md` (`ENTRY`, `:61`), `corpus/knowledge/btrfs-scrub-record-r42.md`
  (`OLD`, `:62`; `pointer_ok` reads its first 20 lines, `:319-321`), `corpus/SOURCES.md` at rev and base
  (`:247-248`), frozen snapshots `.ufo/waves/round-42/frozen/src/scrub.c` and `.ufo/waves/round-43/frozen/src/ioctl.c`
  digest-gated (`SNAP`, `:65-70`), `.ufo/waves/round-43/frozen/hostcap/capture.txt` digest-gated (`:71-72`),
  `.ufo/waves/round-43/{w2,residual}-{dispatch,results}.json` and `w2/<name>.md`/`residual/<name>.md`
  (`bound`, `:178-195`), plus `~/.omp/agent/sessions` transcripts (reported outside the predicate, `:41-42,294`).
- No boot-chain script, no C1 counter, no control files are read. `grep -nE 'boot-chain-audit|bootinputs|BOOTCHAIN'
  tools/check-scrub-record-r43.py` → no hits.

**Nothing written by either counter.** C1 writes only under `--scratch` (tmpfs namespace, selftest TMPDIR);
C2 "Writes nothing" (`:49`). Neither runs git add/commit. The only shared infrastructure is the lane's git
object store (both run `git show`/`git grep` read-only) and host `/proc`/subuid files — not claim surfaces.

**What each claim changed (freeze fe357001 → impl 717b716a, `git diff --name-status`):**
- C1 surface: `tools/boot-chain-audit.sh` (M) + its before receipt `.ufo/waves/round-43/before/c1-before.jsonl`.
- C2 surface: `corpus/SOURCES.md` (M), `corpus/knowledge/btrfs-scrub-record-r42.md` (M, header pointer),
  `corpus/knowledge/btrfs-scrub-record-r43.md` (A), before receipt `c2-before.jsonl`.
- Declaration/controls/` files were already committed at the freeze (fe357001), before any seat.

Conclusion: the declared separability claim is supported. Neither counter reads the other's surface;
each claim is verifiable independently at the tip (C1's predicate depends on the script bytes and host
state only; C2's predicate depends on corpus/frozen/wave-2 bytes only). Caveats recorded (all already
declared): C1's namespace legs leave mount-table/uid_map/script-path channels open (declaration line
2666-2668, control K7), and C2's verdict conjuncts need wave-2 artifacts that do not exist at 717b716a
(they are scored later, per the counter docstring `:20-30`).

## 2. What 717b716a changed (diff summary)

`git diff --stat base impl` → 50 files, +14761/−8; `git diff --name-status base impl` → **0 deletions,
0 renames**; only 4 tracked files modified:
- `SCORECARD.md` +38/−0 (pure append; the round-43 declaration section; `diff-SCORECARD.md.txt` shows a
  single `@@ -2644,3 +2644,41 @@` hunk with no `-` lines).
- `corpus/SOURCES.md` +3/−1: S237's `used-by` cell extended with the r43 entry (every other cell byte-
  identical, `diff-corpus_SOURCES.md.txt`); S240 and S241 added. Row set at impl − base = {S240, S241},
  removed = {} (`SOURCES-impl.md` vs `SOURCES-base.md`).
- `corpus/knowledge/btrfs-scrub-record-r42.md` +1/−0: header line 9 `superseded-in-part: round 43 ...`
  (pointer, marked).
- `tools/boot-chain-audit.sh` +30/−7: new helper `inputs_newer_than` (:463-481) and `boot_inputs_newer`
  call-site rewrite (:491-499), plus three `R43-C1` selftest cases (:1225-1240). No other function body
  changed (kill rule intact).
All other 46 files are new (frozen snapshots, captures, controls, counters, before receipts, entry).

## 3. Harm risks found in the change (named)

- **R1 (new, calibration surface): K07 breaks at impl.** `python3 tools/check-self-assessment.py --revision
  717b716a` (read: tool `:591-597`; run once, receipts `selfassessment-impl.json`) exits 1, mismatches 2:
  K07 depth-row notes 63 vs observed 64 (the new `btrfs-scrub-record-r43.md` is the +1); K10 lessons 60 vs
  observed 61. K10 is pre-existing at base (lessons = 61 at base and impl, table unchanged — the question
  was already red before this commit); **K07 is newly introduced by this commit** because the base notes
  count was exactly 63 (matching the round-42 table) and the commit adds the 64th note without amending the
  axes-table depth row.
- **R2 (low): helper semantic edges.** `inputs_newer_than` prints 0 whenever `find` lists nothing, even if
  find exited 1 (e.g. a start point inside an unreadable parent). That is the intended, oracle-consistent
  behavior (the independent Python walk skips unreadable dirs the same way, `score-bootinputs-r43.py:218-234`),
  but it means "no newer input" and "could not read" are indistinguishable — already declared as the mount-
  table/open-channel limit, not a new fail-open.
- **R3 (low): new selftest cases rely on GNU `touch -d @<epoch>`** (host GNU coreutils present; same
  pattern already in the harness).
- **R4 (none): SCORECARD history untouched** — zero deletions, append-only declaration, no "measured
  outcome" heading added (so no ordinal reference line is shifted; K01–K06 passed in the run).
- **R5 (none): SOURCES existing rows untouched** beyond S237 used-by (CORPUS rule 2 mutable field); census
  clean (below).
- **R6 (none): frozen pins intact and marked** — impl blobs match every declared sha256 (counters
  886f92c8…/b4602c56…, control scripts 8eb69171…/75648627…, candidate 3e5c8763…, ioctl.c 7b3488f2…,
  capture.txt f7ecbe7c…, scrub.c 48df2e2f…); FETCH.txt + SHA256SUMS committed beside ioctl.c; r42 header
  marks the supersession; freeze fe357001 is an ancestor of impl (rc 0).
- **R7 (none): no host mutation** — diff touches only lane files; capture.sh is read-only and unprivileged.

## 4. No-harm checklist — six axes at the final tip

Placeholders: `L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`; `B=6951ead90566b2d74f7c45b4efca29246badad64`;
`T=<final tip revision>` (717b716a today); `S=/fast/scratch/hyaku/tsukuroi-r43/CritSeparability/check` (mkdir -p).
Each block lists the command whose *clean* output shows no harm on that axis.

**depth**
- `python3 $L/tools/check-scrub-record-r43.py --revision $T` → exit 0, `rows=3 quotes_ok=3 props_ok=3 host_ok=3 sources_ok=1 verdicts_ok=3 novelty_base_hits=0 pointer_ok=1` (C2 counter; wave-2 verdicts bound).
- `git -C $L ls-tree -r --name-only $T -- corpus/knowledge/ | grep -c '\.md$'` equals the axes-table depth-row stated note count (today 63; amend to 64 or K07 stays red).
- `git -C $L diff --diff-filter=D $B $T` → empty; `git -C $L diff $B $T -- corpus/knowledge/ | grep -c '^-[^-]'` → 0 (no knowledge line rewritten/deleted).

**coverage**
- `git -C $L diff $B $T -- PROVINCE.md SHONEN.md SKILL.md corpus/README.md` → empty (no covered surface touched).
- `git -C $L diff --name-only $B $T | grep -vE '^(\.ufo/waves/round-43/|tools/(score-bootinputs-r43.py|check-scrub-record-r43.py)|corpus/knowledge/btrfs-scrub-record-r43.md|corpus/knowledge/btrfs-scrub-record-r42.md|corpus/SOURCES.md|SCORECARD.md|tools/boot-chain-audit.sh)$'` → empty (no change outside the declared surfaces).

**operability**
- `python3 $L/tools/score-bootinputs-r43.py --revision $T --scratch $S/c1` → exit 0 with `cases=16 correct=16 identity_ok=1 live_agree=1 selftest_pass=1 selftest_r43>=2`.
- `TMPDIR=$S/st bash $L/tools/boot-chain-audit.sh --selftest` → `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=48 failed=0` (three R43-C1 cases green).
- `git -C $L diff $B $T -- tools/boot-chain-audit.sh` shows only the helper, its call site and the three selftest cases (verified at 717b716a; no other function body changed).

**freshness**
- `git -C $L diff $B $T -- corpus/SOURCES.md` → only S240/S241 insertions and S237's used-by cell; `git -C $L diff --diff-filter=D $B $T` empty.
- Census over the committed bytes (`git -C $L show $T:corpus/SOURCES.md`): rows 241; malformed 0; duplicate ids none; mined used-by paths 0 missing (exact tree membership); tiers A=226 B=5 C=10; status mined=215 queued=5 rejected=21 (observed at 717b716a, `SOURCES-impl.md`).
- S240/S241 `opened` = 2026-10-26 (not future); capture timestamps precede the receipts.

**calibration**
- `python3 $L/tools/check-self-assessment.py --revision $T` → exit 0, `mismatches=0` (currently exit 1: K07 new, K10 pre-existing — amend the axes table so both pass before close).
- `git -C $L diff $B $T -- SCORECARD.md | grep -c '^-[^-]'` → 0 (append-only; historical rows byte-identical), K01–K06 ordinal consistency included in the self-assessment run.

**adjacency**
- `git -C $L diff $B $T -- PROVINCE.md SKILL.md SHONEN.md corpus/README.md` → empty (no sibling-pointer or inbound/outbound drift).
- K16–K23 (capabilities rows and SHONEN boxes name only existing paths at the revision) pass inside the self-assessment run.
- No "measured outcome" heading added (no ordinal move recorded), so no adjacency-claim harm.

## 5. Evidence index
- Receipts: `.ufo/waves/round-43/w1/CritSeparability/{selfassessment-impl.json, name-status.txt, numstat.txt,
  SOURCES-base.md, SOURCES-impl.md, tree-at-impl.txt, diff-*.txt}`.
- Key observed outputs: self-assessment exit 1 (2 mismatches, K07/K10, `selfassessment-impl.json`); digests
  above (§3 R6); census histogram above (§4 freshness); row-set delta {S240, S241}; freeze→impl delta (§1).
- Unrun: the frozen C1/C2 counters themselves (other seats' verification; not this seat's job), and any
  second self-assessment run (single run executed as assigned).
