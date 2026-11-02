
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


