No untracked file at the fleet root has content that names tsukuroi, round 34, or a w1, w2, or res seat of round 34 (0 matches of 18 porcelain-untracked files).

1. [obs] `git -C /home/vgpnk/Projects/shokunin status --porcelain` listed 12 tracked modifications (`M .ufo/state/*.report-baseline` for twelve lanes, including `tsukuroi.report-baseline`, and `M .ufo/watchdog.log`) and 18 untracked paths. A second run with `--porcelain -uall` in the same seat printed the same 18 files; the first run only collapsed two of them to `?? .ufo/waves/round-33/` and `?? .ufo/waves/round-58/`. `git ls-files -o --exclude-standard` also counted 18. Modifications are tracked, so they are outside this sweep.

2. [obs] Seat names were taken from the `items[].name` fields of `/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w1-spec.json` (39), `res-spec.json` (6), and `w2-spec.json` (43): 88 distinct names. Each untracked file was read in full as bytes. A hit required `tsukuroi` (any case), `round` plus optional space, hyphen, or underscore plus `34`, the glued form `round34`, or an exact seat-name substring. Result: 0 hits. Confidence: high for this snapshot.

3. [obs] Examined untracked files. None has a tying line. Sizes and sha256:

- `/home/vgpnk/Projects/shokunin/.omp/mcp.json` size 285 sha256 3439a008a7e682813f88ac8ff5e0390813fec8c9a4cf9106f11ee382ee396a74
- `/home/vgpnk/Projects/shokunin/.ufo/state/kotoba.report-baseline` size 68 sha256 3c2b33f172fa1d78bd239fe0ad421e00b840405f3069215b350ada2482a773fb
- `/home/vgpnk/Projects/shokunin/.ufo/state/kotodama.report-baseline` size 68 sha256 fcab0fc4b052e1807644176b2962d0bc405c06e7fc9f48b925e388cf0848571e
- `/home/vgpnk/Projects/shokunin/.ufo/state/revenger.report-baseline` size 68 sha256 c616a0fa7ffb433ce13f952b5872067d5c7f0f229d29ec295ffb6a6acaa9c2db
- `/home/vgpnk/Projects/shokunin/.ufo/waves/round-33/w1/SentinelParser33.md` size 6557 sha256 d0b2b8f3fe005db684f7364c2c5991f73ee9818beb9ab2e25f34da16a18f90e4
- `/home/vgpnk/Projects/shokunin/.ufo/waves/round-58/falsify/ReviewBudgetMove.md` size 10299 sha256 c288bbd8427b38cda487b6693fe3a3774a674d9dcff944dd7f27fa7d9295cb8d
- `/home/vgpnk/Projects/shokunin/AGENTS.md` size 5921 sha256 382f28ab4e2846a94e176f67b5ea93d6c6a347997778a10ddc4c78772886eb86
- `/home/vgpnk/Projects/shokunin/bm.json` size 5563 sha256 0c3a365ad3530f02b88c8b453f901cc2178b05d8a97aa00d6f7066cdf09c7816
- `/home/vgpnk/Projects/shokunin/live_s228.html` size 5196 sha256 918d496cf0c3e6afda37d8badf7ad046dd9a08eba3767071cb5caebdf9e0a7de
- `/home/vgpnk/Projects/shokunin/nama.html` size 68855 sha256 bee96464d0fe77f7e7abb84b2ad905954e45bf8a133a80bb5626f418a047a06b
- `/home/vgpnk/Projects/shokunin/s395.txt` size 0 sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/__pycache__/append-closure.cpython-314.pyc` size 10738 sha256 3700bf9a7137c40b7e13010ce982fbed99deed7574b8e0ef8357dfcfcc404579
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/__pycache__/wave-live.cpython-314.pyc` size 10708 sha256 a0b914e3bb3a8679ff5249fcfebaf6492714b3b2b7dc67cbe605595c627e79db
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/append-closure.py.bak-20261023T040735Z` size 5757 sha256 0df3f2d8eb6714eac30074e415c20e169783d2f4ce0d99b6e25f660a4692624b
- `/home/vgpnk/Projects/shokunin/scripts/hyaku/fleet-commit.sh.bak-20261023T040735Z` size 2857 sha256 df65e2f49a896ab655770ea1b84e4ce541b5b5ed8953b73d0458968da35f21fb
- `/home/vgpnk/Projects/shokunin/tf_bavelas.html` size 5583 sha256 9f07c0d0e4afa6eaf3aaf6531b3dc355bf364319b5d6edf6dcfe61fdcd3011c3
- `/home/vgpnk/Projects/shokunin/wb2.html` size 620 sha256 e859c18f0c0cc71ffed35c4e7ebc87cbb4f136116156f2de1588aeb71449533e
- `/home/vgpnk/Projects/shokunin/write` size 25 sha256 95443b228053f4522714b3ba9cdb56cbce2e2c43b43b073b56e2c70978e0bac0

4. [obs] Near miss, not a match: `/home/vgpnk/Projects/shokunin/write` line 1 is `agent://U100N079H334f935b` (no trailing newline). The digits `34` sit inside that id. The file does not contain the phrase round 34, `tsukuroi`, or a seat name.

5. [obs] Porcelain does not list four top-level directories because they contain no untracked file that survives excludes. `/home/vgpnk/Projects/shokunin/dir` and `/home/vgpnk/Projects/shokunin/scratch` are empty. `/home/vgpnk/Projects/shokunin/local/fleet-analysis` is empty. `/home/vgpnk/Projects/shokunin/bash: ` holds one file, 8 directories deep, at `bash: /home/vgpnk/Projects/shokunin/souji-shokunin/tests/tools/souji-verify.sh: No such file or directory` (size 10139, sha256 3a127f03b9afbfef76d8cfb4274e0cb16aa7d59b915ce19e70a236321e9b3c33, 39 lines, first byte `{`). `git check-ignore -v` attributes that file to `/home/vgpnk/Projects/shokunin/.gitignore:1` pattern `*-shokunin/` (exit 0). Its bytes also fail the same content test, so it is not a round-34 content match. Nothing was moved or deleted.

6. [obs] `/home/vgpnk/Projects/shokunin/.ufo/waves/` has no `round-34` directory. The only untracked round directories there are `round-33` and `round-58`, and their single files are in the list above.

7. [unk] Anything written after the second porcelain run is not in this snapshot. Trees matched by `*-shokunin/` were not walked except the one file in finding 5; a misroot inside a lane checkout would not appear as `??` at the fleet root.

Scope: read=fleet porcelain untracked set, three round-34 specs' seat names, fleet .gitignore, fleet .ufo/waves directory names, the one ignored file under `bash: `; wrote=/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-34/w2/ScoutMisroot.md; executed=git status --porcelain, git status --porcelain -uall, git ls-files -o --exclude-standard, git check-ignore -v, python content scans
Model: xai-oauth/grok-4.7-build-fast
Installs: none
