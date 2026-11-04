# Round-73 doc deltas (L1 working copy; the SC3Index drafts amend these)

## 1. `SKILL.md` append — the unit-load merge surface (decision table)

```markdown
## Round 73 — the unit-load merge surface (decision table)

Read-only decision table for an observed unit-file or drop-in shape. Every row rests on a rule row of
`corpus/knowledge/systemd-unit-load-plane-r73.md` (UL1-UL6; sources S304-S306, upstream systemd v262; the
host runs 262.1-1-arch, and the rows' `file:line` anchors are tag anchors, not Arch-build line numbers —
QUALITY 103). **No row authorizes a write:** mask, unmask, enable, disable, unit-file and drop-in edits,
`daemon-reload`, start and stop are the operator's and are never executed, attempted or retried here.
The table never states the effective merged value of a specific unit: the surface yields precedence and
order, not a resolved configuration.

| # | Observed shape (read-only probe) | Verdict | Operator action | Rests on |
|---|---|---|---|---|
| U1 | A drop-in file the operator wrote is present, and `systemctl show` still returns the old value | DROP-IN NOT MERGED: the file is not in a directory the manager reads for that name, or a same-named file in a higher-priority directory suppresses it. `/etc` beats `/run` beats `/usr/lib`, and a drop-in beats a unit file wherever the unit file lives | Confirm the drop-in's directory and name (`systemctl show -p DropInPaths <unit>` is the manager's own list); edit the highest-precedence copy, since a lower one is inert while the same name exists above it | UL2 |
| U2 | A packaged `/usr/lib/systemd/system/<unit>` carries a setting, and a small drop-in under `/etc/systemd/system/<unit>.d/` names the same setting | DROP-IN WINS FOR THE SETTINGS IT NAMES: drop-ins are parsed after the unit file and take precedence over unit files wherever located, so the packaged value is not the effective one for that key | Read the drop-in list, then decide whether to keep the override; removing it is operator-owned | UL2 |
| U3 | Two drop-ins with different names, in different directories, set the same key | ONE LEXICOGRAPHIC PASS: different names are applied in alphanumeric order regardless of directory, so the later-ordered name wins for a repeated key; a same-named file replaces the earlier one completely | Rename the drop-in to sort where intended (`10-`, `50-`, `90-`); never rely on directory order between different names | UL2 |
| U4 | `systemctl status` reports the unit as changed on disk / needing a reload | STALE MANAGER COPY: the drop-in path list differs from the loaded one, or a drop-in file is newer than the last reload (a masked drop-in is omitted from that list, so removing a mask is also a change) | Run `systemctl daemon-reload` (operator-owned); a reload re-reads units, it does not restart them | UL3 |
| U5 | The unit's fragment path is a zero-size file or a symlink to `/dev/null`; `systemctl show -p LoadState` reads `masked` | MASKED, NOT MISSING: both forms mask, the configuration is not loaded at all, and the unit cannot be activated even manually | Decide whether the mask is intended; unmask/remove is operator-owned. Do not report "unit not found" for a masked unit | UL4 |
| U6 | `systemctl list-unit-files` reads `<unit> masked enabled` (host case: `systemd-networkd-wait-online.service`) | TWO DIFFERENT QUESTIONS: `UnitFileState` is the enablement symlink, `LoadState` is whether the manager loaded a configuration; a mask makes the unit unloadable while the enablement symlink can remain | Read both properties before judging; the mask is what blocks activation, the stale enablement link is cosmetic and is the operator's to clean | UL4; UL5 |
| U7 | An instance such as `foo@bar.service` has no file of its own, and `systemctl show -p FragmentPath` returns `…/foo@.service` | TEMPLATE FALLBACK: the manager looks for the literal name first and then for the template with the instance string removed; the instance inherits the template's file | Read `FragmentPath` rather than guessing a path; an instance-specific file would take precedence if one existed | UL1 (host reading H5) |
| U8 | Drop-ins exist as `foo@.service.d/` (template), `foo-bar-.service.d/` (prefix), and `foo-bar-baz.service.d/` (name) | MERGE ORDER, NOT ONE FILE: for an instantiated unit the instance `.d/` is read first, then the template `.d/`; names containing dashes also search the prefix-truncated directories, and a deeper prefix wins over a shallower one for the same drop-in name | List the drop-ins the manager actually read (`DropInPaths`); editing a prefix directory changes every unit that matches it | UL2 (host reading H4) |
| U9 | `[Install] Alias=` or `Also=` exists in a unit file | INSTALL-TIME, NOT LOAD-TIME: aliases and also-units are applied when the unit is enabled, by writing symlinks; a load does not create them, and an alias pointing at a missing unit is an unresolvable change that is ignored | Enable the unit (operator-owned) to realise the alias; a dangling alias in the install transaction is reported and skipped | UL6 |

Named limits, not table rows: the effective merged content of a named unit is not read here, so no row
states which value wins for a real key on this host; `SYSTEMD_UNIT_PATH` is unset on this host, so the
path-override leg is documented only (UL1); no `[Install] Alias=` symlink was measured (UL6 is a code-level
statement); a drop-in's own content is not read by this lane; and a mask placed in a directory other than
`/etc/systemd/system` is documented by UL4's still-masked test, not measured here.
```

## 2. `PROVINCE.md` append — promotion note

```markdown
## Round-73 entry — R73-UNITLOAD-CORE: the unit-load merge plane enters Core (new area, not a frontier promotion)

Append-only; every earlier section stays as written. This is a **new area**, not a promotion of a listed
frontier bullet: at the declaration base `eb105757` the held-ground sweep read **0** lines for
`unit_load_dropin|dropin_paths|unit_need_daemon_reload|null_or_empty|unit_file_mask|config_parse_alias`
across `corpus/ SKILL.md PROVINCE.md`, **0** files for `unit load path`, `unit search path`,
`FragmentPath` and `DropInPaths`, and the twelve `drop-in` mentions in `corpus/knowledge/` are host
observations of named drop-in files, not merge rules (`.ufo/waves/round-73/before/held-ground.txt`). The
entry is `corpus/knowledge/systemd-unit-load-plane-r73.md`, rows UL1-UL6, sourced S304-S306 (upstream
systemd v262 `man/systemd.unit.xml`, `src/core/unit.c`, `src/shared/install.c`; the host runs
262.1-1-arch).

**Core now — the reading:** the compiled unit load path and its earlier-directory override, with
`SYSTEMD_UNIT_PATH` replacing it (UL1); the drop-in merge and precedence (`/etc` > `/run` > `/usr/lib`,
drop-ins above unit files wherever located, one lexicographic pass across directories, deeper dash-prefix
directories winning) (UL2); the reload condition — a changed drop-in path list or a newer drop-in, masked
drop-ins omitted (UL3); masking by a zero-size file or a `/dev/null` symlink and the `null_or_empty`
still-masked test (UL4); the mask symlink and the `masked`/`masked-runtime` install modes with a
generator mask unmaskable (UL5); and `[Install] Alias=` parsed at enable time with a dangling alias
ignored (UL6).

**Still Frontier:** the effective merged configuration of a named unit on this host (the surface yields
precedence and order, not a resolved value); the `SYSTEMD_UNIT_PATH` leg (unset here); the alias leg
(no alias symlink measured); masks placed outside `/etc/systemd/system`.
**Operator-owned:** every mask, unmask, enable, disable, unit-file or drop-in edit, `daemon-reload`, unit
start/stop and any write under a unit directory.
**Mori's, unchanged:** nothing about capacity or fleet runway is stated here.

Counted by `python3 tools/count-ul-rows-r73.py --revision <REV>` (target `UL_ROWS=6 UL_VERIFIED=6
UL_SOURCES=3 UL_SNAPSHOTS=3 UL_MALFORMED=0`, `met=1`) at the round-73 measured revision in
`SCORECARD.md`.
```

## 3. `corpus/README.md` append — round-73 index

```markdown
## Round 73 — the unit-load merge plane (C1), the r72 routed repairs (C2)

New area, not a frontier promotion: the held-ground sweep at base `eb105757` read 0 hits for the plane's
code anchors and 0 files for `unit load path`/`FragmentPath`/`DropInPaths`
(`.ufo/waves/round-73/before/held-ground.txt`). The C2 move is registry/lesson/tool-record work, not a
coverage row: three round-72 closure defects close in committed bytes.

### Coverage rows — round 73

| Note | Holds | Sources |
|---|---|---|
| `knowledge/systemd-unit-load-plane-r73.md` | The unit-load merge surface at v262, six rule rows UL1-UL6: the compiled load path with earlier-directory override and `SYSTEMD_UNIT_PATH` (UL1); drop-in merge order and `/etc` > `/run` > `/usr/lib` precedence with one cross-directory lexicographic pass and drop-ins above unit files (UL2); the reload condition and omitted masked drop-ins (UL3); masking by empty file or `/dev/null` symlink and the still-masked test (UL4); the mask symlink and the `masked`/`masked-runtime` install modes (UL5); `[Install] Alias=` at enable time with a dangling alias ignored (UL6). Host: 12 search-path directories, two `/dev/null` masks, `user@1000.service` reading template and prefix drop-ins, `getty@tty1.service` resolving to the template | S304-S306 |
| `../tools/count-ul-rows-r73.py` | The frozen row counter (sha256 `542f9c29…`): per row a unique contiguous id, a statement of at least 12 words, at least 6 distinct non-stopword tokens shared with the row's own snapshot text and a shared/total ratio of at least 0.5, a `source=` id present in the registry whose `source` cell carries the map URL and whose `anchor` cell carries the snapshot basename, a snapshot sha256 equal to both the `digest=` cell and the `SOURCES.json` map digest, and a quote of at most 25 words without a pipe located verbatim in those bytes; no snapshot cited more than twice; an eleven-case `--selftest` | S304-S306 |

**Frontier:** the effective merged configuration of a named unit is not read — the entry states precedence
and order, not a resolved value; `SYSTEMD_UNIT_PATH` is unset on this host, so UL1's override leg is
documented only; no `[Install] Alias=` symlink was measured; and a mask outside `/etc/systemd/system` is
documented, not measured.
```

## 4. Gate-registry continuation rows

```markdown
## Round 73 — registry continuation for the two round-73 instruments (append-only)

Append-only rows for the `## Gate and probe registry — round71 superseding current rows` table. The r71
and r72 rows stay as written; these are the round-73 continuations.

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| ul-row-counter | probe | `python3 tools/count-ul-rows-r73.py --revision <REV>` | 0 target met (`met=1`); 1 target missed; 128 note/registry/map absent; 3 self-test failed | `python3 tools/count-ul-rows-r73.py --selftest` — hermetic, eleven cases over fixtures copied under one `$TMPDIR` root (CONTROL, SHORT, UNREGISTERED, QUOTE, FIVE, DUPID, REUSE, UNGROUNDED, MALFORMED, DIGEST, OWNWORK), one named line each; rc 2 when `$TMPDIR` names no directory | `.ufo/waves/round-73/before/src/{SHA256SUMS,SOURCES.json}` (three systemd v262 snapshots) | `$TMPDIR` only in `--selftest`; reads git objects otherwise | tsukuroi |
| r72-routed-checker | probe | `python3 tools/check-r72-routed-r73.py --revision <REV>` | 0 all three routed items satisfied; 1 at least one stale; 2 usage; 3 self-test failed | `python3 tools/check-r72-routed-r73.py --selftest` — hermetic, five cases (CONTROL, LESSON, DIGEST, CAPABILITY, UNANCHORED), fixtures under one `$TMPDIR` root, rc 2 without `$TMPDIR` | the six lesson tokens, the two instrument digests and the capability receipt path are constants in the tool; the r72 instrument sha256 is re-read from the repo | `$TMPDIR` only in `--selftest`; reads git objects otherwise | tsukuroi |
```
