FROM apache/airflow:2.0.0-python3.8

ENV BACKEND_DATA_DIRECTORY ${AIRFLOW_HOME}/data
ENV BACKEND_DOWNLOAD_DIRECTORY ${BACKEND_DATA_DIRECTORY}/download
ENV BACKEND_ERROR_DIRECTORY ${BACKEND_DATA_DIRECTORY}/download_error
ENV BACKEND_GRAYSCALE_DIRECTORY ${BACKEND_DATA_DIRECTORY}/grayscale
RUN mkdir -p ${BACKEND_DOWNLOAD_DIRECTORY} ${BACKEND_ERROR_DIRECTORY} ${BACKEND_GRAYSCALE_DIRECTORY}

COPY . /opt/backend

#RUN apt-get update -y && apt-get upgrade -y && apt-get install -y libssl-dev libffi-dev
RUN pip3 install --upgrade pip && pip3 install -r /opt/backend/requirements.txt
