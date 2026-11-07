# ExecLints — r89 w1 executor: lane gates at tip + mined-mistake sweep

Lane measured: `git clone --shared` of /home/vgpnk/Projects/shokunin/tsukuroi-shokunin at master HEAD `665408cc45a88ed49717e22f4593e8e6152ac665` (to-be-counted seal commit; the mined-mistake comparisons use pre-round `dfeaab29c42b56128ddee13f46019a453fca4185` and HEAD).

## Lane gates (receipts in ExecLints/)
- `python3 tools/check-registry-coverage.py --revision 665408cc45a88ed49717e22f4593e8e6152ac665` → rc 0, `PASS`, `registered` 142, `tools_total` 142, `rows_total` 142, 0 findings. (Note: `--revision HEAD` is rejected by design with `E-REVISION-INVALID`/"7-64 hex commit required", rc 2 — I re-ran with the hex tip; the tool's usage says so. See ExecLints/check-registry-coverage.out.)
- `python3 tools/check-knowledge-header.py --revision 665408cc45a88ed49717e22f4593e8e6152ac665` → rc 0, `PASS`, `complete_count` 105, `clean_count` 105, `finding_count` 0. (Same `--revision HEAD` note. See ExecLints/check-knowledge-header.out.)
- `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` (read-only) → rc 0, last lines verbatim: `tsukuroi	W04	S329 duplicate url raw.githubusercontent.com/systemd/systemd/v262/man/systemd.unit.xml across scopes` then `tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`. Count: 52 W04 warnings (all pre-existing duplicate-URL warnings), 0 failures. See ExecLints/census-validate.out.

## r87 gate + r88 battery selftests (no harm on live gate surface)
- `python3 tools/check-limine-pins.py --selftest` → rc 0, `selftest PASS 15/15`. See ExecLints/check-limine-pins-selftest.out.
- `python3 tools/limine-pin-battery-r88.py --selftest --work $S/work` → rc 0, `selftest PASS 14/14`. See ExecLints/limine-pin-battery-r88-selftest.out.

## Mined-mistake check (lesson r89 M1: a correction must sweep every mention)
Exact phrase: `"is unread; the upstream tag copies"`.

- `git grep -n -F "is unread; the upstream tag copies" dfeaab29 -- corpus SCORECARD.md LOG.md` → rc 0, 2 hits, verbatim:
  - `corpus/README.md:977:- `limine-install`'s body (run by `limine-update`, PW5) is unread; the upstream tag copies of the mkinitcpio scripts`
  - `corpus/lessons/round-88-verifier-spotcheck.md:129:1. `corpus/README.md` Round-88 Frontier still says "`limine-install`'s body … is unread; the upstream tag copies … returned`
- `git grep -n -F "is unread; the upstream tag copies" HEAD -- corpus SCORECARD.md LOG.md` → rc 0 (not exit 1), 1 hit, verbatim: `HEAD:corpus/lessons/round-88-verifier-spotcheck.md:129:1. ...` — the r88 verifier spot-check quoting the stale line as its routed defect #1 (evidence-of-defect quote; the spot-check file was born at dfeaab29 and is historical evidence, unmodified since).
- `corpus/README.md` at HEAD (line 977), corrected at 81f68d00 (round-89 candidate commit): "`(Corrected round 89; spot-check r88 routed 1, lesson r89 M1.) PW5's flow was read from the installed bytes (S360), and wave seat ScoutSources' `git clone --branch 1.40.0` found the upstream `limine-mkinitcpio`, `limine-install` and `limine-mkinitcpio-install` byte-identical to them (raw URLs alone returned HTTP 429); `limine-install` writes no `path:` pin (seat's reading of its body, not re-checked by the L1) — entry Limits, `limine-pin-writers-r88.md` lines 58-62. Open: an L1 re-read of `limine-install`."

So the candidate claim "must print none, exit 1" is not literally met because the spot-check's quoted routed-defect text still contains the exact mined phrase. That remaining occurrence is a quote-of-the-defect (defect #1 text), arguably not a stale statement. Reported; L1 decides whether M1 compliance tolerates quoting the removed line in the defect record.

## Other stale r88 PW5/limine-install provenance (HTTP 429 never-read claims)
- `corpus/knowledge/limine-pin-writers-r88.md:58-62` (HEAD): "PW5's mkinitcpio flow is read from the installed bytes (S360, own-work); wave seat ScoutSources cloned the upstream tag 1.40.0 (raw URLs returned HTTP 429)..." — accurate, not stale (explains why raw fetch failed but doesn't claim never read; entry's Limits records reading).
- `corpus/lessons/round-88.md:89` (S360 gate-addendum row): "the upstream tag copies returned HTTP 429 to the L1 and to seats ReviewEntry and ScoutSources, so the installed bytes the host actually runs are the evidence" — written at 68ca60f5, before ScoutSources' tag-clone re-open at 35ca9e7e. Gate addendum 2 (line 130) records: "ScoutSources re-opened all 14 pinned files through `git clone --depth 1 --branch <tag>` (raw URLs HTTP 429 host-wide; 6 of 14 also live HTTP 200) ... byte-identical to the tags". So the round-88 lesson's own gate-addendum row is not same-wave-corrected by the later addendum; historically true on its date but reads stale against "byte-identical" now. Candidate disposition, not factually false.
- `corpus/lessons/round-88-verifier-spotcheck.md:66` (`gitlab raw URLs returned HTTP 429 to me too; I used git clone --branch 1.32.1/1.40.0`): true statement — the verifier used clone, not raw URLs. Not stale.
- `corpus/lessons/round-88-verifier-spotcheck.md:129-131` (routed defect #1 quoting the stale README line) — see mined-mistake above.
- Full HEAD grep for `429` across corpus/SCORECARD/LOG: all other hits are unrelated (provider 429 quota, line numbers, hashes); no other `tag-copy-never-read` claim about the r88 PW5/limine-install provenance remains besides the two files named above.

## No mutation
No lane file was edited; all receipts copied from $S (clone HEAD 665408cc); scratch to be removed after copying.

Report: .ufo/waves/round-89/w1/ExecLints.md
