# Round 80 — non-author closure spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed 2026-11-04. Base `467a9b7891a5939dab8460ec6f591fbb16bd82e9`;
measured implementation `160b8889703dd22b38c89368871f27517af02c1f`;
delivered tip `cdcab9f3a6c1046919b84503b7c02935c3a49410`.
Status **ok**, admitted **false**, verdict **rejected-honest-stop**.
C1 verifies; C2 reaches only 1/2 under its unchanged frozen predicate.
No owned-axis harm was identified. A real, defective round is not a marker;
red gates and conformance defects are recorded, not converted into `failed`.
No promotion, capability acquisition, scope transfer or ordinal uplift is awarded.

Dispatch/completion digest, copied from the mutable watchdog log:

```text
2026-11-04T17:07:26-03:00 launch tsukuroi round=80 pgid=2985857 driver=hyaku-inline attempt=1
2026-11-04T17:41:35-03:00 complete tsukuroi round=80; hyaku-inline attempt=1
```

## Step-1 conformance

- `git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-80/tsukuroi.md`
  returned `tsukuroi-shokunin eefe1cd5963bda0999991ea8fd0625f707659d0b`.
  Report commit time was `2026-11-04T17:40:35-03:00`, after lane tip
  `2026-11-04T17:39:22-03:00`. Its committed bytes equal the filed report.
  Work, landed changes/LOG links, measurements, sources/frontier, trends and
  SHONEN sections are present in order; one SHONEN heading and four `[~]`
  lines correspond to the four checklist boxes, with no self-awarded `[x]`.
- `git cat-file -t <hash>` and `git merge-base --is-ancestor <hash> master`
  succeeded for all four cited round commits:
  `61ec89ec6e6f284b6fba2127721359e6931a5789`,
  `aad05ef173176cf5223f7c315297240c2db1abe2`,
  `160b8889703dd22b38c89368871f27517af02c1f`,
  `cdcab9f3a6c1046919b84503b7c02935c3a49410`.
  All four authors and committers are `tsukuroi-shokunin <tsukuroi@shokunin.local>`.
  Ancestry was checked against the branch, not detached HEAD or `@{u}`.
- Before this artifact, `scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
  printed:
  `state branch=master local=cdcab9f3a6c1046919b84503b7c02935c3a49410 remote=cdcab9f3a6c1046919b84503b7c02935c3a49410 ahead=0 behind=0 head=detached tracked=0 untracked=0`.
  `git status --porcelain` was empty; `git ls-remote origin refs/heads/master`
  returned that exact delivered hash. No inherited or uncommitted round work was found.
- Prompt `.ufo/prompts/tsukuroi-round-80.md` was committed by the lane at
  `6e4a2ac0065b191bb6e73bff00c914955688d771`. At fleet snapshot
  `acf6101b8eb8813c9ddaa8ebc2d130b0d200e580`, own Python substitution of
  `templates/round-prompt.md` (fleet root, lane, round, axes and repo placeholder)
  reproduced the prompt's first 140 lines byte-for-byte: `startswith=True`,
  total prompt lines 818, unresolved `{{` tokens 0. Sections 1–5 carry the
  operative contract; the addendum carries write scope, pushed-hash citation,
  commit-before-report ordering and the campaign's superseding route instructions.
  No missing-template correction is required.
- Wave evidence: `after/settlement.json` records one 10-seat wave, eight durable
  reports, two dead attack seats, residual 0; attack allocation 3/10, one connector.
  The eight report paths resolve. CriticCounter-2 and MutationCounter-3 died on
  disclosed `402 … Insufficient account funds`; their missing attacks receive no
  credit. Null result outputs were not reconstructed. L1 planner ownership was
  declared before dispatch, but there is no spawned planner despite template §3's
  minimum role split: retained as the template/validator deviation, not hidden.
- History pin evidence was checked without executing a closure gate:
  `sha256(json.dumps(rounds[:48], sort_keys=True, separators=(',', ':')).encode())`
  is `ce97497ed699a8f0939be062d042cf4d6e3e7531116fbe4681593991d67f0a8e`.
  The prefix equals the one in the pin's anchor commit `ae19fca991aa419ac4c8fe25120c0dc1c363a4fb`; no pin was regenerated.

## Claim re-checks

Both claims were independently re-derived using only committed bytes and the
closure's own Python reader below, executed in Python Eval (not imported from
lane code). The lane's execution/selftest evidence was separately inspected.
The closure's earlier prohibited instrument invocations are disclosed under
**Closure-session deviation**; they do not establish gate conformance.

| Claim | Base | Measured implementation | Delivered tip | Judgment |
|---|---|---|---|---|
| C1 / depth | 0/42; note absent | 42/42 | 42/42 | verified; matches the reported rc1 → rc0 measurement |
| C2 / operability | 0/2 | 1/2 | 1/2 | not verified; matches the reported rc1 → rc1 frozen miss |

Reproducible independent reader, without executing any lane program:

```python
import subprocess, json, hashlib, re, xml.etree.ElementTree as ET
L = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
B = "467a9b7891a5939dab8460ec6f591fbb16bd82e9"
M = "160b8889703dd22b38c89368871f27517af02c1f"
T = "cdcab9f3a6c1046919b84503b7c02935c3a49410"
P = ".ufo/waves/round-80/"
def get(r, p):
    q = subprocess.run(["git", "-C", L, "show", r+":"+p], capture_output=True)
    return q.stdout if q.returncode == 0 else None
def sha(b): return hashlib.sha256(b).hexdigest()
for r in (B, M, T):
    data = get(r, "corpus/knowledge/service-restart-matrix-r80.json")
    c1 = 0
    if data is not None:
        d = json.loads(data)
        x = get(r, P+"before/systemd.service.xml")
        table = ET.fromstring(re.search(rb"<table>\s*<title>Exit causes.*?</table>", x, re.S)[0])
        head = ["".join(e.itertext()).strip() for e in table.findall(".//thead/row/entry")][1:]
        expected_rows = []
        for row in table.findall(".//tbody/row"):
            cells = ["".join(e.itertext()).strip() for e in row.findall("entry")]
            expected_rows.append({"cause": cells[0], "restart": [v == "X" for v in cells[1:]]})
        review = json.loads(get(r, P+"w1/ReviewMatrix/verdict.json"))
        companion = get(r, "corpus/knowledge/service-restart-matrix-r80.md")
        assert d["settings"] == head and d["rows"] == expected_rows
        assert data == get(r, P+"before/expected.json")
        assert sha(data) == "05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153"
        assert sha(x) == d["snapshot_sha256"] == "12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44"
        assert review == {"artifact_sha256":sha(data), "companion_sha256":sha(companion), "verdicts":["holds"]*6}
        sr = [line.split("|") for line in get(r,"corpus/SOURCES.md").decode().splitlines() if line.startswith("| S330 |")]
        assert len(sr)==1 and len(sr[0])==13
        s = [v.strip() for v in sr[0]]
        assert (s[3],s[4],s[8]) == ("docs","A","mined") and d["url"] in s[2] and "corpus/knowledge/service-restart-matrix-r80.json" in s[11]
        c1 = sum(len(row["restart"]) for row in expected_rows)
    reg = get(r,"SKILL.md").decode().split("## Gate and probe registry — round71 superseding current rows\n",1)[1].split("\n## ",1)[0]
    rows = [[v.strip() for v in line.split("|")[1:-1]] for line in reg.splitlines() if line.startswith("| ")]
    c2 = 0
    for name in ("count-kr-rows-r69.py", "check-transaction-order-r39.py"):
        found = [row for row in rows if row[0] == name[:-3]]
        if len(found) != 1: continue
        row = found[0]
        rb = get(r, P+"w1/"+name+".receipt.json")
        if rb is None: continue
        receipt = json.loads(rb); tool = get(r,"tools/"+name)
        shape = len(row)==8 and row[1]=="gate" and row[4]=="`python3 tools/"+name+" --selftest`" and "3 self-test failed" in row[3]
        bound = receipt.get("tool_sha256")==sha(tool) and receipt.get("argv")==["python3","tools/"+name,"--selftest"]
        green = receipt.get("rc")==0 and receipt.get("failed")==0 and type(receipt.get("passed")) is int and receipt["passed"]>=4
        c2 += bool(shape and bound and green and b"--selftest" in tool and b"SELFTEST" in tool)
    print(r, "C1="+str(c1)+"/42", "C2="+str(c2)+"/2")
```

Observed output:

```text
467a9b7891a5939dab8460ec6f591fbb16bd82e9 C1=0/42 C2=0/2
160b8889703dd22b38c89368871f27517af02c1f C1=42/42 C2=1/2
cdcab9f3a6c1046919b84503b7c02935c3a49410 C1=42/42 C2=1/2
```

### C1 — verified source-grounded detail, not runtime equivalence

Independent XML parsing found six rows × seven settings, matching JSON cell for
cell: row marked counts `2,2,4,3,4,3`, 18 marked and 24 empty cells; `no` is
empty in every row. The table's header order also matches. Manual source reads
confirm explicit-stop exceptions (:881-883, :996-1002), oneshot rejection and
successful-exit qualification (:909-911, :1144-1146), main-process-only prevent/
force status rules (:1107-1131, :1139-1146), clean-status scope (:889-897,
:1066-1083) and start limits (:1004-1008). The companion states the limits and
does not infer installed-build equivalence, a past failure cause or future restart.

Committed digests at both measured revision and tip:

- matrix and frozen expected object:
  `05abbf14c2c2e8d5ce31cc5c815e264937d6c11a882d3fc08d90ca6952965153`;
- companion: `81006519e1b5f4d9144c8b6003536204d749f3b1428578aac115b8b5e28e4a56`;
- source snapshot: `12770f86a26dcdf32873225669f5aa9421283c303bbc72bddb04530850f66d44`;
- frozen instrument: `688766756d0fb73ffb8f1d746e3377d58532bd4afa0a3aa92489c61165614d1d`.

The source, expected object and instrument digests also equal their freeze-commit
values. The unique S330 row is docs/A/mined, names the URL and both companions.
`ReviewMatrix/verdict.json` binds both final artifact digests with six `holds`.
The r79 null-output binding problem is therefore not repeated in C1: the required
binding is a committed seat-written file. Complete fabricated bundles can still
pass the finite equality/binding predicate; semantic reading and live re-opening
are separate evidence, not an authenticity certification.

### C2 — truthful repair, unchanged failed target

The fixed current round71 registry has one `count-kr-rows-r69` row but zero
`check-transaction-order-r39` rows at base and tip. Its true second label is
`transaction-order-r39`. At tip the KR row, selftest tokens and digest-bound
receipt satisfy every frozen clause; the transaction row's correct interface
cannot satisfy the counter's invented label. Using the actual labels would show
both repairs, but that is not the frozen claim and is not substituted for it.

`after/commands.json` records measured revision
`160b8889703dd22b38c89368871f27517af02c1f`: base C1 count0/rc1, C2 count0/rc1;
after C1 count42/rc0, C2 count1/rc1. `before/controls.json` contains 11/11
recorded holds. Its C2 positive uses synthetic filename-derived labels, not the
real registry identity: it does not establish actual-input positive coverage.
No target, truthful row name or frozen counter was changed to rescue the miss.

## Gate evidence — capability receipts are not blanket conformance

- KR receipt binds production digest
  `908592d2f8a209fdd070c6adc3157f04d69fcfe6815bda5ceb3d9981848ac97d`,
  argv `python3 tools/count-kr-rows-r69.py --selftest`, rc0, passed10/failed0.
  Transaction receipt binds
  `c7055a81f98b8462b3a34ba17545087bdb09bb17532594dd1a9823aa9b5aec33`,
  its public selftest argv, rc0, passed9/failed0. Both equal committed tool blobs
  and delivery copies. Code inspection confirms isolated fixtures invoking their
  public CLIs rather than a helper-only check. Final author-side selftest tallies
  recur in the committed `after/selftest-*.txt` receipts. No selftest was run here.
- The report calls the final run an exact-revision external export. The evidence
  binds tool digests and names the measured revision globally, but does not retain
  an inventory/digest of the entire exported sandbox. Closure verifies **tool-byte
  binding**, not a complete independently bound exact-revision sandbox replay.
- KR's red receipt records rc3, passed4/failed6; its mutation recipe and raw rc
  file resolve. Transaction's red output records 8/9 with
  `SELFTEST-DUPLICATE-BLOCK`; rc3 is recorded in `ExecTransaction/digests.txt` and
  its report, not in a standalone rc file or structured red-control receipt.
  These are committed execution reports, not independently replayed controls.
- **Red-control digest discrepancy:** `ExecKR/tool.sha256.txt:3` assigns the
  unmutated `908592d2…` digest to `red/count-kr-rows-r69.py`. Its retained recipe
  replaces the unique exit predicate with unconditional `return 0`; applying
  that exact replacement in memory, without executing or writing a mutant,
  gives `f9a9ad74e1d1d72f6dc0eb3d041c1485587f53eb4b296f9922effa4ce4297113`,
  not the listed digest. The historical red-file digest is not verified.
- The new `measure-round80` registry row correctly discloses its helper-only
  absent-reader selftest debt. That is not full public-self-invocation conformance.
  Static code inspection also found that digest tampering returns
  `(0, 'snapshot_tampered')`, then exits1 at main :91, whereas PROTOCOL requires
  `snapshot_tampered` to be could-not-evaluate. No tamper occurred in delivered
  inputs, so this does not overturn the independent C1 content measurement.
- Support receipts at the measured revision: registry120/120, findings0 rc0;
  knowledge references98 notes/dangling0 rc0; headers96/98 with two findings rc1.
  The two header-debt notes are byte-identical base→tip (own hash comparison).
  Line-endings403/violations0 and end-census rc0 are worktree checks, not commands
  explicitly bound to a revision; closure does not upgrade them to exact-tree
  evidence. The requested live census was separately executed below.
- Own parser over the fixed round71 section: base gate93/none-selftest36;
  tip gate94/none-selftest34. The new helper-only gate is additional debt, not
  one of those 34 `none` cells. No whole-registry conformity is certified.

## Outside discernment spot-check

Re-opened URL on 2026-11-04:
https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd.service.xml .
The live response's SHA256 is the committed snapshot's `12770f86…6d44`.
Quotes below were checked after XML-tag stripping and whitespace normalization.

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| New S330 docs/A/mined | admit | Pinned URL :877-878, `Configures whether the service shall be restarted when the service process exits, is killed, or a timeout is reached.` (19 words) | agree | Exact located ≤25-word quote; all 42 table cells and surrounding conditions support the bounded documentation teaching; no installed-build equivalence. |
| Always restarts after operator stop | reject | Same URL :999-1000, `the service is stopped with systemctl stop or an equivalent operation.` (11 words) | agree | The surrounding exception expressly suppresses automatic restart on an explicit stop. |
| Always is accepted for oneshot | reject | Same URL :910-911, `always and on-success are rejected for them.` (7 words) | agree | The manual rejects those settings for oneshot rather than merely leaving them inert. |
| On-watchdog covers unclean exit code | reject | Same URL :906-907, `the service will be restarted only if the watchdog timeout for the service expires.` (14 words), plus unclean-code row :942-951 | agree | The cited row has an empty on-watchdog cell; the prose restricts it to watchdog expiry. |
| Prevent-exit list applies to helpers | reject | Same URL :1126-1128, `this setting has no effect on processes configured via ExecStartPre=, ExecStartPost=, ExecStop=, ExecStopPost= or ExecReload=,` (15 words) | agree | The next clause confines RestartPreventExitStatus to the main process. |

One admit and four rejects independently checked; five agreements. The new row's
quote is 19 words and its URL, date, anchor and used-by paths resolve.
Own committed-byte census reproduces rows329→330; A312→313/B6/C11;
mined291→292/queued5/rejected33; malformed rows0. `git diff` of SOURCES shows
one new row and no old-row changes. No frontier row advanced.

Required command actually executed by closure:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

Observed exit **0**, W04 duplicate-URL warnings only, final line:
`tsukuroi ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`.

## Axis and trend verdicts

`git diff 467a9b7891a5939dab8460ec6f591fbb16bd82e9 cdcab9f3a6c1046919b84503b7c02935c3a49410 -- SCORECARD.md`
adds the declaration and truthful measured miss, with no ordinal change.
Only the two new r80 companion files change under knowledge; existing entries
are not edited or deleted. PROVINCE.md and SHONEN.md are byte-unchanged.

| Axis | Verdict | Evidence |
|---|---|---|
| depth | improved | C1 independently verifies the sourced 42-cell matrix and qualifications; ordinal8→8, without invented uplift. |
| operability | unchanged | C2's frozen target2 is missed (0→1); actual repairs are acknowledged but no partial/renamed claim replaces it; ordinal9→9. |
| coverage | unchanged | Existing systemd-service ground deepened; no frontier or capability row entered. |
| freshness | unchanged | New note has source/verified-at/recheck headers; no older entry was re-verified or superseded. |
| calibration | unchanged | Report preserves C2 miss, old rejections, provider deaths and instrument limits; new evidence defects are routed, not treated as passing proofs. |
| adjacency | unchanged | Province unchanged; no scope absorbed; ADJ06/OUT009 arbitration remains open. |

No axis is graded harmed. Ordinals remain depth8/coverage9/operability9/
freshness9/calibration9/adjacency8; no exploratory claim was declared.

| Trend | Verdict | Evidence |
|---|---|---|
| expansion | unchanged | One new note and S330 deepen already-owned ground, not uncovered coverage-map ground. |
| quality | unchanged | No weaker prior entry superseded or stale entry re-verified; C2 and gate-evidence debt remain explicit. |
| discernment | improved | Outside review agrees on the admit and all four rejects; mistakes ground QUALITY111/112, including r79's extra binding leg and current actual-identity control failure. |

## Routed defects and operator notes

1. **Tsukuroi next round — actual-identity positive control.** Apply QUALITY111 to
   the real registered label before freezing the next predicate; align declaration
   and code. Preserve r80's original predicate, target and rejected result.
2. **Tsukuroi next round — gate-standard debt.** The new counter needs genuine
   public-path isolated self-invocation coverage and correct could-not-evaluate
   handling for tampered snapshots. Repair in new work, not a rewritten r80 freeze;
   continue the inherited 34 `none` selftest rows or justify reclassification.
3. **Tsukuroi next round — evidence correction.** Append an erratum naming the
   contradictory KR red-file digest; distinguish production, mutated-copy and
   execution receipts. Retain the old evidence. Transaction red rc3 remains
   evidence-reported, not independently byte/rc-bound. Do not claim a complete
   exact-revision sandbox replay from the two tool digests alone, or worktree
   support checks as explicitly revision-bound runs.
4. **Tsukuroi next round — inherited red header gate.** Resolve the two unchanged
   provenance-header findings on `modprobe-config-plane-r72.md` and
   `module-parameter-plane-r71.md`; they remain named debt, not new r80 harm.
5. **Operator/protocol — planner and routing.** Reconcile the spawned-planner
   template wording with the validator's prohibition/L1-planner convention.
   Two dead attack seats and null outputs receive no retroactive evidence credit;
   routing repairs belong to the orchestrator, not this lane.
6. **Operator — adjacency/promotion.** ADJ06/OUT009 kaidoku/revenger ownership
   arbitration remains open and untouched. SHONEN boxes 1, 2, 4 look checkable from
   committed evidence; box 3's whole-SKILL no-oral-context replay is unexecuted.
   All four are therefore not fully verified; no `[x]`, promotion or mint is made.

## Closure-session deviation (protocol-owned)

Before switching to the independent reader, this closure session mistakenly
invoked the registered lane gate `python3 tools/measure-round80.py --revision
<REV> --claim <C1|C2>` for both claims at base, measured implementation and tip
(six invocations). Outputs matched the table above, with C1 rc1/0/0 and C2
rc1/1/1. This violated PROTOCOL's no-sibling-gate-execution closure rule; it is
recorded, not presented as compliant evidence verification. No selftest or other
lane gate was executed. Subsequent claim derivation used only the independent
committed-byte reader; semantic and gate-evidence rechecks were also delegated
to two read-only non-author seats, neither of which executed lane code.
This closure-process defect is status-neutral and is not attributed to the lane.

Only this verifier artifact and the closure MANIFEST rounds[] entry are authored
as durable changes by this closure. Lane-authored files remain untouched.
No tools were installed or updated. No domain mutation was performed.
