# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 19:26:39 2016

@author: Janus
"""
import gurobipy as gb
import math

class expando(object):
    '''
        A small class which can have attributes set
    '''
    pass

class elecOpt:
    def __init__(self):       
        #from elecOptClass import expando           
        self.data = expando()
        self.variables = expando()
        self.constraints = expando()
        self._load_data()
        self._build_model()
        
    
    def optimize(self):
        self.model.optimize()
        self.status()
    
    def status(self):
        # Check model status
        self.data.status = self.model.status
        #print(self.status.status)
        if self.data.status != gb.GRB.Status.OPTIMAL:
            print('Optimization was stopped with status %d' % self.data.status)
            if self.data.status == gb.GRB.Status.INFEASIBLE:            
                # do IIS
                print('The model is infeasible; computing IIS')
                self.model.computeIIS()
                print('\nThe following constraint(s) cannot be satisfied:')
                for c in self.model.getConstrs():
                    if c.IISConstr:
                        print('%s' % c.constrName)
                print('Day of problem: %g' % self.data.simulationDay)
                print(self.data.Sn)
                print(self.data.SInit)
                print(self.data.SMax)
                print(self.data.simuType)
                #print('Flex Contract net day production: %(1)g kg H2. Max flex capacity per day: %(2)g kg H2.' % {'1': self.data.cFlexDay+self.data.cFlexDayAS, '2': (1-self.data.alphaFix-self.data.ASgammaDownFix-self.data.ASgammaUpFix)*self.data.pPn*len(self.data.lamEl)} )
                return
        
    def _load_data(self):
        # General model parameters        
        self.data.grbOutput = False # Suppress diagnostic output
        self.data.DualReductions = 1 # Set to 1 once done with debugging.
        
        self.data.simulationDay = 1 # Internal knowledge of the simulation day for error reporting.
        
        self.data.optimizationMethod = 'Deterministic'
        #self.data.ASCoOpt = False
        self.data.ASFix = False
        self.data.ASDelivery = False   
        self.data.ASRobustCoOpt = False
        
        # Non Delivery (ND) 
        self.data.NDPenalty = False
        self.data.NDRTPenalty = False
        self.data.NDRTFrac = 0.0
        self.data.lamND = 1
        #self.data.lamNDFix = 100.0
        #self.data.lamNDFlex = 100.0
        
        # Block order data
        self.data.BlockOrder = False
        #self.data.BlockOrderFlex = False
        # J is the block order matrix, in this example with 3 hour blocks but 
        # it can be changed in the calling script
        self.data.blockSize = 3
        self.data.disableTau = 1 # one for enable, zero for disable

        self.data.alphaFlex = 0.3 # Flex average electrolyzer load
        self.data.alphaFix = 0.3 # Fix electrolyzer load
        
        self.data.lamEl = [1]*24 # Day ahead prices. To be updated by outside function.  
        
        self.data.Tau = 0.00 # To be updated
        self.data.pPn = 0.0
        self.data.Sn = 0.0
        
        self.data.wV = 0.0
        
        self.data.simuType = ''
        
        self.data.pPInit = 0 # Assume that the electrolyzer starts at 0 production, when the simulations starts
        
        self.data.SMinMaxFrac = 0.0
        
        self.data.elecMWhH2 = 0.050 # MWh electricity per kg H2 produced
        
        # Storage parameters
        self.data.etaComp = 0.80 # Compressor efficiency
        self.data.P2 = 200.0 # Storage pressure in bar
        self.data.P1 = 30.0 # Electrolyzer output pressure in bar
        # Compressor work for compressing 1 kg of hydrogen
        self.data.DW = (1/self.data.etaComp)*math.log(self.data.P2/self.data.P1)*3.292*10**(-4)
        
        # Block order production parameters
#        self.data.J = 8 # Block order duration hours
#        self.data.pPBlockTot = self.data.pPn*(self.data.alphaFlex+self.data.alphaFix)*0.5*24 # Block order total consumption
#        if self.data.BlockOrder == True:
#            self.data.lamElBlock = [1]*24 # These can be reg. forecast or perfect forecast depending on clearing method.
        
        
        # AS data
        self.data.ASgammaUpMax = 1.0
        self.data.ASgammaDownMax = 1.0
        self.data.ASgammaUpFix = 0.0
        self.data.ASgammaDownFix = 0.0
        self.data.lamAsDown = 0
        self.data.lamAsUp = 0
        self.data.yAsUp = 0
        self.data.yAsDown = 0
        self.data.yAsUpRobust = 0
        self.data.yAsDownRobust = 0
        
    def _build_model(self):
        self.model = gb.Model()
        self.model.params.OutputFlag = self.data.grbOutput # Suppress diagnostic output
        self.model.params.DualReductions = self.data.DualReductions 
        self._build_variables()
        self._build_objective()
        self._build_constraints()
    
    def _build_variables(self):
        m = self.model
        self.data.tSet = list(range(0,len(self.data.lamEl)))
        tSet = self.data.tSet
        
        ### Data which is calculated based on data, which might be updated
        self.data.cFlexDay = self.data.alphaFlex*self.data.pPn*len(self.data.lamEl) # Flex consumption per day
        self.data.cFlexMax = self.data.pPn # Max consumption per hour for the flexible contract
        self.data.cFix = {}
        for t in self.data.tSet:
            self.data.cFix[t] = self.data.alphaFix*self.data.pPn
        #self.data.cFixDemand = self.data.cFix
        #print(self.data.SMinMaxFrac)
        self.data.SMin = self.data.SMinMaxFrac*self.data.Sn
        self.data.SMax = (1.0-self.data.SMinMaxFrac)*self.data.Sn

        self.data.chargSMax = self.data.Sn
        if self.data.simulationDay == 1:
            self.data.SInit = self.data.SMin # Assume storage starts at Smin
        
        ### General variables
        self.variables.pB = {} # Electricity bought
        self.variables.pP = {} # hydrogen produced in kg
        self.variables.pPDAtot = {}
        self.variables.cFlex = {} # Flex hydrogen demand variable
        if self.data.ASDelivery == False: # dpP will be dependent on k if this is 'True'        
            self.variables.dpP = {} # Ramp variable for pP, dpP[t]
            self.variables.pPtot = {}
            
            
        for t in tSet:
            self.variables.pB[t] = m.addVar(lb=0.0, name='pB.'+str(t))
            self.variables.pP[t] = m.addVar(lb=0.0, ub=self.data.pPn, name='pP.'+str(t))
            self.variables.pPDAtot[t] = m.addVar(lb=0.0, ub=self.data.pPn, name='pPDAtot.'+str(t))
            self.variables.cFlex[t] = m.addVar(lb=0.0, ub=self.data.cFlexMax, name='cFlex.'+str(t))
            if self.data.ASDelivery == False:             
                self.variables.dpP[t] = m.addVar(name='dpP.'+str(t))
                self.variables.pPtot[t] = m.addVar(lb=0.0, ub=self.data.pPn, name='pPtot.'+str(t))
                
                
                

        ### Storage variables                               
        self.variables.S = {} # Storage SOC (State Of Charge)
        self.variables.pD = {} # Storage discharge
        self.variables.pC = {} # Storage charge
        self.variables.yD = {} # Binary discharge variable. Discharge when yD[t] = 1.
        self.variables.pBS = {} # Compressor energy for storage
        for t in tSet:
            if t == tSet[-1]: # The start and end points must respect SMin and SMax
                self.variables.S[t] = m.addVar(lb=self.data.SMin, ub=self.data.SMax, name='S.'+str(t))
            if t in list(range(tSet[0],tSet[-1])): # All other points in time can utilize the full storage volume
                self.variables.S[t] = m.addVar(lb=0, ub=self.data.Sn, name='S.'+str(t))
            self.variables.pD[t] = m.addVar(lb=0.0, ub=gb.GRB.INFINITY, name='pD.'+str(t))
            self.variables.pC[t] = m.addVar(lb=0.0, ub=gb.GRB.INFINITY, name='pC.'+str(t))
            self.variables.yD[t] = m.addVar(vtype=gb.GRB.BINARY, name='yD.'+str(t))
            self.variables.pBS[t] = m.addVar(lb=0.0, ub=gb.GRB.INFINITY, name='pBS.'+str(t))
        
        ### AS Specific variables
        if self.data.ASDelivery == True:
            kSet = range(0,len(self.data.yAsDown[1]))
            self.variables.ASgammaUp = {}
            self.variables.ASgammaDown = {}
            self.variables.pPAsEx = {} # Delete?
            self.variables.EpPAsUp = {}
            self.variables.EpPAsDn = {}
            self.variables.pPtot = {} # Total hydrogen production. Used when delivering DA and AS production simultaneously
            self.variables.dpP = {} # dpP is dependent on k now
            for t in tSet:
                self.variables.ASgammaUp[t] = m.addVar(lb=0.0, ub=self.data.ASgammaUpMax, name='ASgammaUp.'+str(t))
                self.variables.ASgammaDown[t] = m.addVar(lb=0.0, ub=self.data.ASgammaDownMax, name='ASgammaDown.'+str(t))
                self.variables.pPAsEx[t] = m.addVar(lb=-gb.GRB.INFINITY, ub=gb.GRB.INFINITY, name='pPAsEx.'+str(t)) # Delete?
                # Expected produciton is per forecasting scenario k
                self.variables.EpPAsUp[t] = {}
                self.variables.EpPAsDn[t] = {}
                self.variables.pPtot[t] = {}
                self.variables.dpP[t] = {}
                for k in kSet:                
                    self.variables.EpPAsUp[t][k] = m.addVar(lb=-gb.GRB.INFINITY, ub=gb.GRB.INFINITY, name='EpPAsUp.'+str(t)+'.'+str(k))
                    self.variables.EpPAsDn[t][k] = m.addVar(lb=-gb.GRB.INFINITY, ub=gb.GRB.INFINITY, name='EpPAsDn.'+str(t)+'.'+str(k))
                    self.variables.pPtot[t][k] = m.addVar(lb=0.0, ub=self.data.pPn, name='pPtot.'+str(t)+'.'+str(k))
                    self.variables.dpP[t][k] = m.addVar(lb=-gb.GRB.INFINITY, ub=gb.GRB.INFINITY, name='dpP.'+str(t)+'.'+str(k))
        
        ### Block order specific variables
#        if self.data.BlockOrder == True:
#            J = self.data.J
#            jSet = list(range(0,24-J))
#            self.variables.pPBlocks = {}
#            self.variables.pPBlock = {}
#            self.variables.pBBlock = {}
#            self.variables.uBlock = {}
#            for t in tSet:
#                self.variables.pBBlock[t] = m.addVar(lb=0.0, name='pBBlock.'+str(t))
#                self.variables.pPBlock[t] = m.addVar(lb=0.0, ub=self.data.pPn, name='pPBlock.'+str(t))
#            for j in jSet: # j specifies the start hour of a particular block j
#                self.variables.uBlock[j] = m.addVar(vtype=gb.GRB.BINARY, name='uBlock.'+str(j))
#                self.variables.pPBlocks[j] = {}
#                for t in tSet:
#                    if t in list(range(j,j+J)):
#                        self.variables.pPBlocks[j][t] = self.data.pPBlockTot/J
#                    else: 
#                        self.variables.pPBlocks[j][t] = 0
                    

        
        if self.data.ASRobustCoOpt == True:# and self.data.NDPenalty == False):
            kRSet = list(range(0,len(self.data.yAsUpRobust[1])))                            
            self.variables.Sk = {} # Storage SOC (State Of Charge)
            self.variables.dSk = {}
            self.variables.pPAsk = {}
            for k in kRSet:
                self.variables.Sk[k] = {} 
                self.variables.dSk[k] = {}
                self.variables.pPAsk[k] = {}
                for t in tSet:
                    if t == tSet[-1]: # The end point must respect SMin and SMax
                        self.variables.Sk[k][t] = m.addVar(lb=self.data.SMin, ub=self.data.SMax, name='S.'+str(k)+'.'+str(t))
                    if t in list(range(tSet[0],tSet[-1])): # All other points in time can utilize the full storage volume
                        self.variables.Sk[k][t] = m.addVar(lb=0, ub=self.data.Sn, name='S.'+str(k)+'.'+str(t))
                    self.variables.dSk[k][t] = m.addVar(lb=-gb.GRB.INFINITY, ub=gb.GRB.INFINITY, name='dSk.'+str(k)+'.'+str(t))
                    self.variables.pPAsk[k][t] = m.addVar(lb=-gb.GRB.INFINITY, ub=gb.GRB.INFINITY, name='pPAsEx.'+str(k)+'.'+str(t))
        
#        if (self.data.ASRobustCoOpt == True and self.data.NDPenalty == True):
#            kRSet = list(range(0,len(self.data.yAsUpRobust[1])))                            
#            kSet = range(0,len(self.data.lamAsUp[1]))            
#            self.variables.Sk = {} # Storage SOC (State Of Charge)
#            self.variables.dSk = {}
#            self.variables.pPAsk = {}
#            for k in kSet:
#                self.variables.Sk[k] = {} # Storage SOC (State Of Charge)
#                self.variables.dSk[k] = {}
#                self.variables.pPAsk[k] = {}
#                for kR in kRSet:
#                    self.variables.Sk[k][kR] = {} 
#                    self.variables.dSk[k][kR] = {}
#                    self.variables.pPAsk[k][kR] = {}
#                    for t in tSet:
#                        if t == 23: # The end point must respect SMin and SMax
#                            self.variables.Sk[k][kR][t] = m.addVar(lb=self.data.SMin, ub=self.data.SMax, name='S.'+str(k)+'.'+str(kR)+'.'+str(t))
#                        if t in list(range(0,23)): # All other points in time can utilize the full storage volume
#                            self.variables.Sk[k][kR][t] = m.addVar(lb=0, ub=self.data.Sn, name='S.'+str(k)+'.'+str(kR)+'.'+str(t))
#                        self.variables.dSk[k][kR][t] = m.addVar(lb=-gb.GRB.INFINITY, ub=gb.GRB.INFINITY, name='dSk.'+str(k)+'.'+str(kR)+'.'+str(t))
#                        self.variables.pPAsk[k][kR][t] = m.addVar(lb=-gb.GRB.INFINITY, ub=gb.GRB.INFINITY, name='pPAsEx.'+str(k)+'.'+str(kR)+'.'+str(t))
#           
        
        if self.data.NDPenalty == True:
            #kSet = range(0,len(self.data.lamAsUp[1]))
            #print(kSet)
            self.variables.pPND = {}
            self.variables.SkND = {} # Storage SOC (State Of Charge)
            self.variables.dSkND = {}
            self.variables.pPAskND = {}
            #self.variables.pPNDFix = {}
            #self.variables.pPNDFlex = {}
            #self.variables.cFlex = {} # Flex hydrogen demand variable
            #self.variables.cFixWND = {}
            for k in kSet:
                self.variables.pPND[k] = {}
                self.variables.SkND[k] = {} 
                self.variables.dSkND[k] = {}
                self.variables.pPAskND[k] = {}
                #self.variables.pPNDFix[k] = {}
                #self.variables.pPNDFlex[k] = m.addVar(name='pPNDFlex.'+str(k))
                #self.variables.cFlex[k] = {}
                #self.variables.cFixWND[k] = {}
                for t in tSet:
                    self.variables.pPND[k][t] = m.addVar(lb=0.0,ub=gb.GRB.INFINITY, name='pPND.'+str(k)+'.'+str(t))
                    #self.variables.pPNDFix[k][t] = m.addVar(name='pPNDFix.'+str(k)+'.'+str(t))
                    #self.variables.pPNDFlex[t] = m.addVar(name='pPNDFlex.'+str(k)+'.'+str(t))
                    #self.variables.cFlex[k][t] = m.addVar(name='cFlex.'+str(k)+'.'+str(t))
                    #self.variables.cFixWND[k][t] = m.addVar(name='cFixWND.'+str(k)+'.'+str(t))
                    if t == tSet[-1]: # The end point must respect SMin and SMax
                        self.variables.SkND[k][t] = m.addVar(lb=self.data.SMin, ub=self.data.SMax, name='SkND.'+str(k)+'.'+str(t))
                    if t in list(range(tSet[0],tSet[-1])): # All other points in time can utilize the full storage volume
                        self.variables.SkND[k][t] = m.addVar(lb=0, ub=self.data.Sn, name='S.'+str(k)+'.'+str(t))
                    self.variables.dSkND[k][t] = m.addVar(lb=-gb.GRB.INFINITY, ub=gb.GRB.INFINITY, name='dSkND.'+str(k)+'.'+str(t))
                    self.variables.pPAskND[k][t] = m.addVar(lb=-gb.GRB.INFINITY, ub=gb.GRB.INFINITY, name='pPAsExkND.'+str(k)+'.'+str(t))
        
            
        # Integrate new variables
        m.update()
    
    def _build_objective(self):
        tSet = self.data.tSet
        pB = self.variables.pB
        lamEl = self.data.lamEl
        
#        if self.data.BlockOrder == True:
#            pBBlock = self.variables.pBBlock
#            lamElBlock = self.data.lamElBlock
        
        if self.data.ASDelivery == True:
            pPn = self.data.pPn        
            elecMWhH2 = self.data.elecMWhH2 
            yAsUp = self.data.yAsUp
            yAsDown = self.data.yAsDown
            lamAsDown = self.data.lamAsDown
            lamAsUp = self.data.lamAsUp
            ASgammaUp = self.variables.ASgammaUp
            ASgammaDown = self.variables.ASgammaDown 
            DW = self.data.DW
        
        if (self.data.optimizationMethod == 'Deterministic' and 
            self.data.ASDelivery == False):# and self.data.BlockOrder == False):
                
            self.model.setObjective(
                gb.quicksum(pB[t]*lamEl[t]
                + self.variables.dpP[t]*self.data.Tau*self.data.disableTau for t in tSet)
                - self.variables.S[tSet[-1]]*self.data.wV,
                gb.GRB.MINIMIZE)

#        elif (self.data.optimizationMethod == 'Deterministic' and 
#            self.data.ASDelivery == False and self.data.BlockOrder == True):
#
#            self.model.setObjective(
#                gb.quicksum(pB[t]*lamEl[t] + pBBlock[t]*lamElBlock[t]
#                + self.variables.dpP[t]*self.data.Tau for t in tSet)
#                - self.variables.S[23]*self.data.wV,
#                gb.GRB.MINIMIZE)
        
        # NOT IN USE        
        elif self.data.optimizationMethod == 'Stochastic' and self.data.ASDelivery == False:

            kSet = range(0,len(lamEl[1]))
            self.model.setObjective(
                1/len(kSet)*gb.quicksum(gb.quicksum(pB[t]*lamEl[t][k] for t in tSet) for k in kSet)
                + gb.quicksum(self.variables.dpP[t]*self.data.Tau for t in tSet)
                - self.variables.S[23]*self.data.wV,
                gb.GRB.MINIMIZE)
                
        elif (self.data.optimizationMethod == 'Deterministic' and self.data.ASDelivery == True
            and self.data.NDPenalty == False):

            kSet = range(0,len(lamAsUp[1]))
            self.model.setObjective(
                gb.quicksum(pB[t]*lamEl[t] for t in tSet)
                + 1/len(kSet)*gb.quicksum(gb.quicksum((
                (elecMWhH2+DW)*pPn*ASgammaDown[t]*lamAsDown[t][k]*yAsDown[t][k] 
                - elecMWhH2*pPn*ASgammaUp[t]*lamAsUp[t][k]*yAsUp[t][k]) 
                + self.variables.dpP[t][k]*self.data.Tau for t in tSet) for k in kSet)
                - self.variables.S[23]*self.data.wV,
                gb.GRB.MINIMIZE)               
                
        elif (self.data.optimizationMethod == 'Deterministic' and self.data.ASDelivery == True
            and self.data.NDPenalty == True and self.data.NDRTPenalty == False):
            
            kSet = range(0,len(lamAsUp[1]))
            self.model.setObjective(
                gb.quicksum(pB[t]*lamEl[t] for t in tSet)
                + 1/len(kSet)*gb.quicksum(gb.quicksum((
                (elecMWhH2+DW)*pPn*ASgammaDown[t]*lamAsDown[t][k]*yAsDown[t][k] 
                - elecMWhH2*pPn*ASgammaUp[t]*lamAsUp[t][k]*yAsUp[t][k]) 
                + self.variables.dpP[t][k]*self.data.Tau 
                + self.data.lamND*self.variables.pPND[k][t] # ND penalty 
                for t in tSet) for k in kSet)
                - self.variables.S[23]*self.data.wV,
                gb.GRB.MINIMIZE)
                
        elif (self.data.optimizationMethod == 'Deterministic' and self.data.ASDelivery == True
            and self.data.NDPenalty == True and self.data.NDRTPenalty == True):
            
            kSet = range(0,len(lamAsUp[1]))
            self.model.setObjective(
                gb.quicksum(pB[t]*lamEl[t] for t in tSet)
                + 1/len(kSet)*gb.quicksum(gb.quicksum((
                (elecMWhH2+DW)*pPn*ASgammaDown[t]*lamAsDown[t][k]*yAsDown[t][k] 
                - elecMWhH2*pPn*ASgammaUp[t]*lamAsUp[t][k]*yAsUp[t][k]) 
                + self.variables.dpP[t][k]*self.data.Tau 
                + 1/len(tSet)*gb.quicksum(lamEl[t] for t in tSet)*elecMWhH2
                    *self.data.NDRTFrac*self.variables.pPND[k][t] # ND penalty , *yAsDown[t][k] + lamAsUp[t][k]*yAsUp[t][k]
                for t in tSet) for k in kSet)
                - self.variables.S[23]*self.data.wV,
                gb.GRB.MINIMIZE) 
                
        else:
            print('Objective function not defined!')
        
    def _build_constraints(self):
        m = self.model
        tSet = self.data.tSet
        
        ### Import variables
        pB = self.variables.pB
        pP = self.variables.pP
        cFlex = self.variables.cFlex
        pC = self.variables.pC
        pD = self.variables.pD
        yD = self.variables.yD
        S = self.variables.S
        dpP = self.variables.dpP
        pBS = self.variables.pBS
        pPDAtot = self.variables.pPDAtot
        pPtot = self.variables.pPtot

        ### Import data
        cFix = self.data.cFix
        cFlexDay = self.data.cFlexDay
        chargSMax = self.data.chargSMax
        SInit = self.data.SInit
        elecMWhH2 = self.data.elecMWhH2
        #etaComp = self.data.etaComp
        #P2 = self.data.P2 
        #P1 = self.data.P1
        pPn = self.data.pPn
       
        if self.data.ASDelivery == True:
            yAsDown = self.data.yAsDown
            yAsUp = self.data.yAsUp
            ASgammaDown = self.variables.ASgammaDown
            ASgammaUp = self.variables.ASgammaUp
            ASgammaDownFix = self.data.ASgammaDownFix
            ASgammaUpFix = self.data.ASgammaUpFix
            
            #pPAsEx = self.variables.pPAsEx
            EpPAsUp = self.variables.EpPAsUp
            EpPAsDn = self.variables.EpPAsDn
            
            kSet = range(0,len(yAsDown[1])) #kSet is used for expected AS production
            
        if self.data.NDPenalty == True:
            kSet = range(0,len(yAsDown[1]))
            
            pPND = self.variables.pPND            
            #pPNDFix = self.variables.pPNDFix
            #pPNDFlex = self.variables.pPNDFlex
            #cFixWND = self.variables.cFixWND
            #cFixDemand = self.data.cFixDemand
            
        # Block Order Cts.
        if self.data.BlockOrder == True:
            J = [list(range(n*self.data.blockSize,(n+1)*self.data.blockSize)) 
                for n in list(range(0,int(24/self.data.blockSize)))]
            for n in list(range(0,len(J))):
                if len(J[n]) > 1:
                    for j in J[n][0:-1]:
                        m.addConstr(pP[j] == pP[j+1])
        
        ### General constraints
        self.constraints.elecConsCts = {} # Electricity consumption
        #self.constraints.elecConsBlockCts = {}
        self.constraints.hydBalCts = {} # Hydrogen balance
        self.constraints.pPDAtotCts = {}
        self.constraints.pPtotCts = {}
        #self.constraints.pPBlockCts = {}
        for t in tSet:
            # Day ahead power procurement, the pPBlock part is included 
            # seperateley in the objective function because we in one implemen-
            # tation will clear the market with perfect foresight (because the
            # clearing will work as a flex bid, where NordPool situates the bid
            # position in the day)
            self.constraints.elecConsCts[t] = m.addConstr(pB[t] == 
                elecMWhH2*pP[t] + pBS[t], name='elecConsCts.'+str(t))
#            if self.data.BlockOrder == True:
#                self.constraints.elecConsBlockCts[t] = m.addConstr(pBBlock[t] ==
#                    elecMWhH2*pPBlock[t], name='elecConsBlockCts.'+str(t))
                
                        
            # Total DA position with or without block order
#            if self.data.BlockOrder == True:
#                self.constraints.pPBlockCts[t] = m.addConstr(pPBlock[t] == 
#                    gb.quicksum(uBlock[j]*pPBlocks[j][t] for j in jSet), 
#                    name='pPBlockCts.'+str(t))
#                self.constraints.pPDAtotCts[t] = m.addConstr(pPDAtot[t] ==
#                    pP[t] + pPBlock[t], name='pPDAtotCts.'+str(t) )
            #if self.data.BlockOrder == False:
            self.constraints.pPDAtotCts[t] = m.addConstr(pPDAtot[t] == pP[t], 
                name='pPDAtotCts.'+str(t) )
                    
            # Hydrogen balance equations
            if self.data.ASDelivery == False:
                self.constraints.pPtotCts[t] = m.addConstr(pPtot[t] == 
                    pPDAtot[t], name='pPtotCts.'+str(t))
                self.constraints.hydBalCts[t] =  m.addConstr(pPtot[t] == 
                    cFix[t] + cFlex[t] + pC[t] - pD[t], name='hydBalCts.'+str(t))
            if self.data.ASDelivery == True:
                # pPtot becomes scenario dependent for scenarios k
                self.constraints.pPtotCts[t] = {}
                for k in kSet:                
                    self.constraints.pPtotCts[t][k] = m.addConstr(pPtot[t][k] == 
                        pPDAtot[t] + EpPAsUp[t][k] + EpPAsDn[t][k], 
                        name='pPtotCts.'+str(t)+'.'+str(k) )
            if (self.data.ASDelivery == True and self.data.NDPenalty == False):
                self.constraints.hydBalCts[t] =  m.addConstr( 
                    1/len(kSet)*gb.quicksum(pPtot[t][k] for k in kSet) == 
                    cFix[t] + cFlex[t] + pC[t] - pD[t], name='hydBalCts.'+str(t))
            if (self.data.ASDelivery == True and self.data.NDPenalty == True):
                self.constraints.hydBalCts[t] =  m.addConstr( 
                    1/len(kSet)*gb.quicksum(pPtot[t][k] for k in kSet) == 
                    -1/len(kSet)*gb.quicksum(pPND[k][t] for k in kSet) 
                    + cFix[t] + cFlex[t] 
                    + pC[t] - pD[t], name='hydBalCts.'+str(t))
            

        ### Contracts consumption constraint
#        if self.data.NDPenalty == False:
        m.addConstr(gb.quicksum(cFlex[t] for t in tSet) == cFlexDay,
                    name='cFlexCts')
#        if self.data.NDPenalty == True:
#            #kSet = range(0,len(yAsDown[1]))
#            self.constraints.cFlexNDCts = {}
#            self.constraints.cFixNDCts = {}
#            for k in kSet:
#                self.constraints.cFlexNDCts[k] = m.addConstr(gb.quicksum(
#                    cFlex[k][t] for t in tSet) == cFlexDay - pPNDFlex[k], 
#                    name='cFlexCts.'+str(k))
#                self.constraints.cFixNDCts[k] = {}
#                for t in tSet:
#                    self.constraints.cFixNDCts[k][t] = m.addConstr(cFixWND[k][t]
#                        == cFixDemand[t] - pPNDFix[k][t])

        ### Block order constraint, only one block order can be chosen
#        if self.data.BlockOrder == True:
#            m.addConstr(gb.quicksum(uBlock[j] for j in jSet) == 1, 
#                        name='blockOrderBinaryCts')
            
            
        
        ### AS delivery constraints
        if self.data.ASDelivery == True:        
            self.constraints.pPMinCts = {} # Min pP constraint
            self.constraints.pPMaxCts = {} # Max pP constraint
            self.constraints.ASgammaSumCts = {} # Sum over gamma constraint
            self.constraints.ASgammaDownFixCts = {} # If we simulate fixed gamma
            self.constraints.ASgammaUpFixCts = {} # If we simulate fixed gamma
        
            self.constraints.EpPAsUpCts = {} # Expected AS up production
            self.constraints.EpPAsDnCts = {} # Expected AS down production

            
            for t in tSet:
                self.constraints.pPMinCts[t] = m.addConstr(pP[t] 
                >= pPn*ASgammaUp[t],
                name='pPMinCts.'+str(t))
                
                self.constraints.pPMaxCts[t] = m.addConstr(pP[t] 
                <= (1.0-ASgammaDown[t])*pPn, 
                name='pPMaxCts.'+str(t))
                
                self.constraints.ASgammaSumCts[t] = m.addConstr(
                ASgammaDown[t]+ASgammaUp[t] <= 1.0, 
                name='ASgammaSumCts.'+str(t))
                
                if self.data.ASFix == True:
                    self.constraints.ASgammaDownFixCts[t] = m.addConstr(ASgammaDown[t] == ASgammaDownFix, name='ASgammaDownFixCts.'+str(t))
                    self.constraints.ASgammaUpFixCts[t] = m.addConstr(ASgammaUp[t] == ASgammaUpFix, name='ASgammaUpFixCts.'+str(t))
                
                # EpPAsUp and EpPAsDn are the expected productions of AS hydrogen per scenario k
                self.constraints.EpPAsUpCts[t] = {}
                self.constraints.EpPAsDnCts[t] = {}
                for k in kSet:
                    self.constraints.EpPAsUpCts[t][k] = m.addConstr(EpPAsUp[t][k] ==
                        -pPn*ASgammaUp[t]*yAsUp[t][k],
                        name='EpPAsUpCts.'+str(t)+'.'+str(k))
                    self.constraints.EpPAsDnCts[t] = m.addConstr(EpPAsDn[t][k] ==
                        pPn*ASgammaDown[t]*yAsDown[t][k],
                        name='EpPAsDnCts.'+str(t)+'.'+str(k))
      
        ### Storage constraints   
        self.constraints.chargCts = {} # Storage Charging
        self.constraints.dchargCts = {} # Storage Disharging
        self.constraints.storCts = {} # Storage energy balance
        self.constraints.lossChargCts = {} # Storage energy consumption
        for t in tSet:
            self.constraints.chargCts[t] = m.addConstr(pC[t] <= 
            (1-yD[t])*chargSMax, name='chargCts.'+str(t))
            
            self.constraints.dchargCts[t] = m.addConstr(pD[t] <= 
            yD[t]*chargSMax, name='dchargCts.'+str(t))
            
            if t == tSet[0]:
                self.constraints.storCts[t] = m.addConstr( S[t] - SInit == 
                pC[t] - pD[t], name='storCts.'+str(t))
            if t > tSet[0]:
                self.constraints.storCts[t] = m.addConstr( S[t] - S[t-1] == 
                pC[t] - pD[t], name='storCts.'+str(t))
            
            self.constraints.lossChargCts[t] = m.addConstr(pBS[t] == 
            pC[t]*self.data.DW, 
            name='lossChargCts.'+str(t))           

        ### Absolute value of dpP
        #################### Does pPInit include AS production?
        self.constraints.rampHiCts = {}
        self.constraints.rampLoCts = {}
        pPInit = self.data.pPInit
        
        # If we have no AS Delivery, then dpP will be scenario independent (this strategy contains no scenarios)
        if self.data.ASDelivery == False:        
            for t in tSet:
                if t == tSet[0]:
                    self.constraints.rampHiCts[t] = m.addConstr( (pPtot[t]-pPInit) <= 
                    dpP[t], name='rampHiCts.'+str(t))        
                    self.constraints.rampLoCts[t] = m.addConstr( -(pPtot[t]-pPInit) 
                    <= dpP[t], name='rampLoCts.'+str(t))
                if t > tSet[0]:
                    self.constraints.rampHiCts[t] = m.addConstr( (pPtot[t]-pPtot[t-1]) <= 
                    dpP[t], name='rampHiCts.'+str(t))        
                    self.constraints.rampLoCts[t] = m.addConstr( -(pPtot[t]-pPtot[t-1]) 
                    <= dpP[t], name='rampLoCts.'+str(t))
        
        # In case of AS delivery, then dpP will be dependent on scenarios.
        if self.data.ASDelivery == True:
            for t in tSet:
                for k in kSet:
                    self.constraints.rampHiCts[t] = {}
                    self.constraints.rampLoCts[t] = {}
                    if t == tSet[0]:
                        self.constraints.rampHiCts[t][k] = m.addConstr( (pPtot[t][k]-pPInit) <= 
                            dpP[t][k], name='rampHiCts.'+str(t)+'.'+str(k))        
                        self.constraints.rampLoCts[t][k] = m.addConstr( -(pPtot[t][k]-pPInit) 
                            <= dpP[t][k], name='rampLoCts.'+str(t)+'.'+str(k))
                    if t > tSet[0]:
                        self.constraints.rampHiCts[t][k] = m.addConstr( (pPtot[t][k]-pPtot[t-1][k]) <= 
                            dpP[t][k], name='rampHiCts.'+str(t)+'.'+str(k))        
                        self.constraints.rampLoCts[t][k] = m.addConstr( -(pPtot[t][k]-pPtot[t-1][k]) 
                            <= dpP[t][k], name='rampLoCts.'+str(t)+'.'+str(k))
                

        ### Robust AS CoOpt constraints
        if self.data.ASRobustCoOpt == True:# and self.data.NDPenalty == False):
            yAsUpRobust = self.data.yAsUpRobust
            yAsDownRobust = self.data.yAsDownRobust
            kRSet = list(range(0,len(yAsDownRobust[1])))

            Sk = self.variables.Sk
            dSk = self.variables.dSk
            pPAsk = self.variables.pPAsk
            
            self.constraints.storCtsK = {} # Storage energy balance
            self.constraints.hydBalCtsK = {} # Hydrogen balance
            self.constraints.pPAsCtsK = {} # AS production for the k scenarios
            for k in kRSet:
                self.constraints.storCtsK[k] = {} # Storage energy balance
                self.constraints.hydBalCtsK[k] = {} # Hydrogen balance
                self.constraints.pPAsCtsK[k] = {} # Expected AS production
                for t in tSet:
                    #if self.data.NDPenalty == False:
                    self.constraints.hydBalCtsK[k][t] =  m.addConstr(pP[t] + pPAsk[k][t]
                        == cFix[t] + cFlex[t] + dSk[k][t], name='hydBalCtsK.'+str(k)+'.'+str(t))
#                    if self.data.NDPenalty == True:
#                        # kRSet needs to be equal to kSet in this case, which
#                        # means that the robust set has to be equal to the 
#                        # normal scenario set.
#                        self.constraints.hydBalCtsK[k][t] =  m.addConstr(pP[t] + pPAsk[k][t]
#                            == cFix[t] + cFlex[t] + pPND[k][t] + dSk[k][t], 
#                            name='hydBalCtsK.'+str(k)+'.'+str(t))                        
                        
                    self.constraints.pPAsCtsK[k][t] =  m.addConstr(pPAsk[k][t] ==
                    pPn*(ASgammaDown[t]*yAsDownRobust[t][k]-ASgammaUp[t]*yAsUpRobust[t][k]),
                    name='pPAsExCts.'+str(k)+'.'+str(t))    
      
                    if t == tSet[0]:
                        self.constraints.storCtsK[k][t] = m.addConstr( Sk[k][t] - SInit == 
                        dSk[k][t], name='storCts.'+str(k)+'.'+str(t))
                    if t > tSet[0]:
                        self.constraints.storCtsK[k][t] = m.addConstr( Sk[k][t] - Sk[k][t-1] == 
                        dSk[k][t], name='storCts.'+str(k)+'.'+str(t))
                        
                        
        ### Robust AS CoOpt ND constraints
#        if (self.data.ASRobustCoOpt == True and self.data.NDPenalty == True):
#            yAsUpRobust = self.data.yAsUpRobust
#            yAsDownRobust = self.data.yAsDownRobust
#            kRSet = list(range(0,len(yAsDownRobust[1])))
#
#            Sk = self.variables.Sk
#            dSk = self.variables.dSk
#            pPAsk = self.variables.pPAsk
#            
#            self.constraints.storCtsK = {} # Storage energy balance
#            self.constraints.hydBalCtsK = {} # Hydrogen balance
#            self.constraints.pPAsCtsK = {} # AS production for the k scenarios
#            for k in kSet:
#                self.constraints.storCtsK[k] = {} # Storage energy balance
#                self.constraints.hydBalCtsK[k] = {} # Hydrogen balance
#                self.constraints.pPAsCtsK[k] = {} # Expected AS production
#                for kR in kRSet:
#                    self.constraints.storCtsK[k][kR] = {} # Storage energy balance
#                    self.constraints.hydBalCtsK[k][kR] = {} # Hydrogen balance
#                    self.constraints.pPAsCtsK[k][kR] = {} # Expected AS production
#                    for t in tSet:
#                        # kRSet needs to be equal to kSet in this case, which
#                        # means that the robust set has to be equal to the 
#                        # normal scenario set.
#                        self.constraints.hydBalCtsK[k][kR][t] =  m.addConstr(pP[t] + pPAsk[k][kR][t]
#                            == cFix[t] + cFlex[t] + dSk[k][kR][t], #- pPND[k][t]
#                            name='hydBalCtsK.'+str(k)+'.'+str(t))                        
#                            
#                        self.constraints.pPAsCtsK[k][kR][t] =  m.addConstr(pPAsk[k][kR][t] ==
#                        pPn*(ASgammaDown[t]*yAsDownRobust[t][kR]-ASgammaUp[t]*yAsUpRobust[t][kR]),
#                        name='pPAsExCts.'+str(k)+'.'+str(t))    
#          
#                        if t == tSet[0]:
#                            self.constraints.storCtsK[k][kR][t] = m.addConstr( Sk[k][kR][t] - SInit == 
#                            dSk[k][kR][t], name='storCts.'+str(k)+'.'+str(t))
#                        if t > tSet[0]:
#                            self.constraints.storCtsK[k][kR][t] = m.addConstr( Sk[k][kR][t] - Sk[k][kR][t-1] == 
#                            dSk[k][kR][t], name='storCts.'+str(k)+'.'+str(t))
                        
                        
                        
        ### AS CoOpt ND constraints
        if self.data.NDPenalty == True:
            yAsUp = self.data.yAsUp
            yAsDown = self.data.yAsDown
            #kRSet = list(range(0,len(yAsDown[1])))

            SkND = self.variables.SkND
            dSkND = self.variables.dSkND
            pPAskND = self.variables.pPAskND
            
            self.constraints.storCtsKND = {} # Storage energy balance
            self.constraints.hydBalCtsKND = {} # Hydrogen balance
            self.constraints.pPAsCtsKND = {} # AS production for the k scenarios
            for k in kSet:
                self.constraints.storCtsKND[k] = {} # Storage energy balance
                self.constraints.hydBalCtsKND[k] = {} # Hydrogen balance
                self.constraints.pPAsCtsKND[k] = {} # Expected AS production
                for t in tSet:
                    # kRSet needs to be equal to kSet in this case, which
                    # means that the robust set has to be equal to the 
                    # normal scenario set.
                    self.constraints.hydBalCtsKND[k][t] =  m.addConstr(pP[t] + pPAskND[k][t]
                        == cFix[t] + cFlex[t] - pPND[k][t] + dSkND[k][t], 
                        name='hydBalCtsKND.'+str(k)+'.'+str(t))                        
                        
                    self.constraints.pPAsCtsKND[k][t] =  m.addConstr(pPAskND[k][t] ==
                    pPn*(ASgammaDown[t]*yAsDown[t][k]-ASgammaUp[t]*yAsUp[t][k]),
                    name='pPAsExCtsKND.'+str(k)+'.'+str(t))    

                    
                    if t == tSet[0]:
                        self.constraints.storCtsKND[k][t] = m.addConstr( SkND[k][t] - SInit == 
                        dSkND[k][t], name='storCtsKND.'+str(k)+'.'+str(t))
                    if t > tSet[0]:
                        self.constraints.storCtsKND[k][t] = m.addConstr( SkND[k][t] - SkND[k][t-1] == 
                        dSkND[k][t], name='storCtsKND.'+str(k)+'.'+str(t))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
