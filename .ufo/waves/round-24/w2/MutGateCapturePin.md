# Wave 2 mutation test — MutGateCapturePin (FALSIFY wave 2, round 24)

Verdict: the claimed C2 capture pin survives. Both single-byte mutations — one byte of
the committed `.ufo/waves/round-24/capture/l1-4/capture.txt` and one hex char of
`capture_sha256` in the gate JSON — are detected by `python3 tools/check-pause-gate.py
--revision`, dropping `premises_verified` from 5 to 0 with status FAIL and finding
GATE-CAPTURE-PIN. Restoring exact bytes restores 5 verified (PASS). No defect found;
no correction needed.

Bench method: the checker reads all bytes from the bound git commit (`git show
<sha>:<path>` in `tools/_revision.py` reader), so a working-tree edit alone would not be
observed; each mutation was therefore committed in my own private clone
`/fast/scratch/hyaku/tsuku24w2-MutGateCapturePin/lane` (cloned from the lane at
22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0) and checked with `--revision <mutantsha>`.
`bind()` also requires the revision to be an ancestor of `refs/remotes/origin/master`;
the origin ref was deleted only inside the private clone so local-only mutant commits
could be bound. The lane repo itself was never written to. [inf]

## Findings

1. Pristine baseline (before any mutation: 5 premises verified, PASS, no findings.
   Command: `python3 tools/check-pause-gate.py --revision
   22fd1642e7fa4dfbdfba4419a443f06ffbb0b6c0` (run in the private clone), exit 0.
   Output excerpt (`/fast/scratch/hyaku/tsuku24w2-MutGateCapturePin/c2-pristine.json`):
   `"premises_verified": 5`, `"status": "PASS"`, `"findings": []`. [obs]
   Before-hashes at 22fd1642: capture.txt content sha256 `87f70f82f05956ce5de60abe8bfdd748f38d716483a491cfe7c183939884a56f` (matches committed `.ufo/waves/round-24/capture/l1-4/capture.sha256` and the gate `capture_sha256`); git blob `213056c44fc2698be4bcdce8c9f7a067d41dc398`; gate JSON content sha256 `279f2b7811d4a4b4083fb51b555cac0ad0d8b865ec45d8999c5b27b7b7a9f2ef`, git blob `68bbc333cc6d9291c14cb608a45aec33e6843a21`. [obs]

2. Mutation A — one byte of the committed capture.txt changed. Byte offset 45 in
   `capture.txt` (line 3 ` "2026-10-22T08:46:28Z"`, the `8` of `28` flipped to `9`, giving
   `...29Z`). The byte is outside every evidence needle (needles sit at lines 40, 53,
   374, 375, 376) and is not a section header, command echo or exit line. Commit
   `06c6ac387aace9f6f1245b2754ba40f03a156541` on top of 22fd1642. After-hashes:
   capture.txt content sha256 `9f6ebe0bac4c9cd9fa7a07a443d6a07be18bf2b56574cc2d7787804b51ece3c3`, git blob `0e300891ea550594de8f160f0446a52e8b831e61`. [obs]
   Run: `python3 tools/check-pause-gate.py --revision 06c6ac387aace9f6f1245b2754ba40f03a156541`, exit 1. Output (`/fast/scratch/hyaku/tsuku24w2-MutGateCapturePin/c2-mutA.json`): `"status": "FAIL"`, `"premises_verified": 0`, `"premises_total": 5`, findings `GATE-CAPTURE-PIN` at `.ufo/waves/round-24/capture/l1-4/capture.txt` plus `GATE-PREMISE P1:P5:capture-pin`; every premise `"verified": false` with `"problems": ["capture-pin"]`. Detector kills the mutant; verdict: killed. [obs]

3. Mutation B — one hex char of `capture_sha256` in `corpus/knowledge/pause-lift-gate-r24.json` changed (`87f70f82...` → `97f70f82...`, first hex digit `8` → `9`), capture.txt untouched. Commit `81be012d6d2ff650d02d8f700f0388fab0671236` on top of 22fd1642. After-hashes: gate JSON content sha256 `939b6d98229676217f183b1c260f36cc2a32b1efb60c900732eac60c56ed8e2c`, git blob `4bdb5dd7dc56873f0af12b8c3178f01a23e223da`. [obs]
   Run: `python3 tools/check-pause-gate.py --revision 81be012d6d2ff650d02d8f700f0388fab0671236`, exit 1. Output (`/fast/scratch/hyaku/tsuku24w2-MutGateCapturePin/c2-mutB.json`): identical shape to mutation A — `"status": "FAIL"`, `"premises_verified": 0`, findings `GATE-CAPTURE-PIN` plus `P1:P5:capture-pin`. Detector kills the mutant; verdict: killed. [obs]

4. Restoration — after each mutation, `git reset --hard 22fd1642...` restored exact
   bytes in the private clone. Restored hashes equal the before-hashes: capture.txt content sha256 `87f70f82...`, git blob `213056c44f...`; gate JSON content sha256 `279f2b78...`, git blob `68bbc333cc...`. Final rerun at 22fd1642: exit 0, `"premises_verified": 5`, `"status": "PASS"`, no findings (`/fast/scratch/hyaku/tsuku24w2-MutGateCapturePin/c2-restored.json`); `git status --porcelain` empty. [obs]

5. Interpretation: the GATE-CAPTURE-PIN check is the single behavior-bearing point for
   the capture pin; both one-byte tamperings (either side of the pinned pair — file or
   recorded digest) fail all five premises, so no premise can count while the pin is
   broken. The claimed after-value (5 verified) is therefore not reproducible from any
   one-byte deviation of the pinned capture pair. No defect found; smallest correction:
   none. [inf]

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin (SCORECARD.md round-24 sections, tools/check-pause-gate.py, tools/_revision.py, corpus/knowledge/pause-lift-gate-r24.{md,json}, .ufo/waves/round-24/capture/l1-4/{capture.txt,capture.sha256,checkupdates.out}), /home/vgpnk/.omp/agent/RULES.md, skill://godspeed; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/w2/MutGateCapturePin.md, /fast/scratch/hyaku/tsuku24w2-MutGateCapturePin/{c2-pristine.json,c2-mutA.json,c2-mutB.json,c2-restored.json}; executed=git clone/checkout/update-ref/config/reset/commit (private clone only), python3 tools/check-pause-gate.py --revision (pristine 22fd1642, 06c6ac38, 81be012d, restored 22fd1642), sha256sum, git rev-parse (read-only on lane; writes only in private clone)
Installs: none
