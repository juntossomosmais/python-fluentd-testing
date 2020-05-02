FROM fluent/fluentd:v1.10-debian-1

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.7 \
    python3-pip \
    python3-setuptools \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install wheel && pip3 install pipenv

WORKDIR /app
COPY Pipfile /app
COPY Pipfile.lock /app

RUN pipenv install --system --deploy --dev --ignore-pipfile
