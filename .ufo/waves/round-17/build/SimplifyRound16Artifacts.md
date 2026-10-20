# SimplifyRound16Artifacts — advisory

[obs] frozen-cases.json left byte-unchanged; no rebuild.

## Contradictions (frozen-cases.json → tools/check-section-citations.py)
1. `.gate.count_semantics` (:12) makes "opener/heading/md-scope" shared blockers (count 0); gate `SHARED` (:334-336) has no `R16-MD-*`, so counts stay 2. Own vectors: `.cases[id=errata-md-missing].expected_corrections`=2 (:65), `md-openers-missing`=2 (:333), `md-headings-missing`=2 (:342). Prose also omits shared `R16-JSON-MISSING`.
2. `.gate.revision_input` (:9) names a never-existent worktree mode, predating round-17 binding: gate is hex-only (`REV` :61), `--branch` ancestry (`bind_revision` :453-472, parser :493-496), E-REVISION-NOT-LANDED/NOT-PUSHED/E-BRANCH-INVALID. `"worktree"` is only a label (:913, :917).
3. `.gate.files.sources` (:20) calls `R16-SOURCE-ROW` "optional"; gate shares it (:336); `source-row-missing` count 0 (:350).
4. `.gate.selftest` (:10) says in-memory only; selftest also runs a mktemp git sandbox (:25-26, :653).

## Minimal marker (mark, don't rebuild)
Untracked `.ufo/waves/round-16/build/frozen-cases.SUPERSEDED.md` needs only: add "`.gate.files.sources` calls `R16-SOURCE-ROW` optional; gate SHARED blocks it"; retarget stale `:750,753` to `:913,:917`; replace absent `corpus/lessons/round-17.md` with `.ufo/waves/round-17/build/drafts/lesson-r17.md`; scope "43 cases" to db19cc9 (current static total 38+8+9=55, [inf]).

[unk] No gate/selftest/host probe run; reads only. Lines shift under concurrent C3 edits.

Scope: executed=ls, wc, grep, sed, git log, git status, python3(json), head, tail
