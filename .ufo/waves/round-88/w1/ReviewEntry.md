# ReviewEntry — C2 row-by-row review: corpus/knowledge/limine-pin-writers-r88.md (+.json) vs pinned sources

Lane revision measured: `1fac4195243e55e7d9d8a2eddd653443d8559bff` (git rev-parse master). Reviewed 2026-11-06.
Pin set: `.ufo/waves/round-88/before/src/` — `sha256sum -c SHA256SUMS` → rc 0, all 14 files OK (receipts-01).
Method: every quote re-located at its cited raw lines (`grep -n`/`sed -n`, exact numbers in receipts-01);
negative claims swept across the whole pin set (receipts-02); host values checked against
`.ufo/waves/round-88/before/host/receipt.txt`; .md compared field-by-field with .json.

## Verdicts (7 support, 2 partial, 0 unsupported)

| Row | Verdict | Evidence / defect | Proposed fix |
|---|---|---|---|
| PW1 | support | Quote verbatim at ConfigReader.java:31, inside cited 28-32; the four load calls + `// 1. Lowest priority`/`// 4. Highest priority` comments state the order; DEFAULT_CONFIG_FILE_PATH = `/etc/default/limine` (Config.java:8). Host value matches receipt exactly (conf:84 yes; no EV in /etc/default/limine; only resume.conf; /usr/share dir absent). | none |
| PW2 | **partial** | Quote verbatim at ConfigReader.java:175; case-insensitive `yes` + `isCommandPresent("b2sum")` + default false (Config.java:19, else-branch :177) all check out. Gap: the last clause "writes the path with no `#` at all" is sourced by LimineManager.b2sum() returning "" (S355 359-372), which PW2's source column does not cite (PW3 does). | Extend source to "S356 ConfigReader.java 173-177, Config.java 7, 19; S355 LimineManager.java 359-372". |
| PW3 | support | All cited lines exact: pins at 325 (module_path, inside the per-initrd loop → "every"), 329, 331, 353; CMDLINE (332/354) and COMMENT (308/348) carry no b2sum. Quote verbatim at :353. Host value (pins only on lines 30/38) matches receipt. | none |
| PW4 | support (wording nit) | Quote verbatim at Utility.java:144; two parallel futures (144-145), retry loop, final `errorMessage("Repeated hash mismatches. Hardware is faulty…")` :164 then `return hashResult1` :165; cited 118-175 ends exactly at the method's closing brace. Nit: :165 returns the first hash of the **final mismatched pair**, not "the first result" overall — current wording can misread. | Reword: "…and after the last retry it logs 'Hardware is faulty' and still returns the first hash of that final (mismatched) pair." |
| PW5 | **partial** | limine-update verified: `limine-install --no-efi-register` at :16, `limine-mkinitcpio "$@"` at :23 (quote verbatim, cited 16-28); installed-byte identity in receipt. Two defects: (a) the clause "which is the path that re-adds entries and so rewrites their pins" is **inference** — the limine-mkinitcpio body is not pinned (entry Limits disclose this), so the row's blanket `[src]` tag overreaches its strongest sentence; (b) "its `Main.java` options are add/remove/scan/tree/cmdline" cites nothing: Main.java is not in the pin set and no S-row covers it. My fetch of Main.java 1.40.0 got HTTP 429 twice (receipts-03) — factual truth unverified by anyone this round. | (a) Split the tag: sentence 1 `[src]` (S358 limine-update 16-28); the re-add/rewrite clause `[inf]` with "limine-mkinitcpio body not pinned" inline (keep S355:353 as the write-site). (b) Pin `src/main/java/org/limine/entry/tool/Main.java` @1.40.0 as a new S-row (or extend S358) and cite the subcommand list — or move the parenthetical into Limits as unverified. |
| PW6 | support | Windows exact: 154-157 (patterns/matchers), 175-179 (`hashMatcher.find()` first/leftmost match :176-178 — the cut), 196-213 (fresh content hash :199 → name :209 → `snapshotPathValue = …fileHashName + blake2sum` :210, quote verbatim); Limine.java:28 HASH_PATTERN. Negative claim verified by sweep: no `b2sum`/BLAKE2 computation anywhere in the pinned snapper-sync set; the pin text only ever flows from the regex capture (receipts-02). Host value matches receipt + r87 live receipt (history pins 50/56/64 `OK`; snapshot headers 2026-10-20). | none (residual disclosed below) |
| PW7 | support | Name-from-content-hash chain exact: KernelReader 196-209 (calculateHash :199, `fileName + HASH_FUNCTION.hashName + hashSum` :209), Config.java:46 `HASH_FUNCTION = Hash.SHA256`, Hash.java 60-66 with quote verbatim at :66 — compares name suffix vs content, never the pin. Host: history names end `_sha256_<64 hex>` per receipt. Nit: `hasCorruption`'s caller lives in unpinned Utility.java — the method-level claim stands as written. | optional: note the caller file is unpinned |
| PW8 | support (as `[inf]`) | Tag honest: consequence row, "Not executed: no snapshot was created this round" stated in-row. Chain holds on pinned code (PW6 copies text; PW7 names the fresh copy) and the half that is host-checkable is corroborated: journal `Updated: /boot/limine.conf` 19:27:27 and 20:27:30, main pins unchanged at 20:53 (receipt); r87 live receipt shows exactly the LP-MISMATCH/prompt mapping cited. Nit: "hourly" generalizes from two runs 1 h apart. | optional: "the 'Updated' runs (observed hourly, 19:27/20:27)". |
| PW9 | support (completeness nit) | Quote verbatim at 89-warn-missing-file-hashes:22, inside cited 19-25; gate condition at :20-21 matches all four listed conditions. Gap: the conjunction also requires `check_limine_v12` (Limine major 12, :15-17). The four listed conditions remain necessary, so the sentence is true, just incomplete. Host conclusion unchanged (ENABLE_UKI=yes at /etc/default/limine:8 already falsifies it). | Add "and Limine is v12" to the enumeration. |

## Cross-checks
- .md ↔ .json: PW1-PW9 statements, sources, quotes, host values identical field-for-field.
- Header block complete and consistent (source list = S355-S359, verified-at, host capture path, recheck, machine-readable rows, snapshots, companion, Gate).
- SOURCES.md S355-S359 rows (lines 365-370) match the entry's per-row attributions and the pinned digests.
- Host values: PW1/PW2/PW3/PW5/PW6/PW7/PW8/PW9 each verified against the receipt (PW4's `—` is acceptable for a pure-source row).

## Operator actions (the requested check)
No action instructs a seat or the entry itself to write the host; all three executing steps are
`sudo` read-only checks (`check-limine-pins.py --live` — proven byte-neutral by the r87 live receipt,
`cmp` identical) or explicit operator decisions. Action 2 (`sudo limine-update`) is the only host-write
recommendation: it is correctly operator-owned, its trust implication is stated ("accepts the rewritten
UKI bytes as trusted"), and its `limine-install --no-efi-register` side effect is disclosed. One gap:
it does not say that `limine-mkinitcpio "$@"` also **rebuilds the initramfs** (writes /boot images), so
the operator should expect the blast radius to exceed the pin rewrite. Suggested clause: "(note:
limine-mkinitcpio rebuilds the initramfs images, so /boot changes beyond limine.conf)".

## Residual risk / verification gaps
1. Unpinned links in otherwise-supported chains: snapper-sync `Utility.java` (calculateHash /
   fileHashIntegrityCheck bodies; also the only possible caller of hasCorruption) and
   `ImageDetail.getSnapshotLine()` (final line-assembly hop). The pinned write path plus the host
   receipt make these low-risk, but a future pin of snapper-sync Utility.java would close them.
2. PW5's Main.java clause: unverifiable this round (GitLab 429 ×2 + backoff retry, receipts-03);
   entry-tool `limine-mkinitcpio`/`limine-install` bodies unpinned (the entry's Limits say so — the
   Limits section is honest; the row tag is what needs the fix).
3. `hash_mismatch_panic: no` behavior and the LP-MISMATCH/prompt mapping are taken from the r87 entry
   (LP5/LP8) and r87 live receipt, not re-derived here — out of this review's scope (r87 ground).

## Receipts
- receipts-01-digests-and-lines.txt — 14/14 digests OK; every quote's exact raw line.
- receipts-02-snapper-negative-sweep.txt — the no-recompute sweep and caller census.
- receipts-03-mainjava-fetch.txt — the three 429/failed fetch attempts with timestamps.
