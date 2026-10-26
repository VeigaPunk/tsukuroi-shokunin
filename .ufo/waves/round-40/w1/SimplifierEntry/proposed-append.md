
## Round-40 clarification (append-only, 2026-10-26)

- **EX5 host clause withdrawn.** "on this host `/tmp` is a tmpfs" is false: `/tmp` is xfs on
  `/dev/nvme1n1p1` (`findmnt -T /tmp`; `tmp.mount` active since 2026-10-26 00:40:57 -03, before the
  06:54:46Z capture), and no frozen capture holds the fact.
- **Host-column provenance.** Only EX4/EX6 hold values the recheck re-derives from `hostcap/`; EX2's reads
  the round-39 `[ALPM-SCRIPTLET]` lines (S218, TO8). The other host cells add no captured measurement:
  EX3's and EX8's state a rule consequence only, and EX1's root-`/` parenthetical and EX7's live `grep -c`
  (0, 2026-10-26) are host facts no frozen capture holds. So the intro's "the host column comes from a
  frozen read-only capture" covers EX4/EX6 only, the Boundaries "EX1–EX3 and EX5 have no host instance in
  the capture" is superseded here, and EX3's "(and kept by sudo)" asserts no sudo behaviour: which
  variables sudo keeps is Boundary 3's subject.
- **EX6/EX8 targets.** The `NeedsTargets` lines are the matched `filelist.files[f].name` strings (hook.c:275,
  :290, :304) — root-relative, no leading `/`, the form S224 alpm-hooks.5.asciidoc:61-67 requires of
  `Target` — so opening a target means prefixing the installation root.
- **EX4/EX5 scriptlet.** EX4's `<scriptlet>` is the in-root path, not the host path — trans.c:398 strips the
  root prefix (root `/` leaves `/tmp/alpm_XXXXXX/.INSTALL`) — and EX5's value is that string relative to
  `<root>`; the run call (:410) passes a null input callback, so a scriptlet also reads end-of-file on
  stdin (rely-on item 3).
- **EX7 continuation.** A `Depends` skip in a Pre hook without `AbortOnFail` lets the next Pre hook run
  (hook.c:660-668); `AbortOnFail` on a PostTransaction hook warns at parse (hook.c:141-143) and cannot stop
  the transaction (trans.c:238 discards the Post result); S224 `alpm-hooks.5.asciidoc:87-89` states that
  scope, outside the `:83-85` EX7 cites.
