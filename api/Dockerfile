FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir -p /usr/src/api
WORKDIR /usr/src/api
COPY ./requirements.txt /usr/src/api/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /usr/src/api/
ENV PYTHONPATH /usr/src:$PYTHONPATH
