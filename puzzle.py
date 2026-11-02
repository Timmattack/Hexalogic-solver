import copy

class Hexologic:
    MINVAL_CASE=1
    MAXVAL_CASE=3

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
    
    
    @staticmethod
    def __getCasesFromSommes(sommes):
        cases = {}
        for s in sommes:
            for c in s[1]:
                if c not in cases:
                    cases[c] = 1
                else:
                    cases[c] += 1
        
        return cases
    
    @staticmethod
    def __dictCasesToSortedList(dictCases):
        listCases = list(dictCases.items())
        # On trie les cases par leur nombre de contraintes
        listCases.sort(reverse=True, key=lambda case : case[1])
        # On récupère uniquement les coordonnées
        listCases = list(map(lambda c: c[0], listCases))
        
        # Liste de coordonnées, triées par le nombre de contrainte qu'elles ont
        return listCases
    
    def __initSolFromCases(self):
        solution = {}
        for k in self.__cases:
            solution[k] = 0
        
        return solution
    
    def __init__(self, sommes=None):
        self.__sommes = sommes if sommes else []
        
        # Répertorier les cases du problème
        casesSommes = Hexologic.__getCasesFromSommes(self.__sommes)
        
        self.__cases = Hexologic.__dictCasesToSortedList(casesSommes)
        
        # Initialisation des cases à 0
        self.__solution = self.__initSolFromCases()
    
    
    def solve(self):
        # Renvoyer la liste des coordonnées et leur valeur
        if(!self.__solve(0))
            return {}
        else:
            return copy.deepcopy(self.__solution)
    
    def __solve(self, i_case):
        if i_cases >= len(self.__cases):
            # Toutes les cases ont été assignées : est-ce une solution ?
            return self.__checkSommes()
        
        case = self.__cases[i_case]
        
        for val in range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1):
            self.__solution[case] = val
            if self.__solve(i_case+1):
                return True
        
        return false   
    
    def __checkSommes(self):
        for contrainte in self.__sommes:
            if contrainte[0] != self.__sumOfCases(contrainte[1]):
                return False
        return True
    
    def __sumOfCases(self, cases):
        somme = 0
        for c in cases:
            somme += self.__solution[c]
        return somme
    
