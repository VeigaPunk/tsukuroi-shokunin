# ReviewUkiCites

**Outcome: SURVIVES this narrow citation falsifier; full C1 landing/gate status is UNPROVEN.**

- [obs] `corpus/knowledge/boot-chain-r17.md:40-46` claims both UKIs’ init/hooks equal the installed files, but cites only B:182, B:183–184, and installed B:251–253. Round-17 closure defect 3 identifies the missing second-UKI citation scope (`corpus/lessons/round-17-verifier-spotcheck.md:197-200`).
- [obs] `.../.ufo/waves/round-17/l1-capture/boot-chain-capture.txt:170-184` is `omarchy_linux.efi`: init/hooks hashes at B:182–184. The LTS UKI starts at B:186 and its hashes are B:198–200; installed hashes are B:251–253. Exact matches: init `62fcc3a9…` at 182/198/251; btrfs hook `eeac1ed3…` at 183/199/252; plymouth hook `de852646…` at 184/200/253.
- [obs] The R18 draft closes those precise omissions: R18-CORR-02 adds B:198 to the init comparison; R18-CORR-03 adds B:199–200 to the hook comparison (`.ufo/waves/round-18/build/drafts/NoticeBootCorrections.append.txt:10-26`; matching records at `NoticeBootCorrections.records.json:13-30`). The new citations bind each UKI to the installed-file hashes; no broader identity claim is needed for this defect.
- [unk] This is draft evidence only: the current knowledge file still has the original citation set above. I did not verify generic-gate execution or landing, so this does not admit overall C1.

LSP was unavailable (`xd://lsp` returned “No such tool”; mounted-tool list has no LSP device); no grep used. No execution.

Scope: executed=none