# Canonical installation

This fork is `corynaegle-ai/agent-skills`. Keep root installation instructions aligned with this file. Never direct users to install upstream when they intend to use the adapted skills.

## Editable shared installation

```bash
git clone https://github.com/corynaegle-ai/agent-skills.git
cd agent-skills
bash scripts/link-skills.sh --dry-run
bash scripts/link-skills.sh
```

The default links the six recommended skills into `~/.agents/skills` (Codex) and `~/.claude/skills` (Claude Code). Python 3 and Git are the only requirements. `git pull --ff-only` updates linked skills. Re-run the installer after adding selected skills or dependencies. `--agent codex` or `--agent claude` limits installation to one agent. `--destination PATH` uses a custom directory instead.

`--skill NAME` selects one skill and its dependencies; repeat it to select several. `--all` selects all promoted skills. Experimental, misc, and deprecated skills are excluded. Preflight checks every destination before writing, refuses existing unrelated entries, and preserves valid links from this clone. There is no replacement mode. Moving the clone requires relinking manually after removing only the links owned by the old clone.

## Optional full plugin

```bash
claude plugin marketplace add corynaegle-ai/agent-skills
claude plugin install corynaegle-agent-skills@corynaegle-ai
```

The plugin opts into all promoted skills. Use either shared links or a plugin for a given agent, avoiding duplicate skills. Plugin update behavior belongs to the host; this fork does not promise automatic updates across hosts.
