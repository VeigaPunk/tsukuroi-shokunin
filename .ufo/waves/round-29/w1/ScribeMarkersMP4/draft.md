# Draft — C1 owed-statement markers O05, O06, O07 (round 29, wave 1)

Seat: ScribeMarkersMP4. Revision under attack: `81a061a67466c5e1be812814a895a4b5ed89b4ff`.
Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
Every anchor below was re-checked verbatim in the revision blob with
`git show 81a061a...:<path>`; every cited `path:LINE` was checked to exist at that
revision (and is re-resolved by the counter's M6 path rule).

## 1. O05 — `SKILL.md`

Anchor: `SKILL.md` line 2316 at the revision (the MP4 row of the memory-pressure
registry table), substring `so nothing in that chain is monitored` (`grep -cF` = 1).

Placement: insert one marker paragraph after the MP6 table row (revision line 2318)
and its following blank line (revision line 2319), immediately before the
`Recheck after any kernel, systemd or memory-controller change:` paragraph (revision
line 2320). Do not insert between the MP4 and MP5 rows: a plain line there would
terminate the Markdown table and the MP5/MP6 rows would stop rendering as table rows.
The anchor association is carried by the `original:` quote.

Exact line to insert (one line, followed by one blank line):

```
[R29-OWED-O05] verdict: qualified | original: "so nothing in that chain is monitored" | now: No ManagedOOM candidate exists in the four-unit auto chain, but units with OOMRules= are also monitored, and an active systemd-oomd.socket can accept local-account cgroup reports. | basis: corpus/knowledge/memory-pressure-r25.md:387, corpus/knowledge/memory-pressure-r25.md:390
```

Basis resolution: both path refs exist at the revision. `corpus/knowledge/memory-pressure-r25.md:387`
is the MP4 `OOMRules=` correction bullet; `:390` is the MP4 action bullet on the
`socket` mode-0666 local-account reports. `S121` is deliberately not cited here: its
used-by cell names `memory-pressure-r25.md` and `memory-pressure-r25.json`, not
`SKILL.md`, so an `S121` reference in this marker would not pass M6. If the L1 prefers
a source id over a path, extend S121's used-by cell with `SKILL.md` first (or use the
new superseding row S136, whose used-by cell currently names only the `.md` and would
need both the JSON and `SKILL.md` added).

## 2. O06 and O07 — `corpus/knowledge/memory-pressure-r25.json`

Anchors at the revision: row `MP4`, field `action` contains
`Enabling the unit would still monitor nothing while every unit stays 'auto'` (one
occurrence); field `statement` contains
`systemd-oomd monitors only cgroups whose units carry 'kill'.` (one occurrence).
The file has no `corrections_r29` key at the revision; `corrections_r27` is the last
top-level key (object on line 497, array closed by ` ]` on line 498, file closed by
`}` on line 499).

Placement: add one new top-level key `"corrections_r29"` after `"corrections_r27"`,
i.e. change the file tail from

```
  {"row": "MP6", ... "marked_by": "...only)"}
 ]
}
```

to the same object line followed by ` ],`, the new key, and the final `}` (the
`corrections_r27` array's closing bracket gains the separating comma). Exact text to
insert after the `corrections_r27` object line:

```json
 ],
 "corrections_r29": [
  {
   "id": "R29-OWED-O06",
   "row": "MP4",
   "field": "action",
   "withdrawn_text": "Enabling the unit would still monitor nothing while every unit stays 'auto'",
   "verdict": "qualified",
   "now": "Starting systemd-oomd with the four units still auto leaves no ManagedOOM candidate, but a running daemon could accept mode-0666 socket reports for local accounts' cgroups, and OOMRules= units are monitored.",
   "basis": [
    "S121",
    "S123",
    "corpus/knowledge/memory-pressure-r25.md:387",
    "corpus/knowledge/memory-pressure-r25.md:390"
   ]
  },
  {
   "id": "R29-OWED-O07",
   "row": "MP4",
   "field": "statement",
   "withdrawn_text": "systemd-oomd monitors only cgroups whose units carry 'kill'.",
   "verdict": "corrected",
   "now": "systemd-oomd also monitors units that set OOMRules=, in addition to cgroups whose units or ancestors set ManagedOOMSwap= or ManagedOOMMemoryPressure= to kill.",
   "basis": [
    "S121",
    "S123",
    "corpus/knowledge/memory-pressure-r25.md:387"
   ]
  }
 ]
```

Then the existing final `}` closes the file. Indentation follows the file's one-space
per level style. `S121` and `S123` both have status `mined` and their used-by cells
name `corpus/knowledge/memory-pressure-r25.json`, so both pass M6 for this target.
`S136` is not cited: its used-by cell names only the `.md`, so it would not resolve
for the JSON target.

## 3. Verification of this draft (sandbox only)

Applied to a sandbox clone at `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkersMP4/repo`,
checked out at `81a061a...`, committed there as
`1390918e22f1fe77b429a3dac961fdd14192169a` (sandbox commit; the lane and fleet repos
were not written). The counter run from the sandbox:

```
python3 tools/check-owed-statements-r29.py --revision 1390918e22f1fe77b429a3dac961fdd14192169a
```

gave `"ok": true` for O05 (`basis.paths` 387 and 390), O06 (`basis.sources` S121,
S123; `basis.paths` 387 and 390; `unresolved` empty) and O07 (`basis.sources` S121,
S123; `basis.paths` 387; `unresolved` empty), summary
`{"items": 12, "marked": 3, "unmarked": ["O01","O02","O03","O04","O08","O09","O10","O11","O12"]}`,
exit 1 (the other nine items are other seats' work). No rule M1-M7 failed for O05,
O06 or O07.

## 4. Caveats

- The underlying systemd v262 claims rest on S121/S123 as argued in
  `corpus/knowledge/memory-pressure-r25.md:387-390`; those upstream bytes were not
  re-fetched this round. The host conclusion (four units all `auto`, `OOMRules=` empty)
  stands per that Markdown entry.
- The original statements stay in place (M1, append-only); the markers only append.
