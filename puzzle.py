
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
        listCases = list(dict.items())
        # On trie les cases par leur nombre de contraintes
        listCases.sort(key=lambda case : case[1])
        
        return listCases
    
    def __init__(self, sommes=None):
        self.__sommes = sommes if sommes else []
        
        # Répertorier les cases du problème
        casesSommes = Hexologic.__getCasesFromSommes(self.__sommes)
        self.__cases = Hexologic.__dictCasesToSortedList(casesSommes)
        
        # Initialisation de la solution à 0
        self.__solution = list(map(lambda e: {pos: e[0], val: 0}, self.__cases))
    
    """
    def solve():
        # Renvoyer la liste des coordonnées et leur valeur
        if(!self.__solve(premiereCase))
            return {}
        else:
            return self.__solution
    
    def __solve(i_case):
        # if i_cases >= len(self.__cases):
        #   Toutes les cases ont été assignées : est-ce une solution ?
        #   return self.__checkSommes()
        # for i in range()
        # if checkSommes:
        #   return True
        # else:
        #   
    def __checkSommes():
        
    """
