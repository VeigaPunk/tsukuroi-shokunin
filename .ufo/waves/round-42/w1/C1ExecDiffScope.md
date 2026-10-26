VERDICT: supports

# C1-5 — kill-rule scope check, `tools/tsukuroi-census.sh` c8efaa3 → 4476620

**Ruling: the kill rule does not fire.** All 8 hunks of
`git diff -U0 c8efaa3f120834541f8de1e5e0367e8d1593bae6 447662088dfd3155e31aed239179a79c1d1046c7 -- tools/tsukuroi-census.sh`
lie inside `probe_packages`, `probe_update_safety` and `run_selftest`. The set of functions whose
bytes changed is *exactly* `{probe_packages, probe_update_safety, run_selftest}` — `probe_storage_arm`
and every other function (23 of 26, incl. `main`, `usage`, `probe_oom_plane`, `probe_journal`,
`probe_drivers`, `probe_mem_arm`, `version_join`, `root_locator_class`) hash identically at both revisions,
and the function list (names + order) is unchanged, so nothing was added, removed or renamed.

## Method

- Inputs extracted from git, not from the worktree:
  `git show c8efaa3…:tools/tsukuroi-census.sh > base.sh` (sha256 `646c84fcdc166dd4…`),
  `git show 4476620…:tools/tsukuroi-census.sh > impl.sh` (sha256 `46d62a24709ece8e…`).
  Cross-check that these are the revisions' blobs: `git rev-parse <rev>:tools/tsukuroi-census.sh` gives
  `dda066f4…` / `ed83079c…`, and `git cat-file blob <that>` re-hashes to the same two sha256 values
  (receipt `crosscheck.log`, section "blob id <-> file sha256").
- Span computation is from the 4476620 file's own `^name() {` headers and `^}` closers (base spans likewise
  from base.sh), heredoc-aware: content between a `<<'DELIM'` opener and its delimiter line is skipped, so the
  fixture-dispatcher heredoc inside `run_selftest` (`cat > "$bin/.dispatch" <<'STUB'` at
  `impl.sh:1940`, closing `STUB` at `impl.sh:2013`; its heredoc content includes column-0 lines such as
  `rc_of()`/`out_of()` at `impl.sh:1947-1948`) cannot create phantom functions. Each hunk's NEW-side line
  range is mapped to its enclosing span; verdict is per changed line, not per hunk base.
- Independent cross-checks: `bash -n` on both scratch copies parses clean; `probe_storage_arm` extracted with
  `sed -n` + `sha256sum` (a non-Python path) gives the same digest on both revisions
  (`71e6007e566e1af3…`); numstat `+33 -8` (net +25) matches the file growth 3177→3202 lines; sum of
  per-hunk adds (4+1+1+2+2+1+10+12=33) and dels (1+1+1+2+2+1=8) matches numstat exactly, i.e. every
  changed line is accounted for by the eight mapped hunks.

## Hunk table (impl-side line numbers; `git-hint` is git's own `@@ … @@` label)

| # | hunk header | git-hint | changed impl lines | enclosing top-level function | in scope |
|---|---|---|---|---|---|
| 1 | `@@ -692 +692,4 @@` | `probe_packages() {` | 692–695 | `probe_packages` (L654–812) | yes |
| 2 | `@@ -694 +697 @@` | `probe_packages() {` | 697 | `probe_packages` | yes |
| 3 | `@@ -1621 +1624 @@` | `probe_update_safety() {` | 1624 | `probe_update_safety` (L1552–1817) | yes |
| 4 | `@@ -1635,2 +1638,2 @@` | `probe_update_safety() {` | 1638–1639 | `probe_update_safety` | yes |
| 5 | `@@ -1641,2 +1644,2 @@` | `probe_update_safety() {` | 1644–1645 | `probe_update_safety` | yes |
| 6 | `@@ -1652 +1655 @@` | `probe_update_safety() {` | 1655 | `probe_update_safety` | yes |
| 7 | `@@ -2346,0 +2350,10 @@` | `STUB` | 2350–2359 | `run_selftest` (L1931–3107) | yes |
| 8 | `@@ -2542,0 +2556,12 @@` | `STUB` | 2556–2567 | `run_selftest` | yes |

Notes for the L1:
- The base-side hunk line numbers reproduce the frozen claim's coordinates exactly: `-692`, `-694`,
  `-1621`, `-1635`, `-1641`, `-1652`. The two selftest hunks are pure insertions on the base side
  (`-2346,0` / `-2542,0`).
- Hunks 7 and 8 carry the label `STUB` because git's xfuncname heuristic takes the first column-0
  alphanumeric line above the hunk, and the dispatcher heredoc's closing delimiter sits at column 0
  (`impl.sh:2013`). `STUB` is heredoc text, not a function; the computed span owner is `run_selftest`.
  A reviewer trusting the `@@ … @@` hint would mis-read these two hunks as landing outside any function —
  worth one sentence in the wave-1 record if the hint is quoted anywhere.
- Hunk 7 adds `check 'blocked: a sample error ahead of a large -Qkk output still blocks (R42-C1)' …`
  (`impl.sh:2357`); hunk 8 adds `check 'degraded: 4002 update candidates keep the names and the trap row (R42-C1)' …`
  (`impl.sh:2564`) — 2 added lines carry the `R42-C1` label, matching "labels contain `R42-C1`".

## Per-function sha256 (body lines start..end inclusive, trailing newline per line)

```
parsed base: 26 top-level functions over 3177 lines, 85 heredoc-content lines
parsed impl: 26 top-level functions over 3202 lines, 85 heredoc-content lines
  same function list: True
  same  usage                  base 98b9195a1b0747ab (L562-576)  impl 98b9195a1b0747ab (L562-576)
  same  cap                    base 4a950cc5f07d4bd3 (L580-585)  impl 4a950cc5f07d4bd3 (L580-585)
  same  have                   base d89da2ace84fb08f (L587-587)  impl d89da2ace84fb08f (L587-587)
  same  rank                   base 13cf82729e9226c5 (L589-596)  impl 13cf82729e9226c5 (L589-596)
  same  worse                  base af9e72d5eb8b60ba (L598-600)  impl af9e72d5eb8b60ba (L598-600)
  same  nlines                 base 559f70e083cfd7f5 (L602-604)  impl 559f70e083cfd7f5 (L602-604)
  same  count_glob             base 6e77f8e9fb6f7373 (L606-613)  impl 6e77f8e9fb6f7373 (L606-613)
  same  count_pci_nvidia       base ee6ac130173b5621 (L615-623)  impl ee6ac130173b5621 (L615-623)
  same  class_counts           base 93779fa5f3f4db83 (L625-634)  impl 93779fa5f3f4db83 (L625-634)
  same  mem_read               base 1a3a1b9c971ac849 (L636-639)  impl 1a3a1b9c971ac849 (L636-639)
  same  mem_field              base 20dc5e573587d7f6 (L641-645)  impl 20dc5e573587d7f6 (L641-645)
  same  oom_keys               base 4a9858b8c6759f1e (L647-651)  impl 4a9858b8c6759f1e (L647-651)
  DIFF  probe_packages         base 299685346b819901 (L654-809)  impl b44b754893e82136 (L654-812)
  same  root_locator_class     base 2217064d010b659a (L811-826)  impl 2217064d010b659a (L814-829)
  same  probe_root_meta        base cbaa61b07a14b0af (L840-915)  impl cbaa61b07a14b0af (L843-918)
  same  probe_systemd          base 6ed15daa2ba3b47b (L918-981)  impl 6ed15daa2ba3b47b (L921-984)
  same  probe_drivers          base d5436803c8d338f4 (L984-1094)  impl d5436803c8d338f4 (L987-1097)
  same  probe_mem_arm          base a2ac777ab59239ac (L1106-1224)  impl a2ac777ab59239ac (L1109-1227)
  same  probe_oom_plane        base 698ca7966d004e6b (L1242-1388)  impl 698ca7966d004e6b (L1245-1391)
  same  probe_journal          base b9c07ee447bea092 (L1391-1514)  impl b9c07ee447bea092 (L1394-1517)
  same  version_join           base f9011e4bedf2bca8 (L1517-1535)  impl f9011e4bedf2bca8 (L1520-1538)
  DIFF  probe_update_safety    base dee107235193344a (L1549-1814)  impl 3898a2ea7dca725d (L1552-1817)
  same  probe_pacnew_arm       base ade47f83228de04f (L1817-1862)  impl ade47f83228de04f (L1820-1865)
  same  probe_storage_arm      base 71e6007e566e1af3 (L1865-1925)  impl 71e6007e566e1af3 (L1868-1928)
  DIFF  run_selftest           base f485aa04e5fcf68a (L1928-3082)  impl b887b2204b011a2b (L1931-3107)
  same  main                   base a06de9914c6b5427 (L3085-3175)  impl a06de9914c6b5427 (L3110-3200)

functions whose bytes changed: ['probe_packages', 'probe_update_safety', 'run_selftest']
changed-function set == allowed set: True
probe_storage_arm identical: True
unexpected changed functions: []
```

Because the changed-function set equals the allowed set and the function list is identical, the file's
non-function regions (the shebang/preamble before `usage`, the inter-function comment banners, the tail
after `main`) are also untouched: no hunk maps there, and all 33 added / 8 removed lines are inside the
three spans. `probe_storage_arm` is byte-identical to the base (`71e6007e566e1af3…`, confirmed by a second,
`sed`+`sha256sum` extraction).

## Exact commands + observed output

Script and full output are in the receipts; the numbers above are this run of:

```
$ cd /fast/scratch/hyaku/tsukuroi-r42/C1ExecDiffScope
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show c8efaa3…:tools/tsukuroi-census.sh > base.sh
$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 4476620…:tools/tsukuroi-census.sh > impl.sh
$ python3 diffscope.py            # see diffscope.out
KILL RULE (hunk outside probe_packages/probe_update_safety/run_selftest): does not fire
numstat: +33 -8 lines in tools/tsukuroi-census.sh
$ bash -n base.sh && bash -n impl.sh
base: bash -n OK
impl: bash -n OK
```

Receipts (all under `.ufo/waves/round-42/w1/C1ExecDiffScope/`): `diffscope.py` (the script, pasted below),
`diffscope.out` (its stdout), `census-U0.diff` (the exact `-U0` diff analyzed), `crosscheck.log`
(blob↔file sha256, `bash -n`, independent `sed`+`sha256sum` of `probe_storage_arm`, numstat, hunk/label
counts, impl commit subject, the section "score-selftest-mounts-r41.py in this range?", and the appended
heredoc-vs-changed-line section), `heredoc-evidence.py` (the script producing that appended section),
`base.sh`, `impl.sh`
(the two extracted revisions; 179 KB / 181 KB, each under the 2 MB receipt cap).

```
sha256 of the receipts (as copied, before scratch removal):
  646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95  base.sh
  5dbdbe93fd3a45cdd602653b6d6821eba748b500f06566c597c81ab6aa2c4feb  census-U0.diff
  a2482fb5751dde5145d45cb9f01e92aafbed2204ffb0511938a109b6510fb4b3  crosscheck.log
  af4c03cc5f7a1522700f635e841cc59b66358856e5363c1d61f3ce32bc676f5a  diffscope.out
  4e06aec91b9d604057abfae43ae7354b6390632ecfb5d3cbb81e5914b5702842  diffscope.py
  5600f40986f84f14c7c98b7f52ed09b263a94e5b97c12bdce232df9844ff4cb0  heredoc-evidence.py
  46d62a24709ece8efbcd231f4c269bd5b3791237e3c78ac7433fb0115494f1b1  impl.sh
```
`base.sh` / `impl.sh` digests are the same values printed by `git cat-file blob <rev>:tools/tsukuroi-census.sh
| sha256sum` for the two revisions, so the hashed inputs are provably the committed content.

## Script (as run)

```python
#!/usr/bin/env python3
"""C1-5 kill-rule scope check: map every U0 diff hunk of tools/tsukuroi-census.sh
(base c8efaa3 -> impl 4476620) to its enclosing top-level function, computed from the
impl file's own `^name() {` headers and `^}` closers, heredoc-aware. Then sha256 each
function body at both revisions and report which differ."""
import hashlib, re, subprocess, sys

BASE, IMPL = "base.sh", "impl.sh"

HEREDOC = re.compile(r"<<-?\s*(['\"]?)([A-Za-z_][A-Za-z0-9_]*)\1")
FUNC    = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*\(\)\s*\{")
CLOSE   = re.compile(r"^\}$")

def scan(lines):
    """Return (list of (name,start,end)), set of heredoc-content line numbers (1-based)."""
    funcs, stack, cur, hd, hd_body = [], [], None, [], set()
    i = 0
    while i < len(lines):
        ln = lines[i]; no = i + 1
        if hd:
            hd_body.add(no)
            if ln.strip() == hd[0]:
                hd = None
            i += 1; continue
        m = HEREDOC.search(ln)
        if m:
            hd = (m.group(2),)
            i += 1; continue
        mf = FUNC.match(ln)
        if mf:
            if cur is not None:
                funcs.append(cur); stack.append(cur)
            cur = [mf.group(1), no, None]
            if ln.rstrip().endswith("}"):   # single-line definition, e.g. `have() { ...; }`
                cur[2] = no; funcs.append(tuple(cur)); cur = None
            i += 1; continue
        if CLOSE.match(ln) and cur is not None:
            cur[2] = no
            funcs.append(tuple(cur)); cur = None
        i += 1
    if cur is not None:
        funcs.append(tuple(cur))
    return funcs, hd_body

def load(path):
    with open(path, "r", encoding="utf-8", errors="surrogateescape") as f:
        return f.read().split("\n")

def digest(lines, start, end):
    # trailing newline per line, body inclusive
    blob = "".join(l + "\n" for l in lines[start-1:end])
    return hashlib.sha256(blob.encode("utf-8", "surrogateescape")).hexdigest()

def main():
    bl, il = load(BASE), load(IMPL)
    bfuncs, bhdb = scan(bl)
    ifuncs, ihdb = scan(il)
    for tag, fs, n in (("base", bfuncs, len(bl)), ("impl", ifuncs, len(il))):
        bad = [f for f in fs if f[2] is None]
        if bad:
            print(f"PARSE-ERROR {tag}: unclosed {bad}"); sys.exit(2)
        for a, b in zip(fs, fs[1:]):
            if a[2] >= b[1]:
                print(f"PARSE-ERROR {tag}: overlap {a} / {b}"); sys.exit(2)
        print(f"parsed {tag}: {len(fs)} top-level functions over {n} lines, "
              f"{len(bhdb if tag=='base' else ihdb)} heredoc-content lines")

    ihash = {n: digest(il, s, e) for n, s, e in ifuncs}
    bhash = {n: digest(bl, s, e) for n, s, e in bfuncs}

    # hunk headers and new-side ranges from git diff -U0
    diff = subprocess.run(
        ["git", "-C", "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin", "diff", "-U0",
         "c8efaa3f120834541f8de1e5e0367e8d1593bae6",
         "447662088dfd3155e31aed239179a79c1d1046c7",
         "--", "tools/tsukuroi-census.sh"],
        capture_output=True, text=True, check=True).stdout
    H = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$")
    allowed = ("probe_packages", "probe_update_safety", "run_selftest")
    print("\nHUNKS (impl-side line numbers, enclosing function from impl spans):")
    fired, touched, n = False, set(), 0
    for line in diff.split("\n"):
        m = H.match(line)
        if not m:
            continue
        n += 1
        bstart, bcnt, istart, icnt = (int(m.group(1)), int(m.group(2) or 1),
                                      int(m.group(3)), int(m.group(4) or 1))
        rng = list(range(istart, istart + icnt)) if icnt else [istart]
        owners = []
        for ln in rng:
            own = [f[0] for f in ifuncs if f[1] <= ln <= f[2]]
            owners.append((ln, own[0] if own else "TOP-LEVEL/OUTSIDE"))
        uniq = sorted({o for _, o in owners})
        githint = m.group(5).strip()
        ok = all(o in allowed for o in uniq)
        if not ok:
            fired = True
        touched.update(uniq)
        print(f"  hunk {n}: '@@ -{bstart},{bcnt} +{istart},{icnt} @@' git-hint={githint!r} -> "
              f"lines {rng[0]}..{rng[-1]} owner={uniq} {'IN-SCOPE' if ok else 'OUT-OF-SCOPE <<< KILL'}")
        for ln, o in owners:
            print(f"      {ln}: {o}")
    print(f"\nKILL RULE (hunk outside probe_packages/probe_update_safety/run_selftest): "
          f"{'FIRES' if fired else 'does not fire'}")
    print(f"touched functions: {sorted(touched)}")

    print("\nPER-FUNCTION sha256 (base c8efaa3 vs impl 4476620; body lines start..end incl. `}`):")
    names_b = [f[0] for f in bfuncs]; names_i = [f[0] for f in ifuncs]
    print(f"  same function list: {names_b == names_i}")
    diff_names = []
    for name, s, e in ifuncs:
        bs, be = next((f[1], f[2]) for f in bfuncs if f[0] == name)
        same = bhash[name] == ihash[name]
        if not same:
            diff_names.append(name)
        print(f"  {'DIFF' if not same else 'same'}  {name:<22} base {bhash[name][:16]} (L{bs}-{be})  "
              f"impl {ihash[name][:16]} (L{s}-{e})")
    print(f"\nfunctions whose bytes changed: {diff_names}")
    print(f"changed-function set == allowed set: {set(diff_names) == set(allowed)}")
    print(f"probe_storage_arm identical: {bhash.get('probe_storage_arm') == ihash.get('probe_storage_arm')}")
    unn = [n for n in diff_names if n not in allowed]
    print(f"unexpected changed functions: {unn}")

    # ---- parser self-validation: contiguity, closers, balance, gap purity ----
    for tag, lines, fs in (("base", bl, bfuncs), ("impl", il, ifuncs)):
        assert [f[1] for f in fs] == sorted(f[1] for f in fs), tag
        for name, st, en in fs:
            tail = lines[en-1]
            assert tail == "}" or (st == en and tail.rstrip().endswith("}")), (tag, name, en, tail)
            assert FUNC.match(lines[st-1]) or lines[st-1].startswith(name), (tag, name, st)
        gaps = [(fs[k][2], fs[k+1][1]) for k in range(len(fs)-1)]
        for gs, gn in gaps:
            for k in range(gs+1, gn):
                assert not FUNC.match(lines[k-1]) and lines[k-1] != "}", (tag, "gap", k, lines[k-1])
        bal = sum(l.count("{") - l.count("}") for k,l in enumerate(lines,1) if k not in (bhdb if tag=="base" else ihdb))
        print(f"validate {tag}: closers ok, gaps pure, brace balance (heredoc-excluded) = {bal}")
    num = subprocess.run(['git','-C','/home/vgpnk/Projects/shokunin/tsukuroi-shokunin','diff','--numstat',
        'c8efaa3f120834541f8de1e5e0367e8d1593bae6','447662088dfd3155e31aed239179a79c1d1046c7',
        '--','tools/tsukuroi-census.sh'],capture_output=True,text=True).stdout.strip()
    add, dele = num.split("\t")[:2]
    print(f"numstat: +{add} -{dele} lines in tools/tsukuroi-census.sh")

if __name__ == "__main__":
    main()
```

## Full output (diffscope.out)

```
parsed base: 26 top-level functions over 3177 lines, 85 heredoc-content lines
parsed impl: 26 top-level functions over 3202 lines, 85 heredoc-content lines

HUNKS (impl-side line numbers, enclosing function from impl spans):
  hunk 1: '@@ -692,1 +692,4 @@' git-hint='probe_packages() {' -> lines 692..695 owner=['probe_packages'] IN-SCOPE
      692: probe_packages
      693: probe_packages
      694: probe_packages
      695: probe_packages
  hunk 2: '@@ -694,1 +697,1 @@' git-hint='probe_packages() {' -> lines 697..697 owner=['probe_packages'] IN-SCOPE
      697: probe_packages
  hunk 3: '@@ -1621,1 +1624,1 @@' git-hint='probe_update_safety() {' -> lines 1624..1624 owner=['probe_update_safety'] IN-SCOPE
      1624: probe_update_safety
  hunk 4: '@@ -1635,2 +1638,2 @@' git-hint='probe_update_safety() {' -> lines 1638..1639 owner=['probe_update_safety'] IN-SCOPE
      1638: probe_update_safety
      1639: probe_update_safety
  hunk 5: '@@ -1641,2 +1644,2 @@' git-hint='probe_update_safety() {' -> lines 1644..1645 owner=['probe_update_safety'] IN-SCOPE
      1644: probe_update_safety
      1645: probe_update_safety
  hunk 6: '@@ -1652,1 +1655,1 @@' git-hint='probe_update_safety() {' -> lines 1655..1655 owner=['probe_update_safety'] IN-SCOPE
      1655: probe_update_safety
  hunk 7: '@@ -2346,0 +2350,10 @@' git-hint='STUB' -> lines 2350..2359 owner=['run_selftest'] IN-SCOPE
      2350..2359: run_selftest   (10 lines)
  hunk 8: '@@ -2542,0 +2556,12 @@' git-hint='STUB' -> lines 2556..2567 owner=['run_selftest'] IN-SCOPE
      2556..2567: run_selftest   (12 lines)

KILL RULE (hunk outside probe_packages/probe_update_safety/run_selftest): does not fire
touched functions: ['probe_packages', 'probe_update_safety', 'run_selftest']

validate base: closers ok, gaps pure, brace balance (heredoc-excluded) = 0
validate impl: closers ok, gaps pure, brace balance (heredoc-excluded) = 0
numstat: +33 -8 lines in tools/tsukuroi-census.sh
```
(The two `run_selftest` hunk bodies are reproduced line-by-line in `diffscope.out`; condensed here only to
keep the table readable — the receipt has every line, and the per-function table above is verbatim.)

## What I did NOT do

- Did not run the census, the 130-case selftest, or any of the three frozen counters — the L1 owns gate
  execution, and only one counter may run at a time. So this report says nothing about whether the
  predicate holds or whether `tools/score-selftest-mounts-r41.py` still passes (kill rule 3).
  Supporting fact only, from the diff: `tools/score-selftest-mounts-r41.py` is **not** in the changed-file
  set of c8efaa3→4476620 (`grep`-filtered `--name-only` output 0 matches; `crosscheck.log`, section
  "score-selftest-mounts-r41.py in this range?"),
  i.e. the file that rule names is byte-unchanged in this commit.
- Did not evaluate the semantics of the replacement idioms (here-string vs `grep -q`, `awk NR` vs `head -n`)
  — that is C1-3/C1-4's ground, not this item's.

## Limits of this evidence

- Span assignment depends on the script's formatting convention: column-0 `name() {` headers and column-0
  `}` closers. Both files satisfy it (26/26 spans closed; gap regions contain no header or closer;
  heredoc-excluded brace balance 0; `bash -n` clean on both), so no changed line can be silently attributed
  to a neighbour. Residual risk is a change hidden in heredoc *content* — but neither revision marks any
  changed or removed line as heredoc content (`changed impl/base lines that are heredoc content: none`),
  and heredoc content in `run_selftest` is fixture text that would appear as its own hunk (it does not).
- Line-number granularity is per changed line, so an allowed function with a one-line edit anywhere inside
  it reads as in scope even if the edit were semantically unrelated to the codesite; I flag that the scope
  rule is structural, not semantic. Spot-read of the diff content: hunk 1–2 are the `-Qkk` `grep -q`/
  `grep -m1` here-strings, hunks 3–6 are the four `-Qu`/`-Sup`/`-Suu` name extractions, hunks 7–8 are the
  two large-output `check` cases — all four families the claim names.
