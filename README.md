# HaitiWater
Mémoire UCL 2018-2019 - distribution d'eau potable en Haïti
***
## Wiki
Rendez-vous sur notre [wiki](https://github.com/AdrienHalletUCL/HaitiWater/wiki) pour les informations et liens !

## Installation - Windows
Tuto temporaire, à bouger dans une section d'installation, antérieure à une section de lancement
#### Python
1. [Télécharger la dernière version de Python 3](https://www.python.org/downloads/windows/)
2. Installer avec les valeurs par défaut
3. Installer l'utilitaire python pour la BDD :
~~~
pip install psycopg2
~~~

#### Base de Données
1. [Télécharger PostgreSQL (v9.4+)](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)
2. Lancer l'exécutable et suivre l'installation avec les valeurs par défaut jusque ...
3. Sélectionner un mot de passe (à retenir, important!)
4. Continuer l'installation avec les valeurs par défaut
5. Lancer "StackBuilder" à la fin de l'installation lorsqu'il le propose
6. Sélectionner la version PostgreSQL installée (e.g.: 10)
7. Cocher "Categories>Spatial Extensions>PostGIS 2.x" (sélectionner la dernière version adaptée à votre installation PostgreSQL 32/64bits)
8. Poursuivre l'installation et accepter toutes les valeurs par défaut.

#### Environnement de développement python
1. Installer virtual environment :
~~~
pip install virtualenv
~~~
2. Naviguer dans l'arborescence jusque :
~~~
...\HaitiWater\code
~~~
3. Créer un environnement virtuel :
~~~
virtualenv env
~~~
4. Utiliser l'environnement virtuel :
~~~
env\Scripts\activate
~~~

#### Django
1. Installer Django :
~~~
pip install django
~~~
