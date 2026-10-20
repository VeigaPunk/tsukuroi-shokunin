# FxFresh08 — C3 journal/boot-plane freshness review

Axes: evidence/currentness; same-premise coverage; safe recheck semantics.

## Findings

- **MEDIUM — R18-FRESH-NoticeJournal-03 is invalid as an R18 current-image claim.** `journal-boot-plane.md:455` calls the extracted hooks the “current-image fact.” Its cited R17 capture is stamped 12:35 (`boot-chain-capture.txt:2`); it records `HOOKS=...` at :177 and the booted/default image in `boot-chain-r17.md:86-94`. S060 is 16:06 (`host-capture-r18.txt:3`), but :6/:34 establish only running kernel 7.2.11 and installed mkinitcpio 42.2-1—not the current UKI hash/default or its extracted hooks. **Fix:** phrase the image data as the R17 observation and mark R18 image identity/hooks unverified, or bind a current extraction/hash. Also compare against the historical base-file list, not an “effective configured list”: `journal-boot-plane.md:433-436` explicitly says `/etc/mkinitcpio.conf` is not the effective configuration; drop-ins were last re-opened 2026-10-19, not in S060.

- **VALID — R18-FRESH-NoticeJournal-01 / -02, with a citation improvement for -02.** S060 :75-81 directly lists `home`, `root` and `SNAPPER_CONFIGS="root home"`. Both notices explicitly leave current `snapper list-configs` output unverified and rollback re-audit open (`journal-boot-plane.md:447,451`); boot-0 “Creating…” entries remain historical. Add S060 :76-77 to -02’s notice citation (currently it cites :80 for the filesystem listing).

## Coverage, residual risk, verification gaps

Both target-file current-use Snapper loci (:147-149 and :364-365) have notices; other rollback-net restatements have R18 sibling corrections. The appended recheck correctly separates invocation from ALPM completion, mtime from local acquisition, unit properties from active totals, and config names from rollback proof (`journal-boot-plane.md:460-468`). No other actionable defect found. LSP device/server unavailable (`xd://lsp` not mounted); grep was used only to locate literal neighbors, not as semantic proof. No execution.

Scope: executed=none