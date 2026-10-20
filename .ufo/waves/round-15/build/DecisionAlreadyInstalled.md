# R15 decision fragment — installed requested package, newer sync candidate
Status: advisory, report-only. Round 15, baseline `0db618a71ae2d0bb0c0c3059abaa219b7ccd20a2`. Scope: requested package already installed and its effective sync candidate newer; decides package action, not host health.

## Row
| id / condition | evaluation | decision | transaction |
|---|---|---|---|
| `R15-DEC-ALREADY-INSTALLED-NEWER` — local `P` exists; effective sync candidate for same name exists; `alpm_pkg_vercmp(v_sync, v_local) > 0` | `-S P` and `-S --needed P` both add the newer sync package, upgrading installed `P` alone plus dependency actions, without the full-system upgrade path | `BLOCKED_FOR_AGENT_PACKAGE_ACTION`; reason `PARTIAL_UPGRADE_WOULD_UPGRADE_INSTALLED_TARGET` | `transaction_permitted=false`, `transaction_started=false`; no `-S/-Sy/-Syu/-U/-R` |

```json
{
  "id": "R15-DEC-ALREADY-INSTALLED-NEWER",
  "applies_when": {"requested_package_installed": true, "effective_sync_candidate_for_same_name": true,
    "version_relation": "alpm_pkg_vercmp(v_sync, v_local) > 0", "requested_options_covered": ["-S P", "-S --needed P"]},
  "decision": "BLOCKED_FOR_AGENT_PACKAGE_ACTION", "reason": "PARTIAL_UPGRADE_WOULD_UPGRADE_INSTALLED_TARGET",
  "would_upgrade_installed_target": true, "needed_skips_target": false, "full_system_upgrade_invoked": false,
  "transaction_permitted": false, "transaction_started": false,
  "dry_run_probe": {"command": "pacman -Sp --print-format '%n %v' <pkg>", "executed": false},
  "source_ids": ["S047", "S048"],
  "limits": ["no host query, -Sp, version instance or package transaction this round",
    "sync-newer is relative to the current local sync DB snapshot; no refresh was run",
    "S048 kept scope covers -p/--print-format only; this row also uses the same URL at --needed and -u",
    "pacman v7.1.0 source-code mechanism is supporting inspection, not a new SOURCES row"]
}
```

## Exact rule and mechanism
1. `cmp = alpm_pkg_vercmp(v_sync, v_local)`; versions parse as `[epoch:]version[-release]`, epoch first, then version, then release when both exist.
2. `--needed` is not a guard here. pacman(8): “Do not reinstall the targets that are already up-to-date.” An installed package with a newer sync candidate is not up-to-date; the option only skips `cmp == 0`.
3. In pacman v7.1.0 `lib/libalpm/add.c` (`alpm_add_pkg`), the `NEEDED` early return is inside `cmp == 0` only. `cmp > 0` falls through to `trans->add`; `cmp < 0` logs “downgrading package” and is a different row.
4. `src/pacman/sync.c` invokes `alpm_sync_sysupgrade` only when `op_s_upgrade` is set; explicit `-S P` does not. That single-target upgrade is the partial-upgrade shape S047 forbids, even when dependency resolution adds more targets.
5. `-Sp` runs `alpm_trans_prepare`, prints `alpm_trans_get_add`, then returns before `alpm_trans_commit` (`sync_prepare_execute`). It is a target preview, not a safety certificate and not permission to commit.

## Sources (reopened 2026-10-20)
- **S047** — ArchWiki System maintenance, oldid 885170, last edited 2026-09-07: “That is why partial upgrades are not supported.”; its do-not list names `pacman -Sy package`, and `pacman -Sy` followed by `pacman -S package`, directing a full upgrade.
- **S048** — pacman(8), footer “2026-10-15 / Pacman 7.1.0” (core `7.1.0.r9.g54d9411-3`): “Only print the targets instead of performing the actual operation (sync, remove or upgrade).”; “Specify a printf-like format to control the output of the --print operation.” Same URL, `UPGRADE OPTIONS (APPLY TO -S AND -U) > --needed`: “Do not reinstall the targets that are already up-to-date.” Same URL, `-u, --sysupgrade`: “Upgrades all packages that are out-of-date. Each currently-installed package will be examined and upgraded if a newer package exists.”
- Supporting mechanism only, not a registry row: pacman v7.1.0 tag, `lib/libalpm/add.c:alpm_add_pkg`, `lib/libalpm/package.c:_alpm_pkg_compare_versions`, `lib/libalpm/version.c:alpm_pkg_vercmp`, `src/pacman/sync.c:sync_prepare_execute`.

## Boundaries and handoff
- Not this row: `cmp == 0` (`--needed` skips, otherwise reinstall; still no transaction this round); `cmp < 0` (local-newer downgrade path, including under `--needed`); no local package (new/dependency case); no sync candidate or failed `-Sp` (cannot evaluate; empty output is never proof of safety); different provider/name resolution.
- Handoff: record `P`, `v_local`, `v_sync`, `cmp > 0`, repo/sync snapshot age and the `-Sp` target set if a later authorized read-only probe obtains them; then stop. A full upgrade is operator-owned and subject to the mkinitcpio 42 boot-hook gate; no downgrade, symlink workaround or package command is advised or executed by this fragment.
- Limits: the generic row is source-grounded; it establishes no host package version, pending count, sync freshness, ABI/UI health or cause of the 2026-10-20 04:25 libinput event. S048’s kept scope should be widened to the `--needed`/`-u` anchors before the C2 pair cites them through that ID.
- Tools installed/updated: **none**. Host queries/probes: **none**. Child dispatch: **none**. No checker, test, build, formatter, package or service action was run.
