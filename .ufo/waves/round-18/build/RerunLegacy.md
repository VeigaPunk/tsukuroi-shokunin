# RerunLegacy

Axes: gate fidelity; baseline comparability; scope safety.

## Findings
None in the assigned rerun scope.

- [obs] Freshness gate: PASS, no findings, 48/48 records resolved, exit 0 ([`RerunLegacy.outputs.txt:10-24`](/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/build/RerunLegacy.outputs.txt:10-24)).
- [obs] Boot-chain gate: PASS, no findings, 5 verdicted kernel entries among 6 entries, exit 0 ([`RerunLegacy.outputs.txt:26-40`](/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/build/RerunLegacy.outputs.txt:26-40)).
- [obs] The checker code, `corpus/knowledge`, and R17 captures have no diff between baseline 842a5312 and prerequisite 51dd9ee ([`RerunLegacy.outputs.txt:5-8`](/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/build/RerunLegacy.outputs.txt:5-8)). Counts reproduce the R17 spot-check: 5 kernel verdicts and 48 records with 48 unique IDs ([`round-17-verifier-spotcheck.md:42-44,62-64`](/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-17-verifier-spotcheck.md:42-44)).

## Residual risk / verification gap
The boot-chain gate is verdict-conformance only, not a boot test; its reported scope excludes boot, package, service, and initramfs actions ([`RerunLegacy.outputs.txt:35`](/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/build/RerunLegacy.outputs.txt:35)). No host probes or code edits; no tools installed.

Scope: executed=mktemp -d; git clone --no-hardlinks /home/vgpnk/Projects/shokunin/tsukuroi-shokunin /tmp/tsukuroi-r18-rerunlegacy.Ln6wVB; git -C /tmp/tsukuroi-r18-rerunlegacy.Ln6wVB remote remove origin; git -C /tmp/tsukuroi-r18-rerunlegacy.Ln6wVB checkout 51dd9eeaa305539fa3cfc6ee275978dc18043b79; python3 tools/check-freshness-r17.py --revision 51dd9eeaa305539fa3cfc6ee275978dc18043b79 (cwd=/tmp/tsukuroi-r18-rerunlegacy.Ln6wVB); python3 tools/check-boot-chain.py --revision 51dd9eeaa305539fa3cfc6ee275978dc18043b79 (cwd=/tmp/tsukuroi-r18-rerunlegacy.Ln6wVB); git -C /tmp/tsukuroi-r18-rerunlegacy.Ln6wVB diff --quiet 842a5312b704b5cda10fd80ec1fdee5fb381ba97 51dd9eeaa305539fa3cfc6ee275978dc18043b79 -- corpus/knowledge .ufo/waves/round-17/l1-capture tools/check-freshness-r17.py tools/check-boot-chain.py.