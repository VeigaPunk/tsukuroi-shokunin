# ReviewCensusExtract — C1 denominator check (round-19 BUILD wave)

Mechanism [obs] `.ufo/waves/round-19/l1-capture/extract-adjacency-r19.py:15-17,57-60`: inbound = committed-tip `git grep 'tsukuroi-shokunin/<path>:<N>'`; outbound = `../<lane>-shokunin/<path>:<N>` scanned in `PROVINCE.md` only. Counts 114/10 are exact **for that declared form**.

Outbound saturation [obs]: full `PROVINCE.md` read finds exactly 10 `../` pointers (lines 33, 46, 47, 48, 49, 50×2, 51×2, 52), all line-numbered; no line-numberless form exists there. `corpus/README.md`: no sibling pointers (self-title only, :1). `SKILL.md` carries 4 further sibling-file pointers the census excludes: :207 `kama-shokunin/SKILL.md` (no :N), :568 `tameshi-shokunin/tools/mutate-and-run.sh:16-21,60`, :707 `tameshi-shokunin/plans/round-5.plan.md` (no :N), :1504 `.../fleet-kill-rate-ledger.md:47` — tool/precedent pins, not ownership handoffs.

Miss classes (sibling working trees, read/grep only; counts are working-tree upper bounds vs committed tips [inf]):
1. **Line-numberless prefixed** — 175+ files (inflated by wave-JSON duplicates, e.g. kama round-16 `build/dispatch.json:833`). Examples: `game-dev-2d-shokunin/reports/round-103/r103-scout.md:196`; `kaidoku-shokunin/.ufo/waves/luna-round-6/K1.md:5`; `lore-shokunin/.ufo/waves/round-87/followup/K2-adjacency.md:37`. Almost all historical (`.ufo/waves`).
2. **`@rev`-qualified, structurally invisible** (`@` outside the path char class; census JSON has zero `@HEAD` hits [obs]): `kaidoku-shokunin/.ufo/waves/luna-round-2/K1-connector.md:8`, quoted at `S3-sentinel.md:9`. ~2 files.
3. **Bare lane-name citations without repo prefix** — 54 files [obs]. Examples: `kaidoku-shokunin/.ufo/waves/round-18/w2/SiblingOverlap2.md:166,167,169`; `luna-round-9/GB3.md:10` (with a recorded line-slip); `tabi-shokunin/.ufo/waves/round-17/w1/AdjSweep2.md:121-123`; `mado-shokunin/.ufo/waves/round-13/w1/SiblingOverlap.md:69-70`. Sharpest operative (non-.ufo) miss: `mori-shokunin/SCORECARD.md:614`.
4. **Markdown links to tsukuroi**: zero fleet-wide [obs]. **§/heading-style**: none inside sibling repos; only fleet-root `.ufo` files use it (out of census scope), e.g. `.ufo/l0-questions.md:63`.

Verdict: the claim must **narrow its wording** — "line-numbered, repo-prefixed pointers in committed sibling tips" — not widen. Widening would pull in hundreds of historical/duplicated prose citations that the inbound draft schema (`found_line`/`target_ranges`) cannot classify. Absolute `/home/...` paths WITH `:N` are already captured (census JSON :277, :463, :676) — not a miss axis. No installs performed.

Scope: executed=none
