# S170 Gate draft

| Source | URL | Opened | Located quote (at most 25 words) | Location | Decision |
|---|---|---|---|---|---|
| S170 | https://btrfs.readthedocs.io/en/latest/Trim.html; https://btrfs.readthedocs.io/en/latest/Defragmentation.html | 2026-10-22 | “The trim operation issued by user provides hints about what data are” | `.ufo/waves/round-31/w1/ScribeSrcRejectRtd/Trim.html` line 147, sha256 `07d83d2e5af70e4f270a8784f588406a72c36c224f1479946089c74ab941d2e1` | **reject**: both rendered bodies match the substantive Trim/discard and Defragmentation content in the pinned btrfs-progs v7.1 files; only rendering and typographic differences were observed. The page identifies only Read the Docs `latest`, not a release, so it adds no new guidance and cannot identify a pinned version. Flip only if a release-pinned page adds materially new operation-specific guidance absent from v7.1 and is anchored to saved bytes |

## Comparison notes

[obs] `Trim.html` lines 141-179 render the content of the saved v7.1 `Trim.rst` lines 1-43; the visible prose is the same, with RST roles/links rendered as HTML and typographic apostrophes (for example, `there's` at source line 6 becomes `there’s` in rendered line 145). `Defragmentation.html` lines 141-170 render the content of the saved v7.1 `Defragmentation.rst` lines 1-31; the warning and command reference are present with the same substantive wording. Neither rendered page adds operation guidance absent from its v7.1 file. The captured pages' metadata at line 28 names the version slug `latest`; no release identifier or source revision is shown.
