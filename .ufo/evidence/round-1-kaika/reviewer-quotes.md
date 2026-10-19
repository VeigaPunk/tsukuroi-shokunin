# reviewer-quotes — round 1 (kaika), seat W2RoundTsukuroi-8.TsuR1Reviewer-3

(Verbatim L2 output persisted by the L1 so the pointer resolves at closure; L2 = author-side advisory seat, not a non-author verifier. Source transcript: history://W2RoundTsukuroi-8.TsuR1Reviewer-3 — session-scoped, this file is the durable copy.)

Verdict: all 22 items CONFIRMED, 0 WRONG, 0 UNREACHABLE. No peers messaged, since the trigger never fired. Nothing written in the repo; scratch fetches are in `/tmp/tsu-bMoZ`.

Caveat: I fetched the current revisions (raw tags/HEAD, wiki `?action=raw` without oldid). The quote text matches, but ART's oldid anchors (S010 885170, S011 869214, S014 886405, S023 870168, S026 882746) are not re-verified.

| Src | Item | Verdict | Evidence (fetched, then grep/sed) |
|---|---|---|---|
| S015 | "Busybox-based init now uses /sysroot as the root mountpoint…" | CONFIRMED | v42 release notes, line 6–7 (`just like the systemd-based one.`); released_at 2026-09-02 |
| S016 | v42 init 0 `/new_root`; v41.x 7 | CONFIRMED | `grep -c /new_root` = 0 (v42); = 7 (v41.1 and v40); mount `:66-67`, switch_root `:110` |
| S021 | line 4 `root_mnt="/new_root"`; line 7 `|| return 0` | CONFIRMED | lines 4 and 7 exact |
| S022 | `--new-root-dir=/new_root` | CONFIRMED | line 11 (`run_latehook`) |
| S020 | `CapabilityBoundingSet=CAP_SYS_ADMIN` | CONFIRMED | line 13 |
| S027 | CAP_DAC_OVERRIDE "Bypass file read, write, and execute permission checks." | CONFIRMED | lines 58–59 (wrapped) |
| S028 | "Capabilities listed will be included in the bounding set, all others are removed." | CONFIRMED | lines 876–879 (CapabilityBoundingSet=, wrapped) |
| S010 | "never run pacman -Sy; instead, always use pacman -Syu." | CONFIRMED | line 92, §Avoid certain pacman commands (heading 90); wiki bold markup stripped |
| S010 | read-before-upgrading sentence | CONFIRMED | line 82, §Read before upgrading the system (heading 80) |
| S010 | "provides a safe way to check for upgrades…" | CONFIRMED | line 109, §Partial upgrades are unsupported (heading 98) |
| S011 | log-does-not-track quote | CONFIRMED | line 70, §Locating .pac* files (heading 64) |
| S011 | "These files require manual intervention…" | CONFIRMED | line 24, §Why these files are created (heading 14) |
| S007 | HookDir "later directories taking precedence" | CONFIRMED | lines 66–68 (wrapped) |
| S008 | OVERRIDING HOOKS same-name / `/dev/null` | CONFIRMED | lines 87–89, §OVERRIDING HOOKS |
| S009 | `if (( SYNC ))`; `--disable-sandbox-filesystem`; exit 2 | CONFIRMED | line 147; line 150 `fakeroot -- pacman -Sy --disable-sandbox-filesystem --dbpath "$CHECKUPDATES_DB"`; line 181 `exit 2` in the no-updates branch |
| S019 | "≥4 GiB" ESP | CONFIRMED | line 137 "at least **4 GiB** is recommended" |
| S019 | ">3 times … read-only" | CONFIRMED | line 72 "If mismatches occur more than 3 times, Btrfs root and home are set to read-only…" |
| S025 | rd.-prefix sentence | CONFIRMED | lines 26–29 (§KERNEL COMMAND LINE, systemd.mask=); repeated lines 63–65 under systemd.break= (entry line 57) |
| S014 (bonus) | "init pauses the boot process…" | CONFIRMED | line 310 |
| S023 (bonus) | "@.snapshots … create-config will fail" | CONFIRMED | line 36 (wiki markup stripped) |
| S026 (bonus) | "rescue launches a shell shortly after…" | CONFIRMED | line 177 |

Commands: `curl -sSfL -o <file> <url>` for each source, then `grep -n` / `sed -n` on the scratch copies. The v41.1 and v40 init fetches used the `gitlab…/-/raw/v41.1/init` and `…/v40/init` URLs.

Peers messaged: none (no WRONG/UNREACHABLE).
Open issue: S012 (JSON endpoint syntax) and the K3/K4 S010 quotes were not in the list, so they are unchecked.
