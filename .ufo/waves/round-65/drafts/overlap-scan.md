# Round-65 sibling overlap scan (C1SiblingScan, connector)

Scope: read-only scan of sibling lane repos for any claim on round 65's new ground —
C1 the systemd v262 NvPCR/UKI requirement plane measured against this host's boot chain,
C2 the initramfs census arm. **Reported, never absorbed.** No sibling repo was written;
every command below is a read (`git -C <repo> …`, `grep`, `sed`, `git clone --shared`
into a private scratch tree).

Ground vocabulary searched (three families):

| family | terms |
|---|---|
| UKI-family (C1 subject) | `nvpcr`, `ukify`, `systemd-stub`, `sign-initrd-pcrs`, `unified kernel image`, `\bUKI\b`, `tpm2-setup`, `PCR policy` |
| initramfs-family (C2 subject) | `initramfs`, `mkinitcpio` |
| host boot-chain reads | `/EFI/Linux`, `omarchy_linux.efi`, `/boot/EFI`, `/boot/vmlinuz`, `systemd-stub` |

## 1. Per-sibling table

`sibling HEAD` = the commit read. `UKI` = UKI-family hit count. `INIT` = initramfs-family
hit count. Both counts are over **tracked** content at that sibling's HEAD, excluding each
sibling's own `.ufo/` wave directories (their per-round scratch, not lane scope) —
`git -C <repo> grep -niE '<terms>' HEAD -- '*.md' '*.json' '*.py' '*.sh' ':(exclude).ufo/*'`.

| sibling | HEAD | UKI | INIT | what the hits are | verdict on this round's ground |
|---|---|---|---|---|---|
| mori | `84c6cbc3` | 0 | 0 | — (see §3 for the one relevant line) | **LANE-GAP** (nothing here claims it) |
| kama | `6035e952` | 0 | 0 | — | **LANE-GAP** |
| kaidoku | `c7fe6898` | 0 | 0 | — (`:125` names tsukuroi's update-safety gate) | **LANE-GAP** for UKI; kaidoku keeps RE of shipped artifacts |
| revenger | `5915ad8d` | 0 | 0 | — (`:4` owns RE incl. `firmware`; S252 UEFITool = firmware-image parsing) | **LANE-GAP** |
| tameshi | `f20ba482` | 0 | 0 | — (`:32` names tsukuroi's census as a read-only primary surface) | **LANE-GAP** on the UKI subject; tameshi is the method owner |
| kumitate | `3c369336` | 0 | 0 | — | **LANE-GAP** |
| kengaku | `b5032ff8` | 0 | 0 | — | **LANE-GAP** |
| kasegi | `cd302987` | 0 | 0 | — (`:169` owns the *kernel security-bug reporting process*, upstream docs) | **LANE-GAP** |
| kake | `d76ae926` | 0 | 0 | — | **LANE-GAP** |
| **kotoba** | `1c8f37ed` | 0 | **13** | all 13 are kotoba **ceding** host package/initramfs hooks to tsukuroi | **AGREES** (see §2) |
| kotodama | `c285b2af` | 0 | 0 | — (its 17 `uki ` hits are Japanese-language false positives: `uki ` inside `Kuki`, `Kabuki`, `Tsurayuki`) | **LANE-GAP** |
| chousa | `f748abbb` | 0 | 0 | — | **LANE-GAP** |
| tabi | `484bde50` | 0 | 0 | — | **LANE-GAP** |
| **souji** | `fd854c7c` | **1** | 4 | 1 UKI hit = a *captured copy of tsukuroi's own SKILL.md row* inside souji's r43 census scan receipt (`census/round-43/waves/w1/R43connector01/scan-receipts.json:25`, quoting `master:SKILL.md:48`); the 4 INIT hits = historical census fixtures (`/usr/local/bin contains only mkinitcpio`) and more captured lane SKILL rows | **LANE-GAP** (capture artifact, not a claim) |
| **mado** | `524fa1f9` | 0 | 3 | `tools/mado-tripwire.py:264` lists `mkinitcpio`,`bootctl` as **host-mutation** binaries mado refuses to let an agent run; two `corpus/lessons/round-17*` rows recount the 2026-10-20 `-Syu` that took mkinitcpio 41.1→42.2 | **AGREES** (mado classifies these as tsukuroi/OS surfaces) |
| kagi | `91f7752b` | 0 | 0 | — | **LANE-GAP** |

HOLD lanes, read for `PROVINCE.md` only as instructed: **mado** `PROVINCE.md` present, 0 hits
for both families (`mado` names tsukuroi as owner of package/service state at `:24`,`:35`);
**kagi** `PROVINCE.md` present, 0 hits (`:90` names tsukuroi only as tracker of the
1Password *packages*). Neither mado nor kagi claims any boot-chain or initramfs ground.

Host boot-chain reads by any sibling: **0** for every sibling on
`/EFI/Linux|omarchy_linux.efi|/boot/EFI|/boot/vmlinuz|systemd-stub`, except two `.ufo/`
wave artifacts that are *not* host reads — `kama/.ufo/waves/round-26/w1-build/out/ConnectorSiblingOverlap/overlap.md:95`
quotes an error string `Failed to read "/boot/EFI/systemd"` as tool output, and
`kaidoku/.ufo/waves/round-39/w1/artifacts/…/build-dev-carriers.sh:28` writes a synthetic
`kernel=/boot/vmlinuz` into a *fixture* loader.cfg. **No sibling has ever read this host's
boot chain.**

## 2. The two hits that are genuine cross-lane statements

**kotoba — AGREES (owner: tsukuroi).** kotoba is the only sibling that names this round's
C2 subject, and it *cedes* it:

- `kotoba-shokunin/PROVINCE.md:78` — adjacency row, class `adjacent`, pinned to
  tsukuroi commit `8bd001f58bfda29c92d90d2a7a413825c0ca9fcb`:
  *"tsukuroi owns host package and initramfs hooks and OS state as read-only probes
  (PROVINCE.md:22); kotoba routes only client hook-config files and cedes host hooks
  (hook-files-round59.md:20), a split stated on kotoba's side alone."*
- `kotoba-shokunin/SKILL.md:14-15` — *"tsukuroi owns host package and initramfs hooks."*
- `kotoba-shokunin/SKILL.md:127` — *"host package/initramfs hooks are tsukuroi's."*
- `kotoba-shokunin/corpus/knowledge/hook-files-round59.md:20` — *"Host package and
  initramfs hooks are tsukuroi's."*
- `kotoba-shokunin/corpus/knowledge/sibling-overlap-census-round74.md:33,35,42` — records
  that the `none → adjacent` class change happened on kotoba's side; `:103` tabulates it.
- `kotoba-shokunin/corpus/lessons/round-74-verifier-spotcheck.md:83-84` — re-verifies the
  two quotes verbatim and notes *"tsukuroi's own `PROVINCE.md:22` owns mkinitcpio"*.

The lane side of that statement resolves: `tsukuroi-shokunin/PROVINCE.md:22` at HEAD
`37c74e27` is the row `| Initramfs v42 and boot recovery | Inspect effective mkinitcpio
drop-ins, hooks and recovery stages; never rebuild or boot. |` — and the same text stood
at the pin `8bd001f58bfd` that kotoba quotes. So kotoba's inbound pointer is
**INBOUND-RESOLVES**, and its ownership direction agrees with the round's C2 claim:
C2 instruments a surface a sibling already attributes to tsukuroi.

**mado — AGREES (owner: tsukuroi).** `mado-shokunin/tools/mado-tripwire.py:264` puts
`mkinitcpio` and `bootctl` in `HOST_MUTATION_BINS` — mado's own tripwire refuses to let an
agent run them — which is the same direction the round's C2 arm takes (no mkinitcpio, no
ukify, no bootctl call; the arm's contract at `tools/tsukuroi-census.sh:439-441` states
"No mkinitcpio, dracut, ukify or bootctl call, no privilege, no network, no write").

## 3. The sibling line that is adjacent but does not claim the ground

`mori-shokunin/PROVINCE.md:13` — *"systemd unit, driver/firmware and boot state
(→ tsukuroi) — mori reads journal and cgroup events as fleet evidence and reports them,
never owning OS state"*, plus mori's adjacency row `:66` — *"Owns host OS, package,
systemd-unit, driver, firmware, and boot diagnosis"*, whose ownership source is
`../tsukuroi-shokunin/PROVINCE.md:8-14`. So mori already **routes boot-chain state to
tsukuroi**. That is the same ground C1 measures, agreed in advance.

One drift to note (pre-existing, not caused by this round): mori's current pointer text at
`PROVINCE.md:66` is `../tsukuroi-shokunin/PROVINCE.md:8-14`, while the lane's own inbound
register row **IN-067** still records the older pointer `../tsukuroi-shokunin/PROVINCE.md:21-24,35-44`
with `found_line 8`, class `DRIFTED`, note *"the ownership text predates the pointer, so this
is a mis-citation, not movement"*. mori re-pinned that pointer in `af42101d` (round 30).
The lane's register therefore still carries a pointer mori no longer publishes. This is a
lane-side register staleness to report, not a conflict over the round's ground.

## 4. Governing ADJ rows and why none of this round's ground is RE

The round's own ground is **boot-chain STATE**, not artifact internals:

- C1 measures *what the requirement demands* and *what this host has*: the v262 TPM-subsystem
  requirement text (S282), `bootctl` firmware fields, `pacman -Qo` ownership, the
  `/etc/mkinitcpio.conf.d` drop-ins, the hook inventory, `ukify` presence. The draft note's
  own boundary line says it *"names no binary internals — UKI content analysis and any
  RE-class question stay with ADJ-06"*, and SY5 leaves *"whether the current UKIs embed the
  four `.nvpcr` defs (needs a UKI content read)"* as an **unknown**, explicitly out of scope.
- C2 instruments the **initramfs surface the lane already owns** (`PROVINCE.md:22`): four
  fixed paths stat'd or listed (never opened), a `grep -F` over readable hook files for the
  literal `/new_root`, and one `command -v` lookup of `ukify`.

Therefore:

| ADJ row | governs? | why |
|---|---|---|
| **ADJ-06** (kaidoku/revenger, shipped-artifact RE) | **not triggered by the landed claims; named as the boundary** | kaidoku owns RE of shipped artifacts (`PROVINCE.md:3`) and revenger owns it including `firmware` (`PROVINCE.md:4`, S252 UEFITool). Neither has read this host's boot chain (0 hits, §1). C1 reads no UKI bytes and C2 reads no artifact bytes, so no RE-class question is raised. The one place the round approaches RE is SY5's UKI-content read — held as an unknown, and the draft note already routes any such read to ADJ-06 / the protocol integrator. The boundary is respected, not crossed. |
| **ADJ-07** (tameshi, reusable verification/mutation method) | **not triggered; one method question is open** | tameshi owns the *method* (`PROVINCE.md:14-16`), each lane keeps its own gate (`tsukuroi PROVINCE.md:52`: "Census bug, domain contract, implementation and repair in this repo"). C2's arm and its selftest cases stay in-repo. tameshi names tsukuroi's census as a read-only primary surface (`tameshi PROVINCE.md:32`), so the *method* surface touches the file C2 edits — but no method question is raised by C2 as scoped. See §6 for the one item that may need tameshi's method eye. |
| **ADJ-04** (mori, pressure/kill attribution) | **not triggered** | The round's note explicitly keeps pressure attribution with mori ("pressure attribution stays mori's (ADJ-04)"). Nothing in C1 or C2 measures pressure or kill events; the C2 arm's selftest case *deliberately* holds one plane DEGRADED in both arms to prove the arm is not rollup input. |
| **ADJ-02** (kagi, credential helpers) | **not triggered** | The C2 arm stats `/etc/mkinitcpio.conf` and never opens it; the census header states the path *"is never opened (ADJ-02)"* (`tools/tsukuroi-census.sh:417-420`). No secret is read. |
| ADJ-01 / ADJ-03 / ADJ-05 | **not triggered** | No endpoint, desktop or dispatch question is in scope. |

## 5. Non-obvious move — re-pin the lane's own IN-109 anchor in the same commit as the C2 arm

**Move (one, bounded, lane-internal, no sibling write):** when the C2 census edit lands,
land **one** companion change in `corpus/knowledge/adjacency-anchors-r19.json`: update
**IN-109**'s `found_line` from `2683` to the D14/D15 check's new line, and update the
matching published cell in `corpus/knowledge/adjacency-anchors-r19.md:204`.

**Evidence (measured, on a private `git clone --shared` of the lane at `37c74e27`; the lane
repo itself was never written):**

1. At lane HEAD `37c74e27` the gate is green:
   `python3 tools/check-adjacency-anchors.py --revision 37c74e27…` →
   `{"status": "PASS", "inbound_total": 114, "inbound_classified": 114, "inbound_by_class":
   {"RESOLVES": 96, "DRIFTED": 17, "UNRESOLVABLE": 1}, "outbound_portable": 10}`,
   `findings: []`.
2. Applying **only** the C2 census file (the round-65 worktree `tools/tsukuroi-census.sh`,
   sha256 `fe15cc5d…`, +245 lines) onto that HEAD and committing it turns the gate **red**:
   `INBOUND-CLASSIFICATION-WRONG` at
   `corpus/knowledge/adjacency-anchors-r19.json:inbound[108]` — *"classification DRIFTED is
   inconsistent: found_line is not an occurrence of evidence_quote"* — because the C2 arm
   shifts the D14/D15 selftest case (`check 'degraded: kernel ring class counts are
   evidence (D14/D15)' 1 DEGRADED`) from census line `2683` to `2822`.
3. Re-pinning that single `found_line` to `2822` restores the exact HEAD counts
   (`RESOLVES 96 / DRIFTED 17 / UNRESOLVABLE 1`, `inbound_total 114`, `outbound_portable 10`,
   `findings: []`) — no other row moves.

**Why this is the right non-obvious move.** IN-109 is the one lane register row whose
evidence quote lives *inside* the file C2 edits: tameshi's `corpus/knowledge/service-optin-protocol.md:153`
points at `tsukuroi-shokunin/tools/tsukuroi-census.sh:915-970`, and the lane records the
D14/D15 case's own line as the quote's occurrence. The register's own note already documents
this exact re-pin ritual ("Round 32: the census HANDOFF change moved the case from line 2216
to line 2277 (found_line updated…)"; same for rounds 38, 39, 42). C2 is the next census
insertion, so the ritual recurs — and the round-65 C2 predicate (`SCORECARD.md:4799`) names
only *"registry-coverage + knowledge-header gates PASS"*, **not** the adjacency-anchors
gate. Without the companion re-pin, a green C2 measurement would still leave a red
adjacency gate in the lane's own registry at the round's tip.

**Affected axis:** adjacency (the round's tied-lowest axis, 8) — it keeps the lane's
published cross-lane register truthful about a sibling pointer into the file the round
edits. **Harm:** none — the re-pin changes one integer in one JSON field plus one mirrored
table cell; it touches no counted value, no sibling repo, no claim predicate, and no
sibling-facing text. It also *helps* depth: the register's `IN-109` classification is what
proves the tameshi pointer still resolves after the edit.

**Risk (bounded, and stated):** the re-pin must be computed against the *landed* census
bytes, not against the current worktree bytes — the C2 arm is still being edited
(`tools/tsukuroi-census.sh` is modified in the lane worktree at the time of this scan), so
`2683 → 2822` is the value for the current worktree revision and will move again if the
arm's own lines shift. The correct recipe is: after landing the census edit, re-run
`grep -n "degraded: kernel ring class counts are evidence" tools/tsukuroi-census.sh` and
write the number it prints. The two `IN-109` mirrors to update together are
`corpus/knowledge/adjacency-anchors-r19.json` (`inbound[].found_line`) and
`corpus/knowledge/adjacency-anchors-r19.md:204` (the `Found line` cell, currently `2277` —
already stale against the JSON's `2683`, so the companion edit fixes both).

**Verification the L1 can run (all read-only):**

```
python3 tools/check-adjacency-anchors.py --revision <landed-census-commit>
# expect: status PASS, inbound_total 114, inbound_classified 114,
#         inbound_by_class {RESOLVES 96, DRIFTED 17, UNRESOLVABLE 1}, findings []
grep -n "degraded: kernel ring class counts are evidence" tools/tsukuroi-census.sh
# expect: the line number written into IN-109.found_line and into
#         corpus/knowledge/adjacency-anchors-r19.md:204
python3 tools/check-adjacency-overlap.py --revision <landed-census-commit>
# expect: status PASS, anchored_rows 6, sibling_check "sibling-verified" (measured PASS
#         on the C2-applied clone: {"anchored_rows": 6, "expected_rows": 6, "status": "PASS"})
```

## 6. Unfinished / open, for the record

- **Not finished:** the C2 arm's new selftest case `initramfs: the arm changed a line other
  than INITRAMFS, so it is rollup input (R65-C2)` is **intermittently failing**. Measured on
  the C2-applied clone: `TSUKUROI_CENSUS_SELFTEST: FAIL (177 cases, 176 passed, 1 failed)`
  on 3 of 3 fresh-TMPDIR runs in one batch, and `PASS (177 cases, 177 passed, 0 failed)` on
  3 of 3 runs in a different batch, and PASS again on later single runs with a reused
  TMPDIR. The neutral case compares two full census outputs line-for-line outside the
  INITRAMFS line; on the failing runs the differing lines were the **memory-plane** values
  (`PLANE drivers: … C5_pswp=37405521/… C6_avail_kb=20797628 …` vs `C5_pswp=37405522/…
  C6_avail_kb=20852120 …`) — i.e. live `/proc` drift between the two runs, not a
  property of the C2 arm. The arm's own `ENV_BASE` stubs `TSUKUROI_MEMINFO_FILE`,
  `TSUKUROI_PRESSURE_FILE` and `TSUKUROI_VMSTAT_FILE` to fixture paths
  (`tools/tsukuroi-census.sh:2500-2502`), so the fixture is not fully hermetic for those
  counters. **This belongs to the C2 executor seat, not to this seat** — reported, not
  absorbed. I did not attempt a fix.
- **Not finished:** the exact non-`INITRAMFS` differing line set on a failing run was not
  captured to a file. My instrumented clone (writing the two outputs to
  `TSUKUROI_DBG_DIR`) never fired because the failure did not reproduce in the four
  instrumented runs (all PASS). The diff above is from two identical fixture runs of my
  own harness, which reproduces the same class of difference; it is the best-supported
  account of the cause, not a per-case capture.
- **Not done (out of scope by instruction):** no sibling repo was modified; no `git add`/
  `commit`/checkout was run in any lane repo. The only commits made anywhere were inside
  private `git clone --shared` scratch trees under
  `/fast/scratch/hyaku/tsukuroi-r65/C1SiblingScan/`, used to measure gate behaviour, and
  they were removed with the scratch tree.

## 7. Receipts

Machine receipt: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-65/w1/C1SiblingScan-receipts.txt`
(sibling scan counts per HEAD, every non-zero hit with `file:line`, gate outputs before and
after the C2 edit, the IN-109 re-pin measurement, and the selftest observations).
