# ScribeSources — SOURCES.md audit of rows S331 and S332 (round 81, wave w1)

Lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin. Date of observation: 2026-11-04.
Contract: /home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md, section "SOURCES.md — where a shokunin learns" (contract v1) and "Additional corpus rules".
Repo state: HEAD e8e5d5b3 (detached). S331 and S332 are uncommitted working-tree additions (`git diff --stat corpus/SOURCES.md` → 2 insertions). HEAD's maximum id is S330 (`git show HEAD:corpus/SOURCES.md | awk ... | sort | tail -3` → S328, S329, S330).
Mutations: none. No git/jj mutation, no service action, no write outside this seat directory and the binding report. Read-only `journalctl` and `curl` GET were used.

## 1. Census (contract commands, run from lane root)

Raw outputs (also in `census.txt` beside this file):

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
332
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
```

Contract histograms and sweeps (2026-11-04):

```
tier histogram     A=315 B=6 C=11
status histogram   mined=294 queued=5 rejected=33
duplicate ids      (empty)
enum violations    (empty)
mined used-by missing (empty)
```

Id sequence: `awk` over the id column gives S001…S332 with no gap; last id S332; 332 registry rows.

Maintained CLI, read-only (`kimi-shokunin/scripts/sources-census.sh`, invoked with absolute `--file`):

```
$ sources-census.sh validate --file <lane>/corpus/SOURCES.md --today 2026-11-04   -> rc=0
  output: 53 lines = 1 "ok" + 52 "W04" (same-URL-across-scopes warnings)
  E01..E12 codes: 0 occurrences
  lines naming S331 or S332: none
$ sources-census.sh overdue --file <lane>/corpus/SOURCES.md --today 2026-11-04   -> rc=0
  file	cadence	S331 recheck=on-release opened=2026-11-04
  file	cadence	S332 recheck=30d opened=2026-11-04
  overdue lines naming S331/S332: none
```

Hand arithmetic: S332 opened 2026-11-04 + 30d = 2026-12-04; not overdue on 2026-11-04.

## 2. Source and host reproduction

S331 source reproduction (independent of the lane's pinned copy):

```
$ curl -sS -o /tmp/mount-v262.xml -w 'http=%{http_code} size=%{size_download}\n' https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.mount.xml
http=200 size=37234
$ sha256sum <fetched>
afbf3be663b139422b38217cd17083a96fa08507a1a3e58a844cbb2f67652394
```

This equals S331's raw SHA256 and `.ufo/waves/round-81/before/src/SHA256SUMS`. The fetched copy is kept as `mount-v262.fetched.xml` (sha256 above). The `opened` field 2026-11-04 is consistent with this fetch.

S332 host-state claims, read-only:

```
$ uptime -s ; who -b
2026-11-02 12:07:17 ; system boot 2026-11-02 12:07
$ find /run/systemd/generator -printf '%T+ %p\n'   (sorted)
2026-11-04+17:34:49.335... /run/systemd/generator/-.mount   (all generator units share this mtime)
$ journalctl --since '2026-11-04 17:34:30' --until '2026-11-04 17:35:10'
Nov 04 17:34:49 ... sudo[3411313]: vgpnk : ... COMMAND=/usr/bin/systemctl enable --now anydesk.service
Nov 04 17:34:49 ... systemd[1]: Reload requested from client PID 3411315 ('systemctl') (unit user@1000.service)...
Nov 04 17:34:49 ... systemd[1]: Reloading finished in 85 ms.
$ awk '$1!~/^#/ && NF>=4 && $3!="swap" && $3!="tmpfs" && $1!=""' /etc/fstab   (count)
local mounts=7 nofail=2 required=5   (nofail: /tmp, /fast; required: /, /home, /var/cache/pacman/pkg, /var/log, /boot)
$ awk 'NR>=141 && NR<=145 && /\.mount$/' .ufo/waves/round-81/before/host/generator.txt | wc -l
5
$ grep -n '^Before=local-fs.target$' .ufo/waves/round-81/before/host/generator.txt
9,24,55,70,85,100      (six units; fast.mount has none)
```

Commit facts for the capture file:

```
$ git log -1 --format='%h author=%ad committer=%cd' --date=iso 80237118
80237118 author=2026-11-04 17:50:37 -0300 committer=2026-11-04 18:01:19 -0300
$ git show 80237118:.ufo/waves/round-81/before/host/generator.txt | head -1
# live generator capture, round 81, 2026-11-04T17:54:25-03:00, read-only
$ git status --porcelain -- .ufo/waves/round-81/before/host/generator.txt   (empty: unmodified)
```

## 3. Per-column grade

Columns: id · source · kind · tier · scope · anchor · teaches · status · opened · recheck · used-by.

| column | S331 | S332 |
|---|---|---|
| id | pass: S331, unique, next after S330 | pass: S332, unique |
| source | pass: title + canonical raw URL | pass: repo path (tracked file, commit 80237118) |
| kind | pass: `docs` in enum | pass: `own-work` in enum |
| tier | pass: A, upstream man page for its scope | pass by shape; see tier note T1 |
| scope | pass (fstab-only section wording matches lines 182–184) | **FAIL** V-S332-1: "produced at boot on 2026-11-04" contradicted |
| anchor | pass in kind (section + lines + v262 + SHA256); defects V-S331-2, V-S331-3 | pass in kind (section + lines); revision weak: V-S332-4 |
| teaches | defects V-S331-1 (overgeneralised "only"), V-S331-4 (compound) | **FAIL** V-S332-2 (count "four" should be five); defect V-S332-3 (unqualified "only") |
| status | pass: `mined`, used-by resolves | pass: `mined`, used-by resolves |
| opened | pass: 2026-11-04, consistent with today's fetch and capture | pass: 2026-11-04, capture header 17:54:25 same day |
| recheck | pass: `on-release` is a symbolic cadence | pass: `30d` |
| used-by | pass: corpus/knowledge/mount-unit-fstab-plane-r81.md exists on disk | pass: same path; path is untracked (not yet committed) |

Tier note T1 (question, no verdict): contract tier A for own-work means "the lane's own re-runnable gate output". S332 is a one-shot capture, not re-runnable gate output. Precedent S051–S069 grades captures A. Recorded as an open contract question, not a violation.

## 4. Violations (every one, with its column)

Severity: H = contradicts a fact or breaks a contract column; M = overstates a grounded claim; L = precision or anchor-range defect.

**S332**

- **V-S332-1 [scope] H.** Scope says the host "produced" the generated mount units "at boot on 2026-11-04". Observed: boot was 2026-11-02 12:07:17; the generator output was regenerated 2026-11-04 17:34:49 after `sudo systemctl enable --now anydesk.service` triggered a reload (journal lines above). The capture was taken at 17:54:25, after that reload. Fix: scope should say "produced by the 17:34:49 daemon-reload on 2026-11-04 and read at 17:54:25"; the phrase "at boot" must go.
- **V-S332-2 [teaches] H.** "the four required mounts land in .requires". Observed: `.requires` holds five units (generator.txt:141–145) and `/etc/fstab` has five required local mounts (lines 6, 9, 12, 15, 18). Fix: "five required mounts". The row carries no count command, which the CORPUS rule "A count carries its command" requires.
- **V-S332-3 [teaches] M.** "only the /tmp entry carries the Before=local-fs.target its x-systemd.before= option asked for". True inside the nofail pair (fast vs tmp). Unqualified, it is false: six units carry `Before=local-fs.target` (generator.txt:9, 24, 55, 70, 85, 100). Fix: "of the two nofail xfs mounts, only /tmp carries …".
- **V-S332-4 [anchor] L.** Revision is a timestamp inside the file ("capture header 2026-11-04T17:54:25-03:00"). The contract asks for version, commit or publication date. The file is tracked and unmodified since commit 80237118. Fix: append the commit (80237118). Provenance note, not a defect: author date 17:50:37 precedes the header time 17:54:25; committer date 18:01:19 follows it.

**S331**

- **V-S331-1 [teaches] M.** "the x-systemd.* dependency options attach to the created mount unit only". The source sentence "always applies to the created mount unit only" appears at systemd.mount.xml:212 (x-systemd.requires/wants) and :248 (x-systemd.before/after). The x-systemd.wanted-by/required-by entry (:256–267) has no such sentence, so the generalisation to "the x-systemd.* dependency options" is wider than its grounding. Fix: scope the clause to the two quoted entries, or drop "x-systemd.*".
- **V-S331-2 [anchor] L.** Anchor "nofail :498-503" omits line 504 ("ordered before these target units"), which grounds the teaches clause "drops its ordering before the target". Fix: anchor 498–505 (or 502–504).
- **V-S331-3 [anchor] L.** Anchor "fstab options :182-370" ends before the end of the x-systemd.mount-timeout entry (:355–375), which the scope column lists. Fix: extend the range to 375.
- **V-S331-4 [teaches] L.** Teaches has three clauses (nofail, noauto, x-systemd.*). The contract asks for one grounded benefit. Fix: either split into rows or keep the nofail clause only.

**Both rows (gate, rule 1)**

- **V-R1 [gate, not a column] H, blocking.** Rule 1 requires the round lesson's `## Gate` to record, for each new row, the URL, access date and a ≤25-word quote with location. `corpus/lessons/round-81.md` does not exist (`ls corpus/lessons/` ends at round-80 files). The ScribeLesson seat drafts it outside the production tree. Status: unmet until that lesson lands.

**Adjacent, not registry columns (knowledge entry that both rows cite)**

- **V-K1 corpus/knowledge/mount-unit-fstab-plane-r81.md:30** "/etc/fstab carries six local file systems; four are required and two are not". Observed: seven local mounts, five required, two nofail (see §2).
- **V-K2 same file, line 43** "(S332 :35-47 vs :95-107)" for tmp.mount vs fast.mount. In the capture tmp.mount is :64–78; :95–107 is var-log.mount.
- **V-K3 same file, Limits** "one boot's generator output" and S332 scope "at boot": the boot was 2026-11-02; the output is from the 2026-11-04 17:34 reload.
- **V-K4 same file, header `source:` line** cites S331 and S332 by id and name but not the URL or the S332 path; the additional rule asks for the URL alongside the S### row.

These are the knowledge owner's to correct. Per the contract, corrections are new entries, not rewrites; they are not edited here.

## 5. Id provenance

- `git log --all -S'| S331 |' -- corpus/SOURCES.md` returns seven commits, and for each the S331+S332 row bytes hash identically (`sha256 159bf590fd5fd107…`). No commit holds a different S331 or S332. Not reused in git history.
- Staged package outside this lane: `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` lines 138–139 assign S331 and S332 to a round-14 host-journal capture (different material). Round-49 and round-64 receipts also cite those ids for staged material. No live collision today, but any append of that package would collide. Risk noted for its owner; not a violation in this registry.

## 6. Verdict (rows)

- S331: shape and enum conform; used-by resolves; source reproduced today. Three column-level defects (teaches overgeneralised; two anchor-range defects) and a missing gate record (V-R1). Conforms on structure; not yet admissible until V-S331-1 and V-R1 are cleared.
- S332: does not conform. Scope is contradicted by host evidence (V-S332-1); teaches carries a wrong count (V-S332-2). Not admissible as written.

## 7. Checks run and not run

Run: census grep, malformed awk, tier/status/dup/enum/used-by sweeps, maintained `validate` and `overdue`, source GET + sha, mount.xml line ranges (sed/awk), generator.txt ranges, /etc/fstab count, systemd boot time, journal window, git log/show/status on the two rows and the capture file, staged-package grep.
Not run: any rerun of the lane's `count-mount-rows-r81.py` (owned by the executor seats); any `systemctl` state query beyond `uptime`/`who`.

## 8. Tools

No tool installed or upgraded. Used: gawk, awk, jq, curl, journalctl, git, sha256sum (already present). pacman paused host-wide; none attempted.
