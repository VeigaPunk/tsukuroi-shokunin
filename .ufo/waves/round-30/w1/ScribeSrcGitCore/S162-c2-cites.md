# S162 — C2 citations (no D row)

This source backs claim **C2** (operability: frozen git-writing lane tools under residual git channels),
so no C1 `Dnn` row is drafted. The row-shaped records below are seat-local slugs (`C2-*`), not corpus
`Dnn` ids: C1's frozen-token rule assigns a token per `Dnn`, and no `Dnn` exists for this source, so the
quotes carry the C2 channel words (ignore, attributes, hooks) instead. The L1 may renumber or fold them.

Snapshot: `.ufo/waves/round-30/w1/ScribeSrcGitCore/S162-core.adoc`
sha256 `aa6015220b25a284408fa5e03bba40b70fcc69fe1a03a60859e019a84a2c9f5d`, 36651 bytes, 798 lines,
plain curl HTTP 200 from https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/config/core.adoc.

## The lines that make per-user ignore and attributes apply with no config naming them

The operative words are **"Defaults to"** (line 492) and the default-value sentence at 509-510: git reads
those paths as built-in defaults, so the file takes effect on existence alone; no `core.excludesFile` or
`core.attributesFile` entry has to name it, and no config file has to exist at all.

line 492 (leading byte is a TAB):
```
	Defaults to `$XDG_CONFIG_HOME/git/ignore`.
```

lines 493-494 (leading byte is a TAB):
```
	If `$XDG_CONFIG_HOME` is either not set or empty, `$HOME/.config/git/ignore`
	is used instead. See linkgit:gitignore[5].
```

lines 509-510 (leading byte is a TAB):
```
	`$XDG_CONFIG_HOME/git/attributes`. If `$XDG_CONFIG_HOME` is either not
	set or empty, `$HOME/.config/git/attributes` is used instead.
```

## The core.hooksPath lines

lines 513-514 (leading byte is a TAB):
```
	By default Git will look for your hooks in the
	`$GIT_DIR/hooks` directory. Set this to different path,
```

lines 529-532 (no leading whitespace):
```
You can also disable all hooks entirely by setting `core.hooksPath`
to `/dev/null`. This is usually only advisable for expert users and
on a per-command basis using configuration parameters of the form
`git -c core.hooksPath=/dev/null ...`.
```

## Candidate counter rows (JSON list)

```json
[
  {
    "id": "C2-1",
    "statement": "On a btrfs host, read $XDG_CONFIG_HOME/git/ignore before trusting git status; this path is git's built-in default, so a '*' there hides every untracked file with no config naming it.",
    "source": "S162",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitCore/S162-core.adoc",
    "line": 492,
    "quote": "Defaults to `$XDG_CONFIG_HOME/git/ignore`"
  },
  {
    "id": "C2-2",
    "statement": "When XDG_CONFIG_HOME is unset or empty, read $HOME/.config/git/ignore instead; a per-user ignore file left there still applies with no git configuration.",
    "source": "S162",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitCore/S162-core.adoc",
    "line": 493,
    "quote": "`$HOME/.config/git/ignore`"
  },
  {
    "id": "C2-3",
    "statement": "Read $XDG_CONFIG_HOME/git/attributes as git's default attributes file; attributes there apply without any core.attributesFile entry being set by the operator.",
    "source": "S162",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitCore/S162-core.adoc",
    "line": 509,
    "quote": "`$XDG_CONFIG_HOME/git/attributes`. If `$XDG_CONFIG_HOME` is either not"
  },
  {
    "id": "C2-4",
    "statement": "On a host without XDG_CONFIG_HOME, read $HOME/.config/git/attributes instead; per-user attributes such as -text take effect from that default path.",
    "source": "S162",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitCore/S162-core.adoc",
    "line": 510,
    "quote": "set or empty, `$HOME/.config/git/attributes` is used instead."
  },
  {
    "id": "C2-5",
    "statement": "On a btrfs host, hooks run from $GIT_DIR/hooks by default; set core.hooksPath to redirect them, which a stray per-user config can do.",
    "source": "S162",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitCore/S162-core.adoc",
    "line": 514,
    "quote": "`$GIT_DIR/hooks` directory. Set this to different path,"
  },
  {
    "id": "C2-6",
    "statement": "Decide whether to disable hooks: setting core.hooksPath to /dev/null disables all hooks entirely, which is the documented neutralisation for a lane tool.",
    "source": "S162",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitCore/S162-core.adoc",
    "line": 529,
    "quote": "You can also disable all hooks entirely by setting `core.hooksPath`"
  },
  {
    "id": "C2-7",
    "statement": "For one command only, pass git -c core.hooksPath=/dev/null so a stray per-user hooks path cannot run hooks during that invocation.",
    "source": "S162",
    "snapshot": ".ufo/waves/round-30/w1/ScribeSrcGitCore/S162-core.adoc",
    "line": 532,
    "quote": "`git -c core.hooksPath=/dev/null ...`"
  }
]
```

## Corroborating lines, same tag (not registered)

`S162-gitignore.adoc` — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitignore.adoc
(HTTP 200, 9535 bytes, 253 lines, sha256 `338221577b4f47ea61b10eb6e57e7b0aab71e3f7ff8ce8bc067676aede805e71`).
Line 10 is the SYNOPSIS list of exclude sources with no config condition; lines 58-60 repeat the default:

```
$XDG_CONFIG_HOME/git/ignore, $GIT_COMMON_DIR/info/exclude, .gitignore
```
```
   `core.excludesFile` in the user's `~/.gitconfig`. Its default value is
   $XDG_CONFIG_HOME/git/ignore. If $XDG_CONFIG_HOME is either not set or
   empty, $HOME/.config/git/ignore is used instead.
```

`S162-gitattributes.adoc` — https://raw.githubusercontent.com/git/git/v2.56.0/Documentation/gitattributes.adoc
(HTTP 200, 50608 bytes, 1385 lines, sha256 `4ca89456d5b3cf9c4fe3c5f1a020ec86ef81be50b3d5c00f40c15edce9bd3bde`).
Lines 92-94:

```
`core.attributesFile` configuration option (see linkgit:git-config[1]).
Its default value is $XDG_CONFIG_HOME/git/attributes. If $XDG_CONFIG_HOME
is either not set or empty, $HOME/.config/git/attributes is used instead.
```

## Behavioural check with the installed git (supporting evidence, not the frozen counter)

Run 2026-10-22 in `/fast/scratch/hyaku/tsukuroi-r30/ScribeSrcGitCore/probe` with
`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE HOME=<scratch>/home XDG_CONFIG_HOME=<scratch>/home/.config`,
git version 2.56.0, no `<scratch>/home/.gitconfig` and no `git/config` present:

- before any per-user file: `git status --porcelain` printed `?? a.txt` and `?? b.md` (exit 0)
- after writing only `<XDG_CONFIG_HOME>/git/ignore` containing `*`: `git status --porcelain` printed nothing (exit 0)
- after deleting that ignore file again: `?? a.txt` and `?? b.md` returned — the effect came from the file, not the host
- after writing only `<XDG_CONFIG_HOME>/git/attributes` containing `* -text`: `git check-attr text -- a.txt b.md` printed `a.txt: text: unset` and `b.md: text: unset` (exit 0)
- after writing `<XDG_CONFIG_HOME>/git/config` with `core.hooksPath` at a directory holding a failing `pre-commit`: `git commit` printed `HOOK-FROM-USER-CONFIG` and exited 1; with `-c core.hooksPath=/dev/null` the same commit succeeded (exit 0)
