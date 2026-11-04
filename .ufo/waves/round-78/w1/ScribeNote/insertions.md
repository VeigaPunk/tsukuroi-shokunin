# Proposed insertions — drafts only

## SKILL.md

Suggested location: beside the existing round-77 finite journald arithmetic guidance at SKILL.md:6099 onward. Do not replace its arithmetic distinctions.

For path-level journald accounting, read `corpus/knowledge/journald-path-usage-r78.md` and its JSON companion. U1/U2 separate allocated `st_blocks * 512` bytes from apparent size; U3 isolates suffix selection; U4/U5 isolate no-follow and regular-file checks; U6 isolates a failed-stat skip. The upstream v262 scan examines direct entries only, and its separate filesystem-availability result is not the allocated-byte sum. Accepted suffixes do not validate journal contents. These six hypothetical descriptors establish neither installed Arch behavior nor equality with `journalctl --disk-usage`; record package provenance, scope and observation time separately. Detection/report only: no vacuum, rotation, flush, restart or configuration changes.

## README insertion text

No top-level README-named file was found in the lane by the author; L1 chooses the canonical README destination. Proposed prose, not a claim that a missing file was edited:

- Journald path accounting: [`corpus/knowledge/journald-path-usage-r78.md`](corpus/knowledge/journald-path-usage-r78.md) and its JSON companion document six pinned hypothetical upstream-v262 cases, distinguishing allocated blocks from apparent size/free space, suffix filtering from validity, failed-stat skips, symlink no-follow and a nonrecursive scan. They do not establish installed Arch equivalence or identical `journalctl --disk-usage` output. The finite C1 gate also requires a digest-bound independent reviewer result.
