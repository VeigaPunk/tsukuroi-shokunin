# RevProbeLineage — probe lineage audit (read-only), round 36 w1

Seat: tsukuroi-r36.RevProbeLineage · 2026-10-24 02:54:42Z (pasted from `date -u`)
Full audit with the per-rule kept/dropped table: `lineage.md` (same directory).
Machine evidence: `verify-rules.txt`, `diff-r32-r33.patch` (788 ln), `diff-r33-r34.patch` (314 ln).

## Assignment vs result

1. **r32 → r33 → r34 lineage across predicate/channels/rules** — done. Snapshots: working tree ==
   HEAD == base 6d76fb20 for all three files (`git status` empty). r34 sha256
   `5d0d5689…` and VERSION 6 match round-34 amendment-2 (SCORECARD:1459, commit 3457f28); r33
   sha256 `c24f344b…` matches the round-33/34 "probe bytes at `9c89ff4f`" references.
   **Verdict: no silent drop.** 19/19 shared functions AST-identical r33→r34 (11/11 r32→r33);
   28/28 shared constants equal r33→r34; all 6 r33 predicate clauses verbatim in r34; r34
   PREDICATE changes purely additive; r32 name clause reworded (not weakened) at r33; r32's
   11-target set survives as r33/r34 `regression`; r33's 5-target claim set survives verbatim as
   r34 `r33claim`. Ticket-named rules: execveat clause and unparseable-record clause are r34
   *additions* (round-34 amendment 2) and present; marker-script checks, value channel and the
   per-run fresh-copytree fixture mechanics are byte-kept; fork-without-exec was never a
   predicate rule in any version and its exclusion is explicitly documented (finding F1);
   "fixture byte-invariance" names no rule in any of the three versions (F3).
2. **r36 draft check (`.ufo/waves/round-36/w1/ExecProbeR36/`)** — **draft absent; dependency
   recorded (F2).** The w1 directory has no `ExecProbeR36/` seat dir; `swarm-registry.json` shows
   `ExecProbeR36` with `"agentId": null`. The four-additions audit (VERSION 5 paragraph,
   `livefive` set, untraced view, normalisation) and the one-sentence-PREDICATE comparison could
   not run. `lineage.md` precomputes the checklist the draft must pass.

## Findings (detail in lineage.md)

- **F1** fork-without-exec: never a probe clause; static `SPAWN_ANY` (`fork`/`forkpty`/`fork_exec`)
  byte-kept r33→r34; runtime exclusion documented at base SCORECARD.md:1465, :1484, :1542 — loud,
  not silent. Marker-script fork+source evidence intact.
- **F2** r36 draft absent (`agentId: null` in swarm-registry.json) — dependency finding; sibling
  seats declared the same fallback, wave-consistent.
- **F3** "fixture byte-invariance": no such rule in r32/r33/r34 code or base SCORECARD; the
  structural guarantee (single `git archive` export + fresh `copytree(symlinks=True)` per run) is
  kept — naming gap in the ticket, no probe regression.
- **F4** Declaration defect: base SCORECARD.md:1620-1621 calls the frozen predicate "the same
  sentence in this declaration", but the round-36 section (1589→end) contains no predicate
  sentence (last "leaking when" match: line 1461, round 34). [inf] The intended sentence is the
  round-34 predicate extended only by the declared r36 additions.
- **F5** VERSION inconsistency for the draft: declaration says r34 probe is "VERSION 4" and the
  r36 counter "VERSION 5" (SCORECARD:1637-1640); the named r34 file is VERSION 6 (amendments 1+2,
  commits 15c9ac0, 3457f28). A literal `VERSION = 5` would move the counter backwards from its
  starting bytes — resolve before the freeze commit names the probe bytes.

## Tooling record

No tools installed or upgraded (none needed; PACMAN GUARD respected). No pacman, no VCS writes,
no production-file edits. All writes confined to this seat directory.
