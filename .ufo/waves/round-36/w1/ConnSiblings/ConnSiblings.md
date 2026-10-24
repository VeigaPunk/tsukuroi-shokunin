# ConnSiblings — sibling overlap, tsukuroi round 36

Stamp: 2026-10-24T02:51:40Z (`date -u +%H:%M:%SZ` at write). Read-only seat. No installs. No production edits.

Axes judged: adjacency (scan:sibling-overlap). Claims under test are tsukuroi C1 (operability: fixed-dict child env on five tools) and C2 (depth: journalctl v262 `-F`/`-N` rejection note). Home lane excluded from the scan.

## Method

Twenty sibling checkouts under `/home/vgpnk/Projects/shokunin/*-shokunin`. For each, `git log --format='%H %s' -n 500`. An own-round commit is a subject matching `^(?:lore\s+)?r(?:ound[- ])?N`. Last three rounds = the three highest such N. Every commit in those rounds was diffed (`git show --unified=0`) and scanned for child-env / strace / pacnew / journalctl / the five tool names. Follow-up: `git grep` at sibling `HEAD`, `git ls-files` for the five basenames, and the five fleet reports at `/home/vgpnk/Projects/shokunin/.ufo/reports/round-36/`.

The rejection sentence is absent from every sibling `HEAD`:

`git grep -F 'cannot be combined with options that limit the journal'` → no output (run 02:50Z).

`git ls-files` for `check-revision-binding`, `check-report-receipts`, `score-census-handoff-r32`, `mutants-btrfs-space-r30`, `run-receipt.py`, `probe-child-env-allowlist` → no path in any sibling.

## Last-three-round windows

| Lane | Last 3 own-rounds | Commits scanned |
|---|---|---|
| audio | 99, 100, 101 | 21 |
| chousa | 35, 36, 37 | 29 |
| game-dev-2d | 103, 104, 105 | in the 20-lane diff pass |
| game-dev-3d | 106, 107, 108 | in the 20-lane diff pass |
| kagi | 26, 27, 28 | in the 20-lane diff pass |
| kaidoku | 32, 33, 34 | 21 |
| kake | 42, 43, 44 | 18 |
| kama | 29, 30, 31 | in the 20-lane diff pass |
| kasegi | 20, 21, 22 | in the 20-lane diff pass |
| kengaku | 27, 28, 29 | in the 20-lane diff pass |
| kotoba | 61, 62, 63 | in the 20-lane diff pass |
| kotodama | 62, 63, 64 | in the 20-lane diff pass |
| kumitate | 49, 50, 51 | 31 |
| lore | 101, 102, 103 | in the 20-lane diff pass |
| mado | 26, 27, 28 | 39 |
| mori | 36, 37, 38 | 40 |
| revenger | 61, 62, 63 | in the 20-lane diff pass |
| souji | 20, 21, 22 | 33 |
| tabi | 20, 21, 22 | 12 |
| tameshi | 33, 34, 35 | 33 |

`git log --oneline -5` tips at scan time include chousa `b905217` (round-37 freeze), souji `4edb25d`, tabi `e3cf4e0`, tameshi `34fa5b0`, kaidoku `f432c8e3`, mado `317ff19`, mori `b699374` (a later `13f3db7` appeared during the scan; the journalctl conclusion is on `b699374` plus pickaxe), kumitate `a476977` (later `cd7f69d`), kake `942fe18`, kotoba `cbbee56`, kotodama `097c21d`.

## Overlap table (hits only)

| Lane | Round | File | One line |
|---|---|---|---|
| chousa | 37 | `corpus/evidence/round37/c2-count.py:9` and `tools/research-gate.sh:8247` | C2 claim `PIN_CAPTURE_ENV_MATCH=7/7`: pin capture scrubbed `CHOUSA_*` but not `BASH_ENV`, so the child re-sourced a startup file. Still `env = dict(os.environ)` (`c2-count.py:77`). Commit subject: `round-37 freeze: claim-pin provenance (C1) and pin-capture environment (C2)`. |
| chousa | 35–36 | `corpus/evidence/round35/c1-count.py`, `round36/c1-count.py`, `tools/argv-witness.py`, `tools/mechanism-witness.py` | Child env is ambient copy minus a prefix (`not k.startswith("CHOUSA_")` / `RESEARCH_GATE_`), the same shape as tsukuroi C1's before state. Not the five tools. |
| chousa | 35 | `.ufo/waves/round-35/w2/ExecPinModeIntegrity.md` | `strace -f -e trace=execve` counted grep invocations for the pin. Not an env-allowlist probe. |
| chousa | 36 | `.ufo/waves/round-36/w1/ConnOverlap.md` | Already records "tsukuroi env allowlist" as overlap, not absorption. |
| souji | 21 | `census/round-21/run-acceptance.py:107-116` at `7753ed488e` | Landed `CHILD_ENV` fixed dict: `PATH=/usr/bin:/bin`, `LC_ALL=C`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_OPTIONAL_LOCKS=0`. Same keys as tsukuroi C1's after display, different program. |
| souji | 21 | `tests/fixtures/r21-source-head.py:26` | Same fixed dict for synthetic git. |
| souji | 20 | `census/round-14/run-targeted.py` | `_BOOT_ENV` drops `GIT_*` then sets `GIT_CONFIG_NOSYSTEM` / `GIT_CONFIG_GLOBAL`. |
| souji | 20–22 | `tools/souji-seat-audit.py`, acceptance transcripts | strace is a denied-command token (`probe-strace-fleet`), not a child-env probe. |
| tabi | 20–22 | `.ufo/waves/round-2{0,1,2}/measure-c1.mjs`, `run-checks.py`, `selftest-c1.mjs` | Wave counters pass a minimal git env (`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`). Not a landed tool claim. |
| tameshi | 33–35 | `tools/tally-audit-v3.py:332` at `d16f9b5a18` (v2 at r33) | Fixed four-key child env, but `PATH` is ambient (`os.environ.get('PATH', '/usr/bin:/bin')`). Partial allowlist, not C1's fixed `PATH`. |
| tameshi | 35 | `.ufo/waves/round-35/w2/ConnectorConfigGuards.md`, `ConnectorFirstLine.md` | Cites tsukuroi `tools/score-census-handoff-r32.py:786-800` and `tools/run-receipt.py:106-114`. Citation only. Also names `_JOURNALCTL` among tsukuroi constants. |
| tameshi | 33–35 | census stdout | `S075` duplicate URL for `strace.1` — a sources-census warning, not a probe. |
| kaidoku | 32 | `tools/round-32/c1-arm64x-positive.py:90` at `9a73680af` | `clean_env()` copies ambient env and drops only `GIT_DIR` / `GIT_WORK_TREE` / `GIT_INDEX_FILE`. Same function name as tsukuroi's leaking builders; opposite of a fixed dict. |
| kaidoku | 33 | `tools/round-33/measure_driver.py` | Returns `{k: v for k, v in os.environ.items() if not k.startswith("GIT_")}` and also builds a small `PATH`/`LC_ALL` dict. |
| kaidoku | 34 | `.ufo/waves/round-34/w1/CtlHashReplay-files/*.py` | Control copies use `env = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "LC_ALL": "C", "PATH": "/usr/bin:/bin"}`. Wave controls, not the ELF claim. |
| mado | 27 | `.ufo/waves/round-27/c2/count.py:55` at `b6650d5839` | Counter child env `PATH=/usr/bin`, `HOME=SCRATCH`, `GIT_CONFIG_NOSYSTEM=1`, `GIT_OPTIONAL_LOCKS=0`. |
| mado | 28 | `quality/q36-successor-run.sh` | `export HOME=… GIT_CONFIG_NOSYSTEM=1 GIT_OPTIONAL_LOCKS=0` for the q36 witness. |
| kake | 42–44 | `.ufo/waves/round-4{2,3,4}/c4*_count*.py` | Sandbox `env={"PATH": "/usr/bin"}` only. |
| kake | 43 | `.ufo/waves/round-43/w1/ConnectorOverlap.md` | Cites tsukuroi `score-census-handoff-v5.py` for urandom/prefix method kinship. Not the live five and not env hygiene. |
| kumitate | 51 | `.ufo/waves/round-51/w1/ConnSiblingOverlap.md:82` | Cites tsukuroi r35 pacnew/pacsave arm and calls `run-receipt.py` "their score harness". Citation only. |
| kumitate | 50 | `.ufo/waves/round-50/r50/MutSelftest.md` | Host fact `systemd 262` in a selftest note. Not a journalctl `-F` claim. |
| mori | 36–38 | wave reports (`ScoutSurfaces.md`, `RevQuality105.md`, `RevC4Live.md`) | Re-cite existing `S160` `https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journalctl.c` ("option grammar"). |
| mori | standing, not a last-3 diff | `corpus/SOURCES.md` S014, S122, S160; `tools/mori-census.sh:1232`; `tools/mori-journal-window.py:433-442` | See C2 verdict. Pickaxe `git log -S journalctl -- tools corpus/SOURCES.md corpus/knowledge` last hit is `ee61010` round-30, outside 36–38. |
| game-dev-3d | 106 | `AGENTS.md` | Ops hint `journalctl --user -u` to restart a shim. Not v262 `-F`/`-N`. |
| kengaku | 28 | `.ufo/waves/round-28/scratch/.../bench-arena-fresh-run.md` | Scratch copy mentions `journalctl -u qwen-coder.service`. Not a claim. |
| audio | 99–100 | `corpus/live/r99-boundary/probes/r99b_common.py`, `r100sofa.py` | `ENV = dict(os.environ, …)` ambient copy for PipeWire probes. Opposite of a fixed dict; not a hygiene claim. |
| revenger | 61–62 | `.ufo/waves/round-6{1,2}/falsify/R62FReproduce*.md` | `strace` of open/socket on fixture replays (zero network). Not env allowlists. |

No last-3 diff adds `.pacnew` / `.pacsave` / `NoUpgrade` except the kumitate citation of tsukuroi. A tameshi `noextract.sh` mutant name matched the regex and is not a pacman counter.

Lanes with no row above and no four-surface hit in the diff pass: kagi, kama, kasegi, kotoba, kotodama, lore, game-dev-2d (its "allowlist" hits are receipt-line allowlists and `os.environ` in mutants, not child-env policy).

## Fleet round-36 reports vs C1/C2

Reports are claim declarations, not the last-3-round window. Several are stale relative to lane tip.

| Report | Declared surface | Collision with tsukuroi C1 | Collision with tsukuroi C2 |
|---|---|---|---|
| `chousa.md` (attempt 2, tip `f19589d`) | C1 operability: 14 engine-swap canaries on the research gate. C2 calibration: per-record argv witness. | No shared files or predicate. Shared axis word "operability" only. The later r37 pin-capture claim is not in this report; it is in commit `b905217` after the report. | None. |
| `kake.md` (tip `1a16b8e3`, lane now r44) | C1 freshness: `scripts/source_recheck.py`, `met: passed >= 25 of 28`. | None. Current r42–44 claims are a witness-class gate and a ledger checker, still not child-env. | None. |
| `kotodama.md` (2026-10-19; lane now r64) | Depth claim D failed (register-form); coverage timekeeping entry; calibration recount ledger. | None. r62–64 diffs had no four-surface hit. | None. |
| `kumitate.md` (2026-10-21, round 36) | C1 operability includes PIN v1 "scrubbed git env" on `claims-check` / `proxy-check` / `surface-probe`. C2 is Rust section coverage. | Technique kinship only. `GIT_ENV_KEEP` was introduced in `3d5760a` round 36, which is outside kumitate's last three rounds (49–51). At r51 the allowlist still keeps ambient `PATH`/`HOME` (`scripts/claims-check.mjs:161-167`). Different tree, no `leaking_pairs`. | None. |
| `mori.md` (attempt 2) | C2 operability: `mori-sources-appendonly.py`. C1 freshness: `mori-source-drift.py` (lands unprovable). | None. | No shared claim text. Neighborhood only (below). |

## Collision verdicts

**C1 — no file collision, real technique neighborhood, do not treat siblings as prior satisfaction.**

Nobody else edits the five tools or `probe-child-env-allowlist-r36.py`. Nothing in the last three rounds of any sibling is a `leaking_pairs` counter.

The same problem is live elsewhere, with different predicates:

- chousa r37 is an active child-environment claim (`PIN_CAPTURE_ENV_MATCH=7/7`) that still builds the child from `dict(os.environ)` and then unsets names. That is the pattern C1 says is not enough. It does not meet C1's kill rule, and C1's kill rule must not be read as covering chousa's gate.
- souji r21 already landed the fixed dict C1 wants (`PATH`, `LC_ALL`, `GIT_CONFIG_NOSYSTEM`, `GIT_CONFIG_GLOBAL`, `GIT_OPTIONAL_LOCKS`) on `census/round-21/run-acceptance.py`. That does not implement C1. It is prior art for the dict shape only.
- kaidoku r32 `clean_env()` and chousa r35–36 counters are prefix/drop filters — the C1 before-state — under the same function name `clean_env`.
- tameshi's tally auditor and kumitate's r36 `GIT_ENV_KEEP` are allowlists that still pass ambient `PATH`. They are not C1's fixed `PATH=/usr/bin:/bin`.
- kumitate r51 and kake r43 and tameshi r35 only cite tsukuroi tools. They do not own them.

Pacman `.pacnew`/`.pacsave`: no sibling claim and no counter in the last three rounds. Matches the declaration that pacnext v3 is not owed this round. The only hit is kumitate describing tsukuroi's own r35 arm.

Strace: chousa (execve pin), revenger (open/network), souji (denied command), kengaku (selftest opens). None is an env-allowlist probe of the five tools. No sibling is drafting `probe-child-env-allowlist-r36.py`.

**C2 — no claim collision; one source-neighborhood constraint.**

The exact rejection line is not in any sibling tree. No last-3 round opens a journalctl v262 `-F`/`-N` note.

Mori already owns systemd 262 journalctl as sources and as tools, last edited at mori round 30 (`ee61010`, S156–S160), not in rounds 36–38:

- `corpus/SOURCES.md` S014 is already titled `journalctl(1)` and says "systemd 262 man page opened 2026-10-19", including Filtering Options and `--output-fields`.
- S160 is "systemd v262 journalctl option grammar and filter application" at `src/journal/journalctl.c`.
- `tools/mori-census.sh:1232` runs `journalctl "$flag" -b --no-pager -o json --output-fields="$fields"`.
- `tools/mori-journal-window.py:433-442` runs `journalctl --user|--system --no-pager --quiet --no-tail --output=json --output-fields=… --cursor=…`.

Neither argv uses `-F`/`-N`. C2's rejection does not indict those commands. A new tsukuroi row titled like S014 ("journalctl(1) at systemd 262") would duplicate mori's source id space. The behavior sentence itself is still unclaimed.

game-dev-3d's `journalctl --user -u` hint and kengaku's scratch mention are not this claim.

## Proposed move (one)

Record, in the L1 adjacency note and not in either claim's predicate, two non-absorption sentences:

1. C1 stays the five tools' `leaking_pairs`. chousa r37 `PIN_CAPTURE_ENV_MATCH`, souji `CHILD_ENV`, kaidoku `clean_env`, tameshi `tally-audit-v3` env, and kumitate `GIT_ENV_KEEP` are different programs. None is a before-state, an after-state, or a kill-rule witness for C1.
2. C2's new source row must not be titled or numbered as a second `journalctl(1)` at systemd 262 (mori S014/S160 already hold that). Point the row at the rejection sentence, which is absent fleet-wide, and do not edit `mori-census.sh` or `mori-journal-window.py`. Their `--output-fields` invocations are not `-F`/`-N`.

Adjacency improves (contested scope stays reported). Operability and depth predicates are unchanged, so neither axis is harmed.

## Risks

- If C2's "safe substitution" prose is written as generic journalctl advice, a later reader can apply it to mori's `--output-fields` queries. Those queries are a different flag. The note should name tsukuroi consumers only (declaration already says "the lane's journal consumers").
- chousa r37 is in flight (`b905217` is a freeze). Their C2 is also "environment". A fleet scoreboard that keys only on the word environment will double-count. The predicates (`leaking_pairs` vs `PIN_CAPTURE_ENV_MATCH=7/7`) do not overlap.
- souji's dict is similar enough that a reviewer may call C1 non-novel. Novelty here is the five named tools plus the untraced-view probe, not the invention of `GIT_CONFIG_NOSYSTEM=1`.

## Verification not run by this seat

- Re-grep sibling `HEAD` for the rejection sentence after mori/chousa land further commits (mori tip moved past `b699374` during this scan: `13f3db7`).
- L1, not this seat, should re-read mori S014's quote span before minting S198, to confirm the `-F`/`-N` sentence is not already inside that opened man page excerpt. This seat did not open S014's excerpt body.
