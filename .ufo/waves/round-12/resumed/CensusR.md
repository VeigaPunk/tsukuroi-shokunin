# CensusR — round-12 resumed C1: root-directory metadata arm

Seat: executor (leaf, round-12 resumed). Report is author-side seat evidence; it is **not**
independent non-author verification. No tests, selftest, census run, build, lint or formatter
was executed (contract: parent runs checks once after integration). All findings below are
static reads plus the read-only shell probes listed in §7.

## 1. Files and landing state

| File | State |
|---|---|
| `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh` | **modified** (only file this seat wrote in the repo, plus this evidence file) |
| `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-12/resumed/CensusR.md` | this report |

`sha256sum tools/tsukuroi-census.sh` → `f739284b5821d5d096aedb6b36c0d021bb3d0be8706a5f7a31688759a6a1b449`
at report time; `wc -l` → 2679. Starting HEAD `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`.
The inherited `.ufo/waves/round-12/Census.md` did not exist; the inherited script was the
unmodified baseline (`1045244387ffcd5d…`, 2402 lines), re-verified by read before editing.
Other modified files in `git status` are sibling seats' concurrent work, not this lane's.

## 2. Contract as implemented (exact)

Environment seam: `TSUKUROI_ROOT_DIR`; declared with `${TSUKUROI_ROOT_DIR-/}` (not `:-`), so an
explicitly empty override becomes an unavailable root and can never silently select live `/`.
Default (unset) is `/`. `root_src=default|override` records which case applied.

Probe: one `cap env LC_ALL=C stat -L -c '%04a %u %g %F' -- "$ROOT_DIR"` is the sole validator.
`stat -L` resolves symlinks; `%04a` pins a four-digit octal mode; `cap` keeps a failure from
tripping `set -e` (a bare substitution would exit 1 = DEGRADED). Overrides are classified
before stat by `root_locator_class()`: `absolute|empty|relative|unsafe`, where "absolute" means
`/` + only `[A-Za-z0-9._/+-]`. Empty, relative and unsafe overrides are BLOCKED without stat;
the raw caller path is never echoed (a value like `/x root_mode=0755` can neither forge a token
nor reach stat). For accepted absolute paths the path is printed as `root_dir=<path>`.

Fields appended to the `PLANE packages` line, in this fixed sequence:

```
root_status=ok|unavailable(...)|non-directory(...)|mode-unparseable(...)
root_mode=<%04a|unknown> root_uid=<uid|unknown> root_gid=<gid|unknown>
[root_type=symlink(unresolved)]
root_euid=<euid> root_owner_write=<present|absent|unknown>
root_owner_search=<present|absent|unknown>
[root_report=owner-write-absent[,owner-search-absent] root_intent=not-assessed]
root_src=<default|override> root_dir=<absolute path|empty|relative|unsafe>
```

Decision table (parent ruling 2026-10-20, after `systemd 261.2 /usr/lib/tmpfiles.d/root.conf
z / 555` was found):

| Condition | Root arm | Verdict effect |
|---|---|---|
| directory, metadata readable, owner w+x present | `root_status=ok`, both `present` | HEALTHY |
| directory, owner-write absent (e.g. 0555/1555) | `root_status=ok`, `root_owner_write=absent`, `root_report=owner-write-absent root_intent=not-assessed` | **report-only; stays HEALTHY** |
| directory, owner-search absent (e.g. 0644) | same shape with `owner-search-absent` | **report-only; stays HEALTHY** |
| directory, both absent (e.g. 0400) | `root_report=owner-write-absent,owner-search-absent` | **report-only; stays HEALTHY** |
| metadata unavailable (missing/EACCES/dangling/loop) | `root_status=unavailable(stat=rc=N errno=missing|permission-denied|symlink-loop)`, mode/uid/gid/bits `unknown` | **BLOCKED** |
| path exists but is not a directory | `root_status=non-directory(type=…)`, mode/uid/gid actual, bits `unknown` | **BLOCKED** |
| mode string not octal | `root_status=mode-unparseable(...)`, mode/uid/gid/bits `unknown` | **BLOCKED** |
| empty/relative/unsafe override | `root_status=unavailable(override=empty|relative|unsafe)` | **BLOCKED** |

Owner bits are parsed with `8#$mode` and masks `0200`/`0100`; special bits are verdict-neutral
and ride `%04a` (1777, 2755, 1555). No universal 0755 requirement, no mount inference, no
writability claim, no "wrong/read-only" wording. `root_intent=not-assessed` states the census
does not assess whether the mode is declared policy.

Composition/verdict: the arm publishes `ROOT_V`/`ROOT_NOTE`; `main` calls `probe_packages`,
then `probe_root_meta`, folds `PKG_V=$(worse "$PKG_V" "$ROOT_V")`, and emits
`PLANE packages: <verdict> (<PKG_NOTE>; <ROOT_NOTE>)`. Because composition happens at emit
time, the evidence survives **every** `probe_packages` early return (missing binary, db.lck,
`-Qq` failure/empty, `-Qkk` rc, sample `error:`). Plane order, rollup field order
(`packages systemd drivers journal update-safety oom`), verdict vocabulary and exit map
(0/1/2) are unchanged.

Vocabulary change vs the dispatch card: the card said "worsen verdict ... as named DEGRADED";
the parent's later ruling (IRC, 2026-10-20) superseded it with report-only owner bits because
0555 is the host's declared mode. This report follows the later ruling; unavailable metadata
and non-directories still worsen to BLOCKED.

## 3. Selftest harness changes (no case was run)

- `fx_default` creates `$FX/root` and **explicitly** `chmod 0755` (umask 077 would make a bare
  mkdir 0700).
- `check()` common env sets `TSUKUROI_ROOT_DIR="$FX/root"` before `"${EXTRA_ENV[@]}"`.
- `check()` now asserts, on **every** case, that the packages line contains
  `root_status=…root_mode=…root_dir=` and `root_dir=<configured root>`
  (`ROOT_EXPECT`, default `$FX/root`). A live-`/` leak or a missing arm fails the case; this is
  the universal "survives every early return" proof. Override cases set `ROOT_EXPECT`
  explicitly; it and `EXTRA_ENV` reset after each case.
- `fx_hash` now digests entry type/mode/owner/group (`find -printf '%y %m %U %G %p'`, stderr
  suppressed, `|| true`) **plus** regular-file content. A chmod/ownership change on an empty
  fixture root is now inside the zero-mutation proof. Permission errors cannot abort under
  `pipefail`.
- Cleanup trap restores `chmod -R u+rwx` on the temp tree before `rm -rf` (temp path only).
- `skip()` prints a named skip and is not counted as pass or fail; two skip lines are
  registered: non-root-owned fixture (needs `CAP_CHOWN`) and the EACCES/000-parent case
  (unreadable-subtree residue, and euid 0 bypasses DAC).
- C1ReviewR final closures applied: uid/gid stat fields are validated as digits
  (`root_status=unavailable(parse=uid|gid)` otherwise), and the per-case root identity
  assertion now requires a field boundary (`root_dir=<expect>` followed by space or `)`),
  not a bare substring.

Static case count: `grep -cE "^  check(_cli)? '"` → **97** = baseline 77 `check` + 3
`check_cli` + 17 new `check` cases. Expected summary (unrun):
`TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)`.

### Exact new case labels (all prefixed `(R12-C1)`)

Healthy / report-only:
1. `healthy: C1 root arm — 0755 owner bits present (R12-C1)`
2. `healthy: C1 root arm — 0555 owner-write absent is report-only (R12-C1)`
3. `healthy: C1 root arm — owner-search absent independently (R12-C1)`
4. `healthy: C1 root arm — both owner bits absent, both named (R12-C1)`
5. `healthy: C1 root arm — 1777 sticky parses as octal, bits present (R12-C1)`
6. `healthy: C1 root arm — 2755 setgid does not disturb owner bits (R12-C1)`
7. `healthy: C1 root arm — 1555 sticky with owner-write absent, report-only (R12-C1)`

Blocked metadata / locator:
8. `blocked: C1 root arm — missing metadata BLOCKED with explicit unknowns (R12-C1)`
9. `blocked: C1 root arm — regular file is a non-directory (R12-C1)`
10. `blocked: C1 root arm — dangling symlink is unavailable, not a pass (R12-C1)`
11. `blocked: C1 root arm — symlink loop is unavailable, never a pass (R12-C1)`
12. `blocked: C1 root arm — empty override never falls back to live / (R12-C1)`
13. `blocked: C1 root arm — unsafe override rejected, raw path not echoed (R12-C1)`

Early-return survival (root evidence still on the line):
14. `blocked: C1 root arm survives pacman=missing early return (R12-C1)`
15. `blocked: C1 root arm survives db.lck early return (R12-C1)`
16. `blocked: C1 root arm survives empty-db early return (R12-C1)`
17. `blocked: C1 root arm survives sample-rc early return (R12-C1)`

Pinned finding patterns: four-digit `root_mode=0555 ` (not a `555` substring), independent
`root_owner_write`/`root_owner_search`, combined `root_report`, special-bit modes parsed as
octal, explicit `unknown` triples on unavailable, `root_src`/`root_dir` identity (also universally
asserted), and BLOCKED-not-pass for missing/file/dangling/loop/rejected overrides.

## 4. Parent/reviewer rulings incorporated

- C1ReviewR F-A: owner-bit absence report-only (later ruling) — done.
- C1ReviewR F-B: unavailable/unparseable carry explicit `root_mode/root_uid/root_gid` unknowns — done.
- C1ReviewR F-C: `${TSUKUROI_ROOT_DIR-/}` so empty override cannot fall back to `/` — done.
- C1ReviewR F-D: selftest asserts the configured fixture root identity in all cases — done in `check()`.
- FixtureReviewR: `fx_hash` metadata + no 000 subtree; `chmod -R u+rwx` trap; one `stat -L`
  validator (no `[ -d ]` gate); `root_status=unavailable/non-directory` tokens — done.
- SecurityR D1: unsafe overrides rejected before stat, no raw path echo, empty/relative also
  BLOCKED; errno matching uses the `": <strerror>"` suffix and the safe charset excludes `:` and
  whitespace, so path text cannot be matched as the reason — done.
- ClaimCriticR: `%04a` format, verdict independent of euid/ownership, metadata in `fx_hash`,
  `root_intent=not-assessed`, no "wrong/unspecified/no baseline/read-only" wording — done.

## 5. Consumer-visible behavior (live, static prediction only)

Measured read-only host facts (re-observed this seat): `stat -c '%04a|%a %u %g %F' /` →
`0555|555 0 0 directory`; `stat -c '%04a' /tmp` → `1777`. Therefore a live run is expected
**[INFERENCE, not executed]** to append:
`root_status=ok root_mode=0555 root_uid=0 root_gid=0 root_euid=1000 root_owner_write=absent
root_owner_search=present root_report=owner-write-absent root_intent=not-assessed
root_src=default root_dir=/`
with the packages verdict unchanged by the arm (report-only). The CensusScribe `root_mode=`
count gate should see exactly one token on the single `PLANE packages` line, including
BLOCKED-root branches (explicit `root_mode=unknown`).

## 6. Risks and gaps

1. **Unrun.** No selftest, live census, `bash -n`, mutation sweep or build/lint was executed
   here; the 97-case and live-line statements are static/predicted, not observed. Parent must
   run `bash tools/tsukuroi-census.sh --selftest` once after integration.
2. **Live BLOCKED arm is fixture-only.** `stat /` needs search only on path prefixes and `/`
   has none, so DAC cannot make the live probe EACCES (ClaimCriticR K4). BLOCKED is proven
   hermetically (missing/file/dangling/loop/rejected override), not live.
3. **EACCES path unexercised.** The `permission-denied` errno class has no hermetic case: a 000
   parent was dropped per FixtureReviewR, and under euid 0 DAC is bypassed. The classifier is
   static-only; a reviewer should treat it as unverified behavior.
4. **Non-root ownership not fixtureable.** Without `CAP_CHOWN` a fixture cannot be owned by a
   different uid. The verdict is ownership-independent by design (bits only), and `root_uid/gid`
   are printed facts; no case claims non-owned behavior. This is a named gap, not a pass.
5. **Mode-unparseable is unreachable with GNU `stat`** (defensive branch only). `%04a` is GNU
   coreutils behavior; host coreutils is 9.11-2 (measured earlier by sibling seats).
6. **Special-bit semantics are not graded.** setuid/setgid/sticky are printed via `%04a` and
   are verdict-neutral; no source in this lane grounds them as root-health facts.
7. **Selftest count is static** (97 = 94 `check` + 3 `check_cli`). The printed summary is
   `PASS+FAIL`, so a harness regression in case registration would not be caught by this report.

## 7. Commands and exit codes (all read-only, this seat)

| Command | rc | Result |
|---|---|---|
| `stat -c '%04a|%a' -- / /tmp` | 0 | `0555|555`, `1777|1777` |
| `bash -c 'echo $((8#0755)) …'` (octal + `${X-/}` check) | 0 | 493 365 1023 1517 877 256 420; unset=`/`, empty=`` |
| `grep -nE "^  check '.*R12-C1" tools/tsukuroi-census.sh` | 0 | 17 labels (listed §3) |
| `grep -cE "^  check(_cli)? '" tools/tsukuroi-census.sh` | 0 | 97 |
| `sha256sum` / `wc -l` tools/tsukuroi-census.sh | 0 | `f739284b…`, 2679 |
| `git status --short` | 0 | census file modified; sibling files also modified concurrently |

Not run: `--selftest`, live census, `bash -n`, mutation sweep, any package/systemctl/service
operation. No installs or upgrades. No sudo, no host writes, no git mutation. Secrets were not
read (none needed).

## 8. Handoff

Parent: run once after integration:
`bash /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/tsukuroi-census.sh --selftest`
(expect exit 0 and the 97-case summary above) and one live read-only run; then verify exactly
one `root_mode=` token on the `PLANE packages` line and that `/` 0555 is report-only.
C1ReviewR was notified for static re-review; this file is the durable evidence anchor.
