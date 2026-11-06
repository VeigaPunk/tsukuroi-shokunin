# ScoutSources — round 86 wave 1 (tsukuroi)

Lane revision measured: `git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin rev-parse master` →
`b96dc4beb8b826dab80ff07411b07c549c7a1b17` ("round-86: landing — lesson …"). The entry commit named in my
dispatch (`1e1caabcdd740a6429dd31d7aba3b725ff8c677d`) is its parent; every quote/range below was re-checked
against the **landed** blobs at `b96dc4be` (the wave landed while this seat was running).

Receipts (all under `.ufo/waves/round-86/w1/ScoutSources/`):
`live-refetch.txt`, `quotes-verification.txt`, `v7211-diff.txt`, `setup-prefix-sweep.txt`,
`further-sources-opened.txt`.

Scope: re-open every upstream source the round cites (item 1), locate every quote in the entry rows BP1–BP8 and
in SOURCES rows S346–S349 (item 2), re-fetch the same five files at tag **v7.2.11** and diff the cited regions
(item 3), and draft **one** candidate SOURCES row for a further tier-A source the entry Limits need (item 4,
drafted only — not appended).

---

## 1. Live re-fetch of every cited URL — HTTP 200, sha256 identical to the frozen `SHA256SUMS`

Command (cwd `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`, one `curl -sS -L` per URL, the URL list read from
`.ufo/waves/round-86/before/src/URLS.txt`), 2026-11-06T18:18:45-03:00. Full output: `ScoutSources/live-refetch.txt`.

| file | URL | curl rc | HTTP | time_total (s) | sha256 (live) | = SHA256SUMS | `cmp` vs pinned snapshot |
|---|---|---|---|---|---|---|---|
| init_main.c | https://raw.githubusercontent.com/torvalds/linux/v7.2/init/main.c | 0 | 200 | 0.021509 | `e895a643df800a83857b88bebb6e990c17cd0890e485a48a7b972f5d2ae73516` | YES | IDENTICAL |
| kernel_params.c | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/params.c | 0 | 200 | 0.015834 | `51c0eb1dc55d1fcb6b32f6cd66a2ff93d2b516864e6b28a4e4bb583169b8771f` | YES | IDENTICAL |
| kernel_power_main.c | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/power/main.c | 0 | 200 | 0.015461 | `7b60dabe707cf070b416f6375946c213b96bf3f67c3161b69c9a4fcfc9f53955` | YES | IDENTICAL |
| kernel_power_hibernate.c | https://raw.githubusercontent.com/torvalds/linux/v7.2/kernel/power/hibernate.c | 0 | 200 | 0.016450 | `ae3dbeb6ae682c3e03b750d45138aa5644a2db04cfc21c70c59446dad0af86c1` | YES | IDENTICAL |
| lib_vsprintf.c | https://raw.githubusercontent.com/torvalds/linux/v7.2/lib/vsprintf.c | 0 | 200 | 0.054263 | `cabb648a2c72fcbd4a1b00cbbf442ad11235f3224071f5e662db4a77993469ca` | YES | IDENTICAL |

All five re-fetched bytes are byte-identical to the frozen snapshot and to `SHA256SUMS`; the round's pins are
still live-exact. (`kernel_power_hibernate.c` is also byte-identical to the r85 pin — `cmp` silent — so S343 remains
a re-open, not a new row, exactly as the lesson's Gate records.)

## 2. Every quote located at its cited raw lines

Method: each quote is a whitespace-normalized join of consecutive cited lines of the pinned snapshot (the landed
entry states this convention at `corpus/knowledge/hibernation-boot-parse-r86.md:21`); each `…`-separated fragment
was searched inside the cited range. Machine output: `ScoutSources/quotes-verification.txt`.

| Row | source, cited raw lines | quote | words (≤25) | verbatim at cited lines? | cited lines right? |
|---|---|---|---|---|---|
| BP1 | S346 201-228 | `int n = strlen(p->str); if (parameqn(line, p->str, n)) {` | 9 | YES (raw 208+209) | YES — inside `obsolete_checksetup` |
| BP2 | S347 79-95 | `if (dash2underscore(a[i]) != dash2underscore(b[i])) return false;` | 6 | YES (raw 91+92) | YES — `parameqn` body |
| BP3 | S346 503-532 | `repair_env_string(param, val);  …  if (obsolete_checksetup(param)) return 0;` | 7 | YES, both fragments (raw 518; raw 527+528) | YES — inside `unknown_bootoption` |
| BP4 | S343 1440-1444, 1461-1466, 1518, 1524 | `static int __init noresume_setup(char *str) { noresume = 1; return 1; }` | 12 | YES (raw 1440-1444) | YES — `noresume_setup`, plus the two `__setup` table rows |
| BP5 | S343 1402-1409 | `if (noresume) return 1; strscpy(resume_file, str);` | 6 | YES (raw 1404+1405+1407) | YES — `resume_setup` |
| BP6 | S343 46, 982-985 | `if (!strlen(resume_file)) return -ENOENT;` | 4 | YES (raw 984+985) | YES — `find_resume_device` |
| BP7 | S343 1411-1422; S348 3662-3681, 79-95 | `if (sscanf(str, "%llu", &offset) == 1) swsusp_resume_block = offset;` | 9 | YES as the S343 fragment (raw 1418+1419); the S348 half of the citation carries the *supporting* text, not the quoted line | YES |
| BP8 | S343 1402-1405, 1106-1112 | `If the user said "noresume".. bail out early.` | 8 | YES (raw 1109) | YES — `software_resume_initcall` comment |

Verbatim: **8/8** quotes located at the cited raw lines; every one ≤ 25 words (max 12, BP4). No quote is
not-verbatim and no cited range is wrong.

Two citation details I re-checked against the landed entry (both correct as landed, and both were corrected in
`b96dc4be` from the pre-landing text I first read):

- BP4's `raw_lines` now reads `1440-1444, 1461-1466, 1518, 1524` — `nohibernate_setup` really does end at 1466
  (`}`), so `1461-1465` (pre-landing) clipped the closing brace. Landed range is right.
- BP7's `raw_lines` now reads `1411-1422; 3662-3681, 79-95` and its statement names `simple_strntoull` (raw 79-95
  = `lib/vsprintf.c:79-101`; the citation's 79-95 window covers the function head and the `_parse_integer_limit`
  call at 89). Verified: `lib/vsprintf.c:79-95` is `simple_strntoull`, and the digit loop it calls is
  `lib/kstrtox.c:_parse_integer_limit` (raw 58-95) — the entry's "not pinned" note is accurate.

### SOURCES rows S346–S349 and the S343 used-by change

| row | registry anchor | verified |
|---|---|---|
| S346 | `init/main.c` raw 201-228, 463-475, 503-532 | YES — `obsolete_checksetup` (201), `repair_env_string` (463), `unknown_bootoption` (503). Pinned sha256 in the row = the live sha256. |
| S347 | `kernel/params.c` raw 79-95 | YES — `dash2underscore` (79) + `parameqn` (86). |
| S348 | `lib/vsprintf.c` raw 79-95, 3458, 3644-3681 (landed) | YES — `simple_strntoull` (79), `vsscanf` (3458), integer conversion (3644-3681). |
| S349 | `kernel/power/main.c` raw 750-770 | YES — `state_show` (750-770), `hibernation_available()` test at 762-763. |
| S343 used-by old→new | `corpus/knowledge/hibernation-availability-r85.md` → `…r85.md, corpus/knowledge/hibernation-boot-parse-r86.md` | YES — the landed row (SOURCES.md:354) carries exactly the two paths; the r86 entry does cite S343 (rows BP4–BP8), and the r85 entry still cites it. |

Census on the landed `corpus/SOURCES.md` (the seven frozen registry commands, run read-only):
349 rows, malformed 0, tier enum `A=332 B=6 C=11`, status enum `mined=311 queued=5 rejected=33`, duplicate ids 0,
enum violations 0, missing used-by paths 0, reverse-cite violations 0 **for the rows this round touched**
(the 26 `nocite` lines the reverse-cite command prints are all pre-existing r17–r54 rows, none of them S343–S349).

**One registry asymmetry worth the L1's attention (a real defect, in the S346 row).** `S346`'s `used-by` cell lists
only `corpus/knowledge/hibernation-boot-parse-r86.md`, but the r85 entry cites **S346** twice
(`corpus/knowledge/hibernation-availability-r85.md:3` — "S346 (init/main.c) … added round 86" — and `:56` —
"pinned round 86 as S346 (raw 201-228)"). The row's used-by cell therefore under-reports its own users.
`S349`'s row is **not** affected: its used-by entry (`hibernation-availability-r85.md`) does name it (lines 3, 70),
so that row is true as it stands — the r86 round pinned the file, but the r86 entry does not cite it, and
adding the r86 entry to that cell would *break* the reverse-cite census command (which requires every used-by
path to name the row id). Proposed fix (L1's call, not landed by me): `used-by` for S346 →
`corpus/knowledge/hibernation-availability-r85.md, corpus/knowledge/hibernation-boot-parse-r86.md`.
Patch sketch in `ScoutSources/proposed-SOURCES-usedby.patch`.

## 3. v7.2.11 — the same five files at the host's kernel version, and the cited-region diff

Fetched with the URL form the seat spec names, `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/<path>?h=v7.2.11`
(all HTTP 200, curl rc 0; times 0.49–0.70 s). Full receipt: `ScoutSources/v7211-diff.txt`.
The tag exists upstream: `git ls-remote --tags …/stable/linux.git 'refs/tags/v7.2.1[01]'` →
`refs/tags/v7.2.10 57eee103859fa039a1f2bf343c4453ef40661be8` and `refs/tags/v7.2.11 8316c24ec1b77dba19ba072ca4fe251b36dc65d3`.

Line shifts at the cited regions (content compared region by region, whitespace-stripped):

| cited region | v7.2 lines | v7.2.11 lines | shift | content identical? |
|---|---|---|---|---|
| S346 `obsolete_checksetup` | 201-228 | 201-228 | +0 | YES |
| S346 `repair_env_string` | 463-475 | 468-480 | **+5** | YES |
| S346 `unknown_bootoption` window | 503-532 | 508-537 | **+5** | YES |
| S347 `dash2underscore`+`parameqn` | 79-95 | 79-95 | +0 | YES |
| S343 `resume_file` default | 46 | 46 | +0 | YES |
| S343 `find_resume_device` | 982-985 | 984-987 | **+2** | YES |
| S343 `software_resume_initcall` | 1106-1112 | 1108-1114 | **+2** | YES |
| S343 `resume_setup` | 1402-1409 | 1404-1411 | **+2** | YES |
| S343 `resume_offset_setup` | 1411-1422 | 1413-1424 | **+2** | YES |
| S343 `noresume_setup` | 1440-1444 | 1442-1446 | **+2** | YES |
| S343 `nohibernate_setup` | 1461-1466 | 1463-1468 | **+2** | YES |
| S343 `__setup("noresume",…)` / `__setup("nohibernate",…)` | 1518 / 1524 | 1520 / 1526 | **+2** | YES |
| S349 `state_show` | 750-770 | 750-770 | +0 | YES |
| S348 `simple_strntoull` | 79-95 | 79-95 | +0 | YES |
| S348 `vsscanf` | 3458 | 3458 | +0 | YES |
| S348 integer conversion | 3644-3681 | 3644-3681 | +0 | YES |

**Every cited region is content-identical between v7.2 and v7.2.11; only line numbers move (+0/+2/+5).** The
shifts come from unrelated v7.2.x changes: `init/main.c` grew a bootconfig bounds-check hunk (+5 below raw 276),
and `kernel/power/hibernate.c` reordered `dpm_prepare`/`hibernate_preallocate_memory` relative to
`freeze_kernel_threads` (+2 below raw 400). `kernel_power_main.c` and `lib_vsprintf.c` are byte-identical across
the two tags; `init_main.c`, `kernel_params.c` and `kernel_power_hibernate.c` differ elsewhere (bootconfig
hardening; `param_set_charp` allocation rework; the hibernate ordering hunk) — none of it inside a cited region.

Freshness consequence for the entry: the entry's `Limits` says "Snapshots are tag v7.2; the host runs 7.2.11."
The measured content equality means **every BP1–BP8 statement holds verbatim on the host's own 7.2.11 kernel** —
the only thing the version difference changes is the raw line numbers, not the behaviour. That is a strictly
stronger statement than the landed Limits bullet, and it is measured, not inferred.

## 4. Prefix-collision sweep — independent re-derivation of the round's "no other registration matches" claim

Whole-tree sweep of Linux v7.2 (tarball `linux-7.2.tar.xz`, sha256
`f9fef3d14c0df53819026f4be74459835c2a0b0dcbf5b5bbd9ea19f0829402b3`, which matches the official
`https://cdn.kernel.org/pub/linux/kernel/v7.x/sha256sums.asc` entry for `linux-7.2.tar.xz` — checked, HTTP 200).
Same sweep run on v7.2.11 (`linux-7.2.11.tar.xz` sha256 `fd0fc479f983a8c05313f13e9c36330fe6651cf725396748c40d5cd93fa1e6a4`,
also matching the official `sha256sums.asc`). Receipt: `ScoutSources/setup-prefix-sweep.txt`.

Counts (my regex over `__setup("…")`, `early_param("…")`, `early_param_on_off("…")`, all `.c`/`.h`, all
architectures): **760 literal registrations** (416 `__setup`, 343 `early_param`, 1 `early_param_on_off`; the
3 `hugetlb_early_param(...)` sites are a different macro and are excluded), **697 distinct option strings**
after expanding the one macro site `arch/sh/kernel/cpu/init.c:50` (`__setup("no" __stringify(x), …)` → `nofpu`,
`nodsp`). The wave seat ScoutPrefix reported 758 registrations; the two numbers differ because the counts are
taken with different macro/identifier rules — my 760 counts `early_param_on_off` and the arch/sh macro site as
one literal each. **The collision conclusion is identical in both sweeps.**

Matching rule re-implemented from S346+S347: a registration `s` captures a token `t` iff
`fold(t[0:len(s)]) == fold(s)` with `fold('-') == '_'` (both sides folded — `parameqn` folds `a[i]` and `b[i]`
alike). Results, identical at v7.2 and v7.2.11:

| token | matching registrations |
|---|---|
| `noresume`, `noresume=0`, `noresume=1`, `noresumefoo` | `noresume` only |
| `noresum` | none (shorter than the option → no match) |
| `nohibernate`, `nohibernate=1` | `nohibernate` only |
| `resume`, `resume_offset`, `hibernate` (bare) | none |
| `resume=`, `resume=/dev/mapper/root` | `resume=` only |
| `resume_offset=3795013`, `resume-offset=3795013` | `resume_offset=` only |
| `hibernate=1`, `hibernate=noresume` | `hibernate=` only |
| `x.noresume=1` | none |

Two details this sweep pins down beyond the round's own claims:

- `resume-offset=3795013` folds to `resume_offset=3795013`, so the **dashed** form selects `resume_offset=` —
  the kernel really does accept the dashed spelling (BP2's claim), and it selects the *same* handler, so no
  other registration can capture it first.
- `x.noresume=1` matches **nothing**: the dotted form is not a prefix of `noresume`, so the dotted token is not
  routed to the hibernation handler (BP3's claim).

Also checked: no `module_param*`/`core_param` in the whole tree is named `resume`, `noresume`, `nohibernate`,
`hibernate` or `resume_offset` (so `parse_one`'s exact-name table cannot shadow a `__setup` handler), and the four
`sysctl_aliases` entries (`hardlockup_all_cpu_backtrace`, `hung_task_panic`, `numa_zonelist_order`,
`softlockup_all_cpu_backtrace`) do not touch these names. `include/linux/init.h` raw 318-346 confirms the
`__setup` table contract the sweep assumes: `struct obs_kernel_param { str; setup_func; early; }`, the table is
`__setup_start[]…__setup_end[]`, and a `__setup` handler returns 1 for "handled" / 0 for "not handled" — i.e. the
first handler that returns non-zero wins, which is exactly the `obsolete_checksetup` stop condition the entry's
Limits bullet names.

## 5. Findings for the L1 (defects and observations)

1. **`S346`'s `used-by` cell under-reports its users** (see §2): the r85 entry cites S346 at
   `corpus/knowledge/hibernation-availability-r85.md:3` and `:56`, but the row lists only the r86 entry. Patch
   sketch: `ScoutSources/proposed-SOURCES-usedby.patch` (not applied). `S349`'s row is correct as it stands and is
   deliberately left alone in that patch.
2. **The landed round cites wave-seat receipts that are not in the landed tree.** `corpus/lessons/round-86.md:42`
   cites `.ufo/waves/round-86/w1/ScribeLesson/01-mistakes-draft.md`; `corpus/lessons/round-86.md:61` cites
   `.ufo/waves/round-86/w1/CriticClaims.md`; `corpus/knowledge/hibernation-boot-parse-r86.md:50` cites
   `.ufo/waves/round-86/w1/ScoutPrefix.md` (and `ScoutPrefix/collision-emulator.txt`); the same entry's line 59
   cites `.ufo/waves/round-86/w1/CriticKernel.md`. The lane's own landing gate
   (`python tools/check-cited-receipts-r62.py --revision b96dc4be --round 86`, read-only) exits **rc=1** with
   **16 `CITED-RECEIPT-MISSING` findings** — the class this gate was built for (r59/r61/r62). The files exist
   in the worktree (untracked) but are absent from the landed tree; the fix is to land the wave-seat receipts
   under `.ufo/waves/round-86/w1/` in the next commit, which also makes the entry's `Limits` bullet and the
   lesson's M2 row verifiable on committed bytes. This is exactly the round's own claim being false on committed
   bytes, so it is worth an explicit landing step rather than a note.
   (This seat's own report and receipts are in the same class — `.ufo/waves/round-86/w1/ScoutSources.md` is
   listed in the gate's 16 findings — so they must land with the wave dir for the gate to go green.)
3. **Not a defect, a strengthening the L1 may want:** the entry's `Limits` bullet "Snapshots are tag v7.2; the
   host runs 7.2.11" can be replaced by the measured statement "every cited region is content-identical at
   v7.2.11 (line shifts +0/+2/+5 only)", because §3 above measured it region by region.
4. **Unrun:** I did not re-run the C1 battery (`tools/resume-gate-battery-r86.py`) or the gate
   (`tools/check-hibernate-resume.py`) — those are the executor seats' measurements and are outside this seat's
   scope; this report makes no claim about the gate's verdicts.

## 6. Candidate SOURCES row (drafted only — NOT appended, per the seat spec)

One further tier-A source that the entry's `Limits` needs and that the round does not currently pin:
**`include/linux/init.h`**. The entry's first `Limits` bullet rests on "`obsolete_checksetup` stops at the first
matching handler that returns non-zero" — the *meaning* of that return value (1 = handled, 0 = not handled) and
the existence/order of the `.init.setup` table live in `include/linux/init.h` raw 318-346, which no row cites.
Opened live, HTTP 200, sha256 `9315932d0c673d40e9f27e5102f206ffac85e90ecba08d024e2d520f1493aefe` (identical at
v7.2.11 — the file is byte-identical across the two tags), so one row serves both the pinned snapshot and the
host kernel.

Draft row, 11 columns in the census schema (id | source | kind | tier | scope | anchor | teaches | status |
opened | recheck | used-by), no `|` inside any cell:

```
| S350 | Linux v7.2 include/linux/init.h — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/linux/init.h | code | A | The __setup registration contract: the obs_kernel_param table the boot-token search walks, and what a handler's return value means | tag v7.2, raw lines 318-346 (struct obs_kernel_param, __setup_start/__setup_end, __setup_param into .init.setup, "NOTE: __setup functions return values: @fn returns 1 (or non-zero) if the option argument is 'handled' and returns 0 if the option argument is 'not handled'"); sha256 9315932d0c673d40e9f27e5102f206ffac85e90ecba08d024e2d520f1493aefe, byte-identical at tag v7.2.11 | a __setup handler is entered only when its registration string is a prefix of the token, and the first handler that returns non-zero ends the search, so an option is captured by its own registration and by no earlier one | queued | 2026-11-06 | on-release | corpus/knowledge/hibernation-boot-parse-r86.md |
```

Notes for the L1: id `S350` is free (the registry's highest id is S349); `used-by` points at the r86 entry, which
would have to cite `S350` in its `source:` line for the reverse-cite census command to pass; `lib/kstrtox.c`
(raw 43-95, sha256 `0c52ae02259f06adaf0a72a572e31ede4d8d6519e1b5625cb6b18d74db8d1ee4`, identical at v7.2.11) is the
other file the entry names as "not pinned" and would be a second candidate row if the L1 wants the digit loop
cited rather than described; it is **not** drafted as a row here because the seat spec asks for one.

## Tooling

No tool was installed or upgraded for this seat; no `pacman` transaction was made. Only `curl`, `git`
(read-only `ls-remote`), `sha256sum`, `cmp`, `diff`, `tar`, `python3` (stdlib) and the lane's own read-only
`tools/check-cited-receipts-r62.py` were used. Scratch root `/fast/scratch/hyaku/tsukuroi-r86/ScoutSources` was
removed on exit; all receipts were copied into
`.ufo/waves/round-86/w1/ScoutSources/` first. No lane file was modified; the only writes are this report, the
five receipt files, and the two proposed-patch files under my seat directory.
