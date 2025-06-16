import json

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


@pytest.fixture
def setup_fluentd_scenario_4():
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluentd-test-output-4.log")
    fluentd_evaluator = FluentdEvaluator("fluent-4.conf", folder_location, abs_file_path, 24227)
    with fluentd_evaluator.initialize_fluent_daemon() as f_evaluator:
        yield f_evaluator


@pytest.fixture
def setup_fluentd_scenario_5():
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluentd-test-output-5.log")
    fluentd_evaluator = FluentdEvaluator("fluent-5.conf", folder_location, abs_file_path, 24228)
    with fluentd_evaluator.initialize_fluent_daemon() as f_evaluator:
        yield f_evaluator


@pytest.fixture
def setup_fluentd_scenario_6():
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluentd-test-output-6.log")
    fluentd_evaluator = FluentdEvaluator("fluent-6.conf", folder_location, abs_file_path, 24229)
    with fluentd_evaluator.initialize_fluent_daemon() as f_evaluator:
        yield f_evaluator

@pytest.fixture
def setup_fluentd_scenario_9():
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluentd-test-output-9.log")
    fluentd_evaluator = FluentdEvaluator("fluent-9.conf", folder_location, abs_file_path, 24230)
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
        "kubernetes": {
            "container_name": "chumaco",
            "namespace_name": "qa",
        },
    }
    message_2 = {
        "levelname": "INFO",
        "name": "chumaco.services.bear",
        "message": "PRD LOREM IPSUM DOLOR SIT AMET",
        "kubernetes": {
            "container_name": "chumaco",
            "namespace_name": "production",
        },
    }

    setup_fluentd_scenario_3.emit_it(message_1)
    result = setup_fluentd_scenario_3.emit_it_and_get_computed_result(message_2)

    assert result.get("date") is not None
    assert result.get("tag") is not None

    same_as_message_2 = try_to_remove_key_otherwise_return_it(result, "date", "tag")
    assert message_2 == same_as_message_2


def test_should_emit_and_delete_some_keys(setup_fluentd_scenario_4):
    message = {
        "levelname": "INFO",
        "name": "chumaco.services.bear",
        "message": "QA LOREM IPSUM DOLOR SIT AMET",
        "kubernetes": {"container_name": "chumaco", "namespace_name": "qa", "something": "delete-me"},
    }

    result = setup_fluentd_scenario_4.emit_it_and_get_computed_result(message)

    assert result.get("date") is not None
    assert result.get("tag") is not None

    cleaned_result = try_to_remove_key_otherwise_return_it(result, "date", "tag")
    del message["kubernetes"]["something"]
    assert cleaned_result == message


def test_should_not_accept_health_check(setup_fluentd_scenario_5):
    message_1 = {
        "log": '{"levelname": "INFO", "asctime": "2020-04-24 19:00:49,878", "request_id": "646e161e-5f98-43a3-a369-693c0112999a", "name": "gunicorn.access", "message": "GET /healthcheck HTTP/1.1", "http_status": 200, "ip_address": "10.130.81.220", "response_length": "3", "referer": "-", "user_agent": "kube-probe/1.14+", "request_time": 0.000896, "date": "[24/Apr/2020:19:00:49 -0300]"}',
        "stream": "stderr",
        "docker": {"container_id": "b486c8e1725ae522953b6eb5df7ac0a3e0a8316912ab682f7804af6df2302ae9"},
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
        "@timestamp": "2020-04-24T22:00:50.742098210+00:00",
    }
    message_2 = {
        "log": '{"levelname": "INFO", "asctime": "2020-04-24 19:00:49,878", "request_id": "646e161e-5f98-43a3-a369-693c0112999a", "name": "gunicorn.access", "message": "POST /healthcheck HTTP/1.1", "http_status": 200, "ip_address": "10.130.81.220", "response_length": "3", "referer": "-", "user_agent": "kube-probe/1.14+", "request_time": 0.000896, "date": "[24/Apr/2020:19:00:49 -0300]"}',
        "stream": "stderr",
        "docker": {"container_id": "b486c8e1725ae522953b6eb5df7ac0a3e0a8316912ab682f7804af6df2302ae9"},
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
        "@timestamp": "2020-04-24T22:00:50.742098210+00:00",
    }

    setup_fluentd_scenario_5.emit_it(message_1)
    result = setup_fluentd_scenario_5.emit_it_and_get_computed_result(message_2)

    assert result.get("date") is not None
    assert result.get("tag") is not None

    cleaned_result = try_to_remove_key_otherwise_return_it(result, "date", "tag")

    message_2["application"] = json.loads(message_2["log"])
    del message_2["kubernetes"]["master_url"]
    del message_2["kubernetes"]["namespace_id"]
    assert cleaned_result == message_2


def test_should_accept_message_only_if_key_contains_certain_value(setup_fluentd_scenario_6):
    message_1 = {
        "log": '{"levelname": "INFO", "asctime": "2020-04-24 19:00:49,878", "request_id": "646e161e-5f98-43a3-a369-693c0112999a", "name": "gunicorn.access", "message": "POST /healthcheck HTTP/1.1", "http_status": 200, "ip_address": "10.130.81.220", "response_length": "3", "referer": "-", "user_agent": "kube-probe/1.14+", "request_time": 0.000896, "date": "[24/Apr/2020:19:00:49 -0300]"}',
        "stream": "stderr",
        "docker": {"container_id": "b486c8e1725ae522953b6eb5df7ac0a3e0a8316912ab682f7804af6df2302ae9"},
        "kubernetes": {
            "container_image": "quay.io/kubernetes-ingress-controller/nginx-ingress-controller:0.32.0",
            "namespace_name": "production",
            "pod_name": "chumaco-deployment-5bdd6d6d58-chq95",
            "pod_id": "ebe5ff7c-70ad-11ea-b1ce-02c121ebda79",
            "labels": {
                "app": "chumaco",
                "pod-template-hash": "5bdd6d6d58",
                "app_kubernetes_io/name": "ingress-nginx-public-apps-ingress",
            },
            "host": "ip-127-0-0-2.ec2.internal",
            "master_url": "https://127.0.0.1:443/api",
            "namespace_id": "c02f189a-9f2a-11e9-879d-0ad999a381fc",
        },
        "@timestamp": "2020-04-24T22:00:50.742098210+00:00",
    }
    message_2 = {
        "log": '{"levelname": "INFO", "asctime": "2020-04-24 19:00:49,878", "request_id": "646e161e-5f98-43a3-a369-693c0112999a", "name": "gunicorn.access", "message": "POST /healthcheck HTTP/1.1", "http_status": 200, "ip_address": "10.130.81.220", "response_length": "3", "referer": "-", "user_agent": "kube-probe/1.14+", "request_time": 0.000896, "date": "[24/Apr/2020:19:00:49 -0300]"}',
        "stream": "stderr",
        "docker": {"container_id": "b486c8e1725ae522953b6eb5df7ac0a3e0a8316912ab682f7804af6df2302ae9"},
        "kubernetes": {
            "container_image": "952838399835.dkr.ecr.us-east-1.amazonaws.com/yuntiandu:14752-a1ba5719e7ae1c32b0e2c8117884d6177ce2a18b",
            "namespace_name": "production",
            "pod_name": "chumaco-deployment-5bdd6d6d58-chq95",
            "pod_id": "ebe5ff7c-70ad-11ea-b1ce-02c121ebda79",
            "labels": {
                "app": "chumaco",
                "pod-template-hash": "5bdd6d6d58",
                "app_kubernetes_io/name": "ingress-nginx-public-apps-ingress",
            },
            "host": "ip-127-0-0-2.ec2.internal",
            "master_url": "https://127.0.0.1:443/api",
            "namespace_id": "c02f189a-9f2a-11e9-879d-0ad999a381fc",
        },
        "@timestamp": "2020-04-24T22:00:50.742098210+00:00",
    }
    message_3 = {
        "log": '{"levelname": "INFO", "asctime": "2020-04-24 19:00:49,878", "request_id": "646e161e-5f98-43a3-a369-693c0112999a", "name": "gunicorn.access", "message": "POST /healthcheck HTTP/1.1", "http_status": 200, "ip_address": "10.130.81.220", "response_length": "3", "referer": "-", "user_agent": "kube-probe/1.14+", "request_time": 0.000896, "date": "[24/Apr/2020:19:00:49 -0300]"}',
        "stream": "stderr",
        "docker": {"container_id": "b486c8e1725ae522953b6eb5df7ac0a3e0a8316912ab682f7804af6df2302ae9"},
        "kubernetes": {
            "container_image": "952838399835.dkr.ecr.us-east-1.amazonaws.com/yuntiandu:14752-a1ba5719e7ae1c32b0e2c8117884d6177ce2a18b",
            "namespace_name": "production",
            "pod_name": "chumaco-deployment-5bdd6d6d58-chq95",
            "pod_id": "ebe5ff7c-70ad-11ea-b1ce-02c121ebda79",
            "labels": {"app": "chumaco", "pod-template-hash": "5bdd6d6d58"},
            "host": "ip-127-0-0-2.ec2.internal",
            "master_url": "https://127.0.0.1:443/api",
            "namespace_id": "c02f189a-9f2a-11e9-879d-0ad999a381fc",
        },
        "@timestamp": "2020-04-24T22:00:50.742098210+00:00",
    }

    setup_fluentd_scenario_6.emit_it(message_1)
    setup_fluentd_scenario_6.emit_it(message_2)
    result = setup_fluentd_scenario_6.emit_it_and_get_computed_result(message_3)

    assert result.get("date") is not None
    assert result.get("tag") is not None

    cleaned_result = try_to_remove_key_otherwise_return_it(result, "date", "tag")

    message_3["application"] = json.loads(message_3["log"])
    del message_3["kubernetes"]["master_url"]
    del message_3["kubernetes"]["namespace_id"]
    assert cleaned_result == message_3

def test_should_emit_only_message_without_production_namespace(setup_fluentd_scenario_9):
    message_1 = {
        "levelname": "INFO",
        "name": "chumaco.services.bear",
        "message": "QA LOREM IPSUM DOLOR SIT AMET",
        "kubernetes": {
            "container_name": "chumaco",
            "namespace_name": "qa",
        },
    }
    message_2 = {
        "levelname": "INFO",
        "name": "chumaco.services.bear",
        "message": "PRD LOREM IPSUM DOLOR SIT AMET",
        "severity_number": 7,
        "kubernetes": {
            "container_name": "chumaco",
            "namespace_name": "production",
        },
    }

    setup_fluentd_scenario_9.emit_it(message_1)
    result = setup_fluentd_scenario_9.emit_it_and_get_computed_result(message_2)

    assert result.get("date") is not None
    assert result.get("tag") is not None

    same_as_message_1 = try_to_remove_key_otherwise_return_it(result, "date", "tag")
    assert message_1 == same_as_message_1
