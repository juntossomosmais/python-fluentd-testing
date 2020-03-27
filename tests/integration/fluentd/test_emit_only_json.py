import pytest
from python_fluentd_testing.fluentd_evaluator import FluentdEvaluator
from tests.resources.support import absolute_path_fluentd_output_file


@pytest.fixture
def setup_fluentd_test():
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluentd-test-output-1.log")
    with FluentdEvaluator("fluent-1.conf", folder_location, abs_file_path).initialize_fluent_daemon() as f_evaluator:
        yield f_evaluator


def test_should_emit_and_check_if_log_matches(setup_fluentd_test):
    emitted = {"log": "jafar", "tag": "jsm.something"}

    assert setup_fluentd_test.emit_it_and_check_if_matches_with(emitted)
