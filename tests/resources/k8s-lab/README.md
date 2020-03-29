# How to setup your K8S

## Deploying Elastic Search

Commands:

    kubectl create -f namespaces.yaml
    kubectl create -f elasticsearch-statefulset.yaml 

Warnings I saw issuing the command `kubectl get events -w -n kube-logging`:

```text
8s          Warning   ProvisioningFailed   persistentvolumeclaim/data-es-cluster-0   storageclass.storage.k8s.io "slow" not found
<unknown>   Warning   FailedScheduling     pod/es-cluster-0                          pod has unbound immediate PersistentVolumeClaims
34s         Normal    SuccessfulCreate     statefulset/es-cluster                    create Claim data-es-cluster-0 Pod es-cluster-0 in StatefulSet es-cluster success
34s         Normal    SuccessfulCreate     statefulset/es-cluster                    create Pod es-cluster-0 in StatefulSet es-cluster successful
```

Then I found the default storage class with the command `kubectl get storageclass -ALL`:

```text
NAME                 PROVISIONER          AGE
hostpath (default)   docker.io/hostpath   3d23h
```

Looking its details through `kubectl get storageclass hostpath -o yaml`:

```text
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  annotations:
    storageclass.kubernetes.io/is-default-class: "true"
  creationTimestamp: "2020-03-05T19:24:18Z"
  name: hostpath
  resourceVersion: "520"
  selfLink: /apis/storage.k8s.io/v1/storageclasses/hostpath
  uid: 5f67719f-50ce-42fe-8a8a-482d199aaacc
provisioner: docker.io/hostpath
reclaimPolicy: Delete
volumeBindingMode: Immediate
```

I simplified all the setup to have only one ES node, created `local-storage.yaml` file and cleaned up all the stuff I had created previously. Now, in order to this tutorial work properly, you should type the following:

    kubectl create -f kube-logging.yaml
    kubectl create -f local-storage.yaml
    kubectl create -f elasticsearch-statefulset.yaml 

You can follow ES logs typing `kubectl logs -f es-cluster-0 -n kube-logging`.

Do not forget to follow events to see what is happening:

    kubectl get events -w -ALL

### Testing your setup

Do the following:

    kubectl port-forward es-cluster-0 9200:9200 --namespace=kube-logging

Now in another terminal:

    curl http://localhost:9200/_cluster/state?pretty

## Deploying Kibana

    kubectl create -f kibana-deployment.yaml
    kubectl rollout status deployment/kibana --namespace=kube-logging
    
### Testing your setup

    kubectl get pods --namespace=kube-logging
    kubectl port-forward kibana-866c457776-mttvd 5601:5601 --namespace=kube-logging

Do not forget to change `kibana-866c457776-mttvd` to your pod name.

## Deploying and setup of Fluentd as DaemonSet

    kubectl create -f fluentd-daemonset.yaml
    kubectl get ds --namespace=kube-logging

## Setup a sample app which logs to STDOUT

Here I'm using a local App which was built in docker-compose. I even translated its `.env` to a `configmap`.

    kubectl create configmap sample-api-configmap --from-env-file=.env-prd -n=development
    kubectl get configmap sample-api-configmap -o yaml -n=development

It's important to point out your App as we don't have for now a public application which can be used for this test.

Sample recipes that you can use to your tests:

- [sample-api-dev-deployment.yaml](./sample-api-dev-deployment.yaml)
- [sample-api-prd-deployment.yaml](./sample-api-prd-deployment.yaml)

## How to change fluentd config

I configured a custom [kubernetes.conf](./kubernetes.conf) (I get it from [here](https://github.com/fluent/fluentd-kubernetes-daemonset/blob/04122c95689ad2e7b106023b9e4b9894f2ab6426/docker-image/v1.9/debian-elasticsearch7/conf/kubernetes.conf)) that sends only messages which is originated from `production` namespace. Beyond that there is a filter that parses what is contained in `log` key to `json`, I believe that's better than `json_in_json` plugin. To create a `configmap` from it, do the following:

    kubectl create configmap custom-fluentd-conf --from-file=kubernetes.conf --namespace=kube-logging

You can see [custom-fluentd-daemonset.yaml](./custom-fluentd-daemonset.yaml) recipe which uses this setup.

# Useful links

Tutorials:

- [How To Set Up an Elasticsearch, Fluentd and Kibana (EFK) Logging Stack on Kubernetes](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-elasticsearch-fluentd-and-kibana-efk-logging-stack-on-kubernetes)
- [Fluentd Webinar: Best kept secret to unify logging on AWS, Docker, GCP, and more](https://www.youtube.com/watch?v=aeGADcC-hUA)

Interesting issues:

- [Fluentd is skipping logs in kubernetes](https://github.com/fluent/fluentd-kubernetes-daemonset/issues/366)
- [Fluentd not sending logs to ES after a pod restart](https://github.com/fluent/fluentd-kubernetes-daemonset/issues/338)
- [JSON in 'log' field not parsed/exploded after migration from 0.12 to 1.2](https://github.com/fluent/fluentd/issues/2021)
- [Nested JSON parsing stopped working with fluent/fluentd-kubernetes-daemonset:v0.12-debian-elasticsearch](https://github.com/fluent/fluentd/issues/2073)

Docker images:

- [Fluentd Daemonset for Kubernetes](https://hub.docker.com/r/fluent/fluentd-kubernetes-daemonset/)
- [Fluentd Docker Image](https://hub.docker.com/r/fluent/fluentd)

Configuration files used by default concerning this tutorial:

- [Native configs files for v1.9.3-debian-elasticsearch7-1.0](https://github.com/fluent/fluentd-kubernetes-daemonset/tree/master/docker-image/v1.9/debian-elasticsearch7/conf)
- [GitHub issue about json logs not parsing correctly](https://github.com/fluent/fluentd-kubernetes-daemonset/issues/324)
