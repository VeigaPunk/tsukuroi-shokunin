2026-11-03T23:27:30Z
# N1Sentinel — boundary and side-effect sweep (round 69, wave w1)

Axis: operability. Milestone: boundary and side-effect sweep. Verdict: **clean** — no seat crossed the lane's read-only boundary; five observations are listed for the L1 (none is a forbidden invocation). Full receipt with commands, outputs and rc: `.ufo/waves/round-69/probes/N1Sentinel/boundary.md`.

Scope: lane HEAD 920a9ee; wave dispatched 23:18:43Z; sweep window 23:18:50Z–23:27Z, two snapshots (63 files at A=23:25:10Z, 65 at B=23:26:30Z; three drafts and one probe were rewritten between them). Read-only throughout; the only git writes I made were inside `/fast/scratch/hyaku/tsukuroi-r69/N1Sentinel/clone`.

## Sweep result

- Forbidden-action token sweep over `before/` (committed), `drafts/`, `probes/`, and the two wave-control files: snapshot A (23:25:10Z) 16 hit lines, snapshot B (23:26:30Z) 12, closing cutoff B+ (23:27Z) 13. The deltas are four lines in a receipt the seat rewrote at 23:24:59Z and one late quoted note snapshot at `probes/R1Reviewer/attack.md:810`. Classified: 9 declaration/fixture text, 8 permitted read-only commands, **0 invocations**.
- Sandbox-only git mutations: 28 `add`/`commit` lines, every one with `-C` on `/fast/scratch/hyaku/tsukuroi-r69/E2Counter/clone` and fixture identity supplied only inside that clone. Lane-targeted git calls are 27 read verbs (`show` 19, `rev-parse` 3, `cat-file` 3, `ls-tree` 2); 0 mutating git/jj calls outside a sandbox clone; no `jj` anywhere.
- Committed receipts: 0 forbidden tokens.
- Credential-shaped names: `op://` only in guard prose; a corpus note filename containing "credentials"; `/var/lib/pacman/local/<pkg>/desc` (package metadata, verified `NOT_WRITABLE` for uid 1000). No `.env`, `.ssh`, key, token or cookie path and no value anywhere.

## Observations for the L1 (no seat breach found)

1. **Tracked receipt changed mid-round.** `before/s243-v73-recheck.txt` gained one appended line at 23:19:10Z, self-declared: `## correction (appended 2026-11-03 by the L1, no in-place edit): …`. Additive and claim-narrowing, but it is the only tracked-file mutation in the round; if `before/` is meant to be frozen at declaration, cite it explicitly.
2. **Unattributed census receipt.** `before/census-live-baseline.txt` (19 lines, 23:19:24Z) records a full `bash tools/tsukuroi-census.sh` run, `rc=1`. No seat item names that path; S2Scout is the only seat forbidden the lane census and does not claim it. Co-located with the L1's append 14 s earlier and with `probes/l1/taint-table.txt` → most consistent with the L1, unproven from artefacts.
3. **Receipt rewritten after first publication.** `probes/SC1Scribe/quote-check.txt` changed at 23:24:59Z; four `/var/lib/pacman` lines present at snapshot A are gone. The same reads survive at `probes/SC1Scribe/pacman-localdesc.txt:2,11,16`. Cite final bytes plus digest, not earlier line numbers.
4. **C2 census arm absent → its privilege test is UNRUN.** `drafts/c2/tsukuroi-census.sh` and `census-kernel-arm.diff` do not exist (`ls` rc=2, exact error in the receipt). Not a privilege block: every data source the arm needs was exercised unprivileged by me — `uname -r` rc0, `/proc/sys/kernel/tainted` 12288 rc0, both `/usr/lib/modules` trees readable, `pacman -Q`/`-Qo` rc0, `modinfo -F vermagic` rc0, `journalctl -b -k` rc0. The gated paths an arm must avoid are `dmesg` (`dmesg_restrict=1`) and `/sys/kernel/debug` (0700 root); the base census already documents the journalctl fallback (lines 165, 1105).
5. **Nit.** `probes/C1Connector/overlap.md:28` runs `git merge-base --is-ancestor` without `-C`; read-only, so no risk, but the cwd is unrecorded.

## Instrument privilege (uid 1000, `sudo` never used)

| instrument | state | run | rc | needs root? |
|---|---|---|---|---|
| C1 counter `drafts/c2/count-kr-rows-r69.py` | draft present; lane path absent (matches base control) | `--revision HEAD` on a clone copy, note absent → `KR_ROWS=0 KR_VERIFIED=0`; then fixture commit `f07859fa` (S288/S289 + 5 rows) → `KR_ROWS=5 KR_VERIFIED=5`, `KR_ROW KR1..KR5 ok` | 1 / 0 | NO |
| C2 census arm | ABSENT | not runnable | — | UNRUN |

The counter is read-only by construction: `git -C <lane> rev-parse/show/cat-file`, `read_bytes`, `sha256`; no temp file, no network, no write.

## Limits of this evidence

Artefacts are self-reported text: they cannot prove that a recorded command is the command actually executed, that no command ran whose output was never written, that the census-baseline run or the pre-rewrite quote-check bytes were what their authors say, or that the absent census arm needs no privilege.

`N1_FORBIDDEN_HITS=45 N1_FIXTURE_TEXT=9 N1_MISROOT=0 N1_PRIV_BLOCKED=0 N1_VERDICT=clean`

(45 = union of distinct forbidden-action-shaped lines across the window: 17 token hits + 28 sandbox-permitted git mutations; 9 = those shown to be declaration/fixture text rather than invocations; 0 invocations.)
