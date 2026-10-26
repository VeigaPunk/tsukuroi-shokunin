VERDICT: defect-found

# C2-9 (QUALITY 87 attack): entries that state the OPPOSITE of the source score 8/8

The frozen C2 counter does not read a rule; it checks that a rule cell contains the right substrings and no
negation word. Eight rules that are affirmatively false, one of them repeated in every row, and a false host
inference all score `PASS exit 0 rules_verified 8`. The ten passing artifacts are in
`.ufo/waves/round-40/w1/C2CritXFalse/` as `<variant>.entry.md` (exact tree), `<variant>.diff` (vs base) and
`<variant>.counter.json` (full counter output); `runs.log` lists every command and observed result.

## What was run

Scratch clone of the lane (`git clone -q --shared … /fast/scratch/hyaku/tsukuroi-r40/C2CritXFalse/fx`, origin
removed, `rev-parse --show-toplevel` = the clone, commits made with the fixture identity
`fixture@shokunin.local`), base `bf2380503b8e4a5d33162026854b0b7b66d18b86`, counter
`python3 tools/check-exec-environment-r40.py --repo <fx> --revision <sha>` (sha256
`d4a2bb94f95184a87c582ddd7c8e55905390642cd4496aaebefa82b10ebb7d9d`, the declared value). Baseline on the
shipped entry: `PASS exit 0, rules_verified 8, counts_ok 2, source_ok 1`. No lane file was written; the clone
was deleted after the receipts above were copied; no tool was installed.

## Passing false entries

| variant | sha (scratch clone) | counter | receipt |
|---|---|---|---|
| EX1 cwd/chroot inverted | `ab13ea78ea8e1322ea238bb29ffefffa15c01b6b` | PASS 8/8 exit 0 | `EX1.diff`, `EX1.counter.json` |
| EX2 streams inverted | `9f0f3faf52091fc295cc2a2dff1dca1e879eb409` | PASS 8/8 exit 0 | `EX2.diff` |
| EX3 SHLVL/BASH_ENV inverted | `e99d3c0c6c21def3d1e02879014e2f5751c466c1` | PASS 8/8 exit 0 | `EX3.diff` |
| EX4 new/old swapped | `5cb98b3c17184b5bad7de6edd279f56413d3bf9b` | PASS 8/8 exit 0 | `EX4.diff` |
| EX5 permanence + shared dir | `2d54985dc000e63c6894789f3028f56a25e0ec6f` | PASS 8/8 exit 0 | `EX5.diff` |
| EX6 order/dedup inverted | `8df6a946d733b80a05d37e0f8e11238cc47a25ea` | PASS 8/8 exit 0 | `EX6.diff` |
| EX7 before/after + abort scope | `4c3594bcf4565df1822cb53c4d7ab71fbfd929a7` | PASS 8/8 exit 0 | `EX7.diff` |
| EX8 NoUpgrade honoured, `.pacnew` name | `b7f4aaffdb73e853bc6f207ceb5a987b3e5c0bc7` | PASS 8/8 exit 0 | `EX8.diff` |
| ALL (all eight at once) | `9516fcd3595e244e8ed409ac73bc2b6f1b713235` | PASS 8/8 exit 0 | `ALL.entry.md` |
| ONESENT (one padding sentence in all 8 rows) | `46700803d57c48a89eacc51c7be25f3731ab9832` | PASS 8/8 exit 0 | `ONESENT.diff` |
| HOST (false host inference) | `5bfe707642376382c76e43ef07e720cf617c4cfe` | PASS 8/8 counts_ok 2 | `HOST.diff` |
| NEGCTL (same EX2 text plus "not") | `e44e87d0152935fa741ce863b209a7f61aa63dbc` | FAIL 7/8, `rule carries negation word 'not'` | `NEGCTL.diff` |

The NEG control is the whole point: the same inversion survives when phrased affirmatively and dies only when
it contains a word from `NEG` (counter:97).

## The eight false rule cells (verbatim) and why each is false

- **EX1** — "Every command libalpm runs through `_alpm_run_chroot` starts in the caller's working directory: the
  child keeps the caller's working directory and chroot, so a hook that opens a relative path resolves it
  against the directory pacman was started in rather than `/`". False: the parent `chdir(handle->root)`
  (util.c:628) and the child then `chdir("/")` (util.c:683).
- **EX2** — "The child's stdout and stderr go to two separate sockets that the parent reads apart, and its
  stdin is a second socket the parent leaves open, so a command reads end-of-file from the terminal only when
  its own input actually ends". False: fd 1 and fd 2 are both `dup2` of `child2parent_pipefd[HEAD]`
  (util.c:665-666, one socket); the child closes the write end of its stdin socket itself
  (`close(parent2child_pipefd[HEAD])`, util.c:669), so stdin is at end-of-file regardless of the parent.
- **EX3** — "…forces `SHLVL` to 1 overriding any inherited value, keeps `BASH_ENV` from the parent so bash
  sources it…". False: `setenv("SHLVL", "1", 0)` keeps an inherited value (util.c:692) and
  `unsetenv("BASH_ENV")` removes it (util.c:694).
- **EX4** — "…so every install scriptlet runs as `/bin/sh -c` … while the upstream build default is the
  `/usr/bin/bash` value…". False: Arch passes `-Dscriptlet-shell=/usr/bin/bash` (PKGBUILD:115) and the meson
  default is `/bin/sh` (meson_options.txt:17).
- **EX5** — "…copies or extracts the scriptlet into the shared directory `tmp/alpm_XXXXXX` … and leaves both
  the file and its directory in place for later transactions…". False: `mkdtemp` makes a unique directory
  (trans.c:368) and both are removed (trans.c:413 `unlink`, :417 `rmdir`).
- **EX6** — "…on stdin sorted by the order in which its triggers matched, with duplicate matches from several
  triggers preserved…; a hook lacking `NeedsTargets` reads the same sorted and de-duplicated list as well".
  False: `alpm_list_msort(… strcmp)` (hook.c:521), `_alpm_strlist_dedup` (hook.c:524), and a hook without
  `NeedsTargets` is run with a NULL input callback (util.c runs with closed stdin).
- **EX7** — "The `running '<name>'...` line is written only after the hook's `Depends` resolve … and the
  `satisfy dependencies` failure … aborts the PreTransaction phase for every hook in a file that also carries
  one AbortOnFail hook". False: the line is logged at hook.c:653 before `_alpm_hook_run_hook` at :660, and the
  abort is `hook->abort_on_fail` only (hook.c:660, :667).
- **EX8** — "…matches the absolute path the file has on disk after the transaction; … NoExtract excludes still
  matches the file list, and NoUpgrade applies, so a protected file written as `.pacnew` matches under the
  `.pacnew` name". False: matching is against `filelist.files[f].name` (hook.c:271), `hook.c` contains no
  `noupgrade` at all (`grep -c noupgrade hook.c` → 0), so NoUpgrade cannot be honoured.

## The four separable defects

**D1 — polarity is a word list.** counter:17-19 promises "an entry that states the opposite of the source by
negating it fails". The check is `NEG.search(rule)` (counter:97, :287-289). Every one of the eight cells above
states the opposite and contains none of `not|never|no|none|nothing|without|instead|unless|cannot|neither|nor`.
Eight independent inversions, plus all eight combined, exit 0. Refusing these requires replacing the
`polarity` conjunct, not extending `NEG` — the paraphrase space (two separate sockets / forcing SHLVL /
leaves in place / applies) is unbounded.

**D2 — credit is token presence, not proposition.** counter:15-16 credits "every frozen proposition token";
counter:282-286 and :290-292 add only ≥12 words. `ONESENT` puts one 47-word padding sentence — "…are frozen
tokens this cell repeats; the twelve-word minimum is met by this padding sentence alone" — in all eight rule
cells and scores 8/8 with no repeated-heading or duplicate-row complaint (row ids still differ). QUALITY 87's
"rule READ" credit is therefore satisfied by a cell that asserts nothing; the conjunct to change is the same
`polarity` one plus the `tokens`/word-count credit, which must become a comparison against a derived claim.

**D3 — rule and value may contradict each other.** The `value` cell is exact-derived (counter:280) but never
compared to the rule cell. In `ALL.entry.md` EX2 the rule says "two separate sockets" while the value cell on
the same line says `stdout+stderr: one socket; stdin: second socket`; EX7's rule says "only after" while the
value is the message `could not satisfy dependencies`. Any table a reader sees is self-contradictory and the
counter is silent.

**D4 — host cells are substring-checked.** `counts_ok` (counter:322-326) tests only for
`"<N> of <M> effective hook files"` and the presence of `/usr/bin/bash` and `libalpm.so.16.0.1`. `HOST.diff`
appends "14 of 69 effective hook files carry `NeedsTargets`, so most hooks read targets on stdin" (14 of 69 is
20%; `frozen/hostcap/hooks-needstargets.tsv` counts 14 ones and 55 zeros) and "`/usr/lib/libalpm.so.16.0.1`
lists `/usr/bin/bash` only as a fallback, so the effective scriptlet shell is `/bin/sh`"
(`frozen/hostcap/libalpm-shell-strings.txt:2` is the single line `1277:/usr/bin/bash`). Both PASS with
`counts_ok 2`.

**D5 — the counter penalises accurate quoting.** The real message is `could not satisfy dependencies`; the
`NEG` regex matches `not` inside it, and `NEG` is applied to the rule cell only (counter:287) while the value
cell is exempt. A rule cell that quotes the message verbatim, i.e. the most faithful possible EX7 rule,
fails: variant `CLAIM` → `FAIL exit 1, rules_verified 7, EX7: rule carries negation word 'not'`
(`CLAIM.frozen.counter.json`). The counter therefore rewards the paraphrase that D1 exploits and punishes the
source's own wording.

## Which conjunct must change (demonstrated)

A private copy of the counter (`check-exec-environment-r40.claimpatch.py` in the receipt dir,
`claimpatch.diff` for the exact hunks; frozen snapshots reached through a symlink to the lane's
`.ufo/waves/round-40/frozen/`) replaces the polarity/word-count block with exact equality against a claim the
counter itself composes from the same source patterns:

```python
            rc = collapse(rule)
            if rc != collapse(CLAIMS[ex]):
                r['reasons'].append('rule cell differs from the counter-derived claim for ' + ex)
```

with `CLAIMS` built in `derive_values` (EX2, for example: "the child duplicates fd 1 and fd 2 from the same
child-to-parent socket so stdout and stderr arrive merged, and fd 0 from a second socket the parent closes at
once, so stdin reads end-of-file"). Observed:

- `ALL`, `JUNK`, `ONESENT`, `EX2`-false, `NEGCTL` → FAIL `rules_verified 0` (refused);
- `CLAIM` (rule cells replaced by the derived sentences, sha `296f427e08da8261486f2bfc2ff1ed7f5e2af0cc`) → PASS `rules_verified 8` (the correction is
  satisfiable);
- the shipped entry (`bf23805`) → FAIL `rules_verified 0`: the prose rule column no longer earns credit and
  must be replaced by the derived sentences, with the explanation moving to the summary section that carries
  no credit. That cost is the honest consequence of removing prose from the credited path; no cheaper
  conjunct refuses D1/D2, because any check that reads prose by substring can be satisfied by adding the
  required substring next to the false statement.
- `CLAIMHOST` (derived claim cells plus the false host inference, sha `246117570654b300f1fc8e653becdd8f1fe6ff24`) → patched counter PASS `rules_verified 8,
  counts_ok 2`, so the host hole (D4) survives the rule fix: `counts_ok` must likewise become equality with a
  counter-composed host sentence ("{N} of {M} effective hook files carry `NeedsTargets`";
  "`/usr/lib/libalpm.so.16.0.1` carries `/usr/bin/bash` at strings index 1277").

Residual limit of the proposal, stated plainly: exact claim equality constrains only the credited columns.
Falsehood can still live in uncredited prose (the summary list, the host column before D4 is fixed), and the
counter cannot detect contradictions between credited cells and surrounding prose — that is a review
obligation, not a counter conjunct. It cannot, however, be satisfied by a false rule cell, which is what C2
currently claims to check.

## Impacted axes

- **C2 depth (the judged axis).** The declared reading of the counter — value derived, "tokens", "polarity",
  "paraphrase", "source" (counter:13-24) — does not include any check on what the rule cell asserts. The C2
  score of 8/8 measures token coverage of eight rows; the same 8/8 is reachable by eight inverted rules, by
  one repeated padding sentence, or by a false host inference. Any C2 depth number for this entry should be
  read as "the source cells and value cells are correct", which is what round 39 already credited.
- **QUALITY 87 (READ).** Falsified as implemented: an entry whose rule cells state the opposite, or nothing,
  is credited as read.
- **R39-CONTENT-UNREAD (round-39 routed defect).** Only partly closed: it is closed for rules written with a
  negation word and open for rules written affirmatively.
- **Not impacted:** `source_ok`, `duplicate_rows`, `duplicate_headings`, `novelty_base_hits`. All variants keep
  the shipped source cells (S221/S220/S222/S223/S224) and provenance intact; my attack changes only the
  rule/host cells, so this is a rule-credit defect, not a provenance or registry one. The EX rows also remain
  distinct in id, so the duplicate-row guard never sees `ONESENT`.

## Smallest safe correction

1. `polarity` → `claim`: the rule cell must equal, after `collapse`, a sentence the counter composes from the
   source patterns that already produce `value` (the `CLAIMS` table above; eight sentences, ≥12 words each,
   carrying the tokens so the `tokens` check stays as a cheap invariant). Nothing else in the predicate needs
   to change, and the entry's rule column becomes counter-authored.
2. `counts_ok` → exact host sentence equality with the capture-derived values (14/69, index 1277), not
   substring presence.
3. Keep the `NEG` lint only after (1): as written it also rejects the source's own message, so it must not be
   the polarity test, and the message must be quotable in the rule cell.

## Not done

I did not touch the lane, `corpus/SOURCES.md`, the frozen counters or the host; no package, service, mount or
`/etc` change; no network; no sudo. I did not run the C1 census selftest (C1-9's lane), the harness
`run-receipt.py`, or any check of the SCORECARD text itself — the declaration sentences quoted here come from
the counter docstring (counter:13-24), which is what the counter enforces. Variant commits existed only in the
deleted scratch clone; their exact trees survive as `<variant>.entry.md` + `<variant>.diff` receipts, so the
shas in `summary.json` are historical labels, not resolvable objects.
