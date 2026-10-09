# Worker completion

Run `python -m unittest -v suite` from this directory. This fixture has no external services.

run_job signals entered, waits until release or the specified deadline, then returns the callback's result. If release never occurs, it raises TimeoutError without invoking the callback. Errors from the callback propagate to its caller. The default wait is bounded at five seconds. Keep production behavior intact while improving the tests.
