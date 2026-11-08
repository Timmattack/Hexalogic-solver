import copy



class Hexologic:
    MINVAL_CASE=1
    MAXVAL_CASE=3
    DEFAULTVAL_CASE=-1
    
    
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
        sols = {c: Hexologic.DEFAULTVAL_CASE for c in cases}
        return sols
    
    def __getCasesFromSommes(self):
        cases = set()
        for s in self.__sommes:
            for c in s[1]:
                cases.add(c)
        return cases
    
    def __init__(self, sommes=None, forces=None):
        self.__sommes = sommes if sommes else []
        self.__forces = forces if forces else []
        
        casesSommes = self.__getCasesFromSommes()
        
        
        self.__cases = Hexologic.__dictFromCases(casesSommes)
    
    def getNbCases(self):
        return len(self.__cases)
    
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
        # Toutes les sommes ont été parcourues : objectif atteint
        if i_somme < 0:
            return True
        
        somme = self.__sommes[i_somme]
        
        # Si cette somme est complétable :
        #   On continue
        return self.__completeSomme(somme, i_somme)
    
    """
    somme : Une contrainte de somme : paire (somme, [coordonnées])
    """
    def __completeSomme(self, somme, i_somme):
        return self.__atteintSomme(somme[0], somme[1], len(somme[1])-1, i_somme)
    
    
    """
    goal : un entier positif : la somme à atteindre
    liste : une liste de coordonnées : les points à additionner
    i_case : la case
    """
    def __atteintSomme(self, goal, liste, i_case, i_somme):
        if goal < 0:
            return False
        # Si la somme est complétée : On passe à la suivante, avec possibilité de backtrack
        if (i_case < 0) and (goal == 0):
            return self.__completeSommes(i_somme-1)
        if (i_case < 0):
            return False
        
        val = self.__cases[liste[i_case]]
        # Si la case est set : On passe à la case suivante de cette somme
        if val != Hexologic.DEFAULTVAL_CASE:
            return self.__atteintSomme(goal-val, liste, i_case-1, i_somme)
        
        # On cherche quelle valeur peut correspondre à la case
        for i in range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1):
            self.__cases[liste[i_case]] = i
            if self.__atteintSomme(goal-i, liste, i_case-1, i_somme):
                return True
        
        # Aucune valeur ne convient, on la remet à défaut
        self.__cases[liste[i_case]] = Hexologic.DEFAULTVAL_CASE
        return False
