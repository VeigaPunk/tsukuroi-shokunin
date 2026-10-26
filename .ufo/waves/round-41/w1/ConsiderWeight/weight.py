#!/usr/bin/env python3
"""Evidence-weight watch (round-41 item K-1).

Measure, per round 35-41, the bytes each round's commits ADDED under `.ufo/waves/` and
`corpus/`, and flag any added blob over 1 MB.

Method
------
For every commit whose subject starts with `round-NN` (git log --grep '^round-NN'), list the
files it added with `git diff-tree -r -z --no-commit-id` (raw status `A`) and size each added
blob with `git cat-file --batch-check`.  Bucket by path prefix.  Round 41 is measured over the
declared base..tip range `0e5805a1..71851d63` instead of the subject grep; every commit in that
range that does not match `^round-41` is named separately so the ranges can be compared.

Definitions used, stated so the numbers can be argued with:
  * "added bytes" = sum of the sizes of blobs introduced by status `A`; modified and deleted
    content is NOT counted.  Modification/deletion counts are printed for context.
  * "net growth" = sum of blob sizes under the watched directories at the round's last commit
    minus the same sum at the round's first commit's parent (`git ls-tree -r -l`).  This is
    independent of diff-tree and includes adds, modifications and deletions.
  * "over 1 MB" = blob size > 1 048 576 bytes.

Cross-check: every added blob's size from `git cat-file --batch-check` is compared against the
size `git ls-tree -r -l <commit>` reports for the same path; a mismatch is a hard error.

Read-only: only `git log`, `git diff-tree`, `git cat-file`, `git ls-tree`, `git rev-list` are
run.  Nothing is written anywhere.

Usage: weight.py [--repo PATH] [--json PATH] [--rounds 35-41]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys

WAVES = ".ufo/waves/"
CORPUS = "corpus/"
BIG = 1_048_576  # 1 MiB; "over 1 MB" means strictly greater


def git(repo: str, *args: str) -> bytes:
    """Run a read-only git command and return raw stdout."""
    out = subprocess.run(
        ["git", "-C", repo, *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if out.returncode != 0:
        raise SystemExit(
            f"git {' '.join(args)} failed ({out.returncode}): "
            f"{out.stderr.decode('utf-8', 'replace').strip()}"
        )
    return out.stdout


def round_commits(repo: str, rnd: int) -> list[str]:
    """Commits whose subject starts with `round-<rnd>`, oldest first."""
    raw = git(repo, "log", "--format=%H", f"--grep=^round-{rnd}")
    return list(reversed(raw.decode().split()))


def range_commits(repo: str, base: str, tip: str) -> list[str]:
    """Commits in base..tip, oldest first."""
    raw = git(repo, "rev-list", "--reverse", f"{base}..{tip}")
    return raw.decode().split()


def subject(repo: str, sha: str) -> str:
    return git(repo, "log", "-1", "--format=%s", sha).decode("utf-8", "replace").strip()


def parent_of(repo: str, sha: str) -> str | None:
    parents = git(repo, "rev-list", "-1", "--parents", sha).decode().split()
    return parents[1] if len(parents) > 1 else None


def is_merge(repo: str, sha: str) -> bool:
    return len(git(repo, "rev-list", "-1", "--parents", sha).decode().split()) > 2


def diff_tree_added(repo: str, sha: str) -> tuple[dict[str, str], dict[str, int]]:
    """Return ({path: new_blob_sha} for status A, {status: count})."""
    raw = git(repo, "diff-tree", "-r", "-z", "--no-commit-id", sha)
    tok = raw.split(b"\0")
    added: dict[str, str] = {}
    counts: dict[str, int] = {}
    i = 0
    while i + 1 < len(tok):
        meta = tok[i].decode("utf-8", "surrogateescape")
        path = tok[i + 1].decode("utf-8", "surrogateescape")
        i += 2
        if not meta.startswith(":"):
            raise SystemExit(f"unparsable diff-tree record for {sha}: {meta!r}")
        fields = meta[1:].split(" ")
        if len(fields) < 5:
            raise SystemExit(f"short raw record for {sha}: {meta!r}")
        new_sha, status = fields[3], fields[4]
        status = status[0]
        counts[status] = counts.get(status, 0) + 1
        if status == "A":
            added[path] = new_sha
    return added, counts


def blob_sizes(repo: str, shas: list[str]) -> dict[str, int]:
    """Sizes for blob shas via one cat-file --batch-check process."""
    if not shas:
        return {}
    out = subprocess.run(
        ["git", "-C", repo, "cat-file", "--batch-check=%(objectname) %(objectsize)"],
        input=("\n".join(shas) + "\n").encode(),
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if out.returncode != 0:
        raise SystemExit(f"cat-file --batch-check failed: {out.stderr.decode('utf-8', 'replace')}")
    sizes: dict[str, int] = {}
    for line in out.stdout.decode().splitlines():
        parts = line.split()
        if len(parts) != 2:
            raise SystemExit(f"unexpected batch-check line: {line!r}")
        sizes[parts[0]] = int(parts[1])
    return sizes


def ls_tree_sizes(repo: str, commit: str | None, *paths: str) -> dict[str, int]:
    """{path: size} for blobs under `paths` at `commit` (empty when commit is None)."""
    if commit is None:
        return {}
    raw = git(repo, "ls-tree", "-r", "-l", "-z", commit, "--", *paths)
    sizes: dict[str, int] = {}
    for rec in raw.split(b"\0"):
        if not rec:
            continue
        head, _, path = rec.partition(b"\t")
        fields = head.decode("utf-8", "surrogateescape").split()
        if len(fields) < 4 or fields[1] != "blob":
            continue
        sizes[path.decode("utf-8", "surrogateescape")] = int(fields[3])
    return sizes


def bucket(path: str) -> str:
    if path.startswith(WAVES):
        return "waves"
    if path.startswith(CORPUS):
        return "corpus"
    return "other"


def measure(repo: str, commits: list[str]) -> dict:
    """Aggregate added bytes and counts over `commits`; cross-check sizes against ls-tree."""
    per_commit: list[dict] = []
    statuses: dict[str, int] = {}
    for sha in commits:
        if is_merge(repo, sha):
            raise SystemExit(f"merge commit in the measured set, refusing to guess a parent: {sha}")
        added, counts = diff_tree_added(repo, sha)
        for k, v in counts.items():
            statuses[k] = statuses.get(k, 0) + v
        sizes = blob_sizes(repo, list(added.values()))
        tree = ls_tree_sizes(repo, sha, WAVES, CORPUS)
        agg = {"waves": 0, "corpus": 0, "other": 0}
        sized: dict[str, int] = {}
        for path, blob in added.items():
            size = sizes[blob]
            if path in tree and tree[path] != size:
                raise SystemExit(
                    f"size cross-check failed at {sha[:8]}:{path}: "
                    f"cat-file={size} ls-tree={tree[path]}"
                )
            agg[bucket(path)] += size
            sized[path] = size
        per_commit.append(
            {
                "sha": sha,
                "subject": subject(repo, sha),
                "added": sized,
                "added_files": {b: sum(1 for p in added if bucket(p) == b) for b in agg},
                "bytes": agg,
            }
        )
    return {"commits": per_commit, "statuses": statuses}


def net_growth(repo: str, start: str | None, end: str) -> dict:
    """Net blob-size change under the watched dirs from `start` (exclusive) to `end`."""
    before = ls_tree_sizes(repo, start, WAVES, CORPUS)
    after = ls_tree_sizes(repo, end, WAVES, CORPUS)

    def total(d: dict[str, int], prefix: str) -> int:
        if prefix == WAVES:
            return sum(v for k, v in d.items() if k.startswith(WAVES))
        return sum(v for k, v in d.items() if k.startswith(CORPUS))

    return {
        "waves": total(after, WAVES) - total(before, WAVES),
        "corpus": total(after, CORPUS) - total(before, CORPUS),
        "after_waves": total(after, WAVES),
        "after_corpus": total(after, CORPUS),
    }


def diff_tree_all(repo: str, sha: str) -> tuple[dict[str, tuple[str, str, str]], dict[str, int]]:
    """Return ({path: (status, old_sha, new_sha)}, {status: count}) for every change."""
    raw = git(repo, "diff-tree", "-r", "-z", "--no-commit-id", sha)
    tok = raw.split(b"\0")
    changes: dict[str, tuple[str, str, str]] = {}
    counts: dict[str, int] = {}
    i = 0
    while i + 1 < len(tok):
        meta = tok[i].decode("utf-8", "surrogateescape")
        path = tok[i + 1].decode("utf-8", "surrogateescape")
        i += 2
        fields = meta[1:].split(" ")
        new_sha, status = fields[3], fields[4][0]
        counts[status] = counts.get(status, 0) + 1
        if bucket(path) != "other":
            changes[path] = (status, fields[2], new_sha)
    return changes, counts


def closure(repo: str, base: str, tip: str) -> dict:
    """added - deleted + modified_delta must equal the ls-tree delta over base..tip."""
    commits = range_commits(repo, base, tip)
    per_dir = {"waves": 0, "corpus": 0}
    counts: dict[str, int] = {}
    for sha in commits:
        changes, c = diff_tree_all(repo, sha)
        for k, v in c.items():
            counts[k] = counts.get(k, 0) + v
        parts: list[tuple[str, str, int]] = []
        for path, (status, old, new) in changes.items():
            d = bucket(path)
            if status == "A":
                parts.append((d, new, +1))
            elif status == "D":
                parts.append((d, old, -1))
            elif status in ("M", "T"):
                parts.append((d, new, +1))
                parts.append((d, old, -1))
            else:
                raise SystemExit(f"unhandled status {status} at {sha[:8]}:{path}")
        sizes = blob_sizes(repo, [b for _, b, _ in parts])
        for d, blob, sign in parts:
            per_dir[d] += sign * sizes[blob]
    delta = net_growth(repo, base, tip)
    return {
        "commits": len(commits),
        "accounted_waves": per_dir["waves"],
        "accounted_corpus": per_dir["corpus"],
        "delta_waves": delta["waves"],
        "delta_corpus": delta["corpus"],
        "statuses": counts,
        "ok": per_dir["waves"] == delta["waves"] and per_dir["corpus"] == delta["corpus"],
    }


def run(repo: str, rounds: range, override: dict[int, tuple[str, str]]) -> dict:
    result: dict = {"repo": repo, "rounds": {}}
    for rnd in rounds:
        if rnd in override:
            base, tip = override[rnd]
            commits = range_commits(repo, base, tip)
            extra = [c for c in commits if not subject(repo, c).startswith(f"round-{rnd}")]
            start = base
            mode = f"range {base[:8]}..{tip[:8]}"
        else:
            commits = round_commits(repo, rnd)
            if not commits:
                raise SystemExit(f"no commits matched ^round-{rnd}")
            extra = []
            start = parent_of(repo, commits[0])
            mode = f"grep ^round-{rnd}"
        data = measure(repo, commits)
        growth = net_growth(repo, start, commits[-1])
        agg = {b: sum(c["bytes"][b] for c in data["commits"]) for b in ("waves", "corpus", "other")}
        files = {b: sum(c["added_files"][b] for c in data["commits"]) for b in ("waves", "corpus", "other")}
        grep_only = None
        if extra:
            # A range basis can swallow commits that belong to another round; name their weight
            # separately so no byte is silently counted twice.
            matching = [c for c in commits if c not in extra]
            sub = measure(repo, matching)
            grep_only = {
                "commit_count": len(matching),
                "bytes": {b: sum(c["bytes"][b] for c in sub["commits"]) for b in ("waves", "corpus", "other")},
                "files": {b: sum(c["added_files"][b] for c in sub["commits"]) for b in ("waves", "corpus", "other")},
            }
        large = []
        for c in data["commits"]:
            for path, size in c["added"].items():
                if size > BIG:
                    large.append({"path": path, "size": size,
                                  "commit": c["sha"], "subject": c["subject"]})
        result["rounds"][str(rnd)] = {
            "mode": mode,
            "commits": data["commits"],
            "commit_count": len(commits),
            "non_matching_commits": [{"sha": s, "subject": subject(repo, s),
                                      "bytes": next(c["bytes"] for c in data["commits"] if c["sha"] == s)}
                                     for s in extra],
            "statuses": data["statuses"],
            "bytes": agg,
            "files": files,
            "total_bytes": agg["waves"] + agg["corpus"] + agg["other"],
            "net": growth,
            "grep_only": grep_only,
            "large": large,
        }
    return result


def fmt_bytes(n: int) -> str:
    if abs(n) >= 1_048_576:
        return f"{n / 1_048_576:.2f} MiB"
    if abs(n) >= 1024:
        return f"{n / 1024:.1f} KiB"
    return f"{n} B"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/tsukuroi-shokunin")
    ap.add_argument("--rounds", default="35-41", help="inclusive range, e.g. 35-41")
    ap.add_argument("--json", default="", help="write the full data as JSON here")
    args = ap.parse_args()

    lo, _, hi = args.rounds.partition("-")
    rounds = range(int(lo), int(hi or lo) + 1)
    # Round 41 is measured over its declared base..tip range, as the item specifies.
    override = {41: ("0e5805a1f149bd2ed9fe0db2e0a832afb034a835",
                     "71851d636ab1bffaf8fee5016617c88878a666f1")}
    data = run(args.repo, rounds, override)

    print("| round | basis | commits | added files (waves/corpus) | .ufo/waves added | corpus added | other added | total added | net growth waves+corpus | added blobs >1 MiB |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for rnd, r in data["rounds"].items():
        print(
            "| {rnd} | {mode} | {n} | {fw}/{fc} | {w} | {c} | {o} | {t} | {net} | {big} |".format(
                rnd=rnd,
                mode=r["mode"],
                n=r["commit_count"],
                fw=r["files"]["waves"],
                fc=r["files"]["corpus"],
                w=f"{r['bytes']['waves']:,}",
                c=f"{r['bytes']['corpus']:,}",
                o=f"{r['bytes']['other']:,}",
                t=f"{r['total_bytes']:,}",
                net=f"{r['net']['waves'] + r['net']['corpus']:,}",
                big=len(r["large"]),
            )
        )

    print()
    print("Watched total (rounds {}-{}): .ufo/waves {} added bytes in {} files; corpus {} added bytes in {} files.".format(
        lo, hi,
        f"{sum(r['bytes']['waves'] for r in data['rounds'].values()):,}",
        sum(r["files"]["waves"] for r in data["rounds"].values()),
        f"{sum(r['bytes']['corpus'] for r in data['rounds'].values()):,}",
        sum(r["files"]["corpus"] for r in data["rounds"].values()),
    ))
    print("diff statuses across all measured commits (A = counted above): " +
          ", ".join(f"{k}={v}" for k, v in sorted(
              {s: sum(r["statuses"].get(s, 0) for r in data["rounds"].values())
               for s in {k for r in data["rounds"].values() for k in r["statuses"]}}.items())))
    print("size cross-check: every added blob compared with ls-tree -r -l at its commit, 0 mismatches.")

    for rnd, r in data["rounds"].items():
        for x in r["non_matching_commits"]:
            print(f"note: round-{rnd} {r['mode']} contains non-round-{rnd} commit {x['sha'][:8]} "
                  f"({x['subject'][:60]}): waves={x['bytes']['waves']:,} corpus={x['bytes']['corpus']:,} "
                  f"other={x['bytes']['other']:,}")
        g = r["grep_only"]
        if g:
            print(f"note: round-{rnd} subject-grep only ({g['commit_count']} commits, the range extras "
                  f"removed): waves={g['bytes']['waves']:,} in {g['files']['waves']} files, "
                  f"corpus={g['bytes']['corpus']:,} in {g['files']['corpus']} files, "
                  f"other={g['bytes']['other']:,}")

    # Every commit counted once, so a range basis that overlaps another round cannot inflate
    # the headline number.
    seen: dict[str, dict] = {}
    for r in data["rounds"].values():
        for c in r["commits"]:
            seen.setdefault(c["sha"], c)
    print("distinct-commit total (each commit counted once): .ufo/waves {} bytes in {} files, "
          "corpus {} bytes in {} files, other {} bytes, {} commits".format(
              f"{sum(c['bytes']['waves'] for c in seen.values()):,}",
              sum(c["added_files"]["waves"] for c in seen.values()),
              f"{sum(c['bytes']['corpus'] for c in seen.values()):,}",
              sum(c["added_files"]["corpus"] for c in seen.values()),
              f"{sum(c['bytes']['other'] for c in seen.values()):,}",
              len(seen),
          ))

    # Independent closure: over the whole window, added - deleted + modified_delta must equal
    # the ls-tree size delta.  This does not use the per-round diff-tree additions at all.
    win_base = parent_of(args.repo, round_commits(args.repo, int(lo))[0])
    win_tip = override[int(hi)][1] if int(hi) in override else round_commits(args.repo, int(hi))[-1]
    cl = closure(args.repo, win_base, win_tip)
    print(f"closure over {win_base[:8]}..{win_tip[:8]} ({cl['commits']} commits): "
          f"added-deleted+modified waves={cl['accounted_waves']:,} corpus={cl['accounted_corpus']:,}; "
          f"ls-tree delta waves={cl['delta_waves']:,} corpus={cl['delta_corpus']:,} -> "
          f"{'OK' if cl['ok'] else 'MISMATCH'}")
    unlabelled = [c for c in range_commits(args.repo, win_base, win_tip)
                  if c not in seen]
    for sha in unlabelled:
        print(f"note: {sha[:8]} inside the window carries no round label: {subject(args.repo, sha)[:70]}")

    print()
    print("| round | watched added | added in blobs >1 MiB | added outside them | >1 MiB share |")
    print("|---|---|---|---|---|")
    for rnd, r in data["rounds"].items():
        watched = r["bytes"]["waves"] + r["bytes"]["corpus"]
        big = sum(b["size"] for b in r["large"] if bucket(b["path"]) != "other")
        print("| {} | {:,} | {:,} | {:,} | {:.0%} |".format(
            rnd, watched, big, watched - big, (big / watched) if watched else 0.0))

    allbig = [(rnd, b) for rnd, r in data["rounds"].items() for b in r["large"]]
    print()
    if allbig:
        print("Added blobs over 1 MiB (1 048 576 bytes):")
        for rnd, b in sorted(allbig, key=lambda x: -x[1]["size"]):
            where = "" if bucket(b["path"]) == "other" else f" [{bucket(b['path'])}]"
            print(f"  round-{rnd} {b['size']:,} B ({fmt_bytes(b['size'])}) {b['path']}{where} in {b['commit'][:8]}")
        outside = [(rnd, b) for rnd, b in allbig if bucket(b["path"]) == "other"]
        print(f"  of these, {len(outside)} lie outside .ufo/waves and corpus/")
    else:
        print("Added blobs over 1 MiB: none.")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=1, sort_keys=True)
        print(f"json written: {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
