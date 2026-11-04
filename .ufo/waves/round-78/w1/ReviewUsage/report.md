# ReviewUsage — round 78

Axes: depth and operability.

## Findings by severity

No actionable source/companion defect found in U1–U6. All six hold as finite hypothetical entry contributions, not live-host measurements. No C1 source/companion kill rule triggered. This is a lane-authored recommendation, not outside closure or admission; integrated count and final result binding have not been exercised.

## Independently checked evidence

Read SCORECARD.md :6497–6540 and frozen expected.json, then independently derived every input/output from pinned journald-manager.c :91–134 before reading the candidate. Exact derivations and immediate caller/error-path boundaries are recorded in `source-review.md` beside this report.

- U1: regular active.journal, stat succeeds, blocks 8, size 1048576 → 4096; :119–131 uses blocks, not size.
- U2: regular archived.journal~, stat succeeds, blocks 16, size 8192 → 8192; second suffix accepted.
- U3: regular ignored.txt, hypothetical stat succeeds, blocks 8, size 4096 → 0; suffix rejection precedes stat.
- U4: symlink link.journal, stat succeeds, blocks 8, size 4096 → 0; no-follow entry stat and nonregular rejection.
- U5: directory directory.journal, stat succeeds, blocks 8, size 4096 → 0; nonregular rejection, no recursion.
- U6: unstatable.journal, hypothetical regular/blocks 8/size 4096, stat fails → 0; logs and continues without consuming unavailable metadata.

Both frozen source snapshot digests independently observed with sha256sum and match expected.json. Manager :114 separately obtains filesystem availability; :105–112 opening/statvfs errors are fatal, unlike per-entry U6. Caller cache_space_refresh :161–166 propagates errors and stores distinct used/available values. Manual journalctl.xml :943–944 and :969–973 supplies context, not an equality proof between CLI and manager accounting.

Read final ScribeNote/data.json :1–61 and revised note.md :1–83 after ScribeNote-2 explicitly requested renewed review. Every descriptor, order, output and source identifier matches expected.json. Companion accurately explains selection, no-follow scope, nonregular rejection, skipped stats, allocated blocks, source provenance, and hypothetical limits. Reread the revised source header and QUALITY section; registry S327/S328 rows confirm the stated tier/type/ranges and rejected-documentation boundary. The revised prose retains all six source derivations; no new U1–U6 defect or kill rule was found. The earlier companion hash cc0457... is superseded.

Reviewed bytes:
- data.json SHA256 `13fc82d4cd0756f05b997c7f7a8f64a6976c61aa34d601611a0c73a86a06bd1d`
- note.md SHA256 `f1099591008b0fc8db50a79d72ac9033358dc8af0322816697f2c0a899e98608`

`verdict.json` binds those exact data bytes and includes case-specific reasons/source anchors. Any data or companion revision requires renewed review; L1 must integrate reviewed data byte-exact and preserve the final review digest in the unique reviewer-role result.

## Residual risk and verification gaps

LSP unavailable: xd://lsp returned No such tool; references, definition and diagnostics could not run. Literal search and direct source reading are fallback evidence, not semantic tooling proof. No source compilation, tests, installed-systemd execution, network refetch or final integrated counter run by this reviewer. No claim about installed Arch binaries, all filesystem inputs, scan races, overflow, or authenticity. Counter :40–70 checks snapshots/content/digests/seat identity; it cannot authenticate a fabricated report plus fabricated orchestrator bundle, as the frozen declaration already acknowledges. Runtime rerouting/resume admission is not changed or exercised by this source/companion artifact.

No installations, privileged probes, production edits, git mutations, or sibling writes. Own scratch remained empty and is removed before handoff. No ordinal uplift or outside verdict asserted.
