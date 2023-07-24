# The builder image, used to build the virtual environment
FROM python:3.11-buster as builder

RUN pip install poetry==1.5.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /workspace

COPY ./api/ ./api/
COPY ./models/ ./models/
RUN cd api && poetry install --without test && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

ENV VIRTUAL_ENV=/workspace/api/.venv \
    PATH="/workspace/api/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /workspace/api
COPY ./api/api/ ./api
COPY ./models/models/ ./models
#COPY api /worspace/api
# COPY ./model /
