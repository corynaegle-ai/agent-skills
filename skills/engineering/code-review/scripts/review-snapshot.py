#!/usr/bin/env python3
"""Capture a private, stable Git review bundle without changing the source checkout."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def git(repo, *args):
    # git diff can refresh stat data even with optional locks disabled.
    result = subprocess.run(
        ["git", "--no-optional-locks", "--no-pager", "-c", "diff.autoRefreshIndex=false", *args],
        cwd=repo, capture_output=True,
    )
    if result.returncode:
        raise ValueError(result.stderr.decode(errors="replace").strip())
    return result.stdout


def capture(repo, base, scope, paths):
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    requested = git(repo, "rev-parse", "--verify", base + "^{commit}").decode().strip()
    merge_base = git(repo, "merge-base", requested, head).decode().strip()
    diff_args = ("diff", "--binary", "--no-ext-diff", "--no-textconv", "--submodule=short")
    artifacts = {
        "committed.patch": git(repo, *diff_args, merge_base, head, "--", *paths),
        "commits.txt": git(repo, "log", "--oneline", merge_base + ".." + head, "--", *paths),
    }
    untracked = []
    if scope == "worktree":
        artifacts["staged.patch"] = git(repo, *diff_args, "--cached", head, "--", *paths)
        artifacts["unstaged.patch"] = git(repo, *diff_args, "--", *paths)
        artifacts["combined.patch"] = git(repo, *diff_args, merge_base, "--", *paths)
        artifacts["status.txt"] = git(repo, "status", "--short", "--untracked-files=all", "--", *paths)
        raw = git(repo, "ls-files", "--others", "--exclude-standard", "-z", "--", *paths)
        for value in raw.split(b"\0"):
            if not value:
                continue
            name = os.fsdecode(value)
            path = repo / name
            # Review symlinks as links, never by reading their targets.
            if path.is_symlink():
                kind, content = "symlink", os.fsencode(os.readlink(path))
            elif path.is_file():
                kind, content = "file", path.read_bytes()
            else:
                raise ValueError("Unsupported untracked file type: " + name)
            artifact = "untracked/" + str(len(untracked))
            artifacts[artifact] = content
            untracked.append({"path": name, "kind": kind, "artifact": artifact})
    metadata = {
        "scope": scope, "requested_base": requested, "merge_base": merge_base,
        "head": head, "paths": paths, "untracked": untracked,
        "sha256": {name: hashlib.sha256(data).hexdigest() for name, data in artifacts.items()},
    }
    return artifacts, metadata


def snapshot(base="HEAD", scope="worktree", paths=None, output=None, cwd=None):
    repo = Path(os.fsdecode(git(cwd or Path.cwd(), "rev-parse", "--show-toplevel")).strip())
    paths = paths or []
    first = capture(repo, base, scope, paths)
    if capture(repo, base, scope, paths) != first:
        raise ValueError("Checkout changed during capture; retry after the other writer finishes")
    artifacts, metadata = first
    if output:
        output = Path(output).expanduser().absolute()
        resolved = output.resolve()
        if resolved == repo or repo in resolved.parents:
            raise ValueError("Review output must be outside the source repository")
        output.mkdir(mode=0o700, parents=True, exist_ok=False)
    else:
        output = Path(tempfile.mkdtemp(prefix="agent-review-"))
    for name, data in artifacts.items():
        target = output / name
        target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        with target.open("xb") as stream:
            os.chmod(target, 0o600)
            stream.write(data)
    summary = output / "summary.json"
    summary.write_text(json.dumps(metadata, indent=2) + "\n")
    summary.chmod(0o600)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD", help="Branch, commit or tag; defaults to HEAD")
    parser.add_argument("--scope", choices=("worktree", "branch"), default="worktree")
    parser.add_argument("--path", action="append", default=[], help="Root-relative Git pathspec; repeat to scope")
    parser.add_argument("--output", type=Path, help="New private output directory outside the repo")
    args = parser.parse_args()
    print(snapshot(args.base, args.scope, args.path, args.output))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
