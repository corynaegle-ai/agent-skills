---
name: grilling
description: Stress-test a plan or decision through focused questions when the user requests an interview or unresolved choices materially affect the work.
---

Map unresolved decisions as a design tree. Reuse decisions and authorization already supplied by the user; inspect files and tools for facts rather than asking the user to look them up. Delegate factual exploration only when available and permitted.

Ask a small round of independent questions, usually one to three, with a concise recommendation and the consequence of the choice. Use the host's question UI when available, otherwise numbered chat questions. Word questions so "yes" accepts the recommendation. Wait for answers before taking dependent actions; continue independent authorized work while waiting.

Resolve product, scope, and significant architecture choices with the user. Make routine reversible implementation choices yourself and state assumptions where they matter. Recompute the decision frontier after each answer and ask only questions that could change the result. Follow any user-requested interview depth or limit.

A planning-only interview ends with the agreed decisions and remaining uncertainties. It does not authorize implementation. If the user already requested implementation, continue that work after material decisions are settled without adding another generic confirmation gate. Stop asking when the remaining choices can be handled within existing instructions and authorization.
