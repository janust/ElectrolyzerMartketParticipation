# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 08:51:38 2016

@author: Janus
"""

### Day iteration

# Make into class with easier access to changing variables using expando.
# Make a loop function in class to start loop and return result
# Possible integrate with the store/out of sample hydrogen capculations

# Python standard modules to import
from datetime import timedelta
import gurobipy as gb
import numpy as np

# Own modules to import
from elecOptClass import elecOpt


class expando(object):
    '''
        A small class which can have attributes set
    '''
    pass

class dayIteration: #(days,simuDates,priceWDate,simuType,nBack=0,AsUpDownNoneDict=0,yAsDown=0,yAsUp=0,balPriceDown=0,balPriceUp=0):
    def __init__(self, days, simuDates, priceWDate, simuType,studyCase=''):       
        #from elecOptClass import expando           
        self.data = expando()
        self.parameters = expando()
        
        # Store input args
        self.data.days = days
        self.data.simuDates = simuDates
        self.data.priceWDate = priceWDate
        self.parameters.simuType = simuType
        self.parameters.studyCase = studyCase
        
        # Load Optimizer Class
        self.elecOpt = elecOpt() 
        
        # Load data and update parameters
        self._load_data()
        self._load_model_parameters()
        self._update_parameters()
        
        # Variable to dump deficit FlexProd
        #self.data.unservedFlexProdUp = 0
        #self.data.unservedFlexProdDn = 0
        
        
    def _load_data(self):
        self.data.tSet = list(range(0,24))
        
        self.data.AsUpDownNoneDict = 0
        self.data.yAsDown = 0
        self.data.yAsUp = 0
        self.data.balPriceDown = 0
        self.data.balPriceUp = 0
        
        # Used to store the results of the optimization
        self.data.optResults = {    
            'pP': [],
            #'pPBlock': [],
            'pB': [],
            'pBs': [],
            #'pBBlock': [],
            'pPND': [],
            'pPFlare': [],
            'S': [],
            'cFlex': [],
            'objVal': 0,
            'pPAs':[],
            'pPTot':[],
            'pBAs':[],
            'dSAs': [],
            'SAs': [],
            'ASgammaDown': [],
            'ASgammaUp': [],
            'costDA': [],
            'costDAs': [],
            'costAS': [],
            'costTau': [],
            'costND': [],
            'vW': [],
            'beta':     {
                        'dDyn': [],
                        'dSS': [], 
                        'sumDyn': 0,
                        'sumSS':0,
                        'sumTot': 0},
            'Forecasting': {'lamEl': [],
                            'lamAsUp': [],
                            'lamAsDn': [],
                            'yAsUp': [],
                            'yAsDn': [],
                            'lamMeanAs2':[]}
            }
    
    def _load_model_parameters(self):
        # Change model to Stochastic optimization if this is what we use
        self.parameters.ASDelivery = False
        
        self.parameters.BlockOrder = False
        #self.parameters.BlockOrderFlex = False
        self.parameters.blockSize = 3
        self.parameters.disableTau = 1 # 0 to disable, 1 to enable, binary
        
        self.parameters.alphaFix = 0.0
        self.parameters.alphaFlex = 0.0
        self.parameters.pPn = 0
        self.parameters.Sn = 0
        
        self.parameters.NDPenalty = False
        self.parameters.NDRTPenalty = False
        self.parameters.NDRTFrac = 0.0
        self.parameters.lamND = 0.0
                
        self.parameters.ASFix = False # Utilize fixed AS share instead of dynamic co-optimization
        self.parameters.ASgammaUpFix = 0.1
        self.parameters.ASgammaDownFix = 0.1
        
        self.parameters.Tau = 2.0
        
        self.parameters.ASCoOpt = False
        self.parameters.ASRobustCoOpt = False 
        self.parameters.ASRobustPlusCoOpt = False # introducing the extreme case with full up/down reg activation for full secutiry of supply on the battery
        self.parameters.ASgammaUpMax = 1.0
        self.parameters.ASgammaDownMax = 1.0
        self.parameters.nBackASRobust = 0 # Forecasting number of weeks back in time for the AS robustness assesment
        
        self.parameters.AS_SEAS = False
        self.parameters.AS2meanDaysBack = 0
        
        self.parameters.nBack = 0 # Forecasting number of weeks back in time
        
        self.parameters.nBackWW = 14 # Number of days back in time for determining the "water value"
        
        self.parameters.SMinMaxFrac = 0
        

    
    # Create an instance of the optimization model used for simple forecast    
    def _update_parameters(self):    
        
        # Perfect and simple simulations use deterministic optimization
        if self.parameters.simuType == 'Perfect' or self.parameters.simuType == 'Simple':
            self.elecOpt.data.optimizationMethod == 'Deterministic'
        
        self.elecOpt.data.ASDelivery = self.parameters.ASDelivery
        self.elecOpt.data.ASRobustCoOpt = self.parameters.ASRobustCoOpt
        self.elecOpt.data.ASFix = self.parameters.ASFix
        self.elecOpt.data.ASgammaUpFix = self.parameters.ASgammaUpFix
        self.elecOpt.data.ASgammaDownFix = self.parameters.ASgammaDownFix
        self.elecOpt.data.ASgammaUpMax = self.parameters.ASgammaUpMax
        self.elecOpt.data.ASgammaDownMax = self.parameters.ASgammaDownMax
        self.elecOpt.data.Tau = self.parameters.Tau
        self.elecOpt.data.BlockOrder = self.parameters.BlockOrder
        self.elecOpt.data.blockSize = self.parameters.blockSize
        self.elecOpt.data.NDPenalty = self.parameters.NDPenalty
        self.elecOpt.data.NDRTPenalty = self.parameters.NDRTPenalty
        self.elecOpt.data.NDRTFrac = self.parameters.NDRTFrac
        self.elecOpt.data.lamND = self.parameters.lamND
        self.elecOpt.data.alphaFix = self.parameters.alphaFix
        self.elecOpt.data.alphaFlex = self.parameters.alphaFlex
        self.elecOpt.data.pPn = self.parameters.pPn
        self.elecOpt.data.Sn = self.parameters.Sn*self.parameters.pPn # Sn is in hours of full production
        self.elecOpt.data.disableTau = self.parameters.disableTau
        self.elecOpt.data.SMinMaxFrac = self.parameters.SMinMaxFrac
        self.elecOpt.data.simuType = self.parameters.studyCase
        #print(self.parameters.SMinMaxFrac)
        #print(self.elecOpt.data.Sn)
        
   
    def dayIteration(self):
        nBack = self.parameters.nBack
        nBackASRobust = self.parameters.nBackASRobust
        priceWDate = self.data.priceWDate
        optResults = self.data.optResults
        
        balPriceUp = self.data.balPriceUp
        balPriceDown = self.data.balPriceDown
        yAsUp = self.data.yAsUp
        yAsDown = self.data.yAsDown
        ASDelivery = self.parameters.ASDelivery
        
        # Beta stuff
        yearsLifetime = 10
        self.data.Cinv = 35000 # Euro per kg h^-1
        self.data.betaDyn = self.parameters.Tau / self.data.Cinv
        self.data.betaSS = 1 / (yearsLifetime*365*24*0.8)
        
        # Loop over days
        for d in self.data.days:             
            # List with the utilized simulation days
            
            # Perfect is not a day-iteration. It has perfect forecast of the 
            # whole simulation horizon from day 1. 
            if self.parameters.simuType != 'Perfect':
                simuDate = self.data.simuDates[d*24-24:d*24]
                # Watervalue calculation
                self.elecOpt.data.wV = self.waterValue(d,simuDate)
                optResults['vW'].append(self.elecOpt.data.wV)
            if self.parameters.simuType == 'Perfect':
                simuDate = self.data.simuDates
                # Watervalue not used for perfect
                self.elecOpt.data.wV = 0
            self.data.simuDate = simuDate

            # Internal knowledge of the simulation day for error reporting.
            self.elecOpt.data.simulationDay = d
            
            if self.parameters.simuType == 'Perfect' and ASDelivery == False:
                    
                self.elecOpt.data.lamEl = [priceWDate[t] for t in simuDate]
                
            if self.parameters.simuType == 'Perfect' and ASDelivery == True:
                    
                self.elecOpt.data.lamEl = [priceWDate[t] for t in simuDate]
                self.elecOpt.data.lamAsUp = [[balPriceUp[t]] for t in simuDate]
                self.elecOpt.data.lamAsDown = [[balPriceDown[t]] for t in simuDate]
                self.elecOpt.data.yAsUp = [[yAsUp[t]] for t in simuDate]
                self.elecOpt.data.yAsDown = [[yAsDown[t]] for t in simuDate]
            
            if (self.parameters.simuType == 'Simple' and ASDelivery == False
                and self.parameters.BlockOrder == False):        
                self.elecOpt.data.lamEl = [priceForecast(simuDate,nBack,priceWDate).simple()[t] for t in simuDate]
            
            if (self.parameters.simuType == 'Simple' and ASDelivery == False
                and self.parameters.BlockOrder == True):        
                self.elecOpt.data.lamEl = [priceForecast(simuDate,nBack,priceWDate).simple()[t] for t in simuDate]
                self.elecOpt.data.lamElBlock = [priceForecast(simuDate,nBack,priceWDate).simple()[t] for t in simuDate]
            
            if self.parameters.simuType == 'Stochastic' and ASDelivery == False:      
                self.elecOpt.data.lamEl = [priceForecast(simuDate,nBack,priceWDate).scn()[t] for t in simuDate]                
            
            if self.parameters.simuType == 'Simple' and ASDelivery == True:        
                self.elecOpt.data.lamEl = [priceForecast(simuDate,nBack,priceWDate).simple()[t] for t in simuDate]
                # AS price and activation forecasts
                self.elecOpt.data.lamAsUp = [priceForecast(simuDate,nBack,balPriceUp).scn()[t] for t in simuDate]
                self.elecOpt.data.lamAsDown = [priceForecast(simuDate,nBack,balPriceDown).scn()[t] for t in simuDate]
                self.elecOpt.data.yAsUp = [priceForecast(simuDate,nBack,yAsUp).scn()[t] for t in simuDate]
                self.elecOpt.data.yAsDown = [priceForecast(simuDate,nBack,yAsDown).scn()[t] for t in simuDate]
                if (self.parameters.ASRobustCoOpt == True and self.parameters.ASRobustPlusCoOpt == False 
                        and self.parameters.NDPenalty == False):
                    self.elecOpt.data.yAsUpRobust = [priceForecast(simuDate,nBackASRobust,yAsUp).scn()[t] for t in simuDate]
                    self.elecOpt.data.yAsDownRobust = [priceForecast(simuDate,nBackASRobust,yAsDown).scn()[t] for t in simuDate]
                # This Robustness scenario consists of the two extreme scenarios, where either the entire day consists of up or down regulation.
                # In this way, we ensure that no matter what happens in the regulating power market, the storage will not go into negative
                # which means that the cFix and/or cFlex contracts are not respected fully.
                if (self.parameters.ASRobustCoOpt == True and self.parameters.ASRobustPlusCoOpt == True
                        and self.parameters.NDPenalty == False):
                    self.elecOpt.data.yAsUpRobust = [[0,1]]*24 # One scenario with full up activation, one with zero
                    self.elecOpt.data.yAsDownRobust = [[1,0]]*24 # The opposite extreme of the above
                    
                # The ND Penalty simulation relies on scenario forecasts of AS market quantities, but we add one ASRobustPlus 
                # scenario in the down direction to ensure that the storage never becomes overfull. If we did not, the storage
                # could get above Smax and the simulation would be infeasible. 
                if (self.parameters.ASRobustCoOpt == True and self.parameters.ASRobustPlusCoOpt == True 
                        and self.parameters.NDPenalty == True):
                    # Intention is to prevent hydrogen flaring. Non-delivery is allowed and is 
                    # penalized by the ND penalty, lamND.
                    self.elecOpt.data.yAsUpRobust = [[0]]*24 # No up activation, 
                    self.elecOpt.data.yAsDownRobust = [[1]]*24 # Full down activation
                    #self.elecOpt.data.yAsUpRobust = [[0,1]]*24 # No up activation, 
                    #self.elecOpt.data.yAsDownRobust = [[1,0]]*24 # Full down activation
                    # Add the extra scenario
                    # Extra scenario is currently not added because of problems with the rest of the model.
                    # E.g. The extra scenario would also have to be represented in the obj in the current 
                    # implementation, which would have required some fictous prices to be come up with.
                    # A better implementation gets rid of that but it is harder                    
#                    for key in self.elecOpt.data.yAsUpRobust:
#                        self.elecOpt.data.yAsDownRobust[key].append(1)
#                        self.elecOpt.data.yAsUpRobust[key].append(0)
                
                # Append forecasted AS prices and activations
                optResults['Forecasting']['lamAsUp'].extend(self.elecOpt.data.lamAsUp)
                optResults['Forecasting']['lamAsDn'].extend(self.elecOpt.data.lamAsDown)
                optResults['Forecasting']['yAsUp'].extend(self.elecOpt.data.yAsUp)
                optResults['Forecasting']['yAsDn'].extend(self.elecOpt.data.yAsDown)
                
            # Append forecasted DA prices
            optResults['Forecasting']['lamEl'].extend(self.elecOpt.data.lamEl)
            
            # Build model & Run Optimization
            self.elecOpt._build_model()
            self.elecOpt.optimize()
            
            # Make "out of sample" canculations and store the results of the day
            self.outOfSample(simuDate)
            if ASDelivery == True or self.parameters.AS_SEAS == True:
                self.outOfSampleAS(simuDate)
            
            # Store vector of total hydrogen production from electrolyzer
            for pP,pPAs in zip(optResults['pP'][-len(simuDate):],#optResults['pPBlock'][-24:],   pPBlock,
                               # The zero vector is used when there is no AS delivery
                               # Otherwise, the zip fcn will return a [] vector
                               optResults['pPAs'][-len(simuDate):] if (ASDelivery or self.parameters.AS_SEAS) == True else [0]*len(simuDate)):
                # round off errors in GUROBI out on 10^-15 decimal place can give
                # problems when calculating unit costs, which will be falsely
                # high when dividing by a production of 10^-15
                optResults['pPTot'].append(pP+pPAs if pP+pPAs>10**(-10) else 0) #+pPBlock,  +pPBlock
            
            # Store this days last production point for next days optimization
            # degradation costs (from dynamic operation)
            self.elecOpt.data.pPInit = optResults['pPTot'][-1]
            
            # Calculate the degradation costs per hour        
            self.outOfSampleTau()
                 
            # Counter
            if d%100==0:
                print(d)  
        
        # Sum the beta degradations terms          
        optResults['beta']['sumDyn'] = sum(optResults['beta']['dDyn'])
        optResults['beta']['sumSS'] = sum(optResults['beta']['dSS'])
        optResults['beta']['sumTot'] = sum(optResults['beta']['dDyn'] 
                                        + optResults['beta']['dSS'])           
        # Return the optimization results to the calling script  
        return optResults
    
    
    def outOfSampleTau(self):
        optResults = self.data.optResults
        d = self.elecOpt.data.simulationDay
        
#        if self.parameters.ASDelivery == True or self.parameters.AS_SEAS == True:
#            pPtot = [a+b for a,b in zip(optResults['pP'][-25:],optResults['pPAs'][-25:])]
#        else:
        pPtot = optResults['pPTot'][-len(self.data.simuDate)-1:]
        
        # The first simulation day, we dont have a production reading from the
        # previous day. Therefore we insert one, assuming that the electrolyzer
        # were at zero production the day before.
#        if len(pPtot) == 24:          
#            pPtot.insert(0,0)   
        
        # Tau costs are calculated according to change in production
        for t in list(range(1,len(pPtot))):
            optResults['beta']['dDyn']
            if d == 1 and t == 1:          
                optResults['costTau'].append(0) # First point tau costs are set to zero
                optResults['beta']['dDyn'].append(0)
                optResults['beta']['dSS'].append(self.data.betaSS*pPtot[t])

            else:
                optResults['costTau'].append(self.elecOpt.data.Tau*abs(pPtot[t]-pPtot[t-1]))
                optResults['beta']['dDyn'].append(self.data.betaDyn * (abs(pPtot[t]-pPtot[t-1])/self.parameters.pPn ) )
                optResults['beta']['dSS'].append(self.data.betaSS * (pPtot[t]/self.parameters.pPn) )
                
    
    def waterValue(self,d,simuDate):
        # Before the data basis is large enough we use the average power price with a flat profile assumption.
        # This is quite simplistic as flat profile is worst case.
        # Tau costs are not considered at this point
        
        # NB. For multi year simulations, we could use data from last year.
        # One could run multi year simulation and start nBackWW days back the prev 
        # year.
        
        optResults = self.data.optResults
        WW = 0 # Scalar to store water value
        nBackWW = self.parameters.nBackWW*24 # Hours back for WW calculation
        
        ############ NB
        # We have a problem wiht an initial ramp up in storage level because the
        # flat profile strategy utilized before the strategy dependent data is 
        # available over-estimates the value of stored hydrogen (because flat
        # profile is more expensive). 
        
        if d == 1:
            wwDates = [simuDate[0]-timedelta(0,0,0,0,0,t) for t in list(range(1,nBackWW*24))]            
            wwAvrPri = sum(self.data.priceWDate[t] for t in wwDates)/len(wwDates) # Average DA power price for considered period
            WW = self.elecOpt.data.elecMWhH2*wwAvrPri # Water value based on average power price
        else:
            
            costDA = sum(optResults['costDA'][-nBackWW:])
            costAS = sum(optResults['costAS'][-nBackWW:])
            costTau = sum(optResults['costTau'][-nBackWW:])

            pPDA = sum(optResults['pP'][-nBackWW:])
            pPAS = sum(optResults['pPAs'][-nBackWW:])    
            
            WW = (costDA+costAS+costTau)/(pPDA+pPAS) if pPDA+pPAS != 0 else 0
            #print(WW)
            
        return WW
                   
    def outOfSample(self,simuDate):
        tSet = self.elecOpt.data.tSet
        optResults = self.data.optResults        
        
        # Append conventional results to the result dict
        optResults['objVal'] += self.elecOpt.model.objVal    
        for t in tSet:
            optResults['pP'].append(self.elecOpt.variables.pP[t].x)
            optResults['pB'].append(self.elecOpt.variables.pB[t].x)
            optResults['pBs'].append(self.elecOpt.variables.pBS[t].x)
#            if self.parameters.BlockOrder == True:
#                optResults['pPBlock'].append(self.elecOpt.variables.pPBlock[t].x)   
#                optResults['pBBlock'].append(self.elecOpt.variables.pBBlock[t].x)
#            else:
#                optResults['pPBlock'].append(0)   
#                optResults['pBBlock'].append(0)   
            optResults['S'].append(self.elecOpt.variables.S[t].x)   
            optResults['cFlex'].append(self.elecOpt.variables.cFlex[t].x)
            optResults['costDA'].append(self.data.priceWDate[simuDate[t]]*optResults['pB'][-1])#+optResults['pBBlock'][-1]
            optResults['costDAs'].append(self.data.priceWDate[simuDate[t]]*optResults['pBs'][-1])
        # Move storage value to next day.
        # This is done in the outOfSampleAS function for AS delivery operation
        if self.parameters.ASDelivery == False and self.parameters.AS_SEAS == False:
            self.elecOpt.data.SInit = optResults['S'][-1]
    
    def outOfSampleAS(self,simuDate):
        tSet = self.elecOpt.data.tSet
        optResults = self.data.optResults
        elecMWhH2 = self.elecOpt.data.elecMWhH2
        #DW = self.elecOpt.data.DW
        
        # AS activation strategies.
        if self.parameters.ASCoOpt == True or self.parameters.ASFix == True:        
            gammaAsUp = [self.elecOpt.variables.ASgammaUp[t].x for t in tSet]
            gammaAsDn = [self.elecOpt.variables.ASgammaDown[t].x for t in tSet]
        # The AS2 regulation power market strategy is applied here
        if self.parameters.AS_SEAS == True:
            AS2meanDates = [simuDate[0]-timedelta(0,0,0,0,0,1)-timedelta(0,0,0,0,0,t) for t in list(range(0,(round(self.parameters.AS2meanDaysBack*24))))]
            temp2AS = self.as2Strategy(simuDate,AS2meanDates)
            #print(temp2AS)
            gammaAsUp = temp2AS['gammaAsUp']
            gammaAsDn = temp2AS['gammaAsDn']
        
        pPAs = [] # Hydrogen produced for AS
        pPAsDn = []
        for t in tSet:
            pPAs.append(self.elecOpt.data.pPn*(gammaAsDn[t]*self.data.yAsDown[simuDate[t]]-gammaAsUp[t]*self.data.yAsUp[simuDate[t]]))
            pPAsDn.append(self.elecOpt.data.pPn*(gammaAsDn[t]*self.data.yAsDown[simuDate[t]]))
        
        pBAs = [elecMWhH2*pPAs + DW*pPAsDn for pPAs,pPAsDn,elecMWhH2,DW in 
            zip(pPAs,pPAsDn,[elecMWhH2]*len(pPAs),[self.elecOpt.data.DW]*len(pPAs))]
        
        #pBAs = [elecMWhH2*pPAs for pPAs,elecMWhH2 in zip(pPAs,[self.elecOpt.data.elecMWhH2]*len(pPAs))]
        #pBAs = [a*b for a,b in zip(pPAs,[self.elecOpt.data.elecMWhH2]*len(pPAs))]
        
        # Append results
        for t in tSet:
            optResults['pPAs'].append(pPAs[t])
            optResults['pBAs'].append(pBAs[t])
            optResults['dSAs'].append(self.elecOpt.variables.pP[t].x+pPAs[t]-self.elecOpt.data.cFix[t]-self.elecOpt.variables.cFlex[t].x)
            if t == tSet[0]:                
                optResults['SAs'].append(self.elecOpt.data.SInit+optResults['dSAs'][-1])                
            if t > tSet[0]:
                optResults['SAs'].append(optResults['SAs'][-1]+optResults['dSAs'][-1])
            optResults['ASgammaDown'].append(gammaAsDn[t])
            optResults['ASgammaUp'].append(gammaAsUp[t])
            optResults['costAS'].append(self.data.balPriceDown[simuDate[t]]*optResults['pBAs'][-1])
            
#            if t < tSet[-1]:
#                if optResults['SAs'][-1] < 0:
#                    optResults['SAs'][-1] = 0
#                    optResults['pPND'].append(0 - optResults['SAs'][-1])
#                    optResults['pPFlare'].append(0)
#                elif optResults['SAs'][-1] > self.elecOpt.data.Sn:
#                    optResults['SAs'][-1] = self.elecOpt.data.Sn
#                    optResults['pPFlare'].append(optResults['SAs'][-1] - self.elecOpt.data.Sn)
#                    optResults['pPND'].append(0)
#                else:
#                    optResults['pPND'].append(0)
#                    optResults['pPFlare'].append(0)
#            if t == tSet[-1]:        
        if optResults['SAs'][-1] < self.elecOpt.data.SMin:
            self.elecOpt.data.SInit = self.elecOpt.data.SMin
            optResults['pPND'].append(self.elecOpt.data.SMin - optResults['SAs'][-1])
            optResults['pPFlare'].append(0)
        elif optResults['SAs'][-1] > self.elecOpt.data.SMax:
            self.elecOpt.data.SInit = self.elecOpt.data.SMax
            optResults['pPFlare'].append(optResults['SAs'][-1] - self.elecOpt.data.SMax)
            optResults['pPND'].append(0)
        else:
            self.elecOpt.data.SInit = optResults['SAs'][-1]
            optResults['pPND'].append(0)
            optResults['pPFlare'].append(0)
    
        if self.parameters.NDRTPenalty == False:
            optResults['costND'].append(optResults['pPND'][-1]*self.elecOpt.data.lamND)
        # Viel problemoz. We need to evaluate the ND at every hour... Damn, this is close to imposible...
        if self.parameters.NDRTPenalty == True:
            optResults['costND'].append(optResults['pPND'][-1]*self.parameters.NDRTFrac*elecMWhH2
                *1/len(tSet)*sum(self.data.priceWDate[simuDate[t]] for t in tSet))

        
 
    def as2Strategy(self,simuDate,meanDates):
        # This function will derive a strategy for AS participation according
        # to the second AS participation strategy.
        tSet = self.elecOpt.data.tSet      
        
        priceWDate = self.data.priceWDate 
        
        yAsUpRobust = [[1]*24, [0]*24]
        yAsDnRobust = [[0]*24, [1]*24]        
        
        lam = [priceWDate[t] for t in simuDate]
        # Calculate the alphaFlex+alphaFix percentile.
        #lamMean = sum(priceWDate[t] for t in meanDates)/len(meanDates)
        lamMean = np.percentile([priceWDate[t] for t in meanDates],(self.elecOpt.data.alphaFlex+self.elecOpt.data.alphaFix)*100)
        for lamMeanValue in [lamMean]*24:
            self.data.optResults['Forecasting']['lamMeanAs2'].append(lamMeanValue)
        
        pPn = self.elecOpt.data.pPn
        Sn = self.elecOpt.data.Sn
        
        pP = [self.elecOpt.variables.pP[t].x for t in tSet]
        S = [self.elecOpt.variables.S[t].x for t in tSet]
        #print(S)
        
        ### Build optimization model
        m = gb.Model()
        m.params.OutputFlag = False # Surpress std. output from Gurobi
        
        # Variables        
        pPAsUp = {}
        pPAsDn = {}
        
        for t in tSet:
            pPAsUp[t] = m.addVar(lb=0,ub=pPn, name='pPAs.'+str(t))
            pPAsDn[t] = m.addVar(lb=0,ub=pPn, name='pPAs.'+str(t))
            
        SAs = {}
        kSet = list(range(0,len(yAsUpRobust)))
        for k in kSet:
            SAs[k] = {}
            for t in tSet:
                if t < tSet[-1]:
                    SAs[k][t] = m.addVar(lb=0, ub=Sn, name='SAs.'+str(k)+'.'+str(t))
                if t == tSet[-1]:
                    #print(self.elecOpt.data.SMin)
                    if self.parameters.studyCase == 'As2_33':
                        SAs[k][t] = m.addVar(lb=0, ub=Sn, name='SAs.'+str(k)+'.'+str(t))
                    if self.parameters.studyCase == 'As2':
                        SAs[k][t] = m.addVar(lb=self.elecOpt.data.SMin, ub=self.elecOpt.data.SMax, name='SAs.'+str(k)+'.'+str(t))
                    #print(self.elecOpt.data.SMin)
                    #print(self.elecOpt.data.SMax)
        
        # Update variables
        m.update()
        
        # Objective
        m.setObjective(
        gb.quicksum(
        (lam[t]-lamMean)*(pPAsDn[t]-pPAsUp[t]) for t in tSet), 
        gb.GRB.MINIMIZE)
        
        # Constraints
        prodHiCts = {}
        prodLoCts = {}
        
        for k in kSet:
            prodHiCts[k] = {}
            prodLoCts[k] = {}
            for t in tSet:
                prodHiCts[k][t] = m.addConstr(pPAsDn[t]*yAsDnRobust[k][t]-pPAsUp[t]*yAsUpRobust[k][t]+pP[t] <= pPn, name='prodHiCts.'+str(k)+'.'+str(t))
                prodLoCts[k][t] = m.addConstr(pPAsDn[t]*yAsDnRobust[k][t]-pPAsUp[t]*yAsUpRobust[k][t]+pP[t] >= 0, name='prodLoCts.'+str(k)+'.'+str(t))
            
        storCts = {}
        for k in kSet:
            storCts[k] = {}
            for t in tSet:
                if t == tSet[0]:            
                    storCts[k][t] = m.addConstr(SAs[k][t] == 
                    S[t]+pPAsDn[t]*yAsDnRobust[k][t]-pPAsUp[t]*yAsUpRobust[k][t], 
                    name='storCts.'+str(k)+'.'+str(t))
                if t > tSet[0]:
                    storCts[k][t] = m.addConstr(SAs[k][t] == 
                    SAs[k][t-1]+(S[t]-S[t-1])+pPAsDn[t]*yAsDnRobust[k][t]-pPAsUp[t]*yAsUpRobust[k][t], 
                    name='storCts.'+str(k)+'.'+str(t))
                
        # Optimize
        m.optimize()
        
        # Return the resulting up and down regulation strategies
        return {'gammaAsUp':[pPAsUp[t].x/self.elecOpt.data.pPn for t in tSet],
                'gammaAsDn':[pPAsDn[t].x/self.elecOpt.data.pPn for t in tSet]}
                
class priceForecast:
    def __init__(self,fDate,nBack,priceWDate):
        self.fDate = fDate
        self.nBack = nBack
        self.priceWDate = priceWDate

    def scn(self):
        # Makes a scenario based forecast, where each scenario is the same hour,
        # the same day of the week a total of nBack weeks back in time.
        forecastDate = {}
        for d in self.fDate:
            forecastDate[d] = []
    
        for d in self.fDate:
            for b in list(range(1,self.nBack+1)):
                forecastDate[d].append(self.priceWDate[d - timedelta(0,0,0,0,0,0,b)])
        
        return forecastDate
        
    def simple(self):
        # Makes a simple forecast, which is the average of the same hour the 
        # same day of the week a total of nBack weeks back in time.
        forecastDate = self.scn()        
        forecastDate2 = {}
        for k in forecastDate.keys():
            forecastDate2[k] = sum(forecastDate[k])/len(forecastDate[k])
        
        return forecastDate2    
            

                
                