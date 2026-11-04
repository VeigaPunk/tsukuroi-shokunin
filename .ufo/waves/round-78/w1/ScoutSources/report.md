# ScoutSources — round 78

Axes: **depth** and **operability**. Scope: source evidence only; no round-admission verdict.

## Independent reopening

Both exact v262 upstream URLs were independently fetched with curl (exit 0 each), retained in this directory, and hashed with sha256sum alongside the frozen `before/` files. All four hashes match the two `before/expected.json` pins:

| Source | URL | SHA256 |
|---|---|---|
| manager | https://raw.githubusercontent.com/systemd/systemd/v262/src/journal/journald-manager.c | `428dc8308d5caf70faee074e87888264c3708aa8e24c6069854790b952a7ffa2` |
| manual | https://raw.githubusercontent.com/systemd/systemd/v262/man/journalctl.xml | `d54bbede45d5b1e3dc856da9624649ef8cb0829731597c212be303a76a1edbdd` |

Durable receipt: `.ufo/waves/round-78/w1/ScoutSources/receipts.json`. Byte receipts: sibling `journald-manager.c` and `journalctl.xml`.

## Exact frozen-claim wording audit

Read the Round-78 block from **commit `07a607df1a5157daafc91bb5c26858af14415f43`**, not merely the mutable examples or current scorecard. Its source paragraph at SCORECARD.md:6506–6511 agrees with the reopened implementation:

| Frozen wording | Located evidence | Finding |
|---|---|---|
| :119–121 skips filenames without `.journal` or `.journal~` | `manager_determine_path_usage`:119–121 tests the conjunction of both negated suffix checks, then continues | Accurate: either suffix qualifies; it is not a filename/content validity check. |
| :123 uses `AT_SYMLINK_NOFOLLOW` | :123 `fstatat` flag | Accurate; this does not mean the containing path itself cannot traverse a symlink. |
| :125 skips a failed stat | :123–126 negative return, debug message, continue | Accurate; it does not fail the entire scan at this point. |
| :128–129 skips non-regular files | `!S_ISREG(st.st_mode)` then continue | Accurate; no-follow stat makes a symlink fail this regular-file test. |
| :131 adds `(uint64_t) st.st_blocks * 512UL` | :131 exact expression | Accurate; the expression does not use `st_size`. |
| :114 separately obtains availability from `ss.f_bsize * ss.f_bavail` | :110 successful fstatvfs prerequisite; :114 assignment to `*ret_free` | Accurate; availability is not the selected-file sum. |

The function definition occupies :91–135. It opens the supplied directory (:105), zeroes `*ret_used` (:115), and scans directory entries (:116). Textually located caller `cache_space_refresh`:161 supplies `storage->path` and separate used/available outputs, assigned to cache fields at :165–166. This supports the narrow upstream helper interpretation; no installed-Arch line-number or journalctl call-chain equivalence is claimed.

The frozen C1 row also explicitly requires companion accuracy and makes false upstream interpretation a kill condition. The six JSON examples alone cannot discharge that conjunct. Their descriptor outcomes are consistent with these branches: U1=4096, U2=8192, U3–U6=0. This is a source reading, not an executed manager fixture or a reviewer-binding verification.

## Draft located Gate records

Each quoted payload below is verbatim source text, with only line-break whitespace normalized. Each quote is independently at most 25 whitespace-delimited words. These are drafts for L1; no production source rows were written.

### Admit — S327, narrow manager semantics

- Source: manager URL above, v262; hash above; function :91–135.
- :119–121 quote (7 words): `if (!endswith(de->d_name, ".journal") && !endswith(de->d_name, ".journal~")) continue;`
- :123 quote (8 words): `if (fstatat(dirfd(d), de->d_name, &st, AT_SYMLINK_NOFOLLOW) < 0) {`
- :125 quote (1 word): `continue;` (within the failed-stat branch :123–126).
- :128–129 quote (3 words): `if (!S_ISREG(st.st_mode)) continue;`
- :131 quote (6 words): `*ret_used += (uint64_t) st.st_blocks * 512UL;`
- :114 quote (5 words): `*ret_free = ss.f_bsize * ss.f_bavail;`
- Admitted statement: This helper sums allocated 512-byte block units only for matching-suffix regular entries whose no-follow stat succeeds; it obtains filesystem availability separately.
- Boundary/falsifier: different version/source bytes or a contradictory located branch require renewed assessment. No claim about recursive traversal, full journal validity, or physical exclusive disk ownership follows.

### Reject — S328 as sole proof of manager filtering

- Source: manual URL above, v262; hash above; `--disk-usage`:941–948.
- :943–944 quote (15 words): `This shows the sum of the disk usage of all archived and active journal files.`
- Observed support: journalctl's documented disk-usage display includes archived and active journal files.
- Rejected inference: this passage alone proves the internal manager's filename-suffix predicate, `AT_SYMLINK_NOFOLLOW`, failed-stat handling, `S_ISREG` filtering, or block multiplier. None of those implementation details occurs in this passage. The manager code, not the broad manual wording, supplies them.
- Flip condition: a located version-pinned passage explicitly establishing those internal predicates, or direct relevant implementation evidence. This rejects a proposed evidentiary use, not the manual's reliability.

## Confidence and limitations

High confidence in byte identity, located lines, and the frozen source-paragraph audit. `xd://lsp` returned **No such tool**; no semantic server was available, so caller observations above are literal source reading, not semantic-reference proof. No cold empty result was treated as absence. No exported-contract change is proposed.

No host probes, tests, builds, package transactions, installs, clones, git mutations or scratch directories were used. Only seat-owned artifacts were written. Reviewer digest binding, final integrated companion text, complete C2 registry accuracy and outside admission remain outside this source-only assignment.

## Internal quality check (not an outside verdict)

Accuracy 4: independently matching hashes and exact frozen wording; no runtime manager execution. Completeness 4: both URLs, all named lines, admit/reject and source paragraph covered; semantic server unavailable. Clarity 4: evidence and inference separated; detailed audit table retained for integrator. Actionability 4: ready located Gate drafts; production integration belongs to L1. Conciseness 4: bounded source report, with repeated hashes needed for receipts. Mean 4.0. Highest-impact improvement for later authority: pair this source receipt with the separate executed-helper and final-companion reviews; do not promote this report to either. A user should accept the narrow evidence, not infer a round verdict.
