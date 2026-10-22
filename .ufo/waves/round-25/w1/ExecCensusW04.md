# Round 25, wave 1 — ExecCensusW04: classifying the registry duplicate-URL warnings

Seat: `ExecCensusW04` (executor, read-only). Date: 2026-10-22. Claim base: `b9046016831237cd04d38da11ba76e50d5380c53`.
Subject: routed defect 5 of round 24 (`corpus/lessons/round-24-verifier-spotcheck.md:102` — "Registry inflation: six
same-page re-registrations, and W04 went from 9 to 21, because the checker requires an opened-date of this round").

## Verdict

At `b9046016` the tsukuroi registry carries 21 duplicate-URL warnings; all 21 are cross-scope pairs, 17 of them are
same-page re-registrations, 0 are same-scope duplicates and 4 are legitimate distinct-anchor uses of one page, so the
round-25 rows can add zero W04 warnings if every page gets exactly one registry row and a re-read of an
already-registered page updates that row's `recheck` in place instead of minting a new row.

## Findings

1. **[obs] The W04 rule is a pure URL-plus-scope rule, and it has no supersession exemption.**
   `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:643-649`:

   ```awk
   scope_key=u SUBSEP scope
   if (u!="" && (u in url_seen) && !(scope_key in url_scopes))
     printf "%s\tW04\t%s duplicate url %s across scopes\n",lane,id,u
   if (u!="" && (scope_key in url_scopes) && status!="rejected" &&
       url_scope_nonrejected[scope_key] &&
       teaches !~ /supersedes S[0-9]{3}/)
     printf "%s\tE04\t%s duplicate url %s within scope %s\n",lane,id,u,scope
   ```

   Consequences that drive the rest of this report. First, a W04 fires whenever a row re-uses a URL under a scope
   string that differs from the earlier row's; the rule never inspects `opened`, `recheck`, tier or status. Second, the
   `supersedes S###` marker exempts the same-scope case (E04) only; it does not exempt W04. A row that says
   "supersedes S089" and therefore carries a different scope still produces a W04. Third, copying the earlier row's
   scope string to dodge W04 would turn the row into an E04 finding and set the census exit code to 1, which is worse
   than the warning.

2. **[obs] My replica of the census' W04 detection is byte-identical to the real census at the base revision.**
   The script `/fast/scratch/hyaku/tsukuroi-r25/ExecCensusW04/repo/tools-draft/w04-classify.py` re-implements
   `url_of()` and the scope-key logic from the census source, then the real census was run on the same bytes.
   Command: `python3 tools-draft/w04-classify.py --repo <clone> --revision b9046016831237cd04d38da11ba76e50d5380c53
   --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh`. Output line:
   `census cross-check: exit 0, 21 W04 lines, identical to replica: True`.
   The census itself reports `file ok <tmp>/corpus/SOURCES.md` and exit 0, saved at
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ExecCensusW04/census-validate-b9046016.txt`.

3. **[obs] Classification counts over the 21 W04 pairs at `b9046016`:**

   | class | count |
   |---|---|
   | same-page re-registration with a different scope | 17 |
   | same scope duplicate | 0 |
   | different anchor on one URL | 4 |
   | total W04 pairs | 21 |

   The 0 in the middle row is not an artefact: the registry contains no two rows that share both a URL and a scope
   string, which is why the census prints no E04 and exits 0 (`same URL+same scope pairs (E04 shape): 0 []`).

4. **[obs] The 21 pairs, with the rule that decided each one.** R1 = the later row supersedes or restates the earlier
   row id; R2 = both rows cite the same quoted passage; R3 = both rows cite the same anchor location; R4 = both rows
   cite the same code identifiers; R5 = the later claim restates the earlier one by content containment; R6 = no shared
   evidence, so the rows are distinct anchors on one page.

   | earlier → later | class | rule | page |
   |---|---|---|---|
   | S034 → S038 | re-registration | R1 | man.archlinux.org/man/access.2 |
   | S028 → S041 | different anchor | R6 | man.archlinux.org/man/systemd.exec.5 |
   | S036 → S042 | re-registration | R1 | github.com/omacom/omarchy/issues/8047 |
   | S037 → S043 | re-registration | R1 | github.com/omacom/omarchy/issues/6629 |
   | S041 → S044 | re-registration | R3 | man.archlinux.org/man/systemd.exec.5 |
   | S044 → S046 | re-registration | R2 | man.archlinux.org/man/systemd.exec.5 |
   | S048 → S049 | different anchor | R6 | man.archlinux.org/man/pacman.8 |
   | S054 → S058 | re-registration | R1 | gitlab.archlinux.org/…/mkinitcpio/-/raw/v42.2/init |
   | S077 → S082 | different anchor | R6 | git-scm.com/docs/git-rev-parse/2.56.0 |
   | S001 → S087 | re-registration | R3 | archlinux.org/news |
   | S049 → S089 | re-registration | R2 | man.archlinux.org/man/pacman.8 |
   | S089 → S090 | different anchor | R6 | man.archlinux.org/man/pacman.8 |
   | S010 → S092 | re-registration | R3 | wiki.archlinux.org/title/System_maintenance?oldid=885170 |
   | S057 → S095 | re-registration | R5 | gitlab.archlinux.org/…/mkinitcpio/-/merge_requests/482 |
   | S021 → S098 | re-registration | R4 | gitlab.com/Zesko/limine-entry-tool/…/btrfs-overlayfs |
   | S088 → S105 | re-registration | R1 | archlinux.org/news/update-to-ca-certificates-mozilla-31311-1-… |
   | S089 → S106 | re-registration | R1 | man.archlinux.org/man/pacman.8 |
   | S090 → S107 | re-registration | R1 | man.archlinux.org/man/pacman.8 |
   | S093 → S108 | re-registration | R1 | wiki.archlinux.org/title/Downgrading_packages?oldid=887421 |
   | S094 → S109 | re-registration | R1 | gitlab.archlinux.org/…/mkinitcpio/-/raw/v42.2/functions |
   | S097 → S111 | re-registration | R1 | gitlab.archlinux.org/…/plymouth/-/raw/26.134.222-3/plymouth.initcpio_hook |

   The four distinct-anchor pairs are the ones a reviewer can check by eye: `systemd.exec(5)` for
   `CapabilityBoundingSet=` versus the path-view sections, `pacman(8)` for `-p, --print` versus `-Q`/`-u`/`--needed`,
   `pacman(8)` for `-Qu` versus the `-Sy`/`-Scc` sync options, and `git rev-parse(2.56.0)` for `--disambiguate`
   versus `--verify ^{type}`.

5. **[obs] The inflation window is round 24, and it matches the verifier's independent count.** The same script over
   eight revisions (`w04-classify-revision-trajectory.txt`) gives:

   | revision | re-registration | same scope | different anchor | total W04 |
   |---|---|---|---|---|
   | `f169b3b` (round-23 close) | 6 | 0 | 3 | 9 |
   | `674891d`, `10b45f0` (round-24 declare) | 6 | 0 | 3 | 9 |
   | `22fd164` (round-24 wave-1 landing) | 11 | 0 | 4 | 15 |
   | `44e9542`, `333e8fd`, `f923750`, `b904601` | 17 | 0 | 4 | 21 |

   All 12 new pairs have their later row opened 2026-10-22, and exactly 6 of them are explicit supersession
   re-registrations: S105 supersedes S088, S106 supersedes S089, S107 supersedes S090, S108 supersedes S093, S109
   supersedes S094, S111 supersedes S097. That is the "six same-page re-registrations" the round-24 verifier counted
   (`corpus/lessons/round-24-verifier-spotcheck.md:102`), reproduced independently here. Five further same-page
   re-registrations from the same day carry no supersession marker: S087 over S001, S089 over S049, S092 over S010,
   S095 over S057 and S098 over S021.

6. **[obs] The cause is the round-24 gate's opened-date rule, not the census.**
   `/fast/scratch/hyaku/tsukuroi-r25/ExecCensusW04/repo/tools/check-pause-gate.py:7-8` states the requirement that each
   premise cite "a row of corpus/SOURCES.md at the revision whose `opened` cell contains the round date 2026-10-22",
   and `tools/check-pause-gate.py:153-154` enforces it with the finding `source-not-opened:<id>`. A page that is
   already registered therefore cannot be re-read under the existing row, because that row's `opened` cell still holds
   the earlier date; the page has to be registered again under a new id, and the census then warns W04. The warning is
   the symptom of the gate's rule, and the census exit stays 0, so the inflation was silent.

7. **[obs] The round-25 declaration already contains the repair for routed defect 5.**
   `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md:797` requires, for every C2 row, "at least one source
   that is a `mined` SOURCES row whose used-by names the entry and that was either opened 2026-10-22 **or had its
   `recheck` updated in place this round with the change logged old → new in `corpus/lessons/round-25.md`** (this
   answers routed defect 5)". The in-place branch is therefore already sanctioned by the declaration, and no new
   tooling decision is needed to use it.

8. **[obs] The pages the round-25 memory-pressure rows need are not yet in the registry, so new rows for them are
   safe.** At `b9046016`, `corpus/SOURCES.md` contains no row for the kernel pressure-stall documentation, no row for
   the systemd-oomd man page, no row for `proc-vmstat(5)` and no row for the cgroup v2 pressure section; the only
   `docs.kernel.org` row is S063 (zswap administrator guide) and the only pressure-adjacent systemd row is S070
   (`systemd.service(5)`, freedesktop URL). [inf] A row for each of those pages adds no W04, because no earlier row
   uses that URL.

9. **[obs] The verdict is stable across the classifier's one tunable constant.** Sweeping the content-containment
   threshold from 0.20 to 0.50 (`w04-classify-threshold-sweep.txt`) moves the counts only between 16 and 18
   re-registrations, 3 and 5 distinct-anchor pairs, and 0 same-scope duplicates at every setting. The single pair that
   flips is S077 → S082 (`git rev-parse`), whose containment is 0.333; at a threshold of 0.33 or lower it becomes a
   re-registration. [inf] That pair reads as a distinct-anchor use to a human reviewer, so the default 0.35 is kept.

10. **[unk] The pairing of a W04 warning to one earlier row is a heuristic, not a census fact.** The census names only
    the later row and the URL; when one URL carries several rows (for example `pacman(8)` with six rows) the
    counterpart is chosen by an explicit score (supersession reference 6, any id reference 3, shared quoted passage 3,
    shared identifiers up to 3, content containment 2, scope containment 1, ties broken by file order). For the 21
    warnings at `b9046016` the chosen counterpart is also the row the registry itself points at, in every case where
    the later row names an earlier row id.

## Recommendation for the round-25 rows

1. **One registry row per URL.** MP4 (`ManagedOOMMemoryPressure=`/`ManagedOOMSwap=` semantics) and MP5 (the systemd-oomd
   default limits for systemd 262) are both read from the same systemd-oomd man page. Two rows for that one page
   would produce a W04 on the second row, because their scope strings differ. Register the page once, with a scope
   that names both the option semantics and the default limits and with both anchors in the anchor cell, then cite that
   single id from both the MP4 and the MP5 row of the knowledge entry. [obs] The precedent permits this: the round-24
   gate only requires the source ids inside one premise to be distinct (`tools/check-pause-gate.py:147-149`), it does
   not require distinct ids across premises.

2. **Do not mint a row for a page that is already registered; update that row in place.** Keep the existing id, update
   its `recheck` cell in place, log the old value and the new value in `corpus/lessons/round-25.md`, and cite the
   existing id from the new entry. This is the branch the declaration already allows (finding 7), it produces no new
   registry row and therefore no new W04, and it keeps the row count and the W04 count at 114 and 21 instead of letting
   them grow. [obs] Rows S105, S106, S107, S108, S109 and S111 are exactly the six rows that this rule would have
   replaced by in-place updates of S088, S089, S090, S093, S094 and S097.

3. **Keep `opened` as the first-access date and put the re-read date in prose.** The `opened` cell is the first
   access; the re-read belongs in the anchor or teaches text (for example "re-read 2026-10-22") together with the
   old → new `recheck` log line in the lesson. [obs] The census' overdue mode computes the due date from `opened` for
   `Nd` cadences (`scripts/sources-census.sh:675-683`), so an in-place update that sets a fresh cadence or an ISO
   date keeps the row off the overdue list without touching `opened`.

4. **Implement the two-branch rule in the new round-25 checker.** The gate that must exist for C2,
   `tools/check-memory-pressure.py`, has to accept a source row that was either opened 2026-10-22 or had its `recheck`
   updated in place this round with the change logged in `corpus/lessons/round-25.md`. [inf] If it copies the
   `source-not-opened` rule of `tools/check-pause-gate.py:153-154`, the round will be pushed back into minting rows for
   pages it has already opened, and the inflation repeats with a new id range.

5. **Never repeat a scope string to silence W04.** A row with the same URL and the same scope as an existing non-rejected
   row is an E04 finding and sets the census exit code to 1, unless its `teaches` carries the literal
   `supersedes S###` marker, which in turn does not silence W04 in any case (finding 1). [inf] Consolidate the claims
   into one row instead.

6. **[inf] Expected outcome for round 25.** If the C2 entry registers one row per new page (the kernel pressure-stall
   documentation, the systemd-oomd man page, and `proc-vmstat(5)` if that page is used for MP6) and updates any
   already-registered page in place, the registry would carry 114 plus the new rows and the census would report the
   same 21 W04 warnings, all of them pre-existing. The number of new W04 warnings would be zero.

## Reproducing this

```sh
cd /fast/scratch/hyaku/tsukuroi-r25/ExecCensusW04/repo
python3 tools-draft/w04-classify.py \
  --repo /fast/scratch/hyaku/tsukuroi-r25/ExecCensusW04/repo \
  --revision b9046016831237cd04d38da11ba76e50d5380c53 \
  --census /home/vgpnk/Projects/shokunin/scripts/sources-census.sh --verbose
```

Artifacts (all under the lane's seat directory
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ExecCensusW04/`):

| file | sha256 |
|---|---|
| `w04-classify.py` | `a8b945c329dfe33e5ab39bfb29530ccee4e9bb05baab7ed6cfe6c08c148de4af` |
| `w04-classify-b9046016.txt` | `0e2a2755646aa5dd06720ebdd178f2a34d5904cbbc1cfcb72803a80683dd3fad` |
| `w04-classify-b9046016.json` | `f7d22f7d92cb7ed09ba14cf2713d6e8019f4474b9c3f1ddb473c1c56f5948841` |
| `w04-classify-threshold-sweep.txt` | `fcfbd228fad6a0fdd038c1f027096fb2ab2114e5af2124e6ab8ed31e3f97a286` |
| `w04-classify-revision-trajectory.txt` | `254f6ab5e1c866e91e4fbc183897de77a80ff40d7d6d2abcd790c41f7b995217` |
| `census-validate-b9046016.txt` | `4c88eb8570336f01c3ba47353e333bf465726a56449cc55675665e46b6327700` |

The script itself lives in the seat's own clone at
`/fast/scratch/hyaku/tsukuroi-r25/ExecCensusW04/repo/tools-draft/w04-classify.py` (same sha256 as the copy above). It
is read-only: it reads `corpus/SOURCES.md` with `git show`, and when `--census` is given it writes the extracted file
into a temporary directory that it removes again.

## Safety note

[obs] No push was performed by this seat and no write command was aimed at
`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`. The git commands used against the clone are `show`, `log`,
`diff --stat`, `rev-parse`, `remote -v` (all read-only) and one `git fetch origin`, which read from the lane and wrote
only the clone's own `FETCH_HEAD` and remote-tracking refs; the lane's reflog shows only the integrator's "export from
jj" entries and its `refs/heads/master` stands at the L1's own commit `0cd9b28`. The clone's push URL is
`/nonexistent/no-push-to-lane` (`git config --get-regexp '^remote\.'` in the clone), so a push from this seat cannot
reach the lane. No production lane file was edited; the lane received only this report and the seat directory.

Scope: read=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/SCORECARD.md (round-25 declaration), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-24-verifier-spotcheck.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md at b9046016 (114 rows), /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-pause-gate.py, the same repository at seven further revisions for the W04 trajectory; wrote=/fast/scratch/hyaku/tsukuroi-r25/ExecCensusW04/repo/tools-draft/w04-classify.py and /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-25/w1/ExecCensusW04.md plus the seat directory files w04-classify.py, w04-classify-b9046016.txt, w04-classify-b9046016.json, w04-classify-threshold-sweep.txt, w04-classify-revision-trajectory.txt, census-validate-b9046016.txt; executed=python3 tools-draft/w04-classify.py (read-only, eight revisions, threshold sweep), bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-22 --file <temp copy of corpus/SOURCES.md at b9046016> (exit 0, 21 W04 lines), git show/log/diff/remote -v and one git fetch origin in the seat clone (no push, no write into the lane), plus a re-measure at the current lane tip 0cd9b28 (same 21 W04, same 17/0/4 split)
Model: opencode-go/minimax-m3.1-flash-free (route name exposed by the harness; no finer identity exposed to this seat)
Installs: none
