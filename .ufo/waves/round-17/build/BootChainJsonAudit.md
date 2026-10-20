# Boot-chain JSON audit — `corpus/knowledge/boot-chain-r17.json` vs `.ufo/waves/round-17/l1-capture/boot-chain-capture.txt`

[obs] Both files read in full (JSON 269 lines, capture 258). No edits, no execution, no installs.
Entry indices: e0 linux, e1 linux-lts, e2 snapshot-2/linux, e3 snapshot-2/linux-lts, e4 snapshot-1/linux, e5 efi-fallback.

## Verdicts re-derived from the JSON's own fields
e0→rule2, e1→rule5, e2/e3→rule3, e4→rule4, e5→rule1. Stored verdicts agree, but four rule defects:

- **R1** `verdict_rules[1].if` (JSON:25) is image-scoped: e2.sha256 (JSON:127) = `2e9c…` = the booted image (171/219), so the rule as written yields BOOTED-OBSERVED, while `entries[2].booted_observed=false` (JSON:140) and verdict DEGRADED-PREDICTED (JSON:141). Needs “and this entry is the booted one (root/rootflags match /proc/cmdline)”.
- **R2** `verdict_rules[2].if` (JSON:30) never requires the entry to select the snapshot: it fires on `snapshot_ro` alone. The e2/e3 cmdlines are truncated (144/148), so the entry→snapshot binding is unverified; `rootflags` is exactly the unobserved field (H1).
- **R3** `verdict_rules[0].if` (JSON:20) needs the fact “efi_path is not a kernel UKI”; 155–156 give only the path and header. e5's verdict is [inf], not evaluable.
- **R4** `verdict_rules[1]` leaves “boot-chain input” undefined (see H2).

## High — values absent from every cited line
- **H1** `entries[0..4].rootflags`: no capture line contains the value. All five cmdline lines (132,136,144,148,154) were printed through `cut -c1-200` (command 126) and stop at `allow-disc`/`allow-d`/`root=/d`. The only `subvol=` strings in the file are 12 and 14 (`subvol=@`); no `subvol=/@/.snapshots/…` exists. e1 has no /proc/cmdline analogue at all. Consequence: e2/e3 “snapshot becomes the root” and e1 “non-snapshot root” rest on an uninspected field.
- **H2** `entries[0].booted_observed`/`verdict`, freshness clause: cited 158 is only the annotation `(rc=0 ; empty = none newer)` for 157 `find boot-chain inputs -newermt "…09:57:09"` — as printed, two relative path operands with no `-maxdepth`, while 255 itself says “line 158 used -maxdepth 1”. The reproducible sweep is 256–257 (0 of 58674) and its path list omits `/boot`; `/boot/limine.conf` is 12:07:06 (106) and `/boot/loader` 09:57:10 (108), both after 09:57:09. Under a broad reading rule 2 fails for e0 → rules 3/4 also fail → UNTESTED, so “5 kernel-entry verdicts” is at most 4.
- **H3** `entries[0].booted_observed` is not observed: no line hashes the running image; identity is inferred from 5/10/12/14/130/171/173/219. The boolean asserts an observation the capture cannot supply (it is [inf]).
- **H4** `entries[5].verdict` antecedent unproven (R3).

## Medium — wrong/conflicting or missing evidence lines
- **M1** `boot.evidence_lines` (JSON:9–15) includes 6 (uptime `09:57:08`) for `boot_start` `09:57:09`, which comes from 10; line 6 conflicts by 1 s.
- **M2** `entries[0].evidence_lines` includes 127 (`default_entry: 2`), which supports no declared field; `/+Omarchy` is a submenu (128–129) and `/EFI fallback` is the second top-level entry (155–156), so “2” does not demonstrably select `//linux` (the `.md`'s operator check 2 concedes this).
- **M3** `entries[0].note` cites 115 and 219; neither is in `entries[0].evidence_lines`.
- **M4** `entries[1].evidence_lines` omits 197–200 while the note's “same init and hook bytes (198–200 = 182–184)” rests on them, and cites no cmdline line because none carries the value.
- **M5** `entries[4].note` “zswap.enabled=0” and “kernel 7.2.3 modules inside the snapshot” have no capture line (154 is cut before the zswap tokens; nothing lists the snapshot's module tree). “init mounts and switches /new_root” is inferred from a ref count (207); the image init sha `9a25…` (214) differs from the installed `62fc…` (251), so 24–30 do not describe the 41.1 init.

## Note-level contradictions
- **N1** `entries[3].note` “boots the same 42.2 image bytes as the current /boot UKI (sha256 equal)” — its sha is `2d49…` (235), the booted/UKI sha `2e9c…` (171/219); it equals `omarchy_linux-lts.efi` (187/125). Copy-paste of e2's note.
- **N2** `entries[0].note` “Only limine entry with kernel 7.2.11” — e2 also has kernel 7.2.11 (142); with the rootflags conjunct, exclusivity is circular (H1).
- **N3** `entries[1].note` “nvidia dkms build” is absent from this capture (only package lines 40/43/52); the `.md` sources it to `fresh:36–37`.
- **N4** `entries[0].note` “mtime … equals the 09:29:18 history copy by sha256” conflates mtime (09:26:22, 124) with sha (115/171/219); only the sha is equal.

## Per-entry conclusion
- **e0**: label/path 129–131, sha/b2sum/uname/version/init/hooks 171–175,178–181, mtime 124 — supported. `rootflags` inferred from 12 only; `booted_observed` [inf] (H3); evidence list carries 6/127/158 defects (M1–M2, H2).
- **e1**: label/path 133–135, sha/uname/version/init/hooks 187–191,194–196 — supported. `rootflags` unsupported (H1); `booted_observed=false` consistent (189 vs 5); note N3, evidence M4.
- **e2**: label/path/comment 139–143, sha/uname/init/hooks 219–223,226–229, snapshot 139/167, ro 161 — supported. `rootflags` unsupported; `booted_observed=false` contradicts the rule-2 definition (R1).
- **e3**: label/path 139/145–147, sha/uname/init/hooks 235–239,242–245, snapshot/ro 167/161 — supported, except `rootflags`; note N1 is false.
- **e4**: label/path 149–153, sha/uname/version/init/hooks 203–207,210–213, snapshot 149/166, ro 160 — supported. `rootflags` unsupported; `booted_observed=false` consistent (203 ≠ 219); note M5.
- **e5**: label/path only (155–156); every inspected field null as expected; verdict antecedent unproven (H4).

Global check: sha256 171/187/203/219/235; b2sum_prefix 172/188/204/220/236 (20 hex, exact); uname 173/189/205/221/237; version 174/190/206/222/238; init refs 175/191/207/223/239; hooks 179–180,195–196,211–212,227–228,243–244. No line number points at unrelated content; defects are omission/semantics.

## Residual risk / verification gaps
- Full per-entry cmdlines (rootflags/rootfstype/rw) were never captured; `limine.conf` was rewritten 12:07:06, after boot 0 started, so the audited menu is post-boot state and only ~188 chars of e0's cmdline (132) compare with 12.
- Whether `/boot` counts as a “boot-chain input” is undefined; soundly derived verdicts are 4 (e1–e4), e0 conditional.
- Not verified: `BOOTX64.EFI` type, the 41.1 init text, snapshot cmdline selection.

Scope: executed=none
