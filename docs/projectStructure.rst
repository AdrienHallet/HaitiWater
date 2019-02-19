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
    
    
haitiwater - Fichiers Django
----------------------------
``manage.py`` est le fichier à partir duquel vous interagissez avec Django. 
::

  HaitiWater/code/haitiwater/haitiwater
  ├── settings.py
  ├── urls.py
  └── wsgi.py

Le dossier ``haitiwater`` contient les fichiers de base de Django, tout particulièrement:
  - ``settings.py`` : contient les informations de connexion aux services (base de données, serveur mail, serveur hôte, etc)
  - ``urls.py`` : contient les règles de résolution URL de base. Les pages menant à des modules de l'application sont redirigées vers des fichiers ``urls.py`` propres à chaque module.
  

apps - Modules
--------------
Les applications continennet les différents modules d'HaïtiWater.
::
    Haitiwater/code/haitiwater/apps
    ├── administration
    ├── api (communications AJAX serveur/client)
    ├── authentication (utilisateurs)
    ├── consumers (consommateurs)
    ├── dashboard (page d'accueil)
    ├── financial (finances des consommateurs)
    ├── log (logging des actions)
    ├── offline (quand l'application est hors-ligne)
    ├── report (rapports mensuel et technique
    ├── utils (utilitaires du serveur)
    ├── water_network (réseau de distribution d'eau potable)
    └── zone_management (gestion de zone)
    
Chaque module a une structure de type
::
    module
    ├── classes
    ├── migrations
    ├── static
    ├── templates
    ├── test
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py

Veuillez vous référer à la documentation Django pour comprendre la structure générale des applications [1]_

static-common - Fichiers statiques généraux
-------------------------------------------
::

    Haitiwater/code/haitiwater/apps
    ├── images
    ├── javascripts
    ├── stylesheets
    └── vendor
    
- ``images`` contient les ressources graphiques du serveur (favicon, logo)
- ``javascripts`` contient les javascripts réutilisés à travers l'application. Les scripts utilisés par une application sont dans le dossier ´´śtatic´´ de l'application (module) correspondante.
- ``stylesheets`` contient les fichiers CSS
- ``vendor`` contient les librairies utilisées par l'application en front-end.

*La totalité des librairies utilisées par l'application devrait être servie par le serveur et non pas par des CDN externes afin d'optimiser les téléchargements.*

templates - Gabarits généraux
------------------------------
Le fichier ``templates`` contient les gabarits Django réutilisés à travers l'application. On y trouve les menus, graphes et le fichier ``base.html`` étendu par tous les modules de l'application.

.. [1] https://docs.djangoproject.com/fr/2.1/intro/overview/
