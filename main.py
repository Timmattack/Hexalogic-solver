from Hexologic import Hexologic
from timeit import default_timer as timer


def afficheLigneSolution(l):
    for paire in l:
        print(f"{paire[0]}:{paire[1]}", end=' ')

def afficheSolution(res):
    """
    Une solution est un dictionnaire de clé (x,y), valeur la valeur de la case
    On va afficher sur la même ligne les cases de même 'y'
    """
    if not res:
        print("LA SOLUTION EST VIDE : PAS DE SOLUTION")
        return
    
    l = list(res.items())
    affiche = {}
    
    # On collectionne les différentes valeurs Y
    Ys = []
    for paire in l:
        Ys.append(paire[0][1])
    Ys.sort()
    
    # Pour chaque valeur de y, on rassemble les bonnes paires
    for y in Ys:
        affiche[y] = [paire for paire in l if paire[0][1]==y]
        affiche[y].sort(key=lambda paire: paire[0][0])
    
    for ligne in affiche.values():
        afficheLigneSolution(ligne)
        print()

def timeSolve(s=None, f=None, e=None, c=None):
    h = Hexologic(sommes=s, forces=f, egals=e, comps=c)
    start = timer()
    print(f"debut recherche : {h.getNbCases()} cases pour ce puzzle")
    res = h.solve()
    end = timer()
    print(f"Le puzzle a pris {end-start:.2f}s a être résolu")
    return res


def puzzlesMonde1():
	ligne = Hexologic.ligne
	col = Hexologic.colonne
	diag = Hexologic.diagonale
	
	print("--- premier Puzzle du premier monde (juste une case)")
	s = [(2, [(0,0)])] # liste de couples (somme, listeDeCoordonnées)
	afficheSolution(timeSolve(s))
	
	print("--- deuxième Puzzle du premier monde (3 cases isolées)")
	s = [(1, [(2, 2)]), (2, [(0, 0)]), (3, [(2, 0)])]
	afficheSolution(timeSolve(s))
	
	print("--- 3ème Puzzle du premier monde (3 cases, une liée à 2 sommes)")
	s = [(6, diag((0,0), 2)), 
	(4, ligne((1,1), 2)) ]
	afficheSolution(timeSolve(s))
	
	print("--- 4ème Puzzle du premier monde")
	s = [(3, diag((0,0), 3)), 
	(4, ligne((1,1), 2)),
	(2, ligne((2,2), 2))]
	afficheSolution(timeSolve(s))
	
	print("--- bonus 1: Un puzzle bien plus gros")
	# Oui, il y a 16 sommes à compléter, pour 20 cases
	s = [(8, diag((2,0), 3)),
	(2, diag((3,0), 2)),
	(4, ligne((2,0), 2)),
	(7, ligne((1,1), 4)),
	(4, ligne((3,2), 2)),
	(3, col((4,1), 2)),
	(5, col((2,0), 2)),
	(11, ligne((0,4), 4)),
	(3, ligne((1,5), 3)),
	(4, col((3,4), 2)),
	(5, col((2,3), 3)),
	(7, col((1,1), 5)),
	(8, col((0,2), 3)),
	(4, diag((0,4), 2)),
	(3, ligne((0,2), 2)),
	(5, diag((1,2), 3))]
	afficheSolution(timeSolve(s))
	
	print("--- bonus 3: Un autre gros puzzle")
	s = [(6, ligne((0,0), 2)),
    (11, diag((1,0), 5)),
    (3, diag((3,1), 2)),
    (9, col((3,0), 4)),
    (9, ligne((1,1), 4)),
    (7, ligne((0,2), 6)),
    (9, ligne((1,3), 4)),
    (8, col((4,1), 4)),
    (8, col((2,1), 4)),
    (6, col((1,0), 4)),
    (4, diag((0,2), 3)),
    (4, diag((1,2), 2))]
	afficheSolution(timeSolve(s))
    

def puzzlesMonde2():
	"""
	Des cases ont une valeur forcée (en général cette valeur est supérieure à 3)
	
	On rajoute dans le constructeur un autre paramètre [forces]:
	une liste des cases forcées et leur valeur
	"""
	ligne = Hexologic.ligne
	col = Hexologic.colonne
	diag = Hexologic.diagonale
	
	print("--- Puzzle num 16")
	s = [(7, diag((0,0), 2)),
	(4, col((0,0), 2))]
	f = [((1,1), 4)]
	afficheSolution(timeSolve(s=s, f=f))
	
	print("--- Puzzle 17")
	s = [(5, diag((0,0), 2)),
	(9, ligne((1,1), 3))]
	f = [((2,1), 6)]
	afficheSolution(timeSolve(s=s, f=f))
	
	print("--- Puzzle 18")
	s = [(4, diag((0,0), 2)),
	(7, col((2,0), 2)),
	(4, diag((2,1), 2)),
	(8, col((1,1), 2))]
	f = [((2,0), 4), 
	((2,1), 6)]
	afficheSolution(timeSolve(s=s, f=f))
	
	print("--- Bonus 1 (19 sommes, 25 cases, 4 cases forcées)")
	s = [(9, ligne((3,0), 3)),
	(8, col((4, 0), 3)),
	(3, col((5, 0), 2)),
	(9, col((7, 0), 3)),
	(5, diag((7, 1), 2)),
	(9, diag((7, 2), 3)),
	(5, col((8, 2), 2)),
	(7, diag((4, 0), 3)),
	(7, ligne((5, 4), 3)),
	(7, col((6, 2), 3)),
	(4, col((5, 3), 2)),
	(3, ligne((5, 3), 2)),
	(8, diag((1, 1), 3)),
	(4, diag((1, 2), 2)),
	(5, ligne((1, 1), 2)),
	(4, diag((2, 1), 2)),
	(9, diag((4, 2), 3)),
	(10, ligne((1, 2), 4)),
	(9, ligne((6, 2), 3))]
	f = [((4,0), 4), 
	((2,2), 5),
	((7,2), 4),
	((6,4), 4)]
	afficheSolution(timeSolve(s=s, f=f))


def puzzlesMonde3():
	"""
	On peut demander à un ensemble de cases d'être égales:
	On rajoute dans le constructeur un autre paramètre [egals]:
	une liste de liste de cases. Chaque 'sous-liste' est un groupe de cases qui sont contraintes entre-elles
	"""
	ligne = Hexologic.ligne
	col = Hexologic.colonne
	diag = Hexologic.diagonale
	
	print("--- Puzzle 31")
	s = [(2, [(0, 0)]),
	(2, [(0, 3)]),
	(2, [(3, 3)]),
	(3, [(1, 2)])]
	e = [[(0,0), (0,3), (3,3)]]
	afficheSolution(timeSolve(s=s, e=e))
	
	print("--- Puzzle 32")
	s = [(4, ligne((0, 0), 2)),
	(2, diag((1, 0), 2)),
	(4, col((0, 0), 2))]
	e = [[(0, 1), (2, 1)]]
	afficheSolution(timeSolve(s=s, e=e))
	
	print("--- Puzzle 33")
	s = [(4, diag((1, 0), 2)),
	(4, ligne((1, 1), 2)),
	(4, col((1, 0), 2)),
	(5, diag((4, 2), 2)),
	(4, ligne((4, 3), 2)),
	(3, ligne((0, 3), 2)),
	(4, diag((0, 2), 2))]
	e = [[(1, 0), (5, 3), (0, 3)]]
	afficheSolution(timeSolve(s=s, e=e))
	
	print("--- Puzzle 34 (plusieurs groupes d'égalité)")
	s = [(4, ligne((0, 0), 2)),
	(5, diag((1, 0), 2)),
	(5, col((2, 1), 2)),
	(4, ligne((1, 2), 2)),
	(5, diag((0, 1), 2)),
	(5, col((0, 0), 2))]
	e = [[(0, 0), (2, 2)],
	[(1, 0), (1, 2)],
	[(0, 1), (2, 1)]]
	afficheSolution(timeSolve(s=s, e=e))
	
	print("--- Bonus 1")
	s = [(13, ligne((0, 0), 7)),
	(6, ligne((3, 2), 3))]
	e = [[(0, 0), (3, 0), (4, 0), (3, 2)],
	[(1, 0), (2, 0), (5, 0), (6, 0), (4, 2)]]
	afficheSolution(timeSolve(s=s, e=e))

def puzzlesMonde4():
	"""
	Ce monde mixe simplement les cases forcees et les cases egales
	"""
	ligne = Hexologic.ligne
	col = Hexologic.colonne
	diag = Hexologic.diagonale
	
	print("--- Puzzle 46")
	s = [(9, ligne((0, 0), 3))]
	f = [((1, 0), 5)]
	e = [[(0,0), (2,0)]]
	afficheSolution(timeSolve(s=s, f=f, e=e))
	
	print("--- Puzzle 47")
	s = [(5, diag((1, 0), 2)),
	(8, ligne((0, 0), 3)),
	(7, col((2, 0), 3))]
	f = [((1, 0), 4)]
	e = [[(2, 0), (2, 2)]]
	afficheSolution(timeSolve(s=s, f=f, e=e))
	
	print("--- Puzzle 48")
	s = [(9, diag((0, 0), 3)),
	(4, ligne((0, 0), 2)),
	(7, ligne((1, 2), 2))]
	f = [((2, 2), 5)]
	e = [[(1, 0), (1, 2)]]
	afficheSolution(timeSolve(s=s, f=f, e=e))
	
	print("--- Bonus 1 (16 sommes, 1 force, 1 groupe de 3 egals) 23 cases")
	s = [(5, ligne((5, 0), 3)),
	(5, diag((6, 0), 2)),
	(4, col((7, 0), 2)),
	(3, ligne((6, 4), 2)),
	(11, diag((5, 2), 4)),
	(9, diag((5, 3), 3)),
	(8, col((6, 0), 5)),
	(14, col((5, 0), 4)),
	(6, col((4, 3), 3)),
	(14, ligne((3, 3), 4)),
	(6, ligne((0, 1), 3)),
	(11, diag((1, 1), 4)),
	(4, diag((2, 1), 3)),
	(4, ligne((2, 2), 2)),
	(4, ligne((5, 2), 2)),
	(7, ligne((5, 1), 3))]
	f = [((5, 3), 6)]
	e = [[(5, 0), (0, 1), (4, 5)]]
	afficheSolution(timeSolve(s=s, f=f, e=e))

def puzzlesMonde5():
	"""
	Certaines cases contiennent la contrainte : <, > ou =, avec un ensemble de cases qui y sont accrochés
	
	On rajoute un paramètre, liste de 3-uplet [comps]:
	- couple position, caractère (représente le comparateur à utiliser)
	- liste de cases "à gauche" de l'opérateur
	- liste de cases "à droite" de l'opérateur
	"""
	ligne = Hexologic.ligne
	col = Hexologic.colonne
	diag = Hexologic.diagonale
	
	less='<'
	more='>'
	eg='='
	
	# Puzzle 61
	c = [(((1,0), more), [(0,0)], [(2,0)]),
	(((3,0), more), [(2,0)], [(4,0)])]
	afficheSolution(timeSolve(c=c))
	
	# Puzzle 62
	s = [(3, col((0,2), 3))]
	c = [(((3, 0), less), [(2,0)], [(4,0)]),
	(((4, 1), more), [(4,2)], [(4,0)]),
	(((3, 2), eg), ligne((0, 2), 3), [(4,2)]),
	(((0, 3), more), [(0,4)], [0,2]),
	(((1, 4), eg), [(0,4)], ligne((2,4), 2))]
	afficheSolution(timeSolve(s=s, c=c))

	# Puzzle 63
	s = [(6, col((2,0), 5)),
	(5, diag((2,0), 3)),
	(6, diag((0,2), 3))]
	c = [(((2, 1), less), [(2,2)], [(2,0)]),
	(((1, 2), eg), [(0,2)], [(2,2)]),
	(((3, 2), more), [(2,2)], [(4,2)]),
	(((2, 3), less), [(2,4)], [(2,2)])]
	afficheSolution(timeSolve(s=s, c=c))
	
def main():
	"""
	Représentation des coordonnées d'hexagone : 
	Il faut s'imaginer que les cases appartenant à la même anti-diagonale (bas-gauche à haut droite) appartiennent à la même colonne : 
	
	00  10  20
  01  11  21  31
02  12  22  32  42
  13  23  33  43
14  24  34  44  54
  25  35  45  55
    36  46  56
	"""
	puzzlesMonde1()
	puzzlesMonde2()
	puzzlesMonde3()
	puzzlesMonde4()
	puzzlesMonde5()


if __name__ == "__main__":
    main()
