# ConnGodspeedConformance (r17, connector)

**r16 failure [obs].** `.ufo/waves/round-16/build/dispatch.json` `.taskCall.tasks[*].task`: 64/64 start with exactly `/skill:godspeed\n\n` (17 B) then item text (`Own ONLY…`); divergence at directive offset 0 (`Y` of `You are…`). The 429-B directive (`sha256 db88963c…`) occurs 0 times in the file, `taskCall.context` included; header is 17/446 prefix bytes. `round-16` spec prompts: 0/64. `corpus/lessons/round-16.md:63` disclosed it; `corpus/lessons/round-16-verifier-spotcheck.md:130` states the rule. `round-16/falsify/dispatch.json` is absent, so “Fresh falsify tasks explicitly carry the verbatim directive” is uncorroborated.

**r17 [obs].** 72/72 tasks carry `/skill:godspeed\n\n` + all 429 directive bytes, once each, then `\n`; no CRLF; task-name set == `registry.members`.

**Move (C3, mined mistake).** Byte-check now, decoded UTF-8 (writers may emit `\u2014`): `bad=[t for t in tasks if not t["task"].encode().startswith(b"/skill:godspeed\n\n"+D) or t["task"].count(D.decode())!=1]`, after `sha256(D)==db88963c…`. Codify as `tools/check-dispatch-directive.py --revision <hex> --branch master --selftest`: exit 2 on E-DIRECTIVE-DRIFT / E-DISPATCH-ABSENT / E-REVISION-INVALID|NOT-LANDED|NOT-PUSHED; exit 1 on R17-GODSPEED-SHORT (first-divergence offset) or -DUP; JSON carries revision/branch/branch_tip/dispatch_sha256. Authority: committed dated 429-B snapshot (`--revision` reads git only; equals `SKILL.md` body); selftest replays r16's blob (expect 1, 64 findings) and an `ensure_ascii` fixture.

**Risks.** Snapshot ages → drift exits 2, not 1. r17 build dir untracked → commit before revision proof. Proves payload, not transport [inf]. Needs `RevGateRegistry` row.

**Verify.** Inline check on r17 (0 bad), r16 blob (64 bad); gate selftest rc=0; `--revision <landing>` rc=0.

Scope: executed=python3 heredocs (read-only JSON/byte/hash comparisons), git ls-files/status/log/check-ignore, grep, sed, wc, ls, cat, od, sha256sum
