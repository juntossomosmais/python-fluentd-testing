import json
from contextlib import contextmanager
from time import sleep

import requests

from python_fluentd_testing.utils import delete_all_log_files_contained_in_the_folder
from python_fluentd_testing.utils import execute_shell_command
from python_fluentd_testing.utils import execute_system_command_and_does_not_await_its_execution
from python_fluentd_testing.utils import number_of_lines
from python_fluentd_testing.utils import try_to_get_last_line_as_json


class EmitCommandCouldNotBeExecutedProperly(Exception):
    pass


class NoOutputCouldBeExtractedException(Exception):
    pass


class FluentdEvaluator:
    def __init__(self, config_file_location, folder_logs, output_file_name, forward_port=24224):
        self.config_file_location = config_file_location
        self.folder_logs = folder_logs
        self.output_file_name = output_file_name
        self.forward_port = forward_port
        delete_all_log_files_contained_in_the_folder(self.folder_logs)

    def emit_it_through_http_post_and_get_computed_result(
        self, fake_log_data: dict, tag="jsm.testing", number_of_entries_in_output=1
    ) -> dict:
        response = requests.post(f"http://localhost:{self.forward_port}/{tag}", json=fake_log_data)
        assert response.status_code == 200
        result = try_to_get_last_line_as_json(self.output_file_name)
        if not result:
            raise NoOutputCouldBeExtractedException
        assert number_of_lines(self.output_file_name) == number_of_entries_in_output
        return result

    def emit_it_and_get_computed_result(
        self, fake_log_data: dict, tag="jsm.testing", number_of_entries_in_output=1
    ) -> dict:
        self.emit_data_fluent_cat(fake_log_data, tag, self.forward_port)
        result = try_to_get_last_line_as_json(self.output_file_name)
        if not result:
            raise NoOutputCouldBeExtractedException
        assert number_of_lines(self.output_file_name) == number_of_entries_in_output
        return result

    def emit_it(self, fake_log_data: dict, tag="jsm.testing"):
        self.emit_data_fluent_cat(fake_log_data, tag, self.forward_port)

    @contextmanager
    def initialize_fluent_daemon(self):
        command = ["fluentd", "-v", "-c", f"/fluentd/etc/{self.config_file_location}"]
        with execute_system_command_and_does_not_await_its_execution(command):
            yield self

    @staticmethod
    def emit_data_fluent_cat(fake_log_data, tag, forward_port=24224):
        send_to_fluentd_as_text = json.dumps(fake_log_data)
        command = ["echo", f"'{send_to_fluentd_as_text}'", "|", "fluent-cat", "-p", str(forward_port), tag]
        stdout, stderr = execute_shell_command(command)
        # Give some time to commit the data
        sleep(1)
        stdout = stdout.decode()
        if stdout or stderr:
            raise EmitCommandCouldNotBeExecutedProperly(f"Command error: {command}")
        if stderr:
            raise EmitCommandCouldNotBeExecutedProperly(f"Command error: {command}")
