# itm

Image to metadata

# Purpose

Create a workflow of image processing in python using various storage (cloud & database) and orchestrator (Ariflow)

Dags run every 5 minutes:
* Generate random number of url
* Download image (from an online random generator)
* Compute MD5 of image (to use it as id)
* Compute grayscale
* Load result into mongodb (using MD5 to avoid duplicate)
* Allow download of image by a REST API `http://localhost:8000/image/<MD5>`
* Display number of image processed (fail/success) `http://localhost:8000/monitoring`

# Usage

`docker-compose up`

then go to [http://0.0.0.0:8080](http://0.0.0.0:8080)

Use default `admin` user with `test` to connect

Click on "ON" of "main_dag" to start the workflow

once the workflow complete you can use endpoint

[http://localhost:8000/image/<MD5>](http://localhost:8000/image/<MD5>)
and
[http://localhost:8000/monitoring](http://localhost:8000/monitoring)

# Process

Generate will generate a number of image ranging from 1 to 1000, Download will load locally all url generated, then 2 parallel jobs will process this batch, the result of both will update an "event" that will be converted into the final "image" model.
and a last job will update monitoring collection.

# Input parameter

* dags/main_dag.schedule_interval => can lower frequency

# Debug

[http://localhost:8081/](http://localhost:8081/) for admin GUI of mongodb

[http://localhost:5000/images](http://localhost:8000/images) for a list of existing md5

# Resources

https://dzone.com/articles/running-apache-airflow-dag-with-docker

https://airflow.apache.org/docs/apache-airflow/stable/configurations-ref.html
