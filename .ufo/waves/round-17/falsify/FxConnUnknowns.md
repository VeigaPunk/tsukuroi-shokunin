# FxConnUnknowns — [unk]/[inf] labelling honesty audit

Verdict: FAILS — labelling mostly disciplined; one [obs] hides a causal inference; three inferences unlabeled.

[obs] that is really [inf]
- boot-chain-r17.md:26 "[obs] ran `limine-update` …, which rebuilt them outside any pacman transaction": causality inferred from the sudo COMMAND, later mtimes (B:124–125), absent pacman.log builds (B:68–74); no capture shows limine-update output. Same shape at :35 is "[inf] That write explains the … mtime". Repeated unlabeled at :151; contradicts its QUALITY 3 (:158).
- boot-chain-r17.md:106 "[obs] **EFI fallback is not independent.**": headline is the inference; [inf] only on the next sentence.

Unlabeled inference
- arch-news-gate-2026.md:89 "precondition is still unmet … so its TPM2 re-enrollment step does not apply": flavour-from-HOOKS is [inf] in initramfs-v42-sysroot-recovery.md:70 ("does not by itself establish the flavour"); TPM2 non-application adds another unlabeled step.
- boot-chain-r17.md:76–77 "a non-snapshot entry that has not booted → UNTESTED": "linux-lts has not booted" is a negative inference; no boot-history sweep among cited evidence (B:125, 187–200; S:42–43; F:36) [inf]; violates its QUALITY 9 sweep standard.
- Minor: initramfs-v42-sysroot-recovery.md:85 "[obs] every 42.2 image … (E:5, :8)": universal cites one-image lines; the four-image sweep is E:51–66.

Clean: partial-upgrade-r15:175–182, update-safety-v3:439–453, driver-firmware-plane:274–285; lesson STEER-SCOPE carries "[inf]".

Unverified: B:187–200 unread; item 4 rests on the entry's own citations [inf]; partial-upgrade:179 tail unread.

Scope: executed=none
