from datetime import datetime
from uuid import uuid4

import pytest
from faker import Faker

from python_fluentd_testing.fluentd_evaluator import FluentdEvaluator
from tests.resources.support import absolute_path_fluentd_output_file


@pytest.fixture
def setup_fluentd_scenario_1():
    folder_location, abs_file_path = absolute_path_fluentd_output_file("fluent-dynatrace-output-1.log")
    with FluentdEvaluator(
        "fluent-dynatrace-1.conf", folder_location, abs_file_path, 24230
    ).initialize_fluent_daemon() as f:
        yield f


@pytest.mark.skip
def test_should_emit_to_dynatrace_and_file(setup_fluentd_scenario_1):
    # Arrange
    faker = Faker()
    emitted = {
        "content": faker.name(),
        "log.source": "cockatiel",
        "timestamp": datetime.now().isoformat(),
        "severity": "error",
        "service.name": f"{faker.slug()}-service",
        "service.namespace": f'dev-{faker.license_plate().replace(" ", "")}',
        "custom.attribute": faker.job(),
        "audit.action": faker.bank_country(),
        "audit.identity": faker.bban(),
        "audit.result": faker.color_name(),
        "service.version": "1.0.0",
        "trace_id": str(uuid4()),
    }
    # Act
    result = setup_fluentd_scenario_1.emit_it_and_get_computed_result(emitted)
    # Assert
    assert result["service.name"] == emitted["service.name"]
    assert result["timestamp"] == emitted["timestamp"]
