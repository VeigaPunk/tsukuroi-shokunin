# RevSourceS162 — re-open review of corpus/SOURCES.md row S162 at 29bf87fa3971df04cb96e4ad9a28805d8154ed2f

Verdict: partly holds — every content claim (live digest, snapshot, gate quote, cited lines, tier/kind/scope/teaches) verifies; the `used-by` cell fails at the attacked revision because it names `corpus/lessons/round-30.md`, which does not exist in that tree.

## Checks that pass

1. Row shape [obs]: `git show 29bf87f:corpus/SOURCES.md | grep S162` gives NF=13 (11 cells), status `mined`, opened `2026-10-22` (ISO date, today), recheck `on-release` (valid cadence), kind `docs`, tier `A` — all within the CORPUS.md contract v1 enums (/home/vgpnk/Projects/shokunin/CORPUS.md lines 86–108).

2. Live bytes [obs]: `curl -sL https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/config/core.adoc` on 2026-10-22 → HTTP 200, sha256 `aa6015220b25a284408fa5e03bba40b70fcc69fe1a03a60859e019a84a2c9f5d`, 36651 bytes, 798 lines — identical to the anchor cell's claim and to the committed snapshot `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w1/ScribeSrcGitCore/S162-core.adoc` (same sha256, same size). Fetched copy saved at `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS162/S162-core.adoc` (sha256 `aa6015220b25a284408fa5e03bba40b70fcc69fe1a03a60859e019a84a2c9f5d`).

3. Gate quote [obs]: the only `S162-gate.md` is `.ufo/waves/round-30/w1/ScribeSrcGitCore/S162-gate.md`; its drafted quote "Defaults to `$XDG_CONFIG_HOME/git/ignore`" (4 words, ≤25) is verbatim on line 492: `sed -n '492p' <fetched> | grep -cF 'Defaults to `$XDG_CONFIG_HOME/git/ignore`'` → 1.

4. Anchor line ranges [obs]: excludesFile block 488–494 (default line 492, `$HOME/.config/git/ignore` fallback 493–494) ✓; attributesFile block 505–510, the default-value sentence spans 508–510 so "default at 509-510" is right at the edge but on the correct line ✓; hooksPath block 512–532, default `$GIT_DIR/hooks` at 513–514, `/dev/null` disable form at 529–532 ✓.

5. Tier/kind/scope accuracy [obs/inf]: installed `git --version` is 2.56.0, matching the cited tag — upstream primary documentation at the pinned tag is a correct tier-A `docs` assignment. `teaches` is accurate: per-user ignore/attributes defaults take effect without any configuration naming them, and `/dev/null` disables hooks — all directly confirmed in the cited lines. Corroborating snapshots also verify: gitignore.adoc line 10 and 59–60, gitattributes.adoc 93–94 (sha256 `33822157…` and `4ca89456…`).

6. Gate record [obs]: the gate note is also embedded in `corpus/lessons/round-30.md` line 21 at HEAD with URL, access date 2026-10-22, quote and location — satisfying contract rule 1.

## Finding

F1 (medium, contract): **used-by names a file absent from the attacked revision.** Row S162 at 29bf87f (line 168) has `used-by` = `corpus/QUALITY.md, corpus/lessons/round-30.md`. `corpus/QUALITY.md` does cite S162 at 29bf87f (line 149, criterion 78). But `git cat-file -e 29bf87f:corpus/lessons/round-30.md` fails — the file was added only by the merge commit 7165f11, whose sole parent is 29bf87f (i.e., strictly after the revision under attack). Running the contract census check "mined rows whose used-by paths do not exist" at 29bf87f prints `missing: corpus/lessons/round-30.md`. Cause [obs]: the row was drafted at a3f1937 (before the tip) with a forward reference to the lesson draft, which landed in the very next commit; at HEAD both used-by paths exist and cite S162 (round-30.md lines 3 and 24 explain the used-by was set to "the files that cite them"). So the defect is confined to the 29bf87f tree and is self-healed by 7165f11 — it does not indicate a fabricated citation, only an ordering artifact. [inf] Severity is limited: status `mined` is still satisfied by QUALITY.md alone.

## Residual risk / gaps

- Quote ≤25 words verified at 4 words. [obs]
- Only one gate file found for S162; no competing draft. [obs]
- raw.githubusercontent.com answered 200 on first try; no kernel.org fallback needed. [obs]
- [unk] Whether the S162 row existed identically at a3f1937 vs 29bf87f was not diffed cell-by-cell beyond the SOURCES.md worktree==tip equality shown by `git diff 29bf87f -- corpus/SOURCES.md` printing nothing for the file.

Scope: read=corpus/SOURCES.md (row S162 at 29bf87f), /home/vgpnk/Projects/shokunin/CORPUS.md §SOURCES.md, .ufo/waves/round-30/w1/ScribeSrcGitCore/*, corpus/QUALITY.md and corpus/lessons/round-30.md at tip/HEAD, live core.adoc v2.56.0; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS162.md, /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-30/w2/RevSourceS162/S162-core.adoc; executed=curl, sha256sum, wc, sed, grep, git show/log/cat-file/merge-base/status/rev-list (read-only)
Model: not exposed
Installs: none
