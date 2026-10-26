# Security notes

- Case inputs, hypotheses, test definitions, outcome maps, and observations are public and caller-supplied. The contract cannot establish that a test was performed or that a hypothesis set is complete.
- Validators independently classify each result. The leader cannot store extra model-authored fields, a forged result, or an unsupported outcome.
- Strict bounds limit causes, tests, history, IDs, and input text. Unknown, contradictory, or malformed outcomes fail closed; `INCONCLUSIVE` leaves hypotheses unchanged.
- Only the case owner can submit results. Only the currently recommended unused probe is accepted, once.
- `ONE_HYPOTHESIS_REMAINS` means only that one declared candidate remains consistent with submitted inputs. It is not a factual diagnosis, professional advice, or a safety determination.
