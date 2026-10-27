VERDICT: supports

Item C1-14. Line-by-line review of tools/score-scrub-arm-r44.py (frozen; sha256
1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388 — verified by
`sha256sum` on the reviewed file) against the declaration's contract, the census header
paragraph (tsukuroi-census.sh:383-420), and the production probe
(tsukuroi-census.sh:1966-2040). Counter re-run on the implementation revision
7e081698d4fc3c4ea944884fd093058de9909de1:
`python3 tools/score-scrub-arm-r44.py --revision 7e081698... --scratch /fast/scratch/hyaku/tsukuroi-r44/C1RevCounter/s`
→ `{"cases":16,"correct":16,"identity_ok":1,"wired_ok":1,"live_agree":1,
"selftest_pass":1,"selftest_r44":9,"selftest_line":"TSUKUROI_CENSUS_SELFTEST: PASS
(141 cases, 141 passed, 0 failed)","verdict":"PASS","wrong":[]}`.

1. expect() vs the contract (score-scrub-arm-r44.py:194-264)
- State precedence (258): BLOCKED if any reason, else RECORDED iff rec+tmp+sock>0, else
  NONE — identical to probe_scrub_record (census:2035). Exact.
- Detail order (261-263): `det = blocked + info`; block reasons are appended in traversal
  order — sysfs fsids sorted, then devids sorted (203-216), then sorted record-dir names
  (227-251), then timers (254-255) — followed by speed_max pairs (219) which the census
  appends after all block reasons (`detail+=$info`, census:2037). Names are ASCII, so
  Python code-point sort == shell glob bytewise order under LC_ALL=C (census:1968,2037).
  Exact.
- Orphan gating (238): `if sysok and ...` — orphans counted only when the sysfs root is a
  listable directory (sysok set only in the dict branch, 202). Matches census
  `[ "$sysok" -eq 1 ]` (census:2020). Exact.
- sysfs:absent (251-252): fires when rec>0 and sys is None. The census fires when rec>0
  and `[ ! -e "$root" ]` (census:2025). For every reachable state — all 16 drawn cases use
  sys as a dict or 'unreadable' (see make_cases, 371-441), never None, and the live root
  /sys/fs/btrfs always exists — the two conditions coincide. Latent divergence, see F1/F2.
- Bare-template exclusion (257): `n != 'btrfs-scrub@.timer'` under
  `fnmatch.fnmatchcase(n,'btrfs-scrub@*.timer')` — identical to the census's glob plus
  skip of the bare name (census:2030-2032). Timer entry type is ignored by both (census
  counts by name only; materialize allows symlink or file kinds with no oracle effect).
- Readability from the scored uid's view: the model encodes readability as a boolean
  (k[1] for records/tmp, 237/245; 'unreadable' for sysfs speed files, 211-212). Drawn
  readability is realized as mode 0600 vs 0644 (materialize 316-318, 296-301) with the
  visible owner = namespace root = the outer caller uid (INNER runs as ns uid 0; mapping
  `--map-users={uid},0,1`, 566). The census runs after `setpriv --reuid=<outer uid>
  --regid=<outer gid> --clear-groups` (97), i.e. as ns uid == outer uid number — a
  different uid than ns 0, so 0600 files genuinely fail `[ -r ]` and 0700 dirs fail
  listing. The identity leg confirms this identity (99-100, 578-579): observed
  `["1000","1000","1000"]`. Exact for an unprivileged operator; root-run limitation, see F5.
- `dir` type checks: 'unreadable' → dir:unreadable (222-224), dict → present with
  per-name type checks (record/tmp require regular file, 233-245; progress requires socket,
  246-249) — mirror the census (census:2016-2024, 2026-2029). 'notdir' is normalized to
  'unreadable' (341-346) and materialized as a regular file at the dir path (311) — the
  census's `[ ! -d "$dir" ]` then yields unreadable exactly as the oracle says.

2. materialize()/INNER build the model (282-338, 82-155)
- Modes/owners: files/dirs are created by INNER as ns uid 0; readability is encoded via
  0644/0600 or 0700 dirs; root_modes applies 0700 to the /sys/fs/btrfs mount point for
  sysfs-unreadable (286-287, 138-139), and the record-dir itself is 0700 for
  dir-unreadable (307), with a hidden record that only a listable dir would surface
  (308-309) — consistent with the oracle counting nothing for 'unreadable'.
- Sockets: AF_UNIX bind at the entry path (132-135), closed and unlinked between cases
  (103-115); fifos via mkfifo (131); symlinks via os.symlink (129) with a dummy target
  (320) — the census checks only lstat type, never the target.
- Per-case cleanup rebuilds every root (106-115), so no cross-case leftovers.

3. Case-by-case collapse audit (349-442; 16 cases)
- Limited can never collapse to 0 by chance in 'limited-devices': the first fsid's first
  dev is forced to 10^6..10^9 (397) and an extra devid (guaranteed absent from that fsid,
  398-399) is forced to 1..99. All other cases draw speeds '0\n' (default), malformed
  pool (403), or None/'unreadable' (408) — none can accidentally produce a nonzero limit
  where the oracle expects 0, and 'mixed' (431-441) mirrors whatever is drawn.
- Malformed pool (403) is all non-decimal/non-single-line, so 'speed-malformed' always
  blocks. 'speed-unreadable' uses None (missing file) or 'unreadable' (0600 file), both →
  speed-unreadable.
- Orphan/record/tmp/socket counts are computed by the oracle from the same model dict the
  fixture builds, so random presence/absence can only shift counts in lockstep.
- 'wrong-types' (423-427) exercises symlink/dir records, fifo progress, tmp symlink,
  newline-bearing name, uppercase fsid, non-matching names — all ignored by both sides
  except the four block reasons, in bytewise order (progress < status < status_tmp).
- No drawn value can make an expected line wrong for a correct arm within the 16 cases; the
  only divergences found (F1/F2) are unreachable by the current case generator and by any
  real host.

4. Findings (severity order)
- F1 (latent, unreachable): sysfs:absent clause. Oracle: rec>0 ∧ sys is None
  (251-252). Census: rec>0 ∧ `[ ! -e "$root" ]` (census:2025). In the namespace the
  sysfs root is always a tmpfs mount, so a future case with sys=None and records would
  make the census take the `elif [ -d "$root" ]` branch → sysok=1, zero fsids → all
  records counted orphans, no block, RECORDED; the oracle would predict BLOCKED
  sysfs:absent with orphan=0. No current case uses sys=None and the live host always has
  a real sysfs root, so this cannot affect the predicate today. Recommend documenting
  the clause in the oracle comment or tightening the census to match.
- F2 (latent, pathological): if the sysfs root existed as a non-directory (census:
  `[ -d ]` false, no block, no sysfs:absent), the oracle (sys=None) would emit sysfs:absent
  for rec>0. Same unreachability. Grouped with F1.
- F3 (robustness): live_model (445-496) guards SYS/DIR/WANTS listing with isdir+access,
  but `os.listdir(dv)` for devinfo (456) is unguarded — a PermissionError there would
  abort the counter with no JSON verdict (no 'unreadable' map). Not hit on this host
  (/sys is world-readable; the run above completed), but a one-line try/except would make
  the live leg non-crashing.
- F4 (cleanup): SIGINT/SIGTERM handlers raise SystemExit (520-524); the finally block
  chmods and removes the workdir (527-529) — verified path. Children (unshare/python3,
  census subprocesses) are not terminated on signal, so an interrupted run can leave the
  namespace processes running until they finish. No /tmp or lane writes result; resource
  hygiene only.
- F5 (harness limitation): with an outer uid of 0 the mapping `--map-users={uid},0,1`
  makes the scored uid == the owner of all fixtures, so 0600/0700 fixtures become readable
  and the unreadable-dependent cases would fail on a correct arm; the counter also
  requires a subuid/subgid range (167-176). It is correctly intended for an unprivileged
  operator (this host: uid 1000, identity leg verified).
- Positive confirmations: --scratch is argparse-required (514) and everything the counter
  writes lives under it (517-518, 607-608); no /tmp use anywhere in the counter (the
  selftest's TMPDIR is pointed at scratch/st, 607-608; `tempfile.mkdtemp(dir=a.scratch)`,
  518). Defaults SCRUB_DIR/BTRFS_SYSFS/TIMER_WANTS are set at top level of the census
  (census:492-495), so sourcing the lib (CALL, 80) sees them. The selftest summary format
  (census:3295-3296) matches the counter's regex (615) exactly; (R44-C1) label count is 9
  (`grep -c "(R44-C1)"` → 9), satisfying selftest_r44 >= 6 (618). Nine labeled selftest
  cases exist (census:3229-3286) and the run above reported 141/141. Wired placement
  check (503-508) enforces exactly one SCRUB line equal to the oracle, exactly one STORAGE
  and one rollup line, with STORAGE < SCRUB < rollup — matching the header contract
  (census:3374-3376). wired_ok intentionally ignores the wire census's exit code (observed
  rc=2 in the namespace: other arms see an empty host view); the exit-code kill rule is the
  round-level base-vs-measured check, not this counter's.
- Not run: no base-revision run (kill rules are the orchestrator's), no mutation of the
  lane or host, no second heavy run beyond the single counter execution above.

Conclusion: the oracle implements the declared contract exactly for every state the 16
drawn cases and any real host can produce; materialize/INNER faithfully realize the model;
no case's expected line is wrong for a correct arm and no drawn value collapses a case.
Findings F1-F5 are latent/robustness notes, none affecting the frozen predicate on this
host (verified: PASS at 7e081698).
