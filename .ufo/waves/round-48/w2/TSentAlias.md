VERDICT: defect-found

Seat: TSentAlias (leaf; C1-S1, security review of the C1 mechanism). Judged axes: operability, C1, security.
Bytes under test: `git show ae99f021b76f8eb1c8805d32d80644464afb1ff6:tools/tsukuroi-census.sh` — sha256
`375aa7370f84b0ee9d4630e2cd34165c1403901e3266db603ffa43f3a76e2426`, matching
`.ufo/waves/round-48/frozen/FROZEN.md` (read, not cited as evidence for behaviour). Line numbers below are that blob's.
All harnesses, clones and fixtures lived under `/fast/scratch/hyaku/tsukuroi-r48/TSentAlias/` and were removed at the end;
receipts are `.ufo/waves/round-48/w2/TSentAlias/`.

Scope statement up front: **this finding does not falsify the counted C1 predicate.** I re-ran the spaced (dirty)
scenario on the frozen blob and it printed `TSUKUROI_CENSUS_SELFTEST: PASS (166 cases, 166 passed, 0 failed)` with rc=0,
the fixture observed inside the spaced TMPDIR and then removed (`receipts/spaced-counted-case.txt`); I checked the
fail-fast path directly (a non-writable and a missing TMPDIR: non-zero, no fixture anywhere, trap never installed —
`receipts/c-empty-work.txt`); I did **not** re-run the counter's unset//tmp/scratch location legs or its SIGTERM leg —
those remain the counter's evidence, and nothing in this finding touches the trap's INT/TERM status codes. What is falsified is the
*security property the mechanism is documented to provide* — that the fixture tree stays inside the intended directory when
TMPDIR is not trustworthy (census.sh:2050-2056). Under one narrow but real configuration (TMPDIR = a non-sticky directory
writable by another local user) a local attacker obtains **arbitrary code execution as the invoking user** from the census
selftest, plus a `chmod -R u+rwx` that follows a swapped symlink out of the TMPDIR and a fixture tree that the EXIT trap
never removes.

================================================================================
(a) `/proc/self/fd/24x` aliasing: the fd pins the inode, but only for the mktemp step
================================================================================

Answer to the literal question — *can a hostile TMPDIR redirect the fixture tree between `exec 240<"$base"` and
`mktemp -d`, by swapping `$base` for a symlink?* **No.** The fd is opened with `exec ${fdn}<"$base"` (census.sh:2083) and
`ST_BASE_DIR=/proc/self/fd/$fdn` (2085) names the open directory *inode*; `/proc/self/fd/N` is resolved from the fd table,
not from a directory entry. Demonstrated (`receipts/a-fd-and-chmod.txt`, a1):

    fd240 -> .../r1/base
    name base -> .../r1/victim ; fd240 -> .../r1/base.moved ; same inode: YES
    mktemp -> tsukuroi-r3-2-selftest.BcrmKL
    created in moved original: YES ; created in victim: NO

So the round-47 defect (`st_base=/tmp` fallback) is genuinely fixed, and the alias cannot be steered by a rename that
happens *before* mktemp.

**But the pin covers only the mktemp call.** From census.sh:2112 onward every fixture path is spelled through the
*name* `$work`:

    2112  bin="$work/bin"
    2113  mkdir -p "$bin" "$work/fx"
    2115  cat > "$bin/.dispatch" <<'STUB'
    2189  chmod 700 "$bin/.dispatch"
    2192  ln -s .dispatch "$bin/$c"                       # pacman, pacman-conf, systemctl, dmesg, ...
    2320  TSUKUROI_PACMAN="$bin/pacman" \                # and 2321-2330: every plane override
    2109  trap 'chmod -R u+rwx -- "${work:-}" ...; rm -rf -- "${work:-}" ...' EXIT

`$work` is `mktemp -d`'s result inside the caller's TMPDIR (2106). If TMPDIR is a directory another local user can write
to and that is **not sticky**, that user may rename the freshly created (0700, caller-owned) directory and put a symlink
in its place. Every later `$work/...` resolution then follows the symlink. Three consequences, each reproduced:

 1. fixture writes and, decisively, *fixture executions* land in the attacker's directory. The census passes
    `$bin/pacman` as `TSUKUROI_PACMAN` (2320-2321) and the plane runs it. The attacker owns that directory, so it deletes
    the census-written `pacman -> .dispatch` and installs its own executable under the same name.
 2. the EXIT trap's `chmod -R u+rwx -- "${work:-}"` **dereferences a symlink given as the operand** (GNU chmod follows
    command-line symlinks; only links found *during* recursion are not followed). Demonstrated: after the swap,
    `chmod -R u+rwx -- $work` changed a victim tree's `inner` 0500 -> 0700 and `inner/f` 0400 -> 0700 while a recursive
    inner symlink to a third tree was left alone (`receipts/a-fd-and-chmod.txt`, a2).
 3. `rm -rf -- "${work:-}"` unlinks *only the substituted symlink*: the victim survives, and the real fixture tree stays
    behind under the attacker's chosen name — the "fixture removed" contract silently fails.

Deterministic reproducer (a2, no race, same uid):

    work name -> /…/r2/victim
    after trap chmod: victim/inner=0700 victim/inner/f=0700
    after trap rm: victim alive=YES ; real fixture leaked as hidden=YES

End-to-end against the frozen blob, same-uid model (one `--selftest`):
`receipts/exp3-same-uid.txt` — attacker renames the work dir 1.5 s in, symlinks its own dir, installs `pacman`; census
rc=1, summary `FAIL (167 cases, 33 passed, 134 failed)`, and the marker file holds **2752** lines
`CODE-EXEC-AS vgpnk uid=1000` — one per fixture invocation.

End-to-end, **true cross-user** (the decisive one): attacker runs as `nobody` (uid 65534) and holds only `w+x` on
`TMPDIR` (a 0777 non-sticky directory owned by the census user); the census runs as `vgpnk` (uid 1000).
`receipts/exp4-cross-user.txt`:

    census rc=1 ; TSUKUROI_CENSUS_SELFTEST: FAIL (167 cases, 35 passed, 132 failed)
    marker lines: 1420 ; unique: CODE-EXEC-AS vgpnk uid=1000
    atk/bin: -rwxr-xr-x 1 nobody nobody … pacman                 # attacker-owned binary the census executed
    shared/.stash: drwx------ 4 vgpnk vgpnk … bin fx            # real fixture, renamed, never removed

Preconditions, stated exactly (this is why it is moderate and not a break of the counted claim):

 - TMPDIR must be writable by the attacker **and non-sticky**. `/tmp` is 1777 and blocks it: as `nobody`,
   `mv` of a caller-owned 0700 dir inside a 1777 dir fails `EPERM` and `ln -s` fails `EACCES` (a4,
   `receipts/a4-sticky.txt`); inside a plain 0777 dir both succeed (`mv-rc=0`, `ln-rc=0`). A caller-owned private
   scratch TMPDIR is not reachable by the attacker either. The counted cases (unset, `/tmp`, private scratch,
   private spaced scratch) are therefore all outside the vulnerable configuration — consistent with the counter PASS.
 - The census must be run `--selftest` (only `run_selftest` creates `$work`; `grep -n mktemp` shows the single call at
   2106 and live mode creates nothing, census.sh:348).

Is this new? The pattern is **pre-existing**, not introduced by this diff: base `5fdf062f` has
`local st_base=${TMPDIR:-/tmp}` (2055), `work=$(mktemp -d "$st_base/…")` (2059) and the identical trap (2062). What C1
changes is the *exposure surface*: for a refused-character TMPDIR the fixture used to fall back to sticky `/tmp` and now
lands in the caller's TMPDIR (2050-2056, 2074-2088). So C1 does not create the class, but it moves the dirty-TMPDIR case
into a directory the mechanism explicitly claims is safe to honor, and the claim's own wording ("inside the real TMPDIR")
is what a reader will rely on. Report it as a defect in the mechanism under review, not as a counter miss.

Smallest remediation (verified semantics, `receipts/a-fd-and-chmod.txt` a3): after `work=$(mktemp -d …)`, pin the work
directory the same way the base is pinned and derive *every* path from the fd:

    exec 241<"$work"; W=/proc/self/fd/241
    bin=$W/bin ; fx=$W/fx ; PATH entry, TSUKUROI_* overrides, trap chmod all spelled through $W

Verified: after the attacker's swap, `PATH="/proc/self/fd/241/bin:$PATH" pacman` prints `GENUINE` while the name-based
`PATH="$work/bin:$PATH"` prints `HOSTILE`, and `chmod -R u+rwx -- /proc/self/fd/241` repaired the real fixture dir
(0700) while leaving the victim's 0000 dir untouched. Note the cleanup leg needs the same treatment: `rm -rf` through a
proc fd cannot unlink the proc entry, so the trap should delete the *contents* through the pinned fd (e.g.
`find -L /proc/self/fd/241 -delete`-style, with the fd closed afterwards) instead of relying on `$work` the name.
A cheap defence in depth, if a larger change is unwanted before close: fail fast when the resolved base is neither owned
by the caller nor sticky (`stat -c '%u %a'`), which keeps `/tmp` and private scratch working and refuses exactly the
attacker-writable non-sticky case.

================================================================================
(b) `eval "exec ${fdn}<\"\$base\""` with a hostile TMPDIR — no code execution
================================================================================

No injection. census.sh:2083 builds the string `exec 240<"$base"` and the eval's second parse expands `$base` *inside
double quotes*: the TMPDIR value becomes a single word and its bytes are never re-scanned for syntax. Tested with three
real directories whose names are the payloads (dirty branch requires `[ -d "$base" ]`, 2078), each resolved through the
alias with no side effect (`receipts/b-eval-and-options.txt`):

    resolved </proc/self/fd/240> fd=240      # dir literally named ev$(touch PWN1)
    resolved </proc/self/fd/240> fd=240      # dir literally named ev`touch PWN2`
    resolved </proc/self/fd/240> fd=240      # dir literally named ev"; touch PWN3; :"
    PWN files created: []

Fail-fast holds for the clean-charset path too: there is no `[ -d ]` check outside the dirty branch, but a missing clean
TMPDIR makes `mktemp` fail and `set -e` aborts (see (c)); a missing dirty TMPDIR is refused at 2078-2079.

Two adjacent residuals worth recording, neither of which is code execution and neither covered by the counted cases:

 1. **No `--` before mktemp's template (2106), and the alias charset admits `-` (2058-2086).** A dash-leading TMPDIR
    is handed to `mktemp` as options. Observed: `TMPDIR=-p<existing-dir>` makes `ST_BASE_DIR=<-p/…/exists>` and mktemp
    then treats `<dir>/tsukuroi-r3-2-selftest.XXXXXX` as the `-p` argument (error text in the receipt). It fails loudly
    today only because that directory does not exist; a writer of `/tmp` can pre-create
    `/tmp/tsukuroi-r3-2-selftest.XXXXXX` and then `TMPDIR=-p/tmp` builds the tree under `/tmp` on a TMPDIR that does not
    name `/tmp`. Fix: reject a non-absolute TMPDIR and pass `--` to mktemp.
 2. **Relative TMPDIR is accepted** (clean charset) and the fixture is then created relative to the process cwd —
    observed `rel/tsukuroi-r3-2-selftest.msB6wv` under the scratch cwd, i.e. outside any TMPDIR, and with the override
    then classifying `relative` at root_locator_class (census.sh:851-862) instead of `absolute`.

Also noted: fd 240 carries no close-on-exec, so fixture children inherit it and can name the caller's TMPDIR through
`/proc/self/fd/240` (observed in a child: `readlink` -> base, listing shows the caller's marker file). Harmless at one
uid, and it is why TMPDIR cannot be unlinked while a selftest runs; record it, do not fix it as part of C1.

================================================================================
(c) `chmod -R u+rwx -- "${work:-}"` when work is empty — no path to cwd, never `/`
================================================================================

No finding, by ordering plus two independent checks.

 - Ordering: `work=$(mktemp -d …)` is 2106, the EXIT trap is installed at 2109, three lines later; the script runs
   `set -euo pipefail` from 452, and no `set +e` occurs anywhere before 2106 (first is 615 inside `cap()`, unrelated;
   `run_selftest`'s own `set -uo pipefail` is 2118, after the trap). A failing `mktemp` therefore terminates the script
   with the trap *not yet installed*. Verified against the frozen blob with a clean-charset but non-writable TMPDIR
   (`receipts/c-empty-work.txt`): `census rc=1`, stderr `mktemp: failed to create directory … Permission denied`,
   `leftovers in TMPDIR: [] ; fixtures in cwd: [0]`, and no chmod/rm message — the trap never ran.
 - Even if the trap body did run with `work` empty: `chmod -R u+rwx -- ""` fails
   (`chmod: cannot access '': No such file or directory`, rc=1) and touches nothing — cwd mode 0755 and `/` mode 0555
   unchanged, cwd intact; `rm -rf -- ""` is a silent no-op, rc=0, probe file still present. Empty is not `.` and not `/`.
   `${work:-}` also keeps `set -u` satisfied.
 - `work` has exactly one assignment in the file (grep: line 2106 only), so no later code can point the trap at a live
   path either.

Minor, non-redirect residual: a signal delivered in the 2106-2109 window is handled by the default disposition, so the
fixture is leaked (no chmod/rm at all). This only widens the cleanup guarantee, not the chmod scope; mention it in the
mutation/TERM seat's context rather than as a security defect.

================================================================================
Impact, severity, and what I did not do
================================================================================

Severity: **moderate** — high impact (arbitrary code as the census user, plus mode widening on caller-owned trees and a
leaked fixture), narrow precondition (TMPDIR writable by another local user and non-sticky) and a self-inflicted
configuration, but exactly the configuration class the C1 contract says it handles safely. Not exploitable with the
default `/tmp` or a caller-owned TMPDIR; the counted C1 predicate and its four scenarios are unaffected; C2/C3 untouched.

Not done, stated plainly: I did not run the frozen C1 counter or any counter battery (other seats own those; my three
`--selftest` runs were serialized, one at a time); no strace; no attempt to force a PASS line from a hijacked fixture
(only FAIL was observed — forging PASS would need the attacker to reproduce the 166 expected fixture answers, which I did
not demonstrate); no testing of other TMPDIR filesystems (a `noexec` TMPDIR would break the honest fixture dispatch at
2320-2321 too — operability, not security, and not measured here); no other uid than `nobody` was used. Tooling: none
installed or upgraded.

Axis note (Godspeed): moves kept were the ones that improved evidence without harming the claim's byte-level contract —
the alias/fd question, the trap-operand question and the eval question were each answered by the cheapest decisive probe
(inode identity, chmod-on-symlink, literal-payload directory names), and the end-to-end runs were spent only after the
deterministic harness had already localized the defect to `$work` re-resolution.

Receipts (each small, text):
 - `.ufo/waves/round-48/w2/TSentAlias/reproduce.txt` — full deterministic suite transcript.
 - `.ufo/waves/round-48/w2/TSentAlias/a-fd-and-chmod.txt`, `a4-sticky.txt`, `b-eval-and-options.txt`, `c-empty-work.txt`.
 - `.ufo/waves/round-48/w2/TSentAlias/exp3-same-uid.txt`, `exp4-cross-user.txt`, `spaced-counted-case.txt`.
