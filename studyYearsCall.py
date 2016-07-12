# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 17:04:44 2016

@author: Janus
"""


from PlotResults import plotND,alphaFixSnContourPlot,plotResults,plotBlockUnitCosts,plotBlockUnitCosts2,blockContourPlot, fixContourPlot, plotFixFracUnitCosts, alphaFlexTotContourPlot, alphaFlexSnContourPlot, SnIterPlot
from studyYearsAncFcns import yearIteration, tauIteration, lamNDIteration, NDRTIteration, alphaFixSnIter, alphaFlexSnIter, blockIteration, fixIteration, alphaFlexTotIter, SnIter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from EconomicsOfFlexibility import economicsOfFlexibility

#%%Simulation duration and start
startYear = 2011
studyDays = 365 # Set to 365 when simulating multiple years
startMonth = 1
startDay = 1

#%% Study Cases



#studyCaseDict = ['AsPerfectNDP','AsCoOptNDP','AsPerfect','AsCoOpt']
#studyCaseDict = ['AsPerfect','AsCoOpt']
#studyCaseDict = ['Perfect','Simple']#Perfect','Simple']#,

#%% lamND iteration
        
#LamND = [0.0,0.5,1.0,2.0,4.0]
#lamNDResults = lamNDIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,
#                              priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,LamND)
##                             
#plotND(lamNDResults)
        
#%% NDRT iteration     
#studyCaseDict = ['AsCoOptNDP','AsCoOpt']
#LamND = [1.5]#,3.0,5.0]0.5,1.0,,2.0
#Tau = [0.0,0.05,0.2,2.0,8.0]
#lamNDResults = NDRTIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,
#                              priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,LamND,Tau)
#lamNDforPlot = {}
#for a in lamNDResults.keys():
#    if '0.05' in a:
#        lamNDforPlot[a[0:3]] = lamNDResults[a]          
#plotND(lamNDforPlot,LamND)

#%% Year Iteration
#studyCaseDict = ['Base','Perfect','Simple','SimpleBlockOrder','AsPerfect','AsPerfectNDP','As2','AsCoOpt','AsCoOptNDP','AsFix']        
#yearResults = yearIteration(studyCaseDict,startYear,deltaYears,startMonth,startDay,
#                            studyDays,priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,
#                            plotPS=True,Tau=0.0)
       
#%% Block Size & Tau Iteration
#studyCaseDict = ['SimpleBlockOrder']
#Tau = [0.05,0.2,2.0]
#BlockSize = [1,2,3,4,6,8,12,24]
#blockResults = blockIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
#                              yAsUp,balPriceDown,balPriceUp,BlockSize,Tau)
#                     
#blockDF = pd.DataFrame(columns=studyCaseDict)
#for case in studyCaseDict:
#    for tau in Tau:
#        for block in BlockSize:
#            blockDF.loc[str(tau),block] = blockResults[str(block)+'_'+str(tau)]['unitCostDF'].loc[case,'DA&AS&Tau&ND']
#blockDF = blockDF.drop('SimpleBlockOrder', 1)
##blockDF = blockDF.drop('SimBoNt', 1)
#
#blockContourPlot(blockDF)

#plotBlockUnitCosts2(blockDF)

#%% Tau iteration
#studyCaseDict = ['As2']
#Tau = [0.0,0.05,0.2,2.0,8.0]#,8.51]#0.04,0.09,0.43,0.85,
#tauResults = tauIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,
#                    priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,Tau)
#                    
#tauDF = pd.DataFrame(columns=studyCaseDict)
#for case in studyCaseDict:
#    for tau in Tau:
#        tauDF.loc[str(tau),case] = tauResults[str(tau)]['unitCostDF'].loc[case,'DA&AS&Tau&ND']

#plotBlockUnitCosts(tauDF)

#%% Tau iteration for all
#studyCaseDict = ['Base','Simple','SimpleBlockOrder','Perfect','AsCoOpt','AsCoOptNDP','AsFix','As2','As2_33']#,'AsPerfect']#
#Tau = [0.0,0.05,0.2,0.6,1.4,2.0,8.0]#[]
##tauResults = tauIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,
##                    priceWDate,yAsDown,yAsUp,balPriceDown,balPriceUp,Tau)
##                    
#tauDFUC = pd.DataFrame(columns=studyCaseDict)
#tauDFTC = pd.DataFrame(columns=studyCaseDict)
#tauDFTC100 = pd.DataFrame(columns=studyCaseDict)
#for case in studyCaseDict:
#    for tau in Tau:
#        tauDFUC.loc[str(tau),case] = tauResults[str(tau)]['unitCostDF'].loc[case,'DA&AS&Tau&ND']
#        tauDFTC.loc[str(tau),case] = tauResults[str(tau)]['unitCostDF'].loc[case,'Total Costs']
#for case in studyCaseDict:
#    for tau in Tau:        
#        tauDFTC100.loc[str(tau),case] = (tauResults[str(tau)]['unitCostDF'].loc[case,'Total Costs'] / 
#                                        tauResults[str(tau)]['unitCostDF'].loc['Base','Total Costs'])*100
#        
#plotBlockUnitCosts(tauDFUC,studyCaseDict,name='UC')
#plotBlockUnitCosts(tauDFTC,studyCaseDict,ylim=[4000000,4750000],xlim=[0,4],name='TC')
#plotBlockUnitCosts(tauDFTC100,studyCaseDict,name='TC100',ylim=[82,108],xlim=[0,3])


#%% Sn & alphaFix iteration
studyCaseDict = ['Simple','Perfect','As2_33']#,'AsCoOpt','As2'
Sn = np.arange(0,25,4).tolist()
AlphaFix = [round(a,1) for a in np.arange(0.2,1.1,0.2).tolist()] # Otherwise wired decimals show up

tau = 0.05

alphaFlexSnResults = alphaFixSnIter(studyCaseDict,startYear,startMonth,startDay,
                                     studyDays,priceWDate,yAsDown,
                                     yAsUp,balPriceDown,balPriceUp,AlphaFix,Sn,tau)
# Plot
ecoFlex = {}
for case in studyCaseDict:         
    # Plot unit costs on contour plot                         
#    df = alphaFlexSnResults['DfWTau'][case] # This one is with tau
#    alphaFixSnContourPlot(df,case)
    # Calculate and plot value of flex
    ecoFlex[case] = economicsOfFlexibility(alphaFlexSnResults,AlphaFix,Sn,case)

print('tau: %g' %tau)

# Calculate the discounting factor
#difac = pd.DataFrame(columns=Sn)
#for alphaFix in AlphaFix:
#    for sn in Sn:
#        difac.loc[str(alphaFix),sn] = sum((1/(1+r)**n) for n in list(range(1,round(lifeTime.loc[str(alphaFix),sn]))))
#print(difac)

#%% Fix frac & Tau Iteration
#studyCaseDict = ['AsFix']
#Tau = [0.05,0.2,0.8,2.0]
#fixFrac = [0.00,0.05,0.10,0.15,0.20]
#fixResults = fixIteration(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
#                              yAsUp,balPriceDown,balPriceUp,fixFrac,Tau)
#                     
#fixDF = pd.DataFrame(columns=fixFrac)
#for case in studyCaseDict:
#    for tau in Tau:
#        for frac in fixFrac:
#            fixDF.loc[str(tau),frac] = fixResults[str(frac)+'_'+str(tau)]['unitCostDF'].loc[case,'DA&AS&Tau&ND']
##fixDF = fixDF.drop('AsFix', 1)
##blockDF = blockDF.drop('SimBoNt', 1)
#
#fixContourPlot(fixDF)#.loc[[str(tau) for tau in Tau[0:3]],:])
#
#plotFixFracUnitCosts(fixDF)

#%% Alpha flex & Tau Iteration
#studyCaseDict = ['Simple']#,'Perfect','AsCoOpt']#
#AlphaFlexFrac = [0.0,0.3]
#Sn = [0,12]
#alphaFlexSnResults = alphaFlexSnIter(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
#                 yAsUp,balPriceDown,balPriceUp,AlphaFlexFrac,Sn)
##
##
###Plot
##ecoFlex = {}
#for case in studyCaseDict:         
#    df = alphaFlexSnResults['DfWTau'][case] # This one is with tau
#    df100 = pd.DataFrame(columns=Sn)
#    # Plot unit costs on contour plot
#    for sn in Sn:
#        for alphaFlex in AlphaFlexFrac:                     
#            df100.loc[str(alphaFlex),sn] = float(df.loc[str(alphaFlex),sn]/df.loc[str(0.0),12])*100
#    alphaFlexSnContourPlot(df100,case)
    #Calculate and plot value of flex
    #ecoFlex[case] = economicsOfFlexibility(flexResults,AlphaFix,Sn,case)


#%% Alpha flex & alpha tot iteration
#studyCaseDict = ['Simple']#,'Perfect','AsCoOpt']
#AlphaFlexFrac = [round(a,1) for a in np.arange(0,1.1,.1).tolist()]
#AlphaTot = [round(a,1) for a in np.arange(0.1,1.1,.1).tolist()]
#alphaFlexTotResults = alphaFlexTotIter(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
#                 yAsUp,balPriceDown,balPriceUp,AlphaFlexFrac,AlphaTot)
#
#
## Plot
##ecoFlex = {}
#for case in studyCaseDict:         
#    df = alphaFlexTotResults['DfWTau'][case] # This one is with tau
#    df100 = pd.DataFrame(columns=[a for a in reversed(AlphaTot)])
#    # Plot unit costs on contour plot
#    for alphaTot in [a for a in reversed(AlphaTot)]:
#        for alphaFlex in AlphaFlexFrac:
#            if 0 == 0:                    
#                df100.loc[str(alphaFlex),alphaTot] = float(df.loc[str(alphaFlex),alphaTot]/df.loc[str(0.0),1.0])*100
#    alphaFlexTotContourPlot(df100,case)
    # Calculate and plot value of flex
    #ecoFlex[case] = economicsOfFlexibility(flexResults,AlphaFix,Sn,case)


#%% Sn iteration
#studyCaseDict = ['AsCoOpt','As2','As2_33']
#Sn = np.arange(0,25,4).tolist()
#
#SnResults = SnIter(studyCaseDict,startYear,startMonth,startDay,studyDays,priceWDate,yAsDown,
#                            yAsUp,balPriceDown,balPriceUp,Sn)
#                            
#SnWtau = SnResults['DfWTau']
#
#SnIterPlot(SnWtau,studyCaseDict,ylim=[],xlim=[],name='')
#    
#
