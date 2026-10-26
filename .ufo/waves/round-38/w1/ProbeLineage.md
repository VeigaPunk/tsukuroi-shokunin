VERDICT: draft

Item D-4 (considerthese mining). The "probe lineage table" proposed in `considerthese/2026-10-25.md` (section "Self-improvement ideas", bullet 3) is buildable from committed bytes and is built below. Three premises in the proposal text are falsified by the bytes; the table therefore keys on `(path, commit)`, not on `path`, and runs to VERSION 8, not 7.

Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin` at HEAD `5edb6c2e0d0e47b731fb0cb50e5d2df5abb7aacf`, read-only. No probe, counter, gate or selftest was executed; every digest below is `sha256sum` (or `git show <rev>:<path> | sha256sum`) over bytes, and every defect is a quoted spot-check line.

## 1. Method and observed output

Working tree equals HEAD for all seven tracked probe files (`git status --porcelain` lists only untracked `.ufo/waves/round-38/…` paths), so the working-tree digest is the committed digest; each was re-derived per commit to cover the multi-commit paths.

```
$ cd /home/vgpnk/Projects/shokunin/tsukuroi-shokunin && for f in tools/probe-child-env-allowlist-r32.py … ; do sha256sum "$f"; done
d43f95ed8a740b71aac1ab412e769e011127eb4ae29646d12b2075a696cf0576  tools/probe-child-env-allowlist-r32.py
c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd  tools/probe-child-env-allowlist-r33.py
5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92  tools/probe-child-env-allowlist-r34.py
a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a  tools/probe-child-env-allowlist-r36.py
9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064  tools/probe-child-env-allowlist-r37.py
b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0  tools/probe-git-child-env-r31.py
c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c  tools/probe-git-env-residual-r30.py
```

Per-commit re-derivation (`git show <rev>:<path> > blob; sha256sum blob; grep -m1 '^VERSION = ' blob`) found **eight distinct frozen digests across the seven paths**, because two paths each host more than one frozen version:

```
probe-child-env-allowlist-r32.py @fe1ae02  sha=2521711bb4e60a42ddd7a4a026961b3ae4aadbe0cf9036251c96f382630853d5  VERSION=<none>
probe-child-env-allowlist-r32.py @44c8eee  sha=d43f95ed…  VERSION=<none>      (docstring label "Probe v2", r32.py:25)
probe-child-env-allowlist-r33.py @c2e69f3  sha=f34c3b88…  VERSION = 3
probe-child-env-allowlist-r33.py @965bc5d  sha=38a40583…  VERSION = 3
probe-child-env-allowlist-r33.py @9c89ff4  sha=c24f344b…  VERSION = 3
probe-child-env-allowlist-r34.py @6de666c  sha=35a87374…  VERSION = 4
probe-child-env-allowlist-r34.py @15c9ac0  sha=5231dbaf…  VERSION = 5
probe-child-env-allowlist-r34.py @3457f28  sha=5d0d5689…  VERSION = 6
probe-child-env-allowlist-r36.py @1e92680  sha=a2a5acac…  VERSION = 7
probe-child-env-allowlist-r37.py @29b22df  sha=9aee085b…  VERSION = 8
```

`grep -c VERSION` on `probe-git-env-leak.py`, `probe-git-env-residual-r30.py`, `probe-git-child-env-r31.py` and `probe-child-env-allowlist-r32.py` returns **0** in each: no literal `VERSION` constant exists before round 33. First commits were taken with `git log --diff-filter=A --format=%h -- <path>` and resolved full with `git rev-parse`.

**Independent cross-check.** Every digest above appears in a committed spot-check line, which is why I treat them as confirmed rather than merely computed: r30 `:88` (`c8f61996…`), r31 `:75` (`b168b9b8…`), r32 `:63` (`2521711b` → `d43f95ed…`), r33 `:50` (`f34c3b88…` → `38a40583…` → `c24f344b…`), r34 `:55-57` (`35a87374…`, `5231dbaf…`, `5d0d5689…`), r36 `:30-32` (`a2a5acac…`), r37 `:36` (`9aee085b…`).

## 2. Probe lineage table

Round assignment from the path name, confirmed against each file's own docstring (`r32.py:2`, `r33.py:2`, `r34.py:2`, `r36.py:21`, `r37.py:2`). Dates are commit author dates. "Retiring defect" is the defect that ended *this* version, quoted from the verifier spot-check where one records it.

| # | Version in bytes | Path | Frozen in | Commit (full) | Date | sha256 | Retiring defect |
|---|---|---|---|---|---|---|---|
| 1 | none (unlabeled) | `tools/probe-git-env-leak.py` | r29 | `81a061a67466c5e1be812814a895a4b5ed89b4ff` | 2026-10-22 | `46a55ce7b4ad3fa46d873aab6461ee067d67e22b0c2c4f0c508b2969827fcf80` | Four channels unmeasured plus the probe's own inherited `HOME`: "**Residual git-environment channels** … a PATH `git` wrapper, a per-user attributes file, enclosing-repo discovery, and the probe's inherited `HOME`" — `corpus/lessons/round-29-verifier-spotcheck.md:152` |
| 2 | none (unlabeled) | `tools/probe-git-env-residual-r30.py` | r30 | `8fb2cef081787ccb52b38e9f74d95d2a480de18f` | 2026-10-22 | `c8f61996f0cea828c9b88f509a29bb6e09fc6de23ccd2b7f4084efb0d84cb68c` | Exit-code/canary parity only, so a hollow fix scores 0; loader injection invisible: "stdout comparison (hollow fixes score 0)" — `round-30-verifier-spotcheck.md:183`; "`LD_PRELOAD`/`PYTHONPATH`" — `:184` |
| 3 | none (unlabeled) | `tools/probe-git-child-env-r31.py` | r31 | `f4861f4d5c0d03ad769a74e0bcab61b5c6f0877c` | 2026-10-22 | `b168b9b86cc125e5207cd359a37e6d7dad6fc2b1d1c601836ddbe4cc7a68d8b0` | Injects 3 names by value; deny-list copies pass and 36 other names reach children: "The contract is a deny-list: `BASH_ENV`, `GCONV_PATH` and 36 more names still reach children" — `round-31-verifier-spotcheck.md:95`; "7 probe mutants survive the battery (MutProbeC2), and `dotgit-pointer` gave 2 spurious verdicts in 121 runs" — `:97` |
| 4 | "v1" (no constant) | `tools/probe-child-env-allowlist-r32.py` | r32 | `fe1ae02cdf60aca141abf70400a850c59f239576` | 2026-10-22 | `2521711bb4e60a42ddd7a4a026961b3ae4aadbe0cf9036251c96f382630853d5` | **Author pre-data amendment, not a verifier finding:** "Probe v2 (pre-data amendment after wave-1 CritAntiLoop: a filter keyed on the v1 length range 2-20 could keep longer unknown names)" — `tools/probe-child-env-allowlist-r32.py:25-26`; the v1→v2 digest step is recorded at `round-32-verifier-spotcheck.md:63` |
| 5 | "Probe v2" (no constant) | `tools/probe-child-env-allowlist-r32.py` | r32 | `44c8eee550a5dd7fa3729324f8dc77ececa3277b` | 2026-10-22 | `d43f95ed8a740b71aac1ab412e769e011127eb4ae29646d12b2075a696cf0576` | Exclusion list never injected, so 4 mutants survive: "**C2 probe exclusion-list blind spot.** Assert the fixed child environment … or inject a sentinel value for excluded names (HOME, TZ, TERM, PATH), so MutAllowlist m3–m6 die" — `round-32-verifier-spotcheck.md:139`; confirmed as origin in `tools/probe-child-env-allowlist-r33.py:3-8` |
| 6 | `VERSION = 3` (three digests, one version) | `tools/probe-child-env-allowlist-r33.py` | r33 | `c2e69f3e863ff3332e99eae5c419c286435ff123` | 2026-10-23 | `f34c3b8831369baee6a2f9151f1ecf8839528302e50615970ad655d45da152d2` | Not defect-retired: C1 verified under it (`round-33-verifier-spotcheck.md:130`), then superseded by a wider target set (`r34.py:6-11`). Carried, unresolved defect: "the probe's `is_git` recognises only `/usr/bin/git` and `/usr/lib/git-core/`" — `round-33-verifier-spotcheck.md:182` |
| 6a | `VERSION = 3` (amendment) | idem | r33 | `965bc5d965ac20cd4ed6a25a785571884262a89c` | 2026-10-23 | `38a405837f7aa0dc9bb4e04c0851e44f5f0d6ba8429e0683ba21f1f3f38d8864` | Pre-control amendment (source channel hardened); additive only — `round-33-verifier-spotcheck.md:67` |
| 6b | `VERSION = 3` (amendment) | idem | r33 | `9c89ff4f093d07a6f92925518310ca6a7c8a2fa0` | 2026-10-23 | `c24f344b864a13ea4db2909bfa81de77f8f41bae35cd5e0949a88b28ab1e04cd` | Attempt-2 amendment; 54 attempt-1 receipts had already scored under the prior bytes — `round-33-verifier-spotcheck.md:65-66` |
| 7 | `VERSION = 4` | `tools/probe-child-env-allowlist-r34.py` | r34 | `6de666c427ba9aa6b4350561980bde8d0e7c261d` | 2026-10-23 | `35a87374eb89239af841a015965518d63e40de7ac556041f1b0f366a993fa5a8` | Replaced pre-data by amendment 1 (claim-base parity clause) — `round-34-verifier-spotcheck.md:55`; the round simultaneously broke its own freeze promise: "**Freeze breach (recorded; it does not change the verdict).**" — `:69` |
| 8 | `VERSION = 5` | idem | r34 | `15c9ac0e1b02917f43c0bc016d6060f888cb603a` | 2026-10-23 | `5231dbafc472ff42e041cbaad3f48dd8bd204d58b6ab22e497cf9372b23d6bfd` | Replaced pre-data by amendment 2 (any-name ambient value clause, `execveat`/unparseable clause) — `round-34-verifier-spotcheck.md:56`; amendment 2 also narrowed the reading after a seat reported it — `:73` |
| 9 | `VERSION = 6` (spans r34–r35) | idem | r34 | `3457f287e04f34e73f8e70d4417b14b96f903f56` | 2026-10-23 | `5d0d568901c0eeb1c301b3bf825a839d4f41af68bc51e4de40f0706f15d1aa92` | Read-side gap: two ambient-copy mutants read 0/27 while really leaking: "**C1 counter, read side (R34-COUNTER-READ-SIDE-GAPS):** an untraced observation view of child environments" — `round-34-verifier-spotcheck.md:184` (ruling `:67`); still the live counter in round 35 — `round-35-verifier-spotcheck.md:89` |
| 10 | `VERSION = 7` | `tools/probe-child-env-allowlist-r36.py` | r36 | `1e926801195e304950e3eb9d2525ef8bbc245089` | 2026-10-24 | `a2a5acacaf5660754b39238a74d503c22c2241498012f6ee24c6aa27b4af443a` | Crash, vacuity, and a silent channel: "S1 clone-branch crash … S3 livefive vacuity gate; S4 `os.get_exec_path()` ambient PATH shape; parameter-named-`env` source rule" — `round-36-verifier-spotcheck.md:102`; "the frozen counter as shipped cannot certify the after state (S1 crash, S3 vacuity, S4 silent channel, parameter-named-`env` source rule)" — `:55-56` |
| 11 | `VERSION = 8` | `tools/probe-child-env-allowlist-r37.py` | r37 | `29b22df142efb5479333af9d57ecbd069462ba05` | 2026-10-25 | `9aee085b45d7566d6ce398733c10d3d87ae29bce107c4bd13fcdffcb4854b064` | **Live — not retired.** Its own retirement case is already recorded, unmet: no per-fix mutant receipt ("So the conjunct is unmet" — `round-37-verifier-spotcheck.md:39`), the only kill ran under V7 (`:40`), and "a name-level source set cannot see it" (`:128`) |

Receipt with the raw digest lines: `.ufo/waves/round-38/w1/ProbeLineage/digests.txt`.

## 3. Pattern statement

**The defect class that recurs is a clean zero that is indistinguishable from an unobserved zero.** Ten of the eleven versions have a recorded reason for ending, and six of those reasons are the same shape: the counter's pass condition is "measured 0" while its observation key — the injected name set (r31, `round-31:95`), the fixture length range (r32 v1, `r32.py:25-26`), its own exclusion list (r32 v2, `round-32:139`), exit-code-plus-stdout parity (r30, `round-30:183-184`), exec-witnessed tracing only (r34 v6, `round-34:184`), or a name-level source set (r37, `round-37:128`) — is narrower than the channel space, so a leaking control reports a clean 0 and the number reads as evidence. The remaining four are two author pre-data amendments that widen the input key under time pressure (r32 v1, r34 v5), one scope supersession with the defect carried forward rather than fixed (r33 v3 → r34 v4, `round-33:182`), and one crash (S1) that travels with the same vacuity debt. Every fix so far widens the key; **no version adds a standing positive control that proves the channel could have observed a leak in that run**, which is why the class returns: VERSION 8's own outstanding debt is again a sensitivity/vacuity debt (`round-37:39-40`), not a new class. Read as a series, the lineage is not converging on a stronger instrument so much as re-deriving the same lesson at a larger radius — six rounds (31→37) and eight digests without a certified close.

## 4. Findings against the proposal text

1. **"VERSION 1 to 7" is falsified in both directions.** The tip is `VERSION = 8` (`tools/probe-child-env-allowlist-r37.py:314`, frozen in round 37 at `29b22df`, digest confirmed at `round-37-verifier-spotcheck.md:36`). There is no literal VERSION 1 or 2: `grep -c VERSION` is 0 for the r29, r30, r31 and r32 files, and r32's two frozen states are labeled only in prose ("Probe v2", `r32.py:25`). Any table keyed on the integer would silently drop rows 1–5.
2. **A path is not a version.** `tools/probe-child-env-allowlist-r34.py` hosts three frozen versions (4, 5, 6) across three commits, and `-r33.py` hosts one version across three digests (3 frozen, then two pre-data amendments). Keying the table on filename would collapse eight frozen digests into seven rows and three of them would be wrong.
3. **The proposal's causal story is right but its class count is not.** The proposal says the table would "show whether the same defect class keeps returning". It does, and it is a single class (§3), but the mix also contains a scope supersession and two self-amendments that no counter defect explains; a table that lists only "the defect that retired it" would attribute r33 v3 and r34 v4/v5 to defects they did not have. The table above adds a defect-provenance column distinction (verifier finding vs author amendment vs supersession) for that reason.
4. **`considerthese/2026-10-25.md` is stale on the round axis, not just the version axis.** It states "Round 37 has not been declared" and "The last lane commit is still the round-36 verifier spot-check (`564db0b`)"; the lane now carries round-37 commits (`29b22df`, 2026-10-25) and a round-38 declaration. The three "open debts" it lists (probe VERSION 8, three C2 journalctl corrections, the `04:4043Z` stamp) are partially closed: VERSION 8 exists and is frozen, and its own sensitivity debt is now the open item (`round-37-verifier-spotcheck.md:39-40`).

## 5. Limits and what I did not do

- I did not execute any probe, counter, gate or selftest, and I make no claim about their behaviour; every claim above is a digest, a commit fact, or a quoted line.
- Digest-to-spot-check agreement (§1) confirms the bytes are the ones the closures read; it does not confirm the closures' verdicts.
- Row 6's "not defect-retired" reading rests on `round-33-verifier-spotcheck.md:130` (C1 verified) plus `r34.py:6-11` (target set widened); I did not read the round-33 declaration's own reason for a new round.
- The `probe-git-env-leak.py` row (r29) is outside the item's listed range; I included it because `probe-git-env-residual-r30.py:12-14` names it as the ancestor and the lineage is otherwise rootless. Its defect citation is `round-29-verifier-spotcheck.md:152`, which I read directly.
- Lane untouched: no git add/commit/stash/checkout/reset, no jj command, no write outside `.ufo/waves/round-38/w1/ProbeLineage.md` and `.ufo/waves/round-38/w1/ProbeLineage/`. Scratch under `/fast/scratch/hyaku/tsukuroi-r38/ProbeLineage/` was removed. No tool installed; no host change; no sudo.
