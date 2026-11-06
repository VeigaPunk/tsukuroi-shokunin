# Proposed battery changes (round-85 freeze material — not a re-declaration for r84)

Report: `.ufo/waves/round-84/w1/CriticClaims.md`. Findings F-C2-1..5. The r84 predicate is frozen
and the candidate was already counted, so none of this may be applied to r84; a new freeze must
carry the new target (13 → 15 families) and the new controls.

## 1. Kill the schedule replay (F-C2-1)

`tools/resume-gate-battery-r84.py:206-214` (candidate copy `resume-gate-battery-r85.py`):

```diff
--- a/tools/resume-gate-battery-r84.py
+++ b/tools/resume-gate-battery-r85.py
@@ -206,6 +206,7 @@
             plan = [("POSITIVE", b, (0, "HEALTHY", []))]
             m, kind = malformed(b, rng)
             plan.append(("MALFORMED", m, (2, "CANNOT-EVALUATE", [])))
             for fid in IDS:
                 if fid in FILE_ONLY and not file_base:
                     continue
                 plan.append((fid, perturb(b, fid, rng), (1, "DEGRADED", [fid])))
+            rng.shuffle(plan)   # position must carry no information (CriticClaims F-C2-1)
             for fam, facts, want in plan:
```

`rng` is `random.Random()` (unseeded, `:195`); shuffling after the `perturb` calls keeps the answer
attached to each case and destroys the position→family mapping. Verify the control: `f2-replay.py`
must drop below target (it does not read the facts, so it can only guess).

## 2. Test rule-set composition and antecedents (F-C2-2, F-C2-3)

Add to the per-base plan (before the shuffle), together with `TARGET = 15`:

```python
            # composition: two independent faults, expected as a sorted set
            two = perturb(perturb(b, "HR-SWAPFILE-COW", rng), "HR-HOOK-BEFORE-ENCRYPT", rng)
            plan.append(("MULTI-COW+HOOK", two,
                         (1, "DEGRADED", sorted(["HR-SWAPFILE-COW", "HR-HOOK-BEFORE-ENCRYPT"]))))

            # rule 1: nothing else is evaluated
            nr = copy.deepcopy(b)
            nr["cmdline"] = set_token(nr["cmdline"], "resume", None)
            nr["image_size"] = 10 ** 18            # a second, independent fault
            plan.append(("RULE1-SHORT-CIRCUIT", nr, (1, "DEGRADED", ["HR-NO-RESUME-ARG"])))

            # rule 2 antecedent: resume_swapfile null => no file-type findings
            if not file_base:
                pd = copy.deepcopy(b)
                pd["cmdline"] = set_token(pd["cmdline"], "resume_offset", 12345)
                pd["sys_power_resume_offset"] = 12345
                plan.append(("PARTITION-OFFSET-NO-MAP", pd, (0, "HEALTHY", [])))
```

Why each case discriminates (measured on r84's frozen gate, receipts `doc-*.json`):

| Case | candidate | F1 (13/13 today) | F4 first-fault (13/13 today) | strict misreading |
|---|---|---|---|---|
| `multi` | `[HOOK, COW]` | `[HOOK, COW]` | `[COW]` | `[]` |
| `nores-second-fault` | `[NO-RESUME-ARG]` | `[NO-RESUME-ARG, TOO-SMALL]` | `[NO-RESUME-ARG]` | `[]` |
| `partition-offset-no-map` | `HEALTHY` | `HEALTHY` | `HEALTHY` | `[OFFSET-MISSING]` |

Note the `MULTI` case sets `image_size` untouched, so a base whose free swap is below `image_size`
would add `HR-SWAP-TOO-SMALL`; the generator's positive bases keep `image_size <= 0.9*free`, and the
host base is healthy, so the pair is stable. Assert it in the selftest rather than assume it.

## 3. Pin rule-1 vs validation precedence (F-C2-5)

Add one sentence to the battery docstring ("schema and type errors are rc 2 even when `resume=` is
absent; rule 1 runs only on a well-typed document") and a case that exercises it:

```python
            bad_nr = copy.deepcopy(b)
            bad_nr["cmdline"] = set_token(bad_nr["cmdline"], "resume", None)
            del bad_nr[rng.choice(REQUIRED)]
            plan.append(("MALFORMED-NO-RESUME", bad_nr, (2, "CANNOT-EVALUATE", [])))
```

## 4. Optional hardening (F-C2-4, F-C2-6)

- Do not expose a generator-only marker to the gate: drop `sys_power_disk` and the fixed
  `captured_at` shape from `random_base`, or randomise `captured_at` to real-looking timestamps, so a
  shape test cannot route the host base and the random bases to different logic.
- If `--live` is part of the frozen interface, give it one battery leg (e.g. run `--live` once and
  require rc ∈ {0,1} and a parseable JSON object), otherwise drop it from the predicate.

## 5. Freeze hygiene (F-CH-2)

Commit `src-lesson/cpython-subprocess.py` before the freeze if a claim cites it, or keep it outside
`.ufo/waves/round-84/before/` and declare it as post-freeze evidence. Do not rely on author dates;
record the parent commit and the freeze's committer date in the declaration.
