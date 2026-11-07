# ConnectorOverlap — sibling-overlap scan for the r89 C2 facts

scanned-at: 2026-11-06 (wall clock read at 22:2x -03:00)
lane measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` →
`665408cc45a88ed49717e22f4593e8e6152ac665` (pre-round tip `dfeaab29`, candidate `81f68d00`; lane worktree
already carried an uncommitted `corpus/QUALITY.md` and `.ufo/waves/round-89/` entries — not mine, not touched).
scope: every sibling repo under `/home/vgpnk/Projects/shokunin/*-shokunin` except tsukuroi (20 repos), tracked
files only, `git grep`/`git show`, no writes to any repo, no host probe, no subagent.
reference rows: `corpus/knowledge/limine-uri-failure-r89.md` UF1-UF8 and
`corpus/knowledge/limine-pin-plane-r87.md` LP1-LP8 (read at lane master above).
receipts: `.ufo/waves/round-89/w1/ConnectorOverlap/` (`scan-meta.txt`, `grep-corpus.txt`, `grep-all.txt`,
`limine-precise.txt`, `rare-terms.txt`, `rare-rc.txt`, `per-repo-counts.txt`, `uki-knowledge.txt`; each line
truncated to 400 chars in the copies).

Commands used (per repo, cwd irrelevant; every command is read-only):

```
git -C "$r" grep -n -i -E 'limine|chainload|measured_boot|hash_mismatch' -- corpus
git -C "$r" grep -n -i -E 'limine|chainload|measured_boot|hash_mismatch' -- .
git -C "$r" grep -n -i -E '\blimine\b|hash_mismatch_panic|measured_boot|chainload|\buki\b|secure ?boot|blake2b' -- .
git -C "$r" grep -n -i -E 'chainload|hash_mismatch_panic|measured_boot|limine\.conf|limine-pins|LP-UNRESOLVED|LP-MISSING|limine-snapper|boot\(\)|boot\(N\)' -- .
git -C "$r" grep -n -i -E '\blimine\b|limine\.conf' -- LOG.md SCORECARD.md
git -C "$r" show HEAD:<path>            # for each quoted hit
```

## Headline

**No sibling lane holds a Limine semantics fact.** `chainload`, `hash_mismatch_panic` and `measured_boot`
return **0 hits in 20/20 repos** (each `git grep` rc 1, 0 lines; `receipts/rare-rc.txt`). There is no
sibling prior art on URI resources, the `efi` chainload panic, Secure Boot's no-hash rule, measured-boot halting,
or Limine panic behaviour. No sibling text conflicts with UF1-UF8 or LP1-LP8.

What exists is host-surface observation: sibling lanes recorded the same host's Limine *installation* (limine
12.9.3 at 2026-10-20, now 12.9.4-1), its pacman hooks, its `/boot` layout and its limine-snapper processes. One
hit is genuinely adjacent and not in any lane entry: a host script that **moves `/boot/limine.conf` aside**, i.e.
can drop every pin without touching a UKI (Proposal below).

## Repos scanned and HEAD

HEAD as read at the end of the scan (2026-11-06 22:2x -03:00). Sibling lanes are live: `kagi` (7eab7aa4 →
affb270b), `mado` (847f589a → d992ef74), `souji` (eef6f30c → 9cbfd296) and `tabi` (3409ab53 → c44fcf6f)
advanced during the ~40 s sweep; each hit below names the HEAD it was read at.

| repo | HEAD | Limine-term files | note |
|---|---|---|---|
| audio-shokunin | f9da7ee97e0ba95da1803c2afe9c616c519bae18 | 0 | — |
| chousa-shokunin | 408ae68f9e445fc911f713d5bbb3a64dda1ab9fe | 13 | binary captures + copies of tsukuroi docs |
| game-dev-2d-shokunin | 1e033ef053beedf9a201daa21fbeb9c8b2f72dc3 | 7 | `hash_mismatch` in a repo-integrity audit |
| game-dev-3d-shokunin | 39ca3973c7865456d97fae18033f3f460c6cf8c1 | 33 | all `pybullet*.so` binary matches |
| kagi-shokunin | affb270bc9288bf08f72a0197d705cc06ec5ac67 | 0 | — |
| kaidoku-shokunin | 0b518f568da7b40a4ab026508d63c942faa7badf | 13 | `hash_mismatch` = receipt hashing |
| kake-shokunin | dd7a146df338ec3de07a88f08f36c8278760afec | 3 | `boot()` in a Wayland fixture generator |
| kama-shokunin | e2e5fd9bdda08b852db50e0e0272032b280a3373 | 1 | tsukuroi SKILL quote (host guard) |
| kasegi-shokunin | e73c1f945b5c08f5ecfec13d9ff5acfaf8f865d0 | 0 | — |
| kengaku-shokunin | 34b28c47bc38b4e0aa11f44f2dfe7c9470d551ac | 10 | unrelated hash/receipt strings |
| kotoba-shokunin | 0344ddaea831b92546360a55ae02db2654fbccf8 | 4 | omp binary strings + tsukuroi census copy |
| kotodama-shokunin | 5fa04a9bbda25aa31c8270265fd9997eb97d9ebb | 14 | Latin `in limine` + PDFs |
| kumitate-shokunin | 8191f90e2e254a5a6130b2c8e96ab4938fc77ca8 | 3 | `hash_mismatch` = local-ship rollback kind |
| lore-shokunin | 0f044aa7c7e4e17cfd5b6278179709b60db45d61 | 0 | — |
| mado-shokunin | 847f589a… (read) / d992ef74… (final) | 21 | host hook/journal + bwrap probes + S209 |
| mori-shokunin | 7765969c79e6f3df44cce2e303e6a0cf2b054d8b | 11 | host `/boot` + pacman provenance |
| revenger-shokunin | 654d09298960d0886274d37a0492b8e6d98b2c96 | 0 | Arm boot-chain (TF-A) only, no Limine |
| souji-shokunin | eef6f30c… (read) / 9cbfd296… (final) | 1 | tsukuroi SKILL copy |
| tabi-shokunin | c44fcf6f11fe549e8585e073e1cfad66dc2e2cbb | 6 | host autostart log + ps samples |
| tameshi-shokunin | 87d1635c8a1a90a405eb348da5ba3e8f93b4ae83 | 4 | tsukuroi tool-registry copy |

"Limine-term files" = count of `git grep -l -i -E '\blimine\b|hash_mismatch_panic|measured_boot|\buki\b|chainload' -- .`
(`receipts/per-repo-counts.txt`); it counts binary hits.

## Substantive hits

Format: repo @ HEAD read — `file:line` — fact — relation to UF/LP. Quotes are the sibling's own text.

| # | repo @ HEAD | file:line | fact | relation |
|---|---|---|---|---|
| H1 | mori @ 7765969c | `.ufo/waves/round-24/w1/ScoutHostKernelConfig.md:76` | `/boot` listing: "`amd-ucode.img`, `EFI/`, `limine.conf`, `limine.conf.old`, `loader/`, `432d02b544a5459ebbff9c42ec68334d/limine_history`, nothing else" | **agrees UF2/UF5** host observation set and **extends LP8** (file state); the history dir id `432d02b5…` is identical to the one in the lane's r88 receipt. No conflict. |
| H2 | mori @ 7765969c | `.ufo/waves/round-24/w1/ScoutHostKernelConfig.md:94` | "all five configured cmdlines in `/boot/limine.conf` (lines 31, 39, 51, 57, 65 …) are the same string and none contains `psi=`" | **agrees UF2/UF5**: five entries carry `cmdline:` at path-line+1 (paths 30/38/50/56/64), matching the lane's six-`efi` layout (fallback entry at 67/72 has no captured cmdline). Independent earlier read; no conflict. |
| H3 | mori @ 7765969c | `.ufo/waves/round-17/build/PacmanTxnToday.md:62-63,66,124` | `limine` 12.8.0 → **12.9.3** (`:2851`), `limine-mkinitcpio-hook` 1.40.0-2, `limine-snapper-sync` (`:2854`); "The UKI rebuild that followed is logged at `:2990`–`:3063`"; "the off-log `limine-update` hook rebuild after the upgrade is likewise tsukuroi-reported" | **agrees the r87/r89 version claim** (host now 12.9.4-1) and **agrees r88 PW5** (`limine-update` rebuild); temporal lineage, no conflict. |
| H4 | mori @ 7765969c | `.ufo/waves/round-17/build/OverlapTsukuroi.md:38,50` | "mkinitcpio/UKI/hook risk analysis is exclusively tsukuroi's; mori records only liveness correlation around a boot" | **agrees the lane boundary**; no UF/LP fact. |
| H5 | mori @ 7765969c | `.ufo/waves/round-31/w1/ConnectorSiblings.md:68` | `tsukuroi/tools/check-boot-writers.py:2-6` — "Verifier for `/boot/limine.conf` writer attribution" — "**ignore**: name collision only" | **agrees** the writer gate exists (r88 plane); no conflict. |
| H6 | tabi @ c44fcf6f | `corpus/evidence/w4-t4-3-sweep/forensics.log:57,59` | "Failed to create unit file '/run/user/1000/systemd/generator.late/app-limine\x2dsnapper\x2dnotify@autostart.service': File exists" (same for `app-limine\x2drestore\x2dnotify`), 2026-10-14 13:11:07 | **extends r88 PW6/PW8** context: limine-snapper-sync's notify/restore autostart units on this host; no UF/LP row, no conflict. |
| H7 | tabi @ c44fcf6f | `.ufo/waves/round-63/w1/R63Sentinel/samples/run1-ps-2.txt:384` (same in `run2-ps-2.txt`, `run2-ps-5.txt`) | `2629 1487 bash /usr/bin/limine-snapper-notify` | **agrees H6** and extends: the notifier process was live at round 63; no conflict. |
| H8 | tabi @ c44fcf6f | `.ufo/waves/round-15/w1/ToolsSafety.md:14,31` | `limine*` among boot-chain packages in the partial-upgrade hazard; "every logged install runs `10-limine-snapper-lock.hook` and `35-systemd-update.hook`" | **agrees the host guard/update-safety gate**; extends pacman-hook provenance; no UF/LP. |
| H9 | mado @ 847f589a | `.ufo/waves/round-15/w1/reports/LibinputTools.md:167` | "unsynced partial package upgrade … triggering `10-limine-snapper-lock.hook` and `35-systemd-udev-reload.hook`" | same as H8; **agrees**, no conflict. |
| H10 | mado @ 847f589a | `.ufo/waves/round-17/w1/reports/IncidentTimeline.md:86,152` | `10-limine-snapper-lock.hook` ran during the 2026-10-20 transaction; "not that a snapshot was used" | same as H8; **agrees**, extends transaction record; no UF/LP. |
| H11 | mado @ 847f589a | `.ufo/waves/round-16/w1/reports/PolicyScope.md:118` | boot-chain tools (`limine*`, `grub-mkconfig`) are out of scope for mado; "mkinitcpio 42 risk" is tsukuroi's | **agrees the lane boundary**; no fact. |
| H12 | mado @ 847f589a | `.ufo/waves/round-35/scratch-evidence/SentProvenance/S209.convention.txt:5` | host script `/home/vgpnk/.local/share/omarchy/bin/omarchy-refresh-limine:12`: `sudo mv /boot/limine.conf /boot/limine.conf.bak` | **extends r88's writer plane / r87 LP8** with a config mover outside the pinned toolchain. No lane entry names it: the only lane match for `refresh-limine\|limine\.conf\.bak\|limine\.conf\.copy` is the r88 receipt's own saved copy of `/boot/limine.conf` (`limine.conf.copy`, sha256 `34b864…` at `.ufo/waves/round-88/before/host/receipt.txt:5`), a receipt artefact, not a knowledge row. No conflict; see Proposal. |
| H13 | mado @ 847f589a | `.ufo/waves/round-56/w3/R56W3MutBwrapChannels/receipts/jail-probe-bwrap.out:1568-1584` (also `jail-probe-nosb.out:1568-1584`, `probe-jail.out:1829-1845`) | bwrap jail probe: every `/bin/limine*` name returns `errno=20` while `/` and `/usr` exist (`/home` and `/tmp` false) | **C1-adjacent only** `[inf]`: a jail-construction pitfall (the `/bin` symlink target is absent while `/usr` exists), no UF/LP relation, no conflict. |
| H14 | tameshi @ 87d1635c | `.ufo/waves/round-55/w1/T55W1Connector1-receipts/06-kumitate-and-tsukuroi-emitters.txt:19` | tsukuroi tool registry: "Verify round-19 /boot/limine.conf writer attribution." | **agrees** gate provenance (H5); no fact. |
| H15 | souji @ eef6f30c | `census/round-43/waves/w1/R43connector01/scan-receipts.json:25` | tsukuroi SKILL "Journal & boot triage" command text | scope pointer only; no Limine fact. |
| H16 | kama @ e2e5fd9b | `.ufo/waves/round-18/build/advice/ConnectTsukuroi.md:28,50,74` | tsukuroi SKILL "authorizes no pacman, mkinitcpio, limine-update, snapper or service action"; kama must not run `limine-update` | **agrees the host guard/lane boundary**; no UF/LP. |
| H17 | kotoba @ 0344ddae | `.ufo/waves/round-71/receipts/census-after.txt:226` | tsukuroi S098 duplicate-URL row for `gitlab.com/Zesko/limine-entry-tool/-/raw/master/.../btrfs` | **agrees r88's limine-entry-tool source**; a copy of tsukuroi's own census, not sibling knowledge. |
| H18 | revenger @ 654d0929 | `corpus/knowledge/round-73-re-resource-atlas.md:309` | "Arm boot-chain stages (BL2/BL31/BL33) in a FIP are located by UUID ToC entries" | word overlap only (Arm firmware boot chain, not Limine); no relation. |

### Conflicts

**None.** No sibling text states a Limine resource rule, a panic consequence, a Secure Boot hash rule or a
measured-boot behaviour, so none can conflict with UF1-UF8 or LP1-LP8. The only near-miss is a version
difference, and it is temporal, not contradictory:

- mori (H3): `limine` **12.8.0 → 12.9.3** in the 2026-10-20 `-Syu` ("`limine` 12.8.0 → 12.9.3 (`:2851`)").
- lane r89 host receipt (2026-11-06T21:52:29-03:00): `pacman -Q limine` → `limine 12.9.4-1` (rc 0).

The lane's own r87 header already says "the host runs limine 12.9.4-1"; the sibling read predates the later
package, so both agree on the sequence. Likewise mori's five `cmdline:` lines (31/39/51/57/65) are consistent
with the lane's six `path:` lines (30/38/50/56/64/72): five entries + the `EFI fallback`.

## Noise classes (excluded, with counts)

- **Binary matches**: `game-dev-3d` 33 `pybullet*.so` files (regex inside machine code); `chousa` 3 captures
  (`file`: PDF 1.7 / OLE DOC / PDF 1.4 — `pdftotext` of both PDFs returned 0 lines for `limine|secure ?boot|blake2b`,
  rc 0/0, so the hit is in binary metadata); `kama`/`kotoba` omp binary strings.
- **Same word, different object**: `kotodama` `reports/round-60/captures/pages/S604.txt:5333` — Latin
  "Marmoreo aeratus stridens in limine cardo" (threshold); `kake`/`mado` round-41 `boot()` = a Wayland
  session-log fixture generator; `revenger` Arm boot-chain (H18); `game-dev-2d` `hash_mismatches` = repo
  integrity; `kaidoku`/`kengaku`/`kumitate` `hash_mismatch` = receipt/rollback hashing.
- **Copies of tsukuroi artefacts**: `chousa` round-73/80 `tsukuroi--corpus__*.blob`, `souji`/`tameshi`
  tsukuroi SKILL/tool-registry copies, `kotoba` census rows; they agree with the lane but add no independent fact.

## Proposal (one move)

**Route a "config movers outside the pinned writer toolchain" row to the pin-writers plane (r88-style), not to
the frozen r89 entry.** Evidence: H12. The r88 entry enumerates limine-entry-tool, limine-snapper-sync and
`limine-update` as pin writers; the `omarchy-refresh-limine` capture shows a fourth host-side actor whose line 12
**moves the live pin-bearing file aside** (`sudo mv /boot/limine.conf /boot/limine.conf.bak`) before whatever it
writes next. That is a third failure class beside the r86 in-place UKI rewrite (pin mismatch → `prompt`, LP5/LP8)
and PW6's copied stale pin (mismatch on new snapshot entries): **pin loss by config replacement**, with no UKI
byte change.

- **affected axes**: operability (a "refresh/repair" path can silently discard the verification state the r87
  gate is meant to report) and freshness (the provenance of the pin set: which host actors can invalidate it).
  It harms neither axis: it adds a row and a read-only check, changes no gate, battery rule, roster or predicate.
- **second-order effect**: with Secure Boot off (host state, UF7), an unhashed `path:` loads without a pin check
  (r87 LP6/Limits; the no-hash panic is a Secure Boot rule), so the stale-pin `prompt` on lines 30/38 would
  disappear **without the UKIs being repaired** and the gate would stop reading `LP-MISMATCH`; with Secure Boot
  enabled later, the same unhashed paths become the UF7 halt path. `[inf]` — not executed.
- **risks**: the capture is a grep excerpt (2026-10-25T03:35:12-03:00), not the full script; what it writes after
  the `mv`, and whether it ever ran on this host, is unknown. The lane's r88 receipt cat'd `limine.conf.old`
  (limine-entry-tool's own backup, not this script's `.bak`), and the r88 journal since 17:00 shows no
  `omarchy-refresh-limine` run. Treat as latent, not observed. Do **not** edit the frozen r89 C2 entry's UF
  table or the battery; the fact belongs in a later round's r88-plane row or the lesson's routed list.
- **verification** (read-only; I did not run these — host facts go through the L1):
  ```
  sed -n '1,60p' /home/vgpnk/.local/share/omarchy/bin/omarchy-refresh-limine
  grep -rn 'omarchy-refresh-limine' /home/vgpnk/.local/share/omarchy /home/vgpnk/.config 2>/dev/null
  sudo -n find /boot -maxdepth 1 -name 'limine.conf*' -printf '%f %TY-%Tm-%Td %TH:%TM\n'
  # if a .bak exists: sudo -n cmp -s /boot/limine.conf /boot/limine.conf.bak; echo $?
  ```
  The first shows whether the script regenerates a full config (with fresh pins) or a default without pins; the
  third shows whether a `.bak` exists at all; the fourth whether the backup differs from the live file.

**Secondary, no move**: H13 shows a sibling bwrap probe returning `ENOTDIR` for every `/bin/*` name while `/` and
`/usr` exist. If the r89 counter's isolation preflight ever needs one more assertion, resolving one `/bin` symlink
(or using `/usr/bin` paths) is the cheap one. Not a C2 fact; recorded only because the round's C1 arm depends on a
bwrap allowlist.

## Limits

- Sibling HEADs move (four advanced during the scan); every quoted hit names the HEAD it was read at. No sibling
  repo was edited; no host file was read directly, and the one host fact not in a committed receipt (H12's script
  body and any `.bak`) is listed as a read-only command above.
- The sibling captures are historical (2026-10-14 … 2026-10-25); none is a current host probe. H12's script may
  not be wired to anything; the capture does not show the rest of the file.
- The scan is lexical: a fact stated without the words `limine`, `chainload`, `measured_boot`, `hash_mismatch`,
  `UKI` or `Secure Boot` would be missed. No sibling corpus entry is titled or filed under a Limine topic
  (`git ls-files | grep -i limine|uki|boot-chain|secureboot` → 0 files in 20/20 repos).
