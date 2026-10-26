# ProbeNext local audit

Status: local checks complete; not deployed or submission-ready yet.

Intended safeguards include owner-scoped cases, exact cause/probe matrix validation, closed semantic outcomes, independent leader/validator comparison, deterministic minimax tie-breaking, current-probe enforcement, replay protection, and bounded input/history.

Workspace comparison is recorded in `ORIGINALITY.md`. The contract produces a troubleshooting hypothesis workflow, not a diagnosis or safety instruction. Results depend on caller-supplied cause/probe mappings and observations.

Local results: GenVM lint and SDK validation pass (3 lint checks; 3 contract methods, including 2 writes); standard typecheck passes with 0 diagnostics; direct suite passes (9 tests). Cases cover adaptive minimax probe selection and reselection, deterministic ties, inconclusive observations, forged leader outcomes, malformed model results, owner isolation, current-probe/replay/closed-case rejection, and exact probe-matrix validation.

Three gates: technical readiness PASS for local source checks and the pinned-runner StudioNet compatibility probe; distinctiveness PASS against the closest workspace mechanisms; contract evidence readiness FAIL because ProbeNext itself has not been deployed or demonstrated live.

Runner compatibility probe (not ProbeNext): a separate minimal contract deployed on StudioNet; deploy and write receipts reached `FINALIZED` with leader execution `SUCCESS`, and a read returned `smoke-ok`. This confirms runner/network and CLI calldata compatibility only; it is not evidence for ProbeNext behavior.

Not checked: ProbeNext StudioNet execution, deployed-source equality, public repository accessibility, and Explorer/transaction evidence. This audit is not a submission-readiness or acceptance guarantee. Before live release, demonstrate adaptive reselection and replay rejection on StudioNet, require `FINALIZED` plus execution `SUCCESS`, verify the deployed source against the pinned public commit, and read back final state.
