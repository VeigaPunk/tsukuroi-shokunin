VERDICT: supports

Item G-3. Three citation/notice/adjacency gates at `2e1c2a40c13dc52e155d89e72f3fdd560db7399a` and
`0eff65b21bb81195ee06c96a83afbd7a07e52eef`; IN-109 repin `2425 -> 2447` verified; census line pins re-scanned.
Receipts: `.ufo/waves/round-39/w1/GateCitations/` (12 gate outputs, 3 selftest outputs, `runs.tsv`,
`in-109-pin-check.txt`, `census-citation-scan.txt`). Scratch `/fast/scratch/hyaku/tsukuroi-r39/GateCitations`
(`TMPDIR` for every run) removed after the receipts were copied out.

## 1. Gate runs — all PASS, exit 0

Requested revisions plus two extra informative points (the repin commit and the current lane tip):

| revision | check-section-citations | check-appended-notices | check-adjacency-anchors |
|---|---|---|---|
| `0eff65b2` (base) | 0 PASS | 0 PASS | 0 PASS |
| `2e1c2a40` (assigned) | 0 PASS | 0 PASS | 0 PASS |
| `49cc53c7` (IN-109 repin) | 0 PASS | 0 PASS | 0 PASS |
| `394e1ba4` (lane tip) | 0 PASS | 0 PASS | 0 PASS |

(`.ufo/waves/round-39/w1/GateCitations/runs.tsv`; every stderr file is 0 bytes; each run names the bound
`branch_tip` `394e1ba4…` and its own `--revision`.)

Summaries verbatim (`.ufo/waves/round-39/w1/GateCitations/*.out`):

- at `0eff65b2`: `{"correction_count": 2, "findings": [], "status": "PASS"}` (section-citations);
  `{"distinct_paths": 17, "record_count": 97, "resolved_records": 97, "status": "PASS"}` (appended-notices);
  `{"counts": {"inbound_by_class": {"DRIFTED": 17, "RESOLVES": 96, "UNRESOLVABLE": 1}, "inbound_by_scope":
  {"historical": 89, "operative": 25}, "inbound_classified": 114, "inbound_total": 114,
  "live_object_checked": 10, "live_object_match": 10, "outbound_portable": 10, "outbound_total": 10},
  "findings": [], "status": "PASS"}` (adjacency).
- at `2e1c2a40`: byte-identical to the above except the `revision` field. So the boundary that moved
  (`2425 -> 2447`, `total_lines 3055 -> 3099`) changed **no** count and produced **no** finding.

Docstrings read before use: `check-section-citations.py` = narrow round-16 errata gate (two registry records
vs pinned headings/rows/quotes + a `db68e62…` byte prefix; read-only git objects, revision must be landed and
pushed); `check-appended-notices.py` = append-boundary verifier for the round-18 notice registry against
immutable blobs; `check-adjacency-anchors.py` = round-19 portable-anchor verifier (10 outbound live objects,
114 inbound classification, `found_line` must be an occurrence of `evidence_quote`,
`RESOLVES`/`DRIFTED` derived from `target_ranges` — `tools/check-adjacency-anchors.py:741-754`).

Selftests (`TMPDIR` in scratch, all rc=0): section-citations `PASS (68 cases, 68 passed, 0 failed)`,
appended-notices `PASS (47 cases, 47 passed, 0 failed)`, adjacency `PASS (25 cases, 25 passed, 0 failed)`.
Tool bytes: `check-section-citations.py` `149b9a21…`, `check-appended-notices.py` `e6f8bde2…`,
`check-adjacency-anchors.py` `a4f500ef…` (the last matches the round-32 receipt pin).

## 2. IN-109 repin — confirmed exactly

`.ufo/waves/round-39/w1/GateCitations/in-109-pin-check.txt` (machine record vs census bytes at each revision):

```
rev=0eff65b2… census_lines=3055 quote_at=[2425] registry_found_line=2425 class=DRIFTED ranges=[[915,970]] consistent=True
rev=6a08925d… census_lines=3055 quote_at=[2425] registry_found_line=2425 class=DRIFTED ranges=[[915,970]] consistent=True
rev=49cc53c7… census_lines=3099 quote_at=[2447] registry_found_line=2447 class=DRIFTED ranges=[[915,970]] consistent=True
rev=2e1c2a40… census_lines=3099 quote_at=[2447] registry_found_line=2447 class=DRIFTED ranges=[[915,970]] consistent=True
rev=394e1ba4… census_lines=3099 quote_at=[2447] registry_found_line=2447 class=DRIFTED ranges=[[915,970]] consistent=True
```

Quote = `check 'degraded: kernel ring class counts are evidence (D14/D15)' 1 DEGRADED`, exactly one hit per
revision. The repin landed in the same commit as the census change (`49cc53c7`, subject: "C1 storage arm
cross-checks the mount table …; IN-109 repinned"): registry `corpus/knowledge/adjacency-anchors-r19.json`
`found_line` 2425→2447 and the note's last sentence records it. Census insert is +44 lines, hunks
`-363 +5`, `-399 +1`, `-453 +1`, `-1895 +12`, `-2009 +2`, `-2139 +1`, `-2949 +22`; the quote sits after
+22 of them (2425→2447), so the repin arithmetic is right. `ranges [[915,970]]` unchanged, hence `DRIFTED`
stays the correct class at both revisions (the gate recomputes it).

## 3. Other census line pins — no machine pin is stale

- `corpus/knowledge/adjacency-anchors-r19.json` has **exactly one** inbound row whose `target_path` is
  `tools/tsukuroi-census.sh` (IN-109); no outbound row does. The machine pin surface for this file is that row.
- No tool hardcodes a census line: `git grep -n "tsukuroi-census.sh:[0-9]" 2e1c2a40 -- tools` → empty;
  `tools/score-storage-hidden-r39.py` reads census bytes by revision (`CENSUS = 'tools/tsukuroi-census.sh'`,
  line 53) with no line pin.
- The only `UNRESOLVABLE` inbound row is `IN-101 tools/_revision.py found_line 0` — unrelated to the census
  and unchanged at both revisions.

## 4. Stale census line pins found (reported, not edited — lane is read-only for this seat)

**4a. Newly shifted by the round-39 insert (were correct at base):** `corpus/lessons/round-38-verifier-spotcheck.md`
line 53 cites `tools/tsukuroi-census.sh:1855-1901 at tip; :453` and line 54 cites `sed -n '3028,3045p'`.
At base those were exact (`1855 = probe_storage_arm() {`, `453 = BTRFS_SYSFS=${TSUKUROI_BTRFS_SYSFS:-/sys/fs/btrfs}`,
`3034 = printf '%s\n' "$STORAGE_LINE"`, `3044 = printf 'TSUKUROI_CENSUS: …`); at `2e1c2a40` they are
`1862-1908`, `459`, `3072-3089`. Dated round-38 record, no gate reads it — attribution only.

**4b. Carried stale human-readable pin (already wrong at base; round 39 repinned only the JSON):**
`corpus/knowledge/adjacency-anchors-r19.md:204` `| … | 2277 |` and `:231` `| line 2277 |`. Census line 2277 is
`^PLANE packages: DEGRADED …` at base and a `blocked-lck` case at tip — the D14/D15 quote is at 2425/2447.
Same class the round-36 seat recorded (`ExecGateBaselines`), untouched by `49cc53c7`.

**4c. IN-109 `note` field carries three stale positional claims** (`adjacency-anchors-r19.json:2470`):
`range 915-970 now holds probe_drivers kernel-ring code` — that range is `probe_systemd()` (915-980;
`probe_drivers()` begins at 981); `Block comment now 2173-2178` — the round-5 block comment is at 2404
(base 2382); `D14/D15 case 2216` — at 2447 (base 2425). Only `found_line` has been maintained.

**4d. Already divergent at base (pre-existing, not caused by round 39; enumerated, not re-judged):**
`SCORECARD.md:48` (six `PLANE` emitters cited `2377-2382`; actual `3003-3008` at base, `3047-3052` at tip),
`corpus/knowledge/oom-event-plane.md:194` (`399-425`), `SKILL.md:296,600,1017,1204,1294,1368` (dated
round-5/7/9 ledgers), and the dated receipts `aur-drift-receipt-r9.md:199`, `census-closeout-receipt-r10.md:20,32,122`,
`journalctl-v262-field-filter-r36.md:66-78,84`, `kill-oom-boundary-r33.md:13-42`, `memory-arm-mutants-s8.md:14`, and `plans/round-10-record-draft.md:187`.
Full table with base/tip content: `.ufo/waves/round-39/w1/GateCitations/census-citation-scan.txt` (41 changed
citations across 11 tracked markdown files; 0 citations left dangling: no cite exceeds `len(census)` at either revision).

## 5. No-harm and limits

- Writes: only `.ufo/waves/round-39/w1/GateCitations/` (+ this report). No lane content, Git index/jj state,
  fleet repo, sibling lane, host, `/etc`, mount or service touched; no sudo, no package manager (pacman is
  paused host-wide; nothing installed). `git status --porcelain` after my runs shows only pre-existing
  ` M PROVINCE.md`, ` M SKILL.md` and the wave's untracked files — none mine.
- Those two working-tree edits (another seat's) are at `PROVINCE.md` line 224 (+14) and `SKILL.md` line 3204
  (+21), both **after** every registry `found_line` for those files (max 79 and 1968), so they cannot drift an
  adjacency pin; and all gate runs here are `--revision`-bound to git objects, not the worktree.
- Not done (stated, not passed): worktree-mode runs are impossible (`--revision`/`--selftest` are a required
  mutually-exclusive group); I did not run the rest of the lane gate set, did not run the live census, and did
  not judge C1/C2 counting claims (other seats). No TO row was judged, so the `TO<n>: holds|partly|fails` line
  rule does not apply to this report.

## 6. Proposed text (for the owner of the two files; nothing written by me)

`corpus/knowledge/adjacency-anchors-r19.md:204` — replace the `2277` cell with `2447`; `:231` — replace
`line 2277` with `line 2447`.

`corpus/knowledge/adjacency-anchors-r19.json` IN-109 `note` — replace the first sentence with:
`Block began at 915 at landing da95290; range 915-970 now holds probe_systemd (probe_drivers begins at 981).`
Then `Block comment now 2173-2178, D14/D15 case 2216` → `Block comment now 2404, D14/D15 case 2447`.
