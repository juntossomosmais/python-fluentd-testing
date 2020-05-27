FROM fluent/fluentd:v1.10.4-debian-1.0

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.7 \
    python3-pip \
    python3-setuptools \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir wheel pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --dev --ignore-pipfile && pip3 uninstall --yes pipenv

RUN rm Pipfile Pipfile.lock
