VERDICT: supports

# C2-24 — the entry's recheck line, and live drift of the round-39 C2 capture

Seat `C2ExecRecheckLive`. Read-only: no lane file, no host package/service/mount/sysfs, no fleet path and no
sibling lane was touched. Scratch under `/fast/scratch/hyaku/tsukuroi-r39/C2ExecRecheckLive/` was removed at
the end; receipts are in `.ufo/waves/round-39/w1/C2ExecRecheckLive/`. No tool was installed or upgraded.

Short answers: **the recheck line is not runnable verbatim** (`<REV>` is an unsubstituted metavariable and bash
rejects the line); **with a commit substituted it runs and PASSes** at the entry commit, at the current lane tip
and with a short hash. **The live host has zero drift from the capture** on all three compared artifacts
(`/var/log/pacman.log`, `hook-owners.tsv`, `hook-when.tsv`), and hook file bytes still match the round-38 byte
baseline 70/70. Two wording-level notes below; neither falsifies a declared claim.

## 1. Recheck line as written — not runnable verbatim

Entry line: `corpus/knowledge/pacman-transaction-order-r39.md:3`

    recheck: `python3 tools/check-transaction-order-r39.py --revision <REV>` re-verifies every TO row …

`--revision` is mandatory (`tools/check-transaction-order-r39.py:155`, `ap.add_argument('--revision',
required=True)`), so the placeholder cannot be omitted, and pasted literally it is shell syntax:

    $ printf '%s\n' 'python3 tools/check-transaction-order-r39.py --revision <REV>' > literal.sh && bash -n literal.sh
    literal.sh: line 1: syntax error near unexpected token `newline'
    literal.sh: line 1: `python3 tools/check-transaction-order-r39.py --revision <REV>'
    bash_n_exit=2

Observed in `.ufo/waves/round-39/w1/C2ExecRecheckLive/observed.txt` §A (receipts `literal-recheck.sh`,
`literal-recheck.err`). `<REV>` is defined nowhere in round 39; the only definition in the corpus is
`corpus/knowledge/adjacency-anchors-r19.md:3` ("where `<REV>` is a landed lane commit resolved under
corpus/QUALITY.md criterion 27"), and `corpus/QUALITY.md:116` uses the same placeholder undefined. So the line
is runnable under the repo's by-example convention, not verbatim. Proposed wording in note N1.

## 2. Recheck with `<REV>` substituted — PASS at three revisions

    rev=4078eb236c7c67f343c76956c587d0a356e0bf5c exit=0 result=PASS 8 2 1 0 0 0
    rev=394e1ba4fab39a417abe66a7802f87cf1ff8dd61 exit=0 result=PASS 8 2 1 0 0 0
    rev=4078eb2                                    exit=0 result=PASS 8 2 1 0 0 0

(fields: `rules_verified counts_ok source_ok duplicate_rows duplicate_headings oracle_violations`). `4078eb2` is
the entry commit (`round-39: C2 libalpm transaction order entry; SOURCES S213-S218 …`), `394e1ba` the lane tip
at run time. The whole predicate holds: 8 rules verified, 2 host counts matched, source line OK, no duplicate
row or heading, 0 oracle violations. Receipts `recheck-*.json`.

Two context facts: the dispatch tip `2e1c2a4` is an ancestor of the current tip `394e1ba` (only
`round-39: w1 spec (70 seats, v2) validated; dispatch handed to the orchestrator` landed in between), and
`git diff --stat 2e1c2a4 394e1ba -- corpus/knowledge/pacman-transaction-order-r39.md corpus/SOURCES.md
tools/check-transaction-order-r39.py .ufo/waves/round-39/frozen/txcapture/` is empty — the entry, its SOURCES
rows, the counter and the capture are byte-identical across that move, and `git status --porcelain` on those
paths is empty.

## 3. `/var/log/pacman.log` vs the capture — zero drift

    $ sha256sum /var/log/pacman.log
    0845c1df31fcccd1b629f3b5c8190c037a572bbfbd6d9e11f81be635b1a4fc67  /var/log/pacman.log
    .ufo/waves/round-39/frozen/txcapture/MANIFEST.sha256: 0845c1df…  pacman.log

The live hash equals the MANIFEST entry for `pacman.log`; size 252016, mtime `2026-10-25 13:12:06.981386572
-0300`, identical to `capture-meta.txt:2`. Both files are 3254 lines with the same tail
(`transaction completed` / `running '35-systemd-update.hook'...`), i.e. no transaction has been logged since
the capture. `sha256sum -c MANIFEST.sha256` inside the capture directory: all four files OK, and the MANIFEST
file's own digest is `cb5cb4f4…` — the value pinned in the entry at line 1 and in the tool at
`tools/check-transaction-order-r39.py:66`.

The counter's two host counts, recomputed from the **live** log with the counter's own `host_counts`
(`tools/check-transaction-order-r39.py:105`) and from the frozen copy:

    live   {"windows": 86, "transactions_started": 60, "scriptlet_tag_outside_commit": 252,
            "scriptlet_tag_total": 441, "running_inside_commit": 0}
    frozen {"windows": 86, "transactions_started": 60, "scriptlet_tag_outside_commit": 252,
            "scriptlet_tag_total": 441, "running_inside_commit": 0}

Identical. Those are the numbers TO1's and TO8's host cells must carry for `counts_ok == 2`
(`tools/check-transaction-order-r39.py:224-226`), so the frozen counts are also the live counts.

## 4. Hook owner and When maps — identical content, collation-dependent byte order

Regenerated with the commands recorded in `capture-meta.txt:3` (owners) and the reconstruction of
`capture-meta.txt:5` (first `When=` per file):

    owners ambient LANG=en_US.UTF-8 : 7250c924…  vs frozen 236039c5…  → one ordering hunk
    when   ambient LANG=en_US.UTF-8 : 76a591a7…  vs frozen 5d56d412…  → one ordering hunk
    owners under LC_ALL=C           : 236039c5…  == frozen 236039c5…  BYTE-IDENTICAL
    when   under LC_ALL=C           : 5d56d412…  == frozen 5d56d412…  BYTE-IDENTICAL

As (path,value) sets both maps are identical in the ambient locale too (`diff <(sort frozen) <(sort live)`
empty for both). The only difference is the relative order of two adjacent lines:

    +/usr/share/libalpm/hooks/gtk4-querymodules.hook	gtk4
     /usr/share/libalpm/hooks/gtk-query-immodules-3.0.hook	gtk3
    -/usr/share/libalpm/hooks/gtk4-querymodules.hook	gtk4

i.e. 70/70 entries present with the same owner and the same `When` value; the capture's byte order is the
C-collation order (glibc `en_US.UTF-8` collation ignores `-`, so `gtk4…` sorts before `gtk-…`). Receipts:
`hook-owners.live.tsv`, `hook-when.live.tsv` (ambient), `hook-owners.live.C.tsv`, `hook-when.live.C.tsv`
(byte-identical), full transcript `observed.txt` §F–G2. The reconstruction that reproduces the frozen bytes
also validates the loose `capture-meta.txt:5` description:

    awk -F= '/^[[:space:]]*When[[:space:]]*=/ {v=$2; gsub(/^[[:space:]]+|[[:space:]]+$/,"",v); print v; exit}' "$h"

Proposed wording in note N2. This is a reproducibility property of the capture's *commands*, not drift: the
counter reads only the frozen files and pins each one by digest
(`tools/check-transaction-order-r39.py:88-101`), so no counter result depends on the live glob order.

## 5. Hook file bytes vs the only hook-byte baseline — 70/70

The round-39 capture pins hook owner and phase but not hook bytes; the round-38 capture
(`.ufo/waves/round-38/frozen/hooks-capture/`, taken `2026-10-26T04:11:58Z`) holds full copies. Live hooks
copied read-only into scratch:

    files_ok=70 failures=0                    (sha256sum -c r38 MANIFEST)
    usr-share-libalpm-hooks: IDENTICAL bytes  (diff -r)
    etc-pacman.d-hooks:      IDENTICAL bytes  (diff -r)

So no hook file changed between the round-38 capture, the round-39 capture and this run; the hook directories'
mtimes are `2026-10-20` (`hookdir-mtimes.txt`). A standing digest of the live hook set is kept at
`hooks.live.sha256` (70 lines, digest of the listing `df901d2f…`) for later comparison.

## 6. Pin and recheck triggers

`pacman -Q pacman` → `pacman 7.1.0.r9.g54d9411-3` (`pacman-version.txt`), the exact version the entry pins
(line 1) and `capture-meta.txt:4` records. The "on-release of pacman" trigger for S208 and S213–S217 has not
fired; the 30d trigger for S218 is untouched. No transaction has been logged since `2026-10-25T13:12:06-0300`,
so the capture's ground is still current at `2026-10-26T06:0xZ`, ~25 min after it was taken.

## Notes — wording-level, neither falsifies a declared claim

**N1 (entry line 3, minor).** The recheck line is not runnable verbatim (§1). Proposed replacement, matching
the sibling wording at `corpus/knowledge/adjacency-anchors-r19.md:3`:

> recheck: `python3 tools/check-transaction-order-r39.py --revision <REV>`, where `<REV>` is a landed lane
> commit resolved under `corpus/QUALITY.md` criterion 27, re-verifies every TO row against the pinned snapshots
> and the two host counts against the frozen capture; on-release of pacman for S208 and S213–S217; 30d for S218

**N2 (capture-meta.txt lines 3 and 5, minor).** The recorded hook commands do not pin the locale, yet the
frozen `hook-owners.tsv` / `hook-when.tsv` bytes are C-collation and the host's ambient `LANG=en_US.UTF-8`
produces a different byte stream with identical content (§4). Proposed: prefix both recorded commands with
`LC_ALL=C; ` (or note "digests are byte-collation; regenerate under `LC_ALL=C`").

## Scope, and what I did not do

- I did **not** judge the truth of any TO row against the pinned source — that is the reviewer seat's item, and
  the counter checks only that each quote sits at its cited lines. No `TO<n>: holds|partly|fails` line is
  emitted by this seat, per the declared kill rule's "seats that judge" wording.
- I ran no pacman transaction, no hook, no service action, no mount, no `unshare`; the host was read only
  (`sha256sum`, `stat`, `pacman -Q`, `pacman -Qqo`, globs, `diff`).
- I did not re-verify the libalpm source snapshots against upstream (the counter's `SRC_SHA` check passed at
  exit 0, `tools/check-transaction-order-r39.py:58-93`, but I did not fetch anything).
- I did not run the round-39 C1 counter or any sibling item.
- `git status --porcelain` shows `M PROVINCE.md` and `M SKILL.md` in the lane worktree; those are not mine — I
  wrote only inside `.ufo/waves/round-39/w1/C2ExecRecheckLive/`.

## Receipts (`.ufo/waves/round-39/w1/C2ExecRecheckLive/`)

`observed.txt` (full transcript, one run of `reproduce.sh`), `reproduce.sh` (re-runnable, read-only, writes only
into its own directory), `literal-recheck.sh` + `literal-recheck.err` (§1), `recheck-4078eb2*.json`,
`recheck-394e1ba*.json` (§2), `live-counts.json` (§3), `hook-owners.live.tsv`, `hook-when.live.tsv`,
`hook-owners.live.C.tsv`, `hook-when.live.C.tsv` (§4), `r38-manifest-check.txt`, `hooks.live.sha256`,
`hookdir-mtimes.txt` (§5), `pacman-version.txt`, `pacman-log-tail.txt`, `pacman-log-final.sha256` (§6).
