# Patch D2 — S342 cited ranges cannot support the row's own claim (one range is non-minimal)

Status: **proposed, NOT applied.** The lane repo was not modified. The L1 decides whether this lands.
Target: `corpus/SOURCES.md:353` (row S342) and `corpus/lessons/round-84.md:27` and `:33`.
Lane root `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`,
lane revision measured: `f19e73f3aa9817e76044e4e43a343c6ca6d929df`.

## Defect 2a — `corpus/SOURCES.md:353`: the anchor stops one line before the evidence it teaches

The row declares `raw lines 388-401 (def call), 397-400 (wait with timeout, kill in except)` and teaches
"call() kills the child when wait(timeout) raises, **then re-raises**". In
`Lib/subprocess.py` (CPython v3.14.8, re-fetched live 2026-11-06, HTTP 200, sha256
`7fa4af83422024a19e64a80937f6c8094244c3397372a495b348dfbe44a5dd72`) the function is:

```
388 def call(*popenargs, timeout=None, **kwargs):
389     """Run command with arguments.  Wait for command to complete or
390     for timeout seconds, then return the returncode attribute.
391
392     The arguments are the same as for the Popen constructor.  Example:
393
394     retcode = call(["ls", "-l"])
395     """
396     with Popen(*popenargs, **kwargs) as p:
397         try:
398             return p.wait(timeout=timeout)
399         except:  # Including KeyboardInterrupt, wait handled that.
400             p.kill()
401             # We don't call p.wait() again as p.__exit__ does that for us.
402             raise
```

The `raise` — the evidence for "then re-raises" — is line **402**, outside both cited ranges (388-401 ends
at the comment; 397-400 ends at `p.kill()`).

The row's own clause "equal to `inspect.getsource(subprocess.call)` on the host" is true only for 388-402.
Verified on this host (python3 3.14.8):

```
pinned 388..402 == inspect.getsource(subprocess.call)  -> True
pinned 388..401 == inspect.getsource(subprocess.call)  -> False   (missing the trailing "raise")
```
Also `sha256sum /usr/lib/python3.14/subprocess.py` = `7fa4af83…` = the pinned upstream tag, so the pinned
file is byte-identical to the host's own file.

## Defect 2b — `corpus/lessons/round-84.md:27` and `:33`: cited range 397-400 is non-minimal

The row quotes "return p.wait(timeout=timeout) except: # Including KeyboardInterrupt, wait handled that.
p.kill()" and cites `raw 397-400`. That normalized text lies in **398-400**; line 397 is `try:`. Under the
frozen counter's own rule (`exact_span` in `tools/count-resume-rows-r84.py:98-111`, which rejects a span
whose first or last line can be dropped) the range 397-400 is `span-not-minimal`:

```
exact_span(lines, 397, 400, quote) -> (False, 'span-not-minimal')
exact_span(lines, 398, 400, quote) -> (True,  'ok')
```
The quote text itself is verbatim modulo whitespace ✓ (line 399's double space collapses to one).

## Proposed changes

`corpus/SOURCES.md:353`:
```
- raw lines 388-401 (def call), 397-400 (wait with timeout, kill in except);
+ raw lines 388-402 (def call), 398-400 (wait with timeout, kill in except);
```
(the "equal to inspect.getsource(subprocess.call) on the host" clause then holds exactly, as verified above.)

`corpus/lessons/round-84.md:27` (row S342, URL/location column):
```
- https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/subprocess.py, 2026-11-06, raw 397-400
+ https://raw.githubusercontent.com/python/cpython/v3.14.8/Lib/subprocess.py, 2026-11-06, raw 398-400
```

`corpus/lessons/round-84.md:33` (round-83 correction paragraph):
```
- `Popen.wait`". That reason is false: CPython v3.14.8 `Lib/subprocess.py` raw 397-400 (S342) wraps
+ `Popen.wait`". That reason is false: CPython v3.14.8 `Lib/subprocess.py` raw 398-400 (S342) wraps
```

Note: the uncommitted working-tree copy of `corpus/lessons/round-84.md` already differs from the committed
master-tip text in this region, so the L1 should re-check the line numbers against the worktree it commits.

## Verification after landing (read-only)

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff --stat corpus/SOURCES.md corpus/lessons/round-84.md
python3 tools/count-resume-rows-r84.py --root .        # expect verdict met, counted 10, failed 0, rc 0
```
