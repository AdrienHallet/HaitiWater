===================
Tables - DataTables
===================

Les tables disposent de ``handlers`` (ou generator) situés dans le dossier ``static`` de leur module respectif. Chacune dispose d'une :
    * Configuration : pour les actions autorisées sur la table (impression, tri, recherche, etc) et le format (responsive, etc)
    * Initialisation : fonction de dessin appelée par le script de la page requérant la transformation de la table HTML en une DataTable. Cette fonction initialise l'appel à l'API et les différents listeners pour les actions.

Un ``genericTableHandler`` commun est utilisé par toutes les tables pour les fonctions communes (transactions au serveur, traduction française des boutons, etc).
