VERDICT: holds
ROW: PA2
lines checked: frozen/src/be_package.c:555-694

Scope. Row PA2 and its bullet in `## Corrections from the round-41 wave` were read at lane revision
20c327b3f1cf96ad1828792c2ae5db71b5fd9ef7 (`git show 20c327b3…:corpus/knowledge/alpm-package-anatomy-r41.md`;
`diff -q` against the worktree file is empty). The second reader's defects are
`.ufo/waves/round-41/w1/C2RevPA2b.md`; its receipts `.ufo/waves/round-41/w1/C2RevPA2b/probe-final.log`.
Snapshot pin re-checked: `sha256sum frozen/src/be_package.c` =
`24e5890647f80dd953586d8add314b396d0276a37e2f1468f685e90b809db4d7` = `frozen/src/SHA256SUMS:5`.
Host check: `pacman -Q pacman` → `7.1.0.r9.g54d9411-3`, the pinned build, so the seat's probes measure the
pinned source directly. Also read in the same snapshot: `handle_simple_path` 368-393, `alpm_pkg_load`
720-789, `query.c:454-483`.

Every condition the second reader raised is addressed by the correction and independently verified:

1. Exact-name defect → correction sentence 1. `be_package.c:598` is
   `if(strcmp(entry_name, ".PKGINFO") == 0) {`; a member `./.PKGINFO` falls to `:625 handle_simple_path`,
   whose `:380-384` returns 1 (handled) for every other `.`-prefixed path, so `config` stays 0 and
   `:652-653` fires "missing package metadata". Receipt P4: members `./ ./.PKGINFO ./data1` with `.PKGINFO`
   bytes identical to loading P3 (`a1583f859a116afb` both) → `error: missing package metadata …`, rc=1,
   while P3 (exact root name) loads `demo 1.0-1`. The decision-table re-read ("the listing must show a line
   that is exactly `.PKGINFO`; `./.PKGINFO` alone means the file will not load") matches :598 and P4; the
   word "alone" keeps the claim exact for archives that also carry a correctly spelled member.
2. Unparseable-`.PKGINFO` defect → correction sentence 2 = `:600-604`: `parse_descfile(...) != 0` →
   "could not parse package description file in %s" → `goto pkg_invalid`. Receipt P12: one 600000-byte
   line → exactly that message.
3. Later-check defect → correction sentence 3 = `:678-680`:
   `if(_alpm_pkg_check_meta(newpkg) != 0) { goto pkg_invalid; }` after the loop. `grep -rn
   _alpm_pkg_check_meta frozen/src/` returns only the calls at `be_package.c:678` and `be_local.c:635` —
   no definition, so the parenthetical "(body outside the snapshot)" is true. Receipt P13:
   `1.0-1-2`, `1.0-x-1`, `1:1.0-1-2` → "invalid metadata for package … (package version contains invalid
   characters)" while `1.0-`, `-`, `1.0-1:2` load; the correction's hedged "can still refuse" is exact and
   does not overstate the rule the body enforces.

Row clauses unchanged by the correction re-verified in the frozen source: `config = 1;` at `:617` is the
only assignment (`grep -n 'config = \|int config' be_package.c` → `:559`, `:617` only), so only an entry
spelled exactly `.PKGINFO` sets the metadata flag; empty name `:605-608`; empty version `:609-612`; dash
test `:613-616`; `.MTREE` guard `:619 full && strcmp(entry_name, ".MTREE")`; `.BUILDINFO` passed over via
`:625` → `handle_simple_path` `:373-385`; refusal message `:652-655`. Nothing in the row is contradicted;
the correction only narrows "lacks `.PKGINFO`" to the exact root spelling and adds the two refusal paths,
which is where the texts differ, as the section preamble allows.

No new overreach: the correction omits the second reader's explicitly optional items (unreadable-`.MTREE`
archive-scan fallback, the mtree-reader `./` normalization contrast, host-cell remeasure) and claims
nothing beyond :598, :600-604, :678-680 and the cited receipts. `query.c:468`
`alpm_pkg_load(config->handle, strname, 1, 0, &pkg)` passes full=1, so the probes exercised the full-load
path; the negative half of "read only on a full load" (full=0) remains code-read, exactly as the second
reader disclosed, and the correction makes no claim about it.

Not done: no new live probes, no counter or selftest run, no transaction, no write in the lane outside
this report and its receipt.
