# ProbeNext architecture

## Protocol

1. An owner opens a case with 2–6 cause hypotheses and 1–8 tests. Each test maps every cause to an expected `POSITIVE` or `NEGATIVE` result.
2. Deterministic code calculates the maximum branch size for each unused test, selects the test minimizing the worst-case remaining set, and breaks ties by test ID. A test that cannot split the remaining hypotheses is not selected.
3. The owner submits the current test's observed text once. GenLayer classifies it as `POSITIVE`, `NEGATIVE`, or `INCONCLUSIVE`.
4. The validator independently reclassifies the same bounded input and requires exact equality of the closed outcome field.
5. Deterministic code filters out causes inconsistent with a positive/negative result. An inconclusive result removes none. It then selects the next test from the new candidate set or closes as `ONE_HYPOTHESIS_REMAINS`, `STALLED`, or `CONFLICT`.

## Invariants

Cases are owner-scoped and IDs are single-use. Only the owner may post results. The result must name exactly the selected test; each test ID is used at most once. The contract stores only a closed outcome and derived surviving-cause list, never free-form model prose. Test and hypothesis counts, text sizes, and history are bounded.

## Mechanism distinction

PermitDecisionTree traverses a fixed binary tree, asking one frozen question at each node. ProbeNext stores a bounded outcome matrix and recomputes a minimax split from the current surviving hypotheses after every result. No edge or next test is pre-authored as a branch. The mechanism is active test selection by worst-case hypothesis reduction, not a renamed static decision tree.
