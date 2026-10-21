# WrapperSudoLong — round-20 falsify

- Seat: `TsukuroiR19Recovery.WrapperSudoLong` (scout, leaf; no dispatch).
- Baseline: `0cbc34dd6b20896085a8fb07943e3ea4027d8472`. Lane: `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin`.
- **C** = `/tmp/tsukuroi-r20-execscope-20261021/tools/check-recheck-commands.py` (1558 lines). It is the only worktree with the sudo `--user` change.
- **B** = `tools/check-recheck-commands.py` in the lane (1408 lines). Worktrees binder, registry, and adjacency carry the same sudo entry as B at `:79` (`"sudo": ({"-u", "-g", "-C", "-h", "-p", "-r", "-t", "-U", "-D"}, 0)`).
- Tags: [obs] read from source or artifact; [inf] inference; [unk] unresolved.
- Method: read, grep, and glob only. This seat has no `lsp` tool, so callers were traced by literal grep. That is not semantic proof. Nothing was executed.

## Answers to the three checks

1. **Root is skipped as sudo's argument: yes, for the exact spellings `--user <v>` and `--user=<v>`, and only in C.** [obs]
   - C:80 adds `"--user"` to sudo's value-taking set. `command_word` (C:214) skips the pair at C:229-230 (`tokens[index] in options and index + 1 < size` → `index += 2`).
   - Trace of `sudo --user root systemctl --user cat example.service` in C: C:223 resolves `sudo`. Index 1 is `--user`, and C:229-230 move the index to 3. C:225 returns `("systemctl", 3)`. C:247 yields args `["--user","cat","example.service"]`. `_systemctl_read_only` (C:289) takes `cat` as the verb, which is a read verb, so there is no violation. The mutation twin `… --user restart x` makes the verb `restart`, which triggers the violation at C:344-345.
   - Trace in B: `--user` is absent from B:79. B:228 skips one token, so `root` is returned at B:221 and `systemctl` is never reached. This is the finding recorded in `build/ExecWrappers.md:5`.
   - `--user=root` is a single token and is correct in both trees. It is not in the set, C:232 skips one token, and C:225 returns `systemctl`.
2. **The nested systemctl is seen: yes, for this form in C.** The path runs C:225 → C:247 → C:289 → C:343-345, and on the exec-log side C:661-663. [obs]
3. **Hidden command gap: yes.** The change extends a list and leaves the mechanism alone. `command_word` decides a wrapper's argument count only by exact token membership (C:229). The body of `command_word` is the same as B:210-235 in the ranges I read. [obs] Any spelling whose argument is not a standalone member of the table, or whose command sits inside one token, still hides `systemctl` (G1-G8 below).

## Hidden-command gaps

Each row is a single exec-log line `$ …` with a `systemctl restart` payload. In C, `systemctl` is invisible to both `invocations` and `systemctl_violations`.

| ID | Input | Why it is hidden in C | In B |
|---|---|---|---|
| G1 | `sudo -Eu root systemctl restart x` (also `-iu`, `-Hu`) | `-Eu` is not a member of the set (C:79-81). The skip at C:232 consumes one token, and `root` is returned at C:225. [obs] Real sudo accepts the cluster by getopt convention. [inf] | Same. |
| G2 | `sudo -s 'systemctl restart x'`; `sudo -i '…'`; `sudo --shell '…'` | `words` keeps quoted text as one token (quote branch C:180-194). `-s` and `-i` take no argument, so the whole string is returned at C:225. `simple_commands` yields base `systemctl restart x` (C:247), which fails `== "systemctl"` (C:343). Unquoted `sudo -s systemctl restart x` stays visible. [obs] Sudo passing the string to `$SHELL -c` is [inf]. | Same. |
| G3 | `sudo bash -lc 'systemctl restart x'` | The shell recursion requires the exact token `-c` (C:267 in `invocations`, C:349 in `systemctl_violations`). `-lc` fails both. [obs] | Same logic in `invocations` (B:246). |
| G4 | `sudo -T 30 systemctl …`; `sudo -R /x systemctl …`; `sudo --command-timeout 30 systemctl …` | Not in C:79-81. The value token is returned at C:225 (`30`, `/x`, `30`). [obs] That sudo 1.9.17 takes these options with an argument is [inf]. | Same (B:79). |
| G5 | `env -S 'systemctl restart x'`; `env --split-string='…'`; `env -iS '…'` | `-S` is a set member (C:83), so the whole payload is consumed at C:229-230 and no command word remains. Nothing is yielded (C:246). `executable_argv0` (C:510, called at C:595-596) returns False for this case, so steer-safe sections fail closed. [obs] `--split-string=` (one token, not a set member) returns nothing. `-iS 'cmd'` returns the payload as a name and hides it the way G2 does. | `-S` at B:81. `--split-string` is absent in B and hides the same way. |
| G6 | `time -p systemctl restart x` | `time` is in `KEYWORDS` (C:75). It is skipped at C:219-221 before the WRAPPERS lookup at C:223. The `time` entry (C:88) is therefore unreachable for the keyword form, and `-p` is returned at C:225. [obs] The basename form `/usr/bin/time -p …` is not affected, because `time` then reaches C:88. | Same (B:75 keyword, B:86 entry). |
| G7 | `exec -a x systemctl restart y` | `exec` maps to an empty set (C:85). `-a` is skipped as a flag at C:232, and `x` is returned at C:225. [obs] | Same (B:83). |
| G8 | `xargs --replace systemctl restart {}` (also `--eof`, `--max-lines`) | C adds these to xargs's value set (C:94). `systemctl` is consumed at C:229-230 and `restart` is returned. [obs] **Regression against B:** B:91 does not list them, so B yields `systemctl`. The optional-argument arity in GNU findutils is [inf]. | B shows it. |

Visible controls in C: unquoted `sudo -s systemctl …`; `/usr/bin/time -p systemctl …` (basename reaches C:88, and `-p` is not in its set); `sudo --user root systemctl …`; `sudo -- systemctl …` (the loop at C:228 consumes `--`).

Non-bypass notes:
- C:79 treats `-h` as value-taking, and C:82 treats doas `--user` the same way. Neither tool executes a command after those tokens: sudo `-h` is help-only and doas has no long options. [inf] Nothing hidden runs.
- The `--` branch at C:233-234 is unreachable for `--`, because the option loop at C:228 consumes `--` first. [obs]

## Inheritance

- Exec-log: `assess_exec_log` (C:654) calls `invocations` at C:661 and `systemctl_violations` at C:663 (gated by C:662). Both use `simple_commands` (C:242-247), which calls `command_word` (C:214-239). Every G-row is invisible to both branches.
- Generic forbid set: `DEFAULT_FORBID` (C:62; B:62) is `pacman, checkupdates, yay, paru, mkinitcpio, limine-update`. G1-G8 also hide these binaries, not only systemctl.
- Knowledge-entry recheck gates: `follow_pointers` (C:542) and `assess_file` (C:584, C:604) call `invocations`. G1-G8 apply there too.
- `executable_argv0` (C:510; its `any(name.strip() …)` is at C:516) fails closed only when no name is returned, which is the G5 `-S` case. The G-rows that return a name pass it.
- Sibling worktrees binder, registry, and adjacency: `"sudo"` at `:79` is the baseline set, so the assigned case stays hidden there.

## Fixtures and artifacts

- C:1467-1488 is the `systemctl_reads` block. Its positive controls are C:1485 (`sudo --user root … cat`), C:1486 (`env --unset HOME … show`), and C:1487 (`timeout --signal TERM 2s … is-active`). `--user root` appears only at C:1485 in the candidate tools. There is no mutation control for the wrapped `--user root` form. [obs]
- A grep of C for `-Eu`, `-iu`, `-lc`, `sudo -s`, `sudo -i`, `sudo -R`, `sudo -T`, `command-timeout`, `time -p`, `exec -a`, `env -S`, and `split-string` hit only the WRAPPERS table (C:80, C:83) and C:1485. Not searched: `--replace`, `--eof`, `-iS`. [obs]
- Lane artifact `build/ExecWrappers.md:5` (baseline, High) states the exact-match mechanism at `:78-91,224-234`. C:229 keeps that mechanism unchanged. [obs]

## Installed-tool facts

- Installed sudo is `1.9.17.p2-6`, from `/var/lib/pacman/local/sudo-1.9.17.p2-6/desc` (`%VERSION%`). [obs]
- `sudo.8.gz`, `env.1.gz`, `bash.1.gz`, and `getopt.3.gz` exist but are gzip-compressed. `read` returns only a size header, and `grep` returns no matches. The result is inconclusive, not negative. [obs]
- No install or update was performed, and no package tooling was invoked.

## Limits and unknowns

- [unk] G4 depends on sudo 1.9.17 accepting `-R`/`--chroot`, `-T`, and `--command-timeout` with a separate argument. Upstream documents these [inf]. I could not confirm them with the permitted tools.
- [inf] G2, G3, and G5-G7 rely on documented semantics: sudo `-s`/`-i` run a `-c` shell string, bash `time [-p]` and `exec -a`, and GNU `env -S` splitting. The man pages are not readable here.
- [inf] G8 rests on the optional-argument arity of `--replace`, `--eof`, and `--max-lines` in GNU findutils.
- [unk] Exposure: a lane grep of `corpus/`, `tools/`, and `.ufo/` for `command-timeout|--chroot|-R directory|split-string|exec -a|time -p` returned only false positives (`uptime -p` and `…Realtime -p` in systemd property lists). The forms `-Eu`, `-s`/`-i` strings, `-iS`, `bash -lc`, and `xargs --replace` were not searched in the lane.
- Not run: the parser, any fixture, tests, host probes, `sudo --help`, `systemctl`, and boot checks. No host or boot safety claim is made. Boot images remain UNKNOWN.
- Check owner: the main agent can confirm G4 and G8 against the sudo 1.9.17 and findutils documentation before accepting them as findings. That check is outside this seat's NO-EXEC bound.

## Controls for L1 (recommendations; not run)

- Expect `EXEC-STEER-VIOLATION` for each gap line with a `systemctl restart` payload: `sudo -Eu root systemctl restart x`; `sudo -s 'systemctl restart x'`; `sudo bash -lc 'systemctl restart x'`; `sudo -T 30 systemctl restart x`; `env -S 'systemctl restart x'`; `time -p systemctl restart x`; `exec -a x systemctl restart y`; `xargs --replace systemctl restart {}`.
- Keep green: `$ sudo --user root systemctl --user cat example.service` (C:1485).
- Mechanism direction, not designed here: (a) re-parse a command word that contains whitespace, or follows sudo `-s`/`-i`/`--shell`/`--login` or env `-S`/`--split-string`, as shell text; (b) make the `-c` check cluster-aware (`-lc`, `-ec`); (c) let the `time` keyword consume `-p`; (d) give `exec` arity 1 for `-a`; (e) drop `--replace`, `--eof`, and `--max-lines` from the value set, or model optional attached arguments; (f) read each short-option cluster's arity from one table instead of exact-token membership.

Scope: executed=none
