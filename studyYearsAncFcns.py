# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 10:09:33 2016

@author: Janus
"""

from elecStudyCases import studyCases
import pandas as pd

def yearIteration(studyCaseDict,startYear,deltaYears,startMonth,startDay,studyDays,
                  priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,plotPS=False,Tau=0.0):
    studyYears = [startYear + y for y in list(range(0,deltaYears+1))]
    yearResults = {}
    
    for y in studyYears:
       # print('Simulation year %g.' % y)
        yearSim = studyCases(studyCaseDict,y,startMonth,startDay,studyDays,priceWDate,
                             yAsDown,yAsUp,balPriceDown,balPriceUp,Tau=Tau)       
        
        yearResults[str(y)] = yearSim.returnResults()
        
        print(y)
        print(yearResults[str(y)]['unitCostDF'])
        
        if plotPS == True:
            yearSim.plotPS()
        
    return yearResults

def blockIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
                 yAsUp,balPriceDown,balPriceUp,BlockSize,Tau):
    
    blockResults = {}    
    
    for blockSize in BlockSize:
        for tau in Tau:
       # print('Simulation year %g.' % y)
            blockSim = studyCases(studyCaseDict,startYear,startMonth,startDay,studyDays,
                       priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,
                       Tau=tau,blockSize=blockSize)
        
            blockResults[str(blockSize)+'_'+str(tau)] = blockSim.returnResults()
        #blockSim.plotPS()

        
    return blockResults    
    
def fixIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
             yAsUp,balPriceDown,balPriceUp,FixFrac,Tau):

    fixResults = {}    
    
    for fixFrac in FixFrac:
        print('fixFrac: %g' %fixFrac)
        for tau in Tau:
            print('tau: %g' %tau)
       # print('Simulation year %g.' % y)
            fixSim = studyCases(studyCaseDict,startYear,startMonth,startDay,studyDays,
                       priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,
                       Tau=tau,fixFrac=fixFrac)
        
            fixResults[str(fixFrac)+'_'+str(tau)] = fixSim.returnResults()
    #blockSim.plotPS()

    return fixResults    

def tauIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
                 yAsUp,balPriceDown,balPriceUp,Tau):
    
    tauResults = {}    
    
    for tau in Tau:
        print('Simulating with tau: %g' %tau)
       # print('Simulation year %g.' % y)
        tauSim = studyCases(studyCaseDict,startYear,startMonth,startDay,studyDays,
                   priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,
                   Tau=tau)
        
        tauResults[str(tau)] = tauSim.returnResults()
        #tauSim.plotPS()
        
#    for tau in Tau:    
#        print(tau)
#        print(tauResults[str(tau)]['unitCostDF'])
        
    return tauResults
    
def lamNDIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
                 yAsUp,balPriceDown,balPriceUp,LamND):

    lamNDResults = {}
    
    for lamND in LamND:
        lamNDSim = studyCases(studyCaseDict,startYear,startMonth,startDay,studyDays,
                   priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,
                   Tau=0.04,lamND=lamND)
                  
        lamNDResults[str(lamND)] = lamNDSim.returnResults()
        
    for lamND in LamND:   
        print(lamND)
        print(lamNDResults[str(lamND)]['unitCostDF'])
        
    return lamNDResults
    
def NDRTIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
                 yAsUp,balPriceDown,balPriceUp,LamND,Tau):

    lamNDResults = {}
    
    for tau in Tau:
        for lamND in LamND:
            print('tau: %g' %tau)
            print('NDRTFrac: %g' %lamND)
            lamNDSim = studyCases(studyCaseDict,startYear,startMonth,startDay,studyDays,
                       priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,
                       Tau=tau,NDRTFrac=lamND,NDRTPenaly=True)
            
            lamNDResults[str(lamND)+'_'+str(tau)] = lamNDSim.returnResults() 
        #lamNDSim.plotPS()
        
#    for lamND in LamND:   
#        print(lamND)
#        print(lamNDResults[str(lamND)]['unitCostDF'])
        
    return lamNDResults
    
    
def alphaFixSnIter(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
                 yAsUp,balPriceDown,balPriceUp,AlphaFix,Sn,tau):

    alphaFlexWTauSnResults = {}
    alphaFlexWOTauSnResults = {}
    for case in studyCaseDict:
        alphaFlexWTauSnResults[case] = pd.DataFrame(columns=Sn)
        alphaFlexWOTauSnResults[case] = pd.DataFrame(columns=Sn)
    
    alphaFlexSnResultsDumpAll = {}
    
    for alphaFix in AlphaFix:
        print('AlphaFix = %g' %alphaFix)
        alphaFlexSnResultsDumpAll[alphaFix] = {}
        
        # Reset temp dict        
#        snTempResult = {}
#        for case in studyCaseDict:
#            snTempResult[case] = []

        for sn in Sn:
            print('Sn = %g' %sn)
            alphaFlexSnResultsDumpAll[alphaFix][sn] = {}
            alphaFlexSnSim = studyCases(studyCaseDict,startYear,startMonth,startDay,
                       studyDays,priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,
                       Tau=tau,Sn=sn,alphaFix=alphaFix,alphaFlex=0.0)
            
            for case in studyCaseDict:
                alphaFlexWTauSnResults[case].loc[str(alphaFix),sn] = alphaFlexSnSim.returnUnitCostsWTau()[case]
                alphaFlexWOTauSnResults[case].loc[str(alphaFix),sn] = alphaFlexSnSim.returnUnitCostsWOTau()[case]
                alphaFlexSnResultsDumpAll[alphaFix][sn] = alphaFlexSnSim.returnResults()
        

#        for case in studyCaseDict:
#            alphaFlexSnResults[case].loc[str(alphaFix)] = snTempResult[case]

        
    return {'DfWTau':alphaFlexWTauSnResults,
            'DfWOTau':alphaFlexWOTauSnResults,
            'All':alphaFlexSnResultsDumpAll}
            
def SnIter(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
                 yAsUp,balPriceDown,balPriceUp,Sn):

    #alphaFlexWTauSnResults = {}
    #alphaFlexWOTauSnResults = {}
    alphaFlexWTauSnResults = pd.DataFrame(columns=Sn)
    alphaFlexWOTauSnResults = pd.DataFrame(columns=Sn)
    
    alphaFlexSnResultsDumpAll = {}
    

    for sn in Sn:
        print('Sn = %g' %sn)
        alphaFlexSnResultsDumpAll[sn] = {}
        alphaFlexSnSim = studyCases(studyCaseDict,startYear,startMonth,startDay,
                   studyDays,priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,
                   Tau=0.20,Sn=sn,alphaFix=0.6,alphaFlex=0.0)
        
        for case in studyCaseDict:
            alphaFlexWTauSnResults.loc[case,sn] = alphaFlexSnSim.returnUnitCostsWTau()[case]
            alphaFlexWOTauSnResults.loc[case,sn] = alphaFlexSnSim.returnUnitCostsWOTau()[case]
            alphaFlexSnResultsDumpAll[case] = alphaFlexSnSim.returnResults()
        

#        for case in studyCaseDict:
#            alphaFlexSnResults[case].loc[str(alphaFix)] = snTempResult[case]

        
    return {'DfWTau':alphaFlexWTauSnResults,
            'DfWOTau':alphaFlexWOTauSnResults,
            'All':alphaFlexSnResultsDumpAll}
            
def alphaFlexSnIter(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
                 yAsUp,balPriceDown,balPriceUp,AlphaFlex,Sn):

    alphaFlexWTauSnResults = {}
    alphaFlexWOTauSnResults = {}
    for case in studyCaseDict:
        alphaFlexWTauSnResults[case] = pd.DataFrame(columns=Sn)
        alphaFlexWOTauSnResults[case] = pd.DataFrame(columns=Sn)
    
    alphaFlexSnResultsDumpAll = {}
    
    for alphaFlex in AlphaFlex:
        print('AlphaFlex = %g' %alphaFlex)
        
        alphaFlexSnResultsDumpAll[alphaFlex] = {}
        
        # Reset temp dict        
#        snTempResult = {}
#        for case in studyCaseDict:
#            snTempResult[case] = []

        for sn in Sn:
            print('Sn = %g' %sn)
            alphaFlexSnResultsDumpAll[alphaFlex][sn] = {}
            alphaFlexSnSim = studyCases(studyCaseDict,startYear,startMonth,startDay,
                       studyDays,priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,
                       Tau=0.2,Sn=sn,alphaFix=0.6*(1-alphaFlex),alphaFlex=0.6*alphaFlex)
            
            for case in studyCaseDict:
                alphaFlexWTauSnResults[case].loc[str(alphaFlex),sn] = alphaFlexSnSim.returnUnitCostsWTau()[case]
                alphaFlexWOTauSnResults[case].loc[str(alphaFlex),sn] = alphaFlexSnSim.returnUnitCostsWOTau()[case]
                alphaFlexSnResultsDumpAll[alphaFlex][sn] = alphaFlexSnSim.returnResults()
        

#        for case in studyCaseDict:
#            alphaFlexSnResults[case].loc[str(alphaFix)] = snTempResult[case]

        
    return {'DfWTau':alphaFlexWTauSnResults,
            'DfWOTau':alphaFlexWOTauSnResults,
            'All':alphaFlexSnResultsDumpAll}
            
def alphaFlexTotIter(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
                 yAsUp,balPriceDown,balPriceUp,AlphaFlex,AlphaTot):

    alphaFlexWTauSnResults = {}
    alphaFlexWOTauSnResults = {}
    for case in studyCaseDict:
        alphaFlexWTauSnResults[case] = pd.DataFrame(columns=AlphaTot)
        alphaFlexWOTauSnResults[case] = pd.DataFrame(columns=AlphaTot)
    
    alphaFlexSnResultsDumpAll = {}
    
    for alphaFlex in AlphaFlex:
        print('AlphaFlex = %g' %alphaFlex)
        
        alphaFlexSnResultsDumpAll[alphaFlex] = {}
        
        # Reset temp dict        
#        snTempResult = {}
#        for case in studyCaseDict:
#            snTempResult[case] = []

        for alphaTot in AlphaTot:
            if 0 == 0:
                print('alphaTot = %g' %alphaTot)
                alphaFlexSnResultsDumpAll[alphaFlex][alphaTot] = {}
                alphaFlexSnSim = studyCases(studyCaseDict,startYear,startMonth,startDay,
                           studyDays,priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,
                           Tau=0.2,Sn=0,alphaFix=alphaTot*(1-alphaFlex),alphaFlex=alphaTot*alphaFlex)
            
            for case in studyCaseDict:
                alphaFlexWTauSnResults[case].loc[str(alphaFlex),alphaTot] = alphaFlexSnSim.returnUnitCostsWTau()[case]
                alphaFlexWOTauSnResults[case].loc[str(alphaFlex),alphaTot] = alphaFlexSnSim.returnUnitCostsWOTau()[case]
                alphaFlexSnResultsDumpAll[alphaFlex][alphaTot] = alphaFlexSnSim.returnResults()
        

#        for case in studyCaseDict:
#            alphaFlexSnResults[case].loc[str(alphaFix)] = snTempResult[case]

        
    return {'DfWTau':alphaFlexWTauSnResults,
            'DfWOTau':alphaFlexWOTauSnResults,
            'All':alphaFlexSnResultsDumpAll}