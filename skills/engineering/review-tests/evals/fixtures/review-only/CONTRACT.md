# Idempotent delivery

Run `python -m unittest -v suite` from this directory. The live service test is gated and cannot run in this fixture.

Sender.send returns the provider receipt and emits at most one external send per key. Repeating a key returns its saved receipt. Payload version 1 is a public wire-format guarantee. Source layout and helper choreography are not public contracts. This evaluation requests findings only: preserve all files.
