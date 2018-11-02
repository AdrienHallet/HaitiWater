============
Installation
============

Prérequis
---------
Python 3.x
  Windows
    * Télécharger la dernière version (3.x) de `Python <http://www.python.org/downloads/windows>`_. 
    * Lancer l'exécutable
    * Cocher la case : ``Add Python 3.x to PATH``
    * Lancer l'installation par défaut : ``Install Now``
  Linux
    * Installer la dernière version de Python 3.x avec le gestionnaire de paquets de votre distribution
    * Vérifier que la bonne version est installée::
    
      $ python3 --version

PostgreSQL 9.4 ou supérieure
  Windows
    * Télécharger `PostgreSQL (v9.4+) <https://www.enterprisedb.com/downloads/postgres-postgresql-downloads>`_.
    * Lancer l'exécutable et suivre l'installation avec les valeurs par défaut jusque ...
    * Sélectionner un mot de passe (à retenir, important!)
    * Continuer l'installation avec les valeurs par défaut
    * Lancer "StackBuilder" à la fin de l'installation lorsqu'il le propose
    * Sélectionner la version PostgreSQL que vous avez choisie
    * Cocher ``Categories>Spatial Extensions>PostGIS 2.x`` (sélectionner la dernière version adaptée à votre installation PostgreSQL 32/64bits)
    * Terminer l'installation avec les valeurs par défaut

Environnement de développement python
  * Installer virtual environment via l'outil ``pip`` installé par défaut avec Python 3.x ::
  
    $ pip install virtualenv
    
Créer la base de données
------------------------
* Vous avez besoin de créer un superutilisateur avec mot de passe. Référez-vous à des `tutoriels <https://www.tutorialspoint.com/postgresql/postgresql_create_database.htm>`_ pour savoir comment faire précisément sur votre système d'exploitation.

* Déclarez cette nouvelle base de données en tant que base de données géographique PostGIS ::
  
  $ psql -U <nom_superutilisateur_choisi>
  $ CREATE DATABASE haitiwater;
  $ \connect haitiwater
  $ CREATE EXTENSION postgis;

Installer le projet
-------------------
Cloner le repository GitHub
  * Ouvrir un terminal (Windows : cmd.exe) à l'emplacement désiré pour le projet
  * Cloner le repository ::
  
    $ git clone https://github.com/AdrienHalletUCL/HaitiWater
    
  * Naviguer dans l'arborescense jusque ::
  
    ../HaitiWater/code
    
  * Créer un environnement virtuel Python (il permettra d'isoler l'installation, empêchant des conflits avec d'éventuels autres projets) ::
  
    ../HaitiWater/code $ virtualenv env
    
Configurer le projet
--------------------
Configurez l'accès à la base de données dans le fichier ``HaitiWater/code/haitiwater/haitiwater/settings.py`` ::

  DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'haitiwater',
        'HOST': 'localhost',
        'PORT': '<PORT>',
        'USER': '<SUPERUSER>',
        'PASSWORD': '<PASSWORD>',
    }
  }
  
Où
  * <PORT> est le numéro de port utilisé par votre serveur PostgreSQL (5432 par défaut)
  * <SUPERUSER> est le nom de superutilisateur choisi
  * <PASSWORD> est le mot de passe choisi pour le superutilisateur
    
Lancer le projet
----------------
En vous positionnant au chemin (dernier laissé précédemment) ``../HaitiWater/code``:
  * Activer l'environnement virtuel Python
    Windows ::
      
      env\Scripts\activate
      
    Linux ::
    
      $ source env/bin/activate
      
  * Naviguer jusqu'au projet ::
  
    $ cd haitiwater
    
  * Installer les dépendances ::
  
    $ pip install -r requirements.txt
    
  * Exporter le schéma de la base de données ::
  
    $ python3 manage.py makemigrations
    $ python3 manage.py migrate
    
  * Lancer le serveur ::
  
    $ python3 manage.py runserver
 
