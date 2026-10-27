VERDICT: defect-found

Seat ResRevSkill, item R-4: review of the SKILL.md text appended at
`194a4523288759b4b73248d1ebcce53e43d0eec7` (sections "Census first-line readers — round 45"
SKILL.md:4232-4285, "Scrub grounding — round 45 rows" :4286-4346 including
"### Correction — the round-44 scrub rows" :4329-4345, and
"Gate and probe registry — round45 superseding current rows" :4347-4424). Text read verbatim
via `git show 194a4523…:SKILL.md` (receipt copies: `.ufo/waves/round-45/a2r1/ResRevSkill/`).
This is a falsifying read, not a counted verdict. All line numbers below are at `194a4523`.

## Findings

### F1 (defect, factual): the SKILL names the GR2 residual seat `C2ResGR2`; the dispatched seat is `ResRevGR2`

SKILL.md:4342-4344 ("Limits (entry Limits)"): "…GR2 was corrected at the integration after its two
counted seats read `partly` (earlier device checks, the suspended state, the unprivileged sysfs view)
and is read by the residual `C2ResGR2`". `.ufo/waves/round-45/a2r1-dispatch.json` (read at 194a4523
bytes; same at working tree) contains no task named `C2ResGR2`. Its GR2 residual seats are
`ResRevGR2` (agent `reviewer`) and `ResCritGR2` (critic); the full dispatch name set is
ResCritGR2, ResRevAppends, ResRevGR2, ResRevGR3Triage, ResRevSkill
(receipt `ResRevSkill/evidence.txt` §a2r1 dispatch). Consequence beyond the wrong name: the counter's
`bound()` requires exactly one `a2r1-dispatch.json` task with `name == "C2ResGR2" and
agent == "reviewer"` (tools/check-scrub-grounding-r45.py at 194a4523, `RESIDUAL_WAVE='a2r1'`, the
`bound(a.lane, rev, RESIDUAL_WAVE, f'C2ResGR{n}', 'reviewer', row)` call), so a `partly` row's
residual can never bind under the dispatched names — even with a `holds` first line from
`ResRevGR2`, GR2's `verdict_ok` stays false. Observed: my run of the counter at 194a4523 gives
`verdicts_ok: 0` with all six `a2w1` seat outputs `null` anyway, but the dispatch naming removes even
the residual repair path the SKILL describes.
Replacement text: "…and is read by the residual `ResRevGR2` (wave `a2r1`; the counter binds the name
`C2ResGR2` and no such seat is dispatched, so no residual can raise `verdicts_ok` for GR2)."

### F2 (defect, factual): dangling citation — SCORECARD.md has no "Round 45 — measured outcome" section

SKILL.md:4288-4290: "the depth gate FAILED — `verdicts_ok` 0, no counted verdict bound
(`SCORECARD.md` "Round 45 — measured outcome")". At 194a4523 SCORECARD.md (2904 lines) has exactly
two round-45 sections, `## Round 45 — declaration` (line 2847) and
`### Round 45 — attempt-2 rebinding` (line 2892); the file ends there, no "measured outcome" section
(`git show 194a4523…:SCORECARD.md | grep -n 'Round 45'`). The cited substance is true — I ran
`python3 tools/check-scrub-grounding-r45.py --revision 194a4523…`: `verdict FAIL`, `verdicts_ok 0`,
all six counted seats `null` (receipt `ResRevSkill/tool-runs.txt`); and
`a2w1-results.json` has `output: null` for all six C2RevGR/C2CritGR seats — but the named section
does not exist.
Replacement text: "(`a2w1-results.json` `output` null for all counted seats; counter run at the
integration revision: `verdicts_ok` 0)" — or cite whatever round-45 measured-outcome section the
L1 appends, once it exists.

### F3 (minor, imprecision): the "still present" pattern is not `printf '%s\n' "$CAP_OUT" | head` at three of the seven lines

SKILL.md:4265 (observation cell): "`printf '%s\n' "$CAP_OUT" \| head` still present at `:707`,
`:832`, `:997`, `:1196`, `:1517`, `:1531`, `:1817`". At 18389f44 the named lines are
(receipt `ResRevSkill/evidence.txt` §seven-line):
- `:707`, `:997`, `:1531` — `mapfile -t X < <(printf '%s\n' "$CAP_OUT" | … | head -n …)` (process substitution, CAP_OUT-derived);
- `:1517` — continuation of the `printf '%s\n' "$CAP_OUT"` pipeline opened at `:1514`, closed by `|| true` (CAP_OUT-derived, `|| true`-masked);
- `:832` — `holds=$(grep -hE '^[[:space:]]*HoldPkg' "$PACMAN_CONF_FILE" 2>/dev/null | head -n1 | sed … || true)` — a `grep` on a file, no CAP_OUT anywhere;
- `:1196` — `done < <(find "$CGROUP_ROOT" -xdev … -print 2>/dev/null | LC_ALL=C sort | head -n 4000)` — find output, no CAP_OUT;
- `:1817` — `unk_names=$(printf '%s\n' "$cl_out" | grep '^?' | … | head -n6 | paste -sd, - || true)` — `$cl_out`, not `$CAP_OUT`.
The second half of the cell — "each sits in a process substitution or behind `|| true`, so its
status is not the assignment's and cannot kill the census" — is true at all seven (verified
line-by-line; the wave receipt `a2w1/C1ExecMaskedSites.md` enumerates the same three forms and
names the seven "the seven unclaimed `| head` readers"). Only the quoted pattern in the first cell
is wrong: a literal grep for it finds only the prose comment at census:3334. The SCORECARD
declaration's own phrasing is the correct one.
Replacement text: "``| head`` consumers of captured or file output still present at `:707`,
`:832`, `:997`, `:1196`, `:1517`, `:1531`, `:1817`".

### F4 (minor, imprecision): the round-41 `bn` form was `awk … exit`, not `| head`

SKILL.md:4274: "six revert mutants — S1-S5 back to their base lines and the foreign-baseline `bn`
back to the round-41 `| head` form". The round-41 `bn` line (at 78abb8b5^ — the pre-round-42
commit) was `bn=$(printf '%s\n' "$base_txt" | awk -v n="$nm" '$1 == n {print $2; exit}')` — an
early-exiting `awk` reader, no `| head`; the counter's docstring (scrr45.py) calls it the same way
("the round-41 form" of `awk -v n=… exit`). `| head` vs `awk … exit` is the same SIGPIPE class
(the round-42 SKILL section at :3858 names `awk … exit` one of the early-exiting readers), so the
class claim holds; the named mechanism is wrong.
Replacement text: "…and the foreign-baseline `bn` back to the round-41 `awk … exit` early-read form".

### F5 (minor, over-generalization): not every conversion "does the CR removal and trailing-blank strip"

SKILL.md:4243: "each now takes its first line by parameter expansion (`X=${CAP_OUT%%$'\n'*}`) and
does the CR removal and trailing-blank strip in the same expansion". At 18389f44: `:965`, `:1460`,
`:1535` do both expansions; `:1003` does only the CR strip (`r=${r//$'\r'/}`, matching its base
which had only `tr -d '\r'`); `:1085` does neither (its base's post-processing was the `awk` comma
split, kept via `printf | awk`).
Replacement text: "each now takes its first line by parameter expansion (`X=${CAP_OUT%%$'\n'*}`)
and, where the base form had them, does the CR removal and trailing-blank strip in further
expansions — no `head` inside an assignment".

### F6 (minor, gloss incomplete): the quote-size rule understates one disjunct

SKILL.md:4312-4313: "its text occurs on the named line and is substantial (at least half of the
stripped line, and at least 10 characters)". `quote_good` in tools/check-scrub-grounding-r45.py
implements `(len(qs) >= 10 or qs == whole) and 2 * len(qs) >= len(whole)` — a short quote that is
the whole stripped line passes the code but fails the SKILL's stated conjunction.
Replacement text: "…is substantial (at least 10 characters or the whole stripped line, and at least
half of the stripped line's length)".

### F7 (minor, imprecision): "(162000 bytes)" and "~150 KB" fit only one of the five r45pad cases

SKILL.md:4260: "each case puts the deciding first line in front of ~150 KB of padding (162000 bytes)".
`r45pad` (census-impl.sh:3338) emits 2000 × `"%s padding line %05d …"`, so the byte count depends on
the tag: measured `sysrunning` → 162000, `result` → 154000, `NVIDIA GeForce RTX 5070, 999.99.99` →
210000, `active` → 154000 (`awk … | wc -c`); the five r45pad cases land in 154000-210000 bytes
(~150-205 KB), and the sixth case's padding (2000 `zz-r45-baseline-padding-package-` rows plus the
real baseline) measures 88000 bytes — all still past the 65536-byte pipe buffer.
Replacement text: "each case puts the deciding first line in front of ~150-205 KB of padding
(154000-210000 bytes; the sixth ~88 KB)".

## (a) Claims verified against the files named

Census section (`tools/tsukuroi-census.sh` at `18389f44`, counter at `194a4523`):
- Site lines: `set -euo pipefail` :451; converted readers :965 (`probe_systemd` `state`), :1003
  (timer `Result` `r`), :1085 (`probe_drivers` `driver`), :1460 (`probe_journal` `t_word`), :1535
  (timer `ActiveState` `r`) — each now `${CAP_OUT%%$'\n'*}` parameter expansion; the base at the
  same line numbers had `X=$(printf '%s\n' "$CAP_OUT" | head -n1 | …)` (census-base.sh same lines).
- Six `(R45-C1)` selftest cases at census :3342/:3347/:3355/:3360/:3365/:3374; selftest case count
  148 at base (`K0` line: "PASS (148 cases …)") → 154 (`K8`/receipt line "PASS (154 cases …)").
- Census sha256 `237b21c9d757…` at 18389f44 — matches `git show | sha256sum` (receipt
  `ResRevSkill/evidence.txt`).
- Counter sha256 `fe0e31e25c5b…` at 194a4523 — matches.
- Counter sha256 `a1eb402dffae…` for check-scrub-grounding-r45.py at 194a4523 — matches.
- Predicate sentences: C1 `lexical_hits == 0 and sites_found == 5 and equiv_ok == 5 and
  selftest_pass == 1 and selftest_r45 >= 6 and revert_killed == 6 and adjacency_ok == 1` — verbatim
  `PREDICATE` in score-census-readers-r45.py; lexical leg `"$CAP_OUT" | head` before
  `run_selftest() {` — `LEX_RE` + `lines[:st_start]` (run_selftest at census:2046; 0 hits).
- Eight draws/site, ≥3 large (70-300 KB tail) — `draws()` builds 8 draws, first 3 `large`,
  `rng.randint(70_000, 300_000)`. Six revert mutants S1-S5+S6 — code. Adjacency kill rule: lane
  `tools/check-adjacency-anchors.py` + `tools/_revision.py` bytes must equal BASE bytes — code
  `adj['bytes_base']`.
- Rebinding: `057c1804` changed only the two wave-name literals — `git diff 057c1804^ 057c1804
  -- tools/check-scrub-grounding-r45.py` shows only docstring + `VERDICT_WAVE='a2w1'` /
  `RESIDUAL_WAVE='a2r1'` constants and their three call-site uses; the pre-rebinding file sha256
  `7e373196decd…` matches the registry row.
- Controls: `controls/battery-summary-c1.jsonl` — K0 FAIL (lexical_hits 5, equiv_ok 0, selftest_r45
  0, revert_killed 0, adjacency_ok 0), K1-K7+K10 FAIL, K8+K9 PASS, control_accepted 1 —
  all as stated. K1 is the `| head -1` evasion (run_controls_c1.py:79); K9 `sed -n 1p` (:97).
  `controls-a2/battery-summary-c2.jsonl` — 30 controls, K3/K19/K26 PASS, the other 27 FAIL,
  `should_fail_accepted` 0 — as stated.
- `a2w1/C1ExecFullLarge.md` — base 141 / 0 PLANE lines; impl 2 with six PLANE lines identical to
  the unpadded run (receipt §"Exit codes", §"Every plane line equals a first-line-only run").
- `a2w1/C1ExecRerun/c1-after-{1,2}.jsonl` — counter PASS at 18389f44 twice; base FAIL —
  "the scored outcome of the counter at `18389f44` is the receipt line under `.ufo/waves/round-45/`".
- Mechanism reproduced on this host: pipe capacity 65536 (`fcntl` F_GETPIPE_SZ); under
  `set -euo pipefail` a 20000-line variable: base form exits 141 prints nothing; parameter-expansion
  form prints first line exits 0 (commands in `ResRevSkill/evidence.txt` / transcript).
- `probe_packages` `bn` is a full read at census :777 (`awk '$1 == n && !f { print $2; f = 1 }'`).

Scrub section (`tools/check-scrub-grounding-r45.py`, the entry, the snapshots):
- All snapshot digests verified before use: `sha256sum -c` OK on
  `.ufo/waves/round-45/frozen/src/SHA256SUMS` (5 files), `round-44/frozen/src/SHA256SUMS` (5),
  `round-42/frozen/src/SHA256SUMS`; capture.txt sha256 `f5958a83…` equals the `CAPTURE` pin.
- Predicate `rows == 3 and quotes_ok == 3 and props_ok == 3 and host_ok == 3 and sources_ok == 1
  and verdicts_ok == 3 and novelty_base_hits == 0 and pointer_ok == 1` — verbatim `PREDICATE`.
- Verdict binding description matches `bound()`: `C2RevGR<n>`/`C2CritGR<n>` of `a2w1` via
  dispatch+results and report first line `ROW GR<n> VERDICT:`; `partly` answered by residual;
  unbound counted seat → not ok (code `None not in vs`).
- Every cited source line verified on the digest-checked snapshots: S243 sysfs.c:2040 `memparse`,
  :2042 skip_spaces, :2043-2044 EINVAL; S246 cmdline.c:156 `simple_strtoull(ptr,&endptr,0)`, :189
  digit-precedes-suffix, :191-192 overflow→ULLONG_MAX, range 147-193 (memparse incl. K-M-G-T-P-E
  comment :147, both cases); kstrtox.c:29-33 base-0 rule; vsprintf.c:86 `_parse_integer_fixup_radix`;
  S242 scrub.c:3120-3143 the three checks (ENODEV :3123, EROFS :3133, EIO :3142), :3147 dev->scrub_ctx,
  :3148-3153 `!is_dev_replace && btrfs_dev_replace_is_ongoing` → EINPROGRESS; S247 dev-replace.c
  :700-703 + :1265-1268 `btrfs_scrub_dev(…, false, true)`, :1286-1287 STARTED|SUSPENDED;
  S244 btrfs-scrub@.service:9 `KillSignal=SIGINT`, no `KillMode=` in file; S248 systemd.kill.xml
  :68,101 (control-group default, :101 "Defaults to <option>control-group</option>"), :91,96
  (SIGKILL after TimeoutStopSec unless SendSIGKILL=no), :114-115 SIGCONT follows, :108 (KillSignal
  default SIGTERM); S237 progs scrub.c:421 `BTRFS_IOC_SCRUB_CANCEL` in the SIGINT handler
  (installed for the child at :1546); sysfs.c:1288 `device replace`, :2015 REPLACE_TGT;
  capture.txt:1 uid=1000 CapEff=0, :2 systemd 262-1-arch, :3 `KillSignal=2 KillMode=control-group
  TimeoutStopUSec=5s FinalKillSignal=9 SendSIGKILL=yes`, :4 `DefaultTimeoutStopSec=5s` drop-in,
  :5 owner `none`, :8 scrub_speed_max mode=644 owner=root value=0, :9 devids=1 — all exact.
- Gate status: `a2w1-results.json` `output` is `null` for all six counted seats; `C2RevGR1.md` does
  not exist; the other five first lines are `ROW GR1 VERDICT: holds`, `ROW GR2 VERDICT: partly` ×2,
  `ROW GR3 VERDICT: holds` ×2 — consistent with "no counted verdict bound" and two `partly` on GR2.

## (b) GR2 row vs corrected entry row GR2

The SKILL GR2 row (SKILL.md:4304) says exactly what the corrected entry `## GR2` says
(entry.md:55-118): replace copies through scrub via `btrfs_scrub_dev(…, false, true)` at start
(:701-703) and continuation (:1265-1268); three device checks answer first (ENODEV/EROFS/EIO,
scrub.c:3120-3143); then `-EINPROGRESS` while dev->scrub_ctx (:3147) or a non-replace call while
`btrfs_dev_replace_is_ongoing` i.e. started or suspended (:3148-3153; dev-replace.c:1286-1287);
progress query for the source devid answers 0 `[inference for the ioctl return path and the
btrfs-progs printing]`; unprivileged sysfs `exclusive_operation` (sysfs.c:1288) and
`replace_target` (sysfs.c:2015); operator owns start/cancel. SKILL adds nothing the entry does not
contain (the "no scrub was started" Observation gloss matches the entry's Statement conclusion).
PASS.

## (c) Correction block vs the named round-44 rows

All four named targets found verbatim in the same SKILL.md: the first row's tag
"(dev-replace.c:701-703,1265-1268, unpinned)" at :4222; "K/M/G suffixes" in the `scrub_speed_max`
row at :4225; the stop-signal row (Arch units / KillSignal row) at :4226; the two Limits fragments
at :4229-4230. Each correction is source-true per the snapshot lines verified in (a). PASS.

## (d) Registry coverage

`python3 tools/check-registry-coverage.py --revision 194a4523…` → `{"status":"PASS",
"counts":{"registered":72,"rows_total":72,"tools_total":72},"findings":[]}`, exit 0 (receipt
`ResRevSkill/tool-runs.txt`; note the receipt's `branch_tip` field names a newer master tip — the
run evaluates `--revision`, not HEAD). Independent table diff (`ResRevSkill/table-diff.txt`): the
round45 table at :4350-4424 carries the round44 table's 70 rows (:4038-4109) byte-verbatim in order
plus exactly two rows — `census-readers-r45` and `scrub-grounding-r45`. Both new rows match their
counters: commands verbatim from usage/docstrings, predicate sentences verbatim `PREDICATE`,
sha256 values match computed bytes, `7e373196…` is the pre-rebinding freeze digest
(057c1804^:tools/check-scrub-grounding-r45.py sha256), write-scope claims hold (scratch-only
`--scratch` subdir for score-census-readers-r45; committed-reads for check-scrub-grounding-r45).

## Residual risk / not checked

- SKILL's glosses on code are verified against code; I did not re-run the C1 counter end-to-end
  (the wave receipts `c1-after-{1,2}.jsonl` and `c1-check-194a4523.jsonl` already show PASS at both
  revisions; my own runs of the two gates are receipts above).
- `a2w1/C1ExecLiveRead.md` exists (strace kill-rule check); its contents were not re-derived.
- The `(R45-C1)` case-6 fixture crosses the buffer at ~88 KB — confirmed by size, not by a live
  revert run (the counter's own K-mutants already proved the kill).
- F1's consequence (residual can never bind `C2ResGR2`) is code-level certain: `bound()` matches on
  task `name`/`agent` exactly and `a2r1-dispatch.json` contains no `C2ResGR<n>` task.

Tooling: no installs; git 2.x, bash, python3, coreutils from the host. Scratch
`/fast/scratch/hyaku/tsukuroi-r45/ResRevSkill` removed on exit (receipts copied into
`.ufo/waves/round-45/a2r1/ResRevSkill/`). Read-only on the lane: only `git show/diff/log`,
file reads, and the two committed counter invocations (both write nothing outside private tmp;
`check-registry-coverage.py` writes a private TemporaryDirectory HOME).
