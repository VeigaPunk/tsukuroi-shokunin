VERDICT: draft

# R51ScribeReadme — corpus/README.md draft for the scrub rows (item N-7, prose only, not a counted seat)

Basis: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 2732ee6c06108c031c4d8043239b994e0504eb2f:corpus/README.md` (522 lines), and `:tools/check-scrub-admission-r51.py` at the same revision (412 lines). Snapshots kept in my scratch only; the working tree was not read as evidence. Nothing in the lane was written.

## Evidence the draft is bound to

- Marks leg: `tools/check-scrub-admission-r51.py:66` `MARK_README = ('btrfs-scrub-grounding-r45.md', 'admitted round 51')`; `:67` `NEGATE_RE = re.compile(r'unadmitted|not admitted|never admitted|stay pending|stays pending')`.
- `:305-315` `marks_leg`: the README is whitespace-normalised, split with `re.split(r'(?<=[.!?])\s+', …)`, and a README mark is credited only when one sentence contains both the file name and the phrase and no `NEGATE_RE` match. A period followed by whitespace ends a sentence, so no abbreviation may sit before a space inside the admission sentence.
- `:32`, `:382` `marks_ok == 3` is one of the five predicate legs; the README leg is only one-third of it. The counter reads the README at the revision under test (`run()` `read_text(lane, rev, README, …)`), so the sentence must be in the admission commit's bytes.
- Coverage row the rows are depth on: `corpus/README.md:460` (`knowledge/btrfs-scrub-grounding-r45.md`, in the Round-45 coverage note, lines 454-466), which grounds the round-44 `[inference]` marks of the scrub-record row at `corpus/README.md:434` (`knowledge/btrfs-scrub-record-r44.md`, SR7-SR9). No new coverage-map row is created; the existing row is depth-worked.
- Frontier text: `## Frontier` (`corpus/README.md:28-43`) has no scrub or NVMe bullet. The scrub and NVMe statements sit in round notices: `:243`, `:296`, `:335`, `:384`, `:443`, `:497`, `:520`. Storage record and NVMe rows: no change expected; none of them is edited by the draft.
- Append-only convention: the README header states each round is appended and earlier text stays as written (`:454-455`, `:468-469`, `:482` onward). The old pending text at `:462-464` (`GR1-GR3 are pending, not admitted`) is historical and must not be edited; the new text goes in an appended section.

## (a) Admission sentence (use only if the round-51 counter binds all three rows)

Exact text, one sentence, no negation word in it (checked against `NEGATE_RE` and against the plain words not / no / never / without):

> Round 51 is depth work on the scrub-grounding row `knowledge/btrfs-scrub-grounding-r45.md` (`corpus/README.md:460`, grounding the round-44 scrub-record marks at `corpus/README.md:434`), and its three rows GR1-GR3 are admitted round 51 by the counted round-51 depth gate (`tools/check-scrub-admission-r51.py`).

Note the first sentence split: it contains `README.md:460` and `README.md:434`; a period is followed by a non-space there, so `re.split` does not cut them.

Simulated check (my own re-implementation of `marks_leg` lines 305-315 with the same regex and split, not the counter itself): the admission sentence returns True.

Suggested placement: a new appended section after the last line of the file (`:522`), titled e.g. `## Round 51 — scrub grounding rows (depth work, not coverage)`, with the standard "Append-only; … stay as written" line, then the admission sentence as its own paragraph. The Frontier line below may follow it.

Optional companion sentence for the same section (no file name, no phrase, so it cannot affect `marks_leg`):

> The scrub record's content, the running state and NVMe SMART/Health stay Frontier (`corpus/README.md:497`, `:520`).

## (b) Pending-outcome sentence (use if the counter does not bind all three rows)

> Round 51 leaves GR1-GR3 of `knowledge/btrfs-scrub-grounding-r45.md` pending: the counted round-51 depth gate did not bind all three rows, and no admission mark is written.

This sentence does not contain `admitted round 51` (the substring `not admitted round 51` must never be written, since it contains the phrase). Simulated check: returns no README mark, as required. Same placement as (a): one appended section, the pending sentence in place of the admission sentence; the companion Frontier sentence may stay unchanged.

## (c) Frontier-row changes

No change to the `## Frontier` section (`:28-43`). No change to the storage record or NVMe SMART rows: the scrub record and NVMe SMART remain Frontier by the round-44 to round-50 notices and need no new text. Do not rewrite `:460-464`, `:488-497` or `:518-522`; they are append-only. If the admission is written, the only new Frontier statement is the companion sentence in (a), which restates the existing Frontier status and adds no coverage.

## Limits and what I did not do

- I did not run `tools/check-scrub-admission-r51.py`, any census, or any selftest; the item is prose only and the counter is run by the L1 at the admission commit. The simulated split is my re-implementation, not the counter.
- I did not verify that the GR1-GR3 rows will bind; this is a draft for either outcome, as asked.
- No tool was installed; no lane file was edited; no git mutation was run.
