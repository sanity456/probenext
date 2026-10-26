# ProbeNext originality review

## Mechanism fingerprint

Caller-defined cause/test outcome matrix -> deterministic minimax test choice -> validator-interpreted observation -> deterministic hypothesis elimination -> recompute the next test from the residual set.

The core invariant is that each accepted observation changes the remaining cause set, and the next test is selected from scratch by minimizing the largest possible residual group. The contract cannot return a diagnosis as fact; it reports only which caller-defined hypotheses remain consistent with submitted observations.

## Closest workspace matches

- PermitDecisionTree traverses a frozen acyclic binary tree with one semantic answer per node. ProbeNext has no tree edges; its next probe is recalculated by a deterministic worst-case partition score from live remaining causes and unused tests.
- RepairDesk derives volunteer skill masks and selects a team by set cover. ProbeNext selects no people or resources; it sequences diagnostic tests and prunes hypotheses.
- ChangePointWatch computes cumulative per-dimension change signals. ProbeNext does not maintain baselines or time-series scores; each test outcome eliminates rows from a finite cause/test matrix.

The algorithm, participant actions, stored state, and transition invariant differ from these contracts; the distinction is not based on naming or subject matter.
