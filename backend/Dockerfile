FROM python:3.6

RUN groupadd -g 999 backend \
&& useradd -ms /bin/bash -u 2001 -g backend backend

RUN mkdir /opt/backend \
  && chown backend:backend /opt/backend

WORKDIR /opt/backend

COPY --chown=backend:backend . /opt/backend

COPY . /opt/backend

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y libssl-dev libffi-dev
RUN pip install --upgrade pip && pip install -r requirements.txt
USER backend

RUN mkdir -p data/download data/download_error data/to_process_md5 data/processed_md5 data/to_process_rgb data/processed_rgb

ENV PYTHONPATH /opt:$PYTHONPATH

