# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 16:08:42 2016

@author: Janus Tougaard
"""
# Python standard modules to import
from datetime import datetime, timedelta #, date, time
import pandas as pd

# Own modules to import
from DayIterationClass import dayIteration
from PlotResults import plotResults

class expando(object):
    '''
        A small class which can have attributes set
    '''
    pass

class studyCases:

    def __init__(self,studyCaseDict,year,month,day,studyDays,priceWDate,yAsDown,
                     yAsUp,balPriceDown,balPriceUp,Tau=0.0,lamND=5.0,NDRTFrac=1.5,
                     NDRTPenaly=True,Sn=12,alphaFix=0.6,alphaFlex=0.0,blockSize=4,
                     fixFrac=0.20):#,plotYN='Y'):
    #%% Overall parameters
    
        self.data = expando()
        self.result = expando()
        self.sim = expando()
        
        # Store input args
        self.data.studyCaseDict = studyCaseDict
        self.data.studyDays = studyDays
        self.data.priceWDate = priceWDate
        self.data.yAsDown = yAsDown
        self.data.yAsUp = yAsUp
        self.data.balPriceDown = balPriceDown
        self.data.balPriceUp = balPriceUp
        self.data.Tau = Tau
        self.data.lamND = lamND
        #self.data.plotYN = plotYN
        self.data.NDRTPenalty = NDRTPenaly
        self.data.NDRTFrac = NDRTFrac
        self.data.blockSize = blockSize
        self.data.fixFrac = fixFrac
        
        
        self.data.dMax = studyDays # Time steps in days
        self.data.days = list(range(1,self.data.dMax+1)) # List of days
        self.data.tMax = 24*self.data.dMax # Time steps in hours
        
        self.data.nBack = 12
        
        # ELectrolyzer parameters
        self.data.alphaFlex = alphaFlex
        self.data.alphaFix = alphaFix
        self.data.pPn = 100.0
        self.data.Sn = Sn
        
        # This is the set of dates to simulate over
        self.data.simuDates = [datetime(year,month,day,0,0,0)+timedelta(0,0,0,0,0,t) for t in list(range(0,self.data.tMax))]
        
        # Dict to store results
        self.result.allDict = {}
        
        # Compute study cases and calculate unit costs.        
        self.studyCases()
        self.unitCostCalc()
    
    def studyCases(self):
        studyCaseDict = self.data.studyCaseDict 
        #studyDays = self.data.studyDays
        priceWDate = self.data.priceWDate
        yAsDown = self.data.yAsDown
        yAsUp = self.data.yAsUp
        balPriceDown = self.data.balPriceDown
        balPriceUp = self.data.balPriceUp
        Tau = self.data.Tau
        days = self.data.days
        simuDates = self.data.simuDates
        nBack = self.data.nBack
        Sn = self.data.Sn
        blockSize = self.data.blockSize
        fixFrac = self.data.fixFrac
        
        #%% Base case participation
        if 'Base' in studyCaseDict:  
            
            self.result.baseUnitCost = sum(priceWDate[t] for t in simuDates)/len(simuDates)*0.050    
        
        #%% Perfect forecast
        if 'Perfect' in studyCaseDict:
            print('Simulating with perfect price forecast')   
            
            self.sim.dayIterPF = dayIteration([1],simuDates,priceWDate,'Perfect')
            
            # Set model parameters
            self.sim.dayIterPF.parameters.Tau = Tau # Dynamic operation costs
            self.sim.dayIterPF.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterPF.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterPF.parameters.pPn = self.data.pPn
            self.sim.dayIterPF.parameters.Sn = Sn
            self.sim.dayIterPF._update_parameters()    
            
            self.result.allDict['Perfect'] = self.sim.dayIterPF.dayIteration()
    
    
        #%% Simple forecast
        if 'Simple' in studyCaseDict:
            print('Simulating with simple price forecast')   
            self.sim.dayIterSF = dayIteration(days,simuDates,priceWDate,'Simple')
            
            # Set model parameters
            self.sim.dayIterSF.parameters.nBack = nBack 
            self.sim.dayIterSF.parameters.Tau = Tau
            self.sim.dayIterSF.parameters.Sn = Sn
            self.sim.dayIterSF.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterSF.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterSF.parameters.pPn = self.data.pPn
            self.sim.dayIterSF._update_parameters()
            
            self.result.allDict['Simple'] = self.sim.dayIterSF.dayIteration()
            
        #%% Simple forecast, no tau in obj
        if 'SimpleNoTau' in studyCaseDict:
            print('Simulating with simple price forecast and no tau in obj')   
            self.sim.dayIterSFNT = dayIteration(days,simuDates,priceWDate,'Simple')
            
            # Set model parameters
            self.sim.dayIterSFNT.parameters.nBack = nBack 
            self.sim.dayIterSFNT.parameters.Tau = Tau
            self.sim.dayIterSFNT.parameters.Sn = Sn
            self.sim.dayIterSFNT.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterSFNT.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterSFNT.parameters.pPn = self.data.pPn
            self.sim.dayIterSFNT.parameters.disableTau = 0 # disable tau in objective fcn
            self.sim.dayIterSFNT._update_parameters()
            
            self.result.allDict['SimpleNoTau'] = self.sim.dayIterSFNT.dayIteration()
        
        #%% Simple forecast With Block Order 
        if 'SimpleBlockOrder' in studyCaseDict:
            print('Simulating with simple price forecast and Block Order')   
            self.sim.dayIterSFBO = dayIteration(days,simuDates,priceWDate,'Simple')
            
            # Set model parameters
            self.sim.dayIterSFBO.parameters.nBack = nBack 
            self.sim.dayIterSFBO.parameters.Tau = Tau
            self.sim.dayIterSFBO.parameters.Sn = Sn
            self.sim.dayIterSFBO.parameters.BlockOrder = True
            self.sim.dayIterSFBO.parameters.blockSize = blockSize
            self.sim.dayIterSFBO.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterSFBO.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterSFBO.parameters.pPn = self.data.pPn
            self.sim.dayIterSFBO._update_parameters()
            
            self.result.allDict['SimpleBlockOrder'] = self.sim.dayIterSFBO.dayIteration()
        
        #%% Simple forecast With Block Order and no tau in obj
        if 'SimBoNt' in studyCaseDict:
            print('Simulating with simple price forecast and Block Order and No Tau in Obj.')   
            self.sim.dayIterSFBONT = dayIteration(days,simuDates,priceWDate,'Simple')
            
            # Set model parameters
            self.sim.dayIterSFBONT.parameters.nBack = nBack 
            self.sim.dayIterSFBONT.parameters.Tau = Tau
            self.sim.dayIterSFBONT.parameters.Sn = Sn
            self.sim.dayIterSFBONT.parameters.BlockOrder = True
            self.sim.dayIterSFBONT.parameters.blockSize = blockSize
            self.sim.dayIterSFBONT.parameters.disableTau = 0 # disable tau in objective fcn
            self.sim.dayIterSFBONT.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterSFBONT.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterSFBONT.parameters.pPn = self.data.pPn
            self.sim.dayIterSFBONT._update_parameters()
            
            self.result.allDict['SimBoNt'] = self.sim.dayIterSFBONT.dayIteration()        
        
        #%% Perfect forecast with AS perfect forecast
        if 'AsPerfect' in studyCaseDict:
            print('Simulating with perfect price forecast and perfect AS forecast')   
            ## Run model and store results in result dict
            self.sim.dayIterAsPerfect = dayIteration([1],simuDates,priceWDate,'Perfect')
            
            # Model parameters
            self.sim.dayIterAsPerfect.parameters.ASDelivery = True
            self.sim.dayIterAsPerfect.parameters.ASCoOpt = True
            self.sim.dayIterAsPerfect.parameters.ASRobustCoOpt = False
            self.sim.dayIterAsPerfect.parameters.ASRobustPlusCoOpt = False
            self.sim.dayIterAsPerfect.parameters.ASgammaUpMax = 1.0
            self.sim.dayIterAsPerfect.parameters.ASgammaDownMax = 1.0
            #dayIterAsPerfect.parameters.nBack = 12
            #dayIterAsPerfect.parameters.nBackASRobust = 12
            self.sim.dayIterAsPerfect.parameters.Tau = Tau # Dynamic operation costs
            self.sim.dayIterAsPerfect.parameters.Sn = Sn
            self.sim.dayIterAsPerfect.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterAsPerfect.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterAsPerfect.parameters.pPn = self.data.pPn
            self.sim.dayIterAsPerfect._update_parameters()
            
            self.sim.dayIterAsPerfect.data.yAsDown = yAsDown
            self.sim.dayIterAsPerfect.data.yAsUp = yAsUp
            self.sim.dayIterAsPerfect.data.balPriceDown = balPriceDown
            self.sim.dayIterAsPerfect.data.balPriceUp = balPriceUp
            
            self.result.allDict['AsPerfect'] = self.sim.dayIterAsPerfect.dayIteration()  
            
        #%% Perfect forecast with AS perfect forecast & ND Penalty
        if 'AsPerfectNDP' in studyCaseDict:
            print('Simulating with perfect price forecast and perfect AS forecast and ND Penalty')   
            ## Run model and store results in result dict
            self.sim.dayIterAsPerfectNDP = dayIteration([1],simuDates,priceWDate,'Perfect')
            
            # Model parameters
            self.sim.dayIterAsPerfectNDP.parameters.ASDelivery = True
            self.sim.dayIterAsPerfectNDP.parameters.ASCoOpt = True
            self.sim.dayIterAsPerfectNDP.parameters.ASRobustCoOpt = False
            self.sim.dayIterAsPerfectNDP.parameters.ASRobustPlusCoOpt = False
            self.sim.dayIterAsPerfectNDP.parameters.NDPenalty = True
            self.sim.dayIterAsPerfectNDP.parameters.NDRTPenalty = self.data.NDRTPenalty
            self.sim.dayIterAsPerfectNDP.parameters.NDRTFrac = self.data.NDRTFrac
            self.sim.dayIterAsPerfectNDP.parameters.ASgammaUpMax = 1.0
            self.sim.dayIterAsPerfectNDP.parameters.ASgammaDownMax = 1.0
            self.sim.dayIterAsPerfectNDP.parameters.Tau = Tau # Dynamic operation costs
            self.sim.dayIterAsPerfectNDP.parameters.Sn = Sn
            self.sim.dayIterAsPerfectNDP.parameters.lamND = self.data.lamND
            self.sim.dayIterAsPerfectNDP.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterAsPerfectNDP.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterAsPerfectNDP.parameters.pPn = self.data.pPn
            self.sim.dayIterAsPerfectNDP._update_parameters()
            
            self.sim.dayIterAsPerfectNDP.data.yAsDown = yAsDown
            self.sim.dayIterAsPerfectNDP.data.yAsUp = yAsUp
            self.sim.dayIterAsPerfectNDP.data.balPriceDown = balPriceDown
            self.sim.dayIterAsPerfectNDP.data.balPriceUp = balPriceUp
            
            self.result.allDict['AsPerfectNDP'] = self.sim.dayIterAsPerfectNDP.dayIteration()  
        
        
        #%% Simple forecast with AS CoOpt
        if 'AsCoOpt' in studyCaseDict:
            print('Simulating with simple price forecast and AsCoOpt delivery')   
            ## Run model and store results in result dict
            self.sim.dayIterSFASCoOpt = dayIteration(days,simuDates,priceWDate,'Simple',studyCase='AsCoOpt')
            
            # Model parameters
            self.sim.dayIterSFASCoOpt.parameters.ASDelivery = True
            self.sim.dayIterSFASCoOpt.parameters.ASCoOpt = True
            self.sim.dayIterSFASCoOpt.parameters.ASRobustCoOpt = True
            self.sim.dayIterSFASCoOpt.parameters.ASRobustPlusCoOpt = True
            self.sim.dayIterSFASCoOpt.parameters.ASgammaUpMax = 1.0
            self.sim.dayIterSFASCoOpt.parameters.ASgammaDownMax = 1.0
            self.sim.dayIterSFASCoOpt.parameters.SMinMaxFrac = 0.05
            self.sim.dayIterSFASCoOpt.parameters.nBack = nBack
            self.sim.dayIterSFASCoOpt.parameters.nBackASRobust = nBack
            self.sim.dayIterSFASCoOpt.parameters.Tau = Tau # Dynamic operation costs
            self.sim.dayIterSFASCoOpt.parameters.Sn = Sn
            self.sim.dayIterSFASCoOpt.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterSFASCoOpt.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterSFASCoOpt.parameters.pPn = self.data.pPn
            self.sim.dayIterSFASCoOpt._update_parameters()
            
            self.sim.dayIterSFASCoOpt.data.yAsDown = yAsDown
            self.sim.dayIterSFASCoOpt.data.yAsUp = yAsUp
            self.sim.dayIterSFASCoOpt.data.balPriceDown = balPriceDown
            self.sim.dayIterSFASCoOpt.data.balPriceUp = balPriceUp
            
            self.result.allDict['AsCoOpt'] = self.sim.dayIterSFASCoOpt.dayIteration()
        
        
        #%% Simple forecast with AS CoOpt and ND Penalty,
        if 'AsCoOptNDP' in studyCaseDict:
            print('Simulating with simple price forecast, AsCoOpt delivery and ND Penalty')   
            ## Run model and store results in result dict
            self.sim.dayIterSFASCoOptNDP = dayIteration(days,simuDates,priceWDate,'Simple')
            
            # Model parameters
            self.sim.dayIterSFASCoOptNDP.parameters.ASDelivery = True
            self.sim.dayIterSFASCoOptNDP.parameters.ASCoOpt = True
            self.sim.dayIterSFASCoOptNDP.parameters.ASRobustCoOpt = True
            self.sim.dayIterSFASCoOptNDP.parameters.ASRobustPlusCoOpt = True
            self.sim.dayIterSFASCoOptNDP.parameters.NDPenalty = True
            self.sim.dayIterSFASCoOptNDP.parameters.NDRTPenalty = self.data.NDRTPenalty
            self.sim.dayIterSFASCoOptNDP.parameters.NDRTFrac = self.data.NDRTFrac
            self.sim.dayIterSFASCoOptNDP.parameters.ASgammaUpMax = 1.0
            self.sim.dayIterSFASCoOptNDP.parameters.ASgammaDownMax = 1.0
            self.sim.dayIterSFASCoOptNDP.parameters.SMinMaxFrac = 0.05
            self.sim.dayIterSFASCoOptNDP.parameters.nBack = nBack
            self.sim.dayIterSFASCoOptNDP.parameters.nBackASRobust = nBack
            self.sim.dayIterSFASCoOptNDP.parameters.Tau = Tau # Dynamic operation costs
            self.sim.dayIterSFASCoOptNDP.parameters.Sn = Sn
            self.sim.dayIterSFASCoOptNDP.parameters.lamND = self.data.lamND
            self.sim.dayIterSFASCoOptNDP.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterSFASCoOptNDP.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterSFASCoOptNDP.parameters.pPn = self.data.pPn
            self.sim.dayIterSFASCoOptNDP._update_parameters()
            
            self.sim.dayIterSFASCoOptNDP.data.yAsDown = yAsDown
            self.sim.dayIterSFASCoOptNDP.data.yAsUp = yAsUp
            self.sim.dayIterSFASCoOptNDP.data.balPriceDown = balPriceDown
            self.sim.dayIterSFASCoOptNDP.data.balPriceUp = balPriceUp
            
            self.result.allDict['AsCoOptNDP'] = self.sim.dayIterSFASCoOptNDP.dayIteration()
        
        
        #%% Simple forecast with AS Fix
        if 'AsFix' in studyCaseDict:
            print('Simulating with simple price forecast and AsFix delivery')   
            ## Run model and store results in result dict
            self.sim.dayIterSFASFix = dayIteration(days,simuDates,priceWDate,'Simple')
            
            self.sim.dayIterSFASFix.parameters.ASDelivery = True
            self.sim.dayIterSFASFix.parameters.ASFix = True
            self.sim.dayIterSFASFix.parameters.ASRobustCoOpt = True # These also works with fix
            self.sim.dayIterSFASFix.parameters.ASRobustPlusCoOpt = True # These also works with fix
            self.sim.dayIterSFASFix.parameters.ASgammaUpFix = fixFrac
            self.sim.dayIterSFASFix.parameters.ASgammaDownFix = fixFrac
            self.sim.dayIterSFASFix.parameters.SMinMaxFrac = 0.05
            self.sim.dayIterSFASFix.parameters.nBack = nBack
            self.sim.dayIterSFASFix.parameters.nBackASRobust = nBack # These also works with fix
            self.sim.dayIterSFASFix.parameters.Tau = Tau # Dynamic operation costs
            self.sim.dayIterSFASFix.parameters.Sn = Sn
            self.sim.dayIterSFASFix.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterSFASFix.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterSFASFix.parameters.pPn = self.data.pPn
            self.sim.dayIterSFASFix._update_parameters()
            
            self.sim.dayIterSFASFix.data.yAsDown = yAsDown
            self.sim.dayIterSFASFix.data.yAsUp = yAsUp
            self.sim.dayIterSFASFix.data.balPriceDown = balPriceDown
            self.sim.dayIterSFASFix.data.balPriceUp = balPriceUp
            
            self.result.allDict['AsFix'] = self.sim.dayIterSFASFix.dayIteration()
        
        #%% Simple forecast with AS2
        if 'As2' in studyCaseDict:
            print('Simulating with simple price forecast and AS2 delivery')   
            ## Run model and store results in result dict
            self.sim.dayIterSFAS_SEAS = dayIteration(days,simuDates,priceWDate,'Simple',studyCase='As2')
            
            self.sim.dayIterSFAS_SEAS.parameters.ASDelivery = False # The AS delivery calculations inside the Gurobi script
            self.sim.dayIterSFAS_SEAS.parameters.AS_SEAS = True
            self.sim.dayIterSFAS_SEAS.parameters.nBack = nBack
            self.sim.dayIterSFAS_SEAS.parameters.AS2meanDaysBack = 30
            self.sim.dayIterSFAS_SEAS.parameters.SMinMaxFrac = 0.05
            self.sim.dayIterSFAS_SEAS.parameters.Tau = Tau # Dynamic operation costs
            self.sim.dayIterSFAS_SEAS.parameters.Sn = Sn
            self.sim.dayIterSFAS_SEAS.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterSFAS_SEAS.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterSFAS_SEAS.parameters.pPn = self.data.pPn
            self.sim.dayIterSFAS_SEAS._update_parameters()
            
            self.sim.dayIterSFAS_SEAS.data.yAsDown = yAsDown
            self.sim.dayIterSFAS_SEAS.data.yAsUp = yAsUp
            self.sim.dayIterSFAS_SEAS.data.balPriceDown = balPriceDown
            self.sim.dayIterSFAS_SEAS.data.balPriceUp = balPriceUp
            
            self.result.allDict['As2'] = self.sim.dayIterSFAS_SEAS.dayIteration()
        #%% Simple forecast with AS2
        if 'As2_33' in studyCaseDict:
            print('Simulating with simple price forecast and AS2_33 delivery')   
            ## Run model and store results in result dict
            self.sim.dayIterSFAS_SEAS = dayIteration(days,simuDates,priceWDate,'Simple',studyCase='As2_33')
            
            self.sim.dayIterSFAS_SEAS.parameters.ASDelivery = False # The AS delivery calculations inside the Gurobi script
            self.sim.dayIterSFAS_SEAS.parameters.AS_SEAS = True
            self.sim.dayIterSFAS_SEAS.parameters.nBack = nBack
            self.sim.dayIterSFAS_SEAS.parameters.AS2meanDaysBack = 30
            self.sim.dayIterSFAS_SEAS.parameters.SMinMaxFrac = 0.33
            self.sim.dayIterSFAS_SEAS.parameters.Tau = Tau # Dynamic operation costs
            self.sim.dayIterSFAS_SEAS.parameters.Sn = Sn
            self.sim.dayIterSFAS_SEAS.parameters.alphaFix = self.data.alphaFix
            self.sim.dayIterSFAS_SEAS.parameters.alphaFlex = self.data.alphaFlex
            self.sim.dayIterSFAS_SEAS.parameters.pPn = self.data.pPn
            self.sim.dayIterSFAS_SEAS._update_parameters()
            
            self.sim.dayIterSFAS_SEAS.data.yAsDown = yAsDown
            self.sim.dayIterSFAS_SEAS.data.yAsUp = yAsUp
            self.sim.dayIterSFAS_SEAS.data.balPriceDown = balPriceDown
            self.sim.dayIterSFAS_SEAS.data.balPriceUp = balPriceUp
            
            self.result.allDict['As2_33'] = self.sim.dayIterSFAS_SEAS.dayIteration()
    
    def unitCostCalc(self):        
        #%% Calculating Unit Prices
    
        allDict = self.result.allDict
        
        
        resultCategories = ['DA','AS','Tau','DA&AS&Tau','DA&AS&ND','DA&AS&Tau&ND','Total Costs','ND Pct.','ND Abs.','pPDA','pPAS']
        
        participationStrategies = self.data.studyCaseDict        
        #participationStrategies = ['Base','Perfect','Simple','SimpleBlockOrder','AsPerfect','As2','AsCoOpt','AsCoOptNDP','AsFix']
        self.result.unitCostDF = pd.DataFrame(columns=resultCategories)
        
        for strategy in participationStrategies:
            if strategy == 'Base':
                unitCostDA = self.result.baseUnitCost
                unitCostAS = 0.0
                unitCostTau = 0.0
                #unitCostND = 0.0
                unitCostDAASND = unitCostDA
                unitCostDAASTau = unitCostDA
                unitCostDAASTauND = unitCostDA
                totalCosts = unitCostDA*self.data.tMax*(self.data.alphaFix + self.data.alphaFlex)*self.data.pPn
                fractionND = 0.0
                NDAbs = 0.0
                pPDA = 'NA'
                pPAS = 'NA'
            else:
                for resultCat in resultCategories:
                    costDA = sum(allDict[strategy]['costDA'])
                    costAS = sum(allDict[strategy]['costAS'])
                    costTau = sum(allDict[strategy]['costTau'])
                    costND = sum(allDict[strategy]['costND'])
        
                    pPDA = sum(allDict[strategy]['pP'])#+allResults[strategy]['pPBlock'])
                    pPAS = sum(allDict[strategy]['pPAs'])
                    #dSfinal = ( allDict[strategy]['SAs'][-1] - allDict[strategy]['SAs'][0] ) if ( sum(allDict[strategy]['SAs']) != 0 ) else ( allDict[strategy]['S'][-1] - allDict[strategy]['S'][0] )
        
                    unitCostDA = costDA/pPDA if pPDA != 0 else 0
                    unitCostAS = costAS/pPAS if pPAS != 0 else 0
                    unitCostTau = costTau/(pPDA+pPAS) if pPDA+pPAS != 0 else 0
                    #unitCostND = costND/(pPDA+pPAS)
                    unitCostDAASND = (costDA+costAS+costND)/(pPDA+pPAS) if pPDA+pPAS != 0 else 0
                    unitCostDAASTau = (costDA+costAS+costTau)/(pPDA+pPAS) if pPDA+pPAS != 0 else 0
                    unitCostDAASTauND = (costDA+costAS+costND+costTau)/(pPDA+pPAS) if pPDA+pPAS != 0 else 0
                    totalCosts = (costDA+costAS+costND+costTau)
                    
                    #print(dSfinal)
                    NDAbs = sum(allDict[strategy]['pPND']) if sum(allDict[strategy]['pPND']) > 10**(-3) else 0.0
                    fractionND = 100*( NDAbs/
                        ((self.data.tMax+1)*(self.data.alphaFix + 
                        self.data.alphaFlex)*self.data.pPn) )
            self.result.unitCostDF.loc[strategy] = [unitCostDA,unitCostAS,unitCostTau,unitCostDAASTau,unitCostDAASND,unitCostDAASTauND,totalCosts,fractionND,NDAbs,pPDA,pPAS]
    
    
    #%% Plotting    
    def plotPS(self):
        
        allDict = self.result.allDict        
        studyCaseDict = self.data.studyCaseDict       
        
        for case in studyCaseDict:
            
            if case in ['Perfect','Simple','SimpleBlockOrder','SimpleBlockOrderNoTau']:
            #for case in studyCasesWoAs:
                plotResultsPerfect = plotResults(case,'PS')
    #            if case == 'SimpleBlockOrder':
    #                plotResultsPerfect.plotProduction(allResults[case]['pP'],pPBlock=allResults[case]['pPBlock'])
    #            else:
                plotResultsPerfect.plotProduction(allDict[case]['pP'])
                plotResultsPerfect.plotStorage(allDict[case]['S'])
                plotResultsPerfect.saveFig()
            
            if case in ['AsPerfect','AsPerfectNDP','AsCoOpt','AsCoOptNDP','AsFix','As2']:
            #for case in studyCasesWAs:
                plotResultsTemp = plotResults(case,'PS')
                plotResultsTemp.plotProduction(allDict[case]['pPTot'],pPDA=allDict[case]['pP'],pPAS=allDict[case]['pPAs'])
                plotResultsTemp.plotStorage(allDict[case]['SAs'])
                plotResultsTemp.saveFig()
                
                
                
    def plotPDA(self):
        
        allDict = self.result.allDict
        studyCaseDict = self.data.studyCaseDict 
        
        for case in studyCaseDict:
            
            # Plotting with price
            if case in ['Perfect','Simple','SimpleBlockOrder']:
            #for case in studyCasesWoAs:
                plotResultsPerfect = plotResults(case,'PDA')
                plotResultsPerfect.plotProduction(allDict[case]['pP'])
                plotResultsPerfect.plotDAPrice(allDict[case]['Forecasting']['lamEl'])
                plotResultsPerfect.saveFig()
            
        #    studyCasesWAs = ['AsCoOpt','AsFix','As2']
        #    for case in studyCasesWAs:
        #        plotResultsTemp = plotResults(case,'PDA')
        #        plotResultsTemp.plotProduction(allResults[case]['pPTot'],pPDA=allResults[case]['pP'],pPAS=allResults[case]['pPAs'])
        #        plotResultsTemp.plotStorage(allResults[case]['SAs'])
        #        plotResultsTemp.saveFig()
        
    
    def returnResults(self):
                
        return {'allResults': self.result.allDict,
                'unitCostDF': self.result.unitCostDF,
                'dateTime': self.data.simuDates}
    
    def returnUnitCostsWTau(self):
        return self.result.unitCostDF.loc[:,'DA&AS&Tau&ND']
        
    def returnUnitCostsWOTau(self):
        return self.result.unitCostDF.loc[:,'DA&AS&ND']
