VERDICT: draft

Seat ConsiderMap, tsukuroi round 43 w1, item F-6. Mined proposal 5 of
`considerthese/2026-10-26.md` ("Cross-note correction propagation map") and built the map for the
round-42 SC1/SC3 withdrawals and SC4/SC5 narrowings, then drafted the lesson section text.
All line pins are at `717b716a8943151ace8657e0ca23d7d9b8434f26`. Receipts:
`.ufo/waves/round-43/w1/ConsiderMap/map-receipts.txt` (328 lines, 33 027 bytes).

Nothing in this seat ran a counter, built a clone, ran `btrfs`, or installed a tool. All reads were
`git -C <lane> show <rev>:<path>` / `git grep` at the frozen revision; no lane file was written
except this report and the receipts directory above.

---

## 1. Proposition inventory (the things a dependent can depend on)

Taken from `corpus/knowledge/btrfs-scrub-record-r42.md:171-203` (heading at `:171`, body `:173-203`)
and `corpus/knowledge/btrfs-scrub-record-r43.md:8-14` (`## SR1` `:17`, `## SR3` `:45`, `## SR6` `:80`):

| Token | Proposition | Status after round 43 |
|---|---|---|
| P-SC1a | the record is written to `_tmp` and renamed over the record under `flock(LOCK_EX\|LOCK_NB)`, mode 0600 | survives (re-grounded as SR1) |
| P-SC1b | "a reader sees either the old or the new record, **never a half-written one**" | **withdrawn** (r42:178) |
| P-SC1c | `_tmp` is opened `O_WRONLY\|O_CREAT` **without** `O_TRUNC` and never unlinked, so a shorter later record leaves the older tail and status reports `invalid data on line …` | added by the correction (r42:181-184); re-grounded SR1 |
| P-SC3a | the userspace `btrfs scrub start` process writes the record; recording is disabled with a "status recording disabled" warning on mkdir/first-write failure; running state is asked of the kernel ioctl, independent of the file | survives |
| P-SC3b | "an all-zero record when the scrub starts **(or is resumed)**" | **withdrawn** (r42:185-187) |
| P-SC3c | "**only the final write reports a failure**" | **withdrawn** (r42:188-192) |
| P-SC3d | host reading: capture.txt:8 is the template unit, no instance timer listed | **narrowed** (r42:193-194) |
| P-SC4a | fold semantics, `running`/`aborted`/`finished`/`interrupted`, `no stats available`, `ENOENT` = no history | survives |
| P-SC4b | the fold walks the **current** device list; `interrupted` can be read while a scrub runs when the ioctl refuses the caller; a live start process is read through the progress socket first | **narrowed** (r42:195-200) |
| P-SC5a | per-device `scrub_speed_max`, 0 = no limit, a failed read also reads 0, arrived in 6.6.3 | survives |
| P-SC5b | status prints a device's limit only for a device that has a record line, numerically only when >1; `start` reports the limit it **writes** from `--limit` (default 0) | **narrowed** (r42:201-203) |
| P-RUN | running state comes only from `BTRFS_IOC_SCRUB_PROGRESS`, which returns `-EPERM` without `CAP_SYS_ADMIN`, so an unprivileged caller never reads `running` | new in round 43 (SR6, r43:80-100) |

Pointer legend for the map: **C** = a pointer to the corrections exists in the same file
(`Corrections — round-42 wave 2`, or a sentence naming it); **R** = a pointer to
`corpus/knowledge/btrfs-scrub-record-r43.md` exists in the same file; **–** = neither.

## 2. The map — named dependents (`corpus/knowledge`, `SKILL.md`, `corpus/README.md`, `PROVINCE.md`, `SCORECARD.md`, `LOG.md`)

| # | Site | Depends on | C | R | Note |
|---|---|---|---|---|---|
| 1 | `corpus/knowledge/btrfs-scrub-record-r42.md:4` | all of SC1-SC5 | **yes** | **yes** | header `superseded-in-part:` names both the corrections and r43 |
| 2 | `…-r42.md:14` | P-SC1…P-SC5 framing ("Rows SC1-SC5 state upstream behaviour") | file-level only | file-level | the scope paragraph carries no inline marker; `:4` is the marker |
| 3 | `…-r42.md:20-24` (SC1 statement, `:22` "never a half-written one") | **P-SC1b** | **yes** (`:178`) | via `:4` | withdrawn sentence still sits in the row body |
| 4 | `…-r42.md:65-75` (SC3 statement, `:68` "(or is resumed)", `:71-73` "only the final write…") | **P-SC3b**, **P-SC3c** | **yes** (`:185`, `:188`) | via `:4` | |
| 5 | `…-r42.md:145-146` (triage: "not as 'never scrubbed' (SC3); what SC3 adds is the mechanism") | P-SC3a conclusion only | **yes** (`:173`) | via `:4` | conclusion is the held SH4 one; survives |
| 6 | `…-r42.md:157` (Limits: "cannot show that no scrub ever ran (SC3)") | P-SC3a conclusion | **yes** | via `:4` | survives |
| 7 | `corpus/knowledge/btrfs-scrub-record-r43.md:8-14` | P-SC1b/P-SC1c, P-SC3b/P-SC3c, P-SC4b(running state), P-SC5b | points at r42 `:8-10` | n/a (is r43) | two-way link with `…-r42.md:4` |
| 8 | `SKILL.md:3901` (section lead "SC1-SC5 on S237…") | P-SC1a…P-SC5a | file-level (`:3948`) | **no** | |
| 9 | `SKILL.md:3907` (`no stats available` ← SC4) | P-SC4a | – | – | survives unchanged |
| 10 | `SKILL.md:3908` (no `scrub.status.<fsid>` ← SC1, SC3) | P-SC1a, P-SC3a | file-level | **no** | writer-identity leg survives |
| 11 | `SKILL.md:3910` (`_tmp` beside the record ← SC1) | P-SC1a + **P-SC1c** | repaired by the bullet `:3949-3950` | **no** | the row itself still reads as "staging file, not damage" |
| 12 | `SKILL.md:3911` (read fails at once ← SC1 flock) | P-SC1a | – | – | survives (SR1) |
| 13 | `SKILL.md:3913` ("status recording disabled" ← SC3) | P-SC3a + **P-SC3c** | repaired by the bullet `:3951` | **no** | |
| 14 | `SKILL.md:3914` (status `running` ← SC3) | P-SC3a + **P-RUN** | **not named** by the bullet `:3949-3952` | **no** | **gap**: the bullet names `_tmp`, SC3, SC4 rows only; `running` now has a privilege precondition (SR6) the table never states |
| 15 | `SKILL.md:3916` (`finished` ← SC4) | P-SC4a | – | – | survives; P-SC4b device-list caveat absent |
| 16 | `SKILL.md:3917` (`interrupted` "nothing running" ← SC4) | **P-SC4b** | repaired by `:3951-3952` | **no** | |
| 17 | `SKILL.md:3918` (`scrub_speed_max` ← SC5) | P-SC5a + **P-SC5b** | **not named** by the bullet | **no** | **gap**: narrowing absent from both the row and the repair bullet |
| 18 | `SKILL.md:3947-3952` (outcome bullet) | all | **yes** | **no** | the only prose pointer in `SKILL.md` |
| 19 | `SKILL.md:2368` (SH4 row, round 26) | the held conclusion only (pre-r42) | – | – | no dependence on withdrawn text |
| 20 | `SKILL.md:3122` (`scrub-record-r42` counter registry row) | the frozen r42 row set + predicate | – | – | documents a frozen counter, not a proposition; no edit needed |
| 21 | `corpus/README.md:410` (coverage-map row) | P-SC1a, P-SC3a, P-SC4a, P-SC5a — and it restates SC1/SC3/SC5 in the same breath as the verified rows | **no** | **no** | **worst gap**: the coverage map presents all five rows as the entry's content, with no marker that two are withdrawn |
| 22 | `corpus/README.md:412-414` (Frontier summary) | coverage fact only ("stays Frontier, no census arm reads it") | – | – | survives |
| 23 | `PROVINCE.md:212-214` (**Still Frontier**) | coverage fact | – | – | survives |
| 24 | `PROVINCE.md:239-244` (Round-42 note) | P-SC1a (":241 `_tmp`-then-rename under `flock`"), P-SC3a, P-SC5a; **and `:243-244` a privilege claim** | **no** | **no** | **gap + defect**, see §4 |
| 25 | `SCORECARD.md:2574` (round-42 declaration C2 row) | all five rows | – | – | frozen declaration; superseded in-file by `:2606` |
| 26 | `SCORECARD.md:2606` (round-42 outcome row) | SC1/SC3 `fails`, SC4/SC5 `partly` | **yes** | – | the authoritative outcome row |
| 27 | `SCORECARD.md:2621` (depth axis) | "round-42 C2 not verified (bound `fails` on SC1 and SC3)" | **yes** | – | |
| 28 | `SCORECARD.md:2643-2645` (planned row) | routing "re-ground SC1 and SC3" | – | – | discharged by `:2662` |
| 29 | `SCORECARD.md:2653` (round-43 declaration) | "C2 re-grounds the withdrawn SC1/SC3 text" | **yes** | – | |
| 30 | `SCORECARD.md:2662` (round-43 C2 row) | SR1/SR3/SR6 | – | **yes** | |
| 31 | `LOG.md:1570` (round-42 claims) | P-SC1…P-SC5 framing | in-entry at `:1579` | **no** | the pointer is semantic, not the section title |
| 32 | `LOG.md:1574-1575` | SC1/SC3 `fails`, SC4/SC5 `partly` | **yes** | – | |
| 33 | `LOG.md:1579-1580` | "two adopted wave-1 notes made SC3 false (QUALITY 91); SC1/SC3/SC4/SC5 corrections appended to the entry" | **yes** | – | |
| 34 | `LOG.md` (round-43 entry) | would carry the r43 pointer | — | **absent** | no `## Round 43` heading at this revision (`grep -n '^## Round 4[0-9]' LOG.md` ends at `:1561` Round 42) |

## 3. Adjacent dependents (outside the six named paths, same propositions)

| Site | Depends on | C | R | Note |
|---|---|---|---|---|
| `corpus/SOURCES.md:246` (S237) | P-SC1a, P-SC3a | – | **yes** | `used-by: …-r42.md, …-r43.md` |
| `corpus/SOURCES.md:247-248` (S238, S239) | P-SC5a, P-SC3d host readings | – | – | correct: r43 quotes S237/S240/S241 only (`…-r43.md:1`) |
| `corpus/SOURCES.md:249-250` (S240, S241) | P-RUN | – | **yes** | |
| `corpus/QUALITY.md:179` (QUALITY 91) | the SC3 falsehoods as a failing example | (names the withdrawal inline) | – | rule text, historical example |
| `corpus/lessons/round-42.md:26`, `:71` | SOURCES diff, R42-ADOPTED-UNREAD | **yes** (`:71`) | – | append-only lesson |
| `corpus/lessons/round-42-verifier-spotcheck.md:191-193` | the withdrawal, and the demand for "a correction pointer that such a sweep reads" | **yes** | – | this is the origin of `…-r42.md:4` |

`corpus/knowledge/storage-health-r26.md` and `btrfs-space-r30.md` mention scrub but cite no SC row
and restate no withdrawn proposition (`CMD6` in the receipts), so they are not dependents.

## 4. Findings

**F-6/a — the propagation index is machine-checkable in exactly one file, and it is right.**
`corpus/SOURCES.md` `used-by` (CMD8) reads S237 → r42 + r43, S238/S239 → r42, S240/S241 → r43, which
matches what `…-r43.md:1` actually quotes. This is the only place where "did the correction reach the
dependent" is decidable by `grep`. Every prose dependent is hand-maintained.

**F-6/b — four sites restate the corrected text with no pointer at all.**
`corpus/README.md:410` (C– R–), `PROVINCE.md:239-244` (C– R–), `SKILL.md:3914` (C– R–) and
`SKILL.md:3918` (C– R–). The `README.md` row is the coverage map: it is what a reader uses to decide
what the entry contains, and it describes SC1/SC3 as the entry's holdings with no marker that two rows
are withdrawn. Two further index sites, `SKILL.md:3122` and `:3901`, cite the row set without an r43
path but assert no corrected proposition themselves.

**F-6/c — `SKILL.md`'s local repair is incomplete in exactly two rows.**
`:3949-3952` names "the `_tmp` and SC3/SC4 table rows". The table also carries the `running` row
(`:3914`), which now has the P-RUN privilege precondition, and the `scrub_speed_max` row (`:3918`),
whose P-SC5b narrowing (limit printed only for a device with a record line, numerically only when >1;
`start` reports the limit it writes) appears nowhere in `SKILL.md`.

**F-6/d — `PROVINCE.md:243-244` is an unrepaired overreach on the SC1 0600 fact.**
The sentence reads "`btrfs scrub status /` reads the record unprivileged on this host (wave-1
`C2ExecHostRecheck`), so an arm needs no privilege for the record itself." Two things are wrong with it
as written: (i) on this host there is no record, so the run shows the `ENOENT` path only
(`…-r42.md:24` "No record exists: `/var/lib/btrfs` is absent"); (ii) a *present* record is created mode
0600 with every open taking `LOCK_EX|LOCK_NB` (`…-r42.md:20-24`, re-grounded unchanged as SR1), which is
why the round-42 wave-1 promotion note concluded the opposite in terms — "an unprivileged census
**cannot parse record content** on a stock host; what it *can* read unprivileged is the directory
(existence), file stat, and sysfs `scrub_speed_max`" (`.ufo/waves/round-42/w1/ConnFrontier.md:108-111`).
The map's whole point is that this class of sentence is not covered by the corrections, because the
corrections address the withdrawn sentences and this one was never inside a counted row.

**F-6/e — no gate reads a correction pointer.** `git grep -n 'superseded-in-part' <rev> -- tools`
returns nothing (CMD7): no counter or gate consumes the marker that `…-r42.md:4` gained for the
spot-check's K24-style header sweep (`corpus/lessons/round-42-verifier-spotcheck.md:191-193`). The
only structural gate in this area, `tools/check-appended-notices.py`, is bound to the round-18 registry
`corpus/knowledge/freshness-recheck-r18.json` (`tools/check-appended-notices.py:27`, and `:110` matches
the file name explicitly).

**F-6/f — one dependent cannot carry the pointer yet, by construction.** `LOG.md` has no round-43
entry at `717b716a` (CMD9: headings end at `:1561`), so the r43 pointer will have to be written when
that entry lands, not repaired afterwards.

## 5. Exact grep commands used (all against the frozen revision)

```
L=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin
R=717b716a8943151ace8657e0ca23d7d9b8434f26

git -C "$L" grep -l 'btrfs-scrub-record-r42' "$R" | cat
git -C "$L" grep -l 'btrfs-scrub-record-r43' "$R" | cat
git -C "$L" grep -n -E 'scrub' "$R" -- '*.md' ':!.ufo' | grep -E '\bSC[1-6]\b'
git -C "$L" grep -ln 'btrfs-scrub-record-r42' "$R" -- '*.md' ':!.ufo'
for pat in half-written all-zero 'failed to record the result' 'status recording disabled' \
           scrub_speed_max 'scrub\.status' BTRFS_IOC_SCRUB_PROGRESS; do
  git -C "$L" grep -n "$pat" "$R" -- '*.md' ':!.ufo'; done
for f in corpus/knowledge/btrfs-scrub-record-r42.md corpus/knowledge/btrfs-scrub-record-r43.md \
         SKILL.md corpus/README.md PROVINCE.md SCORECARD.md LOG.md corpus/SOURCES.md \
         corpus/QUALITY.md corpus/lessons/round-42.md corpus/lessons/round-42-verifier-spotcheck.md; do
  for t in 'Corrections — round-42 wave 2' 'scrub-record-r43' 'superseded-in-part'; do
    printf '%s %s %s\n' "$f" "$t" "$(git -C "$L" show "$R:$f" | grep -c "$t")"; done; done
git -C "$L" grep -n 'superseded-in-part' "$R" -- tools
git -C "$L" show "$R:corpus/SOURCES.md" | sed -n '246,250p' | awk -F'|' '{print $2, $12}'
git -C "$L" show "$R:LOG.md" | grep -n '^## Round 4[0-9]'
git -C "$L" show "$R:corpus/knowledge/btrfs-scrub-record-r42.md" | grep -n '^## Corrections\|^## SC[1-5]'
git -C "$L" show "$R:corpus/knowledge/btrfs-scrub-record-r43.md" | grep -n '^## '
git -C "$L" grep -n 'DEFAULT_REGISTRY\|freshness-recheck-r18' "$R" -- tools/check-appended-notices.py
```

Observed outputs are verbatim in `.ufo/waves/round-43/w1/ConsiderMap/map-receipts.txt` (CMD1-CMD9).
The pointer-token counts (CMD3) are the table that decides C/R above:

```
corpus/knowledge/btrfs-scrub-record-r42.md     corrections_section=2 r43_path=1 superseded_hdr=1
corpus/knowledge/btrfs-scrub-record-r43.md     corrections_section=1 r43_path=1 superseded_hdr=0
SKILL.md                                       corrections_section=1 r43_path=0 superseded_hdr=0
corpus/README.md                               corrections_section=0 r43_path=0 superseded_hdr=0
PROVINCE.md                                    corrections_section=0 r43_path=0 superseded_hdr=0
SCORECARD.md                                   corrections_section=1 r43_path=2 superseded_hdr=0
LOG.md                                         corrections_section=0 r43_path=0 superseded_hdr=0
corpus/SOURCES.md                              corrections_section=0 r43_path=3 superseded_hdr=0
corpus/QUALITY.md                              corrections_section=0 r43_path=0 superseded_hdr=0
corpus/lessons/round-42.md                     corrections_section=1 r43_path=0 superseded_hdr=0
corpus/lessons/round-42-verifier-spotcheck.md  corrections_section=1 r43_path=0 superseded_hdr=0
```

Note for anyone re-running this: `SC1`-`SC5` is overloaded in the lane. `corpus/knowledge/root-dac-decision-r12.json`,
`root-dac-correction-r13.*` and `closeout-r11.md:379-383` use the same tokens for an unrelated scenario
namespace; only sites that sit in a scrub context (CMD4) are in this map.

## 6. Dependents that need a pointer (the deliverable list)

Ordered by cost; 1-3 are corrections, 4-6 are r43 links.

1. **`corpus/README.md:410`** — add a trailing clause to the coverage-map cell: four words marking that
   SC1 and SC3 stand withdrawn and SC4/SC5 narrowed, pointing at `…-r42.md` "Corrections — round-42
   wave 2" and at `…-r43.md`. (C– R– today.)
2. **`PROVINCE.md:239-244`** — append one sentence under the Round-42 note naming `…-r43.md` (SR1/SR3/
   SR6), and **fix `:243-244`** to say what the host shows: `btrfs scrub status /` runs unprivileged and
   prints `no stats available`; a present record is 0600, so an arm may stat it and read the directory
   but not parse it (`ConnFrontier.md:108-111`).
3. **`SKILL.md:3914` and `:3918`** — extend the repair bullet at `:3949-3952` to name the `running` row
   (SR6: only a caller with `CAP_SYS_ADMIN` sees `running`) and the `scrub_speed_max` row (P-SC5b), and
   add the r43 path to that bullet. Without this the table's two narrowest rows read as unconditional.
4. **`LOG.md` round-43 entry (not yet written)** — must carry the r43 pointer and the path of this map.
5. **`SKILL.md:3901`** — optional: the section lead can gain "(rows SC1/SC3 withdrawn, SC4/SC5 narrowed;
   see the outcome bullet at the end of this section)" so a reader who stops at the lead is not misled.
6. **`corpus/knowledge/btrfs-scrub-record-r42.md:14`** — optional: the scope paragraph could repeat the
   `:4` marker; `:4` already covers a header-reading sweep.

No change is needed at `SCORECARD.md:2574` (frozen declaration, superseded in-file at `:2606`),
`:2606`, `:2621`, `:2643-2645`, `:2653`, `:2662`, `LOG.md:1570-1580`, `corpus/SOURCES.md:246-250`,
`corpus/QUALITY.md:179`, or the two round-42 lesson files — each either states the outcome correctly or
is append-only history whose text was true at its commit.

## 7. Drafted lesson section (exact Markdown)

Destination: `corpus/lessons/round-43.md`, as a `###` subsection under `## Gate`, beside the existing
`### considerthese — …` pattern of `corpus/lessons/round-42.md:53-59`. The `~~~~` fence below is a
delimiter only and is not part of the text.

~~~~markdown
### considerthese — cross-note correction propagation map (`considerthese/2026-10-26.md`, proposal 5)

Mined: "A map of which notes depend on which propositions would let me check that a correction reached
every dependent note." Adopted for its own reason, not as a promise: round 42's seven-note TO1/TO8
propagation was hand-carried, and round 42's SC1/SC3 withdrawals produced text in three other files
without a machine-checkable link.

Built by seat ConsiderMap (`w1/ConsiderMap.md`, receipts `w1/ConsiderMap/map-receipts.txt`; every line
pin at `717b716a`). The map names each dependent site, the proposition it rests on, and whether it
carries a pointer to the round-42 corrections or to `corpus/knowledge/btrfs-scrub-record-r43.md`. The
propositions are P-SC1a/b/c, P-SC3a/b/c/d, P-SC4a/b, P-SC5a/b from `btrfs-scrub-record-r42.md:173-203`
and P-RUN from `btrfs-scrub-record-r43.md:80-100`.

Outcome: **34 dependent sites in the six named paths plus 6 adjacent ones; 4 sites restate a withdrawn
or narrowed proposition with no pointer at all, and one of those also asserts the opposite of what the
SC1 0600 fact implies; 2 rows of the `SKILL.md` triage table are not covered by its own repair bullet.**
One file is machine-checkable, `corpus/SOURCES.md` `used-by`, and it is correct (S237 → r42 + r43;
S238/S239 → r42; S240/S241 → r43), because its cells name what the notes actually quote.

| Dependent | Depends on | Corrections pointer | r43 pointer |
|---|---|---|---|
| `btrfs-scrub-record-r42.md:22` (SC1 body) | P-SC1b withdrawn | yes, `:178` | via `:4` |
| `btrfs-scrub-record-r42.md:68`, `:71-73` (SC3 body) | P-SC3b, P-SC3c withdrawn | yes, `:185`, `:188` | via `:4` |
| `btrfs-scrub-record-r42.md:4` | all rows | yes | yes |
| `SKILL.md:3910` (`_tmp` row) | P-SC1a + P-SC1c | yes, bullet `:3949-3950` | no |
| `SKILL.md:3913` (recording-disabled row) | P-SC3a + P-SC3c | yes, bullet `:3951` | no |
| `SKILL.md:3914` (`running` row) | P-SC3a + P-RUN | **no** | **no** |
| `SKILL.md:3917` (`interrupted` row) | P-SC4b | yes, bullet `:3951-3952` | no |
| `SKILL.md:3918` (`scrub_speed_max` row) | P-SC5a + P-SC5b | **no** | **no** |
| `corpus/README.md:410` (coverage map) | P-SC1a, P-SC3a, P-SC4a, P-SC5a | **no** | **no** |
| `PROVINCE.md:239-244` (Round-42 note) | P-SC1a, P-SC3a, P-SC5a; `:243-244` privilege claim | **no** | **no** |
| `SCORECARD.md:2606`, `:2621`, `:2653` | the outcome | yes | – |
| `SCORECARD.md:2662` | SR1/SR3/SR6 | – | yes |
| `LOG.md:1570-1580` | the claims and the verdicts | yes, `:1579` | no (no r43 entry yet) |
| `corpus/SOURCES.md:246-250` | the sources each note quotes | – | yes for S237/S240/S241 |

Findings carried, none of them repaired here (read-only round):

- **R43-PROP-README.** `corpus/README.md:410` is the coverage map and describes SC1, SC3 and SC5 as
  the entry's holdings with no marker that SC1/SC3 stand withdrawn and SC4/SC5 are narrowed. A reader
  who consults the coverage map instead of the entry reads a rejected claim as a described one.
- **R43-PROP-PROVINCE.** `PROVINCE.md:243-244` reads "`btrfs scrub status /` reads the record
  unprivileged on this host … so an arm needs no privilege for the record itself." On this host there
  is no record, so that run exercises the `ENOENT` path only (`btrfs-scrub-record-r42.md:24`), and a
  present record is mode 0600 with a non-blocking exclusive lock on every open (P-SC1a, re-grounded as
  SR1) — the round-42 wave-1 promotion note states the consequence in terms: an unprivileged census
  "cannot parse record content", only the directory, the file stat and sysfs `scrub_speed_max`
  (`.ufo/waves/round-42/w1/ConnFrontier.md:108-111`). The sentence needs the qualifier, not a pointer.
- **R43-PROP-SKILL-NARROW.** `SKILL.md`'s repair bullet (`:3949-3952`) names "the `_tmp` and SC3/SC4
  table rows", so the `running` row (`:3914`) and the `scrub_speed_max` row (`:3918`) keep their
  pre-correction force: SR6 makes `running` an elevation-gated reading that a census never sees, and
  P-SC5b limits what a status line may be read to report.
- **R43-PROP-NOGATE.** No tool reads the `superseded-in-part:` marker
  (`git grep -n 'superseded-in-part' <rev> -- tools` → no match). The marker exists for the K24-style
  header sweep demanded by `corpus/lessons/round-42-verifier-spotcheck.md:191-193`, and nothing consumes
  it, so propagation is still manual on the reading side as well as the writing side.

Flip: a round that adds a `check-correction-pointers.py` gate reading header markers plus a declared
dependent list would close R43-PROP-NOGATE; until then, the map is the checklist, and the three
unpointed dependents above are its first four items.
~~~~

## 8. What this seat did not do

- Did not touch `.ufo/waves/round-42/*` or `round-43/*` seat outputs beyond reading them as evidence; they
  are reports, not lane content, and the map is about the six named paths.
- Did not run `tools/check-scrub-record-r42.py`, `tools/check-scrub-record-r43.py`, the census selftest or
  any counter; no claim here rests on a counter verdict.
- Did not build a fixture, clone the lane, or install/upgrade any tool.
- Did not edit any lane file: this report and `w1/ConsiderMap/map-receipts.txt` are the only writes.
