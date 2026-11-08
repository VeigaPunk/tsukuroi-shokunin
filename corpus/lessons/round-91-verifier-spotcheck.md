author: hyaku closure (non-author integrator, @m_zfl)

# Round 91 verifier spot-check — tsukuroi (closure judge, non-author)

Closure judge is not the round author. L1 attempt 1 (TsukuroiR91) died
without a report; attempt 2 (TsukuroiR91a2) inherited and reused its
committed work. Head judged: 71fc1b6695e5d6cb04ebef8bf43a5a9d0b402cd0
(branch master, ahead=0, clean). Before: 40efa4ea2862ab39da02430cada68f6dff230e86.

## 1. Step-1 conformance — PASS

- Report `.ufo/reports/round-91/tsukuroi.md` (10279 B) committed by lane
  identity (fleet log `tsukuroi-shokunin 86811a33…`), carries the
  `SHONEN` heading with one `[~]` line per SHONEN.md box (4 lines, non-author
  verification honestly owed, never self-attested `[x]`).
- Every cited lane commit exists and is an ancestor of branch master:
  d3b0987, d6f674f8, 45ae6518, 3d645e2c, 2d7e09e1, 6d181609, 17087261,
  6d12e07f, plus head-chain 20f65353/03b773e5/8a4826e9/71fc1b66;
  `merge-base --is-ancestor 71fc1b66 master` = yes; before `40efa4ea`
  likewise. Report cites tip at writing 6d12e07f; the four post-report
  commits (20f65353 narrowing-path fix, 03b773e5 M1 lesson + receipts,
  8a4826e9 control-fix corrections, 71fc1b66 N10 clone receipt + lesson
  sync) are post-wave control-evidence only — defect noted below, not a
  break of landed-last since the cited 6d12e07f remains an ancestor of
  HEAD at closure.
- Lane tree clean (`git status --porcelain` empty; jj state
  `ahead=0 behind=0 tracked=0 untracked=0`); pushed (remote
  refs/heads/master = 71fc1b66). Not a marker report (real work, evidence
  pointers, LOG-tied changes, checkable hashes).
- Prompt carries the template contract (§1 mission/axes, §2 1–3 claims
  with falsifiable before→after, §2b frontier step, §3 L2 floor,
  §4 report contract incl. SHONEN + marker rule, §5 commit/push scope,
  §6 hyaku addendum). Template-contract step-1 PASS.

Defects (status-neutral, routed §6): (a) report tip 6d12e07f is four
commits behind closure HEAD — evidence landed after the report was
written; (b) frozen SCORECARD declaration literals (sha 8f0daee8…,
"78 families") describe the r90 instrument, not the frozen 82-family
battery 655ee8f3… — disclosed in plans/round-91.md, never rewritten;
(c) census grew 53→56 lines with three W04 duplicate-url warnings
(S374–S376 share URLs with before/src/ pins) — expected, same URLs,
different snapshot dirs; (d) gate selftest 25/25 carries no V1/U1
coverage (ReviewGate S2, disclosed smoke-only).

## 2. Prefile falsification ledger (§2b)

`python3 scripts/hyaku/prefile-falsification.py --lane tsukuroi --round 91`
→ `PREFILE-FALSIFICATION: pass claims=2 rows=14 attack_seats=7 findings=0`,
exit 0. Covers both claims (C1 ×7 rows, C2 ×7 rows); every
`falsifies-wording` row names the narrowing `.ufo/plans/round-91.md`:
C1/CriticClaims (declaration sha/counts, K2 broken control, F2-oracle 80/82,
F3-equivalent-mutant, freeze-manifest omission), C2/ConnectorOverlap
(committed C2 header/prose falsifier at uri.c:106 — the repaired text
and `source:/recheck:/verified-at:` headers are what land, never the
falsified bytes). Ledger not edited. No unreconciled falsifying row.

## 3. Per-claim re-check

### C1 (measured, operability 9, narrowed) — evidence-verified PASS

Per PROTOCOL §Gate standard (Closure consequence) the sibling's gate is
not executed here; the committed evidence is verified instead, against
the frozen revision.

- Counting command (as declared): `python3 tools/limine-pin-battery-r91.py
  --gate tools/check-limine-pins.py --runs 3`, canonical + `git clone
  --shared`. Committed receipts
  `.ufo/waves/round-91/after/measured/c1-receipt-{canonical,clone}.{txt,json}`
  each carry 3 × `families_passed 82/82 verdict met` and per-family JSON
  `families_total: 82, families_passed: 82, verdict: "met", cases: 328,
  failed_families: []` (both layouts). Independent re-count of the
  frozen `FAMILY_ROSTER` literal at the closure tip: 82 items (first
  POSITIVE … last UNVERIFIED-SORTED) — matches the reported 82/82.
- Frozen battery sha256 (closure tip and freeze) `655ee8f3…` — matches
  the receipt headers and the narrowing amendment; the 13-line
  freeze-manifest sha list is unchanged between d3b0987 and the closure
  tip (13 lines both ends). Defect disclosed, not claimed: the manifest
  omits the battery itself and predates 203b3872/1652b086 — the narrowed
  predicate excludes freeze-manifest battery binding (void clause
  disclosed as NOT binding in the report).
- Before→after re-derived: before K1 (r90 landed gate) reads 2/82 unmet
  ×3, 0 error cases, both layouts (control summaries); after: 82/82 met
  ×3, both layouts. Kill rule (any run < 82/82) not triggered on the
  committed receipts. The report's `git ls-remote origin
  refs/heads/master` match at 6d12e07f re-verifies at 71fc1b66
  (identical remote/local tip).
- Controls confirm the Do-Nothing / near-miss discipline: K1 valid
  (2/82 ×3, 0 errors, both layouts). K2 was broken at freeze (duplicate
  `--tpm-present` → 984/984 `error:` cases); repaired post-wave as
  evidence (6d12e07f, `K2-landed-adapter-fixed.*` 2/82 unmet ×3,
  0 errors, canonical + clone). N10 duplicated N01 byte-identically at
  freeze (`7e158cd2…`); rewritten as distinct whole-file LAST-wins bend
  (78/82 unmet ×3 canonical + clone, `N10-panic-first-anywhere-fixed.*`).
  N01–N09 each kill their named families ×3 in both layouts (control
  summaries).
- Gate mechanics verified in committed bytes: the gate reads
  `hash_mismatch_panic`/`measured_boot` only in the global section
  (config.c 642-650 cut, first-line-entry exception preserved) and
  emits sorted `unverified_image_lines` for efi chainload entries whose
  image line is not a pin URI (check-limine-pins.py:181-193, `:258`
  field; S1 sanitize on both top-level values via `sanitize()`).
  F2-oracle-import discrimination is NOT established (F2 80/82;
  sibling-oracle-forgery reads 82/82 met — ScribeLesson M1, open
  channel, disclosed); F3 missing-`unverified.sort()` reads 82/82 but
  is an equivalent mutant (append order already `sorted(image_lines)`),
  not battery blindness — correctly narrowed, not claimed.
- Self-test tally (committed evidence): gate selftest 25/25 PASS and
  battery selftest 18/18 PASS per ExecLints; registry row
  `limine-pins` names entry command, verdict map (0/1/2/64), selftest
  spelling `--selftest`, and pooled sources S350–S353.

C1 verifies on its narrowed predicate (evidence-verified; gate not
re-executed by the judge).

### C2 (exploratory, depth 8, narrowed) — unprovable-but-better

As the named non-author reviewer, the judge rules: better, genuinely.
The entry `corpus/knowledge/limine-unverified-image-r91.md` (+ `.json`,
S374–S376, uri.c/chainload.c/config.c, tag 8ad14430… for host limine
12.9.4-1) documents four sourced clauses no prior entry held — the
silent no-shape fail (uri.c 46-75), the unhashed-but-shaped SB bypass
(uri.c 106 `return true` → chainload.c 423-427 clearing
secure_boot_active), first-PATH precedence (chainload.c 414-421), and
the hash-mismatch prompt bypassing `panic()` (uri.c 307-314). The host's
own line 72 (`path: boot():/EFI/BOOT/BOOTX64.EFI`, no `#`) is a live
instance re-opened on committed bytes. ReviewSource CONFIRMED all
clauses against the pinned v12.9.4 clone; ScoutDrift's upstream
v12.9.5/12.9.6 inversion of the V1 first-line exception is correctly
pinned to the host version only (freshness boundary named in the
entry). Two precision repairs (D3 `#`-missing case; ConnectorOverlap
uri.c:106) were folded into the entry text before landing — the
landed bytes, not the falsified header, are what is judged. No
counting command exists for an exploratory claim; the verdict rests on
the dated, pinned, host-measured content, not on volume. Narrowed
predicate is exactly what the sources support.

### Axis harm check

`git diff 40efa4ea 71fc1b66 -- SCORECARD.md` appends the round-91
declaration + measured + final-measured rows only (96 insertions,
prior rows untouched); SKILL.md +1 line (registry row), README.md +20
(frontier). No owned axis regressed: r87-era gate answers unchanged
except the sourced R4/R9/R10 replacements; the new `on_panic` field
and M1 oracle-import channel are disclosed, not claimed. Axis verdicts:
operability **improved** (V1 visibility + U1 reporting now measured
82/82 ×3 both layouts, S1 sanitize fixed), depth **unprovable-but-better**
(C2 entry better, scored by this named non-author judgment),
coverage/calibration/freshness/adjacency **unchanged**.

## 4. Discernment spot-check (from outside)

Census: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
validate --root /home/vgpnk/Projects/shokunin tsukuroi` → exit 0
(`tsukuroi ok …/corpus/SOURCES.md`), 376 registry rows (before 373
rows, 53 census lines → after 56, +S374–S376). SOURCES went 373→376
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}…'` → 376 at tip), all tier A,
all `mined`, consistent with the report's claim.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| C2 admit — `corpus/knowledge/limine-unverified-image-r91.md` admitted on S374–S376 | admit | pinned snapshot `after/src-c2/limine-v12.9.4-common_lib_uri.c` lines 46-110 + `…_chainload.c` 414-435 + `…_config.c` 642-650; host `before/host/receipt.txt:20` line 72 | agree (admit stands) | every clause re-derived: no-`(`/no-`):/`/empty-path → `return false` without URI_ERROR (uri.c 46-75); hash loop falls through to `return true` at :106 (unhashed-but-shaped); PATH→IMAGE_PATH precedence + secure_boot_active cleared around uri_open (chainload.c 414-427); config cut at 642-650 with first-line-entry guard; host line 72 is the live instance. ScoutDrift pins the inversion to ≥12.9.5, so the 12.9.4 pin is correctly bounded |
| Selftest-gap reject — ReviewGate S2 (gate `--selftest` carries no V1/U1 coverage) left unlanded, routed as known gap | reject-as-claim-defense | `w1/ReviewGate/patch-selftest-coverage.diff` + lesson S2 + SKILL registry row (selftest is smoke-only, battery is the frozen target) | agree (reject stands) | the round did not claim V1/U1 coverage through the selftest; the battery is the measured arm and the gap is disclosed in the lesson, the SCORECARD row, and the narrowing — taste correctly applied: the selftest trap is named and routed, not silently landed |
| Battery-isolation reject — ScribeLesson M1 `R91-JUDGE-ORACLE-IMPORTABLE` patch proposed, not landed mid-round | reject (defer) | `w1/ScribeLesson/receipts/` (sibling-oracle-forgery 82/82 met vs isolated battery 0/82; landed gate 82/82 met under isolation) | agree (reject stands) | freezing is already committed and re-pinning mid-round would falsify the freeze record; the open channel is disclosed in the SCORECARD row and routed as round-92 work with a drafted QUALITY 132 — exactly the right taste |

New-row quote check (S374): the row's `teaches` spans 23 words
("a value with no '(' or no '):/' or no '#' after '):/' makes
uri_resolve return false with no message, and uri_open returns NULL")
grounded in the anchor `uri.c raw lines 32-107 …, 335-336 …` and the
pinned snapshot sha256 `e06cac12…`; the quoted location matches the
re-opened bytes (silent `return false` at 49/62/74/91/99, uri_open
NULL at 335-336). Quote ≤25 words, location-grounded — pass.

## 5. Trend verdicts (with evidence)

- expansion: **unchanged** — 3 new S-rows + 1 knowledge entry on
  genuinely new ground (URI resolution / unhashed image lines); no
  coverage score change.
- quality: **improved** — V1 visibility and U1 reporting are now
  measured by the frozen battery (82/82 ×3 both layouts, receipts
  §3); ReviewGate S1 (JSON sanitize of `measured_boot.value` /
  `hash_mismatch_panic.value`) is fixed in 45ae6518; F2/F3/K2/N10
  defects are disclosed and narrowed, not claimed.
- discernment: **improved** — the lane downgraded its wording to
  `.ufo/plans/round-91.md` where the wave falsified it (CriticClaims,
  ConnectorOverlap), repaired the C2 header/prose before landing, and
  routed M1/S2 as future battery-hardening instead of landing them
  mid-freeze.

## 6. Routed defects (lane fixes next round)

1. **Report-before-final-commits**: the report cites 6d12e07f while
   20f65353/03b773e5/8a4826e9/71fc1b66 landed after — file the report
   last, or re-cite the tip in a correction.
2. **Frozen declaration literals**: SCORECARD `8f0daee8…` sha and "78
   families" describe the r90 instrument, not the 82-family battery —
   correct via an append-only correction entry, never an in-place
   rewrite of the frozen declaration.
3. **Battery oracle-isolation**: land the proposed isolated-battery
   patch + QUALITY 132 (M1 `R91-JUDGE-ORACLE-IMPORTABLE`) so 82/82
   discriminates an honest gate from an oracle-importing one.
4. **Freeze-manifest binding**: regenerate the manifest after the
   final battery commit and include the battery itself; the current
   13-line manifest omits it and predates 203b3872/1652b086.
5. **Selftest coverage**: land the proposed selftest V1/U1 cases
   (ReviewGate S2) so a whole-file regression cannot pass the
   selftest silently.
6. **Upstream re-pin watch**: on host limine ≥12.9.5 (Arch extra
   already ships 12.9.6-1) the V1 first-line exception inverts
   (ScoutDrift) — re-pin is gated on the host upgrade, not on this
   round's pin, which stays correct for 12.9.4-1 only.

SHONEN boxes remain `[~]` with resolvable pointers (SKILL.md decision
table :38-50, checklist :90-141, battery row :5930; LOG.md round-91
end-to-end entry; CriticForgers base.py 82/82 docstring-only; PROVINCE
ADJ rows + ConnectorOverlap 0 conflicts) — non-author verification of
the promotion gate remains owed, honestly marked.
