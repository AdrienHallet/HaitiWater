# Choix et motivations pour l'implémentation

Document rassemblant les choix effectués lors de l'implémentation afin de pouvoir les utiliser plus tard dans la défense écrite et orale.

## Chart.js comme outil de génération de graphes

Comme toutes les librairies qui nous intéressaient, Chart.js est bien entendu open source, documenté, largement utilisé et
à la pointe de la technologie actuelle.

Ce qui a motivé le choix de Chart.js par rapport à une autre librairie (D3.js par exemple), c'est son fonctionnement par canevas plutôt que par
élément du DOM. En effet, D3.js génère ses graphes en utilisant du CSS et du HTML, créant des formes à partir d'éléments HTML paramétrisables.
Cette liberte qu'offre D3.js est la raison pour laquelle c'est la plus utilisée mondialement, mais elle présente un désavantage majeur :

Chaque élément d'un graphe (chaque point, chaque arc, ...) est un élément du DOM qui doit donc être rendu sur le document par le client. Pour ce faire
il doit être généré par le template Django. Pour de larges données ou des graphiques complexes, cela signifie un transfert plus élevé pour le serveur (qui doit
envoyer la totalité des données) et une charge plus importante pour le client (qui doit pouvoir afficher ces données).

Dans le contexte Haïtien, où connexion et puissance de calcul sont limitées, le choix de Chart.js est bien plus approprié car cette librairie
utilise le principe des canevas pour générer et afficher des images. Le serveur ne doit ainsi envoyer que les données affichées, et la librairie se
charge localement de créer une image. On utilise ainsi moins de bande passante, et le DOM aura le même nombre d'éléments.
