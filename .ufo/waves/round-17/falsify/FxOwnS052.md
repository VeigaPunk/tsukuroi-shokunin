# FxOwnS052 — attack on own-work SOURCES row S052

**Verdict: SURVIVES** — anchor ranges, `teaches`, and the lesson Gate quote all match `fresh-capture.txt`; `teaches` does not overreach. [obs]

## Evidence
- Anchor: `corpus/SOURCES.md:58` = "capture header 2026-10-20T12:38:12-03:00; lines 1-86". Timestamp byte-exact at `fresh-capture.txt:2`; `wc -l` → 86. Range exact. [obs]
- `teaches` col 5 maps fully: package dir names `:15-29`; DKMS `:35-38`; snapper configs `:42-46`; enabled units `:47-51`; limine defaults `:58-76`; "without invoking pacman" = header `:2` (pacman.log greps read a log, invoke nothing). [obs]
- `teaches` col 7: 42.2 at `:16` (vs claimed 41.1); NVIDIA 615.78.08 `:24-25,:33,:36-38` (vs 610.57.04); snapper configured `:43-46`; "pending-update count was not re-measured" is a disclosed absence — no `-Qu`/checkupdates output anywhere in the capture. No clause exceeds the bytes. [obs]
- Lesson `corpus/lessons/round-17.md:24` quote "line 16: '/var/lib/pacman/local/mkinitcpio-42.2-1'" byte-exact at `fresh-capture.txt:16`. [obs]
- Lesson Gate row cites fresh:10-12 for core/extra 2026-10-17 mtimes — true (`:10`,`:11`; `:12` multilib also 10-17). Used-by correct: `boot-chain-r17.md:179`. [obs]

## Residual / unverifiable
- "No longer hold" framing presumes the earlier 41.1/610.57.04 claims from prior rows; the capture shows only the new state. Disclosed scope; not overreach. [inf]
- Anchor has no capture file hash — identity rests on the timestamp alone (wave-1 build notes disclose this). [unk]
- Row/lesson omit the pacnew-sweep limits (`:77-82`, rc=1); consistent omissions, but the knowledge entry must not read them as pacnew absence (SourcesRecheckDraft flag 5). [inf]

Scope: executed=wc -l /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-17/l1-capture/fresh-capture.txt
