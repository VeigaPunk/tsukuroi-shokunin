VERDICT: defect-found

Item C1-5 (beat the decoy). A base-census variant that adds **no** round-41 case, touches `probe_storage_arm`
**not at all**, and stays at 125 cases (124 + 1 inline assertion, zero new `check` calls) satisfies every term of
the frozen C1 predicate: `baseline_pass 1, neutral_pass 3, decoy_pass 1, mutants_applied 13, survivors 0, params 4`,
counter exit 0. It kills H5, H6, H9 and H10 by **reading the arm's own source** (here-documents stripped) rather
than by measuring it, and it takes all four `params` keys from **one** fixture line in an unrelated round-40 case.
So `survivors == 0 and params == 4` does not establish that the census "gains four mount-table cases": both terms
are satisfiable without a single behavioural case. This is the limit the declaration records at `SCORECARD.md:2492`
("a self-reader that strips here-documents before grepping is not refused by the decoy") — the item asked for the
attack, and the limit turns out to be total, not partial.

Receipts: `.ufo/waves/round-41/w1/C1CritDecoy/` (`v1-shapegate.diff`, `v1-shapegate.json`,
`v2-loopgrep.diff`, `v2-loopgrep.json`).

# 1. The counter that was beaten

`tools/score-selftest-mounts-r41.py`, sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c`
(`sha256sum`, matches the declaration `SCORECARD.md:2465`). The terms that matter here:

- mutants `MUTANTS` (`tools/score-selftest-mounts-r41.py:85-103`), neutrals `:105-113`, one decoy built from
  the mutants' replacement texts only, inside a dead here-document (`:120-122`).
- a kill is attributed from **stderr labels**: `killed()` `:195-198` = nonzero exit and the same case count and
  `FAIL <baseline label>` on stderr. Nothing requires the failing label to come from a fixture-driven case; an
  inline `ok`/`bad` assertion in `run_selftest` is a first-class label.
- `params_from_capture()` `:173-190` counts a property per **key**, not per case: four keys satisfied by one
  passing label's mount table is `params 4`.

Base text scored: `0e5805a1:tools/tsukuroi-census.sh` (sha256 `032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733`).
Implementation for comparison: `568c397d:tools/tsukuroi-census.sh` (sha256 `646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95`,
`after/c1-after-568c397.jsonl`: 128 cases, four params from four **distinct** labels).

The arm is byte-identical in all three — `sed -n '/^probe_storage_arm() {/,/^}/p'` sha256
`71e6007e566e1af32feb495e04e4f291c75fdddb2b521d9822b7363fcdf34d56` at `0e5805a1`, at `568c397d`, and in both
variants below — so round-41 coverage is fixture-side only, and the counter's whole discrimination between
"four cases" and "no cases" rests on *how* the selftest fails a label, which the counter cannot see.

# 2. C1-DECOY-A — `v1-shapegate`, **PASS** (the counterexample)

Revision `03ea6edb799040c479c56ea425e700f1099ead82` (fixture clone `--shared` of the lane, `origin` removed,
committed on `master` after `git -C "$D" rev-parse --show-toplevel` returned `$D`, identity `fixture@shokunin.local`).
15 added lines + 1 modified line, one file; zero new `check` calls, zero `R41-C1 H*` cases:

```
$ grep -c '^+  check ' v1-shapegate.diff            -> 0
$ grep -c 'R41-C1 H' <variant census>               -> 0
$ python3 tools/score-selftest-mounts-r41.py --repo $D --revision 03ea6edb --scratch $S/s --jobs 4
  counter rc=0
  {'baseline_pass': 1, 'neutral_pass': 3, 'decoy_pass': 1, 'mutants_applied': 13,
   'survivors': 0, 'survivor_names': [], 'params': 4, 'result': 'PASS', 'exit': 0}
```

The receipt (`v1-shapegate.json`): baseline `TSUKUROI_CENSUS_SELFTEST: PASS (125 cases, 125 passed, 0 failed)`;
`D-all-mutant-texts` decoy `pass: true` (the here-document strip is what keeps it green); 13/13 mutants
`killed: true, confirmed: true`, e.g. H5 `first_fails: ["FAIL storage arm shape: field-counted btrfs on unfiltered
rows, exact fstype (R41-C1): narrowed"]` and `confirm_labels` naming that same label; `params 4` with
`param_cases` showing **one** label under all four keys
(`healthy rollup: one read-only btrfs mount among four lines, empty root, is BLOCKED (R40-C1)`, a round-40 case).

The whole variant (`v1-shapegate.diff`):

```diff
@@ -3019,7 +3019,8 @@ STUB
     '/dev/sda2 /var/lib/machines btrfs ro,noatime,compress=zstd:3,subvolid=263,subvol=/machines 0 0' \
-    '/dev/sdb1 /srv ext4 rw,relatime 0 0' > "$FX/mounts"
+    '/dev/sdb1 /srv ext4 rw,relatime 0 0' \
+    'UUID=0b1c2d3e relative/mnt btrfs rw,commit=60 0 0' > "$FX/mounts"
@@ -3034,6 +3035,19 @@ STUB
+  # R41-C1 self-read (shape gate): the arm's own code with every here-document body removed — a
+  # dead here-document is not code, so a text decoy cannot stand in for a rewritten btrfs test.
+  local alab='storage arm shape: field-counted btrfs on unfiltered rows, exact fstype (R41-C1)'
+  local armcode armbad=''
+  armcode=$(declare -f probe_storage_arm | awk '/<<.R41DECOY/{s=1;next} s&&/^R41DECOY$/{s=0;next} !s')
+  printf '%s\n' "$armcode" | grep -qE 'while read -r _src _mp fst|awk .\$3 == "btrfs"' || armbad+=' loop'
+  printf '%s\n' "$armcode" | grep -qE '"\$mt" -gt 0|0 -lt "\$mt' || armbad+=' count'
+  printf '%s\n' "$armcode" | grep -qE 'blocked" -eq 0' || armbad+=' guard'
+  printf '%s\n' "$armcode" | grep -qE 'cat -- "\$PROC_MOUNTS' || armbad+=' mtab'
+  if printf '%s\n' "$armcode" | grep -qE '\$\{fst,,'; then armbad+=' casefold'; fi
+  if printf '%s\n' "$armcode" | grep -qE '_mp:-} == /|_src:-} == /dev/'; then armbad+=' narrowed'; fi
+  if [ -z "$armbad" ]; then ok "$alab"; else bad "$alab:$armbad"; fi
```

The fixture line is not a case: it is appended to the round-40 `storage-mounts-varied-multi` table so that one
existing PASS label's table carries P1 (relative mountpoint), P2 (source not `/dev`), P3 (no `subvol=`) and P4
(two btrfs lines) at once. The base arm passes it for the reason it passes every table: it counts any line whose
third field is `btrfs` and never looks at fields 1, 2 or 4 — the exact blind spot H5/H6/H9 were held out for.

Why the decoy does not bite: the decoy body carries the **mutants'** replacement texts, never the baseline shapes.
The gate asserts *baseline* fragments, so it survives the decoy untouched; only the two *absence* assertions need
the here-document strip, and the strip (`awk`, one line) is the whole cost of the survival. The two cheaper forms
the item suggested do **not** survive the neutral set: grepping only the `while read` loop lines is variant B
below (`neutral_pass 2`), and a stripped line count is refused by `N3-awk-field` for the same reason — declared
arm lines are 95 for base, `N1`, `N2` and 91 for `N3` (measured on `declare -f` output in the scratch). The gate
has to be written as tolerant fragments, which is the form §2 takes.

Corroboration of mechanism, run by hand in the same scratch: `declare -f probe_storage_arm` on the decoy text
prints the here-document at `decl_decoy.txt:68` (`: <<'R41DECOY'`) through `:83` (`R41DECOY` at column 0), and
stripping those lines returns the base arm's declared text unchanged.

# 3. C1-DECOY-B — `v2-loopgrep`, the cheapest that **FAILS** (and why)

Revision `255605872e7b0a5f6ce51ed483c7db281ddc0e4a`, the same fixture line plus 7 lines: `declare -f
probe_storage_arm | grep -q 'while read -r _src _mp fst'` wrapped in `ok`/`bad` (`v2-loopgrep.diff`).

```
counter rc=1
{'baseline_pass': 1, 'neutral_pass': 2, 'decoy_pass': 1, 'mutants_applied': 13,
 'survivors': 2, 'survivor_names': ['H5-mountpoint-absolute', 'H6-source-devonly'], 'params': 4, 'result': 'FAIL'}
```

Two independent reasons, both instructive:

1. **the neutral set refuses it**: `N3-awk-field` (a behaviour-preserving awk rewrite of the same count) removes
   the `while read` line, so the gate fails a neutral —
   `FAIL storage arm shape: btrfs rows counted by a while-read loop (R41-C1)` — `neutral_pass 2`.
2. **it leaves H5/H6**: both keep the loop text and only narrow the count, so their run PASSes the gate and the
   round-40 cases (which never use a relative mountpoint or a non-`/dev` source) do not notice either; only
   H9/H10 fall out of the cheap form (11 of 13 killed: M1-M9, H9, H10).

So the neutral set is what sets the price of a text gate: it forces the gate to be written as *tolerant
fragments* rather than exact lines, and the tolerant-fragment form is exactly what passes (§2: `params 4` in this
variant too, with 2 survivors — `params` is independent of the four cases).

# 4. Impacted axes

- **operability (C1) — the claim's binding.** `survivors == 0 and params == 4` is satisfied by
  `(four fixture cases)` and by `(a text gate + one fixture line)`; the counter cannot tell them apart, so it
  cannot certify "the census gains four mount-table cases". The real candidate `568c397d` *does* add the four
  cases (`after/c1-after-568c397.jsonl`, 128 cases, four distinct param labels) and its PASS is real — but the
  predicate is not what makes it real. Round-40's `C1CritControl.md` (one-line `declare -f` prologue, PASS) is
  the same defect one decoy weaker; the decoy closed the *mutant-text* spelling only.
- **quality / counter authority.** The selftest is at once the subject of the measurement and the witness for it;
  the counter's only instrument is the subject's own stderr. C2 already answers the same problem by declaring its
  lexical checks shape gates and requiring a non-author reviewer read (`SCORECARD.md:2468-2471`); C1 has no
  equivalent read, and this variant shows why it needs one.
- **not impacted**: `neither` mutant is a false positive; `probe_storage_arm` and the round-40 cases are untouched
  in both variants, so no existing behaviour claim is harmed.

# 5. Smallest safe correction (proposal; the lane is read-only for this seat, nothing applied)

Two changes to the counter, both cheap, plus one honest residual. The counter is frozen before data, so applying
them is an L1/declaration decision (re-freeze + re-run of the before receipt), not a seat edit.

1. **Per-case params.** In `params_from_capture()` (`tools/score-selftest-mounts-r41.py:173-190`) attribute each
   property to a case label, then require four *distinct* labels:

   ```python
   distinct = {v[0] for v in params.values() if v}
   n_params = sum(1 for v in params.values() if v)
   ok = ... and n_params == 4 and len(distinct) == 4
   ```

   This is what the declaration already claims ("gains four mount-table cases") and what the implementation
   measures; it costs my §2 shortcut its one fixture line but not, on its own, the text gate.
2. **One decoy outside the neutral set.** Add `D2-benign-rename` to the decoy set — the arm with `mt` renamed to
   `nb` and the count written as the N3 awk pipeline, behaviour identical, plus the same dead here-document —
   and raise the term to `decoy_pass == 2`. Any gate tuned to N1/N2/N3 (as §2's is, by construction) fails it;
   a behavioural selftest passes it. Exact predicate sentence proposed:

   ```
   baseline_pass == 1 and neutral_pass == 3 and decoy_pass == 2 and mutants_applied == 13
   and survivors == 0 and params == 4 and params_distinct == 4                         -> PASS, exit 0
   ```
3. **Residual, stated rather than papered over.** Any *finite* decoy set is defeatable by a gate re-tuned to it,
   because the counter attributes kills from the subject's own text. The durable fix is not another decoy but an
   independent read: require a non-author seat verdict on the four case bodies (as `verdicts_ok` does for C2), and
   keep the counter's role as "the four cases exist and behave", not "the candidate is honest".

# 6. What I ran, what I did not

Ran: two frozen-counter runs, serially, `--jobs 4`, one at a time (v1 327 s, v2 262 s); one 63 s standalone
`--selftest` of the v1 variant (125 cases, 125 passed); one 55 s standalone `--selftest` of the base text
(124 cases); the `declare -f`/strip experiments in the same scratch. Scratch:
`/fast/scratch/hyaku/tsukuroi-r41/C1CritDecoy/` (removed after copying receipts). Lane content, the fleet repo and
the host were not modified; `git add/commit` ran only inside the two fixture clones (toplevel verified); no
package, service, mount or `/etc` change; no new tool installed, so nothing to record under the tooling directive.

Not run: no counter run on a variant that adds four *inert* fixture cases plus the text gate (the §1
`params_distinct` shortcut would need it to be scored, and it would cost another ~5 min for a point already
carried by §2 and §3); no re-run of the implementation's `568c397d` receipt (cited from
`after/c1-after-568c397.jsonl`).

One observed side-note worth the L1's attention: in the v1 run the **baseline** first attempt failed under load
(`FAIL healthy rollup: nonzero lifetime counters … : hostname override not honoured — possible host read`,
`125 cases, 124 passed, 1 failed`) and the counter's single serial retry passed — the retry is load-bearing on this
host, and a `FAIL` that survives one retry is indistinguishable in the receipt from a real host read.
