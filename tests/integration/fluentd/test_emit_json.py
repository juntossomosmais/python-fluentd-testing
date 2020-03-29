import pytest
from python_fluentd_testing.fluentd_evaluator import FluentdEvaluator
from tests.resources.support import absolute_path_fluentd_output_file
from tests.resources.support import try_to_remove_key_otherwise_return_it


@pytest.fixture
def setup_fluentd_scenario_1():
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluentd-test-output-1.log")
    with FluentdEvaluator("fluent-1.conf", folder_location, abs_file_path).initialize_fluent_daemon() as f_evaluator:
        yield f_evaluator


@pytest.fixture
def setup_fluentd_scenario_2():
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluentd-test-output-2.log")
    fluentd_evaluator = FluentdEvaluator("fluent-2.conf", folder_location, abs_file_path, 24225)
    with fluentd_evaluator.initialize_fluent_daemon() as f_evaluator:
        yield f_evaluator


@pytest.fixture
def setup_fluentd_scenario_3():
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluentd-test-output-3.log")
    fluentd_evaluator = FluentdEvaluator("fluent-3.conf", folder_location, abs_file_path, 24226)
    with fluentd_evaluator.initialize_fluent_daemon() as f_evaluator:
        yield f_evaluator


def test_should_emit_and_check_if_log_matches(setup_fluentd_scenario_1):
    emitted = {"log": "jafar"}

    result = setup_fluentd_scenario_1.emit_it_and_get_computed_result(emitted)
    assert result["log"] == emitted["log"]


def test_should_emit_containing_log_key_with_str_value_as_json_and_check_if_log_matches(setup_fluentd_scenario_2):
    emitted = {
        "levelname": "INFO",
        "asctime": "2020-03-28 17:52:31,813",
        "request_id": "2b4d7072-2399-4da4-920f-bbd183b0ce8e",
        "name": "chumaco.services.bear",
        "message": "LOREM IPSUM DOLOR SIT AMET",
        "log": '{"levelname": "INFO", "asctime": "2020-03-28 17:52:31,813", "request_id": "2b4d7072-2399-4da4-920f-bbd183b0ce8e", "name": "chumaco.services.bear", "message": "Lorem ipsum dolor sit amet"}',
        "stream": "stderr",
        "docker": {"container_id": "6138ba46f0c57b7e5a58e6e173bb364a7ac7ee6a1d5550813d1d681696cd8744"},
        "kubernetes": {
            "container_name": "chumaco",
            "namespace_name": "production",
            "pod_name": "chumaco-deployment-5bdd6d6d58-chq95",
            "pod_id": "ebe5ff7c-70ad-11ea-b1ce-02c121ebda79",
            "labels": {"app": "chumaco", "pod-template-hash": "5bdd6d6d58"},
            "host": "ip-127-0-0-2.ec2.internal",
            "master_url": "https://127.0.0.1:443/api",
            "namespace_id": "c02f189a-9f2a-11e9-879d-0ad999a381fc",
        },
    }

    result = setup_fluentd_scenario_2.emit_it_and_get_computed_result(emitted)

    assert result.get("application") is not None
    assert result.get("date") is not None
    assert result.get("tag") is not None
    assert result["application"] == {
        "levelname": "INFO",
        "asctime": "2020-03-28 17:52:31,813",
        "request_id": "2b4d7072-2399-4da4-920f-bbd183b0ce8e",
        "name": "chumaco.services.bear",
        "message": "Lorem ipsum dolor sit amet",
    }

    same_as_emitted = try_to_remove_key_otherwise_return_it(result, "application", "date", "tag")
    assert emitted == same_as_emitted


def test_should_emit_only_message_with_production_namespace(setup_fluentd_scenario_3):
    message_1 = {
        "levelname": "INFO",
        "name": "chumaco.services.bear",
        "message": "QA LOREM IPSUM DOLOR SIT AMET",
        "kubernetes": {"container_name": "chumaco", "namespace_name": "qa",},
    }
    message_2 = {
        "levelname": "INFO",
        "name": "chumaco.services.bear",
        "message": "PRD LOREM IPSUM DOLOR SIT AMET",
        "kubernetes": {"container_name": "chumaco", "namespace_name": "production",},
    }

    setup_fluentd_scenario_3.emit_it(message_1)
    result = setup_fluentd_scenario_3.emit_it_and_get_computed_result(message_2)

    assert result.get("date") is not None
    assert result.get("tag") is not None

    same_as_message_2 = try_to_remove_key_otherwise_return_it(result, "date", "tag")
    assert message_2 == same_as_message_2
