# FxFresh07 — FAILS (C3 evidence precision)

Paths: H=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/knowledge/host-health-report-r3.md`; C=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-18/l1-capture/host-capture-r18.txt`; L=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/corpus/lessons/round-18.md`; B=`/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-17/l1-capture/boot-chain-capture.txt`.

**P2 — unsupported scope/completion**
- `R18-FRESH-NoticeHealth-03` (H:628): “R18 ran no pacman -Qu, so neither 413 nor zero is current.” L:57 says S060 is one wrapper capture, not exhaustive shell tracing; C:42 is mtime, not a pending query. Say no result appears in S060 and neither value is verified; do not assert either value false.
- `R18-FRESH-NoticeHealth-05` (H:630): C:72-73 logs `[PACMAN] Running` invocations, not completed `-U` transactions. L:71 explicitly says invocation is not completion. Say invocation entries only; withdraw the inference that the banner’s transaction set is not current.
- `R18-FRESH-SUPPLEMENT-09` (H:646): “checkupdates itself was not invoked or located in R18” overstates S060’s scope; C:82-86 does not query it. Narrow to “not shown in S060; availability/use elsewhere unknown.” Add C:36 for pacman-contrib; C:83 proves only paccache resolves.

**P3 — incomplete capture anchor**
`R18-FRESH-NoticeHealth-02`: `now` says home and root, but registry anchor C:76 (“home”) omits root at C:77. Cite C:76-77/both lines and fix H:627 citation.

**SURVIVES (bounded claims)**
`NoticeHealth-01`, `NoticeHealth-04`, `NoticeHealth-06`, `SUPPLEMENT-05..08`, `SUPPLEMENT-10`. U1/J4 neighbors at H:35,52-53,283-290 are covered; configuration is not treated as rollback, and historical bytes stay dated (H:622,636). For `NoticeHealth-04`, cite C:27-38 to support reason “only”; for `SUPPLEMENT-10`, cite complete `dkms status` C:92-96 to prove no 7.1.4 row. B:59 proves an `-Syu` invocation only, not completion.

**UNPROVEN:** snapshot inventory/restoration, limine active state, pending count, checkupdates availability, later `-U` outcomes and libinput. No mtime→refresh or enabled→active-count inference (H:626-28,656-59). LSP unavailable (`xd://lsp`: no mounted tool); text review only.

Scope: executed=none