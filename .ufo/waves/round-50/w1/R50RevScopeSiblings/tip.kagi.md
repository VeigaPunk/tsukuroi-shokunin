# kagi-shokunin — Province

**Domain:** secrets & vault ops — the-janitor flows, credential hygiene evidence

**Owns:** the domain knowledge, playbooks, error patterns, and checklists above.
**Refuses:** anything outside this domain; report cross-domain evidence back to the orchestrator rather than absorbing it.

## Surfaces (each path resolved on this host 2026-09-29; `corpus/surface-census.sh` enforces 20 asset / 15 runtime rows, `scanned=4`, `absent=2` runtime rows, symlinks=0, `UNLISTED=0`)

**Round-18 erratum (2026-10-14):** the surfaces below are HISTORICAL — the
janitor substrate was measured absent on this host (no `the-janitor`, no
`~/.config/the-janitor`, no `~/.local/state/the-janitor`, no `tac-check`, no
musketeer profile). The declaration is preserved verbatim as the record of
what the substrate was; live gates correctly fail `DRIFT`/`SETUP`/`DEFECT`
while it is gone, and `claim-ledger` defers the substrate-tagged rows
(`knowledge/substrate-deferral.md`). Unblock: reinstall the substrate, at
which point every pin below is re-verifiable in one run.

Handler:
- `~/.local/bin/the-janitor` (755, 333 lines) — the CLI: `status`/`start`/`stop`/`request`/`run`/`refs`/`whoami`/`cdp-bridge`/`tac-check`/`tac-register`/`_serve` (hidden)
- `~/.config/the-janitor/client.py` (755, 117 lines) — HTTP client: session-id, `THE_JANITOR_REQUEST_TIMEOUT` (the `client.lock` flock lives in the CLI, not here — measured round 15: `grep -nic lock client.py` ⇒ 0; `the-janitor` holds `LOCK_FILE` at L12, `exec 9>"$LOCK_FILE"` at L130/139/175 and `flock 9` at L131/140/176)
- `~/.config/the-janitor/opencode.json` (644) — model overlay (`enabled_providers`, `share: disabled`, `baseURL`)
- `~/.config/the-janitor/op.env` (600) — env-ref file; values never read into an artifact
- `~/.config/the-janitor/config.json` (600) — **inert** decoy (not an opencode-discovered filename; round 6)

Opencode layer that reaches the handler:
- `~/.config/opencode/opencode.json` (644, 455 lines) — global config, merged *under* the overlay
- `~/.config/opencode/agents/janitor.md` — `steps: 4`, `permission: {"*": deny, janitor_auth: allow}`
- `~/.config/opencode/tools/janitor_auth.ts` — `AUTH_OK`/`AUTH_REQUIRED` only
- `~/.config/opencode/plugin/fnm-nudge.js` — global plugin, fails to load at every serve

Runtime state (mutates legitimately; pinned by **shape**, never by content — `corpus/state-shape.tsv`):
- `~/.local/state/the-janitor/{client.lock,session-id}` (600; `session-id` is a conversation marker, ABSENT while stopped); `xdg-data/opencode/opencode.db` (transcripts, 0600; magic + mode + table/row floors); `xdg-data/opencode/log/opencode.log` (0600, size floor); `xdg-data/opencode/{repos,opencode.db-shm,opencode.db-wal}` (created on boot / WAL siblings); `xdg-cache/opencode/models.json` (0600, public catalog)
- The 4 enumerable dirs (`$HOME/.config/the-janitor`, `$STATE`, `$STATE/xdg-data/opencode`, `~/.local/state/tac`) are scanned one level deep: an **undeclared** child is `UNLISTED` + exit 1 — this is the detection path for the round-6 vector (a file dropped into `$CONFIG_DIR` is loaded by the handler)

Evidence/custody:
- `~/.local/bin/tac-check` (755, 88 lines) — offline receipt check
- `~/.local/state/tac/daybreak-blue-access.json`, `~/.local/state/tac/handoff-status.json`, `~/.local/state/the-janitor/tac-daybreak-blue.json`

Network surfaces:
- control plane `127.0.0.1:40961` (unauthenticated OpenCode server, round 7)
- configured model endpoint `127.0.0.1:8080` (dead: Jitsi) vs live llama-server on `34113`
- CDP `9222` + `~/.local/share/the-musketeer/chrome-profile` — **contested with kake** (lease/profile ownership unresolved; kagi pins only the 1Password native-messaging manifest — the profile dir itself is presence-only, mode unchecked). Declared as a partition row in `corpus/adjacency.tsv` (`kake` / `contested` / `presence-only`), so drifting the profile dir to an exact mode pin is `OVERCLAIM`, exit 1 (round 16)

Gates and supporting helpers in this repo:
- `corpus/surface-census.sh` — the declaration gate over the surface list above. `verify` (default): kind/exact mode per declared path, `UNLISTED` children of the 4 enumerable dirs, and the runtime shape pins; `--verbs` exercises the local write-side verbs on scratch overrides (no `op` exec); `--verbs --deep` adds the three probes with a real-world effect (`op run` plain / ref, `tac-register` no-replace) and is operator-present; `--selftest` proves 16 cases on a scratch tree. Exit 0/1/2; `UNVERIFIED` (a shape class that cannot be read) fails the run, `SKIP` (DB locked by a live serve) does not. Data: `corpus/surface-census.tsv` (35 rows, pinned by ledger row `R11-11`), `corpus/state-shape.tsv` (22 rows, pinned by `R11-10`; this said 21 until round 11). Round 10: `CLEAN (assets=20 runtime=15 scanned=4 ok=34 absent=2 skipped=0)`.
- `corpus/drift-pins.sh` + `corpus/drift-baseline.tsv` (15 files) + `corpus/drift-symbols.tsv` (20 claims — 20 since round 12 added the `cmd_run` L248 `exec op run` row, the masking premise) — byte/line/symbol drift; modes cross-checked against the census
- `corpus/transcript-scan.sh` — transcript-leak gate over the durable DB
- `corpus/op-ref-probe.sh` — the `op.env` contract gate: `refs` (`cmd_refs` awk) vs `op run --env-file` (what `cmd_run` execs) over generated plain-value fixtures, plus the dotenv edge classes, precedence, six error signatures (four `op`-side, two wrapper-side; four until the v2 probe) and the masking scope. `--selftest` proves 36 cases (comparator, POLICY-before-exec for a ref token / symlink / FIFO / premise break, SETUP, the hard-failure class, and the seven byte-comparator cases; 29 before the `--dotenv-bytes` arm); `--dotenv-bytes` is the op-only byte contract under `env -i` with scratch HOME/XDG (ledger `R21-01`, `knowledge/op-ref-consumption.md` §11); POLICY refuses any op-side fixture carrying a ref token, so the gate never resolves a reference. Exit 0/1/2. Data: the contract arrays in the script (there is no TSV — the fixtures are generated from the contract).
- `corpus/checklist-run.sh` — the credential-hygiene checklist as executable rows: `corpus/checklist.tsv` holds one row per SKILL.md checklist item (8 columns: `id class lead check expect_exit expect_last reason note`), each either `runnable` (a command + expected exit + expected last output line) or `by-hand` (a closed class + a unique ≥24-char reason). The `lead` ERE is a bijection over the 16 items, so an item with no row, a row with no item, a duplicated lead/item, a below-floor runnable ratio (`ceil(items/2)`) and a repeated by-hand reason are all defects. A `check` naming a denied surface (`op.env`, `op run|read|inject`, handler start/stop/run, `claim-ledger.sh`) is `POLICY`, exit 2 — the gate never reads `$CONFIG_DIR/op.env`, never resolves a reference and never starts the handler. `--list` prints the map, `--only ID` runs one row, `--selftest` proves 34 cases on scratch fixtures (ledger `R15-02`; this line said 28 until round 21). Round-15 baseline: `CHECKLIST_RUN: CLEAN (items=16 runnable=9 by_hand=7 failed=0)` + `CHECKLIST_RATIO: runnable=9/16 floor=8 by_hand=7`, exit 0. Data: `corpus/checklist.tsv` (16 rows).
- `corpus/scope-gate.sh` — ownership partition + shared-directory breadth. `corpus/adjacency.tsv` declares 5 owned prefixes (27 census rows), 4 shared groups (8 rows), 8 no-enumerate boundaries and 4 derived leaf breadth pins. Default verify fails closed on partition/citation/path defects and on missing/invalid/drifted breadth; `--map` prints all 35 row assignments; `--breadth` prints count-only per-leaf measurements (20/4, 105/2, 4/1, 53/1; total 182 children / 8 declared / 174 undeclared); `--selftest` proves 61 cases; `--falsify` catches 18/18 mutations. No child names or bytes are emitted.
- `corpus/claim-ledger.sh` — calibration gate: `verify` (91 revision stamps + 65 claim rows; since round 24 host/substrate rows are HOST-SKIPped by default and run only with `--allow-host-rows`), `citations` (durable evidence; `.ufo/` resolves lane-first; since round 25 a lone clone prints `FLEET-ABSENT` and ends `INCOMPLETE` exit 3, and `verify` reports `LAYOUT-INCOMPLETE`), `cells` (policy/host classification before recursion skips), `docs` and reviewed `stamp`. Exit 0/1/2 (3 = citations incomplete in a lone layout); `--selftest` declares 170 cases (121 at round 23; 151 at round 24; fourteen round-25 layout cases and one network-mode refusal). Only executed output verifies the count. Script expansion, attached external pattern-file operands and symlinked script ancestors are refused; the host-free fixture invocation is a closed vector, not a prefix.
- `corpus/self-counts.py` + `corpus/self-counts.tsv` — binds the current-tense numbers SKILL.md, PROVINCE.md, `corpus/README.md` and (round 27) reviewed `corpus/knowledge/*.md` lines state about this lane's own artifacts to their live source (row counts, a non-host ledger row's output, or a host row's committed pin; nothing host-reading is executed). Exit 0/1/2; `--selftest` proves 48 cases (round 25, ledger `R25-01`/`R25-02`).
- `corpus/release-clock.py` + `corpus/release-clocks.tsv` — every `on-release` row bound to a feed or rendered-quote clock; default is the pinned round-26 rearmed receipt, NOT live vendor truth. `--observe` writes a NEW receipt without rewriting the table and can fail on later receipt/profile drift. S040/S041 retain on-release cadence at named3.15.1 anchors; old3.15.0 anchors stay fired. Since round 27 a strict X.Y.Z observation below its own numeric anchor, any numeric anchor on the same feed, or (observing) the previous observation is `REGRESSED` (exit 1), never fired/CLEAN; equal-to-floor and unorderable anchors are declared limits. Since round 28 a non-canonical token is `NON-CANONICAL` and a `derived:` anchor its feed row's anchor cell does not name is `DERIVATION` (exit 1). Default/table/R25-04 migrate explicitly; original round25 receipt/code/tables remain in the historical frozen snapshot. Exit 0/1/2; `--selftest` proves 114 cases (ledger `R25-03`/`R25-04`). No installed-runtime or system-package management is claimed.
- `corpus/sources-census.sh` — source-registry gate (round 21): the SOURCES-CONTRACT-v1 census over `corpus/SOURCES.md` plus the citation handshake with `corpus/knowledge/` entries that carry `source:`. Read-only, no network; exit 0/1/2; `--selftest` proves 70 cases (40 at first landing; seven fail-open cases added after the round-21 post-landing review; twelve SC_FETCH cases added in round 23; eleven SC_INROW cases in round 24). Checks the citation chain and declared capture/classification records, never page content; entries without a column-1 `source:` line are outside every check.
- Helpers, not gates: `corpus/rendered-text-v1.py` — the one quote/page normalizer declaration (`digest`, `locate`, `--selftest` 22 cases, including two malformed-tag regex bounds); `corpus/row-identity.sh` — count plus digest over declared membership projections, not complete row semantics or assertion bodies.
- `corpus/closure-dispositions.py` — gate for typed outside-closure obligations and in-tree pointer resolution (R23-02); `--selftest` declares 14 isolated cases, pinned by R24-02. It checks obligation/pointer structure, not the substantive correctness of fixes or an independent verdict.

**Deliberate refusals:** vault-side structure (which vaults/items/fields exist) stays unmapped — mapping it would put ref paths in a durable artifact; `op` item-level reads stay unexercised; the CDP lease/profile ownership question is reported to the integrator, never adjudicated here.

## Core / Frontier / Adjacent (round 21)

Appended to the declaration above (`LEARNING.md` §Province is a frontier); the surfaces list stays the record of the host substrate.

- **Core — documented knowledge, not host surfaces:** 1Password machine-credential custody boundaries (`knowledge/onepassword-machine-credentials.md`), SOPS/age recipient vs data-key vs value rotation (`knowledge/sops-age-key-rotation.md`), Vault/OpenBao token, lease and KV clocks (`knowledge/vault-openbao-token-lease-lifecycle.md`). Each is vendor documentation opened 2026-10-19 (`corpus/SOURCES.md`); none is deployed or probed on this host.
- **Frontier — explored, not held:** OIDC workload-federation trust policy; secret-scanning detection vs verification; NIST key-management draft status (`corpus/README.md` §Frontier; leads in `corpus/SOURCES.md` §Leads (unopened)).
- **Adjacent — report, don't absorb:** chousa owns the research method (`SOURCES.md` restates neither method nor admission bar); chousa, kasegi and kumitate run their own secret-shaped tripwires over their outputs (hygiene filters, not vault ops); kama refuses to hold credentials for authenticated health checks and would route that need here through L0; kaidoku reads 1Password binaries statically and tsukuroi tracks the 1Password packages — kagi owns runtime auth and credential custody; kake holds the musketeer profile lease (contested, above). Sweep: round-21 connector over every `*-shokunin` `PROVINCE.md`/`SKILL.md`/corpus — no sibling claims SOPS, OpenBao/Vault, Credential Broker or workload-identity ground.

## Round-22 correction — active documented scope

The round-21 core list is historical admission evidence, not a claim that
its rejected merged rows passed their bar. The corrected active Broker
status/eligibility and product-bound token review lives in
`corpus/knowledge/feature-bound-credential-review.md`: Actions public
preview and custom-OIDC public beta are separate paths with Business
eligibility; OpenBao 2.7.x token evidence supplies no Vault-token or KV
retention parity. E1/E3 original bodies remain history with named errata.
No deployment or live account/vault was probed.

Local typed-review and revision-accounting fixtures do not absorb research
method, secret-scanner ownership, browser leases or authenticated endpoint
operations from siblings. Frontier and operator-owned terminal actions
remain unchanged. The source census checks citations, not vendor truth;
revision pins check bytes, not currentness of historical host facts.