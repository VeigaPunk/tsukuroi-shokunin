# FxMdJsonAgree — boot-chain-r17.md ↔ boot-chain-r17.json consistency

**Verdict: SURVIVES.** No verdict, hash, or rule-semantics disagreement found. Evidence-line sets diverge (cosmetic). [obs] unless marked.

1. **Verdicts** — all 6 rows agree: md:67–72 vs json:77 (BOOTED-OBSERVED), 133 (UNTESTED), 177/230 (PATH-ALIASED-EMULATED), 277 (CONSISTENT-PRE42), 320 (NOT-A-KERNEL-ENTRY). Each json verdict follows its own first-match rules (json:27–54) from its typed fields.
2. **Hashes** — sha256 prefixes match every row (json:62,118,162,215,262,305). All five md:80 `path:`#↔b2sum pairs verified equal: S:34=B:172, S:42=B:188, S:54=B:220, S:60=B:236, S:68=B:204; json b2sum_prefixes match (json:63,119,163,216,263).
3. **Rules** — md:74–79 order and semantics identical to json:27–54. md prose omits rule-2 parentheticals ("file mtime before boot start"; "/boot is outside that sweep"), carried instead at md:91–96 — wording drift, not semantic.
4. **Evidence lines** — spot-verified: B:159–161 ro=true, B:166–167 snapper rows, S:113–115 loader vars, B:255–258 sweep (0/58674), S:84, B:236. All support both files.

**Findings (low):** F1: md table evidence columns are lossy subsets/supersets of json arrays (md:67 omits B:115,219,255,S:7/25/29,E:5; md:68 omits S:37; md:69 omits B:167,S:48–50; md:71 omits B:166,S:62–64; md:72 omits S:84; md ranges include B:176–177/192–193/224–225 json skips). No contradiction. F2 [inf]: json omits md's falsifier/operator-checks prose (schema design).

[unk] none material.

Scope: executed=jq -c '.verdict_rules[],(.entries[]|{...})' boot-chain-r17.json; wc -l + nl -ba + awk line-number check of boot-chain-capture.txt
