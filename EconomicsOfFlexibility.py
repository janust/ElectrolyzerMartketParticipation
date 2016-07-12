# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 15:15:20 2016

@author: Janus
"""

from PlotResults import alphaFixSnContourPlot
import pandas as pd

def economicsOfFlexibility(alphaFlexSnResults,AlphaFix,Sn,name):
    CInvElec = 35000 # €/(kg h^-1), calculating quantities
    CInvStor = 850 # €/kg, # 11 €/kWh, 33.3 kWh/kg, technology data
    pPn = 100
    r = 0.04
    
    ICost = pd.DataFrame(columns=Sn)
    
    for alphaFix in AlphaFix:
        for sn in Sn:
            ICost.loc[str(alphaFix),sn] = pPn*(CInvElec/alphaFix + CInvStor*sn)
    
    lifeTime = pd.DataFrame(columns=Sn)                          
    lifeTimeOC = pd.DataFrame(columns=Sn)  #alphaFlexSnResults['Df']['Perfect']
    lifeTimeTC = pd.DataFrame(columns=Sn)
    lifetimeEAC = pd.DataFrame(columns=Sn)
    
    shelfLife = 30
    
    for alphaFix in AlphaFix:
        for sn in Sn:
            lifeTime.loc[str(alphaFix),sn] = min([1/(alphaFlexSnResults['All'][alphaFix][sn]['allResults'][name]['beta']['sumTot']
                                                    *8760/len(alphaFlexSnResults['All'][alphaFix][sn]['allResults'][name]['pP'])),shelfLife]) # Normalize to one year of operation
            lifeTimeOC.loc[str(alphaFix),sn] = (alphaFlexSnResults['DfWOTau'][name].loc[str(alphaFix),sn]
                                            *(pPn*24*365*sum((1/(1+r)**n) 
                                            for n in list(range(1,round(lifeTime.loc[str(alphaFix),sn]))))))
            lifeTimeTC.loc[str(alphaFix),sn] = lifeTimeOC.loc[str(alphaFix),sn] + ICost.loc[str(alphaFix),sn]
            lifetimeEAC.loc[str(alphaFix),sn] = (lifeTimeTC.loc[str(alphaFix),sn]
                                                /sum((1/(1+r)**n) for n in list(range(1,round(lifeTime.loc[str(alphaFix),sn])))))
    
    DlifetimeEAC = pd.DataFrame(columns=Sn)                                    
    for alphaFix in AlphaFix:
        for sn in Sn:        
            DlifetimeEAC.loc[str(alphaFix),sn] = ((lifetimeEAC.loc['1.0',0] - lifetimeEAC.loc[str(alphaFix),sn])/lifetimeEAC.loc['1.0',0])*100
      
    df = DlifetimeEAC
    alphaFixSnContourPlot(df,name+'_2015')
                                            
    return {'EAC': DlifetimeEAC,
            'L': lifeTime}
    
                                     
    