VERDICT: draft

# F-5 — appended SKILL.md sections: (a) census identity round 46, (b) routed defect D1 status note

Seat: ScribeSkill (round-46 w1, leaf). Item: draft appended `SKILL.md` sections in the register of
`SKILL.md:4232` "Census first-line readers — round 45". Nothing was edited: this file and the receipts under
`.ufo/waves/round-46/w1/ScribeSkill/` are the only writes. No counter was run by me; the C1 counter and the census
selftest were left to the seats that own them (cost rule), and the two figures I take from committed pre-data controls
are labelled as such.

## Draft (a) — exact Markdown, to append at the end of `SKILL.md`

Append after the last line of `SKILL.md` (4424 lines today, ends `| tsukuroi |` + newline), as a new section:

```markdown

## Census identity — round 46

Appended 2026-10-27 (round-46 C1; drafted by wave seat ScribeSkill, integrated by the L1). Base `2042117c`;
implementation `a4477049` — `--identity` plus six `(R46-C1)` selftest cases (154 → 160), census sha256
`d925839cde9737fbd624ad2302671671c7ecc4e9a9331a1ff5a2ad1839112cfa`, md5 `db08a606ce128da3839457372e91e220`,
209208 bytes, 3598 newline bytes. Entry `corpus/knowledge/census-identity-r46.md`; evidence `.ufo/waves/round-46/`
(`before/`, `controls/`, `w1/`).

Surface: `bash tools/tsukuroi-census.sh --identity` prints one `TSUKUROI_CENSUS_IDENTITY:` line and exits 0 before any
plane probe (`:3513-3518`), so a reader names the census revision with one command instead of three (routed debt D12,
`corpus/knowledge/closeout-r11.md:42-44`). The `VERSION` string is still the literal `census-v2` and names nothing:
identity is the sha256.

| Observation | Reading | Action |
|---|---|---|
| `sha256=<64 hex> md5=<32 hex> bytes=<n> lines=<n> verified=yes`, and the four values equal `sha256sum`, `md5sum`, `wc -c` and `wc -l` of the invoked file (`a4477049`: `d925839c…`, `db08a606…`, `209208`, `3598`) | the descriptor bash holds on the script (`/proc/$$/fd/<n>`, normally 255, scanned from 10 up) resolves to `readlink -f` of the invoked path, and both sha256 reads agree (`:3466-3491`) | trust the four fields only with `verified=yes`; `lines` counts newline bytes, so it is one less than an editor's line count — the file ends without a newline |
| `sha256=unverifiable md5=unverifiable bytes=unverifiable lines=unverifiable verified=no` | no descriptor resolves to the invoked file: the script came from stdin (`bash -s -- --identity < tools/tsukuroi-census.sh`) or a pipe (`bash <(cat tools/tsukuroi-census.sh) --identity`), was replaced after bash opened it, or the descriptor limit put it below 10 | an unknown, never a guess — a decoy regular file named `bash` in the working directory is not hashed; ask a privileged reader for the digests |
| `tsukuroi-census: --identity takes no other argument` on stderr, exit 2 | `--identity --selftest`, `--identity --sample 3` and any other parsed option reach the single-argument check (`:3513-3515`) | a usage error, not a reading |
| `--identity --help` prints the usage on **stdout** and exits **0**, with no identity line | `--help`/`-h` exits inside the argument loop (`:3508`), before the single-argument check, so the "takes no other argument (exit 2)" rule does not cover it | do not read a usage dump as an identity answer: check the first token, not only the exit code (routed as a round-46 C1 defect below) |
| the sha256 from the line, fed to the `git log` loop at `corpus/knowledge/census-identity-r46.md` §"Re-deriving the revision from the line", prints `a4477049…` and nothing older | the line names bytes, not a commit; the first hash printed is the newest commit carrying those bytes, and no output means an uncommitted local edit | re-derive the revision before quoting a census verdict |

Counter: `python3 tools/score-census-identity-r46.py --revision <REV> --scratch <DIR> [--lane <repo>]` (sha256
`7c406eb5f4ba1f6265649f7102e7376882483180c161a66abc68e08cad9524ba`) — PASS iff `identity_ok == 1 and tracks_ok == 1
and symlink_ok == 1 and unverifiable_ok == 1 and cli_ok == 1 and nowrite_ok == 1 and selftest_pass == 1 and
selftest_r46 >= 4`. Legs: the line against the counter's own digests over the census bytes of `REV` (`identity_ok`);
one appended comment line must move all four fields (`tracks_ok`); a symlink prints the target's values
(`symlink_ok`); stdin, process substitution and replace-after-open print `unverifiable`/`verified=no`
(`unverifiable_ok`); the CLI arms (`cli_ok`); the identity runs leave cwd and TMPDIR byte-unchanged (`nowrite_ok`);
the census selftest PASSes carrying at least four `(R46-C1)` labels. Pre-data controls
`.ufo/waves/round-46/controls/`: `battery-summary-c1.jsonl` 9/9 as declared — K0 (base) and K1, K2, K3, K5, K6, K7,
K9 FAIL, K8 (candidate) PASS; base selftest `PASS (154 cases, …)`, candidate `PASS (160 cases, 160 passed, 0 failed)`
with `selftest_r46` 6 (`C1-K0-donothing.jsonl`, `C1-K8-candidate.jsonl`). The scored outcome of the counter at
`a4477049` is the receipt under `.ufo/waves/round-46/`, not this section.

Recorded limits: bash behaviour is pinned at tag bash-5.3 (`shell.c:1586,1700,1703`, `general.c:690-700`,
`general.h:252`) and the host runs 5.3.20 — whether patches 1-20 touch `open_shell_script` or `move_to_high_fd` is
not read here [inference: the selftest's descriptor and stdin cases pass on the host bash, consistent with the pinned
lines]; the identity names the bytes at the descriptor when the line is printed, and bash reads a script in pieces, so
an in-place edit during a run can differ from what executed — the second sha256 read only narrows that window; the
counter's legs run drawn copies under `--scratch` on this host's bash, and `nowrite_ok` compares cwd and TMPDIR bytes,
not syscalls; `--identity --help` exiting 0 lies outside the counter's `cli_ok` arms and outside the claim as declared.
```

## Draft (b) — exact Markdown, routed defect D1, to append at the end of `SKILL.md`

The old rows are not edited: `SKILL.md:4214-4231` stays byte-identical, and this block is appended after draft (a)
(or after it in either order — both are pure appends). Placement at EOF is forced by the appended-notice gate, whose
append boundary is the fixed R18 baseline `842a5312`: any insertion before the file's end breaks
`target_bytes.startswith(base_bytes)` (`tools/check-appended-notices.py:231`, again at `:268`). Receipt: the fixture run in
`gate-experiment.txt` §2 shows the notice as `11 0 SKILL.md` added/deleted lines.

```markdown

## Scrub record — round 44 status note (routed defect D1; appended 2026-10-27)

Appended; `SKILL.md:4214` "Scrub record — round 44 rows" and its Limits block stay as written and no row above gains
or loses a word. The mark that section lacks is this: Round 44's depth gate FAILED — `verdicts_ok 0` — at
`tools/check-scrub-record-r44.py --revision fbfef071` (`FAIL`: `.ufo/waves/round-44/after/c2-final-fbfef071.jsonl`,
`corpus/lessons/round-44-verifier-spotcheck.md:84,133,185-186`), so SR7, SR8 and SR9 stay **pending**, not admitted:
read them as source-checked statements that no counted seat has bound. Round 46 C2 admits them only against bound
counted verdicts (`tools/check-scrub-admission-r46.py`: `r45_legs_ok == 1 and verdicts_ok == 3 and marks_ok == 3`);
a PASS there needs the three counted seats, not a rewritten row. Capture: `.ufo/waves/round-46/l1-capture/scribe-d1.txt:1`
— the counter's own line, `verdicts_ok 0`.
```

### Appended-notice shape this draft satisfies (and the one field it cannot honestly carry)

The gate `tools/check-appended-notices.py` (`--help`: `--revision REV`, `--branch`, `--registry`, `--registry-from`)
checks one registry record per notice, eight fields exactly (`id`, `path`, `baseline_quote`, `reason`, `now`,
`capture_ref`, `capture_quote`, `notice_heading`; `:29-30`, enforced at `:351-355`), schema
`tsukuroi-appended-notices-v1` with baseline `842a5312b704b5cda10fd80ec1fdee5fb381ba97` (`:25-26`), and for each
record: target bytes start with baseline bytes,
`baseline_quote` occurs in the baseline and in the target, the heading occurs exactly once in the target and never in
the baseline, the notice section contains the `now` and `capture_ref` strings, and `capture_quote` is an exact
substring of the cited line of a committed `.ufo/waves/round-<N>/l1-capture/<name>` file (`:209-300`).

The draft above is shaped for that record — one ATX heading line, the `now` sentence verbatim
`Round 44's depth gate FAILED — \`verdicts_ok 0\``, and a `capture_ref` line verbatim
`.ufo/waves/round-46/l1-capture/scribe-d1.txt:1` whose committed line 1 contains `verdicts_ok 0`. What it cannot
carry is a *subject* `baseline_quote`: the gate's baseline is the fixed R18 commit, and `git show 842a5312:SKILL.md`
has no occurrence of "scrub" (0 hits), so no round-44 sentence exists at the baseline. Measured both ways on a
fixture clone (`gate-experiment.txt` §3-§4):

- `baseline_quote` = `A device carries a scrub context only inside the run's attached window` (the SR7 row) →
  `status FAIL`, finding `NOTICE-QUOTE-BASELINE`, "baseline_quote is not an exact baseline substring".
- the same notice and capture with `baseline_quote` = `Secrets never read` (an R18-era SKILL line) → `status PASS`,
  `resolved_records 1`.

So registering this notice would require quoting an unrelated R18 line; the round-45 D2 correction block at
`SKILL.md:4329-4346` is likewise unregistered (the live gate at `2042117c` and `a4477049`: PASS, `record_count` 97,
all `R18-*` ids). Recommendation: append the notice unregistered, as D2 did, and let this paragraph record the gate's
R18-baseline limit; if the L1 prefers a record anyway, add
`corpus/knowledge/appended-notices-r46.json` (schema and baseline as above; `id` `R18-CORR-<NN>`; `path` `SKILL.md`;
`notice_heading` exactly `## Scrub record — round 44 status note (routed defect D1; appended 2026-10-27)`;
`now` and `capture_ref` as in the draft; `capture_quote` `verdicts_ok 0`) and choose its `baseline_quote` knowingly.

The capture file to commit (2 lines; the notice cites line 1): `.ufo/waves/round-46/l1-capture/scribe-d1.txt`, copied
verbatim from `.ufo/waves/round-46/w1/ScribeSkill/capture-d1.txt`.

## Evidence actually observed (never re-run to decorate)

- Identity line at `a4477049` (lane file clean): `bash tools/tsukuroi-census.sh --identity` →
  `TSUKUROI_CENSUS_IDENTITY: version=census-v2 sha256=d925839c… md5=db08a606… bytes=209208 lines=3598 planes=packages,systemd,drivers,journal,update-safety,oom exit_map=0:HEALTHY,1:DEGRADED,2:BLOCKED verified=yes`,
  exit 0. Cross-checked against `sha256sum`/`md5sum`/`wc -c`/`wc -l` of the same file, and `tail -c 1` = `"` (no
  trailing newline). Receipt `capture-identity.txt`.
- Unverifiable forms, both observed: `bash -s -- --identity < tools/tsukuroi-census.sh` and
  `bash <(cat tools/tsukuroi-census.sh) --identity` each print the line with all four fields `unverifiable` and
  `verified=no`, exit 0 (same receipt).
- CLI arms: `--identity --selftest` exit 2 with `--identity takes no other argument`; `--identity --help` exit 0 with
  usage on stdout, empty stderr, no identity line — the deviation recorded in the draft's fourth table row and below.
- `check-scrub-record-r44.py --revision fbfef071` run by me: exit **1**, `verdict FAIL`, `verdicts_ok 0`, `rows 3`,
  `quotes_ok 3`, `props_ok 3`, `host_ok 3`, `sources_ok 1`, `pointer_ok 1`, `novelty_base_hits 0`. The committed
  receipt it names exists: `.ufo/waves/round-44/after/c2-final-fbfef071.jsonl`.
- Round-44 lesson lines relied on: `corpus/lessons/round-44-verifier-spotcheck.md:84` (the same values, verdict FAIL),
  `:133` (depth unchanged, `verdicts_ok 0`), `:185-186` (SKILL.md:4214 presents SR7-SR9 with no FAILED/pending mark).
  `grep -n -i 'fail|pending'` over `SKILL.md:4214-4231` → no match (receipt `capture-d1.txt` line 2).
- `check-scrub-admission-r46.py` predicate confirmed in source: `:40` and `PREDICATE` at `:71` =
  `r45_legs_ok == 1 and verdicts_ok == 3 and marks_ok == 3`; sha256 `28c409be…11d8`.
- Counter confirmation: `score-census-identity-r46.py` legs at `:14-36`, predicate at `:38-39` and `:66-67`; sha256
  `7c406eb5…54ba`. Census selftest counts 154 → 160 and `selftest_r46` 6 come from the committed pre-data controls
  `controls/C1-K0-donothing.jsonl` and `controls/C1-K8-candidate.jsonl` — not from a run of mine.
- Gate runs on the live lane (read-only): `check-appended-notices.py --revision 2042117c` and `--revision a4477049`
  both `PASS`, `record_count 97`, `resolved_records 97`, `findings []`.
- `SKILL.md` prefix check: bytes at `842a5312` (168208) are a prefix of today's `SKILL.md` (846662).

## Findings

- **C1-D1 (defect, contract wording).** `SKILL.md`'s (and the declaration's) rule "`--identity` takes no other
  argument (exit 2)" does not hold for `--help`: `bash tools/tsukuroi-census.sh --identity --help` exits **0**,
  prints the usage on stdout and no identity line, because `--help|-)` exits inside the argument loop
  (`tools/tsukuroi-census.sh:3508`) before the `nargs -ne 1` check (`:3513-3515`). The counter's `cli_ok` arms do not
  cover this pair (`score-census-identity-r46.py:14-36`), so a PASS there does not establish the sentence as
  written. Either narrow the sentence (as draft (a) does) or fix the census; the draft states only what was observed.
- **F2 (limit, not a defect).** The appended-notice gate cannot bind a post-R18 subject at all: fixed baseline
  `842a5312` with no "scrub" text, demonstrated by case A/B above. Draft (b) is therefore registry-shaped but
  recommended unregistered, mirroring D2.
- **F3 (consistency check, clean).** `SKILL.md` today is a byte-prefix of the R18 baseline and D1's target range
  contains no `fail`/`pending` word, so appending the draft creates exactly the missing mark and changes no old row.

## Out of scope / not done

- `corpus/README.md:434` and its paragraph `:440-452`, the other half of D1 (`corpus/lessons/round-45-verifier-spotcheck.md:184-190`),
  were not drafted (item asks for SKILL.md only).
- I did not run `score-census-identity-r46.py` (needs the census selftest, ~45 s and 6 CPUs, owned by the C1 seats) or
  the census selftest; no counter verdict at `a4477049` is claimed here.
- No tool was installed or upgraded (nothing needed; no pacman transaction).
- Scratch `/fast/scratch/hyaku/tsukuroi-r46/ScribeSkill` held only the fixture clone and was removed after the receipts
  were copied; no `/tmp` path is evidence anywhere above.

## Receipts

- `.ufo/waves/round-46/w1/ScribeSkill/capture-identity.txt` — the identity run, digests, lookup-loop output, counter digests.
- `.ufo/waves/round-46/w1/ScribeSkill/capture-d1.txt` — the two capture lines to commit as
  `.ufo/waves/round-46/l1-capture/scribe-d1.txt`.
- `.ufo/waves/round-46/w1/ScribeSkill/gate-experiment.txt` — fixture clone, append diffstat, case A FAIL, case B PASS,
  live gate runs.
