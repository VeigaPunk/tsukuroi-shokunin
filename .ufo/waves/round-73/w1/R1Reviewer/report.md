# R1Reviewer — adversarial entailment review of the six planned UL rows (r73 w1, tsukuroi)

Seat: R1Reviewer (L2 attack seat). Scope: the six planned rows UL1-UL6 in
`.ufo/waves/round-73/w1/L1Entry/note.md` (identical text to the self-test rows frozen in
`tools/count-ul-rows-r73.py`), judged against the pinned v262 snapshots in
`.ufo/waves/round-73/before/src/` — not token overlap. Sources re-opened at the pinned bytes;
host claims re-measured live; both frozen instruments re-run and attacked in scratch.

## Pins verified before judging

- `sha256sum -c SHA256SUMS` in `before/src/`: all three snapshots OK; digests equal the per-row
  `digest=` cells and `SOURCES.json` (eb9479be… xml, 47e98d39… unit.c, c11cd575… install.c).
- Instrument digests equal the declaration: counter `542f9c29…` ✓, checker `93f034e3…` ✓ (no edit made).
- `count-ul-rows-r73.py --selftest`: PASS (11 cases) under `TMPDIR=$S`. `check-r72-routed-r73.py --selftest`: PASS (5 cases).
- No tools installed (curl/python3/git only); no lane file outside my wave dir was written; no git/jj mutation anywhere.

## Instrument state observed (attack-seat re-runs)

| command | result |
|---|---|
| `python3 tools/count-ul-rows-r73.py --revision HEAD` (also at base eb105757, at declaration 74937132) | `UL_NOTE absent path=corpus/knowledge/systemd-unit-load-plane-r73.md`, rc=128 (cannot-evaluate; note not yet landed) |
| `python3 tools/check-r72-routed-r73.py --revision eb10575…` | `ROUTED_STALE=3 ROUTED_OK=0/3`, rc=1 — matches the declaration's base claim |
| `python3 tools/check-r72-routed-r73.py --revision HEAD` | `ROUTED_STALE=3 ROUTED_OK=0/3`, rc=1 — LESSON block-incomplete missing 2 tokens; DIGEST block-incomplete missing 1 token; CAPABILITY block-incomplete with 0 missing tokens (tokens present in file, not in one `## ` block) |
| registry wiring | `corpus/SOURCES.md` has **no** S304/S305/S306 rows at HEAD or in the working tree — when the note lands, the counter at that revision reports `source-unregistered` unless the registry rows are committed in the same revision |

## Per-row verdicts (statement vs. what the source says)

| row | verdict | source line | reason |
|---|---|---|---|
| UL1 | partly holds | systemd.unit.xml:366-378 | Override leg verbatim (368-370). "SYSTEMD_UNIT_PATH … replaces the whole path" is unconditional; the man adds the trailing-empty-component exception (376-378: "the usual unit load path will be appended"). |
| UL2 | partly holds | systemd.unit.xml:235-239 | Legs 1-2 verbatim (lexicographic 238-239; /etc > /run > /usr/lib 235-237). Leg 3 drops the scope qualifier: the man says "**Drop-in files under any of these directories** take precedence over unit files wherever located" (237-238); a drop-in not under the unit's drop-in directories does not apply at all. |
| UL3 | holds | unit.c:3884-3914, 4841-4848 | `!strv_equal(u->dropin_paths, dropins)` → reload (3905-3906); `fragment_mtime_newer(*path, u->dropin_mtime, false)` → reload (3910-3911); comment "… any drop-ins that are masked are simply omitted from the list." (3908, quote verbatim). Baseline is `u->dropin_mtime` recorded at drop-in load (4847), refreshed by every daemon-reload — precision note, not a contradiction. The row's "when A or B" is a sufficient condition and does not claim exhaustiveness (fragment/source legs at 3891-3898 also trigger). |
| UL4 | partly holds | unit.c:3859-3894 | The still-masked predicate is real: `path_masked` → `return !null_or_empty(&st)` (3874-3876, quote "For masked files check if they are still so" verbatim at 3875) fed by `u->load_state == UNIT_MASKED` (3892-3893). But (a) "its fragment path is null or empty" misphrases the predicate — the **file at** the fragment path is null_or_empty (host: FragmentPath=/etc/systemd/system/passim.service is a normal path); (b) "until the path changes" is the wrong trigger — the code fires when the file **stops being null_or_empty or can no longer be stat'ed** (3866-3868: stat failure → newer); (c) the two-forms leg ("zero-size file and dev/null symlink alike") rests on `null_or_empty`, which is **outside the pinned snapshots** (stat-util.h:50-52 at v262: `stat_may_be_dev_null(st) || stat_is_empty(st)`; stat-util.c:350-355: "A symlink to /dev/null or an empty file?"). True at v262, but not established by the three committed sources. |
| UL5 | holds | install.c:2350-2391, 2425-2444, 347-348, 3887-3888 | `unit_file_mask` creates a `/dev/null` symlink at `config_path/<unit name>` (2383-2387); state table distinguishes `[UNIT_FILE_MASKED]="masked"` / `[UNIT_FILE_MASKED_RUNTIME]="masked-runtime"` (3887-3888); `unit_file_unmask` reports `INSTALL_CHANGE_IS_MASKED_GENERATOR` — "Unit %s is masked via a generator and cannot be unmasked, skipping." (347-348, 2434-2444) — and its removal step only unlinks the null_or_empty file in the config dir (2447-2451), so the generator mask survives. |
| UL6 | fails | install.c:1965, 2013-2021, 2308-2313, 350-351 | The quote is real but attributed to the wrong moment. At **enable**, `install_info_symlink_alias` resolves the alias, `chase(..., CHASE_NONEXISTENT, ...)` marks `broken = r == 0` ("symlink target does not exist?", 2019) and **creates the symlink anyway**: `create_symlink(..., force || broken, ...)` (2021). `unit_file_verify_alias` checks only name validity/compatibility/self-loop (-EXDEV/-EUCLEAN/-ELOOP, 1854-1905), not target existence. `INSTALL_CHANGE_IS_DANGLING` ("Unit %s is an alias to a non-existent unit, ignoring.", 350-351) is emitted at exactly one site, in `install_context_mark_for_removal` (2278) when `install_info_traverse(SEARCH_LOAD)` returns `-ENOLINK` — a **disable/preset removal** path ("leads to a dangling symlink, removing name.", 2310). |

Corrected sentences I would accept:

- **UL1**: "Unit files are loaded from a set of paths determined during compilation, and a unit found in a
  directory listed earlier overrides the same name lower in the list; setting `$SYSTEMD_UNIT_PATH` overrides
  the unit load path, and if it ends with an empty component (`:`), the usual unit load path is appended to
  the variable's contents (systemd.unit.xml:366-378)."
- **UL2**: "Multiple drop-in files with different names are applied in lexicographic order regardless of
  which drop-in directory they reside in; drop-ins in /etc/ take precedence over /run/ and those in turn
  over /usr/lib/; and drop-in files **under those drop-in directories** take precedence over unit files
  wherever located (systemd.unit.xml:235-239)."
- **UL4**: "A masked unit keeps suppressing a daemon-reload while the file at its fragment path is still
  null_or_empty — an empty regular file or a /dev/null symlink (predicate defined in
  src/basic/stat-util.{c,h} at v262, outside the pinned snapshots) — and stops suppressing it as soon as the
  file is no longer null_or_empty or can no longer be stat'ed (unit.c:3859-3894)."
- **UL6**: "At enable time an `[Install] Alias=` symlink is created even when the alias target does not
  exist (install.c:2013-2021: the alias is marked broken and `create_symlink` is called with
  `force || broken`); `INSTALL_CHANGE_IS_DANGLING` ('is an alias to a non-existent unit, ignoring') is
  reported on disable/preset removal paths when `install_info_traverse` returns -ENOLINK for a name whose
  alias chain dangles (install.c:2308-2313, 350-351)."

## Attack log (each attempt: command in scratch `--fixture` harness reusing the frozen module's own `build_fixture`/`score_tree`)

| # | attempt | result | evidence |
|---|---|---|---|
| A | content-free word-salad statement ("Unit files directories listed earlier override same name lower list compiled variables described tables below system") + the real verbatim quote | **survived** — admitted | `UL_ROW ok UL1 …` ×6, `UL_ROWS=6 UL_VERIFIED=6 … met=1`, rc=0. Grounding (≥6 tokens, share ≥0.5) is satisfiable by word salad; the counter is a form instrument. |
| B | verbatim quote lifted from an unrelated region of the same snapshot ("precedence over any file modification time checks", the ConditionNeedsUpdate text) for UL1 | **survived** — admitted | `UL_ROWS=6 UL_VERIFIED=6 … met=1`, rc=0. No quote-to-statement locality check. |
| C | scripted writer that copies snapshot sentences (the fixture CONTROL rows are exactly that) | **survived** by design | `SELFTEST-CONTROL … rc=0`; admission cannot distinguish a copied sentence from a grounded one — the semantic layer is the attack seats' job (QUALITY 81/90). |
| D | pipe character inside a quote cell | **held** | `UL_ROW fail malformed-row: | UL6 | …` → `UL_MALFORMED=1 met=0`, rc=1. The cell guard works. |
| E | registry anchor cell with no line anchor ("systemd.unit.xml somewhere, no line range") | **survived** — admitted | `UL_ROWS=6 UL_VERIFIED=6 … met=1`, rc=0. The anchor clause binds only the snapshot basename as a substring; no line-range is enforced by the instrument. |
| F | `--selftest` hermeticity | **held** | Both selftests PASS under `TMPDIR=$S`; the counter refuses `TMPDIR=/tmp` (SELFTEST-HERMETIC). |

## Host re-measure (2026-11-03, live; committed reference `.ufo/waves/round-73/before/host.txt`)

`systemctl --version` → `systemd 262 (262.1-1-arch)`; `systemd-analyze unit-paths | wc -l` → 12;
`systemctl show -p DropInPaths -p FragmentPath -p LoadState user@1000.service` → LoadState=loaded,
FragmentPath=/usr/lib/systemd/system/user@.service, DropInPaths=/usr/lib/systemd/system/user@.service.d/10-login-barrier.conf
/etc/systemd/system/user@.service.d/faster-shutdown.conf (same order); `getty@tty1.service` →
LoadState=loaded, FragmentPath=/usr/lib/systemd/system/getty@.service; `find /etc/systemd/system -maxdepth 1
-type l -lname /dev/null` → exactly passim.service and systemd-networkd-wait-online.service;
`passim.service` → LoadState=masked, FragmentPath=/etc/systemd/system/passim.service, UnitFileState=masked.
**Delta from before/host.txt: none.**

## Statements not established at v262 (version-skew list)

1. UL4's null_or_empty two-forms semantics — defined in `src/basic/stat-util.{c,h}` (fetched at v262 read-only:
   stat-util.c sha256 `8d133568388ca5851140dcf278814ef87302b4249b3655287a8ae7b9b023fe59`,
   stat-util.h `a9d72ec2e4b6db35d37ad40fc573f9b52cb696f2d6694caa6d77904caa75de95`), true at the tag but absent
   from the three committed snapshots.
2. UL1's "replaces the whole path" — contradicted at v262 by the documented trailing-`:` append case.
3. UL6's enable-time direction — at v262 dangling alias symlinks **are created** at enable; any text implying
   the IS_DANGLING gate fires at enable describes other versions, not the pin.
4. No row states which copy decides when several directories contain the same unit name at load (the mask/fragment
   decision lives in load-fragment.c, outside the snapshots); UL4's masking decision is likewise out-of-snapshot —
   unit.c only carries the still-masked freshness predicate.
5. The host is an Arch build (262.1-1-arch), possibly patched relative to upstream v262; all measured points
   reproduced the committed readings, so no measured claim is invalidated (QUALITY 103 satisfied for the measured legs).

## Bottom line

ROWS_HOLD=2/6 (UL3, UL5 hold; UL1, UL2, UL4 partly hold with corrections above; UL6 fails as stated).
The frozen counter verifies form only — attacks A/B/C/E pass it without the semantic work — so C1's
depth claim stands or falls on this semantic layer: as planned, UL6 must be rewritten and UL1/UL2/UL4
tightened before the note lands, and S304-S306 registry rows must be committed in the same revision.
