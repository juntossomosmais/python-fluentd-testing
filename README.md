# Python Fluentd Testing

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Integration tests status](https://github.com/juntossomosmais/python-fluentd-testing/workflows/Integration%20tests/badge.svg)

Tired of testing fluentd and wasting lots of your precious time with manual integration tests? How about the lag it causes to your machine?

Now you can easily test your configuration with this project!

## Using remote-interpreter

You can use `remote-interpreter` Docker Compose service as a remote interpreter. It's important that you use `python3` to execute your code.

## Running Fluentd through Docker

You can start a Fluentd daemon by running the following command:

    docker-compose run remote-interpreter fluentd -vv -c /fluentd/etc/fluent-dynatrace-1.conf

Then you can enter the container:

    docker exec -it python-fluentd-testing_remote-interpreter_run_ee7625b3648c bash

Finally emit what you want to test, let's say:

```shell
echo '{"content": "Emma Brown", "log.source": "cockatiel", "timestamp": "2022-11-21T16:15:40.0000", "severity": "error", "service.name": "power-environment-service", "service.namespace": "dev-762HNW", "custom.attribute": "Fine artist", "audit.action": "GB", "audit.identity": "AHJX83322418325012", "audit.result": "Gold", "service.version": "1.0.0", "trace_id": "07edac7f-887d-498f-ab87-ad97d3b875b2"}' | fluent-cat -p 24230 jsm.testing
```

## Run all the tests

Simply execute the following command:

    docker-compose up integration-tests

## Run lint evaluation locally

We have a service for this as well:

    docker-compose up lint

## Updating pipenv dependencies

If you update Pipfile, you can issue the following command to refresh your lock file:

    docker-compose run remote-interpreter pipenv update

## Testing with your K8S

After you test your configuration, you can proceed to apply your setup to your production environment. Now if you are in a phase where you would like to see if your configuration run in your real environment, like K8S, then you need to do a full manual process.

We did in the past and [here](/tests/resources/k8s-lab/README.md) you can see our tutorial.

## Useful links

- [How to test Fluentd config in Ruby](https://knplabs.com/en/blog/how2tips-how-to-test-fluentd-config)
