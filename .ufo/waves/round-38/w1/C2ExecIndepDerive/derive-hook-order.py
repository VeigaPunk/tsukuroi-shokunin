#!/usr/bin/env python3
"""Independent re-derivation of the round-38 effective ALPM hook table.

Seat C2ExecIndepDerive (item C2-2). Written from scratch against the pinned
source snapshot; it does NOT import, read or copy tools/check-hook-order-r38.py.

Model derived from .ufo/waves/round-38/sources/ at pacman 54d9411:

  hook.c:540        for(i = alpm_list_last(handle->hookdirs); i; i = previous)
                    -> directories are walked last-to-first.
  alpm.c:56-62      alpm_list_add(NULL, hookdir) puts the system dir
                    (SYSHOOKDIR = /usr/share/libalpm/hooks) at the list head;
                    pacman.conf HookDir entries are appended after it, so
                    /etc/pacman.d/hooks is the list tail and is walked first.
  hook.c:568-576    only names ending in ALPM_HOOK_SUFFIX (".hook") are hooks.
  hook.c:578-581    find_hook(): first name seen wins, later same-name files are
                    skipped ("skipping overridden hook").
  hook.c:588-591    a directory named *.hook is skipped (S_ISDIR).
  hook.c:603-611    parse_ini() failure or _alpm_hook_validate() failure drops
                    the file from the candidate list.
  hook.c:106-150    _alpm_hook_validate: triggers == NULL is valid (dummy mask
                    hook, returns 0 immediately); otherwise every trigger needs
                    Target(s), Type, Operation, and the hook needs Exec and When.
  hook.c:141-145    AbortOnFail on a PostTransaction hook is only a warning.
  hook.c:443-455    _alpm_hook_cmp: l = strlen(name) - strlen(".hook");
                    strncmp() over min(l1,l2); on a prefix tie the shorter runs
                    first; otherwise the first differing byte decides.
  hook.c:629-631    hooks = alpm_list_msort(hooks, count, _alpm_hook_cmp).
  hook.c:636-641    only hooks with hook->when == when are collected, in the
                    sorted order; positions are counted per phase.
  hook.c:511         _alpm_run_chroot(handle, hook->cmd[0], ...): the program is
                    the first word of Exec.
  parsers (hook.c:157-290)  AbortOnFail / NeedsTargets are bare flags (presence
                    sets the int); When accepts exactly PreTransaction and
                    PostTransaction; unknown section/key/value is a parse error.

Output row format: `when pos name dir abort needs exec0`.
"""

import sys
import os

SUFFIX = ".hook"

USR = "usr"
ETC = "etc"

CAPTURE = "/home/vgpnk/Projects/shokunin/tsukuroi-shokunin/.ufo/waves/round-38/frozen/hooks-capture"
DIRS = [(USR, os.path.join(CAPTURE, "usr-share-libalpm-hooks")),
        (ETC, os.path.join(CAPTURE, "etc-pacman.d-hooks"))]

VALID_SECTIONS = {"Trigger", "Action"}
VALID_TRIGGER_KEYS = {"Operation", "Type", "Target"}
VALID_ACTION_KEYS = {"When", "Description", "Depends", "AbortOnFail",
                     "NeedsTargets", "Exec"}


class ParseError(Exception):
    pass


def parse_ini(text):
    """Yield (section, key, value). Bracketed lines open a section and yield
    (section, None, None); option lines yield (section, key, value-or-None).

    Mirrors hook.c:157-290: any option before a section header is an error, any
    section other than Trigger/Action is an error, and any key outside the
    documented set is an error -- each of those makes the whole hook invalid.
    """
    section = None
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith(";"):
            continue
        if line.startswith("["):
            if not line.endswith("]"):
                raise ParseError("line %d: unterminated section" % lineno)
            name = line[1:-1].strip()
            if name not in VALID_SECTIONS:
                raise ParseError("line %d: invalid section %s" % (lineno, name))
            section = name
            yield (section, None, None)
            continue
        if section is None:
            raise ParseError("line %d: invalid option outside a section" % lineno)
        if "=" in line:
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip()
        else:
            # bare flag lines (AbortOnFail / NeedsTargets), value stays NULL
            key, value = line, None
        allowed = VALID_TRIGGER_KEYS if section == "Trigger" else VALID_ACTION_KEYS
        if key not in allowed:
            raise ParseError("line %d: invalid option %s in [%s]"
                             % (lineno, key, section))
        yield (section, key, value)


def load_hook(path, name):
    """Build the _alpm_hook_t fields the table needs, or raise ParseError."""
    hook = {"name": name, "triggers": [], "when": None, "cmd": None,
            "abort": 0, "needs": 0}
    with open(path, "r", encoding="utf-8", errors="strict") as fh:
        text = fh.read()

    for section, key, value in parse_ini(text):
        if key is None:
            if section == "Trigger":
                hook["triggers"].append({"ops": [], "type": None, "targets": []})
            continue
        if section == "Trigger":
            trig = hook["triggers"][-1]
            if key == "Operation":
                if value not in ("Install", "Upgrade", "Remove"):
                    raise ParseError("invalid Operation %r" % (value,))
                trig["ops"].append(value)
            elif key == "Type":
                if value not in ("Package", "Path", "File"):
                    raise ParseError("invalid Type %r" % (value,))
                trig["type"] = value
            else:  # Target
                if not value:
                    raise ParseError("empty Target")
                trig["targets"].append(value)
        else:
            if key == "When":
                # a redefinition warns and overwrites (hook.c:236-252)
                if value not in ("PreTransaction", "PostTransaction"):
                    raise ParseError("invalid When %r" % (value,))
                hook["when"] = value
            elif key == "Exec":
                if not value:
                    raise ParseError("empty Exec")
                words = value.split()
                if not words:
                    raise ParseError("unparsable Exec")
                hook["cmd"] = words[0]
            elif key == "AbortOnFail":
                hook["abort"] = 1
            elif key == "NeedsTargets":
                hook["needs"] = 1
            # Description / Depends are irrelevant to ordering

    # _alpm_hook_validate (hook.c:106-150)
    if hook["triggers"]:
        for trig in hook["triggers"]:
            if not trig["targets"]:
                raise ParseError("trigger without Target")
            if trig["type"] is None:
                raise ParseError("trigger without Type")
            if not trig["ops"]:
                raise ParseError("trigger without Operation")
        if hook["cmd"] is None:
            raise ParseError("missing Exec")
        if hook["when"] is None:
            raise ParseError("missing When")
    else:
        # dummy mask hook: valid, never runs (hook.c:112-117)
        pass
    return hook


def hook_cmp(a, b):
    """hook.c:443-455, byte-for-byte."""
    l1 = len(a) - len(SUFFIX)
    l2 = len(b) - len(SUFFIX)
    n = l1 if l1 <= l2 else l2
    ab = a.encode()
    bb = b.encode()
    for k in range(n):
        if ab[k] != bb[k]:
            return -1 if ab[k] < bb[k] else 1
    if l1 != l2:
        return -1 if l1 < l2 else 1
    return 0


def collect(swap_priority=False):
    """Walk hookdirs last-to-first, resolving same-name overrides.

    swap_priority=False is the derived model: hookdirs = [system dir, HookDir],
    so the walk sees /etc/pacman.d/hooks first. swap_priority=True is the
    counterfactual used to measure how much of the table depends on HO2.
    """
    dir_of = {d for d, _ in DIRS}
    assert dir_of == {USR, ETC}
    by_dir = {}
    for tag, path in DIRS:
        names = sorted(os.listdir(path))  # readdir order is irrelevant: the
                                          # final msort is by name; names are
                                          # unique inside one directory
        by_dir[tag] = (path, names)

    seen = {}          # file name -> hook (first seen wins)
    order_seen = []    # (dir, name) in walk order, effective hooks only
    invalid = []       # (dir, name, reason)
    overridden = []    # (winner dir/name, skipped dir/name)
    hook_suffixed = 0  # every *.hook file walked, over all dirs
    skipped_non_hook = []      # files not ending in .hook
    skipped_dir = []           # directories named *.hook

    walk = list(DIRS) if swap_priority else list(reversed(DIRS))  # hook.c:540
    for tag, _ in walk:
        path, names = by_dir[tag]
        for name in names:
            if not name.endswith(SUFFIX) or len(name) < len(SUFFIX):
                skipped_non_hook.append(("%s/%s" % (tag, name)))
                continue
            full = os.path.join(path, name)
            if os.path.isdir(full):
                skipped_dir.append("%s/%s" % (tag, name))
                continue
            hook_suffixed += 1
            if name in seen:
                overridden.append(("%s/%s" % (seen[name]["dir"], name),
                                   "%s/%s" % (tag, name)))
                continue               # hook.c:578-581 (override)
            try:
                hook = load_hook(full, name)
            except ParseError as exc:
                invalid.append(("%s/%s" % (tag, name), str(exc)))
                continue
            hook["dir"] = tag
            seen[name] = hook
            order_seen.append((tag, name))

    hooks = sorted(seen.values(), key=__import__("functools").cmp_to_key(
        lambda h1, h2: hook_cmp(h1["name"], h2["name"])))
    return (hooks, order_seen, invalid, overridden, hook_suffixed,
            skipped_non_hook, skipped_dir)


def order_vs_naive(hooks):
    """Pairs whose relative order differs between _alpm_hook_cmp (suffix-stripped)
    and a plain byte sort of the full file names."""
    names_cmp = [h["name"] for h in hooks]
    names_naive = sorted(names_cmp)
    moved = []
    if names_cmp == names_naive:
        return moved
    for i in range(len(names_cmp)):
        for j in range(i + 1, len(names_cmp)):
            a, b = names_cmp[i], names_cmp[j]
            if names_naive.index(a) > names_naive.index(b):
                moved.append((a, b))
    return moved


def rows(hooks):
    out = []
    for when in ("PreTransaction", "PostTransaction"):
        pos = 0
        for hook in hooks:
            if hook["when"] != when:
                continue
            pos += 1
            out.append("%s %d %s %s %s %s %s" % (
                when, pos, hook["name"], hook["dir"],
                "yes" if hook["abort"] else "no",
                "yes" if hook["needs"] else "no",
                hook["cmd"]))
    return out


def parse_md_table(path):
    rows_md = []
    started = False
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if line.startswith("| when | pos | name |"):
                started = True
                continue
            if not started:
                continue
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) != 7 or cells[0] == "---":
                continue
            when, pos, name, d, abort, needs, exe = cells
            rows_md.append("%s %s %s %s %s %s %s" % (
                when, pos, name.strip("`"), d, abort, needs, exe.strip("`")))
    return rows_md


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    order_file = None
    for i, arg in enumerate(sys.argv):
        if arg == "--order-file" and i + 1 < len(sys.argv):
            order_file = sys.argv[i + 1]
            args = [a for a in args if a != order_file]
    md = args[0] if args else None
    swap_priority = "--swap-priority" in sys.argv
    (hooks, order_seen, invalid, overridden, hook_suffixed,
     skipped_non_hook, skipped_dir) = collect(swap_priority)
    if swap_priority:
        print("# COUNTERFACTUAL: hookdir walk order reversed (usr first)",
              file=sys.stderr)

    for name in skipped_non_hook:
        print("SKIP non-hook %s" % name, file=sys.stderr)
    for name in skipped_dir:
        print("SKIP directory %s" % name, file=sys.stderr)
    for item in invalid:
        print("INVALID %s: %s" % item, file=sys.stderr)
    for winner, loser in overridden:
        print("OVERRIDE %s wins, %s skipped" % (winner, loser), file=sys.stderr)

    derived = rows(hooks)

    pre = sum(1 for h in hooks if h["when"] == "PreTransaction")
    post = sum(1 for h in hooks if h["when"] == "PostTransaction")
    masks = [h["name"] for h in hooks if not h["triggers"]]
    aborts = [h["name"] for h in hooks if h["abort"]]
    needs = sum(1 for h in hooks if h["needs"])
    print("# walk order (dir name): %s"
          % ", ".join("%s/%s" % (d, n) for d, n in order_seen[:3]) + " ...",
          file=sys.stderr)
    print("# hook-suffixed files: %d, overridden: %d, invalid: %d, effective: %d"
          % (hook_suffixed, len(overridden), len(invalid), len(hooks)),
          file=sys.stderr)
    print("# Pre=%d Post=%d masks=%d AbortOnFail=%d NeedsTargets=%d"
          % (pre, post, len(masks), len(aborts), needs), file=sys.stderr)

    moved = order_vs_naive(hooks)
    if moved:
        print("# _alpm_hook_cmp order differs from full-name byte sort for:",
              file=sys.stderr)
        for a, b in moved:
            print("#   %s before %s (naive sort reverses this)" % (a, b),
                  file=sys.stderr)
    else:
        print("# _alpm_hook_cmp order == full-name byte sort", file=sys.stderr)

    for row in derived:
        print(row)

    if order_file:
        with open(order_file, "w", encoding="utf-8") as fh:
            for hook in hooks:
                fh.write("%s\n" % hook["name"])
        print("# wrote global sorted order to %s" % order_file, file=sys.stderr)

    if md:
        entry = parse_md_table(md)
        sets_d = set(derived)
        sets_e = set(entry)
        print("", file=sys.stderr)
        print("# diff vs %s: derived=%d entry=%d"
              % (md, len(derived), len(entry)), file=sys.stderr)
        only_d = sorted(sets_d - sets_e)
        only_e = sorted(sets_e - sets_d)
        for r in only_d:
            print("ONLY-DERIVED: %s" % r, file=sys.stderr)
        for r in only_e:
            print("ONLY-ENTRY:   %s" % r, file=sys.stderr)
        if not only_d and not only_e:
            print("# IDENTICAL", file=sys.stderr)
        return 0 if not only_d and not only_e else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
