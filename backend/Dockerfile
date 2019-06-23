FROM puckel/docker-airflow:1.10.3

USER root

RUN mkdir /opt/backend
COPY . /opt/backend
COPY --chown=airflow:airflow . /opt/backend

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y libssl-dev libffi-dev
RUN pip install --upgrade pip && pip install -r /opt/backend/requirements.txt

RUN mkdir -p /opt/backend/data/download /opt/backend/data/download_error

ENV PYTHONPATH /opt:$PYTHONPATH

USER airflow

WORKDIR /usr/local/airflow
ENTRYPOINT ["/entrypoint.sh"]

