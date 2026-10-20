# Reverse locator intent — round 15

## Axes
- **Depth:** recover what the r14 locator meant and separate it from the source proposition.
- No other axis was assessed in this read-only assignment.

## Evidence chain
1. `corpus/knowledge/source-scope-correction-r14.md:31-42` records S044 at `systemd.exec(5) § ProtectSystem= (under SANDBOXING)`, cites “rendered lines 1266-1267,” and gives the exact 11-word quote: “Takes a boolean argument or the special values "full" or "strict".” The line locator's documented purpose is to point to that quoted definition; it is not itself the evidence for the value-domain claim.
2. The contemporaneous r14 source review, `.ufo/waves/round-14/repair/QuoteReview.md:8-22`, says it reopened native HTML (footer `systemd 262.1`), locates the paragraph at page lines 1271-1287, verifies the same 11-word quote, and cautions that the definition does not itself state exhaustiveness.
3. The independent r14 verifier, `corpus/lessons/round-14-verifier-spotcheck.md:233-246`, reports that in its reader lines 1266-1267 concern the AF_UNIX caveat; it places the `ProtectSystem=` heading at 1270 and definition at 1272-1273. It says the stable heading and verbatim quote still resolve, so the discrepancy does not falsify the correction. It recommends a renderer-qualified locator or the stable heading and separately rejects the unsupported “documents no further values” documentation claim.
4. `corpus/SOURCES.md:50` identifies S044 as tier-A documentation for the documented `ProtectSystem=` argument domain and distinguishes it from separately documented unit-side mechanisms. Reopening `https://man.archlinux.org/man/systemd.exec.5` on 2026-10-20 shows the quote under `SANDBOXING > ProtectSystem=` and footer `systemd 262.1`.

## Reconstructed intent and recommendation
The r14 numeric locator was [INFERENCE] an attempted supplemental location for the quoted first definition sentence. The surviving record does not identify the renderer that produced “rendered lines 1266-1267”; other recorded readers number this passage differently. Its exact rendering scheme therefore cannot be recovered from these artifacts. Preserve the historical citation as history, but do not treat its bare numbers as stable source coordinates. For R15-LOCATOR use the stable anchor `systemd.exec(5) > SANDBOXING > ProtectSystem=` and identify the first definition sentence; include line numbers only with the exact reader/renderer identified.

For R15-POSITIVE-DOMAIN retain the positive proposition the source supports: `ProtectSystem=` “takes a boolean argument or the special values "full" or "strict".” Do not turn this into a claim that the source proves an exhaustive parser grammar, excludes undocumented values, or lists every boolean spelling. Supersede the r14 “documents no further values” wording rather than weakening or dropping the positive definition. No parser/runtime behavior was tested.

## Confidence
- High for the exact positive definition and the reader-number discrepancy: directly reopened source plus the contemporaneous source review and independent verifier.
- Medium for the numeric locator's intended role: the artifacts establish it as a supplemental location but do not preserve which renderer produced it.

## Limits and tools
- `xd://lsp` is unavailable (`No such tool`); no LSP status or semantic references could be obtained. Literal grep was used only to locate artifact text; conclusions above rest on direct reads and the reopened source, not grep as semantic proof.
- Research used read/glob/grep only. No tests or runtime checks were run; no packages/tools were installed or updated.
