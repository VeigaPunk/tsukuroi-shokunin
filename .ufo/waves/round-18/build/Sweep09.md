# Sweep09 — pacnew-plane.md C3 reconnaissance

Axes: freshness (candidate notice); depth/operability unchanged.

[obs] One still-live stale imperative at `corpus/knowledge/pacnew-plane.md:19`: “Do not assume the `pacdiff` command is locally available; if available on an operator system, it is the ArchWiki-recommended interface for reviewing these files.” The dated `pacman -Q pacman-contrib` → not-found result (2026-10-19) was true then; only its current-use imperative is superseded. `pacman-contrib` 1.13.1-1 is installed (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:36`), installed by the 2026-10-20T07:45:36 transaction naming it (`.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:55`); `usr/bin/pacdiff` is in the installed package file list and exists executable.

[obs] No fresh evidence for the `:9-15` census: the R18 capture has no `/etc` `.pacnew` sweep and no `.pacnew`/`.pacsave` log query; R17 `fresh-capture.txt:81-83` swept log lines 2462-3063 only (rc=1). [unk] whether the 13:23 `-U` transactions (log 3064-3169) changed the three-path set. No dated fact is called false; no census change is claimed.

Proposed append (id `R18-FRESH-Sweep09-01`; path `corpus/knowledge/pacnew-plane.md`; baseline_quote ``Do not assume the `pacdiff` command is locally available``):

```markdown
## R18-FRESHNESS — pacnew-plane: pacdiff now locally available (2026-10-20)

Appended 2026-10-20; earlier bytes unchanged; supersedes current-use only; historical snapshots preserved; read-only scope, no package or reboot clearance.

- Old at `:19` (2026-10-19): “Do not assume the `pacdiff` command is locally available”. Its dated not-found query was true then and is preserved. Superseded now: `pacman-contrib` 1.13.1-1 is installed (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:36`), so `usr/bin/pacdiff` is present. now: 2026-10-20T16:06:17-03:00. capture_ref: `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:36`. capture_quote: `/var/lib/pacman/local/pacman-contrib-1.13.1-1`. [inf] The `:24` “when available” condition resolves to available; S011 compare/merge advice is unchanged.
- The `:9-15` counts remain dated 2026-10-19 observations. R18/R17 captures carry no fresh `/etc` sweep; [unk] change after 2026-10-20 13:23.

Source: S060; S051/S052; S011.
```

Out of R17 defect5's named file list: candidate-only, no ordinal uplift.

Scope: executed=read-only: read (RULES, target, spotcheck, R17 capture region); bash reads of lane captures; `git show` baseline bytes; `grep`/`sed`/`cat`/`ls` over pacnew-plane, `/var/lib/pacman/local/pacman-contrib-1.13.1-1/files`, `/usr/bin/pacdiff`; wrote only this report.
