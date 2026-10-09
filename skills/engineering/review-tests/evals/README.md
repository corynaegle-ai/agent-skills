# Behavioral evaluation

These are intentionally imperfect miniature projects for evaluating the skill,
not production examples. The library's ordinary test runner does not directly
collect their `suite.py` files. Its integration checks validate the manifest and
run each original baseline in a disposable copy, using the counts declared in
`evals.json`. These checks run in CI through `npm run check`; they establish that
the evaluation inputs are complete and runnable, not model effectiveness.

Copy each fixture to its own fresh temporary directory. Give the reviewing agent
the skill, the corresponding prompt from `evals.json`, and only that fixture's
raw files. Keep the expectations out of the agent's review context. The third
case requests findings only and must preserve every fixture file.

Run each fixture with an available Python 3 interpreter, for example:

```bash
python3 -B -m unittest -v suite
```

Evaluate the resulting source, tests, report, commands, and failure evidence
against `expectations` after the review. Check actual effects and file hashes;
matching report wording is insufficient. Verify temporary mutations were
restored and changed tests still pass. Keep outputs outside the source fixture.

Record the agent/context and execution limits. One successful forward test is a
sanity check, not a model benchmark or proof that all future reviews will work.
