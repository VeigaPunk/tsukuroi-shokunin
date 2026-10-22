# S163 — C2 citations (no D row)

This source backs claim **C2** (operability: the eleven frozen git-writing lane tools under the three
residual git channels), so no C1 `Dnn` row is drafted. The row-shaped records below are seat-local slugs
(`C2-*`), not corpus `Dnn` ids: C1's frozen-token table assigns one token per `Dnn` and none of D01-D10's
tokens names a git variable, so the quotes carry the frozen git variable names instead. The L1 may
renumber or fold them; `S163-rows.json` holds the same four records as a JSON list.

Snapshot: `.ufo/waves/round-30/w1/ScribeSrcGitEnv/S163-git.adoc`, 47005 bytes, 1212 lines,
sha256 `050c5330f1a231be22bee3db27c7ef90d8ba22bb7bd6c72c8bab462f6f0a1f79`,
plain curl HTTP 200 from https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git.adoc
(no fallback needed).

## The four lines the C2 contract cites

Each quote was checked with `sed -n '<line>p' <snapshot> | grep -cF '<quote>'` printing 1.

- **GIT_CEILING_DIRECTORIES** — `S163-git.adoc:568` — ``GIT_CEILING_DIRECTORIES=/maybe/symlink::/very/slow/non/symlink``
  The definition starts at line 555: it is a colon-separated list of absolute paths, "a list of
  directories that Git should not chdir up into while looking for a repository directory" (line 557),
  and line 560 says it will not "exclude the current working directory or a GIT_DIR set on the
  command line or in the environment".
- **GIT_CONFIG_GLOBAL** — `S163-git.adoc:770` — ``will not be read. Likewise, if `GIT_CONFIG_GLOBAL` is set, neither``
  The continuation at line 771 is `` `$HOME/.gitconfig` nor `$XDG_CONFIG_HOME/git/config` will be read. Can``
  and line 772 says it "be set to `/dev/null` to skip reading configuration files of the respective level".
- **GIT_CONFIG_SYSTEM** — `S163-git.adoc:768` — ``system-level configuration files. If `GIT_CONFIG_SYSTEM` is set, the``
  Line 769 names the file it suppresses: "system config file defined at build time (usually `/etc/gitconfig`)".
- **GIT_CONFIG_NOSYSTEM** — `S163-git.adoc:775` — `` `GIT_CONFIG_NOSYSTEM`:: ``
  Lines 776-779: it skips settings from the system-wide `$(prefix)/etc/gitconfig` and "can be used along
  with `$HOME` and `$XDG_CONFIG_HOME` to create a predictable environment for a picky script".

Additional line, same tag, not drafted as a row (the assignment names four variables; this one is the
filesystem-boundary switch the ceiling discussion depends on):

- **GIT_DISCOVERY_ACROSS_FILESYSTEM** — `S163-git.adoc:570` — `` `GIT_DISCOVERY_ACROSS_FILESYSTEM`:: ``
  Lines 571-576: git does not cross filesystem boundaries by default; setting the Boolean true tells it
  not to stop at them, and like the ceiling it "will not affect an explicit repository directory set via
  `GIT_DIR` or on the command line". Dropping the inherited name therefore restores the default
  no-crossing behaviour, which is the safe state for a sandbox whose TMPDIR may be on another filesystem
  than an enclosing repository.

## Where the per-user config is read from when GIT_CONFIG_GLOBAL is unset

Supplementary snapshot `.ufo/waves/round-30/w1/ScribeSrcGitEnv/S163-git-config.adoc`, 21576 bytes,
660 lines, sha256 `655541c20fe58e30c2e45803df422a5a1ed3658bf025ceaed6c1764089edcd27`, HTTP 200 from
https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/git-config.adoc.

From the FILES section (`git-config.adoc:370`), the user-specific configuration files are
`$XDG_CONFIG_HOME/git/config` (line 380) and `~/.gitconfig` (line 381), described at lines 382-384:

> `User-specific configuration files. When the XDG_CONFIG_HOME environment`
> `variable is not set or empty, $HOME/.config/ is used as`
> `$XDG_CONFIG_HOME.`

and lines 386-387 add: "These are also called "global" configuration files. If both files exist, both
files are read in the order given above." So with GIT_CONFIG_GLOBAL unset, git reads
`$XDG_CONFIG_HOME/git/config` (defaulting to `$HOME/.config/git/config` when XDG_CONFIG_HOME is unset or
empty) and then `~/.gitconfig`; this is exactly the per-user channel the C2 contract neutralises by
setting GIT_CONFIG_GLOBAL=/dev/null.

## Candidate counter rows (JSON list)

```json
[
  {
    "id": "C2-1",
    "statement": "On the btrfs host, set GIT_CEILING_DIRECTORIES to absolute paths above a lane tool's sandbox so its git writes cannot climb into an enclosing repository; the documented value is a colon-separated list of absolute paths.",
    "source": "S163",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitEnv/S163-git.adoc",
    "line": 568,
    "quote": "GIT_CEILING_DIRECTORIES=/maybe/symlink::/very/slow/non/symlink"
  },
  {
    "id": "C2-2",
    "statement": "On the btrfs host, point GIT_CONFIG_GLOBAL at /dev/null so a lane tool's git reads no per-user configuration, because setting it stops both $HOME/.gitconfig and $XDG_CONFIG_HOME/git/config being read.",
    "source": "S163",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitEnv/S163-git.adoc",
    "line": 770,
    "quote": "will not be read. Likewise, if `GIT_CONFIG_GLOBAL` is set, neither"
  },
  {
    "id": "C2-3",
    "statement": "On the btrfs host, point GIT_CONFIG_SYSTEM at /dev/null so a lane tool's git skips the build-time system configuration file, usually /etc/gitconfig, when its writes must not depend on host configuration.",
    "source": "S163",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitEnv/S163-git.adoc",
    "line": 768,
    "quote": "system-level configuration files. If `GIT_CONFIG_SYSTEM` is set, the"
  },
  {
    "id": "C2-4",
    "statement": "On the btrfs host, set GIT_CONFIG_NOSYSTEM=1 to skip the system-wide $(prefix)/etc/gitconfig, which the documentation gives as the way to build a predictable environment for a picky script.",
    "source": "S163",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitEnv/S163-git.adoc",
    "line": 775,
    "quote": "`GIT_CONFIG_NOSYSTEM`::"
  }
]
```

## Scope note for the C2 contract

The contract item 5 sets the ceiling to "the tool's temporary directory's parent". The doc's line 560
caveat matters: the ceiling "will not exclude ... a GIT_DIR set on the command line or in the
environment", so the contract's step 1 (drop every GIT_* name) is what actually closes that hole, and
the ceiling only bounds the implicit upward discovery. Nothing in this source contradicts the contract;
it supplies the two caveats (explicit GIT_DIR wins; discovery crosses filesystems only when the Boolean
is true).
