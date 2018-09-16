
# Notes 12/09/2018

# "Water Distribution Basic Concepts"

## D'où vient l'eau ?

L'hydrologie se base sur un cycle naturel (pluies, cycle classique vu en primaire/secondaire). A noter qu'il y a l'écoulement des eaux *et* le ruissellement, puis infiltration pour l'eau sous les terres.

1.4 milliard de km³ d'eau sur terre, l'eau douce est moins de 3% et 99.64% de cette eau douce est inutilisable (glace ou nappes trop profondes).

Même si la fonte des glaces et l'amélioration des moyens de forage s'améliorent, ce n'est pas une bonne solution durable (à titre anecdotique, le conflit Israël / Palestine se base également sur la profondeur et la disponibilité de l'eau douce).

## Intervention de l'homme

L'homme intervient dans le cycle de l'eau par consommation (boisson, irrigation, refroidissement). On pompe l'eau et on la distribue, en essayant de maximiser l'efficacité.

## Usages de l'eau

* En tant que liquide (plutôt un vecteur)
* En tant que H2O (nutriments)
* Transport
* Energie (15% de la production mondiale vient de l'hydroélectrique)
* Industrie

## La pression

La pression est une problématique importante nécessitant le renforcement des conduites. Les conduites résistent plutôt bien aux surpressions mais pas aux dépressions. Exemple du "coup de bélier" qui endommage les conduites par système de conduction de l'onde.

En général dans le réseau de distribution on mesure la pression pour surveiller tout ça.

## Transport de l'eau

### "Rendre" l'eau à la nature

Le système d'évacuation est nécessaire. Exemple donné d'un problème ayant eu lieu à Louvain-la-Neuve peu avant l'inauguration de la ville.

Deux grands types de conduites :
- En dépression
- En "semi-vide"

### Types de Transport

Système de :
- Canalisations
- Aqueducs
- Canaux

## Pour le travail
Distribution de l'eau :
- Eau de consommation potable
- irrigation

## La distribution de l'eau
1. Captation de l'eau (source, eau de surface ou nappes)
2. Traitement (chlore, ...)
3. Pompe
4. Transport
5. Stockage (château d'eau)
6. Distribution (normalement gravitaire, parfois pompée si le chateau d'eau ne fournit pas assez de pression)


## Perte de charge

On peut avoir des pertes d'énergies dans la pression. On a une énergie potentielle (au château d'eau) qui diminue à l'arrivée (en Belgique, on considère qu'à la sortie il faut avoir une pression de 3bar.)

*Quelques formules qui me sont totalement incompréhensibles*

Formule de Darcy (au plus c'est petit, au plus ça va frotter fort, donc pertes). *Reynolds : mesure de l'écoulement*.

Dans le réseau de distribution, le coefficient de frottement est plutôt constant, directement dépendant de la rugosité du réseau. Dépendance avec la viscosité également (pratiquement nulle pour l'eau).

On peut reformuler la perte de charge de Darcy non pas avec la vitesse (inintéressante dans le réseau) mais avec le débit (formule plus simple).

Dès qu'on a un changement de géométrie brusque (e.g.: coude dans le réseau), l'écoulement va se "détacher" puis se "rattacher" à la paroi, donc consommation d'énergie et perte de charge.

On a des pertes de charges théoriques et des pertes de charge empiriques.

## Pression
On parle beaucoup de **perte de charge** en mètres plutôt en bars. On peut en fait exprimer la pression (par rapport à la pression atmosphérique) en mètres grâce à la pression (atmosphère), la vitesse (qui s'annule), donc en fait la pression est la différence de niveau entre deux points.
Ne manque que le débit (qui est calculable), on peut ensuite avoir la charge en chaque point. On calcule donc les pressions sur chaque point clé du réseau.

On dit que la pression ne peut pas diminuer en dessous de 5mètres (pour éviter des problèmes de cavitation par exemple).

On peut faire un *diagramme de charge* (assez visuel, pourrait être intéressant dans l'application) pour comparer charge et pression.

## Conduite simple

*Exemple donné d'une vanne et d'altitudes du niveau de l'eau*

A noter de savoir que les fournisseurs de vannes doivent normalement fournir les coefficients de charge pour permettre le calcul général du réseau.

## Consommation
Il y a des normes de valeurs pour estimer la consommation pour le dimensionnement du réseau, en Belgique il n'y a pas de normes. A voir pour Haïti.

Il y a également les pertes (l'identification des pertes est une composante importante pour l'application).

On peut considérer la consommation horaire et moduler le réseau.

Retour sur le manque d'accès à l'eau (pire encore pour potable) en Haïti.

## Ecoulement à surface libre
Element de référence pour les égoûts, collecteurs urbains, irrigation ... Ce ne sont pas des conduites pressurisées.

L'idée générale est l'écoulement uniforme (débit constant, niveau égal, pression constante). Plusieurs formules sont disponibles pour en calculer les propriétés. A noter que le *rayon hydraulique* devient presque la profondeur si le canal est assez large.

La profondeur varie en fonction des facteurs sus-cités (largeur, vitesse d'écoulement, rugosité).

A noter que les conduites d'évacuation circulaires ne sont presque jamais totalement remplies car si le cylindre est complet, il y a trop de frottement (on utilise ce "reste" en marge de sécurité).

On souhaite une vitesse d'écoulement suffisante pour évacuer rapidement le contenu (on demande même que ça soit plus grand que nécessaire à cause des problèmes de précision d'installation).

*Vidéo exemple de l'explosion d'un égoût*

La vidéo montre qu'il ne faut jamais avoir un écoulement en charge dans un égoût.

## Notes finales (pour le futur)
* Penser aux besoins non-fonctionnels de l'application (sécurité)
* Au niveau des choix technologiques,
* Poser les questions pour arriver à comprendre les UX.
* Essayer d'avoir, avec le client, des scénarios d'utilisation. Laisser le client le faire en premier pour qu'il ait l'application idéale.
* Mailer le client pour tenter d'avoir des usage scenario, user stories, whatever qui permet de savoir ce que l'utilisateur veut, comment il le veut et où.
