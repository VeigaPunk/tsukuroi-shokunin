## Round 17 — boot-chain next-boot verdict, freshness, landed revisions

Authority: read-only observation and source-grounded inference. Nothing here authorizes a package, service, initramfs, bootloader or `/boot` action. A registry row describes a tool only after its item has landed and passed its own selftest; until then the row is the round contract, not observed behaviour.

### Operator pre-reboot procedure (read-only)

1. From the landed lane worktree, run `bash tools/boot-chain-audit.sh --live`. It reads `/boot/limine.conf` and each UKI through `sudo -n`, extracts `.initrd`/`.uname` into a `mktemp` directory, and never writes `/boot`. It runs no pacman, mkinitcpio or limine-update.
2. Compare each entry's sha256 with `corpus/knowledge/boot-chain-r17.md` (Decision table). A changed sha256 for `/boot/EFI/Linux/omarchy_linux.efi` voids BOOTED-OBSERVED for `linux`.
3. Read each verdict from the vocabulary below. DEGRADED-PREDICTED and UNTESTED are not verified boots.
4. Confirm `default_entry: 2` still selects `//linux` in the limine menu (unverified in r17; boot-chain-r17.md operator check 2).
5. Rollback policy is an operator decision. The three options are the L0 question `tsukuroi | round-17` in `.ufo/l0-questions.md`.

Verdict vocabulary (`tsukuroi-boot-chain-v1`; first matching rule wins):

- NOT-A-KERNEL-ENTRY: not a UKI (`efi-fallback`).
- BOOTED-OBSERVED: image identical to the booted image and no boot-chain input newer than boot start.
- DEGRADED-PREDICTED: read-only snapshot, 42.x `/sysroot` init, `/new_root` overlay hook.
- CONSISTENT-PRE42: `/new_root` init and both hook roots.
- UNTESTED: otherwise.

Round-17 derivation: `linux` BOOTED-OBSERVED; `linux-lts` UNTESTED; snapshot-2 `linux` and `linux-lts` DEGRADED-PREDICTED; snapshot-1 `linux` CONSISTENT-PRE42. Five kernel entries carry a derived verdict.

### Gate and probe registry (round 17)

| Name | Kind | Entry command | Verdict map | Self-test | Pinned values | Write scope | Owner |
|---|---|---|---|---|---|---|---|
| boot-chain | gate | `python tools/check-boot-chain.py` or `--revision <REV>` (REV = 7–64 hex landed on master; HEAD rejected) | 0 pass; 1 failed (verdict re-derivation, sha256/b2sum, missing evidence line, `BOOTCHAIN-MISSING`); 2 could-not-evaluate (`E-CLI`, `E-REVISION-INVALID`, `E-REVISION-NOT-LANDED`, `E-REVISION-NOT-PUSHED`, read/git/parse) | `python tools/check-boot-chain.py --selftest` (≥20 cases; exit 0 pass, 1 fail) | Schema `tsukuroi-boot-chain-v1`; `corpus/knowledge/boot-chain-r17.{md,json}`; `verdict_rules` re-derived; output `status`, `verdicted_kernel_entries`, `findings[]`, `revision`, `branch`, `branch_tip` | None; reads files or git objects only | tsukuroi |
| freshness-r17 | gate | `python tools/check-freshness-r17.py --revision <REV> [--registry-from <REV>]` (REV = 7–64 hex landed on master; HEAD rejected) | 0 pass; 1 failed (`STALE-UNFLAGGED`, append-only violation, missing `capture_quote`); 2 could-not-evaluate | `python tools/check-freshness-r17.py --selftest` (≥18 cases) | Registry `corpus/knowledge/freshness-recheck-r17.json`, schema `tsukuroi-freshness-recheck-v1`; output `resolved_records` | None; git objects only | tsukuroi |
| revision-binding | probe | `python tools/check-revision-binding.py --tools-revision <REV>` (REV = 7–64 hex landed on master; HEAD rejected) | Counting command: 0 = 5/5 tools bound; 1 = fewer bound; 2 = could-not-evaluate. Not a truth gate | `python tools/check-revision-binding.py --selftest` (hermetic stub tools) | Five tools (see REV correction). Per tool: `HEAD` → exit 2 `E-REVISION-INVALID`; unlanded sha → exit 2 `E-REVISION-NOT-LANDED`; landed tip → exit ≠2 with JSON `revision` = tip | Sandbox clone and `git show` reads only | tsukuroi |
| seat-scope | gate | `python tools/check-seat-scope.py <wave-dir> --revision <REV>` or `--worktree` (REV = 7–64 hex landed on master; HEAD rejected) | 0 pass; 1 failed (`SCOPE-UNDECLARED`, `SCOPE-EXEC-UNAUTHORIZED`, `SCOPE-REPORT-MISSING`); 2 could-not-evaluate | `python tools/check-seat-scope.py --selftest` (≥10 cases) | Last `Scope: executed=` line per seat; `EXEC-AUTHORIZED` token in spec prompt; round-16 demonstration at `f871697a…` → exit 1 with 64 `SCOPE-UNDECLARED` | None | tsukuroi |
| recheck-commands | gate | `python tools/check-recheck-commands.py --paths <knowledge files> --revision <REV>` (REV = 7–64 hex landed on master; HEAD rejected) | 0 pass; 1 failed (`RECHECK-FORBIDDEN-INVOCATION`); 2 could-not-evaluate | `python tools/check-recheck-commands.py --selftest` (≥10 cases) | `recheck:` header parsed; default forbidden binaries `pacman,checkupdates,yay,paru,mkinitcpio,limine-update`; resolving heading `## R17-RECHECK — steer-safe procedure`; baseline red on `initramfs-v42-sysroot-recovery.md` | None | tsukuroi |
| boot-chain-audit.sh | probe | `bash tools/boot-chain-audit.sh --live` (operator; read-only `sudo -n` reads into `mktemp`) or `--selftest` | Per-entry verdict per `verdict_rules`; summary `TSUKUROI_BOOTCHAIN: CONSISTENT\|DEGRADED\|UNKNOWN`, exit 0/1/2. Summary rule [unk] until the script lands | `bash -n tools/boot-chain-audit.sh`; `bash tools/boot-chain-audit.sh --selftest` (≥12 cases; no sudo, no `/boot`) | Same verdict function for live and selftest paths | None; never writes `/boot`; trap removes `mktemp` | tsukuroi |

### Corrected REV text (five revision tools)

Replace the REV text in the five revision tools' help and registry rows with:

`REV = 7–64 hex landed on master; HEAD rejected.`

The five tools are `check-locator-clarification.py`, `check-root-dac-correction.py`, `check-section-citations.py`, `check-source-scope-correction.py` and `measure-update-recheck.py`. Rows at SKILL.md:1818 and 1819 currently read "REV = `HEAD` or 4–64 hex"; the section-citations row (SKILL.md:1857) gives `--revision <commit>` with no REV spec.

This text is true only after the RevBind* items land and their selftests pass. Until then, the tools still accept `HEAD` and 4-hex (regex `^(?:HEAD|[0-9a-fA-F]{4,64})$`). Ancestry rule: `git merge-base --is-ancestor <sha> refs/heads/master`; when `refs/remotes/origin/master` exists, also require ancestry to it.
