# Python Fluentd Testing

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Integration tests status](https://github.com/juntossomosmais/python-fluentd-testing/workflows/Integration%20tests/badge.svg)
![Lint rules status](https://github.com/juntossomosmais/python-fluentd-testing/workflows/Lint%20rules/badge.svg)

Tired of testing fluentd and wasting lots of your precious time with manual integration tests? How about the lag it causes to your machine?

Now you can easily test your configuration with this project!

## Using remote-interpreter

You can use `remote-interpreter` Docker Compose service as a remote interpreter. It's important that you use `python3` to execute your code.

## Run all the tests

Simply execute the following command:

    docker-compose up integration-tests

## Run lint evaluation locally

We have a service for this as well:

    docker-compose up lint

## Testing with your K8S

After you test your configuration, you can proceed to apply your setup to your production environment. Now if you are in a phase where you would like to see if your configuration run in your real environment, like K8S, then you need to do a full manual process.

We did in the past and [here](/tests/resources/k8s-lab/README.md) you can see our tutorial.

## Useful links

- [How to test Fluentd config in Ruby](https://knplabs.com/en/blog/how2tips-how-to-test-fluentd-config)
