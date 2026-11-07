author: hyaku closure (non-author integrator, @m_zfl)

# tsukuroi round 90 — non-author verifier spot-check

Lane round 90; pre-round tip `c0f91856a5cc4816ae5d075022f16dc6aef0593c`, post-round tip
`b1ef413d88a8fd13f3df9dda6b2e257d4a299318`. Report `.ufo/reports/round-90/tsukuroi.md` (fleet repo).
Driver digest (copied from the mutable `.ufo/watchdog.log`):
`2026-11-06T23:21:22-03:00 launch tsukuroi round=90 pgid=527919 driver=hyaku-inline attempt=1`;
`2026-11-07T01:01:01-03:00 complete tsukuroi round=90; hyaku-inline attempt=1`.
Closure verdict: **status ok, admitted false, `rejected-honest-stop`** (C1 not verified; C2 `unprovable-but-better`).

## 1. Step-1 conformance

| Check | Command | Observed | Result |
|---|---|---|---|
| Report committed by lane identity | `git log --format='%an %ae %H' -- .ufo/reports/round-90/tsukuroi.md` | `tsukuroi-shokunin tsukuroi@shokunin.local 2f107dbc4170978c86888c93fabb0e1533103572` | pass |
| `SHONEN` heading, one line per box | read report §SHONEN | 4 lines, all `[~]` with pointers | pass |
| Cited commits exist and are ancestors of `master` | `git cat-file -e <h>^{commit} && git merge-base --is-ancestor <h> master` for c0f91856, 6511437e, cd165cf2, ce89df93, 58723499, b380483e, 9b4d9cda, b1ef413d | 8/8 `anc ok` | pass |
| Lane pushed, nothing left | `scripts/hyaku/jj-lane.sh state …/tsukuroi-shokunin`; `git status --porcelain`; `git ls-remote origin refs/heads/master` | `ahead=0 behind=0 tracked=0 untracked=0`; porcelain empty; remote `b1ef413d…` | pass |
| Prompt carries template contract | `grep -n '^#' .ufo/prompts/tsukuroi-round-90.md` vs `templates/round-prompt.md` | §1-§5 headings identical, hyaku addendum §6 + §7 + run15 notes appended; 0 `{{` placeholders left | pass |
| Not a marker | report cites 7 lane commits with evidence | real report | ok |

Conformance defects (status-neutral, notes only):
- D1 timestamps (same cause as r89, fleet/jj helper keeps change creation time as author date): freeze `6511437e`
  author date `23:20:02` predates the launch line `23:21:22` (committer `23:44:28`); report `2f107dbc` author date
  `00:52:42` predates cited `b1ef413d` (`00:58:43`; report committer `01:00:05`). Routed to the helper owner again.
- D2 prior-state wording: the report says the C2 absence sweep at `c0f91856` hit "r89 Limits lines only"; the committed
  sweep (`before/new-ground-sweep.txt`) also hits r89 rows UF3 (quote naming `volume_get_by_coord` for `boot(N)`) and
  UF8. Neither states anything about `tpm_present()` or `guid/uuid/fslabel` lookup, so the new-ground ruling stands.

## 2. Claims

### C1 — operability 9 (measured; gate `tools/check-limine-pins.py` on battery `tools/limine-pin-battery-r90.py`)

Evidence-verified, not executed (§Gate standard, Closure consequence: a sibling's gate is never run here):
- `sha256sum tools/limine-pin-battery-r90.py` → `8f0daee82b9d487b5412a45ec1b8cf74c4e037e87d67213f756f1f850fb303e5` = declared freeze digest.
- `sha256sum -c .ufo/waves/round-90/before/freeze-manifest.sha256` (from lane root) → 40/40 `OK`.
- `git diff --stat ce89df93 b1ef413d -- tools/` → empty (measured bytes = landed bytes).
- `after/measured/c1-receipt-canonical-ce89df93.txt` and `c1-receipt-clone-ce89df93.txt`: `families_passed 73/73
  verdict met` ×3, `rc=0` in both; JSONs: 3 runs `verdict met` each.
- Controls `before/controls/summary-{canonical,clone}.txt`: K1 landed gate `0 0 0` / `1 0 0`; K2 `51 50 51` / `51 51 50`;
  N21-N27 each unmet 3/3 with the named killing family. Wave seat ExecReplicate (`w1/ExecReplicate.md`): 73/73 ×3
  both layouts, `--runs 0` and `--runs -1` → rc 2.
- Target reported: 73/73 ×3 canonical and clone — **reproduced from committed evidence.**

Fidelity, re-opened by me: `curl https://raw.githubusercontent.com/limine-bootloader/limine/v12.9.4/common/lib/config.c`
→ `cmp` identical to `before/src/limine-v12.9.4-common_lib_config.c`; raw 642-650:
`char *c = config_get_entry(&s, 0); … while (*c != '/' && c > config_addr) c--; if (*c == '/' && c > config_addr) c[-1] = 0;`
— the buffer is cut before the first entry unless the entry starts at byte 0, so a global lookup of
`measured_boot`/`hash_mismatch_panic` does not see an entry body. The r90 battery requires the opposite: control
`N21-measured-global-only` (the Limine-true reading) is killed 3/3 by family MEASURED-IN-ENTRY, and N27
`panic-before-pins` by PANIC-AFTER-PIN. `after/visibility-probe.txt` shows the landed gate (sha256 `4780da83…`, =
`git show ce89df93:tools/check-limine-pins.py | sha256sum`) answering `on_panic halt` for case A where a global-only
gate answers `menu`. **C1: NOT VERIFIED** — the frozen predicate certifies Limine-false answers; the lane filed it so.
Axis grade: **operability unchanged** (declared 9 → 9, no ordinal claim). Not `harmed`: the wrong `on_panic` arises
only for `measured_boot` inside an entry body, a shape absent on this host (`after/live-receipt.txt`: `measured_boot
None`, `on_panic menu`, `/boot` digest list identical before/after), and r87's R6 already carried the same whole-file
reading; no r87-era answer regressed (lane SCORECARD "No axis harmed by regression"). Routed R90-R1 below.

### C2 — depth 8 (exploratory; I am the named non-author reviewer)

Re-measured:
- `git grep -l -i -e tpm_present -e volume_get_by -e TCG2 -e binary_bios_measurements <rev> -- corpus/knowledge`:
  `c0f91856` → 2 files (r89 entry only); `b1ef413d` → 4 files (+ `limine-tpm-volume-r90.{md,json}`).
- Rows: entry TV1-TV9 (9 rows; JSON 9 distinct `TV` ids).
- `grep -c '^| S[0-9]' corpus/SOURCES.md` at `c0f91856` → 363, at `b1ef413d` → 373 (matches report).

Sources re-opened upstream (byte-compared with the lane pins):
- TV1 / S365 `common/lib/tpm.c` raw 113-114 `bool tpm_present(void) { return tcg2 != NULL || cc != NULL; }` — `cmp`
  identical to the pin. Agree.
- TV5 / S367 `common/fs/file.s2.c` raw 27-31: `fs_get_guid` body `(void)guid; (void)part; return false;`. Agree (no
  filesystem UUID ever matches; `uuid(86D8-C3F6)` names nothing).
- TV7 / S366 `common/lib/part.s2.c` raw 1056 `&& strcasecmp(volume_index[i]->fslabel, fslabel) == 0) {` — pin identical.
  Agree. TV8 raw 575 `ret->partition   = partition + 1;` and S373 `disk.s2.c` raw 1012 `if (ret == NO_PARTITION)` /
  `continue;` (pin sha256 `34e3a81f…` = upstream). Agree: slot numbers with gaps.
- TV2 / S369 systemd v262.1 `src/boot/export-vars.c` raw 57-62 (`s = xasprintf("0x%08x", active_pcr_banks);`). Agree.
- TV2 / S372 TCG EFI Protocol Spec rev 00.13: re-downloaded, sha256 `40a2568e…` = row; `pdftotext -f 29 -l 29`:
  "5. If the platform does not have a TPM then the following values SHALL be returned: … TPMPresentFlag = FALSE". Agree.
- TV3 host value re-read live (read-only): `tail -c +5 /sys/firmware/efi/efivars/LoaderTpm2ActivePcrBanks-… | iconv`
  → `0x00000000`; `ls /sys/class/tpm | wc -l` → 0. Agree.

Ruling: **`unprovable-but-better`**. Reasons: (a) the ground is new — no prior entry said what `tpm_present()` asks or
how `guid/uuid/fslabel/boot(N)` find a volume, and the gate's new `--tpm-present` flag needs exactly this answer;
(b) every `[src]` row I re-opened is verbatim and line-exact on the upstream tag; (c) the one host-to-Limine bridge
(TV4) is labelled `[inf]` with its gap stated, TV9 is limited to the tool's output, and the Limits name the
12.9.5/12.9.6 drift that can invalidate TV5-TV8 and R10's visibility; (d) two scout corrections (TV5, TV8) were
re-read before admission. No counter exists, so no ordinal move: depth stays 8.

## 3. Per-axis verdicts

| Axis | Verdict | Basis |
|---|---|---|
| operability | unchanged | C1 NOT VERIFIED (visibility sub-clause Limine-false); 9 → 9, no regression on host shapes |
| depth | unprovable-but-better | C2, this reviewer, §2 |
| coverage | unchanged | no claim; SCORECARD axes line unchanged |
| freshness | unchanged | no claim |
| calibration | unchanged | no claim |
| adjacency | unchanged | no claim; ConnectorOverlap: no conflict with 20 siblings |

## 4. Discernment spot-check (`corpus/lessons/round-90.md` `## Gate`)

| Item | Decision | Re-opened source | Agree/disagree | Reason |
|---|---|---|---|---|
| S365 tpm.c | ADMIT | upstream raw `v12.9.4/common/lib/tpm.c` 113-114 | agree | quote verbatim at raw 114; defines `--tpm-present` |
| S369 export-vars.c | ADMIT | upstream raw `systemd v262.1 src/boot/export-vars.c` 57-62 | agree | quote verbatim at raw 61; stub writes the variable only when absent |
| S373 disk.s2.c | ADMIT | upstream raw `v12.9.4/common/drivers/disk.s2.c` 984-988, 1010-1013 | agree | quote at raw 1012; `gpt_get_guid` only on the whole block device |
| `hdd(1:1)` as this host's ESP | REJECT | upstream `part.s2.c` 1064-1074 `volume_get_by_coord` | agree | matches `volume_index[i]->index == drive`, Limine's firmware enumeration index, not visible from Linux; three disks present |
| `systemctl --version` `+TPM2` as presence signal | REJECT | `systemctl --version` on this host | agree | prints `+TPM2` while `/sys/class/tpm` is empty and the efivar reads `0x00000000`: a compile-time feature, not firmware state |
| ScoutTPM A2/A6/A7/A11/A12, ScoutVolume extra rows | NOT ADMITTED | `w1/ScoutTPM/proposed-sources.md` (listed) | agree | unopened by the L1 (CORPUS rule 1); TV9 correctly limited |

SOURCES row re-opened: **S373** — URL resolves, pin sha256 `34e3a81fee89…b799d2` = upstream bytes, anchor 986-988 /
1004-1016 lines up; its ≤25-word quote (lesson Gate) `"if (ret == NO_PARTITION)"` is 4 words at raw 1012. Agree.

Census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin tsukuroi` → rc 0, `ok`, 52 `W04`
(pre-existing duplicate-URL warnings, same count the lane reports at both ends), no `E` code.

## 5. Trend verdicts

- **expansion — unprovable-but-better.** TV1-TV9 on new ground (absence sweep 2 → 4 knowledge files), 10 tier-A rows
  (S364-S373), all sampled sources verbatim; exploratory with no counter.
- **quality — improved.** QUALITY 130 (`--runs 0` vacuous `met`; ExecReplicate: `--runs 0` → rc 2) and 131 (visibility
  read at the caller's buffer) present at `corpus/QUALITY.md` lines 318/321; LP5 erratum `corpus/knowledge/
  limine-pin-plane-r87.md` §"Erratum (round 90)" with sweep receipt; scout rows corrected before admission.
- **discernment — improved.** The L1 re-read `config.c` 642-650 on a wave finding, built a probe that separates the two
  readings (`after/visibility-probe.txt`), and filed a 73/73 result as NOT VERIFIED; both sampled rejects hold.

## 6. Routed to the lane (round 91)

1. **R90-R1 visibility:** fix R10 and r87's R6 to global-section-only (unless line 1 is an entry; since 12.9.5 such a
   file has no global options — re-pin first), invert families MEASURED-IN-ENTRY and PANIC-AFTER-PIN, and make
   `N21-measured-global-only` the passing reading; re-score the gate.
2. **Oracle-reuse channel (CriticClaims §1):** a gate importing the battery's own `Case.finish`/`want_on_panic` reads
   73/73; name the channel in the docstring or add a control that kills it.
3. **Battery mutation coverage:** MutBattery 21/43 battery mutants detected; CriticForgers survivors G1-G3; MutGate
   3/29 surviving — add controls or state them as limits.
4. **Drift:** Arch carries limine 12.9.6-1 (ScoutDrift); re-pin and re-check TV5-TV8 and R10 before the host upgrades.
5. **Prior-state wording (D2):** quote the sweep hits exactly (UF3/UF8 rows, not "Limits only").
6. **D1 timestamps:** report/freeze author dates precede the cited commit / launch line; fleet-helper owner.

SHONEN (operator note): the four `[~]` boxes cite checkable artifacts (registry row `limine-pin-battery-r90`, live
receipt, entry "Operator actions", ConnectorOverlap); box 3 still lacks a no-oral-context retest, so none is fully
checkable by a non-author this round. No promotion, no mint.
