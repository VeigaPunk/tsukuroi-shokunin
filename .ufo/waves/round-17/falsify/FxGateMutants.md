# FxGateMutants

[obs] C1 count SURVIVES; C3 binding assurance UNPROVEN. Axes: derivation, witnesses, revision-binding.

R=dd15c183f2f2481db67d0234038117a0d5b7034c; T=tools/check-boot-chain.py.

[obs] Nine isolated mktemp clones; expected detector: `python3 T --selftest` rejects each defect; `python3 T --revision R` is the positive control. Both ran pristine/mutated/restored: 54 executions.

[obs] Every pristine/restored selftest: `CHECK_BOOT_CHAIN_SELFTEST: PASS (53 cases, 53 passed, 0 failed)`, rc0. Every revision run: rc0, `"status": "PASS"`, `"verdicted_kernel_entries": 5`, `"findings": []`.

[obs] Mutant selftest passed/total, verdict, SHA256 (FAIL=rc1; PASS=rc0):

- D1 T:229 no-newer→True; FAIL52/53; KILLED; 8a9e2d8c9f19e9962b0335dfb0a867f2beebfb605d6140815b02f1db191af986
- D2 T:237 symlink-guard→True; FAIL52/53; KILLED; db618be1bd02157b32d4f73d3a94311103b4ab95558bbeefdb0133be29bcbf4e
- D3 T:241 pre42-directory→True; PASS53/53; SURVIVED; bc6cb4aff694c7653ab31391ac0d7e872adf6a2fb83569bf7cadb0b788e40411
- W1 T:303 sha/uname/rootflags-witness→False; FAIL49/53; KILLED; def5d428f888eb781c677c2bbf238211e89bb9a7968eabfe49d71ec89d853c31
- W2 T:308 VERSION-specific→any; FAIL52/53; KILLED; ad5b2fcbb2898e319d492941aebf4eb079f21ffbbb5727f5ce9262f031a27faa
- W3 T:190 line-lower-bound1→0; PASS53/53; SURVIVED; be8dc264f62028fd93c9a8fd7dba75993323bc08b32e17fc16fb6cec1a9befa6
- R1 T:587 local-ancestry-guard→False; FAIL52/53; KILLED; f69d209977b9b62c95fbdab0dc08c2cea6467c79627ee5044946c458a22e6d96
- R2 T:591 remote-ancestry-guard→False; FAIL52/53; KILLED; ec0374614cb633ade59157ac4d5e8fe34a1b6375574804f36f5fc90a8260982e
- R3 T:1115 CLI-bind_revision→ref_sha; PASS53/53; SURVIVED; cb59711a4f7a19094abb88187055c1ddd29904304e3d25f24b84f712d412bf5c

[obs] Killing vectors: D1=derivation-no-newer-witness; D2=derivation-image-dir; W1=sha256-not-cited; W2=version-mismatch; R1=bind-not-landed; R2=bind-not-pushed.

[obs] Before=restored=final SHA256 for all nine: 68fce89fcd2799bf407b774396086bd1b420c65ef8945f57a9646935582900e5. Six killed; three survived; zero inconclusive.

[inf] Survivors identify missing pre42-directory, line-zero and CLI-wiring negative coverage, not false corpus data.

[unk] Live boot and other four revision tools untested. No installs.

Scope: executed=bash -c (mktemp -d; git clone --quiet --no-hardlinks; printf) ×9,git -C /tmp/tmp.gPRteLgpQ6/lane show dd15c183f2f2481db67d0234038117a0d5b7034c:tools/check-boot-chain.py,python3 tools/check-boot-chain.py --selftest ×27,python3 tools/check-boot-chain.py --revision dd15c183f2f2481db67d0234038117a0d5b7034c ×27
