VERDICT: holds
ROW: PA1
lines checked: frozen/src/alpm-package.7.raw:95-124

Row under test, read at the pinned commit (`git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 9cc9aa77e30e0e23de2d4d2697b3b218ada02969:corpus/knowledge/alpm-package-anatomy-r41.md`; blob 467fc0df1579376ad15cc7ca6224acfd500470d0, identical to the worktree blob by `git hash-object`):

| PA1 | The package format document names three metadata files that must be present at the root of an ALPM package, `.BUILDINFO`, `.MTREE` and `.PKGINFO`, and an optional install scriptlet named `.INSTALL` at the same root, beside zero or more data files | `.BUILDINFO .MTREE .PKGINFO; optional .INSTALL` | S227 alpm-package.7.raw:100-120 “The following files must be present at the root of an ALPM based package:” | the local `mtree` of pacman 7.1.0.r9.g54d9411-3 lists `./.BUILDINFO` and `./.PKGINFO` as package members (`mtree-pacman-head.txt`) |

Snapshot integrity and liveness:
- `sha256sum .ufo/waves/round-41/frozen/src/alpm-package.7.raw` → `b551bb392f6899c89c4c0d5778c89ad482f0c1251260ccf336bd5b5ed2693c45`, equal to the `alpm-package.7.raw` line of `frozen/src/SHA256SUMS`.
- Live fetch, access date 2026-10-26T18:07:19Z: `curl -fsSL --http1.1 --retry 4 https://man.archlinux.org/man/alpm-package.7.raw` → sha256 `b551bb39…` and `cmp` against the frozen copy printed `LIVE-IDENTICAL-TO-FROZEN`, so every frozen line number below is also a live line number. (First attempt minutes earlier failed with `curl: (35) TLS connect error … unexpected eof while reading`; the retry succeeded and no evidence was taken from the failed attempt.)
- Rendered page https://man.archlinux.org/man/alpm-package.7 fetched the same minute (15643 bytes) and carries the same statements: “The following files must be present at the root of an ALPM based package:” (live-rendered.html:143-144), the `.BUILDINFO` bullet (:146), “Optionally, an alpm-install-scriptlet named .INSTALL may be present at the root of an ALPM based package.” (:160-162), “Zero or more data files may be present in an ALPM based package” (:166-168).

Clause check of the rule cell against frozen/src/alpm-package.7.raw (line numbers pinned by grep on the frozen file):
- “three metadata files” — `.SS Metadata` at :97-98 with exactly three bullets :101-114. Supported.
- “must be present at the root of an ALPM package” — :100 “The following files must be present at the root of an ALPM based package:” (the doc's “ALPM based package” vs the rule's “ALPM package” is the same referent; no meaning change). Supported.
- “.BUILDINFO, .MTREE and .PKGINFO”, in that order — :102 `\f(CR.BUILDINFO\fR: a \fBBUILDINFO\fR file`, :108 `\f(CR.MTREE\fR: an \fBALPM-MTREE\fR file`, :114 `\f(CR.PKGINFO\fR: a \fBPKGINFO\fR file`. Supported.
- “an optional install scriptlet named `.INSTALL` at the same root” — :120 “Optionally, an \fBalpm-install-scriptlet\fR named \f(CR.INSTALL\fR may be present at the root of an ALPM based package.” (the doc's cross-reference name alpm-install-scriptlet(5) is what the rule calls an “install scriptlet”; “at the same root” matches “at the root of an ALPM based package”). Supported.
- “beside zero or more data files” — :123-124 “Zero or more \fBdata\fR files may be present in an ALPM based package”. Supported. Note: these lines sit three lines past the row's inline citation range 100-120, but they are inside S227's declared window “lines 95-124 of the `alpm-package.7.raw` rendering” (corpus/SOURCES.md S227 at 9cc9aa7) and inside the 95-124 window this seat was told to check — citation hygiene only, no clause is unsupported or overstated; widening the row's range to 100-124 would make the inline citation cover every clause.
- No missing condition: the doc attaches no precondition to the “must be present” list (no “except”, no “if”), and PA1 correctly attributes the requirement to the format document rather than to libalpm load enforcement — the entry itself keeps that split (“Spec and implementation differ on purpose … PA1 is the format document's ‘must be present’, PA2 is what libalpm enforces”, QUALITY section of the pinned entry).
- Value cell `.BUILDINFO .MTREE .PKGINFO; optional .INSTALL` matches the rule cell. The quote “The following files must be present at the root of an ALPM based package:” is verbatim at the first cited line, :100, within S227's cited 100-120.

Host cell check against .ufo/waves/round-41/frozen/hostcap/:
- `mtree-pacman-head.txt:3-4`: `./.BUILDINFO time=1792052823.0 mode=644 size=7080 sha256digest=2111f027…` and `./.PKGINFO time=1792052823.0 mode=644 size=1136 sha256digest=340af35e…` — exactly the two members the host cell names; the head does not list `./.MTREE` and the cell does not claim it does (consistent with PA5's self-exclusion, judged elsewhere).
- Version attribution: `capture-meta.txt:2` `pacman pacman 7.1.0.r9.g54d9411-3` (capture 2026-10-26T16:14:04Z, :1); `capture.sh:30-31` shows the capture is `zcat -- "$p/mtree" | sed -n 1,4p` of the local-db entry matching `pacman-[0-9]*`, so “the local `mtree` of pacman 7.1.0.r9.g54d9411-3” is accurate.
- Capture integrity: `sha256sum -c MANIFEST.sha256` in hostcap/ → all six files OK.
- The host cell is stated as measured (capture-backed) and its claim is exactly what the capture shows — honest, no overreach.

Verdict rationale: every clause of the rule cell is supported by the checked document text at the pinned snapshot, which is byte-identical to the live source as of 2026-10-26; the quote sits at the first cited line; the host cell is true of the capture and honestly framed. Residual (cosmetic): the data-files clause's documentary support lies at :123-124, outside the row's inline 100-120 range but inside S227's declared 95-124 window.

Not done / out of scope: no pacman transaction and no host mutation were performed; rows PA2-PA8 and the S227-S236 SOURCES rows beyond S227 were not judged by this seat; the frozen counter `tools/check-package-anatomy-r41.py` was not run (this verdict file is its input). No tool installs or upgrades were made.
