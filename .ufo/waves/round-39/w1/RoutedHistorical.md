VERDICT: draft

# RoutedHistorical — round-39 routed defect 6 (historical instrument pins)

Item A-4: draft append-only `SKILL.md` registry notes (registry-table format) that mark
`tools/score-pacnew-arm-r35b.py` historical (base-parity failures at post-`52ffd65` census revisions) and
`tools/score-storage-arm-r38.py` fixture `F06` superseded by the round-39 absent-root rule, each pinned with
the census revision it must be read at. Exact markdown is in §4. Nothing was written to `SKILL.md` or any
tracked lane file.

## 1. What was run

All runs were read-only, non-root, with `env -i PATH=/usr/bin:/bin LC_ALL=C HOME=<scratch>/home
TMPDIR=<scratch>/tmp`. Scratch: `/fast/scratch/hyaku/tsukuroi-r39/RoutedHistorical` (removed at the end;
copies kept under `.ufo/waves/round-39/w1/RoutedHistorical/`). Lane tip at measurement:
`394e1ba4fab39a417abe66a7802f87cf1ff8dd61` (dispatch named `2e1c2a40…`; the lane moved on).

    python3 tools/score-pacnew-arm-r35b.py --lane <lane> --revision <REV> [--skip-battery]
    python3 tools/score-storage-arm-r38.py   --revision <REV> --repo . --scratch <scratch>
    bash <git show REV:tools/tsukuroi-census.sh>   # F06-shaped: TSUKUROI_BTRFS_SYSFS=<nonexistent>, mounts unset

Census blob chain measured with `git rev-parse <REV>:tools/tsukuroi-census.sh`:

| revision | census blob | note |
|---|---|---|
| `b40c01df38eb26f74c095c471efc6d1649b00fd4` | (no `DRIFT`, no `STORAGE`; 0 `STORAGE` hits) | r35 claim base |
| `e2f97e6e4beaadda8e1d5ae7bd08baa0e82d61e0` | `10b6d47046c9523bfeefd56c76a06ecc59ea5e01` | `DRIFT pacnew-plane` lands (2026-10-23) |
| `7cbaeb6317cb9f7323d2619eec02db4e4da29449` | `10b6d470…` (same) | `52ffd65^`, r38 freeze |
| `52ffd65f868431f021b8615ab281efd87195eac6` | `119b645349b5eadf182aaa473d2fac38eadea45a` | `STORAGE` arm lands |
| `02eeed07f1c9142a037cab9cd40161feebc3ca67` | `8ef604c001ae2b2edc1598a6dd3877f30dc13de5` | storage hardening |
| `b0005ae9f56fd5a006fc5ec026578c88e2b64b26` | `8ef604c0…` (same) | r38 measured revision |
| `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` | `e3ff0be1299a7704608d304097073510631e28e5` | r39 absent-root rule |
| `394e1ba4fab39a417abe66a7802f87cf1ff8dd61` | `e3ff0be1…` (same) | measured tip |

`git log e2f97e6e^..7cbaeb63 -- tools/tsukuroi-census.sh` names only `e2f97e6e`, and
`git log 52ffd65..HEAD -- tools/tsukuroi-census.sh` names only `02eeed07` and `49cc53c7`: the two windows are
contiguous single-blob surfaces, so endpoint measurement covers each window.

## 2. Measured outcomes

`score-pacnew-arm-r35b` (receipts `r35b-<rev>.jsonl`):

| revision | mode | candidate | reason | control | exit |
|---|---|---|---|---|---|
| `b40c01df` | skip-battery | 0/24 | `drift_lines=0` on all 24 | — | 1 |
| `e2f97e6e` | skip-battery | **24/24** | — | — | **0** |
| `7cbaeb63` | skip-battery | **24/24** | — | — | **0** |
| `52ffd65` | skip-battery | 4/24 | `base parity` on all 20 stub views | — | 1 |
| `52ffd65` | battery | 4/24 | — | 24 | 1 (`should_fail_accepted` 0 of 17, `harness_errors` empty) |
| `49cc53c7` | skip-battery | 4/24 | `base parity` on all 20 stub views | — | 1 |

The four matching views at post-`52ffd65` revisions are the 3 namespace views and the live view, which carry
no base comparison (parity is defined "in a stub view", `tools/score-pacnew-arm-r35b.py:426-433`).

`score-storage-arm-r38` (receipts `r38-<rev>.jsonl`):

| revision | fixtures | live | six | result |
|---|---|---|---|---|
| `52ffd65` | 10/10 | 1 | 1 | PASS exit 0 |
| `02eeed07` | 10/10 | 1 | 1 | PASS exit 0 |
| `b0005ae9` | 10/10 | 1 | 1 | PASS exit 0 |
| `49cc53c7` | 9/10 | 1 | 1 | FAIL exit 1 — `F06-no-btrfs-root` expected `HEALTHY 0 0 0`, got `BLOCKED 0 0 0`, line `STORAGE … detail=mounts:btrfs-without-sysfs` |
| `394e1ba` | 9/10 | 1 | 1 | FAIL exit 1 — same single mismatch |

F06-shaped census runs (`f06-shaped-boundary.txt`), env exactly the counter's `run_census`
(`PATH`, `LC_ALL`, `HOME`, `TMPDIR`, `TSUKUROI_BTRFS_SYSFS=<nonexistent path>`):

| census revision | `STORAGE` line |
|---|---|
| `52ffd65`, `02eeed07`, `b0005ae9` | `STORAGE btrfs-device-stats state=HEALTHY filesystems=0 devices=0 nonzero=0` |
| `49cc53c7`, `394e1ba` | `STORAGE btrfs-device-stats state=BLOCKED filesystems=0 devices=0 nonzero=0 detail=mounts:btrfs-without-sysfs` |

Every run printed six `PLANE` lines and one `TSUKUROI_CENSUS:` line. `awk '$3=="btrfs"' /proc/self/mounts`
lists four mounts here (`/`, `/home`, `/var/cache/pacman/pkg`, `/var/log`; `host-btrfs-mounts.txt`), which is
exactly what the post-rule arm reads when the counter leaves `TSUKUROI_PROC_MOUNTS` unset.

## 3. Findings

- **F1 — both landed prose notes are off by one on inclusivity.** `SKILL.md:3147-3149` says "at any revision
  after `52ffd65` it reads `base parity` failures"; measured, `52ffd65` itself already reads 4/24
  (`r35b-at-52ffd65.jsonl`). `SKILL.md:3221-3224` says "at revisions after `49cc53c7` it reads BLOCKED and
  that counter FAILs 9/10"; measured, `49cc53c7` itself FAILs 9/10 (`r38-49cc53c7….jsonl`). The draft states
  both boundaries as inclusive.
- **F2 — the r35b counter is not a valid reading at its own claim base.** At `b40c01df` it reports 0/24 with
  `drift_lines=0`, because that census predates the arm; the valid window starts at the arm-landing commit
  `e2f97e6e`, not at the base. The operative row (`SKILL.md:3110`, "claim base b40c01df") and the consumer
  note ("valid at its round-35 revisions") name no revision, which is what let the two claims drift apart;
  the draft names the blob and both ends of the window.
- **F3 — F06's supersession is structural, not incidental.** `run_census` sets only `TSUKUROI_BTRFS_SYSFS`
  (`tools/score-storage-arm-r38.py:154-160`); on any host whose default mount table lists a btrfs mount, the
  post-rule arm necessarily returns BLOCKED for F06, whose expectation is hard-coded `('HEALTHY', 0, 0, 0)`
  (`:82`). The counter cannot be rescued by re-pinning a different revision alone; only a new freeze with the
  two seams and a corrected F06 expectation would, and that is not proposed here.
- **F4 — the r38 counter is not globally superseded: only F06 is.** At `49cc53c7` and `394e1ba` the live leg
  still matches (`live_match` 1) and the plane count holds (`six_planes_all` 1); F01-F05 and F07-F10 still
  match. The draft records this so a later reader does not discard the whole instrument.
- **F5 — the failure is not a harness artifact.** Battery mode at `52ffd65` keeps `control_matches` 24 and
  `should_fail_accepted` 0 of 17 while the candidate scores 4 (`r35b-battery-52ffd65.jsonl`): the census at
  the named revision is what fails, not the counter's scaffolding.
- **F6 — placement matters for my own draft.** The highest-table selector takes the section whose heading
  matches `^## Gate and probe registry — round([0-9]+) superseding current rows$` and ends at the next
  `#`/`##` heading (`tools/check-registry-coverage.py:52-54,196-222`). The operative section still carries the
  round36 title (`SKILL.md:3050`) and holds the r37-r39 rows. The draft therefore appends its own `##` heading
  at end of file (currently `SKILL.md:3224`) so the two historical rows are outside the operative section and
  cannot displace it; §4 says this in the note itself.
- **F7 — limit of the pin's lower r35b bound.** The counter's parity reference is the `b40c01df` census, whose
  stdout omits the DRIFT line; the 24/24 pass at `e2f97e6e`/`7cbaeb63` is measured, and F5 explains why the
  missing base line does not break alignment of `others()`. No revision between `e2f97e6e` and `7cbaeb63`
  needs separate measurement because both read blob `10b6d470…`, verified above.

## 4. Proposed text (exact markdown, append after the current last line, `SKILL.md:3224`)

```markdown
## Historical instrument pins — round 39

Appended 2026-10-26 (round-39 routed defect 6, seat RoutedHistorical). Append-only: every earlier row and the
two prose consumer notes (`SKILL.md:3147-3149`, `SKILL.md:3221-3224`) stay as written. Both of those notes say
"after `52ffd65`" and "after `49cc53c7`"; measured, both boundaries are **inclusive** — each instrument
already fails at the commit named. This section starts with its own heading, so it sits outside the operative
registry section and the highest-table selector is unchanged; the two rows restate the instruments as
historical readings, pinned to the census revision each must be read at. A revision outside a pin is an
out-of-window reading, not a regression.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| historical-pacnew-arm-r35b | probe | `python3 tools/score-pacnew-arm-r35b.py --lane <repo> --revision <REV> [--skip-battery]` | inside the pin only: 0 candidate and control match every view and no should-fail arm is accepted;1 otherwise;2 harness error | the battery itself (control arm plus 17 should-fail arms) | HISTORICAL. Read only where `tools/tsukuroi-census.sh` is blob `10b6d47046c9523bfeefd56c76a06ecc59ea5e01`: `e2f97e6e4beaadda8e1d5ae7bd08baa0e82d61e0` (the arm lands) through `7cbaeb6317cb9f7323d2619eec02db4e4da29449` (`52ffd65^`). Measured skip-battery 24 of 24, `harness_errors` empty, exit 0 at `e2f97e6e` and at `7cbaeb63`. Not a reading at the claim base `b40c01df38eb26f74c095c471efc6d1649b00fd4`: 0 of 24, all 24 `drift_lines=0` — the base is the parity reference and predates the arm; at `52ffd65f868431f021b8615ab281efd87195eac6` and `49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82` it reads 4 of 24 with `base parity` on all 20 stub views, exit 1 (battery mode at `52ffd65`: candidate 4, control 24, `should_fail_accepted` 0 of 17). Cause: the round-38 `STORAGE` line is a non-DRIFT line that `judge()` compares with the claim base (`tools/score-pacnew-arm-r35b.py:426-433`), and the census prints it after `DRIFT pacnew-plane` (`tools/tsukuroi-census.sh:3077`, line numbers at the measured tip `394e1ba4fab39a417abe66a7802f87cf1ff8dd61`) | private temp fixtures; unprivileged user+mount namespace; live view reads /etc names and pacman.log read-only | tsukuroi |
| historical-storage-arm-r38-f06 | gate | `python3 tools/score-storage-arm-r38.py --revision <REV> [--repo <PATH>] [--scratch <DIR>]` | inside the pin only: 0 ten fixtures, the live leg and six PLANE lines per run match;1 any fixture, the live leg or the plane count differs;2 revision, git or bash could-not-evaluate | none: the ten built-in fixtures F01-F10 and the live leg are the measurement | HISTORICAL at fixture `F06-no-btrfs-root` only. Read only where `tools/tsukuroi-census.sh` is blob `119b645349b5eadf182aaa473d2fac38eadea45a` (`52ffd65f868431f021b8615ab281efd87195eac6`, the arm lands) or `8ef604c001ae2b2edc1598a6dd3877f30dc13de5` (`02eeed07f1c9142a037cab9cd40161feebc3ca67`, hardening; `b0005ae9f56fd5a006fc5ec026578c88e2b64b26` reads the same blob), i.e. `52ffd65 <= REV < 49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82`: measured PASS 10 of 10, `live_match` 1, `six_planes_all` 1, exit 0 at `52ffd65`, `02eeed07` and `b0005ae9`. F06 is superseded by the round-39 absent-root rule in the section above (commit `49cc53c7`): it declares an absent override root clean as `('HEALTHY', 0, 0, 0)` (`tools/score-storage-arm-r38.py:82`) while its census environment sets only `TSUKUROI_BTRFS_SYSFS` and never `TSUKUROI_PROC_MOUNTS` (`:154-160`), so the default `/proc/self/mounts` is read and this host's four btrfs mounts make the post-rule arm print `BLOCKED ... detail=mounts:btrfs-without-sysfs` (`tools/tsukuroi-census.sh:1906-1914` at the measured tip). Measured at `49cc53c7` and at `394e1ba4`: 9 of 10, F06 expected `HEALTHY` got `BLOCKED`, exit 1, with `live_match` 1 and `six_planes_all` 1 still holding — the failure is F06 alone, by construction. The absent-root case is scored now by `storage-hidden-r39` (hidden legs H1/H2) | private mkdtemp fixtures under `--scratch`/`TMPDIR`; reads the census at REV through git; no host write | tsukuroi |
```

## 5. Touched surfaces and boundaries

- Lane: read-only. Only `.ufo/waves/round-39/w1/RoutedHistorical.md` (this report) and
  `.ufo/waves/round-39/w1/RoutedHistorical/` (receipts) were created. No `SKILL.md`, `SCORECARD.md`,
  `corpus/`, `tools/` or Git/jj state was touched; no `git add/commit/stash/checkout/reset/push`; no `jj`.
- Host: no package, service, mount, sysfs, journal or `/etc` change; no `sudo`; no tool install (nothing
  needed). The census and counters ran read-only against the live host, as their own contracts allow.
- Scratch removed: `/fast/scratch/hyaku/tsukuroi-r39/RoutedHistorical` deleted after the receipts were
  copied; the originals are the two windows' endpoints, reconstructible from the files in §6.

## 6. Receipts

Under `.ufo/waves/round-39/w1/RoutedHistorical/`:

- `r35b-b40c01df38eb26f74c095c471efc6d1649b00fd4.jsonl`, `r35b-e2f97e6e.jsonl`,
  `r35b-7cbaeb6317cb9f7323d2619eec02db4e4da29449.jsonl`, `r35b-at-52ffd65.jsonl`,
  `r35b-battery-52ffd65.jsonl`, `r35b-49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82.jsonl` — one JSON record per
  run with `candidate_matches`, `of`, `control_matches`, `should_fail_accepted`, `harness_errors`, `exit_code`
  and per-view rows.
- `r38-52ffd65.jsonl`, `r38-02eeed07f1c9142a037cab9cd40161feebc3ca67.jsonl`, `r38-b0005ae9.jsonl`,
  `r38-49cc53c7b40ec2cac4bb9cd2fffcb1e1513adf82.jsonl`, `r38-394e1ba4fab39a417abe66a7802f87cf1ff8dd61.jsonl`
  — `fixtures_matched`, `live_match`, `six_planes_all`, `result`, `exit`, and the per-fixture `expected`/`got`/
  `storage_lines`.
- `f06-shaped-boundary.txt` — the five F06-shaped census runs with the blob id printed per run.
- `host-btrfs-mounts.txt` — the four btrfs mounts read from `/proc/self/mounts`.

## 7. Not done / out of scope

- `tools/score-storage-arm-r38-q82.py` was **not** run at post-rule revisions. Its views bind forged trees that
  carry an fsid directory, so the `fsn == 0` branch is normally not reached, but whether any random view can be
  empty is unmeasured here; this draft therefore says nothing about the q82 sibling.
- The r35b **battery arms** were not re-run at `7cbaeb63` or `e2f97e6e`; both were scored in skip-battery mode,
  and battery mode was run at `52ffd65` only. The window claim rests on the shared `judge()` plus the measured
  candidate outcomes.
- No TO1-TO8 rows were judged (this seat did not review the C2 entry), so no `TO<n>:` lines are emitted.
- No claim about the round-39 C1/C2 predicates is made; this seat only pins two historical instruments.
