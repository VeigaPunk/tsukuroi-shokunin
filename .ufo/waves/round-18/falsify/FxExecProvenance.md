# FxExecProvenance

## SURVIVES
- `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/l1-capture/harness-probe-capture.json:6-16,20-25` contains exactly two linked records: invocation `e6ad937b` and result `cff2269b` share tool-call ID `toolu_01Dud7UPXm3fqougBLBpGvU2`; the invocation explicitly runs `sha256sum capture-r18.sh` before the wrapper. Its reported `bfe32ba3076512bfa8b24fe7f00c6f32c99bfad04c5daa20d3fd6f22e415824f` matches `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/l1-capture/host-capture-r18.txt:1` and the result text at JSON line 29. The long output at result line 72 matches `host-capture-r18.txt:72` via retained artifact 80975. JSON `:32-45` discloses 768-byte truncation on that result line; the standalone capture retains it.
- The bounded scope is accurately stated: JSON `:55` says this is one wrapper capture, omitting thinking/unrelated payload and “not an exhaustive shell audit.” `capture-r18.sh:7-29` defines the command/output/rc probes. R17 `.../round-17/l1-capture/exec-log.txt:1-4` identifies its excerpt as transcript-derived; `corpus/lessons/round-18.md:57` explicitly does not promote it to a harness trace.

## Residual risk / required fix
No actionable fix to the bounded claim. Do not use these two records (one invocation/result) as proof of a full-session audit. Independent re-hashing of the landed script was not performed; it would require execution, which was out of scope. Full audit claims would require a complete session ledger and independently retained script/output digests. `xd://lsp` is unavailable; literal search was used only to locate text, not as semantic proof.

Scope: executed=none