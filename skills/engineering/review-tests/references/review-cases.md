# Judgment cases

Use these distinctions to turn a suspicious pattern into a concrete finding. A pattern by itself is insufficient evidence.

## Independent expectations

**Weak:** stub a TLS context with `check_hostname=True`, inject it, then assert the same attribute is true. That assertion establishes the test's setup rather than production TLS policy.

**Stronger:** let production create the context, replace only the socket handshake, and observe the context actually used. Verify hostname checking, certificate verification, and the intended destination. A mutation that disables verification should fail the assertion.

A fixed expected value can be legitimate even when the fake supplied the input. For example, an external catalog fixture provides a malicious package; the real scanner must reject it and retain a safe neighboring package. The test asserts the production decision rather than echoing the fixture.

Avoid deriving the expected result from the same helper used by production. A known input/output pair or independent reference implementation can be useful. Property tests can cover many inputs when their invariants follow from the domain; copying the implementation into a property is still circular.

## Structural checks and actual contracts

**Weak:** search JavaScript for a button ID or `textContent`, or assert the complete serialized HTML/CSS string. Those checks can pass while the page is broken and fail after harmless refactors.

**Stronger:** navigate the actual page, inspect the untrusted preview, verify no injected element or script executes, exercise the acknowledgement control, and observe the approved installation or other durable effect. Keep downloads external to the test replaced while the real validation and persistence run.

An exact public wire format, a published function signature, or a serialized compatibility fixture may be the behavior under contract. Retain that precision when an actual consumer depends on it. Otherwise call the API to establish compatibility instead of reflecting on its shape.

Broad snapshots are candidates for focused assertions, not automatic deletions. Visual regression snapshots may intentionally test appearance. Review fixture provenance and meaningful differences; do not regenerate expectations from an unexplained failure.

## Mock calls and durable effects

**Weak:** replace the service under test, call its mock, and assert it was called. No relevant service logic executes.

**Stronger:** run the real service and check the returned result, saved state, emitted protocol message, or rejection before an effect. Use a temporary real database for transaction and restart behavior where practical. A public read plus reopen can establish persistence; direct storage inspection is justified when durability or integrity is itself the contract.

Keep exact call counts for guarantees such as one external send per idempotency key, no retry after an uncertain delivery, or bounded costly work. Pair a count with the outcome when possible. Ordering matters for transactions and protocols that require it, not for arbitrary internal helper sequences.

Private fault injection can be appropriate for exercising disk corruption, rollback, crash recovery, or hard-to-trigger external failures. Judge what the assertions observe and which behavior remains real, rather than banning all private access.

## Timing, isolation, and negative claims

**Weak:** sleep briefly, assert a thread is alive, and join without inspecting its result. The thread might have failed or not reached the operation yet.

**Stronger:** signal that the worker reached the relevant boundary, observe bounded completion behavior, release it in cleanup, and retrieve the result or exception. Ensure cleanup cannot hang forever. A controlled clock can move past the original lease while the actual renewal loop and store remain active.

Some elapsed time is part of the behavior: streaming PCM, timeout enforcement, rate limiting, and scheduler integration can need real time. Make the reason explicit and use a generous bound or an observed condition. A timeout alone is not proof that the intended guard ran.

For absence claims, first reach the state where the forbidden effect could occur. Verify rejection or cancellation has completed, then inspect the relevant effect boundary. Immediate absence before the worker starts proves little.

Avoid ambient network, locale, timezone, environment, fixed ports, shared directories, and developer profile assumptions. Keep live provider acceptance separate from deterministic local coverage. Do not bypass a version, credential, or security gate to run an optional test.
