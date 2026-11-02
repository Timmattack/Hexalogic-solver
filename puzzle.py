
class Hexologic:
    @staticmethod
    def ligne(case, nb_cases):
        x, y = case
        cases = [(x+i, y) for i in range(nb_cases)]
        return cases
    
    @staticmethod
    def colonne(case, nb_cases):
        x, y = case
        cases = [(x, y+i) for i in range(nb_cases)]
        return cases
    
    @staticmethod
    def diagonale(case, nb_cases):
        x, y = case
        cases = [(x+i, y+i) for i in range(nb_cases)]
        return cases
    
    def __init__(self, sommes=None):
        self.__sommes = sommes if sommes else []
        self.__cases = []
        # Répertorier les cases du problème
        
    
    def solve():
        ...
        # Renvoyer la liste des coordonnées et leur valeur
