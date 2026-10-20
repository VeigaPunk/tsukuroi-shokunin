# FxMutLts — SURVIVES; mutant KILLED

Axes: domain sensitivity; original-five stability; byte-exact restoration.

Sandbox `/tmp/tsukuroi-r18-FxMutLts.GxX0QFVM`: unique mktemp, `clone --no-hardlinks`, origin removed. P=`68a8ae035fde33360cbbe21dc92ca0eacf0a5b33`; M=`c93e7d2ad2cb79174476109e93b95c3e478e6b0f`; R=`9568611c4b77a4776d3df90049d114e7849dab8b`.

Mutant: authoritative `Now` citations become linux-only; historical evidence/fixtures unchanged. Exact diff:

```diff
diff --git c/corpus/knowledge/boot-chain-r17.md w/corpus/knowledge/boot-chain-r17.md
index 3e9c57e..c30fefd 100644
--- c/corpus/knowledge/boot-chain-r17.md
+++ w/corpus/knowledge/boot-chain-r17.md
@@ -207 +207 @@ Checks (read-only) and operator-only actions; tsukuroi takes none of these actio
-- Now: and equals the installed `/usr/lib/initcpio/init` (B:182, 198, 251)
+- Now: and equals the installed `/usr/lib/initcpio/init` (B:182, 251)
@@ -216 +216 @@ Checks (read-only) and operator-only actions; tsukuroi takes none of these actio
-- Now: byte-identical to the installed hooks (B:183–184, 199–200, 252–253)
+- Now: byte-identical to the installed hooks (B:183–184, 252–253)
```

Let G=`/usr/bin/python3 -B /tmp/tsukuroi-r18-FxMutLts.GxX0QFVM/tools/check-boot-chain.py`.

Same detector: `G --revision <P|M|R> --branch FxMutLts --statement-corrections --registry-from <P>`.

Domain P/M/R: PASS4/FAIL2/PASS4; expected/observed exits0/1/0; P/R findings=[].

M findings: `CORR-R18-CORR-02-UNRESOLVED` and `CORR-R18-CORR-03-UNRESOLVED`, each “notice Now value is missing or wrong” (`tools/check-boot-chain.py:726–739`).

Controls P/M/R: ordinary revision PASS, five kernels/six entries, findings=[], exit0; selftest76/76, exit0. Historical `842a5312b704b5cda10fd80ec1fdee5fb381ba97`, registry P: count0, expected/observed exit1, `CORR-R18-CORR-{01,02,03,04}-UNRESOLVED`, each “correction notice missing or duplicated”.

MD SHA256 P=R: `4e5018ca90f40b7687c74f6688f371677b0eaef4e0cba02bebefe08081c8c9a0`; M: `9a9591cdc8794b55b63dce6d59f408ddc720eafece3c8492f8cad2b985d9cbb2`. Verdict JSON unchanged: `1ec99ab757700f6bed9f2b171ce4ee3626b58f982f021fe22f33ad1911f08f14`. Gate/registry hashes also unchanged.

Unknowns: other prose mutations/real boots untested. No installations or production-code edits.

Scope: executed=mktemp; sandbox-only git clone --no-hardlinks/checkout --detach/remote remove origin/switch -c/commit --only --no-verify/rev-parse HEAD/diff; sha256sum(P,M,R); G --selftest(P,M,R), --revision(P,M,R) --branch FxMutLts, --revision(P,M,R,842a5312b704b5cda10fd80ec1fdee5fb381ba97) --branch FxMutLts --statement-corrections --registry-from P.
