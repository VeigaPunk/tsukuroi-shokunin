# CriticClaims — round 88, wave w1 (critic on the C1 counter, roster and predicate)

Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master`
= `1fac4195243e55e7d9d8a2eddd653443d8559bff` (registry rows commit; the frozen counter/roster are
unchanged since the freeze).

Instrument identity, checked against `.ufo/waves/round-88/before/freeze-manifest.sha256`:

```
7d2073dfd120c8ac5ebaf8c68e7c270f970b5c7a75850561d7ceb9db76c13305  tools/battery-discrimination-r88.py
1e2dcc8bab709b99dfdb62fad1b123fe3cd3fab4fc542e782b8a20489a95ae8c  .ufo/waves/round-88/before/roster/roster-r88.json
```

Every run below used those bytes (the counter's `counter_sha256`/`roster_sha256` in each receipt
match the two digests above, except `p1`/`p2`/`p3`, which used a patched copy of the counter in my
own clone to validate the proposed fix; the roster is the frozen file in all runs). Candidate
battery `tools/limine-pin-battery-r88.py` (clone bytes) was used for `p1` and `p4`.

The counting setup is the declared one: cwd = `git clone --shared <lane> $S/lane`, gates handed
over nonce-perturbed and renamed, `--runs 1 --jobs 4` per the seat brief.

## Verdicts

| # | Check | Verdict |
|---|---|---|
| F1 | Sandbox hides the roster from the battery | **FALSE as implemented** — the frozen roster-oracle control reads `met` under the declared counting command |
| F2 | The nonce line stops a stored-digest oracle | **FALSE** — striking the trailing comment recovers the roster digest; two forgers read `met` |
| F3 | The KILL RULE's void condition is enforced | **FALSE** — no code reads the freeze manifest; `--roster` accepts a forged 1-gate roster and prints `verdict met` |
| F4 | Axis named by the surface | **Disputed (wording)** — the measured surface is battery calibration, booked as operability 9 assurance |
| L  | Roster labels (3 POSITIVE / 45 NEGATIVE) | **No dispute found** on 48/48; one scope note (m01/g00 lack the landed gate's `resolve_in_esp`/`sanitize`, which no family exercises) |
| C1 | Per-run counts for the candidate battery | **3/3 and 45/45 in the run I made** (`p4`, frozen counter, battery `ab6c1b33…`) — the counts hold; the isolation half of the predicate does not |

`p4` — frozen counter, declared counting shape, candidate battery, one run:

```
$ cd $S/lane && time python3 /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/battery-discrimination-r88.py \
    --battery tools/limine-pin-battery-r88.py --runs 1 --jobs 4 --scratch $S/work
run 1 positives 3/3 negatives 45/45 failures -
verdict met
real 1m18.749s   rc=0
counter 7d2073dfd120c8ac5ebaf8c68e7c270f970b5c7a75850561d7ceb9db76c13305
battery ab6c1b33f84dd252979296d1b56ccea8c5e89af221e02e1ec08ef8e579fac374
roster  1e2dcc8bab709b99dfdb62fad1b123fe3cd3fab4fc542e782b8a20489a95ae8c
```

A `met` on the candidate battery therefore does not carry the isolation the predicate names: the
same counter reads `met` for `f1`, `f2`, `f3`, `f8` and `f9`.

## F1 (critical) — the sandbox masks only one copy of the lane; the roster is readable

Counterexample: `bwrap` argv at `tools/battery-discrimination-r88.py:85-92` is
`--ro-bind / / … --tmpfs lane …`, where `lane = LANE` (`:151`, `LANE` from the counter's own
directory, `:40-41`). `/` is bound read-only *whole* and only the one path the counter was invoked
from is replaced by a tmpfs. The declared counting command runs the counter **from a clone**, so
`lane` is the clone and the lane itself — `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` — stays
readable inside the sandbox. Symmetrically, when the counter is run from the lane, any clone under
`/fast/scratch` stays readable. A copy of the roster is reachable in both directions.

The committed freeze control `bat-roster-oracle.py` (unmodified) is the counterexample — it reads
the roster at the lane's absolute path:

```
$ cd $S/lane && python3 tools/battery-discrimination-r88.py \
    --battery .ufo/waves/round-88/before/controls/bat-roster-oracle.py --runs 1 --jobs 4
run 1 positives 3/3 negatives 45/45 failures -
verdict met
rc=0
```
(`f1-roster-oracle-from-clone.txt` / `.json`; `counter_sha256 7d2073df…`, `roster_sha256 1e2dcc8b…`)

Run from the lane cwd, the same control reads `0/3 0/45` (`f4-roster-oracle-from-lane.txt`,
`rc=1`) — because it *crashes*, not because isolation held. Reproduced directly under the counter's
bwrap shape:

```
Traceback (most recent call last):
  File ".../b.py", line 14, in <module>
    for g in json.load(open(R))["gates"]:
FileNotFoundError: [Errno 2] No such file or directory:
  '/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-88/before/roster/roster-r88.json'
rc=1
```

So the freeze-time receipt `bat-roster-oracle.receipt.txt` (`0/3 0/45`, run with cwd = the lane at
`rev 029454fc`) is a crash artefact, not evidence that a roster oracle fails. A forger that does not
hardcode one path also passes: `forger-glob-roster-v2-r88.py` (walks `/home`, frozen-roster sha256
filter, nonce strip) reads `3/3 45/45` `met` from the clone (`f8`) and `forger-glob-roster-v3-r88.py`
reads `3/3 45/45` `met` from the lane (`f9`).

Impacted axes: operability 9 assurance — the predicate's sentence "inside a sandbox that hides the
lane repository" (`:5`, `:14-19`) and the declaration's "a battery that answers from the roster …
fails (controls above)" are both false; any battery can answer from the roster.

Smallest safe correction (proposed, not applied): replace the all-of-`/` bind with a minimal
read-only root and tmpfs every root that can hold a copy; see
`w1/CriticClaims/proposed-sandbox-allowlist.patch`:

```
-        argv = ["bwrap", "--ro-bind", "/", "/", "--dev", "/dev", "--proc", "/proc",
+        argv = ["bwrap", "--ro-bind", "/usr", "/usr", "--symlink", "usr/bin", "/bin",
+                "--symlink", "usr/sbin", "/sbin", "--symlink", "usr/lib", "/lib",
+                "--symlink", "usr/lib64", "/lib64", "--ro-bind", "/etc", "/etc",
+                "--dev", "/dev", "--proc", "/proc",
+                "--tmpfs", "/home", "--tmpfs", "/fast", "--tmpfs", "/tmp", "--tmpfs", "/var",
                 "--tmpfs", lane, "--bind", d, d, "--chdir", d, "--unshare-net",
```

Validated in my clone (`p1`-`p3`, patched counter, same frozen roster):
- the candidate battery still reads `run 1 positives 3/3 negatives 45/45` `verdict met` `rc=0`
  (`p1-patched-real-battery.txt`) — the fix costs nothing on the claim;
- the roster-oracle control now reads `0/3 0/45` `verdict unmet` `rc=1`
  (`p2-patched-roster-oracle.txt`) — the isolation sentence becomes true.

The counter should also run the frozen roster-oracle control as a built-in negative control each
run and void if it reads `met` (today isolation is asserted in prose only).

## F2 (high) — the nonce is an appended comment; stripping it recovers the roster digest

`one()` appends `# nonce <hex>` as a trailing line to the roster bytes (`:74`). The perturbed
copy is therefore a *superset* of the original, and any oracle that removes a trailing comment
recovers the digest the roster stores. `forger-embedded-digests-r88.py` (48-entry sha256 table
embedded, trailing `# nonce …` stripped, no gate executed, no file read):

```
$ cd $S/lane && python3 tools/battery-discrimination-r88.py \
    --battery <wave>/forgers/forger-embedded-digests-r88.py --runs 1 --jobs 4
run 1 positives 3/3 negatives 45/45 failures -
verdict met
rc=0
```

Same result with an AST-normalised table (`forger-ast-normalised-r88.py`, `ast.dump` ignores
comments and formatting): `3/3 45/45` `met` (`f3-ast-normalised.txt`). It still reads `met` under
the patched counter (`p3`), i.e. no sandbox can fix this class.

The counter's own sentence `:15-16` — "so no stored digest or name identifies it" — is false. The
declaration already excludes this class ("Not certified: … behaviour-preserving normalisation of
their source text (left to the non-author review)"), so the defect is the *unconditional isolation
claim*, not the predicate's scope; and the freeze control `bat-neg-digest-list.py` tested only the
un-normalised hash, so it passes for a cosmetic reason.

Smallest safe correction: strike `:15-16`'s claim and state the limit where the predicate is
quoted; require C1's receipt to read "certified against behavioural batteries only; a battery that
identifies gates by source text is outside the certified set" (the SCORECARD sentence, promoted into
the receipt), and retitle the control `bat-neg-digest-list` as "raw digest only" so its pass is not
read as covering the class. Do not promise a stronger isolation than this.

## F3 (medium) — the declared void condition is not implemented; `--roster` is unguarded

Docstring `:11-12`: "void (exit 2) if this file or any roster file differs from
`.ufo/waves/round-88/before/freeze-manifest.sha256` / the roster digests." No code reads the
freeze manifest; `load_roster` (`:51-62`) checks each gate file against the digest *stored in the
same roster file*, which is self-referential, and `main`'s only void check is that loop (`:144-146`).
`--roster` (`:135`) accepts any path.

Counterexample (forged 1-gate roster, matching internal digest, no NEGATIVE gate at all):

```
$ cd $S/lane && python3 tools/battery-discrimination-r88.py --battery .ufo/waves/round-88/before/controls/bat-always-met.py \
    --runs 1 --jobs 4 --roster <wave>/forged-roster/roster-forged.json
run 1 positives 1/1 negatives 0/0 failures -
verdict met
rc=0
```
(`f5-forged-roster.txt`; the receipt records `roster_sha256 9bc084d3…`, not the frozen `1e2dcc8b…`.)

Impacted axes: operability 9 assurance — a `met` receipt can be produced against a roster the
predicate does not name; only a reviewer recomputing `roster_sha256` catches it. The recorded hash
is the mitigation and the receipt must be read against the manifest.

Smallest safe correction: drop `--roster` (read the constant `ROSTER` only) or `void` unless its
sha256 equals the frozen digest; and either check the counter's own bytes against the manifest
(reading `.ufo/waves/round-88/before/freeze-manifest.sha256`) or delete `:11-12`.

## F4 (low) — the measured axis is battery calibration, credited as operability

The predicate measures whether *a test battery* separates 3 correct gates from 45 deviant ones. The
surface (prompt §9) is instrument calibration/quality of the `limine-pins` assurance, not a change in
host operability: nothing about the host is repaired by a `met`. The declaration's wording —
"Operability stays 9 (an assurance move, no ordinal claim)" — is defensible only if the receipt
says exactly that. If the receipt books C1 as an operability *measurement*, it is mislabelled.
Recommend the receipt line: "calibration of the limine-pins gate battery over a frozen 48-gate
roster; credited to the operability 9 assurance arm, no ordinal claim". Also drop, in the same
receipt, any claim that discrimination is by behaviour: F1/F2 show the counter cannot tell
behaviour from identity.

## Roster labels — checked, no dispute

- POSITIVE provenance holds: `pos-landed-gate-3ba37eb0.py` sha256 `e3b0fab4…` equals
  `git show 3ba37eb0:tools/check-limine-pins.py`.
- 30/30 `m02`-`m30` mutants: each differs from `m01` by exactly one live change (blank-strip, key
  case, hash lengths 127/129, lowercase-only hex, any-resource/any-root resolution, gzip
  decompression, missing→unresolved, missing→OK, panic last/default/inverted, secureboot ignored,
  optional skip, 0-based lines, CR, value lstrip, pin-key set, optional set, case-sensitive digest
  compare, sha256-for-blake2b, last-pin-only, entry=None, panic line 0). Each contradicts R1-R8 text
  — all genuine NEGATIVE.
- 16/16 `g01`-`g16` forgers: read through `_lib.py`'s option branches; every flag bends a named
  R1-R7 clause (`nohash`, `sb_presence`, `raw_panic_scan`, `drop_keys global_dtb`, `loose_key`,
  `no_paren`, `format_after_resolve`, `hashfmt_always_panic`, `last_uri`, `any_empty_root`,
  `panic_key_case`, `eacces_rc1`, `no_cr_strip`, `first_hash`, `panic_any_non_yes`,
  `constant_panic`) — all genuine NEGATIVE.
- `P-m01-comment-not-skipped`: its removed `line[0] == "#"` guard is provably inert, because
  `split_key`'s key regex `([A-Za-z_]+):` cannot match a leading `#`; the claim "equivalent mutant"
  holds. Scope note: `m01` and `g00` lack the landed gate's `resolve_in_esp`/`sanitize` hardening,
  and no family exercises either, so the battery certifies R1-R8 only — consistent with the gate's
  own docstring ("round-87 hardening, not a Limine rule"), but it means `P-m01` is equivalent to
  `g00` *within the rule set*, not to the landed gate's bytes.

## Refusals

No lane file edited; no host path written; no `sudo`, no pacman, no boot/ESP tool. All work in
`/fast/scratch/hyaku/tsukuroi-r88/CriticClaims/` (clone + fixtures) and this wave dir. No live
roster/gate file was modified; the forged roster is a new file under my wave dir.

## Receipts (all in `w1/CriticClaims/`)

`f1-roster-oracle-from-clone.{txt,json}` (met), `f2-embedded-digests.{txt,json}` (met),
`f3-ast-normalised.{txt,json}` (met), `f4-roster-oracle-from-lane.txt` (unmet, crash),
`f5-forged-roster.{txt,json}` (met), `f6-glob-roster-from-lane.txt` (unmet; depth-8 walk pruned
the clone and merged a sibling fixture's flipped roster — failed variant, kept for honesty),
`f7-glob-roster-v2-from-lane.txt` (unmet, empty table), `f8-glob-roster-v2-from-clone.txt` (met),
`f9-glob-roster-v3-from-lane.txt` (met), `p1-patched-real-battery.txt` (met),
`p2-patched-roster-oracle.txt` (unmet), `p3-patched-embedded-digests.txt` (met,
known limit), `p4-frozen-counter-real-battery.txt` (frozen counter, candidate battery),
`forgers/`, `forged-roster/`, `proposed-sandbox-allowlist.patch`.
