# CriticKernel — r86 w1: where the frozen r86 parse still diverges from v7.2

Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` →
`1e1caabcdd740a6429dd31d7aba3b725ff8c677d` (entry commit). No lane file was edited; every experiment ran on a
copy in `/fast/scratch/hyaku/tsukuroi-r86/CriticKernel/` (removed on exit). Receipts:
`.ufo/waves/round-86/w1/CriticKernel/`.

Instrument identity as measured:
`sha256(tools/check-hibernate-resume.py)` = `8123d033c0ccf8e3c6bdbdd1…`,
`sha256(tools/resume-gate-battery-r86.py)` = `a49a18aa21322579f723cbdd…`,
`sha256(before/src/kernel_power_hibernate.c)` = `ae3dbeb6ae682c3e03b750d4…` (matches the r85 pin).

## Method

- **Gate side (measured).** `probe.py` loads the unchanged r85 host base
  `.ufo/waves/round-85/before/host/facts-v2.json`, replaces only `cmdline` (and, where stated, one field), and runs
  `python3 tools/check-hibernate-resume.py --facts F`; rc, verdict and findings are recorded verbatim in
  `gate-out-candidate-cases1.json` … `-cases3.json` (and the patched gate's in the matching `-patched-` files).
- **Kernel side (transcribed, not booted).** `kmodel.c` is a mechanical transcription of the pinned parse path —
  `next_arg` (lib/cmdline.c v7.2 raw 237-284), `repair_env_string` (init/main.c raw 463-476),
  `obsolete_checksetup` (raw 201-228), the seven hibernation `__setup` handlers (hibernate.c raw 1402-1466),
  `parse_args`' `--` stop (kernel/params.c raw 182-183), and `sscanf("%llu")` via `_parse_integer_limit`
  (lib/kstrtox.c raw 58-95). It is run on the same strings; output in `kmodel-out.txt`. Byte-for-byte kernel
  behaviour is therefore **[INFERENCE]** from the cited lines, not an observation. Device *resolution* outcomes
  (`early_lookup_bdev`, block/early-lookup.c raw 244-253) are likewise **[INFERENCE]**.
- Fetched v7.2 files used for lines the pin does not carry are stored with their sha256 in
  `CriticKernel/upstream/` (`cmdline.c`, `kstrtox.c`, `early-lookup.c`, `bootconfig.c`).

## Headline

Candidate gate, my run: **30/30 families, 231 cases, rc 0** (`candidate-battery.json`). Patched gate (below):
**30/30, rc 0**, `--selftest` **PASS 16/16**. Every divergence below is therefore *outside* the 30 frozen
families — none of them kills C1, and none of them is visible to the frozen predicate. Of the six, three are
already declared limits (quoted values, tokens after `--`, bootconfig: SCORECARD r86 last paragraph; entry
`hibernation-boot-parse-r86.md` §Limits line 48) and the fourth declared limit, token order, is **not** a
divergence (HR-NORESUME-ARG covers every order case I tried). Three are **not** declared: the device-value class,
the capture/gate `resume=` first-vs-last mismatch, and the `%llu` overflow saturation.

## Divergences, ranked by false-HEALTHY risk

Facts = host base except `cmdline` (and the noted field). "Gate" is the candidate's verbatim output.

| # | cmdline | Kernel will do (file:line) | Gate | Direction |
|---|---|---|---|---|
| 1 | `resume=/dev/mapper/nonexistent resume_offset=3795013` (`resume_dev_majmin:null`) | `resume_setup` copies the string (hibernate.c 1407); `find_resume_device` → `early_lookup_bdev` → `devt_from_devname` fails → `-ENODEV`, initcall returns (hibernate.c 996-1010, 1114-1119) → **no resume** | `{"findings": [], "verdict": "HEALTHY"}` rc 0 | **false HEALTHY** |
| 1 | `resume=UUID=cf3d875f-…-015c9e953618 resume_offset=3795013` (`resume_dev_majmin:null`) | `early_lookup_bdev` has no `UUID=` branch (early-lookup.c 244-253): it falls to `devt_from_devnum`, `sscanf("%u:%u")` fails and `simple_strtoul(…,16)` stops at `U` → `-EINVAL` (197-214) → **no resume** | HEALTHY rc 0 | **false HEALTHY** |
| 1 | `resume=0 resume_offset=3795013` (`resume_dev_majmin:null`) | `devt_from_devnum("0")` → devt 0 → `swsusp_check` on 0 fails → no resume | HEALTHY rc 0 | **false HEALTHY** |
| 1 | `resume=8:2 resume_offset=3795013` (`resume_dev_majmin:null`) | `devt_from_devnum` accepts `8:2` (early-lookup.c 197-214) → resumes from the wrong device, no image → no resume | HEALTHY rc 0 | **false HEALTHY** |
| 1 | `resume=PARTUUID=cf3d875f-…-015c9e953618 resume_offset=3795013` (`resume_dev_majmin:null`) | `devt_from_partuuid` (early-lookup.c 246-247) → the *root* partition, not the swap → no image | HEALTHY rc 0 | **false HEALTHY** |
| 1 | `resume=LABEL=swap …` / `resume="/dev/mapper/a b" …` | `devt_from_devnum` → `-EINVAL`; `devt_from_devname` with a space → `-ENODEV` | HEALTHY rc 0 | **false HEALTHY** |
| 2 | `quiet splash -- resume=/dev/mapper/root resume_offset=3795013` | `parse_args` stops at `--` (kernel/params.c 182-183); the rest goes to `set_init_arg` (init/main.c 478-499, 1016-1018) and never reaches `obsolete_checksetup` → `resume_file=""` → `-ENOENT` (hibernate.c 984) | HEALTHY rc 0 | **false HEALTHY** |
| 2 | same string, produced by bootconfig `init.resume=…` | `extra_init_args` is appended after `" -- "` into `saved_command_line` (init/main.c 427, 637-655), so `/proc/cmdline` shows it while the kernel ignores it | HEALTHY rc 0 | **false HEALTHY** |
| 3 | `quiet resume="" resume_offset=3795013` | `next_arg` strips the quotes (lib/cmdline.c 242, 267-271) and `repair_env_string` rejoins `resume=` (init/main.c 463-476) → `strscpy(resume_file, "")` → `-ENOENT` (hibernate.c 984) | HEALTHY rc 0 | **false HEALTHY** |
| 4 | `resume=/dev/mapper/root resume=/dev/mapper/bogus resume_offset=3795013` | last wins (hibernate.c 1402-1409) → `/dev/mapper/bogus` → `-ENODEV` | HEALTHY rc 0 | **false HEALTHY** |
| 5 | `resume=/dev/mapper/root resume_offset=18446744073709551616` | overflow saturates at `ULLONG_MAX` (lib/kstrtox.c 50, 83-88) — not modulo | DEGRADED `[HR-OFFSET-MISMATCH, HR-SYSFS-OFFSET-MISMATCH]` rc 1 | agrees (both broken); gate reads the exact bigint |
| 6 | `resume=/dev/mapper/root resume_offset=3795013 quiet -- noresume` | `noresume` after `--` is inert → healthy resume | DEGRADED `[HR-NORESUME-ARG]` rc 1 | **false DEGRADED** (safe direction) |

### Why #1 is the worst, and it is not the parse

The token parse is right in every #1 row: `resume_file` gets exactly the string the gate sees. What fails is the
*device rule's input*: `capture-resume-facts-r84.py:81-88` only fills `resume_dev_majmin` when the value starts
`/dev/` **and** `stat -L` succeeds. Otherwise the field is `null` and rule 3 (`resume_dev_majmin set and !=
sys_power_resume`) is skipped — so a typo, a `UUID=`/`PARTUUID=`/`LABEL=`/`major:minor` value, or any quoted
path makes the device check vacuous and the gate answers HEALTHY on a host that cannot resume. The host's own
`resume=/dev/mapper/root` is the form that keeps rule 3 live here; any other form silently retires it.

Direct answer to the round's question: **v7.2 accepts `PARTUUID=`, `PARTLABEL=`, `/dev/…`, `major:minor` and a bare
hex devnum — and nothing else (early-lookup.c 244-253). There is no `UUID=` branch**, so `resume=UUID=…` is a
*broken* cmdline that the gate reports HEALTHY. `/dev/disk/by-uuid/…` is the form that works in both worlds: the
kernel resolves the symlink path through `devt_from_devname`, and the capture's `stat -L` fills
`resume_dev_majmin`, so rule 3 stays live.

### #4 is an internal inconsistency, not a kernel question

`capture-resume-facts-r84.py:81` takes the **first** `resume=` token (`next(...)`); the gate's `arg()`
(`tools/check-hibernate-resume.py:137-144`) takes the **last**, as the kernel does (hibernate.c 1402-1409). With
two tokens the facts' `resume_dev_majmin` describes device A while the gate reasons about device B — wrong in
both directions.

### #5 needs no code change; it needs one sentence in BP7

`resume_offset` in the gate is `int(leading digits)` with no bound; the kernel saturates to `ULLONG_MAX`. I could
not construct a realistic false HEALTHY from this (it needs `/sys/power/resume_offset` > 2^64−1), so the frozen
`OFFSET-SSCANF` family is not weakened. The entry's BP7 quote is accurate but silent on overflow.

## Non-divergences I tested and cleared (the frozen parse is faithful here)

- `hibernate=protect_image` and `hibernate=protect_imageXYZ` → kernel enables restore-image protection
  (hibernate.c 1433-1436) and stays resumable; gate HEALTHY. No finding is correct — the option is neither
  availability nor resume-chain. No divergence.
- `no-resume …` → does **not** match `noresume` in the kernel (`dash2underscore` maps `-`→`_`, so `no_resume` ≠
  `noresume`); gate HEALTHY. Agrees (the `-`/`_` equivalence is not a wildcard).
- bare `resume` token → no `__setup` match (parameqn compares the NUL against `=`); gate HR-NO-RESUME-ARG. Agrees.
- `noresume resume=…` and `nohibernate=1 resume=…` → kernel never copies the device (hibernate.c 1404-1405,
  1415-1416) and the initcall bails (1111-1112); gate DEGRADED. Agrees in direction (this is BP8, the declared
  order limit).
- `hibernate=no*` / `hibernate=noresume*` / `hibernate=nocompress*` prefix order (hibernate.c 1426-1432) → gate's
  `elif` chain reproduces it exactly.
- bootconfig `kernel.resume=…` lands **before** the bootloader cmdline (init/main.c 625-632), so the gate's
  last-wins still matches the kernel's.

## Smallest safe corrections (patches in this directory, nothing applied)

1. `patch-gate-tokens.diff` — replace `cmdline.split()` with a `next_arg`-faithful `tokens()` (quote stripping +
   `name=value` rejoin) that stops at a bare `--`. Closes #2, #3, #6. Adds three `--selftest` cases
   (`quoted-empty-resume`, `quoted-device`, `dashes-post-resume`).
2. `patch-capture-last-resume.diff` — capture takes the **last** `resume=` after the `--` cut and strips quotes.
   Closes #4 and makes the captured value consistent with the gate.
3. #1 needs a new finding (`HR-RESUME-DEVICE-UNRESOLVED`) plus a battery family, i.e. a docstring/rule-set
   amendment — **r87 scope**, not this wave: adding a finding changes the frozen C1 predicate.

### Evidence that (1) is C1-safe

```
$ python3 tools/resume-gate-battery-r86.py --gate <scratch>/gate.py
{"bases": ["host", "random0", "random1", "random2", "random3", "random4"], "cases": 231, "failed_families": [], "families_passed": 30, "families_total": 30, "order_head": ["HR-OFFSET-MISMATCH", "HR-NO-RESUME-ARG", "HIBERNATE-NOX", "MALFORMED", "HR-NO-RESUME-HOOK"], "target": 30, "verdict": "met"}
rc=0
$ python3 <scratch>/gate.py --selftest | tail -1
{"cases": 16, "failed": [], "selftest": "PASS"}
rc=0
```

No frozen family emits a quote or a `--`, so the patch changes no expectation; the candidate is unchanged on all
30 families (`candidate-battery.json`: 30/30, rc 0). That is exactly why C1 cannot see these defects: the
predicate certifies the rule set, and the rule set does not model the kernel's tokenizer.

## Routed to r87 (not applied; I do not edit lane files)

- **D1 (undeclared).** `tools/capture-resume-facts-r84.py:81-88` — device check vacuous for every `resume=` that
  is not a stat-able `/dev/…`; propose `HR-RESUME-DEVICE-UNRESOLVED` + family `RESUME-DEVICE-CLASS` (values:
  `UUID=…`, `8:2`, `0`, `PARTUUID=…`, `PARTLABEL=…`, `LABEL=…`, `/dev/mapper/typo`, quoted path).
- **D2 (undeclared).** `tools/capture-resume-facts-r84.py:81` first-vs-last, above.
- **D3 (declared limit, now quantified).** `tools/check-hibernate-resume.py:105-156` — apply
  `patch-gate-tokens.diff`; add families `DASHES-R86` and `QUOTED-R86` so the limit becomes a rule.
- **D4 (entry erratum).** `corpus/knowledge/hibernation-boot-parse-r86.md` BP7 — add: overflow saturates at
  `ULLONG_MAX` (lib/kstrtox.c v7.2 raw 50, 83-88), it does not wrap; and §Limits line 48 — add "and `resume=`
  values the capture cannot resolve to a major:minor leave the device rule unevaluated".
- **D5 (entry erratum).** §Limits line 48 currently says the entry "does not prove that no other v7.2 `__setup`
  string is a prefix of these tokens". My rows do not depend on that sweep; it stays open.

## Refusals

- No lane file, `MANIFEST.json`, `.ufo/state/`, sibling lane or fleet-root file was written; no `git`/`jj`
  mutation; no host write, no `/boot`, no sysctl, no swap or hibernate. `sudo -n` was not used.
- I did not run the three-run C1 count (another seat's assignment) and do not claim C1's verdict: my single
  candidate run (30/30, rc 0) is context for this report only.
- No tool was installed or upgraded.
