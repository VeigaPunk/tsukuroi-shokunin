# ReviewGate — surgical review of the V3 gate diff (round 93, wave w1)

Seat: reviewer (leaf; no subagent dispatch). Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
read-only. Freeze tip reviewed: `c633f49aa512e1c8a0e0464b7fb5d354c70096cf` (`git rev-parse HEAD`
printed it). Instruments verified before any run:

| instrument | sha256 read | matches |
|---|---|---|
| `tools/check-limine-pins.py` | `6b4c53d1b56f4935cbcad3327259c15dd643af5ecec428522f998b7c5b6260aa` | yes |
| `tools/limine-pin-battery-r93.py` | `ddd7e9550da163575ea5c41416f7fc6effd6dcdea9e477843b9fd759675e1aad` | yes |
| `do-nothing-gate-r92.py` / `do-nothing-battery-r92.py` | `35c1088b…c87f` / `aef33925…614f` | yes |

Scratch: `/fast/scratch/hyaku/tsukuroi-r93/ReviewGate/` (fixtures, fake `limine` binaries,
`--work` dirs; deleted on exit). No lane file edited; no git/jj mutation; no `--live` privileged run;
no tool installed (host tools: `/usr/bin/python3` 3.14.8, `bwrap`, `git`; `limine` never executed by
this seat — its banner was read from `.ufo/waves/round-93/w1/ExecLive.md` and the literal
`Limine 12.9.4` in `/usr/bin/limine`).

Axes under review (Godspeed): **A — refusal-contract integrity of the probe** (does every probe
failure end in rc 64/empty stdout, or can it end in a verdict, a crash, or a wrong era);
**B — control honesty** (does each one-clause bend implement the clause it is named after);
**C — receipt verifiability** (do the frozen manifest, counters, and live receipt reproduce).

## What the diff changes (inventory)

`git diff c633f49a^ c633f49a -- tools/check-limine-pins.py`: +75/−8, and only these sites:

1. docstring: the `auto` paragraph (lines 42-47) and usage (54-58);
2. imports `re`, `subprocess` (70-72);
3. new `probe_limine_version()` (104-118);
4. `check()` gains a trailing keyword `limine_version_source="flag"` and emits it on **both** JSON
   return paths — the unreadable-conf return (194-199) and the normal return (312-313);
5. selftest: `era-exact-first-entry` and the `probe-version` block with `fake_probe` (453-468);
6. `main`: `--limine-version` help (495), the `auto` branch (502-509), the refusal message (511-514),
   and the two `check()` callsites now pass `(version, version_source)` (519, 524).

No line of the era/visibility logic (`lines`/`first_entry`/`in_global`, 214-240), R1-R10, U1, or
`live_secure_boot()` is touched. `check()`'s new parameter is keyword-with-default, so no caller
breaks; a lane-wide search found no in-lane importer of `check` (grep across `tools/`; the r87
battery only names the gate in its docstring and ExecLive's import ran in scratch), so no callsite
is left behind. Verified empirically: `--selftest` **39/39 PASS**, and
three fresh canonical battery runs read **96/96 met, 0 error rows** (all 89 r92 families included).

## Findings

| # | Sev | File:line | One-line defect | One-line fix |
|---|---|---|---|---|
| F1 | medium | `tools/check-limine-pins.py:117` | The probe regex accepts a **suffixed** version (`12.9.6-rc1`) because `\b` matches before `-`, records it as `12.9.6` and selects era B — the exact string the gate *refuses* on the flag path (`REFUSAL-VERSIONS` includes `12.9.5-rc1`). | `re.search(r"(?i)\blimine\s+v?(\d+\.\d+\.\d+)(?![\w.-])", p.stdout)` |
| F2 | medium | `tools/check-limine-pins.py:112` | `text=True` decodes strictly; a probe emitting one non-UTF-8 byte raises `UnicodeDecodeError` (a `ValueError`, not caught by `OSError/SubprocessError`) → traceback, **exit 1**, which collides with the gate's own DEGRADED rc, instead of the contracted rc 64 refusal. | add `errors="replace"` to the `subprocess.run(...)` call |
| F3 | medium | `.ufo/waves/round-93/before/freeze-manifest.sha256:4` | The live worktree no longer satisfies the claim's own `sha256sum -c` check: the plan line FAILS after Amendment A1 was appended to the manifest-covered plan (freeze tip itself is 14/14 OK). | drop the `.ufo/plans/round-93.md` line (the brief counts 13 lines; 13 then verify) and treat the declaration as append-only outside the byte-freeze |
| F4 | medium | `tools/make-r93-bends.py:31` (emitted `N02-first-body.py`) | The N02 bend is named "the era-B cut lands one line late" but the flip lives inside the `startswith("/")` branch, so `lineno == first_entry + 1` never matches an entry line: the era-B cut is **suppressed** for every single-root-entry config (8 families fail, 3 of them from the new roster). The named family is still in `failed_families`, so the frozen target holds. | emit the bend as an insertion before `kv = split_key(raw)`: `in_global = True` when `lineno == first_entry + 1`, or relabel N02 "era-B cut suppressed" in plan/claims |
| F5 | low | `tools/check-limine-pins.py:495,502` | With `--limine-version` **omitted**, JSON says `limine_version_source: "flag"`; the value came from the built-in default, not a flag. | `default=None` and `version, version_source = (a.limine_version, "flag") if a.limine_version is not None else ("12.9.4", "default")` |
| F6 | low | `tools/limine-pin-battery-r93.py:1902,1944,2237` | The ISOLATION launcher execs `sys.executable` **absolutely** (so `<case>/bin` cannot shadow `python3` — the seat's question answers "no"), but bwrap binds only `/usr`; any interpreter outside `/usr` (uv, venv) makes every case fail rc 1 with no diagnostic. | in `main`, `if not sys.executable.startswith("/usr/"): print(...); return 2` |
| F7 | info | `after/live-c2.json` vs `w1/ExecLive/live.stdout` | Two live receipts: the rc 1/pins-30-38 one came from a **privileged** run a seat cannot reproduce (`/boot/limine.conf` is root-only — my `open` gets EACCES); the unprivileged shape is rc 2 CANNOT-EVALUATE with the same `12.9.4`/`probe`. Not a code defect; a verification-boundary note. | cite both receipts; do not present the rc 1 run as seat-reproducible |
| F8 | info | `tools/limine-pin-battery-r93.py:1694-1707` | `AUTO-PROBE-FAIL` alone is satisfiable by any gate that refuses every `auto` value (the r92 do-nothing gate passes it); Amendment A1 already records this and points the discrimination at N06. | keep A1's narrowing in the closure; do not cite AUTO-PROBE-FAIL as a standalone anti-vacuity control |

### F1 — the probe's grammar is looser than the flag's (measured)

Fake `limine` printing `Limine 12.9.6-rc1`, landed gate, r92 first-line-entry fixture:

```
--limine-version auto -> rc 1, stdout {"limine_version": "12.9.6", "limine_version_source": "probe",
                         "visibility_era": "12.9.5+", pins [[3,LP-MISMATCH,panic]]}
--limine-version 12.9.5-rc1 (flag path) -> rc 64, stdout 0 bytes
   (required by the battery's REFUSAL-VERSIONS row, which `met` in my three runs)
```

So the same pre-release string is a usage error when typed and a silently-promoted release when
probed. `limine_version` then records a string the binary did not print. No frozen receipt is
affected (the battery's fakes are unsuffixed; the host prints `Limine 12.9.4`), but a `-rc`/`-git`
build of the boundary release can select the wrong era — the class of error this gate exists to
prevent. The negative lookahead also refuses `Limine 12.9.4-1` (Arch pkgrel), which is the safe
direction: the operator must pass the flag.

### F2 — a non-UTF-8 banner crashes the refusal path (measured)

Fake `limine` = `printf 'Limine 12.9.4\n\377\n'`:

```
rc 1, stdout 0 bytes, stderr: subprocess._translate_newlines ... UnicodeDecodeError:
  'utf-8' codec can't decode byte 0xff in position 14
```

The claimed contract is "a failed probe … is a usage error (rc 64, no verdict)" (gate docstring
45-47; C2 predicate). Here the probe *succeeded* in finding a version but the decode killed the
process; `rc 1` is also the gate's DEGRADED verdict code, so a consumer keyed on rc alone reads a
probe crash as "pin mismatch found". `errors="replace"` makes the banner decode to replacement
characters, the regex still finds `12.9.4`, and every other probe failure keeps its rc 64. The
battery cannot reach this (its fakes print ASCII), so no receipt lies — the product has an
uncontracted hole.

### F3 — the freeze check fails in the live tree (measured)

```
$ sha256sum -c .ufo/waves/round-93/before/freeze-manifest.sha256
... .ufo/plans/round-93.md: FAILED ... 1 of 14
$ git show c633f49a:.ufo/plans/round-93.md | sha256sum   -> 4600cfa3…  (== manifest line 4)
$ sha256sum .ufo/plans/round-93.md                       -> 3668f0e8…
```

The committed blob matches; the worktree plan differs by the appended **Amendment A1** (line 125),
which the plan's own protocol sanctions ("a later narrowing is an appended amendment section"). So
the manifest's inclusion of the mutable declaration is self-contradictory: every legitimate
amendment voids the `sha256sum -c` leg of C1's kill rule. At the freeze tip the check is 14/14 OK
(`w1/ExecAutoReplicate.md`), so instruments are intact; the live tree is not. The wave brief counts
13 lines — exactly the manifest minus the plan line.

### F4 — N02 does not implement its named clause (measured, corroborated)

`make-r93-bends.py:29-31` replaces `lineno == first_entry` with `lineno == first_entry + 1` *inside*
the `if stripped.startswith("/")` branch (gate:220-222), so the cut can only fire when an entry line
immediately follows another entry line. Receipt `after/bend-N02-first-body.json`, 3/3 runs:

```
unmet 88/96 failed: AUTO-ERA-B, ERA-B-FIRST-BODY, ERA-EXACT-125, ERA-FLE-MEASURED-B,
                    ERA-FLE-PANIC-B, GLOBAL-VS-ENTRY, MEASURED-IN-ENTRY, PANIC-AFTER-PIN
```

A true "cut one line late" would fail **only** the first-body-line family; the other seven are
era-B configs whose cut is simply gone. `w1/ReviewBattery/probes-n02-nocut.txt` shows the mechanism
directly (N02 reads the after-body `hash_mismatch_panic: no` at both 12.9.4 and 12.9.6). N01, N03,
N04, N05, N06 are surgical: each fails exactly its named family, 3/3 (receipts cross-checked; my
own one-run checks agree for N01/N05/N06).

### F6 — re-run trap for the battery (measured)

`/home/vgpnk/.local/share/uv/python/cpython-3.13.16-…/bin/python3 tools/limine-pin-battery-r93.py
--gate tools/check-limine-pins.py --usage-check` → all 11 rows `rc 1`, `verdict unmet`, no stderr:
the sandbox cannot exec an interpreter under `/home`. With `/usr/bin/python3` the same run is
`met`. This is loud and deterministic (never a false `met`), but a reviewer using `uv run` would see
"the gate is broken" rather than "the launcher cannot bind this interpreter". Explain the answer to
the seat's shadowing question: `run_gate`/`run_usage` pass `[sys.executable, "-I", gate, ...]` as
inner argv (lines 1902, 1944); `sys.executable` is absolute and bwrap execs it directly, so a case's
`bin/` (containing only `limine`) can never shadow `/usr/bin/python3`, and `-I` removes the script
dir from `sys.path`. Verified by code and by the 96/96 runs under `PATH=<case>/bin:/usr/bin`.

## Checklist answers for the named review items

| item | result |
|---|---|
| probe regex | matches `Limine 12.9.4`, `limine v12.9.5`, `Limine 12.9.6 (x86_64)`; **also** `12.9.6-rc1`/`12.9.4-git` (F1); first match wins; stdout only |
| probe timeout | 5 s, enforced: `sleep 6` → `None`, rc 64 at **5.07 s**; a background grandchild holding the pipe does **not** extend it (measured 5.10 s; CPython's POSIX timeout path does not re-drain). The orphan is not killed — harmless for a trusted system binary |
| probe returncode | nonzero → `None` (fake `exit 1` → rc 64). `subprocess.run` has no `check=`, but `p.returncode` is checked explicitly — not a defect |
| probe stderr | ignored by design; version-only-on-stderr → rc 64 (measured). Matches the documented "stdout only" |
| PATH lookup | `["limine", "--version"]` → `execvpe`; absent binary → `FileNotFoundError` → rc 64 (ExecLive's `PATH=/nonexistent` row, and the selftest's `absent` row) |
| `auto` order | probe first, then `parse_limine_version(version)`; a >9-digit component from the probe still reaches the rc 64 refusal (line 511) — no crash path |
| usage before message | `ap.print_usage(sys.stderr)` then the message, both on stderr; **stdout 0 bytes on every rc 64 row measured** (auto probe fail, malformed flag, `AUTO` uppercase) |
| `AUTO` uppercase | `version == "auto"` is exact → falls to the parser → rc 64; a marker fake proved the probe is **not** executed on the `AUTO` path |
| `limine_version_source` | present on the unreadable-conf return too (measured: `--conf <dir>` + auto → rc 2 JSON with `12.9.4`/`probe`); "flag" for a flag, but also for the default (F5) |
| `--live` signature | `check(conf, esp, bool(sb), tpm, version, version_source)`; live still adds `secure_boot_source`; fake-12.9.4 live run → JSON `12.9.4`/`probe`/`efivar`, rc 2 (EACCES on `/boot/limine.conf`), identical in shape to ExecLive's real run |
| era-A / R1-R10 / U1 unchanged | no hunk touches them; selftest 39/39; three 96/96 battery runs sample every r92 family |
| battery `case_path` | `"<case>/bin:/usr/bin"` iff the case has `auto` **and** the dir exists; otherwise `/usr/bin`; the fake is the case input, committed as bytes (`build()`, 1854-1863) |
| fake writer `chmod` | `os.chmod(fake, 0o755)`; the fake lives inside the case dir, removed with it (`shutil.rmtree(d)`); no executable survives a run |
| `run_usage` | each `c.usage` value (10 for `REFUSAL-VERSIONS`) and `auto` for the fail case, same ISOLATION argv, `rc == 64 and stdout.strip() == ""`; TIMEOUT 20 s |
| `auto_ok` | requires `got[8] == c.auto` **and** `got[9] == "probe"`; skips only non-auto and probe-fail cases — a gate that probes but reports the flag's value fails |
| `bin/` shadowing inner `python3` | impossible (absolute `sys.executable`, above) |

## Independent measurements run by this seat

| run | result |
|---|---|
| `--selftest` | `selftest PASS 39/39` (`probe-version`, `era-exact-first-entry` included) |
| battery, landed gate, 3 separate processes, own `--work` | `96/96 met` ×3, `failed -`; receipts `after/` agree (rc 0) |
| battery N01 / N05 / N06, one run each | `unmet 95/96` failing exactly `ERA-EXACT-125` / `AUTO-ERA-B` / `AUTO-PROBE-FAIL` |
| gate counterexamples (14 rows) | (a) `12.9.6-rc1`→rc 1, `12.9.6`/probe/era B; (b) `limine 12.9`→rc 64, stdout 0; (c) version on stderr→rc 64, stdout 0; (d) `AUTO`→rc 64, stdout 0, probe not run; (e) 6 s→rc 64 at 5.07 s; (f) 30 s-grandchild→rc 64 at 5.10 s; `v12.9.6`→accepted; era-A fake→prompt; flags 12.9.4/12.9.5→prompt/panic, source `flag` |
| non-UTF-8 banner | rc 1 + `UnicodeDecodeError` traceback (F2) |
| `--live --limine-version auto`, fake 12.9.4 | rc 2 JSON `12.9.4`/`probe`/`efivar`, conf-unreadable (same as ExecLive) |
| `sha256sum -c freeze-manifest` | 13/14 OK, plan FAILED (F3) |
| `after/` receipts cross-check | canonical 3× met (0 errors); N01/N03/N04/N05/N06 fail exactly their family 3/3; N02 fails 8 (F4); `c2-donothing` 94/96, 8 error rows (A1's evidence) |
| clone layout | **not run by this seat**; covered by `w1/ExecReplicate/compare-clone-vs-canonical.txt` (c1 3/3 MATCH, N01-N04 MATCH) and `w1/ExecAutoReplicate.md` (C2 auto families, clone 96/96 met) |

## Residual risk and verification gaps

- C2's rc 1 live receipt (`after/live-c2.json`, pins at `/boot/limine.conf` 30/38) is not
  reproducible from a seat; only the rc 2 unprivileged shape is. Both agree on version/source.
- The battery's sample does not include a suffixed banner (F1) or non-UTF-8 output (F2); the frozen
  target reads met because those inputs are absent, not because the code handles them.
- `AUTO-PROBE-FAIL` is not anti-vacuous by itself (F8); A1 already says so.
- The battery is only re-runnable with an interpreter under `/usr` (F6); the after receipts are
  consistent with `/usr/bin/python3` (a non-`/usr` interpreter yields `unmet` on every family).
- N02's receipt supports "the family is sensitive to the cut", not "the cut is one line late"
  (F4); the plan's label overstates it.

## Verdict

**Supports C1 (depth) and C2 (operability) as frozen**: landed gate 96/96 `met` reproduced 3× on the
canonical lane (and the frozen receipts' 3× plus the clone receipts), zero error rows; N01/N03/N04
and N05/N06 fail exactly their named family 3/3, N02 contains its named family 3/3 (broad, F4); the
probe records `limine_version`/`limine_version_source: probe`, selects the era from the probe, and
refuses rc 64 with empty stdout on every failure the battery and the seat sample. **No finding
falsifies a frozen target.** F1-F4 are medium-severity defects outside or beside the frozen
sample (probe grammar, probe decode crash, manifest drift, N02's self-description) and should be
recorded in the closure as narrowing candidates, not scored as counter-evidence. Receipts:
`.ufo/waves/round-93/after/c1-canonical.json`, `after/bend-N0{1,5,6}-*.json`,
`.ufo/waves/round-93/w1/ExecBends/freeze-check.txt`, `w1/ReviewBattery/probes-n02-nocut.txt`,
`w1/ExecReplicate/compare-clone-vs-canonical.txt`, `w1/ExecAutoReplicate.md`.
