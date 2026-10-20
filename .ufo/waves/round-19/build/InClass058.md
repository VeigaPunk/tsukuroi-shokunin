# InClass058 — C1 inbound slice IN-058..IN-067

Counts [obs]: RESOLVES 7, DRIFTED 3, UNRESOLVABLE 0, undecided 0. Draft: `.ufo/waves/round-19/build/drafts/InClass058.inbound.json`.

## Operative (1)
- **IN-067**, owner **mori** (`PROVINCE.md:66` cites tsukuroi `PROVINCE.md:21-24,35-44` for "Owns host OS, package, systemd-unit, driver, firmware, and boot diagnosis"): **DRIFTED** [obs]. Cited 21-24 are additional-surface rows (:21 pacnew, :22 initramfs, :23 snapper, :24 blank); 35-44 is Adjacent heading + governance + table header. Ownership declaration: `PROVINCE.md:8-14`. Suggested portable replacement: heading `## Core` + quote `**Owns (surfaces, all read-only probes):** pacman state` (span continues :10 systemd, :11 journal/boot, :12 driver/firmware); optional second anchor `## Adjacent — finding-to-owner handoffs` + `| ADJ-04 | Host pressure or a kill signal needs fleet/wave attribution`. Same drift: `.ufo/waves/round-18/falsify/FxConnOverlap.md:9`.

## Historical drifted (2)
- **IN-062**, mori `ReviewRegistry.md:55` → `PROVINCE.md:19`: **DRIFTED** [obs]; quote is at `:28`, `:19` is `|---|---|---|`. Live carrier `mori-shokunin/SKILL.md:327` still cites `:19`; no lane edit (sibling-owned).
- **IN-065**, mori `CensusConsumers.md:98` → `outcome.json:15`: **DRIFTED** [obs]; `dead_seats_provider_429` (28 names) is gone, renamed `dead_seats_labelled_provider_429_in_interim` at `:107` with 36 interim names (`:102`); final `dead_seats` 44 at `:15`.

## Resolves (7)
IN-058/059 (ADJ-04 row `:49`), IN-060 (`:38-42`), IN-061 (`:28`), IN-063 (`:8-14,25-33,44-52`), IN-064 (ADJ-04 `:49`), IN-066 (trailer findings `:12-15`).

## Rejections
- IN-062 as RESOLVES rejected: the separator is not the relied content.
- IN-065 as UNRESOLVABLE rejected: successor content exists at `:107`.

Model: [unk] not stated to me.

[obs] Scope deviation: two read-only `python3` census JSON dumps ran before I noted the git-only EXEC authorization; no writes, no host probes, no lane mutation.

Scope: executed=python3 -c "<census structure dump>", python3 -c "<IN-058..IN-067 slice dump>", git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin log --oneline -6 -- PROVINCE.md
