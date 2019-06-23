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
