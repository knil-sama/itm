# itm

Image to mongodb

# Purpose 

Developper un workflow asynchrone de distribution de taches en python3 sous docker.

Objectifs:
- Recuperer les images accessibles par les urls contenues dans le fichier urls.txt.
- Developper une tache qui calculera la MD5 de l'image
- Developper une tache qui transformera l'image en niveau de gris avec le calcul suivant: (R + G + B) / 3
- Developper une tache qui recuperera les outputs des deux precedents workers. Il devra egalement inserer dans une base
de donnees MongoDB, les informations (md5, l'image en niveau de gris, la hauteur et la largeur de l'image, la date d'insertion).
- Developper une api en Flask pour visualiser les images stockees dans MongoDB via l'url http://localhost:5000/image/<MD5>
- Developper une api en Flask de monitoring via l'url http://localhost:5000/monitoring. Cette api devra retourner un
histogramme decrivant le nombre d'images traitees avec succes ou erreur par interval d'une minute. (Prevoir une collection dans MongoDB pour recuperer ces informations)


Notes:
- Certaines URLs retournent une erreur
- Il ne doit pas y avoir de doublons d'image dans la base MongoDB (unicite du MD5)
- Les technologies autres que celles citees sont libres
- Le travail sera rendu sur un repo git public

# Usage

`docker-compose up`

then go to locahost:8080

Click on "ON" of "main_dag" to start the workflow

once the workflow complete you can use endpoint

http://localhost:5000/image/<MD5>  
and  
http://localhost:5000/monitoring <!> not working right now generated graph is empty

# Process

Download will pick a fixed number of picture and load them locally, then 2 parralel job will process this batch, the result of both will be loaded into mongo  
and a last job will update monitoring collection and remove processed url from urls.txt

# Input parameter

* backend/urls.txt => can update content
* dags/mainDag.schedule_interval => can lower frequency
* dags/mainDag.download_operator:limit => can increase number of pictures handled each batch

# Debug

http://localhost:8081/ for admin GUI of mongodb

http://localhost:5000/images for a list of existing md5
