VERDICT: defect-found

Seat `C1ExecBootTools` (L2, round 43, wave w1). Item C1-7: which lane tools read
`tools/boot-chain-audit.sh` or its output; run each at base
`6951ead90566b2d74f7c45b4efca29246badad64` and implementation
`717b716a8943151ace8657e0ca23d7d9b8434f26`; report verdict changes; try `--live` once as myself.

The defect is a **registry-coverage regression, not a boot-chain behaviour change**: the C1 helper edit
harm no reader and the live audit still works, but the implementation commit adds two tools with no
operative registry row, so `check-registry-coverage.py` goes PASS (exit 0, 66/66) -> FAIL (exit 1,
66/68, two `REGISTRY-ROW-MISSING`). One of the two new tools is the C1 counter, which reads
`tools/boot-chain-audit.sh`. Section 5 gives the exact finding and a proposed (unapplied) row.

## 1. Which lane tools read the script or its output

Command (exact item command):

```
$ grep -ln 'boot-chain-audit' /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/*.py \
      /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/*.sh
tools/check-registry-coverage.py
tools/check-self-assessment.py
tools/score-bootinputs-r43.py
tools/boot-chain-audit.sh
```

(`boot-chain-audit.sh:2` is its own banner.) Three readers, three different surfaces:

| Tool | Reads the script how | Verdict-bearing? |
|---|---|---|
| `tools/score-bootinputs-r43.py` (new in r43) | executes it: `SCRIPT = 'tools/boot-chain-audit.sh'` (`:61`), `git show <rev>:tools/boot-chain-audit.sh` (`:263`), strips `main "$@"`, sources the body as `/mnt/bca-lib.sh` and calls `boot_inputs_newer` (`:111`, `:313`); also runs `bash <script> --selftest` and counts `st_check 'R43-C1-` lines (`:329-331`) | yes, the C1 counter |
| `tools/check-registry-coverage.py` | committed text only: registry row/paths (`audit_path` `:331`; the `AUDIT_LIVE_*` constants `:60-66`; `_audit_live_map` `:330-350`) and a text scan of the selftest flag `--self-?test` (`SELFTEST_FLAG` `:56`, scan `:306-315`, finding `REGISTRY-SELFTEST-UNRESOLVED` `:313`) | yes (registry gate) |
| `tools/check-self-assessment.py` | **does not read the real file**: the path occurs only as a hermetic-fixture literal (`:833`) and a fixture scorecard row (`:889`); its revision inputs are `git show`/`git ls-tree`/`git archive` over SCORECARD/SKILL/corpus files and `tools/tsukuroi-census.sh --selftest` (`:177-200`), never `tools/boot-chain-audit.sh` | no (fixture text only) |

No lane tool consumes the script's **output**. `grep -rn 'TSUKUROI_BOOTCHAIN' --include='*.py' --include='*.sh'`
outside `.ufo` returns only the script itself and the counter's selftest-line regex (`score-bootinputs-r43.py:32,329-331`);
`grep -rn 'audit-live' tools/` is empty. `tools/check-boot-chain.py` is a neighbouring boot gate but binds the
round-17 witness `corpus/knowledge/boot-chain-r17.json` (its docstring `:4,13`), and `check-freshness-r17.py:60`
reads the round-17 capture files, not this audit's stdout; neither names `boot-chain-audit`.

## 2. Verdicts at base and at implementation

Receipts written by `tools/run-receipt.py` (private clone, fixed child env) into
`.ufo/waves/round-43/w1/C1ExecBootTools/`:

| Check | base `6951ead9` | impl `717b716a` | Change |
|---|---|---|---|
| `check-registry-coverage.py --revision <REV>` | exit 0, `PASS`, 66 tools / 66 rows / 66 registered, findings 0 (`registry-coverage-plain-6951ead9.jsonl`) | exit 1, `FAIL`, 68 tools / 66 rows / 66 registered, findings 2 (`registry-coverage-plain-717b716a.jsonl`) | **PASS -> FAIL** |
| `... --audit-live-map` | exit 0, `PASS`, `audit_live_map_errors: 0` | exit 1, `FAIL`, `audit_live_map_errors: 0`, same 2 findings | PASS -> FAIL (map itself clean) |
| `... --baseline-tools 6951ead9` (impl run) | — | exit 1, `baseline_tools_missing: 0`, `discovered_tools: ["tools/check-scrub-record-r43.py","tools/score-bootinputs-r43.py"]` (`registry-coverage-baseline-tools-717b716a.jsonl`) | attributes the 2 findings to the two new tools |
| `check-self-assessment.py --revision <REV>` | exit 1, `FAIL`, checked 27, mismatches 1: K10 only (`self-assessment-6951ead9.jsonl`) | exit 1, `FAIL`, checked 27, mismatches 2: K07 + K10 (`self-assessment-717b716a.jsonl`) | status same, **one new mismatch** |
| `score-bootinputs-r43.py --revision <REV> --scratch <DIR>` | exit 2 at `run-receipt`: `{"error": "tool is not a tracked file at the tool revision", "tool": "tools/score-bootinputs-r43.py"}` (`score-bootinputs-base.stdout`) | exit 0, `PASS`: cases 16, correct 16, identity_ok 1, live_agree 1, `selftest_line "TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=48 failed=0"`, selftest_r43 3, `wrong: []` (`score-bootinputs-717b716a.jsonl`) | tool absent -> PASS |
| `tools/boot-chain-audit.sh --selftest` (git-archive copies at each revision, `TMPDIR` in scratch) | exit 0, `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=45 failed=0` (`bca-6951ead9.selftest.out`) | exit 0, `TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=48 failed=0` (`bca-717b716a.selftest.out`) | 45 -> 48, both PASS |

Attribution of the two non-boot changes:

- The `check-registry-coverage` findings are exactly
  `REGISTRY-ROW-MISSING site=tools/check-scrub-record-r43.py` and
  `REGISTRY-ROW-MISSING site=tools/score-bootinputs-r43.py`: the operative table still has 66 rows while
  the tree now has 68 `tools/` files (`git diff --name-status 6951ead9 717b716a`: `A tools/check-scrub-record-r43.py`,
  `A tools/score-bootinputs-r43.py`). Neither the audit's registry row nor its live map broke:
  `audit_live_map_errors` is 0 at impl and no `REGISTRY-SELFTEST-UNRESOLVED` is emitted, and both new findings
  name the *tools*, not `tools/boot-chain-audit.sh`.
- The new self-assessment mismatch is K07 only: `depth row states 63 notes; corpus/knowledge holds 64 .md files`
  at impl (63 at base). That is C2's new note `corpus/knowledge/btrfs-scrub-record-r43.md` (added in the same
  commit), not C1. K10 (`states 60 lesson files; holds 61`) is identical at both revisions.
- Worktree bytes equal the implementation blob for the audit:
  `git hash-object tools/boot-chain-audit.sh` = `459fb17667644a08e0f5ee9614edd00c1c8cfd17` =
  `git rev-parse 717b716a:tools/boot-chain-audit.sh`; `git status --porcelain -- tools/boot-chain-audit.sh` empty.

## 3. Live run as myself (item-authorized read-only sudo path)

Command: `TMPDIR=/fast/scratch/hyaku/tsukuroi-r43/C1ExecBootTools/live bash tools/boot-chain-audit.sh --live`
(from the lane worktree, at the impl blob). **sudo was not refused**: the audit's documented read-only
`sudo -n cat`/`sudo -n stat` (header `tools/boot-chain-audit.sh:89-95`) succeeded for the unprivileged caller.
Observed exit 0, stderr empty, stdout header plus six entries and the summary:

```
label	efi	sha256	b2_ok	uname	VERSION	init_sysroot_refs	init_new_root_refs	image_new_root	latehooks	overlay_root	plymouth_root	rootflags	snapshot	snapshot_ro	selected	verdict
//linux	/EFI/Linux/omarchy_linux.efi	2e9c9bdc…	ok	7.2.11-arch1-1	42.2	7	0	symlink->sysroot	plymouth btrfs-overlayfs	/new_root	/new_root	subvol=@	-	-	true	BOOTED-OBSERVED
…
# counts entries=6 kernels=5 booted=1 path-aliased=2 pre42=1 untested=1 not-kernel=1 unknown=0 b2_mismatch=0
TSUKUROI_BOOTCHAIN: CONSISTENT
```

Full bytes: `live-stdout.txt` (2078 B), `live-stderr.txt` (0 B) in the seat dir. Only my two redirect files
remained in the work dir afterwards (`ls -la` showed `live-stdout.txt`, `live-stderr.txt`; the audit's
`mktemp -d` work tree is removed), so the run made no host write. No password was entered.
Because `newer = 0` had to hold for the `BOOTED-OBSERVED` row, the fix's live path is demonstrated on the
real host; the counter's independent Python walk agrees (`live {"expect":"0","got":"0","rc":0}`, live_agree 1).

## 4. What did not change (no-harm for the C1 edit itself)

- No reader's verdict changes because of the helper edit: the registry row/map still validates
  (`audit_live_map_errors` 0), the `--selftest` flag text is still present (no `REGISTRY-SELFTEST-UNRESOLVED`),
  the selftest still PASSes with three more cases (45 -> 48), and the live path still returns CONSISTENT.
- `check-self-assessment.py` is not a reader of the real script; its K07 flip is C2's new note.
- The C1 counter reads the script through `git show <rev>:` (`:263`), so it is revision-bound and cannot be
  satisfied by worktree bytes.

## 5. Findings

**F1 (defect, no-harm / operability).** At the implementation commit `check-registry-coverage.py` is red:
`66` of `68` `tools/` files registered, two `REGISTRY-ROW-MISSING` (`tools/check-scrub-record-r43.py`,
`tools/score-bootinputs-r43.py`). The new C1 counter is one of them, and it is a reader of
`tools/boot-chain-audit.sh`. The round-43 declaration (`SCORECARD.md:2648-2673`) does not disclose a registry
update, and "Causal separability: C1 touches `tools/boot-chain-audit.sh` only" omits the added counter file.
Same pattern and repair as round 27 (`corpus/lessons/round-27.md:74`: "The registry-coverage gate read FAIL at
`099c7b3f` (2 missing rows: the two new counters); `SKILL.md` now carries … 31 rows") and round 35
(`corpus/lessons/round-35.md:60`). Repair is L1-owned: add operative rows for both new tools to the superseding
registry table. Proposed, **not applied** (seats are read-only on lane content):

```
| bootinputs-r43 | probe | `python3 tools/score-bootinputs-r43.py --revision <REV> --scratch <DIR> [--lane <repo>]` | 0 PASS, predicate `cases == 16 and correct == 16 and identity_ok == 1 and live_agree == 1 and selftest_pass == 1 and selftest_r43 >= 2`;1 any conjunct fails;2 harness error | none: the 16 namespace cases, the live leg and the script's own `--selftest` are the measurement; controls `.ufo/waves/round-43/controls/` | R43 C1 frozen counter sha256 `886f92c8cd58e52e4e74f4df81708f243b77e9d33de567b47371f21419b3e10f` (matches `git show 717b716a:tools/score-bootinputs-r43.py | sha256sum`); caller uid/gid via setpriv | private `--scratch` only, removed on exit; reads the revision's script through `git show`; no host writes | tsukuroi |
```

(The `check-scrub-record-r43` row belongs to C2's item, not this seat.) Kind/exit cells are grounded in
`score-bootinputs-r43.py:64-65` (predicate), `:121` (`die(code=2)`), `:348` (`return 0 if ok else 1`), `:45` (usage).

**F2 (observation, low weight).** `SKILL.md:3893` still carries the round-42 routed note
"Not fixed here (routed): `tools/boot-chain-audit.sh:480-487` … reads false under pipefail". Its sentence is
scoped "here" = round 42 and the section is historical (`SKILL.md:3851`), so it is not literally false; but a
reader grepping the defect after this round lands at a line that still reads as open. A one-line supersession
pointer in the round-43 text (not an edit of the historical section) would close it. Not called a defect.

**F3 (attribution).** The only self-assessment delta, K07 63 -> 64 knowledge notes, is C2's
`corpus/knowledge/btrfs-scrub-record-r43.md`; K10 is pre-existing at base. Neither is the boot surface.

## 6. Not done

- No census selftest, no control battery, no round-42 C1 counter, no `check-scrub-record-r43.py` (C2's item;
  its verdict conjunct binds only wave-2 seats) — deliberately, to avoid stacking heavy counters.
- `check-self-assessment.py --selftest` and the two gates' own hermetic `--selftest` modes were not run (not
  revision readers of the audit).
- No package/tool installs (nothing was needed), no `pacman`, no service, mount, sysfs, `/etc` or boot change,
  no btrfs ioctl, no lane git/jj mutation. Scratch `…/tsukuroi-r43/C1ExecBootTools/` removed after the receipts
  were copied into the seat dir.

## Evidence index (`.ufo/waves/round-43/w1/C1ExecBootTools/`)

`registry-coverage-plain-{6951ead9,717b716a}.jsonl`, `registry-coverage-auditmap-{6951ead9,717b716a}.jsonl`,
`registry-coverage-baseline-tools-717b716a.jsonl`, `self-assessment-{6951ead9,717b716a}.jsonl`,
`score-bootinputs-717b716a.jsonl` + `.stdout`, `score-bootinputs-base.stdout`,
`bca-{6951ead9,717b716a}.selftest.{out,err}`, `live-{stdout,stderr}.txt`.
