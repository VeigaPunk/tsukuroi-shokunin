VERDICT: defect-found

Item C1-9 — mutation probe of `probe_scrub_record` (tools/tsukuroi-census.sh @ 7e081698d4fc3c4ea944884fd093058de9909de1), scored with the frozen C1 counter.

Result: 6/12 mutants killed; **5 behaviour-changing survivors** (counter gaps, each named below); 1 identity-true survivor. The milestone "counter kills arm mutants" holds for every site with direct fixture coverage, and fails for: detail-segment order, multi-zero limit forms, non-instance timer names, readable-but-unsearchable sysfs roots, and (draw-dependent) empty-line speed content and tmp/progress-only record state.

# Setup and integrity
- Counter verified frozen: `sha256sum tools/score-scrub-arm-r44.py` → `1409a5fd75adaa4c0a238a7f9ad31621dd34a52ad1a40483e4a18d27c9536388` (matches SCORECARD declaration). Run: `python3 tools/score-scrub-arm-r44.py --revision <sha> --scratch /fast/scratch/hyaku/tsukuroi-r44/C1MutArm/s --lane <fixture-clone>` (for mutants `--lane` is the fixture clone; with the lane repo the counter errors `cannot resolve <sha>`, receipt mut-a.json first attempt).
- Baseline (pristine 7e081698): **PASS** — rc=0, cases=16 correct=16 identity_ok=1 wired_ok=1 live_agree=1 selftest_pass=1 selftest_r44=9 (pristine-baseline.json). Live leg: `SCRUB btrfs-scrub-record state=NONE dir=absent records=0 tmp=0 sockets=0 unreadable=0 orphan=0 limited=0 timers=0` (host has one fsid `1d02a454-…`, scrub_speed_max=`0`, no /var/lib/btrfs, no btrfs timer links — observed read-only).
- Fixture recipe per tasking: `git clone -q --shared` into /fast/scratch/hyaku/tsukuroi-r44/C1MutArm/base, origin removed, `rev-parse --show-toplevel` == that dir, pristine checkout of 7e081698, one mutation per commit with `-c user.name=fixture -c user.email=fixture@invalid`.
- Before/after hashes: pristine worktree sha256 `fca419b4714f7d24314b8d5877f0992c7f326aa8ff80045743990d058e8eaa1c`; after all probes, checkout of 7e081698 restores it byte-identical (`git status --porcelain` empty, fixture HEAD = 7e081698). Lane repo untouched by me: lane HEAD still ff2c264a7f7b3fe4aec694ded959566f8f5b7d33; the only lane worktree change (` M tools/tsukuroi-census.sh`, +46/−3: a `sysfs:not-directory` split and a timer-directory skip) is a concurrent seat's in-progress draft — none of my 12 mutants match that content; my writes in the lane are limited to this seat dir.
- Receipts (this dir): `pristine-baseline.json`, `mut-{a..l}.json` (counter output lines), `mut-{a..l}.diff` (each mutant's exact hunk vs 7e081698), `mut-e-r{2..4}.json` (reruns), `harness-cases.txt` + `harness-case.sh` (survivor delta harness + transcript).

# Per-mutant results (site = tools/tsukuroi-census.sh @ 7e081698; full context in mut-*.diff)

| id | site | verdict | correct | wrong ids | wired_ok | live_agree | selftest_pass | classification |
|----|------|---------|---------|-----------|----------|------------|---------------|----------------|
| a | :1968 drop `local LC_ALL=C` | PASS (rc=0) | 16/16 | — | 1 | 1 | 1 (9 R44 labels) | **survived, identity-true on this host** |
| b | :2008 records `[ -r ]`→`[ -e ]` | FAIL (rc=1) | 13/16 | root-records-unreadable, orphan-records, progress-socket | 0 | 1 | 0 | killed |
| c | :2009 orphan test `!=`→`==` | FAIL | 11/16 | recorded-readable, root-records-unreadable, orphan-records, tmp-beside-record, progress-socket | 1 | 1 | 0 | killed |
| d | :2015 progress `[ ! -S ]`→`[ ! -e ]` | FAIL | 15/16 | wrong-types | 1 | 1 | 0 | killed |
| e | :1989 `^[0-9]+$`→`^[0-9]*$` | PASS ×4 runs | 16/16 | — | 1 | 1 | 1 | **survived (draw-dependent killer exists, P≈1/8/run, missed 4/4)** |
| f | :2029 drop bare-timer skip | FAIL | 15/16 | timers-enabled | 1 | 1 | 0 | killed |
| g | :2019 drop `sysfs:absent` | FAIL | 16/16 | — | 1 | 1 | 0 | **killed via S leg only** |
| h | :1992 `[[ $v =~ ^0+$ ]]`→`[ "$v" = 0 ]` | PASS | 16/16 | — | 1 | 1 | 1 | **survived** |
| i | :2035 RECORDED iff rec>0 | FAIL | 15/16 | mixed | 1 | 1 | 1 | killed (draw-dependent; landed 1/1 runs) |
| j | :2037 `detail+=$info`→`detail=$info$detail` | PASS | 16/16 | — | 1 | 1 | 1 | **survived** |
| k | :2027 glob `btrfs-scrub@*.timer`→`btrfs-scrub*.timer` | PASS | 16/16 | — | 1 | 1 | 1 | **survived** |
| l | :1974 drop `-x` from sysfs-root check | PASS | 16/16 | — | 1 | 1 | 1 | **survived** |

Mutant commits (fixture clone): a=e771cf75, b=e1b15a43, c=1b41d1c1, d=e5c0e6c9, e=eea8a91f, f=4de2931d, g=b625e632, h=5d3f17a2, i=1ce2ed5c, j=01cec53a, k=92f68d90, l=1aeacb9a.

# Survivors: behaviour deltas (proven on constructed fixtures, uid 1000, LANG=en_US.UTF-8; harness-cases.txt)

- **(e)** speed content `\n` (one empty line): pristine `state=BLOCKED … detail=12345678:1:speed-malformed`; mutant `state=NONE … limited=1 detail=12345678:1:speed_max=` (empty value; BLOCKED→NONE flip). Killer is only drawn when the `speed-malformed` case picks `'\n'` from an 8-way choice (tools/score-scrub-arm-r44.py:403) — P≈1/8 per run; 4 runs missed (consistent, (7/8)^4≈0.59). **Gap case:** pin one malformed device to the empty-line content (dedicated `speed-empty-line` case), or always include `'\n'` in the drawn choice.
- **(h)** speed content `00\n`: pristine `limited=0` (zero forms are "no limit" per regex `^0+$`); mutant `limited=1 detail=12345678:1:speed_max=00`. No leg ever draws a non-canonical zero: every drawn zero is exactly `'0\n'` (counter :393,:403,:431) and the selftest uses `0` and `104857600` (census :3251). **Gap case:** add `'00\n'` to the drawn speed choices (or a third device with `00` in the `scrub-limited` selftest).
- **(j)** detail order: pristine `detail=record:not-regular,12345678:1:speed_max=104857600`; mutant `detail=12345678:1:speed_max=104857600,record:not-regular`. No leg ever combines a block-reason flag with a `speed_max=` pair: limited-devices is info-only, speed-malformed/unreadable are flag-only, `mixed` draws only plain files (flags never co-occur with info), the W-leg mixed draw likewise, the live host has no flags and no limits, and the selftest cases are each one-sided (`scrub-limited` :3251 vs `scrub-speed-malformed` :3257). The contract pins the order ("block reasons … then the speed_max pairs", counter docstring order clause). **Gap case:** one namespace case (or selftest device) combining a symlinked record with a limited device.
- **(k)** a plain `btrfs-scrub.timer` (no instance) link in wants: pristine `timers=1`, mutant `timers=2`. The drawn pool (counter :363-366), the `timers-enabled` case (:416) and the selftest `scrub-timers` (census :3271) contain no such name, and the live host has none (fstrim.timer only). For every `@`-bearing name the globs agree. **Gap case:** add `btrfs-scrub.timer` to `timer_names()`/the `scrub-timers` fixture.
- **(l)** sysfs root readable but not searchable (mode 0444) with one readable record: pristine `state=BLOCKED … detail=sysfs:unreadable`; mutant `state=RECORDED records=1 orphan=1` (the arm then judges every record an orphan against an fsid set it could not stat). No leg constructs r-without-x: the `unreadable` fixture is 0700, which denies r to the scored uid (1000) so both versions block it, and the live /sys/fs/btrfs is r+x. **Gap case:** `root_modes {'/sys/fs/btrfs': 0o444}` plus a record entry.
- **(a)** identity-true here, not merely undetected: with `LANG=en_US.UTF-8` (which the counter passes through to the case env, minus TSUKUROI_*/UFO_*/TMPDIR) and an uppercase-hex record + `_tmp` + mounted-fsid fixture, pristine and mutant produce byte-identical lines; observed `LC_ALL=en_US.UTF-8 bash -c '[[ ABCDEF =~ ^[a-f]+$ ]]'` → NOMATCH (no collation-range widening on this bash/glibc), and every output fragment is either nameless (flags), or ordered by name families whose relative order is identical under both collations. Remaining exposure is to other locales/glob collations, which no leg varies. **Gap case (weakest of the set):** run one case under a locale with divergent collation and two fsids whose `fsid8` order differs there; absent such a locale on the host, this mutant is equivalent for this grammar.

# Kill-path observations worth keeping
- **(g) died only through the selftest:** namespace cases and the W leg cannot see `sysfs:absent` because the inner harness always mounts tmpfs over `/sys/fs/btrfs` (counter INNER, mount of ROOTS; :87-95), and the live host has the directory. Its 16/16 + wired_ok=1 + live_agree=1 with FAIL verdict shows the S leg is load-bearing for that branch. Gap case for an N/W leg: an inner view that mounts only `/var/lib` and `/etc/systemd/system` (leaving no sysfs root) plus one readable record → pristine `state=BLOCKED detail=sysfs:absent`, mutant `state=RECORDED`.
- **(c)** kill is robust (5 case ids + the selftest `scrub-recorded` pin `orphan=0` for a mounted record, census :3236), but the `scrub-tmp-orphan-unreadable` selftest case is blind to the inversion by coincidence: pristine and inverted both read `orphan=1` there (mounted 000-record vs foreign record counts tie).
- **(i)** killed when the `mixed` draw produces a tmp-only/progress-only directory (status 0.7 / tmp 0.4 / progress 0.3 per fsid, counter :431-441); a dedicated tmp-only case (or selftest) would make it deterministic.
- Draw-dependence means single counter runs understate coverage for (e)/(i); the frozen control battery runs the counter once per revision.

# Not done
- No reruns beyond the listed ones (e ×4, others ×1); no concurrency/stress probing of the counter itself; no judgment of the concurrent lane worktree edit described above.
