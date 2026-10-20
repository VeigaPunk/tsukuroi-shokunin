# SrcSystemdRun — systemd-run(1) `--unit=` / `--collect` source row

Answering model: commandcode/deepseek/deepseek-v4.1-flash (as reported by the harness).

- [obs] The named URL did not answer: `https://man.archlinux.org/man/systemd-run.1` and four
  variants (`.1.en`, `.1.txt`, `extra/systemd/systemd-run.1.en`, `.1/`) all failed with
  `ECONNRESET`, zero body bytes. Transport failure, not a 404; not recorded as absence.
- [obs] Text verified instead at pinned `v262`:
  `https://raw.githubusercontent.com/systemd/systemd/v262/man/systemd-run.xml` — creation sentence
  lines 64-65, `--unit=` lines 127-133 (quote 130-131), `--collect` lines 543+ (quote 545) — and in
  the installed `/usr/share/man/man1/systemd-run.1.gz`
  (`.TH "SYSTEMD-RUN" "1" "" "systemd 262"`). The freedesktop `latest` render also carries the
  same wording under header `systemd 262`.
- [obs] Exact quotes:
  1. “systemd-run may be used to create and start a transient .service or .scope unit and run the
     specified COMMAND in it.” (21 words)
  2. “Use this unit name instead of an automatically generated one.” (10 words)
  3. “Unload the transient unit after it completed, even if it failed.” (11 words)
- [obs] Version: systemd 262. The Arch render's own footer was never observed, so no `262.1` footer
  string is claimed.
- [obs] C2 linkage: the snapper plugin runs
  `systemd-run --unit="limine-snapper-${op}-${SNAP_ID}-$$" ... --quiet --collect`
  (`.ufo/waves/round-19/l1-capture/host-capture-r19b.txt:1184-1188`); the journal shows
  `_SYSTEMD_UNIT=limine-snapper-add-1-5846.service` and `limine-snapper-add-2-260668.service`
  (`.ufo/waves/round-19/l1-capture/host-capture-r19c.txt:14-15`), matching op/SNAP_ID/PID.
- [inf] `--collect` makes a finished transient unit unloadable, so such a unit may be absent from
  later unit listings while its journal records remain; the man page grounds the mechanism, not that
  a write happened.
- [unk] Whether the Arch man page currently renders identical text/footer (site unreachable).
- Rejected: splicing quotes 1+2 into one “exact” quote; asserting an unobserved Arch footer;
  treating `--unit=` as proof of provenance for any specific `/boot` event.

Draft row (S066 provisional, docs, A): `.ufo/waves/round-19/build/drafts/SrcSystemdRun.row.md`.

Scope: executed=none
