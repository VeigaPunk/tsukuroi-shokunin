# Round-73 sources: search log, new rows, rejections (L1 working copy)

## Search log (PRISMA-inspired; rule 5)

- **Question.** Which systemd rules decide what bytes become a unit — the load path, drop-in merge and
  precedence, masking, the reload condition, and alias installation — and which of them can this lane
  read without privilege?
- **Where searched.** `https://raw.githubusercontent.com/systemd/systemd/v262/` (tag v262, the release the
  host's 262.1-1-arch build descends from), `https://man.archlinux.org/man/systemd.unit.5`,
  `https://archlinux.org/packages/core/x86_64/systemd/`; the lane's own registry checked for collisions
  first (`grep -oE 'S[0-9]{3,}' corpus/SOURCES.md`).
- **Date.** 2026-11-03.
- **Identified 5 · screened 5 · included 3 · excluded 2.**
  - Identified: `man/systemd.unit.xml`, `src/core/unit.c`, `src/shared/install.c` (upstream at v262);
    `man/systemd.unit.5` (Arch's rendered man page); `archlinux.org/packages/core/x86_64/systemd/`.
  - Excluded: the rendered man page (same upstream bytes as the pinned snapshot, no independent
    evidence, no Arch patch visible in it — a duplicate of S304's source, not a second source) and the
    Arch package page (build provenance only: it names `systemd 262.1-1`, which the host reading already
    measures, and states no merge, precedence or mask rule).
  - Stop rationale. Three upstream artifacts already ground all six planned rows at the tag the host's
    build descends from; one more source would add vocabulary, not resolve an open question. The two
    exclusions exercise the gate's taste rather than adding rows.
- **Rejection rows** (a rejection is evidence of taste and stays in the registry): recorded as
  `REJECTED: … ; flip: …` under the next free ids (S307, S308) with `status` `rejected`, `opened`
  2026-11-03, `used-by` `—`.

## Gate quotes (new rows; URL, access date 2026-11-03, ≤25-word located quote)

| id | snapshot | quote | location |
|---|---|---|---|
| S304 | `man/systemd.unit.xml` @ v262 | "Unit files found in directories listed earlier override files with the same name in directories lower in the list" | `man/systemd.unit.xml:367-370` |
| S304 | `man/systemd.unit.xml` @ v262 | "Multiple drop-in files with different names are applied in lexicographic order, regardless of which of the directories they reside in" | `man/systemd.unit.xml:238-240` |
| S305 | `src/core/unit.c` @ v262 | "For masked files check if they are still so" | `src/core/unit.c:3874-3875` |
| S305 | `src/core/unit.c` @ v262 | "any drop-ins that are masked are simply omitted from the list" | `src/core/unit.c:3908` |
| S306 | `src/shared/install.c` @ v262 | "Unit %s is masked, ignoring." | `src/shared/install.c:345` |
| S306 | `src/shared/install.c` @ v262 | "Unit %s is an alias to a non-existent unit, ignoring." | `src/shared/install.c:351` |

## The two refusals, opened this round

| candidate | fetch | verdict |
|---|---|---|
| `https://man.archlinux.org/man/systemd.unit.5` | HTTP 200, 135978 bytes, title `systemd.unit(5) — Arch manual pages` | **rejected** — `REJECTED: the rendered Arch man page is the same upstream manual source as S304 and shows no divergence, so it is not a second source; flip: a rendered page that carries an Arch patch changing the merge, precedence or mask text` |
| `https://archlinux.org/packages/core/x86_64/systemd/` | HTTP 200, 101009 bytes, body names `systemd 262.1-1` | **rejected** — `REJECTED: the package page is build provenance only (version and packager), states no merge, precedence or mask rule, and the host's installed version is already an own-work host reading; flip: a package note or patch list that names a change to the unit-loading code or man page` |
