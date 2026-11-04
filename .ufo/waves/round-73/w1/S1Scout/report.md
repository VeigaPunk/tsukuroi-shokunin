# S1Scout — independent second-route proof of the v262 snapshots, quote locations, host re-capture

status: complete
verdict: held — no claim-breaking delta; the three pinned snapshots are the upstream v262 bytes by three
independent GitHub endpoints plus the resolved tag commit, all six planned quotes sit in the committed
snapshots at the ranges below, and the host surface re-captures to `HOST_DELTAS=0`.
seat: S1Scout (scout, round 73 / wave w1 / hyaku 15)
lane: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin
captured: 2026-11-03 ~23:06–23:10 -03:00, Linux 7.2.11-arch1-1, systemd 262 (262.1-1-arch), kmod 34.2
tools installed/upgraded: none (curl, git, python3 stdlib sufficed)
scratch: /fast/scratch/hyaku/tsukuroi-r73/S1Scout, trap-deleted per shell, removed before yield

`ROUTE2_OK=3/3`

---

## 1. Second-route re-fetch: the committed snapshots are the upstream v262 bytes

All three files were fetched again by more than one route and compared against the committed working
tree **and** against the Git blob the frozen counter actually reads (`--revision` reads git objects).

### 1.1 Digests, computed — not trusted

```
$ cd .ufo/waves/round-73/before/src && sha256sum *.xml *.c
eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6  systemd.unit.xml
c11cd57579931f04ab08f17fe058fd9d4a962c0fe5c4c4a9d5ae2e86c7e6ef4d  install.c
47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7  unit.c
```

These equal `before/src/SHA256SUMS` line for line, and the byte sizes equal the `bytes` fields in
`before/src/SOURCES.json`:

```
$ stat -c '%n %s' *
SHA256SUMS 232
SOURCES.json 739
install.c 140296
systemd.unit.xml 165445
unit.c 263849
```

Git-object view (what the counter sees), at HEAD `8eeadcb92ad5362cae155e1903cdf11b52a5ac5d` and at the
declaration commit `749371321c00f04d98c29d2c26b57d75a92d7e37` — identical:

```
$ for f in systemd.unit.xml unit.c install.c; do git cat-file blob "HEAD:.ufo/waves/round-73/before/src/$f" | sha256sum; done
eb9479be... systemd.unit.xml  (HEAD)
47e98d39... unit.c            (HEAD)
c11cd575... install.c         (HEAD)
$ for f in ...; do git cat-file blob "74937132:.ufo/waves/round-73/before/src/$f" | sha256sum; done
eb9479be... systemd.unit.xml  (declaration commit)
47e98d39... unit.c            (declaration commit)
c11cd575... install.c         (declaration commit)
```

### 1.2 Route table (all three files, all routes)

| file | committed / SHA256SUMS | raw `github.com/.../raw/v262/<path>` | codeload `tar.gz/refs/tags/v262` | contents API `?ref=v262` (base64-decoded) | raw by tag commit `8cc40e0c` | verdict |
|---|---|---|---|---|---|---|
| `man/systemd.unit.xml` | `eb9479be…f82714c6` | `eb9479be…` | `eb9479be…` | `eb9479be…` | `eb9479be…` | MATCH |
| `src/core/unit.c` | `47e98d39…a92efcb7` | `47e98d39…` | `47e98d39…` | `47e98d39…` | `47e98d39…` | MATCH |
| `src/shared/install.c` | `c11cd575…c7e6ef4d` | `c11cd575…` | `c11cd575…` | `c11cd575…` | `c11cd575…` | MATCH |

Byte comparison, not just digest comparison:

```
$ tar -xzf v262.tar.gz systemd-262/man/systemd.unit.xml systemd-262/src/core/unit.c systemd-262/src/shared/install.c
$ sha256sum systemd-262/man/systemd.unit.xml systemd-262/src/core/unit.c systemd-262/src/shared/install.c
eb9479bea50ccb0e7643836ec083e8ef68bdf9ef2b26f31839939168f82714c6  systemd-262/man/systemd.unit.xml
47e98d394462e05bf4bc0be2d1105fa8c21044cc9f5ebf00464f1742a92efcb7  systemd-262/src/core/unit.c
c11cd57579931f04ab08f17fe058fd9d4a962c0fe5c4c4a9d5ae2e86c7e6ef4d  systemd-262/src/shared/install.c
$ cmp -s <tarball file> <.ufo/.../before/src/<file>>   # per file
IDENTICAL systemd.unit.xml
IDENTICAL unit.c
IDENTICAL install.c
```

Contents-API route (independent endpoint and encoding):

```
api_man_systemd.unit.xml.json  blob=54d24961893748d6aa56d22aa57bf37d61254735  len=165445  sha256=eb9479be…
api_src_core_unit.c.json       blob=805642f2d35a63ea8c9c0ca8a328aa9ca999ecf1  len=263849  sha256=47e98d39…
api_src_shared_install.c.json  blob=f8f05c624f99fdc59a0c646ff4f91548e5af44e6  len=140296  sha256=c11cd575…
```

### 1.3 The tag resolves to the commit whose bytes we verified

```
$ git ls-remote --tags https://github.com/systemd/systemd 'refs/tags/v262*'
1f7dffaf714cc4488159c498b7a17cf34c5a96d5	refs/tags/v262
8cc40e0c5e9234bf45084751ac53b1fbfe70b492	refs/tags/v262^{}
$ curl …/git/tags/1f7dffaf714cc4488159c498b7a17cf34c5a96d5
tag_object commit 8cc40e0c5e9234bf45084751ac53b1fbfe70b492
tag_message_first systemd v262
tag_signed= True
verified= True
reason= valid
tagger= Luca Boccassi luca.boccassi@gmail.com
commit_verified= False reason= unsigned
commit_date= 2026-09-22T13:12:10Z
```

So the chain is: signed annotated tag `v262` (GitHub reports the PGP signature `valid`) → commit
`8cc40e0c5e9234bf45084751ac53b1fbfe70b492` → bytes fetched by that commit SHA, by the tag, and from the
release tarball, all identical to the committed snapshots.

### 1.4 Rejected route (recorded, not counted)

`https://gitlab.freedesktop.org/systemd/systemd/-/raw/v262/<path>` is **auth-walled**, so it cannot
serve as an independent-host route:

```
$ curl -sSL -D hdr.txt -o gl_man_systemd.unit.xml https://gitlab.freedesktop.org/systemd/systemd/-/raw/v262/man/systemd.unit.xml
location: https://gitlab.freedesktop.org/users/sign_in
HTTP/2 200
content-type: text/html; charset=utf-8
content-length: 19551
$ file gl_man_systemd.unit.xml
HTML document, Unicode text, UTF-8 text … <!DOCTYPE html> … html-devise-layout gl-system
```

The three "different" digests from that attempt are three different sign-in HTML pages (19551/19550/19550
bytes), not source. `git ls-remote` against the same host prompts for a username and fails. This route
contributes **nothing** to `ROUTE2_OK`; it is a limit, not a delta.

---

## 2. The six planned quotes, located after whitespace normalization

Method: replicate the counter's normalization (`norm(s) = " ".join(s.split())`, `tools/count-ul-rows-r73.py:132`),
build a token → source-line map over each committed snapshot, find the normalized quote, and report the
first and last source lines it touches. Each quote occurs **once** case-sensitively; word counts are
≤ 20 (limit 25, `tools/count-ul-rows-r73.py:44`), none contains `|`, none contains `"`, so all six fit the
row grammar `| quote="…" |` (`tools/count-ul-rows-r73.py:228-233`).

```
quote=systemd.unit.xml:368-370
quote=systemd.unit.xml:238-239
quote=unit.c:3875-3875
quote=unit.c:3908-3908
quote=install.c:345-345
quote=install.c:351-351
```

| label | quote (whitespace-normalized) | words | lines | enclosing context (observed) |
|---|---|---|---|---|
| manifest-1 | Unit files found in directories listed earlier override files with the same name in directories lower in the list | 19 | `systemd.unit.xml:368-370` | inside `<refsect1><title>Unit File Load Path</title>` (364-365), `<para>` opens 367; the quote wraps across 368/369/370 |
| manifest-2 | Multiple drop-in files with different names are applied in lexicographic order, regardless of which of the directories they reside in | 20 | `systemd.unit.xml:238-239` | drop-in precedence paragraph (`.d/` in `/etc`, `/run`, `/usr/lib`); wraps 238/239 |
| unitc-1 | For masked files check if they are still so | 9 | `unit.c:3875` | `static bool fragment_mtime_newer(...)` (3859), `if (path_masked)` branch |
| unitc-2 | any drop-ins that are masked are simply omitted from the list | 11 | `unit.c:3908` | `bool unit_need_daemon_reload(Unit *u)` (3884), inside `if (u->load_state == UNIT_LOADED)` |
| instc-1 | Unit %s is masked, ignoring. | 5 | `install.c:345` | `static void install_change_dump_success(...)` (331), `case INSTALL_CHANGE_IS_MASKED:` (344) |
| instc-2 | Unit %s is an alias to a non-existent unit, ignoring. | 10 | `install.c:351` | same function, `case INSTALL_CHANGE_IS_DANGLING:` (350) |

Raw wrapped lines behind the two XML ranges (the `grep` line numbers are the wrap anchors, not the quote
bounds):

```
367:    <para>Unit files are loaded from a set of paths determined during
368:    compilation, described in the two tables below. Unit files found
369:    in directories listed earlier override files with the same name in
370:    directories lower in the list
371:    <xi:include href="standard-conf.xml" xpointer="usr-local-footnote" />.

237:    in <filename>/usr/lib/</filename>. Drop-in files under any of these directories take precedence
238:    over unit files wherever located. Multiple drop-in files with different names are applied in
239:    lexicographic order, regardless of which of the directories they reside in.</para>
```

### Should the note cite these line numbers?

**Yes — as v262 citations, exactly as above.** They are audit evidence, not a counter gate: the frozen
counter checks only `norm(quote) in norm(snapshot)` plus pipe/word limits (`tools/count-ul-rows-r73.py:228-233`);
it has **no line-number clause**. So a note that cites `install.c:345` and `install.c:351` for v262 is
correct and adds human-checkable depth, but omitting the numbers would still pass the instrument.

Two cautions for the note author:

1. **manifest-2 uniqueness is case-sensitive.** The capital-M sentence above occurs once, but a lowercase
   near-duplicate occurs in the top-level `type.d/` paragraph at lines 246-248
   ("… multiple drop-in files with different names are applied in lexicographic order, regardless of which
   of the directories they reside in, so a file in …"). Measured: `occurrences_case=1`,
   `occurrences_nocase=2`. Quote the **full capital-M sentence** (or at least start at "Multiple drop-in
   files …"), never the shared tail `regardless of which of the directories they reside in`, which is
   ambiguous.
2. **Line numbers are v262-specific.** Under the host's patch release v262.1 the two install.c quotes sit
   at 348 and 354 (see §5). A row that says `snapshot=install.c` and `digest=c11cd575…` must cite 345/351;
   citing 348/354 against that digest would be wrong.

### Falsification attempts on the quote predicate

| attempt | command | result |
|---|---|---|
| claim a quote that is not in the snapshot | normalized-search for `"For masked files check if they are still so"` in `install.c` | absent — the counter's `quote-absent` clause would fire (row cannot pass on a fabricated quote) |
| use an ambiguous tail phrase | `grep -c "regardless of which of the directories"`-style search | case-sensitive full sentence unique; the tail alone is **not** unique (2 hits under case-insensitive search), so a lazy short quote is a real risk for the author, though the capital-M full sentence is safe |
| cite a digest with the wrong snapshot | digest cross-check | `ULA` rows bind digest → `SOURCES.json` → registry URL; a v262.1 `install.c` digest (`41cea46b…`) is not in `SOURCES.json`, so it cannot be substituted |
| pass line numbers instead of text | counter source inspection (`228-233`) | no line clause exists; line numbers cannot satisfy anything, and a row with only numbers fails `quote-absent` |

---

## 3. Host surface re-captured read-only vs `before/host.txt`

Commands exactly as specified, plus the count commands the committed file uses, run as uid 1000
(`uid=1000(vgpnk)`), no unit mutation:

```
systemd-analyze unit-paths
systemctl list-unit-files --state=masked --no-legend
systemctl show -p DropInPaths -p FragmentPath -p LoadState user@1000.service getty@tty1.service
find /etc/systemd/system -maxdepth 1 -type l -lname /dev/null | wc -l
find /etc/systemd/system -maxdepth 1 -type f | wc -l
find /etc/systemd/system -maxdepth 1 -type f -name '*.service' | wc -l
find /etc/systemd/system -maxdepth 1 -type l | wc -l
find {/etc,/run,/usr/lib}/systemd/system -mindepth 1 -maxdepth 1 -type d -name '*.d' | wc -l
systemctl show -p LoadState -p FragmentPath -p UnitFileState passim.service
```

Raw fresh output:

```
=== unit-paths ===
/etc/systemd/system.control
/run/systemd/system.control
/run/systemd/transient
/run/systemd/generator.early
/etc/systemd/system
/etc/systemd/system.attached
/run/systemd/system
/run/systemd/system.attached
/run/systemd/generator
/usr/local/lib/systemd/system
/usr/lib/systemd/system
/run/systemd/generator.late
=== masked ===
passim.service                       masked disabled
systemd-networkd-wait-online.service masked enabled
=== show ===
LoadState=loaded
FragmentPath=/usr/lib/systemd/system/user@.service
DropInPaths=/usr/lib/systemd/system/user@.service.d/10-login-barrier.conf /etc/systemd/system/user@.service.d/faster-shutdown.conf

LoadState=loaded
FragmentPath=/usr/lib/systemd/system/getty@.service
DropInPaths=
=== masks via find ===
2
=== counts ===
etc-files 0
etc-service-files 0
etc-symlinks 10
/etc dropin-dirs 3
/run dropin-dirs 0
/usr/lib dropin-dirs 12
=== passim ===
LoadState=masked
FragmentPath=/etc/systemd/system/passim.service
UnitFileState=masked
```

### Host delta table — empty

| # | field | command | expected (`before/host.txt`) | fresh | delta |
|---|---|---|---|---|---|
| 1 | search-path directories | `systemd-analyze unit-paths` | 12 lines, same order | 12 lines, same order | none |
| 2 | masked rows | `systemctl list-unit-files --state=masked --no-legend` | `passim.service masked disabled`; `systemd-networkd-wait-online.service masked enabled` | identical | none |
| 3 | `user@1000.service` DropInPaths | `systemctl show …` | `/usr/lib/systemd/system/user@.service.d/10-login-barrier.conf /etc/systemd/system/user@.service.d/faster-shutdown.conf` | identical | none |
| 4 | `user@1000.service` FragmentPath | same | `/usr/lib/systemd/system/user@.service` | identical | none |
| 5 | `user@1000.service` LoadState | same | `loaded` | `loaded` | none |
| 6 | `getty@tty1.service` FragmentPath | same | `/usr/lib/systemd/system/getty@.service` | identical | none |
| 7 | `getty@tty1.service` LoadState | same | `loaded` | `loaded` | none |
| 8 | masks via find | `find … -lname /dev/null \| wc -l` | 2 | 2 | none |
| 9 | files in `/etc/systemd/system` | `find … -type f \| wc -l` | 0 | 0 | none |
| 10 | `.service` files in `/etc/systemd/system` | `find … -name '*.service' \| wc -l` | 0 | 0 | none |
| 11 | symlinks in `/etc/systemd/system` | `find … -type l \| wc -l` | 10 | 10 | none |
| 12 | `/etc` drop-in dirs | `find … -name '*.d' \| wc -l` | 3 | 3 | none |
| 13 | `/run` drop-in dirs | same | 0 | 0 | none |
| 14 | `/usr/lib` drop-in dirs | same | 12 | 12 | none |
| 15 | `passim.service` LoadState / FragmentPath / UnitFileState | `systemctl show …` | `masked` / `/etc/systemd/system/passim.service` / `masked` | identical | none |

Scripted tally: `HOST_DELTAS=0 HOST_CHECKS=15`.

One honest note on method: my first diff script printed a false `DELTA unit-paths :: 12 vs 17` because it
took every line in `host.txt` beginning with `/`, which also captures the five count lines
(`/etc/systemd/system regular units: 0`, … `/run/systemd/system drop-in dirs (*.d): 0`). Re-scoped to the
`## unit search path` section, the comparison is 12 vs 12. The host file's own superseded-line note
(“the earlier 'regular units: 0' line was a bad find expression”) is consistent with my re-measure
(0 files, 0 `.service` files, 10 symlinks, 2 masks).

---

## 4. Unclaimed probe: are `/usr/lib/systemd/system/*.d/` drop-ins visible without privilege?

The round does not claim this. Observed as uid 1000 (no sudo, no unit mutation):

```
$ ls -ld /etc/systemd/system /run/systemd/system /usr/lib/systemd/system
drwxr-xr-x 1 root root  1006 Oct 20 09:48 /etc/systemd/system
drwxr-xr-x 2 root root    40 Nov  2 12:07 /run/systemd/system
drwxr-xr-x 1 root root 26798 Oct 29 03:45 /usr/lib/systemd/system

$ ls -ld /etc/systemd/system/*.d /run/systemd/system/*.d /usr/lib/systemd/system/*.d
drwxr-xr-x /etc/systemd/system/docker.service.d
drwxr-xr-x /etc/systemd/system/plocate-updatedb.service.d
drwxr-xr-x /etc/systemd/system/user@.service.d
drwxr-xr-x /usr/lib/systemd/system/snapper-boot.timer.d
drwxr-xr-x /usr/lib/systemd/system/snapper-cleanup.service.d
drwxr-xr-x /usr/lib/systemd/system/snapper-timeline.timer.d
drwxr-xr-x /usr/lib/systemd/system/systemd-hibernate.service.d
drwxr-xr-x /usr/lib/systemd/system/systemd-homed.service.d
drwxr-xr-x /usr/lib/systemd/system/systemd-hybrid-sleep.service.d
drwxr-xr-x /usr/lib/systemd/system/systemd-suspend.service.d
drwxr-xr-x /usr/lib/systemd/system/systemd-suspend-then-hibernate.service.d
drwxr-xr-x /usr/lib/systemd/system/systemd-udevd.service.d
drwxr-xr-x /usr/lib/systemd/system/user@0.service.d
drwxr-xr-x /usr/lib/systemd/system/user@.service.d
drwxr-xr-x /usr/lib/systemd/system/user-.slice.d
ls: cannot access '/run/systemd/system/*.d': No such file or directory
```

- `/etc`: 3 drop-in dirs, all `drwxr-xr-x` — listable/traversable unprivileged. **Held.**
- `/usr/lib`: 12 drop-in dirs, all `drwxr-xr-x` — listable/traversable unprivileged. **Held.**
- `/run`: **zero** `*.d` dirs exist (the directory itself is `drwxr-xr-x`, so a drop-in dir would be
  readable if present, but there is nothing to observe). **Vacuous, not demonstrated.**
- File-level: `find /etc/systemd/system /run/systemd/system /usr/lib/systemd/system -mindepth 2 -maxdepth 2
  -path '*.d/*' -type f ! -perm -0444` returned **no rows** — every drop-in file present is world-readable.
  Sampled reads as uid 1000 succeed, e.g.:
  `-rw-r--r-- /etc/systemd/system/user@.service.d/faster-shutdown.conf` (`[Service] TimeoutStopSec=5s`),
  `-rw-r--r-- /usr/lib/systemd/system/user@.service.d/10-login-barrier.conf` (605 B),
  `-rw-r--r-- /usr/lib/systemd/system/systemd-udevd.service.d/50-rc_keymap.conf` (95 B).

So the unprivileged-visibility claim that the round does not make would be **held for `/etc` and
`/usr/lib` and vacuous for `/run`** on this host, at this capture time.

---

## 5. Pinned v262 vs the host's shipped v262.1 (a limit the note must not paper over)

The host runs `systemd 262 (262.1-1-arch)`. The round pins **v262**, one patch release behind. Two of the
three files are bit-identical between `v262` and `v262.1`; `install.c` is not:

| file | v262 (pinned) | v262.1 (host tag) | relation |
|---|---|---|---|
| `man/systemd.unit.xml` | `eb9479be…f82714c6` | `eb9479be…f82714c6` | identical |
| `src/core/unit.c` | `47e98d39…a92efcb7` | `47e98d39…a92efcb7` | identical |
| `src/shared/install.c` | `c11cd575…c7e6ef4d` | `41cea46b…baccfa7` (`41cea46befd50bfb0168b823832bdce5103e5e6cc1aaf794f6db4bd51820a1d4`) | **4 hunks, +8/−5 lines** |

The four hunks (`diff -u before/src/install.c <v262.1 install.c>`, `@@` headers at 251, 262, 3688, 3727):

1. `path_is_vendor_or_generator()` — adds `int r;`.
2. Same function — replaces `if (path_is_generator(lp, rpath)) return true;` with a call on the
   root-prefixed `path` and propagation of the nonzero return value
   (`r = path_is_generator(lp, path); if (r != 0) return r;`), with the comment “The lookup paths are root
   prefixed, so we have to pass in a root prefixed path.”
3. `unit_file_preset()` — `InstallContext plus = { .scope = scope }, minus = { .scope = scope }`.
4. `unit_file_preset_all()` — same scope-initialization change.

Impact on this round: **the two quoted install.c strings are unchanged** — in v262.1 they sit at lines
348 and 354 (v262: 345 and 351) with identical text (`grep -n` verified). So the note's quotes are true of
both releases; only the line numbers move. But any note sentence that generalizes v262 `install.c`
behaviour of `path_is_vendor_or_generator` (vendor/generator classification) to “the host” is one patch
release stale: the host's 262.1 changed that function. The round's own claim is only about v262 bytes, so
this is a limit to state, not a defect in the claim.

---

## 6. Attack summary (each attempt with its command)

| # | attack | command (abbreviated) | outcome |
|---|---|---|---|
| 1 | trust the committed digests | recomputed `sha256sum` on all three | held — digests reproduce |
| 2 | working-tree only, not committed | `git cat-file blob HEAD:… \| sha256sum`; same at declaration commit | held — git-object bytes identical at both revisions |
| 3 | one endpoint only | raw + codeload tarball + contents API + commit-SHA raw | held — 3/3 (+commit route) agree; `cmp` identical |
| 4 | tag points somewhere else | `git ls-remote` + tags API object resolution | held — signed tag `v262` → commit `8cc40e0c`, signature `verified=true reason=valid` |
| 5 | independent non-GitHub host | gitlab.freedesktop.org raw, `-L` | **unavailable** — sign-in HTML (HTTP 200, `text/html`), recorded as a limit |
| 6 | fabricated/ambiguous quote | normalized search, case-sensitive and case-insensitive counts | held for the capital-M full sentence (1 hit); the shared tail is ambiguous (2 hits) — author caution |
| 7 | quote constraints | word/pipe/double-quote counts | held — max 20 words (limit 25), no `|`, no `"` |
| 8 | stale line numbers | v262 vs v262.1 grep | held for text, shifted by +3 lines under v262.1 — cite v262 numbers only |
| 9 | host drift since the committed capture | 15-field scripted re-capture | held — `HOST_DELTAS=0` |
| 10 | unprivileged drop-in visibility (unclaimed) | `ls -ld`, `find ! -perm -0444`, sampled reads | held for /etc and /usr/lib; vacuous for /run (0 dirs) |

## Limits

1. **All working routes terminate at GitHub.** raw.githubusercontent.com, codeload.github.com and
   api.github.com are distinct endpoints/pipelines but one forge/account trust domain. The only candidate
   independent host (gitlab.freedesktop.org mirror) is auth-walled and returned sign-in HTML, so I could
   not cross-check outside GitHub. A compromised GitHub tag+tree would pass every route I ran.
2. **Signature scope.** GitHub reports the annotated tag `v262` signature as `verified=true, reason=valid`
   (tagger Luca Boccassi; message begins “systemd v262”). I did not independently fetch and verify the PGP
   signature against a locally trusted keyring, and the release commit itself is unsigned
   (`verified=false, reason=unsigned`), which is normal for this project.
3. **Line numbers are normalization-derived, not counter-gated.** The frozen counter checks quote text
   (`norm(quote) in norm(snapshot)`), word count ≤ 25 and no pipe (`tools/count-ul-rows-r73.py:228-233`);
   it has no line clause. The ranges in §2 are what a human should cite for v262; they are not what makes
   the counter pass.
4. **No live merge-plane behaviour was exercised.** The lane is read-only: I did not start/stop/mask/
   enable any unit, and I did not test override/drop-in resolution dynamically. Host statements are static
   surface readings (`systemd-analyze`, `systemctl show`, file system), matching `before/host.txt`.
5. **Host capture is a snapshot in time** (~23:06–23:10 -03:00). No drift was observed within the window,
   but the host is live; the committed `before/host.txt` is from 23:00:38 the same evening.
6. **`/run` visibility is vacuous.** There are zero `*.d` directories under `/run/systemd/system`; the
   parent's `drwxr-xr-x` mode is the only evidence that one would be readable, which is inference, not an
   observation of a drop-in.
7. **v262.1 is what the host ships.** The pinned snapshots are v262; `install.c` differs from the host's
   262.1 in 4 hunks (one in `path_is_vendor_or_generator`, two preset scope initializations). The six
   quotes are text-stable across the patch, but v262 line numbers (345/351) must not be presented as
   262.1 line numbers (348/354), and v262 behaviour claims are one patch behind the installed binary.
8. **I did not exercise the frozen instruments** (`count-ul-rows-r73.py`, `check-r72-routed-r73.py`) beyond
   reading their clauses; that is E1/E2/M seat work. At 23:08 the declared sha256 values did match the files
   on disk (`542f9c29…a3d6` and `93f034e3…9e`); during seat closure the C2 checker's **working tree** began
   changing under me (see §8). The committed C2 blob is still the declared `93f034e3…`.
9. **`systemd.unit.xml` quote spans XML line wraps.** The 368-370 and 238-239 ranges are line ranges after
   whitespace normalization; a tool that greps per line will not find the full sentences on one line
   (line-based `grep -c` returns 0 for the full manifest-1 sentence).

---

## 8. Post-capture observation (outside the C1 source claim): the C2 instrument was mid-edit

While closing this seat, `tools/check-r72-routed-r73.py` changed in the lane working tree. It is **not my
edit** — I never wrote under `tools/`, and `git status` shows an unstaged working-tree modification only.
The new header says it was "hardened post-data against the wave's attacks — see SCORECARD 'Round 73 — C2
instrument repair'". Recorded facts, no verdict:

```
now=2026-11-03T23:11:23-03:00
$ sha256sum tools/check-r72-routed-r73.py
316dd51aacc29e1590fbea27657e81956a30198f377d14c52d41ae2369419441  tools/check-r72-routed-r73.py
$ git diff --stat -- tools/check-r72-routed-r73.py
 tools/check-r72-routed-r73.py | 161 +++++++++++++++++++++++++++++-------------
 1 file changed, 113 insertions(+), 48 deletions(-)

now=2026-11-03T23:11:43-03:00
HEAD-blob-c2   = 93f034e3dbb1edbe73995d11e7bd8311c45c0929f1902e342bf8305f902a2f9e   (declared, frozen)
worktree-c2    = f1c4b4d36b8e2f4c5b85fee9b5de333b604b39606ad9618331c25b44f16048fe
HEAD-blob-c1   = 542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6   (declared, frozen)
worktree-c1    = 542f9c2947139b5c8f6aec7110f1e6c874d106efc7dc05efe6a91f090711a3d6
$ grep -c "Round 73 — C2 instrument repair" SCORECARD.md
0
$ git status --porcelain tools/
 M tools/check-r72-routed-r73.py
```

- The **committed** C2 blob is still the declared `93f034e3…`; the frozen declaration digest is intact in
  Git. Only the working tree drifted.
- The working tree changed twice within 20 s (`316dd51a…` → `f1c4b4d3…`), which is consistent with an
  in-flight edit by another seat, not with a settled instrument.
- At 23:11:43 the SCORECARD section the checker's own header cites does not yet exist, so the old→new
  digest record the declaration requires had not been written at that moment.
- The C1 counter was byte-stable throughout (HEAD blob = worktree = `542f9c29…`).
- Consequence for this seat: none — §1–§5 concern snapshots, quotes and the host, none of which this edit
  touches. Consequence for the lane: C2 must be scored with one fixed instrument; running the checker from
  a working tree that is being edited does not attribute the result to a pinned digest.
