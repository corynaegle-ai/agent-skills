#!/usr/bin/env python3
"""Link curated skills into user scope, preserving every existing installation."""

import argparse
import json
import os
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent


def catalog():
    skills = {}
    for bucket in ("engineering", "productivity"):
        for entry in sorted((REPO / "skills" / bucket).glob("*/SKILL.md")):
            name = entry.parent.name
            if name in skills:
                raise ValueError("Duplicate skill name: " + name)
            skills[name] = entry.parent.resolve()
    return skills


def select_skills(skills, requested, dependencies):
    selected, visiting = set(), set()

    def visit(name):
        if name not in skills:
            raise ValueError("Unknown promoted skill: " + name)
        if name in visiting:
            raise ValueError("Dependency cycle at " + name)
        if name in selected:
            return
        visiting.add(name)
        for dependency in dependencies.get(name, []):
            visit(dependency)
        visiting.remove(name)
        selected.add(name)

    for name in requested:
        visit(name)
    return sorted(selected)


def install(names, skills, destinations, dry_run=False):
    # Complete the preflight for every destination before creating any directory.
    plan, problems, resolved_destinations = [], [], set()
    for destination in destinations:
        destination = Path(os.path.abspath(destination.expanduser()))
        resolved = destination.resolve()
        if resolved in resolved_destinations:
            continue
        resolved_destinations.add(resolved)
        if resolved == REPO or REPO in resolved.parents:
            problems.append("Destination is inside the source repo: " + str(destination))
            continue
        if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
            problems.append("Destination must be a real directory: " + str(destination))
            continue
        for ancestor in destination.parents:
            if ancestor.exists() and not ancestor.is_dir():
                problems.append("Destination parent is not a directory: " + str(ancestor))
        for name in names:
            target, source = destination / name, skills[name]
            if target.is_symlink() and target.resolve() == source:
                plan.append(("unchanged", target, source, resolved))
            elif os.path.lexists(target):
                problems.append("Preserving existing entry: " + str(target))
            else:
                plan.append(("link", target, source, resolved))
    for destination in resolved_destinations:
        if any(destination in other.parents for other in resolved_destinations):
            problems.append("Installation destinations must not contain one another")
    if problems:
        raise ValueError("\n".join(problems) + "\nNo installation changes made.")
    for action, target, source, resolved in plan:
        if action == "link" and not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            if target.parent.is_symlink() or target.parent.resolve() != resolved:
                raise ValueError("Destination changed during installation: " + str(target.parent))
            # symlink() refuses any entry created by another writer after preflight.
            target.symlink_to(source, target_is_directory=True)
        label = "would link" if dry_run and action == "link" else action
        print(f"{label}: {target} -> {source}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--all", action="store_true", help="Install all promoted skills")
    selection.add_argument("--skill", action="append", help="Select a skill; repeat for several")
    parser.add_argument("--agent", choices=("codex", "claude", "both"), default="both")
    parser.add_argument("--destination", type=Path, help="Use one custom directory instead of user scope")
    parser.add_argument("--dry-run", action="store_true", help="Preflight and print without writing")
    args = parser.parse_args()
    skills = catalog()
    config = json.loads((REPO / "skills.json").read_text())
    requested = list(skills) if args.all else args.skill or config["recommended"]
    names = select_skills(skills, requested, config["dependencies"])
    if args.destination:
        destinations = [args.destination]
    else:
        destinations = []
        if args.agent in ("codex", "both"):
            destinations.append(Path.home() / ".agents" / "skills")
        if args.agent in ("claude", "both"):
            destinations.append(Path.home() / ".claude" / "skills")
    install(names, skills, destinations, args.dry_run)
    print(f"{'Selected' if args.dry_run else 'Available'}: {len(names)} skills per destination")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
