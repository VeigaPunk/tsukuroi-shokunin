VERDICT: supports

Item C2-10 — Novelty as facts, not tokens. Comparison baseline: what the lane already holds
(`corpus/knowledge/btrfs-scrub-record-r42.md` SC5, `btrfs-scrub-record-r43.md` SR3/SR6,
`storage-health-r26.md` SH3/SH4, `SKILL.md` scrub-record sections). For each of SR7/SR8/SR9:
facts listed, each marked new or held with file:line, and a judgment whether the row adds at
least one new decision-relevant fact. Then the frozen tokens ENOTCONN, memparse, KillSignal:
facts or words?

## 0. Token scan (what the lane already holds)

- `grep` `ENOTCONN|memparse|KillSignal|scrub_ctx` over `corpus/knowledge/`: hits **only** in
  `btrfs-scrub-record-r44.md` (lines 23, 46, 60, 71, 92, 110, …). Zero hits in r42, r43, r26,
  SKILL.md or any other knowledge entry.
- `grep` `EINPROGRESS|dev-replace|device_list_mutex|is_scrub_running_in_kernel` over
  `corpus/knowledge/`: `is_scrub_running_in_kernel` hits in r43 SR6 (r43:101,115) and r44;
  the other three terms hit only r44.
- The underlying sources were pinned long ago (e.g. S133 `sysfs.c` from round 26 already contains
  the same `memparse`/`skip_spaces`/`-EINVAL` block at lines 2040-2044; S132 `volumes.c` carries
  `-ENOTCONN`; round-35/36 systemd NEWS discuss `KillSignal=`). So novelty is a claims-level gap,
  not a source-level one — exactly the distinction the item asks to enforce.
- Source confirmation of the token-bearing lines (frozen `src/`, read directly):
  - S242 `scrub.c:3336` = `return dev ? (sctx ? 0 : -ENOTCONN) : -ENODEV;`
  - S243 `sysfs.c:2040-2044` = `limit = memparse(buf, &endptr); … endptr = skip_spaces(endptr);
    if (*endptr != 0) return -EINVAL;`
  - S244 `btrfs-scrub@.service:9` = `KillSignal=SIGINT`
  - and the context lifecycle S242 `scrub.c:3147,3153,3159,3222`, attr mode S243 `sysfs.c:72-74,2048`,
    install S244 `PKGBUILD:100-101`, cancel/canceled/handler `S237 scrub.c:421,969,1546`.

## 1. SR7 — scrub-progress ioctl success direction (r44:17-28)

Facts stated:

| # | Fact | New / held (file:line) |
|---|---|---|
| F1 | A device carries `scrub_ctx` exactly while `btrfs_scrub_dev` runs on it; attached before the scrub, NULL at end | NEW (r44:18-19; S242:3159,3222) |
| F2 | A second scrub attempt on the same device is refused with `-EINPROGRESS` while `scrub_ctx` is set | NEW (r44:18; S242:3147,3153) |
| F3 | `btrfs_scrub_dev` serves both scrub and device replace via its `is_dev_replace` argument (replace side marked inference, not pinned) | NEW (r44:19-21; S242:3081) |
| F4 | The progress lookup runs under `device_list_mutex` | NEW (r44:22; S242:3328) |
| F5 | Returns 0 only when the device exists **and** carries a context (stat copied) | kernel-side condition NEW; the userspace "0 = running" half was held in r43 SR6 (r43:101-102) |
| F6 | `-ENOTCONN` when the device exists without a context (idle) | NEW (r44:23; S242:3336) |
| F7 | `-ENODEV` when no device has that devid | NEW (r44:24; S242:3336) |
| F8 | The ioctl handler copies arguments back to the caller only when the return is 0 | NEW (r44:24-25; S240:3141) |
| F9 | Derived triage: privileged `running` = some device is being scrubbed (or is the replace source) at that moment; an idle device answers `ENOTCONN`, never 0; momentary per-device reading, not a record of past scrubs | NEW as stated (r44:25-28); the "live probe" half was implicit in SR6, but "idle never answers 0" is the new grounding |

Held beside it: SR6's `in_progress` semantics ("answers 1 on the first call that returns 0, and
0 only after every call failed, whatever the errno") and the `CAP_SYS_ADMIN` gate (r43:100-109).
SR6 deliberately did not distinguish errnos; SR7 supplies that distinction.

**Judgment: yes.** F5+F6+F7 are the success-direction facts SR6 left open — 0 = running now,
ENOTCONN = idle, ENODEV = unknown devid — and F9 converts them into the reading a privileged status
gives. That is decision-relevant for the census/status semantics ("running" means now, and idle is
never mistaken for a 0 answer).

## 2. SR8 — scrub_speed_max attribute (r44:57-63)

| # | Fact | New / held (file:line) |
|---|---|---|
| F1 | Path `devinfo/<devid>/scrub_speed_max` under `/sys/fs/btrfs/<fsid>/` | HELD (r42 SC5:125-126; SKILL.md:3918) |
| F2 | Bytes per second | HELD (r42 SC5:126) |
| F3 | 0 means no limit | user-facing conclusion HELD (r42 SC5:126; SKILL.md:3918); the kernel throttle mechanism (reads `bwlimit`, returns at once when 0) is NEW (r44:62-63; S242:1380-1381) |
| F4 | Mode 0644 via `BTRFS_ATTR_RW`: world-readable, only owner (root) can write | NEW (r44:58-59; S243:72-74,2048) |
| F5 | Read prints one decimal number followed by a newline | NEW (r44:59-60; S243:2028) |
| F6 | Write parsed with `memparse`: `K`/`M`/`G` suffixes accepted, trailing whitespace/newline skipped, anything else after the number rejected with `-EINVAL` | NEW (r44:60-62; S243:2040-2044) |
| F7 | Userspace reporting: status/start read and report a set limit, `btrfs scrub limit` shows/sets it, arrived in btrfs-progs 6.6.3, a failed read is reported as 0 | HELD (r42 SC5:126-128, 137-139; SKILL.md:3918) |

**Judgment: yes.** F4 (root-only write; the census reads unprivileged and `limited=` is root's to
set) and F5/F6 (format and write-parse semantics) are new and decision-relevant. SC5 covered only
the read/report side.

## 3. SR9 — packaged scrub timer/service (r44:88-96)

| # | Fact | New / held (file:line) |
|---|---|---|
| F1 | The units come from the Arch package (PKGBUILD), not btrfs-progs upstream; installed into `/usr/lib/systemd/system` | NEW (r44:88-90; S244 PKGBUILD:100-101) — SH4 held "the packaged … timer exists" (r26:57,65) but not the source/install path |
| F2 | `OnCalendar=monthly` | HELD (r26 SH4:57 + S131 quote r26:65; SKILL.md:2368) |
| F3 | `RandomizedDelaySec=1w` | NEW (r44:90; S244 timer:7) |
| F4 | `Persistent=true` | NEW (r44:90; S244 timer:8) |
| F5 | `WantedBy=timers.target`; enabling an instance creates a `timers.target.wants/btrfs-scrub@<instance>.timer` link | the wants-link mechanism is held generically for other units (systemd-user-plane.md:38,40,89-90; timer-drift-plane.md:57,81-83; journal-boot-plane.md:268,283-286); for this unit NEW, and it is exactly what the census `timers=` counts (r44:91,135) |
| F6 | Service `ExecStart=/usr/bin/btrfs scrub start -B %f` | NEW (r44:92; S244 service:10) |
| F7 | `KillSignal=SIGINT` on the service | NEW (r44:92; S244 service:9) |
| F8 | `-B` keeps the start foregrounded and sets `do_print`, so SR3's recording failures print into the service's output | mechanism HELD in SR3 (r43:64-66; S237:1293-1295); its application to the service is NEW |
| F9 | The foreground start installs a SIGINT handler that issues `BTRFS_IOC_SCRUB_CANCEL` | NEW (r44:94; S237:421,1546) |
| F10 | SIGINT (the service's stop signal) cancels the running scrub; a device whose scrub ioctl returns nonzero is recorded with `canceled` set, which `btrfs scrub resume` takes up | resumability of canceled records HELD (SR3, r43:55-56); the stop→cancel chain NEW (r44:94-96; S237:969) |

**Judgment: yes.** F3-F7, F9 and the F10 chain are new; F5 directly drives the census timer count and
F10 changes triage (stopping a scrub service cancels the scrub and leaves a canceled, resumable record).

## 4. The frozen tokens: facts, not words

- **ENOTCONN** stands for the new fact that an existing-but-idle device yields `-ENOTCONN` (never 0),
  distinguishing idle from running (0) and from an unknown devid (ENODEV). r43 SR6 treated all failures
  alike ("whatever the errno"); the distinction is unheld until SR7. New fact.
- **memparse** stands for new write-path facts: `K`/`M`/`G` suffixes accepted, trailing
  whitespace/newline skipped, `-EINVAL` on any other trailing text. Prior knowledge held only the
  read/report side (SC5); nothing about how a limit can be set (or malformed how rejected). New facts.
- **KillSignal** stands for the new stop-path fact: `systemctl stop` sends SIGINT, the `-B`
  foreground handler converts it into `BTRFS_IOC_SCRUB_CANCEL`, and the scrub ends recorded `canceled`
  and resumable. Resumability was held (SR3); the cancellation-on-stop mechanism was not. New fact.

None of the three tokens appears in prior knowledge (section 0), and each refers to facts the prior
entries did not state. They are not re-wordings of held content.

## 5. Conclusion

Each of SR7, SR8, SR9 adds at least one new decision-relevant fact (SR7: F5-F9; SR8: F4-F6; SR9:
F3-F7, F9, F10-chain). No row is a pure restatement. The frozen novelty tokens stand for new facts.

Not done: I did not run `tools/check-scrub-record-r44.py` or the census counters — quote/proposition
verification belongs to the verifier seats and the C2 counter, and this comparison is answered from
the knowledge entries and the frozen sources directly. No files were created outside the report path.
