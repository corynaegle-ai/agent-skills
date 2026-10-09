# Agent Skills

This is an MIT-licensed adaptation of mattpocock/skills. Preserve upstream copyright, attribution, and history. Historical upstream decisions in `.out-of-scope/` and `.agents/adr/` describe upstream behavior; this fork's current instructions and tested behavior take precedence.

## Layout and packaging

Promoted skills live under `skills/engineering/` and `skills/productivity/`. The full plugin ships exactly those folders. `skills.json` defines the six recommended user-scope skills and dependency closure for selective installation. Experimental, misc, and deprecated buckets are not installed by the supported installer.

Every promoted skill must appear in the root README, its bucket README, `.claude-plugin/plugin.json`, and `docs/<bucket>/<name>.md`. Preserve invocation policy in both SKILL frontmatter and `agents/openai.yaml`. Update `ask-matt` when the workflow changes.

## Changes and validation

For skill behavior changes, update the corresponding human documentation. Follow `.agents/writing-docs.md`; installation wording lives in `.agents/install-block.md`. Keep prose concise and use no em-dashes in new prose.

Run `npm run check` before committing. After plugin manifest changes, also run `claude plugin validate . --strict` when the CLI is available. Functional tests run in temporary directories and must never modify the user's actual skills folders or credentials.

## Shared installation

`scripts/link-skills.sh` installs the recommended skills into user scope for Codex and Claude Code. Use `--dry-run` to preflight, `--skill NAME` for selected extras, `--all` for the full promoted set, or `--destination PATH` for an isolated install. Existing unrelated files, folders, and symlinks must be preserved. Use no destructive replacement mode.

## Scope and authorization

Use the target project's instructions, tests, glossary, ADRs, and issue tracker. Preserve existing user authorization and unrelated dirty work. Shared skills do not grant permission to publish issues, push, deploy, access production, or send messages beyond the user's task. Report local checks, CI, release/signing, deployment, and physical acceptance separately.

Delegation must be permitted by the active environment. Reviewer and implementer subagents are leaf workers; orchestrators enforce capacity. When delegation is unavailable, work sequentially and disclose shared review context.
