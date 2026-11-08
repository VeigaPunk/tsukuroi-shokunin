# CriticClaims — falsifying the WORDING of C1/C2 (round 92, wave w1)

Seat: CRITIC. Lane read-only; receipts in `.ufo/waves/round-92/w1/CriticClaims/`; scratch
`/fast/scratch/hyaku/tsukuroi-r92/CriticClaims/` (removed on exit). Instruments were never edited;
every probe/harness is a copy under the seat scratch.

State note (matters for every citation below): the lane moved while this review ran. Commit
`429fd1a3` (A2) was HEAD at start; `d1f6934f` (A3, "gate hardening", 02:15:15) landed mid-review and
rewrote `tools/check-limine-pins.py`, `tools/limine-pin-battery-r92.py`, the four C2 bends and the
freeze manifest. Current bytes: gate `35c1088b…`, battery `aef33925…`; the declaration's frozen
bytes are gate `af90ae63…`, battery `fde864ea…`. Findings are stated against the sentence as
written and name which generation the receipt proves.

---

## 1. C1's "0 of 89 families passed" and "0 error rows" — `falsifies-wording` (evidentiary role)

**Sentence touched** (`/.ufo/plans/round-92.md:30-32`, SCORECARD `Round 92` C1 row): "each of the
five oracle-channel controls … reads `verdict unmet` with 0 of 89 families passed and 0 error rows
in each of three runs".

**Which rows are verdict rows.** In the after state every case row of every control is a *verdict*
row: `case_log[*].error` is `null` in all 5 × 3 × 356 rows
(`after/c1-controls/canonical-after/K3-sibling.json`, `after-clone/*`). The battery emits an `error`
row only on timeout or unparseable output (`tools/limine-pin-battery-r92.py:1770-1795`), and the
control's fallback always exits 0 with JSON, so "0 error rows" in the after state is guaranteed by
the generator, not measured. In the **before** leg, the tracked `before-clone/` receipt contains 984
**error** rows for K4 (`bad-output: AttributeError: module 'batt_oracle' has no attribute 'r1_key'`,
`after/c1-controls/before-clone/K4-syspath.json`) — those are crash rows, not rejections; K3/K5/K6/K7
have 0 error rows and 82/82 `met`.

**The counterexample (executed).** A closed-channel control does **not** have to read 0/89. The
shipped fallback is a constant `HEALTHY` answer; its verdict coincides with the expected answer of
EMPTY-PIN-LIST, and only the U1 field separates them. I copied K3-sibling to scratch and gave the
closed-channel fallback a U1 model (and nothing else); under the frozen launcher it reads
**`families_passed 1/89`, EMPTY-PIN-LIST passing 4/4 cases** (`fallback-u1-aware-1of89.json`;
control copy `fallback-u1-aware-control.py`; unpatched control for contrast
`fallback-shipped-0of89.json`). Under C1's own kill rule that closed-channel control would be "unmet
because a control passed a family". So `0/89` is a property of *how incomplete the fallback is*, not
of channel closure; the closure evidence is the before/after differential (same control bytes, open
channel → 82/82 `met`), not the 0/89 number.

**Narrowing required.** Write: "the shipped controls' constant fallback fails all 89 families; one
family (EMPTY-PIN-LIST) is separated only by the U1 answer, so 0/89 is not by itself a measurement
of closure — the before leg is." (Numbers themselves stand for the shipped bytes.)

## 2. C1's launcher sentence — `neutral-shaped` (survives; unnamed channels found, none reach the oracle)

**Sentence touched** (`round-92.md:24-33`): "copies the gate's bytes into a private directory that
holds nothing else and runs it as `bwrap --unshare-all --clearenv --die-with-parent --new-session`
with only `/usr` and `/etc` read-only, fresh `/dev` `/proc` `/tmp`, the case directory read-only and
the gate copy read-only mounted, cwd = the case directory, `python3 -I`".

I ran probes through the frozen battery's own `sandbox_argv`/`copy_gate` (imported by path; battery
sha256 checked before use) for every channel the sentence does **not** name:

| channel probed | result | receipt |
|---|---|---|
| `argv` / `/proc/self/cmdline` | names only `python3 -I <gate-copy>`; no battery path | `launcher-probe-inner.json` |
| `/proc/1/cmdline` | full bwrap argv incl. the random gate-copy and case paths; no battery path | `launcher-probe-lane-work.json` |
| `/tmp` leftovers | `[]` (fresh tmpfs) | `launcher-probe-inner.json` |
| `/proc` PIDs | `["1","2"]` only — the battery parent is not in the PID namespace | `launcher-probe-inner.json` |
| case dir | fixture only | `launcher-probe-inner.json` |
| a second/other run's work dir | not visible; ancestors of the bound case path are created as **empty** dirs | `launcher-probe-lane-work.json` |
| inherited fds | only 0/1/2 pipes; no fd to the battery | `launcher-probe-lane-work.json` |
| battery bytes by direct path, ancestor-relative path, or walk of `/usr` `/etc` `/tmp` `/` | unreachable (`exists()` false; walk finds only `/usr/share/man/limine.1.gz` etc.) | `launcher-probe-inner.json`, `launcher-probe-lane-work.json` |

Channels that **do** work but carry no oracle: `/proc/1/cmdline` and the host-path ancestor chain
listable inside (both expose random `mkdtemp` names, not bytes); `/dev/shm` fresh and writable;
full read of `/usr` and `/etc` (host fingerprint; no oracle installed there); hostname shared (UTS
not unshared). Verdict: the sentence is a read-path contract and it holds — every unnamed channel
either leaks names/fingerprints or is write-only. No narrowing needed; if the round wants the
wording airtight, add "path names and host fingerprints remain visible; no oracle bytes are."

## 3. C2's era sentence — `neutral-shaped` (boundary correct; one wording overreach)

**Sentence touched** (`round-92.md:56-60`, SCORECARD C2 row): "applies the visibility rule of the
era the version selects — below 12.9.5 the r91 V1 rule, from 12.9.5 on `create_menu_tree`'s in-place
cut with no first-line-is-entry exception (v12.9.6 raw 328-330, 362-365)".

I compiled both pinned `config.c` copies (`before/src/limine-v12.9.4…`, `…-v12.9.5…`) against stub
headers with stubbed `ext_mem_alloc`/`panic`/`blake2b`/`smbios` and ran `init_config()` +
`config_get_value(NULL,0,key)` over a 30-shape matrix (`era-harness/` in the receipts; binaries
rebuilt from the copies with `cc -Iinclude harness.c shim.c obj-<era>.o`). Every key-visibility
difference found is the **first-line-is-entry class**, including whitespace-indented first entries,
`/` alone, `/a/b`, and macros/CRLF/blank-line/comment variants (which show no key difference):
`era-differential.json`, full run log `era-differential-run.txt` (13 diffs, all line-1-entry
shapes).

Two results the wording should absorb:

1. **The boundary is right, and upstream says so in its own words.** v12.9.6 ChangeLog:
   "A config whose first line is an entry has had no global options since 12.9.5, whereas every
   option in it used to count as global. Fixes #700." That is exactly the two eras the gate models.
2. **"The global section is empty" is one sentence wider than the code.** In v12.9.5/v12.9.6 the
   first entry's label line survives (the NUL is written at the label's newline), so the visible
   text is the label (`"/boot"`), not `""` (`era-differential.json`,
   `era_b_visible_text_when_line1_is_entry`). Behaviourally identical for every key lookup (a label
   line cannot be a key line), so no family is missing; the *mechanism* sentence should say
   "no global options are visible" rather than "the section is empty".
   No config shape other than first-line-is-entry behaved differently between the eras in the
   compiled differential; the roster is not missing an era family.

## 4. The `--usage-check` / rc-64 clause — `falsifies-number` (clause is real, but uncertified by the round's receipts; and "no verdict" is unasserted)

**Sentence touched** (`round-92.md:59-60` + target line 65; SCORECARD C2 target): "refuses any
version outside `X.Y.Z` with rc 64 and no verdict" and "`--usage-check` `met` (8/8 refused/accepted
cases)".

- **rc 64 is measured through the launcher.** `usage_check()` copies the gate and runs
  `sandbox_argv(gpath, case, [python3,-I,gate,--conf,--esp,--limine-version V])`
  (`tools/limine-pin-battery-r92.py:2015-2050`). It is not the gate's own exit outside a sandbox.
- **Bytes enforcing it:** `parse_limine_version()` → `None` for a non-`X.Y.Z` string, then main():
  `if parse_limine_version(a.limine_version) is None: ap.print_usage(sys.stderr); return 64`
  (`tools/check-limine-pins.py`). Not argparse: the option is a free string, so argparse only
  handles missing/unknown flags (also rc 64 via `UsageParser`).
- **"and no verdict" is not asserted.** `usage_check` compares only `p.returncode`; stdout is never
  inspected. A gate that printed a JSON verdict *and* returned 64 would still score `met`.
- **N04 surviving the families does leave the clause uncertified by the counting command** — as
  committed, no receipt in the wave ran `--usage-check` on any near-miss (the only usage receipts
  are `after/c1-controls/usage-{canonical,clone}.json`, both on the landed gate). I ran it:
  N04 `unmet` (every refusal case rc 1 — an uncaught `ValueError` traceback, not a clean 64);
  landed gate `met` on 11 cases (post-A3 battery); N01 `unmet` (see §5/C2 bend defect)
  — `usage-N04-accept-any.txt`, `usage-landed-gate.txt`, `usage-N01-era-flat-a.txt`.
- **The numeral is stale.** The frozen target says `8/8`; A3's battery runs **11** usage cases
  (`9"*5000+".0.0"`, `12.09.4`, `00.00.00` added). A3's amendment says "No predicate, target …
  changes", yet the target's count no longer matches the instrument.

**Narrowing required.** Say "`--usage-check` `met` (11/11)"; add to the check "stdout carries no
JSON verdict in the refusal cases"; and land a `--usage-check` receipt for N04 (the clause's named
certifier) — `usage-N04-accept-any.txt` is one.

## 5. The kill rule — `falsifies-wording` (the check cannot bind the freeze)

**Sentence touched** (`round-92.md:41`): "void if any instrument byte differs from
`.ufo/waves/round-92/before/freeze-manifest.sha256` (`sha256sum -c`)".

- **It can fail** on a changed copy: tampering a copy of the gate in scratch and running
  `sha256sum -c` on a derived manifest exits 1 (`killtest/`, scratch). So the mechanism works
  mechanically.
- **It cannot bind.** The manifest is a lane file and has been regenerated in every amendment
  (freeze → A1 → A2 → A3). Today `sha256sum -c .ufo/…/freeze-manifest.sha256` exits **0** while
  the instruments are **not** the frozen ones: gate `35c1088b…` vs freeze `af90ae63…`, battery
  `aef33925…` vs `fde864ea…`, all five controls differ from the freeze-commit bytes, and 34 manifest
  lines differ from `git show da99b2f4:.ufo/waves/round-92/before/freeze-manifest.sha256`.
  The kill rule is satisfied *by construction*, because the document that defines "the instrument"
  moves with it. A3 made this concrete by rewriting the gate, the battery, the four C2 bends and
  the manifest in one commit; C1's gate receipts (02:06–02:07, `gate-canonical.json`,
  `gate-clone.json`) were measured on pre-A3 bytes, and A3 re-measured only C2.

**Narrowing required.** Bind the manifest by hash (record its sha256 in the declaration and check
that), or define the void condition as `git diff --quiet <freeze> -- tools/ .ufo/waves/round-92/before/controls/`
being empty, and cite every receipt by the instrument sha it measured.

Live confirmation of the defect: at 02:17 `sha256sum -c` on this manifest exited **0**; at 02:21 the
same command exits **1** only because an uncommitted repair of N01/N02/`make-c2-gates.py` and two
corpus files is in flight — nothing about the frozen instrument bytes changed. The check's verdict
tracks whoever last regenerated the manifest, not the freeze.

---

## 6. C1 target "before leg: each control 82/82 `met` ×3" — `falsifies-number` (committed receipts contradict it for K4)

**Sentence touched** (`round-92.md:32-33, 36-37`; SCORECARD C1 target): "the same controls read
82/82 `met` against the r91 battery in the same clone layout and the same environment" and "before
leg (r91 battery, clone, `PYTHONPATH=<clone>/tools`) each control 82/82 `met` ×3".

The tracked before-leg receipt `after/c1-controls/before-clone/summary.tsv` reads:

```
K4-syspath  3  1  0,0,0  unmet,unmet,unmet  984  f3be5624…
```

i.e. **0/82 with 984 error rows**, not 82/82. The 82/82 `met` receipt exists only for the A2 bytes
(`before-clone-fixed/summary.tsv`, `efb53f76…`), and the matching A2 after-leg lives in
`canonical-after-fixed/` and `after-clone-fixed/` (committed by A3). Meanwhile the tracked after-leg
C1 receipts still carry A1 K4 `f3be5624…`, which the manifest no longer pins (`efb53f76…`). The
claim stands only by splicing three amendments; as one dataset the legs never share control bytes.

**Narrowing required.** Cite the A2 (`efb53f76…`) K4 before/after pair only, name the 984-error A1
run as the repair's evidence (it is a crash, not a rejection), and state which control bytes each
leg used.

## 7. C2's near-miss controls N01/N02 — `falsifies-number` (they crash; they do not "fail 2/3 families")

**Sentence touched** (`round-92.md:65-67`, SCORECARD C2 target): "the near-miss variants
`N01-era-flat-a` (2 families fail), `N02-era-flat-b` (3 fail) … each `unmet` ×3 both layouts".

Both committed control files are **syntactically invalid**: `python3 -m py_compile` reports
`IndentationError: unexpected indent` at line 164 (`before/controls/c2gates/N01-era-flat-a.py:163`,
`N02-era-flat-b.py:163`), because `make-c2-gates.py` splices the override line `era_b = False` at
column 0 inside `check()`. Both were regenerated again by A3 and are still broken. The committed
receipts show `families_passed 0`, `failed_families` = all 89, and **356 error rows per run**
(`after/c2-near-misses/canonical/{N01,N02}*.json`; the clone leg, 02:17–02:18, is the same
1068-error crash on the same bytes) — crash rows, not the declared 2/3 family failures. N03 is
sound (88/89, only ERA-DEFAULT, 0 errors) and N04 is 89/89 `met` as disclosed.

**A repair is landing while this review ran, and it changes one numeral.** The working tree now
(uncommitted, outside the manifest) has an indentation fix in `make-c2-gates.py` and regenerated
N01/N02 that compile. I ran both once through the frozen battery:
- N01 `87/89`, failed **ERA-FLE-MEASURED-B, ERA-FLE-PANIC-B**, 0 errors — the declared "2 families
  fail" is right once the receipt lands (`n01-repaired-working-tree-87of89.json`);
- N02 `85/89`, failed **ERA-DEFAULT, ERA-FLE-MEASURED-A, ERA-FLE-PANIC-A, FIRST-LINE-ENTRY**,
  0 errors — the declared "3 fail" is **wrong**: it is **4** (FIRST-LINE-ENTRY is era-A-only and
  the declaration omits it) (`n02-repaired-working-tree-85of89.json`,
  `near-miss-repaired-summary.json`).

Consequence: until repaired receipts land, the era branch has no working one-clause mutant on
record; and the N02 numeral needs to become 4 either way.

**Narrowing required.** Land receipts for the repaired bends (both layouts) and correct N02's count
to 4; make `make-c2-gates.py` `py_compile` its output so a spliced control cannot be frozen again.

---

## Verdict

- **C1 wording (`0 of 89`, `0 error rows`, launcher): partly falsified.** The launcher sentence
  (`round-92.md:24-33`) holds under every probe (`launcher-probe-*.json`). The evidentiary claim
  "0 of 89 families passed" is `falsifies-wording`: a closed-channel control with a U1-aware
  fallback reads 1/89 (`fallback-u1-aware-1of89.json`), so 0/89 is an artifact of the fallback, not
  a measurement of closure; and the target's before-leg "82/82 ×3" is falsified as committed by
  `after/c1-controls/before-clone/summary.tsv` (K4: 0/82, 984 error rows).
- **C2 wording (era boundary): survives.** Compiled differential over 30 shapes
  (`era-differential.json`, `era-harness/`) finds only the first-line-is-entry class; the v12.9.6
  ChangeLog states the same boundary. One wording overreach: era B leaves the first entry's label
  line visible (`"/boot"`), not an empty section.
- **C2 numbers: falsified where they name controls.** N01/N02 are non-executing
  (`IndentationError`, 356 error rows/run), so "2 families fail / 3 fail" and "both layouts" are
  false; `--usage-check` numerals are stale (8 vs 11) and "no verdict" is unasserted
  (`usage-*.txt`).
- **Kill rule: falsified as binding.** `sha256sum -c` exits 0 today over instruments that are not
  the freeze bytes, because the manifest was regenerated (freeze → A1 → A2 → A3; A3 landed at
  02:15:15 mid-review).
