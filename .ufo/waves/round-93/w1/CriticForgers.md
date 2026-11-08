# CriticForgers — r93 forgery battery: discrimination of the new families and V3 leakage

- Seat: CriticForgers (critic; read-only on the lane).
- Lane root: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, HEAD `c633f49aa512e1c8a0e0464b7fb5d354c70096cf`.
- Instruments verified before use (`sha256sum`): gate `6b4c53d1…b6260aa`, battery `ddd7e955…75e1aad`,
  do-nothing gate `35c1088b…8d5c87f`, do-nothing battery `aef33925…d02614f`. Unmodified.
- Environment: Python 3.14.8, bubblewrap 0.13.1, 32 cores. No tool install or upgrade was needed
  (pacman is paused host-wide; nothing was installed).
- Scratch: `/fast/scratch/hyaku/tsukuroi-r93/CriticForgers/` (removed on exit); receipts copied to
  `.ufo/waves/round-93/w1/CriticForgers/`.
- Every battery run below: `python3 <lane>/tools/limine-pin-battery-r93.py --gate <gate> --runs 1
  --work <own dir> --json <out>` inside the frozen ISOLATION launcher, own `--work` dir per run.
  Seven battery runs in three batches: ref + independent in parallel (85 s), f1–f5 in parallel
  (60 s), f6 alone (32 s).

## Axes

- **A. Discrimination of the r93 families** — every new clause must have a family whose expected
  answer changes when that clause alone is bent.
- **B. Specification completeness** — can an independent implementer reproduce the judged answers
  from the battery docstring alone, and where does the docstring under-specify the landed gate?
- **C. V3 answer leakage** — does the fixture expose the expected era/version outside the intended
  probe channel, and does the battery notice?
- **D. Evidence integrity** — instrument hashes, baselines, error rows, no lane writes.

## Baselines

| gate | run | verdict | families | cases | error rows | receipt |
|---|---|---|---|---|---|---|
| landed `tools/check-limine-pins.py` | canonical, 1 run | `met` | 96/96 | 384 | 0 | `ref.json`, `ref.log` |
| `independent.py` (docstring-only) | 1 run | `met` | 96/96 | 384 | 0 | `ind.json`, `ind.log` |

## 1. Docstring-only independent implementation

`independent.py` (sha256 `2bea245d864a088e7403b2bcbfc3da9c336f2d7eb9bf217f3f1664db67401b3b`) was
written from the battery's module docstring — R1–R10, V1, V2, V3, U1 and the GATE OUTPUT CONTRACT —
with no import of the battery or the gate, a fresh parser and a different internal structure. It was
annotated `AMBIGUITY:` wherever the docstring was silent. The lane gate's source was open for
cross-checking during review, so this is not a blind reimplementation; the four measured divergences
below (A1–A4) are the evidence that the implementation is not a copy and that the docstring text
alone fixes the sampled answers. It **reads 96/96 `met`, 384 cases, 0 error
rows** (`ind.json`): the docstring is complete for every answer the battery samples, including the
four r93 C1 families and the three V3 families.

The 96/96 does *not* mean the docstring specifies the landed gate. The independent gate differs from
the landed gate on four clauses the battery never samples, and still reads `met`:

| # | clause | independent (docstring-literal) | landed gate | family that samples it |
|---|---|---|---|---|
| A1 | R5 ESP containment for `..` / symlink out of `--esp` | `boot():/../outside#<b2>` → `OK`, `HEALTHY`, rc 0 (it read the file outside the ESP) | `LP-UNRESOLVED`, `CANNOT-EVALUATE`, rc 2 | **none** |
| A2 | R8 empty entry label (a bare `/` line) | label `""` for the following pin | keeps the previous label (`or entry`) | **none** (ENTRY-LABEL/ENTRY-LABEL-EDGES draw only non-empty labels) |
| A3 | R5 regular file that exists but cannot be read | `LP-MISSING` (a choice; docstring silent) | `LP-UNRESOLVED` | **none** |
| A4 | V3 probe output grammar | first bare `X.Y.Z` anywhere | requires a `limine` token before the version | **none** (every fake prints `Limine X.Y.Z`) |

A1 is measured (`amb/traversal.conf`, sha256 `acb72205…d8d3616`): the docstring-faithful gate hashes
a file outside the ESP and calls the config `HEALTHY`; the landed gate refuses with
`LP-UNRESOLVED`. A2 is measured (`amb/labels.conf`, sha256 `1a3822c6…49e635e7`): independent prints
entry `""`, the gate prints entry `"A"`. The battery's rule text therefore describes an accepted
gate that can escape the ESP root; the landed gate's hardening is *stricter than the judged rule
set*, and the battery's "Not modelled (limits, not families)" list does not mention it. This is a
specification gap, not a bend: the instrument was not touched.

Smallest safe correction: add the containment clause to R5 (a path whose `realpath` leaves `--esp`
is `LP-UNRESOLVED`; a lane hardening, not a Limine rule) **and** one TRAVERSAL family, or list it
explicitly under "Not modelled". As written, a gate that follows `..` outside the ESP can be
certified `met`.

## 2. One-clause forgers (f1–f5) and the leakage forger (f6)

Each forger is a copy of the landed gate with exactly one clause bent (sources under receipts,
sha256 listed). `failed families` gives family: failed cases / 4.

| id | clause bent | sha256 | verdict | families passed | failed families |
|---|---|---|---|---|---|
| f1 | V1/V2 first-entry visibility → “line 1 is an entry **and** `len(text.split("\n")) <= 8`”, era ignored | `363d7cbd…2e7ac78e4` | `unmet` | 90/96 | ERA-EXACT-125 4/4, ERA-B-FIRST-BODY 4/4, ERA-FLE-PANIC-B 4/4, ERA-FLE-MEASURED-B 4/4, FIRST-LINE-ENTRY 4/4, AUTO-ERA-B 4/4 |
| f2 | U1 candidate set → every `path:` key line with a non-pin value, regardless of protocol/image line | `893fd144…5fddf4d` | `unmet` | 93/96 | UNVERIFIED-IMAGE-PATH 4/4, UNVERIFIED-NON-EFI 4/4, UNVERIFIED-SORTED 4/4 |
| f3 | version handling → every non-`auto` `--limine-version` refused rc 64 (blanket refusal) | `67f9197e…cea34597` | `unmet` | 4/96 (368 error rows) | POSITIVE and 91 others; passes REFUSAL-VERSIONS, AUTO-ERA-A, AUTO-ERA-B, AUTO-PROBE-FAIL |
| f4 | V3 → probe output echoed into `limine_version`/`source: probe`, era forced to pre-12.9.5 | `e05ff3eb…ea9e3f` | `unmet` | 95/96 | AUTO-ERA-B 4/4 |
| f5 | V3 → era B whenever the probe target’s PATH head is not `/usr/bin` (the fake path); probed version still reported | `197c0086…f15726a1` | `unmet` | 95/96 | AUTO-ERA-A 4/4 |
| f6 | V3 probe mechanism → read `<cwd>/bin/limine` source, never execute `limine --version` | `7e612f6d…beee85b6f` | **`met`** | **96/96** | — (survivor) |

Readings:

- **f1** is the strongest positive result for C1 depth. The r93 families `ERA-EXACT-125` and
  `ERA-B-FIRST-BODY` and the V3 family `AUTO-ERA-B` all fail 4/4 under a line-1-plus-line-count
  heuristic; the r92 pair `ERA-FLE-PANIC-A/B` also fails on the B side. The era boundary is load
  bearing: the forger still passes `ERA-FLE-PANIC-A`, `ERA-FLE-MEASURED-A` and `ERA-DEFAULT` (era-A
  answers) and dies only on the era-B shapes.
- **f2** is aimed at the r93 U1 family and is *not* killed by it: `ERA-B-U1` passes 4/4. The
  over-report is killed by the r91 U1 families (non-efi entries, image_path-only entries, sorted
  list). So `ERA-B-U1` certifies the whole-file *scope* of U1 in era B, not U1 correctness; a round
  that cites `ERA-B-U1` as a U1-correctness upgrade would overclaim.
- **f3** shows the refusal contract is two-sided. `REFUSAL-VERSIONS` passes a blanket refuser
  (all 10 values refused, rc 64, empty stdout), and only `POSITIVE` (and the 91 non-auto families)
  kills it — 368/384 cases are `bad-output: JSONDecodeError rc=64`. Conversely `REFUSAL-VERSIONS`
  is the family that kills the r92 `N04-accept-any` class. Neither family alone certifies the
  version contract.
- **f4** is killed by `AUTO-ERA-B` and nothing else: reporting the probed version while ignoring it
  for the era is invisible to `AUTO-ERA-A` (default era is A). The B family is the only probe-use
  witness.
- **f5** is killed by `AUTO-ERA-A` and nothing else: the fake's path says “a fake is present”, not
  which era it prints, and hardcoding B fails the A case 4/4. The A family is not redundant with B.
  (The literal `"/bin" in PATH` variant would answer era B for every case, since non-auto PATH is
  `/usr/bin`, and fails ~90 families including `POSITIVE`; the measured f5 is the sharper variant.)

## 3. Survivor and leakage verdict (f6)

`f6` replaces `probe_limine_version()` with a read of `os.getcwd()/bin/limine`; it greps the fake's
source for `Limine X.Y.Z`, treats the literal `exit 1` as a failed probe, and never runs
`limine --version`. It reads **96/96 `met`, 384 cases, 0 error rows** (`f6.json`, `f6.log`), with
`AUTO-ERA-A`, `AUTO-ERA-B` (got `12.9.6`, `source: probe`, era-B `panic`) and `AUTO-PROBE-FAIL`
(rc 64, empty stdout) all passing. This is a coverage gap, not an isolation break: the case
directory is the gate's cwd, the fake is committed as bytes there, and the battery only observes the
JSON.

**Is reading the fake different from reading the conf?** Yes. The conf is the artifact under test:
its bytes legitimately determine the expected answer, and every gate must read it. The fake
`limine` is the *probe target*; V3 says the gate “runs `limine --version` read-only” and takes the
first `X.Y.Z` in its *output*. Reading the script source bypasses the probe contract, and on a real
host there is no case-local `bin/limine` to read — the mechanism only appears to work because the
fixture fake is a shell script whose literal output is its source. The battery cannot distinguish
“executed the probe” from “read the fake”.

**Is the docstring sentence “Fixtures carry no answer … no expected value on disk” now false?**
Yes, for the three AUTO families. `bin/limine` contains `echo "Limine 12.9.4"` /
`echo "Limine 12.9.6"` (the expected `limine_version` and hence the era) or `exit 1` (the expected
rc-64 refusal). The rest of the sentence remains true: names are random and carry no digest, and
the conf lives outside the ESP.

Honest wording for that paragraph:

> Fixtures carry no expected verdict on disk **except the V3 fake `limine`**: for the AUTO families
> the case's `bin/limine` is an executable whose literal source encodes the version it prints (and
> `exit 1` for the probe-failure case), so the case directory does carry the expected era/version
> bytes and the gate's cwd is that directory. The fake is an input the gate must **execute**
> (`limine --version`), not an answer to read: the V3 families certify the observable result
> (reported version, `source: probe`, selected era, refusal), and cannot distinguish a correct
> probe from a gate that reads the fake's source. Every other family's fixtures carry no expected
> value on disk; names are random (history names too: no content digest in any name); the conf
> lives outside the ESP directory; the gate runs inside the ISOLATION sandbox.

Smallest safe corrections:

1. Make the fake's source a decoy instead of the answer: write one extra line before the echo in
   `build()`, e.g. `# Limine 12.9.2 (fixture metadata)`. A first-`X.Y.Z` source reader then reports
   12.9.2: `AUTO-ERA-A` fails the `limine_version` check and `AUTO-ERA-B` fails the era, so f6's
   class dies. Expected values (`c.auto`) are unchanged. A reader that parses the echo line
   specifically still wins; this is cheap, not complete.
2. If “runs `limine --version`” must itself be certified (C2 says it must), add an execution
   receipt: bind one small writable directory into the sandbox and have the fake touch/append a
   marker; assert the marker after the run. Only this distinguishes “probed” from “produced”.
3. Apply the docstring rewording above.

## 4. Claim support

- **C1 (depth)** — supported for the sampled clauses. `ERA-EXACT-125` and `ERA-B-FIRST-BODY` are
  load bearing against f1 (4/4 each), as is the r92 boundary pair. `REFUSAL-VERSIONS` catches the
  accept-any side but not the refuse-all side (f3); `POSITIVE` is the needed control. The U1 r93
  family is a scope family, not a correctness upgrade (f2 passes it, the r91 U1 families kill it).
- **C2 (operability)** — supported at the *result* level: `AUTO-ERA-B` alone kills f4 (probe echo
  without era use) and `AUTO-ERA-A` alone kills f5 (fake-path era inference), so the two era
  families are jointly necessary and the probe bytes, not the fixture path, are what is tested.
  The mechanism clause (“runs `limine --version` read-only”) is **not certified by the battery**:
  f6 reads the fake's source and reads 96/96. The live run remains the only receipt for the
  mechanism on the landed gate.
- **Spec/docstring** — the docstring is sufficient for all 96 judged families (independent gate
  met 96/96), but under-specifies four landed-gate clauses; the ESP-containment one is
  security-relevant and unlisted in “Not modelled”.
- No bend, mutant or forged instrument was written into the lane; every forger and the independent
  gate are copies under the seat scratch/receipts.

## Verdict

My evidence **supports** C1's family-level depth for `ERA-EXACT-125` and `ERA-B-FIRST-BODY` (f1
unmet 90/96, those two 4/4) and C2's result-level probe families (`AUTO-ERA-B` kills f4, `AUTO-ERA-A`
kills f5, each 4/4), and reproduces the landed gate's 96/96 `met` baseline (384 cases, 0 error
rows). It **falsifies** two statements attached to C2/the battery docstring: (i) that the battery
certifies the gate “runs `limine --version`” — `f6`, which only reads `<cwd>/bin/limine` source,
reads `met` 96/96, so V3 certifies the observable result, not the mechanism; (ii) that “fixtures
carry no answer … no expected value on disk” — the AUTO fake's literal source encodes the expected
version/refusal, hence the leakage. It also shows the documented R5 does not cover the landed gate's
ESP-containment hardening: a docstring-faithful gate escapes `--esp` and still reads `met`
(`amb/traversal.conf` → `OK`/`HEALTHY` independent vs `LP-UNRESOLVED`/rc 2 gate). Receipts:
`.ufo/waves/round-93/w1/CriticForgers/` (`ref.json`, `ind.json`, `f1.json`…`f6.json`, the six forger
sources, `independent.py`, logs, `summary.json`, `amb/`).
