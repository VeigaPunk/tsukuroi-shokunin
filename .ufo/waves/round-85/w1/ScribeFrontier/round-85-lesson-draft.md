# Round 85 — lesson (tsukuroi, fresh start)

author: draft by wave seat ScribeFrontier (w1, 2026-11-06) for the L1 to land. Freeze `66374a4db963e5c655506e64cb0fea2d67ec9d0d`
precedes every candidate file; candidate tip `479d868b2fc8969a19a617cd55ced5c13edd84b6`; pre-round tip
`3ed94533d581aa542d330ce2c97a798983839348`. Chronology is commit-graph order, not author dates: the freeze
`66374a4d` carries its parent's author date (`16:44:20`, committer `16:52:22`), so the r84 routed defect 5
(helper stamps the parent's author date) recurs and every citation here is by hash (r84 defect 5).

## Fresh-start read

MANIFEST `rounds[]` for tsukuroi 82/83/84 are all `rejected-honest-stop`; read with their non-author
spot-checks `corpus/lessons/round-82-verifier-spotcheck.md`, `round-83-verifier-spotcheck.md`,
`round-84-verifier-spotcheck.md`. One line each, root failure:

| Round | Closure | Root failure |
|---|---|---|
| 82 | `rejected-honest-stop` (`round-82-verifier-spotcheck.md` §1 R82-V1) | the frozen target was unreachable by construction: its own recipe set caps the maxima at 22/26 and 16/17, and the round froze 26/26, 17/17 anyway. |
| 83 | `rejected-honest-stop` (`round-83-verifier-spotcheck.md` §2) | the battery's legs each keyed on one fixture path, so a four-line path sniff reached C1 3/3 and C2 4/4 without the domain work. |
| 84 | `rejected-honest-stop` (`round-84-verifier-spotcheck.md` §2 C2) | fixed case order plus single-fault families: `f2-replay.py` (never opens `--facts`), `f1-signature.py` and `f4-firstfault.py` each read 13/13. |

The three numbers reproduced; the claims still failed. All three closures are instrument defects, so a fourth
meta-round would be the same move again. This round works ground no entry held — hibernation *availability*,
the precondition the r84 resume chain never read (`grep -rli 'lockdown_hibernation\|nohibernate\|hibernation_available'
corpus/knowledge` at `3ed94533` → empty) — and the instrument was frozen with candidate-free controls
(`.ufo/waves/round-85/before/controls/controls-receipt.txt`, K0–K6) before any candidate file existed.

## Gate

Sources opened 2026-11-06. Every pinned body was re-fetched live in this wave (curl `-sS -L`, HTTP 200) and
`cmp -s` against `.ufo/waves/round-85/before/src/` is empty for all four files (`kernel_power_hibernate.c`
35262 B, `include_linux_security.h` 67333 B, `security_lockdown_lockdown.c` 4344 B,
`Documentation_admin-guide_kernel-parameters.txt` 317993 B), so no row below rests on an unpinned body.
Quotes are verbatim at the cited raw line and ≤25 words; each row's `sed -n` proof is printed under the table.

| Candidate | URL, access date, location | Located quote (≤25 words) | Decision, reason and flip |
|---|---|---|---|
| S343 (new, code/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/power/hibernate.c, 2026-11-06, raw 109-113, 1424-1432, 1518-1524 | `return nohibernate == 0 && !security_locked_down(LOCKDOWN_HIBERNATION) && !secretmem_active() && !cxl_mem_active();` (10 tokens) | ADMIT, HA1–HA5. No admitted source states the conjunction: S336 documents `nohibernate` (raw 4479) and `hibernate=` (raw 1962-1969) without it, and the prefix order (`noresume`, `nocompress`, then `no`) appears only here. Flip: a tag where `hibernation_available()` drops or reorders a term. |
| S344 (new, code/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/security.h, 2026-11-06, raw 104-113 (comment), 128-158 (enum; `LOCKDOWN_HIBERNATION` 133, `LOCKDOWN_INTEGRITY_MAX` 149) | `Lockdown reasons that protect kernel integrity (ie, the ability for userland to modify kernel code) are placed before LOCKDOWN_INTEGRITY_MAX.` (19 words, starts after `LSM hook. ` on raw 105) | ADMIT, HA6. The ordering is only visible here: S336 lists `integrity` and `confidentiality` and never says hibernation is an integrity reason. Flip: a revision moving `LOCKDOWN_HIBERNATION` after `LOCKDOWN_INTEGRITY_MAX`. |
| S345 (new, code/A) | https://raw.githubusercontent.com/torvalds/linux/v7.2/security/lockdown/lockdown.c, 2026-11-06, raw 20-22 (`lockdown_levels`), 59-73 (`lockdown_is_locked_down`) | `static const enum lockdown_reason lockdown_levels[] = {LOCKDOWN_NONE,` (7 tokens); `if (kernel_locked_down >= what) {` (5 tokens, raw 65) | ADMIT, HA6/HA9. The sysfs labels are *max sentinels*: `integrity` stores `LOCKDOWN_INTEGRITY_MAX`, and the refusal test is `>=`, so `integrity` refuses every lower reason — hibernation included — while `none` refuses none. Flip: a revision whose level list or comparison changes that encoder. |
| REJECTED: man7 `kernel_lockdown(7)` | https://man7.org/linux/man-pages/man7/kernel_lockdown.7.html, 2026-11-06, raw HTML 135 (body sha256 `d07ec15a…5e0a`, 9861 B) | `Unencrypted hibernation/suspend to swap are disallowed as the` (8 words) | REJECTED, no row. (a) a man-pages-6.19 rendering generated 2026-09-09, not pinned to v7.2; (b) its "Unencrypted" qualifier is not in the pinned file — `grep -ic 'encrypt\|luks\|dm-crypt' kernel_power_hibernate.c` → `0`, so admitting it imports a condition the host's kernel does not implement; (c) it says "restricted", never which mode. Flip: a v7.2 line conditioning the hibernation lockdown on swap encryption, or a man-pages revision whose text matches the pinned behaviour. |
| REJECTED: ArchWiki mode sentence | https://wiki.archlinux.org/index.php?title=Power_management/Suspend_and_hibernate&action=raw, 2026-11-06, raw 105 (body sha256 `98320ec9…830d`, 49846 B) | `Enabling kernel lockdown prevents hibernation.` (5 words) | REJECTED, no row. Tier C secondary restatement of S344/S345 with no located mode boundary — read alone it cannot separate the `[none]` state this host reports. The r84 reject reason (unreachable interstitial) does **not** survive: the same URL now returns wikitext, so this is a reject on value, not on reach. Flip: a revision-pinned sentence naming that the mode must be integrity or confidentiality, or one carrying a host fact the kernel source lacks. |
| REJECTED: ArchWiki swap-size sentence | same URL/body, 2026-11-06, raw 111 | `Even if your swap partition is smaller than RAM, you still have a good chance of hibernating successfully.` (18 words) | REJECTED, no row. No bound, no unit, no mechanism; the rule the battery scores (rule 7, free swap vs `image_size`) already rests on S340's `image_size` definition. Flip: a sentence stating the free-swap-versus-image-size comparison the kernel makes. |

`sed -n` proofs (pinned snapshots, cwd `.ufo/waves/round-85/before/src`):

```text
$ sed -n '109,113p' kernel_power_hibernate.c
bool hibernation_available(void)
{
	return nohibernate == 0 &&
		!security_locked_down(LOCKDOWN_HIBERNATION) &&
		!secretmem_active() && !cxl_mem_active();

$ sed -n '1426,1431p' kernel_power_hibernate.c
	if (!strncmp(str, "noresume", 8)) {
		noresume = 1;
	} else if (!strncmp(str, "nocompress", 10)) {
		nocompress = 1;
	} else if (!strncmp(str, "no", 2)) {

$ sed -n '1521,1524p' kernel_power_hibernate.c
__setup("hibernate=", hibernate_setup);
__setup("resumewait", resumewait_setup);
__setup("resumedelay=", resumedelay_setup);
__setup("nohibernate", nohibernate_setup);
```

The `__setup` pair proves `nohibernate` and `hibernate=` are separate option keys: `hibernate=nocompress`
never reaches the `"no"` branch (it matches `"nocompress"` first), so it is a decoy, not a disable — the
reason the battery carries a PREC-DECOYS family.

```text
$ sed -n '104,113p' include_linux_security.h
/*
 * These are reasons that can be passed to the security_locked_down()
 * LSM hook. Lockdown reasons that protect kernel integrity (ie, the
 * ability for userland to modify kernel code) are placed before
 * LOCKDOWN_INTEGRITY_MAX.  Lockdown reasons that protect kernel
 * confidentiality (ie, the ability for userland to extract
 * information from the running kernel that would otherwise be
 * restricted) are placed before LOCKDOWN_CONFIDENTIALITY_MAX.

$ sed -n '133p;149p;158p' include_linux_security.h
	LOCKDOWN_HIBERNATION,
	LOCKDOWN_INTEGRITY_MAX,
	LOCKDOWN_CONFIDENTIALITY_MAX,
```

```text
$ sed -n '20,22p' security_lockdown_lockdown.c
static const enum lockdown_reason lockdown_levels[] = {LOCKDOWN_NONE,
						 LOCKDOWN_INTEGRITY_MAX,
						 LOCKDOWN_CONFIDENTIALITY_MAX};

$ sed -n '65,73p' security_lockdown_lockdown.c
	if (kernel_locked_down >= what) {
		if (lockdown_reasons[what])
			pr_notice_ratelimited("Lockdown: %s: %s is restricted; see man kernel_lockdown.7\n",
				  current->comm, lockdown_reasons[what]);
		return -EPERM;
	}

	return 0;
}
```

```text
$ sed -n '43,46p' security_lockdown_lockdown.c
	if (strcmp(level, "integrity") == 0)
		lock_kernel_down("command line", LOCKDOWN_INTEGRITY_MAX);
	else if (strcmp(level, "confidentiality") == 0)
		lock_kernel_down("command line", LOCKDOWN_CONFIDENTIALITY_MAX);
```

`LOCKDOWN_HIBERNATION` (133) < `LOCKDOWN_INTEGRITY_MAX` (149), and `integrity` sets the level to 149, so
`149 >= 133` refuses hibernation; `none` is 0 and refuses nothing. Host `[none]` therefore leaves hibernation
available, which is what C1 row HA7 records.

```text
$ sed -n '133,136p' man7-lockdown.html            # scratch copy, sha256 d07ec15a…
          appraisal).

       •  Unencrypted hibernation/suspend to swap are disallowed as the
          kernel image is saved to a medium that can then be accessed.

$ sed -n '105p' archwiki-raw.txt                  # scratch copy, sha256 98320ec9…
* Enabling [[Security#Kernel lockdown mode|kernel lockdown]] prevents hibernation.

$ sed -n '111p' archwiki-raw.txt
Even if your swap partition is smaller than RAM, you still have a good chance of hibernating successfully. …
```

Registry changes (proposed; rows `S343`–`S345` were drafted in the working tree at drafting time, `git status`
→ `M corpus/SOURCES.md`, and are not committed at `479d868b`, so this table is the admission record that lands
with them): three rows added, status none → `mined`, tier `code`/`A`, opened 2026-11-06, recheck `on-release`,
used-by `corpus/knowledge/hibernation-availability-r85.md` and `corpus/lessons/round-85.md`. No existing row
touched. Collision check: highest id before was S342 (`grep -oE '^\| S[0-9]{3}' corpus/SOURCES.md | tail -1` at
`479d868b`).

## Mistakes

| # | Class | Evidence | Captured-by | Fix |
|---|---|---|---|---|
| M1 | lane seat labelled as named non-author reviewer | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-84/tsukuroi.md:12` `**unprovable-but-better** (named non-author reviewer: seat ReviewEntry).`; committed entry text `git show 2ad4d1ef:corpus/knowledge/hibernate-resume-plane-r84.md` :67 `Non-author per-row review: … (seat ReviewEntry …)`; `corpus/lessons/round-84-verifier-spotcheck.md` §5 routed defect 2 | LEARNING.md §Discernment :45-46 — "A subagent the lane dispatched is still the lane"; an exploratory claim is admitted only through a named non-author ruling at closure | Proposed QUALITY 120: a wave seat is never named as the non-author reviewer of an exploratory claim; the ruling comes from the closure, and a report or entry that says otherwise is a finding. Shown able to fail: `check-nonauthor-label-r85.py --results .ufo/waves/round-84/w1-results.json` flags both lines above (rc 1, finding per file:line) and reads rc 0 on the corrected text; ExecLints builds it (`.ufo/waves/round-85/w1/ExecLints/`). Until it lands, both red sites stay on the record. |
| M2 | knowledge entry without `source:`/`recheck:` header lines | `git show 3ed94533:corpus/knowledge/hibernate-resume-plane-r84.md` opens `# Hibernate-resume plane (round 84)`, then `verified-at:` — no `source:`, no `recheck:`; `corpus/lessons/round-84-verifier-spotcheck.md` §5 routed defect 1 | LEARNING.md §Files the path writes :67-68 ("opens with `source:`, `verified-at:` … and `recheck:`") and QUALITY 8, which already required those lines — the rule existed, the enforcement did not | `check-entry-headers-r85.py --revision REV PATH...`: rc 1 with one finding per file lacking `source:` or `recheck:` in its first 12 lines, rc 0 clean, rc 2 unreadable. Shown able to fail: red on `corpus/knowledge/hibernate-resume-plane-r84.md` at `3ed94533`; green on the repaired copy (`source:` :3, `recheck:` :4 in the working tree). ExecLints builds it; the L1 registers it in the SKILL gate table. The row is a check, not a new criterion, because QUALITY 8 already says it. |

## Routed defects received (r84 → round 85)

| # | Defect routed by `round-84-verifier-spotcheck.md` §5 | Disposition | Evidence |
|---|---|---|---|
| 1 | the r84 entry opens without `source:`/`recheck:` | FIXED in the working tree at drafting (uncommitted); M2 supplies the check that keeps it fixed | `head -4 corpus/knowledge/hibernate-resume-plane-r84.md` → `source:` :3, `recheck:` :4, `verified-at:` :5; the red fixture is the committed `3ed94533` text |
| 2 | report and entry call a lane seat the "named non-author reviewer" | ADOPTED: declaration says it correctly, the entry's review record is retitled "Lane-seat per-row review (advisory)", and M1 + the non-author-label check make the class able to fail | SCORECARD `## Round 85 — declaration` :7268 "the hyaku closure; a wave seat is the lane, LEARNING.md §Discernment"; `git diff` on the entry shows `-Non-author per-row review:` → `+Lane-seat per-row review (advisory):` plus the appended round-85 correction |
| 3 | re-freeze the C2 battery (order shuffle, multi-fault, precedence, boundary, multi-swap, duplicate token) with the r84 forgers as committed controls reading below target before any candidate is scored | DONE at the freeze `66374a4d`: instrument sha256 `b30a7c1e…ba21`, 20 families, case list shuffled per run with an OS-entropy RNG, `resume-facts/2`; controls K0–K6 committed beside it | `.ufo/waves/round-85/before/controls/controls-receipt.txt`: K0 absent 0/20; K1 r84 gate 0/20; K2 schema shim 13/20 ×3; K3a/K3b/K3c (the r84 f1-signature, f2-replay, f4-firstfault forgers, each rc 1, `verdict: unmet`) 0/20; K3d/K3e shims 13/20; K4 constant HEALTHY 2/20; K5 v2 order replay 0/20 ×3; K6 substring sniffer 14/20, 14/20, 15/20 — every control below the 20/20 target |
| 4 | do not cite the provenance counter as a measurement again | HONOURED this round: the counter is cited nowhere in the declaration, the r85 battery, the gate, or this lesson; the lane's own SKILL row labels it "NOT a content measurement" | `grep -rn count-resume-rows` over `SCORECARD.md corpus/lessons/round-85* tools/check-hibernate-resume.py tools/resume-gate-battery-r85.py` → no hit; hits exist only in round-84 wave artifacts and the tool itself. Residual, truthful: the r84 entry still says its JSON is "counted by" the counter — a shape statement, not a measurement |
| 5 | cite commit-graph order, not author dates | ADOPTED and demonstrated: the freeze carries its parent's author date again (`66374a4d` author `16:44:20` = `3ed94533` author, committer `16:52:22`), so this lesson's order claims rest on hashes only | `git log -1 --format='%H author=%ad committer=%cd' 66374a4d` / `66374a4d^` |

## Seat harm

`entries: none observed` by this seat at drafting (seat disclosure class; the wave had not settled when this
draft was written). Wave-settlement source for the L1 to confirm before landing:
`.ufo/waves/round-85/w1-results.json` and the per-seat reports under `.ufo/waves/round-85/w1/`. No kill
signal, scratch or lane write outside a seat's tree, shared-file collision or provider incident reached this
seat; a suspicion with neither trace nor disclosure stays `[unk]` and is never attributed by timing alone
(QUALITY 110).

## Landing notes (for the L1; not part of the lesson's content)

- The lane tree was dirty at drafting — `M SKILL.md`, `M corpus/SOURCES.md`, `M corpus/knowledge/hibernate-resume-plane-r84.md`,
  untracked `corpus/knowledge/hibernation-availability-r85.json` plus the wave dir — so every Gate, registry and
  defect disposition above cites committed bytes (`479d868b`) or the working-tree file it names, never the tree
  as a whole.
- `.ufo/waves/round-85/w1-spec.json` states the milestone as "HA1-HA8"; the drafted JSON carries nine rows
  (`HA1`…`HA9`, `HA9` = `lockdown=` takes integrity or confidentiality). Either the milestone line or the row set
  is one row short; the L1 decides, and no count is claimed here.
- `corpus/knowledge/hibernation-availability-r85.md` did not exist at drafting. M2's check must pass on it before
  it lands (C1's entry header rule); its `source:` must name S343–S345 and S336.
- C2's 20/20 candidate measurement is not this seat's: MutGate, MutBattery, ExecReplicate and ReviewGate own it.
  This lesson records only the frozen controls, and records them as controls.
- Every quote in `## Gate` was re-fetched live on 2026-11-06 and `cmp`-equal to its pin; the two rejected pages
  were fetched the same day and their bodies kept under this seat's scratch, digests quoted in the table.
