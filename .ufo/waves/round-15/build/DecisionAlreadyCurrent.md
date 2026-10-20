# DecisionAlreadyCurrent — round-15 concrete decision row

Seat TsukuroiR15.DecisionAlreadyCurrent (executor, depth only). Baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`.
Report-only: no docs/LOG/SCORECARD/SOURCES edit, no host probe by this seat, no transaction, no child dispatch.

## Row (ready for L1's LOG/decision table)

| ID | Observed condition | Documented outcome | What "no upgrade evidence" means here | Decision this round |
|---|---|---|---|---|
| `R15-DEC-ALREADY-CURRENT` | Snapshot `2026-10-20T07:44:39Z`: `libinput 1.32.0-1`, `libinput-tools 1.32.0-1`; `pacman -Qu` exit0, 413 rows, neither name present; sync dbs born `2026-10-18 14:11:00 -0300`, no later sync line | `--needed`: “Do not reinstall the targets that are already up-to-date.” With installed == effective sync candidate, a repeat `pacman -S --needed libinput libinput-tools` drops both targets: no ALPM upgrade line, and no target printed by `--print` (print consequence [inference]; not executed) | Definitional for a *repeat* only. The 04:25 log **does** record an upgrade: `[ALPM] upgraded libinput (1.31.3-1 -> 1.32.0-1)`. A future empty action proves neither the 04:25 transaction safe/complete, nor the other 413 pending updates benign, nor sync freshness, nor host health | `BLOCKED_FOR_AGENT_PACKAGE_ACTION` — no package/service action, repair, dry run or upgrade clearance this round |

## Evidence and reasoning

1. **The trigger command did upgrade despite `--needed`.** Snapshot `libinput_log` (command `grep -nE 'libinput|synchronizing package lists' /var/log/pacman.log`, exit0):
   - `2429:[2026-10-20T04:25:16-0300] [PACMAN] Running 'pacman -S --needed --noconfirm libinput libinput-tools'`
   - `2432:[2026-10-20T04:25:17-0300] [ALPM] upgraded libinput (1.31.3-1 -> 1.32.0-1)`
   - `2436:[2026-10-20T04:25:17-0300] [ALPM] installed libinput-tools (1.32.0-1)`
   This is direct evidence that `--needed` skips only a target already up-to-date; it did not suppress the 1.31.3→1.32.0 upgrade and it did not prevent a new package (`libinput-tools`) from entering the transaction.
2. **Why a repeat is now a documented no-op for these two names.** `package_versions` exit0 gives both at `1.32.0-1`. The 04:25 upgrade drew 1.32.0-1 from the sync dbs whose birth is 2026-10-18 14:11:00; log line 2288 is the last `synchronizing package lists` at `2026-10-18T14:11:00-0300`, with none later. `pacman -Qu` at 07:44:39Z lists 413 newer candidates and omits both names. So installed is not behind the effective sync entry; equality of the 1.32.0-1 pair is the supported reading [observed + inference; `pacman -Si` was not captured].
3. **The absence is not upgrade evidence.** "No upgrade evidence" is true only of the hypothetical repeat's target list. It is false if read as "the host shows no evidence that libinput was upgraded": line 2432 is such evidence. It also says nothing about whether the 04:25 transaction was a partial upgrade, whether dependency closure held, or whether the 413 other pending updates are safe.
4. **`--needed` is version-relative, not a no-upgrade guard.** If sync metadata is refreshed and libinput gains a newer candidate (including a pkgrel or epoch bump), the same command upgrades it again. ArchWiki: “That is why partial upgrades are **not supported**.” and “When refreshing the package database, **always** do a full upgrade with `pacman -Syu`.”

## Exact sources

- **S048** `https://man.archlinux.org/man/pacman.8` (S047/S048 rows owned by SourceRegistry; not edited here). Footer `| 2026-10-15 | Pacman 7.1.0 |`. Quotes, all ≤25 words:
  - UPGRADE OPTIONS (APPLY TO -S AND -U) > `--needed`: “Do not reinstall the targets that are already up-to-date.” (9 words)
  - TRANSACTION OPTIONS > `-p, --print`: “Only print the targets instead of performing the actual operation (sync, remove or upgrade).” (14 words)
  - OPERATIONS > `-S`: “When upgrading, pacman performs version comparison to determine which packages need upgrading.” (12 words)
- **S047** `https://wiki.archlinux.org/title/System_maintenance`, §Partial upgrades are unsupported: “That is why partial upgrades are **not supported**.” (8 words) and “When refreshing the package database, **always** do a full upgrade with `pacman -Syu`.” (13 words).
- **Snapshot** `.ufo/waves/round-15/build/host-snapshot.json`, `captured_at` `2026-10-20T07:44:39Z`; probes `package_versions`, `pending_updates`, `sync_metadata`, `libinput_log` as quoted. Values are HostSnapshot's capture, not this seat's probe.

## Recommendations for L1

1. Keep the row as an epistemic boundary, not a health or safety verdict. Do not let the future no-op support “the 04:25 partial upgrade was harmless”.
2. Keep the 04:25 upgrade line and the repeat no-op in the same row so “no upgrade evidence” cannot be quoted without its counter-evidence.
3. If a later authorized round wants a dry run, `pacman -Sp --needed --print-format '%n %v' libinput libinput-tools` would test target selection only against the then-current dbs; this round never runs it, and empty output is still not clearance.
4. If sync metadata is refreshed and libinput reappears in `pacman -Qu`, re-enter the partial-upgrade/boot-chain gate; never treat `--needed` as protection.
5. No new source, claim count or axis uplift is created here; depth stays ordinal 8, freshness stays 9, all other axes unchanged and unharmed.

## Limits and tools

- Leaf advisory only; no live host command, `pacman -Si`, `--print`, transaction, service action, sudo, snapper call or daemon activation. Snapshot is one capture at `2026-10-20T07:44:39Z`; `-Qu` is relative to the 2026-10-18 sync dbs and effective repo order, not upstream truth. Exact equality (rather than installed-ahead) is inferred, not directly observed. No causality, dependency-closure or health conclusion is made. No test, build, lint, formatter or verification run; L1 verifies after integration.
- **Tools installed/updated: none.** Used pre-existing `read`, `grep`, `python3` on local files; read the two public documentation pages as source research. No package transaction, install, service change or credential access.
