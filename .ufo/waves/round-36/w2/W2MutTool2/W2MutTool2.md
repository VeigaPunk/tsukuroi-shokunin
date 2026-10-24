# W2MutTool2 — kill-check, after-mutant m2 (`check-report-receipts.py`)

Seat: `W2MutTool2`, mutation-tester. Lane: `tsukuroi-shokunin`. Wave: round-36 w2 (FALSIFY).
Written UTC: 04:35:59Z (pasted from `date -u +%H:%M:%SZ`).
Claim under test: C1 — the five live tools build child envs from fixed dicts
(`tools/probe-child-env-allowlist-r36.py`, VERSION 7, frozen at `1e926801`, probe sha256
`a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` == claim prefix `a2a5acac`).

## Verdict

**KILLED.** Frozen probe, `--set livefive --only tools/check-report-receipts.py`:
pristine **leaking 0** (exit 0) → mutant **leaking 3** (exit 1), `harness_errors []`,
`predicate_label leaking`. Channels fired: **names, quiet, source**; `untraced` read
0 records in both trees (uninformative by the probe's own rule — the mutant's fixed
`PATH=/usr/bin:/bin` survives, so the wrapper directory is unreachable).

## 1. Mutant applied

`mutant-2.diff` was **present** at `.ufo/waves/round-36/w1/MutToolMutants/mutant-2.diff`
(md5 compared by size/head, not reconstructed). It restores the ambient copy at the
declared m2 site:

```
tools/check-report-receipts.py  find_receipts()  (line 313)
+    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
+    env.update({            # fixed dict demoted to an overlay
         ...
-    }
+    })
```

Construction (all inside `mktemp`; no lane/fleet byte touched, no `git add/commit/push`):

| step | evidence |
|---|---|
| sandbox clone | `git clone -q --no-local file:///home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/w2m2t2.tuY0TZ/mut`; HEAD `8d5fa7f` |
| base = c052bb7 | `tools/check-report-receipts.py` **byte-identical** at `c052bb7` and lane HEAD `8d5fa7f` (`git diff --stat` empty) |
| apply | `git archive c052bb7 \| tar -x` into scratch tree, then `patch -p1 < mutant-2.diff` (hunk 1 clean, hunk 2 fuzz 2 offset 1 — this diff does carry context; output bytes verified below) |
| mutant bytes | sha256 `77178b4388b3e3dad4e4b398a52e90d3e27e443c6242a44204f38a1353b2cd7d` (pristine `e7a7911309725cce20f446f51d491395c26eb490047d50b5b3ee8d73d726627e`) |
| mutant commit | blob `35a8540b`, tree `9603236287`, commit `25d958ac77adc47b772c0e018c906e2473d059e1` (parent `c052bb7`), built with plumbing (`hash-object -w`, `read-tree`, `update-index --cacheinfo`, `write-tree`, `commit-tree`) + `update-ref refs/heads/m2` **in the mktemp clone only** — no `git add`/`commit`/`push` was run anywhere |

Site check on the mutant bytes (`sed -n 305,325p`): the dict comprehension over
`os.environ.items()` filtered by `GIT_` is present at line 313 and the fixed dict is
applied afterwards with `env.update(...)` — the exact declared shape.

## 2. Frozen-probe score (one scoring run each; same probe bytes, sha re-hashed at run time)

```
python3 tools/probe-child-env-allowlist-r36.py \
  --lane /tmp/w2m2t2.tuY0TZ/mut --revision <rev> \
  --base  c052bb7d41ced49aa888817069afd804eccfecf1 \
  --set livefive --only tools/check-report-receipts.py --scratch <fresh>
```

| run | revision | last JSON line | exit |
|---|---|---|---|
| pristine | `c052bb7d41ced49aa888817069afd804eccfecf1` | `"pairs": 4, "leaking": 0, "leaking_pairs": [], "harness_errors": []` | **0** |
| mutant | `25d958ac77adc47b772c0e018c906e2473d059e1` | `"pairs": 4, "leaking": 3, "leaking_pairs": ["tools/check-report-receipts.py:names","…:quiet","…:source"], "harness_errors": []` | **1** |

Both runs: `probe_version 7`, `probe_sha256 a2a5acac…443a`, `target_set livefive`,
`base c052bb7…`, `predicate_label leaking`, `control_rc 0`, `control_git_execs 366`,
`git_execs 366`. Control stdout sha256 identical in both trees
(`765f5f3cd46d60df4d695b3ca6ba0c726f772f11a20d6589e5ea781ac2470d45`), so the base is a
passing baseline and the kill is attributable to the mutation.

Channel detail (mutant):

- **names** — `leak: true`; evidence: `12 of 12 injected names reached a child`,
  `7 of 10 value-channel NAME=VALUE strings reached a child: LANG,LOGNAME,SHELL,TERM,TMPDIR,TZ,USER`,
  `18 child environment strings carry a run-unique ambient …`.
- **quiet** — `leak: true`; `8 of 8 injected names reached a child`, 7 value strings, 15 strings.
- **source** — `leak: true`; `findings: ["tools/check-report-receipts.py:313 ambient-read .environ"]`.
- **untraced** — `leak: false`, `untraced_record_count: 0`, `untraced_log_exists: true`,
  `unparsed_exec_records: 0`. Zero records = UNINFORMATIVE (fixed `PATH` in the surviving
  dict), not a miss: the mutant is killed by three other channels.

Pristine: names/quiet/source all `leak: false`, source `findings: []`, untraced 0.

## 3. Ordinary-run check (ambient marker reaches a child)

No probe instrumentation, no `strace`: an `LD_PRELOAD` constructor
(`ordinary-run-marker.c`, built `gcc -shared -fPIC`) appends `pid/comm/R36LEAKMARK/LD_PRELOAD`
to `$R36MARKLOG` in every process that loads it. `LD_PRELOAD` and `R36LEAKMARK` are not
`GIT_`-prefixed and are absent from the fixed dict, so only an ambient copy can deliver them
to the `git` child.

Run: `cd <tree> && env LD_PRELOAD=…/mark.so R36LEAKMARK=leak-m2-<tree> R36MARKLOG=… python3
tools/check-report-receipts.py --report .ufo/waves/r36-probe-report.md --lane <bare clone>
--revision <rev>` (a report file was written into both trees exactly as the probe's
`write_livefive_report` does, so the run does not differ by input).

| tree | rc | log lines | git-child lines carrying the marker |
|---|---|---|---|
| pristine `c052bb7` | 0 | 1 (the target python only) | **0 of 366** |
| mutant `25d958a` | 0 | 367 | **366 of 366** — e.g. `comm=git mark=leak-m2-mutant LD_PRELOAD=/tmp/w2m2t2.tuY0TZ/mark.so` |

Official stdout identical in both (`f4e90f8d…`), so the leak is silent — exactly the
operability defect m2 models. 366 matches the probe's `control_git_execs`, i.e. every git
child in the run inherited the ambient environment.

## 4. Restoration

Reverse patch on the scratch tree, then hashes:

```
patch -p1 -R < mutant-2.diff      # hunk 2 fuzz 2, offset 1
sha256  scratch tree file          e7a7911309725cce20f446f51d491395c26eb490047d50b5b3ee8d73d726627e
sha256  pristine reference         e7a7911309725cce20f446f51d491395c26eb490047d50b5b3ee8d73d726627e   (equal)
sha256  mutant reference           77178b4388b3e3dad4e4b398a52e90d3e27e443c6242a44204f38a1353b2cd7d
```

Sandbox clone: HEAD still `8d5fa7f`; `tools/check-report-receipts.py` in its worktree
`e7a7911…` (never edited); `git status --porcelain` → 0 entries after restore. Note: the
plumbing tree build left the clone's **index** dirty (staged deletions of files added in
`8d5fa7f` plus the mutant blob), observed as `MM`/`D `/`??` in `git status`; worktree bytes
were unaffected (hash above) and the index was reset with `git read-tree HEAD`. This did not
affect scoring: the probe exports trees with `git archive <rev>` and clones bare, neither
reads the index. Mutant commit `25d958a` remains only as a scratch object under
`refs/heads/m2` in `/tmp/w2m2t2.tuY0TZ/mut` — disposable scratch, no lane ref/commit/index
was written at any point.

## 5. Findings for the wave

1. **m2 killed** — the frozen probe's names/quiet/source channels all fire on the ambient
   copy at `find_receipts()`; the mutant is not a gap in the counter. The `untraced` channel
   is silent here by design (fixed `PATH`), so a zero there must not be read as "no leak".
2. **Ordinary-run leak is silent** — identical stdout on pristine and mutant; a passing run
   of the tool cannot reveal this defect, only environment observation can.
3. **Base drift (minor)** — the assigned base `c052bb7` is no longer lane HEAD (`8d5fa7f`,
   wave-2 spec). `tools/check-report-receipts.py` is byte-identical across the two, so the
   mutant base assumption holds; recorded so a later reader does not mistake the clone's
   HEAD for the tasked commit.
4. **Tooling** — no install/upgrade performed; `patch`, `coreutils`, `gcc` and `/usr/bin/strace`
   were already present. PACMAN untouched.

## Artifacts (same directory)

| file | sha256 |
|---|---|
| `probe-pristine.jsonl` | `b1807335596a03bd9d9e540936b2a936fe2b489d3d2ac741e01ac014ef9f9dfa` |
| `probe-mutant.jsonl` | `50a89825f3eaba49b1e3f24c338631b05275a5cf22e67ff24c1998252f12de72` |
| `ordinary-run-pristine.log` | 1 line (target python only) |
| `ordinary-run-mutant.log` | 367 lines, 366 `comm=git` |
| `ordinary-run-marker.c` | LD_PRELOAD marker source |
| `official-stdout-{pristine,mutant}.json` | identical (`f4e90f8d…`) |
| `mutant-2.diff` | copy of the w1 artifact actually applied |
| `summary.json` | machine verdict |

Report: `.ufo/waves/round-36/w2/W2MutTool2`
