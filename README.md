# itm

Image to mongodb

# Purpose 

Create a workflow of image processing using python and airflow

Dags run every 5 minutes:
* Generate random number of url
* Download image
* Calculate MD5 of image
* Calculate grayscale
* Load result into mongodb (using md5 to avoid duplicate)
* Allow download of image by a REST API `http://localhost:5000/image/<MD5>`
* Display number of image processed (fail/success) `http://localhost:5000/monitoring`  

# Usage

`docker-compose up`

then go to locahost:8080

Click on "ON" of "main_dag" to start the workflow

once the workflow complete you can use endpoint

`http://localhost:5000/image/<MD5>`  
and  
`http://localhost:5000/monitoring`

# Process

Generate will generate a number of image ranging from 0 to 1000, Download will load locally all url generated, then 2 parralel job will process this batch, the result of both will be loaded into mongo  
and a last job will update monitoring collection and remove processed url from urls.txt
The generate part can be replaced by an airflow `s3_key_sensor` or anything that can continously stream data. 
# Input parameter

* dags/mainDag.schedule_interval => can lower frequency
* dags/mainDag.download_operator:limit => can increase number of pictures handled each batch

# Debug

http://localhost:8081/ for admin GUI of mongodb

http://localhost:5000/images for a list of existing md5
