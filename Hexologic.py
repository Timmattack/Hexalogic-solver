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
    def __dictFromCases(cases):
        sols = {c: 0 for c in cases}
        return sols
    
    def __getCasesFromSommes(self):
        cases = {}
        for s in self.__sommes:
            for c in s[1]:
                cases.add(c)
        return cases
    
    def __init__(self, sommes=None):
        self.__sommes = sommes if sommes else []
        casesSommes = self.__getCasesFromSommes()
        
        self.__cases = dictFromCases(casesSommes)
    
    def solve(self):
        if(self.__solve()):
            return copy.deepcopy(self.__cases)
        else:
            return {}
    
    def __solve(self):
        # Problème résolu si toutes les sommes sont complétées
        return self.__completeSommes(len(self.__sommes)-1)
    
    """
    i_somme : la contrainte concernée
    """
    def __completeSommes(self, i_somme):
        # Toutes les cases ont été parcourues : objectif atteint
        if i_somme < 0:
            return True
        
        somme = self.__sommes[i_somme]
        
        # Si cette somme est complétable :
        #   On continue
        return self.__completeSomme(somme) and self.__completeSommes(i_sommes-1)
    
    """
    somme : Une contrainte de somme : paire (somme, [coordonnées])
    """
    def __completeSomme(self, somme):
        return self.__atteintSomme(somme[0], somme[1], len(somme[1])-1):
    
    """
    goal : un entier positif : la somme à atteindre
    liste : une liste de coordonnées : les points à additionner
    i_case : la case
    """
    def __atteintSomme(self, goal, liste, i_case):
        if goal < 0:
            return False
        if (i_case < 0) and (goal == 0):
            return True
        
        val = self.__cases[liste[i_case]]
        # Si la case est set : On passe au suivant
        if val != 0:
            return self.__atteintSomme(goal-val, liste, i_case-1)
        
        for i in range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1):
            self.__cases[liste[i_case]] = i
            if self.__atteintSomme(goal-i, liste, i_case-1):
                return True
        
        self.__cases[liste[i_case]] = 0
        return False
