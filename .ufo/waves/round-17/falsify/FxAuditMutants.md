# FxAuditMutants

[obs] **FAILS: selftest mutation coverage** — seven killed, one survived, none inconclusive.
Axes: coverage, operability, calibration.

Eight fresh clones: `dd15c183f2f2481db67d0234038117a0d5b7034c`; `/tmp/tsukuroi-r17-FxAuditMutants-r6bbpbat/m{1..8}/lane`.
Detector: `bash tools/boot-chain-audit.sh --selftest`, 45s bound; expected detection=rc1.
P=`TSUKUROI_BOOTCHAIN_SELFTEST: PASS total=44 failed=0`;
F(n)=`TSUKUROI_BOOTCHAIN_SELFTEST: FAIL total=44 failed=n`.
All pristine/restored runs: P/rc0; all stderr empty.

`tools/boot-chain-audit.sh` token/block diffs; K=killed, S=survived:

|Mutant:line|Old→new|Result/output/rc|Mutated SHA256|
|---|---|---|---|
|M1:593|`"$kernel" != 1`→`"$kernel" = 1`|K/F(14)/1|cfd6f144887d12ecbc6e4e80d601c5a28f0f72f920d490dc2672095ec0b34ba2|
|M2:597|`"$booted" = 1`→`"$booted" != 1`|K/F(14)/1|3c9c87d4b3dcbabbfd00ce423080b924aff635692fa1dc8fad2d51e7bf2c4440|
|M3:601|`"$hassnap" != 1`→`"$hassnap" = 1`|K/F(6)/1|e8958e84e706b1d6eed0ef315c5dd91b8298643a74acf3555e991aafab426aa6|
|M4:601|`"$selected" != 1`→`"$selected" = 1`|K/F(5)/1|585f3111e00894cf881500d5ac6f7c97ed3641a88620a6ae3614126b8b47d773|
|M5:605|`"$sys" -gt 0`→`"$sys" -eq 0`|K/F(7)/1|87180de7001f08a7ff6142c20508c97491bd537c142dac02fe8e0c4b872040e9|
|M6:301|Delete `&& [ -s "$dst" ]`|S/P/0|69f2d21c77723407dbdec9811cdd9eb28c4271c9d30f93c40053a616fc3e5708|
|M7:601–609|Swap blocks 601–604↔605–609|K/F(2)/1|dd4aec8c39df0fbd0a919622fad6e4dd44af2169d005afadc151e099cf4e063d|
|M8:605|`symlink->sysroot`→`symlink->/sysroot`|K/F(7)/1|7ce22a6a6f84bc45a17427c8f7b62194c4cc2a84192c523770e1cd2368ba64da|

[obs] M1: `FAIL v1-not-a-kernel: expected [NOT-A-KERNEL-ENTRY] got [UNTESTED]`.
M7: `FAIL v3-non-snapshot-not-selected: expected [UNTESTED] got [PATH-ALIASED-EMULATED]`.

Before=restored SHA256, all eight: `c81a6faeb5613d14db99a98b25396e3020b9f61049ac0b0cbd28cc0ad05ef8e4`.
[obs] Selftest sets fixture mode (:861); image_identity's fixture return (:282–294) bypasses :301.
[inf] M6 exposes nonempty-section coverage gap, not incorrect corpus verdicts.
[unk] Live C1 behavior UNPROVEN; no host execution. Lane source untouched.

Scope: executed=python3 mutation harness,git clone --quiet --no-hardlinks,git -C <clone> rev-parse HEAD,git -C <clone> diff --unified=0 -- tools/boot-chain-audit.sh,bash <clone>/tools/boot-chain-audit.sh --selftest
