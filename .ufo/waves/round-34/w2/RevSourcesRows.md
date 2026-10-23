# RevSourcesRows — review of SOURCES.md rows S186–S188 at 879daa95b898b5c624c609eced31f7d0d5b933e8

Verdict: MEETS the review criteria — all three new rows (S186, S187, S188) are well-formed, hash-anchored to saved snapshots, non-duplicate, and the sources-census validator exits 0 on the lane.

## Findings

1. Row shape: each of S186, S187, S188 has exactly 11 cells against the `| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |` schema (counted on the committed file at 879daa95: `corpus/SOURCES.md:192-194`; the registry contract requires NF=13 fields per line, `sources-census.sh` header comment). [obs]

2. Kind and tier: S186 `code|A` (upstream C sources), S187 `docs|A` (man page), S188 `docs|A` (man page + doc). Tier A is consistent with precedent rows for the same host (S024 systemd NEWS A, S180 CPython subprocess.rst A); no community row here, so the "community never A" rule is not implicated. The validator's E05/E06/E10 checks fired nothing. [obs]

3. Anchors are tag-pinned (all three say `tag v262`) and carry per-file line anchors plus SHA-256 digests. All seven declared digests equal the saved wave-1 snapshots byte-for-byte [obs]:
   - `SrcCoredumpCode/coredump-submit.c` = `54ce12400ce7e7c5ec4f8a6acdeac58659780434ed964f9c941f82ec11d0e538` (row declares same)
   - `SrcCoredumpCode/coredump-context.c` = `7f5157d92b63a0af1f37c592cbd6954390d22fa8910fa938e13edaf45a79e5a6`
   - `SrcCoredumpCode/coredump-config.c` = `1021bd028c11a93596e268eefce516fcd859b7163e6824818d84c27c7210d3fd`
   - `SrcCoredumpCode/sd-messages.h` = `fb613f71807344eb29b9353cad8c09cb644fff4a18b1651fda9b49e0a23064fc`
   - `SrcCoredumpConf/coredump.conf.xml` = `b1c2eeee292175ff687fc428635bb25c7908ed14143a3cfc34016ba78278a39d`
   - `SrcJournalctlJson/journalctl.xml` = `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd`
   - `SrcJournalctlJson/JOURNAL_EXPORT_FORMATS.md` = `207a646c067be133ff711f039bb2997a706bc5c146b7db6aa0f0350997b25543`
   Command: `sha256sum` of the seven files under `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/Src*/`, exit 0.

4. Line anchors spot-checked against snapshots and consistent with the teaches cells: `sd-messages.h:41-42` is `#define SD_MESSAGE_COREDUMP ... fc2e22bc6ee647b6b90729ab34a250b1`; `coredump.conf.xml:77-80` states Storage=none cores "may be logged ... but not stored permanently"; `journalctl.xml:591-593` states fields larger than 4096 bytes are encoded as null unless `--all`. [obs]

5. Status / opened / recheck / used-by: all three rows are `mined`, `opened` 2026-10-23 (today, a valid past/present ISO date), `recheck` = `on-release` (declared symbolic cadence in the validator's contract, same value used by other systemd rows), `used-by` = `corpus/knowledge/coredump-count-unit-r34.md`. The used-by path exists at the commit (`git cat-file -e` passed) and cites all three ids: `source:` line at `coredump-count-unit-r34.md:3` names S186, S187, S188 (and S177 re-opened), `verified-at: 2026-10-23` at line 4 — the round-33 rejection cause (missing source:/verified-at:) is absent here. [obs]

6. Duplicates: none of the seven URL fragments (`coredump-submit.c`, `coredump-context.c`, `coredump-config.c`, `sd-messages.h`, `man/coredump.conf.xml`, `man/journalctl.xml`, `JOURNAL_EXPORT_FORMATS.md`) or seven SHA-256 digests appears in any other committed row (programmatic scan of all `| S…` rows except S186–S188 in the committed file: zero hits). S177 (`man/systemd-coredump.xml`, SHA `56bed6ed…`) is a related but distinct systemd v262 doc — different URL and different bytes; the committed note documents its re-open with unchanged digest (`coredump-count-unit-r34.md:66`). No E04 duplicate or E03 duplicate-id findings from the validator. [obs]

7. Validator run: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0; last output line `tsukuroi\tok\t/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`. Preceding lines are pre-existing W04 same-URL-across-scopes warnings on older ids only (S038, S041–S046, S049, S058, S082, S087–S098, S105–S111, S126, S136–S138, S149, S155, S158, S182, S184, S185); W-codes do not affect exit status and none touches S186–S188. [obs]

8. Scope note [inf]: the working tree carries uncommitted additions S189 and S190 after S188 (`git status`: `M corpus/SOURCES.md`, +2 lines). The review target is commit 879daa95, where the three assigned rows end the table; S186–S188 are byte-identical between commit and working tree. The validator read the working file (including S189/S190) and still returned clean. `SrcCoredumpCode/` also holds two undeclared extras (`coredump.c`, `systemd-coredump.xml` — the latter is S177's re-opened file); extra snapshot files are not flagged by the validator. [unk] whether the row-review scope intended the committed table only; flagged for completeness, not a defect of S186–S188.

Scope: read=corpus/SOURCES.md rows + header, corpus/knowledge/coredump-count-unit-r34.md (working + committed), scripts/sources-census.sh header, w1 snapshot files; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/RevSourcesRows.md; executed=git rev-parse/status/diff/show/cat-file (read-only), sha256sum on 7 snapshot files, sources-census.sh validate, sed -n line spot-checks
Model: devin/swe-2
Installs: none
