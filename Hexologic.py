from constraint import Problem, AllEqualConstraint

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
    
    ###              ###
    ### --- INIT --- ###
    ###              ###
    """
    sommes : liste de contrainte somme : (goal, [cases])
    forces : liste de contrainte force : (case, valeur)
    egals : liste de constrainte egal : [cases] (les cases d'une même liste sont égales)
    """
    def __init__(self, sommes=None, forces=None):
        self.__sommes = sommes if sommes else []
        self.__forces = forces if forces else []
        self.__egals = egals if egals else []
        
        self.__casesSommes = self.__getCasesSommes()
        self.__casesForces = self.__getCasesForces()
        self.__casesEgals = self.__getCasesEgals()
        
        self.__cases = set() | self.__casesSommes | self.__casesForces | self.__casesEgals
        
        self.__pb = Problem()
        
        # Toutes les variables on pour domaine [MINVAL_CASE, MAXVAL_CASE]
        # SAUF les cases contraintes par forces
        self.__addCasesVariables()
        self.__addSommesConstraint()
        
        self.__addCasesVariableForces()
        # Pas de contrainte sur forces : c'est déjà le domaine qui contraint
        
        self.__addEgalsConstraint()
    
    ### Sommes
    def __getCasesSommes(self):
        return {case for somme in self.__sommes for case in somme[1]}
    
    def __addCasesVariables(self):
        self.__pb.addVariables(self.__casesSommes - self.__casesForces, range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1))
    
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
        return {case for egal in egals for case in egal}
    def __addEgalsConstraint(self):
        for egal in self.__egals:
            self.__pb.addConstraint(AllEqualConstraint(), egal)
    
    
    def getNbCases(self):
        return len(self.__cases)
    
    ###               ###
    ### --- SOLVE --- ###
    ###               ###
    def solve(self):
        res = self.__pb.getSolution()
        return res if res else {}
