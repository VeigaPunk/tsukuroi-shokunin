# SC1Entry report — C1 knowledge entry draft (round 73, wave w1)

status: complete
verdict: C1 draft meets the frozen counter on a fixture mirror carrying my note, the
committed `before/src`, and the three registry rows the note cites; it does not yet score at
`HEAD`, because `corpus/SOURCES.md` at `HEAD` (8eeadcb9) stops at S303 and does not register
S304-S306.

## Deliverable

`systemd-unit-load-plane-r73.md` — the whole note, in this directory, ready to be copied to
`corpus/knowledge/systemd-unit-load-plane-r73.md`: front matter paragraph (plane, why repair
needs it, tag v262 vs host 262.1-1-arch, upstream line anchors are not host-build line numbers),
six rows UL1-UL6 in the frozen format, a `## Host readings` table with command plus observed
value, and a `## Limits` section.

Rows and sources:

| row | source | snapshot | subject |
|---|---|---|---|
| UL1 | S304 | systemd.unit.xml | compiled load path; earlier directory wins; `$SYSTEMD_UNIT_PATH` override and empty-component append |
| UL2 | S304 | systemd.unit.xml | drop-in `/etc` > `/run` > `/usr/lib`, drop-ins beat unit files, cross-directory lexicographic order |
| UL3 | S305 | unit.c | `unit_need_daemon_reload`: `strv_equal` set change, per-drop-in `fragment_mtime_newer`, masked drop-ins omitted |
| UL4 | S305 | unit.c | mask as empty file or `/dev/null`; `null_or_empty` still-masked test |
| UL5 | S306 | install.c | `unit_file_mask` writes `/dev/null` symlink under config path; `masked` vs `masked-runtime` states |
| UL6 | S306 | install.c | `[Install] Alias=` parsed at enable time; dangling alias ignored |

## Counter evidence

`python3 tools/count-ul-rows-r73.py --fixture "$S/mirror"` on the mirror described above:

```
UL_ROW ok UL1 source=S304 snapshot=systemd.unit.xml
UL_ROW ok UL2 source=S304 snapshot=systemd.unit.xml
UL_ROW ok UL3 source=S305 snapshot=unit.c
UL_ROW ok UL4 source=S305 snapshot=unit.c
UL_ROW ok UL5 source=S306 snapshot=install.c
UL_ROW ok UL6 source=S306 snapshot=install.c
UL_ROWS=6 UL_VERIFIED=6 UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0
UL_TARGET rows=6 verified=6 sources>=3 snapshots>=3 max_reuse=2 met=1
rc=0
```

Saved verbatim as `counter-output.txt`. Two further runs:

- `--selftest` (TMPDIR inside my scratch, not `/tmp`): `SELFTEST: PASS (11 cases, 11 passed, 0 failed)`, rc 0.
- `--revision HEAD`: `UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md`, rc 128 —
  expected, the note is my draft and is not committed.
- Instrument identity: `sha256sum tools/count-ul-rows-r73.py` =
  `542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6` (matches the declaration);
  `tools/check-r72-routed-r73.py` = `93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e`
  (matches; not touched by this seat). Neither instrument was edited.

## Blocking dependency for the L1 commit

C1 requires `source=S304/S305/S306` to resolve in `corpus/SOURCES.md`, and that registry has no
row past S303 at `HEAD`:

```
$ git show HEAD:corpus/SOURCES.md | grep -E '^\| S[0-9]{3} ' | tail -1
| S303 | kmod v34 tools/modprobe.c — https://git.kernel.org/...
$ git show HEAD:corpus/SOURCES.md | grep -cE '^\| S30[4-6] '
0
```

The note can only verify once three rows exist with (a) `kind` = `docs` for S304 and `code` for
S305/S306, (b) a `source` cell containing the exact URL recorded in `before/src/SOURCES.json`
(`https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml`, `.../src/core/unit.c`,
`.../src/shared/install.c`), and (c) an `anchor` cell containing the snapshot basename
(`systemd.unit.xml`, `unit.c`, `install.c`). My mirror used exactly that shape; without it the
counter reports `source-unregistered`, `source-not-bound` and `anchor-not-bound`.

## Falsification attempts against my own rows

Each mutation applied to a fresh copy of the mirror, then the frozen counter re-run; full output in
`counter-mutations.txt`.

| attempt | counter result | verdict |
|---|---|---|
| truncate UL1 to a 4-word statement | `UL1 statement-words=4 statement-grounding=1/2`, rc 1 | held |
| fabricate UL4 quote | `UL4 quote-absent`, rc 1 | held |
| re-point UL6 at S304 | `UL6 source-not-bound anchor-not-bound`, rc 1 | held |
| cite `unit.c` a third time | `snapshot-reuse unit.c=3`, rc 1 (plus `quote-absent`) | held |
| duplicate UL6 id as UL5 | `UL5 duplicate-id`, rc 1 | held |
| append a shapeless `| UL7 |` line | `malformed-row`, `UL_MALFORMED=1`, rc 1 | held |
| replace UL2 with a 20-word word salad of snapshot tokens | `UL_ROWS=6 UL_VERIFIED=6 ... met=1`, rc 0 | **survived** |

The survived case is a real instrument limit worth stating in the closure: the counter scores word
count, distinct-token overlap (`>=6` and share `>=0.5`), digest, registry binding and verbatim quote
placement, and cannot distinguish a true statement from snapshot vocabulary in arbitrary order.
`grounding()` lowercases and searches; it has no order or semantics test. My rows are therefore
asserted against the snapshots by reading, not merely by passing the counter: UL1/UL2 from
`systemd.unit.xml:365-378` and `233-250`, UL3/UL4 from `unit.c:3859-3878` and `3884-3915`,
UL5/UL6 from `install.c:2350-2391`, `3881-3894`, `1261`, `1392`, `350-351`.

## Host readings (re-measured read-only, 2026-11-03)

Every value matched the committed `before/host.txt`:

| command | observed |
|---|---|
| `systemd-analyze unit-paths` | 12 directories, `/etc/systemd/system.control` first, `/run/systemd/generator.late` last |
| `systemctl list-unit-files --state=masked --no-legend` | 2 rows (`passim.service masked disabled`, `systemd-networkd-wait-online.service masked enabled`) |
| `systemctl list-unit-files --state=masked-runtime --no-legend` | 0 rows (rc 1) |
| `systemctl show -p Id -p LoadState -p FragmentPath -p UnitFileState passim.service` | `LoadState=masked`, `FragmentPath=/etc/systemd/system/passim.service`, `UnitFileState=masked` |
| same for `systemd-networkd-wait-online.service` | `LoadState=masked`, `FragmentPath=/etc/systemd/system/systemd-networkd-wait-online.service` |
| `ls -l` both mask paths | both `-> /dev/null` |
| `systemctl show -p Id -p LoadState -p FragmentPath -p DropInPaths user@1000.service` | `FragmentPath=/usr/lib/systemd/system/user@.service`; drop-ins `10-login-barrier.conf` under `/usr/lib`, `faster-shutdown.conf` under `/etc` |
| `systemctl show -p Id -p LoadState -p FragmentPath getty@tty1.service` | `LoadState=loaded`, `FragmentPath=/usr/lib/systemd/system/getty@.service` |
| `find /etc/systemd/system -maxdepth 1 -type f \| wc -l` | 0 |
| `find /etc/systemd/system -maxdepth 1 -type l \| wc -l` | 10 |
| `find /etc/systemd/system -maxdepth 1 -type l -lname /dev/null \| wc -l` | 2 |
| `/usr/lib/systemd/systemd --version`; `pacman -Q systemd`; `uname -r` | `systemd 262 (262.1-1-arch)`; `systemd 262.1-1`; `7.2.11-arch1-1` |

No unit was started, stopped, masked, unmasked, enabled, disabled or edited.

## Notes and limits

- The note states `/dev/null` for the mask form and `/etc` > `/run` > `/usr/lib` as documented,
  because the quoted snapshot lines carry no `/dev/null` string in `unit.c` and no plain path text
  in the precedence sentence (markup interrupts it), so those two phrases are carried by the
  statement while the quotes stay bitexact. `null_or_empty` is called at `unit.c:3876` but defined
  outside the snapshot set; the note says so.
- The note declares upstream anchors as v262 snapshot lines, not host-build line numbers.
- No tool was installed or upgraded; pacman was not used.
- Scratch `/fast/scratch/hyaku/tsukuroi-r73/SC1Entry` was created and removed inside each shell
  (trap); the mutation driver removed only its `mut/` subtree and left the empty root, which I then
  removed and verified absent before yield.

## Lane state observed (not my edit)

At my first instrument check (~23:07) `tools/check-r72-routed-r73.py` in the lane working tree
hashed to the frozen `93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e`. At my final
check the lane reports:

```
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain
 M tools/check-r72-routed-r73.py
$ git -C ... diff --stat
 tools/check-r72-routed-r73.py | 161 +++++++++++++++++++++++++++++-------------
 1 file changed, 113 insertions(+), 48 deletions(-)
$ sha256sum tools/check-r72-routed-r73.py
316dd51aacc29e1590fbea27657e81956a30198f377d14c52d41ae2369419441  tools/check-r72-routed-r73.py
$ git show HEAD:tools/check-r72-routed-r73.py | sha256sum
93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e  -
```

I did not make this edit and did not revert it (no `git checkout`/`restore`). The frozen C2
instrument's working-tree copy is therefore no longer the declared digest while its committed
version still is. `tools/count-ul-rows-r73.py` remains at the declared
`542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6` and is not in `git status`.
The L1 should decide whether the peer's edit is the declared repair path or an out-of-band change,
and should re-verify the C2 instrument digest at commit time.

My own defect, fixed before yield: the mutation driver left the empty scratch root
`/fast/scratch/hyaku/tsukuroi-r73/SC1Entry` behind after removing only its `mut/` subtree; I removed
the root and verified it absent.

Resolution (L1 `TsukuroiR73`, after this report was first written): the drift was the L1's own C2
hardening pass, not a seat edit. The final bytes are pinned at
`328a6bf60c5237fe4ba857b36d2b4401833a61b933f735ec468139b7531a03fe` (`--selftest` PASS 11/11,
re-checked by me on 2026-11-03), with the SCORECARD erratum `93f034e3…` → `328a6bf6…`, the four
attacks that forced it (F2 digest direction, F4 receipt-path superstring, F6 vacuous keyword list,
F7 "ten" substring) and a re-run before control landing before the repair commit. `check-r72-routed-r73.py`
is frozen at `328a6bf6…` for any further C2 scoring; `count-ul-rows-r73.py` remains
`542f9c29…a3d6`. S304-S306 plus two rejected rows (S307, S308) are planned in the same commit as
the note, with R1Reviewer's per-row entailment verdicts deciding any statement wording.

## Artifacts

- `systemd-unit-load-plane-r73.md` — the draft note (deliverable)
- `counter-output.txt` — final `--fixture`, `--selftest` and `--revision HEAD` transcripts
- `counter-mutations.txt` — the seven falsification attempts and their counter output
- `.ufo/waves/round-73/w1/SC1Entry.md` — the seat report
