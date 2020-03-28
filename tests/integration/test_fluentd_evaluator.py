import re
from datetime import date

import pytest
from python_fluentd_testing.fluentd_evaluator import FluentdEvaluator
from python_fluentd_testing.utils import delete_all_log_files_contained_in_the_folder
from python_fluentd_testing.utils import erase_file_content
from python_fluentd_testing.utils import execute_system_command_and_does_not_await_its_execution
from python_fluentd_testing.utils import try_to_get_log_as_json
from tests.resources.support import absolute_path_fluentd_output_file


@pytest.fixture
def run_fluentd_1():
    command = ["fluentd", "-c", "/fluentd/etc/fluent-1.conf"]
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluentd-test-output-1.log")
    delete_all_log_files_contained_in_the_folder(folder_location)
    with execute_system_command_and_does_not_await_its_execution(command):
        erase_file_content(abs_file_path)
        yield abs_file_path


def test_should_emit_data(run_fluentd_1):
    abs_file_path = run_fluentd_1
    sample_fake_log = {"log": "jafar"}
    tag = "jsm.something"
    FluentdEvaluator.emit_data(sample_fake_log, tag)

    result = try_to_get_log_as_json(abs_file_path)
    assert result is not None
    assert result["log"] == sample_fake_log["log"]
    assert result["tag"] == tag
    assert bool(re.search(f"{str(date.today())}:\w{{2}}:\w{{2}}:\w{{2}}", result["date"]))
