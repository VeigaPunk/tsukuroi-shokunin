# RevIndependentP1P2 — independent re-derivation of C2/P1 and C2/P2

Verdict: both premises reproduce exactly under my own commands — 3 pending upgrades from omarchy (2) and openai-chatgpt (1), and 0 installed packages newer than any sync repo — so the capture's P1 and P2 readings are confirmed independently.

Commands below were run by me this session; the analysis itself was a fresh sweep over `pacman -Q` and `pacman -Sl` with pacman's own `vercmp` binary, not the capture script. Host tools: pacman v7.1.0 / libalpm v16.0.1 [obs].

## Findings

1. P1 count: 3 pending upgrades [obs]. `pacman -Qu` (exit 0) returned exactly three lines: `1password-beta 8.12.42_34.BETA-1 -> 8.12.44_25.BETA-1`, `chatgpt-bin 26.1013.40934-1 -> 26.1016.51333-1`, `claude-code 2.1.304-1 -> 2.1.307-1`. This matches capture.txt:40-42 and the count 3 at /home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-24/capture/l1/capture.txt:47. The corpus figure of 413 belongs to the round-23 cohort and is not what the live host shows now.

2. P1 repos: omarchy 2, openai-chatgpt 1 [obs]. Cross-check with a different method than the capture used: `pacman -Sup --print-format '%r %n %v'` (exit 0) resolved the upgrade set to `omarchy 1password-beta 8.12.44_25.BETA-1`, `openai-chatgpt chatgpt-bin 26.1016.51333-1`, `omarchy claude-code 2.1.307-1`. The capture's probe (capture.txt:51-54) went via `pacman -Qqu` plus per-package `pacman -Si`; both methods agree on package set and repo attribution, all third-party, none from core/extra/multilib.

3. P2 count: 0 installed packages newer than sync [obs]. Method: I crossed all 1399 installed packages (`pacman -Q`, exit 0) against all five sync repos (`pacman -Sl`, exit 0: core, extra, multilib, omarchy, openai-chatgpt; 15756 rows over 15751 distinct names) and ran pacman's `vercmp` on every installed/sync version pair whose strings differ. Count with vercmp(installed, sync) > 0: 0 under the any-repo criterion and 0 under the stricter every-repo criterion. Only 3 of the 1378 sync-covered installed packages had any version difference at all, and all 3 point the other way (sync newer than installed — exactly the pending set). This matches the capture's empty `local-newer-than-sync` probe with exit 0 at capture.txt:57-59.

4. libinput sanity: installed `libinput 1.32.0-1` equals `extra/libinput 1.32.0-1` (vercmp 0) [obs], consistent with the claim wording "libinput 1.32.0 equals sync" and capture.txt:73 and capture.txt:88.

5. Coverage difference, counted and found harmless [inf]: the capture's probe at capture.txt:58 only sees packages whose `pacman -Sl` row carries an `[installed: ...]` marker, so installed packages absent from every sync repo are invisible to it. My sweep additionally covered the 21 installed packages with no sync entry (android-apktool-bin, the 13 elephant* modules, obsidian-cli-inspector, omarchy-walker, openssl-1.0, openssl-1.0-debug, tizen-sdb, tizen-sdb-debug, zcode). None has a sync version to be newer than and none appears in the pending list, so the widened coverage does not change the count: both readings give 0.

6. No hidden holds [obs]: `pacman -Qqu` (exit 0), which lists upgrade candidates including ignored ones, returned the same three names as `pacman -Qu`. No IgnorePkg entry is suppressing a pending upgrade that the capture would have missed.

## Residual risk and verification gaps

- My sweep compares against today's on-disk sync databases; it inherits whatever `pacman -Sy` last refreshed (P4 territory, out of my scope). A premise about the *live mirror* state would need a network query, which I did not run [unk].
- The capture's P1 wording "all from the third-party omarchy and openai-chatgpt repos" is confirmed for count and attribution, but repo priority on a name collision was not exercised: no pending package exists in two repos, so the any/entry distinction in my method never had to break a tie [inf].

Scope: read=round-24 capture.txt (pending, local-newer-than-sync, libinput lines); wrote=.ufo/waves/round-24/w1/RevIndependentP1P2.md; executed=pacman -Qu, pacman -Sup --print-format '%r %n %v', pacman -Sl, pacman -Q, pacman -Qqu, pacman --version, vercmp (batched over version-differing pairs)
Installs: none
