# ConnectorOverlap — sibling-overlap scan + one cross-lane pattern (tsukuroi, round 91, wave w1)

Seat: ConnectorOverlap. Read-only. Lane measured: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
`git rev-parse master` = **`2d7e09e101996cc1ac5836c6d635f3f608453ac5`** (tip at exec; the lane moved
during the wave: `b516d6ae` → `45ae6518` → `3d645e2c` → `2d7e09e1`).

Receipts (this seat's subdir): `receipts/sibling-scan-terms.txt`, `receipts/gate-conformance.txt`,
`receipts/host-build-probe.txt`, `receipts/c2-uri-falsifier.txt`.
Proposed patch (not landed, L1 decides): `ConnectorOverlap/proposed-r91-c2-entry-repair.diff`.

## Axes named (per seat instruction)

| Axis | What it means here | What I measured against it |
|---|---|---|
| **adjacency** | does any sibling lane already hold a claim or instrument that overlaps the r91 rules or the C2 topic, and does it conflict? | 20 sibling lanes swept (§1) |
| **operability** | can an operator run the lane's own gates on the landed r91 artifacts and get a usable answer? | 3 lane gates × the r91 commit chain (§3) |
| **freshness** | does the host-build evidence the C2 entry leans on still hold, and is the host's own state current? | host-build patch-offset probe (§4) |

## 1. Sibling-lane sweep — table of hits (conflicts first)

Command per repo (read-only, as specified):
`git -C <repo> grep -n -i -e limine -e measured_boot -e tpm2 -e LoaderTpm2 -- corpus tools`
Full receipt: `receipts/sibling-scan-terms.txt`. 20 sibling repos swept (all `*-shokunin` under
`/home/vgpnk/Projects/shokunin` except `tsukuroi-shokunin`).

**CONFLICTS: none.** No sibling lane holds a competing statement about Limine's global-section
visibility, `hash_mismatch_panic`, `measured_boot`, TPM presence detection, Secure Boot state, or
partition-GUID/fslabel resolution. The r91 rule set is **uncontradicted** across the fleet. That is a
finding, not a null result: the r91 rules were derived from pinned upstream sources, and no sibling
lane has a competing derivation to collide with.

| # | Repo | file:line | Hit | Class | Bearing on r91 / C2 |
|---|---|---|---|---|---|
| 1 | `mori-shokunin` | `corpus/evidence/sources-r55/Documentation_admin-guide_kernel-parameters.txt.v7.2:7606`; `…v7.3:7640`; `corpus/evidence/sources-r61/kernel-parameters.txt:7640`; `…/v7.2:7606` | `TPM2_PCR_Extend` in the **Linux kernel** parameter docs | **COMPLEMENTS (weak)** | Linux-side TPM prose, not Limine's. Does not bear on `tpm_present()` (firmware TCG2/CC), which is what C2's `--tpm-present` flag asks. Note: `mori` has **no** Limine, `measured_boot`, TPM-presence or Secure-Boot knowledge entry. |
| 2 | `tabi-shokunin` | `corpus/evidence/w4-t4-3-sweep/forensics.log:57` and `:59` | `app-limine-snapper-notify@autostart.service`, `app-limine-snapper-restore@autostart.service` — **systemd user-unit names** from a forensics log | **COMPLEMENTS (weak)** | `limine-snapper-*` unit names only. No `limine.conf` semantics, no pin/URI/measured-boot/TPM content. |
| 3 | `tabi-shokunin` | `.ufo/waves/round-74/w1/R74Connector/scoped-hits.json:12426-12468` | A sibling connector's **own** grep receipt citing tsukuroi's `tools/limine-pin-battery-r87/r88/r89/r90.py` (pinned at `b380483e…`, `TIMEOUT = 20`) | **DUPLICATES (instrument-shaped)** | Confirms the r87–r90 battery lineage is externally indexed; r91 continues that lineage. No competing rule. |
| 4 | `kaidoku-shokunin` | `corpus/lessons/round-30.md:45` (M30-2); `.ufo/waves/round-30/w1/RevOracleVsReadobj.md:9-13` | **`llvm-objcopy --dump-section` without an output-object argument rewrote 4 of its own frozen carriers in place**, and "the 0444 mode did not protect (file rewrite, not write(2))" | **COMPLEMENTS (material — the one cross-lane pattern, §2)** | The same class of defect as tsukuroi's own round-86 `M3` (`corpus/lessons/round-86.md:63-67`, `LP7`). Independent second lane, same mechanism. **See §2.** |
| 5 | `souji-shokunin` | `.ufo/waves/round-79/ctx-tail.txt:4` (also rounds 80/81/82) | Wave-context rule: "never run a binary-editing tool on them (2026-11-06 incident: `objcopy --dump-section` without an output operand rewrote a UKI in place)" | **COMPLEMENTS (material)** | Souji's ctx-tail carries tsukuroi's round-86 incident as a **fleet-wide** rule. Cross-lane propagation of tsukuroi's finding — evidence the r86 lesson is already the fleet's, so tsukuroi need not re-derive it. |
| 6 | `mado-shokunin` | `.ufo/waves/round-56/w3/R56W3MutBwrapChannels/receipts/jail-probe-bwrap.out:656, 1584, 1648, 2180` | The host binaries `/bin/efibootmgr!`, `/bin/limine-update!`, `/bin/llvm-objcopy!`, `/bin/objcopy!` each `errno=20` | **COMPLEMENTS (operability)** | Mado already ran a **read-only** bwrap jail probe that enumerates exactly the host binaries tsukuroi's rules forbid (`objcopy`, `llvm-objcopy`, `limine-update`, `efibootmgr`). A ready-made, already-measured inventory of the dangerous set. |
| 7 | `chousa-shokunin` | `.ufo/waves/round-73/w1/R73S03/.ufo__l0-questions.md.txt:63,64,66,100`; `round-80/w1/R80ConnectorA/tsukuroi--corpus__QUALITY.md.blob:65,67,68,70` | Verbatim copies of tsukuroi's own `l0-questions` and `QUALITY.md` in chousa wave dirs (incl. the `limine-snapper-sync` / `limine-mkinitcpio-install` writer rows) | **DUPLICATES (stale copy)** | Wave-dir artefacts, not lane knowledge. Note the copies are of tsukuroi's *writer* plane (r19), predating the r87–r91 pin plane entirely. |
| 8 | `kake-shokunin` | `.ufo/waves/round-92/w1/ConnectorScope/receipts/query-422.txt:220-243`; `query-stale.txt:1009-1054` | A sibling connector's grep over tsukuroi's `corpus/knowledge/*` (mkinitcpio-v42, boot-chain-r17, limine-pin-writers r88 freshness) | **DUPLICATES (instrument-shaped)** | Same connector-grep instrument, different round. No competing Limine claim. |
| 9 | `kasegi-shokunin` | `.ufo/waves/round-94/w1/ConnectorOverlap-receipts/sibling-scorecards.txt:33`; `round-96/w1/ConnectorOverlap-receipts/sibling-grep-attribution-tools.txt:217-218`; `round-97/w1/.../sibling-grep-attribution-tools.txt:194-195` | Kasegi's connector scores tsukuroi's `boot-chain-audit` capability row and attributes tsukuroi `tools/check-boot-writers.py` | **COMPLEMENTS (adjacency)** | External confirmation that tsukuroi is the fleet's boot-writer/pin owner — no sibling claims the plane. |
| 10 | `kama-shokunin` | `.ufo/waves/round-18/build/advice/ConnectTsukuroi.md:28,50,74` | Kama *refuses* `mkinitcpio` / `limine-update` / `boot-chain-audit.sh --live` "to respect that gate", citing tsukuroi `SKILL.md:1921` | **COMPLEMENTS (ownership)** | Clean boundary: no sibling acts on the boot plane. |
| 11 | `kumitate-shokunin` | `.ufo/waves/round-71/receipts/census-after.txt:226` (path not present at exec; recorded from the earlier sweep) | Duplicate-URL census row `W04 S098 duplicate url …/limine-mkinitcpio-hook/…` | **COMPLEMENTS (weak)** | Same duplicate-URL class as tsukuroi's own r91 census note (`corpus/lessons/round-91.md`: 3 new W04 warnings from S374–S376 sharing URLs with the `before/src/` pins). |
| 12 | `kagi-shokunin` | `.ufo/waves/round-58/build/R58ConnectorSiblings/sweep-raw.txt:246-292`; `round-62/w1/R62Connector.md:71`; `round-63/build/R63Connector/sweep.md:48,119,202,246` | Kagi's connector registers tsukuroi's `corpus/knowledge/` + `PROVINCE.md` as an adjacency surface; `snapper-eacces-mechanism.md` cites the limine-snapper-sync README | **DUPLICATES (instrument-shaped)** | Confirms tsukuroi owns this plane in the fleet's adjacency registers. |

**Summary of §1:** 20/20 sibling lanes swept. **0 conflicts. 0 competing rule statements.** The
r91 rule set and the C2 topic are single-owner. The only substantive cross-lane overlap is the
objcopy/llvm-objcopy class of incident (§2) — a *hazard* overlap, not a *rule* overlap.

### Note on scope discipline (I did not claim more than the evidence supports)

The prescribed grep hits in `mori` and `tabi` are **kernel-doc and systemd-unit-name** matches. They
are not Limine pin/measured-boot/TPM knowledge. I checked for the specific r91 surfaces
(`hash_mismatch_panic`, `measured_boot`, `unverified_image_lines`, `config_get_value`,
`/sys/class/tpm`, `LoaderTpm2ActivePcrBanks`, `has-tpm2`, `SecureBoot`, `fslabel`, `hdd(`) across
**all** tracked files of all 20 siblings, and every hit was either a git/mako/llama.cpp "global
section" of an unrelated project, a wave-dir artefact, or one of rows 1–12 above. **No sibling holds
a Limine config-visibility or pin-grammar claim.**

## 2. The one cross-lane pattern (adjacency axis)

**Pattern: "a read-only-looking binary probe rewrites its own input."** Two lanes hit it
independently; one lane's finding propagated fleet-wide as a rule.

- **tsukuroi (owner).** `corpus/lessons/round-86.md:63-67` — seat `ScoutHost` ran
  `sudo objcopy --dump-section .cmdline=<out> /boot/EFI/Linux/<uki>` and **rewrote both UKIs in
  `/boot` in place**. Lane rule `R86-OBJCOPY-IS-A-WRITER`; knowledge row `LP7`
  (`corpus/knowledge/limine-pin-plane-r87.md:32`), sourced to the binutils manual
  (`corpus/SOURCES.md:365`, S354): *"If you do not specify outfile, objcopy creates a temporary file
  and destructively renames the result with the name of infile."*
- **kaidoku (independent second instance).** `corpus/lessons/round-30.md:45` (M30-2) — seat
  `RevOracleVsReadobj` ran `llvm-objcopy --dump-section <sec>=<out> <input>` **without an
  output-object argument** and rewrote 4 of 16 frozen carriers; the seat's own words: *"The 0444 mode
  did not protect (file rewrite, not write(2))"* (`.ufo/waves/round-30/w1/RevOracleVsReadobj.md:12-13`).
- **souji (the rule, fleet-wide).** `.ufo/waves/round-79/ctx-tail.txt:4` (rounds 79/80/81/82 all
  carry it) — tsukuroi's incident, re-stated as a fleet wave-context ban.
- **mado (the safe inventory).** `.ufo/waves/round-56/w3/R56W3MutBwrapChannels/receipts/jail-probe-bwrap.out:656,1584,1648,2180`
  — a **read-only** bwrap probe that already enumerates `/bin/objcopy`, `/bin/llvm-objcopy`,
  `/bin/limine-update`, `/bin/efibootmgr` as the host binaries to keep out of reach.

**Why this is the connector's pattern and not a repeat of a lane lesson:** the *knowledge* is
tsukuroi's (S354/LP7); the *pattern* is fleet-wide. The actionable consequence for **this** round
is negative and worth stating plainly, because it constrains what the r91 wave may do: **every byte
the r91 C2 entry asserts about the host came from a read-only receipt, and the r91 wave created no
new host write.** Nothing in the r91 wave re-ran the dangerous class of probe. The obligation the
pattern leaves for r91 is *coverage*, not knowledge: the r91 battery's own fixtures must not be
written in place by a probe, and no sibling lane offers an instrument that would catch it if they were.

**Non-obvious consequence the fleet has not yet drawn (adjacency, offered as a proposal, not
implemented):** kaidoku's M30-2 mitigation is `chattr +i` on the frozen carriers plus an
"always pass an explicit output object" driver change (`RevOracleVsReadobj.md`, *"Driver now always
passes an explicit output object"*). **The tsukuroi lane has no `chattr`/`lsattr`/immutable practice
at all** — `git grep -n "chattr" -- tools corpus SKILL.md` returns only unrelated btrfs/journal
mentions (no hit in `tools/`). The lane's protection is a *rule* (QUALITY 124
`R87-BOOT-NO-INPLACE-WRITER`, `corpus/QUALITY.md:285`) plus a digest receipt, not an *attribute*.
That is a real, currently-unexercised difference between the two lanes on the same hazard class. It
is a proposal for a future round, not for this one: round 91's frozen battery and controls are
byte-pinned by `freeze-manifest.sha256`, so an immutability attribute on them would interact with
the freeze. **Not proposed for r91.**

## 3. Operability: the lane's own gates FAIL on the landed r91 C2 entry (operability axis)

**This is the substantive operability finding, and it is in-lane (not sibling) — the lane's own
instruments, run read-only at the lane's own revisions, contradict the landed r91 state.**

| Gate | at freeze `d3b0987d` | at `45ae6518` (C2 landed) | at tip `2d7e09e1` |
|---|---|---|---|
| `tools/check-knowledge-header.py` | **PASS** findings=0, clean=106 | **FAIL** findings=3 | **FAIL** findings=3 |
| `tools/check-recheck-commands.py` | FAIL flagged=3, files=106 | **CANNOT_EVALUATE** files=0 | **CANNOT_EVALUATE** files=0 |

Verbatim (receipt `receipts/gate-conformance.txt`):

```
== A. check-knowledge-header.py across the r91 commit chain ==
-- d3b0987d68364ccf8b781a755cbcd9563f939468 --
   status=PASS findings=0 clean=106 complete=106 notes=106
-- 45ae6518 --
   status=FAIL findings=3 clean=106 complete=106 notes=107
    KNOWLEDGE-HEADER-MISSING corpus/knowledge/limine-unverified-image-r91.md | recheck: no line starts with recheck: (outside fenced blocks)
    KNOWLEDGE-HEADER-MISSING corpus/knowledge/limine-unverified-image-r91.md | source: no line starts with source: (outside fenced blocks)
    KNOWLEDGE-HEADER-MISSING corpus/knowledge/limine-unverified-image-r91.md | verified-at: no line starts with verified-at: (outside fenced blocks)
-- 3d645e2c --
   status=FAIL findings=3 ... (same three)
-- 2d7e09e101996cc1ac5836c6d635f3f608453ac5 --
   status=FAIL findings=3 ... (same three)

== B. check-recheck-commands.py across the same chain ==
-- d3b0987d68364ccf8b781a755cbcd9563f939468 --
   status=FAIL flagged=3 files=106
    RECHECK-FORBIDDEN-INVOCATION corpus/knowledge/journald-retention-plane-r76.md:5 | recheck procedure invokes pacman
    RECHECK-FORBIDDEN-INVOCATION corpus/knowledge/kernel-taint-plane-r69.md:3 | recheck procedure invokes pacman
    RECHECK-FORBIDDEN-INVOCATION corpus/knowledge/mkinitcpio42-onrelease-r64.md:3 | recheck procedure invokes pacman
-- 45ae6518 --
   status=CANNOT_EVALUATE flagged=0 files=0
    E-RECHECK-MISSING corpus/knowledge/limine-unverified-image-r91.md | no recheck: line
-- 2d7e09e101996cc1ac5836c6d635f3f608453ac5 --
   status=CANNOT_EVALUATE flagged=0 files=0
    E-RECHECK-MISSING corpus/knowledge/limine-unverified-image-r91.md | no recheck: line
```

**Defect D1 — `corpus/knowledge/limine-unverified-image-r91.md` has no QUALITY-8 header block.**
`corpus/QUALITY.md:12` requires every knowledge entry to carry `source:`, `verified-at:` and
`recheck:`. The r91 entry has **none of the three** (it starts `# Limine v12.9.4 — unverified image
lines…` then a prose paragraph naming S374–S376, but with no `source:` line at column 0). Its three
sibling Limine entries all have them at lines 3–5:
`limine-pin-plane-r87.md:3-5`, `limine-uri-failure-r89.md:3-5`, `limine-tpm-volume-r90.md:3-5`.
Two consequences, both operator-visible:
- `check-knowledge-header.py` reports FAIL at the tip — the lane's standing knowledge-header gate is
  red on its own landed artifact.
- `check-recheck-commands.py` degrades from FAIL to **CANNOT_EVALUATE with `files=0`** — it
  aborts before evaluating *any* file, so the three pre-existing `pacman`-invocation findings it was
  reporting at the freeze are now **invisible** (the gate's `E-RECHECK-MISSING` short-circuits at
  `tools/check-recheck-commands.py:660`). An operator running the recheck gate at the tip gets
  "could not evaluate", not the three real findings it would otherwise print. That is a
  **silently weakened instrument**, which is the worst failure mode for a gate.

**Defect D2 — `check-knowledge-refs-r68.py` cannot resolve the r91 note's sources.**
The same missing `source:` line means the refs gate sees `source_line: null, refs: []` for the r91
note at the tip:

```
-- tip 2d7e09e1 --
   PASS dangling 0 refs 336 sourced 106
   r91 note -> {'dangling': [], 'path': 'corpus/knowledge/limine-unverified-image-r91.md', 'refs': [], 'source_line': None}
```

The gate reads only the column-0 `source:` line, so **S374/S375/S376 are never checked for
danglingness** for the r91 note. I confirmed the blindness is real, not cosmetic: injecting a bogus
`S999` into the r91 note's *body* at the tip leaves the gate **PASS** (`dangling 0`, `refs []`,
`source_line None` — the bogus id is never looked at). The same bogus id in a `source:` line after my
proposed patch makes the gate **FAIL** (`KNOWLEDGE-REF-DANGLING`, `source: line 3 cites S999,
absent from corpus/SOURCES.md at the revision`). The r91 entry is the only one of 107 notes with an
unresolved source line.

**Why the wave did not catch it:** `ExecLints` (§2 of `.ufo/waves/round-91/w1/ExecLints.md`) ran
`check-knowledge-header.py` at `ce89df93` and at the freeze `d3b0987d` — both **before** the C2 entry
landed in `45ae6518` — and reported PASS for both. It ran `check-registry-coverage.py` at the tip
(`3d645e2c`, PASS) but has **no tip run** of the header gate or the recheck gate. The C2 entry
therefore entered the lane with no gate ever run against it. The lint seat's own scope note says the
lane tip was checked "in addition to" the named revisions; for these two gates it was not.

### Defect D3 (same file, different kind): the C2 entry's `uri_resolve` claim is falsified by the pinned bytes

The C2 entry's "What the gate should report" section, `corpus/knowledge/limine-unverified-image-r91.md:14-17`:

> `uri_resolve` (uri.c 32-107) returns `false` with **no `URI_ERROR` message** for a
> value with no `(`, no `):/`, or no `#` after `):/` — the "silent no-shape fail"
> (uri.c 46-70, 77-106).

and the same claim in the machine-readable companion,
`corpus/knowledge/limine-unverified-image-r91.json` → `findings[0]`:

> `uri_resolve returns false with no URI_ERROR for values with no '(', no '):/', or no '#' after '):/' (uri.c 46-70, 77-106)`

**The "no `#` after `):/`" disjunct is false.** I extracted `uri_resolve` verbatim from the pinned
snapshot (`.ufo/waves/round-91/before/src/limine-v12.9.4-common_lib_uri.c`, raw lines 32–107) and
compiled it with a `URI_ERROR` counter (no host write, no sudo; full harness in
`receipts/c2-uri-falsifier.txt`):

```
shaped, no '#' (host line 72 shape)        -> ret=true  hash=NULL   uri_errors=0
    URI_ERROR: Blake2b hash must be 128 characters long
shaped, short hash                         -> ret=false hash=SET    uri_errors=1
no '(' at all                              -> ret=false hash=NULL   uri_errors=0
'(' but no '):/'                           -> ret=false hash=NULL   uri_errors=0
empty path 'boot():/'                      -> ret=false hash=NULL   uri_errors=0
shaped, 128-hex hash                       -> ret=true  hash=SET    uri_errors=0
```

A value with no `#` returns **true** with `*hash == NULL` and **zero** `URI_ERROR`s: the hash loop
(`uri.c` raw 78–104) simply finds no `#`, falls out of the loop, and hits `return true` at raw 106.
The "silent no-shape fail" class is exactly **two** shapes (no `(`, no `):/`), plus the empty-path
case at raw 73–74 — **not** the no-`#` case.

The entry is **internally inconsistent**: §"The unhashed-but-shaped case (host line 72)"
(lines 19–28) states the opposite and correctly — *"`hash == NULL` — is **not** a resolve failure:
`uri_resolve` returns true with `*hash == NULL` (uri.c 77-106 falls through `return true`)"* — and
`findings[2]` in the JSON says it too. So the md's first section and its own second section
contradict each other, and the JSON's `findings[0]` carries the wrong one.

**Why it matters (this is not cosmetic wording).** `findings[0]` is the machine-readable statement of
*why* the gate reports an unverified image line. A reader who takes it literally concludes that the
host's line 72 (`path: boot():/EFI/BOOT/BOOTX64.EFI`, no `#`) makes Limine **panic** ("efi: Failed
to open image"). The pinned bytes say the opposite: line 72 is URI-shaped, `uri_resolve` succeeds,
`uri_open` succeeds, and the image **boots unverified** (the entry's own lines 21–28). The C2 entry's
*headline* claim — host line 72 is a live instance of the class the gate must report — is **correct**;
the *mechanism* sentence attached to it is wrong, and it is wrong in the direction that predicts a
panic where the host actually boots.

**Verification of the falsifier's independence:** the harness compiles the function extracted from the
pinned snapshot, not from any lane copy. The pinned file's own sha256 is
`e06cac1212fec55150c109843e22fde01cd618d4e812ef538b23a8a2ed6f`… (matching
`.ufo/waves/round-91/before/freeze-manifest.sha256` row for
`limine-v12.9.4-common_lib_uri.c`).

**Note on D3's relationship to the frozen C1 predicate:** D3 is a defect in the **C2 entry's prose and
its JSON companion**. It does **not** touch the frozen battery, the frozen gate, the 12 controls, the
declaration, or the freeze manifest. The battery's U1 rule is *unaffected* — U1 reports an image line
whose value "is not a parseable `[$]resource(root):/path#hash` pin", which correctly includes the
no-`#` value regardless of what `uri_resolve` returns. So D3 harms C2's accuracy, not C1's count.

### Proposed patch (L1 decides; NOT landed by me)

`ConnectorOverlap/proposed-r91-c2-entry-repair.diff` — touches **only**
`corpus/knowledge/limine-unverified-image-r91.md` (10 insertions, 3 deletions) and its `.json`
companion (1 line). Verified in a `git clone --shared` fixture
(`/fast/scratch/.../ConnectorOverlap/lane3`, fixture commits only, `git diff --stat`:
`2 files changed, 10 insertions(+), 3 deletions(-)`):

```
== check-knowledge-header.py ==   status PASS  findings 0  clean 107  notes 107
== check-knowledge-refs-r68.py == status PASS  findings 0  dangling 0  refs 339  sourced 107
   (r91 note now binds source_line -> refs ['S374','S375','S376'], dangling [])
== check-recheck-commands.py ==  status FAIL  flagged 3  files 107   (the same three
   PRE-EXISTING pacman findings that were visible at the freeze — restored, not new)
== git diff --name-only == corpus/knowledge/limine-unverified-image-r91.{md,json}   (tools/ untouched)
```

The recheck gate's 3 remaining findings are the **pre-existing** `pacman`-invocation findings that
were already reported at the freeze commit and are **not** caused by this patch — the patch restores
the gate from `CANNOT_EVALUATE files=0` back to reporting them.

## 4. Freshness: the host-build patch-offset leg, measured (freshness axis)

`corpus/README.md:844` lists as still open: *"Patch-offset host-build check (considerthese/2026-10-26.md
#22, partial): needs a host-build measurement outside the frozen legs."* The r91 C2 entry cites upstream
raw line numbers (`uri.c 46-63`, `chainload.c 414-435`, `config.c 642-650`) for claims about **host
behaviour**, and its r90 sibling carries the QUALITY-103 caveat verbatim
(`corpus/knowledge/limine-tpm-volume-r90.md:24-25`): *"raw line numbers refer to those files (upstream
tags; the host runs the Arch builds `limine 12.9.4-1` and `systemd 262.1-1`, whose line numbers were
not checked: QUALITY 103)"*. The r91 entry carries **no such caveat** (`grep -c "QUALITY 103"` = 0 for
the r91 file, 1 for the r90 file). So I measured the leg, read-only, on the host:

1. `pacman -Q limine` → `limine 12.9.4-1`; `/var/lib/pacman/local/limine-12.9.4-1/desc` → packager
   Robin Candau, builddate `1792481650` (= 2026-10-20T04:34:10-03:00).
2. The installed package's **own** `.BUILDINFO` records
   `pkgbuild_sha256sum = 1fd1cc4265b91ed6efb17b8c8423152533cc76b010b4037b809c259a36840926`.
3. The Arch packaging commit that produced 12.9.4-1 is `9883569bd4255fc19cd093b5776546a676a66a6a`
   ("upgpkg: 12.9.4-1: New upstream release", 2026-10-20T09:35:02+02:00). Fetching its `PKGBUILD`
   and hashing it gives **the same digest**
   `1fd1cc4265b91ed6efb17b8c8423152533cc76b010b4037b809c259a36840926`. The host's build recipe is
   therefore *exactly* the upstream Arch recipe, unmodified.
4. That `PKGBUILD` **has no `patch`/`sed` on any source file**: `prepare()` runs `./bootstrap` only,
   `build()` runs `./configure --prefix=/usr --enable-all; make`.
5. Upstream's `bootstrap` (v12.9.4) writes into `common/`: `freestanding-lgrt.s2.c`,
   `compress/pdgzip.c`, `compress/pdgzip.h`, `lib/stb_image.h` (+ `stb_image.patch` on that one
   header). **None of `uri.c`, `chainload.c`, `config.c`, `menu.c` or `panic.s2.c` is copied, patched
   or rewritten.**
6. Independent cross-check: the installed `/usr/share/doc/limine/CONFIG.md` is **byte-identical** to
   upstream v12.9.4 `CONFIG.md`
   (`c9e8b670d20d839add4f651f8c49e9565302b132f9f86269acbc7cd1e0358923` both sides).

**Reading (for the L1, not a claim I score):** for the three files the r91 C2 entry cites
(`uri.c`, `chainload.c`, `config.c`), the *upstream* raw line anchors coincide with the host build's
sources, because the host build applies no source patch and the bootstrap touches none of them. That
supports the C2 entry's `uri.c`/`chainload.c`/`config.c` line anchors as read against the host, and it
is a **narrowing** of the r90 caveat, not a claim about the `systemd 262.1-1` half (which remains
unchecked, and which the r91 C2 entry does not cite). Full receipt:
`receipts/host-build-probe.txt`.

**Host facts I did not have and did not fabricate:** the r91 host receipt
(`.ufo/waves/round-91/before/host/receipt.txt`) is the lane's committed read-only capture; I did not
run any host probe of my own. `/boot/limine.conf` is unreadable without root (`ls: cannot open file
'/boot/limine.conf': Permission denied`) and I did not escalate — no `sudo`, no `objcopy`, no
`/boot` write. The `52b6cc83…` /boot digest list in the receipt is a sha256 **over** the sha256sum
output, so it cannot be compared to a per-file digest I could obtain read-only; I did not attempt it.

## 5. `considerthese/` — the one proposal still unimplemented that fits this round

Latest file: `considerthese/2026-10-26.md` (operator-authored; read only, never edited). Its five
"self-improvement ideas (proposed only, not acted on)". Four are already mined in-lane
(`Burst-aware reading` → `corpus/lessons/round-46.md:97`, QUALITY 112; `Counter-attack scoreboard` →
`corpus/lessons/round-52.md`, adopted round 64; `Seat-harm incident log` → `corpus/lessons/round-45.md:124`,
QUALITY 110; `Cross-note correction propagation map` → QUALITY 108).

**The one still unimplemented is "Downstream patch-offset check"** — quoted verbatim:

> **Downstream patch-offset check.** Round 40 found an Arch patch shifts util.c lines after :675 by +5.
> I could flag any knowledge anchor that cites upstream line numbers for code the host runs as a patched
> Arch build, so line pins don't silently drift.

Evidence it is still unimplemented (not merely unimplemented-in-name):
- `corpus/README.md:844` — *"Patch-offset host-build check (considerthese/2026-10-26.md #22, partial):
  needs a host-build measurement outside the frozen legs."* — i.e. the lane's own README lists it as
  **partial, still owed**.
- `corpus/QUALITY.md:201` (row 103, `R69-PATCH-OFFSET`) states the rule; the rule is adopted, the
  **host-build measurement leg is not done**.
- Adoption is visible only in the notes that *happen* to cite host-built code and remembered to
  add the caveat: `limine-tpm-volume-r90.md:25`, `systemd-dependency-propagation-r79.md:24`,
  `systemd-unit-fragment-plane-r74.md:71`, `hibernate-resume-plane-r84.md:20`,
  `mount-unit-fstab-plane-r81.md:106`, `systemd-job-transaction-plane-r75.md:82`. The r91 C2 entry
  cites the same class of upstream line numbers for host behaviour and **does not carry it**
  (`grep -c "QUALITY 103"` → 0). So the flagging is **advisory and manual**, not enforced: a new entry
  can omit it silently, and this round's entry did.

**Why it fits this round (and fits it exactly):** the r91 C2 entry is a host-behaviour entry built on
upstream raw line anchors (`uri.c 46-63`, `chainload.c 414-435`, `config.c 642-650`), it is the entry
the round's depth claim rests on, and the lane's own README already names the missing leg as a
"host-build measurement". §4 supplies that measurement for the three cited files, so the caveat can
be replaced by a **narrower, measured** statement instead of the blanket "not checked".

**What landing it would take** (a proposal, not implemented by me):
1. Add the QUALITY-103 sentence to the r91 C2 entry, scoped to the files it actually cites
   (`uri.c`/`chainload.c`/`config.c`: line anchors coincide with the host build per §4; `systemd 262.1-1`
   still unchecked and **not** cited by this entry).
2. Turn the flag from advisory to enforced where it is cheap: a `check-knowledge-header.py`-style rule
   (or a sibling of it) that flags any `corpus/knowledge/*.md` row citing `common/lib/*.c` raw lines
   **without** either the QUALITY-103 sentence or a host-build measurement reference. The r91 entry
   would fail that rule, which is the point.
3. Record the §4 measurement as a lane receipt (`.ufo/waves/round-91/after/host-build-offset.txt` or
   the next round's `before/host/`) plus a `SOURCES.md` row for the Arch packaging commit
   `9883569b…` and the upstream `bootstrap` script — so the anchor is source-backed rather than a
   one-off probe. (`corpus/SOURCES.md` currently has no row for either; the r91 `S374-S376` rows cover
   only the Limine tag files.)
4. Close `corpus/README.md:844` when (2) lands.

**Why not implement it here:** the r91 freeze manifest does not cover `corpus/knowledge/`, but the
round's declaration freezes the C2 entry's *content* as the depth claim's subject; editing the entry's
substance inside the scoring wave is the L1's call, and the C2 judgement (named non-author
`unprovable-but-better`) is not mine to make. §3's patch touches only *header metadata* plus one
falsified sentence (D3) — it does not change what the entry claims about the host — and the caveat in
item (1) is a separate, additive edit I have deliberately left for the L1.

## 6. Proposed move, risks, verification (UFO-FSD connector summary)

**Proposed move (one move):** land `ConnectorOverlap/proposed-r91-c2-entry-repair.diff` — restore the
QUALITY-8 header block on the r91 C2 entry (which re-enables two lane gates and re-binds S374–S376 to
the refs gate), and correct the falsified `uri_resolve` silent-fail sentence in the md and in
`findings[0]` of the JSON companion.

**Affected axes:** operability ↑ (header gate FAIL→PASS; recheck gate CANNOT_EVALUATE(files=0)→FAIL
reporting its 3 pre-existing findings again; refs gate binds S374–S376 and now catches a dangling id);
depth/accuracy of C2 ↑ (the mechanism sentence no longer predicts a panic where the host boots).
**Not affected:** C1's count, the frozen battery, the 12 controls, the declaration, the freeze
manifest, `tools/` — all untouched by the patch (verified by `git diff --name-only`).

**Risks, stated honestly:**
- The patch **changes the C2 entry's text**. C2's judgement is a named non-author
  `unprovable-but-better` closure; the L1 owns whether a corrected entry changes that judgement. My
  patch makes the entry *more* accurate, not less — but that is the L1's call, not mine.
- `verified-at: 2026-11-08` and the `recheck:` wording are **my** choices; a different L1 phrasing
  changes nothing observable (both gates accept any ISO date and any `on-release`/`30d` cadence).
- The `recheck:` line I propose mentions re-running "the read-only host receipt commands". The
  recheck gate's forbidden list is `pacman, checkupdates, yay, paru, mkinitcpio, limine-update`; my
  line names none of them (verified: the gate's only 3 findings are the pre-existing `pacman` ones in
  other notes).
- The **3 pre-existing** `pacman` findings in `journald-retention-plane-r76.md`, `kernel-taint-plane-r69.md`
  and `mkinitcpio42-onrelease-r64.md` are **out of scope for r91** and remain FAIL either way; my patch
  merely makes them visible again. I did not touch them.
- The §4 patch-offset reading is scoped to three files and to the *build recipe*; it is not a claim
  about the running `/boot` bytes, and the entry's `systemd` half stays unchecked.

**Verification (all run by me, read-only, at named revisions):**
- sibling sweep — 20 repos, `receipts/sibling-scan-terms.txt`
- gate conformance across the r91 commit chain — `receipts/gate-conformance.txt`
- compiled falsifier of `uri_resolve` from the pinned bytes — `receipts/c2-uri-falsifier.txt`
- host-build patch-offset probe — `receipts/host-build-probe.txt`
- proposed patch applied in a `git clone --shared` fixture, three gates re-run — §3 table + diff stat

**What I did NOT do (refused / out of scope):** no `sudo`; no `objcopy`/`strip`/`sbsign`/`ukify`/
`patchelf`/`mkinitcpio`/`limine`/`limine-update`/`snapper`/`bootctl`/`efibootmgr`/`pacman` transaction;
no write to `/boot`, `/efi`, `/etc`, `/usr`, `/var`, `/sys`, `/proc`; no sysctl change; no lane file
edited; no commit in the lane; no `agent://all` broadcast; no subagent dispatched; no model chosen.
`/boot/limine.conf` was unreadable without root and I left it that way.
