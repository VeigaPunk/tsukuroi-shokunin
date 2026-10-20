# NoticeJournal — journal-boot-plane.md freshness drafts (round 18)

Target: `corpus/knowledge/journal-boot-plane.md`, baseline 842a5312; unchanged in HEAD 51dd9ee.

## Drafts
- `.ufo/waves/round-18/build/drafts/NoticeJournal.append.txt`: three `## R18-FRESHNESS` sections.
- `.ufo/waves/round-18/build/drafts/NoticeJournal.records.json`: 3 records, eight required keys.

## Findings
- **R18-FRESH-NoticeJournal-01 (147-149)**: [obs] `/etc/snapper/configs` = home, root (`host-capture-r18.txt:76-77`); `SNAPPER_CONFIGS="root home"` (`:80`). [unk] `snapper list-configs` output not re-run.
- **R18-FRESH-NoticeJournal-02 (364-365)**: same evidence (`:80`) against the "empty `snapper list-configs`" premise. Boot-0 "Creating a Snapper config" lines stay historical; re-audit stays open.
- **R18-FRESH-NoticeJournal-03 (244-245)**: image scope. R17 `boot-chain-capture.txt:174-177`: default UKI VERSION 42.2, `HOOKS="udev plymouth keymap consolefont encrypt resume"`, which differs from the configured list at :244-245. R18 `:6` kernel 7.2.11; `:34` mkinitcpio-42.2-1. [unk] current `/etc/mkinitcpio.conf`: not captured in R18, not re-read.

## Verified (read-only)
- Each `baseline_quote` occurs once in the 842a5312 bytes; each heading is absent there and appears once in the draft; each `now` and `capture_ref` is in its section; each `capture_quote` is an exact substring of its cited line; JSON parses.

## Integrator dependencies
- `S060` is absent from `corpus/SOURCES.md` (HEAD ends at S059); add the row before landing.
- `tools/check-freshness-r17.py` expects `observed_now` and a round-17 `CAPTURES` list; these drafts use `now` and R18 captures. The build gate must accept this schema.
- Both cited captures are tracked in git.

Installs/updates: none. Production files untouched; no notice appended.

Scope: executed=read-only `git show`, `git ls-files`, `git status`; `grep -cF`, `sed -n`, and `jq` checks on the drafts and captures.
