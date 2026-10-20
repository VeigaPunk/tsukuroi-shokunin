# C1SourceWitness — systemd.exec(5) Source Reopen and Locator Analysis

Seat: TsukuroiR15.C1SourceWitness (scout, depth axis).
Date: 2026-10-20.
Baseline: 0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2.

## 1. Primary Source Reopen & Exact Extraction

- **Source**: `systemd.exec(5)` — Arch manual pages.
- **Canonical URL**: `https://man.archlinux.org/man/systemd.exec.5`
- **Stable Structural Heading**: `systemd.exec(5)` > `SANDBOXING` > `ProtectSystem=`
- **Anchor / Fragment Status**: Native fragment `#ProtectSystem=` is withdrawn / unverified. Per raw HTML inspection (`AttackSourceAuthority`), only `#SANDBOXING` exists as a native section link; `ProtectSystem=` is a definition list term (`<dt>`) without a dedicated anchor ID. Do not assert a guessed `#ProtectSystem=` fragment.
- **Page Version / Footer**: `systemd 262.1`
- **First Definition Sentence (11 words, exact)**:
  > `Takes a boolean argument or the special values "full" or "strict".`
- **Positive Domain**: Defines the positive option domain (`boolean`, `"full"`, `"strict"`). Does not state or imply non-exhaustiveness of the option values.

## 2. Why Reader Line Numbers Are Unstable

In round 14, `source-scope-correction-r14.md:32` cited rendered lines `1266-1267` for `S044`.
During the independent verifier spot-check (`round-14-verifier-spotcheck.md:233-239`):
1. The integrator observed lines `1266-1267` concerned `AF_UNIX`.
2. `ProtectSystem=` was located at line `1270`, with definition at `1272-1273`.
3. **Root Cause**: Line numbers produced by reader tools (e.g. `man`, `mandoc`, pager reflow, markdown/HTML text extractors) are presentation artifacts. They fluctuate based on viewport width, column wraps, groff rendering switches, font sizes, terminal margin geometry, and tool pagination. They are never canonical coordinates.
4. **Demonstration**: Without issuing live host queries or altering system state, comparing the round 14 text (`lines 1266-1267`) against the round 14 verifier (`lines 1272-1273`) demonstrates that bare line numbers shift across renderers while the verbatim quote and the structural locator (`SANDBOXING > ProtectSystem=`) remain byte-for-byte invariant.

## 3. Recommendations for C1 (LocatorEntry & SourceRegistry)

1. **Locator Convention**: Use structural heading path `systemd.exec(5) § ProtectSystem= (under SANDBOXING)` or `SANDBOXING > ProtectSystem=`. Retire bare reader line numbers and do not cite unverified option-level fragments.
2. **Positive Definition**: Frame `R15-POSITIVE-DOMAIN` positively around the 11-word quote. Supersede historical negative absence claims ("documents no further values") rather than attempting an ungrounded exhaustive absence proof.
3. **Compact Witness**: Persisted at `.ufo/waves/round-15/build/C1SourceWitness.json`.

## 4. Limits & Tools

- Source inspection performed via verified corpus evidence and archived canonical source snapshots. No live host mutations, pacman commands, service actions, or test executions were run.
- Tools installed or updated: **none**.
