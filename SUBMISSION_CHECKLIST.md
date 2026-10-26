# Submission checklist

- [x] Local GenVM lint and SDK validation pass.
- [x] Standard typecheck passes with no diagnostics.
- [x] Direct tests pass, including forged leader outcome, unauthorized caller, malformed response, replay, invalid matrix, adaptive next-probe selection, and inconclusive handling (9 passed).
- [x] StudioNet pinned-runner compatibility probe passed (separate trivial contract only; not a ProbeNext live test).
- [ ] StudioNet deployment and live adaptive demonstration are complete; all writes are `FINALIZED` with execution `SUCCESS`.
- [ ] Deployed contract source matches the pinned public commit byte-for-byte.
- [ ] Public repository, pinned source, manifest, contract Explorer page, and key transaction links are verified while logged out.
- [ ] Portal note is under 1,000 characters and states that the outcome is based on caller-supplied hypotheses and observations.
