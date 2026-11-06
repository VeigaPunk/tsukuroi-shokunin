# Draft — `## Frontier` paragraph for `corpus/README.md` (append at the end, round-86)

Seat ScribeLesson (w1), 2026-11-06. Draft only; the L1 lands it. Read at `1e1caabc`; the pinned-file listing is
this seat's read-only `grep` over `.ufo/waves/round-86/before/src/` (`r06`), not the full-tree sweep the entry's
`Limits` still owes.

## Text to append

### Frontier (round-86 addition)

- The `__setup` prefix rule is now pinned and frozen (S346 `init/main.c` raw 201-228, S347 `kernel/params.c` raw
  79-95; battery docstring `tools/resume-gate-battery-r86.py:7-19` at `2f67de80`), but the entry does not prove
  that no *other* v7.2 `__setup` string is a prefix of `noresume`, `nohibernate`, `resume=`, `resume_offset=` or
  `hibernate=`. `obsolete_checksetup` walks `__setup_start`..`__setup_end` in link order and returns at the first
  non-early handler whose function returns true (raw 201-228), so a second matching string would make the gate's
  single-rule model wrong on a token it currently reads clean. The five pinned files register thirteen setup
  strings (`grep -ho '__setup("[^"]*"' *.c` → `hibernate=, init=, initcall_blacklist=, nohibernate, noresume,
  pm_async=, pm_debug_messages, rdinit=, reset_devices, resume=, resumedelay=, resume_offset=, resumewait`), and
  none outside `kernel/power/hibernate.c`'s seven (raw 1518-1524) is a prefix of the five tokens; nine early
  params are registered in the same files (`debug`, `quiet`, `loglevel`, `bootconfig`, `randomize_kstack_offset`,
  `rodata`, `debug_boot_weak_hash`, `hash_pointers`, `no_hash_pointers`), none colliding. Next ground: enumerate
  every `__setup` and early-param string in the v7.2 tree and test each against the five tokens.
- Token order (BP8) is frozen as a limit, not modelled: a `noresume` before `resume=` makes `resume_setup` return
  early (raw 1404-1405) so `resume_file` is never copied, while a `noresume` after `resume=` leaves the device
  copied and the resume initcall bails (raw 1106-1112); the gate reports `HR-NORESUME-ARG` in both orders. The
  kernel state differs (no device at all versus a device that is never read); a gate that names the state rather
  than the token needs the order.
- Not modelled by the gate and not claimed by the entry: quoted values (`param="v"`), tokens after `--` (handed to
  init), and bootconfig-supplied options (entry `Limits`).
- Uncertified, and listed as such in the declaration: `sys_power_resume` whitespace handling. The battery never
  draws whitespace there, so no control exists; r85 `M28` survives only as a mutant of the r85 gate.
- secretmem/CXL have no fact key of their own. `kernel/power/main.c` is now pinned (S349, `state_show` raw
  762-763), so the next arm can read `/sys/power/disk` `[disabled]` beside `/sys/power/state` and name the
  blocker instead of reporting `HR-NO-DISK-STATE` alone — the r85 Frontier item, carried, now with its source.
- The r86 battery's discrimination is certified per property by N01-N12 (each 26-29/30, failing exactly its
  family); what it does not carry is a token that matches two setup strings, which is the first bullet above.

## Notes for the L1

- The first bullet is the one that needs a wave-scout receipt before landing: the entry's `Limits` says "wave
  scout sweep: see the lesson Gate", and the round-86 lesson's `## Gate` has no such row yet. If the sweep did not
  run, keep the bullet as open ground and drop the parenthetical promise from the entry, or land the sweep result.
- The listing above is scoped to the five pinned files and says so; do not let it read as a tree-wide claim.
