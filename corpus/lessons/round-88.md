# Round 88 — lesson (tsukuroi)

author: TsukuroiR88 (L1). Pre-round tip `029454fce571f3e27da16c72f94726504bd27886`; freeze
`01b2a9b091fe8af22b054bc061bbe14e9f96bf86` (frozen counter, 48-gate roster, do-nothing + five forgery controls,
declaration); candidate `5b98ca98c9a19641e77832bc57579d95fa5571a3` (battery r88, entry PW1-PW9, S355-S359, pinned
sources, host receipt); registry rows `1fac4195243e55e7d9d8a2eddd653443d8559bff`. Citations are by hash; the
helper's author dates are not chronology.

## Inputs read

Round-87 closure (MANIFEST `rounds[]` tsukuroi r87, `admitted`) and `corpus/lessons/round-87-verifier-spotcheck.md`
§5. Disposition of its six routed defects:

| r87 defect | Disposition this round | Evidence |
|---|---|---|
| 1 Residual clause probe ran on pre-landing gate bytes | Re-run on the landed bytes by wave seat ExecResidual | `.ufo/waves/round-88/w1/ExecResidual.md` |
| 2 C1 discrimination gap (R87-R1..R5) | This round's C1: battery r88 with 16 families for the uncertified clauses and gate mutants, literal roster, one-field lie selftest, judged by a frozen counter over the r87 forgers and mutants (45 negatives) under isolation | `SCORECARD.md` "Round 88 — declaration"; `.ufo/waves/round-88/after/measured/c1-receipt.txt` |
| 3 SHONEN box 4 sibling scan unfinished | Re-dispatched: wave seat ConnectorOverlap | `.ufo/waves/round-88/w1/ConnectorOverlap/sibling-scan.txt` |
| 4 Wave provenance after the kernel restart | Note appended below (Wave provenance); r88 seats told to write receipts to disk as they go | `.ufo/waves/round-88/w1-spec.json` context |
| 5 R87-R6 erratum (`ScoutHost.md:23` "sha256" label) | Erratum appended below (Errata) | this file |
| 6 Host incident repair (operator-owned) | Unrepaired; C2 names who writes the pins, the packaged repair command and why the stale pins spread to new snapshot entries | `corpus/knowledge/limine-pin-writers-r88.md` PW5-PW8 |

## Gate

Sources opened 2026-11-06 (America/Sao_Paulo) 20:46-20:50 by the L1, `curl -sSf`, tag-pinned raw URLs, snapshots in
`.ufo/waves/round-88/before/src/` (`URLS.txt`, `SHA256SUMS`). The installed `limine-entry-tool` and
`limine-snapper-sync` are native binaries; the tags matching the installed packages (`pacman -Q`:
limine-mkinitcpio-hook 1.40.0-2, limine-snapper-sync 1.32.1-2) are the ones pinned and cited, and the packaged
script and config bytes were compared with the installed files (host receipt).

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| S355 (new, code/A) | https://gitlab.com/Zesko/limine-entry-tool/-/raw/1.40.0/src/main/java/org/limine/entry/tool/processes/LimineManager.java, 2026-11-06, raw 325, 329, 331, 353, 359-372 | "bootConfig.add(Config.SPACES + Limine.PATH + \" \" + config.pathFunction() + ukiEspPath + this.b2sum(ukiFullPath));" (raw 353) | ADMIT, PW2/PW3/PW5. The only statement of which lines carry a pin. Flip: a limine-mkinitcpio-hook upgrade (re-pin at the new tag). |
| S356 (new, code/A) | https://gitlab.com/Zesko/limine-entry-tool/-/raw/1.40.0/src/main/java/org/limine/entry/tool/processes/ConfigReader.java (+ objects/Config.java), 2026-11-06, raw 28-32, 173-177; Config.java 7-8, 19 | "loadConfigFile(Config.DEFAULT_CONFIG_FILE_PATH); // 4. Highest priority" (raw 32) | ADMIT, PW1/PW2. Load order and the verification switch; the README (S075) states neither. Flip: upgrade. |
| S357 (new, code/A) | https://gitlab.com/Zesko/limine-entry-tool/-/raw/1.40.0/src/main/java/org/limine/entry/tool/processes/Utility.java, 2026-11-06, raw 118-175 | "CompletableFuture<String> hashFuture1 = CompletableFuture.supplyAsync(() -> blake2sum(absoluteFilePath));" (raw 144) | ADMIT, PW4. How the pin is computed. Flip: upgrade. |
| S358 (new, code/A) | https://gitlab.com/Zesko/limine-entry-tool/-/raw/1.40.0/install/arch-linux/limine-mkinitcpio-hook/usr/bin/limine-update (+ 89-warn-missing-file-hashes, limine-entry-tool.conf), 2026-11-06, raw 16-28; hook 13-25; conf 84 | "limine-mkinitcpio \"$@\"" (limine-update raw 25) | ADMIT, PW5/PW9. Byte-identical to the installed `/usr/bin/limine-update` (sha256 `55b7d578…`). Flip: upgrade. |
| S359 (new, code/A) | https://gitlab.com/Zesko/limine-snapper-sync/-/raw/1.32.1/src/main/java/org/limine/snapper/processes/KernelReader.java (+ Limine.java, Hash.java, Config.java), 2026-11-06, raw 154-157, 175-179, 196-213 | "String snapshotPathValue = Utility.buildPath(config.machineID(), Config.HISTORY_FOLDER, fileHashName + blake2sum);" (raw 210) | ADMIT, PW6/PW7/PW8. The mechanism by which a stale main pin is copied into new snapshot entries. Flip: limine-snapper-sync upgrade. |
| REJECTED: installed native binaries `/usr/lib/limine/limine-entry-tool`, `/usr/lib/limine/limine-snapper-sync` (strings) | local files, read 2026-11-06 20:44 by the L1 (`grep -n -i 'blake2\|ENABLE_VERIFICATION'` over the binaries) | symbol names only: "computeBlake2", "blake2IntegrityCheck", "ENABLE_VERIFICATION", "fileHashIntegrityCheck" | REJECT as a source: names in a GraalVM image show what exists, not what the code does; the tag source (S355-S359) is the evidence. Flip: none; kept as the pointer that led to the tag source. |

Registry changes, old→new: S355–S359 absent → `mined` (opened 2026-11-06; recheck `on-release`). No existing row's
status, recheck or used-by changed. At landing the L1 also pinned `limine-entry-tool-1.40.0/Main.java` (opened
2026-11-06 ~20:50, same tag; added to `URLS.txt`/`SHA256SUMS` after the candidate commit, cited by PW5's option list)
because wave seat ReviewEntry found PW5's option-list clause uncited and its own fetch hit HTTP 429.

Census (`sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi`): round start rc 0, 354 rows,
52 W04, `tsukuroi ok` (`.ufo/waves/round-88/before/census-before.txt`) → round end in
`.ufo/waves/round-88/after/census-after.txt`. Rows added by tier: A +5 (S355–S359).
Assimilation: none (no `merge/tsukuroi/` theme fits a Limine-writer surface; nothing adopted). considerthese: latest
file `considerthese/2026-10-26.md`, not mined this round.

## Mistakes

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| M1 | a forgery control recorded as evidence of isolation read `unmet` because it crashed, and it was only run from one layout of the counting command (`R88-CONTROL-PASSED-BY-CRASH`) | Freeze receipt `.ufo/waves/round-88/before/controls/bat-roster-oracle.receipt.txt` (0/3, 0/45 ×3, run with the counter in the canonical lane). Wave seat CriticClaims reproduced the reason: inside the sandbox the control dies with `FileNotFoundError` on the lane roster path (`w1/CriticClaims/f4-roster-oracle-from-lane.txt`), so every row is an `error:` row, not a verdict. Run from a `git clone --shared` (the declared counting layout), the counter hides only the clone, and the same unmodified control reads 3/3, 45/45 `met` rc 0 (`w1/ExecReplicate.md` §4-5, `w1/CriticClaims/f1-roster-oracle-from-clone.txt`). A roster walker reads `met` from the canonical layout too (`f9-glob-roster-v3-from-lane.txt`). | wave seats ExecReplicate (D1) and CriticClaims (F1); the freeze had no rule that a control must fail for its named reason | QUALITY 126 (below). The r88 counter is frozen and stays as measured; its successor masks the clone origin and every host root that can hold a roster copy (patches `w1/ExecReplicate/patch-isolation-hide-origin.diff`, `w1/CriticClaims/proposed-sandbox-allowlist.patch`, both validated: oracle `met` → `unmet`, candidate still `met`). Shown able to fail: the r88 receipt pair itself — the canonical-layout control rows are all `error:json FileNotFoundError` (crash, not verdict), which the QUALITY 126 check rejects. |
| M2 | an instrument docstring promised a void condition the code never checks, and a perturbation was described as hiding identity while it only appended to it (`R88-PROMISE-IN-DOCSTRING-NOT-CODE`) | `tools/battery-discrimination-r88.py:11-12` "void (exit 2) if this file or any roster file differs from … freeze-manifest.sha256"; no code reads the manifest, and `--roster` accepts any path: a forged one-gate roster read `met` rc 0 (`w1/CriticClaims/f5-forged-roster.txt`), a label-flipped roster ran as an ordinary `unmet` (`w1/ExecLints.md` L-1). `:15-16` "so no stored digest or name identifies it": the nonce is an appended comment, and a battery that strips it and looks the digest up reads `met` (`w1/CriticClaims/f2-embedded-digests.txt`, AST-normalised `f3`). | wave seats ExecLints (L-1) and CriticClaims (F2, F3) | The kill rule was enforced outside the instrument this round (`sha256sum -c` of the freeze manifest in every C1 receipt: `after/measured/c1-receipt*.txt`). Successor: the counter reads the manifest and voids, drops `--roster`, and its receipt states the certified set as behavioural batteries only. Shown able to fail: `f5` (forged roster, `met`) is the control a manifest check must turn into exit 2. |
| M3 | a probe run on pre-landing working-tree bytes was read as landed evidence (`R87-PRE-LANDING-EVIDENCE-READ-AS-LANDED`) | r87 `.ufo/waves/round-87/after/residual-diff/controls.txt:1-2` names "working tree (patched, pre-landing)", sha256 `1b51a68f…`; the landed gate is `e3b0fab4…` (`round-87-verifier-spotcheck.md` §5 item 1). | the r87 non-author spot-check, routed 1 | Re-run on the landed bytes at `3ba37eb0`: 11/11 discriminating, candidate = base on all 11, rc 0 ×3; negative controls g07 (1 disagreement) and g10 (2) read rc 1 (`w1/ExecResidual.md` §2, §4). The same class appeared in this round's first C1 receipt (measured at candidate `5b98ca98`, not the tip); answered by re-measuring at the tip in both layouts (`after/measured/c1-receipt-1fac4195.txt`, `c1-receipt-canonical.txt`) and by naming the battery digest `ab6c1b33…` in each. Shown able to fail: the r87 pair (`1b51a68f…` ≠ `e3b0fab4…`) fails a digest-equals-landed check. |

## Errata

- **R87-R6** (`.ufo/waves/round-86/w1/ScoutHost.md:23`, not edited): the column headed "sha256 before (recorded in
  `/boot/limine.conf`)" holds the leading 8 hex of the 128-hex BLAKE2b-512 pins, not SHA-256. Full values:
  line 30 `b990d8c699ef1987…db784cf9`, line 38 `a68c281d9e34c1bf…be539c14`
  (`.ufo/waves/round-87/after/live-receipt.txt:5`; prefixes equal the r88 host receipt). The file's own body already
  says BLAKE2b-512 (`ScoutHost.md:51-52`, `:82-83`); no value or conclusion changes. Likely origin: the history
  copy's name ends `_sha256_…` (limine-snapper-sync names history files by SHA-256 of content, PW7), a different
  field. Draft: wave seat ScribeLesson (`w1/ScribeLesson/erratum-R87-R6.md`).
- **R87 report, "Landed byte-identical"** (fleet `.ufo/reports/round-87/tsukuroi.md`, Work performed, ReviewGate
  bullet; fleet commit `a547d8e1`, not edited): the landed gate was not byte-identical to
  `w1/ReviewGate/check-limine-pins.proposed.py`. Proposed 12691 B `1b51a68f…`, landed 12821 B `e3b0fab4…`; the delta is
  one docstring hunk of 5 lines (ESP-confinement clause, "Y or y"), no executable change
  (`.ufo/waves/round-88/w1/ExecResidual/receipts/diff-prelanding-vs-landed.patch`). Read: "landed with the ReviewGate
  patch; it differed from the proposed file only in the header docstring". Found by wave seat ExecResidual (§6);
  same class as M3.

## Wave provenance (r87 routed 4)

`.ufo/waves/round-87/w1-results.json` records 12 seats, all 12 with `"output": null` and one note (orchestrator
kernel restart); `.ufo/waves/round-87/w1/finals/` holds 13 files, all mtime 2026-11-06 20:23:39, recovered from the
session store. CriticLimine, ScoutSources and ScoutRepair have no seat-written file under `.ufo/waves/round-87/w1/`;
their finals are quotable but are not seat receipts. Round 88's wave context required seats to write receipts to disk
as they go (`.ufo/waves/round-88/w1-spec.json` context). Draft: `w1/ScribeLesson/wave-provenance-r87.md`.

### Gate addendum at landing (after the wave's reviews)

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| S360 (new, own-work/A) | installed `/usr/bin/limine-mkinitcpio` and `/usr/share/libalpm/scripts/limine-mkinitcpio-install` (limine-mkinitcpio-hook 1.40.0-2), read-only `cp` 2026-11-06T21:16:26-03:00 into `.ufo/waves/round-88/after/host-scripts/` (sha256 `e0c8375b…`, `22e44591…`) | "limine-entry-tool --add-uki \"$name\" \"$file\" \\" (limine-mkinitcpio-install line 196) | ADMIT, PW5. Wave seat ReviewEntry rated PW5 partial (the re-add claim was inference); the upstream tag copies returned HTTP 429 to the L1 and to seats ReviewEntry and ScoutSources, so the installed bytes the host actually runs are the evidence. It corrected the entry: the repair rebuilds the UKIs (new bytes, new pins), it does not pin the rewritten bytes. Flip: a limine-mkinitcpio-hook upgrade. |

Registry changes, old→new (landing): S360 absent → `mined`; S355 anchor gains `Main.java raw lines 45-207` (pinned
`c76c3c61…`) and its `teaches` gains "no hash-only refresh option exists". No other row changed.
Entry fixes from wave seat ReviewEntry (7 support, 2 partial): PW2 source + `S355 LimineManager.java 359-372`; PW4
wording ("first hash of that final, mismatched pair"); PW5 rewritten on S360 with split `[src]`/`[obs]` tags; PW8
"observed 19:27 and 20:27" instead of "hourly"; PW9 adds "and Limine is v12" (range 13-25); Operator action 2 now
states the rebuild and its wider `/boot` writes.

## Wave w1 (12 seats; seats wrote their own receipts)

executor 3 (ExecReplicate, ExecResidual, ExecLints), mutation-tester 2 (MutBattery, MutHeldOut), critic 2
(CriticForgers, CriticClaims), reviewer 2 (ReviewBattery, ReviewEntry), scout 1 (ScoutSources), scribe 1
(ScribeLesson), connector 1 (ConnectorOverlap); attack seats 6/12. Integrated: ReviewEntry's row fixes, ExecResidual's
landed-bytes re-run, ScribeLesson's drafts (M3, erratum, provenance), ConnectorOverlap's completed scan. Not
integrated (frozen instruments; routed below): the counter patches (ExecReplicate D1, CriticClaims F1-F3), battery
findings (ReviewBattery F1-F5, MutBattery, MutHeldOut, CriticForgers).

## Routed to round 89

- R88-R1 (CriticClaims F1-F3, ExecReplicate D1, ExecLints L-1): a successor counter — mask the clone origin and every
  host root that can hold a roster copy (allowlist root, patches in `w1/ExecReplicate/` and `w1/CriticClaims/`), read
  the freeze manifest and void, drop `--roster`, count `error:` rows separately, and run each forgery control from
  both layouts before freezing (QUALITY 126). A source-text-fingerprint battery (F2) is outside any sandbox; certify
  behavioural batteries only and say so in the predicate.
- R88-R2 (MutBattery ¹): `WHITESPACE-CRLF` draws CRLF with p 0.6 per case, so `N-m22`/`N-g15` escape a run with
  probability 0.4⁴ ≈ 2.6 %; the pristine battery read `met` on `N-m22` in 1 of 8 of the seat's runs. Every C1 run this
  round read 45/45 (12 counter runs by the L1 in four receipts, 3 by ExecReplicate), but the CR clause is certified by chance. Make the
  CRLF case deterministic.
- R88-R3 (MutBattery 4.3): `r8_ok`'s `hash_mismatch_panic.value` comparison has no detector (M18 survives both the
  counter and the selftest); add a value-lie wrapper and a roster gate that lies about the value.
- R88-R4 (MutBattery 4.1-4.2): 14 redundant lines or families (`ALL-PIN-KEYS` whole, `SB-FLAG-ZERO`, decoys); the
  selftest kills weakened expectations only through lie wrappers — six counter-killed mutants pass it.
- R88-R5 (CriticForgers, MutHeldOut): clauses r88 leaves uncertified — f01, f03, f06, f07, f08, f12, f14, f16, f18,
  f19 and h01, h10, h11, h19, h20; ReviewBattery F1 (Limine resolves `boot(N)` when partition N exists; unknown
  resources halt) and F3 (a URI-less path is an entry failure, not "ignored").
- R88-R6 (CriticClaims F4): name C1-class claims by their surface — battery calibration — in the declaration.
- Host repair of lines 30 and 38 stays operator-owned; PW5/Operator action 2 now say what `limine-update` does.
