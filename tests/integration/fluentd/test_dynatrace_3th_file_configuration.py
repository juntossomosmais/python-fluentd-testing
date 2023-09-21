import pytest

from python_fluentd_testing.fluentd_evaluator import FluentdEvaluator
from tests.resources.support import absolute_path_fluentd_output_file
from tests.resources.support import try_to_remove_key_otherwise_return_it


@pytest.fixture
def setup_fluentd_scenario_3():
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluent-dynatrace-output-3.log")
    with FluentdEvaluator(
        "fluent-dynatrace-3.conf", folder_location, abs_file_path, 24232
    ).initialize_fluent_daemon() as f:
        yield f


def test_should_emit_and_transform_content_and_body_keys_to_send_to_dynatrace(setup_fluentd_scenario_3):
    # Arrange
    sample_stream_payload = [
        {
            "log_id": "90020221124231024915274964892613219266671587159978278962",
            "data": {
                "date": "2022-11-24T23:10:23.560Z",
                "type": "fp",
                "description": "Wrong email or password.",
                "connection": "jsm-main-including-migrations",
                "connection_id": "con_DtzeqpeWHFrePk99",
                "client_id": "DMx4w5HbYCCWzAXRxZmK2pPJMyXzYPjx",
                "client_name": "Loja Virtual",
                "ip": "2804:14d:1a87:cf49::9311",
                "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
                "details": {
                    "error": {"message": "Wrong email or password."},
                    "request": {
                        "method": "requestOptions",
                        "path": "requestOptions",
                    },
                    "response": {
                        "body": "httpResponseBody",
                        "statusCode": "httpResponseStatusCode",
                    },
                },
                "user_id": "auth0|45f28abf-e4d6-4001-a29a-0a00a38e87b2",
                "user_name": "cleverson.purkot@gmail.com",
                "strategy": "auth0",
                "strategy_type": "database",
                "log_id": "90020221124231024915274964892613219266671587159978278962",
            },
        }
    ]
    # Act
    result = setup_fluentd_scenario_3.emit_it_through_http_post_and_get_computed_result(sample_stream_payload)
    # Assert
    cleaned_result = try_to_remove_key_otherwise_return_it(result, "tag")
    # https://www.dynatrace.com/support/help/dynatrace-api/environment-api/log-monitoring-v2/post-ingest-logs
    # Content. If the content key is not set, the whole JSON is parsed as the content.
    auth0_event = sample_stream_payload[0]["data"]
    expected_namespace = f'{auth0_event["strategy"]}|{auth0_event["strategy_type"]}|{auth0_event["connection"]}'
    assert cleaned_result == {
        "content": "Wrong email or password.",
        "body": {
            "error": {"message": "Wrong email or password."},
            "request": {"method": "requestOptions", "path": "requestOptions"},
            "response": {"body": "httpResponseBody", "statusCode": "httpResponseStatusCode"},
        },
        "date": auth0_event["date"],
        "severity": "alert",
        "service.name": "auth0",
        "service.namespace": expected_namespace,
        "audit.action": auth0_event["type"],
        "audit.identity": auth0_event["user_id"],
        "audit.result": auth0_event["details"]["error"]["message"],
        "trace_id": sample_stream_payload[0]["log_id"],
        "log.source": "fluentd",
    }
