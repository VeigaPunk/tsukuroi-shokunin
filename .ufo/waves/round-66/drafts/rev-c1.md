# C1-ATTACK — Independent Re-derivation (R1RevC1, reviewer)

Timestamp: 2026-11-03T21:01:32Z (`date -u +%Y-%m-%dT%H:%M:%SZ`, rc=0)
Scratch: /fast/scratch/hyaku/tsukuroi-r66/R1RevC1 (removed before yield; receipts below are verbatim copies)
Seat: R1RevC1 · Item C1-ATTACK · lane tsukuroi-shokunin · base c68bfe97
Claim attacked: C1 (SOURCED, S283) — frozen in SCORECARD.md "Round 66 — declaration".

---

## Attack A1 — target: C1 source identity (S283 fetch + sha256)

$ S=/fast/scratch/hyaku/tsukuroi-r66/R1RevC1; mkdir -p "$S" && date -u +%Y-%m-%dT%H:%M:%SZ
2026-11-03T21:01:32Z
rc=0

$ curl -sS -o "$S/rel.json" -w "http_code=%{http_code}\n" https://api.github.com/repos/systemd/systemd/releases/tags/v262; echo "rc=$?"
http_code=200
rc=0

$ sha256sum "$S/rel.json"
008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b  /fast/scratch/hyaku/tsukuroi-r66/R1RevC1/rel.json

Fresh bytes over HTTP 200 hash exactly the frozen S283 sha256 008e1265088e4a8b11f749cb646789fb805a5d82c23dc8996588a85c9babce0b. Also matches the independent fetch recorded in drafts/scout-s283-scope.md (same URL, same sha) — two independent agents, one hash.

**AGREE** — source identity reproduces byte-exactly.

## Attack A2 — target: C1 bullet location + verbatim sentence + documented values + scope

$ python3 - "$S/rel.json" <<'EOF'  (json.load; body split on "\n")
tag_name: v262
published_at: 2026-09-22T13:19:16Z
hits: 1
BODY-LINE 248:
        * The new systemd.credentials_boot_policy= kernel command line option
rc=0

Bullet continuation, body lines 248–253 verbatim:

        * The new systemd.credentials_boot_policy= kernel command line option
          controls when boot credentials encrypted with the "null" key are
          accepted. It accepts "strict" (never), "tofu" (first boot or no
          TPM2), "relaxed" (SecureBoot disabled or no TPM2, the default and
          previous behavior), and "off" (always). It does not affect
          credentials encrypted with host or TPM2 keys.

Section membership:

$ python3 - (loose search over lines starting with "#", containing "system and service manager")
line 155: '##         Changes in the system and service manager:'
248 under section: True
nearest above: (155, '##         Changes in the system and service manager:')
rc=0

Cross-check against the frozen predicate text:
- "strict" (never) — matches line 250.
- "tofu" (first boot or no TPM2) — matches lines 250–251.
- "relaxed" (SecureBoot disabled or no TPM2; default and previous behavior) — matches lines 251–252 ("SecureBoot disabled or no TPM2, the default and previous behavior"); comma vs semicolon is punctuation only, semantics identical.
- "off" (always) — matches line 252.
- Scope "boot credentials encrypted with the 'null' key only" — matches lines 249 and 252–253 ("does not affect credentials encrypted with host or TPM2 keys").
- Section "Changes in the system and service manager:" — header at body line 155; bullet at 248 sits under it.
- published_at 2026-09-22T13:19:16Z matches the S282 row (line 292 of corpus/SOURCES.md).

**AGREE** — every documented value, the scope clause, and the section anchor re-derive from the frozen hash's bytes.

## Attack A3 — target: C1 Gate quote length (<= 25 words)

Quote chosen for citation (body line 250–252, the values sentence):

$ printf '%s\n' 'It accepts "strict" (never), "tofu" (first boot or no TPM2), "relaxed" (SecureBoot disabled or no TPM2, the default and previous behavior), and "off" (always).' > "$S/quote.txt"; wc -w "$S/quote.txt"
It accepts "strict" (never), "tofu" (first boot or no TPM2), "relaxed" (SecureBoot disabled or no TPM2, the default and previous behavior), and "off" (always).
24 /fast/scratch/hyaku/tsukuroi-r66/R1RevC1/quote.txt
rc=0

**AGREE** — 24 <= 25 words.

## Attack A4 — target: C1 counter semantics (SOURCES registry shape, NF 13, grep count)

Header row (line 5):

$ sed -n '5p' corpus/SOURCES.md
| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
rc=0

$ awk -F'|' '/^\| S282 /{print "S282 NF="NF} /^\| ID /{print "HEADER NF="NF}' corpus/SOURCES.md
S282 NF=13

$ grep -n '^| S282' corpus/SOURCES.md
292:| S282 | systemd v262 release notes — https://api.github.com/repos/systemd/systemd/releases/tags/v262 | docs | A | ... (row continues; full text at corpus/SOURCES.md:292, 2675 bytes for lines 290–293)
rc2=0

S283-shape simulation (S282's row with id swapped to S283, written to scratch — no tracked file touched):

$ awk -F'|' '{print "sim NF="NF}' "$S/s283_sim.txt"
sim NF=13

$ grep -cE '^\| S[0-9]{3,}' "$S/s283_sim.txt"
1

$ { sed -n '292p' corpus/SOURCES.md; cat "$S/s283_sim.txt"; } | grep -cE '^\| S[0-9]{3,}'
2

An S283 row written in the same 13-field (11-column + 2 edge) shape yields NF=13 under `awk -F'|'` and is counted once by `grep -cE '^\| S[0-9]{3,}'`. Live registry count:

$ grep -cE '^\| S[0-9]{3,}' corpus/SOURCES.md
282
rc=0

**AGREE** — counters behave as the predicate assumes; S283 in S282's shape counts, and the live count (282) is exactly one short of the frozen floor (>= 283), i.e. the claim's delta is exactly S283.

## Attack A5 — target: C1 do-nothing control at base c68bfe97

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin cat-file -e c68bfe97:corpus/knowledge/systemd262-credentials-boot-policy-r66.md; echo "rc=$?"
fatal: path 'corpus/knowledge/systemd262-credentials-boot-policy-r66.md' does not exist in 'c68bfe97'
rc=128

$ git -C /home/vgpnk/Projects/shokunin/tsukuroi-shokunin show c68bfe97:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3,}'
282
rc=0

Predicate FAILS at base exactly as frozen: knowledge file absent (rc 128) and registry at 282 rows (< 283). The claim is not vacuously true.

**AGREE** — do-nothing control reproduces.

## Attack A6 — target: C1 land dependency (present-file clause, '^| CB' >= 5)

$ F=corpus/knowledge/systemd262-credentials-boot-policy-r66.md; ls -la "$F"
ls: cannot access '.../corpus/knowledge/systemd262-credentials-boot-policy-r66.md': No such file or directory
ls_rc=2

$ grep -c '^| CB' "$F"
grep: .../corpus/knowledge/systemd262-credentials-boot-policy-r66.md: No such file or directory (os error 2)
grep_rc=2

The working tree does not yet contain the knowledge file, so `grep -c '^| CB' >= 5` is currently unrunnable (not zero, not >= 5 — no file). This is the C1 scribe's in-flight deliverable, not a defect of the predicate: the clause is well-defined once the file lands at integration, and the base control (A5) proves the predicate fails without it. Recorded as **PENDING-LAND**, commands and errors verbatim above. No tracked file was touched.

**AGREE** with the clause as a claim-time condition; untestable at this instant by design of the wave (scribe seats still running).

---

## Verdict

C1-PREDICATE-SOUND

Six attacks (A1–A6), zero disagreements. The one non-reproducing check (A6) is pending a sibling's write, is expected mid-wave, and its base-side failure control (A5) reproduces exactly. Source identity, bullet text, documented values, scope clause, section anchor, quote budget, counter semantics, and the do-nothing baseline all re-derive from primary evidence.
