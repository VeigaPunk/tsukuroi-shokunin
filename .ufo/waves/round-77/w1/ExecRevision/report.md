# ExecRevision — independent C2 factual audit

Axes: depth (8, lowest tied); freshness (9). Verdict: **all three frozen corrective strings are factually supported for the specified inputs**. Registry inputs were read from committed objects, not the changing working tree. The specified staged package is a read-only working-tree input, not identical to its repository's committed version; this distinction is material and retained below. No production changes, promotion, instrument changes or score claim.

## Commands, exits and retained receipts

Every subprocess used `TMPDIR=/fast/scratch/hyaku/tsukuroi-r77/ExecRevision`; Python's `subprocess.run(..., capture_output=True, text=True, env=env)` retained stdout, stderr and exit individually in `commands.json`. Its git argv use absolute `-C` paths. All eight commands in that receipt exited **0**:

1. `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 780bad66cd0d62a58153bad541531ebc4f349c4e:corpus/SOURCES.md`
2. Same command at `06f1bbbb803790b35358d277bb7807b82a9fab99`.
3. `git -C /home/vgpnk/Projects/shokuknow rev-parse HEAD` → `8b94c5c12c0521e4cd9ed8e5b6939afd8518c715`.
4. `git -C /home/vgpnk/Projects/shokuknow show 8b94c5c12c0521e4cd9ed8e5b6939afd8518c715:merge/tsukuroi/SOURCES.append.md`.
5–6. `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5:.ufo/waves/round-77/before/expected.json` and the same prefix with `collisions.json`.
7–8. `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 06f1bbbb803790b35358d277bb7807b82a9fab99:corpus/lessons/round-76.md` and the same prefix with `round-76-verifier-spotcheck.md`.

Additional executed commands, all exit **0**: `git show eb4bedb92da4d0d2ea2808d4e9e6ad7c9d429be5:SCORECARD.md` in the absolute lane cwd (frozen declaration read); `git ls-tree -r --name-only 06f1bbbb803790b35358d277bb7807b82a9fab99 shokuknow merge corpus/lessons/round-76-verifier-spotcheck.md corpus/SOURCES.md` in that cwd (outputs the latter two paths); `git log -1 --format=%H -- merge/tsukuroi/SOURCES.append.md` in `/home/vgpnk/Projects/shokuknow` → `ba6779f0160d12dd7373627e00291d6d5e3ba7ee`; absolute `mkdir -p` and final `rm -r --` of this seat's scratch directory (empty stdout/stderr). No fixture git mutation was used.

`evidence.json` retains full registry id lists at both revisions, complete staged and intersection lists for both the specified package and the committed-package comparison, digests, exact frozen repair strings, and indentation fixture bytes/results. Python Eval analysis cells completed normally without exceptions; those are not external process exit codes. Initial wrong-location discovery under `/home/vgpnk/Projects/shokunin/shokuknow` returned path-not-found; parent-directory discovery located the actual sibling checkout. No installed tools.

## Independent extraction

Executed extraction in Python:

```python
pattern = r'^ {0,3}\|\s*(S[0-9]{3,})\s*\|'
def extract(text, registry=False):
    if registry:
        text = re.split(r'^## Registry\s*$', text, flags=re.M)[1]
        text = re.split(r'^## ', text, flags=re.M)[0]
    return re.findall(pattern, text, re.M)
# Both committed registries: extract(text, True).
# Staging: extract(text), a single registry table without a Registry heading.
# Collisions: sorted(set(registry_ids) & set(staged_ids)).
```

| Registry revision | Rows | Unique ids | S323 | Specified staged rows/unique | Intersection |
|---|---:|---:|---|---:|---:|
| `780bad66cd0d62a58153bad541531ebc4f349c4e` | 323 | 323 | present | 147 / 147 | 124 |
| `06f1bbbb803790b35358d277bb7807b82a9fab99` | 323 | 323 | present | 147 / 147 | 124 |

Both registry blobs have SHA-256 `e5f540d5ac0620438f7c24ed09c6d9f89794c8562b486df1e9b03d790316e360`; neither has duplicate extracted ids. Whole-file row extraction also gives 323, so section scoping does not hide extra matching rows. Every base registry id, specified staged id and intersection id matches the corresponding frozen `collisions.json` list exactly.

Specified read-only input: `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md`, SHA-256 `7914d3b93cea2015c00091d7db28ca2acd289d5097cb513ad1176dc0d7148406`. Its bytes differ from the same path at staging HEAD `8b94c5c1...`: the committed file has SHA-256 `6ddc98c10063788be5bb0157ed96b0ce35da759bac3df7d7591fbad3ecbd11f8`, **107 ids and 107 intersections** at either registry revision. Therefore **“147 staged ids / 124 intersections derived exclusively from committed shokuknow HEAD bytes” would be inaccurate**. The frozen correction does not make that stronger claim: its base registry is committed and its full input id lists are preserved in committed `before/collisions.json`. Do not silently substitute the committed package for the specified read-only staged package.

### Indentation control

One fixture at the assigned absolute scratch path contained S001 unindented, S002 with **three leading spaces**, S003 with one, S004 with two, and S005 with four. Executed extraction yielded exactly `[S001, S002, S003, S004]`; the four-space row was excluded as the frozen expression requires. A strict `^\|` control returned only S001, demonstrating why it is not interchangeable. Fixture bytes and expected/actual ids are durable in `evidence.json`; its scratch tree was removed successfully before handoff.

## Exact repairs: source truth

1. **R77-GATE-SHAPE — supported.** The base lesson's Search log says “included four, rejected none this round”; its original Gate contains admits but no reject row. Committed closure section 3 explicitly says “agree on the round's rejections; disagreement on the Gate shape” and names pre-correction JD3 and the withheld package. The closure identifies initial JD3 FAIL and its subsequent correction. Pinned manager line 168 uses `LESS_BY`; macro snapshot lines 320–325 define saturated subtraction, not minimum. The correction explicitly qualifies the Search-log sentence as an account of the **whole round**, avoiding an inaccurate claim that one of the four opened upstream sources was rejected. The flip is hypothetical, not an assertion that a minimum-using revision exists. The cited outside check belongs to round 76; it is not round-77 admission.
2. **R77-GATE-COUNT — supported.** The base lesson's “Registry 317 → 322 rows” is inaccurate: the requested measured revision has 323 rows, including S323. Independent section-scoped and whole-file regex counts agree at 323. The frozen string's displayed grep command was not separately executed; this seat used the indentation-tolerant extraction above and retained all ids. The correction's cited observed exit 0 is consistent with its nonzero matching-row count; this seat does not claim to have rerun that grep invocation.
3. **R77-COLLISION-COUNT — supported for the specified staged input.** The old lesson says 114 of 147; independently measured input sets give 124 of 147. Exact list equality to the frozen receipt confirms more than just equal totals. This does not authorize assimilation or establish release of an operator hold. Committed-only staging produces the different 107/107 figures explained above.

An additional **inaccurate closure summary**, not repeated by the three repairs: section 3 says “4 admits + 2 reject-shaped decisions” while its table explicitly includes **five** admitted source ids S318, S319, S320, S321 and S323, plus the S314 reject and Gate-reject sample. “Four” can describe the original four-source Gate but not all admitted-id entries re-opened in that table. Also its table's shorthand “Gate says rejected none” mislocates that literal text: it is in the Search log, as closure defect 2 and the R77 correction correctly clarify. These do not falsify the three frozen correction strings.

## Limits and delivery

All three exact strings are absent from the committed round-77 base lesson. This audit validates factual inputs; it does **not** run the production C2 instrument, attest an integrated revision, recheck external authority, prove universal arithmetic, or claim startup-normalized metrics. Production integration and post-integration verification remain L1-owned. No LSP facility is mounted; this text/data audit required no symbol refactor. No builds, linters, formatters, census, host probes, package transactions, raw journal reads, credential reads, git mutations or sibling writes were performed.

Write-scope conflict: the trailing requested `.ufo/waves/round-77/w1/ExecRevision.md` lies outside the explicitly sole write directory. This report is delivered at the acceptance path inside `ExecRevision/`; the outside trailer file was intentionally not written.

Self-evaluation (advisory, not judging the round): accuracy 4/5 (staging history beyond the pinned HEAD comparison not investigated); completeness 5/5 (both revisions, full lists, indentation, all repairs and cleanup covered); clarity 4/5 (necessary distinction between committed and staged-package inputs adds complexity); actionability 5/5 (exact receipts and revision pins retained); conciseness 4/5 (full stdout deliberately externalized to commands.json). Average 4.4/5. Main improvement: preserve the specified staged-package digest with any eventual promotion record so the 147/124 claim is never mistaken for its repository HEAD's 107/107 result.
