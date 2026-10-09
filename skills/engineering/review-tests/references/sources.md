# Research and design rationale

Researched 2026-10-09 against primary sources. The workflow is an adaptation of the guidance below for coding agents reviewing existing suites. These sources do not empirically validate this particular skill.

| Source | Relevant guidance | Adaptation in this skill |
| --- | --- | --- |
| [Google: Change-Detector Tests Considered Harmful](https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html), 2015 | Tests that mirror implementation changes add maintenance without independently establishing correctness. | Require a behavior and independent oracle; replace incidental source, shape, and choreography assertions. |
| [Google: Don't Put Logic in Tests](https://testing.googleblog.com/2014/07/testing-on-toilet-dont-put-logic-in.html), 2014 | Direct examples are easier to verify than complex calculations embedded in expectations. | Prefer known outcomes and justified properties over copies of the production algorithm. |
| [Google: Increase Test Fidelity By Avoiding Mocks](https://testing.googleblog.com/2024/02/increase-test-fidelity-by-avoiding-mocks.html), 2024 | Prefer real implementations, then fakes, then mocks, balancing fidelity against test size and reliability. | Trace which behavior remains real; use lightweight production components and isolate necessary external boundaries. |
| [Playwright: Best Practices](https://playwright.dev/docs/best-practices) | Check visible behavior, isolate tests, and use resilient locators and retrying assertions. | Replace source-string UI checks with rendered behavior and condition-based waits. |
| [pytest: Flaky tests](https://docs.pytest.org/en/stable/explanation/flaky.html) | Shared state, ordering, strict timing, and thread cleanup can cause unreliable results. | Inspect isolation and asynchronous cleanup, reproduce suspected ordering problems, and report limits honestly. |
| [Meta: Automated Unit Test Improvement using Large Language Models](https://arxiv.org/abs/2402.09171), 2024 | Generated tests pass through execution and measurable-improvement filters; plausible text alone is insufficient. | Execute repaired tests, inspect their actual assertions, and compare against the baseline. Coverage is a diagnostic aid rather than the sole acceptance gate. |
| [Meta: Introducing LLM-powered bug catchers](https://engineering.fb.com/2025/02/05/security/revolutionizing-software-testing-llm-powered-bug-catchers-meta-ach/), 2025 | Domain concerns guide fault generation, which guides tests that detect those faults. | Ask for a plausible regression and verify important repairs against that defect. |
| [Google: Mutation Testing](https://testing.googleblog.com/2021/04/mutation-testing.html), 2021 | Unproductive or equivalent mutants can encourage fragile tests; relevant surviving mutants are more useful than maximizing a score. | Use targeted counterexamples, inspect survivors, and preserve behavior-resilient tests. |
| [Stryker: Mutant states and metrics](https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/) | Killed, survived, uncovered, timeout, and invalid mutants represent different outcomes. | Record outcomes separately. This skill requires a relevant assertion/contract failure for semantic evidence; a tool's aggregate detected score can also include timeouts. |

## Agent-specific design choices

The inventory ledger prevents a pattern search or a small sample from being presented as a full audit. Tracing test inputs through the real entrypoint distinguishes useful boundary fakes from tests that validate their own setup. Independent behavior contracts prevent an agent from simply updating expectations to match a bug. The green/defect/failure/restoration/green sequence makes the claimed regression sensitivity reviewable.

Those are workflow design choices informed by the sources and actual test-review work. They are not promises that all surviving tests are non-brittle, that every mutation is meaningful, or that local evidence establishes live service or device acceptance.
