# RevRowQ03 — C1 row Q03 review at f3a5723a988bf1c2835985880e7a38d477462cd0

Verdict: holds. Row Q03 (btrfs check --repair usage guidance) is verbatim-quoted, every clause of the JSON statement, the SKILL.md line and the decision-table row is supported by the cited snapshot lines, the row answers its frozen question completely, and the fact is novel against base 2077e2fa.

## Findings

1. [obs] Pinned snapshot exists, bytes match the SOURCES row hash, and the raw URL fetch matches the pin. The lane snapshot `.ufo/waves/round-31/w1/ScribeSrcCheck/btrfs-check.rst` sha256 is `927b67b4ab13f681866e699fcd6ea4917a42ef08e4db1731b0adf065022d955c` (`sha256sum` in sandbox clone). `curl -sL https://raw.githubusercontent.com/kdave/btrfs-progs/v7.1/Documentation/btrfs-check.rst` saved to `.ufo/waves/round-31/w2/RevRowQ03/btrfs-check.rst.raw` gives the same sha256 and `diff -q` says IDENTICAL (183 lines). This matches the sha256 in the S166 SOURCES row (`corpus/SOURCES.md:260`) and in the snapshot pin `.ufo/waves/round-31/w1/CritCounterC1Shapes/fixtures/snapshots.sha256` (`927b67b4... snaps/btrfs-check.rst`).

2. [obs] Quote is verbatim at the cited line. The JSON row's quote `Do not use *--repair* unless you are advised to do so by a developer` occurs as a substring of snapshot line 30 only: `sed -n '30p' ... | grep -cF 'Do not use *--repair* unless you are advised to do so by a developer'` → 1. Line number 30 matches the JSON `"line": 30` field.

3. [obs] Every clause of the JSON statement is supported by cited snapshot lines, with no lost branch and no "only"/"always" overreach:
   - "By default... leaves the device unchanged; --readonly reaffirms that" — lines 17-18 ("By default, :command:`btrfs check` will not modify the device but you can reaffirm that by the option *--readonly*.").
   - "while --repair attempts fixes" — line 116 ("enable the repair mode and attempt to fix problems where possible").
   - "recommends unmounting before a check, though --force permits a mounted check" — lines 13-15 ("It is recommended to unmount the filesystem prior to running the check, but it is possible to start checking a mounted filesystem (see :ref:`--force...`)").
   - "Use --repair only on a developer's or experienced user's advice and after accepting that no fsck can successfully repair every type of filesystem corruption" — lines 30-32 ("Do not use *--repair* unless you are advised to do so by a developer or an experienced user, and then only after having accepted that no *fsck* successfully repair all types of filesystem corruption"). The source's own missing "can" typo is rendered as "no fsck can successfully repair every type": semantically equivalent, acceptable paraphrase [inf].
   - "Finish or cancel any running replace or balance first" — line 124 ("Please finish/cancel the running replace/balance before using this command.").
   - "Without --force, repair displays a warning and waits ten seconds" — lines 119-121 ("There's a warning and 10 second delay when this option is run without *--force* to give users a chance to think twice before running repair...").
   - "--force allows mounted checks and skips mount checks and that warning delay" — lines 141, 151-152 ("allow work on a mounted filesystem and skip mount checks..." and "This option also skips the delay and warning in the repair mode (see *--repair*).").
   - "Mounted repair most likely causes corruption unless the filesystem is quiescent, which may not be possible to guarantee" — lines 147-149 ("It is possible to run with --repair but on a mounted filesystem that will most likely lead to a corruption unless the filesystem is in a quiescent state which may not be possible to guarantee."). The qualifiers "most likely" and "may not be possible" are retained verbatim; no strengthening.
   - "an external device change can make a forced check crash" — lines 142-144 ("this should work fine on a quiescent or read-only mounted filesystem but may crash if the device is changed externally, e.g. by the kernel module.").

4. [obs] SKILL.md line supports the row. `SKILL.md:2682` `[R31-Q03]` says "Proceed only with advice from a developer or experienced user and after accepting that no fsck can successfully repair every corruption type." — exactly lines 30-32 of the snapshot, and its "S166 line 29-33" citation is accurate (the warning block spans lines 29-33).

5. [obs] Decision-table row supports the row. `corpus/knowledge/btrfs-repair-r31.md:14` says "Unmounting before a check is recommended, and the default check does not modify the device. Do not use `--repair` without developer or experienced-user advice and acceptance that not all filesystem corruption can be repaired and other software or hardware bugs may fatally damage a volume." — supported by lines 13-14 (unmount), 17-18 (default no modify) and 30-33 (advice, no fsck repairs all types, "some other software or hardware bugs can fatally damage a volume"). Its citation `btrfs-check.rst:12-18,29-33` (S166) is accurate.

6. [obs] The row answers every part of its frozen question "When may btrfs check --repair be run on a damaged filesystem?": it states the affirmative conditions (developer/experienced-user advice plus acceptance of repair limits), the procedural precondition (finish/cancel replace/balance), and the negatives (mounted non-quiescent filesystem most likely corrupts; external device change can crash a forced check).

7. [obs] SOURCES metadata verified. `corpus/SOURCES.md:260` names the exact URL that was fetched, the sha256 that matched, and line ranges 12-18, 29-33, 115-124, 140-152; spot-checked against the numbered snapshot: 115-124 contains the `--repair` option block (repair mode line 116, warning/10-second note lines 119-121, replace/balance note line 124) and 140-152 contains the `--force` block (lines 140-144, 146-149, 151-152). The tag provenance claim is also correct: `git ls-remote https://github.com/kdave/btrfs-progs.git refs/tags/v7.1 refs/tags/v7.1^{}` → `0a919c7d...` (tag) and `4ab0e80be9e3bb1db2e6038e6d4316d35fb7ba8b` (peeled), exactly the peeled commit named in the SOURCES row.

8. [obs] Novelty holds at base 2077e2fa. `git grep -c -i` at 2077e2fa over SKILL.md, PROVINCE.md and corpus/: `--repair` → 0 matches, `quiescent` → 0 matches, `10 second delay|ten second delay` → 0 matches; `fsck` → 5 matches, all in unrelated contexts (mkinitcpio HOOKS lines in `corpus/knowledge/journal-boot-plane.md` and `degraded-triage-r4.md`, and a round-25 verifier lesson), none holding the repair-advice fact. The base storage-health-r26 entry explicitly excludes filesystem repair from its scope.

## Residual risk and verification gaps

- [unk] I did not attempt to recover the sealed answer keys (prohibited), so the counter substrate's key binding was not re-derived; this does not affect the row-content judgment.
- [inf] The statement's "no fsck can successfully repair every type" normalizes the source typo (missing "can"); a strictly literal reading of the source would be ungrammatical, so the paraphrase is the only faithful rendering.

Scope: read=<sandbox clone /fast/scratch/hyaku/tsukuroi-r31/RevRowQ03/repo at f3a5723 (git show/grep/sed/sha256sum/diff), lane JSON/MD/SKILL/SOURCES at f3a5723 via git show/grep, fetched raw btrfs-check.rst (sha256 927b67b4...), git ls-remote kdave/btrfs-progs v7.1>; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevRowQ03.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-31/w2/RevRowQ03/btrfs-check.rst.raw; executed=git clone/checkout at f3a5723, git show/grep/ls-tree/ls-remote (read-only), sha256sum, diff, sed/grep -cF, curl -sL

Model: inception/mercury-3

Installs: none
