# ReviewGate-5 — surgical review, round-94 V4 gate (freeze eb3b3e5150a63507a382003fa1a70039b190396b)

Scope: `tools/check-limine-pins.py` V4 diff (76 lines), five adversarial probes plus
extra probes P6/P7/P8. Freeze manifest `sha256sum -c`: 12/12 OK. All probe fixtures,
receipts stay under `.ufo/waves/round-94/w1/ReviewGate/`.

## Diff review (full-diff.txt)

The V4 freeze touches exactly three hunks in `tools/check-limine-pins.py` (the rest of
the commit is batteries, controls, fixtures, plans):

1. Docstring (`:42-50`): `--limine-version` default `auto`, probe = first `X.Y.Z`
   immediately following `limine`, case-insensitive, optional `v`, not-word-char suffix
   guard, failed probe = rc 64 / no verdict. Matches code.
2. `probe_limine_version` (`:107-122`): regex gains `(?![\w.-])` guard. Stdout-only,
   5 s timeout, rc!=0 → None, no parsable → None. This is the sole probe text parser.
3. Selftest (`:59-62`): adds `12.9.6-rc1 → None`, `12.9.6.1 → None`, stderr-version →
   None, bare `12.9.6` (no `limine` prefix) → None. All exercised by `probe-version`
   case. `main()` (`:503`): `default="auto"`, help updated, `version == "auto"`
   branch probes, records `limine_version_source: "probe"`, refusal on failed probe
   precedes the `parse_limine_version` check. `--live` path (`:524-530`) reuses the
   same resolved `version`/`version_source` — no separate packaged default.

Completeness check on the "other packaged defaults" question: the only other
`12.9.4` default is `check()`'s own parameter default
(`:187`, `limine_version="12.9.4"`). It is unreachable from the CLI — both CLI call
sites pass an explicit version (`:527` live, `:532` conf/esp; auto resolves in
`main()` first). It IS reachable from two selftest-internal legs: `case()` with
`ver=None` (`:357`, e.g. `era-default` at `:438`) and the `conf-absent` check
(`:478`). Those legs pass a literal `12.9.4` that the gate records as
`limine_version: "12.9.4"` — but parse/era selection still goes through
`parse_limine_version` + `VISIBILITY_ERA_SPLIT` exactly once. No second parse site
exists: `parse_limine_version` (`:91-101`) has the 1-9-digit bound, used by `check()`
(`:190`) and by `main()`'s guard (`:519`). The usage roster in the battery passes
values via the flag API into that one parser. So the suffix guard is applied
everywhere version text is parsed — there is only the one parser and one probe
regex, both guarded. (F1 below is the one asymmetry actually found.)

## Probes (gate binary run directly, receipts under ReviewGate/p1..p8/)

- P1 — first-line entry + `hash_mismatch_panic: no` body + mismatch pin, fake
  `Limine 12.9.6-rc1`. `auto` → **rc 64, stdout 0 bytes, no verdict**. Explicit
  `12.9.6` control → `panic` (body key invisible, era B), explicit `12.9.4` control
  → `prompt` (key visible, era A). The gate refuses the suffixed probe instead of
  answering either era. `p1.out/p1b.out/p1a.out`.
- P2 — two-version fake (`Limine 12.9.4` then `Limine 12.9.6`): `auto` reports
  `limine_version 12.9.4`, era pre-12.9.5. Reversed (12.9.6 first): reports 12.9.6,
  era 12.9.5+. **First match wins** (`re.search`), consistent with the docstring's
  "accepts the first X.Y.Z". The battery's `AUTO-PROBE-SHAPES` fake (no-version
  line, then rc1, then stderr copy) never triggers the two-version ambiguity — the
  first line is unparsable so the search falls to the rc1 line and the guard
  refuses; stderr is never read. `p2.out/p2r.out`.
- P3 — ten-digit flag value `1234567890.0.0` under do-nothing gate → **rc 64,
  empty stdout**. Under landed gate → same rc 64. The 1-9 bound predates r94 (the
  r93 gate carries it at `:96`), so the *parser* refusal is not new; what is new is
  the battery family pinning it at family level. And the do-nothing gate under
  `auto` with the rc1 fake answers a **verdict** `12.9.6` / source probe, rc 0 —
  the exact leniency the r94 guard closes. `p3.out/p3b.out/p3c.out`.
- P4 — empty conf (0 bytes), `auto` via fake `12.9.6` → rc 0, HEALTHY, pins [],
  version 12.9.6/probe, era 12.9.5+. No crash, no usage fire. `p4.out`.
- P5 — whitespace-only stdout fake → rc 64, stdout 0 bytes; empty-stdout/exit-0
  variant → same. `p5.out/p5b.out`.
- P6 — flag-free run (no `--limine-version`) with fake 12.9.6 → version 12.9.6,
  source probe, era B, rc 0. **The default is `auto`** — omitting the flag probes.
  `p6.out`.
- P7 — `Limine 12.9.6+build1` via `auto` → **verdict 12.9.6, rc 0** (see F1).
  Flag `12.9.6+build1` → rc 64. `12.9.6_1` probe → rc 64. `p7.out/p7b.out/p7c.out`.
- P8 — flag-free, no fake, host `limine --version` = 12.9.4 → version 12.9.4,
  source probe, rc 0. `p8.out`.

Selftest: `python3 tools/check-limine-pins.py --selftest` → `selftest PASS 39/39`,
rc 0 (re-run by this seat).

## Findings

**F1 (minor).** `probe_limine_version` (`tools/check-limine-pins.py:121`) guards
`\w` and `.` and `-` in the negative lookahead `(?![\w.-])`, but not `+`. A
`+`-suffixed answer (`Limine 12.9.6+build1`) is accepted and resolves to `12.9.6`,
while the same string as a flag value is refused (rc 64) and `12.9.6_1` is
refused everywhere. Asymmetry is between *parse sites of the same text shape*, not
between version sources. This does not falsify the landed claims: every enumerated
r94 refusal is a `-` suffix (`12.9.6-rc1`), a `.` extra component (`12.9.6.1`), or
a stderr/no-version shape — all refused (P1, selftest, P5). No battery row sends a
`+` suffix. Filing as a spec-completeness gap only: "not-word-char suffix guard"
is enforced for `\w`, `.`, `-` and not for `+`.

**F2 (documentation).** Stale `default 12.9.4` statement. The module docstring still
says at line 35 that the version "is selected by `--limine-version` (round 92 V2;
default 12.9.4, the host package)", and `check()`'s signature at `:187` keeps a
literal `12.9.4` default, while the flag default at `:503` is `auto`. The
docstring's own V4 bullet (`:42`) and `:503` agree that `auto` is the default, so
the `:35` line is contradicted within the same module. Functionally inert (no CLI
path reaches the `:187` default; P6/P8 prove flag-free = probe), but a reader
taking `:35` literally would conclude the opposite of the shipped behavior. The
live usage line at `:59` (`sudo check-limine-pins.py --live --limine-version auto`)
is also now redundant-with-default rather than wrong.

**F3 (battery scope note, not a defect).** P3 shows the ten-digit refusal already
existed in the r93 gate. The r94 claim C1's new substance on that axis is the
battery-side `REFUSAL-VERSIONS-10DIGIT` family (four X.Y.Z-shaped values, each one
component exactly ten digits — battery `:1681-1695`) plus the positive control row
(`12.9.4`) inside the same family. The family wiring is correct: `usage_check`
(`:2260-2306`) enumerates the values and requires rc 64 / empty-or-whitespace
stdout per row, with the `12.9.4` row required rc 0; the do-nothing battery grep
for both new family names is 0, the r94 battery carries five hits, and the FAMILIES
dict at `:1849-1850` registers both. Nothing falsified here; noting that the
parser side of REFUSAL-VERSIONS-10DIGIT is the longest-standing refusal in the
gate rather than new code, so a reviewer looking only at the gate diff might
misattribute the novelty.

## Verified not-findings

- `default="auto"` complete: argparse `:503`, help text, `--live` branch `:524`,
  selftest `probe-version` (`:467-475`) — all agree. Selftest 39/39.
- Probe regex is the only place probe text is parsed; `parse_limine_version` is
  the only place flag text is parsed; the guard and the 1-9 bound live in those
  two spots and nowhere else.
- Stale-tree bend (N04) is a genuine decoy: `os.environ.get("LIM_STD_VERSION"…)`
  assigned and never read (`bends/N04-stale-tree.py:108`); the battery's ISOLATION
  sandbox clears the env (`--clearenv` at battery `:1937`), so even a reader could
  not fire. Consistent with the plan's "any family in failed_families" note.
- Two-version first-wins (P2) is documented behavior ("accepts the first X.Y.Z",
  docstring `:44-45`) and no battery row exercises ambiguity.

## Verdict

Evidence supports both claims. C1: the suffixed probe refuses (P1 rc 64 / 0-byte
stdout, no verdict) while AUTO-ERA-B-shaped plain `Limine 12.9.6` reads a verdict
with version and source probe — the exact probe-shape pair from the claim; the
ten-digit family enumerates four X.Y.Z-shaped values with one ten-digit component
plus the 12.9.4 positive control, correctly enforced, and the do-nothing gate
answers a verdict at precisely that gap (P3 rc 0 / 12.9.6). C2: `--limine-version`
defaults to `auto` and the flag-free live-style run probes the installed
`limine --version`, records `limine_version` + `limine_version_source: probe`,
selects era from it, and refuses rc 64 with empty stdout on probe failure (P5,
P6, P8); selftest PASS 39/39. No finding falsifies either claim; F1 (`+` suffix
asymmetry) and F2 (stale `:35` docstring line) fall below the claim thresholds.
