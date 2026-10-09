---
name: code-review
description: "Review a branch, PR, or uncommitted work against repository standards and requested behavior. Includes staged, unstaged, and untracked changes for work in progress."
---

Review along two axes: **Standards** (repository conventions and regression risk) and **Spec** (the behavior the user requested). Report both separately so one passing axis cannot hide the other.

## Capture the review scope

Honor the user's base and scope. Work in progress defaults to `HEAD` and `worktree`. A branch or PR uses its target branch and `branch`. Establish the target from tracking or PR metadata; ask only if it cannot be determined. An implementation review uses the recorded task-start commit.

Run the bundled [snapshot helper](scripts/review-snapshot.py) from the project being reviewed, resolving the script from this skill's installed folder:

```bash
python3 <skill-folder>/scripts/review-snapshot.py --base <base> --scope <worktree-or-branch>
```

It prints a private temp directory containing pinned commit IDs, a committed patch, and the commit list. Worktree scope also captures staged and unstaged patches, the combined final diff, and non-ignored untracked contents. Review every relevant artifact, including staged changes later reversed in the worktree. Symlinks are captured as links. The checkout and index remain unchanged. Use repeated `--path <root-relative-pathspec>` arguments to limit the review to task-owned paths when unrelated work exists. Ignored files need separate explicit inspection if requested.

Both reviewers receive the same snapshot and `summary.json`. Review the frozen artifacts rather than recomputing a live diff. Consult surrounding source at the recorded revision where needed, and note any later source drift. Keep snapshots private and redact sensitive content in reports. A failed capture must be resolved before review. If every patch is empty and no untracked entries exist, report an empty scope rather than claiming a clean review.

The helper checks the capture twice and rejects changes between reads. Review changed submodule checkouts separately: the superproject patch records their pointers, not full nested diffs.

## Identify the requirements and standards

Use the user's acceptance criteria and supplied spec/issue first, then issue references in commits or a matching local spec under `docs/`, `specs/`, or `.scratch/`. Existing tracker configuration helps fetch issues but is not a prerequisite. If no requirements can be established, report "no spec available" and skip the Spec axis; ask only when missing context prevents a useful requested review.

Read documented standards, including `AGENTS.md`, `CLAUDE.md`, `CODING_STANDARDS.md`, and `CONTRIBUTING.md` when present. Respect applicable instructions and relevant ADRs.

On top of whatever the repo documents, the Standards axis always carries the **smell baseline** below: a fixed set of Fowler code smells (_Refactoring_, ch.3) that applies even when a repo documents nothing. Two rules bind it:

- **The repo overrides.** A documented repo standard always wins; where it endorses something the baseline would flag, suppress the smell.
- **Always a judgement call.** Each smell is a labelled heuristic ("possible Feature Envy"), never a hard violation. Like any standard here, skip anything tooling already enforces.

Each smell reads *what it is* → *how to fix*; match it against the diff:

- **Mysterious Name**: a function, variable, or type whose name doesn't reveal what it does or holds. → rename it; if no honest name comes, the design's murky.
- **Duplicated Code**: the same logic shape appears in more than one hunk or file in the change. → extract the shared shape, call it from both.
- **Feature Envy**: a method that reaches into another object's data more than its own. → move the method onto the data it envies.
- **Data Clumps**: the same few fields or params keep travelling together (a type wanting to be born). → bundle them into one type, pass that.
- **Primitive Obsession**: a primitive or string standing in for a domain concept that deserves its own type. → give the concept its own small type.
- **Repeated Switches**: the same `switch`/`if`-cascade on the same type recurs across the change. → replace with polymorphism, or one map both sites share.
- **Shotgun Surgery**: one logical change forces scattered edits across many files in the diff. → gather what changes together into one module.
- **Divergent Change**: one file or module is edited for several unrelated reasons. → split so each module changes for one reason.
- **Speculative Generality**: abstraction, parameters, or hooks added for needs the spec doesn't have. → delete it; inline back until a real need shows.
- **Message Chains**: long `a.b().c().d()` navigation the caller shouldn't depend on. → hide the walk behind one method on the first object.
- **Middle Man**: a class or function that mostly just delegates onward. → cut it, call the real target direct.
- **Refused Bequest**: a subclass or implementer that ignores or overrides most of what it inherits. → drop the inheritance, use composition.

## Review independently

When delegation is available and permitted, dispatch at most two independent reviewer subagents, one per axis. Both are leaf reviewers: give them the snapshot, sources, and their brief, and explicitly say "Perform this review directly. Do not invoke code-review or spawn agents." Otherwise perform the same briefs sequentially and disclose shared context.

- **Standards brief:** Find correctness/regression risks, documented-standard breaches, and relevant baseline smells. Cite the file, location, triggering scenario, consequence, and supporting rule. Separate actionable problems from optional stylistic judgments. Skip mechanically enforced style.
- **Spec brief:** Find missing or partial requirements, unintended behavior, and incorrect implementations. Cite the requirement and the affected file/location. Use concrete triggering scenarios and consequences, not hypothetical improvements.

Supply the frozen snapshot directory and `summary.json` to both reviewers. Reference requirements in full or by accessible path. Review requests alone do not authorize source edits.

## Report

Present the findings under `Standards` and `Spec`, preserving each axis's verdict. State the reviewed base, head, scope, and whether review was independent. Report checks actually run and material gaps. End with counts and the highest-impact finding within each axis. If no actionable findings exist, say so and identify remaining validation limits.
