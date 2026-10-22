# ScribeMarkersStorage — round 29 wave 1 (C1 markers O09 to O12)

Verdict: done — four correction objects for `corpus/knowledge/storage-health-r26.json` rows SH1, SH3, SH4
and SH5 are drafted and pass the declared counter's M1 to M6 at a sandbox commit over the pinned base;
inserted in the lane they would move `marked` from 0 to 4 of 12, with O01 to O08 still unmarked.

1. Anchors are present and unmarked at the revision under attack. At `81a061a67466c5e1be812814a895a4b5ed89b4ff`
   each frozen anchor is a verbatim substring of its named row field (`git show 81a061a:corpus/knowledge/storage-health-r26.json | grep -cF`
   → 1 for each of the four), and the entry has no `corrections_r29` key (`grep -c corrections_r29` → 0).
   The declared command in the seat clone (`python3 tools/check-owed-statements-r29.py --revision 81a061a... --lane .`)
   printed `{"items": 12, "marked": 0, "unmarked": ["O01",...,"O12"]}`, exit 1. [obs]

2. The draft passes the counter's rules in the sandbox. Applied verbatim to a clone at the base plus the two
   used-by cells and committed there as `c4e4173f5db7671cbf2cc4a85ec356e69bfb87c1`, the counter reports
   `marked` 4 with O09 `corrected` (basis `corpus/knowledge/storage-health-r26.md:128`, `S133`), O10
   `corrected` (`:135`), O11 `qualified` (`:133`) and O12 `qualified` (`:129`, `S134`), `basis.unresolved`
   empty for all four, unmarked `["O01".."O08"]`, exit 1. `git diff --stat 81a061a HEAD` there:
   `corpus/SOURCES.md` 4 ++--, `corpus/knowledge/storage-health-r26.json` 6 ++++++ (8 insertions, 2 deletions).
   The exit 1 is expected: the counter returns 0 only at 12 of 12, so this four-item draft cannot satisfy the
   claim's exit-0 half alone; O01 to O08 are other seats' work. [obs]

3. Verdicts follow the Markdown corrections line by line, all four lines checked at the pinned revision
   (`git show 81a061a:corpus/knowledge/storage-health-r26.md | sed -n '128p;129p;133p;135p'`; the file is 135
   lines, so `:135` is its last line). O09 `corrected` at md:128 (only write, read and flush have shorter
   sysfs names; `corruption_errs` and `generation_errs` are identical in both views, and the "at once"
   wording is the comment's intent over five unlocked reads). O10 `corrected` at md:135 ("stale for systemd
   262"; the NOCOW flag comes from the tmpfiles snippet `journal-nocow.conf`, and systemd clears or drops it
   when a journal file is archived). O11 `qualified` at md:133 (narrowed to the status file and the six
   retained boots, older or recording-disabled scrubs not excluded). O12 `qualified` at md:129 (the
   overall-health line exists only after a successful SMART log read, S134 lines 772-778, 786-788, 833-836).

4. O10 deliberately carries no `S###` id. md:135 records its systemd v262 NEWS and `src/shared/journal-file-util.c`
   read as "not registered this round", so no registry row backs it; citing S136 or S137 (systemd-oomd pages)
   would be a wrong-provenance claim. Its basis is the path reference only, which M6 accepts. [obs]

5. Used-by proposal (needed only for the two S ids the draft cites). `corpus/SOURCES.md:139` (S133) and
   `:140` (S134) carry `corpus/knowledge/storage-health-r26.md` as cell 11; propose appending
   `, corpus/knowledge/storage-health-r26.json` to each, because the JSON rows cite those ids
   (`rows[SH1].sources` = S128, S133, S132 with `quotes[3].source` = S133; `rows[SH5].sources` = S134, S135
   with `quotes[0..2].source` = S134) and because the lane's paired entries list both companions (S120 to
   S127 name `memory-pressure-r25.md, memory-pressure-r25.json`). `tools/check-storage-health.py:651` tests
   `ENTRY_STEM_RE.search(used_by)`, and that predicate is True for the old and the new cell text
   (evaluated directly), so R3 does not regress. The markers do not depend on it: at scratch commit
   `6a331d943889bba7d4e85fbc2a0fd5d95e3c1b69` (markers, old used-by cells) O09 and O12 are still `ok`, with
   `S133` and `S134` under `basis.unresolved`. [obs]

6. The storage-health counter could not be run end to end on the draft. `python3 tools/check-storage-health.py
   --revision c4e4173f... --repo .` exits 2 with `{"status": "CANNOT_EVALUATE", "findings": [{"id":
   "E-REVISION-NOT-PUSHED", "site": "refs/remotes/origin/master"}]}` because the tool binds the measured
   revision to a pushed ref, and pushing is outside this seat's bounds. Its JSON loader path was exercised
   directly instead (its duplicate-key `object_pairs_hook`): `schema` `tsukuroi-storage-health-r26-v1`, six
   rows SH1 to SH6, four `corrections_r29` objects. [obs] No end-to-end run of that tool is claimed.

7. Formatting hazard for the integrator: the entry is hand-formatted one object per line at 2-space indent,
   and `json.dumps(json.load(f), indent=1)` does not reproduce it (round-trip equality False), so the literal
   block in `draft.md` must be inserted, not a re-dump. The exact edit is the last two lines
   ` ]` / `}` becoming ` ],` plus the new ` "corrections_r29": [ ... ]` block (`draft.md` section "Exact
   text to insert"). [obs]

8. Limits. O09's `now` covers both clauses of md:128; O10's mechanism was not re-read from the systemd
   source this round (it rests on the wave-2 read recorded at md:135); O11 rests on the live read recorded
   at md:133, not on a registered source; no fresh source was opened and S148 to S151 were not used (they
   belong to O01 to O04 and O08). [inf] Every anchor check and correction line was read at
   `81a061a`, not at the working-tree tip `3c94d730`, which differs only by the receipt commits. [obs]

9. Containment. No lane file outside the seat directory was written and the lane working tree shows only
   `.ufo/waves/round-29/w1/` untracked; all git writes (clone checkout, two sandbox commits, one branch
   reset) happened in `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkersStorage/`, with
   `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE` on every call, and the lane was only read with `git show`,
   `git rev-parse` and `git status`. [obs]

Artifacts:
- `.ufo/waves/round-29/w1/ScribeMarkersStorage/draft.md` — exact insertion block, used-by changes, verdict rationale, validation record
  (sha256 `d6581b959d3a1c69619ec05a8b24fe399c2b51bfecc28202544813371f39482d`).
- `.ufo/waves/round-29/w1/ScribeMarkersStorage/corrections_r29.json` — the four objects alone as a JSON array
  (sha256 `a6c01c49816e0d1ee66a2fcb5cfa68622c222861a49293a5c6a3bc4dc3e91502`).
- `.ufo/waves/round-29/w1/ScribeMarkersStorage/evidence.md` — command outputs, anchor counts, line text, commit ids, hashes
  (sha256 `68860c68b7e4f635c220c541a533352826ffb75cc3c2a3ef468e6a17e2a769fa`).
- Sandbox: `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkersStorage/repo` at `c4e4173f` (draft) and
  `81a061a` (base); counter outputs `sms_before.jsonl`, `sms_r2.jsonl`, `sms_r4.jsonl` in
  `/fast/scratch/hyaku/tsukuroi-r29/ScribeMarkersStorage/`.

Scope: read=corpus/knowledge/storage-health-r26.json and .md at 81a061a, corpus/SOURCES.md rows S120-S139, tools/check-owed-statements-r29.py, tools/check-storage-health.py (R3/parse paths), SCORECARD.md round-29 declaration, .ufo/waves/round-27/w1/RevRoutedDefects.md:20; wrote=.ufo/waves/round-29/w1/ScribeMarkersStorage/draft.md, .ufo/waves/round-29/w1/ScribeMarkersStorage/corrections_r29.json, .ufo/waves/round-29/w1/ScribeMarkersStorage/evidence.md, .ufo/waves/round-29/w1/ScribeMarkersStorage.md; executed=env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git clone --no-local, git checkout, git show, git rev-parse, git status, git add, git commit, git diff --stat, git checkout -B, python3 tools/check-owed-statements-r29.py (revisions 81a061a, 6a331d94, b13b1f7, c4e4173f), python3 tools/check-storage-health.py (E-REVISION-NOT-PUSHED), grep -cF, sha256sum
Model: opencode-go/deepseek-v4.1-flash
Installs: none
