import copy



class Hexologic:
    MINVAL_CASE=1
    MAXVAL_CASE=3
    DEFAULTVAL_CASE=-1
    
    COMP_LESS='<'
    COMP_MORE='>'
    COMP_EGAL='='
    
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
    
    def __getCasesFromComps(self):
        cases = set()
        for comp in self.__comps:
            cases.add(comp[0][0])
            for cg in cases[1]:
                cases.add(cg)
            for cd in cases[2]:
                cases.add(cd)
        return cases
    
    # Les cases qui servent de comparateur ont pour valeur 0
    def __setCasesFromComps(self):
        for comp in self.__comps:
            self.__cases[comp[0][0]] = 0
    
    # --- Constructeur
    """
    sommes : [sommes], pour chaque contrainte de somme de la forme : (s, [cases])
    forces : [forces], pour chaque contrainte de force de la forme : (case, val)
    egals : [egals], pour chaque contrainte de egal de la forme : [cases]
    comps : [comps], pour chaque contrainte de comp de la forme : ((case, comparateur), [casesGauche], [casesDroite])
    """
    def __init__(self, sommes=None, forces=None, egals=None, comps=None):
        self.__sommes = sommes if sommes else []
        self.__forces = forces if forces else []
        self.__egals = Hexologic.__initEgals(egals) if egals else {}
        self.__comps = comps if comps else []
        
        casesSommes = self.__getCasesFromSommes()
        casesForces = self.__getCasesFromForces()
        casesEgals = self.__getCasesFromEgals()
        casesComps = self.__getCasesFromComps()
        
        self.__cases = Hexologic.__dictFromCases(casesSommes | 
            casesForces | 
            casesEgals | 
            casesComps)
        
        self.__setCasesFromForces()
        self.__setCasesFromComps()
    
    def __estCaseSet(self, case):
        return self.__getCaseValue(case) != Hexologic.DEFAULTVAL_CASE
    
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
    
    ###
    ### --- COMPLETE SOMME --- ###
    ###
    """
    i_somme : la contrainte concernée
    """
    def __completeSommes(self, i_somme):
        # Toutes les sommes ont été complétées : Tentons de compléter les comparaisons maintenant
        if i_somme < 0:
            return self.__completeComps(len(self.__comps)-1)
        
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
        
        if self.__estCaseSet(liste[i_case]):
            return self.__atteintSomme(goal-val, liste, i_case-1, i_somme)
        
        # On cherche quelle valeur peut correspondre à la case
        for i in range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1):
            self.__setCaseValue(liste[i_case], i)
            if self.__atteintSomme(goal-i, liste, i_case-1, i_somme):
                return True
        
        # Aucune valeur ne convient, on la remet à défaut
        self.__setCaseValue(liste[i_case], Hexologic.DEFAULTVAL_CASE)
        return False
    
    ###
    ### --- CompleteComparaison --- ###
    ###
    
    # À partir de là, on fait le pari qu'assez de cases sont complétées,
    # et qu'il est moins long de faire un brute force sur les cases contraintes par comparaison
    def __completeComps(self, i_comp):
        return self.__bruteForceReste()

    def __bruteForceReste(self):
        # Listons les cases qui ne sont pas encore set
        cases = list(filter(lambda case: not self.__estCaseSet(case), self.__cases))
        
        return __bruteForcereste1(self, cases, len(cases)-1)
    
    def __bruteForceReste1(self, cases, i_cases):
        if i_cases < 0:
            return self.__estValideParComps()
        
        if self.__estCaseSet(cases[i_cases]):
            return self.__bruteForceReste1(cases, i_cases-1)
        
        # On cherche quelle valeur peut correspondre à la case
        for i in range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1):
            self.__setCaseValue(cases[i_cases], i)
            if self.__bruteForceReste1(cases, i_cases-1)
                return True
        
        # Aucune valeur ne convient, on la remet à défaut
        self.__setCaseValue(cases[i_cases], Hexologic.DEFAULTVAL_CASE)
        return False
        
    def __estValideParComps(self):
        for comp in self.__comps:
            if not self.__estValideParComp(comp):
                return False
        return True

    def __estValideParComp(self, comp):
        mode = comp[0][1]
        sommeG = self.__sumCasesFromTab(comp[1])
        sommeD = self.__sumCasesFromTab(comp[2])
        
        match mode:
            case Hexologic.COMP_EGAL:
                return sommeG == sommeD
            case Hexologic.COMP_LESS:
                return sommeG < sommeD
            case Hexologic.COMP_MORE:
                return sommeG > sommeD
            case _:
                raise Exception(f"La comparaison '{mode}' dans la contrainte {comp} n'est pas prise en charge")

    # Retourne la somme des valeurs assignées aux cases d'une liste
    def __sumCasesFromTab(self, tab):
        somme = 0
        for case in tab:
            somme += self.__cases[case]
        
        return somme
