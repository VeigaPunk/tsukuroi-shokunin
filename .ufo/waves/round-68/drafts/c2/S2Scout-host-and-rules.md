2026-11-03T22:33:38Z

# S2Scout Host Applicability and Gate-Rule Ground

## 1. Host Kernel and Package Facts

### Command Evidence
```
$ uname -r
7.2.11-arch1-1
rc=0

$ pacman -Q linux
linux 7.2.11.arch1-1
rc=0

$ pacman -Q linux-headers 2>&1
linux-headers 7.2.11.arch1-1
rc=0

$ pacman -Qi linux | grep -E '^(Version|Build Date)'
Version         : 7.2.11.arch1-1
Build Date      : Thu 15 Oct 2026 09:28:58 PM -03
rc=0

$ ls /usr/lib/modules/
6.18.57-2-lts
7.2.11-arch1-1
rc=0

$ find /usr/lib/modules -maxdepth 1 -mindepth 1 -printf '%f\n' | sort
.old
6.18.57-2-lts
7.2.11-arch1-1
rc=0

$ stat -c '%y %n' /usr/lib/modules/*/pkgbase 2>/dev/null
2026-10-15 21:26:56.000000000 -0300 /usr/lib/modules/6.18.57-2-lts/pkgbase
2026-10-15 21:28:58.000000000 -0300 /usr/lib/modules/7.2.11-arch1-1/pkgbase
rc=0
```

### Kernel Releases and Version Match
- **Installed kernel release(s)**: `7.2.11-arch1-1`, `6.18.57-2-lts`
- **Any installed kernel 7.3 or newer**: `NONE`

---

## 2. Kernel Source Trees (/usr/src)

### Command Evidence
```
$ find /usr/src -maxdepth 1 2>/dev/null
/usr/src
/usr/src/debug
/usr/src/linux-lts
/usr/src/linux
/usr/src/nvidia-615.78.08
rc=0

$ ls /usr/src 2>/dev/null
debug
linux
linux-lts
nvidia-615.78.08
rc=0
```

- Symlink resolution:
  - `/usr/src/linux` -> `../lib/modules/7.2.11-arch1-1/build`
  - `/usr/src/linux-lts` -> `../lib/modules/6.18.57-2-lts/build`
- **Result**: No 7.3 tree is installed anywhere readable.

---

## 3. Numbered Gate Rules (check-knowledge-header.py)

1. **(a) Revision Binding and File Reading**
   - Import: Lines 99-100 (`sys.path.insert(0, str(LANE / "tools")); import _revision`).
   - Revision binding: Lines 288-295 inside `run()`:
     - `binding = _revision.bind(repo, args.revision, branch)`
     - Unpacks `sha, tip, origin_tip = binding.sha, binding.branch_tip, binding.origin_tip`.
   - Git runner: Lines 109-114 `git(repo, *args, timeout=60)`:
     - `subprocess.run(["git", "--no-pager", "-C", str(repo), *args], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=_revision.clean_env(), timeout=timeout)`
   - File listing: Lines 131-149 `notes_at(repo, sha)`:
     - Listing: `git(repo, "ls-tree", "-r", "--name-only", sha, SCOPE)` at Line 132 (`SCOPE = "corpus/knowledge"` at Line 57).
     - Filter: `names = [name for name in listing.stdout.decode("utf-8", "replace").splitlines() if name.endswith(".md")]` at Lines 136-137.
   - File reading: Lines 117-128 `read_blob(repo, commit, path)`:
     - Object type check: `git(repo, "cat-file", "-t", f"{commit}:{path}")` must equal `"blob"` (Lines 118-123).
     - Object extraction: `git(repo, "show", f"{commit}:{path}")` returning `proc.stdout` (Lines 124-128).
     - Decoded to UTF-8 in `notes_at` at Line 146.

2. **(b) Fence Rule**
   - Regex: Line 61: `FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")`.
   - Skipping logic: Lines 156-169 in `header_lines(text)`:
     - Initializes `fence = None` (Line 156).
     - For each line: `marker = FENCE.match(line)` (Line 159).
     - Opening fence: if `fence is None`, sets `fence = run` (Lines 162-163).
     - Closing fence: checks `run[0] == fence[0] and len(run) >= len(fence) and not line.strip()[len(run):].strip()` (Lines 164-165); if matched, resets `fence = None` (Line 166).
     - If `fence is not None`, skips line with `continue` (Lines 168-169).

3. **(c) Column-Zero Rule**
   - Header check: Lines 170-173 in `header_lines(text)`:
     ```python
     for key in KEYS:
         if line.startswith(key + ":"):
             found[key].append((number, line[len(key) + 1:].strip()))
             break
     ```
   - Column-0 enforcement: `line.startswith(key + ":")` checks the unstripped line prefix directly at index 0. Any leading whitespace or tab causes the check to fail. Indented keys (e.g. 4-space code block tested at Lines 461-465) do not match.

4. **(d) Exit Codes and JSON Output Shape**
   - Exit codes: Line 55 and Line 254:
     - `0` (PASS): Evaluation succeeded with 0 findings.
     - `1` (FAIL): Evaluation succeeded but findings were generated.
     - `2` (CANNOT_EVALUATE): Cannot evaluate (CLI errors, invalid/unlanded/unpushed revision, unresolved lane, git failure, internal error).
   - JSON payload shape emitted by `emit()` at Lines 231-254:
     ```json
     {
       "branch": "<str>",
       "branch_tip": "<sha|null>",
       "clean_count": <int>,
       "complete_count": <int>,
       "finding_count": <int>,
       "findings": [{"detail": "<str>", "id": "<str>", "site": "<str>"}],
       "note_count": <int>,
       "notes": [{"lines": {"recheck": <int|null>, "source": <int|null>, "verified-at": <int|null>}, "path": "<str>", "problems": [<str>]}],
       "origin_tip": "<sha|null>",
       "revision": "<sha>",
       "scope": "<str>"
     }
     ```
   - Selftest payload shape (Lines 499-501):
     ```json
     {"selftest": {"cases": <int>, "failures": [<str>], "passed": <int>, "status": "PASS" | "FAIL"}}
     ```

5. **(e) Hermetic Selftest Fixture Repository**
   - Function: `selftest(out=None)` at Lines 355-502.
   - Temp directory: Line 393: `repo = Path(tempfile.mkdtemp(prefix="knowledge-header-gate-"))`.
   - Init: Line 395: `sandbox_git(repo, "-c", "init.defaultBranch=master", "init", "-q")`.
   - Configuration: Lines 396-399 configure `user.email`, `user.name`, `commit.gpgsign="false"`, `core.hooksPath="/dev/null"`.
   - Commits: helper `sandbox_commit(repo, tree)` (Lines 335-342) writes tree dictionary files, calls `git add`, `git commit -q -m "fixture"`, returns HEAD sha.
   - Cleanup: Lines 495-497 in `finally:` block executes `shutil.rmtree(repo, ignore_errors=True)`.

---

## 4. Verification and Knowledge Base Counts

### Operative Dangling Source References at Base 42400ec6
- **Command**:
  ```bash
  python3 -c '
  import subprocess, re
  repo = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
  commit = "42400ec6"
  sources_text = subprocess.check_output(["git", "-C", repo, "show", f"{commit}:corpus/SOURCES.md"], text=True)
  valid_sids = set(re.findall(r"\bS\d{3,}\b", sources_text))
  notes = [p for p in subprocess.check_output(["git", "-C", repo, "ls-tree", "-r", "--name-only", commit, "corpus/knowledge"], text=True).splitlines() if p.endswith(".md")]
  fence_re = re.compile(r"^ {0,3}(`{3,}|~{3,})")
  dangling = []
  for p in notes:
      text = subprocess.check_output(["git", "-C", repo, "show", f"{commit}:{p}"], text=True)
      fence = None
      last_source = None
      for line in text.splitlines():
          m = fence_re.match(line)
          if m:
              run = m.group(1)
              if fence is None: fence = run
              elif run[0] == fence[0] and len(run) >= len(fence) and not line.strip()[len(run):].strip(): fence = None
              continue
          if fence is not None: continue
          if line.startswith("source:"): last_source = line
      if last_source:
          sids = re.findall(r"\bS\d{3,}\b", last_source)
          bad = [s for s in sids if s not in valid_sids]
          if bad: dangling.append((p, last_source, bad))
  print(f"DANGLING_COUNT={len(dangling)}")
  '
  ```
- **Output**: `DANGLING_COUNT=0` (rc=0)
- **Count**: 0

### Knowledge Notes Mentioning S999 or S-id > 300 on source: Line
- **Command**:
  ```bash
  python3 -c '
  import subprocess, re
  repo = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin"
  commit = "42400ec6"
  notes = [p for p in subprocess.check_output(["git", "-C", repo, "ls-tree", "-r", "--name-only", commit, "corpus/knowledge"], text=True).splitlines() if p.endswith(".md")]
  fence_re = re.compile(r"^ {0,3}(`{3,}|~{3,})")
  s999_or_above_300 = []
  for p in notes:
      text = subprocess.check_output(["git", "-C", repo, "show", f"{commit}:{p}"], text=True)
      fence = None
      last_source = None
      for line in text.splitlines():
          m = fence_re.match(line)
          if m:
              run = m.group(1)
              if fence is None: fence = run
              elif run[0] == fence[0] and len(run) >= len(fence) and not line.strip()[len(run):].strip(): fence = None
              continue
          if fence is not None: continue
          if line.startswith("source:"): last_source = line
      if last_source:
          sids = re.findall(r"\bS\d{3,}\b", last_source)
          hits = [s for s in sids if s == "S999" or int(s[1:]) > 300]
          if "S999" in last_source or hits:
              s999_or_above_300.append((p, last_source))
  print(f"S999_OR_ABOVE_300_COUNT={len(s999_or_above_300)}")
  '
  ```
- **Output**: `S999_OR_ABOVE_300_COUNT=0` (rc=0)
- **Count**: 0

### Existing S-id Checkers in tools/ at 42400ec6
- **Command**:
  ```bash
  $ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin ls-tree -r --name-only 42400ec6 tools | grep -iE 'source|sid|knowledge|ref'
  tools/check-knowledge-header.py
  tools/check-source-scope-correction.py
  tools/probe-git-env-residual-r30.py
  rc=0
  ```
- **Analysis**:
  - `check-knowledge-header.py`: checks presence of `source:`, `verified-at:`, `recheck:` keys, not S-id validity against SOURCES.md.
  - `check-source-scope-correction.py`: narrow gate for round-14 S042/S045 correction only.
  - `probe-git-env-residual-r30.py`: checks child environment residuals.
- **Existing generic S-id reference checkers**: 0 (none)

---

## 5. Summary Key-Value Results
- `HOST_KERNEL=7.2.11-arch1-1`
- `PKG_LINUX=7.2.11.arch1-1`
- `V73_INSTALLED=NONE`
- `DANGLING_BASE=0`
- `S999_MENTIONS=0`
- `REF_CHECKERS=0`
