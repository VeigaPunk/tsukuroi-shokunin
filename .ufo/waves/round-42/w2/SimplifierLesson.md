VERDICT: defect-found

# F-24 — lesson/SKILL concision: the entry's triage block and its SH3/SH4 recap

Seat `SimplifierLesson`, round-42 w2, item F-24. Target read at `78abb8b5cdc9da511b4fc523e661517a68dd33d3`
(entry sha256 `536846f6cb49c2c41cc48228bb03945da0d232dff28c89b35164dc88ee445ef8`, 168 lines; `SKILL.md`
sha256 `1306a0907f08c55e4d15ef640798e1e9e988bb6c65142166f722adc2d3122872`, 3941 lines). Lane tip at dispatch
`78abb8b5`; all line numbers below are at that pin.

The defect is duplication, measured, not argued: the entry's four triage bullets (:144-150) are covered four of
four by the SKILL decision table (:3905-3916), and the entry's scope (:8-10) recaps SH3 and two SH4 clauses before
the next sentence claims novelty against them. Neither region is a counted row: the counter's unit is the lines
under each `## SC<n>` heading (`tools/check-scrub-record-r42.py:83-96`), and both regions sit outside every heading it
parses. Nothing proposed here moves a frozen token (`:54-61`), a quote, a host reading or a row verdict.

Three exact texts follow: **§2** the triage collapse (the duplication removal proper — deferred on measured anchor
cost), **§3** the scope drop (landable now, no line moves), **§4** the append-only clarification (landable now, no
line moves). §5 lists what I examined and did **not** delete, with the axis each deletion would harm.

## 1. What duplicates what (measured)

Bullet → table row, read against the table's `Reading` and `Action` columns (entry lines at the pin, SKILL lines
`3905`-`3916`):

| entry bullet | bytes | SKILL rows that already carry it | lexical overlap of the best row |
|---|---|---|---|
| `:144-145` read "no scrub record" as a gap, not "never scrubbed"; SC3 adds mechanism, not verdict | 148 | `:3905` (Action: "read \"no record of a run\", not \"never scrubbed\""), `:3906` (Action: "stored-data integrity stays `UNVERIFIED` (SH4)") | 27 % |
| `:146-147` record is per device; one canceled device makes the run `aborted` | 162 | `:3913` ("any device record is canceled (SC4)"), `:3914` ("every device that has a record is finished; devices without a record are skipped (SC4)") | 27 % |
| `:148-149` `interrupted` is a process outcome, not media; read `-d`/`-R` error sums | 209 | `:3915` ("an unfinished record and nothing running (SC4)" \| "a process outcome; read the per-device error sums (`-d`, `-R`)") | 59 % |
| `:150` slow scrub → read `scrub_speed_max` first | 80 | `:3916` ("`devinfo/<devid>/scrub_speed_max` limits it") | 80 % |

Lexical overlap is a stopword-filtered token ratio, and it understates the duplication for the first two bullets
because the table compresses the same propositions into different words; the semantic mapping above is the claim,
the percentages are the shape. b3 and b4 are near-verbatim restatements. The only proposition in the block that the
table does not carry is b1's "what SC3 adds is the mechanism, not a new verdict" — meta about the entry, itself
restated in the scope (:10-13) and in SC3 (:73-74).

The bullets also cost more than they carry because the same proposition then stands five times in two files:

```
$ git grep -n -i "never scrubbed" 78abb8b5 -- corpus/knowledge/btrfs-scrub-record-r42.md SKILL.md
SKILL.md:3905:| `btrfs scrub status` prints `no stats available` | … | read "no record of a run", not "never scrubbed"; …
corpus/knowledge/btrfs-scrub-record-r42.md:13:… how far "no record" may be read as "never scrubbed". Rows SC1-SC5 …
corpus/knowledge/btrfs-scrub-record-r42.md:144:- Read "no scrub record" as a gap in evidence (`UNVERIFIED`, SH4), not as "never scrubbed" (SC3); …
```

with `corpus/knowledge/btrfs-scrub-record-r42.md:72-73` (SC3's own conclusion) and `:157` (the Limits bullet "they
cannot show that no scrub ever ran") completing the set; `SKILL.md:3906` carries the verdict half alone. Each grep
line above is elided to the clause that matters (prefix and tail cut); the untouched output is
`SimplifierLesson/proposition-sites.txt`.

On the other half of the item — sentences restating SH3/SH4 — the entry carries four candidates and only one is
pure restatement: the scope's `:8-10` recaps SH4's reader side ("`btrfs scrub status` reads a file under
`/var/lib/btrfs`") and SH3's whole subject ("what scrub verifies and repairs") before :10-13 claims the record's
statement was not held. The other three are load-bearing and §5 keeps them.

## 2. T (deferred) — collapse the triage block to the pointer it has become

Replace entry `:144-150` (7 lines, 609 B) with (2 lines, 230 B):

```
- The operator actions for every scrub-status signal are the decision table under `## Scrub status record — round 42`
  in `SKILL.md` (rows SC1-SC5); what SC3 adds to triage is the mechanism behind "no record", not a new verdict.
```

Net: −5 lines, −379 bytes. The enumeration of signals is not lost — it is the table's `Observation` column, which
the pointer names by heading (a stable anchor; I deliberately did not cite `SKILL.md:3905-3916`, which drifts on
every append above it). The section keeps the `## How this changes OS triage` heading and bullet form the neighbouring entry uses
(`corpus/knowledge/storage-health-r26.md:97-102`); it carries one bullet where that entry carries four, so the form
is shared and the content is not duplicated.

**Why this is deferred and not recommended for this wave.** It is the only one of the three that moves lines, and
the moved region is cited by in-flight reports. Live wave-2 citations of the entry, from
`grep -rn "btrfs-scrub-record-r42\.md[:`]\+[0-9]\+" .ufo/waves/round-42/w2/` (19 spans in 8 other seats' reports;
my own report is excluded by name):

| fate under T | spans (11 + 1 + 3 + 4 = the 19) |
|---|---|
| target unchanged | `:1`, `:2`, `:3`, `:47-48`, `:64-89`, `:66-67`, `:70-72`, `:91-121`, `:116`, `:118-121`, `:134` |
| span partly rewrapped by S, no line moves | `CritNoHarmFinal.md` `:4-9` — it cites the SH4 name-pattern credit, which S keeps inside that span |
| text deleted | `C2CritSC4.md` `:146-149`, `ConnRound43.md` `:149-150`, `CritTrendFinal.md` `:144` |
| shifted −5 | `CritTrendFinal.md` `:158`→`:153`, `SrcReopenS239.md` `:160`→`:155`, `:165-166`→`:160-161`, `:167`→`:162` |

Those reports name their pin (`w2/C2CritSC4.md:11` runs `git show 78abb8b5…` and records the entry's sha256), so
their citations remain true **of** `78abb8b5`; what breaks is tip-following. Landing T without a re-pin note leaves
seven locators pointing at text that no longer exists at the tip. Receipt: `SimplifierLesson/anchor-cost.txt`.

## 3. S (landable now) — drop the SH3/SH4 recap from the scope, keeping every claim the wave has bound

Replace entry `:8-15` (9 lines) with the nine lines below. Line count is deliberately unchanged, so every line
number below the hunk — including all 12 unaffected citations above and the 7 in `:144-168` — keeps its meaning.

Before (`:8-15`):

```
The lane already holds what scrub verifies and repairs and that `btrfs scrub status` reads a file under
`/var/lib/btrfs` (`corpus/knowledge/storage-health-r26.md` SH3, SH4; S129, S139), including the record's name
pattern (SH4) and that a scrub run with recording disabled cannot be excluded (SH4 note). It held no statement of the
record itself: how the file is replaced, its line format, which process writes it and when recording is switched off,
how the status command turns per-device lines into one filesystem verdict, and the per-device throughput limit that
same command reports (SC5). Those decide how far "no record" may be read as "never scrubbed". Rows SC1-SC5 state upstream behaviour of btrfs-progs v7.1 (the
version this host runs) from `cmds/scrub.c` and `CHANGES`; the host readings are this machine's, unprivileged.
Nothing here runs a scrub, writes `/var/lib/btrfs` or changes a scrub limit (operator actions).
```

After:

```
The lane already holds, in `corpus/knowledge/storage-health-r26.md`, what scrub verifies and repairs (SH3), the
record's name pattern (SH4) and that a scrub run with recording disabled cannot be excluded (SH4 note). It held no
statement of the record itself: how the file is replaced, its line format, which process writes it and when
recording is switched off, how the status command turns per-device lines into one filesystem verdict, and the
per-device throughput limit that same command reports (SC5). Those decide how far "no record" may be read as
"never scrubbed". Rows SC1-SC5 state upstream behaviour of btrfs-progs v7.1 (the version this host runs) from
`cmds/scrub.c` and `CHANGES`; the host readings are this machine's, unprivileged. Nothing here runs a scrub, writes
`/var/lib/btrfs` or changes a scrub limit (operator actions).
```

−88 bytes, 9 ↔ 9 lines, 0 citations moved. What leaves: the SH4 reader-side recap (the path is stated by SC1 itself
at `:19`, and by `SKILL.md:3906`), and the `; S129, S139` provenance recap — `corpus/SOURCES.md` rows S129 and S139
record `used-by: corpus/knowledge/storage-health-r26.md` and **not** this entry, so removing the ids changes no
registry claim; leaving them in cites two rows whose `used-by` does not name this entry. What stays is exactly what
the wave has bound:

- the name-pattern credit — `w2/CritNoHarmFinal.md:95` cites `btrfs-scrub-record-r42.md:4-9` for "it credits SH4 for
  the name pattern", and `w1/C2CritNovelty.md:125-133` (C1) requires that credit to survive in the *first* sentence
  while the novelty list must not re-claim the name. Both hold.
- "recording disabled cannot be excluded (SH4 note)" — the novelty boundary of SC3.
- `w1/C2CritNovelty.md:46-50` quoted the sentence this edit rewrites as a self-contradiction ("The base does not
  merely hold 'a file under `/var/lib/btrfs`'"). S removes the understating clause instead of correcting it; if the
  L1 prefers to keep a reader-side pointer, the minimal alternative is to replace only
  ``and that `btrfs scrub status` reads a file under `/var/lib/btrfs` (… SH3, SH4; S129, S139)`` with
  ``and that the status command reads `scrub.status.<fsid>` files under `/var/lib/btrfs` (SH4)`` — that keeps the
  pointer, saves less, and still needs the same 9-line rewrap.

## 4. E (landable now) — append the authority rule; the duplication stops growing even before T lands

Append after `:168` (the file's last line), nothing above it moves:

```markdown
## Errata (round 42, append-only)

- 2026-10-26 — **the triage section above restates the operator decision table; recorded, not silently edited.**
  The four bullets at `:144-150` repeat rows of the table under `## Scrub status record — round 42` in `SKILL.md`:
  bullet 1 the `no stats available` and `no scrub.status.<fsid>` rows, bullet 2 the `aborted` and `finished` rows,
  bullet 3 the `interrupted` row, bullet 4 the slow-scrub row. That table is the authority for what to do on a
  signal; this entry's section records what the rows change about reading one. New triage text lands in the table,
  not here. The bullets stay at this revision because wave-2 reports cite `:144`, `:146-149` and `:149-150`; the
  replacement that collapses them (7 lines to 2) is `.ufo/waves/round-42/w2/SimplifierLesson.md` §2, to land once
  those anchors retire.
```

`## Errata` is an existing closing section in this corpus (`corpus/knowledge/package-state-plane.md:228`,
`aur-risk-plane.md`, `driver-firmware-plane.md`, `memory-arm-ver-s8.md`), so this uses the lane's own append shape.
It is the part of the item that is *append-only* by construction: it names one authority, records why the duplicate
cannot be deleted at this pin, and stops the next round from adding a fifth bullet to the wrong copy. I did **not**
mirror it in `SKILL.md` — a symmetric note in the table would re-create the duplication it removes; the table
already cites its row source (SC1-SC5) on every line.

## 5. Examined and deliberately not deleted

| candidate | why it stays |
|---|---|
| SC3 `:72-74` "So a missing record does not prove that no scrub ran … That conclusion was already held (SH4 note); new here are the mechanism and the disable conditions." | Inside a counted row. The first sentence is the row's consequence, the second its novelty contrast: delete either and SC3 reads as a restatement of SH4's note — the exact finding `w1/C2CritNovelty.md:66-71` raises for a *different* reason (it calls the conclusion restatement-as-new but keeps the row "still depth"). Deleting text cannot fix that; the tags and the mechanism quotes do. |
| SC1 `:20` "(… the name pattern is already held, SH4)" | The row's own novelty boundary; with it gone, SC1's first sentence re-claims the name formula the base holds (`w1/C2CritNovelty.md:55-59`). Harm to the novelty axis. |
| Limits `:157` "they cannot show that no scrub ever ran (SC3)" | Not triage: it bounds what the host readings prove. Third of the five copies above, and the only one that states the evidence limit rather than the action. |
| SKILL table rows `:3905` and `:3906` (both "no record") | Two different observations (command output vs absent directory/file) and two different actions (read the file / nothing was modified). Merging them would collide with work in flight: `w2/C1RevSkill.md` proposes replacement cells at exactly `:3906` (`:124`) and `:3907` (`:79-85`), and rewrites `:3930`, `:3937` and `:3940-3941`, all of which a row merge moves. Deferred on the same anchor cost as T, and on that collision. |
| SKILL host paragraph `:3918-3924` (repeats the four host readings) | The only place in `SKILL.md` that states this host's scrub state; removing it pushes the operator to the entry for a reading the table needs inline. |
| A `## Triage` heading rename or a new "single authority" section in SKILL | Creates a fourth surface for the same content. §4 records the rule where the redundant copy lives. |

### Tradeoff of the three texts

S trades the entry's one explicit statement of SH4's reader side for 88 bytes; the path survives at `:19` (SC1 names
`/var/lib/btrfs/scrub.status.<fsid>`) and at `SKILL.md:3906`, and the alternative in §3 keeps the pointer instead.
T trades a one-hop lookup for a reader who has the entry but not `SKILL.md` — every action stays one heading away in
the same repo, and the entry's own SC rows carry the mechanism. E adds 856 bytes that are meant to expire: when T
lands, E's last three lines become false and must be superseded by the errata that lands T (the lane's append-only
shape allows exactly that; rewriting E in place is what §4 forbids for other text).

## 6. Evidence: the counted rows and the counter are untouched

Applied to a scratch clone at `78abb8b5` (`/fast/scratch/hyaku/tsukuroi-r42/SimplifierLesson/lane`, fixture
commits, no lane write); S and E only in `zerodrift.rev`, S+T+E in `full.rev`.

```
$ python3 tools/check-scrub-record-r42.py --revision <REV> --lane <fixture clone>
revision                       rows quotes_ok novelty_ok novelty_base_hits host_ok sources_ok capture_ok
78abb8b5 (pin)                    5         5          5                 0       5          1       True
zerodrift S+E                     5         5          5                 0       5          1       True
fullset S+T+E                     5         5          5                 0       5          1       True

per-row quote counts (good/in_window), before -> zerodrift -> fullset
  SC1 6/5 -> 6/5 -> 6/5   SC2 5/4 -> 5/4 -> 5/4   SC3 5/5 -> 5/5 -> 5/5
  SC4 7/6 -> 7/6 -> 7/6   SC5 5/5 -> 5/5 -> 5/5
```

`verdicts_ok` is 0 in all three runs because the fixture clone has no `w2-results.json` / `residual-results.json`
or `w2/<seat>.md` files: that field is a property of the clone, not of the edit, and **I did not measure it on the
real lane** (it depends on the ten counted verdicts landing this wave). Row text identity, computed with the
counter's own `sections()`:

```
SC1 identical=True sha dd6e6a0e76244d3e -> dd6e6a0e76244d3e  token LOCK_EX present
SC2 identical=True sha bc43120f32211169 -> bc43120f32211169  token scrub status:1 present
SC3 identical=True sha 53635b00932188f8 -> 53635b00932188f8  token status recording disabled present
SC4 identical=True sha 5328ae702bae5515 -> 5328ae702bae5515  token _SCRUB_FS_STAT_MIN present
SC5 identical=True sha f00c91e568969ffc -> f00c91e568969ffc  token scrub_speed_max present
```

Hunk geometry of the two fixture commits (`git diff -U0`): `zerodrift` = `@@ -8,6 +8,6 @@` and an append at
`:168`; `fullset` adds `@@ -144,7 +144,2 @@`. Entry 168 → 168 lines (S only) or → 174 lines (S+T+E).

## 7. What I did not do

- Did not land anything: the lane is read-only for this seat, and the L1 is the only committer. Both diffs are
  reproducible from the exact texts above; `SimplifierLesson/apply.py` applies them to a copy of the lane
  (`F24_LANE=<copy root> python3 apply.py P1 P2 P3`, where P1/P2/P3 are S/T/E in §3/§2/§4) and asserts line counts and
  row identity.
- Did not measure the counter at the real lane's tip (only at three revisions of my clone, §6); did not run the
  census, the C1 counter or any host probe — none is in this item's scope and nothing here touches a tool.
- Did not touch `SKILL.md`: every candidate there failed on the same anchor cost (§5, row 4), so the proposal is
  entry-only and no line of `SKILL.md` moves under any of the three texts.
- Did not verify the counter's `transcripts_bound` cross-check, `sources_ok` on the real lane, or the ten w2 verdicts.
- Installed/upgraded no tool.

## 8. Receipts — `.ufo/waves/round-42/w2/SimplifierLesson/`

`full.diff` (S+T+E, unified), `zerodrift.diff` (S+E), `apply.py` (exact text + assertions),
`counter-before.json` / `counter-zerodrift.json` / `counter-full.json` / `counter-compare.txt`,
`row-identity.txt`, `dup-map.txt`, `proposition-sites.txt`, `anchor-cost.txt`, `anchor.py`, `receipts.py`.
Scratch (`/fast/scratch/hyaku/tsukuroi-r42/SimplifierLesson`) removed after the copy.
