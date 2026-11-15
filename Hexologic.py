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
    casesSommes : liste de contrainte caseSomme : ([casesOutput], [casesInput])
    """
    def __init__(self, sommes=None, forces=None, egals=None, comps=None, casesSommes=None):
        self.__sommes = sommes if sommes else []
        self.__forces = forces if forces else []
        self.__egals = egals if egals else []
        self.__comps = comps if comps else []
        self.__casesSommes = casesSommes if casesSommes else []
        
        
        self.__VarSommes = self.__getVarSommes() # Des cases peuvent avoir un domaine différent
        self.__VarForces = self.__getVarForces() # Domaine forcé, différent du défaut
        self.__VarEgals = self.__getVarEgals()
        self.__VarComps = self.__getVarComps() # Des cases peuvent avoir un domaine différent
        self.__VarComparator = self.__getVarComparator() # Domaine forcé, différent du défaut
        self.__VarSommesInput = self.__getVarSommesInput() 
        self.__VarSommesOutput = self.__getVarSommesOutput() # Domaine dépendant des inputs
        
        # On enregistre les sets qui auront un domaine restreints dont on s'occupe à part
        self.__setToRestrictedDomain(self.__VarForces, 
            self.__VarComparator, 
            self.__VarSommesOutput)
        
        self.__cases = set() |\
            self.__VarSommes |\
            self.__VarForces |\
            self.__VarEgals |\
            self.__VarComps |\
            self.__VarComparator |\
            self.__VarSommesInput |\
            self.__VarSommesOutput
        
        self.__pb = Problem()
        
        # Toutes les variables on pour domaine [MINVAL_CASE, MAXVAL_CASE]
        # SAUF celles qui ont un domaine restreint (forces, comparateur, sommesOutput)
        self.__addVariablesNonRestricted()
        self.__addSommesConstraint()
        
        self.__addVariableForces()
        # Pas de contrainte sur forces : c'est déjà le domaine qui contraint
        
        self.__addEgalsConstraint()
        
        # Les cases comparateur sont à 0
        self.__addVariablesComparator()
        self.__addCompsConstraint()
        
        self.__addVariablesSommesOutput()
        self.__addSommesConstraint()
    
    
    def __setToRestrictedDomain(self, *sets):
        self.__VarRestricted = set()
        for s in sets:
            self.__VarRestricted |= s
    def __getRestrictedVar(self):
        return self.__VarRestricted
    
    def __addVariablesNonRestricted(self):
        self.__pb.addVariables(self.__cases - self.__getRestrictedVar(),
            range(Hexologic.MINVAL_CASE, Hexologic.MAXVAL_CASE+1))
    
    ##########
    ### Sommes
    def __getVarSommes(self):
        return {case for somme in self.__sommes for case in somme[1]}
    
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
    
    ##########
    ### Forces
    def __getVarForces(self):
        return {force[0] for force in self.__forces}
    
    def __addVariableForces(self):
        for force in self.__forces:
            self.__pb.addVariable(force[0], [force[1]])
    
    #########
    ### Egals
    def __getVarEgals(self):
        return {case for egal in self.__egals for case in egal}
    def __addEgalsConstraint(self):
        for egal in self.__egals:
            self.__pb.addConstraint(AllEqualConstraint(), egal)
    
    #########
    ### Comps
    def __getVarComps(self):
        return {case for comp in self.__comps for case in comp[1]} |\
            {case for comp in self.__comps for case in comp[2]}
    
    def __getVarComparator(self):
        return {comp[0][0] for comp in self.__comps}
    
    def __addVariablesComparator(self):
        self.__pb.addVariables(self.__VarComparator, [0])
    
    def __addCompConstraint(self, comp, ic):
        # La somme des cases de gauche est raccrochée à une variable
        nomGauche = f"c{ic}G"
        nbVarGauche = len(comp[1])
        self.__pb.addVariable(nomGauche, 
            range(nbVarGauche*Hexologic.MINVAL_CASE, nbVarGauche*Hexologic.MAXVAL_CASE+1))
        
        self.__pb.addConstraint(lambda goal, *args: goal==sum(args), [nomGauche]+comp[1])
        
        # La somme des cases de droite est raccrochée à une variable
        nomDroite = f"c{ic}D"
        nbVarDroite = len(comp[2])
        self.__pb.addVariable(nomDroite, 
            range(nbVarDroite*Hexologic.MINVAL_CASE, nbVarDroite*Hexologic.MAXVAL_CASE+1))
        
        self.__pb.addConstraint(lambda goal, *args: goal==sum(args), [nomDroite]+comp[2])
        
        # On compare la variable de gauche et de droite
        match comp[0][1]:
            case Hexologic.COMP_MORE:
                self.__pb.addConstraint(lambda g,d: g > d, 
                    [nomGauche, nomDroite])
                
            case Hexologic.COMP_LESS:
                self.__pb.addConstraint(lambda g,d: g < d, 
                    [nomGauche, nomDroite])
                
            case Hexologic.COMP_EGAL:
                self.__pb.addConstraint(lambda g,d: g == d, 
                    [nomGauche, nomDroite])
                
            case _:
                raise Exception(f"ERREUR : COMPARATEUR INCONNU\nLe comparateur '{comp[0][1]}' est inconnu({comp=})")
    
    def __addCompsConstraint(self):
        for ic, comp in enumerate(self.__comps):
            self.__addCompConstraint(comp, ic)
    
    ###############
    ### casesSommes
    def __getVarSommesInput(self):
        return {case for cs in self.__casesSommes for case in cs[1]}
    def __getVarSommesOutput(self):
        return {case for cs in self.__casesSommes for case in cs[0]}
    
    def __addVariablesSommesOutput(self):
        for cs in self.__casesSommes:
            nbInput = len(cs[1])
            self.__pb.addVariables(cs[0], 
                range(nbInput*Hexologic.MINVAL_CASE, nbInput*Hexologic.MAXVAL_CASE+1))
    
    def __addCasesSommesConstraint(self):
        for cs in self.__casesSommes:
            for caseOutput in cs[0]:
                self.__pb.addConstraint(lambda output,*args: output==sum(args), 
                    [caseOutput] + cs[1])
    
    def getNbCases(self):
        return len(self.__cases)
    
    ###               ###
    ### --- SOLVE --- ###
    ###               ###
    def solve(self):
        
        res = self.__pb.getSolution()
        if not res:
            return {}
        
        # La solution contient aussi des variables 'inutiles':
        # - Les variables qui servent à la comparaison 'ciG' et 'ciD' : filtrons les
        trueRes = {k: res[k] for k in res if isinstance(k, tuple)}
        return trueRes
