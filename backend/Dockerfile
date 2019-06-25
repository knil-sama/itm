FROM puckel/docker-airflow:1.10.3

USER root

RUN mkdir /opt/backend
ENV BACKEND_DATA_DIRECTORY /opt/backend/data
ENV BACKEND_DOWNLOAD_DIRECTORY ${BACKEND_DATA_DIRECTORY}/download
ENV BACKEND_ERROR_DIRECTORY ${BACKEND_DATA_DIRECTORY}/download_error
ENV BACKEND_PROCESSED_DIRECTORY ${BACKEND_DATA_DIRECTORY}/processed
RUN mkdir -p ${BACKEND_DOWNLOAD_DIRECTORY} ${BACKEND_ERROR_DIRECTORY} ${BACKEND_PROCESSED_DIRECTORY}

COPY . /opt/backend
RUN chown -R airflow:airflow /opt/backend

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y libssl-dev libffi-dev
RUN pip install --upgrade pip && pip install -r /opt/backend/requirements.txt


ENV PYTHONPATH /opt:$PYTHONPATH

USER airflow

WORKDIR /usr/local/airflow
ENTRYPOINT ["/entrypoint.sh"]

