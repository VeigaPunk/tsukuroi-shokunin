# Round 13 — bounded data-walk: R12 unit read-only overclaim

**Axes:** depth (source scope and correction coverage); adjacency (preserve the R12 record while making the R13 correction authoritative). **Scope:** this is a read-only occurrence/provenance walk, not a correction implementation or verification run.

## Finding

The rejected R12 universal is not the valid comparison that `ProtectSystem=full` does not make `/` read-only. It is the attempted correction's *exhaustive* tail: “Only `strict` or a `ReadOnlyPaths=` entry covering `/`…” The R12 B2 discriminator itself already names `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=`, and `RootImage=` as other path-view changes, so the prose and structured branch disagree.

The outside gate states this defect directly: `corpus/lessons/round-12-verifier-spotcheck.md:140-161`, especially 143-160, identifies the same universal in the MD R13/current-host text and JSON B2 `limit`; it separately notes that the discriminator lists the broader alternatives. It rejects C2 as delivered despite the structural counter passing.

## Provenance chain

- The resumed R12 critique first objected to the opposite overreach: `.ufo/waves/round-12/resumed/C2ReviewR.md:46-51` says the original `ProtectSystem=full` signal was wrong for `/`; it recommends the narrower `full`-scope statement.
- The critique also listed omitted unit mechanisms (`.ufo/waves/round-12/resumed/MatrixCriticR.md:72-80`, X3). The matrix executor then recorded the corrected `full` scope but retained “Only `strict` or `ReadOnlyPaths=`” in its prose while reporting that its discriminator queried four additional settings (`.ufo/waves/round-12/resumed/MatrixR.md:63-65`). This is the most direct evidence for how the false universal survived: a valid `ProtectSystem=` correction was not propagated to the accompanying exhaustivity claim. The outside spot-check later isolated that inconsistency.
- This reconstructs the document-edit sequence from author-side reports; it does not establish the author’s unrecorded intent. **Confidence: high** that the universal and mismatch are present; **medium-high** on this edit-sequence explanation.

## Exact R12 sites to supersede

Three locations contain the same unit-read-only exhaustivity claim called out by the verifier:

1. `corpus/knowledge/root-dac-decision-r12.md:53` — current-host paragraph: `ProtectSystem=no` and empty `ReadOnlyPaths=` are followed by “only `strict` (or … `ReadOnlyPaths=`) would make `/` read-only through the unit.”
2. `corpus/knowledge/root-dac-decision-r12.md:86` — R13 rejection: the `ProtectSystem=full` rejection is correct, but its final “Only `strict` or … `ReadOnlyPaths=`” is not exhaustive.
3. `corpus/knowledge/root-dac-decision-r12.json:87` — B2 `limit`: after admitting other unit settings may change the view, it repeats “so only strict or a `ReadOnlyPaths=` entry can make `/` read-only through the unit.”

The same unsupported “B2 is not configured” negative is repeated separately at MD `:53` (for `/`), MD worked-example step 3 `:64` (for this host), and JSON B2 `interpretation` `:77` (for `/`). Round 12 only recorded `ProtectSystem=no`, empty `ReadOnlyPaths=`, and the host-global `/` mount as `rw`; it explicitly says `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=`, and `RootImage=` were not captured (`MD:53`; `JSON:87`). A host `findmnt` observation cannot rule out a unit-private mount namespace (`MD:64`; `JSON:87`). Thus the supported statement is “those captured signals were absent; other unit views were not assessed,” not “B2 is not configured.”

Also replace JSON `decision_procedure[1]` (the human-numbered step 2 at `:172`): its B2 collection list names `ProtectSystem`, `ReadOnlyPaths`, and `ReadWritePaths` but omits the alternate unit path-view settings. The discriminator already lists some alternatives at `JSON:79-85`, but its `TemporaryFileSystem=` signal needs an explicit read-only condition; any temporary filesystem overlay is not necessarily read-only.

## Source-grounded scope for the replacement

The reopened primary source is Arch `systemd.exec(5)`, https://man.archlinux.org/man/systemd.exec.5.en, sections `ProtectSystem=`, `BindPaths=/BindReadOnlyPaths=`, `ReadWritePaths=/ReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=`, `RootImage=`, and `RootImageOptions=`:

- `ProtectSystem=full` adds `/etc` to the read-only `/usr`, `/boot`, and `/efi` coverage; it does not cover `/`. `strict` covers the hierarchy subject to the documented exceptions.
- A covering `ReadOnlyPaths=` entry and `BindReadOnlyPaths=` provide unit-side read-only paths. `TemporaryFileSystem=` needs read-only mount options (the manual gives `TemporaryFileSystem=/var:ro` as an example).
- `RootDirectory=` and `RootImage=` change the service's root/path view; neither setting alone proves that the view is read-only. If discussing an image's read-only state, scope it to the applicable `RootImageOptions=` mount options (e.g. `ro`) rather than treating `RootImage=` alone as a read-only flag.

The source registry's current S028 row (`corpus/SOURCES.md:34`) is tier A for the same man page but its registered anchor is `CapabilityBoundingSet=`. The correction should cite the exact systemd.exec section anchors for these path claims and keep registry/source attribution aligned; do not imply that the capability-only anchor itself proves the B2 mechanisms.

## Append-only cutover recommendation

Preserve both R12 files and their source-seat/history evidence. Publish a new R13 MD/JSON correction as the single active procedure, explicitly superseding the three universal sites, the three “B2 is not configured” claims, and JSON decision-procedure step 2. In the correction, distinguish (a) the valid `ProtectSystem=` comparison, (b) the complete, source-backed set of unit-side read-only mechanisms, and (c) what was actually captured for this host versus the unobserved unit-private namespace. Make the JSON selector semantics match the MD exactly; retain R12's original text as historical data rather than editing it into apparent agreement.

A R13 supersession notice/pointer is now visible at the top/end of the R12 MD and JSON. At the time of this walk, the named `root-dac-correction-r13.md` and `.json` targets were not yet readable, so the pointer alone is not evidence that their corrected content has landed. Main/L1 should confirm those targets and run the assigned narrow red/green check after integration; this seat ran no checks.

## Method / limits

Read `AGENTS.md`, `corpus/QUALITY.md`, the R12 verifier spot-check, the R12 MD/JSON, `SOURCES.md`, the R12 resumed critique/executor reports, and the current systemd.exec manual. Literal text searches were used only to map occurrences. The `lsp` device is not mounted (`xd://lsp` returned “No such tool”); no semantic reference service was available for these Markdown/JSON files. No source, registry, lesson, or sibling report was edited; no tests/build/lint/formatter or runtime was invoked; no tool was installed or updated.
