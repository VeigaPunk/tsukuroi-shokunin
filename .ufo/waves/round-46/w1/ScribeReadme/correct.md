
### Round-46 index row — the fields, the counter and the round-44 receipt (appended 2026-10-27)

Append-only; the row at `:474` and the round-44 status paragraph at `:476-480` stay as written, and no
Frontier/Core line moves. Read them with this:

- **The fields and the CLI contract.** The row names "sha256, md5, bytes and newline count"; the line's fields, in
  order, are `version=… sha256=… md5=… bytes=… lines=… planes=… exit_map=… verified=yes|no`, printed once before
  any plane probe with exit 0. `--identity` with any other argument (`--selftest`, `--help`) prints
  `--identity takes no other argument` and exits 2 (`../tools/tsukuroi-census.sh:3518-3522`). `lines` counts
  newline bytes, and `version` stays the literal `census-v2`, so the sha256 alone names the revision.
- **Sources in the round-45 row's shape.** That row's Sources cell names its counter
  (`tools/check-scrub-grounding-r45.py`) and its frozen snapshot (sha256 `f5958a83…`); this round's are
  `tools/score-census-identity-r46.py --revision <REV> --scratch <DIR>` and
  `.ufo/waves/round-46/frozen/src/SHA256SUMS` (sha256 `02fa1d2d…`), with `FETCH.txt` for the fetch log.
- **`:476` reads "the row above".** The round-44 row is at `:434`, above the round-45 note; the row directly
  above that sentence is this round's census-identity row.
- **The FAILED mark's chain.** The round-44 legs are rows 3, quotes_ok 3, props_ok 3, host_ok 3, sources_ok 1,
  verdicts_ok 0, novelty_base_hits 0, pointer_ok 1, verdict FAIL
  (`.ufo/waves/round-44/after/c2-final-fbfef071.jsonl`,
  `corpus/lessons/round-44-verifier-spotcheck.md:84`), against a predicate that requires `verdicts_ok == 3`
  (`../tools/check-scrub-record-r44.py:50-51`); the SR8/SR9 narrowings made after the counted reads were judged by
  no counted seat (that lesson §2 C2).
