# Hibernation boot-option parse (round 86)

source: S346 (Linux v7.2 init/main.c), S347 (kernel/params.c), S348 (lib/vsprintf.c), S343 (kernel/power/hibernate.c, re-opened this round, same sha256); all `mined`, tier A; Gate in `corpus/lessons/round-86.md`
recheck: `python3 tools/check-hibernate-resume.py --selftest` and `--live`, cadence 30d and on any kernel update or cmdline change
verified-at: 2026-11-06
host capture: `.ufo/waves/round-86/before/host/receipt.txt` (2026-11-06T17:55:05-03:00, read-only)
machine-readable rows: `corpus/knowledge/hibernation-boot-parse-r86.json`
gate: `tools/check-hibernate-resume.py` token parse (round-86 C1); battery `tools/resume-gate-battery-r86.py`
snapshots: `.ufo/waves/round-86/before/src/` (tag v7.2, `SHA256SUMS`); the host runs 7.2.11

## What this plane answers

The round-85 plane says which boot options switch hibernation off. This one says which *tokens* the kernel reads as
those options. The answer is wider than the option names suggest: matching is by prefix, a value after the name is
ignored for the two switches, `-` and `_` are the same character, and the last `resume=` / `resume_offset=` wins.
A gate that matches whole tokens reads `noresume=1` as HEALTHY while the kernel will not resume (round-85 gate,
spot-check `round-85-verifier-spotcheck.md` §5 defect 4).

## Rows

Quotes are verbatim at the cited raw lines of the pinned snapshot; `…` joins two quoted lines of one function.

| Row | Statement | Source, raw lines | Quote (≤25 words) | Host value (2026-11-06) |
|---|---|---|---|---|
| BP1 | A boot token reaches a `__setup` handler when its first strlen(option) characters equal the option string; the handler receives the rest of the token, value included. No check that the next character is `=` or end of token (that check exists only for early params). | S346 201-228 | "int n = strlen(p->str); if (parameqn(line, p->str, n)) {" | — |
| BP2 | The comparison reads `-` as `_` on both sides, so `resume-offset=` selects `resume_offset=`. | S347 79-95 | "if (dash2underscore(a[i]) != dash2underscore(b[i])) return false;" | no dashed hibernation token |
| BP3 | An unknown `param=val` token is rejoined into `param=val` before the `__setup` search; dotted module-style names (`x.noresume=1`) only reach the search under their full name and so match no hibernation option. | S346 503-532 | "repair_env_string(param, val);  …  if (obsolete_checksetup(param)) return 0;" | — |
| BP4 | `noresume` and `nohibernate` are registered bare and their handlers ignore the argument, so `noresume=0`, `noresume=1`, `noresumefoo` and `nohibernate=1` all set the flags. `noresum` (shorter than the option) does not. | S343 1440-1444, 1461-1465, 1518, 1524 | "static int __init noresume_setup(char *str) { noresume = 1; return 1; }" | none of these tokens |
| BP5 | `resume=` copies its value verbatim and each later token overwrites it (last wins); a `noresume` earlier on the line makes it return before copying. | S343 1402-1409 | "if (noresume) return 1; strscpy(resume_file, str);" | one token, `resume=/dev/mapper/root` |
| BP6 | An empty `resume_file` means no resume device: `find_resume_device` returns -ENOENT before any lookup. Its default is `CONFIG_PM_STD_PARTITION`, so an empty last `resume=` on this host leaves nothing to resume from. | S343 46, 982-985 | "if (!strlen(resume_file)) return -ENOENT;" | `CONFIG_PM_STD_PARTITION=""`, `CONFIG_HIBERNATION=y` (`/proc/config.gz`) |
| BP7 | `resume_offset=` changes the offset only when sscanf `%llu` converts; base-10 conversion stops at once without a leading decimal digit (no `+`, no `-` for unsigned), so `resume_offset=abc` keeps the earlier value and `resume_offset=4096k` reads 4096. | S343 1411-1422; S348 3662-3673 | "if (sscanf(str, "%llu", &offset) == 1) swsusp_resume_block = offset;" | `resume_offset=3795013`, `/sys/power/resume_offset` = 3795013 |
| BP8 | Token order matters only through `noresume`: before `resume=` the device is never copied (BP5); after it the resume initcall still bails out (1106-1112). Either way the image is not read; the gate reports HR-NORESUME-ARG and does not model the order. | S343 1402-1405, 1106-1112 | "If the user said "noresume".. bail out early." | — |

## Operator actions

- Read `/proc/cmdline` through the prefix rule, not by eye: any token *starting* `noresume` or `nohibernate`
  (`noresume=0` included) is the switch. Remove the token at its source (boot entry / kernel cmdline file); a
  value of `0` does not undo it.
- A trailing bare `resume=` (often a template variable that expanded to nothing) erases the resume device. The
  gate reports it as HR-NO-RESUME-ARG; fix the template, then re-run `--live`.
- `resume_offset=` must be digits; a unit suffix is silently cut (`4096k` reads 4096) and a non-numeric value is
  ignored, leaving the earlier one in force. Compare with `/sys/power/resume_offset` after boot.

## Limits

- Other `__setup` strings are searched in link order and the first handler that returns true wins; this entry does
  not prove that no other v7.2 `__setup` string is a prefix of these tokens (wave scout sweep: see the lesson Gate).
- Not modelled by the gate: token order (BP8), quoted values (`param="v"`), tokens after `--` (handed to init),
  and bootconfig-supplied options.
- Snapshots are tag v7.2; the host runs 7.2.11. No hibernate or reboot was run; parse behaviour is read from source
  and exercised only through the gate.
