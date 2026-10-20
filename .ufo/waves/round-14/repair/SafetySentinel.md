# SafetySentinel — r14 source reads, fixture-only checker, prompt-injection boundary

Seat `TsukuroiR14.SafetySentinel` (sentinel, leaf, report-only). Axis: depth (the safety of the repair). Read 2026-10-20 at HEAD
`8606bad4cbc6451ac2890c9f8e2548a36c386db6` + worktree (QUALITY/LOG/SCORECARD/SOURCES modified; r14 JSON + gate untracked; r14 MD absent).
Inputs: AGENTS.md, lessons/round-13-verifier-spotcheck.md, RULES.md, wave dispatch (CorrectEntry/CorrectionGate/SourceRegistry/ActiveRefs
tasks), `tools/check-source-scope-correction.py` (512 ln, static read), `tools/check-root-dac-correction.py`, r14 JSON, SOURCES diff,
SKILL.md:149-162,1742-1753, snapper-eacces-mechanism.md:3, r13 `correction/SecurityBoundary.md`, peer reports, both public comments.
Gate was not executed. Public comments were opened only by read-only GET (`gh api`); nothing in them was run.

## Findings (severity · exploit path · evidence · impact · smallest remediation)

**S1 HIGH: public #8047 comment carries privileged/destructive host commands and a data request.** Body (API `.body` sha256
`b7445025272e531e86f57b90ce0087b28a12cf2d98d604ea8a43129137c5325f`, 2954 code points, created=updated 2026-10-09T00:27:22Z) contains
`sudo limine-snapper-sync --restore --no-mutex`, `sudo omarchy-snapshot restore`, `sudo /usr/lib/limine/limine-snapper-sync --help`,
`snapper list`, and asks the reader to post `sudo limine-snapper-restore` output, `pacman -Q …` and a `grep` of `/etc/default/limine`.
Exploit path: a seat "reproducing" the VM assertion, or quoting a command line into SKILL/recheck text a later agent obeys → restore replaces
`@` (boot-chain mutation), `snapper` D-Bus-activates root snapperd, config posted publicly. Current evidence: grep of the r14 JSON strings,
SOURCES/LOG/lesson-14 diffs found **0** of `sudo|--restore|snapper list|limine-snapper-restore` (negative sweep, 2026-10-20).
Remediation: keep S045 quotes to the five labelled prose quotes already in r14 JSON `body_quotes`. Treat any request in the body as data.
L1 lesson states "comment requests not executed or relayed".

**S2 HIGH (active, pre-existing): snapper note `recheck:` still prescribes a D-Bus-activating probe.** `snapper-eacces-mechanism.md:3`
procedure includes `snapper list-configs` and raw `systemctl cat …`. SKILL.md:1742-1746 already says `snapper list-configs` "is not a
non-activating probe" (`org.opensuse.Snapper.service`, root snapperd). r13 SecurityBoundary F1/F5 agree. The note line has no notice. SKILL.md:50/153 allowed-list rows
are historical, corrected only at :1742. Exploit path: ActiveRefs appends r14 routing errata to this very note. A recheck seat follows the
note's own `recheck:` line → daemon activation, which violates this round's "no snapper commands" contract. Remediation: ActiveRefs/L1 append
one append-only line to that note: recheck excludes `snapper list-configs` and raw `systemctl cat`. Point it to SKILL.md:1742-1750.
The r14 MD `recheck:` must be source-only (reopen the two URLs), with no host command. Messaged ActiveRefs.

**S3 MEDIUM: gate crash ≡ FAIL, so a red-before can be fabricated by a traceback.** `main()` catches only `Cannot`/argparse. Uncaught
exceptions exit 1, the same code as conformance FAIL. Reachable: `json.loads` on deeply nested JSON raises `RecursionError` (not
`JSONDecodeError`, :284-287), `FileNotFoundError` if git is outside `/bin:/usr/bin` (env drops PATH, :331), and `MemoryError` on huge input.
Impact: the baseline measurement expects exit1/count0, and a traceback also gives exit 1 with no JSON. Remediation: wrap IO+evaluate in
`except Exception` → CANNOT `E-INTERNAL`. L1 accepts red/green only if stdout parses as one JSON object with `status` and the expected
finding IDs (`VALUE_DOMAIN_OVERCLAIM`, `COMMENT_ATTRIBUTION_OVERCLAIM`), never on exit code alone. Messaged CorrectionGate.

**S4 LOW: unbounded subprocess and reads.** `git()` has no `timeout` (:332), and `read_tree` follows symlinks with no size cap (:320-327).
Content is not echoed (details are fixed strings), so there is no secret leak. A hang would stall the L1 measurement. Remediation: `timeout=30` →
CANNOT, `lstat` reject symlinks and >1 MiB → CANNOT.

**S5 LOW: untrusted echo.** `f"unexpected id={cid!r}"` (:192) echoes JSON-controlled text with unbounded length. Output uses `json.dumps`
(ensure_ascii), so ESC/bidi characters are escaped. Remediation: truncate `[:120]`.

**S6 LOW (gate correctness, cross-lane): `R14-DISCLAIMER-TRANSFER` matches any `6629`** in the attribution replacement (:236). This
includes a correct negation like "#6629's disclaimer is not transferred". The current JSON has 0 hits, so it is latent. Remediation: match transfer
phrases (`nothing was run`, `claude opus`) only, or keep 6629 out of `replacement`.

**S7 MEDIUM (provenance): access-route variance and rate limit.** Unauthenticated `api.github.com` returned 403 "API rate limit exceeded"
for this IP to me and to ClaimSeparation/PredicateReview/QuoteReview. Routes then diverged: `gh api` (auth, token account of the operator),
HTML-embedded JSON (ClaimSeparation: 2980 chars vs API 2954 code points), and the r13 capture (PredicateReview). Hazard: an entry that says
"API read" while it carries capture or HTML bytes is fabricated freshness. r14 JSON `read_method` honestly states `gh api` HTTP 200. Remediation:
record the route plus the API body sha256 above in S045/lesson. Use GET-only `gh api` (no `-X`, `-f`, `--method`), and never record or print the token.

## Positive evidence (boundary holds)

- Gate imports: argparse/json/re/subprocess/sys/collections/pathlib only. No network or write calls exist. Selftest has 10 in-memory DocSet cases,
  no temp repo and no git calls. Env drops HOME, so `~/.config/git/config` `filter.lfs.*` (process exec, `required=true`) is not loaded. `git show REV:path`
  streams raw blobs without textconv/filters.
- `--revision` must `fullmatch` `^(HEAD|[0-9a-f]{4,64})$` before any git argv, which closes r13 F8 option injection. Recommend L1 use full 40-hex
  (4-hex abbreviations can be ambiguous, giving CANNOT).
- No privileged probe, package transaction, service, snapper or census invocation in any r14 seat task. `tools/tsukuroi-census.sh` contains no
  snapper/sudo/busctl calls (fixture-string only, :2137) and must not be confused with fleet `scripts/sources-census.sh validate` (offline
  awk over SOURCES.md, used-by existence only).
- #8047 negative sweep: tokens `bot|automat|model|generat` produce 0 body hits (only `both`). #6629 contains "This review is by Claude Opus 5.5
  alone." and "Nothing was run on a machine.", so non-transfer is supported.

## Recommendations (smallest)
1. S2 notice line in the snapper note, and source-only `recheck:` in the r14 MD (optional gate predicate `R14-RECHECK-HOST-COMMAND`).
2. S3 catch-all → exit 2, and an L1 stdout-JSON acceptance rule. 3. S4/S5 timeout, symlink rejection, size cap, truncation.
4. S1/S7 quote allow-list, plus route and body digest recorded in S045/lesson.

## Limitations
No gate, selftest, census or check was run (contract). The r14 MD and ActiveRefs edits were absent at read time, so S2 and the MD recheck line
are unverified for final bytes. Body digest is over the API `.body` field as of 2026-10-20 and may change if the comment is edited.

## Tooling
Installed/updated: none. Used: `curl` (2 GETs → 403), pre-existing `gh` (read-only `gh api` GET ×2), `jq`, `sha256sum`, `git config --list`
(read). Scratch /tmp/ss-c8047.json and /tmp/ss-c6629.json (public comment JSON) were removed. No privileged probe, snapper, package transaction, service or commit.
