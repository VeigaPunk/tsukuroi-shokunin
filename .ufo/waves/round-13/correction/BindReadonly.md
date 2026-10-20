# BindReadOnlyPaths Analysis — Refutation of False Exclusivity

## Axes
- **depth**: Semantic precision of unit filesystem namespace mechanisms under `systemd.exec(5)` vs. over-broad exclusivity.
- **calibration**: Strict separation between documented upstream capability and observed host unit configuration.
- **operability**: Verified read-only inspection commands (`systemctl show`) without host mutation.
- **coverage**: Explicit inclusion of `BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=`, and `RootImage=`.
- **freshness**: Re-opened against `systemd.exec(5)` (systemd 262.1).
- **adjacency**: Leaf seat write strictly bounded to `.ufo/waves/round-13/correction/BindReadonly.md`.

## Source Grounding
- **Source**: `systemd.exec(5)` (S028, and S041 scope), § `BindPaths=, BindReadOnlyPaths=` (added in systemd 233).
- **Upstream specification**:
  - `BindReadOnlyPaths=` configures unit-specific read-only bind mounts: "BindReadOnlyPaths= creates read-only bind mounts."
  - Mount namespace isolation: "Any bind mounts created with this option are specific to the unit, and are not visible in the host's mount table."
  - Implicit namespace allocation: "Using this option implies that a mount namespace is allocated for the unit, i.e. it implies the effect of PrivateMounts=."
  - Definition syntax: Takes a whitespace-separated list of `source:destination:options` triples. If destination is omitted, destination equals source.
  - Target root remapping: "This option is particularly useful when RootDirectory=/RootImage= is used. In this case, the source path refers to a path on the host file system, while the destination path refers to a path below the root directory of the unit."

## Refutation of the Round-12 False Universal
- **Round-12 universal claim**: `root-dac-decision-r12.md` (§ "Current host evidence" line 53, R13 line 86) and JSON B2 `limit` asserted that *only* `ProtectSystem=strict` or `ReadOnlyPaths=` covering `/` could make `/` read-only through the unit.
- **Mechanism of refutation**:
  1. `BindReadOnlyPaths=` is an independent, first-class directive in `systemd.exec(5)` that creates read-only bind mounts in the unit's private filesystem namespace.
  2. A unit specifying `BindReadOnlyPaths=/` (or `BindReadOnlyPaths=<source>:/`, or combining with `RootDirectory=` / `RootImage=`) mounts `/` as a read-only bind mount inside its mount namespace, even when `ProtectSystem=no` and `ReadOnlyPaths=` is completely empty.
  3. Any write attempt to a filesystem mounted read-only via `BindReadOnlyPaths=` is rejected by the VFS with `EROFS` (S035), matching the denial behavior of `ProtectSystem=strict` and `ReadOnlyPaths=`.
  4. Furthermore, `TemporaryFileSystem=/:ro` can independently mount a read-only tmpfs over `/`.
  5. Consequently, asserting that *only* `ProtectSystem=strict` or `ReadOnlyPaths=` can make `/` read-only through a unit is logically and technically false.
  6. The valid, source-grounded exclusivity is strictly internal to `ProtectSystem=`: among `ProtectSystem=` options, `full` covers `/usr`, `/boot`, `/efi`, and `/etc` (not `/`), whereas `strict` covers the whole hierarchy (excluding API VFS subtrees `/dev`, `/proc`, `/sys`). It does not preclude independent directives like `BindReadOnlyPaths=`.

## Host Observation vs. Upstream Capability (No Host Configuration Claim)
- **Observed host state [obs]**:
  - Command: `systemctl show -p ProtectSystem -p ReadOnlyPaths -p BindReadOnlyPaths -p TemporaryFileSystem -p RootDirectory -p RootImage limine-snapper-sync.service` (exit 0).
  - Output:
    - `ProtectSystem=no`
    - `ReadOnlyPaths=`
    - `BindReadOnlyPaths=`
    - `TemporaryFileSystem=`
    - `RootDirectory=`
    - `RootImage=`
  - All four alternate path/mount directives (`BindReadOnlyPaths=`, `TemporaryFileSystem=`, `RootDirectory=`, `RootImage=`) are completely empty/unset in the unit configuration.
- **Separation of fact and refutation [inf]**:
  - The refutation does **not** claim that `BindReadOnlyPaths=` was configured on this host.
  - The refutation does **not** attribute the logged `errno:13` (EACCES) failure to `BindReadOnlyPaths=`.
  - Instead, the refutation operates strictly on the analytical boundary: discriminator B2 cannot claim theoretical exclusivity for `ProtectSystem=strict` or `ReadOnlyPaths=` when `BindReadOnlyPaths=` provides an alternate path to a unit-private read-only root view.
  - On this specific host, neither the primary (`ProtectSystem=strict` / `ReadOnlyPaths=`) nor the alternative (`BindReadOnlyPaths=` / `TemporaryFileSystem=/:ro`) unit read-only mechanisms were configured.

## Confidence and Residual Unknowns
- **Confidence**: High (1.0). Upstream man-page text and live `systemctl show` output are unambiguous and verified.
- **Residual unknowns**: Whether dynamic or transient unit drop-ins were active during historical boot sessions; ruled unobserved, while current static unit configuration confirms all read-only path mechanisms remain unset.
