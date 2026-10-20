Axes: evidence fidelity; current-use coverage; safe scope.

Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/partial-upgrade-recheck-r15.md`.

## Findings

- **MEDIUM — INVALID, R17-FRESH-PARTIAL-02 and -06** (target:176,180). `fresh-capture.txt:8` records only `starting full system upgrade`; `:84` counts 448 upgraded/installed log lines, not transaction completion. “Pending set was consumed” and “full system upgrade ran” / gate no longer describes host exceed those captures. Fix: state start marker and package-action lines observed, completion/current total pending count unknown; retain no clearance. The R18 blanket notice (target:192) does not correct this distinct completion premise.
- **MEDIUM — UNPROVEN breadth, R17-SYMLINK** (target:187). Its “42.x images” generalization is not established by `overlay-emulation.txt:51-66`: named `x-omarchy_linux.efi` is a symlink (:59-61), while a hash-suffixed extracted tree has a directory (:62-63); that tree’s version/role is unknown. Narrow to the named image and capture date; do not generalize.

## Record dispositions

Exactly one freshness-registry record targets this path: **R18-FRESH-SUPPLEMENT-33 — VALID, narrowly**. Target:194 and R18 `host-capture-r18.txt:34` support installed local-db `mkinitcpio-42.2-1`, not current pending status. Historical R15 measurements remain historical. Reason is safe but generic; replace with: “R15:55-56 says 41.1 installed/42.2 pending; R18 capture:34 lists 42.2-1. This supersedes that current package premise only; pending status was not queried.” Clarify “current mkinitcpio pending row” in `now`.

R17-FRESH-PARTIAL-01, -03, -04, -05 are **VALID with bounds**: package DB entries (boot-chain-capture:32,39; fresh-capture:27); :7 is a latest *synchronizing* marker, not refresh completion; :13 is mtime, not refresh; boot/image facts are dated R17 observations (boot-chain-capture:10,20-21,175). The R18 notice’s blanket coverage marks the repeated 41.1/42.2 current-use neighbors (target:55-58,112-118,175-179). No enabled→active-count or config→rollback claim found by literal scan.

Residual unknowns: R17 transaction completion; R18 `pacman -Qu`; current initramfs contents and the hash-tree identity. LSP unavailable (`xd://lsp` unmounted; `xd://lsp/status` has no topics); literal reads/grep only, not semantic proof. No execution.

Scope: executed=none