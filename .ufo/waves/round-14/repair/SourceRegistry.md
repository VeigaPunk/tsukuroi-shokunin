# SourceRegistry — round 14 (TsukuroiR14.SourceRegistry, depth)

## Scope and writes
- Wrote only `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md`:
  appended rows S044/S045 plus one append-only Search-log paragraph. No historical
  line, row, lesson or search-log paragraph was edited; S042/S043 stay visible history
  and S045 carries `supersedes S042`.
- Registry-only authority change: no host cause, capability, maintainer acceptance,
  source-truth enforcement or gate result is claimed.

## Opened sources (2026-10-20, ~05:58–06:04Z)
| Row | Opened source | Exact located quote | Words |
|---|---|---|---|
| S044 | https://man.archlinux.org/man/systemd.exec.5 § ProtectSystem= (SANDBOXING), footer systemd 262.1, native HTML | `Takes a boolean argument or the special values "full" or "strict".` | 11 |
| S045 | https://api.github.com/repos/omacom/omarchy/issues/comments/6071740243, comment 6071740243, authenticated `gh api` HTTP 200 | `I tried this on a stock Omarchy worker VM` | 9 |
| S045 | same body, full first clause | `I tried this on a stock Omarchy worker VM and could not reproduce the central claim` | 16 |
| S045 | same body, second opinion | `Codex Medium reviewed the same evidence and upstream files and reached the same conclusion.` | 14 |
| S045 | same body, independence caveat | `It may have seen this analysis first, so its agreement is not guaranteed to be independent.` | 16 |
| S045 | same body, #6634 referent | `which is waiting on the maintainer to decide whether snapshot boots should keep the overlay.` | 15 |
| S045 | same body, #8047 close (reporter addressee) | `This now waits on your answer.` | 6 |
| S045 contrast | #6629 comment only, not transferred | `Nothing was run on a machine.` | 6 |

- S044 also states `This setting cannot ensure protection in all cases.` (8 words): a
  protection limitation, not a value-domain statement.
- The #8047 body has zero case-insensitive hits for `model`, `generated`, `triage`,
  `automated` (only `Codex`), so S042's “self-described model-generated automated
  triage” is unsupported.

## Registry result
- 43 → 45 rows: A37/B1/C7; mined32/queued5/rejected8. S044 docs/A/mined, on-release,
  used-by `corpus/knowledge/source-scope-correction-r14.md`; its scope differs from
  S028/S041, so no E04 and one new W04 is expected (6 total). S045 community/C/rejected,
  90d, same used-by; its API URL differs from S042's issue URL, so no new W04. The E11
  target is now on disk.
- S041 remains current and is not superseded; S044 pins only the documented value
  domain and adds no host observation or new semantic surface.

## Supersession and bounded screen
- The new log paragraph supersedes the round-13 paragraph's two claims without editing
  its bytes: “the text self-describes a model-generated review” holds only for #6629;
  the unscoped “defers the decision to a maintainer” conflates #6634's remount question
  with #8047, whose close addresses the reporter. The “nothing ran on a machine”
  transfer is #6629-only.
- S045 rejects host-cause use on absent host-specific proof and the still-open thread,
  not on an authority self-disclaimer by the body; account fields are identity only.
- Screen: 2 sources identified/screened; 1 support (S044), 1 reject for cause (S045).

## Cross-check with the landed pair (read-only)
- JSON corrections cite S044 with the exact 11-word quote and S045 with the exact
  16-word quote; field/body separation matches this registry.
- Its R14-VALUE-DOMAIN replacement's “non-exhaustive set” sentence is not source text.
  Recommend tagging mechanism-list openness as lane scope/inference; keep “documents
  no further values” and do not assert a “closed domain” as a source fact.
- The pair's QUALITY #7 records S044/S045 absent at 06:00:33Z; they are now present.

## Limitations
- Unauthenticated `api.github.com` returned HTTP 403 (core rate limit, reset
  06:12:56Z). The authenticated `gh` 2.102.0 read-only fetch returned HTTP 200, and the
  HTML anchor carried the same sentence. 403 is an access limit, not source absence.
- `systemd.exec.5` is on-release; cite § and footer, not rendered lines.
- No census, validate, gate, selftest, build or formatter was run; counts are manual
  file reads. Word counts are whitespace-normalized; the #6634 quote is 15 words with
  “which is” and 13 starting at “waiting”.
- The correction pair is another seat's artifact, inspected read-only.

## Tooling
- Installed/updated: none. Used existing `curl`, `python3` and `gh` 2.102.0
  (authenticated read-only). No privileged probe, snapper call, package transaction or
  service action; no source-supplied command was executed.
