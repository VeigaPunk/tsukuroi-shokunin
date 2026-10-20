# ConnW04 — duplicate URLs, append-only

**Axes.** C1 depth (named corrections, ordinal 8). C2 operability (`tools/_revision.py` shared; `tools/check-revision-binding.py` does not import it). C3 freshness (registry-scoped notices, no ordinal uplift).

**Evidence.** [obs] `.ufo/waves/round-18/measure/census-start.txt:1-10`: eight W04s, then `ok`, exit 0 — S038 access.2; S041/S044/S046 systemd.exec.5; S042 #8047; S043 #6629; S049 pacman.8; S058 `…/raw/v42.2/init`. [obs] `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:644-649`: W04 is a new scope on a seen URL and does not honor `supersedes`; E04 does. [obs] `CORPUS.md:116-118` and `corpus/lessons/round-17.md:17`: append-only; merging the earlier seven was rejected.

**Active.** [obs] `corpus/SOURCES.md:60` S054 (mined) teaches host-init equality. `:64` S058 (mined) supersedes that and assigns the equality to S051. Both list `corpus/knowledge/boot-chain-r17.md` in `used-by`. The note cites S054 at `:1`, `:2`, `:165`, `:185` and never S058. `:40-42` already cites capture B:182, 251. [inf] That citation still teaches S054’s withdrawn host clause.

**Rest.** [obs] S038:44 limits S034:40 at `root-dac-decision-r12.md:121-123`. S044:50 and S046:52 supplement S041:47; the exclusive-`/` line is historical (`root-dac-decision-r12.md:6-11`, `:129-134`). S042:48 and S043:49 are rejected; #8047’s live row is S045 (`source-scope-correction-r14.md:17-18`). S049:55 supplements S048:54 (`partial-upgrade-recheck-r15.md:165-166`). S016 is `/raw/v42/init`, a different URL.

**Move.** Append one C1 notice on `boot-chain-r17.md`, apart from `.ufo/waves/round-18/build/drafts/NoticeBootCorrections.append.txt` (that draft keeps `:40-42` on S051 and adds B:198). State that the tagged-init citation is S058 and host equality stays S051. Keep S054’s `teaches` and all eight W04s. Leave the revision binder and its judge untouched.

**Risks.** Rewriting S054 breaks Rule 2. Hiding W04 on `supersedes` conceals scope reuse. Using S058 for the host-byte claim repeats the defect. Folding this into the `:40-42` draft mixes two fixes.

**Verification.** After the notice, census still prints these eight W04s and exit 0; the note names S058; `:40-42` still cites the capture. Gate not run here.

Scope: executed=none
