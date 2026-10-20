# CritMinedMistake — r17 critic

**Verdict:** it was a real mistake, but the cause is misattributed. The proposed gate cannot fail on the actual event.

1. [obs] The steer is at `history://TsukuroiR17:9`: "read-only — never run pacman". The prompt pauses only *transactions* and prescribes `pacman -Sp` (`.ufo/prompts/tsukuroi-round-17.md:303-308`). The narrower steer governs (`:162` "never relaxes"). So this was a literal violation, but [inf] it had no effect on the host.
2. [obs] There was one pacman call, at 15:31:16Z: `pacman -Q` on 13 packages, including linux, systemd, nvidia-dkms and btrfs-progs (`…/TsukuroiR17.jsonl:51-52`). The recheck line names 3 (`initramfs-v42-sysroot-recovery.md:3`). The 13 match the pacman.log read 10 s earlier (`jsonl:50`). Cause: the habitual way to read versions. "Recheck prescribed it" is weak [inf].
3. Counterexamples:
   - The event is missing from every capture (`fresh-capture.txt:2` says "no pacman invocation"). A recheck gate stays green on it.
   - Matching bare names flags `boot-chain-r17.md:3` ("No pacman invocation", "any mkinitcpio … change"). It also fires on `/etc/mkinitcpio.conf` at baseline, so "red at baseline" proves nothing unless the finding is pinned to the binary actually being run (argv0) `pacman`.
   - `--paths` on one file misses five others: aur-risk-plane:15, driver-firmware-plane:268, foreign-provenance-r6:313, package-state-plane:328, snapper-eacces-mechanism:3.
   - `## R17-RECHECK` creates a second convention. Line 3 still primes the reader; the existing convention is "supersedes the … recheck: line above" (`journal-boot-plane.md:442`).
4. QUALITY26 binds recheck documents. They are written before future steers exist, so they cannot comply with them.

**Correction:**
- QUALITY26 should bind the executor, including L1. L1 copies the steer's forbidden binaries into its capture header and declares `Scope: executed=`.
- check-seat-scope.py should cover L1, using a frozen excerpt of `jsonl:51`. Expected result: red, 1 finding.
- The recheck gate should match only the binary being run inside backticks, use the last `recheck:` line, and check the whole corpus.

Not verified: whether pacman `-Q` takes a lock.

Scope: executed=none
