status: complete
verdict: held

# E3HostProbe — a read-only probe for the unit-fragment resolution plane (round 74, C1 surface)

Seat: L2, tsukuroi lane, round 74 (hyaku 15), wave w1. Assigned item: build a read-only
host probe that measures the unit-fragment resolution surface the C1 entry
(`corpus/knowledge/systemd-unit-fragment-plane-r74.md`, rows UF1-UF6) describes, verify
masked units resolve to `/dev/null`, confirm template/instance resolution, and demonstrate
failure-mode behavior under tool absence and hostile input. Judged on operability, C1, probe.

Deliverables in this directory:

| file | what it is |
|---|---|
| `probe.sh` | the probe (810 lines, bash, sha256 `eff63e2c979f9ae0589135a4456973b9192c30911c3f2d8e23612fe7a4a3932f`) |
| `receipt-a-live.txt` | live run, fourteen readings against the committed host capture |
| `receipt-b-tool-absent.txt` | stub-PATH degradation to `BLOCKED reason=tool-absent` for all six readings |
| `receipt-c-echo-guard.txt` | hostile-name blocking: pipe, newline, semicolon, traversal, dot, 256-char, quote, tab/space |
| `receipt-d-selftest.txt` | hermetic `--selftest`, 21/21 |
| `receipt-e-c2-instrument.txt` | the C2 checker: selftest, base/declaration controls, vacuous attack battery 8/8 |
| `receipt-f-c1-counter.txt` | the C1 counter: selftest, base/declaration controls, scripted-writer attack battery 7/7 |
| `receipt-g-landing.txt` | frozen instrument digests + baseline controls + probe selftest + live run at HEAD 810daf13 |
| `attack-c1-scripted-writer.py` | C1 attack, reproducible (control + 7 scripted-writer mutants) |
| `attack-c2-vacuous.py` | C2 attack, reproducible (control + 7 vacuous/malformed mutants) |

Nothing was installed, upgraded or removed (no `pacman`, no `uv`, no `npx`, no binary fetched).
Host: Linux 7.2.11-arch1-1, systemd 262 (262.1-1-arch), GNU bash 5.3.20.
The lane tree was not modified; the probe reads `/etc`, `/run`, `/usr` and a handful of
read-only D-Bus queries.

## 1. What the probe emits

One line per reading, exactly one line per reading:

```
SEARCHPATH scope=<system|user> dirs=<n> first=<path> etc_before_usr=<0|1>
MASKED count=<n> targets=/dev/null:<n>
CAT unit=<unit> fragment=<path> masked=<0|1> dropins=<n>
TEMPLATE instance=<unit> fragment=<basename> template=<0|1>
ALIAS alias=<unit> target=<target> may_alias=<0|1>
UNITSTATE unit=<unit> file_state=<state> load_state=<load>
BLOCKED reading=<READING> reason=<tool-absent|bad-unit-name|bad-path|unparsable|unknown-unit|self-alias|incompatible-type>
```

Reason enum (closed): `tool-absent`, `bad-unit-name`, `bad-path`, `unparsable`,
`unknown-unit`, `self-alias`, `incompatible-type`.
Load enum (closed, from `unit.h`'s state table): `loaded|not-found|bad-setting|error|merged|masked`.
File-state enum (closed, from `unit-file.h`'s `UnitFileState` table):
`enabled|enabled-runtime|linked|linked-runtime|alias|masked|masked-runtime|static|disabled|indirect|generated|transient|bad|not-found`.

Every value written after a `key=` is matched against a closed pattern before it is printed
(QUALITY 84): `^[0-9]{1,9}$`, `^/[A-Za-z0-9._/@+%,:-]+$`, a unit-name pattern
`^[-A-Za-z0-9:_.@\\]+\.(service|socket|device|mount|automount|swap|target|path|timer|slice|scope)$`
capped at 255 characters and forbidden a leading dot, or one of the three enums. A name
that fails its pattern blocks that reading with a fixed reason token and is never echoed.

Mapping onto the C1 rule rows (as declared in SCORECARD.md line 6092):
`SEARCHPATH` measures UF1 (directory order is what makes `/etc` win; first-seen name
registration; T21 fixture proves an `/etc` entry shadows a `/usr` duplicate);
`CAT` + `MASKED` + `UNITSTATE` measure UF4 (fragment resolution to `/dev/null` yields
masked state; on-disk files and masks override any other state) and UF5
(`UNITSTATE` emits both `UnitFileState` and `LoadState`; `enabled-runtime` observed on
`systemd-remount-fs.service` distinguishes runtime from persistent variants);
`ALIAS` measures UF2 (self-alias rejection with `self-alias`, target-name-type
validation with `incompatible-type`) and UF3 (`unit_type_may_alias` gate, enforced
*before* any filesystem lookup, so a `.slice` alias is blocked even if the symlink
exists); `TEMPLATE` measures instance→template fragment resolution;
`UNITSTATE` on `nosuch-unit-xyz.service` measures the not-found path (no fragment
found on disk or in builtins for system scope). UF6 (built-in fallback) is
code-gated (system scope only, `builtin_unit_lookup` at load-fragment.c:6186) and the
host's `emergency.service` has an on-disk fragment at `/usr/lib/systemd/system/`,
so the probe reports the on-disk override rather than exercising the built-in path.

## 2. Receipt A — live run

```
SEARCHPATH scope=system dirs=12 first=/etc/systemd/system.control etc_before_usr=1
SEARCHPATH scope=user   dirs=18 first=/home/vgpnk/.config/systemd/user.control etc_before_usr=1
MASKED count=2 targets=/dev/null:2
CAT unit=passim.service        fragment=/etc/systemd/system/passim.service        masked=1 dropins=0
CAT unit=user@1000.service     fragment=/usr/lib/systemd/system/user@.service     masked=0 dropins=2
TEMPLATE instance=getty@tty1.service  fragment=getty@.service   template=1
TEMPLATE instance=user@1000.service   fragment=user@.service    template=1
ALIAS alias=dbus.service    target=dbus-broker.service  may_alias=1
ALIAS alias=default.target  target=graphical.target     may_alias=1
UNITSTATE unit=systemd-remount-fs.service file_state=enabled-runtime load_state=loaded
UNITSTATE unit=passim.service             file_state=masked          load_state=masked
UNITSTATE unit=getty@tty1.service         file_state=enabled         load_state=loaded
UNITSTATE unit=user@1000.service          file_state=static          load_state=loaded
UNITSTATE unit=nosuch-unit-xyz.service    file_state=not-found       load_state=not-found
rc=0
```

Every token agrees with `.ufo/waves/round-74/before/host.txt`: 12 system search-path
directories with `/etc/systemd/system.control` first and every `/etc/` entry ahead of
every `/usr/` entry; 18 user search-path directories with the same ordering; two masked
units both symlinked to `/dev/null` (`ls -l` confirms: `passim.service` → `/dev/null`
Oct 20 09:48, `systemd-networkd-wait-online.service` → `/dev/null` Oct 3 17:44);
`user@1000.service` resolving to the template fragment `user@.service` with two drop-ins
(`/usr/lib/.../user@.service.d/10-login-barrier.conf` and
`/etc/systemd/system/user@.service.d/faster-shutdown.conf` — one `/usr`, one `/etc`);
`getty@tty1.service` resolving to `getty@.service`; `dbus.service` aliasing
`dbus-broker.service` (service→service, alias-capable); `default.target` aliasing
`graphical.target` (target→target, alias-capable). `systemd-remount-fs.service` is the
host's only `enabled-runtime` unit — the runtime variant of `enabled`, matching
`UNIT_FILE_ENABLED_RUNTIME` in `unit-file.h:9`. An absent unit is a reading, not a
block: `UNITSTATE unit=nosuch-unit-xyz.service file_state=not-found load_state=not-found`, rc 0.

## 3. Receipt B — tool-absent degradation

A stub `$STUBDIR/systemctl` and `$STUBDIR/systemd-analyze` (both `#!/bin/sh` + `exit 127`)
are placed first on PATH. Every reading degrades:

```
BLOCKED reading=SEARCHPATH reason=tool-absent
BLOCKED reading=MASKED   reason=tool-absent
BLOCKED reading=CAT      reason=tool-absent
BLOCKED reading=TEMPLATE reason=tool-absent
BLOCKED reading=ALIAS    reason=tool-absent
BLOCKED reading=UNITSTATE reason=tool-absent
rc=1
```

The probe reports an unresolvable command and a wrapper that returns it is
indistinguishable from one. No partial output, no silent zero-exit.

## 4. Receipt C — echo guard

Hostile names are blocked before any subprocess runs; the name is never echoed, never
reaches a shell, and the reading is a single grammar line:

| input class | probe output | rc |
|---|---|---|
| `cat:worker.service\|forged` | `BLOCKED reading=CAT reason=bad-unit-name` | 1 |
| `cat:worker.service\nSEARCHPATH dirs=99` (real newline) | `BLOCKED reading=CAT reason=bad-unit-name` | 1 |
| `cat:worker.service;rm -rf /` | `BLOCKED reading=CAT reason=bad-unit-name` | 1 |
| `template:../../etc/passwd.service` | `BLOCKED reading=TEMPLATE reason=bad-unit-name` | 1 |
| `template:.hidden.service` (leading dot) | `BLOCKED reading=TEMPLATE reason=bad-unit-name` | 1 |
| `alias:plainname` (no valid suffix) | `BLOCKED reading=ALIAS reason=bad-unit-name` | 1 |
| `alias:bad<TAB>name.service` (real tab) | `BLOCKED reading=ALIAS reason=bad-unit-name` | 1 |
| `alias:bad name.service` (space) | `BLOCKED reading=ALIAS reason=bad-unit-name` | 1 |
| `unitstate:bad"quote.service` | `BLOCKED reading=UNITSTATE reason=bad-unit-name` | 1 |
| `unitstate:bad'quote.service` | `BLOCKED reading=UNITSTATE reason=bad-unit-name` | 1 |
| `unitstate:` + 256×`a` + `.service` | `BLOCKED reading=UNITSTATE reason=bad-unit-name` | 1 |

## 5. Receipt D — hermetic selftest, 21/21

`--selftest` builds a synthetic unit tree under `$TMPDIR` (never `/tmp`) and runs 21
cases: searchpath hermetic + tool-absent; masked hermetic (one `/dev/null` symlink + one
0-byte file, matching `null_or_empty` in load-fragment.c:6247) + tool-absent; cat
hermetic normal + masked + tool-absent + unknown-unit + bad-unit-name; template
instance→template + plain + bad-name; alias valid + self-alias rejection (UF2 ELOOP) +
incompatible target type (UF2 EXDEV) + disallowed alias type `.slice` (UF3
`unit_type_may_alias` — enforced before any filesystem lookup); unitstate static +
masked + not-found + bad-name; first-seen precedence (UF1: an `/etc/shadow.service`
shadows a `/usr/shadow.service` duplicate in the name map). All 21 PASS, rc=0.

## 6. Receipts E/F — frozen instrument controls and attacks

Both frozen instruments are byte-identical to the declaration's recorded digests:
`count-uf-rows-r74.py` sha256 `94d46a5edfcdc00858a1b1c37bc459322fc7e337fba19cc38a85776d0dd36482`
(13-case selftest PASS); `check-r73-routed-r74.py` sha256
`2da4ff1fd8e7ed1287230e43769a1d75233b992b9f04eeb77cc981f2677efd77` (6-case selftest PASS).
No instrument bytes changed during this wave.

`attack-c1-scripted-writer.py` (7 mutants): every scripted-writer attack is rejected
rc=1 by the frozen counter — insufficient grounded tokens, diluted token share, quote
>25 words, quote not verbatim in snapshot, snapshot reuse >2, own-work source kind,
duplicate registry S-ID. Control fixture evaluates met=1 rc=0 before any mutant is
applied. 7/7 caught.

`attack-c2-vacuous.py` (7 mutants): every vacuous or malformed repair draft is
rejected — lesson missing new location, missing superseded location, missing corrected
anchor, heading-only tokens, log missing superseded counts, log missing final counts,
log heading-only. Control fixture evaluates ROUTED_STALE=0 ROUTED_OK=2/2 rc=0.
8/8 caught.

## 7. Mapping to UF rows

| UF row (declared) | probe reading | host evidence |
|---|---|---|
| UF1 search-path priority, first-seen name registration | `SEARCHPATH` (dirs, first, etc_before_usr); `CAT` first-match; T21 hermetic | 12 dirs, `/etc` first, `etc_before_usr=1`; T21: `/etc/shadow.service` wins over `/usr/shadow.service` |
| UF2 symlink alias: reject self-alias (ELOOP); validate target name types (EXDEV) | `ALIAS` (self-alias, incompatible-type blocks); T14/T15 hermetic | `dbus.service`→`dbus-broker.service` resolves; T14 blocks `bad-self.service`; T15 blocks `bad-type.socket` |
| UF3 `unit_type_may_alias` permits service/socket/target/device/timer/path | `ALIAS` pre-check before filesystem access; T16 hermetic | T16 blocks `bad-mount.slice` (type gate, not filesystem); live `.service`/`.target` aliases accepted |
| UF4 `UnitFileState` enabled/linked/masked vs runtime variants; fragment mask sets UNIT_MASKED on `null_or_empty` | `UNITSTATE` (file_state + load_state); `MASKED`; `CAT` (masked=1) | `systemd-remount-fs.service` = `enabled-runtime`; both masked units on `/dev/null`; `passim.service` masked/masked |
| UF5 (with UF4) perpetual units immune from masking | code-gated (`u->perpetual ? UNIT_LOADED : UNIT_MASKED`, load-fragment.c:6250) | no perpetual unit on host carries an on-disk fragment; immune-by-construction |
| UF6 missing system-scope units fall back to `builtin_unit_lookup`; on-disk files and masks unconditionally override built-ins | `UNITSTATE` on not-found; `CAT` fragment path | `nosuch-unit-xyz.service` → not-found (not in builtins); `emergency.service` has on-disk fragment overriding any built-in |

## Limits

The probe is a host observer, not the manager: it cannot load a unit into PID 1 to
observe `UNIT_MASKED` being set, and it cannot create the cross-product of alias types
on a live system (that is what the hermetic fixture covers). The `ALIAS` live reading
reports `may_alias=1` only after both the type gate and the `systemctl is-enabled` =
`alias` (or FragmentPath-is-symlink) check pass; a unit that is not an alias yields
`unknown-unit`, not a false positive. `SEARCHPATH` in fixture mode substitutes
`TSUKUROI_UNIT_DIRS` for `systemd-analyze unit-paths` (documented in the script header).
The host's two masked units are both vendor-preset masks (`passim` disabled-preset,
`systemd-networkd-wait-online` enabled-preset); both resolve to `/dev/null` and both
report `masked/masked`, agreeing with the committed `before/host.txt` capture.

Report: `.ufo/waves/round-74/w1/E3HostProbe.md`
