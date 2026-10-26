VERDICT: defect-found

# C2-5 — attack on C2's depth label

Lane HEAD at read: `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf`; base: `8bd001f58bfda29c92d90d2a7a413825c0ca9fcb`.
Read-only: I edited nothing, ran no counter, built no scratch clone (nothing to remove), installed no tool.

## The rule I am testing against

`/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-38.md:457-461` (word count 25, inside the quote bound):

> Re-scoring a rule the lane already holds on new inputs, or counting rows a sourceless fixture also counts, is quality work, never coverage or depth.

C2's registered surface (`SCORECARD.md:2118`, frozen at `7cbaeb63`): "the host's effective ALPM hook order (69 effective hooks from 70 files; override, suffix-ignoring order, phase positions, AbortOnFail/NeedsTargets, Exec)". Predicate: `rows_expected == rows_matched and mismatches == 0 and extra_rows == 0 and source_ok == 1`.

## What the lane held at base (commands and observed output)

```
$ git -C <lane> grep -n -i -F <token> 8bd001f5 -- corpus SKILL.md | wc -l
alphabetical        1    (corpus/knowledge/package-state-plane.md:262 — "fragment attribution by
                          alphabetical position", unrelated to hooks)
AbortOnFail         0
HOOK_FAILED         0
triggerless         0
PostTransaction     5 lines in 5 files
HookDir            11 lines in 4 files (boot-writers-r19.md, degraded-triage-r4.md,
                          lessons/round-1.md, SOURCES.md)
override           97 lines / precedence 27 / same-name 6
strncmp|runs before|run order|order of hooks|suffix   11 hits, none the hook run-order rule
                          (all "suffix" in version/local-dir contexts; nearest are SOURCES.md:198
                          S192 libalpm remove.c, not hook.c)
```

So the base held: the HookDir direction + same-name override, the three `/etc/pacman.d/hooks/`
operator files by name (`update-safety-note.md:216`), the winner of the `90-mkinitcpio-install.hook`
collision with its two `Exec` values re-measured (`degraded-triage-r4.md:619-621`), the
`PostTransaction` phase of the boot hooks (`boot-writers-r19.md:36,45,51,58`;
`update-safety-note.md:224-232`; `degraded-triage-r4.md:413`), and observed `running '<hook>'`
sequences (`boot-writers-r19.md:37` "ALPM prints one `running '90-mkinitcpio-install.hook'` per
transaction"; `aur-drift-receipt-r9.md:118`; `degraded-triage-r4.md:229`).

## Per-rule classification (HO1-HO7, `corpus/knowledge/pacman-hook-order-r38.md:21-27`)

| Rule | Base state | Class | Counted by the frozen predicate? |
|---|---|---|---|
| HO1 suffix-ignoring bytewise name order, shorter-first tie (`hook.c:443-455`) | 0 hits for the rule; doc:21 host consequence (three `-32` pairs reverse under a full-name sort) | **new verified detail** (subject to C2Rev seats) | yes, but only 6 of 69 rows (control `C2-plain-sort` 63/69) |
| HO2 last-to-first directory walk, first-seen wins, system dir is list head | S007/S008 quoted at `degraded-triage-r4.md:619-620`; host instance re-measured [obs] at `:621`; `/etc` files named at `update-safety-note.md:216`; the entry itself says it "turns the round-19 [inf] … into a source-backed reading" (doc:22) | **restates a held rule**; new part is the code path + list head (S211), i.e. mechanism | yes, 3 rows — exactly the `dir` column of the three known `/etc` hooks (control `C2-no-override` 66/69) |
| HO3 triggerless file = valid mask | 0 base hits; host has 0 masked hooks (doc:13-14) | new rule, **null host consequence** | no — counter's mask branch never fires (table `when` column has only Pre/Post) |
| HO4 Pre-hook non-zero exit only stops on `AbortOnFail` | 0 base hits; base held the narrower one-hook inference that a `10-limine-snapper-lock.hook` timeout "cannot fail the transaction" (`update-safety-note.md:238-244`) | new rule; host instance held as [inf] | no — 0/69 rows carry `abort=yes` (constant column) |
| HO5 unparseable `.hook` aborts the Pre phase before any hook runs (`ALPM_ERR_TRANS_HOOK_FAILED`) | 0 base hits; no broken hook on the host | new rule, **null host consequence** | no — the counter models no parse-error input; `source_ok` only checks that S-rows exist |
| HO6 Post hooks only after a completed commit; failed/interrupted commit runs none; Post failure ignored | 0 base hits for the rule; base held only the log phrase `transaction completed` (`SKILL.md:136`) and per-hook Post labels | new rule, **counterfactual** (52 Post hooks; no failed transaction exercised) | no — not modelled |
| HO7 only triggered hooks run, in HO1 order | base held observed per-transaction `running '<name>'` sequences (`boot-writers-r19.md:37` and the two rows above) | **partly held** (subset fact held; order part new) | no — the entry itself restricts the table to candidates (doc:27) |

## Strongest case that C2 is not depth

1. **The counter's own controls show the counted rows are dominated by inventory.**
   `.ufo/waves/round-38/controls/controls.jsonl:2-4`:
   `C2-plain-sort` → `rows_matched 63, mismatches 6`; `C2-no-override` → `66, 3`;
   `C2-correct` → `69, 0`. A table that gets the run-order rule **wrong** (full-name byte sort —
   the rule HO1 replaces) still counts 63 of 69 rows, and a table with the held override rule
   applied wrongly still counts 66 of 69. The rows that encode new information are the 6 positions
   of the three `-32` pairs; the 3 override rows re-count facts already held at
   `degraded-triage-r4.md:621` and `update-safety-note.md:216`. The predicate's discriminating
   surface is 6 of 69 rows (8.7%); the rest is a listing of two directories that a rule-ignorant
   table also produces.
2. **The novelty sweep is a spelling dodge, not a fact sweep.**
   `.ufo/waves/round-38/before/c2-novelty-sweep.txt:3-13`: `hookdirs` → 0, but the base writes
   `HookDir` (11 lines); `PostTransaction hooks` → 0, but the base writes `PostTransaction`
   (5 files); `alphabetical order` → 0, but the held fact is "precedence"/"override" (97/27 lines).
   There is **no token at all** for `override`, `same-name` or `precedence`, and no synonym sweep
   is recorded, although the entry's own first sentence (doc:7-9) concedes it held "HookDir
   precedence (S007) and same-name override (S008)" and QUALITY 80's appended limit clause
   (`corpus/QUALITY.md:153`) requires exactly that synonym sweep "naming what the lane already
   holds in other words". The one non-zero token, `transaction completed`, is dismissed as
   "pacman.log line quotes" (`SCORECARD.md:2153`), but `SKILL.md:136` uses the phrase as held
   transaction-state knowledge.
3. **Four of the seven rule rows have zero host instances.** HO3 (0 masks), HO4 (0/69
   `abort=yes`), HO5 (no unparseable file) and HO6 (no failed commit) are prose rows; the
   "effective hook order" surface does not move for them, HO5/HO6 are not modelled by the counter
   at all, and HO7 is expressly excluded from the table by the entry (doc:27). The pass therefore
   moves one rule, HO1, and six positions.
4. **Restating a held rule is the rule's named quality case.** HO2 is the same sentence the base
   already quotes from S007/S008 (`degraded-triage-r4.md:620`, verbatim: "hooks in later
   directories taking precedence over hooks in earlier directories" / "Hooks may be overridden by
   placing a file with the same name in a higher priority hook directory"), re-applied to a new
   70-file capture. The entry's own description of HO2 — turning an [inf] into a source-backed
   reading — is a provenance upgrade; per the fleet rule that is quality, never depth. The three
   counted override rows are precisely those held facts.

Net: the honest depth of the counted surface is **one new rule (HO1) and its six row positions**,
inside a 69-row framing in which 63 rows are reachable with the wrong order rule and 3 are held.
The depth label survives only in that narrow form; the registered wording ("69 effective hooks …
override … AbortOnFail/NeedsTargets, Exec") presents held, constant and inventory fields as the
moved surface.

## Impacted axes

- **depth (8)** — the round's depth contribution should be scored as HO1 + phase positions over the
  held rows, not as a 69-row surface; HO2 is a held-row upgrade.
- **C2 axis naming** — the axis name must be the surface changed: "ALPM hook run-order rule", not
  "the host's effective hook order" (the order is only 6 rows different from a wrong-rule table).

## Smallest safe correction

Do not touch the frozen declaration or counter (narrowing a landed target is forbidden). Record one
outcome limit, with this exact text:

> C2 depth limit (round-38 outcome): the counted surface's new information is HO1 and the six
> table positions the `C2-plain-sort` control changes (63/69 otherwise); the three override rows
> re-count held S007/S008 facts (`degraded-triage-r4.md:619-621`) and are quality, not depth; HO3,
> HO4 (0/69 `abort=yes`), HO5 and HO6 have no host instance and are not modelled by the counter;
> HO7 is excluded from the table by the entry. Novelty was swept as tokens only; `hookdirs`,
> `PostTransaction hooks` and `alphabetical order` are token variants of held `HookDir`
> (11 base lines) / `PostTransaction` (5 base files) / `override` (97 base lines), and no synonym
> sweep naming those held neighbours is on record (QUALITY 80).

and add the QUALITY 80 held-knowledge-restated control as a named row — it already exists in
substance as `C2-plain-sort` (63/69, FAIL), so no new data is needed, only the label.

## Not done (stated, not passed)

- I did not run `tools/check-hook-order-r38.py` or the frozen controls; per-row truth of HO1-HO7
  belongs to the C2Rev/C2CritHO seats and the predicate PASS to the C2Exec seats.
- I did not open the pinned S208-S211 snapshots; my per-rule classification is by base-corpus
  novelty and by the entry's own text, not by re-reading `hook.c`.
- No scratch directory was created; no package/service/sysfs/git state was touched.
