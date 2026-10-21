# FxC2Skill — falsification of exact `skill://godspeed` authority

Target: `.ufo/waves/round-22/candidate/tools/check-seat-bindings.py`. The assigned SHA-256 is recorded in the receipt below. These bytes were not re-hashed: the seat is NO-EXEC, so no hashing tool was run.

Attack: the exact `skill://godspeed` is allowed. Other skills, selectors and spellings must not get blanket authority.

## Verdict

The exact-spelling authority on the `path` field holds. I found no source-visible spelling, selector or other-skill counterexample that the auditor classifies as clean.

There are two residual issues:
- **R1 (fixable defect):** arguments other than `path` are never audited.
- **R2 (fixture gap):** the selftest has no negative skill fixtures, so a mutation of the binding-side guard would survive it.

## Why exact spelling holds (two independent layers)

1. **Request layer.** `requested_path` short-circuits only on the literal `value == 'skill://godspeed'`, and it does this before any selector stripping. Every other spelling falls through to `local()`, which requires the `LANE + '/'` prefix, so those spellings get `SCOPE-PATH-DENIED`. Spellings that fall through this way include:
   - `skill://godspeed:raw` and `skill://godspeed:1-5`, after the selector regex strips them back to `skill://godspeed`
   - `skill://godspeed/SKILL.md` and `skill://godspeed/`
   - `skill://other` and `skill:///godspeed`
   - `SKILL://godspeed` and `skill://GODSPEED`
   - zero-width or fullwidth variants
2. **Membership layer.** Even the exact URI is allowed only if it is literally in that seat's `read_paths` (`classify`, the `path not in binding[...]` check). If the binding omits it, an exact skill read is `SCOPE-PATH-DENIED`. A write of `skill://godspeed` is checked against `write_paths`, which binding validation forbids from containing it (`field == 'read_paths' and p == 'skill://godspeed'`), so the write is denied.
3. **grep and glob splitting.** `grep` and `glob` split on `;`, and each piece is checked through the same two layers. For example, `skill://godspeed;` produces an empty piece, which is denied.

Expected fixture verdicts (derived from the source; none were observed, because nothing was run):

| Request | Expected exit | Expected findings |
|---|---|---|
| `read skill://godspeed`, skill bound | 0 | none |
| `read skill://godspeed:raw` | 1 | `SCOPE-PATH-DENIED` |
| `read skill://other` | 1 | `SCOPE-PATH-DENIED` |
| `read skill://godspeed/x` | 1 | `SCOPE-PATH-DENIED` |
| `read skill://godspeed`, skill not bound | 1 | `SCOPE-PATH-DENIED` |
| `write skill://godspeed` | 1 | `SCOPE-PATH-DENIED` |

## R1 — non-`path` arguments are unaudited (fixable defect)

**Counterexample (source-visible):** `glob {"path": "skill://godspeed", "pattern": "/home/vgpnk/.omp/agent/skills/*/SKILL.md"}`. The same applies to a `grep` request with a `glob` argument, or any extra path-like key. `classify` reads only `args.get('path')`. Every other key is ignored, and nothing marks unknown keys as malformed.

- **Expected fixture verdict:** exit 0, PASS, no findings.
- **Observed runtime:** none; nothing was executed.
- **[INFERENCE]** I have not confirmed whether the host's glob or grep resolves such a pattern outside the bound path. If it does, a request whose only declared path is the exact skill URI could enumerate other skills or lane-external files while auditing clean.

This contradicts the UNKNOWN decision ("malformed arguments → DENY, fail closed") and weakens the claim that LOCAL_READ is only "literal bound source paths and approved skill URI".

- **Impacted axes:** operability (C2: `request_audit_mode` correctness) and depth (C1: the LOCAL_READ and UNKNOWN decisions).
- **Smallest safe correction:** in `classify`, give each tool an allowed key set and fail closed (`SCOPE-SCHEMA`) on any other key:
  - `read`: `{path, i}`
  - `write`: `{path, content, i}`
  - `grep`: `{pattern, path, i}`, with `pattern` treated only as a regex
  - `glob`: deny a non-empty `pattern` that contains `/` or `..`, or treat `pattern` as a path that must also be bound

  Add one negative fixture per tool.

## R2 — no negative skill fixtures in `selftest` (fixture gap, not a current bypass)

The only skill case is the positive `skill` case. I traced these mutations by reading the source; none were run.

- **M1:** replace `value == 'skill://godspeed'` with `value.startswith('skill://')` in `requested_path`. It survives the selftest, but the membership layer masks it, so behaviour is unchanged.
- **M2:** delete `field == 'read_paths' and` from the binding validation. It survives the selftest. A binding with `write_paths: ["skill://godspeed"]` is then accepted, and `write skill://godspeed` audits clean (exit 0). That is a real regression the selftest would not catch.
- **M3:** M1 plus changing the binding check to `p.startswith('skill://')`. It survives the selftest. A binding listing `skill://other` and a read of `skill://other` then audit clean.

**Smallest safe correction:** add fixtures that each expect exit 1 or 2 with the named finding:
- the skill URI in `write_paths` must fail binding validation with `SCOPE-SCHEMA`
- `skill://other` in `read_paths` must fail binding validation with `SCOPE-SCHEMA`
- `read skill://godspeed:raw` must give `SCOPE-PATH-DENIED`
- `read skill://godspeed/x` must give `SCOPE-PATH-DENIED`
- a skill read with an unbound skill must give `SCOPE-PATH-DENIED`
- `write skill://godspeed` must give `SCOPE-PATH-DENIED`

## Tradeoff, not defect

`grep` and `glob` on the exact skill URI are allowed. That matches the LOCAL_READ decision ("read/grep/glob ... approved skill URI"), so it is not a finding.

No runtime prevention is claimed. The module docstring and `SCOPE` both state post-hoc detection only, which is consistent with the host-tool-boundary source (`native_per_seat_allowlist: false`).

## Tooling

No installs or updates. Only the declared read paths were read, and only this report path was written.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2skill
Scope: executed=none
Lane bounds: leaf member — no subagent dispatch.
