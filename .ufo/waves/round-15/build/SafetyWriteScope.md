# SafetyWriteScope — tsukuroi r15 build (sentinel, report-only)
Audit ≈2026-10-20T07:48Z; lane HEAD `0db618a` (no seat commits). Wave start (`start.json`) 07:43:44Z. Axis: depth.
## Findings (severity · exploit path · evidence · smallest remediation)
1. **HIGH — operator install directive is in force for every seat; the contract is prompt text only.**
   Every seat's injected rules say to install "without asking first" via `sudo pacman -S --needed --noconfirm
   <pkg>` (task-result.json progress lines 15–169). Nothing outside the prompt enforces the wave context's ban.
   Path: a read-only seat decides a tool "helps" (e.g. pacman-contrib, SafetySourceInjection I5) → passwordless
   sudo partial upgrade. This class actually ran: snapshot `libinput_log` 2429, by a mado seat
   (IncidentTimeline.md:16). Fix: L1 appends one `.ufo/l0-questions.md` line asking the operator to scope the
   directive away from read-only/host-safety seats (allowed by round prompt :215-217). Never edit RULES.md or routing.
2. **MED — fabricated observation.** IncidentTimeline.md:30 says "pending update count is 229". In host-snapshot.json
   (sha256 `b101f374…ea81`, 07:44:39Z), `pending_updates` has 413 lines, exit0, empty stderr. Path: C2 copies
   229. Fix: never cite that line. IncidentEntry messaged.
3. **MED — probe-exclusivity breach ("Only HostSnapshot runs probes").** Seats that read host files directly:
   IncidentTimeline.md:40 (`pacman.log:2285-2439`), ReviewSourceTier.md:27-30,53, ReviewSnapshotPrivacy.md:24
   (log 2035–2254), PacmanPrint.md:47 (`/usr/share/man/man8/pacman.8.gz`). The reads mutate nothing, but their
   lines (fuse2/shellcheck `-Sy`, python deps, argv paths) are outside the snapshot digest. IncidentTimeline
   also claims "no live host commands". Fix: C2/LOG cite only snapshot-pinned lines
   (2,292,300,306,313,415,771,1134,1406,1415,2252,2255,2288,2429,2432,2436). Label anything else as a seat claim.
4. **LOW-MED — new bare locator inside the locator fix.** ActiveRefs' R15 notices in the r14 MD/JSON cite
   verifier lesson `:143-165` for AF_UNIX/1270/1272–1273. At HEAD that text is :233-239 (§ Adjudicated
   concerns and routing, item 1; AF_UNIX :235). Fix: cite the stable section/item. ActiveRefs messaged.
5. **LOW — interface gap invites a cross-seat write.** IncidentMeasure requires C2 `snapshot_sha256`, but the field
   is absent from the C2 field list (spec.json:3) and from IncidentEntry's task. Only IncidentEntry (owner) may add
   it. IncidentMeasure must never patch the C2 JSON. This matches ReviewIncidentObservation F1.
6. **LOW — labrat vs "Leaf/no delegation".** Executors may spawn one labrat, read-only per round prompt :203-205;
   labrat writes have no owner row. Fix: L1 rejects labrat artifacts outside the executor's owned files.
7. **INFO — publication.** Wave dirs are committed wholesale (round-14/repair: 44 files); origin is GitHub, visibility
   unchecked. host-snapshot.json holds 413 package rows + a pacman argv line. ReviewSnapshotPrivacy owns this.

## Clean results (observed)
- Ownership (dispatch `taskCall.tasks`, 64/64 prefix-identical to spec): LocatorEntry C1 pair; LocatorGate
  check-locator-clarification.py; IncidentEntry C2 pair; SourceRegistry SOURCES.md; ActiveRefs r14 MD/JSON, SKILL,
  README; HostSnapshot snapshot; IncidentMeasure measure-update-recheck.py; C1SourceWitness own .json; L1
  LOG/SCORECARD/QUALITY/lesson. 56 seats report-only. No file has two owners; 64 report paths are unique.
- Worktree (`git status -uall`, 51 entries): all map to their owner. Only `build/l1-source-review.json`
  (04:47:31 -03) is unassigned; it is L1-named and inside L1's lane scope [INFERENCE: L1 authored].
- Diffs are additive (`git diff --numstat`): LOG +33, SCORECARD +27, QUALITY +3, SOURCES +5, r14 MD +41, r14 JSON
  +40/−1. The −1 is only `]`→`],` for the appended `r15_supersession` key. Verifier lessons, PROVINCE, SKILL and
  README are unchanged.
- Fleet: `find -newermt 07:43:44Z` finds no file outside lane/mori/souji. Fleet HEAD `e7b1f98` (04:40:40 -03, before
  the wave) adds only `.ufo/prompts/tsukuroi-round-15.md`. The dirty watchdog.log and state baselines have mtimes
  04:40:39–41, also before the wave. Relative-path trap: fleet `.ufo/waves/round-15` holds only 2026-10-13
  historical files. Recent mori and souji writes are under their own wave/tools paths [INFERENCE: own rounds].
- Host: every snapshot probe is read-only (`pacman -Q`, `-Qu`, `stat`, `grep` on log and hooks). libinput 1.32.0-1
  and mkinitcpio 41.1-1 match the post-incident state.
- LocatorGate checker (static): `git` only, with list argv. `--revision` must match `^(HEAD|hex{4,64})$` and then
  `rev-parse --verify`, which blocks `--output=` option injection. GIT_* env is stripped, GIT_OPTIONAL_LOCKS=0,
  and the checker makes no writes.

## Recommendations to L1
- After integration, run one read-only closure probe: repeat `pacman -Q libinput libinput-tools mkinitcpio systemd`
  for equality, plus `pacman.log` lines ≥04:43:44 -03. This proves zero package mutation across the wave; the
  snapshot's libinput filter misses non-libinput transactions.
- Statically audit `tools/measure-update-recheck.py` once it lands. It was absent at audit time.

## Limits
- No host probe, process listing (argv probing prohibited) or pacman run by me. "No omp CLI" rests on a static grep of
  build outputs (none found); live processes unchecked. Point-in-time: seats still running; mtimes ≠ authorship.
- Tools used: read, grep, glob, bash (git, find -newermt, stat), Python JSON parsing. Installed/updated: none.
