MEETS the C1 after-value: pacnew-log-without-backreference matches=24/of=24, harness_errors=[], exit=0. This is a counter gap.

1. [obs] The mutant that replaces the installed-as target backreference with .* survived. It still requires the ALPM warning prefix and the .pacnew end suffix, but no longer requires the source and target names to pair. Its committed revision is c21cff93244a90f99b0d22bdc20a8ffca7133fc8. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/pacnew-log-without-backreference.jsonl:2-28; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/pacnew-log-without-backreference.mutation.patch:1.

2. [obs] The reference baseline first passed 24/24, harness_errors=[], exit=0. I copied the supplied arm into a subshell function and called it before the census rollup, ignoring its original exit 1 so that the pre-existing rollup remained in charge. All fourteen mutants are separate one-change commits whose parent is the reference commit 5e91daae65bd21fe8f0b3fe43e6139858c93dfa1; only tools/tsukuroi-census.sh was staged and committed. Each distinct variant was scored once. One additional receipt reran the unchanged reference after restoration, as required by the mutation-tester restoration contract; it is not a new variant commit and also passed 24/24. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/base-reference.patch:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/base-reference.jsonl:27-28; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/restored-reference.jsonl:27-28; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/commands.json:1.

3. [obs] Thirteen mutants were killed, one survived, and none was inconclusive. Killed means the mutant failed the 24/24 after-value with no harness errors, while both pristine-reference and restored-reference measurements passed. Every row below has harness_errors=[]; exit is the counter summary exit_code and agrees with its receipt footer and runner return code. The eight +1 changes alter only the named printf argument. Evidence for each row is its named receipt at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/<run>.jsonl:27-28.

| Mutant/run | matches/of | exit | killed yes/no |
|---|---:|---:|---|
| base-reference | 24/24 | 0 | n/a (reference) |
| pacnew-plus-one | 0/24 | 1 | yes |
| pacsave-plus-one | 0/24 | 1 | yes |
| pacorig-plus-one | 0/24 | 1 | yes |
| unreadable-plus-one | 0/24 | 1 | yes |
| log-pacnew-plus-one | 0/24 | 1 | yes |
| log-pacsave-plus-one | 0/24 | 1 | yes |
| unlogged-plus-one | 0/24 | 1 | yes |
| gone-plus-one | 0/24 | 1 | yes |
| duplicate-drift-line | 0/24 | 1 | yes |
| drop-gone-field | 0/24 | 1 | yes |
| duplicate-gone-field | 0/24 | 1 | yes |
| gone-ignores-unreadable | 15/24 | 1 | yes |
| unlogged-against-base-names | 1/24 | 1 | yes |
| pacnew-log-without-backreference | 24/24 | 0 | no |
| restored-reference | 24/24 | 0 | n/a (reference) |

4. [obs] The expected detector was the unchanged VERSION 1 score-pacnew-arm-r35.py at 6b4561e43e15c1cce038e390ad7d4691b0af4cc8, executed through the prescribed committed-receipt form without --seed or --fixtures. It checks one drift line, each of the eight named integer fields exactly once, oracle equality, bounded allowed census exit, and unchanged fixture bytes/modes/ctime. All runs drew fresh seeds. The reasons below are the counter’s literal reason values; null means the fixture matched, not an absent result. The fixture IDs are zero-based within that receipt, and every fixture from 0 through 23 is covered explicitly. The complete ungrouped ledger, with original receipt line pointers and census exits, is /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/fixture-reasons.tsv:2-385. The original fixture rows are lines 3-26 of each named receipt. Expected and reported values are retained in those receipt rows. Counter evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/counter-v1.source.txt:48-56,269-285,321-367.

| Run | Fixture IDs | Counter reason |
|---|---|---|
| base-reference | 0-23 | null |
| pacnew-plus-one | 0-23 | field mismatch |
| pacsave-plus-one | 0-23 | field mismatch |
| pacorig-plus-one | 0-23 | field mismatch |
| unreadable-plus-one | 0-23 | field mismatch |
| log-pacnew-plus-one | 0-23 | field mismatch |
| log-pacsave-plus-one | 0-23 | field mismatch |
| unlogged-plus-one | 0-23 | field mismatch |
| gone-plus-one | 0-23 | field mismatch |
| duplicate-drift-line | 0-23 | drift_lines=2 |
| drop-gone-field | 0-23 | missing gone |
| duplicate-gone-field | 0-23 | duplicate field gone |
| gone-ignores-unreadable | 0, 1, 2, 5, 6, 9, 10, 11, 12, 14, 15, 16, 19, 20, 23 | null |
| gone-ignores-unreadable | 3, 4, 7, 8, 13, 17, 18, 21, 22 | field mismatch |
| unlogged-against-base-names | 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23 | field mismatch |
| unlogged-against-base-names | 10 | null |
| pacnew-log-without-backreference | 0-23 | null |
| restored-reference | 0-23 | null |

5. [obs] In the bounded fixture-generator source, deliberately mismatched ALPM source/target names occur for saved-as .pacsave events. The installed-as distractors either use ALPM-SCRIPTLET, end in .pacnew.tmp, or are correctly paired non-/etc events. Valid installed-as events always copy the same hostfile into the source and target. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/counter-v1.source.txt:141-170. [inf] This explains the surviving mutant: the generated inputs do not discriminate correct installed-as pairing from this broader pacnew regex. The 24/24 is therefore a coverage finding against the counter, not a contract change or a claim of correct mutant behavior. I did not edit the counter or add another distinguishing probe.

6. [obs] Every counter header reports counter_sha256=19d25d14f9ee6ad15c036c75f997f2fba7aa756779c9e3b70a0ff136297e0155. Each full census digest and revision is below. The same reference digest was observed before mutation, after every individual restoration, and in the restored-reference receipt. Evidence: line 2 of each receipt; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/restorations.json:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/measurements.json:1.

| Run | Committed revision | census_sha256 |
|---|---|---|
| base-reference | 5e91daae65bd21fe8f0b3fe43e6139858c93dfa1 | 991c2c522486bf6f5cee686ff4b5bb439a8da206714c5d6e0d6595bcb628fcdd |
| pacnew-plus-one | 253d6f3e037bb48da71f6baa401715da9ed3382b | 19b06185c918ecb24e633c2f7ae36bd360c47b27fed50a8b54d89a9dcb9fe779 |
| pacsave-plus-one | f04ee28719b958d3f58a4b4a9385c7295cf9ad6b | 9cfb737280f0895fc9049c4e8cfb79432a2a3ea4b138780bb61f96188bec16be |
| pacorig-plus-one | a9515b8f703fcdf8d0582bf5c73e5f1ddba9cb75 | a9ae84199c5c73fe0c85718e5c072457daa8c4c9e4af1a8321bc1294e7f7afcb |
| unreadable-plus-one | 74d18be3baf5cea807a5ce3d52a10f6a5e8a6baa | ec0a7e31f248264d355ee825701d1f9985725d689d52704cdc0668e45dedca32 |
| log-pacnew-plus-one | c593ad7ffa55dacf48578103f16e4e0f08c58b56 | a149ae0a817b12a044dd6842096e9e70f04f6303694d51d7e31a967cf4ab6197 |
| log-pacsave-plus-one | 16ef584073a7cf92dde739d9b8e8757dde1f830b | b84bc74abe75bbb1ce4257cdacec73b72004b8662779f5414deee9190a8d0861 |
| unlogged-plus-one | 3369b8bad88bf614ba5d6e8ca1641f03b453378a | 7f0855ee7416b0ba9280e7c0579335ab077ef6b621bfe515f0f1e84b25cc320a |
| gone-plus-one | cfb4ef626a7149876c85a61b6668846e3b2c995c | 5ef1fa0227d75ae20e6aa247b7513777ab60bca8d766492ff06e979a2856f86a |
| duplicate-drift-line | d88a99cb1443ffa6f836691458b8c26c17d777a7 | 837c7869fe5365ac1550711c7a8ce3b77b8236e2ae033fb2b29103e012261409 |
| drop-gone-field | 901b0c515fae101a2d69418bb34b0776be31331b | 28888f945886856a0a5081da71209643cb4eb79117925e44f63c8c5bd88c335f |
| duplicate-gone-field | 523e45c649778b78057dfcc0962778fe08f4f13a | 3bf0819584569bb365d5c624d3ee96ce86a9b35f0c78425b2a9bf20cf59645dd |
| gone-ignores-unreadable | ad3f1698b94962b12fb7402a40cd6ba4b99edb22 | 3ec567b3e82c1b7e1b317478135918862986e9bb7913230a7a13cf34940d11b7 |
| unlogged-against-base-names | 02988dc2f5085ff239cf6886fd9fe41653e9bcac | ea91332666ee23ec899cf21d6ebe9932f6a57ea75157c851ae003ce9b4dafce3 |
| pacnew-log-without-backreference | c21cff93244a90f99b0d22bdc20a8ffca7133fc8 | 08094373ca75a93ed323070175466359cb47fe1cce4fe5df54ac538b83f46777 |
| restored-reference | 5e91daae65bd21fe8f0b3fe43e6139858c93dfa1 | 991c2c522486bf6f5cee686ff4b5bb439a8da206714c5d6e0d6595bcb628fcdd |

For each run, its full candidate-to-variant patch is saved beside its receipt as <run>.patch. Each mutant additionally has <run>.mutation.patch containing only the difference from the reference commit. Restored-reference reuses the reference commit and base-reference.patch. The supplied reference-arm snapshot SHA-256 is de2b036eab01df75d361700743e86374de224a69e46b5ab17ee97c7bb3dfa4ad; the unchanged bytes are retained at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/reference-arm.source.txt:1.

7. [obs] Each mutant was restored in a finally block by checking out the reference commit, and all fourteen resulting census hashes equal 991c2c522486bf6f5cee686ff4b5bb439a8da206714c5d6e0d6595bcb628fcdd. The common restored detector then read 24/24, exit 0. Finally I checked out the original candidate commit: the sandbox census hash returned exactly to 7daa2ccbbded3a931abdbd76cb8ad34ccbe596f6dabc3524c519cc123e44e7b5, its entry hash. The sandbox push URL was set to DISABLED. No lane source was edited, no package transaction or service operation ran, and no persistent/background process was started. All launched subprocess calls were synchronous and bounded by timeout; all completed. Evidence: /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/restorations.json:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/restored-reference.jsonl:2,27-28; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/final-restoration.json:1; /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/commands.json:1. Initial containment commands and their successful outputs are recorded in this seat’s tool transcript (clone/checkout/push-disable exit 0; df -h /fast showed 85G available).

8. [obs] No external source was fetched, no tool was installed, and no build, lint, selftest, host census, or other detector was run. These were the assigned fourteen mutation probes plus their shared positive baseline and restoration detector only. Axes exercised were field-value sensitivity, output cardinality/schema, log/filesystem pairing, unreadable-directory handling, and restoration integrity. This report does not judge or integrate C1.

Scope: read=provided candidate declaration, QUALITY, reference arm, counter and receipt runner, sandbox census, godspeed and shokunin instructions; wrote=/fast/scratch/hyaku/tsukuroi-r35/K15FieldMutants/**, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/**, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants.md; executed=timeout-wrapped df, mkdir, sha256sum, read-only lane git show, sandbox git clone/checkout/remote/add/commit/rev-parse/diff/show, 16 committed-receipt counter calls, and bounded Python evidence collation; command argv and outputs in /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-35/w1/K15FieldMutants/commands.json
Model: openai-codex/gpt-6.1-sol
Installs: none
