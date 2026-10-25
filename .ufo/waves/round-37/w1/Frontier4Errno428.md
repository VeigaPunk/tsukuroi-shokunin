# Frontier4Errno428 — errno theme overlap scan

## Axes
- **Adjacency:** keep this diagnosis within Tsukuroi's host/rollback-net boundary; refer binary internals elsewhere.
- **Frontier:errno:** distinguish permission denial from other filesystem/create failure classes without overstating the historical event.

## Scope and evidence
Bounded sweep: current `PROVINCE.md` core/frontier and adjacency clauses; full corpus coverage-map index; errno-oriented note `corpus/knowledge/snapper-eacces-mechanism.md`; SOURCES.md errno rows S027–S035 and nearby correction S038; staged ids/collisions list. The staged-ids file lists S200–S346; collision list is empty. No staged payload/source files were present in the assimilation directory listing, so I could not independently resolve the three proposed entries from their text or open their referenced sources.

The theme is in-scope at the host-state level: PROVINCE.md lines 8–14 owns read-only host/systemd and recovery diagnosis; lines 25–28 refuses binary RE, which this scan does not enter. The corpus already has substantial errno discrimination, so a broad claim of novelty would duplicate existing material: `snapper-eacces-mechanism.md` lines 9–14 gives measured `/` DAC state, bounded service capability, recurring errno 13, and explicitly labels the cause inference; lines 17–30 distinguishes the pre-existing-subvolume hypothesis and gives a falsifier. SOURCES S035 explicitly covers mkdir errno categories EACCES, EROFS, EEXIST, EPERM and ENOSPC; S034/S038 bound access(2) as a permission proxy. The corpus index already points to this mechanism at README.md lines 20 and 40–41.

## Precise scope issue
**Reject any staged entry that presents ordinary `mkdir(2)` errno mapping as proof of the historical Btrfs subvolume-create errno:13.** Existing `root-dac-correction-r13.json` lines 24–26 explicitly say its alternatives are illustrative, not historical causes, and that the B2/EROFS mapping is API-scoped, not proof of Btrfs ioctl behavior or historical event. A new entry can be admitted only if it adds a genuinely distinct discriminator and keeps this API boundary explicit; otherwise it is duplicate of S035 / existing errno note. This is a bounded conclusion, not an assertion that all three unseen entries are bad.

## Source access
No newly opened external source is cited. Attempted opening `https://man.archlinux.org/man/mkdir.2` on 2026-10-25; fetch failed with ECONNRESET, so I do not claim fresh source access or quote it. Local observed sources: `PROVINCE.md`, `corpus/README.md`, `corpus/knowledge/snapper-eacces-mechanism.md`, `corpus/knowledge/root-dac-correction-r13.json`, and `SOURCES.md`, all opened 2026-10-25. No tools installed or updated.

## Confidence
High that errno discrimination is an existing, in-scope area and that historical Btrfs causality must remain bounded; low on admit/reject decisions for the three staged entries because their payloads were not available in the bounded staging listing.