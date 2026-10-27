VERDICT: defect-found

# SentMisroot — X-7 misroot and scope sweep (round 46 w1)

Sweep window 2026-10-27T02:22–02:30 -03:00. Every observation below is a read-only command output; I removed
nothing, edited no lane file, ran no C1 counter or census selftest. Receipts: `w1/SentMisroot/scope-sweep-receipt.txt`.
My only writes: that receipt and `/fast/scratch/hyaku/tsukuroi-r46/SentMisroot-5/` (two `sort` temporaries).

Four findings, in severity order: F1/F2 are fleet-root misroots (already cleaned by someone else at 02:28:44);
F3 is a live uncommitted edit of the frozen census tool; F4 is the one that can silently void the round's C2 verdicts.

## F1 — fleet root received 12 stray files (live-fetch byproducts), 02:22:07–02:22:16 (medium; since cleaned)

`git -C /home/vgpnk/Projects/shokunin status --porcelain` at 02:22, 02:26 and 02:27 listed exactly 13 untracked
entries. Twelve were files (386,438 B total), all written inside a nine-second window, none at the fleet root's
tracked paths — a relative-path write from a process whose cwd was the fleet root:

```
btrfs-scrub@.service  190      02:22:11.671
dev-replace.c         39841    02:22:11.147
kstrtox.c             11483    02:22:07.225
scrub.c               100417   02:22:11.358
scrub237.c            57034    02:22:11.789
sha256-live.txt       628      02:22:11.807
sysfs.c               72925    02:22:11.305
systemd.kill.xml      11224    02:22:10.907
tags-linux.txt        121      02:22:13.215
tags-systemd.txt      115      02:22:15.976
tags-btrfs-progs.txt  115      02:22:16.682
vsprintf.c            92345    02:22:07.302
```

Attribution (strong, not certain): `.ufo/waves/round-46/w1/C2ExecLiveSources.md:3` says the eight S246–S248/S242–S244
files "and the S237 file were fetched with `curl -sfL URL -o FILE`". Its receipt dir holds `tags.txt`, and
`cat tags-linux.txt tags-systemd.txt tags-btrfs-progs.txt | sort` equals `sort w1/C2ExecLiveSources/tags.txt`
exactly (`TAGS-IDENTICAL`); the twelve files also carry the frozen bytes (`sha256sum` of each equals the
round-42/44/45 `frozen/src` copy, e.g. `scrub237.c` = `48df2e2f…` = `.ufo/waves/round-42/frozen/src/scrub.c`).
So the seat's `curl … -o FILE` ran with cwd = `/home/vgpnk/Projects/shokunin`.

**Receipt defect inside that seat's own evidence.** The fleet-root `sha256-live.txt` (628 B) has **8** rows and no
`cmdline.c`; the seat's copy at `w1/C2ExecLiveSources/sha256-live.txt` (704 B) has **9** rows, including
`1af5ad98fface0b59694e7565c33be2e37c089cc9a1a841285414ee94546ca9d  cmdline.c`. No live `cmdline.c` existed anywhere
(`find /home/vgpnk/Projects/shokunin /fast/scratch/hyaku/tsukuroi-r46 -maxdepth 4 -name cmdline.c` → empty), and the
fleet-root capture written at 02:22:11 — the same instant as the eight other digests — omits it. The report's claim
that **all** eight S246–S248/S242–S244 files were live-fetched is therefore not established for `cmdline.c`
(its digest matches the frozen row, which is what a fabricated live row would also produce). Smallest remediation:
the seat must paste per-file `curl` exit status (or a `curl -w '%{http_code}'` row) for `cmdline.c`, or drop that row
and say the file was taken from the frozen snapshot.

Harm if left: a subsequent `git add -A` at the fleet root would commit 386 KB of upstream source under names
(`scrub.c`, `sysfs.c`, …) that shadow the lane's frozen-snapshot vocabulary, and any seat reading `scrub.c`
relative to the fleet root would read an unversioned copy rather than a revision-pinned one.

**State now:** at 02:28:44 all 13 entries were gone and `git status --porcelain` at the fleet root is empty.
Not by me.

## F2 — shadow lane tree `kengaku-shokukin/` at the fleet root (medium; since cleaned)

The 13th fleet-root entry was a directory `kengaku-shokukin/` containing exactly one file:
`kengaku-shokukin/.ufo/waves/round-46/w1/R46CritC1Freeze.md` (9187 B, 12 KB tree). The real kengaku lane is
`/home/vgpnk/Projects/shokunin/kengaku-shoku**n**in`; the shadow is a one-letter typo (`-shokukin`) resolved
against the fleet-root cwd. Its mtime, `2026-10-27 02:06:37.472774735 -0300`, is **identical to the nanosecond**
to the real report's mtime (`kengaku-shokunin/.ufo/waves/round-46/w1/R46CritC1Freeze.md`, 9187 B, sha256
`59027753f36a3a61becd6ea1e3e74c36750b05ca724472aa57cfe2c1c0f4fbdf9`), so the correct copy also exists and no
evidence was lost — the stray was a duplicate write (a `cp -p`-style copy or a hard link), not the only one.

Damage model that mattered while it lived: a following seat with the same typo'd path would have appended to the
shadow, and any glob over `kengaku*` at the fleet root would have read the shadow copy as lane content. Nothing
outside the fleet root could reach it, so the blast radius was the uncommitted-worktree status of the fleet repo.

## F3 — live uncommitted edit of the frozen census tool, 02:28:53 (medium; needs a commit-or-revert decision)

At 02:30 the only lane entry outside `.ufo/waves/round-46/` is ` M tools/tsukuroi-census.sh`
(209505 B, mtime `2026-10-27 02:28:53.087645808 -0300`, 10 insertions / 6 deletions, hunks starting at
`@@ -3391`, `-3446`, `-3492`, `-3510`). Content: (a) `|| true` appended to the `planes=$(grep … | paste -sd, -)`
helper in `id_check` (`tools/tsukuroi-census.sh:3394`); (b) a new selftest case
`cli: --identity with --help exits 2, never usage and 0 (R46-C1)`; (c) the `--identity` exclusivity test moved from
after flag parsing to a pre-scan over `"$@"` in `main()` (`:3497-3503`), so `--identity --help` and `--help --identity`
now exit 2 instead of printing usage with 0.

Against the declared kill rule ("a census line at or before :3383 moves"): every hunk starts at or after line 3391,
so the rule's line bound is respected by the edit **as it stands in the worktree**; if it is committed, the
`:3383` bound still holds. Two things it does change, and one it cannot be scored on:

- Behaviour: `--help` no longer wins when `--identity` is also present. That is what the freeze line says
  ("`--identity` takes no other argument (exit 2)"), but the entry `corpus/knowledge/census-identity-r46.md` must
  state the ordering, or a later reader will call it a regression.
- `|| true` only degrades a diagnostic: on a pipeline failure `planes` becomes empty and the comparison fails
  (`bad`), so it cannot turn a real failure into a pass. It is not a false-pass path.
- Scored visibility: `score-census-identity-r46.py` clones a **revision**. An uncommitted worktree edit is invisible
  to it, so right now the wave's `selftest_r46` and `cli_ok` are being measured on a file that differs from what a
  seat just tested. Commit it (with `(R46-C1)` labels intact) or revert it before the C1 scoring run; do not score
  while `git status` shows ` M tools/tsukuroi-census.sh`.

## F4 — the GR2/GR3 measurement instrument was mutated after the counted seats measured it (high)

Commit `b57740c2` ("GR2/GR3 narrowed per counted partly findings …") is not the four-file doc commit its subject
suggests: it also rewrites 41 lines (13 deletions) of `corpus/knowledge/btrfs-scrub-grounding-r45.md`, i.e. the
document `check-scrub-admission-r46.py` hashes per row and the counted reports bind with `SECTION SHA256:`.
The counter's own `--section-hash` (read-only, run from my scratch):

```
--revision a44770491eb5ca15ce9f8b3207309d1af683ffaf
  GR1 fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8
  GR2 a963df81745c7770f73406eda78cfdf6c1355e23c65c17d43b16e3ebeff62781
  GR3 8fa626768b49a98186b5a03fbc348175e5ed73484648b6e68a4277c6907a2800
--revision b57740c2 (current tip)
  GR1 fe77ac765c7dd9f568e0b296ce8c7f8f53de3d8966d6a2029bada662badf9ca8
  GR2 4bf28bcf3682fc5bed1d020601f35d19f696301579d2fe66f8667e7f7602f6da
  GR3 43430a14069598947d225c1f8ae897d9baea1c0e268cb88c2b5ad9e247bbc32c
```

Every counted report on disk still carries the a4477049 values:

- GR2: `V46RevGR2a.md`, `V46CritGR2a.md`, `V46CritGR2b.md` → `a963df81…`
- GR3: `V46RevGR3a.md`, `V46CritGR3a.md`, `V46CritGR3b.md` → `8fa62676…`
- GR1: `V46RevGR1a/1b.md`, `V46CritGR1a/1b.md` → `fe77ac76…` (unaffected)

(`V46RevGR2b.md` and `V46RevGR3b.md` were not yet on disk; both seats were still running at 02:30.)
Consequence: at the tip, GR2 and GR3 have `bound_on_current = 0`, and the counter's row rule
(`tools/check-scrub-admission-r46.py:31-32`: at least two bound seats whose `SECTION SHA256` equals the row's hash at
REV, all `holds`) can never be satisfied — `verdicts_ok` caps at 1 (`marks_ok` is separately 0 with
`marks {entry:false, readme:false, skill:false}`). A live run at the tip confirms the shape and exits 1:
every seat reads `dispatched 0 times` with `marks_ok 0` — because `w1-dispatch.json`/`w1-results.json` are untracked
and so absent from any committed revision (structural, expected until closure; it does not hide F4, which is visible
in `--section-hash` alone).

Smallest remediation, pick one, before the C2 scoring run:
1. Do not re-measure: revert the GR2/GR3 text hunks of `b57740c2` in a follow-up commit and keep the text to which
   the ten reports bind; the narrowed wording then waits for round 47 with a fresh seat universe.
2. Or re-measure: re-dispatch two GR2 seats and two GR3 seats against the amended text, have them emit
   `SECTION SHA256: 4bf28bcf…` / `43430a14…`, and treat every pre-amendment GR2/GR3 report as superseded (the
   running `V46RevGR2b`/`V46RevGR3b` may already have read the amended text — check which hash they printed).
Either way, `b57740c2`'s subject line should say that the measured GR document changed, and LOG should record that the
round-45 grounding entry was rewritten in round 46 after five seats had bound to its earlier bytes.

## F5 — checklist items that came back clean, and the two that did not

Clean (commands and outputs in the receipt): no `/tmp` or `/var/tmp` entry newer than
`.ufo/waves/round-46/make-w1-spec.py` names tsukuroi/r46/census/scrub/hyaku (476 newer unrelated entries, all
`tameshi-r14` or harness); no new `~/.local/bin` entry (100 entries, directory mtime 02:20:02, nothing newer than the
spec); no zombie and no `ppid==1` orphan among the 34 live `tsukuroi-r46` processes; no `__pycache__` under `tools/`.

Not clean:

- **`__pycache__` inside the lane:** `.ufo/waves/round-46/controls/__pycache__/run_controls_c2.cpython-314.pyc`
  (16533 B, 02:23) — a python import of the lane's `controls/run_controls_c2.py` in place. Invisible to
  `git status` because `.gitignore:2` is `__pycache__/`. Owner unattributed; the pyc embeds the absolute path
  `…/round-46/controls/run_controls_c2.py`. Harmless bytes, but it is a write inside the lane from a seat that
  was told to copy the battery into scratch. Candidate seats: the C2 battery critic or the mutation tester.
- **Harness leftovers on `/fast`:** 14 `/fast/scratch/hyaku/run-receipt-*` directories, 3.1 GB, four of them newer
  than this wave's spec (`run-receipt-en9qlzud` 400 MB at 02:26:28, `run-receipt-home-f91n65hg` 02:26:24,
  `run-receipt-home-hqsemj0v` 02:28:31, `run-receipt-e_b0d_77` 02:28:33), oldest 23:51 from the prior round.
  `tools/run-receipt.py` copies tools and a clone per run and they are not being reaped. Seat scratch itself is
  healthy: 32 dirs / 3.1 GB under `/fast/scratch/hyaku/tsukuroi-r46/`, every one named for a live seat.
- **Host pressure, wave-level not seat-level:** 14, 15 and 17 concurrent `tsukuroi-census.sh --selftest` processes
  at three samples, with loadavg 42.6/55.4/51.7 on `nproc=32`. The seat rule ("never more than one C1 counter or
  census selftest at a time **in your seat**") is being satisfied per seat; the wave has ~15 seats inside it at once.
  Each selftest fans out ~6 CPUs and the C1 counter lasts ~1.5 min, so wall times are inflated several-fold and any
  leg whose observation window is host-timing-sensitive carries a contention risk. Nothing observed failed because
  of it — I did not run the C1 counter — but the L1 should expect slow returns and should not read a timeout as a
  seat failure at this load.

## What I did not do

No C1 counter and no census selftest (cost rule, and F3 makes a C1 run against the worktree meaningless); one C2
counter read-only run and two `--section-hash` runs (0.16 s each, both under my scratch cwd). I did not run
`git status` in any sibling lane, did not read lane index/jj state, did not remove or repair anything — including the
13 fleet-root entries, which disappeared between 02:28:00 and 02:28:44 without my help.
