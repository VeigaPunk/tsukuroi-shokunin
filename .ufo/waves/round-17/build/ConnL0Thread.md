# ConnL0Thread — host-recovery thread vs the 09:15 -Syu

**Verdict:** closes the partial-upgrade *shape*, not the thread — risk moves from pending upgrades to 42.2 images whose late hooks target unmounted `/new_root`.

Thread (`.ufo/l0-questions.md`): `:54` hyaku HOST PARTIAL UPGRADE (keep/revert/full `-Syu` via tsukuroi's `/sysroot` gate); `:55` tsukuroi r15; `:60` tsukuroi r17. Only `:52–53` carry an `L0 ANSWER`.

Mark in the r17 report (append-only; queue untouched):

- `:54` **moot, not resolved** — option (c) ran 09:15:30 as `pacman -Syu --needed … linux-lts` from `~/Documents/nvhelpme` (boot-chain-capture.txt:59,82; 448 records, fresh-capture.txt:84). The `/sysroot` gate was bypassed, so keep/revert close (libinput-1.32.0-1 now in a full-upgrade set, fresh-capture.txt:27) without validating it.
- `:55` **split** — recovery choice superseded; "host-wide" pause was not operative (13 operator pacman runs, boot-chain-capture.txt:76–96); only the agent-side pause holds; `--needed` warning vindicated; hook-risk clause now observed (boot-chain-r17.md "Image facts") → r17, not closed.
- `:57` "all pacman transactions are paused" — now post-upgrade containment; still true.
- `:60` **live** — (a)/(b)/(c) untouched; pre-reboot guard stands.

Unaffected: `:49`, `:58`, `:59`.

[unk] No `-Qu` in either r17 capture; core/extra/multilib mtimes remain 2026-10-17 22:37 (fresh-capture.txt:10–12), so "current vs today's mirrors" is unproven.

Axes: C2+C1; no C3 impact.
Scope: executed=none
