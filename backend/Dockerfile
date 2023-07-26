# The builder image, used to build the virtual environment
FROM python:3.11-buster as builder

RUN pip install poetry==1.5.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /workspace

COPY ./backend/ ./backend/
COPY ./models/ ./models/
RUN cd backend && poetry install --without test && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM python:3.11-slim-buster as runtime

ENV BACKEND_DIRECTORY ${AIRFLOW_HOME}/backend
ENV BACKEND_DATA_DIRECTORY ${AIRFLOW_HOME}/data
ENV BACKEND_DOWNLOAD_DIRECTORY ${BACKEND_DATA_DIRECTORY}/download
ENV BACKEND_ERROR_DIRECTORY ${BACKEND_DATA_DIRECTORY}/download_error
ENV BACKEND_GRAYSCALE_DIRECTORY ${BACKEND_DATA_DIRECTORY}/grayscale
RUN mkdir -p ${BACKEND_DOWNLOAD_DIRECTORY} ${BACKEND_ERROR_DIRECTORY} ${BACKEND_GRAYSCALE_DIRECTORY}

ENV VIRTUAL_ENV=/workspace/backend/.venv \
    PATH="/workspace/backend/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /workspace/backend
COPY ./backend/backend/ ./backend
COPY ./models/models/ ./models
#COPY api /worspace/api
# COPY ./model /
