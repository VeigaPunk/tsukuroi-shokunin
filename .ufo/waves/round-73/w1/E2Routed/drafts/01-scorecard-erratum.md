## Round 72 — instrument digest erratum (appended round 73; R72-C3-INSTRUMENT-DIGEST-DRIFT)

R72-C3-INSTRUMENT-DIGEST-DRIFT. The round-72 declaration (`SCORECARD.md:5616`, commit `6b42676`) froze
`tools/check-r71-routed-r72.py` at sha256
`df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712`, and that is the tool's actual blob
at the declaration commit. The tool's committed bytes then moved
`df8a59c7a2891f58ab37a1b22e73819d953f1781528d4f2f4937641e093de712` →
`2610ff433bf5d4e945ce5b2da0cf168745e4142ecffabc3d160afee33005cdcc` (landed by the round-72 repair
commit `53bcddef`, unchanged at the round-73 base `eb105757`), after an intermediate `b17fddfa…` state
committed at `123e1c57`.

The repairs the round-72 close landed in that checker: the receipt must now carry the record revision
token `2b358d2d`; the `## Round 71 — receipt erratum` block is matched from a line start, so prose that
quotes the heading no longer satisfies it; and the round-71 note correction is checked against the five
`/usr/lib/modprobe.d` filenames (`README`, `bluetooth-usb.conf`, `gsr-nvidia.conf`, `nvidia-utils.conf`,
`systemd.conf`) instead of a prose token list.

Same-instrument evidence: `python3 tools/check-r71-routed-r72.py --revision a7015d27` reads
`ROUTED_STALE=3` rc 1 (pre-repair data) and `--revision eb105757` reads `ROUTED_STALE=0` rc 0
(post-repair data) with the same tool bytes `2610ff43…` on both sides, recorded at
`.ufo/waves/round-73/after/r72-c3-same-instrument-before.txt`. The same-instrument selftest receipt for
the capability chain — its header records a run on the committed tool with the ten-case v2 patch — is
`.ufo/waves/round-72/after/selftest-selftest-after.txt`
(`SELFTEST: PASS (10 cases, 10 passed, 0 failed)`, rc 0).

Counted by `python3 tools/check-r72-routed-r73.py --revision <REV>` (item DIGEST).
