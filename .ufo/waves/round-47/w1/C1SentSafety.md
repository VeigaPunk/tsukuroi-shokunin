VERDICT: defect-found
ITEM: C1-S1 — security review of tools/check-scrub-admission-r47.py (runs `git -C <lane> show|ls-tree|rev-parse|merge-base` + json/sha256 on repo bytes).
COUNTER REVIEWED: `sha256sum tools/check-scrub-admission-r47.py` = e20c322171db76f1d08b51066e602707516f62eccdf3f64ca8356c69767f023b (matches the frozen digest); lane HEAD at review time f6bc6d056ebdf79a585745d4292faf90ae12d9fd (`git -C … log --oneline -1`), `base_ok` printed as 1 by the counter itself.

METHOD. Every probe ran against a `--shared` clone under /fast/scratch/hyaku/tsukuroi-r47/C1SentSafety/ (`git rev-parse --show-toplevel` asserted equal to the clone before the first commit, commits as `user.name=fixture user.email=fixture@invalid`), driven by four replay scripts now stored with their transcripts in `.ufo/waves/round-47/w1/C1SentSafety/` (`exp1.sh`..`exp4.sh`, `fixcheck.py`, `transcript-*.txt`). Nothing in the lane, the fleet repo, PATH or the host was written; the counter itself is write-free (see P7).

Two grant-side defects, one availability defect, one evidence-leg weakness, and four informational items. S1 and S2 are the ones that change what the frozen predicate can certify.

────────────────────────────────────────────────────────────────────────
S1 — HIGH (gate integrity, predicate conjunct defeated): the F2 README mark is grantable to text that denies admission
────────────────────────────────────────────────────────────────────────
Site: `tools/check-scrub-admission-r47.py:77` (`MARK_README = ('btrfs-scrub-grounding-r45.md', 'admitted round 47')`), `:78` (`NEGATE_RE = re.compile(r'unadmitted|not admitted|never admitted|stay pending|stays pending')`), `:369-371` (`'readme': any(all(x in ln for x in MARK_README) and not NEGATE_RE.search(ln) …)  # F2: negation earns nothing`), consumed by the top-level predicate at `:84` and `:373`.
Exploit path: the mark is a *substring* test plus an ASCII, case-sensitive, space-exact deny-list, so any spelling of the negation outside the list is scored as a grant. Three spellings defeat it; the honest-lowercase control does not:

    A1 `| … | Not admitted round 47: still pending |`            -> marks= {entry:true, readme:true, skill:true} marks_ok=3
    A2 `| … | not\u00a0admitted round 47; still pending |`         -> marks_ok=3   (NBSP, not U+0020)
    A4 `| … | \u043d\u043e\u0442 admitted round 47, row pending |` -> marks_ok=3   (Cyrillic "not")
    A3 `| … | not admitted round 47: still pending |`  (control) -> readme:false marks_ok=2
    (receipts: .ufo/waves/round-47/w1/C1SentSafety/transcript-exp1.txt, exp1.sh A1-A4)

End-to-end, with every other leg green (6 fabricated-but-well-formed seat reports + results + the real w1 dispatch, `structural_ok=1 quotes_ok=3 verdicts_ok=3`), the counter's own output is:

    H1 README `Not admitted round 47: still pending`  -> marks_ok=3  VERDICT= PASS
    H4 README `not<NBSP>admitted round 47; still pending` -> marks_ok=3  VERDICT= PASS
    H3 README `GR1-GR3 admitted round 47 (all three holds)` -> marks_ok=3  VERDICT= PASS
    H2 README `not admitted round 47: still pending` (control) -> marks_ok=2 VERDICT= FAIL
    (receipts: transcript-exp4.txt, exp4.sh — 1.7 s, three commits from lane HEAD f6bc6d05)

Impact: the machine verdict `PASS` and the human-readable gate record can contradict each other: a README (or a README line added by an agent that believes the gate failed) can say "Not admitted round 47: still pending" while the counter prints PASS and C1 admission is declared. Rule F2 is documented as "admission marks must not be grantable to negating text"; it is grantable to the first variant a person types. A deny-list is the wrong shape for a grant.
Smallest remediation (either; A is smaller and removes the whole surface): (A) make the README mark an exact line, exactly as MARK_SKILL already is — `MARK_README = 'admitted round 47: btrfs-scrub-grounding-r45.md (GR1-GR3)'` and `'readme': MARK_README in readme_lines`; or (B) keep prose and normalize before the test — NFKC + `\u00a0`->space + casefold + whitespace collapse, then a negation test on the 40 chars before and the text after `admitted round 47`:

    def readme_grant(lines):
        for ln in lines:
            s = ' '.join(unicodedata.normalize('NFKC', ln).replace('\u00a0', ' ').casefold().split())
            if not all(x in s for x in ('btrfs-scrub-grounding-r45.md', 'admitted round 47')):
                continue
            head, _, tail = s.partition('admitted round 47')
            if NEGATE_RE_2.search(head[-40:]) or NEGATE_RE_2.search(tail):
                continue
            return True
        return False
    NEGATE_RE_2 = re.compile(r"(?:^|[\s\u2014|(\[])(?:un|not|never|no|non)[\s\-]*admitted|pending")

  Verified by `.ufo/waves/round-47/w1/C1SentSafety/fixcheck.py`: A1/A2/A3/A4 -> False, both genuine grant lines -> True (transcript-fixcheck.txt).

────────────────────────────────────────────────────────────────────────
S2 — MEDIUM (availability of the verdict): CITE_RE is quadratic and reachable from any seat report body; a 1 MiB body stalls the gate for about an hour
────────────────────────────────────────────────────────────────────────
Site: `:83` `CITE_RE = re.compile(r'\b([A-Za-z0-9_.@+-]+\.[a-z0-9]+):(\d+)\b')`, applied to the whole report body at `:287` (`hits = CITE_RE.findall(body)`), invoked once per bound seat (`:344`, up to 24 bodies per run). `bind` accepts a body of any size (`:222` only enforces a 300-byte floor).
Cause: the leading class matches `.` itself, so on a single long token the engine restarts the token scan at every offset, and there is no `:` to end it -> O(n²) with no backtracking trick available. Possessive quantifiers do **not** fix this (measured below); the scan shape must change.
Evidence (this host, python 3.14.8):
    direct regex         4 KiB 0.044 s | 16 KiB 0.687 s | 64 KiB 11.07 s | 128 KiB did not finish in 30 s
    through the counter  8 KiB body: wall 0.30 s | 64 KiB body: wall 16.44 s (transcript-exp2.txt C1a/C1b)
    possessive variant   16 KiB 0.10 s | 64 KiB 1.50 s  -> still 16x for 4x bytes (transcript-fixcheck.txt)
    [INFERENCE] 1 MiB body ≈ 256 × the 64 KiB cost ≈ 45-60 min per bound seat; the counter has no timeout on it.
Reachability: the body is the seat's own report; the two binding lines need only the verdict word and the section digest, and the digest is computable by anyone (`--section-hash`). No hostile lane or host access is required.
Impact: the counted gate command (and the L1's receipt run) hangs without output; `git` is also invoked without `timeout=` (`:109`), so a stalled lane reproduces the same failure mode. A seat that emits a long unbroken token by accident (a pasted base64 blob, a URL without spaces) can hang the round.
Smallest remediation (measured, recall-preserving): split before matching and cap the token —
    CITE_CAP = 512
    def cite_hits(body):
        return [h for tok in body.split() for h in CITE_RE.findall(tok[:CITE_CAP])]
  -> 16 KiB 0.0008 s, 64 KiB 0.0012 s, 1 MiB 0.0012 s; on a real report body (`.ufo/waves/round-47/w1/R47CritGR1a.md`, 6063 B) the hit list is identical to the shipped scanner (33 hits, `True`). Add a body ceiling in `bind` (`if len(rest.encode('utf-8')) > 262144: return None, None, None, 'body too large'`) and `timeout=120` in `git()`.

────────────────────────────────────────────────────────────────────────
S3 — LOW/MEDIUM (evidence leg is satisfiable by a content-free quote): K22 quote containment accepts a fragment
────────────────────────────────────────────────────────────────────────
Site: `:278` `if norm(want) not in norm(got[line_no - 1]):` with `norm = lambda s: ' '.join(s.split())` (`:264`). Containment means a quote of a single character satisfies the leg.
Evidence: replacing GR1's first quote (entry line 27, `S246 cmdline.c:147`, "potentially suffixed with K, M, G, T, P, E.") with `"."` in a fixture keeps `quotes_ok= 3` and `GR1 quotes= {"bad": [], "ok": 12, "quotes": 12}`; the fabricated-text control (`"this sentence is nowhere in the source file"`) is caught (`quotes_ok= 2`, `bad: ["S246 cmdline.c:147: quote mismatch"]`). Receipts: transcript-exp1.txt B1/B2.
Impact: a row's evidence leg can stay green while its quotes carry no information — the leg stops distinguishing a grounded row from a fabricated one, which is exactly the property K22 was added for.
Smallest remediation: after computing `want`, `if len(norm(want)) < 24: bad.append(f'{sid} {fname}:{line_no}: quote under 24 normalised chars'); continue`, and optionally require `len(norm(want)) >= len(norm(got[line_no - 1])) // 2`.

────────────────────────────────────────────────────────────────────────
S4 — LOW (provenance precision): citations resolve by basename, not by the S-id the row pins
────────────────────────────────────────────────────────────────────────
Site: `:243` `cands = [lines for (sid, sf), lines in cache.items() if sf == fname]` and `:246`. The `sid` is discarded, and the line number only has to exist in *some* snapshot with that basename.
Evidence (direct call on the HEAD snapshots): `scrub.c` is pinned twice with different lengths — `('S237','scrub.c')` 2232 lines, `('S242','scrub.c')` 3338 lines — so `verify_citation(cache,'scrub.c',3000)` -> `(True, 'resolves')` although S237 has no line 3000; `3339` -> `(False, 'scrub.c:3339 outside all pinned snapshots')`. A GR1 report — whose row pins no `scrub.c` at all (`CITE['GR1'] = ('cmdline.c','vsprintf.c','kstrtox.c','sysfs.c')`, `:72-73`) — passes with `report_citations_ok(cache, 'anchors scrub.c:3000 and cmdline.c:147')` -> `(True, '2 citations resolve')`.
Impact: a seat can cite a line that exists only in the other revision of the same file, or in another row's snapshot, and the counter reports "citations resolve". Provenance is weaker than the report's own wording implies.
Smallest remediation: thread the row's quoted `(sid, fname)` set from `quote_legs` into `verify_citation` and require the pair to match (`if sf == fname and sid in row_sids`).

────────────────────────────────────────────────────────────────────────
S5 — LOW (integrity, defence in depth): the anti-contradiction leg is a case-sensitive ASCII deny-list
────────────────────────────────────────────────────────────────────────
Site: `:80` `ANY_VERDICT_RE = re.compile(r'ROW (GR\d) VERDICT: (\w+)')`, used at `:218`. Direct probes: `'ROW GR2 VERDICT: fails'` -> detected; `'row GR2 verdict: fails'`, `'ROW\xa0GR2 VERDICT: fails'`, `'R\u041eW GR2 VERDICT: fails'` (Cyrillic О) -> not detected; a homoglyph inside the verdict word IS treated as a contradiction (`'ROW GR2 VERDICT: \u0444ails'` -> `('GR2','фails')`), so the hole is the `ROW`/spacing side only. Impact: a report can bind GR1 while its prose states another row fails, without the check noticing. Remediation: normalize (NFKC, `\u00a0`->space, casefold, whitespace collapse) before the scan and use `r'row\s*gr(\d)\s*verdict\s*:\s*(\w+)'`; a full fix needs confusable folding, which is why this is filed as defence in depth, not as a gate.

────────────────────────────────────────────────────────────────────────
S6 — INFO (no escape today; no validation either): `--lane` is not checked, and an empty value silently grades the caller's CWD
────────────────────────────────────────────────────────────────────────
Site: `:303` `lane = os.path.abspath(a.lane)` — no directory check, no toplevel assertion, no rejection of `''`.
Evidence: `--lane ''` from /home/vgpnk/Projects/shokunin graded the **fleet** repo (`revision b9df86692509865ab3af157e2836f74480935e07`, `problems: ["GR1: header absent", …]`); `--lane <clone>/.ufo/waves` graded the enclosing clone (`revision f6bc6d05…, structural_ok 1`, transcript-exp2.txt E3). No write follows from either (see P7), so the impact is a wrong-repo verdict, not a write escape. Remediation: require `os.path.isdir(lane)` and `realpath(git -C lane rev-parse --show-toplevel) == realpath(lane)` (or `--lane-is-a-subdir` opt-in), and reject an empty `--lane`.
Adjacent, same site: `git()` (`:108-109`) inherits the environment, so `GIT_DIR` overrides `-C` — probed: `GIT_DIR=<other>/.git … --revision <lane sha>` -> `{"error": "cannot resolve <sha>"}`, rc 2, i.e. fail-closed rather than a cross-repo read (transcript-exp2.txt E2). Pinning `GIT_DIR`/`GIT_WORK_TREE` off in `env` would make this explicit; `core.fsmonitor` and `core.hooksPath` set inside a lane did **not** execute anything (canary not fired, E1).

────────────────────────────────────────────────────────────────────────
S7 — INFO (attacked, no exploit): a wave name reaches the report path unsanitised, but git rejects `/../` and the row fails closed
────────────────────────────────────────────────────────────────────────
Site: `:174` `out[name[:-len('-dispatch.json')]] = …` (the wave name is the file-name stem) and `:202` `rb = show(lane, rev, f'{WAVES}/{wave}/{seat}.md')`. A file `..-dispatch.json` in `.ufo/waves/round-47/` therefore yields `wave = '..'` and the report path `.ufo/waves/round-47/../<seat>.md`.
Evidence: `waves_seen= ['..']` — the wave IS accepted — `GR1 seat: {"detail": "no report ../R47RevGR1a.md", "hash": null, "verdict": null} bound= 0`; the underlying read fails: `git show <rev>:.ufo/waves/round-47/../R47RevGR1a.md` -> rc 128 `fatal: path … exists on disk, but not in <sha>` (transcript-exp3.txt F1, transcript-exp1.txt D1). `.` as a wave name fails the same way ("exists on disk, but not in"). Seat names themselves never reach a path: `bind` uses the frozen literal from `universe()` (`:87-93`) and only compares the dispatch `name` field (`:189`). Residual nit: the failure is only safe because git refuses to normalise `.`/`..` in `rev:path`; the detail string happily prints a `../` path. Remediation (cheap, belt and braces): reject a wave name that is not `re.fullmatch(r'[A-Za-z0-9_.-]+', wave)` and not equal to `.`/`..`.

────────────────────────────────────────────────────────────────────────
S8 — INFO: F1/F3/K23 and the digest pin hold under the same probes (no action)
────────────────────────────────────────────────────────────────────────
- F1 structural bound: `row_extent` (`:131-146`) rejects a duplicated row header and any `## ` line inside the extent; not defeated by any probe here.
- F3: a dispatch JSON with a duplicate key is discarded in-band (`waves_seen= ['w1','w9']`, `verdict= FAIL`, no traceback) — `:306` catches it (transcript-exp2.txt E4).
- K23: `distinct` (`:352`) is computed from bodies that already passed the citation leg, so padding cannot fake distinctness into `on_cur`.
- Snapshot digests: tampering with a pinned file invalidates the row's quotes (`quotes_ok= 1`; `GR2 ok= 12/28`, `S242 scrub.c: snapshot absent or digest moved`), and the substitution attack — copying the S237 bytes over the S242 path, the "second file with the same sha256 path" shape — is rejected (`quotes_ok= 2`, same reason). Digests are checked per literal path, so a renamed/replaced blob cannot spoof them (transcript-exp3.txt G1/G2).
- Verdict-line unicode: NBSP inside the binding line is rejected end-to-end (`first line 'ROW\\xa0GR1 VERDICT: holds'`, D1 seat b); the digest line is ASCII-only (`[0-9a-f]{64}`), BOM/CRLF forms fail `fullmatch`, and folding of the frozen marks is exact on U+2014 (writing the em dash as mojibake turned `marks.entry`/`marks.skill` false in my first H-run — fail-closed, benign, but it means a re-typed mark line silently earns nothing).
- `--revision` injection: `--help`, `--all`, `-h`, `HEAD:corpus`, `HEAD^!`, `nonexistent` all exit 2 with `{"error": "cannot resolve …"}`; a trailing newline is trimmed by git and resolves to the commit; downstream reads use the full sha printed by `rev-parse --verify` (`:313-317`), so the revision text cannot change which blob is read.

────────────────────────────────────────────────────────────────────────
P7 (positive control) — the counter writes nothing, even when mis-rooted
────────────────────────────────────────────────────────────────────────
`git -C <fixture> status --porcelain | wc -l` = 0 after a full run (transcript-exp3.txt), and `git -C /home/vgpnk/Projects/shokunin status --porcelain | wc -l` = 0 after the `--lane ''` mis-root run. No `open(...,'w')`, no temp files, no index touch: read-only by construction.

────────────────────────────────────────────────────────────────────────
NOT DONE / LIMITS
────────────────────────────────────────────────────────────────────────
- No 1 MiB end-to-end run (extrapolated from 4/16/64/128 KiB, flagged [INFERENCE]); the 64 KiB run is measured end-to-end twice (12.25 s and 16.44 s on a loaded host).
- No symlinked-lane, FIFO-lane, missing-git, or hung-FS test; the no-timeout point (`:109`) is code-level only.
- No 18-seat full-lane PASS fixture: the S1 bypass was proven with 6 well-formed reports over the committed w1 dispatch, which is enough to reach `PASS` while `marks.readme` is earned by a negating line, but it does not exercise every seat in the frozen universe.
- `exp1.sh` line 90 calls a non-existent `/usr/bin/time` (visible in transcript-exp1.txt); the timing evidence is exp2.sh C1a/C1b and fixcheck.py, not that line.
- No host mutation, no package/service/sysfs action, no `btrfs` command; no tool installed, so nothing to record under the tooling authorization.
- Scratch /fast/scratch/hyaku/tsukuroi-r47/C1SentSafety/ holds the four fixtures at report time and is removed on exit; the replay scripts and their transcripts are copied to `.ufo/waves/round-47/w1/C1SentSafety/`.
