# ReadScanAmbientReads — C1 code reading, ambient-read rule family (source channel)

**Verdict:** coverage review of the frozen probe's ambient-READ rule family: 4 construct classes the
rules do NOT flag lie OUTSIDE the declared named limit (S181 procfs read side); 2 further classes
inside that limit are also unflagged (declared debt). No code was executed (NO-EXEC: read/grep/glob
only).

**Frozen counter:** `tools/probe-child-env-allowlist-r34.py` at `6de666c427ba9aa6b4350561980bde8d0e7c261d`,
sha256 `35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8` (matches the declared hash).
It is the round-33 probe with only docstring header, usage, VERSION and target sets changed; the scan
rules are byte-identical. All line citations below are to this frozen blob (extracted copy:
`/fast/scratch/hyaku/tsukuroi-r34/ReadScanAmbientReads/probe-r34.py`, sha256 identical).

**Named limit (declaration, `SCORECARD.md:1431` at 6de666c):** "Named limit, carried from round 33
and not built: the read side is open (a target that learns through procfs that it is traced and reads
its initial environment there, S181)." This item is round-33 routed defect 4 (round-33 spot-check
lesson §5 item 4: "list every construct class those rules do not flag").

## 1. The rule family as implemented (what the flag does flag)

| # | Rule | Site (frozen blob) |
|---|---|---|
| R1 | ambient-read attribute: ANY `.environ`/`.environb`/`.getenv`/`.getenvb` on any object | `scan_module`, `if node.attr in OS_AMBIENT` (line 686; `OS_AMBIENT` line 487) |
| R2 | ambient Name alias: name resolving to `os.environ`/`os.environb`/`os.getenv`/`os.getenvb`/`sys.modules` | `scan_module` Name branch (lines 692-693) |
| R3 | `from os import environ/environb/getenv/getenvb/<OS_INHERIT>/*` | `scan_module` ImportFrom branch (lines 679-680) |
| R4 | import of HIDING_MODULES top-level names (posix, importlib, ctypes, nt, inspect, builtins, gc, asyncio, pty, multiprocessing, concurrent, _posixsubprocess, webbrowser, platform, pydoc, cffi, distutils, runpy, code, codeop, pickle, marshal, types, zipimport) | lines 670-671, 675-676; `HIDING_MODULES` lines 491-496 |
| R5 | call of `exec`/`eval`/`compile`/`__import__`/`globals`/`locals`/`vars`/`dir` | line 705 (`HIDING_CALLS` 489-490); calls with unnameable callee skipped at 701-703 |
| R6 | `getattr`/`setattr`/`hasattr`/`delattr` with os/posix/sys receiver, <2 args, non-constant name, or constant in OS_AMBIENT ∪ SPAWN_ANY | lines 707-712 |
| R7 | `__dict__`/`__getattribute__`/`__builtins__`/`__globals__`/`__subclasses__`/`__loader__`/`__spec__`, `sys.modules` | lines 688-689 (`HIDING_ATTRS` 497-499) |
| R8 | names `__builtins__`/`__loader__`/`__spec__` | lines 692-693 |
| R9 | any non-docstring str constant containing `/proc/self/status`, `/proc/self/environ`, `TracerPid`, `environ`, or `getenv` | lines 730-734 (`TRACE_STRINGS` 488, `HIDING_STRINGS` 500) |
| R10 | `env=` shape rule (spawn side): Dict/DictComp pass (617), `dict(...)` pass (626-627), verified builder (632-634; body checked only for None/fall-off-end by `_builder_findings` 738), name bindings must recurse into expr kinds else fail closed (661) | `env_ok` (609-663) |

Docstring Known-limit sentence: lines 96-99 ("a hiding construct this list does not name escapes it;
in particular the read side is not closed (a target can learn it is observed, or read the ambient
environment through a path assembled from fragments, with constructs the scan does not name), and an
`env=` dict whose values are taken from an unflagged ambient source passes the shape rule").

**Why source-channel rules exist:** a traced run is the only observed run, so a target that learns it
is observed can behave benignly under trace; the source channel is the only static witness of that
hidden branch (probe docstring lines 44-47). A construct class the source rules miss is therefore a
candidate primitive for the untraced branch of a tracer-detecting variant — exactly the shape the
S181 named limit bounds but does not build.

## 2. Classes INSIDE the named limit (S181 procfs) — unflagged, but declared debt

- **A1 — composed-path procfs read (str).** Example: `open("/proc/self/" + "".join(["envir","on"]), "rb").read()`.
  Missed by R9: no single constant contains a banned substring (lines 730-734); no other rule inspects
  `open()`/file paths. The learn side (`/proc/self/status` TracerPid) can be parsed positionally or
  with a composed field name, likewise without any banned literal. INSIDE the named limit (S181).
- **A2 — bytes-literal procfs path.** Example: `os.open(b"/proc/self/environ", os.O_RDONLY)`.
  Missed by R9's `isinstance(node.value, str)` guard (line 730): `ast.Constant` bytes values never
  enter the substring loop; no other rule examines constants. INSIDE the named limit (S181).

## 3. Classes OUTSIDE the named limit — unflagged by the source rules (count: 4)

- **C1 — stdlib / foreign-module wrapper reads, values fed through an env_ok-approved container.**
  Example: `subprocess.run(..., env={"GIT_HOME": os.path.expanduser("~")})` (equally
  `dict(os.path.expandvars(x) for x in ...)` via 626-627, or a `|` merge via 619-621).
  Missed by R1 (wrapper attribute names are not in OS_AMBIENT, 486-487/686), R4 (shutil/getpass/
  tempfile/locale/time/pathlib/urllib.request/posixpath are not in HIDING_MODULES, 491-496; the
  exact top-level split-match at 670 also lets `posixpath` dodge the `posix` ban), R9 (no banned
  substring in `"~"`, `"$HOME"`, `""`), and R10's unconditional Dict/DictComp pass (617) and
  `dict()` pass (626) — the docstring itself declares the last (lines 97-99).
  Grounded stdlib env readers on this host (Python 3.14.8): `posixpath.expanduser` → `os.environ['HOME']`
  (`/usr/lib/python3.14/posixpath.py:244,257`); `expandvars` → `os.environ` (`:315,327`); `shutil.which`
  → `os.environ.get("PATH")` (`shutil.py:1581`); `getpass.getuser` → `os.environ.get(LOGNAME/USER/LNAME/
  USERNAME)` (`getpass.py:231`); `tempfile.gettempdir` → TMPDIR/TEMP/TMP (`tempfile.py:163`);
  `locale.setlocale(LC_ALL, "")`/`getlocale` → LANG/LC_*; `os.get_exec_path()` → `os.environ` PATH
  (`os.py:649`); `pathlib.Path.home()` → expanduser; `urllib.request.getproxies` → http_proxy family.
  HOME, TMPDIR, PATH, LANG, USER, LOGNAME, SHELL are value-channel names, so the exact NAME=VALUE
  strings these return would trip the predicate if passed to a child. OUTSIDE the named limit.

- **C2 — higher-order attribute-lookup callables with runtime-composed names.**
  Example: `operator.attrgetter("".join(["enviro","n"]))(os)` (equivalently
  `functools.reduce(getattr, ["".join(["enviro","n"])], os)` or
  `functools.partial(getattr, os)("".join(...))`). Returns `os.environ` with no flagged construct.
  Missed by R5 (only HIDING_CALLS is checked, 705; `operator`/`functools` are absent from
  HIDING_MODULES, 491-496), R6 (a bare `getattr` *reference* is not a Call node, so 707-712 never
  fires), R9 (composed pieces carry no banned substring, 730-734). OUTSIDE the named limit.

- **C3 — frame-object attribute route.**
  Example: `bi = sys._getframe(0).f_builtins; osm = bi["".join(["__imp","ort__"])]("os"); home = operator.attrgetter("".join(["envir","on"]))(osm)["HOME"]`.
  Reaches builtins/import machinery without one banned name. Missed by R7 (HIDING_ATTRS, 497-499,
  lists `__globals__`/`__builtins__` but not the frame spellings `f_globals`/`f_builtins`/
  `f_locals`; 688-689), R8 (692-693), R4 (the `sys` import is unrestricted — only the
  `sys.modules` patterns are banned, 681-682), R2 (alias list has no `sys._getframe`). OUTSIDE the
  named limit.

- **C4 — calls through unnameable callee expressions (subscript / arbitrary callee).**
  Example: `cmds = {"e": eval}; cmds["e"]("os." + "".join(["envir","on"]))`.
  Missed by R5's pre-filter `name = canon(node.func); if not name: continue` (lines 701-703): any
  call whose callee is not a Name or dotted-Attribute chain bypasses every call rule (HIDING_CALLS,
  getattr family, spawn checks) — and lets any string-composed source past R9. OUTSIDE the named
  limit.

**Count of classes OUTSIDE the named limit: 4** (C1, C2, C3, C4).

## 4. Checked-and-closed routes (for boundary clarity)

Direct attribute access on any receiver, `from os import ...` incl. aliases and `import os as y`
(R1/R2/R3); getattr-family with constant env names, non-constant names or os/posix/sys receivers
(R6); `__dict__`/`__getattribute__`/`__globals__`/`__builtins__`/`__subclasses__`/`__loader__`/
`__spec__`/`sys.modules` (R7/R8); called `eval`/`exec`/`compile`/`__import__`/`globals`/`locals`/
`vars`/`dir` (R5); the 24 banned modules (R4); any str constant containing the five banned substrings
inclusive of f-string literals (R9; docstring exemption is inert because docstrings cannot execute
without a banned call); `env=` from a name bound to any import fails closed (661: "bound by
ImportFrom"); `env=` from builders in non-tools modules or dar packages fails closed (648: "which
this scan cannot read"); env= deeper than 8 nested bindings fails closed (612); `subprocess` spawns
without env=/env=None/**kwargs-no-env/positional args flagged (714-727 region); `os.system`/
`os.popen`/non-`e` `os.exec*`/`os.spawn*`/`subprocess.getoutput|getstatusoutput` inherit forms
flagged; star-imports from SPAWN_HEADS flagged (684); uncalled spawn-function references flagged.
Multi-level `tools/` imports are not scanned (`source_findings` queues only `tools/<toplevel>.py`,
773-774), but their use as env= builders fails closed at 648; a leak through them would require the
C1 shape again.

## 5. Findings (severity order)

1. **[inf] Counter-spec gap:** the declaration's named limit ("SCORECARD.md:1431`, S181 procfs
   read side) is narrower than the probe docstring's own Known-limit clause (lines 96-99), whose
   umbrella wording ("a hiding construct this list does not name escapes it", "path assembled from
   fragments", "env= dict whose values are taken from an unflagged ambient source") arguably
   pre-declares C1-C4. "Inside the named limit" therefore depends on which document is authoritative;
   the two disagree. This ambiguity is itself worth fixing before any re-claim on this probe.
2. **[obs] C1 (stdlib wrapper reads) is the only class whose leak path is explicitly acknowledged in
   the docstring (97-99) yet not bounded by the named limit; it is also the most practical (pure
   stdlib, zero exotic constructs), and it bypasses the source channel entirely.
3. **[obs] C2/C3/C4 are not mentioned anywhere in the docstring; they are new relative to both the
   named limit and the Known-limit sentence except through its unbounded umbrella phrase.
4. **[obs] A1/A2 are inside the named limit and are purely declared debt — they only confirm the
   declaration's limitation rather than extend it.

## 6. Residual risk and verification gaps

- NO-EXEC: nothing was run; every example is AST-level reasoning over the CPython 3.14.8 grammar
  with no execution. Each example should be compiled/run in a sandbox before being relied on.
- Stdlib grounding is static (grep of `/usr/lib/python3.14/...` lines cited above); behavior matches
  CPython source. [obs]
- Whether any concrete tool construct would *also* be caught by the runtime (names/quiet) channels is
  outside this item's family; the source-channel miss matters exactly for tracer-detecting variants
  whose untraced branch is never observed. [inf]
- The two sibling families (spawns and env= shapes; run-channel carriers, is_git and parity
  normalisation) are owned by the other code-reading seats and were not examined here.

Scope: read=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/tools/probe-child-env-allowlist-r34.py (git show 6de666c…; scratch copy /fast/scratch/hyaku/tsukuroi-r34/ReadScanAmbientReads/probe-r34.py), SCORECARD.md@6de666c (lines 1416-1450), corpus/SOURCES.md row S181, corpus/lessons/round-33-verifier-spotcheck.md §5.4, .ufo/prompts/tsukuroi-round-34.md lines 343-365, host stdlib posixpath.py/getpass.py/shutil.py/tempfile.py/os.py; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1/ReadScanAmbientReads.md, /fast/scratch/hyaku/tsukuroi-r34/ReadScanAmbientReads/probe-r34.py; executed=read-only git show / grep (no analyzer runs)
Model: zai/glm-5.3-flash
Installs: none
