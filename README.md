# Agent Skills

Reusable engineering workflows adapted from [Matt Pocock's skills](https://github.com/mattpocock/skills), based on upstream commit `49dd158d1076134a641b33efb035946536778336`. The upstream MIT copyright and Git history are preserved. This is an independent fork maintained by Cory Naegle; upstream has not endorsed these changes.

## Install once, use across projects

```bash
git clone https://github.com/corynaegle-ai/agent-skills.git
cd agent-skills
bash scripts/link-skills.sh --dry-run
bash scripts/link-skills.sh
```

Requires Python 3 and Git. The installer links six recommended skills into your user-level Codex and Claude Code folders, so every local project can use the same source. It preserves existing entries and stops on conflicts before writing. User-scope installation is per machine; remote agents need their own checkout/installation.

| Default skill | Purpose |
| --- | --- |
| [diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md) | Reproduce, test hypotheses, fix, and verify the original symptom |
| [domain-modeling](./skills/engineering/domain-modeling/SKILL.md) | Keep domain terms and architectural decisions consistent |
| [codebase-design](./skills/engineering/codebase-design/SKILL.md) | Concentrate complexity behind useful, testable interfaces |
| [retro](./skills/engineering/retro/SKILL.md) | Improve tools and instructions based on actual session failures |
| [to-tickets](./skills/engineering/to-tickets/SKILL.md) | Split authorized work into verifiable slices with dependencies |
| [writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md) | Write concise, discoverable agent instructions |

Add an optional skill with its dependencies:

```bash
bash scripts/link-skills.sh --skill improve-codebase-architecture
bash scripts/link-skills.sh --skill pr --skill code-review
```

Use `--agent codex` or `--agent claude` for one agent, `--all` for all promoted skills, or `--destination PATH` for an isolated installation. Experimental, misc, and deprecated skills are excluded. Configuration and supported plugin installation are described in [.agents/install-block.md](./.agents/install-block.md).

Update the shared source with `git pull --ff-only`. Symlinks use the new contents immediately; refresh or restart an agent if its skill list is cached. Re-run the installer for newly selected skills or dependencies. Keep the clone at a stable path. Do not install both links and the full plugin for the same agent.

## Project context

Skills provide shared procedures. Each project's `AGENTS.md`/`CLAUDE.md`, glossary, ADRs, tests, and issue tracker provide its own context. Debugging and design skills work without setup. For tracker-based planning, run `setup-matt-pocock-skills` in that project, or supply the existing tracker/local-file convention. Setup writes only to that project and is not run by the global installer.

Skills can be explicitly selected; model-invoked skills may also activate when their descriptions match the task. User-invoked skills retain their explicit-only policy. Installation makes skills available, not mandatory for every task. Shared skills preserve the user's existing authorization and project instructions.

## Changes from upstream

- Safe selective installation with dependency closure, dry-run, idempotence, and no destructive replacement.
- Review snapshots include committed, staged, unstaged, and non-ignored untracked changes without changing the checkout or index.
- Routine testing choices reuse existing authorization; interviews focus on unresolved material decisions.
- Parallel implementation is bounded, preserves dirty worktrees, and verifies the combined result before readiness or closure.
- Reviewer/research workers are leaves, with sequential fallbacks when delegation is unavailable.
- The full plugin has its own identity; inherited scheduled issue-management workflows are disabled by removal.

## Validation

```bash
npm run check
claude plugin validate . --strict
```

The first command needs Python 3 and Node/npm, with no npm dependency installation. On Node 22 or newer, `node --run check` works without npm. It checks packaging and metadata and runs isolated installer/Git snapshot tests. Structural and functional checks do not establish model effectiveness; validate behavioral changes against real project tasks.

## Reference

These split on one axis: who can invoke them. **User-invoked** skills are reachable only when you type them (e.g. `/grill-me`); their job is to orchestrate. **Model-invoked** skills can be invoked by you _or_ reached for automatically by the agent when the task fits; they hold the reusable discipline. A user-invoked skill may invoke model-invoked skills, but never another user-invoked one.

### Engineering

Skills I use daily for code work.

**User-invoked**

- **[ask-matt](./skills/engineering/ask-matt/SKILL.md)**: Ask which skill or flow fits your situation. A router over the user-invoked skills in this repo.
- **[grill-with-docs](./skills/engineering/grill-with-docs/SKILL.md)**: Grilling session that also builds your project's domain model, sharpening terminology and updating `GLOSSARY.md` and ADRs inline.
- **[triage](./skills/engineering/triage/SKILL.md)**: Move issues through a state machine of triage roles.
- **[improve-codebase-architecture](./skills/engineering/improve-codebase-architecture/SKILL.md)**: Scan a codebase for deepening opportunities, present them as a visual HTML report, then grill through whichever one you pick.
- **[setup-matt-pocock-skills](./skills/engineering/setup-matt-pocock-skills/SKILL.md)**: Configure this repo for the engineering skills (issue tracker, triage labels, domain doc layout). Run once per repo before using the other engineering skills.
- **[to-spec](./skills/engineering/to-spec/SKILL.md)**: Turn the current conversation into a spec and publish it to the issue tracker. No interview, just synthesizes what you've already discussed.
- **[to-tickets](./skills/engineering/to-tickets/SKILL.md)**: Break any plan, spec, or conversation into a set of tracer-bullet tickets, each declaring its blocking edges, written as text in a local file, or as native blocking links on a real tracker.
- **[implement](./skills/engineering/implement/SKILL.md)**: Build the work described by a spec or set of tickets, driving `/tdd` at established test boundaries and closing out with `/code-review` before committing.
- **[implement-spec](./skills/engineering/implement-spec/SKILL.md)**: Implement a whole spec on one integration branch. Works the tickets as a task graph, running implementer subagents across the ready frontier with bounded concurrency and combined verification, then closes out with `/code-review`.
- **[wayfinder](./skills/engineering/wayfinder/SKILL.md)**: Plan a huge chunk of work, more than one agent session can hold, as a shared map of decision tickets on the issue tracker, and resolve them one at a time until the way to the destination is clear.
- **[retro](./skills/engineering/retro/SKILL.md)**: Suggest improvements to the coding agent's environment (navigation, automated checks, coding standards, steering files, tooling) after a session, most severe first.

**Model-invoked**

- **[prototype](./skills/engineering/prototype/SKILL.md)**: Build a throwaway prototype to answer a design question, either a single shareable HTML file for state/logic questions, or several radically different UI variations toggleable from one route.
- **[diagnosing-bugs](./skills/engineering/diagnosing-bugs/SKILL.md)**: Disciplined diagnosis loop for hard bugs and performance regressions: build a feedback loop that goes red on this bug → minimise → hypothesise → instrument → fix → regression-test.
- **[research](./skills/engineering/research/SKILL.md)**: Investigate a question against high-trust primary sources and capture the findings as a cited Markdown file in the repo, run as a background agent.
- **[tdd](./skills/engineering/tdd/SKILL.md)**: Test-driven development with a red-green-refactor loop. Builds features or fixes bugs one vertical slice at a time.
- **[domain-modeling](./skills/engineering/domain-modeling/SKILL.md)**: Actively build and sharpen a project's domain model: challenge terms against the glossary, stress-test with edge-case scenarios, and update `GLOSSARY.md` and ADRs inline.
- **[codebase-design](./skills/engineering/codebase-design/SKILL.md)**: Shared discipline and vocabulary for designing deep modules: a lot of behaviour behind a small interface, placed at a clean seam, testable through that interface.
- **[code-review](./skills/engineering/code-review/SKILL.md)**: Two-axis review of the diff since a fixed point: **Standards** (does it follow the repo's coding standards, plus a Fowler smell baseline?) and **Spec** (does it faithfully implement the originating issue/spec?), with independent leaf reviewers when available.
- **[pr](./skills/engineering/pr/SKILL.md)**: The shape a pull request body should take: a summary as the smallest visual that makes the change clear, before/after evidence that it works, and a merge-danger call (one-way or two-way door, plus blast radius).
- **[wizard](./skills/engineering/wizard/SKILL.md)**: Generate an interactive bash wizard that walks a human through steps only they can perform: provisioning infrastructure, setting up credentials or CI secrets, walking an unfamiliar third-party dashboard, or running a one-off migration or cutover.

### Productivity

General workflow tools, not code-specific.

**User-invoked**

- **[grill-me](./skills/productivity/grill-me/SKILL.md)**: Get relentlessly interviewed about a plan or design until material decisions are settled.
- **[handoff](./skills/productivity/handoff/SKILL.md)**: Compact the current conversation into a handoff document so another agent can continue the work.
- **[teach](./skills/productivity/teach/SKILL.md)**: Teach the user a new skill or concept over multiple sessions, using the current directory as a stateful teaching workspace.
- **[to-questionnaire](./skills/productivity/to-questionnaire/SKILL.md)**: Turn a decision you can't answer alone into a Markdown questionnaire for the one person who can, filled in async, or together over a meeting. It grills you about the send (who it's for, what you need back), not the subject.
- **[wait-what](./skills/productivity/wait-what/SKILL.md)**: Fire this the moment a message doesn't land. The agent re-pitches it with the context you're missing, in plain English, using your `GLOSSARY.md` vocabulary.

**Model-invoked**

- **[grilling](./skills/productivity/grilling/SKILL.md)**: Interview the user relentlessly about a plan, decision, or idea until material decisions are settled. The reusable interview primitive behind `grill-me`, `grill-with-docs`, `triage`, `wayfinder` and `improve-codebase-architecture`.
- **[writing-for-agents](./skills/productivity/writing-for-agents/SKILL.md)**: Writing documents for agents: skills, AGENTS.md/CLAUDE.md, and any doc an agent reaches by a pointer.
