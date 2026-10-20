# Freshness mutants

[obs] Axes: freshness, detector coverage, exact restoration. **C2 SURVIVES; selftest-sensitivity completeness FAILS.**

Clone: `/tmp/tmp.xcs0h6L27D/lane`; HEAD=`dd15c183f2f2481db67d0234038117a0d5b7034c`. P=`tools/check-freshness-r17.py`. Expected detector: `python3 P --selftest` (S); also ran `python3 P --revision dd15c183f2f2481db67d0234038117a0d5b7034c` (R).

[obs] Pristine/eight restorations: S `CHECK_FRESHNESS_R17_SELFTEST: PASS (53 cases, 53 passed, 0 failed)`, rc=0. Every R: `status=PASS, resolved_records=48, record_count=48, findings=[]`, rc=0.

Seven killed mutants: S `CHECK_FRESHNESS_R17_SELFTEST: FAIL (53 cases, 52 passed)`, rc=1; failing fixture below. M3: S PASS, 53/53, rc=0.

| Mutant at P:line | Fixture/verdict | Mutated Git-blob SHA1 |
| --- | --- | --- |
| M1:202 prefix→False | history-rewritten/KILLED | a6196acc679c57b2b9953b32da33bcfb35c7544f |
| M2:214 baseline-heading→False | notice-at-baseline/KILLED | 763ddfc51866f2833dee89c85abacbc9146dbf8a |
| M3:102 section-end→EOF | SURVIVED | 6c8f4c4e673ecc2172e238c69f8bb01d30110316 |
| M4:256 capture-quote→False | capture-quote/KILLED | 290b9ac9d5d5100a32429ba7a654e3d451218865 |
| M5:222 duplicate→False | notice-duplicated/KILLED | 1e7cfadc097197308d468c91cfa8a3d810bad54e |
| M6:205 baseline-quote→False | quote-absent-everywhere/KILLED | 19bd9278d71974e7ffeaf47ada447a18f0cc212a |
| M7:233 omit observed_now | notice-content-observed/KILLED | c7569b4f908a591e757462fc14451eae2dd81d50 |
| M8:233 omit capture_ref | notice-content-ref/KILLED | 981f676c043a4ad1dd426fbede2040ac500059a4 |

[obs] Every cycle: B→mutant→B; pristine/restored Git-blob SHA1 B=`d2a0bd0194e9fba430b37e900c6d73de68cde56f`.

[obs] M2/M6: finding-set kills.

[inf] M3 can borrow content across headings; missing isolation fixture. [unk] Host truth untested; no contract change.

Scope: executed=bash -c 'scratch=$(mktemp -d) && git clone --quiet --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin "$scratch/lane" && printf "%s\n" "$scratch/lane"',git -C /tmp/tmp.xcs0h6L27D/lane rev-parse HEAD,git -C /tmp/tmp.xcs0h6L27D/lane show dd15c183f2f2481db67d0234038117a0d5b7034c:tools/check-freshness-r17.py,git -C /tmp/tmp.xcs0h6L27D/lane hash-object --no-filters /tmp/tmp.xcs0h6L27D/lane/tools/check-freshness-r17.py,python3 /tmp/tmp.xcs0h6L27D/lane/tools/check-freshness-r17.py --selftest,python3 /tmp/tmp.xcs0h6L27D/lane/tools/check-freshness-r17.py --revision dd15c183f2f2481db67d0234038117a0d5b7034c
