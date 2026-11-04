status: complete
verdict: held

# E3HostProbe — a read-only probe for the unit-load merge plane (C1 surface)

Seat: L2, tsukuroi lane, round 73 (hyaku 15), wave w1. Assigned item: build a read-only probe
that measures the unit-load surface the C1 entry (`corpus/knowledge/systemd-unit-load-plane-r73.md`,
rows UL1-UL6) describes, show what it does when `systemctl` is absent, and prove an echo guard
against a hostile unit name. Judged on operability, C1, probe.

Deliverables in this directory:

| file | what it is |
|---|---|
| `probe.sh` | the probe (418 lines, bash, `sha256 da25458a721040d9dd7ada71e29435434c2435fc1ce62b12450edf7d66d419ac`) |
| `receipt-a-live.txt` | live run, five readings against the committed host capture |
| `receipt-b-tool-absent.txt` | stub-`PATH` degradation to `BLOCKED reason=tool-absent` |
| `receipt-c-echo-guard.txt` | `|` / newline / `=` / tab unit names in a fixture directory |
| `receipt-d-selftest.txt` | hermetic `--selftest`, 16/16 |
| `receipt-e-c2-instrument.txt` | the freeze finding, both instruments, with the digest sequence |
| `receipt-f-c1-scripted-writer.txt` | the C1 scripted-writer attack |
| `receipt-g-landing.txt` | both claims at the landing commit, before controls, both attacks |
| `attack-c1-scripted-writer.py` | the C1 attack, reproducible |
| `attack-c2-vacuous.py` | the C2 residual attack, reproducible |
| `evidence/` | the C2 instrument bytes as observed at `328a6bf6…` |

Nothing was installed, upgraded or removed (no `pacman`, no `uv`, no `npx`, no binary fetched).
Host: Linux 7.2.11-arch1-1, systemd 262 (262.1-1-arch), GNU bash 5.3.20 (`/usr/bin/bash`).
The lane tree was not modified; the probe reads `/etc`, `/run`, `/usr` and a handful of read-only
D-Bus queries.

## 1. What the probe emits

One line per reading, exactly one line per reading:

```
SEARCHPATH dirs=<n> first=<path> etc_before_usr=<0|1>     systemd-analyze unit-paths
MASKED count=<n> targets=/dev/null:<n>                    systemctl list-unit-files --state=masked
                                                          (+ FragmentPath + readlink per row)
DROPINS unit=<unit> paths=<n> etc=<n> usr=<n>             systemctl show -p LoadState -p DropInPaths
TEMPLATE instance=<unit> fragment=<basename> template=<0|1>  systemctl show -p LoadState -p FragmentPath
UNITSTATE unit=<unit> load=<load-state>                   systemctl show -p LoadState
BLOCKED reading=<READING> reason=<enum>
```

Reason enum (closed): `tool-absent`, `bad-unit-name`, `bad-path`, `unparsable`, `unknown-unit`.
Load enum (closed, from `unit.h`'s state table): `loaded|not-found|bad-setting|error|merged|masked`.

Every value written after a `key=` is matched against a closed pattern before it is printed
(QUALITY 84): `^[0-9]{1,9}$`, `^/[A-Za-z0-9._/@+%,:-]+$`, a unit-name pattern
`^[-A-Za-z0-9:_.@\\]+\.(service|socket|device|mount|automount|swap|target|path|timer|slice|scope)$`
capped at 255 characters and forbidden a leading dot, or one of the two enums. A name that fails
its pattern blocks that reading with a fixed reason token and is never echoed.

Mapping onto the C1 rule rows: `SEARCHPATH` measures UL1 (directory order is what makes `/etc`
win); `DROPINS` measures UL2 (which directories hold the drop-ins that merge lexicographically)
and UL3 (the drop-in path list that is compared at reload); `MASKED` + `UNITSTATE` measure UL4
(masked state while the fragment is `/dev/null`) and UL5 (the mask is a `/dev/null` symlink);
`TEMPLATE` is a supporting reading with no UL row of its own — see Limits.

## 2. Receipt A — live run

```
$ bash probe.sh
SEARCHPATH dirs=12 first=/etc/systemd/system.control etc_before_usr=1
MASKED count=2 targets=/dev/null:2
DROPINS unit=user@1000.service paths=2 etc=1 usr=1
TEMPLATE instance=getty@tty1.service fragment=getty@.service template=1
UNITSTATE unit=passim.service load=masked
rc=0
```

Every token agrees with `.ufo/waves/round-73/before/host.txt`: 12 search-path directories with
`/etc/systemd/system.control` first and every `/etc/` entry ahead of every `/usr/` entry; two
masked units both symlinked to `/dev/null`; `user@1000.service` carrying one `/usr/lib` and one
`/etc` drop-in; `getty@tty1.service` resolving to the template fragment `getty@.service`;
`passim.service` loading as `masked`. Two further units the capture records also agree
(`systemd-udevd.service` → `paths=1 etc=0 usr=1`; `passim.service` → `paths=0`), and an absent
unit is a reading rather than a block: `UNITSTATE unit=nosuch-unit-xyz.service load=not-found`, rc 0.

## 3. Receipt B — `systemctl` absent

The stub the item names is `$S/bin/systemctl` = `#!/bin/sh` + `exit 127`, first on `PATH`. The
probe treats exit 127 from a tool it can already resolve as absence, because 127 is how a shell
reports an unresolvable command and a wrapper that returns it is indistinguishable from one.

```
$ PATH="$S/bin:$PATH" bash probe.sh
SEARCHPATH dirs=12 first=/etc/systemd/system.control etc_before_usr=1
BLOCKED reading=MASKED reason=tool-absent
BLOCKED reading=DROPINS reason=tool-absent
BLOCKED reading=TEMPLATE reason=tool-absent
BLOCKED reading=UNITSTATE reason=tool-absent
rc=1

$ PATH="$S/bin" bash probe.sh          # nothing but the stub resolves
BLOCKED reading=SEARCHPATH reason=tool-absent
BLOCKED reading=MASKED reason=tool-absent
BLOCKED reading=DROPINS reason=tool-absent
BLOCKED reading=TEMPLATE reason=tool-absent
BLOCKED reading=UNITSTATE reason=tool-absent
rc=1

$ PATH="$S/bin:$PATH" bash probe.sh | grep -c '^MASKED count='
0
```

Two facts this fixes in place. First, the four `systemctl`-backed readings degrade on the item's
stub; `SEARCHPATH` is backed by `systemd-analyze`, so it keeps reading (correctly — it is not a
`systemctl` question) and only the second run, whose `PATH` holds nothing else, degrades all five.
Second, no count is printed at all under the stub: the failure mode is `BLOCKED`, never a zero.
A stub that prints garbage and exits 3 is also refused rather than counted:
`BLOCKED reading=MASKED reason=unparsable`.

`systemctl list-unit-files --state=masked` legitimately exits 1 with empty output when no unit file
matches (measured on `--state=masked-runtime`: rc 1, 0 bytes). The probe reads that case as
`MASKED count=0 targets=/dev/null:0` and every other non-zero exit as `unparsable`; the selftest
pins both ends (`masked-nomatch`, `masked-rc3`).

## 4. Receipt C — the echo guard

Fixture `$S/fixtures/etc/systemd/system/`, selected with `TSUKUROI_UNIT_DIRS`, which replaces
`systemctl list-unit-files` as the candidate source for the `MASKED` reading:

```
$ ls -1b $S/fixtures/etc/systemd/system
a=b.service
evil.service\nMASKED\ count=999
evil|pipe.service
legit.service
tab\tstop.service

$ TSUKUROI_UNIT_DIRS=$S/fixtures/etc/systemd/system bash probe.sh --reading masked
BLOCKED reading=MASKED reason=bad-unit-name
rc=1

$ ... | wc -l                      -> 1
$ ... | grep -c '^MASKED count='   -> 0
$ ... | grep -c 'count=999'        -> 0
$ ... | grep -c 'reason=bad-unit-name' -> 1
```

The forged payload is `MASKED count=999` inside a filename, chosen because it contains no `/` and
therefore *can* be created as a filename. It cannot become a line: the probe prints exactly one
line per reading and only validated tokens reach it. The name position is guarded too — a hostile
name in the *argument* blocks the same way:
`--reading 'dropins:evil|pipe.service'` → `BLOCKED reading=DROPINS reason=bad-unit-name`, and a
newline in the argument → `BLOCKED reading=UNITSTATE reason=bad-unit-name`.

Two controls keep the guard from being a blanket refusal:

```
$ TSUKUROI_UNIT_DIRS=$S/fixtures-clean bash probe.sh --reading masked
MASKED count=1 targets=/dev/null:1
rc=0

$ TSUKUROI_UNIT_DIRS=/etc/systemd/system bash probe.sh --reading masked
MASKED count=2 targets=/dev/null:2
rc=0
$ systemctl list-unit-files --state=masked --no-legend --no-pager | wc -l
2
$ readlink /etc/systemd/system/passim.service /etc/systemd/system/systemd-networkd-wait-online.service
/dev/null
/dev/null
```

The second control is the one that matters: the fixture reader and the `systemctl` reader agree on
the live host (2 and 2, both to `/dev/null`), so the override is a real second view of the same
surface and not a fixture-only code path (QUALITY 82).

## 5. Receipt D — selftest

`bash probe.sh --selftest` with `TMPDIR` set to scratch (never `/tmp`) runs 16 cases and passes all
16: `clean`, `pipe`, `newline`, `space`, `extension`, `dotfile`, `withdirs`, `per-reading-arg`,
`absent`, `absent-all`, `dropins-forged`, `searchpath-forged`, `masked-rc3`, `masked-nomatch`,
`loadstate-forged`, `containment`. It is hermetic (its own fixture tree under `$TMPDIR`) and it
refuses to run unhermetically: `TMPDIR=` → `SELFTEST: FAIL (SELFTEST-TMPDIR)` rc 4,
`TMPDIR=/tmp` → `SELFTEST: FAIL (SELFTEST-HERMETIC)` rc 4.

## 6. Two defects the probe carried, and the receipts that found them

Both were found by running the probe, not by reading it; both are fixed in `probe.sh` and both now
have a selftest case.

**D1 — directories were name-validated as unit files.** The first live cross-check of the
directory reader read:

```
$ TSUKUROI_UNIT_DIRS=/etc/systemd/system bash probe.sh --reading masked
BLOCKED reading=MASKED reason=bad-unit-name
```

The directory holds `basic.target.wants`, `docker.service.d` and similar; the reader validated the
basename of every entry before testing whether it was a symlink, so a legitimate host blocked. Fixed
by skipping directories first; the same command now reads `MASKED count=2 targets=/dev/null:2`, and
the `withdirs` selftest case pins it.

**D2 — per-reading arguments collapsed to one variable.** This run

```
$ bash probe.sh --reading dropins --dropin systemd-udevd.service \
                --reading dropins --dropin passim.service
DROPINS unit=passim.service paths=0 etc=0 usr=0
DROPINS unit=passim.service paths=0 etc=0 usr=0
```

printed `passim.service` twice: the later `--dropin` overwrote the earlier one before either reading
was emitted. Fixed by binding the argument at the reading — `--reading NAME:ARG` — so the same
question now reads `DROPINS unit=systemd-udevd.service paths=1 etc=0 usr=1` then
`DROPINS unit=passim.service paths=0 etc=0 usr=0`; the `per-reading-arg` case pins it.

## 7. Attacks on the two frozen instruments

Both instruments moved during this wave and both landed. At the close of this seat's reading
(`583eea87`) each working-tree file equals `git show HEAD:<path>` and `git status --porcelain --
tools/` is empty.

| instrument | declared before data | final, committed | what changed |
|---|---|---|---|
| `tools/count-ul-rows-r73.py` | `542f9c2…` | `97f6f5ec…` | `MIN_QUOTE_WORDS = 4` and the `EMPTYQUOTE` arm |
| `tools/check-r72-routed-r73.py` | `93f034e3…` | `71931c1c…` | 125 insertions / 48 deletions: whole-token matching, receipt presence and case count, a supersede verb, digest direction |

### 7.1 Final state — both declared targets read met

```
$ python3 tools/count-ul-rows-r73.py --revision HEAD
UL_ROW ok UL1 source=S304 snapshot=systemd.unit.xml
UL_ROW ok UL2 source=S304 snapshot=systemd.unit.xml
UL_ROW ok UL3 source=S305 snapshot=unit.c
UL_ROW ok UL4 source=S305 snapshot=unit.c
UL_ROW ok UL5 source=S306 snapshot=install.c
UL_ROW ok UL6 source=S306 snapshot=install.c
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1
rc=0

$ python3 tools/check-r72-routed-r73.py --revision HEAD
ROUTED_ITEM LESSON ok
ROUTED_ITEM DIGEST ok
ROUTED_ITEM CAPABILITY ok
ROUTED_STALE=0 ROUTED_OK=3/3
rc=0
```

Both before controls hold at base `eb105757…` with those same final bytes: C1
`UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md`, rc 128 (the note does not
exist there); C2 `ROUTED_STALE=3 ROUTED_OK=0/3`, rc 1. Both selftests pass at the committed bytes
(12/12 for C1 including `EMPTYQUOTE`, 11/11 for C2 including `VACUOUS` and `DIGEST-REVERSED`), and
`corpus/SOURCES.md` now carries S304-S308, so the `source-unregistered` conjunct resolves.

### 7.2 The freeze was broken while the wave ran (closed at the landing)

For several minutes of this seat's turn neither instrument's working-tree bytes were a committed
revision, and the C2 checker was never committed at its declared digest:

```
$ git show 74937132:tools/check-r72-routed-r73.py | sha256sum
93f034e3…        # the declared digest, and what `git show HEAD:` returned at 23:13
$ sha256sum tools/check-r72-routed-r73.py
f1c4b4d3…        # 23:09
328a6bf6…        # 23:12:19
71931c1c…        # 23:17, committed at 583eea87
$ sha256sum tools/count-ul-rows-r73.py
542f9c29…        # 23:13, still the declared bytes
84501ab8…        # 23:15:57, +14 lines, mtime 23:14:42
97f6f5ec…        # 23:16:05, committed at 09dac09f
```

At `f1c4b4d3…` the C2 checker's own `--selftest` read `FAIL (11 cases, 9 passed, 2 failed)`:
`SELFTEST-CONTROL` — the declared target state — was **rejected** by the instrument then running
(`CAPABILITY-STALE path=SCORECARD.md reason=block-no-supersede-verb`, `ROUTED_STALE=1 ROUTED_OK=2/3`),
and `SELFTEST-VACUOUS` was **credited** (`ROUTED_ITEM LESSON ok` for a block that is only a token
salad under a `## Correction` heading). Both are gone at the committed bytes. The durable defect is
not those two fixtures but the window itself: a `--revision <REV>` receipt produced then named a
predicate no revision contained, so the declaration's "re-run the before control with the final
instrument and record old→new digests" clause had no fixed "final" to bind to. It is closed by the
landing commit; the digest sequence above is that old→new record.

### 7.3 Residuals that survive the final bytes

**C1 — a scripted writer is credited (survived).** The predicate is a token-overlap test, so a
writer that never reads the source passes it. `attack-c1-scripted-writer.py` cuts a verbatim
430-character slice out of `systemd.unit.xml` — XML markup and all — and drops it into UL1's
statement cell:

```
COPIED STATEMENT: Unit files found in directories listed earlier override files with the same name in
directories lower in the list <xi:include href="standard-conf.xml" xpointer="usr-local-footnote" />.
</para> <para>When the variable <varname>$SYSTEMD_UNIT_PATH</varname> is set, …
UL_ROW ok UL1 source=S304 snapshot=systemd.unit.xml
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1
```

This is a property of the declared predicate, not a deviation from it: grounding cannot tell prose
from copied bytes, and the new `MIN_QUOTE_WORDS` floor does not touch it. The declaration's own
defence is QUALITY 81's committed non-author reviewer verdict, which is why a reviewer seat exists
in this wave. Recorded so `met=1` is not read as "someone read the source".

**C2 — a bare token list under the capability heading is credited (survived).**
`attack-c2-vacuous.py` replaces the capability block with

    <block heading>  Capability refresh (round 73)
    <block body>     gate-selftest 10 cases .ufo/waves/round-72/after/selftest-selftest-after.txt

and gets `ROUTED_ITEM CAPABILITY ok` and `ROUTED_STALE=0 ROUTED_OK=3/3`. The `CAPABILITY` item is
the only one of the three with no `need_verb`, so it carries no requirement that the block say what
changed — the tool name, the case count and the receipt path suffice (QUALITY 87's
content-free-cell shape). The lesson and digest blocks are not exposed the same way: a lesson block
that is only tokens under `## Correction` is refused with `reason=block-no-supersede-verb`.
A `need_verb` conjunct on `CAPABILITY` would close it, and that is a post-wave instrument repair the
L1 owns, not this seat.

## 8. What a probe like this must never do here

The probe is unprivileged and read-only in the strict sense the lane's existing gates use
(`tools/tsukuroi-census.sh:348` "Live mode creates no files"; `:514` "no probe writes";
`PROVINCE.md:16` "all read-only"). Concretely, on this host it must never:

- `systemctl mask` / `unmask` / `enable` / `disable` / `daemon-reload` / `start` / `stop` / `reload` —
  each is a bus transaction that changes state on a host the operator is still recovering, and
  `enable`/`disable` also writes or deletes symlinks in `/etc/systemd/system`, which is exactly the
  directory whose contents the `MASKED` reading counts;
- write a unit file, a drop-in, a `.wants` link, or a mask symlink — including "temporarily", to test
  the reading; the `TSUKUROI_UNIT_DIRS` override exists so fixtures live in scratch instead;
- call any `systemd-analyze` verb that is not a pure query, or pass a `--root`/`--profile` style flag
  that points the reading at another tree while claiming to describe this one;
- write under `/tmp`, create a git fixture inside the lane, or leave a scratch tree behind.

`probe.sh` performs no mutation: five `systemctl show` / `list-unit-files` reads,
`systemd-analyze unit-paths`, and `readlink` on paths it has already validated. The `--selftest`
writes only inside `$TMPDIR` and deletes its tree.

**Census or probe?** It stays a probe, and cannot join the census as written. The census's systemd
plane is declared **user scope only** — `tools/tsukuroi-census.sh:136-137`: "systemd (user scope
only — PROVINCE.md:8-9 owns `systemctl --user`; the system-scope row lives in SKILL.md:42 and is out
of this gate's scope)". The unit-load merge plane is system scope by definition: the 12-directory
search path, `/etc` versus `/usr` precedence, and masks in `/etc/systemd/system` are all invisible
to `systemctl --user`. The census also pins six `PLANE` lines that frozen consumers parse, so a
seventh plane is a format break, and its systemd legs are driven through `TSUKUROI_SYSTEMCTL`
(`tools/tsukuroi-census.sh:586`, stubbed at `:2594`, wired at `:2868`) so the hermetic selftest can
replace the tool — a system-scope reading cannot be made hermetic that way. The right home is a
sibling of `tools/recheck-drift-r54.sh`: one committed, verdict-neutral, read-only recheck command,
outside the six-plane rollup.

## 9. Limits

- **Five readings, one host.** Everything in receipt A is one machine at one moment
  (`2026-11-03T23:0x-03:00`, systemd 262.1-1-arch). Nothing here shows the readings hold on another
  systemd version; `LoadState`'s enum is taken from `unit.h` at v262 and would need re-pinning for
  another tag.
- **`TEMPLATE` has no UL row.** It measures the instance→template fragment indirection that the C1
  entry's UL1-UL6 do not state. It is included because the item asks for it and because UL4's masked
  claim is only meaningful for a name that resolves to a real fragment; it is not evidence for any
  UL row.
- **`targets=/dev/null:<n>` is narrower than "masked".** It counts masks whose fragment is a
  `/dev/null` symlink. A zero-size regular file also masks a unit in systemd's model (UL4's subject)
  and is counted in `count` but not in `targets`; the probe distinguishes them deliberately rather
  than folding them together. No such unit exists on this host.
- **`etc_before_usr` is a prefix test.** It compares the first entry under `/etc/` with the first
  under `/usr/` in the printed order, not the position of the two canonical directories, so
  `/usr/local/lib/systemd/system` counts as `/usr/`. On this host both readings agree
  (`/etc/systemd/system` at index 5, `/usr/local/...` at 10).
- **The directory reader is a second view, not a replacement.** `TSUKUROI_UNIT_DIRS` enumerates a
  directory and follows symlinks; it does not reproduce `systemctl`'s view of `/run/systemd/transient`
  units or generator output. It is cross-checked against `systemctl` on `/etc/systemd/system` only.
- **The C1 attack proves the predicate is a grounding test, not that the landed note was unread.** It
  shows one row can be machine-copied and still credited; it says nothing about how the L1 wrote the
  six that landed. The attack was run against a fixture built by the counter's own `build_fixture`,
  so it isolates the predicate, not the note.
- **The freeze finding is timestamped and its intermediate bytes are gone.** `f1c4b4d3…` and the two
  selftest cases it failed are observations with no surviving file; the copy under `evidence/` is
  `328a6bf6…` only. The digest sequence in §7.2 is what makes the finding checkable; re-deriving the
  intermediate behaviour is not possible, and a seat reading `tools/` later sees the committed bytes.
- **Probe scope is measurement only.** It produces no verdict and is not wired to any exit gate; the
  L1 decides whether it lands, and where.

---

Report: `.ufo/waves/round-73/w1/E3HostProbe.md`
