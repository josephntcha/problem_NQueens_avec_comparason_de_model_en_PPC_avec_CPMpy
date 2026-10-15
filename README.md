# Problème des N reines

Ce projet compare deux modèles de programmation par contraintes pour résoudre le problème des N reines : placer N reines sur un échiquier N × N sans qu’elles puissent se menacer. C'est-à-dire: Sur une ligne, colonne, il doit avoir exactement une seule reine. Il doit avoir au plus une seule reine sur les diagonales

## Modèles comparés

- **Variables booléennes** : une variable par case de l’échiquier, avec des contraintes sur les lignes, les colonnes et les diagonales.

- **Variables lignes** : une variable par ligne, avec des contraintes `AllDifferent` sur les colonnes et les deux diagonales.

Le programme énumère toutes les solutions pour les tailles `n = 4` et `n = 5`, mesure le temps de résolution avec OR-Tools, puis affiche un graphique comparatif.

Ensuite on fait varier le n jusqu'à n = 12

## Installation et lancement

Prérequis : Python 3.

```bash
python -m pip install cpmpy ortools matplotlib
python -m venv venv
pip install matplotlib
venv\Scripts\Activate.ps1

python Nqueens_boolean.py
```

## Interprétation de la comparaison

Le modèle à variables booléennes représente directement chaque case de l’échiquier : il utilise donc `n²` variables. Le modèle à variables lignes n’en utilise que `n`, chaque variable indiquant la colonne de la reine sur une ligne. Il exprime ainsi le problème de façon plus compacte.

Le graphique permet de comparer le temps nécessaire à chaque modèle pour énumérer toutes les solutions. Un temps plus faible indique une meilleure performance pour la taille testée, mais ne garantit pas que le modèle sera toujours plus rapide : les résultats dépendent notamment de la taille de l’échiquier, du solveur et de l’environnement d’exécution.

Sur la base de nos mésures expérimentales, on conclut que la modélisation de variables en lignes est plus performant que la modélisation en variables booléennes.

Voici un exemple de graphe obtenu

![alt text](image.png)

