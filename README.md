
# Hexologic, représenter le puzzle

Le puzzle est formé par un ensemble de contraintes:
- Les sommes
- Les cases forcées
- Les cases égales
- Les comparaisons

## Représentation du puzzle et coordonées des cases

Le jeu est sous forme de cases hexagonales.
Mais on peut le représenter comme une simple matrice, en admettant que les cases sur une même diagonale (principale, de haut-gauche à bas-droite) sont adjoints.
Les coordonnés `xy` pour un hexagone sont alors : 

```
    00  10  20
  01  11  21  31
02  12  22  32  42
  13  23  33  43
14  24  34  44  54
  25  35  45  55
    36  46  56
```

Donc si on replace en forme de matrice :
```
00  10  20
01  11  21  31
02  12  22  32  42
    13  23  33  43
    14  24  34  44  54
        25  35  45  55
            36  46  56
```

C'est ce système de coordonnées qui sera utilisé pour représenter les cases du puzzle.

---

## Sommes : la base

C'est la première contrainte rencontrée : Un ligne / colonne / diagonale doit atteindre une certaine somme

Pour représenter **UNE** contrainte de somme, on créer alors un couple `(valeur, cases)`, avec `valeur` la somme à atteindre, et `cases` une liste des cases concernées par la somme.

Si un puzzle contient alors la contrainte de somme de valeur 5, et 3 cases sur une même ligne, avec comme première case `(0,0)`, alors cette contrainte s'exprime
```py
(5, [(0,0), (1,0), (2,0)])
```

Alors pour un puzzle entier, il faut mettre la contrainte dans une liste :
```py
s = [(5, [(0,0), (1,0), (2,0)])]
```

Si il y a plusieurs contraintes de sommes, on a alors on regroupe les contraintes dans une liste:
```py
# 3ème Puzzle du premier monde (3 cases, une liée à 2 sommes)
s = [ (6, [(0,0), (1,1)] ), 
    (4, [(1,1), (2,1)] ) ]
h3 = Hexologic(sommes=s)
```

*Roooh, mais c'est long de mettre la coordonnée de chaque case, à chaque fois, non ?*

### Des outils pour se simplifier la vie

La classe Hexologic propose alors 3 fonctions static pour obtenir une liste de coordonées à partir d'un point d'origine, et du nombre de cases suivants

- `Hexologic.ligne(case, nb_cases)` pour les cases d'une même ligne
- `Hexologic.diagonale(case, nb_cases)` pour les cases d'une même colonne (se référer à la vision matricielle)
- `Hexologic.colonne(case, nb_cases)` pour les cases de la même diagonale (principale, se référer à la vision matricielle)

Pour utiliser simplement ces fonctions, il est conseillé de les assigner ainsi : 
```py
ligne = Hexologic.ligne
col = Hexologic.colonne
diag = Hexologic.diagonale

# On réécrit le 3ème puzzle avec ces fonctions :
s = [(6, diag((0,0), 2)), 
	(4, ligne((1,1), 2)) ]
h3 = Hexologic(sommes=s)
```

**ATTENTION**
Si vous ne mettez qu'une case pour une contrainte, il faut bien penser à mettre cette case dans une liste ^^


# 02/11/2026 : Solveur bête et méchant :
On met la première case à 1, puis la deuxième à 1 aussi, ainsi de suite ...
Si cette solution ne marche pas, on met la dernière case à 2
Si cette solution ne marche pas, on met la dernière case à 3
Sinon, on backtrack, on met l'avant dernière case à 2, puis la dernière case à 1
...

Jusqu'à trouver la solution qui stisfait la contrainte

Sur des tout petits exemples (Puzzle 4, 5 cases), on met très peu de temps (moins d'un millième de seconde),
Mais pour des instances plus grandes (premier Puzzle bonus, 20 cases), le temps d'éxécution explose (1000 s)

# 8/11/2026 : Un solveur qui suit la contrainte :
Maintenant, au lieu de bruteforce comme un idiot, le solveur va chercher à compléter les sommes une par une, suivant ainsi un objectif plus clair

- Je complète la première contrainte de somme, en assignant aux cases de cette contrainte une valeur vérifiant celle-ci
- Je complète la suivante ...

Si une contrainte n'est plus vérifiable, HOP, backtrack


Les résultats sont BEACUOUP plus rapides sur les "gros exemples" (20 cases), on est inférieur à 0.01s

# 8/11/2026 : Force ajouté
Ça ne change pas grand chose, on assigne simplement la valeur demandée aux cases spécifiée avant le processus de résolution

