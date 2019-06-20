===============================
Fenêtres modales et formulaires
===============================

Les modales/formulaires disposent de ``handlers`` situés dans le dossier ``static`` de leur module respectif. Chacune dispose d'une :
    * Validation : pour vérifier localement les informations entrées dans les champs et préparer la requête d'envoi
    * Initialisation : En ajout et en édition pour respectivement vider ou pré-remplir les champs en fonction des informations déjà disponibles

Un ``genericModalHandler`` commun est utilisé par toutes les modales pour les fonctions communes.
