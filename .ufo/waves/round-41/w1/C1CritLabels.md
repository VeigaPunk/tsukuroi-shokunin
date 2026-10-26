VERDICT: defect-found

# C1-6 — attack on the kill attribution and the retry rule (counter `score-selftest-mounts-r41.py`)

Counter under attack: `tools/score-selftest-mounts-r41.py` at `e479fdc54d0977ccd8112a42d8d139baaebcb02e`,
sha256 `8306d9990b156ceb625eabbe942910fc0d09b20f350a7e8af1ff2237fd07355c` (matches the declaration).
Candidate: `tools/tsukuroi-census.sh` at `568c397da11339aed65181be598414f268835555`, sha256 `646c84fc…6f9eb95`.
Lane content was read only (`git show`); every run happened in `/fast/scratch/hyaku/tsukuroi-r41/C1CritLabels/`
(with `TMPDIR` there), which is removed at the end of this seat. Receipts under
`.ufo/waves/round-41/w1/C1CritLabels/` (6 files, ≤4 KB each); the census itself was never copied there.

Short answers to the three questions:

1. **A selftest that detects mutants can score kills by printing forged stderr output: yes, demonstrated end to
   end through the counter's own `killed()` and confirmation path.**
2. **Can flake break attribution: yes, in both directions, and asymmetrically — p² to fake a kill (the same
   label must fail in both runs), ~2p to lose a genuine one (either run can flake), and I measured one
   single-case flake in 21 runs of the same bytes.**
3. **Can the one serial retry hide a real decoy failure: yes for any nondeterministic decoy failure, which is
   the only kind the retry exists to absorb — a coin-flip self-detector's survival rises from 1/2 to 3/4.**

Two holes the item did not name, found while testing it, matter more than the retry:

- **The run directory is the candidate's identity card.** `run_selftest` writes the candidate to
  `<work>/<run name>/tsukuroi-census.sh` and points `HOME`/`TMPDIR` at the same directory
  (`:137-141`), so `$0`, `HOME` and `TMPDIR` all announce `baseline`, `capture`, `D-all-mutant-texts`,
  `N1-rename-counter`, `<mutant name>`, `<mutant name>.confirm` or `<name>.retry` (`:241,:243,:245,:257,:266`).
  A candidate therefore never has to read its own text to detect a mutant — the attack does not need
  `declare -f`/`BASH_ARGV0` at all. The declared decoy ("refuses a selftest that reads its own text via
  declare -f / $0 / BASH_ARGV0") is void for the `$0` half: reading `$0` gives the mutant's name, not its text,
  and no here-document can hide a directory name.
- **`params == 4` is a fixture-shape gate plus a label-text gate, not evidence of four killing cases**
  (`:162-170,:173-187`). Verified below.

## Evidence

### H1 — the kill channel is untrusted self-report; a forged `FAIL` line plus a forged summary is a kill

Code: the only kill input is stderr lines beginning `FAIL ` (`:156`), matched against the *baseline's own* PASS
labels (`:190-192`); `killed()` compares the summary's **case count only** (`:196`) and never the summary's
passed/failed fields; confirmation re-runs the **same text** and only asks for the same label to fail again
(`:264-272`); the row takes `killed(res[name]) and confirmed` (`:287`).

Demonstration (payload and full transcript: `C1CritLabels/c1-6-counterexample.txt`,
`c1-6-forged-kill.json`): a single line inserted after `run_selftest() {` in the **real** census, no mount
cases added, `probe_storage_arm` untouched:

```sh
case ${0%/*} in */baseline|*/capture|*/N[0-9]*|*/D-all-mutant-texts) : ;; *) \
  printf 'FAIL %s: forged on path, no case ran\n' \
    'healthy rollup: two btrfs lines are still btrfs without sysfs, BLOCKED (R41-C1 H10)' >&2; \
  printf 'TSUKUROI_CENSUS_SELFTEST: FAIL (128 cases, 127 passed, 1 failed)\n'; return 1 ;; esac
```

Driven through the counter's own `run_selftest`/`killed`/`failed_base_labels`:

| run (same text) | exit | cases | PASS lines | `killed()` |
|---|---|---|---|---|
| `<work>/baseline` | 0 | 128 | 128 | (baseline passes) |
| `<work>/H10-count-exactly-one` | 1 | 128 | **0** | **True** |
| `<work>/H10-count-exactly-one.confirm` | 1 | 128 | **0** | **True**, common label = the H10 label, `confirmed` **True** |
| `<work>/D-all-mutant-texts` | 0 | 128 | 128 | passes → `decoy_pass 1` |
| `<work>/N1-rename-counter` | 1 | 128 | — | **this run hit the H3 flake** (`FAIL`, `127 passed, 1 failed`), not the prologue: byte-identical re-runs at that directory print `PASS (128 cases, 128 passed, 0 failed)` and the prologue is a verified no-op for `N[0-9]*` |

Unit calls on the same functions: `{'pass':False,'exit':1,'cases':128,'labels':[],'fail_labels':['<H10 label>: forged']}`
→ `killed() True` — **zero cases executed, zero PASS lines, and a summary whose counts contradict the observed
output**. So `survivors == 0` does not say that the four declared cases killed H5/H6/H9/H10; it says something
wrote the right words twice. The declaration's kill rule is literally satisfied ("a baseline case label
failing, twice") while the case never ran.

### H2 — the decoy is bypassable without self-reading, and the confirmation is labelled as a confirmation

`:114-122` build the decoy as a dead here-document (`: <<'R41DECOY'`) carrying every mutant's replacement text.
That catches a *text* reader (control C1-K1 is exactly such a reader and trips on it). It cannot catch a
*path* reader: the honest arm list in the payload above was written from the directory basename, and the decoy
passed. The decoy also announces itself: it is the one file that contains all thirteen replacement texts plus
the baseline loop, so "more than one signature present" identifies it, and the delimiter alone does.
Confirmation is equally visible: `<mutant>.confirm` shows a forged failure is being re-checked, so a forger
knows to forge twice.

### H3 — flake: p² to fake a kill, ~2p to lose a genuine one, and the retry is on the safe arm only

Code: `:255` retries **non-mutants only**; `:149-150` turns a timeout into `cases None`; `:196` rejects any run
whose case count moved; `:291` scores "not killed" as a survivor; `:269-272` needs the *same* baseline label to
fail in both runs. Consequences:

- a flaky case that fails in an *unkilled* mutant's run **and** its confirm is a false kill (p² per survivor,
  because the counter never ties the failing label to the mutated text — any baseline label qualifies, including
  packages/journal/OOM labels);
- a flake, timeout or early abort in a **genuine** kill's first or confirm run is scored as a survivor, and
  mutants get no retry (`:255`), so the arm that *is* the measurement has no noise tolerance while the arms
  whose failure is already fatal (baseline/capture/neutral/decoy) do;
- the same event class is therefore treated as noise when it costs the producer nothing and as evidence when it
  costs the producer the round.

Measured flake input: one run of the byte-identical candidate at the byte-identical directory produced
`TSUKUROI_CENSUS_SELFTEST: FAIL (128 cases, 127 passed, 1 failed)` (demo run 15:06-15:09) while the other 20 runs
of the same bytes — including three at that same directory — printed `PASS (128 cases, 128 passed, 0 failed)`
(`c1-6-flake-probe.txt`: 8 runs 15:14-15:18 in the counter's env, 6 runs in the counter's own run-directory
names, plus the early single runs; wall 27-49 s each). The prologue was verified to be a no-op for that
directory (`bash case` on all six shapes), so a **case in the selftest body failed with no mutation present**.
The failing case's name was not kept by that driver (`run_selftest` discards stderr; the counter would keep it
in `first_fails`/`confirm_labels`), so I cannot name it: that is the honest limit of this receipt. Rate from one
event: 1/21, no interval worth quoting.

### H4 — the one retry can hide a real decoy failure

`:255-259` replaces any failed non-mutant verdict with a second attempt; `:259` records the first attempt in
`retried`, and the predicate (`:295-296`) and `decoy_pass` (`:293`) never read it. So `decoy_pass == 1` means
"passed the second attempt". A deterministic decoy failure stands (that is why C1-K1/C1-K3 show `decoy_pass 0`),
but a *nondeterministic* self-reader — the only kind a retry was added for — is admitted with probability
q(2−q) for a per-run pass probability q (1/2 → 3/4). The retry also silently absorbs baseline nondeterminism:
`baseline_pass == 1` cannot distinguish one clean run from "failed once, passed on retry", and the observed H3
flake is exactly that kind of event.

### H5 (adjacent, enabling) — `params == 4` does not attest four killing cases

`:162-170` derives P1-P4 from the fixture table alone; `:182` accepts the reason string anywhere in the case's
argument text — **including the label**. Verified with the counter's own `params_from_capture` on a scratch
capture whose case label merely *names* the reason and whose assertions are about the packages plane:
`params_by_that_gate = 4` with P1/P2/P3 carried by a one-btrfs-line fixture (`c1-6-params-label.txt`).
Verified with the counter's own `mount_props` plus a bash evaluation of the frozen mutant texts
(`c1-6-decorative-table.txt`): the table
`data btrfsdata btrfs rw 0 0` + `/dev/sda3 /data btrfs rw,relatime,subvol=/@data 0 0` has all four properties,
and H5, H6 and H9 all still yield `blocked=1 detail=mounts:btrfs-without-sysfs` on it — they would survive a
case built on that table. H10 does **not** survive a table with two btrfs lines (`mt=2, blocked=0`), so P4's
carrier must be a case that does not assert the storage line; with the label-carried reason string that is
possible, but composing and running the full fraudulent candidate was out of this seat's budget
[INFERENCE, not demonstrated]. Net: `params` constrains fixtures and wording, not kills.

### Controls coverage

`controls/controls-c1.jsonl` is actually three files, `C1-K1-declare-f-prologue-on-base`,
`C1-K2-candidate-without-H9-case`, `C1-K3-declare-f-prologue-on-candidate`.

| hole | covered? | why |
|---|---|---|
| H1 forged `FAIL` line + matching case count | **no** | K1/K3's prologue (`controls/run_controls.py:64-70`) writes `TSUKUROI_CENSUS_SELFTEST: FAIL (1 cases, 0 passed, 1 failed)` with `printf` (stdout, not the `bad()` stderr channel) and returns 1; it emits **no** `FAIL <label>` line and a case count of 1, so it is rejected twice over (`:196` case count, `:192` label). The calibrated forgery — a real label on stderr and the real case count — is untested. |
| H2 path/identity leak | **no** | all three controls are text-based (`declare -f` markers, a dropped `case_home`); none reads `$0`/`HOME`/`TMPDIR`, and none distinguishes the confirm/retry directories. |
| H3 flake double-kill / lost kill | **no** | K2 is the only surviving-mutant control and it is deterministic (one dropped case → one survivor). No control exercises a nondeterministic case, and none exercises a mutant whose confirm run fails. |
| H4 retry masking a decoy failure | **no** | K1/K3's decoy failure is deterministic, so it survives the retry; no control fails the decoy on one attempt only. K1's record does show `decoy_pass 0`, i.e. the retry did not rescue it. |
| H5 params as a shape gate | **no** | K2 shows `params 3` for a dropped case, which is the *honest* direction; no control carries a property with a decorative case. |

## Impacted axes

- **operability (C1)** — `survivors == 0` and `decoy_pass == 1` are asserted as evidence that "the round-40
  held-out survivors H5, H6, H9 and H10 fail it". Under H1+H2 they are satisfiable without the four cases; under
  H5 the `params` leg is a shape gate on the same axis. The claim's *predicate* wording stays true; its
  *attribution* wording ("a kill needs a baseline case label failing, twice") overstates what is measured —
  what is measured is that a label was printed, not that the case ran or that the mutation caused it.
- **C1 measurement robustness** — the retry policy (H3) makes the round's single permitted counter run
  load-sensitive in the direction that ends in FAIL, so a spurious FAIL burns an item's only measurement; the
  observed 1/21 flake is enough to matter at ~31 runs per invocation.
- **depth (C2)**, saturation, window: not moved by this item.

## Smallest safe correction

Measured on a scratch copy of the frozen counter; the lane was not edited; receipts in
`c1-6-patch-verification.txt`.

1. **Make the run directory opaque** — closes H2 (identity, role, and the `$0`/`HOME`/`TMPDIR` channel at once):

```python
def run_dir(work: Path) -> Path:
    return work / ('r' + secrets.token_hex(8))     # import secrets
```

   use it at `:241,:243,:245,:257,:266`, keying `res` by the run name only. Nothing else needs to change: `cwd`
   is `/` and the argv path is inside the opaque directory.
2. **Stop crediting a kill to text alone** — closes H1 (and keeps attribution on the storage plane):

```python
MOUNT_LABEL_RE = re.compile(r'\(R4[01]-C1 H(5|6|9|10)\)|mounts:btrfs-without-sysfs|btrfs')

def inventory_ok(res, base):
    if len(res['labels']) + len(res['fail_labels']) != res['cases']:
        return False
    return (res.get('sum_passed') == len(res['labels'])
            and res.get('sum_failed') == len(res['fail_labels']))

def mount_fail_labels(res, base):
    return {lb for lb in failed_base_labels(res, base) if MOUNT_LABEL_RE.search(lb)}

def killed(res, base):
    if res['pass'] or res['exit'] == 0 or res['cases'] != base['cases']:
        return False
    if not inventory_ok(res, base):
        return False
    return bool(mount_fail_labels(res, base))
```

   with `run_selftest` also returning `sum_passed`/`sum_failed` from `sm.group(3)/(4)` (`:154-159`).
   Measured: forged run `killed False` (was True, both attempts), honest baseline unchanged, and the genuine
   M2, H5 and H10 kills unchanged (`killed True`, e.g. H5 → `127 PASS + 1 FAIL = 128`, summary `127/1`). The
   label filter is deliberately loose (`btrfs` included) because three of the eighteen mount-plane labels do not
   contain "rollup"; a tighter filter needs one honest counter run to confirm all 13 still die.
3. **Do not retry the decoy** — closes H4: skip the retry when `applied[name]['kind'] == 'decoy'` (require the
   single attempt), and surface `retried` in the receipt row (it already records `first_last`/`first_fails`)
   so a baseline absorbed on the second attempt is visible instead of silent.
4. **Give the mutant arms the same one-retry rule, and treat exit 124 as could-not-evaluate** rather than a
   survivor (exit 2 / `E-TIMEOUT`), so a load flake is never scored as a defect claim under H3.

Items 1-2 are the ones that close the attack in this ticket; 3-4 fix the measurement noise direction. With 1
and 2 alone, the forgery needs a full 128-line inventory emulation plus a storage-plane label, which is a
different (and much more visible) kind of fraud than a two-line prologue.

## What I did not do

- I did not run the whole counter (19+ runs) on any variant: no variant could demonstrate more than the
  counter's own functions did, and the declaration's rule is one run per item.
- I did not build the full fraudulent candidate needed for an end-to-end `result: PASS` (four decorative
  `params` carriers + the path-gated prologue). The kill half is demonstrated end to end; the `params` half is
  demonstrated only as gates (H5), and the composition is marked [INFERENCE].
- I did not identify the flaky case (H3): the driver that observed it discarded the run's stderr. Reproducing it
  needs a run whose `first_fails` is kept — which the counter already does.
- No tools installed or upgraded; no package, service, mount or lane state touched. Scratch under
  `/fast/scratch/hyaku/tsukuroi-r41/C1CritLabels/` removed at the end.
