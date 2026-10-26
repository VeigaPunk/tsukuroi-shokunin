VERDICT: defect-found

Item C1-14 — sweep for the early-reader-under-pipefail class OUTSIDE the frozen sites, at 447662088dfd3155e31aed239179a79c1d1046c7. A routing report, not a claim. Read-only: sources were extracted with `git archive 447662088… tools` into scratch (the lane tip is 87c4f7c6; the commit named in the item is an ancestor, so line numbers below are the 4476620 blobs: census blob ed83079c…, 3201 lines; boot-chain-audit.sh 1297 lines). Scratch removed at the end; receipts in `.ufo/waves/round-42/w1/C1SweepSites/`.

## Scope found

Shell files outside `.ufo/` at 4476620: exactly two, `tools/tsukuroi-census.sh` and `tools/boot-chain-audit.sh` (`git ls-tree -r --name-only 4476620 | grep -v '^\.ufo/' | grep -E '\.sh$|bin/'`). Python tools run bash only through `check-self-assessment.py:195` (`bash tools/tsukuroi-census.sh --selftest`) and the counters' stub dispatchers (`score-census-handoff-r32.py:113`, `score-size-invariance-r42.py:236`); the dispatchers' pipelines contain no early reader (`sed -n 1940,2110p tsukuroi-census.sh | grep -nE '\|'` -> only `exit 97` line). The round-42 hostcap `capture.sh` (`set -uo pipefail`, 18 lines) has one `| head -n1` on a systemctl one-liner, no pipe-buffer risk. Modes: census `set -euo pipefail` (:423; unguarded probe calls at :3149-3159 so a failing bare assignment kills the script); `cap()` toggles `set +e` around the capture only (:581-584); boot-chain-audit `set -uo pipefail` (:139, NO `-e`).

## Commands (run in the extracted `tools/` dir)

```
grep -nE '\|\s*(grep\s+(-[a-zA-Z]*q[a-zA-Z]*|-m ?[0-9]+|--quiet|--max-count)|head\b|sed\b[^|]*[0-9$]?q|awk\b[^|]*exit|sed -n[^|]*q|tail\b)' tsukuroi-census.sh      # 30 hits (grep-narrow-census.txt)
grep -nE '\|\s*(grep\s+(-[a-zA-Z]*q[a-zA-Z]*|-m ?[0-9]+|--quiet|--max-count)|head\b|sed\b[^|]*q|awk\b[^|]*exit)' boot-chain-audit.sh                                          # 374,379,384,483
grep -nE '\bhead\b|grep +(-[a-zA-Z-]* +)*-[a-zA-Z]*[qm]|grep +--(quiet|max-count|silent)|exit *[;}]|[;{] *exit\b.*\}|sed +(-[a-zA-Z]+ +)*.*[0-9$/]q|-quit|\bread +(-[a-zA-Z]+ +)*[a-zA-Z_ ]+ *< *<\(|\|\s*(read|while read|\{ *read)|\bcmp +-s|\bsort .*\| *head|\bgrep -[a-zA-Z]*l\b|\bgrep -[a-zA-Z]*L\b|\btimeout\b' tsukuroi-census.sh boot-chain-audit.sh   # 50 hits (grep-broad.txt)
grep -nE "awk.*\bexit\b|sed .*(;|[0-9'\"])q['\"; ]|\bsed (-[a-zA-Z]+ )?['\"]?[0-9$]*q|\| *(read|while|cmp|diff|sed -n [^|]*q)|\bhead -c|\bfirst\b.*\|" tsukuroi-census.sh boot-chain-audit.sh
grep -nE '\| *(grep|awk|sed|head|tail|sort|cut|tr|wc)' boot-chain-audit.sh      # every pipeline in the audit
```

Result: after 4476620 NO `printf|grep -q`, `grep -m`, or `printf|head` remains on a probe buffer in the census apart from the intended fixes (:695/:697 here-strings; update lists `awk 'NR <= 3'`/`'NR == 1'` at :1624,:1639,:1645,:1655). `grep -c`, `tail`, `sed -n 1p` (boot-chain-audit :909-:1164; sed does not quit at line 1), `sed -nE 's///p'`, `awk … END` are full readers and never SIGPIPE their producer.

## Evidence measured

1. Threshold is NOT 64 KiB in practice. `race.sh` (receipt) = 300 runs of `set -uo pipefail; printf '%s\n' "$buf" | grep -q '^match'` with the match on line 1, host load average ~16:
   `bytes=8118 false=0`; `16219: 0`; `32422: 8 and 11 (two runs)`; `48624: 119 and 191`; `60776: 239 and 275`; `65839: 268`; `70903: 294`; `101282: 299`; `303814: 300`; `1012675: 300` (race-matrix.txt has the second set). So a false pipeline status starts around 30 KB and is ~certain above 64 KiB, because bash's printf writes in 4 KiB stdio chunks and the reader can exit between chunks. The frozen counter's 1 MiB padding is the conservative end; sites whose input can reach 30-64 KiB are exposed too.
2. Bare-assignment kill under `set -e`: `t3.sh` (`set -euo pipefail; bn=$(printf '%s\n' "$base_txt" | awk … '$1==n{print $2; exit}')`, base_txt 100 KB, match on line 1) -> `survived` never printed, `t3 rc=141`.
3. Real sizes on this host (read-only, 2026-10-26): `pacman -Qq` 16287 B / 1409 lines; `-Qm` 539 B; `-Qu` 136 B; `-Sl` 481700 B; `journalctl -b -p err -o json` 222998 B; cgroup `memory.events*` path list 208 paths / 19218 B; enabled user timers 92 B.
4. Census output size seen by the selftest assertions: instrumented copy (scratch only; added `printf ${#out}` after `set -e` at :2174) — 127 `check` cases, max `${#out}` = 2642 B (`sizes.log`), selftest PASS 130/130 rc=0 (`selftest-tail.txt`).

## Site table (census, `tools/tsukuroi-census.sh`)

Columns: input >64 KiB (or >30 KB race zone) on a real host? / SIGPIPE effect / neutralised?

| site | pipeline | input | effect if SIGPIPE | neutralised |
|---|---|---|---|---|
| :676 | `mapfile < <(printf CAP_OUT \| grep -v … \| head -n "$SAMPLE_N")` (`-Qq`) | 16 KB here; >30 KB needs ~2800 pkgs (plausible only on very large installs) | none on the verdict: producers die inside the process substitution, `mapfile` gets the first N names as designed | yes — process substitution isolates pipefail; status never read |
| :743 | `bn=$(printf base_txt \| awk '$1==n {print $2; exit}')` bare assignment in a `while` over live `-Qm` rows | base_txt = foreign baseline (R6 embedded or `TSUKUROI_FOREIGN_BASELINE` file); real host 539 B. >64 KiB needs ~2000 baseline rows, a hand-fed override only | **kills the census, exit 141** (t3.sh); the awk exits on first match so any name matched in the first chunk triggers it | NO (no `|| true`, errexit live). Same shape as the fixed :1621-:1652 sites; residual, low reachability. Fix: `awk … '$1==n {print $2}' <<<"$base_txt"` with `{r=$2} END{print r}`/or here-string and `exit` removed |
| :798 | `grep -hE '^HoldPkg' FILE \| head -n1 \| sed … \|\| true` | pacman.conf lines, <1 KB | none | yes `|| true`; producer is a file grep, status unused |
| :931, :969, :1426, :1501 | `printf CAP_OUT \| head -n1 \| tr \| sed` | one word / one line (`is-system-running`, `show --value`, `is-active`) | assignment status is the last stage (sed/tr), `head -n1` on 1 line: even a SIGPIPE'd printf only lowers the middle status; with pipefail it WOULD kill under set -e (bare `state=$(…)`/`r=$(…)`/`t_word=$(…)`) but needs the probe to print >30 KB | not neutralised, but unreachable: systemctl returns a word. Latent if a probe's stderr flood (2>&1 in `cap`) ever exceeded ~30 KB |
| :963, :1497 | `mapfile < <(printf \| awk \| head -n "$TIMER_SCAN_MAX")` | 92 B | none | yes (process substitution) |
| :991, :3134 | `head -n1 FILE \| tr … \|\| true` | file head, producer is head | none | yes `|| true`; head is first stage |
| :1051 | `driver=$(printf CAP_OUT \| head -n1 \| awk …)` | nvidia-smi 1 line per GPU | none unless >30 KB | last stage awk reads all, but with pipefail a SIGPIPE'd printf would kill; unreachable size |
| :1162 | `done < <(find … \| sort \| head -n 4000)` | 208 paths / 19 KB here; hosts with thousands of containers/scopes exceed 64 KiB (4000 paths ~ 350 KB) | none: truncation to 4000 is intended; sort dies of SIGPIPE inside the process substitution | yes (process substitution). Note: >4000 paths silently truncates the sweep (not a pipefail issue; a coverage gap) |
| :1198, :1274, :1413 | `read … < <(awk …)` | `--list-boots`, PSI file | awk reads everything; none | n/a |
| :1480-1483 | `printf CAP_OUT \| grep -E \| grep -oE \| sort -u \| head -n 6 \| paste -sd, - \|\| true` | CAP_OUT = `journalctl -b -p err -o json` = 223 KB HERE, already >64 KiB | grep consumes all input, so printf never dies; only `sort` could die when >6 unique units (its output is <4 KB, one write) — name list is a note, not a verdict | yes `|| true`; also the early reader is fed by sort not printf |
| :1783 | `printf cl_out \| grep '^?' \| sed \| head -n6 \| paste \|\| true` | foreign-class rows, tiny | none | yes `|| true` |
| :1678, :1686, :1714 | `… \| tail -n1 \|\| true` | log tail / pair_out | tail is a full reader | n/a |
| :1855 | `grep -qxF -- "$t" <<< "$host"` | — | here-string, safe form | n/a |
| :2175 | `pkgline=$(… \| grep '^PLANE packages:' \| head -n1 \|\| true)` | 2.6 KB max | none | yes `|| true` |
| :2178, :2180, :2184 (selftest `check`) | `! printf "$out" \| grep -q …` | `$out` = census stdout+stderr, max 2642 B over 127 cases | a SIGPIPE would be a spurious FAIL (fail-closed) | not neutralised; unreachable (max 2.6 KB) |
| :2190 (selftest, `ABSENT:` arm) | `if printf "$out" \| grep -qE …; then unwanted+=` | same | **fail-open direction**: a SIGPIPE'd match reads "absent" and the case passes | not neutralised; unreachable at 2.6 KB. Cheap to switch to `grep -qE … <<<"$out"` for consistency with :695 |
| :2195, :2226 (`\|\| miss=`) | `printf \| grep -qE \|\| miss=…` | same / `check_cli` outputs <1 KB | SIGPIPE -> spurious "missing" (fail-closed) | unreachable |

Sites that look like early readers but read a FILE argument, not a pipe (no SIGPIPE possible): :644, :1149 (`awk … exit FILE`), boot-chain-audit :153, :460.

## Site table (`tools/boot-chain-audit.sh`, `set -uo pipefail`, no `-e`)

| site | pipeline | input | effect | neutralised |
|---|---|---|---|---|
| :371 | `head -n 1 "$tree/VERSION" \| tr` | file | none | head is first stage |
| :374, :379, :384 | `sed -n 's/…/p' FILE \| head -n 1` | extracted initramfs `config`, `hooks/btrfs-overlayfs`, `hooks/plymouth`; KB-scale | sed could die only after head has the first match; value is correct either way; status unused | yes — no `-e`, assignment status never tested |
| :483 | `find /etc/fstab /etc/crypttab /etc/mkinitcpio.conf /etc/mkinitcpio.conf.d /etc/default/limine /etc/limine-snapper-sync.conf /usr/lib/initcpio /usr/lib/modules -newermt "@$btime" -print -quit 2>/dev/null \| grep -q .` | at most ONE short path (-quit) -> no SIGPIPE possible | — | — |
| :929 | `printf out \| while read …; done` | full consumer, no `break` | none | n/a |
| :909-:1212 selftests | `printf out \| sed -n 1p`, `\| awk`, `\| wc -l`, `\| paste` | full readers | none | n/a |

## Same class, different mechanism — found while sweeping (route this)

**boot-chain-audit.sh:480-487 reads FALSE under pipefail whenever `find` exits 1, regardless of size.** `find` returns 1 when any start point is missing (stderr suppressed), and `-quit` returns that status. With `pipefail` (:139) the pipeline status is `find`'s 1 even though `grep -q .` matched, so the `if` takes the else branch and prints `0` ("no boot-chain input newer than boot start"). Reproduced in scratch:

```
find t2/missing_crypttab t2/present_newer -newermt "@$btime" -print -quit 2>/dev/null ; echo rc=$?   -> prints t2/present_newer, rc=1
no pipefail:   if find … | grep -q . ; then echo 1; else echo 0; fi   -> 1
set -uo pipefail (same shape as :139/:483):                            -> 0   (wrong)
```

Verdict effect: `newer=$(boot_inputs_newer)` (:749) feeds the `booted=1` gate (:761, `[ "$newer" = 0 ]`), i.e. verdict rule 2 BOOTED-OBSERVED can be awarded while a boot-chain input IS newer than boot start — a fail-open on the lane's own freshness guard. Not neutralised (no `|| true`; `set +e` irrelevant). Reachability: needs one of the eight start points absent. On this host all eight exist now (`ls -ld` run 2026-10-26), but `/etc/crypttab`, `/etc/mkinitcpio.conf.d`, `/etc/default/limine`, `/etc/limine-snapper-sync.conf` are optional paths on other Arch/omarchy hosts, and the fixture mode (`$BOOTCHAIN_FIXTURE/boot_inputs_newer`) bypasses the code so no selftest case covers it. Proposed fix shape (for the integrator to decide): `out=$(find … -print -quit 2>/dev/null || true); [ -n "$out" ]`, or pre-filter the start points with `[ -e ]`; plus one selftest-style case with a missing start point and a newer present one. This is outside the frozen C1 sites and outside the frozen kill rule's three hunks (it is in boot-chain-audit.sh, not the census), so it is a routing item, not a C1 claim.

## Findings summary for routing

1. Census residual under the frozen claim's own mechanism: **:743** (`bn=$(printf "$base_txt" | awk … exit)`), the only remaining bare assignment from an early-exit consumer on a buffer; kills the census (rc 141) if the foreign baseline exceeds the pipe buffer. Low reachability (539 B live baseline; needs an override file of ~2000 rows) — in the diff-scope the C1 kill rule allows (probe_packages).
2. Everything else in the census is neutralised by `|| true`, by process substitution, by a full-reader consumer, or by input size (table above). Not neutralised but unreachable: :931/:969/:1051/:1426/:1501 (single-line probes) and the selftest asserts :2178-:2195/:2226 (max census output 2642 B), with :2190 the fail-open direction.
3. The effective SIGPIPE threshold for `printf "$var" | grep -q` is ~30 KB (2-4% at 32 KB, ~40-60% at 48 KB, ~80-90% at 60 KB, ~certain above 64 KiB; host load ~16). The C1 text "once a probe printed more than the 64 KiB pipe buffer" understates the exposure window; the verdict-flip risk begins earlier (any `-Qkk` sample over ~30 KB, pre-fix).
4. boot-chain-audit.sh has no SIGPIPE-class site that changes a verdict (:374-:384 neutralised by missing `-e`; :483 cannot SIGPIPE), but :480-487 has the pipefail-plus-nonzero-producer defect above (verified, fail-open on BOOTED-OBSERVED).

## Not done

No lane counter was run; no mutation of the census or audit; no live `boot-chain-audit.sh --live` run (the find reproduction used scratch paths, not host /etc); the 30 KB threshold is measured on one loaded host with bash's builtin printf, not across kernels/pipe sizes; the host real-size table is a single read, not a distribution.
