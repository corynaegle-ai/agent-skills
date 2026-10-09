#!/usr/bin/env python3
"""Check curated packaging, invocation metadata, and local skill references."""

import ast
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import importlib.util

spec = importlib.util.spec_from_file_location("installer", ROOT / "scripts/install-skills.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def main():
    skills = installer.catalog()
    plugin = json.loads((ROOT / ".claude-plugin/plugin.json").read_text())
    packaged = [(ROOT / path).resolve() for path in plugin["skills"]]
    assert set(packaged) == set(skills.values()), "Plugin does not match promoted skills"
    assert len(packaged) == len(set(packaged)), "Duplicate packaged skill"
    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
    assert market["plugins"][0]["name"] == plugin["name"], "Marketplace name mismatch"
    config = json.loads((ROOT / "skills.json").read_text())
    for name in [*config["recommended"], *config["dependencies"]]:
        installer.select_skills(skills, [name], config["dependencies"])
    for name, directory in skills.items():
        skill = directory / "SKILL.md"
        body = skill.read_text()
        assert body.startswith("---\n"), f"{name}: missing frontmatter"
        front = body.split("---", 2)[1]
        assert re.search(r"^name: " + re.escape(name) + r"$", front, re.M), f"{name}: name mismatch"
        assert re.search(r"^description: .+", front, re.M), f"{name}: missing description"
        meta = (directory / "agents/openai.yaml").read_text()
        assert ("disable-model-invocation: true" in front) == ("allow_implicit_invocation: false" in meta), f"{name}: invocation mismatch"
        relative = directory.relative_to(ROOT)
        assert str(relative / "SKILL.md") in (ROOT / "README.md").read_text(), f"{name}: missing README reference"
        assert f"./{name}/SKILL.md" in (directory.parent / "README.md").read_text(), f"{name}: missing bucket reference"
        assert (ROOT / "docs" / directory.parent.name / (name + ".md")).is_file(), f"{name}: missing docs"
        prose = re.sub(r"```[^\n]*\n.*?```", "", body, flags=re.S)
        for link in re.findall(r"\]\(([^\s)#]+)(?:#[^\s)]*)?\)", prose):
            if not re.match(r"[a-z]+:", link):
                assert (directory / link).exists(), f"{name}: missing reference {link}"
    for path in [*ROOT.glob("scripts/*.py"), *ROOT.glob("tests/*.py"), *ROOT.glob("skills/**/scripts/*.py")]:
        ast.parse(path.read_text(), filename=str(path))
    for path in [*ROOT.glob("scripts/*.sh"), *ROOT.glob("skills/**/*.sh")]:
        subprocess.run(["bash", "-n", str(path)], check=True)
    print(f"Packaging, metadata, local references, Python/Bash syntax: {len(skills)} skills passed")


if __name__ == "__main__":
    main()
