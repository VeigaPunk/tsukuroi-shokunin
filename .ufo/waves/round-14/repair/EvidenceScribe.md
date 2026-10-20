# EvidenceScribe — round 14 source-count baseline (report only)

Lane: tsukuroi-shokunin. Seat: TsukuroiR14.EvidenceScribe (leaf). No edits outside this file.
Verification commands: none executed (no census, validate, gate, selftest or build).

## 1. Latest baseline closure

- Baseline `8606bad4cbc6451ac2890c9f8e2548a36c386db6` = HEAD. Subject: "round-13 verifier spot-check
  (integrator, hyaku): non-author admit/reject". Adds `corpus/lessons/round-13-verifier-spotcheck.md`,
  LOG.md, SCORECARD.md, `corpus/lessons/round-13.md`, `.ufo/reports/round-13/correction/verification-fixed.json`.
- Closure verdict (lesson, read at HEAD): status ok; admitted false; **verdict rejected-harmed**.
  Depth **harmed** (new MD:97 value-domain sentence contradicts systemd.exec(5) ProtectSystem= domain;
  S042 asserts a self-description absent from comment 6071740243). Coverage, operability, freshness,
  calibration, adjacency: unchanged. Routed defects 1-4 feed this round (MD:97 correction, S042
  supersession, stale S041 metadata in correction JSON, gate-contract over-specification).
- Working tree: `corpus/SOURCES.md` clean; only untracked `.ufo/waves/round-14/` present.
- `corpus/knowledge/source-scope-correction-r14.{md,json}` does not exist at 8606bad (expected; this round creates it).

## 2. Previous source counts (read via `git show <rev>:corpus/SOURCES.md`, python row regex
   `^ {0,3}\|\s*S\d{3,}\s*\|`, 13 fields per row, tier = col 5, status = col 9)

| rev | blob | rows | ids | malformed | A/B/C | mined/queued/rejected |
|---|---|---|---|---|---|---|
| 9574a18 (r13 closure baseline) | c79a6b6a | 40 | S001-S040 | 0 | 35/1/4 | 30/5/5 |
| e1fc8fd (r13 delivered) | 6e045d54 | 43 | S001-S043 | 0 | 36/1/6 | 31/5/7 |
| 8606bad (r14 baseline = HEAD) | 6e045d54 | 43 | S001-S043 | 0 | 36/1/6 | 31/5/7 |

- 8606bad and e1fc8fd SOURCES.md blobs are byte-identical. Both match the lesson's stated counts.
- Rejected at baseline: S029, S030, S033, S036, S037, S042, S043. Queued: S006, S012, S013, S018, S024.

## 3. Exact initial census disclosures at baseline (expected; before any r14 row lands)

Expected `validate` stdout for lane `tsukuroi`, exit 0 (W-codes never fail a clean lane):

```
tsukuroi	W04	S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi	W04	S041 duplicate url man.archlinux.org/man/systemd.exec.5 across scopes
tsukuroi	W04	S042 duplicate url github.com/omacom/omarchy/issues/8047 across scopes
tsukuroi	W04	S043 duplicate url github.com/omacom/omarchy/issues/6629 across scopes
tsukuroi	ok	/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

Provenance: the four W04 lines and the ok line are the lesson's observed output (r13 integrator,
same blob). Independently, I derived the same four rows from `scripts/sources-census.sh:644-645`
(W04 fires on the later row whose url is already seen under a different `scope_key`) plus a
python url/scope table over the blob: duplicates are systemd.exec.5 (S028/S041), access.2
(S034/S038), omarchy#8047 (S036/S042), omarchy#6629 (S037/S043). This is [INFERENCE] from source
reading, not a fresh run. `census` mode prints no W-codes; disclosures appear only in `validate`.

## 4. Predicted registry after r14 rows (conditional; [INFERENCE] from spec, not landed)

Spec adds S044 (docs, A, mined, ProtectSystem definition) and S045 (community, C, rejected):
rows 45; tier A37/B1/C7; status mined32/queued5/rejected8.

Conditions that change the warning set:
- S044 url `man.archlinux.org/man/systemd.exec.5` duplicates S028 and S041. With a scope string
  distinct from both, expect one new `W04 S044 duplicate url ... across scopes` line (6 W04 total).
- If S044 reuses S028's or S041's exact scope string, the row triggers **E04** (exit 1) unless its
  teaches contains `supersedes S0NN`. Avoid this by choosing a distinct scope.
- S045 url should be `api.github.com/repos/omacom/omarchy/issues/comments/6071740243`. Its host and
  path differ from S042's `github.com/omacom/omarchy/issues/8047`, so no W04 is expected. The
  first `https?://` token in the source cell determines the url, so the API URL must come first.
- S045 rejected: W02 fires if teaches is under 8 characters. Its used-by must be `—` or an existing
  path (E11 on a missing path). Rejected rows never trigger W03.
- S044 mined with used-by `corpus/knowledge/source-scope-correction-r14.md`: E11 unless that file exists
  when validate runs. W01 fires only for tier-C mined rows with used-by, so S045 must stay rejected.

## 5. Proposed reproducible commands (not executed here)

Lane census (default root is the shokunin root; pin it anyway):

```
cd /home/vgpnk/Projects/shokunin && scripts/sources-census.sh census tsukuroi --root /home/vgpnk/Projects/shokunin | sort
```

Expected lane lines at baseline ([INFERENCE]): `tsukuroi rows 43`, `tsukuroi tier.A 36`, `tsukuroi tier.B 1`,
`tsukuroi tier.C 6`, `tsukuroi status.mined 31`, `tsukuroi status.queued 5`, `tsukuroi status.rejected 7`.
Keys with count 0 are not printed by the lane census (awk prints only observed keys); the FLEET
lines always print zero defaults. `| sort` is needed because awk `for (t in ...)` order is not fixed.

Validate (warnings and exit code):

```
scripts/sources-census.sh validate tsukuroi --root /home/vgpnk/Projects/shokunin --today 2026-10-20; echo rc=$?
```

Blob-level histogram, independent of the census script, pinned to a revision (works for any rev):

```
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show 8606bad4cbc6451ac2890c9f8e2548a36c386db6:corpus/SOURCES.md | python3 -c '
import re,sys,collections
rows=[l for l in sys.stdin if re.match(r"^ {0,3}\|\s*S\d{3,}\s*\|",l)]
c=[[x.strip() for x in r.split("|")] for r in rows]
print("rows",len(c),"ids",len({x[1] for x in c}),"malformed",sum(len(x)!=13 for x in c))
print("tiers",dict(sorted(collections.Counter(x[4] for x in c if len(x)==13).items())))
print("status",dict(sorted(collections.Counter(x[8] for x in c if len(x)==13).items())))'
```

For the working tree after r14 edits, replace the `git show ...:corpus/SOURCES.md |` prefix with `cat corpus/SOURCES.md |`
(run from the tsukuroi-shokunin directory). Expected after r14 (conditional, section 4): rows 45, A37/B1/C7, mined32/queued5/rejected8.

## 6. Limitations

- No census, validate, gate or selftest was executed. Sections 3 and 5 expected outputs are inferred
  from script source and the lesson's observed output; they are not observed in this seat.
- Section 4 depends on S044/S045 scope, url and teaches choices that have not landed.
- Fleet-level FLEET totals were not measured; only the tsukuroi lane was read.
- Round-14 routed defects (JSON S041 stale `reserved`/`SourceRegistry` metadata; gate_contract
  over-specification) are outside this count task and were not inspected further.

## 7. Tooling

Installed or updated: none. Used existing `git` and `python3` for read-only blob reads. Read RULES.md
(tooling directive); no privileged probes, package transactions, or services were touched.
