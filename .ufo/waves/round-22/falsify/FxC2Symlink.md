# FxC2Symlink — lexical spelling vs symlink effect

Target: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-22/candidate/tools/check-seat-bindings.py` (241 lines). The digest below is the one supplied by dispatch; it was not recomputed in this seat (NO-EXEC). Source was read at the declared path and via `grep` restricted to the declared read paths.

Verdict: **not falsified within its declared scope; falsified if its PASS is cited as containment.** Every path decision is a literal string decision over recorded request text. A declared and recorded path that is lexically under the lane can nonetheless resolve outside it through a symlinked component, and the checker still emits `PASS`, `violations: 0`. The file never claims OS containment, so the defect is a downstream-citation defect, not a bug in the stated predicate; the only source-level weakness is naming/salience (`local()`, `SCOPE-PATH-DENIED`, `PASS`) that invites the stronger reading.

## Observed facts (source)

1. `local()` (lines 33–36) is a pure string predicate: `startswith(LANE + '/')`, no backslash, no `Cc/Cf/Cs/Zl/Zp`, no `*?[];:`, and no empty/`.`/`..` segment. It performs no filesystem call.
2. The only canonicalization in the file is `ROOT = Path(__file__).resolve().parents[1]` (line 15), used for Git reads. `LANE` (line 16) is a literal, unresolved constant, and nothing compares the resolved `ROOT` with `LANE`.
3. `grep` for `symlink|realpath|resolve|islink|lstat|readlink|stat(|follow_symlinks|normpath|abspath` returns only lines 15 and 17: no resolution or link inspection of audited paths exists. The same grep over `check-review-snapshots.py` returns only line 17, its own `ROOT` — the sibling checker is equally lexical.
4. `classify()` (lines 58–92) never opens the requested path. For `read` it strips a selector suffix (`requested_path`, lines 43–56), then applies exact membership against `binding['read_paths']`; for `write` it applies exact membership against `binding['write_paths']` (lines 90–91).
5. Binding validation (lines 109–115) itself requires every `read_paths`/`write_paths` entry to satisfy `local()` (or be the literal `skill://godspeed`). Declared bindings, therefore, can name symlinked spellings.
6. `evaluate()` maps an empty finding list to exit 0 / `PASS` with `request_audit_mode: 1` and `violations: 0` (lines 149–152); the `SCOPE` constant (line 17) says "Recorded request spellings only; not runtime prevention, symlink/effect proof, reading proof or universal trace completeness" and is carried in the payload.
7. The selftest's path negatives (lines 173–177) attack prefix-extension, child paths, `..`, `.`, glob text, and `;` — no fixture models a symlinked component or leaf. The expected verdict for such a fixture is therefore unexercised by the selftest.
8. Corroborating declared sources: `seat-boundary-r22.md` line 22 disclaims "OS sandbox ... proof of actual reading, or proof of request effects"; `preregister.json` limits deny "proof of ... request effects"; the corpus JSON makes the same disclaimer. No declared source claims containment. No LSP device is exposed in this seat's tool inventory and the seat declares no commands, so this is text/grep evidence only, not semantic proof.

## Counterexample (fixture; source-only)

Premise requiring no execution but one unverified filesystem fact: `<LANE>/linkdir` is a directory symlink to `/tmp/outside` and `<LANE>/report` is a directory symlink (or dangling leaf link) to `/tmp/elsewhere`. Neither existence nor type is observable with the declared tools; the seat cannot `lstat`/`readlink` under NO-EXEC.

Manifest:

```json
{"schema":"tsukuroi-seat-bindings-v1","seats":[{"name":"A","root":"<LANE>","read_paths":["<LANE>/linkdir/secret.txt"],"write_paths":["<LANE>/report/out.md"],"commands":[],"fetches":[]}]}
```

Events:

```json
{"schema":"tsukuroi-seat-events-v1","seats":[{"name":"A","agent":"agent-A","complete":true,"events":[{"tool":"read","args":{"path":"<LANE>/linkdir/secret.txt"}},{"tool":"write","args":{"path":"<LANE>/report/out.md"}}]}]}
```

Static walkthrough: both bindings pass `local()`; the read event passes selector stripping and exact membership; the write event passes exact membership; findings are empty; `incomplete_seats` is 0, so the code is 0. **Expected fixture verdict: exit 0, `PASS`, `requests_total: 2`, `violations: 0`, no findings.** Under ordinary POSIX semantics the same two spellings read `/tmp/outside/secret.txt` and create or overwrite `/tmp/elsewhere/out.md`, outside the lane. The dangling-link case is the sharpest: `write` to a dangling link creates the target outside, and nothing in the checker can see it.

**Observed runtime: none.** This seat executed no fixture, no tool selftest, and no audit; `executed=none` below is literal.

The same shape applies to this seat's own declared write path, `<LANE>/.ufo/waves/round-22/falsify/FxC2Symlink.md`: it passes `local()`, and if any ancestor or the leaf is a symlink the write lands outside while the audit stays clean. Whether any such component is actually a link is unresolved here.

The `..` ban is orthographic, not semantic: `linkdir` yields the same escape without the `..` token, and `requested_path`/`local()` cannot distinguish the two. Note the exact-membership requirement limits the issue to declared spellings: the seat cannot request an arbitrary symlinked path, but a binding authored with one — or a path that becomes one after declaration — is audited as compliant.

## Bounded reason it holds as scoped

- The domain of the predicate is recorded strings. On strings, `local()` is sound and complete for its own definition; a symlink does not change the string, so the checker misses nothing *relative to its declared question* ("is this request spelling in the declared set?").
- The audit never observes the agent's syscalls or inode identity. Recorded requests are metadata. Even audit-time `realpath`/`lstat` would establish only current resolution, not dispatch-time resolution (TOCTOU: the manifest is read from the audited revision while the referenced filesystem is mutable), and would not detect bind mounts or mount-namespace differences. So canonicalization cannot upgrade this tool to containment; the limitation is structural, not a missing call.
- The claim that survives falsification: every recorded request path is a literal member of the declared spelling set. The claim that fails: an allowed record proves the operation stayed physically inside the host directory.

## Residual risk and wording (no edit made)

`local()` and `SCOPE-PATH-DENIED` suggest filesystem locality, while `PASS`/`violations: 0` are the salient payload fields; the `scope` string is the only disclaimer and is easy to drop when quoting results. Any citation of C2 must keep the spelling-only qualifier and must not render a clean audit as an outside-access finding of zero. If write effects ever need checking, an audit-time `realpath` plus per-component `lstat`, compared against the resolved lane, would be the minimum additional test — still post-hoc, still blind to bind mounts, and requiring its own negative fixtures (symlinked directory, symlinked leaf, link to outside, link chain, dangling link). C2 as registered does not ask for that, so no change is proposed.

## Remaining unknowns

- Actual symlink topology under the lane (including the declared `.ufo`/`waves`/`round-22`/`falsify` path): not observable without `stat`/`readlink`, which NO-EXEC forbids and no declared source states.
- Target digest not independently recomputed; accepted from dispatch.
- Host `read`/`write` symlink-following behavior not observed; the fixture verdict is derived statically from `local()`, `classify()`, and `evaluate()`.

Confidence: high on the source facts and the PASS verdict derivation; high that the declared documents disclaim containment; unresolved on the host filesystem premise and on any claim that the lane actually contains a link.

Reviewed-SHA256: c45c93e5e3dcbb0029a58242848d0311c1b281eb8a210afddefb64b4c0aa69c4
Predicate: r22-fxc2symlink
Scope: executed=none
