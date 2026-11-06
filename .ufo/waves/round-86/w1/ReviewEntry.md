# ReviewEntry — C2 knowledge-entry review, round 86 wave w1 (2026-11-06)

Seat: ReviewEntry (lane seat; advisory review — per the round-86 declaration a wave seat is the lane,
LEARNING.md §Discernment; this is not and does not claim to be a non-author reviewer judgment).
Lane revision measured: `git rev-parse master` → `1e1caabcdd740a6429dd31d7aba3b725ff8c677d`
(entry commit; parent `dc884949` candidate gate, grandparent `2f67de80` freeze).

Subject: `corpus/knowledge/hibernation-boot-parse-r86.md` (+ `.json`), rows BP1–BP8; and the
round-86 edits to `corpus/knowledge/hibernation-availability-r85.md`
(`git diff dc884949 1e1caabc -- corpus/knowledge/hibernation-availability-r85.md`).

Method: every "quote at cited raw lines" claim was re-pinned by numbered grep over the pinned
snapshots in `.ufo/waves/round-86/before/src/` (read-tool elisions make prose reads unreliable for
line numbers); `sha256sum -c SHA256SUMS` was run in that directory; host values were checked against
`.ufo/waves/round-86/before/host/receipt.txt`. Receipts: `.ufo/waves/round-86/w1/ReviewEntry/`.

## Snapshot integrity

```
$ cd .ufo/waves/round-86/before/src && sha256sum -c SHA256SUMS
init_main.c: OK
kernel_params.c: OK
kernel_power_hibernate.c: OK
kernel_power_main.c: OK
lib_vsprintf.c: OK
rc=0
```

- SOURCES-row pinned hashes equal SHA256SUMS lines for S346–S349 (e895a643…, 51c0eb1d…, cabb648a…,
  7b60dabe…; receipt `pinned-hashes.txt`).
- S343 "re-opened this round, same sha256": r86 snapshot
  `ae3dbeb6ae682c3e03b750d45138aa5644a2db04cfc21c70c59446dad0af86c1` == r85 pin
  `.ufo/waves/round-85/before/src/SHA256SUMS` line 3. Verified.

## Row verdicts (BP1–BP8)

Ground-truth line numbers below are grep-pinned (receipt `line-pins.txt`).

| Row | Verdict | Evidence at cited lines | Reason |
|---|---|---|---|
| BP1 | **supports** | S346 init_main.c 201–228 is exactly `obsolete_checksetup` (sig 201, `return had_early_param;` 227, `}` 228). Quote = raw 208–209 joined. Prefix match (208–209), handler gets `line + n` with value (221), the `line[n] == '\0' \|\| line[n] == '='` test exists only inside `if (p->early)` (210–215). | Every clause of the statement is at the cited lines. |
| BP2 | **supports** | S347 kernel_params.c 79–95: `dash2underscore` (79, `-`→`_` at 81–82), `parameqn` (86), quote = raw 91–92, in range. `__setup("resume_offset=", …)` at S343 1519. | `-` read as `_` on both sides; `resume-offset=` therefore selects `resume_offset=`. Lesson Gate independently records 91–92. |
| BP3 | **supports** | S346 503–532: `unknown_bootoption` sig 503, `repair_env_string(param, val);` 518, `if (obsolete_checksetup(param))` 527 — the quote's `…` join is exactly the sanctioned form. `repair_env_string` (463–475) writes `'='` back ("make "param" the whole string", comment 462). | Rejoin-before-search holds; `x.noresume=1` reaches the search under its full name and parameqn over the first 8 chars fails, so it matches no hibernation option. |
| BP4 | **supports** | S343: `noresume_setup` 1440–1444 exact; `nohibernate_setup` 1461–1465 (through `nohibernate = 1;`; `return 1;`/`}` at 1466–1467 just outside); bare registrations `__setup("noresume", …)` 1518 and `__setup("nohibernate", …)` 1524. Handlers never read `str`. | `noresume=0/1`, `noresumefoo`, `nohibernate=1` all match by prefix and set flags; `noresum` fails parameqn at index 7 (`\0` vs `e`). (Range-end nit: F4.) |
| BP5 | **supports** | S343 1402–1409 is exactly `resume_setup` (1404–1405 `if (noresume) return 1;`, 1407 `strscpy(resume_file, str);`). | Verbatim copy, each later token overwrites (last wins — mirrored by the gate's `arg()`, tools/check-hibernate-resume.py:137–143), early return when noresume already seen. |
| BP6 | **supports** | S343 46 `static char resume_file[256] = CONFIG_PM_STD_PARTITION;` exact; `find_resume_device` 982–985 exact (984 `if (!strlen(resume_file))`, 985 `return -ENOENT;`), before any lookup (pm_pr_dbg 987). | Host: `CONFIG_PM_STD_PARTITION=""`, `CONFIG_HIBERNATION=y` in the receipt; an empty last `resume=` copies `""` and leaves nothing to resume from. |
| BP7 | **partial** | S343 1411–1422 is exactly `resume_offset_setup` (1418 `if (sscanf(str, "%llu", &offset) == 1)`, 1419 assignment). S348 3662–3673: 3662 `if (is_sign && digit == '-') {` (minus only when signed; no `+` skip anywhere in the window), 3671 `|| (base == 10 && !isdigit(digit))`. | "abc keeps the earlier value" fully supported (no leading digit → break, 0 conversions). But `break;` is raw 3674 — one line past the window — and the `4096k reads 4096` half rests on the `simple_strntoull` dispatch at 3675+ (outside; kstrtox stop-at-nondigit is unpinned). Fix: extend the S348 range to 3662–3680. See F1. |
| BP8 | **partial** | S343 1402–1405 (resume_setup bails before copying when noresume precedes) and 1106–1112 (`software_resume_initcall`, verbatim quote at 1109, `if (noresume \|\| !hibernation_available())` 1111) fully support the noresume mechanism. | The lead clause "Token order matters **only** through noresume" overclaims literally: order also selects the winner between two same-option tokens (BP5/BP7 last-wins; battery OFFSET-DUP expects HR-OFFSET-MISMATCH only when the wrong offset comes *after* the right one), and the gate models that order (offset parser keeps the last token, gate 148–152). "Does not model the order" is true only for noresume placement (availability loop 113–117 is position-insensitive, and the kernel outcome — image not read — holds in both positions). Fix: reword to "cross-token suppression of the resume happens only through noresume …". See F2. |

No row is does-not-support. Both partials are low-severity wording/citation-window issues; the
kernel mechanisms they describe are correct and pinned.

## Header and foot-matter

- `source:` — S346/S347/S348/S343 all `mined`, tier A in `corpus/SOURCES.md` (rows 357, 358, 359,
  354). S349 is correctly *not* listed here: no BP row cites it; it is used by the repointed r85
  entry (the round-level C2 sourcing "S346–S349" spans both entries). Consistent.
- `recheck:` — names `python3 tools/check-hibernate-resume.py --selftest` and `--live`, cadence 30d,
  triggers kernel update / cmdline change. Well-formed.
- `verified-at: 2026-11-06` — current. `host capture:` timestamp
  `2026-11-06T17:55:05-03:00` equals receipt line 1 verbatim.
- `gate:`/`battery:` files exist. `snapshots:` line true (`sha256sum -c` rc 0; host runs
  7.2.11-arch1-1). "Gate in `corpus/lessons/round-86.md`" — exists, `## Gate` at line 21, and its
  per-source line-pin columns (208–209, 91–92, 3671, 762–763, 1404–1407) agree with my independent
  pins.

## Host values vs receipt

All five populated Host-value cells match `.ufo/waves/round-86/before/host/receipt.txt`:
BP2 no dashed hibernation token ✓; BP4 none of the tokens ✓; BP5 exactly one `resume=/dev/mapper/root`
✓; BP6 `CONFIG_PM_STD_PARTITION=""` + `CONFIG_HIBERNATION=y` ✓; BP7 `resume_offset=3795013` on the
cmdline and `/sys/power/resume_offset` = 3795013 ✓. Null cells are shown as `—` in the md. ✓

## .md / .json agreement

All 8 rows agree field-for-field (statement, source, raw_lines, quote, host_value incl. null↔`—`).
BP7 splits `S343 1411-1422; S348 3662-3673` as source `S343; S348` + raw `1411-1422; 3662-3673` —
same facts, different partition; acceptable. ✓

## Limits section — spot-verified

- "first handler that returns true wins", link order: `obsolete_checksetup` 201–227 iterates
  `__setup_start…__setup_end`, `else if (p->setup_func(line + n)) return true;` (221–222). ✓
- Quoted values not modelled by the gate: true — the gate tokenizes with `cmdline.split()` only
  (114/140/149) and implements no unquote; the kernel's `param="v"` unquote branch is
  repair_env_string 468–471. ✓
- Tokens after `--` handed to init: pinned snapshot init_main.c 477 comment "Anything after -- gets
  handed straight to init." above `set_init_arg`. ✓
- Bootconfig unmodelled: no bootconfig handling in the gate. ✓

## Round-86 edits to hibernation-availability-r85.md (diff dc884949→1e1caabc)

Three hunks; all accurate:

1. `source:` line adds "S346 (init/main.c) and S349 (kernel/power/main.c) added round 86" — both
   pinned in round-86 `src/`, checksums OK, tier A, mined. ✓
2. Prefix paragraph: "pinned round 86 as S346 (raw 201-228)" ✓ (exact function bounds);
   "the gate now parses tokens this way (BP1-BP4)" ✓ (gate `matches()` implements the prefix + dash
   rule, gate 105–108). The retained "This host's cmdline carries none of these forms" stays true.
3. "Round 86: fixed in the gate (HR-NO-RESUME-ARG; BP6)" ✓ — gate 161–162 returns HR-NO-RESUME-ARG
   when `resume=` is absent *or empty* (comment names the empty case), and the battery's EMPTY-RESUME
   family expects exactly `["HR-NO-RESUME-ARG"]` (battery 357–358). And the S349 repoint
   "raw 762-763: `if (hibernation_available()) count += sysfs_emit_at(buf, count, "disk ");`" is
   exact (grep-pinned 762–763 in kernel_power_main.c). ✓

Twin check: `hibernation-availability-r85.json` cites only S343/S344/S345/S336/host rows; none of
the fields the diff touched (header source line, two Limits prose bullets) has a .json counterpart,
so the md edit desyncs nothing. ✓

## Findings (severity order)

- **F1 (low, BP7 — citation window).** `corpus/knowledge/hibernation-boot-parse-r86.md` BP7 row /
  `.json` raw_lines `3662-3673`: the `break;` that realizes "stops at once" is raw 3674, and the
  `4096k reads 4096` half depends on the `simple_strntoull` dispatch at 3675+ (kstrtox stop-at-
  non-digit, not pinned). Proposed patch: cite `3662-3680` (or add "(the conversion loop then stops
  at the first non-digit, raw 3675-3680)"). Content otherwise correct.
- **F2 (low, BP8 — scoping of "only").** BP8 statement lead "Token order matters only through
  `noresume`": literal reading is false — last-token-wins between two same-option tokens is order
  too (BP5, BP7; battery OFFSET-DUP: wrong offset before right → HEALTHY, after →
  HR-OFFSET-MISMATCH), and the gate models that order. Proposed patch: "Cross-token suppression of
  the resume happens only through `noresume`: before `resume=` the device is never copied (BP5);
  after it the resume initcall still bails out (1106-1112). Apart from last-token-wins (BP5, BP7)
  the gate does not model where `noresume` sits, and need not: either way the image is not read
  (HR-NORESUME-ARG)."
- **F3 (info — quote fidelity vs header).** Header: "Quotes are verbatim at the cited raw lines…
  `…` joins two quoted lines". In fact only BP3 uses the sanctioned `…` join and BP8 quotes a single
  line verbatim; BP1/BP2 join two consecutive lines with a space and BP4/BP5/BP7 collapse multi-line
  statements to one line with inline braces (all line-pinned verbatim content). Proposed patch:
  reword the header to "quotes are whitespace-normalized joins of consecutive cited lines; `…`
  marks a skipped line" — or reformat the five quotes as `…`-joins.
- **F4 (info, BP4 — range end).** Second range `1461-1465` stops one line before `return 1;` (1466)
  of `nohibernate_setup`; every flag-setting line is inside, so the quote and statement are
  unaffected. May be folded into F3's touch-up.

## Verdict

C2 entry **supported as an exploratory depth candidate**: 7/8 rows supports, 2 partial (BP7, BP8,
both low severity with concrete patches above), 0 does-not-support; header, host values, md/json
agreement, snapshot integrity and the r85-entry repoint all verified. Nothing here blocks C2; the
findings are editorial and for the L1 to apply or waive. No lane file was edited; no tools were
installed or upgraded.

Receipts in `.ufo/waves/round-86/w1/ReviewEntry/`: `line-pins.txt`, `pinned-hashes.txt`,
`r85-diff.diff`, `host-values-check.txt`, `verdict.json`.
