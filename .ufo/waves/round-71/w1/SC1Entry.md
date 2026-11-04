# SC1Entry — C1 knowledge entry draft (round 71, wave w1)

Seat: L2 SC1Entry. Scope: draft the C1 note `corpus/knowledge/module-parameter-plane-r71.md`
in the frozen MP1-MP6 grammar and prove it against the frozen counter. Read-only against
the lane; writes only under `.ufo/waves/round-71/w1/` and scratch.

## Behavior

- Drafted six rule rows MP1-MP6 in the frozen one-line grammar (6 cells, no pipe inside a
  cell), one row per frozen theme:
  - MP1 perm==0 invisibility — `params.c` (`module_param_sysfs_setup` / `param_sysfs_builtin`
    skip `perm == 0`; `add_sysfs_param` carries `BUG_ON(!kp->perm)`).
  - MP2 mode == perm and store only with a write bit — `params.c` (`attr.mode = kp->perm`,
    store installed only when `S_IWUSR|S_IWGRP|S_IWOTH`, `-EPERM` when `set` absent).
  - MP3 `kernel_param_ops` set/get contract — `moduleparam.h` (`set` returns 0 or `-errno`,
    `get` returns length into a 4k buffer, optional `free`).
  - MP4 unknown parameter warned and ignored — `main.c` (`unknown_module_param_cb`: dynamic
    debug / `async_probe` special cases, else `pr_warn ... unknown parameter ... ignored`,
    returns 0 so the load proceeds).
  - MP5 `module_blacklist` refusing the load — `main.c` (`blacklisted()` walks the
    comma-separated list; `early_mod_check` returns `-EPERM` after `pr_err`).
  - MP6 two specification routes plus the sysfs reveal — `kernel-parameters.rst` (command line
    with module-name prefix, or modprobe; loaded modules reveal parameters under
    `/sys/module/${modulename}/parameters/`).
- Source allocation keeps snapshot reuse at the declared maximum: params.c x2 (S297),
  main.c x2 (S299), moduleparam.h x1 (S298), kernel-parameters.rst x1 (S300) — 4 distinct
  sources, 4 distinct snapshots, no snapshot cited more than twice.
- Added a host-applicability section: one line per row against `before/host.txt`
  (btrfs `read_policy` absent as the zero-perm case; nvidia_drm `modeset=Y` and peers at
  `-r--r--r--`; nvidia_uvm `-rw-r--r--` root-only with an empty unprivileged-writable list;
  `/proc/cmdline` carrying no `module.parameter` token; blacklist configured only through the
  three `/etc/modprobe.d` and four `/usr/lib/modprobe.d` paths recorded by path/mode; 136
  modules / 829 parameter files as the disclosure half).

## Gate / counter evidence

- Counter: `tools/count-mp-rows-r71.py` (sha256
  fa67d4deb5f01a5124120276a8571fa36c7367d9db711ceb39bc1ca6fded48bc), run in `--fixture`
  mode over a mirror holding `corpus/SOURCES.md` (S297-S300), the note, the four committed
  snapshots and `src/SOURCES.json`. Counter untouched; only my wording iterated.
- First and only fixture run: all six rows `MP_ROW ok`, `MP_ROWS=6 MP_VERIFIED=6
  MP_SOURCES=4 MP_SNAPSHOTS=4 MP_MALFORMED=0`, `met=1`, rc 0 (receipt `counter-run.txt`).
- The note placed at the Report path was copied back into the mirror and re-run byte-identical
  (same sha256 cdc4b7af71224ccc6c22b8b4e26c9547d257da7104aad35d902b091a9090281f before and
  after), so the published draft, not a scratch variant, is the file the counter accepted.
- Digest chain re-checked read-only: `sha256sum -c SHA256SUMS` rc 0 on all four snapshots, and
  each `SOURCES.json` map digest equals the file digest (4/4 match), matching the declared
  digests for kernel-parameters.rst / params.c / moduleparam.h / main.c.

## Touched surfaces

- `.ufo/waves/round-71/w1/SC1Entry/module-parameter-plane-r71.md` (draft; sha256
  cdc4b7af71224ccc6c22b8b4e26c9547d257da7104aad35d902b091a9090281f)
- `.ufo/waves/round-71/w1/SC1Entry/counter-run.txt` (sha256
  efb0d2c1a7e8d04e33a4cd21421d21396f83de9ea1d1f594d74ef8d55fc01c08)
- `.ufo/waves/round-71/w1/SC1Entry.md` (this report)
- Scratch `/fast/scratch/hyaku/tsukuroi-r71/SC1Entry` (mirror tree deleted before yield)

No edits to the lane tree, `corpus/`, `tools/`, `.ufo/state`, the fleet repo, siblings or
shokuknow; no git/jj mutation; no pacman; no tool install.

## Out of scope

- Registering S297-S300 in the real `corpus/SOURCES.md` and landing the note at
  `corpus/knowledge/module-parameter-plane-r71.md` — L1-only writes; the fixture registry rows
  are a mirror, not a landing.
- C2, C3, census, battery and any verdict term.
- Reading key material, host serials or WWIDs; none touched.

## Findings

- The frozen grammar admits the six themes without strain; the binding constraints are the
  grounding clause (>= 6 distinct non-stopword tokens of length >= 4 shared with the snapshot,
  shared/total >= 0.5) and the 25-word quote cap. Wording that leans on source vocabulary —
  identifier names and comment phrasing — clears both; ordinary English paraphrase does not
  (`parameter`, `kernel`, `module`, `sysfs`, `path`, `value` are stopwords and earn no credit).
- `perm`-zero is only indirectly observable on this host: the btrfs `read_policy` absence is
  consistent with the rule but cannot distinguish "perm==0" from "parameter not compiled in",
  so the row is cited to the snapshot and the host line stays an observation.
- MP2's host line depends on the capture's empty "writable parameter files among the four
  nvidia modules" list; the `-rw-r--r--` files are root-writable by mode, so the correct claim
  is "root-only", not "read-only".

KEY=VALUE: MP_ROWS=6 MET=1 SOURCES=4 SNAPSHOTS=4
