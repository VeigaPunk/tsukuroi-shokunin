status: complete
verdict: attacked — 8 defects (3 high: D2 answer key, D3 lexical-only channel, D6 declaration sizing; 3 medium: D4 selftest self-reference, D5 predicate accepts a denial, D9 landed-row fabrication surface; 2 low: D8 rejection class, D11 frozen UL4 text); D1/D7 held, D10 closed at the landing

# K1Critic — round 73 declaration attack (L2 seat, w1)

Report target per the seat spec: `.ufo/waves/round-73/w1/K1Critic.md` (this file). Binding copy in
`w1/K1Critic/K1Critic.md`. Evidence transcript: `w1/K1Critic/evidence/attacks.txt`.

## Scope and instruments observed

- Declaration `749371321c00f04d98c29d2c26b57d75a92d7e37`, base `eb1057575d5d8b940c4846e21611674cf5571aea`;
  lane HEAD at read `8eeadcb9`.
- `tools/count-ul-rows-r73.py` — declared sha256 `542f9c29…0711a3d6`; at my first runs the working
  bytes and the blob at `74937132` both hashed to that value. It then moved with the landing:
  `542f9c29…` → `84501ab8…` (EMPTYQUOTE, `MIN_QUOTE_WORDS=4` + twelfth selftest case) →
  `97f6f5ec…` (exit-map docstring), all recorded at SCORECARD.md:5934-5952; sections 1-11 below
  used the declared `542f9c…` bytes, the Addendum re-ran every attack on `97f6f5ec…`.
- `tools/check-r72-routed-r73.py` — declared `93f034e3…02a2f9e` (verified: the blob at `74937132`
  hashes to it), but **the working tree changed at 23:12:19** to `328a6bf6…531a03fe` (+125/−48) with
  no commit yet. The appended SCORECARD block `## Round 73 — C2 instrument repair` (SCORECARD.md:5869)
  records the change and the attacks that motivated it. My C2 runs therefore come in pairs: the frozen
  blob (reconstructed from `git show 74937132:…` under a scratch `gitdir` shim) and the current bytes.
- **The round then landed while this report was being written.** At `09dac09f`/`583eea87` the
  instruments moved again and were committed, and `3efb9b24` appended the measured outcome: counter
  `542f9c29…` → `84501ab8…` (EMPTYQUOTE) → **`97f6f5ec…`** (exit-map fix); checker `93f034e3…` →
  `328a6bf6…` (hardening) → **`71931c1c…`** (exit-map fix); SCORECARD.md:5934-5952 is the old→new
  chain. At `583eea87` both counting commands read their targets (`met=1` rc 0;
  `ROUTED_STALE=0 ROUTED_OK=3/3` rc 0) and the before controls with the final bytes still read
  `rc=128` / `ROUTED_STALE=3`; selftests 12/12 and 11/11. **Every attack below was re-run against the
  final bytes** (Addendum); sections 1-11 record the observations at 23:06-23:17, the Addendum records
  what the landing did and did not close.
- All fixtures were built under `$TMPDIR=/fast/scratch/hyaku/tsukuroi-r73/K1Critic`; the lane was read
  only; no unit was started, stopped, enabled, disabled, masked or edited; no git mutation was run in
  the lane. Scratch deleted before yield. No tool installed or upgraded.
- Re-measured host readings (read-only) match `before/host.txt` exactly: 12 unit-path directories,
  `passim.service` and `systemd-networkd-wait-online.service` masked, `user@1000.service` DropInPaths
  both `/usr/lib/.../10-login-barrier.conf` and `/etc/.../faster-shutdown.conf`, `getty@tty1.service`
  → `getty@.service`.
- Re-fetched all three pinned snapshots from `https://raw.githubusercontent.com/systemd/systemd/v262/…`
  and hashed them: **all three are byte-identical to the committed snapshots** (`eb9479be…`, `47e98d39…`,
  `c11cd575…`). The source base is genuine, not a doctored copy.

## Attack 1 — held ground

**Verdict: held.** No counterexample found. The sweep is reproducible and the closest held sentences do
not state the C1 plane.

```
$ git grep -nE 'unit_load_dropin|dropin_paths|unit_need_daemon_reload|null_or_empty|unit_file_mask|config_parse_alias' -- corpus/ SKILL.md PROVINCE.md
(0 lines, rc 1)
$ git grep -niE 'lexicographic order' -- corpus/ SKILL.md PROVINCE.md
PROVINCE.md:451 (modprobe.d), corpus/SOURCES.md:312 (S301 modprobe.d), corpus/knowledge/modprobe-config-plane-r72.md:18 (MD2), corpus/lessons/round-72.md:25
$ grep -rn 'precedence' corpus/knowledge/*.md    # modprobe / pacman-hook / journalctl planes only
```

The twelve `corpus/knowledge` files the sweep names were opened at their `drop-in` lines: all are host
observations of a *named* file (`systemd-user-plane.md:44` a drop-in hardening a generated unit;
`btrfs-scrub-grounding-r45.md:252` a `system.conf.d` default; `kill-event-deep-r8.md:258,263` and
`oom-event-plane.md:352` the `faster-shutdown.conf` timeout; `degraded-triage-r4.md:358` mkinitcpio).
`grep -n 'mask\|Alias=' SKILL.md PROVINCE.md` returns no unit-mask, mask-runtime or `[Install] Alias=`
rule. The merge/precedence plane is genuinely unheld.

Caveat (calibration, not a defect): "this lane never held" is a universal over the whole corpus with no
instrument and no digest in the claim row — it rests on a text sweep (`before/held-ground.txt`) that a
later reader must trust. That is folded into D6.

## Attack 2 — do-nothing control and the cheapest fake

**Verdict: the do-nothing controls are honest and reproduce; the cheapest fake reaches the target and
no frozen clause stops it. Severity: high (D2).**

Controls re-run by me:

```
$ python3 tools/count-ul-rows-r73.py --revision eb105757
UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md
rc=128
$ python3 tools/check-r72-routed-r73.py --revision eb105757
ROUTED_STALE=3 ROUTED_OK=0/3
rc=1
```

(At `74937132` the same two read `rc=128` and `ROUTED_STALE=3`; at `8eeadcb9` likewise. The declaration
commit itself moves only the checker's *missing-token* count on the DIGEST item, 2 → 1, because its C2
row names `R72-C3-INSTRUMENT-DIGEST-DRIFT` in an ineligible block; the summary value is unchanged.)

The cheapest fake is **not** to read a source: it is to copy the frozen counter's own `SAMPLE_ROWS`
(`tools/count-ul-rows-r73.py:68-92`) into the note and append three registry rows carrying the map
URLs. Those rows are admissible by construction — their statements are the round's statements, their
quotes are verbatim from the committed snapshots, and their digests are the map's. Built as a tree
with the **real** `corpus/SOURCES.md`, the **real** `before/src` snapshots and `SOURCES.json`:

```
$ python3 tools/count-ul-rows-r73.py --fixture <tree>
UL_ROW ok UL1 source=S304 snapshot=systemd.unit.xml
...
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1
rc=0
registry rows in that tree: 306
```

Which frozen clause stops it: **none**. The quote-location, word-count, id, reuse and digest clauses are
all satisfied precisely because the instrument ships the answer key; its own comment ("The self-test
scores the counter's mechanics, never the note's admission") is a statement of intent, not a check.
`E1Counter` observed the same identity independently (`w1/E1Counter/report.md:209`, `identical_rows=6/6`);
my run adds the end-to-end path against the real registry and snapshots.

**Fix (smallest safe, instruments frozen):** commit, under `after/`, a receipt that (a) extracts the
note's six rows and the instrument's `SAMPLE_ROWS` and prints the normalized intersection (must be 0),
and (b) per row, re-opens the quote by line in the declared snapshot:
`grep -nF -- "<quote>" .ufo/waves/round-73/before/src/<snapshot>` with the line cited in the report.
For the next round: move the self-test fixtures onto a synthetic snapshot under `$TMPDIR` so the
admissible rows are not the target note's rows.

## Attack 3 — counter channels: which clause is lexical only

**Verdict: the grounding clause is lexical only; a negated row and a content-free row both read
`met=1`. Severity: high (D3).**

Two rows substituted for UL1 in an otherwise control fixture (frozen counter, `--fixture`):

```
| UL1 | Unit files found in directories listed earlier do not override files with the same name in directories lower in the list | source=S304 | snapshot=systemd.unit.xml | digest=eb9479be… | quote="Unit files found in directories listed earlier override files with the same name in directories lower in the list" |
| UL1 | unit files directories earlier override same name lower list unit files directories unit files | source=S304 | snapshot=systemd.unit.xml | digest=eb9479be… | quote="Unit files found in directories listed earlier override files with the same name in directories lower in the list" |
```

```
UL_ROW ok UL1 source=S304 snapshot=systemd.unit.xml
...
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1
rc=0            (both cases)
```

Why: `grounding()` counts distinct `[A-Za-z][A-Za-z0-9_-]{3,}` tokens shared with the *whole* 165 KB
snapshot, after dropping the stopword list — and "not"/"no"/"nor" are stopwords, while the snapshot
contains every other token. The negation scores 11/11; the word-salad (a term list, not a statement)
scores 9/9. The declaration admits the negation case in "planned (next round)" ("a row that negates its
snapshot reads `met=1`"); the content-free case is the same channel one step further and is not
recorded anywhere.

The quote is likewise bound only to the snapshot, not to its row: swapping UL5's mask quote with UL6's
alias quote inside `install.c` leaves both rows `ok` and `met=1` (same command). A row can therefore
carry a quote that does not support its statement — the predicate cannot see it.

**Fix:** the note's rows are the deliverable and they are correct (R1Reviewer re-opened each against the
snapshots); the *claim* is what overstates. Record in the after receipt: (a) each row's statement and
its quote side by side, with the quote's line number in the snapshot; (b) a one-line non-author verdict
per row (the round already has the attack seats for this). For the next round's instrument: score
statement tokens against the *quote* (not the snapshot) and require a propositional shape (at least one
finite verb), which kills both the salad and the negation-by-substitution class.

## Attack 4 — selftest integrity

**Verdict: `--selftest` cannot vouch for its own instrument; only the declaration-commit digest does.
Severity: medium (D4), but the mechanism exists and is being used.**

```
$ python3 <fake-counter>.py
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1
rc=0
$ python3 <fake-counter>.py --selftest
... SELFTEST: PASS (11 cases, 11 passed, 0 failed)
rc=0
$ sha256sum <fake-counter>.py tools/count-ul-rows-r73.py
45206cfb…  <fake-counter>.py
542f9c29…  tools/count-ul-rows-r73.py
$ git show 74937132:tools/count-ul-rows-r73.py | sha256sum
542f9c29…0711a3d6
```

The counter's `selftest()` never hashes its own bytes, and it builds its fixtures from the committed
snapshots, so a replacement with the same output is indistinguishable from the declared tool **by
running it**. `before/absence-controls.txt`'s digest lines are author text in the same commit family and
do not bind anything. What catches a swap is the declaration blob: `git diff 74937132 HEAD -- tools/`
must be empty for the counter, and `sha256sum` must equal the value inside
`git show 74937132:SCORECARD.md`. The live proof that this check matters: the *other* instrument did
change mid-wave (`93f034e3` → `328a6bf6`), and it was caught and recorded only because a seat compared
digests (SCORECARD.md:5869).

**Fix for C1:** none to the instrument; put the two commands in the after receipt:
`sha256sum tools/count-ul-rows-r73.py` and `git diff --stat 74937132 HEAD -- tools/` (expected: only the
checker, covered by the erratum).

## Attack 5 — the instrument-change rule

**Verdict: necessary, not sufficient as written. Missing receipt named below. Severity: medium (D5).**

The rule ("re-run the before control with the final instrument and cite old→new digests in an appended
erratum") is the right shape, and the L1 has now done most of it: `after/c2-before-final-instrument.txt`
exists (mtime 23:12) with both the old and new digest in its header and the base/re-round-72 runs, and
SCORECARD.md:5869 names the old→new pair. What is still missing at my read:

1. **The receipt is not committed, and the C2 row does not name it.** `git status --porcelain` reads
   `M SCORECARD.md`, `M corpus/lessons/round-72.md`, `M tools/check-r72-routed-r73.py`; the C2 claim row
   (SCORECARD.md:5844) still says only "the same-instrument before/after receipt" with no path. The claim
   is about committed bytes, so the receipt and erratum must land in the after commit and the appended
   note must cite the path.
2. **The receipt's digest line is typed text, not tool output.** Its header reads
   `# tool: tools/check-r72-routed-r73.py sha256 328a6bf6…` — someone typed it. The receipt that must
   exist is one whose digest line is *produced by* `sha256sum tools/check-r72-routed-r73.py` (or a
   `--identity`-style self-print), so a reader does not have to trust the author's transcription.
3. **The frozen predicate does not read the receipt at all.** The DIGEST item's `need_any` still accepts
   the literal phrases `same-instrument`, `re-run`, `re-ran`, or the *round-72* receipt path — it does
   not require the round-73 receipt file to exist or to contain the digest pair. Demonstrated: a block
   that says the repair is a fiction still satisfies it (see Attack 8/D8 below; same tree).

**Fix:** commit `.ufo/waves/round-73/after/c2-before-final-instrument.txt` with a
`sha256sum tools/check-r72-routed-r73.py` output line; append the erratum naming both digests, the
receipt path and the base revision; then re-run `--revision <after>` with the final bytes and cite both
revisions. A non-author check is `sha256sum tools/check-r72-routed-r73.py` against the receipt header and
`git diff 74937132 HEAD -- tools/check-r72-routed-r73.py`.

## Attack 6 — claim sizing

**Verdict: C2's predicate is one concrete value and one command (correctly sized); C1's row is sized to
precedent but three of its after-state conjuncts are unmeasured by the counting command. Severity: high
(D6) for the registry conjunct, low for the census.**

What is right: C2's target is exactly `ROUTED_STALE=0 ROUTED_OK=3/3`, rc 0 — one command, re-derivable.
C1's six rows match the round-72 calibration (MD1–MD6, six rows, three snapshots:
`grep -c '^| MD' corpus/knowledge/modprobe-config-plane-r72.md` → 6), so one round can land it.

What is not entailed by `python3 tools/count-ul-rows-r73.py --revision <REV>`:

- **"registry 303 → 306".** The counter never counts registry rows and never reads a row's `status`. It
  only requires three distinct `source=S###` ids whose source cell contains the map URL and whose anchor
  cell contains the snapshot basename. Demonstrated with the same answer-key note, but the three URLs
  written into three **existing** registry rows (S001–S003) and those rows marked `status=rejected`:

  ```
  UL_ROW ok UL1 source=S001 snapshot=systemd.unit.xml
  ...
  UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
  UL_TARGET ... met=1
  rc=0
  registry rows in that tree: 303
  ```

  So `met=1` is reachable with the registry unchanged and the three "sources" rejected. The claim's
  "303 → 306" and "SOURCED — S304–S306" are extra-predicate assertions; they need their own receipt
  (`grep -cE '^\| *S[0-9]{3,}' corpus/SOURCES.md` → 306, and
  `git diff eb105757 <REV> -- corpus/SOURCES.md` showing three added rows, none edited or rejected).
- **"notes 90 → 91".** Implied by the note existing, but not in the counting command; one line closes it
  (`git ls-tree --name-only <REV>:corpus/knowledge | grep -c '\.md$'` → 91).
- **"canonical census rc 0".** No command and no digest named in the row. The census is the fleet-root,
  read-only `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`
  (`scripts/sources-census.sh:1-8`: "Read-only: parses shokunin.conf LANES rows textually … writes only
  stdout or --out"). The *after* outcome row and `after/measure-583eea87.txt` name it (`census_rc=0`,
  `tsukuroi ok …/corpus/SOURCES.md`), but the frozen C1 row does not, its digest is not pinned in the
  declaration, and I did not run it (it is outside the lane). Prior rounds use the same unanchored
  phrase (`SCORECARD.md:5733`), so this is an inherited pattern, not a new invention — but it is still
  an unenumerated conjunct in the frozen row.

Universal clauses not enumerated: C1's "this lane never held" (Attack 1 — text sweep, no digest) and
C2's **"appended"** (below). C2's "appended correction/erratum/refresh" is not checked against the base:
a lesson file rewritten to three lines passes:

```
$ python3 tools/check-r72-routed-r73.py --root <three-line tree>
ROUTED_ITEM LESSON ok
ROUTED_ITEM DIGEST ok
ROUTED_ITEM CAPABILITY ok
ROUTED_STALE=0 ROUTED_OK=3/3
rc=0
```

The round's actual draft is a pure append (`git diff -- corpus/lessons/round-72.md | grep -c '^-[^-]'`
→ 0, same for SCORECARD.md), so the defect is in the predicate, not in the work. Fix: a diff receipt
`git diff --diff-filter=D --name-only eb105757 <REV> -- corpus/lessons/round-72.md SCORECARD.md` must be
empty.

## Attack 7 — separability

**Verdict: held, both directions, with commands.** No defect.

```
# C2-only tree (lesson + SCORECARD blocks, no note)
$ python3 tools/check-r72-routed-r73.py --root <c2 tree>      → ROUTED_STALE=0 ROUTED_OK=3/3 rc=0
$ python3 tools/count-ul-rows-r73.py --fixture <c2 tree>      → UL_NOTE absent rc=128

# C1-only tree (note + registry rows, no SCORECARD/lesson)
$ python3 tools/count-ul-rows-r73.py --fixture <c1 tree>      → met=1 rc=0
$ python3 tools/check-r72-routed-r73.py --root <c1 tree>      → ROUTED_STALE=3 ROUTED_OK=0/3 rc=1
```

The counters read disjoint files and neither depends on the other's landing. The only shared file is
`SCORECARD.md` (C1's result row and C2's blocks); the blocks are disjoint, so the separability sentence
holds as written.

## Attack 8 — sources rejection (R72-GATE-NO-REJECT)

**Verdict: the repair is unmeasured and the cheap version is a rubber stamp. Severity: low (D8) — the
declaration is honest that this is work, not a claim.**

Evidence:

- The round-72 closure defect is real: `corpus/lessons/round-72-verifier-spotcheck.md` §1 defect (3)
  records "the gate recorded zero rejections, so no reject could be spot-checked from this round's
  Gate."
- The round-73 repair has no instrument and no receipt path: it points at `corpus/lessons/round-73.md`,
  which does not exist at HEAD (`git cat-file -e HEAD:corpus/lessons/round-73.md` → rc 128). It is
  excluded from C2's predicate by design ("the defect is reported, not folded into C2's predicate"), so
  nothing catches a no-op.
- The registry's own precedent shows how cheap a "reject" is: S184 is rejected as "duplicate URL and
  identical bytes already represented by S122" and S190 as "redundant with S188" (`corpus/SOURCES.md:190,196`).
  A plan that refuses a duplicate/render/summary can therefore be satisfied by an already-established,
  foreordained outcome whose flip condition can never fire inside the round — a rubber stamp.

A real rejection here would refuse a candidate that *would have carried one of UL1–UL6*, for a reason a
reader can check: e.g. refuse v263/v263.1 bytes because the host runs systemd 262.1 (`pacman -Q systemd`
→ 262.1-1-arch) with the flip "host upgraded to 263"; refuse a rendered man page whose sha256 does not
equal the pinned XML (`eb9479be…`) with the flip "a render whose bytes equal the pinned XML"; refuse a
distro patch of `unit.c`/`install.c` because the host's package build differs from the upstream tag
bytes, with the flip "the installed systemd's sources match the tag". The declaration should name the
candidate class and the flip condition when the Gate runs, not after.

**Fix:** put the refusal in the round-73 lesson with four fields — candidate, would-have-carried row,
verifiable refusal reason with its command, flip condition — and commit it in the same after commit as
the note. A non-author check is the candidate's URL/digest re-read, not a reading of prose.

## Attack 9 — fabrication risk, and the commands that catch it

**Verdict: the receipts that could be fabricated wholesale are the note rows (high, D2/D3) and the
registry rows (high, D6); the source and host receipts are sound and were re-verified (held).**

| receipt | fabricated how | catch (command) | result |
|---|---|---|---|
| six UL rows | copy `SAMPLE_ROWS` (`count-ul-rows-r73.py:68-92`) | normalize both row sets and intersect; expect 0 (`python3 - <<'PY'` extracting `\| ULn \|` rows and `ctr.SAMPLE_ROWS`) | **met=1** as shown (D2) |
| registry rows | edit three existing rows, mark `rejected` | `git diff eb105757 <REV> -- corpus/SOURCES.md`; expect three added rows, none edited (`^-[^-]` count 0) | **met=1 at 303** as shown (D6) |
| C2 blocks | keep tokens, deny the repair | non-author read; the checker cannot (recorded in SCORECARD.md:5869 "remaining limit") | **3/3** as shown (D5) |
| `before/host.txt` | type plausible values | re-ran `systemd-analyze unit-paths` (12), `systemctl show -p FragmentPath,DropInPaths,LoadState,…` | **matches** |
| three snapshots | commit doctored bytes + matching map | re-fetch the v262 raw URLs and sha256 | **all three match** |
| the instrument | swap a printer | `sha256sum tools/count-ul-rows-r73.py` vs `git show 74937132:SCORECARD.md`; `git diff 74937132 HEAD -- tools/` | digest `542f9c…` matches; checker diff is the recorded repair |

The one command a non-author should run first for C1 is the SAMPLE_ROWS intersection; for C2 it is
`git diff` over the two text files (append-only) plus a human read of the three blocks.

## Attack 10 (bonus) — exit map

**Verdict: the checker's documented exit 2 is not implemented. Severity: low (D10).**

```
$ python3 tools/check-r72-routed-r73.py --root <empty tree>
LESSON-STALE absent path=corpus/lessons/round-72.md
DIGEST-STALE absent path=SCORECARD.md
CAPABILITY-STALE absent path=SCORECARD.md
ROUTED_STALE=3 ROUTED_OK=0/3
rc=1
```

The header says "2 cannot evaluate (a required file is absent, or no readable input)" (line 13), but the
check path returns 1; only `--selftest` can return 2 (bad `$TMPDIR`). Same in the frozen bytes and the
hardened bytes. Effect: an absent/truncated input and a genuinely stale state are indistinguishable to
a caller. Fix: return 2 when any required file is absent, or correct the header.

## Attack 11 (bonus, confirming R1Reviewer) — the UL4 wording

**Verdict: a false-as-worded clause passes the counter. Severity: low-medium (D11).**

C1 says "a masked unit stays masked while its fragment path is null or empty, so a zero-size file and a
`/dev/null` symlink both keep the masked state" (SCORECARD.md:5843); the sample row UL4 repeats it.

```
$ systemctl show -p LoadState,UnitFileState,FragmentPath passim.service
LoadState=masked
FragmentPath=/etc/systemd/system/passim.service
UnitFileState=masked
$ sed -n '3874,3876p' .ufo/waves/round-73/before/src/unit.c
        if (path_masked)
                /* For masked files check if they are still so */
                return !null_or_empty(&st);
```

A masked unit's `FragmentPath` is a normal, non-empty path (the `/dev/null` symlink); it is the **file
at** that path whose `stat` is `null_or_empty` (zero-size regular file or `/dev/null`), and a `stat`
failure also counts as "newer" (`unit.c:3866-3868`). `install.c:1424` confirms the zero-size file is
`INSTALL_MODE_MASKED`. The counter passes the row because the tokens appear in `unit.c` and the quote is
verbatim, so a note copied from (or written like) UL4 would teach the wrong condition. R1Reviewer found
the same (`w1/R1Reviewer/report.md:33`); this is a confirmation, not a new claim. Fix: the note's UL4
must read "while the file at its fragment path is zero-size or a `/dev/null` symlink (or cannot be
stat'ed)"; the declaration's sentence should not be copied into the note.

## Findings table

| # | finding | verdict at the final bytes | severity | fix / state after the landing |
|---|---|---|---|---|
| D1 | held ground | held | — | keep the sweep as evidence, not as a check |
| D2 | `SAMPLE_ROWS` is an admissible answer key; the copy reaches `met=1` | survived at `97f6f5ec`; the round's actual note is not a copy (`after/final-checks.txt`: `IDENTICAL=0`) | **high** (predicate), medium (this round) | after receipt exists (`final-checks.txt`); next round: synthetic self-test snapshots so the answer is not admissible |
| D3 | grounding is lexical; negation and word-salad both `met=1`; quote need not support its row | survived at `97f6f5ec`; the note's rows are propositions (R1Reviewer) and the quotes are line-reopened (`final-checks.txt`) | **high** (predicate), medium (this round) | receipts exist; next round: score statement tokens against the quote and require a finite verb |
| D4 | `--selftest` cannot vouch for its own instrument; only the declaration blob catches a swap | survived | medium | `after/final-checks.txt` carries `sha256sum` + `git diff 74937132 HEAD -- tools/`; keep both in the closure receipt |
| D5 | instrument-change rule lacked a committed, final-bytes receipt; predicate accepts a bare phrase | receipt closed (final `71931c1c…` named, base output committed); the predicate still accepts a denial (negated tree → 3/3) | medium (narrowed) | checker could read the receipt path; or the closure keeps the non-author read |
| D6 | C1's registry 303→306, notes 90→91 and "canonical census rc 0" sit outside the counting command; "appended" unenforced | survived: the landing is registry **308** (S304-S308) against the frozen row's 306, and the counter still read `met=1` | **high** (declaration sizing), low (census naming) | the after receipts now count 308/91/census rc 0 and the lesson records 308; the frozen row cannot be edited, so the outcome row is the correction |
| D7 | separability | held | — | none |
| D8 | R72-GATE-NO-REJECT rejection class | narrowed: two refusals landed with measured fetches, reasons and flips; both structurally ineligible classes (render, package page) | low | keep the four-field refusal; a future round should refuse an eligible source (e.g. v263 bytes) to exercise taste |
| D9 | fabrication: note rows and registry rows uncaught by the predicates; snapshots and host readings verified sound | rows: receipts exist and the actual note is clean; sources: held (upstream digests match) | medium (as landed) | the catches in the Attack 9 table remain the non-author check |
| D10 | checker exit 2 documented but not implemented | closed at `71931c1c` (header corrected; empty root rc 1) | — | none |
| D11 | UL4 "fragment path is null or empty" wrong as worded | closed in the deliverable (note UL4 reworded to "the file at its fragment path"); the frozen declaration sentence still has the old phrasing | low (declaration text only) | none to the note; do not copy the frozen sentence |

## Addendum — the landing (`3efb9b24`; claims measured at `583eea87`)

Final instruments at the close snapshot were committed (`git status --porcelain tools/` empty at 23:21):

```
$ sha256sum tools/count-ul-rows-r73.py tools/check-r72-routed-r73.py
97f6f5ec83401b02d6c83b48bcad27f0f97c06c9e4ad134cc1cbfb202dbb03d0  tools/count-ul-rows-r73.py
71931c1c225ecda5f8b6529091dc9383542d0c054ae62ff6e0a16f3fbe51496e  tools/check-r72-routed-r73.py
$ python3 tools/count-ul-rows-r73.py --revision 583eea87
... UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0 ; UL_TARGET ... met=1 ; rc=0
$ python3 tools/check-r72-routed-r73.py --revision 583eea87
ROUTED_STALE=0 ROUTED_OK=3/3 ; rc=0
$ python3 ... --revision eb105757          # before controls, final bytes
UL_NOTE absent ... rc=128 ; ROUTED_STALE=3 ROUTED_OK=0/3 rc=1
```

Both claims' targets are met on committed bytes with the final bytes, and the before→after pair is
same-instrument at the summary level; the checker's *reason strings* differ between the declared and
final bytes (`block-incomplete missing_tokens=2` → `no-block` / `block-tokens` / `block-incomplete`), so
the erratum must carry the reason delta as well as the digest delta (it does name the chain,
SCORECARD.md:5934-5952).

Re-tests of this report's channels against the final bytes:

| attack tree | final counter `97f6f5ec` | final checker `71931c1c` |
|---|---|---|
| `SAMPLE_ROWS` verbatim (answer key) | `met=1` rc 0 (D2 survives) | — |
| negated UL1 | `met=1` rc 0 (D3 survives) | — |
| word-salad UL1 | `met=1` rc 0 (D3 survives) | — |
| swapped UL5/UL6 quotes | `met=1` rc 0 (D3 survives) | — |
| token-soup C2 blocks | — | `ROUTED_STALE=3` (held) |
| negated C2 blocks + real receipt | — | `ROUTED_STALE=0 ROUTED_OK=3/3` (survives) |
| 3-line lesson, no prior blocks | — | `ROUTED_STALE=0` (survives; "appended" unseen) |

**At yield (`65cc1f17`).** The lane moved once more after the close snapshot: the checker is now
`731841988c…` (13 selftest cases) with `after/c2-final-instrument.txt` recording its before/after pair;
the counter stays `97f6f5ec…`. At this tip both commands still read `met=1` rc 0 and
`ROUTED_STALE=0 ROUTED_OK=3/3` rc 0, and the **negated C2 tree still reads 3/3 on `731841988c…`** — the
D5 predicate gap survives the third checker state. Each instrument move re-opens the same-instrument
requirement; the new receipt does re-establish it for `731841988c…`, and a closure reader should cite
that receipt, not the `71931c1c…` one, for the tip pair.

What the landing closed (not findings any more):

- **D5's live gap.** `after/c2-before-final-instrument.txt` is committed, names the final digest
  `71931c1c…` (with the intermediate `328a6bf6…` in the chain), and carries the base and round-72-base
  outputs; the outcome row cites it. The *predicate* still does not read it — the DIGEST item's
  `need_any` accepts the bare phrase, which is why the negated tree above still reads 3/3.
- **D10.** The checker's header now says 2 is `--selftest`-only and an absent file is rc 1; the
  empty-root run returns rc 1. Closed.
- **D11 in the deliverable.** The note's UL4 landed as "A masked unit keeps suppressing a daemon reload
  while **the file at** its fragment path is still null or empty … and stops suppressing it once that
  file is no longer null or empty or can no longer be stat test" — the wording defect is repaired in
  the note; only the frozen declaration sentence retains the old phrasing.
- **D2/D3 in this round's actual work.** `after/final-checks.txt` compares the six note statements with
  `SAMPLE_ROWS` (`IDENTICAL=0`) and re-opens each quote in its own snapshot; the note's rows are
  propositions, not the answer key. The channels survive as *predicate* defects, not as fabricated
  content.

What the landing did not close, and the sharpest new evidence:

- **D6, now concrete.** The frozen C1 row says "registry 303 → 306" and the separability sentence says
  "three registry rows"; the committed landing opened **five**: `git show 583eea87:corpus/SOURCES.md |
  grep -cE '^\| *S[0-9]{3,}'` → **308** (S304-S308; S307 and S308 rejected). The counting command
  printed `met=1` and cannot see the difference. The outcome row and `measure-583eea87.txt` record the
  true value (`registry 303 -> 308`), so the accounting is honest — but the frozen row as written is
  contradicted by the committed bytes, and nothing in the frozen predicate would have caught it. This
  is the cleanest proof that the C1 after column is not the counter's value.
- **D8 calibration.** The Gate did produce two refusals (`corpus/lessons/round-73.md:46-53`), each with
  a measured fetch (HTTP 200, byte counts, digest stability across two fetches), a verifiable reason and
  a flip condition; S307's flip (an Arch patch that changes the merge text) is real, so these are not
  bare duplicates. But both candidates are structurally ineligible to carry a UL row (a render of the
  same upstream text; a package page with 0 rule phrases), so the gate exercised screening, not taste
  between admissible sources. Low stands, narrowed to that.
- **D2/D3/D5 as predicate channels.** The final instruments still accept the answer key, the negation,
  the word salad, the swapped quote, and the denial-with-receipt. The round's compensating receipts
  catch the actual note; the instruments cannot.

## Calibration — what was already recorded

- The `SAMPLE_ROWS` copyability: `w1/E1Counter/report.md:209-210` (`identical_rows=6/6`). My D2 confirms
  it end-to-end against the real registry/snapshots at the final bytes; it is not a new discovery.
- Token presence cannot prove direction/receipt/negation: `w1/R2Reviewer/report.md:52` and the appended
  SCORECARD.md:5869 limit. My negation run (3/3 on the frozen, hardened and final bytes) is the concrete
  instance; the `appended` gap, the registry/census conjuncts and the 306-vs-308 landing are the parts
  I did not find recorded before this report.
- The UL4 wording: `w1/R1Reviewer/report.md:33`. Confirmation only; the note was reworded at the landing.
- The instrument changes (`542f9c29→84501ab8→97f6f5ec`, `93f034e3→328a6bf6→71931c1c`) are recorded in
  SCORECARD.md:5934-5952; my contribution is the frozen/intermediate/final side-by-side on identical
  trees and the observation that the intermediate receipt preceded the final bytes.

## Remaining items after the landing

Closed by the landing (recorded here so the L1 does not redo them): the erratum + final-bytes receipt
(`after/c2-before-final-instrument.txt` names `71931c1c…` with the base outputs, and the outcome row
cites it); the C1 after receipts (`final-checks.txt`: `IDENTICAL=0`, per-row quote re-open;
`measure-583eea87.txt`: `registry_rows=308`, `knowledge_notes=91`, `census_rc=0`); the append checks
(`deleted_lines_in_corpus_and_docs=0`, `file_deletions_or_renames=0`); the UL4 reword; the checker's
exit-map header.

Still open, in priority order:

1. **The C1 declaration row's after value is wrong and the frozen predicate cannot see it.** The row
   says "registry 303 → 306"; the landing is 308. The outcome row is the append-only correction, but a
   closure reader must not quote the declaration row's 306. This is the one place where the claim as
   frozen and the committed bytes disagree.
2. **The answer-key and entailment channels are predicate defects, not content defects.** The round's
   note is not a copy (`IDENTICAL=0`) and its rows are propositions (R1Reviewer), but the instrument
   still admits a copy, a negation, a word salad and a mispaired quote. Next round: synthetic
   self-test snapshots and statement-vs-quote scoring; this round: the non-author read is the guard.
3. **C2's "appended" and "correction" are not entailed by `ROUTED_STALE=0`.** A three-line file and a
   block that denies the repair both pass the final checker; the erratum's "remaining limit" sentence
   must stay in the claim accounting, and a non-author should read the three blocks for polarity.
4. **The Gate refusals are real but structurally ineligible.** S307 (render) and S308 (package page)
   could not have carried a UL row; a future round should refuse an eligible candidate (e.g. v263
   bytes against the host's 262.1) to exercise taste rather than screening.
5. **Census provenance.** The after receipts name the fleet `scripts/sources-census.sh validate` and
   record `census_rc=0`; the frozen declaration row names no command and no digest. Pin the command
   (and its digest) in the row for the next round.

No instruction was sent to any other seat; nothing was admitted, edited, integrated or shipped.
