VERDICT: supports

G-4 (causal separability of C1 and C2) holds on the declared commits. Building the two changes apart,
each one moves its own counter and leaves the other at its base value. One defect in the item's
construction sentence (D1) and one counter-blindness note (N1) follow the evidence.

All work in a scratch clone under `/fast/scratch/hyaku/tsukuroi-r41/CritSeparability/`
(`TMPDIR` set there; the clone's `--scratch` arguments pointed there). The lane was never written:
`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain` before my work showed the
same pre-existing entries (`M tools/check-self-assessment.py`, untracked `.ufo/waves/round-41/w1/`,
`w1.ready*`, `make-w1-spec.py`, `revs.json`, `w1-dispatch.*`, `w1-spec.json`,
`corpus/lessons/round-41.md`) and I added none of the tracked ones (only this seat's directory).

## 1. Construction

Clones: `git clone -q --shared <lane> $S/{A,B,B0}`; `git -C $D remote remove origin`;
toplevel check `[ "$(git -C $D rev-parse --show-toplevel)" = "$D" ]` printed the clone path for A, B and B0;
`git -C $D reset --hard -q d8b4d5217b2a74c7b7cddd33351c2a0cce5e8b84`; cherry-picks with the fixture identity only
(`-c user.name=fixture -c user.email=fixture@shokunin.local`).

    A  = 566adebcc4c2400d3f3d33f272399e7aa4a93710   d8b4d521 + cherry-pick 568c397d
    B  = 1727abf9e7d76fb0154d32bcc6b2439df3d6672a   d8b4d521 + cherry-pick c7c40c0f, 9cc9aa77
    B0 = 9e0cf5d138ebc3f9a0b34093a46ed7a9871434b7   d8b4d521 + cherry-pick c7c40c0f      (control, §5)

File sets are disjoint, line for line from the declaration commit:

    $ git -C $S/A diff --name-only d8b4d521 HEAD     -> tools/tsukuroi-census.sh
    $ git -C $S/B diff --name-only d8b4d521 HEAD     -> corpus/SOURCES.md
                                                        corpus/knowledge/alpm-package-anatomy-r41.md

The census is byte-identical across the intended pairs, so neither build carries a stray census edit:

    $ git -C $S/A show HEAD:tools/tsukuroi-census.sh | sha256sum
    646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95  -      # == git show 71851d63:tools/tsukuroi-census.sh
    $ git -C $S/B show HEAD:tools/tsukuroi-census.sh | sha256sum
    032faa8f1c914dd63a1de673aa9ed6767c4bd19cdfc2751ac34331005da45733  -      # == d8b4d521 == base 0e5805a1
    $ git -C <lane> diff --numstat 0e5805a1 d8b4d521 -- tools/tsukuroi-census.sh   -> (empty: base census == declaration census)
    $ git -C <lane> diff --numstat d8b4d521 71851d63 -- tools/tsukuroi-census.sh   -> 27  0  tools/tsukuroi-census.sh

`568c397d` is one hunk, `@@ -3034,6 +3034,33 @@`, inside `run_selftest` (defined at
`tools/tsukuroi-census.sh:1928`; `probe_storage_arm` at `:1865` untouched) — the declared surface.

## 2. Result matrix

| build | C1 (`score-selftest-mounts-r41.py`) | C2 (`check-package-anatomy-r41.py`) |
|---|---|---|
| base 0e5805a1 (frozen before receipts) | FAIL survivors 4 H5/H6/H9/H10, params 0 | FAIL entry absent 0/0/0/0 |
| **A** declaration + census change | **PASS** (exit 0): survivors 0, params 4 | entry absent: rules 0, verdicts 0, host 0, source 0 (exit 1) |
| **B** declaration + C2 entry change | survivors 4 H5/H6/H9/H10, params 0 (exit 1) | **rules_verified 8, host_ok 6, source_ok 1**, verdicts_ok 0 (exit 1) |

Both C1 runs are the declared expectations exactly ("The C1 counter must PASS on A and give survivors 4 on
B"; "The C2 counter must give rules_verified 8 / host_ok 6 on B ... and the entry absent on A"). Each move
leaves the other counter at the base receipt's value: A's C2 numbers equal
`.ufo/waves/round-41/before/c2-before.jsonl` (`entry_present False, rules_verified 0, verdicts_ok 0,
host_ok 0, source_ok 0, FAIL`), B's C1 numbers equal `.ufo/waves/round-41/before/c1-before.jsonl`
(`survivors 4, survivor_names [H10-count-exactly-one, H5-mountpoint-absolute, H6-source-devonly,
H9-subvolkey-option], params 0, baseline_pass 1, FAIL`). That is the 2x2 separability the item asks for,
and it is not an artefact of the two counters reading the same input: the C1 counter names no corpus path
(`grep -n "corpus|alpm-package-anatomy|SOURCES" tools/score-selftest-mounts-r41.py` -> docstring line 6 only)
and the C2 counter names no census (`grep -n "census|selftest" tools/check-package-anatomy-r41.py` -> no match).

## 3. C1 on A — PASS (one run, `--jobs 4`)

    $ python3 $S/A/tools/score-selftest-mounts-r41.py --repo $S/A --revision 566adebc... --branch master \
        --scratch $S/c1A --jobs 4
    exit=0  start 2026-10-26T15:08:40-03:00  end 15:14:44  (6m04s; load average 62.83 at start, 32 cores)

    baseline_pass = 1     baseline cases = 128   capture_pass = 1
    neutral_pass = 3      decoy_pass = 1         mutants_applied = 13
    survivors = 0         params = 4             result = PASS
    param_cases: P1-mountpoint-not-absolute, P2-source-not-dev, P3-no-subvol-option, P4-two-btrfs-lines
                 (each carrying "BLOCKED (R41-C1 H5|H6|H9|H10)")

Receipt: `.ufo/waves/round-41/w1/CritSeparability/c1-A.json`; stderr empty.

## 4. C1 on B — survivors 4, exactly H5/H6/H9/H10 (one run, `--jobs 4`)

    $ python3 $S/B/tools/score-selftest-mounts-r41.py --repo $S/B --revision 1727abf9... --branch master \
        --scratch $S/c1B --jobs 4
    exit=1  start 2026-10-26T15:14:51-03:00  end 15:18:52  (4m01s)

    baseline_pass = 1     baseline cases = 124   neutral_pass = 3   decoy_pass = 1
    mutants_applied = 13  survivors = 4  survivor_names = [H10-count-exactly-one, H5-mountpoint-absolute,
                                         H6-source-devonly, H9-subvolkey-option]
    params = 0            result = FAIL
    param_cases: all four keys present, every value list empty
    killed: M1-VA-device-literal M2-VB-root-mountpoint M3-VC-substring-btrfs M4-VG-subvolid-256 M5-a-grep-count
            M6-b-fstype-casefold M7-e-guard-drops-blocked M8-subvol-at-literal M9-last-line-only

Baseline 124 vs A's 128 is exactly the four added cases, and `decoy_pass = 1` on B shows B's census carries
no mutant replacement text — so B's survivor set is the base census's own, not a decoy artefact.
Receipt: `.../CritSeparability/c1-B.json`; stderr empty.

## 5. C2 on A and B

    $ python3 $S/A/tools/check-package-anatomy-r41.py --repo $S/A --revision 566adebc... --branch master
    exit=1  entry_present=false  rules_verified=0  verdicts_ok=0  host_ok=0  source_ok=0
            duplicate_rows=0 duplicate_headings=0 novelty_base_hits=0   result=FAIL

    $ python3 $S/B/tools/check-package-anatomy-r41.py --repo $S/B --revision 1727abf9... --branch master
    exit=1  entry_present=true   rules_verified=8  verdicts_ok=0  host_ok=6  source_ok=1
            duplicate_rows=0 duplicate_headings=0 novelty_base_hits=0   result=FAIL
            rules verified: PA1 PA2 PA3 PA4 PA5 PA6 PA7 PA8

Receipts: `.../CritSeparability/c2-A.json`, `c2-B.json`. C2 cannot reach PASS inside either build because
`verdicts_ok` needs the wave-1 reviewer files (`VERDICT_DIRS` = `.ufo/waves/round-41/w1`,
`.ufo/waves/round-41/residual`), which are seat deliverables and are committed in neither build — as the item
states ("verdicts are absent in both").

## 6. D1 — defect: the item's B cannot be built literally

`git -C $S/B cherry-pick 9cc9aa77` on d8b4d521 fails, and must: the entry file the counter reads is created
by `c7c40c0f` ("corpus/knowledge/alpm-package-anatomy-r41.md | 62 ++++"), while `9cc9aa77` only refines 3 lines
of it (`git show --stat 9cc9aa77` -> `1 file changed, 3 insertions(+), 3 deletions(-)`).

    $ git -C $S/B cherry-pick 9cc9aa77
    error: could not apply 9cc9aa77... round-41: C2 pre-dispatch refinement (PA1 data files, PA3 sort condition
    and stop point, PA6 unreadable mtree path)
    $ git -C $S/B status --porcelain
    DU corpus/knowledge/alpm-package-anatomy-r41.md

Aborted; B was then built from the C2 commit set `{c7c40c0f, 9cc9aa77}`, i.e. the C2 artifact state the
declaration pins at commit `9cc9aa77`. Under the literal reading the entry is absent on B and
`rules_verified = 0`, so the item's own predicate could not be met by any correct construction.

Counterexample to the literal wording, evidence: the two lines above.

Impacted axes: C2 depth (B's `rules_verified`), C1 unaffected. This is item text, not the frozen claim:
`SCORECARD.md:2454` ("Round 41 — declaration") contains no A/B construction, and no separability wording, so
no frozen predicate is contradicted.

Smallest safe correction (replace the construction sentence):

    build A = d8b4d5217b2a74c7b7cddd33351c2a0cce5e8b84 + only 568c397da11339aed65181be598414f268835555's
    change and B = d8b4d5217b2a74c7b7cddd33351c2a0cce5e8b84 + only the C2 entry changes as at
    9cc9aa77e30e0e23de2d4d2697b3b218ada02969 (c7c40c0f then 9cc9aa77; 9cc9aa77 alone does not apply because
    c7c40c0f creates the entry file)

## 7. N1 — the frozen C2 counter cannot tell c7c40c0f from 9cc9aa77

B0 = d8b4d521 + c7c40c0f only scores identically to B:

    $ python3 $S/B0/tools/check-package-anatomy-r41.py --repo $S/B0 --revision 9e0cf5d1... --branch master
    exit=1  entry_present=true  rules_verified=8  verdicts_ok=0  host_ok=6  source_ok=1  result=FAIL

Receipt `.../CritSeparability/c2-B0.json`. So the three corrections the declared commit makes (PA1 data files,
PA3 sort condition and stop point, PA6 unreadable mtree path) are invisible to every counter field: the
counter credits the unrefined entry 8/8 as well. Those three corrections rest on the per-row reviewer verdicts
and the pinned sources alone (`frozen/src/alpm-package.7.raw`, `makepkg.sh.in`, `check.c`), not on a measurement.
Not a separability failure; an observability limit worth recording next to the declared lexical-gate limit.

## 8. Not done / limits

- No C1 run at base 0e5805a1 by me: the base C1 figures quoted are the lane's before receipt
  (`.ufo/waves/round-41/before/c1-before.jsonl`); B reproduces them structurally (census sha256 equal).
- One C1 run per build as instructed (`--jobs 4`). Neither receipt records a retry (`baseline` has no `retried`
  key; no neutral or decoy carries one) and no record shows exit 124/137; on A all 13 applied mutants were
  confirmed killed (`confirmed` == `killed` == 13), on B the nine base-census mutants were confirmed killed
  and H5/H6/H9/H10 survived (`confirmed` == `killed` == 9).
- No package, service, sysfs, mount, `/etc` or sudo action; no tool installed or upgraded; no pacman transaction.
  Read-only `git show/diff/ls-tree/cat-file` in the lane, all mutations inside the scratch clones.
- Scratch `/fast/scratch/hyaku/tsukuroi-r41/CritSeparability/` (656 MB at peak: two clones, a third clone,
  c1A/c1B work dirs) removed before finishing; receipts kept in
  `.ufo/waves/round-41/w1/CritSeparability/` (`c1-A.json` 62369 B, `c1-B.json` 40939 B, `c2-A.json` 2408 B,
  `c2-B.json` 3922 B, `c2-B0.json` 3922 B).
