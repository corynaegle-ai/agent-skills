## What it does

Audit existing tests for real production execution, independent assertions, meaningful behavior, and resilience to refactors and flakiness. Correct test defects by default and summarize every issue found, fixed, or still open. Honor findings-only requests.

## When to reach for it

Run `/review-tests` for a repository-wide test-quality audit, or scope it to a directory, test layer, or suspicious family. It can also be selected automatically when a request clearly asks for test-quality review. Use [tdd](tdd.md) to build a new feature test-first and [code-review](code-review.md) for a general change review.

## Common questions

**Does it ban mocks, snapshots, private access, or exact assertions?**

No. It checks what they establish. Protocol compatibility, durable recovery, safety settings, idempotency, and bounded work can justify precise checks. Replacements should leave the behavior under review real and expectations independently grounded.

**How does it check that a passing test has value?**

It identifies a plausible regression and verifies important repairs against a known bug or targeted production mutation, then restores the code and reruns. Invalid mutants and unrelated failures do not prove semantic coverage. A sample only supports claims about the defects actually tried.

**Will it silently weaken a failing test or change product behavior?**

No. It establishes the expected behavior from project requirements and contracts. It reports production bugs separately, makes source fixes only within the user's authorization, and names unresolved requirements or environment blockers.

**What does a whole-repository review mean?**

Every in-scope test file is accounted for, including standalone and optional suites. The report distinguishes files reviewed, checks executed, skipped tests, and incomplete work. It does not equate a clean search or coverage percentage with a complete audit.

**Are its evaluation fixtures covered by CI?**

Yes. The repository checks validate their manifest and run the original baselines in disposable copies. The fixtures deliberately contain weak tests and a production defect for an agent to find; baseline success only establishes runnable exercises. Evaluating an agent's repairs remains a separate behavioral evaluation described in the [evaluation guide](../../skills/engineering/review-tests/evals/README.md).

## It's working if

- Findings identify a test, an actual consequence, and a useful correction.
- Repaired tests call real code and reject independently defined wrong behavior.
- Meaningful protocol and safety guarantees survive the cleanup.
- The report accounts for the scope, validation evidence, remaining issues, and shared review context.

Read the [skill](../../skills/engineering/review-tests/SKILL.md) and its [research rationale](../../skills/engineering/review-tests/references/sources.md). Installation options are in the [root guide](../../README.md#install-once-use-across-projects).
