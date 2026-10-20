# ReviewIncidentBoundary — round-15 C2 STOP/operator handoff (read-only)

Seat: TsukuroiR15.ReviewIncidentBoundary · baseline 0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2 · 2026-10-20
Tools: read, grep, glob (repo-local only). No bash, no host probe, no pacman.log read, no tests. Installed/updated: none.

## Verdict

No handoff text authorizes a package or service change by tsukuroi, and the boundary rule still holds (SKILL.md:156-157; PROVINCE.md:27-28). Three handoff-shaped routes nonetheless make a full upgrade look reachable, and the always-on tooling directive names the exact command class that produced the incident. C2 must say so explicitly. Note: `partial-upgrade-recheck-r15.*`, `host-snapshot.json` and `source-locator-clarification-r15.*` do not exist on disk yet (round-15/build holds spec/task-result/validation only), so this reviews the contract and existing text, not C2 output.

## Findings (severity order)

**F1 (high) — operator option routes a full upgrade through the gate.** `.ufo/l0-questions.md:54` (hyaku-orchestrator, 2026-10-20) lists "run the full -Syu through tsukuroi's /sysroot update-safety gate" as an option. The gate never runs `-Syu` (SKILL.md:137-140, 156-157) and no arm can clear it: post-refresh composes to UNKNOWN-UPSTREAM + REQUIRES-PREP (update-safety-v2.md:239-240, :364-366). "/sysroot" is the mkinitcpio v42 mount point, not a gate name. Fix: IncidentEntry states "gate = detection only; `-Syu` operator-owned; no arm clears it" and does not repeat the option as a route.

**F2 (high) — always-on directive authorizes the incident's command class.** The generic-rules tooling directive lists `sudo pacman -S --needed --noconfirm <pkg>` as channel 1 and says agents install/update "without asking first." The l0 entry records that exact command (pacman.log:2429, 04:25:16). The round's stricter host instruction (spec.json:3: "ANY package changes ... prohibits") governs this lane, but the directive is not scoped out for tsukuroi. Fix: handoff text states the directive does not override PROVINCE.md:27-28, SKILL.md:156-157, or the round ban, and never cites it as authority.

**F3 (high) — boot-chain blocker is stated as fact; the lane measured risk.** Directive wording: mkinitcpio 42 "moves root to /sysroot; hooks still expect /new_root." Lane evidence (initramfs-v42-sysroot-recovery.md): v42 `init` has 0 `/new_root` (:13, obs); `btrfs-overlayfs:4` and `plymouth:11` hardcode `/new_root` (:12, obs); btrfs-overlayfs predicted silent no-op [inf] (:14); plymouth behaviour [unk] (:14); "not a claim that the current 41.1 image has failed" (:14); falsifier is an operator test boot, none run (:32). Fix: record "unverified boot-chain risk, operator discriminator required"; keep it as a blocking condition for any `-Syu` that includes mkinitcpio ≥42, not as a proven boot failure.

**F4 (medium) — update-safety gate omits the boot-chain item.** SKILL.md checklist items 1–11 (:94-140) and update-safety-v2/v3 and note contain no mkinitcpio-version or `/new_root` hook check; the only initramfs item is item 7 (BLOCKED read-only, :122-124). Wave prep (a)–(d) = rollback, dkms, schedule, trust (update-safety-v3.md:225-227) omits hook compatibility. SKILL.md:1658 names the candidate in a table only. Aggravating: `90-mkinitcpio-install.hook` fires on the `mkinitcpio` package trigger and rebuilds the limine image in the same transaction (update-safety-note.md:224-228), so the chain is not deferrable to a later check. Fix: add a checklist item (installed/candidate mkinitcpio version via `-Q`/`-Sup` plan; `grep -n '/new_root' /usr/lib/initcpio/hooks/*`) as a gate condition.

**F5 (medium) — stale "INERT" readings.** update-safety-v2.md:239, update-safety-note.md:39-40 and update-safety-v3.md:216 say `-Syu` is INERT (0 candidates), measured 2026-10-14 against 2026-10-11 dbs. The lane's own erratum records a later bare `pacman -Sy` at pacman.log:2287 (2026-10-18 14:11; update-safety-v2.md:356-361), which the operator now reports as 413 pending. round-1-verifier-spotcheck.md:17 already flagged that partial state and routed a full upgrade to the gate, the same pattern F1 repeats. Fix: IncidentEntry marks the INERT readings superseded and takes counts only from HostSnapshot.

**F6 (medium) — the dry-run guard cannot clear anything against a stale db.** Guard per spec: `pacman -Sp --print-format '%n %v'` on uninstalled candidates only. `-Sp` resolves against the same stale sync db (413 behind per l0:54), so a clean plan proves consistency with that db only. Dependency rows must also be checked (`%n` prints deps). Fix: guard result = INCONCLUSIVE when sync db is stale; never a clearance.

**F7 (medium) — cross-lane mutation and reverts.** The seat was a mado lane seat (l0:54 "during mado r15"). PROVINCE.md:8-9 gives tsukuroi package-state ownership, and unresolved ownership goes to the integrator (PROVINCE.md:41-42). The l0 entry offers revert-by-cache (a downgrade via `pacman -U` class) and removing libinput-tools. Spec forbids -U/-R. Fix: report as operator/integrator decision; tsukuroi endorses no revert, downgrade or removal.

**F8 (low) — seat claims are unverified.** l0:54 states "soname libinput.so.10 unchanged, ldd -r 0 unresolved, running Hyprland keeps 1.31.3." These are the seat's checks, not lane evidence. Soname equality is weaker than ABI equivalence. The running-vs-disk version split is itself a state to record. Fix: cite as seat claims; HostSnapshot re-measures `pacman -Q libinput` and the running mapping.

**F9 (low) — source-registry collision.** S010 is already ArchWiki System_maintenance (SOURCES.md:16). If S047 reuses that URL, census emits W04 (cf. r14 census output in the round-14 closure). Recommend an explicit scope or oldid, with a W04 disclosure.

## Recommendations

1. Decision line: `BLOCKED_FOR_AGENT_PACKAGE_ACTION` plus "no agent action clears this; operator decides libinput 1.32.0 keep/revert and defers full upgrade pending boot-chain gate."
2. List three non-authorizations explicitly: l0:54 option 3; directive channel 1 and "through the gate"; update-safety-v3.md:217 row 2 ("plain -Syu after refresh").
3. Add mkinitcpio/hook check (F4) as a gate condition, with the falsifier from initramfs-v42 :32.
4. Mark 2026-10-14 INERT readings superseded (F5); take counts only from HostSnapshot.
5. Guard INCONCLUSIVE on stale db (F6); no revert/downgrade/removal command in any handoff text (F7).
6. Keep the boot risk labelled [inf]/[unk] (F3); do not upgrade it to "boot blocker" in the report.

## Limits

- Not verified: any live host state; pacman.log:2287 and :2429 are cited from lane docs and l0, not re-opened (HostSnapshot-only probes).
- C2 artifacts absent on disk at review time; findings are against spec and existing text.
- Did not open S046–S048; no SOURCES rows touched. No tests run; none claimed passed.
- F1–F3 rank by consequence, not by probability of a live event; no evidence a full upgrade is queued.

## C2 output review (static, 2026-10-20)

Target: `corpus/knowledge/partial-upgrade-recheck-r15.md`/`.json`, snapshot `host-snapshot.json` sha256 `b101f374…ea81`. No probes or tests; read/grep only.

Verified against snapshot raw bytes: pending stdout contains `mkinitcpio 41.1-1 -> 42.2-1`, `limine 12.8.0-1 -> 12.9.3-1`, `linux 7.2.3.arch1-3 -> 7.2.11.arch1-1`; log lines 2288, 2429, 2432, 2436 exact; five sync DBs share birth `14:11:00.026 -0300`; hook probe shows `/new_root` only, no `/sysroot`. Not located in my reads (grep snippets ambiguous): the plymouth and non-lib32 systemd pending rows. S047/S048 quotes not opened by me.

Boundary language is otherwise consistent: log transaction, installed DB version and running mapping kept separate; `%z` ctime; 413 bounded to the stale DB; mkinitcpio 42 stated as untested risk; no `-S`, downgrade or repair advice.

Overstated or imprecise sentences (flagged, not edited):
- O1 md:28-29 and JSON:31 "both used metadata about 38.2 hours older than themselves": 38.2 h is the logged transaction (07:25:16Z); this capture (07:44:39Z) is ~38.6 h. "used" is [inference].
- O2 md:31-32 and JSON:23 "no libinput* row appears because installed 1.32.0-1 equals the stale database entry": the stale entry is never probed; label [inference].
- O3 md:44-45 "both named hooks still resolve /new_root only": the probe is literal string matching; say "contain only /new_root references".
- O4 md:103-104 "A restart/reboot is required to apply upgraded libraries": the quoted doctrine says restart processes; reboot applies to kernel/initramfs only.
- O5 md:105-107 "the wiki treats downgrading as a last resort ... rejects symlinking libraries": no located quote in the doctrine block; add one or delete.
- O6 md:33-34 "historical pending413 context": source row not located in my reads; cite or drop.

Tools: read, grep, edit. Installs/updates: none.

Re-read after fixes (2026-10-20): O1, O2, O3, O4, O6 confirmed in md and JSON. O5 quotes present at md:102 and md:104. Open: handoff md:124-125 still paraphrases beyond the quotes ("after pacman output, news and forum checks"; "symlinking libraries"). Quote at md:104 says "the problem", not libraries. Narrow the paraphrase or cite a located source. Doctrine quotes at md:102-104 do not name S047 or S048 individually.

O5 closed (re-read 2026-10-20): handoff md:124-126 follows the quoted text only; doctrine quotes md:84-104 carry S047/S048/S049 tags; header keys in lines 1-3. Note: S048/S049 share the pacman(8) URL and S047 shares the System_maintenance oldid with S010; expect W04 duplicate-URL disclosure in the census.

## Final C2 pair — bounded static review (result, replaces pre-artifact risk)

Scope: final `corpus/knowledge/partial-upgrade-recheck-r15.md` and `.json` only. No tests, probes, or source re-opening.

Result: **no unsafe permission, source, or health overreach found** in the reviewed text.
- Permissions: no sudo, install, refresh, service, downgrade or repair command is advised. Decision stays `BLOCKED_FOR_AGENT_PACKAGE_ACTION`; handoff is operator-only (md:109-127; JSON:58).
- Timestamp: `libinput_log` 2026-10-20T07:25:17Z matches line 2432 at 04:25:17-0300 (verified against snapshot stdout in the earlier pass). Line 2436 shares that second.
- Health: boot risk stays `[inference]`/untested (md:55-58; JSON:47); running mapped version and ABI are not measured (md:64-67).
- Sources: S047/S048/S049 tags present on every quote (md:85-105). Quote text was not re-opened here; only the tags were checked.
- Freshness: 413 is bounded to the 2026-10-18 local sync DB (md:31-48; JSON:23).

Remaining low-severity wording (not blocking):
- L1 md:121: "The documented path is a single full upgrade at a controlled time" reads as endorsement. Qualify it as the source's general doctrine, conditional on the operator gate in md:112-118.
- L2 JSON:39: the `meaning` string is truncated in display ("names no acto…"); confirm the closing sentence is complete.
- L3 The gate at md:112-118 does not name the stale-DB guard result (`pacman -Sp` against stale metadata = INCONCLUSIVE). Optional addition.

Pre-artifact risks F1–F9 status: F1 (gate-as-route) mitigated, md:124-127 and md:119-121; F2 (directive) not addressed in the pair, but the pair does not cite it; F3 mitigated; F4 partly mitigated (gate names mkinitcpio/hooks, no checklist item); F5 mitigated (md:43-48); F6 partly (L3); F7 mitigated (no revert advice); F8 mitigated (seat claims not reused); F9 disclosed (md:161-164).
