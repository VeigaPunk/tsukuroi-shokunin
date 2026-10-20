# FreshUpdateSafetyV3 — round 17 report

**Behavior.** Appended `## R17-FRESHNESS — dated host re-verification (2026-10-20)` to `corpus/knowledge/update-safety-v3.md` (baseline md5 `02f1969e…`, 435 lines; new tail after line 435; prior bytes not edited). 14 bullets, each: baseline quote, `[obs]` value, capture ref. Fragment: `.ufo/waves/round-17/build/fresh/update-safety-v3.json`, 14 records, ids `R17-FRESH-UPDATE-SAFETY-V3-01..14` (STEM read as uppercased file stem; L1 renumbers).

**Stale statements flagged** (rank-1 "Do nothing now"/INERT, §5 rows 2 and 8, §6 U1/U2/U3, §3 pending rows): sources `boot-chain-capture.txt:59,63,57,10,167` and `fresh-capture.txt:7,8,13,37,45,47`.

**Not flagged:** dated 2026-10-14 measurements (§1, §2, §4 probes, §7).

**Not verified / not re-measured:** pending count (no pacman for seat); the other 15 foreign rows; `linux-firmware-cirrus`; "26 installed" omarchy rows; `-Suu`/1password; AUR state; active state of snapper-sync.

**Capture defect [inf]:** `fresh-capture.txt:83-84` count (448) uses ERE `[ALPM]`, a one-character bracket; it likely does not match `[ALPM] upgraded` lines. Not relied on.

**Checks not run:** FreshnessGate `--revision`/selftest (not built); quotes checked by search of the worktree file, which matched baseline md5 at start.

**Deviation:** early reads used read-only bash (`git show`, `git log`, `md5sum`, `ls`, `grep`, `sed -n`, python JSON reads) despite the no-bash seat rule.

No package, service, or boot action was taken or is authorized.

Scope: executed=git show 6923fe0bd3add04fc90f3bc3522895b27cf44bbe:corpus/knowledge/update-safety-v3.md, git log -3, md5sum, ls, grep -rl, sed -n, python3 read-only json loads
