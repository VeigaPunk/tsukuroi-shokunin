## Attack
Audited the three committed round-19 host captures and their three capture scripts for retained sudo `COMMAND=` history, credential-like material, non-loopback IPs, and mutating probe commands. This targets the capture-hygiene criterion for C2’s evidence inputs; a read-only capture can still expose historical operator records.

## Method
Inspected the files at revision `8e5916360f2dfe7bc4eb4ba144081af555900116`, read all three scripts and all three host captures, and compared the committed capture blobs with the checked-out files. Read-only checks run:

- `wc -l .ufo/waves/round-19/l1-capture/{capture-r19.sh,capture-r19b.sh,capture-r19c.sh,host-capture-r19.txt,host-capture-r19b.txt,host-capture-r19c.txt}`
- `grep -c "COMMAND="` over the three captures and three scripts.
- `sha256sum` over the three capture files and three scripts; Python `-c` scans for redaction markers, credential-shaped terms, IP literals, and host identifiers.
- `git rev-parse`, `git ls-tree -r --long`, `git cat-file -p <blob> | sha256sum`, `git show <revision>:<capture> | sha256sum`, and read-only `git log`/`git ls-files` checks.
- `grep -n -E "^[[:space:]]*run |systemctl|journalctl|sudo|pacman|mkinitcpio|limine-update|limine-snapper-sync"` over the three scripts.

No gate, installation, or host action was run.

## Verdict
**REFUTE — C2-associated capture-hygiene criterion.** Capture A’s redaction checks out, and the inspected probes are read-only; however, capture C retains 12 unredacted historical sudo `COMMAND=` records, contrary to the attack criterion. This is an operator-history exposure, not evidence that the capture script itself executed those commands.

## Evidence
- Target revision contains the audited capture blobs (A `436d1b22…`, B `0d49c6b9…`, C `b44c2f7f…`); their SHA-256 values match the checked-out captures. **A:** 613 lines, SHA-256 `d060de16892fbcb3ca85f45e28a94c9b6ef818c20029d91e05fa9459bbbde32b`; zero `COMMAND=` and 20 in-place redaction markers at lines `527-535, 538-539, 542, 544, 549-552, 554-555, 557`. This is consistent with the stated 20-record replacement and current 613-line count (`8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/l1-capture/host-capture-r19.txt:527-557`; `corpus/lessons/round-19.md:58`).
- **C:** 70 lines, SHA-256 `669cada8c08e00cae06b1429f81f254a744f3a7a1d6fe684592fbe202dea298d`; actual records at `26-36,43` contain `sudo[...]`, `USER=root`, and `COMMAND=`. The two other literal `COMMAND=` matches, at `22,38`, are probe-command text, not sudo records. The retained records include snapper configuration/snapshot commands and a `systemctl enable --now` record (`8e5916360f2dfe7bc4eb4ba144081af555900116:.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:22-43`). The capture script only reads journal data and filters it (`capture-r19c.sh:11-21`).
- **B:** 1,704 lines, SHA-256 `c4cc08fe1b92d65baeb40fc4c82fd8dc1d622a32602f14be0b50b924c0a066d6`; zero `COMMAND=`. The sole credential-keyword hit is generic README prose about graphical password prompts, not a credential (`host-capture-r19b.txt:70`). The four repeated UUIDs at `300,306,325,331` occur in the captured README’s example configuration, not a demonstrated host value.
- No credential/token/Bearer/private-key values or IPv4/IPv6 addresses were found in the three captures. The marker at A’s lines `527-557` still reveals timestamps and labels the removed entries as operator reads of `/boot/limine.conf`; it does not retain the raw command or user name.
- Remaining host-identifying metadata (not credentials): A has the operator home path at line `409`, a root PARTUUID at `421`, host name `plazir27` at `443-522, 541, 543, 546-548, 553, 556, 558-560`, and boot IDs at `525-526, 536-537, 540, 545`. B has host name `plazir27` at `1635-1638, 1641, 1644-1645, 1647-1655, 1657-1665, 1667-1681, 1683`, boot IDs at `6-11, 1646, 1656, 1666, 1682`, and machine-ID-derived boot-history paths at `1635-1637, 1676-1677, 1679-1681`. C has host name `plazir27` at `23-36, 39-43, 46-57, 65-68`, operator name `vgpnk` in the sudo records at `26-36,43`, boot-history paths at `23-24,39-41`, and boot IDs at `60-64,69`. Hashes for these files are given above.
- The scripts’ `run` commands are observational: A uses `date`, `uname`, `ls`, `grep`, `systemctl cat/list/show`, `file`, `stat`, `journalctl`, `wc`, and `tail` (`capture-r19.sh:8-34`); B uses `date`, `journalctl`, `cat`, and `grep` (`capture-r19b.sh:6-22`); C uses `date`, `journalctl`, and output filters (`capture-r19c.sh:9-21`). No capture probe invokes a state-changing systemctl verb, sudo, pacman, mkinitcpio, limine-update, or limine-snapper-sync. The `enable --now` text in C is captured historical journal data, not a probe invocation.

## Residual
The tracked revision has no pre-redaction A blob to independently compare against the 613-line post-redaction file; the original bytes are described as existing only in the L1 harness record (`corpus/lessons/round-19.md:58`). Host names, boot IDs, disk identifiers, timestamps, and the 12 C command records remain in the committed evidence as noted above; they are not credential values.

Scope: executed=wc -l on the three scripts and three captures; sha256sum on capture files/scripts; grep -c 'COMMAND=' over captures/scripts; git rev-parse, git ls-tree, git cat-file, git show, git log, git ls-files; grep -n -E over the three scripts; read-only Python -c line/secret/IP scan; no host actions.