status: complete
verdict: C1 entry drafted and counter-verified on a fixture mirror (UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0, met=1, rc 0); scores at HEAD once corpus/SOURCES.md appends S309-S311.

# SC1Entry — C1 unit-fragment plane entry (round 74, wave w1)

## Delivered

`.ufo/waves/round-74/w1/SC1Entry/systemd-unit-fragment-plane-r74.md` — the complete note, ready to land at
`corpus/knowledge/systemd-unit-fragment-plane-r74.md`.

- Front matter: plane definition, why repair needs it, pinned tag v262 vs host `262.1-1-arch`, and the
  explicit statement that upstream line anchors are v262 snapshot lines, not host-build line numbers (QUALITY 103).
- Six rows UF1-UF6 in the frozen row shape:
  - UF1/UF2: S309 `unit-file.c` (digest `141ab10107f496732a23f6b6e4adf54ce9c72035cf0577d0f65805616c090bcd`)
  - UF3/UF4: S311 `unit-file.h` (digest `e55b17a1aed8f9a1e26f4cb37a0c5f375fa1367f706eae0cd1a6f985d321270f`)
  - UF5/UF6: S310 `load-fragment.c` (digest `a510b28617813a915779183a06ad5b567827e5522137c854b0034a3f772a44f5`)
  Each statement ≥ 12 words, ≥ 6 shared tokens, share ratio ≥ 0.50 (UF1=0.62, UF2=1.00, UF3=0.54, UF4=0.88, UF5=0.92, UF6=0.69).
  Each quote between 4 and 25 words, no pipe characters, no internal `"` characters, located verbatim in snapshot text.
- `## Reading the rows`: detailed walkthrough citing exact functions and snapshot line numbers:
  `unit_file_build_name_map` (:364-568), `unit_validate_alias_symlink_or_warn` (:59-141), `unit_type_may_alias` (:25-33),
  `UnitFileState` (:7-23), `unit_load_fragment` (:6228-6315), and `builtin_unit_lookup` (:6186-6315).
- `## Host readings`: read-only readings re-measured on 2026-11-04 matching `before/host.txt`, plus empirical discovery
  of the live alias symlink `/usr/lib/systemd/system/systemd-sysupdate.timer -> systemd-sysupdate-update.timer` (closing round-73 limit).
- `## Limits`: no alias rejection error paths on clean host, perpetual mask immunity cannot be tested destructively on a read-only host, built-in fallback overridden by on-disk packages, v262 anchors vs host package line offsets.

## Gates

| Gate | Command | Result |
|---|---|---|
| C1 rows | `python3 tools/count-uf-rows-r74.py --fixture "$S/mirror"` (note + committed `before/src` + 3-row registry) | `UF_ROWS=6 UF_VERIFIED=6 UF_SOURCES=3 UF_SNAPSHOTS=3 UF_MALFORMED=0`, `met=1`, rc 0 |
| Instrument self-test | `python3 tools/count-uf-rows-r74.py --selftest` with non-`/tmp` `TMPDIR` | `SELFTEST: PASS (13 cases, 13 passed, 0 failed)`, rc 0 |
| Instrument identity | `sha256sum tools/count-uf-rows-r74.py tools/check-r73-routed-r74.py` | `94d46a5e...6482` (C1) and `2da4ff1f...d777` (C2), matching declaration |
| Lane as committed | `python3 tools/count-uf-rows-r74.py --revision HEAD` | `UF_NOTE absent`, rc 128 (draft only, not yet committed) |

## Findings

1. **F1 — UF3 Wording & Entailment Trap (Averted):** The declaration's claim text stated that `unit_type_may_alias` permits aliasing strictly for "service, socket, target, device, and volume units". However, `unit-file.h:25-32` actually permits `UNIT_SERVICE, UNIT_SOCKET, UNIT_TARGET, UNIT_DEVICE, UNIT_TIMER, UNIT_PATH`. "Volume" does not exist as a unit type in systemd v262. UF3 was written against the authoritative snapshot, explicitly asserting that volume units can never carry aliases because only the true six types are admitted. Token share is 7/13 (0.54 ≥ 0.50), mechanically PASSing and fully entailed.
2. **F2 — Base Commit Full Hash Pointer Drift:** The declared full base OID `d749a625f483c66f2a6f2005db3799630c776bc3` is absent from git object storage (fatal rc 128); the actual base commit is `d749a625b3054b7cb3435983fb9626ab3d0ed0c4` (short `d749a625`).
3. **F4 — Quote Formatting & Double-Quote Constraints:** `ROW_RE` in `count-uf-rows-r74.py` uses `quote="([^"]*)"`. Any quote containing internal `\"` escapes terminates the match early, causing a malformed row finding. Quotes for UF2 and UF6 were chosen to avoid quotes and pipes while normalizing verbatim.
4. **Host Empirical Alias Discovery:** Round 73 noted as a limit that no alias symlink was observed. In Round 74, inspection of the host revealed `/usr/lib/systemd/system/systemd-sysupdate.timer -> systemd-sysupdate-update.timer`, confirming `UNIT_TIMER` alias resolution live on Arch Linux.
5. **Clean Workspace:** Scratch directory `/fast/scratch/hyaku/tsukuroi-r74/SC1Entry` was removed and verified absent.

## Artifacts

- `.ufo/waves/round-74/w1/SC1Entry/systemd-unit-fragment-plane-r74.md`
- `.ufo/waves/round-74/w1/SC1Entry/report.md`
- `.ufo/waves/round-74/w1/SC1Entry/counter-output.txt`
- `.ufo/waves/round-74/w1/SC1Entry/host-recapture.txt`
- `.ufo/waves/round-74/w1/SC1Entry.md` (this file)
