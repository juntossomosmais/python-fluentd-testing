import pytest

from python_fluentd_testing.fluentd_evaluator import FluentdEvaluator
from tests.resources.support import absolute_path_fluentd_output_file


@pytest.fixture
def setup_fluentd_scenario_json_with_more_than_xxx_bites():
    folder_location, abs_file_path = absolute_path_fluentd_output_file(
        "fluentd-test-output-json-with-more-than-xxx-bites.log"
    )
    with FluentdEvaluator(
        "fluent-big-json.conf", folder_location, abs_file_path
    ).initialize_fluent_daemon() as f_evaluator:
        yield f_evaluator


def test_should_emit_logs_with_to_json_length_less_than_20(setup_fluentd_scenario_json_with_more_than_xxx_bites):
    small_log = {"log": "small text just for test"}
    long_log = {"log": "bit text just for test to make it more than 20"}

    setup_fluentd_scenario_json_with_more_than_xxx_bites.emit_it(small_log)
    emitted = setup_fluentd_scenario_json_with_more_than_xxx_bites.emit_it_and_get_computed_result(long_log)

    assert emitted["log"] == small_log["log"]
    assert emitted.get("must_be_deleted") is None
