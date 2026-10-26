# ProbeNext

ProbeNext is a reusable GenLayer contract for adaptive troubleshooting. A case owner registers a bounded set of possible causes and a set of tests with caller-defined expected positive/negative outcomes. GenLayer validators interpret each reported test result into a closed outcome. Deterministic code removes hypotheses contradicted by the result, then chooses the unused test whose outcomes split the remaining causes most evenly. A test is recorded once and only the current recommended test can be submitted.

## GenLayer's role and boundary

Validators interpret natural-language test output; ordinary code enforces the outcome map, candidate elimination, tie-breaking, replay protection, and lifecycle. This is an informational investigation aid. The user supplies the hypotheses, test definitions, expected outcome map, and result text; the contract cannot verify the test was performed or that these inputs are true. It does not diagnose, repair, or certify safety.

The adaptive set-splitting rule is distinct from PermitDecisionTree's traversal of a frozen binary authority tree. ProbeNext has no pre-authored branch tree: every turn recomputes the next test from the surviving hypotheses and remaining tests. It also differs from RepairDesk's volunteer selection and ChangePointWatch's cumulative signal monitoring.

## Interface

Writes: `open_case`, `record_result`

View: `get_case`

One deployment supports multiple owner-scoped cases. See `ARCHITECTURE.md`, `ORIGINALITY.md`, and `SECURITY.md` for comparisons and limits.

## StudioNet evidence

Deployed at `0xa8Ed75F155aEDD08296cE33478Ba344E785FCA5a`. The released source is pinned to commit `cd9ee9af0ed33f8a8d437607426fa81b89f0756b`; the deployment and live test transaction receipts, expected guard rejection, state readback, and source hash are recorded in [`STUDIONET_RELEASE_EVIDENCE.json`](STUDIONET_RELEASE_EVIDENCE.json).

## Local checks

```text
genvm-lint check contracts/probe_next.py
genvm-lint typecheck contracts/probe_next.py --strict
python -m pytest tests/direct -q -p no:cacheprovider
```

MIT licensed.
