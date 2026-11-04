# ScribeSources — binding report (round 81, wave w1)

Seat: ScribeSources (scribe, leaf). Judged on: depth, operability, freshness.
Scope: registry audit of corpus/SOURCES.md rows S331 and S332 against CORPUS.md "SOURCES.md — where a shokunin learns".
Full evidence: `.ufo/waves/round-81/w1/ScribeSources/audit.md` (commands and observed output). Receipts copied beside it: `census.txt`, `overdue.tsv`, `mount-v262.fetched.xml`.

## Verdict

- **S331 (systemd.mount(5), docs, A):** structure and enum conform; used-by resolves; upstream source reproduced today (sha256 afbf3be6…, HTTP 200). Column defects remain: teaches overgeneralises "the x-systemd.* dependency options attach … only" (V-S331-1); anchor ranges omit line 504 (V-S331-2) and extend short of 375 (V-S331-3); teaches is compound (V-S331-4).
- **S332 (own-work capture, A):** does not conform. Scope says the units were produced "at boot on 2026-11-04"; boot was 2026-11-02, and the output was regenerated 17:34:49 on 2026-11-04 by `sudo systemctl enable --now anydesk.service` (V-S332-1). Teaches says "four required mounts"; the count is five (V-S332-2). Teaches' "only the /tmp entry" is unqualified (V-S332-3). Anchor revision is a timestamp, not a commit (V-S332-4).
- **Rule 1 gate, both rows (blocking):** `corpus/lessons/round-81.md` does not exist, so no `## Gate` records URL, access date and ≤25-word quote for either row (V-R1).

## Census (run, pasted in audit.md §1)

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
332
$ awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
```

Also clean: duplicate ids (none), enum violations (none), mined used-by missing (none). Maintained `validate`: rc=0, no E-codes, no line for S331/S332. Maintained `overdue`: no overdue line; S332 recheck 30d not due until 2026-12-04.

## Violations by column

| id | column | severity | finding |
|---|---|---|---|
| S332 | scope | H | "produced at boot on 2026-11-04" contradicted (boot 2026-11-02 12:07:17; regeneration 17:34:49 from a systemctl reload) |
| S332 | teaches | H | "four required mounts" → five (generator.txt:141–145; /etc/fstab) |
| S332 | teaches | M | "only the /tmp entry carries Before=local-fs.target" is true only within the nofail pair (six units carry it: generator.txt:9,24,55,70,85,100) |
| S332 | anchor | L | revision is a timestamp; add commit 80237118 |
| S331 | teaches | M | "x-systemd.* … only" generalises two entries (systemd.mount.xml:212, :248); wanted-by/required-by has no such sentence |
| S331 | anchor | L | "nofail :498-503" omits line 504 that grounds "drops its ordering" |
| S331 | anchor | L | "fstab options :182-370" stops before mount-timeout ends at :375 |
| S331 | teaches | L | compound teaches (three clauses) against "one grounded benefit" |
| both | gate (rule 1) | H, blocking | no round-81 lesson `## Gate` exists yet |

Adjacent defects in the knowledge entry both rows cite (`corpus/knowledge/mount-unit-fstab-plane-r81.md`, lane-owned, not edited): line 30 says "six local … four required"; line 43 gives tmp.mount's range as :95–107 (it is :64–78); Limits says "one boot's generator output"; the `source:` line lacks the URL.

## Provenance and freshness

- S331 `opened` 2026-11-04 is corroborated by a fetch today that matches the pinned digest.
- S331 anchors upstream v262; the host runs 262.1-1-arch. The knowledge entry's Limits already discloses this; no registry violation.
- S332 provenance: file tracked, unmodified since commit 80237118 (author 2026-11-04 17:50:37, committer 18:01:19). Author date precedes the file's own header time 17:54:25; committer date follows it. Not a contradiction.
- Id history: seven commits containing S331 each hold identical S331/S332 bytes (sha256 prefix 159bf590…). No reuse in git. Staged package at `/home/vgpnk/Projects/shokuknow/merge/tsukuroi/SOURCES.append.md` (lines 138–139) uses S331/S332 for a different round-14 capture; any append would collide. Risk for that package's owner, not a violation here.
- Tier question (no verdict): contract tier A means "re-runnable gate output"; S332 is a one-shot capture. Precedent S051–S069 grades captures A.

## Actions and state

- Production edits: none. Lane tree untouched. No git/jj mutation, no push, no commit. No writes to the fleet repo or any sibling lane.
- Writes: `.ufo/waves/round-81/w1/ScribeSources/audit.md`, `.ufo/waves/round-81/w1/ScribeSources/{census.txt,overdue.tsv,mount-v262.fetched.xml}`, and this report.
- Scratch: `${HYAKU_SCRATCH:-/fast/scratch/hyaku}/tsukuroi-r81/ScribeSources` created for working copies; receipts copied; scratch removed before yield (see next line).
- Host reads: `curl` GET of the upstream v262 XML (HTTP 200); `journalctl` 17:30–17:40 window; `uptime`, `who -b`; `stat`/`find` on /run/systemd/generator; read-only `systemctl`-free checks. Nothing started, stopped, reloaded or enabled.
- Temporary /tmp files from the audit (`/tmp/mount-v262.xml`, `/tmp/val*.tsv`) were removed.

## Tools

No install or upgrade. Existing gawk, awk, jq, curl, journalctl, git, sha256sum used. pacman paused; not invoked.

## Unknown / not checked

- Which actor ran the 17:34:49 reload beyond the journal's `sudo` entry (the entry names `vgpnk` and `systemctl enable --now anydesk.service`; no further causal claim made).
- Whether the lane's count instrument (`tools/count-mount-rows-r81.py`) passes on these rows; that belongs to the executor seats.
- Whether the knowledge entry's `source:` must also carry the URL under the additional rule; reported, not adjudicated.

## Checks the main agent should run

1. `sources-census.sh validate --file corpus/SOURCES.md --today 2026-11-04` (expect rc 0, no E-codes).
2. The contract census block above (expect 332, 0).
3. After the round-81 lesson lands: confirm its `## Gate` covers S331 and S332 with URL, access date and quote location (V-R1).
4. After S332 scope and teaches are corrected in a new commit: re-check the "four" → "five" and "at boot" phrases are gone.
