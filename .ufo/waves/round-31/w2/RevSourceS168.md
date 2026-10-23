# RevSourceS168 — round 31 wave 2 (falsify) — source S168 review

Verdict: **holds** — S168 (btrfs-replace.rst, btrfs-progs v7.1) re-opened independently: the fetched bytes match the registry anchor sha256 and the committed snapshot; the lesson Gate row is exact; every registry cell is true at f3a5723a988bf1c2835985880e7a38d477462cd0, and teaches keeps every branch its quoted source states (QUALITY rule 66).

Sandbox: `/fast/scratch/hyaku/tsukuroi-r31/RevSourceS168/repo` cloned from the lane, checked out at f3a5723a988bf1c2835985880e7a38d477462cd0 (git rev-parse HEAD = f3a5723a988bf1c2835985880e7a38d477462cd0). All reads below are at that revision.

## Numbered findings

1. [obs] Fetch vs anchor vs committed snapshot — byte-identical. `curl -sL 'https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-replace.rst'` saved to `.ufo/waves/round-31/w2/RevSourceS168/btrfs-replace.rst.fetch` (4562 bytes); `sha256sum` = `da4bf595f072a96a309535c1022b0171a8657a4f207a3d3da73250886fd8bc9e`. The S168 registry row anchor (`corpus/SOURCES.md:262`) states the same hash, and the committed snapshot `.ufo/waves/round-31/w1/ScribeSrcReplace/btrfs-replace.rst` has the same hash. All three equal; the snapshot is the exact upstream v7.1 bytes.

2. [obs] Lesson Gate row (`corpus/lessons/round-31.md:15`): URL matches the row URL; date 2026-10-22; location `.ufo/waves/round-31/w1/ScribeSrcReplace/btrfs-replace.rst line 106, sha256 da4bf595f072a96a309535c1022b0171a8657a4f207a3d3da73250886fd8bc9e` matches the computed hash. Quote `"btrfs replace start 1 /dev/sdc /mnt/my-vault/"` is a verbatim substring of ONE line (snapshot line 106), 6 words (≤ 25); `sed -n '106p' <snapshot> | grep -cF 'btrfs replace start 1 /dev/sdc /mnt/my-vault/'` prints `1`.

3. [obs] Anchor peel: `git ls-remote https://github.com/kdave/btrfs-progs.git 'refs/tags/v7.1' 'refs/tags/v7.1^{}'` → tag object `0a919c7d6e389c07920675b7fad3f793b92aa78b`, peeled commit `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b`, which is exactly the anchor's "peeled commit 4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b" (GitHub API was rate-limited, so peel verified via ls-remote instead).

4. [obs] Registry row `corpus/SOURCES.md:262` cells:
   - kind `docs`: the source is upstream btrfs-progs documentation — true.
   - tier `A`: version-pinned upstream primary documentation (tag v7.1) — true.
   - scope: live source / unavailable source / `-r` read-error path / disconnected source / device-size condition / larger-target use — every item is present in the cited anchor ranges (see 5).
   - anchor ranges: lines 20-38 (start syntax, live and unavailable-source branches, removal, source identification, size and resize conditions), 54-57 (`-r` mirror/read-error behavior), 101-119 (larger-drive example and resize). All verified against the snapshot (read of lines 1-119): 20-33 contain live duplicate, unavailable/`-r` RAID-only, removal, devid vs path, disconnected-must-use-devid, same-or-larger target; 35-38 contain resize-to-`<devid>:max`; 54-57 contain `-r` "only read from *srcdev* if no other zero-defect mirror exists" and the many-read-errors/slow-access note; 101-119 contain the bigger-drive example (`btrfs replace start 1 /dev/sdc /mnt/my-vault/` at line 106) and `btrfs filesystem resize 1:max /mnt/my-vault/` at line 119.
   - teaches: each clause maps to a source sentence in the anchor ranges (live duplicate → 23-24; unavailable or `-r` RAID-only → 25-26; `-r` zero-defect-mirror condition and many-read-errors/slow justification → 54-57; device path or devid and disconnected-must-use-devid → 29-32; completion removes source → 27-28; target same-size-or-larger → 33; resize to `<devid>:max` to use a larger target → 35-38). Every conditional branch the source states is kept: unavailable vs `-r` (both), same-or-larger (both), numeric/deviceid vs path, mirror-exists vs not (QUALITY.md:133 rule 66, R26-TEACHES-OVERSTATED/R26-DRAFT-DRIFT: "a condition with two branches keeps both"). No "only"/"otherwise"/"exactly" claim exceeds a source sentence. teaches is not overstated.
   - status `mined`, opened `2026-10-22`, recheck `on-release`: consistent with the Gate row decision `admit, mined, tier A` and with lesson `corpus/lessons/round-31.md:22` (S164-S169, S171-S173 absent → mined, recheck on-release).
   - used-by `corpus/knowledge/btrfs-repair-r31.md, corpus/knowledge/btrfs-repair-r31.json, SKILL.md, corpus/lessons/round-31.md`: all four files exist at f3a5723 and cite S168 — btrfs-repair-r31.md (2 occurrences: Q07 row at line 18 and error-pattern line 36), btrfs-repair-r31.json (`"source": "S168"`), SKILL.md (`:2686` `[R31-Q07]` row cites "S168 lines 20-33, 54-57"), round-31.md (Gate row line 15). `grep -c 'S168'` = 2 / 1 / 1 respectively.

5. [inf] No falsifying observation found in any cell; no status/recheck/used-by cell changed between the integration commit (13ca52d0) and the revision under attack (f3a5723) — the git log for `corpus/SOURCES.md` shows the round-31 registry landed at 13ca52d and f3a5723 only adds wave-1 evidence and after-receipts.

Verification gaps: none material. GitHub REST API rate limit prevented an API-based tag peel and commit existence check; replaced with `git ls-remote` (peeled ref) which is a direct upstream source. No re-run of the wave-1 probes was needed for this seat.

Scope: read=corpus/SOURCES.md:262, corpus/lessons/round-31.md:9-23, corpus/QUALITY.md:120-149, .ufo/waves/round-31/w1/ScribeSrcReplace/btrfs-replace.rst:1-138, SKILL.md:2686, git log/rev-parse/ls-remote, fetched upstream bytes; wrote=.ufo/waves/round-31/w2/RevSourceS168.md, .ufo/waves/round-31/w2/RevSourceS168/btrfs-replace.rst.fetch; executed=curl (save bytes), sha256sum, sed|grep -cF, git ls-remote, git rev-parse/log, grep -c, mkdir.

Model: not exposed

Installs: none
