# ConnSourceLimits — Bounded Proposal: Hermetic Object Disambiguation Preserving Commit-ish Peeling

**Seat:** `TsukuroiR19Recovery.ConnSourceLimits-2`  
**Role:** UFO-FSD Connector  
**Round:** Tsukuroi round 20, attempt 1 (`TsukuroiR20`)  
**Baseline:** `0cbc34dd6b20896085a8fb07943e3ea4027d8472`  
**Mode:** NO-EXEC (read/grep/glob only; no shell/eval, subprocesses, imports, gates, selftests, or host probes)

---

## 1. Declared Axes

The round's declared axes and contract metrics (per `.ufo/waves/round-20/preregister.json:4-29` and canonical assignment):

- **C1 Adjacency** (ordinal 8, lowest/tied-lowest, ordinal delta 0):
  Metric: `ownership_corrections` (before: 0, after: 1).
  Evaluator: `python3 tools/check-adjacency-anchors.py --revision <REV> --ownership-corrections`.
  Scope: Explicit sibling-declaration wording for OUT-009 at retained pinned scope, no integrator arbitration or write authority.
- **C2 Operability** (ordinal 9, ordinal delta 0):
  Metric: `object_selector_tools` (before: 0, after: 9).
  Evaluator: `python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors`.
  Scope: Original-nine consumer continuity under object-only hexadecimal selector tests; discovered tools separate. Read-only systemctl exec-log classifier supporting repair.
- **C3 Calibration** (ordinal 9, ordinal delta 0):
  Metric: `audit_live_map_errors` (before: 1, after: 0).
  Evaluator: `python3 tools/check-registry-coverage.py --revision <REV> --audit-live-map`.
  Scope: Highest operative boot-chain-audit live map is `0 CONSISTENT/observation`, `2 UNKNOWN/could-not-evaluate`; code 1 is selftest failure only, never live DEGRADED. Append named R19 false-erratum and non-prefix disclosure.

All ordinal deltas remain strictly 0; genuine finite improvements within claims, with no certificates of host or boot safety.

---

## 2. Evidence: Git Object/Ref Grounding vs Known Binder Alias Residual

### A. Grounded Upstream Git Documentation
1. **Source S077 (`git-rev-parse` 2.56.0, `OPTIONS`):**
   `--disambiguate=<prefix>`: *"Show every object whose name begins with the given prefix. The <prefix> must be at least 4 hexadecimal digits long to avoid listing each and every object in the repository by mistake."*
   - *Evidentiary significance:* `--disambiguate` queries the repository object database directly (loose and packed objects). It does not search or resolve symbolic refnames in `refs/`.
2. **`gitrevisions` 2.56.0 (`SPECIFYING REVISIONS`):**
   - `<sha1>`: *"The full SHA-1 object name (40-byte hexadecimal string), or a leading substring that is unique within the repository."*
   - `<refname>`: *"A symbolic ref name... When ambiguous, a <refname> is disambiguated by taking the first match in the following rules: 1. $GIT_DIR/<refname>... 2. refs/<refname>... 3. refs/tags/<refname>... 4. refs/heads/<refname>... 5. refs/remotes/<refname>... 6. refs/remotes/<refname>/HEAD."*
   - *Evidentiary significance:* In general revision parsing, Git checks ref directories before treating a string as a raw object hash. When a ref exists whose name matches an abbreviated or full hex string, Git resolves the ref, emitting an ambiguity warning to stderr.
3. **Commit-ish Peeling Syntax (`git-rev-parse` 2.56.0, `SPECIFYING REVISIONS`):**
   `$VAR^{commit}`: *"will make sure $VAR names an existing object that is a commit-ish (i.e. a commit, or an annotated tag that points at a commit)."*
   - Peeling dereferences an annotated tag object (object type `tag`) to the target commit object it references.
   - Non-commit objects (such as `blob` or `tree`) cannot peel to `^{commit}`; attempting to peel them causes `git rev-parse` to return non-zero exit status.

### B. The Known Binder Alias Residual in Baseline
In baseline `tools/_revision.py:97-109,134-154`:
```python
def _commit(repo, ref):
    proc = _git(repo, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{ref}^{{commit}}")
    if proc.returncode == 0:
        return proc.stdout.decode("ascii", "replace").strip()
    ...
```
When `bind(repo, revision, branch)` is called:
`revision` is verified against `re.compile(r"^[0-9a-fA-F]{7,64}$")`, then passed directly to `_commit(repo, revision)`. Because `revision` is passed directly as `f"{ref}^{{commit}}"`, Git applies refname precedence:
- **Ghost Hex Ref Vulnerability:** If a ref exists named with hexadecimal characters (e.g., `refs/heads/000000000000` or `refs/tags/000000000000`) pointing to a landed commit, `_commit` resolves the ref target, accepting a hash string for which no object exists in the object store.
- **Shadow Prefix Ref Vulnerability:** If an object exists with prefix `deadbeef01` pointing to commit A, but a branch `refs/heads/deadbeef01` exists pointing to decoy commit B, `_commit` resolves commit B instead of commit A. If B is unlanded, it causes `E-REVISION-NOT-LANDED`; if B is landed, it binds the wrong commit.

### C. Seeded Implementation and Proposal Cache Observations
In `/tmp/tsukuroi-r20-binder-20261021/tools/_revision.py:112-126`, `_object_commit` was introduced:
```python
def _object_commit(repo, revision):
    proc = _git(repo, "rev-parse", f"--disambiguate={revision.lower()}")
    if proc.returncode:
        raise RevisionError(E_GIT, "revision", f"object lookup failed: {_err(proc)}")
    objects = proc.stdout.decode("ascii", "replace").splitlines()
    if len(objects) != 1:
        return None
    return _commit(repo, objects[0])
```
Cross-referencing this seeded implementation against round-20 peer proposals (`BindAmbiguous.md`, `SrcGitRevisions.md`, `spec.json`, and `preregister.json`):
1. `_object_commit` correctly converts uppercase hex selectors via `revision.lower()`.
2. It enforces object uniqueness before peeling (`len(objects) != 1: return None`), preventing an ambiguous prefix from silently resolving if one match is a commit and another is a blob.
3. **The Residual Leak:** Notice line 125: `return _commit(repo, objects[0])`.
   `objects[0]` is a 40-hex string. `_commit` invokes `rev-parse objects[0]^{commit}`. If an adversarial ref exists whose name is the full 40-hex string `refs/heads/<objects[0]>` or `refs/tags/<objects[0]>` pointing to a different commit, Git's revision parser still resolves the ref rather than the object!
4. **Judge Asymmetry:** In `tools/check-revision-binding.py`, the judge tests other tools using `object_selector_probes`, yet the judge's own `bind()` function (lines 162-177) uses `rev_parse(repo, rev)` (`rev^{commit}`) without `--disambiguate`. If `--tools-revision` is supplied as a ghost hex branch, the judge's own CLI option binder suffers from the exact residual it tests.
5. **Preregister Key Alignment:** `preregister.json:37-47` names cases: `valid_prefix_shadow_branch`, `valid_prefix_shadow_tag`, `full_id`, `unlanded`, `unpushed`. The seeded judge keyed them as `real_prefix_shadow_branch`, `real_prefix_shadow_tag`, `full_object_id`, `unlanded_object`, `unpushed_object`.

---

## 3. Compatible Synthesis: The Proposed Move

**Proposed Move:** Connect Git object database isolation to commit-ish resolution through a **Hermetic Two-Stage Object Resolution Pipeline** in `_revision.py` and align the independent judge `check-revision-binding.py` without code sharing.

### Step 1: Hermetic Object-to-Commit Peeling in `tools/_revision.py`
In `_object_commit(repo, revision)`:
1. Enumerate matching object IDs via `git rev-parse --disambiguate={revision.lower()}`.
2. If `len(objects) != 1`, return `None` (0 matches = unresolvable/ghost -> `E-REVISION-INVALID`; >1 matches = ambiguous -> `E-REVISION-INVALID`).
3. Take the unique resolved OID `oid = objects[0]`.
4. To eliminate any possibility of a 40-hex/64-hex refname collision during peeling, inspect the object type directly from the object database:
   - Use `_git(repo, "cat-file", "-t", oid)`.
   - If the type is `"commit"`: return `oid` directly. A commit object is already its own canonical commit SHA; bypassing `rev-parse oid^{commit}` prevents any full-hash refname collision.
   - If the type is `"tag"`: the object is an annotated tag. Peel it hermetically using `_git(repo, "rev-parse", "--verify", "--quiet", "--end-of-options", f"{oid}^{{commit}}")`. Because `oid` is confirmed to be an object-database tag, peeling returns its referenced commit SHA.
   - If the type is `"blob"` or `"tree"`: return `None` immediately. A blob or tree cannot be a commit-ish.

*Alternative Minimal Patch:* If `cat-file -t` is deemed a new subcommand, retain `_commit(repo, objects[0])` but explicitly verify that the returned SHA either matches `objects[0]` (for commit objects) or dereferences an annotated tag where `objects[0]` is of type tag. Direct `cat-file -t` is preferred because it strictly uses Git's plumbing object inspector.

### Step 2: Symmetrical Hardening of `--tools-revision` in `check-revision-binding.py`
In `tools/check-revision-binding.py`:
- In the judge's own `bind(repo, rev, branch="master")` function (lines 162-177), resolve `rev` using independent object disambiguation:
  ```python
  object_ids = git(repo, "rev-parse", f"--disambiguate={rev.lower()}").stdout.splitlines()
  if len(object_ids) != 1:
      raise Cannot(ID_INVALID, "revision", "commit selector unresolvable or ambiguous")
  sha = rev_parse(repo, object_ids[0])
  ```
- This maintains clean separation (the judge does not import `_revision.py`), while closing the self-binding blind spot so the judge itself rejects ghost hex branches passed to `--tools-revision`.

### Step 3: Exact Case-Key Alignment with `preregister.json`
In `tools/check-revision-binding.py` `object_selector_probes()`:
Ensure that probe dictionary keys match `preregister.json:37-47` exactly:
- `valid_prefix_shadow_branch` (accept, binds object)
- `valid_prefix_shadow_tag` (accept, binds object)
- `ghost_hex_branch` (refuse, `E-REVISION-INVALID`, exit 2)
- `ghost_hex_tag` (refuse, `E-REVISION-INVALID`, exit 2)
- `uppercase_object` (accept, binds commit)
- `full_id` (accept, binds commit)
- `annotated_tag_object` (accept, peels tag to commit)
- `noncommit_blob` (refuse, `E-REVISION-INVALID`, exit 2)
- `unlanded` (refuse, `E-REVISION-NOT-LANDED`, exit 2)
- `unpushed` (refuse, `E-REVISION-NOT-PUSHED`, exit 2)

---

## 4. Second-Order Effects & Affected Axes

- **C2 Operability (Primary Beneficiary, 0 → 9):**
  - Resolves the core C2 metric `object_selector_tools` across all 9 original tools.
  - Guarantees that neither short hex prefixes nor full 40/64-hex strings can be aliased by branch or tag refs.
  - Strictly preserves commit-ish behavior: annotated tag objects continue to peel to their landed commit, satisfying the backward-compatibility contract established in round 18.
  - Ambiguous prefixes (such as an identical 7-hex prefix matching a commit and a blob) are rejected before peeling, preventing silent commit-preference leaks.
- **C1 Adjacency (Unharmed, 0 → 1):**
  - C1's gate `check-adjacency-anchors.py` imports `_revision.bind()`. Hardening `_revision` ensures that C1's `--revision <REV>` evaluation is protected against ref-aliasing bugs without modifying any adjacency anchor or PROVINCE citation.
- **C3 Calibration (Unharmed, 1 → 0):**
  - C3's gate `check-registry-coverage.py` imports `_revision.bind()`. Hardening `_revision` ensures C3's `--revision <REV>` evaluation is similarly protected.
- **Substrate / Execution Surfaces:**
  - Read-only operations only: `git rev-parse --disambiguate` and `git cat-file -t` access local object files without mutating `.git`, refs, worktrees, or filesystem state.
  - Zero host action: no pacman, systemctl, bootloader, kernel, or mount commands are invoked.

---

## 5. Risks and Explicit Contradictions

| Risk | Severity | Mechanism | Mitigation |
|---|---|---|---|
| **Prefix Length < 4 Error** | High | Git's `--disambiguate` exits with fatal error if prefix length is < 4 characters. | `tools/_revision.py:41` enforces `REV = re.compile(r"^[0-9a-fA-F]{7,64}$")`. The minimum selector length is 7, strictly above Git's 4-character threshold. |
| **Silent Tag-Peeling Failure on Tag-to-Blob** | Medium | An annotated tag pointing to a blob or tree object might be parsed as a tag, but fails peeling to a commit. | Peeling `oid^{commit}` fails for non-commit-target tags, correctly returning `None` and raising `E-REVISION-INVALID`. |
| **Contradiction Between Gitrevisions and Ref Precedence** | Explicit Contradiction | `gitrevisions` specifies that `<sha1>` names an object, but `git rev-parse` prioritizes `<refname>` when a ref matches the hex string. | Explicitly acknowledge that Git's parser gives precedence to refnames. Enforce object-database-first resolution via `--disambiguate` rather than relying on `rev-parse <rev>^{commit}` to favor objects over refs. |
| **Judge Code Leakage** | Critical | If `check-revision-binding.py` imports `_revision.py` to fix its own `--tools-revision` binding, it violates the independent-judge isolation contract. | Implement the disambiguation directly inside `check-revision-binding.py` using standard `subprocess` calls to `git rev-parse --disambiguate`, maintaining complete source independence. |

---

## 6. Verification Plan (For L1 Post-Wave Final Evaluation)

*Note: Per seat contract, NO verification commands, gates, or selftests were executed by this seat.*

After external worktree integration by L1:

1. **Verify C2 Object-Selector Continuity:**
   ```bash
   python3 tools/check-revision-binding.py --tools-revision <REV> --object-selectors
   ```
   *Expected:* `object_selector_tools=9`, `object_selector_status=PASS`, exit code `0`.
2. **Verify Hermetic Binder Selftests:**
   ```bash
   python3 tools/_revision.py --selftest
   ```
   *Expected:* All hermetic cases pass (ghost branch/tag rejected, shadow prefix resolved to object, uppercase resolved, tag peeled, blob rejected), exit code `0`.
3. **Verify Independent Judge Selftests:**
   ```bash
   python3 tools/check-revision-binding.py --selftest
   ```
   *Expected:* All independent judge fixtures pass, exit code `0`.

---

Scope: executed=none
