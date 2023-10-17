FROM fluent/fluentd:v1.15.3-debian-1.0

USER root

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-setuptools \
    curl \
    git \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir wheel pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy --dev --ignore-pipfile

RUN rm Pipfile Pipfile.lock

# Leaving this just as an example for you!
# https://docs.fluentd.org/output/rewrite_tag_filter#installation
RUN fluent-gem install fluent-plugin-rewrite-tag-filter
# https://docs.fluentd.org/deployment/plugin-management#fluent-gem
RUN fluent-gem install fluent-plugin-dynatrace
RUN fluent-gem install fluent-plugin-split-array
RUN fluent-gem install fluent-plugin-record-modifier --no-document

RUN chown root:root .
