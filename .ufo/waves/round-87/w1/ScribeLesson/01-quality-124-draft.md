# Draft — `corpus/QUALITY.md` criterion 124 (round 87)

Seat: ScribeLesson (scribe, leaf). Draft only; the L1 lands. Every number and quote below is read from a
committed artifact or a wave-seat receipt named inline; this seat ran no battery, gate or selftest. Lane revision
measured: `cefb4188b484329c4908a19a277f8fb120fb4f56`. Receipts: `ScribeLesson/receipts/r01`-`r10`.

Status note: the lane working tree already carries an **uncommitted** 124 draft (`git status` → ` M
corpus/QUALITY.md`; `git diff --stat` → `1 file changed, 3 insertions(+)`, the entry at `corpus/QUALITY.md:285`).
This draft is the same predicate with two repairs: (i) the after-a-change leg is written as a decidable exit
contract (the working draft's "must read rc 0 or name the mismatched pins" is self-contradictory — rc 1 is the
naming outcome), and (ii) the `Shown able to fail` leg cites committed controls instead of a hypothetical ("a
check that could not see the incident would read rc 0"). Diff in `ScribeLesson.md` § Findings 1.

## Text to paste (after criterion 123)

```text
124. **No in-place writer touches `/boot`, and every `sudo` step leaves a `/boot` digest receipt (R87-BOOT-NO-INPLACE-WRITER):** a seat or L1 step never runs, on `/boot`, `/efi` or any file a boot pin names, a tool whose default output is its input (`objcopy`/`strip` without an explicit output file, `sed -i`, `sbsign` without `--output`, `ukify`, `mkinitcpio`, `limine*`, `bootctl`, `efibootmgr`); a wave context that permits `sudo` at all forbids it to seats by default and names the read commands it does permit, and every `sudo` step that runs records `sudo -n sh -c 'find /boot -type f -print0 | sort -z | xargs -0 b2sum'` into a before file and again into an after file and writes the `cmp` result into its committed receipt. After any suspected `/boot` change, `sudo python3 tools/check-limine-pins.py --live` is the read-only detector: rc 0 when every pin's file hashes to its `#<blake2b>` suffix, rc 1 naming each mismatched/missing/malformed pin, rc 2 when the conf is unreadable or a pin cannot be resolved. Captured by: round 86's bound "`sudo -n` is allowed ONLY for read-only inspection" was a rule on intent, naming no tool class and requiring no receipt; wave seat ScoutHost read `objcopy --dump-section` as inspection, and two calls (18:11:21 and 18:11:22) rewrote both UKIs in place (`.ufo/waves/round-86/w1/ScoutHost.md:17-27`; 5 PE header bytes changed per file on a controlled copy). No round-86 receipt holds a `/boot` digest list (`grep -rl 'b2sum' .ufo/waves/round-86/` → no path), so the change was found only by the L1's post-hoc reading (`.ufo/waves/round-87/before/host/receipt.txt`; `corpus/lessons/round-86.md` M3; `round-86-verifier-spotcheck.md` §5 routed 1). Red, round 86:

$ grep -c 'IS FORBIDDEN FOR EVERY SEAT' .ufo/waves/round-86/w1-spec.json
0
$ grep -rl 'b2sum' .ufo/waves/round-86/ ; echo rc=$?
rc=1
$ sudo -n b2sum /boot/EFI/Linux/*.efi          # post-hoc, round 87: .ufo/waves/round-87/before/host/receipt.txt
57f5eb94…  /boot/EFI/Linux/omarchy_linux.efi      # /boot/limine.conf:30 pins b990d8c6…
eff78d32…  /boot/EFI/Linux/omarchy_linux-lts.efi  # /boot/limine.conf:38 pins a68c281d…
# both mtimes 2026-11-06 18:11:22, the minute of the two objcopy calls

Green, round 87:

$ grep -c 'IS FORBIDDEN FOR EVERY SEAT' .ufo/waves/round-87/w1-spec.json
1
$ cat .ufo/waves/round-87/after/live-receipt.txt
$ sudo -n sh -c 'find /boot -type f -print0 | sort -z | xargs -0 b2sum' > before   # digest of the list
0f6acc28a3f9f4e3448fa2e9813dc61fb13f18c5d7a0fee6c5c21774e3560028  -
$ sudo -n python3 tools/check-limine-pins.py --live
{"findings": ["LP-MISMATCH line 30", "LP-MISMATCH line 38"], "hash_mismatch_panic": {"line": 8, "value": "no"}, …}
rc=1
$ (same list after) | sha256sum ; cmp before after
0f6acc28a3f9f4e3448fa2e9813dc61fb13f18c5d7a0fee6c5c21774e3560028  -
cmp: identical (no /boot byte changed by the live run)

Shown able to fail: the detector is not vacuous in either direction. On the state the round-86 writer left it reads rc 1 and names `LP-MISMATCH line 30` and `line 38` (the same live receipt), so a clean reading would be an observation, not a default; and a gate that answers HEALTHY whatever it reads is rejected by the committed freeze controls — `f1-constant-healthy` reads `0 0 0` of 22 with `HOST-SHAPE` among the failed families, and the do-nothing `K1` (gate absent) reads `0 0 0` (`.ufo/waves/round-87/before/controls/controls-summary.txt`, three runs each). The receipt leg is falsifiable the same way: the round-86 pair would not have been `cmp`-identical (the pin is the digest `ScoutHost.md:23` books as the file's "before" value, the file is the post-incident one).
Lesson: `corpus/lessons/round-87.md` Mistakes `R87-INTENT-RULE-NOT-TOOL-RULE`.
```

## Why each leg is written that way

- **Tool class, not intent.** The r86 bound admitted any command a seat judged read-only; the failure was a
  judgement, not a rule. The class is the set of tools whose default output *is* their input (binutils
  `objcopy`/`strip` manual: "If you do not specify outfile, objcopy creates a temporary file and destructively
  renames the result with the name of infile", pinned S354), which needs no seat judgement.
- **Pin-named files, not just `/boot`.** Limine pins name UKIs under `/boot/EFI/Linux/` and history copies under
  `/boot/432d…/limine_history/` (`/boot/limine.conf:30,38,50,56,64`), so the rule's object is "any file a boot pin
  names"; a writer on any of them breaks the pin.
- **Digest pair before `cmp`.** `find … | sort -z | xargs -0 b2sum` is content+path only. The pair catches an
  overwrite (digest changes under the same path) and an addition/removal (the list changes); it does not catch a
  metadata-only change, which is why the detector leg (pin comparison) is stated separately.
- **Exit contract.** `tools/check-limine-pins.py` docstring: "Exit: 0 HEALTHY; 1 DEGRADED (a pin mismatches, is
  missing, or is malformed); 2 CANNOT-EVALUATE (conf unreadable, or a pin that cannot be resolved here)" — the
  criterion quotes that map rather than "rc 0 or name the pins".
- **Sanctioned writers.** The rule binds a seat or L1 step; the package's own hook (`limine-mkinitcpio-hook`) and
  `limine-snapper-sync` remain the sanctioned writers of `/boot/limine.conf` and its pins, run by the operator.
  A seat never invokes them either (the r87 context names them in the forbidden list).

## Sources consulted (read, not re-run)

`corpus/lessons/round-86.md` §M3; `corpus/lessons/round-86-verifier-spotcheck.md` §5.1; `.ufo/waves/round-86/w1/ScoutHost.md`
§0 and `ScoutHost/objcopy-incident/CURRENT-HASHES.txt`; `.ufo/waves/round-86/w1-spec.json` (context bound);
`.ufo/waves/round-87/w1-spec.json` (context bound); `.ufo/waves/round-87/after/live-receipt.txt`;
`.ufo/waves/round-87/before/host/receipt.txt`; `.ufo/waves/round-87/before/controls/controls-summary.txt`;
`.ufo/waves/round-87/before/freeze-manifest.sha256`; `tools/check-limine-pins.py:1-31`;
`tools/limine-pin-battery-r87.py:1-60,451-479`; `corpus/QUALITY.md:236-286`.
