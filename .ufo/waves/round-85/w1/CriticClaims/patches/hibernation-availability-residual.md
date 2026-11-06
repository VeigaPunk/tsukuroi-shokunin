# Proposed C1 residual corrections — hibernation-availability-r85 (seat CriticClaims)

Audited version: `corpus/knowledge/hibernation-availability-r85.md` sha256
`fc67c150345420ffce58e7c4e8e1f701b9c38bdd7bc2108ad2d5e366b7c86a67`, `.json`
`7a5db591b41282c610ae3a2626ee76c2aa9fc6ca2dcac760c1e49a1419817e0e` (both 17:12:52).
All HA1–HA9 rows are accurate at their cited raw lines; HA8 already carries the measured host values.
These five items are calibration, not correctness. Nothing here was applied.

## C1-1 — pin the `__setup` matching code the Limits paragraph rests on (low, sourcing)

`hibernation-availability-r85.md:50-57` says the kernel's `__setup` matching is a byte-prefix match and
correctly adds "The prefix behaviour rests on `init/main.c` `obsolete_checksetup`, which is not in the
pinned set." The claim is true (verified at v7.2: `obsolete_checksetup` → `parameqn(line, p->str, n)`;
`parameqn` compares n bytes with `-`→`_`), and the gate side reproduces: `noresume=1`, `nohibernate=1`,
`noresumefoo` each return `{"findings": [], "verdict": "HEALTHY"}` rc 0 (ReviewGate T9–T11).

Correction: pin `init/main.c` and `kernel/params.c` at tag v7.2 next to S343–S345 (the wave already fetched
unpinned referents into `.ufo/waves/round-85/w1/ScribeEntry/receipts/FETCHES.txt`) and cite them; then the
disclosure clause can name the pinned file instead of saying "not in the pinned set".

## C1-2 — HA5 / `HR-NORESUME-ARG`: the image is still resumable at runtime (low, completeness)

`hibernate-availability` HA5 (`:30`) and the `HR-NORESUME-ARG` action (`:41-42`) are correct for the boot
path. `hibernate.c:1306-1307` (`resume_store`) additionally sets `noresume = 0` and calls
`software_resume()` after a successful write, so the image can still be read from userspace.

Proposed clause after "the next boot discards the image":

> The image is still readable at runtime: `echo <maj:min> > /sys/power/resume` clears `noresume` and
> calls `software_resume()` (raw 1306-1307). Root, one-shot, and not a boot-time fix.

## C1-3 — HA8: the secretmem/CXL measurement is point-in-time (low, precision)

`hibernation-availability-r85.md:33` now carries `CONFIG_SECRETMEM=y`, 0 secretmem VMAs,
`CONFIG_CXL_MEM=m`, no CXL module/device/iomem range (receipts:
`ScribeEntry/receipts/host-recheck.txt`, `secretmem_vma_hits_root=0`). The ScribeEntry draft carried the
caveat that a later `memfd_secret()` changes the answer without changing any gate input; the landed table
does not. Add:

> point-in-time scan; a later `memfd_secret()` makes the predicate false without changing any gate input.

## C1-4 — quote form (informational)

`hibernation-availability-r85.md:23` promises "Quotes are verbatim at the cited raw lines". HA2, HA3 and
HA4 merge source lines (`{`, `}` and line breaks compressed); word order and tokens are exact, the slices
are not byte-exact. Either restore the draft's byte-exact slices (it has `gen_rows.py` and
`receipts/quote-check.txt`) or change the header to "code quotes elide line breaks; tokens are verbatim".

## C1-5 — HA7 novelty scope (informational)

`corpus/README.md:899` (ScoutHost r84 §3a) already records "lockdown `none`, no `noresume`/`nohibernate`".
HA7 is new to `corpus/knowledge` (the declaration's grep is scoped there and empty at `3ed94533`), not new
corpus-wide; do not claim it as new information in the closure.
