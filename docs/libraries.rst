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
[Bootstrap 3](https://getbootstrap.com/docs/3.3/) est une librairie/framework HTML/CSS/JS destinée à la création de sites internets
responsives et compatibles mobiles/desktops. Nous utilisons la version 3 pour sa grande compatibilité avec d'autres librairies, sa
documentation complète et l'aide qui peut être aisément trouvée sur les forums d'aide.

Bootstrap - Datepicker
----------------------
[Bootstrap Datepicker](https://github.com/eternicode/bootstrap-datepicker/) permet d'utiliser des fenêtres modales pour sélectionner
une date. Datepicker est utilisé dans les tables utilisant la périodicité pour choisir le mois pour lequel les données sont affichées.

Bootstrap - Multiselect
-----------------------
[Bootstrap Multiselect](https://github.com/davidstutz/bootstrap-multiselect) permet de créer des composants de type "select" permettant
la sélection multiple, la recherche, etc ...
*Note: Multiselect a été remplacé durant le développement par la librairie Select2, plus performante et permissive. Préférez
son utilisation.*

Bootstrap - Wizard
------------------
[Bootstrap Wizard](https://github.com/VinceG/twitter-bootstrap-wizard) permet de gérer les pages de type "wizard" (step-by-step).
L'application utilise ce wizard dans le rapport mensuel pour accompagner l'utilisateur et lui donner une vue plus simple du formulaire.

FontAwesome
-----------
[FontAwesome](https://fontawesome.com) est utilisée dans sa version gratuite pour ses icônes SVG. L'application utilise ces icônes
en tant que présentation / référence rapide de l'information (e.g. menus) ou en tant que boutons (e.g. tables)

========
Back-End
========
