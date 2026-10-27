VERDICT: supports

Item C2-4 — novelty facts test re-run at 8eee79db608b5815c325a5af7cbfdeac50eda9f4, against
`corpus/knowledge/btrfs-scrub-record-r44.md` as integrated (SR7/SR8 were narrowed after w1 in commit
071ab0d1; w1 seat `C2CritNovelty` judged the pre-narrowing draft). Baselines: r42 SC5
(`btrfs-scrub-record-r42.md:123-141`, narrowing :201-203), r43 SR3 (:52-96) / SR6 (:98-138),
storage-health-r26 SH3 (:41-52) / SH4 (:55-65), SKILL.md (:2361, :2368, :3901-3922, :4005-4023).
Receipts: `.ufo/waves/round-44/w2/C2CritFinalNovelty/receipts.txt`.

## 0. Token-level novelty (counter leg, re-verified at tip)

`git grep -n 'ENOTCONN\|memparse\|KillSignal' 98020ece0674e0b569ee23aed10ffbee355b248e --
corpus/knowledge SKILL.md` exits 1, zero hits — matches the counter's `novelty_base_hits == 0`
receipt (`before/c2-before.jsonl`). At the tip the tokens appear only in
`btrfs-scrub-record-r44.md`. Token novelty holds; the counter's novelty leg cannot fail on
provenance.

## 1. Re-verified fact deltas (tip text)

SR7 (r44:17-28, narrowed): attaches `dev->scrub_ctx` at S242 scrub.c:3159 after the refusal
checks (:3147, :3153 -EINPROGRESS) and clears at :3222 under `scrub_lock` before the
`need_commit` finalize tail — verified directly in the pinned file; no early return exists
between attach and clear, so "every return path leaves the field as it found it" holds on this
read. New over r43 SR6 (which treated all ioctl failures alike, "whatever the errno"):
the 0 / -ENOTCONN / -ENODEV split (S242:3336), the `device_list_mutex` lookup, the
copy-back-only-on-0 ioctl leg (S240:3141), and the device-replace sharing of
`btrfs_scrub_dev` (S242:3081; replace side honestly tagged inference, dev-replace.c lines
701-703/1265-1268 opened this round, not pinned). Decision-relevant: a privileged status's
`running` means a scrub-or-replace source is live now; an idle device answers ENOTCONN, never
0 — grounding SR6 left open.

SR8 (r44:58-66, extended): the held user-facing facts (path, bytes/s, 0 = none — r42 SC5:125-126,
SKILL.md:3918) are joined by new kernel-side facts: mode 0644 via BTRFS_ATTR_RW (S243:72-74,
2048), `%llu\n` read format (S243:2028), memparse write parse with skip_spaces and -EINVAL on
trailing text (S243:2040-2044), WRITE_ONCE/READ_ONCE discipline (S243:2045, S242:1380), the
0-short-circuit throttle (S242:1381), and the new persistence sentence. Decision-relevant: only
root writes the limit (the unprivileged census reports `limited=` but cannot set it), malformed
limits fail closed, and — new — the value is per-boot.

SR9 (r44:92-100): held `OnCalendar=monthly` (SH4:57 + S131) is joined by new facts: Arch
PKGBUILD provenance and install paths (S244 PKGBUILD:100-101 — SH4 said "packaged" without the
install mechanism), `RandomizedDelaySec=1w`, `Persistent=true` (S244 timer:7-8),
`WantedBy=timers.target` → the `timers.target.wants/btrfs-scrub@<i>.timer` link the arm counts
(S244 timer:11; the wants-link mechanism exists in lane knowledge for other units — new for this
unit and exactly what `timers=` measures), `ExecStart=... -B %f` with `KillSignal=SIGINT`
(S244 service:9-10), and the stop→SIGINT→`BTRFS_IOC_SCRUB_CANCEL`→`canceled`→resumable chain
(S237:421, 969, 1546; resumability held in SR3, the cancel-on-stop mechanism new).
Decision-relevant: `systemctl stop` on the unit cancels the running scrub and leaves a
resumable record — a triage fact SH4's "disabled timer" reading did not carry.

Each row adds multiple new decision-relevant facts; none is a restatement.

## 2. SR8 persistence sentence — justified, not ungrounded

Claim (r44:63-66): in-memory only; written with WRITE_ONCE, read with READ_ONCE; nothing on the
write path persists it; unmount loses it; kzalloc initialisation restores 0.

Method: shallow-cloned stable/linux.git tag v7.2.11 into scratch (peeled commit
a2de78ee6ed8bf8cd99d177c74865a6e8c3cb6ea — identical to the doc's verified-at line) and ran
`git grep -n 'scrub_speed_max' v7.2.11 -- 'fs/btrfs/'`. Every hit:

- scrub.c:1369 — comment only; 1380 — READ_ONCE (the throttle)
- sysfs.c:2028 — READ_ONCE (show); 2045 — WRITE_ONCE (store); 2048-2049 — attribute decl;
  2113 — attribute-table entry
- volumes.h:216 — the field declaration

The only write site in all of `fs/btrfs` is the sysfs store. No ioctl, no superblock write,
no dev_item round-trip, no dev-replace copy writes it (dev-replace.c grep clean; the replace
target is a fresh `btrfs_alloc_device`). `struct btrfs_device` is zero-allocated at
volumes.c:7470 (`kzalloc_obj(*dev)`, volumes.c:7460 signature) — confirming the
"`kzalloc_obj` zeroes the device allocation" inference, and `kzalloc_obj` is the typed kzalloc
macro (include/linux/slab.h:1152). The on-disk `btrfs_dev_item` (include/uapi/linux/btrfs_tree.h)
carries devid/total_bytes/bytes_used/io_*/dev_group/seek_speed/bandwidth/uuid/fsid — no speed
field — so persistence through the device tree is structurally impossible. Devices are freed on
unmount via btrfs_free_device (volumes.c:405 ff.), so the value genuinely dies with the mount.

Prior-lane check: `scrub_speed_max` mentions outside r44 (r42 SC5, SKILL.md:3918,4011) carry
existence and reporting only; no prior entry states the write discipline, the ephemerality, or
the zero-initialisation — the sentence is new knowledge, and it is grounded, though the
"[inference]" tag in the doc could now be upgraded since this grep enumerates the whole
write path. Only residual nit: "a single-device filesystem loses it on unmount" understates —
any filesystem loses it on unmount; the qualifier is harmless (the host is single-device).

## 3. Attempted falsifications that failed

- Hidden write path via device replace or device-add: no `scrub_speed_max` hit outside sysfs.
- Hidden persistence via dev item / superblock: no such field in btrfs_dev_item; the claim is
  structurally safe.
- Token-only novelty (facts already held elsewhere): fact-level comparison above shows new
  content in every row; e.g. SR8's write path and ephemerality, SR9's stop-cancels-scrub chain.
- Stale w1 judgment: re-run against the narrowed tip text; the narrowing strengthened precision
  (attach/clear line numbers) without removing any novel fact.

## 4. Proposed text

Optional one-line upgrade in SR8's bracket, since the grep now exists:
`[verified: `git grep scrub_speed_max fs/btrfs` at v7.2.11 (a2de78ee) hits only the sysfs
WRITE_ONCE store, the READ_ONCE readers and the declaration; `kzalloc_obj` zeroes the device
allocation]` — replacing "[inference: no persistence site was found …]". Not required for holds:
the sentence is justified as written.
