# FxGodspeedW2 — godspeed conformance of wave-2 dispatch (re-check wave 1)

Verdict: **SURVIVES** — godspeed conformance of THIS wave survives byte-level falsification; wave 1 also re-verified clean.

Method: one python3 read-only byte comparison (JSON-decoded task strings encoded back to UTF-8) over both dispatch files against `/home/vgpnk/.agents/skills/godspeed/directive.md` (429 bytes; required preamble `/skill:godspeed\n\n` + directive = 446 bytes). A task passes iff its bytes start with the full 446-byte preamble AND the directive bytes occur exactly once.

Evidence [obs]:
- `tsukuroi-shokunin/.ufo/waves/round-17/falsify/dispatch.json` `taskCall.tasks`: **81 tasks, 81 pass, 0 fail**.
- `tsukuroi-shokunin/.ufo/waves/round-17/build/dispatch.json` `taskCall.tasks`: **72 tasks, 72 pass, 0 fail** (re-verification).
- Output: `directive_bytes=429 required_prefix_bytes=446`; `wave2-falsify tasks=81 pass=81 fail=0`; `wave1-build tasks=72 pass=72 fail=0`.
- Counts cross-check [obs]: falsify `counts.total=81` (spawn 81), build `counts.total=72` — task arrays match declared counts.

Could not verify: nothing material; the read tool's elided `tasks` arrays were fully covered by the python parse, not sampled. Directive file read fresh this session [obs].

No installs performed (none needed).

Scope: executed=python3 single read-only byte comparison of taskCall.tasks[*] in .ufo/waves/round-17/falsify/dispatch.json and .ufo/waves/round-17/build/dispatch.json against /home/vgpnk/.agents/skills/godspeed/directive.md
