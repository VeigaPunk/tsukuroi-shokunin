# RevQuality7779 — review of corpus/QUALITY.md criteria 77-79 at 29bf87fa3971df04cb96e4ad9a28805d8154ed2f

Verdict: criteria 77 and 78 hold; criterion 79 fails — its rule body describes counter v1
(sha256 1bf7ee14..., at 8fb2cef0), not the committed v2 (sha256 4953203d...), and its cited
battery denominators (46 should-fail, 6 should-pass) are v1's; the committed battery v2 has 72
should-fail and 11 should-pass shapes, so the admission test as written cannot be evaluated
against the committed battery.

Reviewed against the style of criteria 60-76 (single numbered bolded rule with R-tag, rule
text, "Falsified by"/"Failing input" examples, lesson pointer; 77-79 are single long lines
like 73-75 — style conforms [obs]).

## Findings

1. **Criterion 77 (R30-UNRECEIPTED-GATES) — HOLDS.** [obs]
   - Named tool exists and does what the criterion states: `tools/check-report-receipts.py`
     (sha256 0a435346...) prints one JSON line per cited (revision, tool) pair with
     `receipted`/`receipt`, a `{"cited": N, "unreceipted": M}` summary, exits 1 when any pair
     is unreceipted (`main` line 446), and has fixture selftests (`selftest()` passes: exit 0).
   - The named failing input actually fails. Command:
     `python3 tools/check-report-receipts.py --report /home/vgpnk/Projects/shokunin/.ufo/reports/round-29/tsukuroi.md --lane <clone> --revision 8976ca92ec3c2e6a2aef07b7065a24ff84a1291b`
     → `{"cited": 25, "unreceipted": 25}`, exit 1 (run in a scratch clone; the 25 include the
     "Gates at `434a7903`" table tools and the `06e00daf`/`81a061a6`/`409ceed4`/`75257ea6` rows).
   - The criterion's own evidence is verbatim-accurate: "Gates at `434a7903` (the last content
     revision), run by the L1:" is at
     /home/vgpnk/Projects/shokunin/.ufo/reports/round-29/tsukuroi.md:60 with the gate table at
     :62-71; `git grep -l 434a7903 8976ca9 -- .ufo/waves/round-29` exits 1 in the clone;
     corpus/lessons/round-29-verifier-spotcheck.md:26-29 records exactly this defect;
     "Gates at `ca6b1499`" is at /home/vgpnk/Projects/shokunin/.ufo/reports/round-28/tsukuroi.md:35
     and corpus/lessons/round-28-verifier-spotcheck.md:45 says "No committed battery receipt
     measures the tip counter." [obs]
   - Receipt format matches run-receipt.py: header `{"receipt":1,"revision","tool_revision",
     "tool","tool_sha256","argv","started_utc"}`, footer `{"receipt_end":1,"exit_code",...}`
     (tools/run-receipt.py:13-16), executed in a sandbox clone detached at the tool revision
     (:6-10). [obs]
   - Minor note [inf]: the criterion writes `.ufo/waves/round-<N>/` without saying whether N
     must be the report's own round; the checker accepts any `round-<n>` directory
     (`receipt_path_matches`, :293-304), and at tip the round-29 pairs are receipted only by
     round-30 wave-1 receipts (run at tip: `{"cited":25,"unreceipted":0}`, exit 0). Harmless
     because revision-scoping makes the distinction moot — a receipt cannot name a revision
     that predates it. Optional fix: spell out "any committed round directory".

2. **Criterion 78 (R30-GIT-RESIDUAL-CHANNELS) — HOLDS.** [obs]
   - S162/S163 cited verbatim lines verified against the committed snapshots:
     `.ufo/waves/round-30/w1/ScribeSrcGitCore/S162-core.adoc` line 492 reads
     `Defaults to `$XDG_CONFIG_HOME/git/ignore`.` under `core.excludesFile::` (:488-494;
     snapshot sha256 aa601522... recorded verbatim in SOURCES.md S162 row :168).
     `.ufo/waves/round-30/w1/ScribeSrcGitEnv/S163-git.adoc` has `GIT_CEILING_DIRECTORIES` at
     :555-568 and `GIT_CONFIG_GLOBAL` at :765-773 (snapshot sha256 050c5330... recorded in the
     S163 row :169). The criterion's parenthetical citations match the SOURCES row anchors
     exactly. [obs]
   - The contract text matches the landed implementation: `git_env()` in
     tools/check-adjacency-overlap.py:75-89 drops every `GIT_*`, sets
     `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM`=`os.devnull`,
     `HOME=<tmp>/home`, `XDG_CONFIG_HOME=HOME+'/.config'`, `PATH=/usr/bin:/bin`,
     `GIT_CEILING_DIRECTORIES=dirname(tmp)`. Commit identity passed via
     `-c user.name=… -c user.email=…` in mutants-owed-statements-r29.py:63,
     mutants-kernel-taint.py:91-92, check-self-assessment.py:1023. [obs]
   - The probe mechanics match its docstring and the criterion: 11 frozen targets × 3 channels,
     leak = canary log non-empty / canary fingerprint changed / exit code differs from control;
     failed control = `harness_error` (tools/probe-git-env-residual-r30.py:19-41; probe sha256
     c8f61996..., unchanged since 8fb2cef0). [obs]
   - Named failing input is real: the committed receipt
     `.ufo/waves/round-30/measure/c2-before-8fb2cef081787ccb52b38e9f74d95d2a480de18f.jsonl`
     summary (line 33 of 34) reads `pairs 30`, `leaking 17`,
     `harness_errors ["tools/check-self-assessment.py"]`, with check-adjacency-overlap leaking
     under path-wrapper and user-files, mutants-owed-statements-r29-landed.py under
     path-wrapper, and the self-assessment harness_error row (`control_rc 2`) at line 26;
     footer exit_code 2. Every element the criterion names is in that receipt. [obs]
   - Minor note [inf]: the criterion says identity is passed "through `-c user.name=…` or
     `GIT_AUTHOR_*`/`GIT_COMMITTER_*`"; mutants-kernel-taint.py:101-102 instead runs
     repo-local `git config user.email/user.name` inside its sandbox — same effect, not one of
     the two literal mechanisms. The probe shows no leak, so the contract is met in substance;
     an uncharitable reader could dispute the mechanism list. Optional fix: add "or a repo-local
     `git config user.*` inside the sandbox".

3. **Criterion 79 (R30-SOURCED-ROWS) — FAILS: it describes counter v1 and v1 battery sizes.**
   - [obs] The criterion's rule text matches v1 (bytes at 8fb2cef0, sha256 1bf7ee14...) and not
     v2 (tip, sha256 4953203d...). Concrete divergences:
     * "HTML tags are removed and entities unescaped" unconditionally — v1 R6 does this for all
       snapshots; v2 R6 applies tag stripping/entity unescaping ONLY to `.html`/`.htm`
       snapshots, all others match verbatim after whitespace collapse. The criterion states a
       rule v2 does not have.
     * "contains one of the question's frozen tokens case-insensitively" — v1 R7 substring;
       v2 R7 requires whole word (not preceded/followed by letter or digit). Underdescribed.
     * "whose `capture_line` contains `value` verbatim" — v1 R8 verbatim substring; v2 R8
       requires value as a whole number plus the FROZEN capture key
       (`CAPTURE_KEYS` D08/D09/D10) on the capture line and no two host rows sharing a capture
       line. Underdescribed.
     * Omits v2 rules entirely: R1 every `rows` element an object with id within D01-D10; R2
       `line`/`capture_line` integers and other values strings; R4 the contiguous 11-column
       registry-table restriction; R5 no-symlink + normalized path; R6 `line` non-blank and
       min(20,len(quote)) chars on the cited line; R9 the full "visible" definition (fence ≤3
       indent, backtick-info-string rule, code spans ignored for `<!--`, raw
       `<pre>/<script>/<style>/<textarea>` blocks, inside a pipe-table block).
   - [obs] The admission clause "the committed battery's control at 10 accepting 0 of 46
     should-fail shapes and refusing 0 of 6 should-pass shapes" cites v1 battery sizes; the
     committed battery (sha256 6d4e5a0a...) contains 72 `F##` and 11 `P##` shapes
     (`grep -oE "\('(F|P)[0-9]+" | sort -u` → 72 / 11) and its docstring says v2 adds F47-F72
     and P07-P11. At tip the literal test cannot evaluate: the committed battery yields
     should_fail_total 72 / should_pass_total 11, never 46 / 6.
   - [obs] The failing examples are still real shapes in the committed v2 battery:
     list-prefixed marker = F32, indented marker = F31 (4-space), quote off cited line =
     F14/F17; the `tools/mutants-btrfs-space-r30.py:10-13` citation covers these shape classes;
     the SCORECARD.md:1149 citation lands on the declaration's battery paragraph (whose own
     46/6 counts are the v1 declaration numbers, not a defect there since they describe what
     was committed in the declaration).
   - Exact fix options:
     a) If the criterion intends to police the declared (judged) artifacts: name the pinned
        bytes — "the declared counter v1 (sha256 1bf7ee14… at 8fb2cef0) and the battery as
        committed in the declaration (46 should-fail, 6 should-pass)" — so the rule is
        self-consistent, and keep the v1 rule body.
     b) If the criterion intends the committed artifacts: rewrite the rule body to v2 R1-R9
        (registry-table restriction, whole-word token, `.html`-only tag stripping, whole-number
        value + capture key + unique capture line, integer types, normalized non-symlink
        snapshot path, non-blank cited line with ≥min(20,len) chars on it, v2 "visible" marker
        definition) and change the admission numbers to "accepting 0 of 72 should-fail shapes
        and refusing 0 of 11 should-pass shapes".

Residual risk / gaps: criteria 77 and 78 verified end-to-end including actual tool runs at
8976ca9 and the committed receipts. For 79 I verified docstring rules and shape inventory
statically plus the receipts in .ufo/waves/round-30/measure/after-a3f19372 were not re-run by
me; [unk] whether the criterion's authors intended v1 as the normative referent — under (a) the
fix is a one-clause pinning, under (b) a rewrite; either way the current text conflates v1
rules with a "committed battery" label that resolves to v2.

Scope: read=lane clone at 29bf87f (tools, QUALITY, SOURCES, SCORECARD, lessons, receipts, reports); wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevQuality7779.md; executed=git clone/checkout/grep/show/ls-tree/rev-parse in /fast/scratch/hyaku/tsukuroi-r30/RevQuality7779/repo, python3 tools/check-report-receipts.py (--report round-29 tsukuroi.md --revision 29bf87f… exit 0; --revision 8976ca9… exit 1; --selftest exit 0), sed/grep/sha256sum/wc
Model: devin/swe-2
Installs: none
