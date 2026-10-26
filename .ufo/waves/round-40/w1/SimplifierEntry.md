VERDICT: defect-found

Item S-2: minimal append-only clarifications for `corpus/knowledge/pacman-exec-environment-r40.md`, plus flags on
sentences that restate TO8/HO rows without adding. The file is byte-identical at the authoring commit and at the lane
tip (`git show bf23805:<entry> | sha256sum` = `2230ccaf4037…c9ef`, same at `f951f28`). One host cell is false; the
rest are ambiguities. No EX rule, no S219–S225 row and no counter predicate is falsified: the C2 counter PASSes at
`bf23805` and still PASSes with the proposed append applied (receipts below).

## Findings

**F1 — defect: EX5's host cell asserts a false host fact** (`…r40.md:25`): "on this host `/tmp` is a tmpfs".
Observed 2026-10-26, read-only:

    $ findmnt -T /tmp
    TARGET SOURCE         FSTYPE OPTIONS
    /tmp   /dev/nvme1n1p1 xfs    rw,nosuid,nodev,noatime,inode64,…
    $ stat -f -c 'fstype=%T' /tmp        -> fstype=xfs
    $ grep -E '\s/tmp\s' /proc/mounts
    /dev/nvme1n1p1 /tmp xfs rw,nosuid,nodev,noatime,inode64,logbufs=8,logbsize=256k,noquota 0 0
    $ systemctl status tmp.mount         -> Active: active (mounted) since Mon 2026-10-26 00:40:57 -03
                                            (03:40:57Z, i.e. before the 06:54:46Z capture)

The mount predates the capture recorded in `.ufo/waves/round-40/frozen/hostcap/capture-meta.txt:1`, so the claim was
already false when written, not merely stale. The claim is also absent from the capture: `hostcap/MANIFEST.sha256`
lists exactly `capture-meta.txt`, `libalpm-shell-strings.txt`, `hooks-needstargets.tsv`, and
none records `/tmp`. Severity: the rule half of EX5 holds (`trans.c:360-372`), only the host clause is wrong; the C2
predicate does not read that cell.

**F2 — ambiguity: the intro's provenance claim is wider than the evidence** (`:13`: "the host column comes from a
frozen read-only capture"). The counter re-derives host values for EX4 and EX6 only
(`tools/check-exec-environment-r40.py:322-325`), which matches the recheck line (`:3`, "the two host values"). EX2's
host cell instead applies EX2 to the round-39 capture (S218/TO8), and the host facts in EX1 (`root /`), EX5 (tmpfs)
and EX7 (`grep -c 'could not satisfy dependencies' /var/log/pacman.log`, 0 today — I ran it) are in no frozen capture.

**F3 — ambiguity: the Boundary row list is wrong in both directions** (`:43`: "EX1–EX3 and EX5 have no host instance in
the capture"). EX2's host cell does rest on a capture (S218), so "no host instance" misdescribes it; and EX7/EX8, whose
host cells also hold no captured measurement, are omitted.

**F4 — ambiguity: the form of a `NeedsTargets` line is unstated.** EX6 (`:26`) says "its matched trigger targets on
stdin" and EX8 (`:28`) says Path triggers match "as the package's file list names them, relative to the installation
root", but no row says the stdin lines are those same strings. Source: `hook.c:275`, `:290`, `:304` add
`filelist.files[f].name`; `_alpm_hook_feed_targets` copies `(*pos)->data` (`hook.c:475`); S224
`alpm-hooks.5.asciidoc:61-67`: "Paths refer to the files in the package archive; the installation root should *not* be
included in the path."

**F5 — ambiguity: EX4's `<scriptlet>` and EX5's value are two forms of one path with no marker.** EX4 (`:24`) prints
`/usr/bin/bash -c '. <scriptlet>; …'`; EX5 (`:25`) gives the value `tmp/alpm_XXXXXX/.INSTALL`. `trans.c:398` sets
`scriptpath = scriptfn + strlen(handle->root) - 1`, so the command line carries the **in-root** path (root `/` leaves
`/tmp/alpm_XXXXXX/.INSTALL`) and never the host path — the distinction matters for `--root` other than `/`. A reader who
fills `<scriptlet>` from EX5 gets a different string (harmless only because cwd is `/`, EX1).

**F6 — ambiguity: EX7 states the abort case but not continuation, Post scope, or the citation gap.** `:27` says the
Depends failure stops the phase "only for a hook carrying `AbortOnFail`". It does not say that without it the next Pre
hook runs: `hook.c:660-662` sets `ret = -1` only with `abort_on_fail`, and `hook.c:667-669` breaks only when
`ret != 0 && when == ALPM_HOOK_PRE_TRANSACTION`. A PostTransaction hook with `AbortOnFail` gets a parse warning
(`hook.c:141-143`) and cannot stop anything (`trans.c:238` calls `_alpm_hook_run(…, POST_TRANSACTION)` and discards
the result). Its source cell cites S224 `:83-85` (`Depends` only); the `AbortOnFail` scope is at
`alpm-hooks.5.asciidoc:87-89`.

**F7 — ambiguity: rely-on item 3 asserts scriptlet EOF without a source in the entry.** `:34` "end-of-file for
everything else" is right — `trans.c:410` calls `_alpm_run_chroot(handle, SCRIPTLET_SHELL, argv, NULL, NULL)` — but no
EX row records the null callback for scriptlets, so the claim is only derivable by opening `:410` (cited bare in EX4's
source cell, which does not mention the callback).

**F8 — ambiguity: EX3's host cell leans on what Boundary 3 excludes.** `:23` says variables "exported in the shell that
ran pacman (and kept by sudo) reach the command"; `:45` puts "the environment that reaches pacman itself (sudo's
`env_reset`…)" outside the entry. EX3 itself only guarantees pass-through of whatever pacman's process holds; the
parenthetical should not be read as a sudo claim.

## Flags — sentences that restate TO8/HO rows

- `:33` rely-on item 2: "logged line by line under `[ALPM-SCRIPTLET]` (EX2, TO8)" — the tag clause is TO8's (S216);
  EX2 supplies only the merged stream. TO8 is already named at `:8-9`, so the clause adds nothing. Keep the item as the
  summary it says it is; no append is needed (it is not wrong, only duplicated).
- `:21` EX1's parenthetical "(hook `Exec` commands, install scriptlets and `ldconfig`)" restates TO8's command set; it
  earns its words only as EX1's scope. No append.
- `:26` EX6's host clause "a file in `/etc/pacman.d/hooks` replaces the same-named file in
  `/usr/share/libalpm/hooks`" restates HO2 (`corpus/knowledge/pacman-hook-order-r38.md:22`) without a pointer. It is
  nonetheless the entry's only definition of "effective", so it adds that definition; a future rewrite should write
  "effective (HO2)" and drop the rest.
- `:27` EX7's "stops the PreTransaction phase … only for a hook carrying `AbortOnFail`" restates HO4's conditional
  (`pacman-hook-order-r38.md:24`) while adding a new failure kind (a Depends skip, where no command runs). It adds;
  the proposed EX7 bullet carries the part HO4 does not.
- `:14-15` repeats four items already listed at `:10-12`; its only new content is the round-39 origin. Provenance —
  keep, do not append.
- `:22` EX2's host cell restates TO8's tag and adds the merged-stream reading. It adds; leave it.

## Proposed text (exact; append at end of file, after `:45`)

```markdown

## Round-40 clarification (append-only, 2026-10-26)

- **EX5 host clause withdrawn.** "on this host `/tmp` is a tmpfs" is false: `/tmp` is xfs on
  `/dev/nvme1n1p1` (`findmnt -T /tmp`; `tmp.mount` active since 2026-10-26 00:40:57 -03, before the
  06:54:46Z capture), and no frozen capture holds the fact.
- **Host-column provenance.** Only EX4/EX6 hold values the recheck re-derives from `hostcap/`; EX2's reads
  the round-39 `[ALPM-SCRIPTLET]` lines (S218, TO8). The other host cells add no captured measurement:
  EX3's and EX8's state a rule consequence only, and EX1's root-`/` parenthetical and EX7's live `grep -c`
  (0, 2026-10-26) are host facts no frozen capture holds. So the intro's "the host column comes from a
  frozen read-only capture" covers EX4/EX6 only, the Boundaries "EX1–EX3 and EX5 have no host instance in
  the capture" is superseded here, and EX3's "(and kept by sudo)" asserts no sudo behaviour: which
  variables sudo keeps is Boundary 3's subject.
- **EX6/EX8 targets.** The `NeedsTargets` lines are the matched `filelist.files[f].name` strings (hook.c:275,
  :290, :304) — root-relative, no leading `/`, the form S224 alpm-hooks.5.asciidoc:61-67 requires of
  `Target` — so opening a target means prefixing the installation root.
- **EX4/EX5 scriptlet.** EX4's `<scriptlet>` is the in-root path, not the host path — trans.c:398 strips the
  root prefix (root `/` leaves `/tmp/alpm_XXXXXX/.INSTALL`) — and EX5's value is that string relative to
  `<root>`; the run call (:410) passes a null input callback, so a scriptlet also reads end-of-file on
  stdin (rely-on item 3).
- **EX7 continuation.** A `Depends` skip in a Pre hook without `AbortOnFail` lets the next Pre hook run
  (hook.c:660-668); `AbortOnFail` on a PostTransaction hook warns at parse (hook.c:141-143) and cannot stop
  the transaction (trans.c:238 discards the Post result); S224 `alpm-hooks.5.asciidoc:87-89` states that
  scope, outside the `:83-85` EX7 cites.
```

24 added lines, 283 words; the receipt is the same bytes at
`.ufo/waves/round-40/w1/SimplifierEntry/proposed-append.md` (sha256 `24787fcc…41b9`). It adds no `| EX… |` row and no
duplicate `## ` heading, so the counter's row/heading checks are untouched.

## Verification

- Baseline at the authoring commit, lane repo: `python3 tools/check-exec-environment-r40.py --revision bf2380503b8e4a5d33162026854b0b7b66d18b86`
  → `result PASS, rules_verified 8, duplicate_rows 0, duplicate_headings 0, source_ok 1, counts_ok 2,
  novelty_base_hits 0, exit 0` (`.ufo/waves/round-40/w1/SimplifierEntry/baseline-bf23805.json`).
- Append applied on a `--shared` clone of the lane at `f951f28` (clone toplevel verified; identity
  `fixture@shokunin.local`; commit `c482aa9008fe3341346d07f2652d70ec6454e70f`), then
  `python3 tools/check-exec-environment-r40.py --repo <clone> --revision c482aa9`
  → `result PASS, 8, 0, 0, 1, 2, 0, exit 0` (`.ufo/waves/round-40/w1/SimplifierEntry/append-counter.json`); the diff is
  `append.diff` (24 insertions, 0 deletions).
- Every line cited in the append was re-read in the pinned snapshots: `hook.c:275,290,304,475,519-526,653,660-669,141-143`,
  `trans.c:357-358,398,410,238`, `util.c:628,666,679,683,692,694,695,698,722-726`, `alpm-hooks.5.asciidoc:61-67,87-89,91-93`.

## Tradeoff and limits

The append grows the entry by 24 lines to fix one false host cell and four reader-facing gaps. If fewer survive, drop
the last clause of the provenance bullet (`EX3's "(and kept by sudo)"…`) and the `:87-89` clause of the EX7 bullet
first — they are the two trims that lose evidence precision only, not a fact. I did not edit the lane, did not run a
transaction (paused host-wide), did not install any tool, and did not re-run the C1 counter (not this item). I could
not date the `/tmp` mount earlier than its `tmp.mount` active-since time; the mount already predates the capture, which
settles the cell. Scratch removed.
