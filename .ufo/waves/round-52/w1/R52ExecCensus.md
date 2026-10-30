VERDICT: defect-found

# Round-52 frozen corpus census

The requested `corpus/CORPUS.md` is absent at freeze `ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0` (`git show <freeze>:corpus/CORPUS.md` returned `fatal: path 'corpus/CORPUS.md' does not exist`). Consequently the seven commands specified in its §Census could not be identified or claimed as run. I ran all five modes documented by the live census script header (`scripts/sources-census.sh:10-38`): census, validate, overdue, shared, selftest. The frozen registry was extracted from the pinned commit into the seat scratch and validated against the complete frozen lane tree, so used-by checks used actual frozen target files.

## Frozen corpus results

Evidence: command `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin archive ff9470ea9ff06966a37dd91c1cbe823ffe46ecf0 | tar -x -C /fast/scratch/hyaku/tsukuroi-r52/R52ExecCensus/frozen` followed by `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --file /fast/scratch/hyaku/tsukuroi-r52/R52ExecCensus/frozen/corpus/SOURCES.md`.

Observed census: `rows=257`, tiers `A=241 B=5 C=11 invalid=0`, statuses `mined=229 queued=6 rejected=22 invalid=0`, `missing=0`.

Validation command: `.../sources-census.sh validate --file <frozen>/corpus/SOURCES.md --today 2026-10-30`. Exit 0, final output `file ok <frozen>/corpus/SOURCES.md`; 40 W04 cross-scope duplicate-URL warnings, no E-code errors, no E03 duplicate IDs, no invalid kind/tier/status/date/recheck enums, and no E11 missing used-by paths. S257 is included and has `used-by —` as expected (frozen SOURCES row S257; full source text was read from pinned file).

Overdue command `.../sources-census.sh overdue --file <frozen>/corpus/SOURCES.md --today 2026-10-30 | wc -l` yielded `257`: rows report cadence, symbolic cadence (including on-release) is not judged overdue; no actual overdue date entries were emitted in observed output.

Shared command `.../sources-census.sh shared --file <frozen>/corpus/SOURCES.md | wc -l` yielded `0`. This single-registry invocation cannot report cross-lane URL sharing; it is not a full fleet-wide shared census.

Selftest command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh selftest` yielded `selftest ok`; all 97 displayed `killed` checks passed, including parser, validation, date, missing, indentation, and error handling cases.

## Live validation

Command `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` exited 0, ended with `tsukuroi ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`, and emitted the same 40 W04 advisories. This is live-tree evidence, not the frozen revision measurement.

## Limitation / remaining evidence

Seven-command compliance is unresolved because the named `corpus/CORPUS.md` is absent at the frozen commit. The five documented modes were exercised as above, but this does not establish which seven commands the assignment intended. No tool installation occurred. Scratch was removed after collecting results.
