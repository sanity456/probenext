import json
import re


PROBLEM = "A community water pump intermittently loses pressure."
CAUSES = [
    {"id": "filter", "description": "The intake filter is obstructed."},
    {"id": "seal", "description": "A pressure seal is leaking."},
    {"id": "power", "description": "The motor supply is unstable."},
    {"id": "valve", "description": "The outlet valve is sticking."},
]
PROBES = [
    {"id": "screen", "description": "Run a basic flow and pressure screening test; positive means the intake or pressure path shows an abnormal result.",
     "outcomes": {"filter": "POSITIVE", "seal": "POSITIVE", "power": "NEGATIVE", "valve": "NEGATIVE"}},
    {"id": "intake", "description": "Inspect the intake filter for blockage; positive means visible obstruction.",
     "outcomes": {"filter": "POSITIVE", "seal": "NEGATIVE", "power": "NEGATIVE", "valve": "NEGATIVE"}},
    {"id": "pressure", "description": "Run a static pressure hold test; positive means pressure falls while pump is off.",
     "outcomes": {"filter": "NEGATIVE", "seal": "POSITIVE", "power": "NEGATIVE", "valve": "NEGATIVE"}},
    {"id": "supply", "description": "Measure voltage during pump operation; positive means voltage fluctuates outside spec.",
     "outcomes": {"filter": "NEGATIVE", "seal": "NEGATIVE", "power": "POSITIVE", "valve": "NEGATIVE"}},
    {"id": "valve-check", "description": "Cycle the outlet valve; positive means it catches during the cycle.",
     "outcomes": {"filter": "NEGATIVE", "seal": "NEGATIVE", "power": "NEGATIVE", "valve": "POSITIVE"}},
]
OBSERVATION = "The inspection found the intake mesh visibly clogged with sediment."
PROMPT = "Classify the recorded troubleshooting result for the specified test"


def open_case(probe, direct_vm, direct_alice, case_id="pump-1"):
    direct_vm.sender = direct_alice
    return probe.open_case(case_id, PROBLEM, json.dumps(CAUSES), json.dumps(PROBES))


def set_result_mock(direct_vm, result):
    direct_vm.mock_llm(rf".*{re.escape(PROMPT)}.*", json.dumps({"outcome": result}))


def test_selects_most_discriminating_probe_and_recomputes_after_result(probe, direct_vm, direct_alice):
    open_case(probe, direct_vm, direct_alice)
    case = probe.get_case(direct_alice, "pump-1")
    assert case["current_probe"] == "screen"
    assert case["remaining_causes"] == ["filter", "seal", "power", "valve"]
    set_result_mock(direct_vm, "POSITIVE")
    probe.record_result("pump-1", "screen", "The screening test found abnormal flow and pressure behavior.")
    case = probe.get_case(direct_alice, "pump-1")
    assert case["remaining_causes"] == ["filter", "seal"]
    assert case["current_probe"] == "intake"
    set_result_mock(direct_vm, "POSITIVE")
    probe.record_result("pump-1", "intake", OBSERVATION)
    case = probe.get_case(direct_alice, "pump-1")
    assert case["remaining_causes"] == ["filter"]
    assert case["state"] == "ONE_HYPOTHESIS_REMAINS"
    assert case["current_probe"] == ""


def test_ties_are_deterministic_and_only_current_probe_is_accepted(probe, direct_vm, direct_alice):
    open_case(probe, direct_vm, direct_alice)
    set_result_mock(direct_vm, "INCONCLUSIVE")
    probe.record_result("pump-1", "screen", "The screening result was obscured and inconclusive.")
    case = probe.get_case(direct_alice, "pump-1")
    assert case["remaining_causes"] == ["filter", "seal", "power", "valve"]
    assert case["current_probe"] == "intake"
    with direct_vm.expect_revert("probe_not_current"):
        probe.record_result("pump-1", "screen", "The same screening test is attempted a second time.")


def test_different_result_changes_next_probe_choice(probe, direct_vm, direct_alice):
    open_case(probe, direct_vm, direct_alice)
    set_result_mock(direct_vm, "NEGATIVE")
    probe.record_result("pump-1", "screen", "The screening test found stable flow and pressure.")
    case = probe.get_case(direct_alice, "pump-1")
    assert case["remaining_causes"] == ["power", "valve"]
    assert case["current_probe"] == "supply"


def test_only_case_owner_can_record(probe, direct_vm, direct_alice, direct_bob):
    open_case(probe, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("case_missing"):
        probe.record_result("pump-1", "screen", OBSERVATION)


def test_replay_and_closed_case_writes_are_rejected(probe, direct_vm, direct_alice):
    open_case(probe, direct_vm, direct_alice)
    set_result_mock(direct_vm, "POSITIVE")
    probe.record_result("pump-1", "screen", OBSERVATION)
    probe.record_result("pump-1", "intake", OBSERVATION)
    with direct_vm.expect_revert("case_not_active"):
        probe.record_result("pump-1", "pressure", "Attempt to continue after one hypothesis remains.")


def test_validator_rejects_forged_outcome_even_with_valid_shape(probe, direct_vm, direct_alice):
    open_case(probe, direct_vm, direct_alice)
    set_result_mock(direct_vm, "NEGATIVE")
    probe.record_result("pump-1", "screen", "The screening test found stable flow and pressure.")
    assert direct_vm.run_validator() is True
    assert direct_vm.run_validator(leader_result={"outcome": "POSITIVE"}) is False


def test_invalid_model_shape_fails_without_mutating_case(probe, direct_vm, direct_alice):
    open_case(probe, direct_vm, direct_alice)
    direct_vm.mock_llm(rf".*{re.escape(PROMPT)}.*", json.dumps({"outcome": "POSITIVE", "cause": "filter"}))
    with direct_vm.expect_revert("invalid_model_response"):
        probe.record_result("pump-1", "screen", OBSERVATION)
    case = probe.get_case(direct_alice, "pump-1")
    assert case["state"] == "ACTIVE"
    assert case["used_probes"] == []


def test_probe_matrix_must_cover_exactly_each_cause(probe, direct_vm, direct_alice):
    bad = [dict(PROBES[0], outcomes={"filter": "POSITIVE"})]
    with direct_vm.expect_revert("incomplete_probe_outcome_map"):
        probe.open_case("bad-map", PROBLEM, json.dumps(CAUSES), json.dumps(bad))
    assert probe.get_case(direct_alice, "bad-map") == {}


def test_repeated_case_id_is_rejected(probe, direct_vm, direct_alice):
    open_case(probe, direct_vm, direct_alice)
    with direct_vm.expect_revert("case_id_already_used"):
        probe.open_case("pump-1", PROBLEM, json.dumps(CAUSES), json.dumps(PROBES))
