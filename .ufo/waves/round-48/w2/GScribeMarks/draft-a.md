
## Gate status — round 48 (GR1-GR3 admitted)

Round 48 read GR1-GR3 through the seat-written channel of its one counted wave (`w2`): `tools/check-scrub-admission-r48.py`
(frozen with the claims at `ae99f021b76f8eb1c8805d32d80644464afb1ff6`) binds each counted seat through the report file it
writes — line 1 `ROW GR<n> VERDICT: holds|partly|fails`, line 2 `SECTION SHA256: <hex>` — and credits it only on the
current row hash with every `file:line` citation resolving in the pinned snapshot. The frozen predicate is
`structural_ok == 1 and quotes_ok == 3 and verdicts_ok == 3 and marks_ok == 3`, run as
`python3 tools/check-scrub-admission-r48.py --revision <REV>`. A row is admitted when at least three credited seats read
`holds`, at least one of them a reviewer and one a critic, their report bodies pairwise distinct, and no bound-format
seat on the current row hash reads `partly` or `fails`.

Frozen section hashes at `ae99f021b76f8eb1c8805d32d80644464afb1ff6` (whole-row extent, `## GR<n>` up to the next header):

| Row | Section sha256 |
|---|---|
| GR1 | `fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8` |
| GR2 | `e0b391e198f67ff57ce7971e2dd589faaa9390ebf2d2fd49dc6d103c163a52ce` |
| GR3 | `43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c` |

The 18 counted seats of wave `w2`, three reviewers and three critics per row; fill each verdict and hash cell from the
first two lines of `.ufo/waves/round-48/w2/<seat>.md` before landing this block.

| Row | Seat | Role | Verdict | Section sha256 |
|---|---|---|---|---|
| GR1 | R48RevGR1a | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR1 | R48RevGR1b | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR1 | R48RevGR1c | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR1 | R48CritGR1a | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR1 | R48CritGR1b | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR1 | R48CritGR1c | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48RevGR2a | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48RevGR2b | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48RevGR2c | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48CritGR2a | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48CritGR2b | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR2 | R48CritGR2c | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48RevGR3a | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48RevGR3b | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48RevGR3c | reviewer | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48CritGR3a | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48CritGR3b | critic | <fill: holds / partly / fails> | <fill: hex> |
| GR3 | R48CritGR3c | critic | <fill: holds / partly / fails> | <fill: hex> |
