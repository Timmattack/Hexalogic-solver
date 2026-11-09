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
    
    @staticmethod
    def __initEgals(egals):
        es = {}
        for e in egals:
            for case in e:
                es[case] = [c for c in e if c!=case]
        return es
    
    def __getCasesFromSommes(self):
        cases = set()
        for s in self.__sommes:
            for c in s[1]:
                cases.add(c)
        return cases
    
    def __getCasesFromForces(self):
        cases = set()
        for f in self.__forces:
            cases.add(f[0])
        return cases
    
    def __setCasesFromForces(self):
        for f in self.__forces:
            self.__cases[f[0]] = f[1]
    
    def __getCasesFromEgals(self):
        cases = set()
        for cs in cases:
            for c in cs:
                cases.add(c)
        return cases
    
    # --- Constructeur
    """
    sommes : [sommes], avec une contrainte de somme : (s, [cases])
    forces : [forces], avec une contrainte de force : (case, val)
    """
    def __init__(self, sommes=None, forces=None, egals=None):
        self.__sommes = sommes if sommes else []
        self.__forces = forces if forces else []
        self.__egals = Hexologic.__initEgals(egals) if egals else {}
        
        casesSommes = self.__getCasesFromSommes()
        casesForces = self.__getCasesFromForces()
        casesEgals = self.__getCasesFromEgals()
        
        self.__cases = Hexologic.__dictFromCases(casesSommes | casesForces | casesEgals)
        
        self.__setCasesFromForces()
    
    def __getCaseValue(self, case):
        return self.__cases[case]
    
    def __setCaseValue(self, case, val):
        self.__cases[case] = val
        if case in self.__egals:
            for autre in self.__egals[case]:
                self.__cases[autre] = val
    
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
        
        val = self.__getCaseValue(liste[i_case])
        # Si la case est set : On passe à la case suivante de cette somme
        if val != Hexologic.DEFAULTVAL_CASE:
            return self.__atteintSomme(goal-val, liste, i_case-1, i_somme)
        
        # On cherche quelle valeur peut correspondre à la case
        for i in range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1):
            self.__setCaseValue(liste[i_case], i)
            if self.__atteintSomme(goal-i, liste, i_case-1, i_somme):
                return True
        
        # Aucune valeur ne convient, on la remet à défaut
        self.__setCaseValue(liste[i_case], Hexologic.DEFAULTVAL_CASE)
        return False
