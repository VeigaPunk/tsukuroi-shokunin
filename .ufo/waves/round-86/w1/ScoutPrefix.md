# ScoutPrefix — round 86, wave w1: first-match collisions in the Linux v7.2 `__setup` table

**Question assigned.** Does any `__setup` / `early_param` string in Linux v7.2 capture a token meant for
`noresume`, `nohibernate`, `hibernate=`, `resume=`, `resume_offset=`? And are any of the five also reachable through
`early_param` / `core_param` / `module_param` (which would route them through `parse_one` before
`unknown_bootoption`)?

**Answer.** **No collision exists.** Across all **758** `__setup`/`early_param` registrations in the whole v7.2 tree
(every architecture, not just x86), each of the five hibernation option strings is matched by **exactly one**
registration — its own — and by nothing else, under the kernel's own `parameqn` comparison with `-` read as `_`.
The five are **not** registered via `early_param`, `core_param` or `module_param`. **The gate's rule is unchanged
by this sweep.** The one latent hazard found is a *macro* in `arch/sh` that reads as `__setup("no", …)` in a naive
text grep but expands to `"nofpu"`/`"nodsp"`; it is a hazard only if that macro is ever changed.

**Lane revision measured.** `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` →
`1e1caabcdd740a6429dd31d7aba3b725ff8c677d` (the declared entry commit; HEAD of `master`).

**Method.** A shallow sparse clone of tag `v7.2` under the seat scratch root
(`git clone --depth 1 --branch v7.2 --filter=blob:none --sparse https://github.com/torvalds/linux`), sparse-checkout
of all `*.c` (**36 927** files) plus `*.lds.S`. Every `__setup`/`early_param` invocation was extracted and its
string literal resolved, then the kernel's own match rule was re-implemented and run over the full table for every
hibernation token form. The clone was removed on exit (§Receipts).

**Trust anchor.** The five files of the clone are **byte-identical** to the lane's pinned snapshot
`.ufo/waves/round-86/before/src/` (`sha256` compared file by file), so every line cited below holds for the pinned
sources the round-86 declaration cites:

```
init/main.c vs pinned init_main.c: IDENTICAL
kernel/params.c vs pinned kernel_params.c: IDENTICAL
kernel/power/hibernate.c vs pinned kernel_power_hibernate.c: IDENTICAL
kernel/power/main.c vs pinned kernel_power_main.c: IDENTICAL
lib/vsprintf.c vs pinned lib_vsprintf.c: IDENTICAL
```

---

## 1. The rule being tested, and the two things that could break it

`init/main.c:201-228` (pinned `init_main.c` 201-228, clone `init/main.c` 201-228):

```c
201: static bool __init obsolete_checksetup(char *line)
202: {
203: 	const struct obs_kernel_param *p;
204: 	bool had_early_param = false;
205:
206: 	p = __setup_start;
207: 	do {
208: 		int n = strlen(p->str);
209: 		if (parameqn(line, p->str, n)) {
210: 			if (p->early) {
...
215: 				if (line[n] == '\0' || line[n] == '=')
216: 					had_early_param = true;
217: 			} else if (!p->setup_func) {
218: 				pr_warn("Parameter %s is obsolete, ignored\n",
219: 					p->str);
220: 				return true;
221: 			} else if (p->setup_func(line + n))
222: 				return true;
223: 		}
224: 		p++;
225: 	} while (p < __setup_end);
226:
227: 	return had_early_param;
228: }
```

`kernel/params.c:79-95` (pinned `kernel_params.c` 79-95):

```c
79: static char dash2underscore(char c)
80: {
81: 	if (c == '-')
82: 		return '_';
83: 	return c;
84: }
85:
86: bool parameqn(const char *a, const char *b, size_t n)
87: {
88: 	size_t i;
89:
90: 	for (i = 0; i < n; i++) {
91: 		if (dash2underscore(a[i]) != dash2underscore(b[i]))
92: 			return false;
93: 	}
94: 	return true;
95: }
```

Two consequences that decide the whole question:

**(a) A registration matches a token iff the registration string is a folded prefix of the token.** `n` is
`strlen(p->str)`, so the comparison is over the registration's own length only — a *prefix* test, in both
directions of interest: a registration shorter than the token can capture it, and a registration longer than the
token can be captured by it.

**(b) The walk stops at the first handler that returns non-zero — but a handler that returns 0 does *not* stop it.**
`setup_func(line + n)` returning 0 falls through to `p++` and the scan continues. This is the one place where a
"first match" reading is wrong, and it is why the benign `ro`/`root=` overlap in §5 does not actually steal
`root=`.

The kernel reaches `obsolete_checksetup` only from `unknown_bootoption` (`init/main.c:527`), which is itself the
`handle_unknown` of `parse_one` (`kernel/params.c:117-155`); `parse_one` first tries the builtin parameter table by
`parameq(param, params[i].name)` — an **exact** match — and only falls through to `handle_unknown` on no match.
`next_arg` (`lib/cmdline.c:237-285`) splits each token at its first `=`, so `param` handed to `parse_one` is the
name and `val` the value; `unknown_bootoption` then re-joins them with `repair_env_string` (`init/main.c:463-475`,
called at `init/main.c:518`) before calling `obsolete_checksetup(param)` at `init/main.c:527`, which is why the
handler sees the whole `name=value` token.

## 2. The registrations of interest

`kernel/power/hibernate.c:1518-1524` (pinned `kernel_power_hibernate.c`, identical):

```c
1518: __setup("noresume", noresume_setup);
1519: __setup("resume_offset=", resume_offset_setup);
1520: __setup("resume=", resume_setup);
1521: __setup("hibernate=", hibernate_setup);
1522: __setup("resumewait", resumewait_setup);
1523: __setup("resumedelay=", resumedelay_setup);
1524: __setup("nohibernate", nohibernate_setup);
```

Note the trailing `=` on three of them (`"resume="`, `"hibernate="`, `"resume_offset="`) and its absence on
`"noresume"` / `"nohibernate"`. That single character is what keeps the table unambiguous (§3, §4).

## 3. Result: the match sets

The kernel's rule re-implemented exactly (`parameqn` with `-`→`_` on both sides, over the registration's own
length) and applied to the full 758-entry table for each hibernation token form. Every token has **one** match —
the intended handler — and zero others:

| token | matches | registration | file:line |
|---|---|---|---|
| `noresume` | 1 | `__setup "noresume"` | `kernel/power/hibernate.c:1518` |
| `noresume=1` | 1 | `__setup "noresume"` | `kernel/power/hibernate.c:1518` |
| `noresume=0` | 1 | `__setup "noresume"` | `kernel/power/hibernate.c:1518` |
| `noresumefoo` | 1 | `__setup "noresume"` | `kernel/power/hibernate.c:1518` |
| `nohibernate` | 1 | `__setup "nohibernate"` | `kernel/power/hibernate.c:1524` |
| `nohibernate=1` | 1 | `__setup "nohibernate"` | `kernel/power/hibernate.c:1524` |
| `hibernate=noresume` | 1 | `__setup "hibernate="` | `kernel/power/hibernate.c:1521` |
| `hibernate=nocompress` | 1 | `__setup "hibernate="` | `kernel/power/hibernate.c:1521` |
| `hibernate=noxyz` | 1 | `__setup "hibernate="` | `kernel/power/hibernate.c:1521` |
| `hibernate=protect_image` | 1 | `__setup "hibernate="` | `kernel/power/hibernate.c:1521` |
| `resume=/dev/mapper/root` | 1 | `__setup "resume="` | `kernel/power/hibernate.c:1520` |
| `resume=` | 1 | `__setup "resume="` | `kernel/power/hibernate.c:1520` |
| `resume=UUID=xyz` | 1 | `__setup "resume="` | `kernel/power/hibernate.c:1520` |
| `resume_offset=4096` | 1 | `__setup "resume_offset="` | `kernel/power/hibernate.c:1519` |
| `resume_offset=abc` | 1 | `__setup "resume_offset="` | `kernel/power/hibernate.c:1519` |
| `resume-offset=4096` | 1 | `__setup "resume_offset="` | `kernel/power/hibernate.c:1519` |

Verbatim from the emulator receipt (`.ufo/waves/round-86/w1/ScoutPrefix/collision-emulator.txt`):

```
A) registrations scanned: 758 (757 literal + 1 macro-expanded pair)
...
  ALL FIVE OPTIONS CLEAN: True
```

## 4. The four collision classes, checked exhaustively

**Class 1 — strict prefix of an option string** (would capture *every* token of that option). Every prefix of each
of the five option strings was looked up in the folded registration set. The only hits are the five intended
registrations themselves:

```
=== A) STRICT PREFIX collisions (R proper prefix of an option string, '-'=='_' folded)
   COLLISION 'noresume' <- __setup 'no' arch/sh/kernel/cpu/init.c:50      <-- ARTIFACT, see §6
   COLLISION 'nohibernate' <- __setup 'no' arch/sh/kernel/cpu/init.c:50   <-- ARTIFACT, see §6
=== B) registration string EQUAL to an option string (the intended handler)
   'noresume'       __setup  kernel/power/hibernate.c:1518
   'nohibernate'    __setup  kernel/power/hibernate.c:1524
   'hibernate='     __setup  kernel/power/hibernate.c:1521
   'resume='        __setup  kernel/power/hibernate.c:1520
   'resume_offset=' __setup  kernel/power/hibernate.c:1519
```

**Class 2 — registration longer than the option whose folded form starts with the option** (would capture tokens
that merely *start* with the option). **NONE** for all five. The nearest neighbour in the whole tree is
`__setup("hibernate_compression_threads=", hibernate_compression_threads_setup)` at `kernel/power/swap.c:1710`, and
it does **not** collide, because the option is `"hibernate="` (10 chars) and `"hibernate_compression_threads="`
begins `hibernate_` — position 9 is `_`, not `=`:

```
=== reverse: is any option string a prefix of a LONGER registration? ===
  'noresume'       -> NONE
  'nohibernate'    -> NONE
  'hibernate='     -> NONE
  'resume='        -> NONE
  'resume_offset=' -> NONE
```

**Class 3 — hyphen/underscore siblings** (a registration whose folded form equals an option). Only the five
themselves; there is no `"no-resume"`, `"nohibernate"`-with-dash, or `"resume-offset="` registration anywhere.

**Class 4 — the five name-parts reachable via `early_param` / `core_param` / `module_param`.** **NONE.**
* `early_param`: `do_early_param` (`init/main.c:721-735`) matches with `parameq(param, p->str)` — an **exact**
  name match — and calls `p->setup_func(val)`. No `early_param` in v7.2 is named `resume`, `noresume`,
  `nohibernate`, `hibernate` or `resume_offset`.
* `core_param` / `module_param` / `module_param_cb` / `module_param_array` / `module_param_named` /
  `core_param_cb` / `core_param_unsafe` / `postcore_param*`: **4 178** distinct builtin parameter names extracted
  from the whole tree; **none** equals any of the five name-parts (the only near misses are `autoresume`,
  `autoresume_interval_ms`, `max_autoresume`, `turn_on_panel_on_resume` — all different names, and `parameq` is
  exact). `parse_one` (`kernel/params.c:131`) matches the builtin table with `parameq` too, so none of these can
  preempt the `__setup` path.

Full list of the only registrations in the whole tree that mention `resume`/`hibern` outside `hibernate.c`:

```
__setup	hibernate_compression_threads=	kernel/power/swap.c	1710
```

### Two routes that would preempt, checked and clear

* `unknown_bootoption` (`init/main.c:503-530`) runs `sysctl_is_alias(param)` at `init/main.c:515` **before**
  `obsolete_checksetup` at `init/main.c:527`. `sysctl_is_alias` (`fs/proc/proc_sysctl.c:1606-1611`) resolves
  `sysctl.`-style aliases only; no alias matches `resume`/`noresume`/`nohibernate`/`hibernate`/`resume_offset`.
* The bootloader identifiers `{"BOOT_IMAGE=", "kexec", NULL}` (`init/main.c:512`) are tested with `strstarts`
  at `init/main.c:522`; none of the five starts with either.

## 5. Positive control — the method does detect real overlaps

A sweep that finds nothing proves nothing unless it can find something. Two real overlaps in v7.2, both benign, both
caught by the same scan:

**`ro` vs `root=`** (`init/do_mounts.c:53` and `init/do_mounts.c:62`) — `"ro"` is a *strict prefix* of `"root="`,
so the token `root=/dev/sda1` matches **both** registrations:

```
C) POSITIVE CONTROL -- a real prefix collision that exists in v7.2 (method detects it)
  token 'root=/dev/sda1' -> 2 match(es):
        __setup     'ro'           init/do_mounts.c:53 fn=, readonly
        __setup     'root='        init/do_mounts.c:62 fn=, root_dev_setup
```

It is benign *because of rule (b) of §1*: `readonly` (`init/do_mounts.c:37-44`) returns 0 when its argument is
non-empty (`if (*str) return 0;`), so the scan **continues** and `root=` still gets the token. Had `readonly`
returned 1, `root=` would have been lost. This is the exact mechanism that would have broken the hibernation
options had a shorter prefix existed — and none does.

**`ro` vs `rootflags=` / `rootfstype=`** — likewise caught by the same scan (the host cmdline in §7 shows
`rootflags=subvol=@` and `rootfstype=btrfs` each matching `ro` first and the real option second).

## 6. The one real hazard: `arch/sh`'s `"no" __stringify(x)` macro

`arch/sh/kernel/cpu/init.c:42-53`:

```c
42: #define onchip_setup(x)					\
...
50: __setup("no" __stringify(x), x##_setup);
51:
52: onchip_setup(fpu);
53: onchip_setup(dsp);
```

A text-level grep of the registration list shows the literal `"no"` here, and `"no"` **is** a strict prefix of both
`"noresume"` and `"nohibernate"` — it is the only candidate collision in the entire tree. It is an **artifact**:
the macro expands to `"nofpu"` and `"nodsp"`, which are not prefixes of anything hibernation-related:

```
=== CLASS 1: hyphen/underscore siblings of the five (folded-equal) ===
  'noresume'       -> [('__setup', 'noresume', 'kernel/power/hibernate.c', 1518)]
  'nohibernate'    -> [('__setup', 'nohibernate', 'kernel/power/hibernate.c', 1524)]
```

**Why it still matters to report.** `"no"` is the only string in v7.2 that would capture `noresume` *and*
`nohibernate` if it existed, because `arch/sh`'s `cpu_idle_poll_setup`-style handlers return 1 (they set a flag and
return 1, `arch/sh/kernel/cpu/init.c:45-49`) and would therefore stop `obsolete_checksetup` at the first
`noresume`/`nohibernate` token — silently disabling hibernation on SuperH. Today the macro is `"no" __stringify(x)`
and the two expansions are `"nofpu"`/`"nodsp"`, so the hazard is **latent, not active**: it fires only if that
macro is changed to a bare `"no"`, or if any tree adds `__setup("no", …)`. The mitigation is structural — the
`=`-terminated option strings (`"resume="`, `"hibernate="`, `"resume_offset="`) cannot be shadowed by a bare
`"no"`-style name anyway, and `"noresume"`/`"nohibernate"` are protected only by their length.

Note also that `arch/sh` is not the host architecture (`uname -m` → `x86_64`), so the sweep deliberately covered
**all** architectures rather than the host's, so that the "no other `__setup` string in v7.2" claim is a statement
about the kernel source, not about this host.

## 7. Host check

The host cmdline (`.ufo/waves/round-86/before/host/receipt.txt`, `2026-11-06T17:55:05-03:00`, read-only) is

```
resume=/dev/mapper/root resume_offset=3795013 quiet splash loglevel=0 systemd.show_status=false
rd.udev.log_level=0 vt.global_cursor_default=0 cryptdevice=PARTUUID=cf3d875f-…:root:allow-discards,
no-read-workqueue,no-write-workqueue root=/dev/mapper/root zswap.enabled=1 zswap.max_pool_percent=25
rootflags=subvol=@ rw rootfstype=btrfs
```

Run through the same table:

```
F) host cmdline hibernation tokens vs the whole table
  'resume=/dev/mapper/root'          -> [('resume=', 'kernel/power/hibernate.c:1520')]
  'resume_offset=3795013'            -> [('resume_offset=', 'kernel/power/hibernate.c:1519')]
  'root=/dev/mapper/root'            -> [('ro', 'init/do_mounts.c:53'), ('root=', 'init/do_mounts.c:62')]
  'rootflags=subvol=@'               -> [('ro', 'init/do_mounts.c:53'), ('rootflags=', 'init/do_mounts.c:121')]
  'rootfstype=btrfs'                 -> [('ro', 'init/do_mounts.c:53'), ('rootfstype=', 'init/do_mounts.c:122')]
```

The two hibernation tokens on this host each match exactly one registration. `resume=` and `resume_offset=` are
unshadowed. (`root=`/`ro` is the benign overlap of §5.)

## 8. Does any of this change the gate's rule?

**No.** The gate implements the same prefix rule (`tools/check-hibernate-resume.py:106-109`):

```python
def matches(tok, setup):
    """obsolete_checksetup: the first len(setup) characters equal setup, '-' read as '_' (parameqn)."""
    n = len(setup)
    return len(tok) >= n and tok[:n].replace("-", "_") == setup.replace("-", "_")
```

This is `parameqn` plus the length guard. The length guard is not cosmetic — it is what makes the gate agree with
the kernel on the *shorter-token* side, where the kernel's `parameqn` would read past the token's NUL and compare
`'\0'` against a non-`'\0'` registration character:

* token `noresum` (7 chars) vs option `noresume` (8) — kernel: `parameqn` compares 8 bytes, byte 7 is the token's
  `'\0'` against `'e'` → false. Gate: `len("noresum") >= 8` is false → no match. **Agree.**
* token `resume` (6) vs option `resume=` (7) — kernel: byte 6 is `'\0'` vs `'='` → false. Gate: `6 >= 7` false.
  **Agree.**
* token `hibernate` (9) vs option `hibernate=` (10) — same. **Agree.**

The gate's DECOYS family (`tools/check-hibernate-resume.py:232`, `"noresum no_resume xnoresume nohibernat"`)
therefore decodes exactly as the kernel does: `no_resume` differs from `noresume` at position 2 (`_` vs `r`, and
`dash2underscore` maps `-`→`_` on *both* sides but never `_`→`-`), and `xnoresume`/`nohibernat` fail on length or
first character.

So the frozen rule set in the r86 battery docstring — "a token selects a boot option when its first len(option)
characters equal the option with `-` read as `_`" — is **exactly** the kernel rule, and the sweep shows it is
**unambiguous**: for these five options there is no second candidate anywhere in v7.2, so the gate never has to
break a tie, never has to model link order, and never has to model a handler that returns 0 and lets the scan
continue.

### One adjacent observation, explicitly out of scope

The kernel's `hibernate_setup` (`kernel/power/hibernate.c:1424-1438`) tests `"noresume"` (8), then `"nocompress"`
(10), then `"no"` (2), and the `"no"` branch sets **both** `noresume = 1` and `nohibernate = 1`. The gate's
`availability()` (`tools/check-hibernate-resume.py:112-135`) sets only `disabled = True` for a `hibernate=V` with
`V` starting `no`. The *finding* is the same one either way (HR-HIBERNATE-DISABLED is reported, and `noresume`
would additionally suppress resume), so this is a difference in internal flags, not in reported findings, and it
is the **round-85** rule set which the round-86 declaration freezes unchanged. It is recorded here only because
the sweep read that handler; it is **not** a defect raised by this seat and **not** a proposed change.

## 9. What this sweep does and does not establish

**Establishes (source-level, whole-tree):**
* No `__setup`/`early_param` string in Linux v7.2 is a prefix of `noresume`, `nohibernate`, `hibernate=`,
  `resume=` or `resume_offset=` (folded), and none of those five is a prefix of a longer registration.
* Each of the five hibernation tokens is matched by exactly one registration in the whole tree.
* None of the five is reachable via `early_param`, `core_param` or `module_param`; neither `sysctl_is_alias` nor
  the bootloader-identifier check preempts them.

**Does not establish (limits, matching the C2 entry's own stated limits):**
* Nothing about **link order** within the `__setup` table. It was not needed here (no ties to break) but it is not
  modelled and not measured.
* Nothing about **token order** on the command line (the round-86 C2 entry BP8 already records that the gate does
  not model it), quoted values, tokens after `--`, or bootconfig-supplied options.
* The sweep is a **source** result for tag `v7.2`; the host runs 7.2.11-arch1-1. The host's two hibernation tokens
  were checked against the same table (§7) and are unshadowed.
* No hibernate, suspend, swap, reboot or sysctl write was performed; the host was read only.

## 10. Proposed patches

**None.** No defect was found in the gate, the battery, or the C2 entry, so there is nothing to propose. The C2
entry `corpus/knowledge/hibernation-boot-parse-r86.md` currently records, under *Limits*:

> "Other `__setup` strings are searched in link order and the first handler that returns true wins; this entry
> does not prove that no other v7.2 `__setup` string is a prefix of these tokens (wave scout sweep: see the lesson
> Gate)."

This sweep is that sweep, and it **discharges the open half of that limit**: the entry's *own* statement that no
other v7.2 `__setup` string is a prefix of these tokens is now established for the whole tree. If the L1 wants the
limit narrowed, the precise replacement for the first half of that sentence is a statement of the *actual* kernel
semantics rather than the shorthand — that the scan stops at the first handler that returns **non-zero**, and a
matching handler that returns 0 lets the scan continue (`init/main.c:221-222`) — together with the measured fact
that for these five options there is exactly one matching registration in v7.2, so link order cannot matter here.
That is a wording suggestion for the L1, not a patch from this seat; this seat proposes no edit to any lane file.

## Receipts

| receipt | path |
|---|---|
| collision emulator output (full) | `.ufo/waves/round-86/w1/ScoutPrefix/collision-emulator.txt` |
| every registration extracted, with file:line | `.ufo/waves/round-86/w1/ScoutPrefix/all-registrations.txt` |
| all 4 178 builtin parameter names | `.ufo/waves/round-86/w1/ScoutPrefix/builtin-param-names.txt` |

### Commands (cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`)

```
$ git rev-parse master
1e1caabcdd740a6429dd31d7aba3b725ff8c677d

$ python3 tools/resume-gate-battery-r86.py --gate tools/check-hibernate-resume.py
{"bases": ["host", "random0", "random1", "random2", "random3", "random4"], "cases": 231, "failed_families": [],
 "families_passed": 30, "families_total": 30, "order_head": ["HR-NO-RESUME-HOOK", "HR-SYSFS-OFFSET-MISMATCH",
 "MULTI-SWAP", "HIBERNATE-NOX", "HR-OFFSET-MISSING"], "target": 30, "verdict": "met"}
EXIT=0
```

Run once, as evidence that the instrument at the landed tip is intact and the freeze manifest still matches
(`a49a18aa21322579f723cbddd38f0fcdff686cde85f525a9a81976ef176fbc21  tools/resume-gate-battery-r86.py` — identical
to the freeze-manifest entry). Not a claim of the three-run C1 target, which is the C1 seat's to run.

### Tooling

**No tool was installed, upgraded or removed.** `/home/vgpnk/.omp/agent/RULES.md` was read first; no pacman, `uv
tool`, `npm` or `cargo` transaction was needed, so nothing to record there. The only tools used were the ones
already present: `git`, `python3`, `sha256sum`, `curl`, `grep`.

### Scope compliance

* The Linux clone lived entirely under the seat scratch root `/fast/scratch/hyaku/tsukuroi-r86/ScoutPrefix/` and was
  **removed on exit**; the scratch directory was removed with it. Nothing was written outside
  `.ufo/waves/round-86/w1/ScoutPrefix.md` and `.ufo/waves/round-86/w1/ScoutPrefix/`.
* No git/jj mutation was performed (`git add|commit|push|stash|checkout|switch|reset|pull` never run; the only
  git commands were `rev-parse`, `clone` into scratch, `grep`, `ls-files`, `sparse-checkout`, `show`).
* The host was read-only: no hibernate, suspend, swapon/swapoff, no write to `/sys` or `/proc`, no sysctl change,
  no `/boot` touch, no mkinitcpio, no pacman. `sudo -n` was never needed.
* No subagent was dispatched (leaf seat); no model was chosen.
