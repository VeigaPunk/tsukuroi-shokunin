{
  "seat": "ReviewEntry-4",
  "lane_revision": "cefb4188b484329c4908a19a277f8fb120fb4f56",
  "scope": "C2 entry limine-pin-plane-r87 LP1-LP8 vs pinned sources S350-S354 + Operator actions + Limits",
  "verdicts": {
    "support": [
      "LP1",
      "LP3",
      "LP4",
      "LP6",
      "LP7 (anchor gap)"
    ],
    "partial": [
      "LP2 (cmdline/comment sub-claim uncited; fix: S350 267-268,272-274 + S351 28-32)",
      "LP5 (uri.c:311 accepts y; fix: Y-or-y wording + S352 798-802)"
    ],
    "refute": []
  },
  "counts": "6 support, 2 partial, 0 refute; 8/8 quotes verbatim (whitespace-normalized) and ≤25 words",
  "sources_check": "sha256 all five pins OK rc=0, matches SOURCES.md + freeze manifest; S354 anchor misses quote line 191 (189-190 → 188-191); used-by verified; trunk-BLAKE3 Limits claim unpinned → flag",
  "host_claims": "LP1/LP3/LP5/LP6/LP7/LP8 host_value cells verified against host + live receipts (mtimes 18:11:22, 5 pins 128 lower-hex, line 8 'no', SecureBoot byte 0, rc 1, cmp identical); QUALITY 124 = QUALITY.md:285; gate stricter-SB reading confirmed at check-limine-pins.py:154-156",
  "report": "tsukuroi-shokunin/.ufo/waves/round-87/w1/ReviewEntry.md",
  "receipts": [
    "tsukuroi-shokunin/.ufo/waves/round-87/w1/ReviewEntry/sed-proofs.md",
    "tsukuroi-shokunin/.ufo/waves/round-87/w1/ReviewEntry/quote-verification.txt",
    "tsukuroi-shokunin/.ufo/waves/round-87/w1/ReviewEntry/sources-check.txt"
  ],
  "refused": "nothing; read-only review, no lane edits, no installs, no scratch left behind",
  "gaps": "C1 battery/gate not re-run (out of scope; L1 live receipt used as committed evidence); no lsp server → text-level verification only"
}