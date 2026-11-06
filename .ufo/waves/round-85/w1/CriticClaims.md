# CriticClaims — round 85, wave w1 (critic: falsify C2 and audit the C1 rows)

Measured lane revisions: wave runs at `479d868b2fc8969a19a617cd55ced5c13edd84b6`; the L1 then landed
`ffae885fc136596cca400bbed4e8f190693edfc2` (17:18:10), where the gate and battery bytes are unchanged and
three more runs read 20/20 (`receipts/candidate-at-ffae885f.txt`). Current master = `ffae885f`.
Instrument `tools/resume-gate-battery-r85.py` sha256 `b30a7c1ed8fca5fa9c30fb3f4b221ccae11137f688bffc47844b16f0a117ba21`
(= the freeze manifest and the declared sha). Candidate `tools/check-hibernate-resume.py` sha256
`88041b7509fc5824b036d45dd3416bfadbaeb17f0b702e15af0edd17944483e7` (worktree clean for `tools/`).
All scoring below is `python3 tools/resume-gate-battery-r85.py --gate <gate>` with cwd
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, the declared counting command. Receipts:
`CriticClaims/receipts/`; proposed patches: `CriticClaims/patches/`; forger and proposed-battery sources:
`CriticClaims/forgers/` (sha256 in `receipts/sha256s.txt`). Nothing in the lane was edited.

## Verdicts

| Check | Verdict |
|---|---|
| C2 target (`20/20`, rc 0, three consecutive runs at the landed tip) | **met** — 3/3 at `479d868` (`receipts/candidate-run{1,2,3}.txt`) and 3/3 re-run at the landed tip `ffae885f` (`receipts/candidate-at-ffae885f.txt`); gate sha `88041b75…`, battery sha `b30a7c1e…` unchanged |
| C2 predicate as *measured* | **underdetermined** — five different single-clause gate deviations each read **20/20**; a gate stacking four of them also reads 20/20 |
| K1 = 0/20 (do-nothing, r84 gate) | **not reproducible** — 0/20 or 1/20; 8 of 24 re-runs read 1/20, always passing exactly MALFORMED |
| K2 = 13/20 (schema shim) | **verified** — 13/20, same 7 failed families as the committed receipts |
| Freeze chronology (d) | **clean** — no scoring before the freeze; hashes and graph order verify |
| Expectation leak a forger can read | **none on disk or in parent memory**; the battery *source* is importable (rules, not an answer key); a self-plan forger reaches 5/20 |
| C1 rows | **accurate** at every cited raw line (revised entry, 17:12:52); HA8 now carries the host secretmem/CXL measurement; Limits' `__setup` claim is true and its unpinned source disclosed; five calibration nits below |

The candidate gate itself conforms: prefix order `check-hibernate-resume.py:109-113`, last-token
`arg()` `:125-129`, strict `<` at `:163`, multi-swap `sum(...)` at `:161-164`, bool guards at `:58,72`.
Every counterexample below is a **battery** defect, not a candidate defect.

## C2 (a) — can a gate that does not implement the frozen rules reach 20/20? Yes.

| Forger (`CriticClaims/receipts/`) | Deviation from the frozen rule set | Score |
|---|---|---|
| `f1-literal-avail` | A1/A3 match only `hibernate=no` / `hibernate=noresume`; no prefix semantics | **20/20** |
| `f2-first-token` | `resume_offset=` takes the **first** token, not the last | **20/20** |
| `f5-boundary-le` | rule 7 fires at `free == image_size` (`<=`) | **20/20** |
| `f6-first-swap` | rule 7 sums **only `swaps[0]`** | **20/20** |
| `f8-no-bool-guard` | accepts `true` where an int is required | **20/20** |
| `f7-mutant-stack` | all four of A1/A3, first-token, `<=`, `swaps[0]` at once | **20/20** |
| `f3-docstring-nowap` | reads the docstring's rule 2 literally (NO-ACTIVE-SWAP only under file-swap) | 19/20 (HR-NO-ACTIVE-SWAP) |
| `f9-const-cannot` | prints `CANNOT-EVALUATE` for everything | 1/20 (MALFORMED, free) |
| `f10-selfplan` | imports the battery and re-plans the case as its own base (no rule implemented) | 5/20 |

Exact line from `receipts/f7-mutant-stack.txt` (the four-deviation stack):
`{"bases": ["host", "random0", "random1", "random2", "random3", "random4"], "cases": 134, "failed_families": [], "families_passed": 20, "families_total": 20, "order_head": ["HR-HIBERNATE-DISABLED", "MULTI-FAULT", "HR-OFFSET-MISSING", "PREC-DECOYS", "POSITIVE"], "target": 20, "verdict": "met"}` rc 0.

Cause, by generated-case coverage:

* **A1/A3 prefix** — `resume-gate-battery-r85.py:167,171,264-265` draw only the literals `nohibernate`,
  `noresume`, `hibernate=no`, `hibernate=noresume`. The frozen rule's prefix branch
  (`hibernate=V` with `V = no…` but not `noresume*`/`nocompress*`, docstring :19-20) is never exercised.
  This directly contradicts the declaration (`SCORECARD.md:7271-7273`): "A gate that reaches 20/20 must …
  parse `hibernate=` by the kernel's prefix order" — f1 and f7 do not and still read 20/20.
* **last-vs-first token** — every base and every perturbation carries at most one `resume_offset=`
  (`random_base` :138-139; `set_token` removes and re-adds at most one); the frozen "last occurrence" clause (docstring :13-14)
  is untested. This is r84 routed item "duplicate-token cmdline" (`corpus/lessons/round-84.md:76`).
* **boundary `free == image_size`** — `image_size = rng.randint(1, int(free * .9))` (:156) can never be
  equal. r84 routed item (`round-84.md:76`), r84 mutant M12 class survives.
* **multi-swap** — `random_base` always emits exactly one swap area (:147); `perturb` keeps that
  cardinality. r84 routed item, mutants M20/M21 survive.
* **bool type** — the MALFORMED kinds list (:226-227) has no bool-where-int case; `f8` deleting both
  bool guards changes no outcome. r84 mutant M22 survives.
* **docstring nesting** — `resume-gate-battery-r85.py:31` still nests
  `swaps empty -> HR-NO-ACTIVE-SWAP` under rule 2's file-swap clause, while the expectation applies it on
  the partition base. This is precisely r84 routed item "un-nest `swaps empty → HR-NO-ACTIVE-SWAP`"
  (`round-84.md:79`), still unfixed; a literal implementer reads 19/20.

**Smallest safe correction.** `patches/battery-composition.patch` (78 lines, applied to a scratch copy;
the lane file is untouched). It adds: A1/A3 prefix variants and a `nocompressX` decoy (:167,171,264-265,267),
a duplicate-`resume_offset=` POSITIVE case, an `image_size == free` boundary case, a two-swap POSITIVE
case (inserted after :252), an `image-size-bool` MALFORMED kind (:226-247), and un-nests the docstring bullet (:31).
Validated against the proposed battery:

```
check-hibernate-resume 20 / 20 failed:
f1-literal-avail       16 / 20 failed: HR-HIBERNATE-DISABLED,HR-NORESUME-ARG,MULTI-FAULT,PREC-NOHIB
f2-first-token         19 / 20 failed: POSITIVE
f5-boundary-le         19 / 20 failed: POSITIVE
f6-first-swap          19 / 20 failed: POSITIVE
f8-no-bool-guard       19 / 20 failed: MALFORMED
f7-mutant-stack        14 / 20 failed: HR-HIBERNATE-DISABLED,HR-NORESUME-ARG,MULTI-FAULT,POSITIVE,PREC-NO-RESUME-ARG,PREC-NOHIB
```

`git apply --check patches/battery-composition.patch` in the lane tree → rc 0 (read-only check).
The patch changes the instrument sha256, so under the frozen kill rule it requires a **re-freeze**; until
then the declaration's "must … prefix order" sentence is false as measured and should be narrowed to what
the current battery actually forces.

## C2 (b) — is the predicate the same sentence in all three places?

The SCORECARD row (`SCORECARD.md:7267`) defines the predicate by reference ("the frozen resume-facts/2 rule
set in the battery docstring"), and the battery docstring (:12-60) carries the rules, the 20-family list,
the QUALITY claim and the target; the counting command prints only
`families_passed/families_total/target/verdict/failed_families` — a count, never the predicate. The
*sentence* is the same. The *case generator* is not: five clauses of that sentence are unreachable by any
generated case (above), so "20/20" certifies a strict subset of the sentence. That, not the wording, is the
calibration defect.

## C2 (c) — does the do-nothing control move, and can a schema bump alone pass?

* K1 (r84 gate, schema `resume-facts/1`) re-run at the tip: `"families_passed": 0` in the first run and in
  the committed receipt — **but 1/20 in 8 of 24 re-runs** (`receipts/k1-variance.txt`, `k1-variance2.txt`). MALFORMED's expected
  output is `(2, CANNOT-EVALUATE, [])`, exactly what the r84 gate returns for every v2 document; the only
  malformed kind that breaks it is `schema-v1`, which the r84 gate accepts. P(no `schema-v1` among the 12
  MALFORMED draws) = (8/9)^12 ≈ 0.24 against 8/24 = 0.33 observed; every 1/20 run passed
  exactly MALFORMED. `f9-const-cannot` reads 1/20
  deterministically. K1 is a random variable 0–1, not the fixed 0 the SCORECARD states (it is still far
  from `met`, so the kill rule does not void).
* K2 (r84 rules + v2 schema) re-run: `13/20`, failed = `HR-HIBERNATE-DISABLED, HR-LOCKDOWN-BLOCKS,
  HR-NORESUME-ARG, MALFORMED, MULTI-FAULT, PREC-NO-RESUME-ARG, PREC-NOHIB` — matches the three committed
  receipts. A schema bump alone cannot reach the target; the availability work and the extra families are
  needed. The SCORECARD's "answers a v1 document as HEALTHY" also verifies:
  `k1-r84-gate.py --facts <resume-facts/1 doc>` → `{"findings": [], "verdict": "HEALTHY"}` rc 0.

## C2 (d) — was anything scored before the freeze?

No. Graph and committer order: `3ed94533` (16:44:20) → `66374a4` freeze (committer 16:52:22; contains the
battery, 10 controls + receipts, the C1/C2 declaration +41 SCORECARD lines, the manifest) → `479d868`
candidate (16:53:32; touches only `tools/capture-resume-facts-r84.py` and `tools/check-hibernate-resume.py`).
`git show 66374a4:tools/resume-gate-battery-r85.py | sha256sum` = `b30a7c1e…ba21`; the gate at the freeze is
`d68e71ff…bb042`, byte-identical to `controls/k1-r84-gate.py`; `sha256sum -c freeze-manifest.sha256` →
13/13 `OK`; `sha256sum -c src/SHA256SUMS` → 4/4 `OK`, `SHA256SUMS` sha `af40e46d…f284` as declared. The
author dates of `3ed94533` and `66374a4` are both 16:44:20 (the known jj artifact; commit order is the
evidence, per r84 routed defect 5). A fresh read-only capture at 17:04:22 reproduces the pinned base exactly
except `used_kib` (11942400 → 12148176, live swap drift); the `lockdown` value is identical, so the base's
availability key is genuine.

## C2 — expectation-leak probe (the explicit question)

* `/proc/<ppid>/cmdline`, `environ`, `fd`, `maps` are readable from the child (same uid); the battery path
  is visible in argv. 134/134 gate calls found it, read the 17 095-byte source and imported the module.
* `/proc/<ppid>/mem` → `PermissionError: [Errno 13]`; `PTRACE_ATTACH` → `-1`, errno 1; Yama
  `ptrace_scope = 1`. **No per-case `want` is readable from parent memory.**
* The case file is written to a random-named directory under a random name and deleted before the next
  case; nothing else is on disk. The battery has no `want`/`expect` module globals.
* What *is* exposed is the rule text (docstring + `plan_base`/`perturb`), which the assignment says counts
  as copying the battery's logic. A forger that imports the module and re-runs `plan_base(case)` recovers
  the exact expected tuple for idempotent single-fault cases — `f10-selfplan` reads 5/20 (POSITIVE,
  HR-NO-RESUME-ARG, HR-NO-ACTIVE-SWAP, HR-SWAPFILE-COW, PREC-DECOYS) without implementing a rule — but
  cannot reach 20/20. State it as a property of the instrument; hardening (running the battery from a
  private copy) is obscurity, not a fix.

## C1 — row audit (entry as revised 17:12:52; md sha256 `fc67c150…86a67`, json `7a5db591…17e0e`)

The file changed during the wave: the 17:00 version lacked the HA8 host measurement and the
`__setup`-sourcing caveat; the 17:12:52 version adds both, so the earlier HA8 note is dropped — the residual notes are in
`patches/hibernation-availability-residual.md`. Version audited = the one now in the tree, and it landed
unchanged at `ffae885f` (committed md sha = `fc67c150…`, json = `7a5db591…`), so this audit is against the
landed bytes.

Novelty at `3ed94533`: `git grep -n -i -E "hibernation_available|nohibernate|lockdown_hibernation"
3ed94533 -- corpus/knowledge` → rc 1 (empty); `noresume` alone → rc 1. HA7's values already appear at
`corpus/README.md:899` (ScoutHost r84 §3a) — new to `corpus/knowledge`, not new information. Registry
rows S343–S345 exist, tier A, `mined`, linked to the entry; the cited Gate section in
`corpus/lessons/round-85.md` is no longer a placeholder (17:11:09).

| Spec row (entry row) | New ground | Load-bearing | Overreach | Verdict |
|---|---|---|---|---|
| HA1 conjunction + call sites (HA1, HA2) | yes | yes (gates the whole r84 plane) | none — 109-113; call sites 766-769, 1111, 1211-1212, 1269-1270 verified | accurate |
| HA2 `nohibernate` sets both (HA3) | yes | yes (one token kills both) | none — 1461-1465; doc 4479 | accurate |
| HA3 `hibernate=` prefix order (HA4) | yes | yes (a `no…` typo silently disables) | none — 1426-1432; `nocompress` does not set `noresume` in v7.2 | accurate |
| HA4 `noresume` only (HA5) | yes | yes (image silently dropped at boot) | none for the boot path; the sysfs `resume_store` rescue (1306-1307) is omitted | accurate; add a clause |
| HA5 enum order / `integrity` blocks (HA6) | yes | yes (security-posture tradeoff) | none — `lockdown_levels[]` 20-22, `kernel_locked_down >= what` 65 | accurate |
| HA6 doc rows (HA3/HA4/HA5/HA9) | not new facts | yes (operator finds the token) | none — 1962-1969, 4479, 4593, 3538-3545 verified | accurate |
| HA7 host values (HA7) | new to `corpus/knowledge`; at `README.md:899` | yes (live verdict) | none — receipt, fresh capture 17:04:22, `--live` HEALTHY rc 0 | accurate; scope novelty |
| HA8 secretmem/CXL (HA8) | yes | yes (explains `[disabled]` under a HEALTHY gate) | none now — host cell carries `CONFIG_SECRETMEM=y`, 0 secretmem VMAs, `CONFIG_CXL_MEM=m`, no CXL device/iomem; receipts exist (`ScribeEntry/receipts/host-recheck.txt`, `FETCHES.txt`) | accurate |

Every row maps to an operator decision: HA1 whether hibernation is possible at all; HA2/HA3 which tokens
disable it; HA4 the parse trap; HA5 the image-at-boot consequence; HA6 the lockdown tradeoff; HA7 the live
verdict; HA8 why a HEALTHY gate and `[disabled]` can coexist.

Residual findings (severity-ranked):

1. **C1-1 (low, sourcing).** `hibernation-availability-r85.md:50-57` — the `__setup` prefix claim is true
   (v7.2 `obsolete_checksetup` calls `parameqn(line, p->str, n)`, and `parameqn` compares n bytes with
   `-`→`_`), and the entry now states it rests on unpinned `init/main.c`. I reproduced the gate side:
   `noresume=1`, `nohibernate=1` and `noresumefoo` each → `{"findings": [], "verdict": "HEALTHY"}` rc 0
   (matches ReviewGate T9–T11). Correction: pin `init/main.c` + `kernel/params.c` at tag v7.2 and cite them
   (`ScribeEntry/receipts/FETCHES.txt` already fetches other unpinned referents). No claim is wrong.
2. **C1-2 (low, completeness).** HA5 (`:30`) is correct for the boot path, but a successful write to
   `/sys/power/resume` clears `noresume` and calls `software_resume()` at runtime (`hibernate.c:1306-1307`).
   Add one clause to the `HR-NORESUME-ARG` action: the image is still resumable from userspace.
3. **C1-3 (low, precision).** HA8's "0 `secretmem` mappings" is a point-in-time root scan
   (`host-recheck.txt`: `secretmem_vma_hits_root=0`); the ScribeEntry draft carried the caveat that a later
   `memfd_secret()` changes the answer without changing any gate input, the landed table does not. Add it.
4. **C1-4 (informational).** The table header promises "Quotes are verbatim at the cited raw lines"; HA2/HA3/HA4
   merge source lines (`{`, `}` and line breaks compressed). Word order and tokens are exact; the slices are
   not byte-exact. Either restore the draft's byte-exact slices or write "code quotes elide line breaks".
5. **C1-5 (informational).** HA7 is new to `corpus/knowledge`, not corpus-wide (`README.md:899`); do not claim
   it as new information in the closure.

No row is wrong, no row overreaches its source; the five residual items are calibration, not correctness.
The `unprovable-but-better` judgment remains the closure's, not this seat's.

## Proposed patches (nothing applied)

* `CriticClaims/patches/battery-composition.patch` — the six-case battery correction above (needs a
  re-freeze because it changes the instrument sha256).
* `CriticClaims/patches/hibernation-availability-residual.md` — C1-1…C1-5 (pin `init/main.c` +
  `kernel/params.c`, the `noresume` runtime rescue, HA8 point-in-time caveat, quote form, HA7 scope).
* `SCORECARD.md:7271-7273` — until a re-freeze, replace "must … parse `hibernate=` by the kernel's prefix
  order" with "must map `nohibernate`/`hibernate=no` and `noresume`/`hibernate=noresume`" and record K1 as
  "0–1/20 (n=24; MALFORMED is free to any constant-refusal gate)". I made no edit to the lane.

## Refused / not run

Host untouched: no hibernate/suspend, no swapon/swapoff, no /sys or /proc writes, no sysctl, no /boot,
no mkinitcpio/limine/pacman. No git/jj mutation, no lane edit. I did not re-run K0, K3a–e, K4, K5, K6
(their committed receipts verify against the freeze manifest; K1 and K2 were re-run at the tip).
