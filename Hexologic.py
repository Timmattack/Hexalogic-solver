from constraint import Problem

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
    """
    def __init__(self, sommes=None):
        self.__sommes = sommes if sommes else []
        
        self.__cases = set()
        self.addCasesSommes()
        
        self.__pb = Problem()
        
        self.__addCasesVariables()
        self.__addSommesConstraint()
    
    def addCasesSommes(self):
        self.__cases = self.__cases | {case for somme in self.__sommes for case in somme[1]}
    
    def __addCasesVariables(self):
        self.__pb.addVariables(self.__cases, range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1))
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
    
    def getNbCases(self):
        return len(self.__cases)
    
    ###               ###
    ### --- SOLVE --- ###
    ###               ###
    def solve(self):
        res = self.__pb.getSolution()
        return res if res else {}
