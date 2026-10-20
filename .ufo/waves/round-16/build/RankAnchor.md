# RankAnchor — v3 risk-table anchor

`corpus/knowledge/update-safety-v3.md` @ baseline `db68e62` (415 lines; worktree `cmp`-identical).

Observed, byte-verified, unique:
- Heading `:208`: `## 5. Risk-ordered operations table (recommendation only — nothing here was run)`
- Rank row `:216`, row_key `| 1 | Do nothing now |`: `| 1 | Do nothing now | official | — | \`-Syu\` would be INERT: 0 candidates by three probes; …`
- Row substring (quote candidate), unique: `` `-Syu` would be INERT: 0 candidates by three probes ``
- Defect locus `:398` (span `:398–:400`): notice says `§7 rank 1 row`; v3 §7 is `## 7. Observation / inference / unknown` (`:269`, no table). Correct target is §5 row 1 at `:216`.

Separation (unchanged): `:210` `v2 §7's table` and `:366` `v2's §7 ranks` reference v2's §7 (`update-safety-v2.md:244`); v2 row 1 (`:253`) says `0 actions`, unlike v3's `0 candidates by three probes`.

Concern: the notice quote wraps `0\ncandidates`, so the JSON quote must use the unwrapped row substring. Errata JSON and gate are absent; no output seen.

Confidence: high (static bytes). Unknown: final old_locator wording.
