# Gate record — S297, S298, S299, S300 (CORPUS rule 1)

Round 71 (hyaku run 15), wave w1, seat SC2Sources. Lane `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`
at `0fcfca315fbdf4ff6a47abeff08efa7fd27aa32e`.

Access date for every row: **2026-11-04** (`date -u +%FT%TZ` → `2026-11-04T00:55:41Z`). Every URL below
is the exact string the matching entry carries in `.ufo/waves/round-71/before/src/SOURCES.json`, and the
snapshot bytes are the committed ones under `.ufo/waves/round-71/before/src/` (`sha256sum -c SHA256SUMS`
→ `kernel-parameters.rst: OK`, `params.c: OK`, `moduleparam.h: OK`, `main.c: OK`, rc 0).

Each quote is verbatim from the named snapshot at the stated **1-based** lines, whitespace-normalized,
contains no pipe, and is at most 25 words (the counter's quote bound). Supporting locators cover the
parts of a row that the single primary quote does not.

## S297 — `kernel/params.c`

- URL: `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/kernel/params.c?h=v7.2.11`
- Snapshot: `params.c`, sha256 `923610d5de631d8b8dddcb89bf4b0f6932fb0dbf1f500d07453ea0b73b3782a4`
- Primary quote, line 669, 12 words: `/* Do not allow runtime DAC changes to make param writable. */`
- Supporting locators: line 634 `BUG_ON(!kp->perm);` (1 word); line 675
  `mk->mp->attrs[mk->mp->num - 1].mattr.attr.mode = kp->perm;` (5 words); line 569
  `if (!attribute->param->ops->get)` (2 words); line 586 `if (!attribute->param->ops->set)` (2 words,
  inside the row's anchor range 579-598, with `return -EPERM;` at 587).

## S298 — `include/linux/moduleparam.h`

- URL: `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/include/linux/moduleparam.h?h=v7.2.11`
- Snapshot: `moduleparam.h`, sha256 `220f2dac723a7b080211791a33cb3308ed12eaeb2309747232786d786cd14846`
- Primary quote, line 63, 10 words: `/* Returns 0, or -errno.  arg is in kp->arg. */`
- Supporting locators: line 65 `/* Returns length written or -errno.  Buffer is 4k (ie. be short!) */`
  (13 words); line 86 `const u16 perm;` (3 words); line 118 `@perm: visibility in sysfs.` (4 words).
  The 0444 and 0644 wording the row quotes sits at lines 124-127 and is not repeated here because the
  wrapped comment's leading `*` interrupts a multi-line verbatim substring.

## S299 — `kernel/module/main.c`

- URL: `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/kernel/module/main.c?h=v7.2.11`
- Snapshot: `main.c`, sha256 `e1e1a1c8a13f3d5e402bb8773b4aea3561dadcdca446b3dfb0482b0ddcb95929`
- Primary quote, line 3393, 7 words: `pr_warn("%s: unknown parameter '%s' ignored\n", modname, param);`
- Supporting locators: line 3407 `pr_err("Module %s is blacklisted\n", info->name);` (5 words) with
  line 3408 `return -EPERM;` (2 words); line 2953
  `core_param(module_blacklist, module_blacklist, charp, 0400);` (4 words).

## S300 — `Documentation/admin-guide/kernel-parameters.rst`

- URL: `https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git/plain/Documentation/admin-guide/kernel-parameters.rst?h=v7.2.11`
- Snapshot: `kernel-parameters.rst`, sha256 `45587d8e411db06dc600550f03236d3b7cbe7ad5bd898dbb9f965934ecd88799`
- Primary quote, lines 26-27, 18 words: `Parameters for modules which are built into the kernel need to
  be specified on the kernel command line.`
- Supporting locators: lines 20-21
  `Module parameters can be specified in two ways: via the kernel command line with a module name
  prefix, or via modprobe, e.g.::` (22 words); line 35
  `reveal their parameters in /sys/module/${modulename}/parameters/. Some of these` (8 words).

## Re-location status

All four primary quotes and all twelve supporting locators were re-located in the committed bytes on
2026-11-04 by whitespace-normalized containment over the declared span (`located=True` for each; see
`rows.md` §3 for the transcript of the four primary quotes). No quote was fetched from the network this
round; the snapshots are the pinned bytes the declaration committed.
