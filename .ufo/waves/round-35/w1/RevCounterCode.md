# RevCounterCode — review of tools/score-pacnew-arm-r35.py at 6b4561e43e15c1cce038e390ad7d4691b0af4cc8

Identity: bytes extracted with `git show 6b4561e…:tools/score-pacnew-arm-r35.py`; sha256
`19d25d14f9ee6ad15c036c75f997f2fba7aa756779c9e3b70a0ff136297e0155` — equals the declared
counter bytes. Static review only (no execution, per assignment). Counter file cited as
`counter:NN` = /fast/scratch/hyaku/tsukuroi-r35/RevCounterCode/counter-6b4561e.py (blob
lines). Census baseline cited as `census:NN` = the blob at the same commit.

VERDICT: counter is internally consistent (code == docstring == PREDICATE, clause by
clause) and the hermetic harness closes every host read I could trace; one MEDIUM
spec-tension defect (non-`/etc` log targets counted into `log_pacnew`/`log_pacsave` while
the declaration calls them distractors), three LOW findings, no false-pass path found.

## Findings

1. MEDIUM — `log_pacnew`/`log_pacsave` count non-`/etc` targets, which the declaration
   labels "distractor lines". Fixture generator emits
   `[ALPM] warning: /usr/share/X installed as /usr/share/X.pacnew` (counter:167); the
   oracle loop counts any `[ALPM] warning: <F> installed as <F>.pacnew` line regardless of
   path — `logged[k] += 1; tset.add(...)` with no `/etc` filter (counter:185-190), and the
   docstring's `log_pacnew`/`log_pacsave` definitions (counter:20-22) likewise carry no
   path restriction. The round-35 declaration's fixture spec lists "non-`/etc` targets"
   among the distractor log lines. A positive control that pairs log events with the
   `/etc` sweep and therefore filters warning lines to `/etc` targets — a defensible
   reading of both the declaration and of "pairing the readable `/etc` sweep with
   pacman.log" — fails every fixture containing at least one `/usr/share` line
   (P = 1-(6/7)^k, k~U(3,8) distractor lines ≈ 31-56%, ~43% average) and lands near
   ~14/24, reading as an implementer bug rather than a counter-text ambiguity. No
   false-pass risk either way (both readings still have to get every other field right).
   Docstring and code agree with each other; the conflict is declaration-vs-counter.
   Fix before the freeze byte-freeze, one or the other: (a) state in the docstring that
   `log_pacnew`/`log_pacsave` count warning lines for any target path, or (b) restrict the
   oracle's event regex loop and `tset` intake to targets under `/etc/` (counter:188).
   [obs for the code, inf for the probability]

2. LOW — parse() silently ignores unknown tokens on the DRIFT line (counter:274-281):
   `foo=bar`, `pacnewx=3` (`name not in FIELDS`) and bare tokens (`sep == ''`) are dropped
   without error; only the 8 FIELDS are validated. The PREDICATE as written
   (counter:50-56) constrains only the named fields, so code and predicate agree, but a
   census may append arbitrary junk (even `seed=…` debug output) to the DRIFT line and
   still match. Cosmetic looseness; no shortcut value. Also accepts `pacnew=007` as 7
   ("integer" reading of `[0-9]+`). [obs]

3. LOW — `--fixtures 0` (or negative) exits 0 vacuously: `code = 2 if errors else
   (0 if matches == a.fixtures else 1)` (counter:365) with matches==0==fixtures. No
   validation that fixtures > 0 (counter:292). Unreachable through the contracted
   run-receipt invocation (default 24), but a foot-gun for ad-hoc scoring runs. [obs]

4. LOW — fixture generates `.pacsave.0` (counter:114, `'.pacsave.%d' % rng.randint(0,
   12)`), a name pacman never creates: upstream rotation starts at `.pacsave.1`
   (sources/remove.c-54d9411:409-416 renames `X.pacsave` to `X.pacsave.1`, then shifts
   N→N+1). pacdiff's find glob `*.pacsave.[0-9]*` would list it (pacdiff.sh.in:235), so
   the surface is self-consistent, but the fixture exercises a filename outside pacman
   7.1's actual output space. [obs]

5. INFO — `TSUKUROI_BOOT_TARGET` sits in DIR_SEAMS (counter:62-63) and the harness points
   it at an empty directory, but the census uses it as a systemd unit name passed to the
   (stubbed) systemctl (census:1362 `is-active "$target"`). Harmless hermetically — the
   stub answers everything — just a miscategorized seam. [obs]

6. INFO — `assert __doc__.count('VERSION 1') == 1` (counter:68) is stripped under
   `python3 -O`; the version self-identity guard is advisory only. [obs]

## Verified sound (positive results, not defects)

- Oracle log shapes match pacman 7.1 bytes: NoUpgrade pacnew
  `warning: %s installed as %s.pacnew` (sources/add.c-54d9411:349-350); backup-case pacnew
  `warning: %s installed as %s` with `filename = origfile + ".pacnew"` (add.c:323, 400-404);
  removal save `warning: %s saved as %s` with `newpath = file + ".pacsave"`
  (remove.c:546-560). Counter regexes plus the `group(2) == group(1) + '.' + k` equality
  (counter:182-190) accept exactly these shapes and reject the mismatched-pair and
  `.pacnew.tmp` distractors (counter:168-169).
- `.pacsave.N` rotation is unlogged upstream (remove.c:347-417 — pure renames, no
  logaction), and the counter treats `.pacsave.N` entries as never-pairable/unlogged: the
  event builder guards on `rel.endswith('.' + k)` so a `.pacsave.5` entry never gets a log
  line (counter:158-160). Matches the declared "unlogged `.pacsave.N` shift".
- pacdiff v1.13.1 searches exactly `*.pacnew *.pacorig *.pacsave *.pacsave.[0-9]*` under
  DIFFSEARCHPATH default /etc (pacdiff.sh.in:29, 228-235) with no type filter; the
  counter's `kind()`/SAVE_GLOBS (counter:63-65, 71-80) match pacdiff's name set while
  excluding directories ("non-directory entries", counter:15-18), so control K13
  ("pacdiff's exact find expression (directories counted)") is a true discriminator.
- pacman 7.1 no longer creates `.pacorig` (no pacorig in add.c at 54d9411) — the counter
  counts pacorig as drift surface with no log pairing, consistent with pacdiff still
  searching for names pacman no longer makes.
- Hermetic harness PASS. All 9 census probe commands are in CMD_SEAMS (pacman,
  pacman-conf, systemctl, dmesg, journalctl, nvidia-smi, lsmod, expac, vercmp —
  census:375-408 vs counter:57-59). All 7 file reads are in FILE_SEAMS. Dir seams cover
  PACMAN_DB, ROOT_DIR, PCI_SYSFS, DEV_DIR, CGROUP_ROOT; MEM_SLICE needs no seam because
  the census joins it under CGROUP_ROOT (census:1055 `slice="$CGROUP_ROOT/$MEM_SLICE"`).
  FOREIGN_BASELINE/OOM_BASELINE are forced empty → embedded baselines, no host read.
  The census env is built from scratch BASE_ENV (counter:66-67, 248), so no inherited
  TSUKUROI_*/GIT_* leaks in; HOME and TMPDIR are private. Host-path literals appear only
  as `${VAR:-default}` seam defaults; the only live `find` reads seamed CGROUP_ROOT
  (census:1099); the baseline census contains no `TSUKUROI_ETC_DIR` at all. Under the
  stubs every plane degrades/blocks, so the census exits 1 or 2 — inside the predicate's
  accepted exit set {0,1,2}. No probe reaches host state.
- Unchanged check ordering is sound: snapshot → pre-ctimes → run → post-ctimes →
  snapshot (counter:327-340). snapshot()'s locked-dir chmod churn (counter:219-243) lands
  outside the ctime window; create/delete/rename move parent-dir ctimes (dirs are lstat'd
  by ctimes(), counter:206-214); chmod/utimes/rewrite move entry ctimes; bytes, modes,
  type bits, symlink targets and locked-dir interiors are hashed by snapshot(). The
  docstring's claim that a census which "renames or rewrites anything and then restores
  it still moves a ctime" holds.
- Fixture attack surface clean: counted/distractor/gone name collisions are structurally
  impossible (counted names are 6-char base + counted suffix; distractor dirs 6-char base
  + non-counted suffix; locked dirs and gone-event bases are 7-char), a same-name rewrite
  dedupes harmlessly in the oracle dict (counter:178-193) or fails loudly as a harness
  error, and makedirs/symlink overlaps raise rather than misreport. No counted entry can
  sit inside an unreadable dir: locked dirs are created after all entries and never used
  as parents (counter:96-104, 141-147); the counted-looking file inside a locked dir is
  deliberately uncounted and the oracle excludes it — consistent with what any sweep can
  see under mode 000/300 (300 is -wx, no read, so listing fails). Dangling symlinks
  (~15%) are counted entries, never followed — K12 (`find -type f`) discriminates.
  Gone-event targets (7-char base + suffix) can never collide with counted entry paths.
- Exit-code semantics match the docstring (counter:30-31 vs :365): 0 = all match and no
  harness errors, 1 = any fixture mismatch, 2 = harness error (euid==0 guard, unreadable
  census bytes, fixture build exception — each still prints its row and the summary).
  Header pins `counter_sha256` of the running bytes and `census_sha256` of the scored
  census (counter:296-311).
- PREDICATE (counter:50-56) vs code, clause by clause: census bytes read from
  `git show rev:tools/tsukuroi-census.sh`, never the working copy (counter:306-307) ✓;
  TSUKUROI_ETC_DIR/TSUKUROI_PACMAN_LOG set per fixture (counter:330-331) ✓; exit in
  {0,1,2} within 120 s, timeout → fail (counter:333-337, 342) ✓; exactly one stdout line
  beginning `DRIFT pacnew-plane ` (counter:270-272) ✓; each field once, integer
  (counter:276-284) ✓; all equal the oracle (counter:342) ✓; etc tree and log unchanged in
  bytes, modes and ctimes (counter:342 via snapshot+ctimes) ✓.

## Residual risk and verification gaps

- Static review only: no fixture was built and no census was executed (assignment:
  read-only). Collision and probability figures are analytic [inf].
- No `lsp` device exists in this environment's tool inventory; caller/definition checks
  were read/grep over the sha256-verified blob, not semantic index answers.
- Sources fetched via GitLab raw at short ref `54d9411` and tag `v1.13.1`; contents
  self-identify (formats match pacman 7.1 behaviour), but I did not verify the resolved
  full commit sha [unk].
- Finding 1 interacts with K14: if the positive control reads 24 failures concentrated in
  `log_pacnew`, check for an `/etc`-filtered log reader against counter:167/185-190
  before blaming the census.
- The harness's empty stub outputs force several census planes to BLOCKED; a variant whose
  DRIFT arm sits behind an early return scores 0 of 24. Design constraint for the
  positive control, not a counter defect [inf].

## Sources

Saved unchanged under .ufo/waves/round-35/w1/RevCounterCode/sources/:
- add.c-54d9411 — https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/add.c —
  sha256 fd3136291885cae73ad00abab3d83de49ea0276f040e53cca3902cfb93cf58f1
- remove.c-54d9411 — https://gitlab.archlinux.org/pacman/pacman/-/raw/54d9411/lib/libalpm/remove.c —
  sha256 a052d455f088f34bf1d713a434957de7e1b9322862a07b69160c65ee15dca314
- pacdiff.sh.in-v1.13.1 — https://gitlab.archlinux.org/pacman/pacman-contrib/-/raw/v1.13.1/src/pacdiff.sh.in —
  sha256 f65e626da3d4c6d30c9fda8efcfa5ef64d790c902890de62b9b7f4a71056d309
Each URL duplicates a row reserved this round (S191, S192, S193 per the round-35
declaration); the registry itself holds S001-S190, so they are not yet registered rows.

Scope: read=SCORECARD r35 declaration + counter/census/run-receipt blobs at 6b4561e via read-only git show; pacman add.c/remove.c@54d9411 and pacdiff v1.13.1 via curl; wrote=.ufo/waves/round-35/w1/RevCounterCode.md, .ufo/waves/round-35/w1/RevCounterCode/sources/{add.c-54d9411,remove.c-54d9411,pacdiff.sh.in-v1.13.1}, /fast/scratch/hyaku/tsukuroi-r35/RevCounterCode/{counter-6b4561e.py,census-6b4561e.sh,run-receipt-6b4561e.py}; executed=git show (read-only) x4, sed -n declaration slice, curl x3, sha256sum, wc — no counter or census execution
Model: zai/glm-5.3-flash (exposed via workstation context)
Installs: none
