VERDICT: defect-found

# C1-7 — beat the parameter capture

Scope: item C1-7 (counter `tools/score-selftest-mounts-r41.py`, sha256 `8306d999…`, lane tip
`71851d636ab1bffaf8fee5016617c88878a666f1`). The C1 claim itself is not falsified: the landed
four cases do kill H5/H6/H9/H10 (after receipt `.ufo/waves/round-41/after/c1-after-568c397.jsonl`
line 20 `"survivors": 0`; my clone's baseline reproduces `PASS (128 cases, 128 passed, 0 failed)`).
The defect is in the `params` term: it is a shape/literal gate, not a test of the parameter, and it
credits the wrong polarity and the wrong text (and can refuse a genuine test).

## Counterexample (scored)

Variant commit `fc74df417e009dfea1b45dccad9c976596ddd7d7` on fixture `master` (parent `71851d63`,
clone `git clone -q --shared`, origin removed, toplevel checked, fixture identity). The four round-41
case blocks (`tools/tsukuroi-census.sh:3037-3063` at tip) are replaced by four cases whose mount
tables carry the same four shapes, but each case first writes a populated sysfs root
(`st_write "$FX/btrfs/$sfs/devinfo/1/error_stats" 0 0 0 0 0`) and asserts the
`storage-mounted-populated` outcome (`census:2997-3002`) plus
`ABSENT:detail=mounts:btrfs-without-sysfs`. Because `fsn=1`, the arm's mount read
(`census:1906` `if [ "$fsn" -eq 0 ] && [ "$blocked" -eq 0 ]`) is never entered, so the tables are
never consulted. Diff: `.ufo/waves/round-41/w1/C1CritParams/variant-fc74df4.diff`.

Command (one counter run, `--jobs 4`; output `.ufo/waves/round-41/w1/C1CritParams/counter-variant-fc74df4.json`):

    python3 tools/score-selftest-mounts-r41.py --repo <clone> --revision fc74df41… \
        --scratch /fast/scratch/hyaku/tsukuroi-r41/C1CritParams/ctr --jobs 4

Observed:

    baseline_pass 1  (PASS (128 cases, 128 passed, 0 failed))
    capture_pass 1   neutral_pass 3   decoy_pass 1   mutants_applied 13
    survivors 4      ["H10-count-exactly-one","H5-mountpoint-absolute","H6-source-devonly","H9-subvolkey-option"]
    params 4         param_cases: P1,P2,P3,P4 each credited to "healthy: a populated sysfs root is read and
                     the mount table adds nothing (variant P<n> table)"
    result FAIL      exit 1

So `params == 4` — full credit, every declared shape — on a selftest where no mount table is ever read
and all four held-out mutants survive. The composite predicate still rejects, but only through
`survivors`; the `params` term supplied no evidence and could not distinguish this suite from the real one.

Direct runs of the four mutants on the same variant text (frozen `MUTANTS` replacement texts,
`mut.py`; `.ufo/waves/round-41/w1/C1CritParams/receipts.md`): H5, H6, H9, H10 each
`rc=0 PASS (128 cases …)`; M1 still `rc=1 FAIL (128 cases, 126 passed, 2 failed)`, its failures the two
round-40 varied tables, i.e. the suite is live and only the four new tables are inert.

## Why the capture credits them

`params_from_capture` (`tools/score-selftest-mounts-r41.py:173-190`) keeps a case when
`label in passed_labels` and `any(WANT_BLOCK in x for x in args[1:])` (`:182`). Three independent
defects make that condition vacuous:

1. **Wrong polarity accepted.** The capture writes `$*` (`CAPTURE_LINE`, `:116`), and a must-not-match
   pattern keeps its literal: `ABSENT:detail=mounts:btrfs-without-sysfs` contains `WANT_BLOCK`. The
   variant uses exactly this. Unit probe of the frozen function credited P2 from that string alone.
2. **The label counts as a "wanted pattern".** `$*` also carries the label (and `wrc`/`wverdict`).
   Unit probe: a case whose label is `… detail=mounts:btrfs-without-sysfs never asserted` with a plain
   `state=HEALTHY` regex credited P1. No selftest needs a WANT_RE at all.
3. **`mount_props` reads the fixture table, not the case** (`:162-170`): shape presence is all that is
   asked; nothing ties the credited label to an outcome that depends on the shape (no cross-check against
   `confirm_labels` computed at `:270`).

## Reverse direction: a genuine test can be refused

The same lexical gate can drop real work. On the original census I replaced only the mp-relative case's
regex with `^STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0` (no `$`, no
detail literal): baseline `rc=0 PASS (128 cases…)`, H5 `rc=1 FAIL (… 127 passed, 1 failed)` with the
failure on that label — a genuine P1 kill. `params_from_capture` on that case's `.args`/`.mounts`
credits nothing (`mount_props` P1=True, credited P1=[]), because the literal is no longer anywhere but the
label; with the other three round-41 cases present this suite would report `params 3` and be rejected
despite killing all four mutants [the count 3 is inference from the observed credits; the missing P1
credit and the kill are observed].

## The injected capture line changes no case outcome (checked, as asked)

Anchor `tools/tsukuroi-census.sh:2135`, injected line `score-selftest-mounts-r41.py:116`, injection at
`:227-229`. Mechanics and observations:

* The group is before `shift 3`, writes only under `$R41_CAP` (outside `$FX`), and is on the left of
  `|| true`, so a failed redirect/`cp` is swallowed and the group's status is 0; a failed redirect under
  `set -e` inside such a group is also swallowed (probe: `{ printf x > /nonexistent-dir/x; } 2>/dev/null
  || true; echo after-failed-write` → `after-failed-write`). File names come from `PASS + FAIL`, which is
  injective because every `check()` ends in exactly one `ok`/`bad`.
* FIFO case: `[ -f "$FX/mounts" ]` is false for the FIFO (probe `F-FALSE`; group continues `rc=0`), so the
  FIFO is never opened and cannot hang; the capture file for that case has no `.mounts` sibling.
* Unreadable-root case (`chmod 000 "$FX/btrfs"`, `census:2971-2977`): the captured file is `$FX/mounts`
  (0644, untouched by the 000 btrfs dir); `cp` succeeds and `fx_no_mutation` hashes only `$FX`, so the
  zero-mutation proof is unaffected.
* Full differential on the original text (`capdiff.py`): plain vs injected both
  `rc=0 PASS (128 cases, 128 passed, 0 failed)`, ordered PASS-label lists identical, FAIL sets both empty;
  capture fired for 125 `check()` calls (125 `.args`, 123 `.mounts`; the FIFO and removed-mounts cases are
  the two skipped). Receipt: `.ufo/waves/round-41/w1/C1CritParams/receipts.md`.
* Caveat (not an outcome change for the counter): the line is unsafe outside the counter's private copy —
  with `R41_CAP` unset, `set -u` aborts the suite (probe: outer rc 1, the following `echo` never runs).
  `run_selftest` always sets `R41_CAP` for the capture run, so the scored behaviour is unaffected, but the
  line must never be committed to the lane.

## Impacted axes

operability (C1). The `params` term is the QUALITY-88 addition named in the declaration
(`SCORECARD.md:2465`; predicate `score-selftest-mounts-r41.py:41`, `:291-295`): it was meant to stop a
selftest that varies no table. It does not: it is satisfied by four tables the arm never reads, by an
`ABSENT:` pattern, or by label text, and it can reject a case that does test the shape. In the landed
suite it is also redundant — the after receipt's `param_cases` credit exactly the four round-41 cases,
which are already the H5/H6/H9/H10 kill cases.

## Smallest safe correction (proposed text)

Close the lexical holes and tie each property to a confirmed kill. (a) Write only the WANT_RE arguments:

```python
CAPTURE_LINE = ('    { printf "%s\\n" "$label" "${@:4}" > "$R41_CAP/$((PASS + FAIL)).args"; '
                '[ -f "$FX/mounts" ] && cp -- "$FX/mounts" "$R41_CAP/$((PASS + FAIL)).mounts"; } 2>/dev/null || true\n')
```

(b) In `params_from_capture`, scan must-match patterns only (the label/wrc/verdict are no longer in the
scanned lines):

```python
        patterns = [x for x in args[1:] if not x.startswith('ABSENT:')]
        if label not in passed_labels or not any(WANT_BLOCK in x for x in patterns):
            continue
```

(c) In `main()`, after the kill pass (`:273-275`), keep a property only when the credited label is one the
corresponding mutant fails — a table shape that a mutant never contradicts earns nothing:

```python
PROP_MUTANT = (('P1-mountpoint-not-absolute', 'H5-mountpoint-absolute'),
               ('P2-source-not-dev', 'H6-source-devonly'),
               ('P3-no-subvol-option', 'H9-subvolkey-option'),
               ('P4-two-btrfs-lines', 'H10-count-exactly-one'))
...
        for prop, mname in PROP_MUTANT:
            kill = set(res.get(mname, {}).get('confirm_labels') or [])
            params[prop] = [lb for lb in params[prop] if lb in kill]
```

The cross-check is behavioural, not lexical, so it survives a renamed detail field; it also keeps H9's
non-btrfs `subvol=` kill (where the table has no btrfs line at all) from being mistaken for a P3 shape
test. After it, the variant scores `params 0` (the four labels are not in any mutant's `confirm_labels`),
while the landed selftest keeps `params 4`. The alternative — delete the `params` term — is safe for
P1/P2/P4 (a kill forces the shape) but not for P3, so the cross-check is the smaller correct change.

## Not done

No live-host command beyond read-only probes; no lane write except this report and the receipts under
`.ufo/waves/round-41/w1/C1CritParams/`; scratch removed after copying receipts. The counter was run once
for this item (`--jobs 4`); all other runs were single `--selftest` invocations.
