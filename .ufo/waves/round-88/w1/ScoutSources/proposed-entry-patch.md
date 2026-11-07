# Proposed patch — `corpus/knowledge/limine-pin-writers-r88.md` / `.json` (NOT applied)

Seat ScoutSources, round 88 wave w1. Nothing in the lane was edited. This file is the L1's decision
material. Every claim below is grounded in the upstream tags opened this wave
(limine-entry-tool `1.40.0` = `35dab4b732861f5e8d307a1a7873856a877913aa`;
limine-snapper-sync `1.32.1` = `b4c0da2d4532a993809219f9e5d51a1fa85fcb93`) and in the L1's committed host
receipts. Line numbers are upstream raw lines.

## P1 — PW8: scope the claim to *newly created* snapshot entries

Current PW8 wording: "until the main pins are recomputed (PW5), **every snapshot entry** limine-snapper-sync
adds for `linux` or `linux-lts` carries the stale main pin … next to a history copy of the rewritten UKI".

Why it over-claims: existing snapshot entries are **not** re-derived on each sync. They live in
`snapshots.json` and are re-emitted from the manifest:

```
Main.java:299            manager.historyAddSnapshot(manifest, newSnapshotEntry);
SnapshotManager.java:241 manifest.getSnapshotEntries().add(lastSnapshotEntry);
Main.java:313            writer.setSnapshots(manifest);
```

`writer.setSnapshots` → `overwriteSnapshotsNode(manifest.getSnapshotEntries())`
(`processes/LimineWriter.java:153`) rebuilds the Snapshots node from the **stored** entries. The host's
three history entries (lines 50/56/64) still match their files, which is only possible if the pin each was
born with was preserved — they were created 2026-10-20, before the incident.

Proposed replacement for the first clause of PW8:

> "[inf] Consequence on this host: while the main pins are stale (until the repair of PW5), **each snapshot
> entry created after the incident** carries the stale main pin (`b990d8c6…`/`a68c281d…`, PW6) beside a
> history copy of the rewritten UKI (`57f5eb94…`/`eff78d32…`, PW7), so it reads `LP-MISMATCH` (`prompt` under
> `hash_mismatch_panic: no`). Entries created **before** the incident keep the pin they were born with and
> still verify (the host's lines 50/56/64 are that case); the manifest, not a re-read of `limine.conf`, is
> what carries them. The stale pin spreads with each new snapshot; the hourly "Updated" runs (observed 19:27
> and 20:27) leave the main pins as they are. Not executed: no snapshot was created this round."

The unchanged part of PW8 ("Not executed: no snapshot was created this round") stands.

## P2 — PW6: add the copy site and the path-line writer to the anchors, and name the divergence

Current PW6 anchors: `S359 KernelReader.java 154-157, 175-179, 196-213; Limine.java 28`. Those two files
compute the value but neither performs the copy nor writes the line. Add:

* `S360? limine-snapper-sync 1.32.1 processes/SnapshotManager.java 212-243` —
  `Utility.copyFile(sourceFilePath, targetFilePath);` (raw 238): the history file is a plain byte copy of the
  live ESP UKI; the name carries a fresh SHA-256 of those bytes (`KernelReader.java:196-209`,
  `Config.java:46`), the `#` pin is not part of the copy.
* `S361? limine-snapper-sync 1.32.1 formats/json1/ImageDetail.java 47-50` —
  `return Limine.replace(limineKey) + " " + Limine.uri(properties, this.snapshotFilePathLine().trim());`
  (raw 49), with `formats/limine8/Limine.java:83-86` (`uri`) prepending `boot():`: this is where the copied
  `#hex` lands in Limine's hash position.

Wording refinement of PW6's first clause, to name the divergence instead of only the mechanism:

> "[src] limine-snapper-sync builds a snapshot entry from the main entry's `path:` line: it cuts the **first**
> `#hex` run off that line (`KernelReader.java:176-178`, pattern `#[a-fA-F0-9]*`, `Limine.java:28`) and
> appends that same text to the history-file path it writes (`KernelReader.java:210`). It never recomputes the
> BLAKE2b — and cannot: the tool has no BLAKE2b hash function at all (`objects/Hash.java:9-12` offers sha1,
> sha256, blake3, xxhash), and the installed image contains no `b2sum` string
> (`strings -a /usr/lib/limine/limine-snapper-sync | grep -c b2sum` → 0). Note the divergence from Limine's
> own reader (r87 `S351`, `common/lib/uri.c:78-101`), which takes the **last** `#` and requires exactly 128
> hex; on this host every path carries one `#`, so the two agree."

## P3 — PW6/PW7: say what the two hashes on one line are

PW7's "The history file is named after the current file's content hash (`HASH_FUNCTION`, default SHA-256),
computed fresh at sync time" is right, but the *line* carries two hashes and the entry never says so. The
host's line 50:

```
path: boot():/432d02b544a5459ebbff9c42ec68334d/limine_history/omarchy_linux.efi_sha256_2e9c9bdc…#822299bb…
```

* `…_sha256_2e9c9bdc…` — inside the **file name**: a fresh SHA-256 of the copied bytes
  (`SnapshotManager.java:227` names the file `fileHashName` alone, without the `#…`);
* `#822299bb…` — after `#`, in Limine's **URI hash position**: text copied from the main entry's `path:`
  line.

Proposed addition to PW7 (or a new row PW10):

> "[src] One snapshot path line therefore carries two different hashes: a 64-hex SHA-256 inside the history
> file name (fresh, of the bytes just copied) and a 128-hex after `#` (copied text, never recomputed). The
> file on disk is named without the `#…` suffix; Limine reads the `#…` as the expected pin for it."

## P4 — PW2: name the command path

Current PW2: "Pins are written only when `ENABLE_VERIFICATION` is `yes` (case-insensitive) AND the `b2sum`
command exists". The predicate is `Utility.isCommandPresent(Config.HASH_COMMAND)` with
`Config.HASH_COMMAND = "b2sum"` (`Config.java:7`), and the hash itself is produced by shelling out to
`b2sum <path>` (`Utility.java:122-129`, `blake2sum`). On this host that is `/usr/bin/b2sum` (coreutils
9.12-2). Proposed host_value refinement: "`b2sum` is `/usr/bin/b2sum` (coreutils 9.12-2); the check is
`isCommandPresent("b2sum")` (`Config.java:7`)". This matters because the writer's hash is a **command
invocation**, so a host without coreutils' `b2sum` silently drops every pin.

## P5 — Limits: delete the closed bullet, add the enrolled-config condition

Current Limits bullet 2 — *"The body of `limine-mkinitcpio` and `limine-install` was not opened; PW5 rests on
`limine-update` calling them and on LimineManager writing the pin when an entry is (re-)added."* — **can be
deleted**: both bodies were opened this wave and both are byte-identical to upstream 1.40.0
(`limine-mkinitcpio` `e0c8375b…`, `limine-install` `a7563f6b…`, and the ALPM script `limine-mkinitcpio-install`
`22e44591…`; all equal to the installed copies). The measured chain, suitable to replace the bullet:

> "`limine-update` (`limine-update` raw 16-28) runs `limine-install --no-efi-register` and then
> `limine-mkinitcpio "$@"`. `limine-mkinitcpio` (raw 26-33) is only a wrapper: with no argument it pipes
> `rebuild` into `/usr/share/libalpm/scripts/limine-mkinitcpio-install`, which builds a **new** UKI per kernel
> (`/usr/bin/mkinitcpio … --uki`, raw 180) and installs it with `limine-entry-tool --add-uki` (raw 196) —
> the call that writes the pin (`LimineManager.java:353`). `limine-install` writes **no** `path:` pin: it
> b2sums the Limine binary only for backup/restore comparison (raw 415-419, 458-462). All four files are
> byte-identical to upstream 1.40.0."

New Limits bullet (worth adding — it conditions the entry's own repair advice):

> "- The *enrolled-config* checksum is a second, independent `b2sum` surface: `limine-common-functions:368`
> runs `limine enroll-config "$BINARY_TARGET_PATH" "$(b2sum "$LIMINE_CONFIG_PATH" | awk '{print $1}')"`. It is
> inactive on this host (`ENABLE_ENROLL_LIMINE_CONFIG` appears only commented out,
> `/etc/limine-entry-tool.conf:151`), which is what makes the hand-edit alternative in Operator actions
> safe here. With it enabled, a hand edit of `limine.conf` needs a re-enrolment
> (`/etc/boot/hooks/post.d/90-limine-enroll-config`) or the boot is refused. Not executed."

## P6 — SOURCES registry: candidate rows with ids left blank

Eight candidate rows are listed in `ScoutSources.md` §7 with URL, access time, anchor and a ≤25-word quote.
They need S-ids from the L1; the two that most change the entry's evidence base are the
`SnapshotManager.java` copy site and the `formats/json1/ImageDetail.java` path-line writer, because PW6/PW7
currently cite neither.

## Not proposed

* No change to PW1, PW3, PW4, PW5, PW9 — each was re-opened at the tag and holds as written (PW5 as the L1
  rewrote it; the repair-rebuilds chain is confirmed by §4 of `ScoutSources.md`).
* No change to the frozen predicates, targets, kill rules or instrument digests: none of this touches
  `tools/limine-pin-battery-r88.py`, `tools/battery-discrimination-r88.py`, the roster or the controls.
