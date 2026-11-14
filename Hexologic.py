from constraint import Problem, AllEqualConstraint

class Hexologic:
    MINVAL_CASE=1
    MAXVAL_CASE=3
    
    COMP_MORE='>'
    COMP_LESS='<'
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
    
    ###              ###
    ### --- INIT --- ###
    ###              ###
    """
    sommes : liste de contrainte somme : (goal, [cases])
    forces : liste de contrainte force : (case, valeur)
    egals : liste de constrainte egal : [cases] (les cases d'une même liste sont égales)
    comps : liste de constrainte comp : ((case, comparateur), [casesGauche], [casesDroite])
    """
    def __init__(self, sommes=None, forces=None, egals=None, comps=None):
        self.__sommes = sommes if sommes else []
        self.__forces = forces if forces else []
        self.__egals = egals if egals else []
        self.__comps = comps if comps else []
        
        self.__casesSommes = self.__getCasesSommes()
        self.__casesForces = self.__getCasesForces()
        self.__casesEgals = self.__getCasesEgals()
        self.__casesComps = self.__getCasesComps()
        self.__casesComparator = self.__getCasesComparator()
        
        self.__cases = set() | self.__casesSommes | self.__casesForces | self.__casesEgals | self.__casesComps | self.__casesComparator
        
        self.__pb = Problem()
        
        # Toutes les variables on pour domaine [MINVAL_CASE, MAXVAL_CASE]
        # SAUF les cases contraintes par forces, 
        # et les cases comparateur
        self.__addCasesVariables()
        self.__addSommesConstraint()
        
        self.__addCasesVariableForces()
        # Pas de contrainte sur forces : c'est déjà le domaine qui contraint
        
        self.__addEgalsConstraint()
        
        # Toutes les variables qui ne sont pas set par:
        # ni sommes, ni forces
        self.__addCasesVariablesComps()
        # Les cases comparateur sont à 0
        self.__addCasesVariablesComparator()
        self.__addCompsConstraint()
    
    ### Sommes
    def __getCasesSommes(self):
        return {case for somme in self.__sommes for case in somme[1]}
    
    def __addCasesVariables(self):
        self.__pb.addVariables((self.__casesSommes - self.__casesForces) - self.__casesComparator, range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1))
    
    @staticmethod
    def FUNestSommeValide(goal):
        def estSommeValide(*args):
            return goal == sum(args)
        return estSommeValide
    
    def __addSommeConstraint(self, somme):
        self.__pb.addConstraint(Hexologic.FUNestSommeValide(somme[0]), somme[1])
    def __addSommesConstraint(self):
        for somme in self.__sommes:
            self.__addSommeConstraint(somme)
    
    ### Forces
    def __getCasesForces(self):
        return {force[0] for force in self.__forces}
    
    def __addCasesVariableForces(self):
        for force in self.__forces:
            self.__pb.addVariable(force[0], [force[1]])
    
    ### Egals
    def __getCasesEgals(self):
        return {case for egal in self.__egals for case in egal}
    def __addEgalsConstraint(self):
        for egal in self.__egals:
            self.__pb.addConstraint(AllEqualConstraint(), egal)
    
    ### Comps
    def __getCasesComps(self):
        return {case for comp in self.__comps for case in comp[1]} | {case for comp in self.__comps for case in comp[2]}
    
    def __getCasesComparator(self):
        return {comp[0][0] for comp in self.__comps}
    
    def __addCasesVariablesComps(self):
        self.__pb.addVariables((self.__casesComps - self.__casesSommes) - self.__casesForces,
            range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1))
    
    def __addCasesVariablesComparator(self):
        self.__pb.addVariables(self.__casesComparator, [0])
    
    def __addCompConstraint(self, comp, ic):
        # La somme des cases de gauche est raccrochée à une variable
        nomGauche = f"c{ic}G"
        nbCasesGauche = len(comp[1])
        self.__pb.addVariable(nomGauche, range(nbCasesGauche*Hexologic.MINVAL_CASE, nbCasesGauche*Hexologic.MAXVAL_CASE+1))
        
        self.__pb.addConstraint(lambda goal, *args: goal==sum(args), [nomGauche]+comp[1])
        
        # La somme des cases de droite est raccrochée à une variable
        nomDroite = f"c{ic}D"
        nbCasesDroite = len(comp[2])
        self.__pb.addVariable(nomDroite, range(nbCasesDroite*Hexologic.MINVAL_CASE, nbCasesDroite*Hexologic.MAXVAL_CASE+1))
        
        self.__pb.addConstraint(lambda goal, *args: goal==sum(args), [nomDroite]+comp[2])
        
        # On compare la variable de gauche et de droite
        match comp[0][1]:
            case Hexologic.COMP_MORE:
                self.__pb.addConstraint(lambda g,d: g > d, [nomGauche, nomDroite])
                
            case Hexologic.COMP_LESS:
                self.__pb.addConstraint(lambda g,d: g < d, [nomGauche, nomDroite])
                
            case Hexologic.COMP_EGAL:
                self.__pb.addConstraint(lambda g,d: g == d, [nomGauche, nomDroite])
                
            case _:
                raise Exception(f"ERREUR : COMPARATEUR INCONNU\nLe comparateur '{comp[0][1]}' est inconnu({comp=})")
    
    def __addCompsConstraint(self):
        for ic, comp in enumerate(self.__comps):
            self.__addCompConstraint(comp, ic)
    
    def getNbCases(self):
        return len(self.__cases)
    
    ###               ###
    ### --- SOLVE --- ###
    ###               ###
    def solve(self):
        
        res = self.__pb.getSolution()
        # La solution contient aussi des variables 'inutiles':
        # - Les variables qui servent à la comparaison 'ciG' et 'ciD' : filtrons les
        trueRes = {k: res[k] for k in res if isinstance(k, tuple)}
        return trueRes if trueRes else {}
