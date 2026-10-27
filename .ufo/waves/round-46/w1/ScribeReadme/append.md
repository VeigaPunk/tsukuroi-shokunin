
## Round-46 coverage note (appended 2026-10-27)

Append-only; the coverage map, the Frontier bullets and the round-38 to round-45 notes above stay as written.

| Note | Holds | Sources |
|---|---|---|
| `knowledge/census-identity-r46.md` | The census's own identity in one command: `bash tools/tsukuroi-census.sh --identity` prints one `TSUKUROI_CENSUS_IDENTITY: version=… sha256=… md5=… bytes=… lines=… planes=… exit_map=… verified=yes\|no` line before any plane probe and exits 0, while `--identity` with any other argument (`--selftest`, `--help`) prints `--identity takes no other argument` and exits 2. The digests are read through the descriptor bash holds the script on (`/proc/$$/fd/<n>`; bash moves the script to a high descriptor, normally 255, capped at `HIGH_FD_MAX` 256) and a descriptor qualifies only when it is 10 or more, a regular file, its link equals `readlink -f` of the invoked path, its `flags:` line in `/proc/$$/fdinfo/<n>` carries `O_CLOEXEC` (`02000000`), and exactly one descriptor qualifies; a script read from stdin (`BASH_SOURCE[0]` unset), through a pipe or process substitution (`pipe:[…]`), a file replaced after bash opened it, a relinked path, or an ambiguous match prints `unverifiable` in the four byte fields and `verified=no`, and a path is never hashed on trust. `lines` counts newline bytes as `wc -l` does; sha256 is taken again after md5, bytes and lines, and all four print only when both sha256 reads agree. The sha256 names a revision (hash each committed census blob and compare); `version` stays the literal `census-v2` | S250 (bash tag bash-5.3 `shell.c`, `general.c`, `general.h`), S251 (`proc_pid_fd(5)`); `.ufo/waves/round-46/frozen/src` (SHA256SUMS + FETCH.txt); counter `tools/score-census-identity-r46.py` |

Frontier: nothing moves. `--identity` extends the existing host-census gate (`../PROVINCE.md`, the
`../tools/tsukuroi-census.sh` row) and claims no new coverage-map ground; the mode runs no plane probe and writes
nothing (`../tools/tsukuroi-census.sh:3467-3513`, the `nowrite_ok` leg), so the storage, boot and boot-loader
frontiers stay as the round-38 to round-45 notes leave them. Measured with
`../tools/score-census-identity-r46.py --revision <REV> --scratch <DIR>` at the revision named in
`../SCORECARD.md` "Round 46 — measured outcome" (predicate identity_ok == 1 and tracks_ok == 1 and symlink_ok == 1
and unverifiable_ok == 1 and cli_ok == 1 and nowrite_ok == 1 and selftest_pass == 1 and selftest_r46 >= 4); the
selftest cases carrying the label `(R46-C1)` are the entry's own.

## Round-44 correction — the depth gate FAILED and SR7-SR9 are pending (appended 2026-10-27, routed D1)

Append-only; the round-44 note above, its row at `:434` and its paragraph at `:440-452` stay byte-for-byte as
written, and no Frontier/Core line moves. Read that note with this status:

- **The round-44 depth gate FAILED.** `tools/check-scrub-record-r44.py` at `fbfef071` reports rows 3, quotes_ok 3,
  props_ok 3, host_ok 3, sources_ok 1, verdicts_ok 0, novelty_base_hits 0, pointer_ok 1: three rows measured, no
  counted seat bound a verdict (`.ufo/waves/round-44/after/c2-final-fbfef071.jsonl`), against a predicate that
  requires `verdicts_ok == 3` (`tools/check-scrub-record-r44.py:50-51`).
- **SR7-SR9 are pending, not admitted.** `:434` lists what the entry holds; it is not a pass mark. The SR8/SR9
  narrowings made after the counted reads were judged by no counted seat
  (`corpus/lessons/round-44-verifier-spotcheck.md` §2 C2, its D3, carried as D1 in
  `corpus/lessons/round-45-verifier-spotcheck.md` §5). The entry carries the same status in
  `knowledge/btrfs-scrub-record-r44.md` section "Round-45 grounding and gate status"; D1 names the same status for
  `SKILL.md` section "Scrub record — round 44 rows".
- **The grounding is not the admission.** Round 45 grounded the three `[inference]` marks from source
  (`knowledge/btrfs-scrub-grounding-r45.md`, rows GR1-GR3) and bound none of them either (round-45 gate FAILED,
  `verdicts_ok` 0, `:462-466`). The round-46 attempt is counted by `tools/check-scrub-admission-r46.py`
  (`r45_legs_ok == 1 and verdicts_ok == 3 and marks_ok == 3`); until that counter reports `verdicts_ok 3` at a
  measured revision, SR7-SR9 stay pending.
- **The Frontier/Core split at `:436-444` is unaffected.** The promotion rests on the round-44 census arm
  (`../tools/tsukuroi-census.sh` `probe_scrub_record`, counted by `tools/score-scrub-arm-r44.py`), not on the depth
  rows; the record's content, the running state and NVMe SMART/Health stay Frontier exactly as `:441-444` writes
  them, and running, canceling, resuming or limiting a scrub stay operator-owned.
- **The round-45 lesson's D3 row credits a half-close.** `corpus/lessons/round-45.md:94` marks the defect closed and
  credits `194a4523` with the mark in `corpus/README.md`; that commit appended only the round-45 note's sentence
  (`:465-466`, GR1-GR3 pending), and `:434` with `:440-452` still carries no status — the half-close
  `corpus/lessons/round-45-verifier-spotcheck.md` §5 routes as D1.
