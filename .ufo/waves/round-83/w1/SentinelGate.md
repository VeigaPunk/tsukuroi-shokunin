# SentinelGate — round 83 w1 (security & bounds review)

Seat: SentinelGate-6 · frozen commit `d78b3b3982b5df62286dd65b0a42ae8a91847608` · scratch `/fast/scratch/hyaku/tsukuroi-r83/SentinelGate` (399G free, ENOSPC never hit). All runs were made in a `--shared` scratch clone checked out at the frozen commit; the lane itself was only ever read. No tools were installed (none needed).

Provenance first: worktree instrument bytes are byte-identical to the frozen manifest `.ufo/waves/round-83/before/instrument-sha256.txt` — 5/5 sha256 match (anchor `b1e208af…`, ordinals `abc7e037…`, mutation `91ee1417…`, battery `bf06ba63…`, mutants-r83.json `499c594b…4f09`), and `sha256sum -c SHA256SUMS` in the clone's `before/` reports 12/12 `OK`, `EXIT=0`. Lane HEAD was already `d78b3b3982b5df62286dd65b0a42ae8a91847608` (read-only `rev-parse`).

## Check 1 — Write-bounds (battery + 3 r83 selftests in scratch clone)

Commands (cwd = `$S/lane`, `TMPDIR=$S`):
- `python3 tools/round83-battery.py --instrument r83 --revision d78b3b3982b5df62286dd65b0a42ae8a91847608` → `EXIT=0`; JSON: `"C1_depth": {"passed": 3, "of": 3 … "finding": "met"}`, `"C2_calibration": {"passed": 4, "of": 4 … "finding": "met"}` (legs C1.a rc2 cannot-evaluate digest-mismatch `declared-afbf3be663b1:actual-c718576fcce8`; C1.b rc0 8/8; C1.c rc0 8/8; C2.a rc1 count1; C2.b rc0 count0; C2.c rc0 count0; C2.d rc2 JSON `absent-at-revision:SCORECARD.md`).
- `python3 tools/check-anchor-coordinates-r83.py --selftest` → `EXIT=0`, `SELFTEST total=16 passed=16 failed=0`.
- `python3 tools/check-ordinals-r83.py --selftest` → `EXIT=0`, `SELFTEST total=11 passed=11 failed=0`.
- `python3 tools/mutation-kill-r83.py --selftest` → `EXIT=0`, `SELFTEST total=6 passed=6 failed=0` (incl. red arm `timeout-is-not-a-kill: killed=0 rc=None detail=selftest-timeout:exceeded-2s`).

Bounds evidence:
- Clone `git status --porcelain --ignored` before the runs: **empty (clean)**. After all four runs: **empty**, `EXIT=0`. Nothing written in the clone; no `__pycache__` created by these runs (`tools/round83-battery.py:38`, `:46` anchor, `:44` ordinals, `:50` mutation all set `sys.dont_write_bytecode = True`, and battery children get `PYTHONDONTWRITEBYTECODE=1` via `ENV`, `round83-battery.py:45-46,52`). The three `.pyc` files under `.ufo/waves/round-44/w1/ConsiderMine/pycache/` are **tracked content at the frozen revision** (clean status proves they predate; not writes of this wave).
- Lane `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain --ignored -- tools/ .ufo/waves/round-83/before/`: before **empty**, after the runs **empty**, `EXIT=0`; tool mtimes unchanged (04:47–04:49, all before my 05:07 runs). Full-lane baseline diff (16 untracked lines) is sibling-seat wave-dispatch traffic (`w1-dispatch.json`, `w1/`, …), unchanged by me.
- Scratch after runs: only `lane/` + empty `receipts/` — battery `mkdtemp("r83-battery-")` removed in `finally` (`round83-battery.py:103,125`); `/tmp` scan for `r83-battery-*`, `anchor83-*`, `mutkill83-*` residue: no matches (ls `EXIT=2`).

**Verdict: PASS.** Zero mutation inside the clone beyond its own checkout, zero in the lane, no `__pycache__`.

## Check 2 — Credential-shaped material

Regex scan (grep, gitignore off) over the 4 tools + `.ufo/waves/round-83/before/` (incl. fixture subdirs):
- `op://|-----BEGIN|ghp_|AKIA|password=` → **No matches found**.
- `\bsk-[A-Za-z0-9_\-]{8,}|token=|cookie|session_id` (case-insensitive) → **No matches found**.
- Private IPs `\b(10\…|192\.168\…|172\.(1[6-9]|2[0-9]|3[01])\…|127\…)\b` → **No matches found**.

**Verdict: PASS — zero hits.**

## Check 3 — Environment hygiene

Every subprocess environment site (file:line):
- `tools/round83-battery.py:45-46` — `ENV = {"PATH": "/usr/bin:/bin:/usr/local/bin", "LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}`; used at `:52` (`env={**ENV, "TMPDIR": env} if env else ENV`). **Scrubbed; does not forward parent env.**
- `tools/mutation-kill-r83.py:80-81` — `env = {"PATH": …, "TMPDIR": str(work), "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C.UTF-8"}` used at `:86`. **Scrubbed** (the R82-V6 standard per docstring `:23-25`).
- **FINDING (low): parent env is forwarded to `git` children at 4 sites** — no `env=` argument means verbatim inheritance of `HOME`, `GIT_*`, and any exported secrets: `round83-battery.py:107-118` (six git calls building the C2.d fixture repo, incl. the only write-capable child, `git commit` `:113-114`), `check-anchor-coordinates-r83.py:126-130` (`git show`), `check-ordinals-r83.py:223-226` (`git show`), `mutation-kill-r83.py:69-72` (`git show`). Exploit path: an odd/hostile parent env (e.g. `GIT_CONFIG_GLOBAL`, or `core.hooksPath`/`init.templateDir` via inherited `HOME`) can redirect object reads or execute hook code during the battery's fixture commit, and secrets ride along into every child. Severity low: local seat-owned parent env, no network egress in the tools.
- `resume_continuity_v1`: `grep -r resume_continuity tools/` → **no matches**; the mechanism does not exist in this round's instruments, so there is no rejection path to adversarially verify.

Proposed smallest patch (written to scratch, **not** applied; L1 decides): `/fast/scratch/hyaku/tsukuroi-r83/SentinelGate/patch-env-hygiene-git-subprocess.diff` — pass the same scrubbed dict as `env=` at the four git call sites.

**Verdict: FINDING (low) — python children scrubbed, git children inherit parent env.**

## Check 4 — Path confinement

- Battery: `root = Path(__file__).resolve().parent.parent` (`:134`); reads only `INSTRUMENTS` tool paths (`:40-43`) and `FIXTURES = .ufo/waves/round-83/before` (`:44`) under that root. Writes: only `tempfile.mkdtemp(prefix="r83-battery-")` (`:103`) + fixture repo inside it (`:105-118`), removed `:125`. Note (informational): `ENV` carries no `TMPDIR`, so battery *children* default their tempdirs to `/tmp` — self-cleaning (`TemporaryDirectory`), no residue observed, all well under 50 MB.
- `check-anchor-coordinates-r83.py`: reads `ENTRY` (`:48`) + `SNAPDIR/snapshot` (`:49`) beneath the `--fixture`/`--repo` root (`load()` `:142-166`: `base / ENTRY`, `base / SNAPDIR / snapshot`) or, with `--revision`, via `git show rev:path` only (`:126-130`). Digest gate `bind_digest` runs before any scoring (`load()`), refusing `snapshot-digest-mismatch/undeclared`. **Writes: none.** Confined.
- `check-ordinals-r83.py`: reads exactly one `--fixture` file (`:269`) or `SCORECARD.md` via `git show` (`:222-226`); all else is in-memory regex. **Writes: none.** Confined.
- `mutation-kill-r83.py`: reads `RECIPES` (`:52`), `tools/<recipe.tool>` and `tools/_revision.py` (`:53`, via `read_at` `:63-74`) beneath root. Writes only under `scratch = Path(work) or mkdtemp("mutkill83-")` (`:116`; files `:122-146`), `shutil.rmtree` on exit (`:155-156`), child `TMPDIR=work` (`:80-81`). Informational: `tools/{tool}` is a recipe-controlled join, so a malicious recipe could name a traversing path — but the recipes are sha-pinned operator bytes (`499c594b…4f09`), so not reachable this round.

**Verdict: PASS (2 informational notes, no out-of-bounds read or write found).**

## Summary

| Check | Verdict |
|---|---|
| 1 Write-bounds (battery + 3 selftests, clone & lane) | PASS — C1 3/3, C2 4/4, selftests 16/16, 11/11, 6/6, all `EXIT=0`; zero lane mutation |
| 2 Credential-shaped material | PASS — 0 hits |
| 3 Environment hygiene | FINDING (low) — 4 git call sites inherit parent env (`round83-battery.py:107-118`, `check-anchor-coordinates-r83.py:126-130`, `check-ordinals-r83.py:223-226`, `mutation-kill-r83.py:69-72`); patch in scratch |
| 4 Path confinement | PASS — reads/writes confined; 2 informational notes |

Refusals: none. Blocked checks: none — all four ran to completion. Lane left untouched except this report file, which the seat spec names.
