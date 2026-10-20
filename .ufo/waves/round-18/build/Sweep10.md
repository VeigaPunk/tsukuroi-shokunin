# Sweep10 — partial-upgrade-recheck-r15.md C3 reconnaissance

Axes: freshness (one candidate notice); depth/operability unchanged.

[obs] Surface equals baseline bytes (`sha256 d19c6fbf…`); all quotes are baseline-exact.

Already covered by R17, no new record: `:13` package_versions → R17-FRESH-PARTIAL-01; `:14` pending_updates → -02; `:34` marker 2288 → -03; `:15` shared birth → -04; `:55` "Boot coupling is latent, not active." → -05; `:117` "stays blocked" → -06; `:56-57` hook mismatch → R17-SYMLINK.

[obs] One still-live stale sentence at `:55-56` is unquoted: "Installed `mkinitcpio 41.1-1` has `42.2-1` pending." R17-FRESH-PARTIAL-05 notes 42.2-1 installed but supersedes only the paragraph thesis. R18: `mkinitcpio-42.2-1` installed (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:34`); 7.2.11-arch1-1 running (`:6`). The 41.1 record stays historical; no dated fact is called false.

Proposed append (id `R18-FRESH-Sweep10-01`; path `corpus/knowledge/partial-upgrade-recheck-r15.md`; baseline_quote ``Installed `mkinitcpio 41.1-1` has``):

```markdown
## R18-FRESHNESS — partial-upgrade-recheck-r15 mkinitcpio installed-version sentence (2026-10-20)

Appended 2026-10-20; earlier bytes unchanged; supersedes current-use only; historical snapshots preserved; read-only scope, no package or reboot clearance.

- Old at `:55-56`: "Installed `mkinitcpio 41.1-1` has `42.2-1` pending." True at the R15 snapshot; preserved. now: 2026-10-20T16:06:17-03:00; `mkinitcpio-42.2-1` installed (`.ufo/waves/round-18/l1-capture/host-capture-r18.txt:34`); 7.2.11-arch1-1 running (`:6`). capture_ref: `.ufo/waves/round-18/l1-capture/host-capture-r18.txt:34`. Supersedes the installed-version clause only; hook observation and R17-SYMLINK pointer unchanged.
- [unk] R18 re-measures no `pacman -Qu`, `%w` birth, libinput log or hook file, so the five-probe recheck precondition is unmet.

Source: S060; S052; S051; S059.
```

No duplicate for `:112-113` "The pending set crosses the boot chain": R17-FRESH-PARTIAL-06 supersedes that bullet's conclusion for the same pending set. [unk] 09:31/13:23 `-U` transactions change nothing (zcode/elephant unmentioned; `:3` invalidates on any transaction).

Out of R17 defect5's named files: candidate-only, no ordinal uplift.

Scope: executed=read-only: read; bash grep/awk/sed/sha256sum/git show/cat/ls/wc; python3 read-only JSON; lane repo and committed captures only; wrote only this report.
