==========
Librairies
==========

HaïtiWater utilise plusieurs librairies pour gérer, traiter et afficher les données utilisées par l'application. Cette section
vous décrit les librairies utilisées et leur(s) rôle(s) dans l'application.


=========
Front-End
=========
Les librairies du front-end sont situées dans le dossier ``HaitiWater/code/haitiwater/static-common/vendor``. Il est important
d'importer les librairies localement (sans import provenant de CDNs). Cela permet d'optimiser la connexion en diminuant le nombre
de résolutions DNS, de garantir la disponibilité des librairies et de fixer leur comportement.

Bootstrap 3
-----------
`Bootstrap 3 <https://getbootstrap.com/docs/3.3/>`_ est une librairie/framework HTML/CSS/JS destinée à la création de sites internets
responsives et compatibles mobiles/desktops. Nous utilisons la version 3 pour sa grande compatibilité avec d'autres librairies, sa
documentation complète et l'aide qui peut être aisément trouvée sur les forums d'aide.

Bootstrap - Datepicker
----------------------
`Bootstrap Datepicker <https://github.com/eternicode/bootstrap-datepicker/>`_ permet d'utiliser des fenêtres modales pour sélectionner
une date. Datepicker est utilisé dans les tables utilisant la périodicité pour choisir le mois pour lequel les données sont affichées.

Bootstrap - Multiselect
-----------------------
`Bootstrap Multiselect <https://github.com/davidstutz/bootstrap-multiselect>`_ permet de créer des composants de type "select" permettant
la sélection multiple, la recherche, etc ...
*Note: Multiselect a été remplacé durant le développement par la librairie Select2, plus performante et permissive. Préférez
son utilisation.*

Bootstrap - Wizard
------------------
`Bootstrap Wizard <https://github.com/VinceG/twitter-bootstrap-wizard>`_ permet de gérer les pages de type "wizard" (step-by-step).
L'application utilise ce wizard dans le rapport mensuel pour accompagner l'utilisateur et lui donner une vue plus simple du formulaire.

FontAwesome
-----------
`FontAwesome <https://fontawesome.com>`_ est utilisée dans sa version gratuite pour ses icônes SVG. L'application utilise ces icônes
en tant que présentation / référence rapide de l'information (e.g. menus) ou en tant que boutons (e.g. tables)

Fonts Google
------------
Import de polices Google CSS pour l'application. La seule police d'écriture importée/utilisée est 'Open Sans'.

JQuery
------
`JQuery <https://api.jquery.com/>`_ est une librairie JavaScript permettant la manipulation du DOM très aisément. JQuery devient de plus en plus obsolète par les nouvelles fonctionnalités des navigateurs récents (plus rapides), mais est utilisée dans notre application pour permettre la compatibilité avec plus de navigateurs et librairies.

JQuery - DataTables
-------------------
`DataTables <https://datatables.net/>`_ est une librairie permettant d'utiliser des tables dynamiques, qui ont une forte dépendance à JQuery. Les DataTables sont utilisées dans l'application pour présenter les données via des requêtes AJAX à l'API du serveur.

Leaflet
-------
`Leaflet <https://leafletjs.com/>`_ est une librairie permettant d'inclure une carte interactive que nous utilisons pour présenter l'information dans le module du Système d'Information Géographique.

Magnific Popup
--------------
`Magnific Popup <http://dimsemenov.com/plugins/magnific-popup/>`_ TODO


========
Back-End
========

Django
------
`Django <https://www.djangoproject.com>`_ est la librairie principale de l'application. Elle donne la structure du serveur et son fonctionnement principal. Nous utilisons plusieurs extensions à django :

- *auth* nous permet de gérer des groupes d'utilisateurs et leurs permissions.
- *sessions* nous permet de gérer des sessions d'utilisation de l'application.
- *messages* nous permet d'afficher des notifications à l'utilisateur.
- *staticfiles* nous permet de renvoyer des fichiers statiques par le serveur.
- *gis* nous permet de gérer des données géographiques.

Django REST framework
---------------------
`Django REST framework <https://www.django-rest-framework.org>`_ est une librairie permettant de créer une API web au sein de notre serveur.

Django compressor
-----------------
`Django compressor <https://django-compressor.readthedocs.io/en/stable/>`_ est une librairie permettant de compresser plusieurs fichiers statiques comme des scripts javascripts en un seul fichier.

Django Bootstrap 3
------------------
`Django Bootstrap 3 <https://django-bootstrap3.readthedocs.io/en/latest/quickstart.html>`_ est une librairie permettant d'utiliser des fonctionnalités de bootstrap dans des templates django.

DateUtil
--------
`DateUtil <https://dateutil.readthedocs.io/en/stable/>`_ est une librairie rajoutant plusieurs fonctions utiles sur les dates. Elle est utilisée ici pour sa fonction relativedelta qui permet de faire des calculs avancés sur les dates.
