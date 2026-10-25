
source: S202 — https://man7.org/linux/man-pages/man3/errno.3.html — `DESCRIPTION`, significance paragraph, man-pages 6.19 (opened 2026-10-25)
source: S203 — https://man7.org/linux/man-pages/man3/errno.3.html — `DESCRIPTION`, error-number portability paragraph, man-pages 6.19 (opened 2026-10-25)
source: S204 — https://man7.org/linux/man-pages/man3/errno.3.html — `EXAMPLES`, `errno -s permission`, man-pages 6.19 (opened 2026-10-25)
source: S205 — https://raw.githubusercontent.com/torvalds/linux/v7.2/include/uapi/asm-generic/errno-base.h — `EACCES` definition, Linux kernel tag v7.2 (opened 2026-10-25)
source: S206 — `shokuknow/lanes/tsukuroi/round9/host-errno-capture.txt` — lines 1-10, capture dated 2026-10-24 (opened 2026-10-25)
source: S207 — `shokuknow/lanes/tsukuroi/round9/lane-errno13-probe.txt` — lines 1-8, capture dated 2026-10-24 (opened 2026-10-25)
verified-at: 2026-10-25
recheck: on-release — re-read errno(3), compare its footer and the host's retained journal window; do not infer a repair from an empty retained window

ground: the existing errno:13 classification question in `corpus/knowledge/snapper-eacces-mechanism.md` and the update-surface frontier's interpretation of a logged errno number

# The errno contract: significance, portability and the host's expired observation

## What an errno value says

The man-pages `errno(3)` contract is conditional: errno is significant only when the call's return value indicated an error; a successful call may change errno. The value is thread-local. Therefore, a number recorded in a log is not by itself evidence that a call failed, and a value from one thread cannot be assigned to another thread's operation without source evidence.

## Why a bare number is not portable

The numeric value corresponding to an errno name varies across UNIX systems and even across Linux architectures. The errno page omits numeric values from its list of names. Its worked `errno -s permission` example prints `EACCES 13 Permission denied`; this is an example of one system's lookup, not a portable mapping. The Linux v7.2 generic errno header assigns `EACCES` 13, and the opened Arch Linux x86_64 host capture shows the same mapping for that host. The scope is only the named host and kernel ABI snapshot; read another system's own mapping before asserting it there.

## The lane's recorded observation has aged out

The opened lane capture records zero `errno:13` journal matches in its 2026-10-24 recheck, zero matches since 2026-10-01, and six retained boots; it separately records the then-observed `/` mode and unit capability fields. An empty retained search is not evidence that the mechanism was repaired: it says only that the old log evidence is no longer present in the measured window. A new operation failure under an authorized, observed call is still required to classify an actual cause.

## Boundaries

- The upstream contract is about the C library's errno variable, not a claim about any particular program.
- The kernel header is an ABI source; the host capture is the host-specific mapping. Neither proves which call produced an historical journal number.
- The archived 2026-10-24 zero-result probe is not a current host recheck and does not close the operator-owned mechanism question.
- No privileged operation, host configuration change, package action, or repair is authorized by this entry.
- This deepens existing errno frontier ground; it does not claim new coverage or a completed repair.

## QUALITY check

- QUALITY 1-3: pass — the upstream contract, host-local mapping and aged-out observation are separated; the conclusion is falsifiable and bounded to the cited captures.
- QUALITY 7: pass — each upstream or own-work proposition cites its exact mined S202-S207 row and located anchor.
- QUALITY 8: pass — the negative log claim states the bounded query window and capture date; it is not generalized to current host state.
- QUALITY 14: pass — each source and capture cited here was opened this round and the quoted proposition is checked against the located bytes.
- Coverage-map check: pass for deeper treatment of existing errno ground; no new coverage is claimed.
