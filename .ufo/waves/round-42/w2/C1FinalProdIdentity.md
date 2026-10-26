VERDICT: supports — both declared expectations reproduce at production identity, and the ns-gated V1 arm is separated only there.

# F-3 — production-identity leg (seat C1FinalProdIdentity)

Re-run of `.ufo/waves/round-42/w1/C1CritNsView.md` §4 against the census at the dispatch tip
`78abb8b5cdc9da511b4fc523e661517a68dd33d3` and at the base `c8efaa3f120834541f8de1e5e0367e8d1593bae6`, plus the
V1 `ns-gated` arm at the same identity. Driver: `w1/C1CritNsView/uid1000.py` **unmodified**
(sha256 `b7fd191741c13ba32e6822f157f92e8c6cf8ee62b395578f08f0272dd5420bdf`, copy in this seat dir). No sudo, no
pacman, no host mutation; every mount lived inside a private `unshare` namespace.

## 1. Bytes under test

Extracted read-only with `git -C <lane> show <rev>:tools/tsukuroi-census.sh`:

| label | revision | sha256 | lines |
|---|---|---|---|
| `tip.sh` | `78abb8b5` (dispatch tip) | `7c9f79036782de951a69325fe6f5cc742d8acac4de389626026bc33d8f7877f9` | 3221 |
| `base.sh` | `c8efaa3f` (base) | `646c84fcdc166dd4f5321a467e60036d785c106f061dd4fa7849424696f9eb95` | 3177 |
| `fix447.sh` | `447662088` (C1 fix commit) | `46d62a24709ece8efbcd231f4c269bd5b3791237e3c78ac7433fb0115494f1b1` | 3201 |

The lane's working-tree `tools/tsukuroi-census.sh` hashes to `7c9f7903…` as well (lane HEAD at my run was
`a968393c`, i.e. later than the dispatch tip), so the tip row below is the census the lane carries today, not
only a historical blob. The base carries the round-41 early readers at `base.sh:692` (`printf '%s\n' "$s_out" |
grep -q '^error:'`) and `base.sh:694` (`… | grep -m1 '^error:'`); the tip replaces them with the whole-input awk
reader at `tip.sh:698` and the declared fix commit with a here-string pair at `fix447.sh:695-697`.

Probe text is the driver's own: `small` = **126 B** of `-Qkk` output, `large` = **1,048,712 B**, both starting
with `error: alpha: /usr/bin/x-<6-hex-token> (Permission denied)`, `-Qkk` rc=1 (sizes measured with
`python3 -c "import uid1000 as m; len(m.qkk(True|False, 'tok'))"` in the scratch copy of the driver). A fresh random token per run.

## 2. Identity of the leg (what "production identity" means here)

`probe.sh` run through the same driver, receipt `probe-identity.txt:1-2`:

```
PLANE packages: PROBE id=1000 euid=1000 tsk_vars=0 home=/mnt/home tmpdir=/mnt/tmp cwd=… nenv=7 sh=/mnt/census
```

uid/euid 1000, **zero** `TSUKUROI_*` variables, 7 environment entries. Control at the counter's identity
(`capture.py --uid0`, plain `unshare -rm`), `uid0-identity.txt:3`: `id=0 euid=0 tsk_vars=0 … nenv=7`.

## 3. Result table (all runs, `PLANE packages:` first token)

| census | uid | `-Qm` arm | large | small | receipt |
|---|---|---|---|---|---|
| tip `78abb8b` | 1000 | real pacman | **BLOCKED** | **BLOCKED** | `uid1000-tip.txt:1-2`, `tip-uid1000.txt:3,6`, `tip-uid1000-cleanforeign.txt:3,6` |
| tip `78abb8b` | 0 | real pacman | BLOCKED | BLOCKED | `tip-uid0-real.txt:3,6` |
| base `c8efaa3` | 1000 | real pacman | **DEGRADED** | **BLOCKED** | `uid1000-base.txt:1-2`, `capture-base.txt:3,6` |
| base `c8efaa3` | 1000 | clean stub | **HEALTHY** | **BLOCKED** | `capture-base-cleanforeign.txt:3,6` |
| base `c8efaa3` | 0 | clean stub | HEALTHY | BLOCKED | `base-uid0-cleanforeign.txt:3,6` |
| fix `4476620` | 1000 | clean stub | BLOCKED | BLOCKED | `fix447-uid1000-cleanforeign.txt:3,6` |
| V1 @ `4476620` | 1000 | real pacman | **DEGRADED** | **BLOCKED** | `uid1000-v1-447.txt:1-2` |
| V1 @ `4476620` | 1000 | clean stub | **HEALTHY** | BLOCKED | `v1447-uid1000-cleanforeign.txt:3` |
| V1 @ tip `78abb8b` | 1000 | real pacman | **DEGRADED** | **BLOCKED** | `uid1000-v1-tip.txt:1-2`, `v1tip-uid1000.txt:3,6` |
| V1 @ tip `78abb8b` | 1000 | clean stub | **HEALTHY** | BLOCKED | `v1tip-uid1000-cleanforeign.txt:3` |
| V1 @ tip `78abb8b` | 0 | real pacman | **BLOCKED** | **BLOCKED** | `v1tip-uid0-real.txt:3,6` |
| V1 @ tip `78abb8b` | 0 | clean stub | **BLOCKED** | **BLOCKED** | `v1tip-uid0-cleanforeign.txt:3,6` |

Both declared expectations hold exactly: **tip BLOCKED/BLOCKED**, **base DEGRADED-or-HEALTHY/BLOCKED**.

The judgement-bearing lines, verbatim:

```
uid1000-tip.txt:1   large rc=2 PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: alpha: /usr/bin/x-47cae2 (Permission denied); …
uid1000-base.txt:1  large rc=2 PLANE packages: DEGRADED (pacman -Qkk rc=1 sample=4(alpha,beta,gamma,delta) drift=0 backup_diffs=0 nonroot_artifacts=1; foreign=21(…
uid1000-base.txt:2  small rc=2 PLANE packages: BLOCKED (pacman -Qkk sample probe error: error: alpha: /usr/bin/x-c0045d (Permission denied); …
```

Stability: the base `-Qm`-real arm ran three times (tokens `c0045d`, `967939`, `58be0c`) with `DEGRADED` every
time; the base clean-stub arm twice (`36c312`, `bc391f`) with `HEALTHY` every time; the tip four times with
`BLOCKED` every time. `capture-base.txt` was re-shot with the shipped `capture.py` after the helper reached its
final hash, so every receipt above reproduces from the scripts in this seat dir.

**Why the `-Qm` column exists.** In the uid-1000 legs the real `-Qm` probe is answered by the host and the
foreign-watch fold fires (`foreign=21(known=3 new=5 drift=13 gone=0)`, `capture-base.txt:3`), which by itself
produces `DEGRADED`. That is not the defect under test, so I added one stub case (`capture.py --qm-clean`) in
which `-Qm` answers with the census's *own* embedded `R6_FOREIGN_BASELINE` (`base.sh:481`, 16 rows, identical at
tip and base — same 46-line region hash `2bbeacf3…`). With the foreign arm quiet the packages plane's own verdict
is the only thing left: base/V1 read `HEALTHY` on a 1 MiB error-bearing sample where the tip reads `BLOCKED`.

## 4. The V1 arm is separated by this leg, and only by this leg

`mkvariant.py` (w1, sha256 `3b82a6fe…`) applied cleanly to the fix-commit census (`v1-447.diff`, 1386 B) — its
anchors are that commit's here-string text. It does **not** apply at the tip: the tip replaced that pair with the
awk reader (`tip.sh:698`), so `mkvariant.py` exits on its uniqueness assertion there, measured:
`mkvariant-anchor-check.txt:1` = `anchor not unique (0): '  if grep -q '^error:' <<<"$s_out"; then …'`.
`mkvariant-tip.py` (this seat, sha256 `a30ec0a5…`) is the same arm with the tip anchor: `tsk_watched()` = "fixture
override set, or uid 0"; watched → the tip's awk reader; unwatched → the round-41 `printf | grep -q` /
`printf | grep -m1` pair (`v1-tip.diff`, 1367 B). Semantics are unchanged from w1's V1; only the anchor text moved.

Four-way contrast with the same fabricated view:

- at uid 0 (the counter's own leg shape, `tools/score-size-invariance-r42.py:273-283`: `unshare -rm`, no
  `setpriv`, no uid mapping anywhere in the file — `grep -n 'setpriv\|id -u\|map-users'` returns nothing):
  base = `HEALTHY`, V1 = `BLOCKED`, tip = `BLOCKED`. So the uid-0 view *is* sensitive to the base defect; it is
  not leg insensitivity that hides V1.
- at uid 1000: base = `DEGRADED` (real `-Qm`) / `HEALTHY` (quiet foreign arm), V1 = the same pair, tip =
  `BLOCKED` in every arm.

V1 is therefore a census that is broken in production while reading exactly like the fixed tip under every
observation the counter can make. The production-identity leg is what separates it, and it does so on both the
fix commit (V1@447 `HEALTHY` vs fix447 `BLOCKED`) and the dispatch tip (V1@tip `HEALTHY` vs tip `BLOCKED`).

Note the ordering of the gate: at uid 0 V1 is `BLOCKED` while the base is `HEALTHY`, i.e. the gate opens exactly
on the identity the instrument runs under. Nothing about the gate is visible to the counter.

## 5. Mechanism, measured independently of the census

`probe2.sh` at uid 1000, receipt `pipe-mechanism.txt:3-6` (identical in both driver passes):

```
PLANE packages: PIPE small     len=     89 pipestatus=[0 0]
PLANE packages: PIPE mid       len=  52250 pipestatus=[0 0]
PLANE packages: PIPE big       len= 696050 pipestatus=[141 0]
PLANE packages: AWK  big       len= 696050 rc=0 first=error: alpha: /usr/bin/x-PROBE (Permissi
```

The base's verdict flip is `pipefail` + `SIGPIPE` on the early reader: `printf` dies with 141 once the buffer
exceeds the pipe capacity, the `if` reads false, and the error line is never reported. Measured pipe capacity on
this host: `pipe_buf_size= 65536`. The single-write 89 B and 52,250 B buffers complete before `grep -q` exits;
696,050 B and 1,048,712 B do not. The tip's awk reader on the same 696,050 B buffer exits 0 and returns the line.

So the size threshold is real and sits at the 64 KiB pipe buffer, which also bounds the defect's live
reachability: the base's 126 B case and w1's measured default live sample (617 B for 8 packages,
`w1/C1CritNsView/live-sample.txt`) are both in the `[0 0]` regime. At production identity the packages arm
therefore produces a **wrong verdict**, not an exit 141 — the 141 mode belongs to the assignment-site half of the
declaration (the `-Qu`/`-Sup`/`-Suu` extractions), which I did not exercise.

## 6. What this supports, and what it does not settle

Supports, from my own runs:
- C1's substance holds at the dispatch tip **at production identity**: a 1 MiB `-Qkk` probe whose first line is
  a permission error reads `BLOCKED` as uid 1000 with no `TSUKUROI_*` override (`uid1000-tip.txt:1`), and the
  same holds at the declared fix commit (`uid1000-fix447.txt:1`). The fix is unconditional, not view-gated.
- The base reproduces the defect at production identity: `DEGRADED`, and with the foreign arm quieted,
  `HEALTHY`, on a 1 MiB error-bearing sample.
- w1 §4's production-identity result reproduces token-for-token: same verdicts, same note shapes, both
  revisions, and stable across repeated runs with fresh random tokens.
- The tip carries selftests for exactly this: `tip.sh:2360` `check 'blocked: a sample error ahead of a large -Qkk
  output still blocks (R42-C1)'` (4000 warning lines ≈ 300 KB) and the three update-safety large cases at
  `tip.sh:2567,2577,2584`.

Does not settle (unchanged from w1 §2/§7, and my leg closes only the first of these):
- uid is the *only* production channel this leg closes. The fabricated package names (`alpha beta gamma delta`),
  `/proc/self/mountinfo`, the stub's shell text and `$0` remain readable, so a census can still be written to
  detect the view by data rather than by identity. w1's V3 arm is that case; I did not re-run it.
- I did not run the frozen counter (`tools/score-size-invariance-r42.py`, sha256 `c511104a…`, matches
  `SCORECARD.md:2573`) in this seat. The claim "V1 scores PASS on the frozen predicate" rests on w1's
  `variant.jsonl`/`variant2.jsonl`; what I measured is the other half — the production-identity numbers that
  predicate cannot see.
- The four update-safety C1 sites were not exercised at uid 1000 (their trigger is a `-Qu`/`-Sup`/`-Suu` buffer,
  not `-Qkk`); the packages site is the one C1 declares a counter measurement for.

## 7. Not done / limits of this seat

- No counter run (see §6). No pacman, no sudo, no service, no sysfs, no `btrfs` command; nothing outside a
  private `unshare` namespace was mounted or written. No tool installs or upgrades were needed.
- `root_uid=65534` in every receipt is the userns overflow uid for the host's uid 0, not a host observation; it
  is identical in all arms and does not enter any verdict.
- The `large`/`small` fixtures are the driver's synthetic `-Qkk` text, so this measures verdict logic under
  production *identity*, not against real `pacman -Qkk` output.
- `[INFERENCE]`: that the live default sample can never exceed 64 KiB follows from w1's 617 B/8-package
  measurement and my 64 KiB capacity measurement; I did not construct a live over-threshold probe (the only
  route is `TSUKUROI_SAMPLE_N=`, a user-visible channel).
- Scratch `/fast/scratch/hyaku/tsukuroi-r42/C1FinalProdIdentity/` removed at the end; all receipts copied here.

## 8. Receipts (this seat dir)

`uid1000-tip.txt`, `uid1000-base.txt`, `uid1000-v1-tip.txt`, `uid1000-v1-447.txt`, `uid1000-fix447.txt` (w1
driver verbatim) · `tip-uid1000.txt`, `tip-uid1000-cleanforeign.txt`, `tip-uid0-real.txt`,
`capture-base.txt`, `capture-base-cleanforeign.txt`, `base-uid0-cleanforeign.txt`,
`v1tip-uid1000.txt`, `v1tip-uid1000-cleanforeign.txt`, `v1447-uid1000-cleanforeign.txt`,
`fix447-uid1000-cleanforeign.txt`, `v1tip-uid0-real.txt`, `v1tip-uid0-cleanforeign.txt` (full-output captures) ·
`probe-identity.txt`, `uid0-identity.txt`, `pipe-mechanism.txt`, `mkvariant-anchor-check.txt` · `v1-447.diff`, `v1-tip.diff` ·
scripts: `uid1000.py`, `mkvariant.py` (w1 copies), `capture.py` (`6c640007…`), `mkvariant-tip.py`
(`a30ec0a5…`), `probe.sh` (`10b6c0af…`), `probe2.sh` (`a76991e4…`) · `hashes.txt` (sha256 of every file).

Reproduce: `python3 uid1000.py <census> <token>`; `python3 capture.py <census> <token> <tag> [--uid0]
[--qm-clean]`.
