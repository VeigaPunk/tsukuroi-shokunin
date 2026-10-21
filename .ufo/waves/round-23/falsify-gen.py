#!/usr/bin/env python3
"""Generate the round23 falsify wave (post-build, designed from the integrated landed state a61db549).

L1 author: TsukuroiR23-2 (session3 replacement). Every seat is source-only NO-EXEC/NO-FETCH under a
schema-v2 binding; items attack the landed C1/C2/C3 instruments, the ledger and wave-1 outputs.
"""
import hashlib
import json
from collections import Counter
from pathlib import Path

R = Path('/home/vgpnk/Projects/shokunin/tsukuroi-shokunin')
W23 = R / '.ufo/waves/round-23'
C = W23 / 'candidate'
LANDED = '5a25c88b77f52e940bcad87825c4ac1cd529470d'
DIRECTIVE = (W23 / 'sources/godspeed-directive.txt').read_text()
(W23 / 'falsify').mkdir(exist_ok=True)

# Exact per-pack ledger slices: byte-derived subsets of the landed ledger, one per historical pack.
ledger = json.loads((C / '.ufo/waves/round-23/path-reconciliation.json').read_text())
(C / 'ledger-slices').mkdir(exist_ok=True)
for cohort in ledger['cohorts']:
    wave = cohort['wave']
    for g in range(1, 9):
        pack = json.loads((W23 / f'packs/{wave}-{g:02}.json').read_text())
        names = {s['name'] for s in pack['seats']}
        rows = [r for r in cohort['rows'] if r['site'].rsplit(':', 1)[0] in names]
        (C / f'ledger-slices/{wave}-{g:02}.json').write_text(json.dumps(
            {'schema': 'tsukuroi-path-reconciliation-slice-v1', 'wave': wave, 'group': g, 'landed': LANDED,
             'seats': sorted(names), 'rows': rows,
             'scope': 'Exact rows of the landed ledger for this pack; not a recomputation.'}, indent=1) + '\n')

items, bindings, reviews = [], [], []
common = [str(W23 / 'preregister.json'), str(W23 / 'sources/godspeed-directive.txt'), 'skill://godspeed']


def add(name, role, source, work, extra=()):
    src = W23 / source
    sha = hashlib.sha256(src.read_bytes()).hexdigest()
    report = f'.ufo/waves/round-23/falsify/{name}.md'
    rp = str(R / report)
    pred = 'r23f-' + name.lower()
    reads = list(dict.fromkeys([str(src), *common, rp, *map(str, extra)]))
    bind = {'name': name, 'root': str(R), 'read_paths': reads, 'write_paths': [rp], 'edit_paths': [rp], 'commands': [], 'fetches': []}
    prompt = ('/skill:godspeed\n' + DIRECTIVE + '\nNO-EXEC\nNO-FETCH\n# Seat binding\n' + json.dumps(bind, separators=(',', ':'))
              + '\n# Target\nRead ' + str(src) + '; declared SHA256 ' + sha + '.\n# Attack\n' + work
              + '\nState the attacked claim (C1/C2/C3/frontier), a concrete falsifier or the bounded search that found none, and the smallest in-scope remedy.'
              + '\n# Receipt\nDigest is supplied identity, NOT independently computed: never hash, list, wc, import or run any command to validate it. Write only your exact report. End with these three physical unfenced lines exactly once. Indent example receipt lines.\nReviewed-SHA256: '
              + sha + '\nPredicate: ' + pred + '\nScope: executed=none\n')
    items.append({'name': name, 'role': role, 'prompt': prompt})
    bindings.append(bind)
    reviews.append({'name': name, 'report': report, 'source': str(src.relative_to(R)), 'sha256': sha, 'predicate': pred})


cand = lambda p: C / p  # noqa: E731
EC, SB, PR = 'candidate/tools/check-edit-contract.py', 'candidate/tools/check-seat-bindings.py', 'candidate/tools/check-path-reconciliation.py'
know_e = [cand('corpus/knowledge/structured-edit-r23.json'), cand('corpus/knowledge/structured-edit-r23.md'), W23 / 'sources/structured-edit-observations.json']

# C1 — one attack per landed decision row (8).
for idx, row in enumerate(json.loads(cand('corpus/knowledge/structured-edit-r23.json').read_text())['decisions']):
    add('FxC1' + row['id'].title().replace('_', ''), 'reviewer' if idx % 2 == 0 else 'scout', EC,
        f"Attack C1 row {row['id']} -> {row['decision']}. Construct the smallest literal knowledge JSON/Markdown/SOURCES/preregister input that the landed check-edit-contract.py would count as validated for this row while the row's meaning is violated, or show by reading evaluate()/table_cells()/visible() why none exists. Compare the landed row against the preregistered tuple.",
        extra=know_e + [cand('corpus/SOURCES.md')])
# C1 — gate mechanics (6).
for name, work in [
    ('Table', 'Attack table extraction: HTML comments spanning lines, setext/indented code, nested blockquotes, escaped pipes, trailing spaces, CRLF and Unicode lookalike IDs in the knowledge Markdown. Name any visible-table spelling that counts or hides a row wrongly.'),
    ('Evidence', 'Attack evidence_ok(): S086 observations show CritRuntime starts before its request line and OraclePathArtifact edits without read starts. Does the gate overclaim what the evidence proves? Name any observation mutation it accepts that it should not.'),
    ('Source', 'Attack the S086 SOURCES row check: duplicate rows without a leading pipe, a decoy path suffix, wrong status/tier, column-count shifts. Name a registry text the gate wrongly accepts or rejects.'),
    ('Prereg', 'Attack the preregistration binding: the gate compares the knowledge decisions against preregister.json edit_decisions. Could a later preregister edit silently move the target? Is the comparison exact for order, case and extra rows?'),
    ('Limit', 'Attack the non-enforcement limit: the prose must visibly contain "It is not native permission enforcement" and the JSON scope must match exactly. Find an overclaim that still passes, e.g. a later sentence asserting enforcement.'),
    ('Selftest', 'Attack selftest independence: are clean fixtures literal and independent of production EXPECTED? Name any weakened rule (one line change) that no selftest case would detect.'),
]:
    add('FxC1' + name, 'critic' if name in ('Evidence', 'Limit') else 'reviewer', EC, work, extra=know_e + [cand('corpus/SOURCES.md')])

# C2 — v2 audit authority (8 mechanics + 8 shape oracles).
for name, work in [
    ('ClassifyEdit', 'Attack classify_edit(): key-shape set equality with optional i, URL/host:port detection, exact edit_paths membership. Find an edit request spelling that is clean but outside its exact declared target, or a legitimate one wrongly denied.'),
    ('SchemaV2', 'Attack v2 manifest validation: exact seat key set, edit_paths subset of read AND write, uniqueness, local(). Find a manifest that grants edit authority beyond read+write, or a v1 manifest that gains edit authority.'),
    ('Recursion', 'Attack allow_structured_edit propagation through multi_tool_use.parallel nesting and the depth limit; can a nested wrapper or a row/event marker enable edits under v1?'),
    ('Continuity', 'Attack v1 continuity: compare the landed file against snapshot/tools/check-seat-bindings.py line by line; name any v1 behavior change (outputs, exits, the 73 controls).'),
    ('Mode', 'Attack structured_edit_mode semantics: emitted only for v2, 1 when code is 0/1, 0 on could-not-evaluate. Is availability being sold as compliance? Is a red v2 audit with mode 1 honest?'),
    ('Collector', 'Attack the round23 collector projection for edit requests: key presence only, values redacted, unknown keys mapped to __unknown_argument__. Find an edit argument form that the collector projects into a clean v2 shape though the original was not structured.'),
    ('Expansion', 'Attack EXPANSION/CHECK_EACH: native edit adapters record separate read/write starts. Does the gate audit each additional recorded start independently, and can a valid edit target clear a backend read of another path?'),
    ('Selftest', 'Attack the 37 v2 selftest controls: name a one-line mutant of the v2 path that none would kill (the L1 mutation log at candidate measure/l1-mutation.json lists those already killed).'),
]:
    add('FxC2' + name, 'critic' if name in ('Mode', 'Expansion') else 'reviewer', SB, work,
        extra=[W23 / 'snapshot/tools/check-seat-bindings.py', W23 / 'candidate/collect.py', cand('.ufo/waves/round-23/measure/l1-mutation.json'), W23 / 'build/bindings.json'])
for i, (name, case) in enumerate([
    ('Stream', 'path+stream_content to the exact declared report'), ('OldNew', 'path+old_string+new_string with i to the exact declared draft'),
    ('Prefix', 'declared path plus .extra or /child suffix'), ('Spelling', 'dot segment, double slash, trailing slash or case variant of a declared path'),
    ('Scheme', 'skill://, xd://, artifact:// and https:// edit targets'), ('Half', 'old_string without new_string, or stream_content mixed with old_string'),
    ('Legacy', 'a schema-v1 manifest that carries an edit_paths field'), ('WriteOnly', 'an edit target present in write_paths but absent from read_paths'),
]):
    add('FxC2Oracle' + name, 'scout' if i % 2 else 'reviewer', SB,
        f'Hand-derive, from the landed source only, the exact exit code, finding IDs and structured_edit_mode for a v2 audit of: {case}. Then check the landed selftest contains an equivalent control; if not, give the literal fixture.',
        extra=[W23 / 'build/bindings.json'])

# C3 — ledger slices re-derived per historical pack (16) + gate mechanics (5).
for wave in ('build', 'falsify'):
    for g in range(1, 9):
        add(f'FxC3{wave.title()}{g:02}', 'scout' if g % 2 else 'reviewer', f'candidate/ledger-slices/{wave}-{g:02}.json',
            'For every row in this ledger slice, re-derive by hand from the raw pack events and bindings: the rough category/first bad component under the exact S085 regex and break rule, the canonical bad components under literal v1 authority and selector grammar, and the disposition. Report every row whose recorded value you dispute with seat, index, call_id and reason; if none, list the non-agree rows you checked and the path spelling that drove them.',
            extra=[W23 / f'packs/{wave}-{g:02}.json', W23 / 'sources/r22-rough-census.txt'])
for name, work in [
    ('Disposition', 'Attack derive(): agree / selector-normalization / unit-difference / unexplained. Find an event class the dispositions mislabel (e.g. URL reads that rough counts as path but lane counts as fetch, parallel wrappers, write selectors).'),
    ('Arithmetic', 'Attack the cohort identity rough - retained = selector-normalization - sum(unit extra) and the totals checks. Can cancelling errors still balance? Is any check redundant or vacuous?'),
    ('Canonical', 'Attack canonical_event() against the lane classifier in snapshot/tools/check-seat-bindings.py requested_path(): name any spelling where they diverge, and whether the per-event canonical count equal to retained count is then a real independent check.'),
    ('Pins', 'Attack pinning: frozen/reconciliation-inputs.json digests, ledger inputs_sha256, missing vs tampered exits, and --emit-ledger. Can the ledger be regenerated from tampered inputs and still pass?'),
    ('Selftest', 'Attack the 26 reconciliation selftest controls and the 10 recorded L1 mutants for it; name an unkilled one-line weakening.'),
]:
    add('FxC3' + name, 'critic' if name in ('Arithmetic', 'Canonical') else 'reviewer', PR, work,
        extra=[W23 / 'frozen/reconciliation-inputs.json', W23 / 'sources/r22-rough-census.txt', W23 / 'snapshot/tools/check-seat-bindings.py', cand('.ufo/waves/round-23/measure/l1-mutation.json')])

# Wave-1 output comparisons (3): independent executor drafts versus the landed tools.
for name, draft, landed in [('ExecEditContract', 'check-edit-contract.py', EC), ('ExecEditAudit', 'check-seat-bindings.py', SB), ('ExecReconciliation', 'check-path-reconciliation.py', PR)]:
    add('FxDraft' + name, 'reviewer', landed,
        f'Compare the landed tool with the independent wave-1 draft {draft} written by {name} (and its report). List every semantic divergence (decision, finding ID, exit, disposition, control) and say which side is right with a literal case.',
        extra=[W23 / f'worktrees/{name}/draft/{draft}', W23 / f'build/{name}.md'])

# Corpus and frontier (6).
for name, source, work, role in [
    ('KnowReconcile', 'candidate/corpus/knowledge/path-reconciliation-r23.md', 'Attack every factual sentence of the reconciliation knowledge entry against the ledger slices and packs: counts, the six events, strict-subset claim, the regex explanation.', 'reviewer'),
    ('KnowEdit', 'candidate/corpus/knowledge/structured-edit-r23.md', 'Attack the structured-edit entry: source-vs-policy separation, bounded procedure, limits; find an overclaim or an untestable sentence.', 'reviewer'),
    ('Lesson', 'candidate/corpus/lessons/round-23.md', 'Attack the round23 lesson: each Mistakes row needs class, evidence pointer, captured-by and a fix shown able to fail. Name any fix not shown able to fail.', 'critic'),
    ('Quality', 'candidate/corpus/QUALITY.md', 'Attack QUALITY 49-51: are they testable, non-duplicative of 1-48, and grounded in the cited lessons? Does 49 actually prevent a quality-improved verdict for this round without prior-entry supersession?', 'reviewer'),
    ('Sources', 'candidate/corpus/SOURCES.md', 'Re-open S085/S086 rows: 11 columns, own-work A mined, located anchors, used-by entries existing. Verify the round23 curation note is consistent with the lesson Gate quotes.', 'scout'),
    ('Frontier', 'candidate/corpus/QUALITY.md', 'Classify this round honestly: held-ground instrument depth vs frontier expansion. State what expansion/quality/discernment evidence the round has and lacks.', 'scout'),
]:
    extra = [cand('corpus/lessons/round-23.md'), cand('.ufo/waves/round-23/measure/l1-mutation.json'), W23 / 'sources/r22-closure.json']
    if name in ('Sources', 'KnowReconcile'):
        extra += [W23 / 'sources/structured-edit-observations.json', W23 / 'sources/r22-rough-census.txt']
    add('Fx' + name, role, source, work, extra=extra)

# Critics on claims as a whole (6).
for name, work in [
    ('Separability', 'Attack causal separability of C1/C2/C3: can each verify without the others landed? Shared files (SOURCES, QUALITY, lesson) do not count against separability unless a gate reads another claim\'s content.'),
    ('Inflation', 'Attack metric inflation: 0->8 decisions, mode 0->1, unexplained cohorts 2->0. Which are new-document counts rather than repaired behaviour, and are they labelled so?'),
    ('Order', 'Attack ordering: the preregistration (56c8ba3) predates tools landed by the replacement L1 (a61db549) before wave 1 spawned. Did any target move after outputs were visible? Is landing before the build wave a protocol defect?'),
    ('NoHarm', 'Attack no-harm: did any landed change weaken an existing gate, rewrite history, reauthorize an old event, or alter v1 results? Name the evidence.'),
    ('Quality', 'Apply the outside quality-unchanged precedent of rounds[422]: does this round have prior-entry supersession or reverification that would justify anything other than quality unchanged?'),
    ('Discernment', 'Attack the discernment trend: the round mined R23-QUALITY-TREND and R23-PATH-UNIT; are these real catches with fail-capable fixes or relabelled bookkeeping?'),
]:
    add('Crit23f' + name, 'critic', 'preregister.json', work,
        extra=[cand('corpus/lessons/round-23.md'), W23 / 'sources/r22-closure.json', cand('corpus/knowledge/path-reconciliation-r23.md'), cand('corpus/knowledge/structured-edit-r23.md')])

# Mutation design (4), sentinels (2), connectors (2), scribes (2).
add('MutFxEdit', 'mutation-tester', EC, 'Design (do not run) three one-line mutants of check-edit-contract.py not in the recorded L1 log; give the literal selftest case that should kill each.', extra=[cand('.ufo/waves/round-23/measure/l1-mutation.json')])
add('MutFxBindings', 'mutation-tester', SB, 'Design (do not run) three one-line mutants of the v2 path not in the recorded L1 log; give the killing literal control for each.', extra=[cand('.ufo/waves/round-23/measure/l1-mutation.json')])
add('MutFxReconcile', 'mutation-tester', PR, 'Design (do not run) three one-line mutants of check-path-reconciliation.py not in the recorded L1 log; give the killing literal control for each.', extra=[cand('.ufo/waves/round-23/measure/l1-mutation.json')])
add('MutFxLog', 'mutation-tester', 'candidate/.ufo/waves/round-23/measure/l1-mutation.json', 'Audit the L1 mutation log: are the mutants meaningful, were survivors handled honestly (fixed vs declared equivalent), is "killed = nonzero selftest exit" a sound criterion?', extra=[cand(EC.split('candidate/')[1]), cand(SB.split('candidate/')[1]), cand(PR.split('candidate/')[1])])
add('SentFxPrivacy', 'sentinel', 'candidate/.ufo/waves/round-23/path-reconciliation.json', 'Audit the committed ledger for retained secrets, report bodies, command bodies or environment data (it carries call IDs, argument digests and paths). Recommend minimal fields if any retention is excessive.')
add('SentFxEffects', 'sentinel', SB, 'Attack any inference that v2 authority prevents requests, contains effects, proves reading or licenses host action. Exact refusal boundary only.', extra=know_e)
add('ConnFxSiblings', 'connector', 'candidate/corpus/knowledge/structured-edit-r23.md', 'Sibling-overlap scan: does typed edit authority or path-census reconciliation overlap another lane\'s province (orchestration, kumitate tooling)? Name the boundary text that keeps this lane-local.', extra=[W23 / 'snapshot/PROVINCE.md'])
add('ConnFxPlanner', 'connector', 'preregister.json', 'Bounded planning data walk for the L1 planner seat: map each claim to its counting command, landed evidence and the falsifier items in this wave; name any claim with no attacking item.', extra=[W23 / 'snapshot/SCORECARD.md'])
add('ScribeFxLesson', 'scribe', 'candidate/corpus/lessons/round-23.md', 'Draft, in your report only, the falsify-wave section the L1 should append to the lesson: what was attacked, what survived, open defects. Plain prose, no invented results.', extra=[W23 / 'sources/r22-closure.json'])
add('ScribeFxErrata', 'scribe', 'candidate/corpus/knowledge/path-reconciliation-r23.md', 'Draft, in your report only, an errata template for the reconciliation entry (what changes if a falsifier disputes a ledger row) without asserting any dispute.')

n = len(items)
assert 64 <= n <= 100, n
assert len({i['name'] for i in items}) == n
context = (W23 / 'build/spec.json').read_text()
context = json.loads(context)['context']
context = context.replace('C1 depth eight typed structured-edit policy/source rows; C2 operability explicit v2 edit-target audit authority; C3 calibration exhaustive frozen round22 path-census reconciliation.',
                          'FALSIFY wave (post-build, from integrated landed state ' + LANDED + '): attack C1 eight edit-contract decisions, C2 v2 edit audit authority, C3 path-census ledger. Landed copies under ' + str(C) + '.')
context = context.replace('Only the three code executors may write their exact named draft in their own actual separate worktree; everybody else writes report only.', 'Every seat writes its report only.')
spec = {'wave': 'tsukuroi-r23-falsify', 'context': context, 'reportDir': '.ufo/waves/round-23/falsify', 'items': items, 'maxLanes': n}
(W23 / 'falsify/spec.json').write_text(json.dumps(spec, indent=2) + '\n')
(W23 / 'falsify/bindings.json').write_text(json.dumps({'schema': 'tsukuroi-seat-bindings-v2', 'seats': bindings}, indent=2) + '\n')
(W23 / 'falsify/reviews.json').write_text(json.dumps({'schema': 'tsukuroi-review-snapshots-v1', 'reviews': reviews}, indent=2) + '\n')
print(json.dumps({'seats': n, 'roles': dict(Counter(i['role'] for i in items))}))
