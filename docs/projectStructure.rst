===================
Structure du projet
===================

HaïtiWater est un projet Django et utilise l'architecture MVC.

Arborescence Générale
---------------------
::

    HaitiWater/code/haitiwater
    ├── apps
    ├── haitiwater
    ├── static-common        
    ├── templates         
    ├── initial_data.json
    ├── manage.py       
    └── requirements.txt
    
    
Fichiers Django
---------------
``manage.py`` est le fichier à partir duquel vous interagissez avec Django.

Le dossier ``haitiwater`` ::

  HaitiWater/code/haitiwater/haitiwater
  ├── settings.py
  ├── urls.py
  └── wsgi.py


Contient les fichiers de base de Django, tout particulièrement:
  * ``settings.py`` : contient les informations de connexion aux services (base de données, serveur mail, serveur hôte, etc)
  * ``urls.py`` : contient les règles de résolution URL de base. Les pages menant à des modules de l'application sont redirigées vers des fichiers ``urls.py`` propres à chaque module.
