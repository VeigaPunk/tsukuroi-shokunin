# ScoutSkill (F-13 SKILL staleness sweep) — verification receipts

## Census identity at sweep time (working tree)
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && wc -l SKILL.md tools/tsukuroi-census.sh && md5sum tools/tsukuroi-census.sh && sha256sum tools/tsukuroi-census.sh
4546 SKILL.md
3644 tools/tsukuroi-census.sh
8190 total
cf005e9a946e0a37c96f81d443d520d8c  tools/tsukuroi-census.sh
adb1b4ce2325c38da2acbb815d820d3d8d6a0dd45b34796d808590c8ab32ce41  tools/tsukuroi-census.sh

## Freeze-commit check: amended GR2 present at 77e9e2b2 (the revision counted seats read)
$ git show 77e9e2b2e96b85d8f048ae2087e246a542b71611:corpus/knowledge/btrfs-scrub-grounding-r45.md | grep -c "btrfs_fs_closing"
2
$ git show 77e9e2b2e96b85d8f048ae2087e246a542b71611:corpus/knowledge/btrfs-scrub-grounding-r45.md | sed -n '55,60p'
## GR2

**Statement.** In Linux v7.2.11 a device replace copies the source device through the scrub code: both the replace
start path (the comment "the disk copy procedure reuses the scrub code") and the path that continues an interrupted
replace call `btrfs_scrub_dev` on the source device's devid with `readonly` false and `is_dev_replace` true, the last
two parameters of `btrfs_scrub_dev`. Inside `btrfs_scrub_dev`, after a filesystem-closing check that returns `-EAGAIN` first

## R47-C2 evidence in the census source
$ grep -n "R47-C2" tools/tsukuroi-census.sh
412:# or /tmp itself when TMPDIR holds characters the root-override locator refuses — R47-C2).
2050:  # (R47-C2) The fixture roots below are handed to the census as caller root overrides,
3473:  # (R47-C2) pin the fixture-base contract: the work dir the harness runs under must
3477:    && ok 'selftest: the fixture base classifies absolute even when TMPDIR contains a space (R47-C2)' \
3478:    || bad 'selftest: the fixture base must classify absolute under a dirty TMPDIR (R47-C2)'
3481:    && ok 'selftest: a space in a root override stays unsafe by design (R47-C2)' \
3482:    || bad 'selftest: root_locator_class must refuse whitespace overrides (R47-C2)'

## Exact line anchors cited in the report
$ grep -n "Gate status (round 45)\|GR1-GR3 are pending\|still writes only under its\|154 → 162\|D12 one-command\|--identity does not exist\|D12 still unlanded" SKILL.md
4288:Gate status (round 45): the depth gate FAILED — `verdicts_ok` 0, no counted verdict bound ...
4289:measured outcome"). GR1-GR3 are pending, not admitted: ...
1301:unchanged: the selftest still writes only under its `mktemp -d /tmp/tsukuroi-r3-2-selftest.XXXXXX`
1469:- **D12 one-command re-derivation** — one machine-readable identity line. **Not landed**: ...
4449:the freeze). Selftest 154 → 162 cases, eight `(R46-C1)`.
(SKILL.md:1541-1543 and :1595 carry the "--identity does not exist" / "D12 still unlanded" sentences; cited via the report body.)

## Round-47 declaration anchors (SCORECARD.md)
:3053 declaration (base 916019057147...); :3065 C1 GR1-GR3 admission; :3066 C2 TMPDIR-space fix + two
(R47-C2) cases, counting command → PASS (164 cases, 164 passed, 0 failed); :3073 F2a names the SKILL
admission mark `## Scrub grounding — round 47 admission`.

No census selftest and no frozen counter run in this seat (cost rule); no host mutation.
