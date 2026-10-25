# Round 12 — non-author verification and discernment spot-check

author: hyaku closure (non-author integrator, @m_strong)

Verified 2026-10-20. Baseline: `b76b5c377eaee3e3d8d47fdddde977828d05dbd5`.
Delivered revision: `f3868cdef07027f7ec8ecd095457d95108f75676`.
Report: fleet `.ufo/reports/round-12/tsukuroi.md`, committed by
`tsukuroi-shokunin` at `6800f05beba8d9e217b35cc81a5e1ab9c037f5da`.
The report-time pushed lane HEAD was `670126f5161b824d9dabdfacd085d27ff0afa3e3`;
the measured implementation was `70fede2a7a890cb50a72db2d4230ee541183bf7b`.

## Closure

**status: ok; admitted: false; verdict: rejected-harmed.** This is a substantive,
landed report, not a completion marker. Both numeric counters reproduce, and C1
runs successfully, but the new C2 knowledge entry introduces a source-inconsistent
exclusive condition. Do not aggregate that defect away against the other useful
additions. The integrator cannot repair lane-authored files or admit a future fix.
No promotion, mint or SHONEN checkbox change is performed.

## Step-1 conformance

Commands were executed from the fleet root, with the lane addressed explicitly:

```sh
git -C /home/vgpnk/Projects/shokunin log --format='%an %H' -- .ufo/reports/round-12/tsukuroi.md
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin status --porcelain
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-list --count '@{u}..HEAD'
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin merge-base --is-ancestor <hash> HEAD
git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin diff b76b5c377eaee3e3d8d47fdddde977828d05dbd5 f3868cdef07027f7ec8ecd095457d95108f75676 -- SCORECARD.md
```

Observed report history: `tsukuroi-shokunin 6800f05beba8d9e217b35cc81a5e1ab9c037f5da`.
Initial lane status printed no entries; ahead-of-upstream count was `0`.
The ancestry command exited 0 for baseline, implementation, report-time lane HEAD
and delivered revision above. SCORECARD changed by additions only; all six ordinal
scores remain unchanged. Its capability row and claim evidence are present.

The dispatched `.ufo/prompts/tsukuroi-round-12.md` carries the template's mission,
claims, frontier, batched-L2, report, commit/push, write-scope and L0 contract,
plus the operator's campaign addendum. An independent conformance reviewer found
no missing template contract item. Report sections are in order; `## SHONEN`
has four corresponding `[~]` lines. Author-side reviewers are not outside verifiers.

**Conformance defect — report did not land last.** The operator-identified late
seat write to `corpus/SOURCES.md` was committed at `f3868cd` after the report.
`git show --format=fuller f3868cd -- LOG.md corpus/SOURCES.md` shows only the
additional S027 source-reopening paragraph and its appended LOG erratum. No
registry row, implementation or counter changed; the filed report bytes were
preserved. This is a status-neutral ordering defect, not the reason for rejection.

Driver digest, copied from the closure assignment rather than drifting log lines:

```text
2026-10-19T23:10:56-03:00 launch tsukuroi round=12 pgid=12830 driver=hyaku slot=2 attempt=1
2026-10-19T23:24:27-03:00 lane-dead-no-report tsukuroi round=12; retry same round (hyaku: headless attempt ended by operator directive to run in-session)
2026-10-20T00:41:10-03:00 launch tsukuroi round=12 pgid=288324 driver=hyaku-inline attempt=1
2026-10-20T01:04:01-03:00 complete tsukuroi round=12; hyaku-inline attempt=1
```

The stale-lane disclosure identifies progressing committed work after the resumed
launch. The predecessor is not counted as a separate round or an honest pass.

## Claim rechecks

### C1 — operability / root-metadata-observer: improved

The delivered census bytes equal the committed `f3868cd` blob. Their SHA-256 is
`d17d32a35946c71c1fc195e36178aa383f4a04d7172cc579b6e9e25fa537f27e`, matching the report.
The persisted regex is `C1_pattern` in
`.ufo/waves/round-12/resumed/count-commands.json`. For each live run, count only
`PLANE packages:` lines matching that regex; the presence predicate is exit 0
when the count is nonzero, otherwise 1.

An initial verifier wrapper, `git show <rev>:tools/tsukuroi-census.sh | bash -s`,
failed before probing: `BASH_SOURCE[0]: unbound variable` (exit 1). Those attempted
runs are **not** baseline or delivered measurements. The successful baseline
invocation used an anonymous in-memory file descriptor to preserve BASH_SOURCE,
without a checkout or persistent script. Reproducer from the lane directory:

```python
import json, os, re, subprocess
revs = ['b76b5c377eaee3e3d8d47fdddde977828d05dbd5',
        'f3868cdef07027f7ec8ecd095457d95108f75676']
commands = json.loads(subprocess.check_output([
    'git', 'show', revs[1] + ':.ufo/waves/round-12/resumed/count-commands.json']))
for rev in revs:
    fd = os.memfd_create('tsukuroi-r12-census', 0)
    os.write(fd, subprocess.check_output([
        'git', 'show', rev + ':tools/tsukuroi-census.sh']))
    p = subprocess.run(['bash', '/proc/self/fd/' + str(fd)],
                       pass_fds=(fd,), capture_output=True, text=True)
    os.close(fd)
    count = sum(bool(re.search(commands['C1_pattern'], s))
                for s in p.stdout.splitlines() if s.startswith('PLANE packages:'))
    print(rev, 'count=', count, 'presence_exit=', 0 if count else 1,
          'census_exit=', p.returncode)
```

Observed baseline, via the memfd wrapper: `count=0 presence_exit=1 census_exit=1`.
Observed delivered bytes, run directly as `bash tools/tsukuroi-census.sh`:
`count=1 presence_exit=0 census_exit=1`.
Both successful probes emitted exactly this plane sequence:
`packages, systemd, drivers, journal, update-safety, oom`.
Both rollups were:

```text
TSUKUROI_CENSUS: DEGRADED (packages=DEGRADED systemd=HEALTHY drivers=DEGRADED journal=DEGRADED update-safety=DEGRADED oom=DEGRADED)
```

Delivered root observation:

```text
root_status=ok root_mode=0555 root_uid=0 root_gid=0 root_euid=1000 root_owner_write=absent root_owner_search=present root_report=owner-write-absent root_intent=not-assessed root_src=default root_dir=/
```

Capability demonstration executed now: `bash tools/tsukuroi-census.sh --selftest`:

```text
TSUKUROI_CENSUS_SELFTEST: PASS (97 cases, 97 passed, 0 failed)
```

Exit 0. Two additional explicit skips remained: non-root-owned fixture requiring
CAP_CHOWN; EACCES metadata fixture with 000-subtree/root-bypass limitations. Skips
are not passes. The named 0555 report-only case and package-early-return cases
passed. The prior committed policy-mutant evidence records exit 1, 93 passed /
4 failed with the stable 0555 finding; I inspected it but did not rerun a mutant.
No host repair, package transaction, service operation or privileged probe ran.

### C2 — depth: count reproduced, substantive claim harmed

Executed the exact persisted `C2_script` via
`python -c "$C2_SCRIPT" <revision>`, loading that string from the delivered
`count-commands.json`. Baseline stdout was `0\n`, exit 0; delivered stdout was
`4\n`, exit 0; both stderr streams were empty. This matches the reported 0→4.
The counter verifies nonempty fields and mined-row/used-by resolution, **not**
the truth of each branch sentence. An unchanged ordinal 8→8 is not itself a
failure or a reason to relabel a measurable claim exploratory.

The matrix genuinely adds useful DAC/search, read-only namespace, credential and
collision discriminators. Its independence from the census, ordinary-mkdir scope,
unmeasured live capability state and refusal to prove historical Btrfs causality
are explicit. However, `root-dac-decision-r12.md` R13 (line 86), also repeated in
its current-host explanation (line 53) and JSON B2 `limit`, asserts that **only**
`ProtectSystem=strict` or `ReadOnlyPaths=` can make `/` read-only through a unit.
That exclusivity is false. The same B2 discriminator correctly lists
`BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=` and `RootImage=`.

I independently reopened https://man.archlinux.org/man/systemd.exec.5.en:
`BindPaths=/BindReadOnlyPaths=` says the latter creates read-only bind mounts;
`TemporaryFileSystem=` accepts mount options such as `ro`. These mechanisms are
not excluded by `ProtectSystem=no` and empty `ReadOnlyPaths=`. The source-backed
statement is narrower: **among ProtectSystem values**, `full` does not cover `/`
and `strict` covers the hierarchy (subject to its documented exceptions).

This is not a cosmetic concern: the exclusive sentence can cause a reader to
dismiss an alternative unit-side read-only view. Correct operational commands
elsewhere do not make the contradictory factual condition true. The independent
matrix reviewer agreed that the false universal is substantive and C2 is
admissible only after correction. No such correction exists in the delivered
revision. C2's passing structural count cannot waive that requirement.

## Outside discernment spot-check

Source reviewer `CloseTsukuroiR12.DiscernmentAudit` was dispatched by this fresh
closure integrator, not by the lane. Sources below were reopened on 2026-10-20.
The integrator also directly reopened the packaged root policy and systemd.exec.

| Item | Lane decision | Reopened source | Outside result | Reason |
|---|---|---|---|---|
| S035 | Admit API-level errno distinctions | https://man.archlinux.org/man/mkdir.2.txt, ERRORS, man-pages 6.19 / 2026-02-11 | agree | EACCES, EROFS, EEXIST and EPERM are distinct documented cases; the source does not establish universal errno priority or Btrfs ioctl ordering. |
| S036 | Reject as host-cause support | https://api.github.com/repos/omacom/omarchy/issues/8047 and its `/comments` endpoint | agree | Unresolved community snapshot-restore report is not evidence of this host's create-time EACCES; a bot rebuttal is not authoritative host proof. |
| S037 | Reject as host-cause support | https://api.github.com/repos/omacom/omarchy/issues/6629 and its `/comments` endpoint | agree | Version-scoped dependency/config report does not establish the host's permission mechanism. |
| S040 | Admit present declarative root policy | `/usr/lib/tmpfiles.d/root.conf:10` | agree | Direct re-open reads `z / 555 - - -`; policy observation is not proof of incident-time causation. |
| C2 entry, lesson Gate lines 111–116 | Author-side admit subject to final measurement and outside closure | Matrix R13, JSON B2 limit; systemd.exec sections above | disagree as delivered | The unconditional exclusivity statement is unsupported and contradicts the entry's own broader discriminator; correction is still owed. |

New-row quote sample: S035's Gate quote, “path refers to a file on a read-only
filesystem.”, is verbatim at ERRORS → EROFS (9 whitespace-delimited words).
S040's “z / 555 - - -” is verbatim at local line 10 (6 tokens). The source critic
also found the located S036–S039 Gate excerpts in the reopened sources, within
the 25-word limit. No inaccessible source was represented as reopened.

One attribution defect: S036/S037 call `omarchybot` comments “maintainer-side”.
The comments are automated triage, not maintainer acceptance; the bot explicitly
defers to a maintainer. This does not reverse either rejection. Future registry
corrections must respect immutable fields and append superseding rows where needed.

## Required source census

Executed:

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi
```

Observed stdout, exit 0; stderr empty:

```text
tsukuroi W04 S038 duplicate url man.archlinux.org/man/access.2 across scopes
tsukuroi ok /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/SOURCES.md
```

Fields above are tab-separated in the original output. W04 is the disclosed
superseding access(2) row, not concealed warning-free output. A pinned-byte census
using `^\|\s*S\d{3,}\s*\|` and the eleven table cells reproduced baseline 34 rows
(A31/B1/C2; mined26/queued5/rejected3) → delivered 40 rows
(A35/B1/C4; mined30/queued5/rejected5). Counts are not an expansion verdict.

## Per-axis verdicts

| Axis | Verdict | Evidence |
|---|---|---|
| operability | improved | Root metadata 0→1, unchanged six-plane contract, live demonstration and 97/97 selftest. |
| depth | harmed | Newly admitted C2 prose and JSON contain the false exclusive unit-read-only condition above; useful branch additions do not cancel it. |
| coverage | unchanged | Existing rollback-net surface refined; no evidence of lost coverage or a new ownership surface. |
| freshness | unchanged | Dated observations and source reopens retained; no separate freshness claim or ordinal gain. |
| calibration | unchanged | Ordinal scores and historical-cause limits are candid; current outside rejection remains explicit debt. |
| adjacency | unchanged | PROVINCE/SKILL preserve sibling method and fleet-attribution boundaries; no ownership transfer. |

## Learning trends

- **expansion: harmed** — the root-metadata capability genuinely runs, but the new
  admitted matrix fails source/observation-separation criteria on the exclusive
  condition. LEARNING's admitted-entry failure rule is not offset by registry growth.
- **quality: harmed** — the policy/proxy/ordering corrections and regression suite
  are real improvements, but an unsupported current factual condition remains in
  the admitted procedure. It is now explicitly flagged by this outside review,
  not silently accepted as a stronger entry.
- **discernment: harmed** — outside review agrees with sampled API-source admit
  and community rejections, but disagrees with admission of the matrix as delivered.
  The disagreement has not yet become a lane correction or lesson-backed criterion.
  Existing QUALITY #14–16 and prior outside-disagreement learning are acknowledged,
  not mistaken for resolution of this new disagreement.

## Routed defects and boundaries

1. **tsukuroi / next steered round — blocking correctness:** narrow the exhaustive
   read-only-unit sentence everywhere it occurs in the MD current-host explanation,
   R13 and JSON B2 limit. Keep the valid ProtectSystem comparison and explicitly
   retain the alternate path-view mechanisms. Resolve this outside gate disagreement
   in the lane's own lesson/QUALITY evaluation, then seek fresh non-author verification.
   This closure does not pre-admit that future correction.
2. **tsukuroi / next round — conformance:** stop/join source seats before the final
   measurement/commit/report boundary. Preserve `f3868cd` and its LOG erratum as
   history; never rewrite the filed report to conceal the late write.
3. **tsukuroi / source attribution:** qualify bot versus maintainer authority for
   S036/S037 without editing immutable source-row fields in place.
4. **tsukuroi / evidence precision:** SC1/SC2 specify root-owned hypothetical
   inputs but cite caller-owned smoke controls as their actual basis; distinguish
   the inferred same-mode outcome from executed fixture identity. Replace stale
   mid-wave process language in the new note's QUALITY evaluation with an accurate
   landing-time account in the lane's next correction. These do not change C1's
   observed counts. S034 already has a superseding S038 row; no in-place rewrite
   or new mandatory one-row-per-section convention is requested.

The note is a status-neutral conformance record except for the explicit C2
correctness/admission finding. SHONEN remains operator-owned and not fully
checkable on this review: whole-SKILL no-oral-context execution is still unverified.
No `[x]` is authorized. Tools installed/updated by this verifier or its reviewers:
**none**. All lane-authored files remain untouched.
