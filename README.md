# Python Fluentd Testing

Tired of testing fluentd and wasting lots of your precious time with manual integration tests? How about the lag it causes to your machine?

Now you can easily test your configuration with this project!

## Using remote-interpreter

You can use `remote-interpreter` Docker Compose service as a remote interpreter. It's important that you use `python3` to execute your code.

## Run all the tests

Simply execute the following command:

    docker-compose up integration-tests

## Testing with your K8S

After you test your configuration, you can proceed to apply your setup to your production environment. Now if you are in a phase where you would like to see if your configuration run in your real environment, like K8S, then you need to do a full manual process.

We did in the past and [here](/tests/resources/k8s-lab/README.md) you can see our tutorial.

## Useful links

- [How to test Fluentd config in Ruby](https://knplabs.com/en/blog/how2tips-how-to-test-fluentd-config)
