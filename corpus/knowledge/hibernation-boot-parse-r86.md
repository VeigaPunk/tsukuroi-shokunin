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

Quotes are whitespace-normalized joins of consecutive cited lines of the pinned snapshot; `…` marks skipped lines.

| Row | Statement | Source, raw lines | Quote (≤25 words) | Host value (2026-11-06) |
|---|---|---|---|---|
| BP1 | A boot token reaches a `__setup` handler when its first strlen(option) characters equal the option string; the handler receives the rest of the token, value included. No check that the next character is `=` or end of token (that check exists only for early params). | S346 201-228 | "int n = strlen(p->str); if (parameqn(line, p->str, n)) {" | — |
| BP2 | The comparison reads `-` as `_` on both sides, so `resume-offset=` selects `resume_offset=`. | S347 79-95 | "if (dash2underscore(a[i]) != dash2underscore(b[i])) return false;" | no dashed hibernation token |
| BP3 | An unknown `param=val` token is rejoined into `param=val` before the `__setup` search; dotted module-style names (`x.noresume=1`) only reach the search under their full name and so match no hibernation option. | S346 503-532 | "repair_env_string(param, val);  …  if (obsolete_checksetup(param)) return 0;" | — |
| BP4 | `noresume` and `nohibernate` are registered bare and their handlers ignore the argument, so `noresume=0`, `noresume=1`, `noresumefoo` and `nohibernate=1` all set the flags. `noresum` (shorter than the option) does not. | S343 1440-1444, 1461-1466, 1518, 1524 | "static int __init noresume_setup(char *str) { noresume = 1; return 1; }" | none of these tokens |
| BP5 | `resume=` copies its value verbatim and each later token overwrites it (last wins); a `noresume` earlier on the line makes it return before copying. | S343 1402-1409 | "if (noresume) return 1; strscpy(resume_file, str);" | one token, `resume=/dev/mapper/root` |
| BP6 | An empty `resume_file` means no resume device: `find_resume_device` returns -ENOENT before any lookup. Its default is `CONFIG_PM_STD_PARTITION`, so an empty last `resume=` on this host leaves nothing to resume from. | S343 46, 982-985 | "if (!strlen(resume_file)) return -ENOENT;" | `CONFIG_PM_STD_PARTITION=""`, `CONFIG_HIBERNATION=y` (`/proc/config.gz`) |
| BP7 | `resume_offset=` changes the offset only when sscanf `%llu` converts; base-10 conversion stops at once without a leading decimal digit (no `+`, no `-` for unsigned), so `resume_offset=abc` keeps the earlier value; with a leading digit the conversion stops at the first non-digit, so `resume_offset=4096k` reads 4096 (`simple_strntoull` raw 79-95, whose digit loop `_parse_integer_limit` lives in `lib/kstrtox.c`, not pinned). | S343 1411-1422; S348 3662-3681, 79-95 | "if (sscanf(str, "%llu", &offset) == 1) swsusp_resume_block = offset;" | `resume_offset=3795013`, `/sys/power/resume_offset` = 3795013 |
| BP8 | Across options, order matters only through `noresume`: before `resume=` the device is never copied (BP5); after it the resume initcall still bails out (1106-1112). Either way the image is not read; the gate reports HR-NORESUME-ARG and does not model where `noresume` sits. Within one option, order selects the winner (last wins, BP5, BP7), which the gate does model. | S343 1402-1405, 1106-1112 | "If the user said "noresume".. bail out early." | — |

## Operator actions

- Read `/proc/cmdline` through the prefix rule, not by eye: any token *starting* `noresume` or `nohibernate`
  (`noresume=0` included) is the switch. Remove the token at its source (boot entry / kernel cmdline file); a
  value of `0` does not undo it.
- A trailing bare `resume=` (often a template variable that expanded to nothing) erases the resume device. The
  gate reports it as HR-NO-RESUME-ARG; fix the template, then re-run `--live`.
- `resume_offset=` must be digits; a unit suffix is silently cut (`4096k` reads 4096) and a non-numeric value is
  ignored, leaving the earlier one in force. Compare with `/sys/power/resume_offset` after boot.

## Limits

- `obsolete_checksetup` stops at the first matching handler that returns non-zero (S346 raw 221-222), so a second
  registration matching the same token would change the outcome. Wave seat ScoutPrefix swept all 758
  `__setup`/`early_param` registrations of the whole v7.2 tree (every architecture; shallow clone of tag v7.2):
  each of the five options is matched by its own registration only, and none is also an early, core or module
  param (`.ufo/waves/round-86/w1/ScoutPrefix.md` §3-§4, `ScoutPrefix/collision-emulator.txt`). The only near-miss is
  `arch/sh/kernel/cpu/init.c:50` `__setup("no" __stringify(x), …)`, which expands to `nofpu`/`nodsp` (§6). The
  sweep is a seat receipt over an unpinned clone, not a registry row.
- Not modelled by the gate: token order across options (BP8; frozen as a rule in the round-86 declaration — the
  verdict is HR-NORESUME-ARG in either order), quoted values (`param="v"`), tokens after `--` (handed to init),
  and bootconfig-supplied options. Routed: round 87, `corpus/lessons/round-86.md` Routed R86-R1 (wave seat
  CriticKernel's divergence list).
- `resume=` values the capture cannot resolve to a major:minor (`UUID=`, `PARTUUID=`, `LABEL=`, a bare `8:2` or
  `0`, a mistyped `/dev/mapper/…`) leave the gate's device rule unevaluated, so the gate can answer HEALTHY where
  the kernel finds no image (wave seat CriticKernel, `.ufo/waves/round-86/w1/CriticKernel.md` divergence 1; the
  capture also keeps the first `resume=` while the kernel keeps the last). Routed: round 87, lesson R86-R2.
- A `resume_offset=` above 2^64−1 saturates at `ULLONG_MAX` in the kernel (`lib/kstrtox.c`, not pinned; CriticKernel
  divergence 5); the gate reads the exact integer. Both then mismatch any real offset, so no verdict differs.
- Snapshots are tag v7.2; the host runs 7.2.11. No hibernate or reboot was run; parse behaviour is read from source
  and exercised only through the gate.
