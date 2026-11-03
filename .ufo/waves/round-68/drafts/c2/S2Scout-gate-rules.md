# S2Scout Gate Rules: `check-knowledge-header.py` Analysis

Line references from `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/check-knowledge-header.py` (base 42400ec6):

1. **(a) Revision Binding and File Reading**
   - **Shared module import**: Lines 99-100 (`sys.path.insert(0, str(LANE / "tools")); import _revision`).
   - **Binding function and arguments**: Lines 288-295 in `run(argv, lane=LANE, out=None)`:
     - `binding = _revision.bind(repo, args.revision, branch)`
     - Extracts `sha, tip, origin_tip = binding.sha, binding.branch_tip, binding.origin_tip`
   - **Git runner function**: Lines 109-114 `git(repo, *args, timeout=60)`:
     - Invocation: `subprocess.run(["git", "--no-pager", "-C", str(repo), *args], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=_revision.clean_env(), timeout=timeout)`
   - **File listing function**: Lines 131-149 `notes_at(repo, sha)`:
     - Invocation: `git(repo, "ls-tree", "-r", "--name-only", sha, SCOPE)` (Line 132, where `SCOPE = "corpus/knowledge"` at Line 57).
     - Filter: `names = [name for name in listing.stdout.decode("utf-8", "replace").splitlines() if name.endswith(".md")]` (Lines 136-137).
   - **File blob reading function**: Lines 117-128 `read_blob(repo, commit, path)`:
     - Verifies blob object: `git(repo, "cat-file", "-t", spec)` where `spec = f"{commit}:{path}"` (Lines 118-123).
     - Fetches raw content: `git(repo, "show", spec)` returning `proc.stdout` (Lines 124-128).
     - Decoded as UTF-8 in `notes_at`: `raw.decode("utf-8")` (Line 146).

2. **(b) Fence Rule**
   - **Regex**: Line 61: `FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")`. Matches up to 3 leading spaces followed by 3 or more backticks (```) or tildes (~~~).
   - **Skipping logic**: Lines 156-169 in `header_lines(text)`:
     - State tracking: `fence = None` (Line 156).
     - For each line, `marker = FENCE.match(line)` (Line 159).
     - If opening fence (`fence is None`): records active fence character run `fence = run` (Lines 162-163).
     - If closing fence candidate: checks `run[0] == fence[0] and len(run) >= len(fence) and not line.strip()[len(run):].strip()` (Lines 164-165). If satisfied, resets `fence = None` (Line 166). Note that closing fence requires matching fence character, at least matching run length, and no info string.
     - While `fence is not None`: line is skipped with `continue` (Lines 168-169).

3. **(c) Column-Zero Rule**
   - **Header prefix check**: Lines 170-173 in `header_lines(text)`:
     ```python
     for key in KEYS:
         if line.startswith(key + ":"):
             found[key].append((number, line[len(key) + 1:].strip()))
             break
     ```
   - **Column-0 enforcement**: Because `line.startswith(key + ":")` checks the unmodified string `line` without stripping leading whitespace (`line.lstrip()`), any leading spaces or tabs fail the condition.
   - **Verification in tests**: Lines 461-465 (`case("indented-key", ...)`), testing that a four-space indented `    source: S999.` is treated as an indented code block and fails to match as a header key.

4. **(d) Exit Codes and JSON Output Shape**
   - **Exit codes**: Defined at Line 55 (`PASS, FAIL, CANNOT = 0, 1, 2`) and mapped at Line 254:
     - `0` (PASS): Evaluation succeeded with 0 findings.
     - `1` (FAIL): Evaluation succeeded but one or more policy findings were raised.
     - `2` (CANNOT_EVALUATE): Execution aborted due to CLI error, revision binding failure (`E-REVISION-INVALID`, `E-REVISION-NOT-LANDED`, `E-REVISION-NOT-PUSHED`, `E-BRANCH-MISSING`, `E-BRANCH-INVALID`), path missing/invalid, git error, or internal error.
   - **JSON output shape**: Emitted by `emit()` at Lines 231-254 (formatted with `json.dumps(payload, sort_keys=True)`):
     - `status`: `"PASS"` | `"FAIL"` | `"CANNOT_EVALUATE"`
     - `revision`: Git SHA string (e.g. 40 hex characters) or CLI input string
     - `branch`: Branch name string (default `"master"`)
     - `branch_tip`: Git SHA string of local branch tip or `null`
     - `origin_tip`: Git SHA string of remote origin tracking ref or `null`
     - `note_count`: Total evaluated markdown notes count (`int`)
     - `complete_count`: Count of notes with all required keys present (`int`)
     - `clean_count`: Count of notes without any problems (`int`)
     - `finding_count`: Total count of findings (`int`, `len(findings)`)
     - `scope`: Scope description string
     - `findings`: Array of objects: `[{"id": "<finding-id>", "site": "<site-path>", "detail": "<detail-message>"}]`
     - `notes`: Array of note detail objects: `[{"path": "<note-path>", "lines": {"source": <int|null>, "verified-at": <int|null>, "recheck": <int|null>}, "problems": [<str>]}]`
     - `message` (optional): Extra message string if passed to `emit`
   - **Selftest JSON output shape**: Emitted by `selftest()` at Lines 499-501:
     - `{"selftest": {"cases": <int>, "failures": [<str>], "passed": <int>, "status": "PASS" | "FAIL"}}`

5. **(e) Selftest Hermetic Fixture Repository**
   - **Function name**: `selftest(out=None)` at Lines 355-502.
   - **Hermetic temp directory**: Line 393: `repo = Path(tempfile.mkdtemp(prefix="knowledge-header-gate-"))`.
   - **Git repository creation**: Line 395: uses `git init` via helper `sandbox_git(repo, "-c", "init.defaultBranch=master", "init", "-q")`.
   - **Fixture commits helper**: Lines 335-342 `sandbox_commit(repo, tree)` writes files in `tree` dictionary, runs `git add`, and commits with `git commit -q -m "fixture"`.
   - **Sandbox configuration**: Lines 396-399 set `user.email="fixture@example.invalid"`, `user.name="Fixture"`, `commit.gpgsign="false"`, `core.hooksPath="/dev/null"`.
   - **Cleanup**: Lines 495-497 in `finally:` block: `shutil.rmtree(repo, ignore_errors=True)`.
