2026-11-03T21:50:08Z
# R2Reviewer — C2 false-positive attack (ANCHOR-LIVE-OBJECT-UNRESOLVED)

Lane base 5abc31d9, declaration frozen 071a55c9. Question: does the new finding fire on honest records?

## Step 1 — all 10 outbound records resolve at the honest base

Probe: register read at base, then per record
`$ git -C /home/vgpnk/Projects/shokunin/<sibling>-shokunin cat-file -e <sibling_commit>^{commit}`

Register source: `$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 5abc31d9:corpus/knowledge/adjacency-anchors-r19.json` → rc 0, `outbound_total 10`.

| record | sibling | sibling_path | sibling_commit | dir | cat-file rc | stderr |
|---|---|---|---|---|---|---|
| OUT-001 | mori | PROVINCE.md | 91940fa339e38006f8db5bd7d78bb6f037f4d016 | exists | 0 | (empty) |
| OUT-002 | kama | PROVINCE.md | e75cf680b53484a61709ee1b2787d8dbc6419f74 | exists | 0 | (empty) |
| OUT-003 | kagi | PROVINCE.md | c2cab35bc92e57e39e5489bac3386db078345b3f | exists | 0 | (empty) |
| OUT-004 | mado | PROVINCE.md | a4046a8216080d4004de3f268c62cf142095ac07 | exists | 0 | (empty) |
| OUT-005 | mori | PROVINCE.md | 91940fa339e38006f8db5bd7d78bb6f037f4d016 | exists | 0 | (empty) |
| OUT-006 | kumitate | PROVINCE.md | 1770305fae20826b39905a8251ddeca6b4957ac4 | exists | 0 | (empty) |
| OUT-007 | mori | PROVINCE.md | 91940fa339e38006f8db5bd7d78bb6f037f4d016 | exists | 0 | (empty) |
| OUT-008 | kaidoku | PROVINCE.md | d1d981d2cc041dda4656c5b01d2c8445d8d17124 | exists | 0 | (empty) |
| OUT-009 | revenger | PROVINCE.md | cf02419276e5dd8aafb6fe09d4e9aaa6bcb78c97 | exists | 0 | (empty) |
| OUT-010 | tameshi | PROVINCE.md | 01d586ddbc5fcd78659557c4e93a6ee8517b87d1 | exists | 0 | (empty) |

HONEST_RESOLVING = 10 of 10, rc 0 each. No FALSE-POSITIVE-RISK named on the honest base.

## Step 2 — outbound records with sibling_path under .ufo/

0 of 10 outbound records have a sibling_path beginning `.ufo/` (all are `PROVINCE.md`). The historical-scope outbound subset is empty; the check is vacuously satisfied and the 10 resolving commits above cover the whole outbound set. (`.ufo/` sibling_paths occur only in inbound records, which `_live_object_hash` never touches — it is called from the outbound loop only.)

## Step 3 — shallow-clone limit (kama)

```
$ git clone --depth 1 --no-local file:///home/vgpnk/Projects/shokunin/kama-shokunin /fast/scratch/hyaku/tsukuroi-r67/R2Reviewer/shallow   # rc 0
$ git -C /fast/scratch/hyaku/tsukuroi-r67/R2Reviewer/shallow cat-file -e e75cf680b53484a61709ee1b2787d8dbc6419f74^{commit}
# rc 128: fatal: Not a valid object name e75cf680b53484a61709ee1b2787d8dbc6419f74^{commit}
$ git -C .../shallow rev-parse HEAD    # 6035e952c2521999e192d6f236331f265ac98392, rc 0
$ git -C .../shallow rev-list --all --count  # 1, rc 0 ; .git/shallow exists
```

SHALLOW_TRIPS = yes: in a depth-1 clone the honest pinned round-19 commit does not resolve, so the new finding would fire on an honest record there. This is an environment/checkout limit (a truncated local clone lacks the pinned history), not a fleet defect: the canonical fleet checkouts are full clones and resolve 10/10 (Step 1). The gate should treat `live_object_checked < outbound_total` on partial clones as an environment caveat, not silence — the finding firing is correct behavior for a checkout that cannot verify the pin.

## Step 4 — absent-sibling path

Base `_live_object_hash` (git show 5abc31d9:tools/check-adjacency-anchors.py, rc 0):

```python
repo = Path(root) / f"{sibling}-shokunin"
try:
    proc = subprocess.run(["git", "--no-pager", "-C", str(repo), "show", f"{commit}:{path}"], ...)
except (subprocess.TimeoutExpired, OSError):
    return None
if proc.returncode:
    return None
return hashlib.sha256(proc.stdout).hexdigest()
```

An absent sibling directory makes `git -C <absent>` exit 128 → `proc.returncode` nonzero → return None. Base outbound block: `live_digest = _live_object_hash(...)`; `if live_digest is not None: counts["live_object_checked"] += 1; ...`. Confirmed: absent directory returns None without any finding, and an unresolvable commit is indistinguishable from it at base (both rc≠0 on the same `git show`) — the C2 predicate "silently uncounts" holds at base.

Draft `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-67/drafts/check-adjacency-anchors.r67.py`: ABSENT at check (`ls -A .../round-67/drafts/` → empty, rc 0, 2026-11-03T21:50:08Z). Contract-level analysis per E2Gate: the finding must key on sibling-directory existence — fire only when `<siblings_root>/<sibling>-shokunin` exists and the commit does not resolve. That keying is the correct complement of base behavior (base already yields no finding for absent dirs, so absent must stay finding-free) and it cannot fire on the honest base of Step 1. Residual design note: resolution should be probed with the same `git show <commit>:<path>` the live check uses (dir-exists ∧ show-fails), not only `cat-file -e <commit>^{commit}`; a resolvable commit with a missing path would otherwise remain silently uncounted (under-firing, not a false positive).

## Verdict

VERDICT = SURVIVES. The contracted rule (fires only when the sibling directory exists and its commit does not resolve) has no false positive on the honest base: 10/10 outbound records resolve in the canonical environment, absent siblings stay finding-free, and the only trip observed is the self-inflicted shallow-clone environment limit.
