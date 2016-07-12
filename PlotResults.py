# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 08:32:53 2016

@author: Janus
"""

# Plot results

import matplotlib.pyplot as plt
import numpy as np

class plotResults():

    def __init__(self,simuName,prefix):
        self.simuName = simuName
        self.prefix = prefix         
        
        self.fig1 = plt.figure(figsize=(5,5))
        
    def plotND(self,x1=[],y1=[],name1=[],x2=[],y2=[],name2=[]):
        simuName = self.simuName          
        fig1 = self.fig1
        
        ax11 = fig1.add_subplot(1,1,1)
        ax11.hold(True)
        ax11.set_title(simuName,y=1.29)
        
        box = ax11.get_position()
        ax11.set_position([box.x0, box.y0, box.width*1, box.height])
        
        if x1 != []:
            ax11.plot(x1,y1,'g-',label=name1)

        if x2 != []:
            ax11.plot(x2,y2,'b-',label=name2)
            
        ax11.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=8, ncol=3, 
                    borderaxespad=0.02, mode="expand")#bbox_to_anchor=(0, 1.2), loc='upper left', ncol=3)#loc = 0)#, bbox_to_anchor = (0, 0))
        
        ax11.set_xlabel('$\mathrm{\lambda^{ND} [€/kg]}$')
        ax11.set_ylabel('ND Pct.')
        
    def plotNDcost(self,x1=[],y1=[],name1=[],x2=[],y2=[],name2=[],y3=[],
                   name3=[],y4=[],name4=[]):
        simuName = self.simuName          
        fig1 = self.fig1
        
        ax11 = fig1.add_subplot(1,1,1)
        ax11.hold(True)
        ax11.set_title(simuName,y=1.29)
        
        box = ax11.get_position()
        ax11.set_position([box.x0, box.y0, box.width*1, box.height])
        
        if y1 != []:
            ax11.plot(x1,y1,'g-',label=name1)

        if y2 != []:
            ax11.plot(x1,y2,'b-',label=name2)
        if y3 != []:
            ax11.plot(x1,y3,'r-',label=name3)
        if y4 != []:
            ax11.plot(x1,y4,'m-',label=name4)
            
        ax11.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=8, ncol=2, 
                    borderaxespad=0.02, mode="expand")#bbox_to_anchor=(0, 1.2), loc='upper left', ncol=3)#loc = 0)#, bbox_to_anchor = (0, 0))
        
        ax11.set_xlabel('$\mathrm{\lambda^{ND} [€/kg]}$')
        ax11.set_ylabel('Unit Cost')
        
        #ax11.set_ylim([0,1.5])
        
    def plotProduction(self,pP,pPDA=[1],pPAS=[1]):#pPBlock=[1],
        simuName = self.simuName        
        fig1 = self.fig1
        
        ax11 = fig1.add_subplot(3,1,1)
        ax11.hold(True)
        ax11.set_title(simuName,y=1.59)
        
        box = ax11.get_position()
        ax11.set_position([box.x0, box.y0, box.width*1, box.height])

        ax11.plot(pP,'g-',label='Total')
#        if pPBlock != [1]:
#            ax11.plot(pPBlock,'k-',label='Day Ahead Block')        
        if pPDA != [1]:
            ax11.plot(pPDA,'b-',label='Day Ahead')
        if pPAS != [1]:
            ax11.plot(pPAS,'r-',label='Balancing')
        
        #if pPDA != [1]:
        #ax11.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=8, ncol=3, borderaxespad=0.02, mode="expand")#bbox_to_anchor=(0, 1.2), loc='upper left', ncol=3)#loc = 0)#, bbox_to_anchor = (0, 0))
        #else:
            #ax11.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=8, ncol=1, borderaxespad=0.)#, mode="expand", borderaxespad=0.)
            #ax11.legend(loc=0)
        
        ax11.set_ylabel('$\mathrm{H_2}$ prod. [kg/hour]')    
        
        ax11.set_ylim([min(min(pP,pPDA,pPAS))-0.1*max(max(pP,pPDA,pPAS)),1.1*max(max(pP,pPDA,pPAS))])
        
    def plotDAPrice(self,DAPrice,DAPrice2=[]):
        fig1 = self.fig1        
        
        ax12 = fig1.add_subplot(3,1,3)
        ax12.plot(DAPrice,'b-',label='Test2')
        if DAPrice2 != []:
            ax12.plot(DAPrice2,'b--',label='Test2')
        box = ax12.get_position()
        ax12.set_position([box.x0, box.y0, box.width*1, box.height])
        ax12.set_ylabel('DA forecast [€/MWh]')
        ax12.set_xlabel('Time [hour]')
        #ax12.legend(loc = 0)#, bbox_to_anchor = (0, 0))
        
    
    def plotStorage(self,S):
        fig1 = self.fig1        
        
        ax12 = fig1.add_subplot(3,1,2)
        ax12.plot(S,'b-',label='SOC')
        box = ax12.get_position()
        ax12.set_position([box.x0, box.y0, box.width*1, box.height])
        ax12.set_ylabel('$\mathrm{H_2}$ SOC [kg]')
        ax12.set_xlabel('Time [hour]')
        
        
    def saveFig(self):
        fig1 = self.fig1
        simuName = self.simuName
        prefix = self.prefix
        
        fig1.savefig('figures/'+prefix+simuName+'.eps', format='eps', dpi=1000)
        
        
        
def plotND(lamNDResults,LamND):
    plotTemp1 = plotResults('NDpct','')
    
    #x1 = []
    #y1 = []
    x2 = []
    y2 = []
                              
    for lamND in LamND:
        #x1.append(lamND)
        #y1.append(lamNDResults[str(lamND)]['unitCostDF']['ND Pct.']['AsPerfectNDP'])
        x2.append(lamND)
        y2.append(lamNDResults[str(lamND)]['unitCostDF']['ND Pct.']['AsCoOptNDP'])
    
    plotTemp1.plotND(x2=x2,y2=y2,name2='AsCoOptNDP')#x1=x1,y1=y1,name1='AsPerfectNDP',
    plotTemp1.saveFig()#'figures/plotNDpct.eps', format='eps', dpi=1000)
    
    
    plotTemp2 = plotResults('NDTotalCosts','')
    x1 = []
    #y1 = []
    #y2 = []
    y3 = []
    y4 = []

    for lamND in LamND:
        x1.append(lamND)
        #y1.append(lamNDResults[str(lamND)]['unitCostDF']['Total Costs']['AsPerfectNDP'])
        #y2.append(lamNDResults[str(lamND)]['unitCostDF']['Total Costs']['AsPerfect'])
        y3.append(lamNDResults[str(lamND)]['unitCostDF']['Total Costs']['AsCoOptNDP'])
        y4.append(lamNDResults[str(lamND)]['unitCostDF']['Total Costs']['AsCoOpt'])
    
    plotTemp2.plotNDcost(x1=x1,y3=y3,name3='AsCoOptNDP',y4=y4,name4='AsCoOpt')#x1=x1,y1=y1,name1='AsPerfectNDP',x2=x1,y2=y2,name2='AsPerfect',
    plotTemp2.saveFig()#'figures/plotNDTotalCosts.eps', format='eps', dpi=1000)       
    
    plotTemp3 = plotResults('NDUnitCosts','')
    x1 = []
    #y1 = []
    #y2 = []
    y3 = []
    y4 = []

    for lamND in LamND:
        x1.append(lamND)
        #y1.append(lamNDResults[str(lamND)]['unitCostDF']['DA&AS&Tau&ND']['AsPerfectNDP'])
        #y2.append(lamNDResults[str(lamND)]['unitCostDF']['DA&AS&Tau&ND']['AsPerfect'])
        y3.append(lamNDResults[str(lamND)]['unitCostDF']['DA&AS&Tau&ND']['AsCoOptNDP'])
        y4.append(lamNDResults[str(lamND)]['unitCostDF']['DA&AS&Tau&ND']['AsCoOpt'])
    
    plotTemp3.plotNDcost(x1=x1,y3=y3,name3='AsCoOptNDP',y4=y4,name4='AsCoOpt')#x1=x1,y1=y1,name1='AsPerfectNDP',x2=x1,y2=y2,name2='AsPerfect',
    
    plotTemp3.saveFig()#'figures/plotNDUnitCosts.eps', format='eps', dpi=1000)  
    
def alphaFixSnContourPlot(df,case):
    im = plt.contourf(df.values,# np.arange(df.values.min(), df.values.max(), 0.2), 
                      cmap=plt.cm.YlOrRd_r)#)#, extent=(-3, 3, 3, -3))  
    cset = plt.contour(df.values,# np.arange(df.values.min(), df.values.max(), 0.2), 
                       linewidths=2,
                       cmap=plt.cm.winter_r)#,
                       #extent=(-3, 3, -3, 3))#, 
    plt.yticks(np.arange(0, len(df.index), 1), df.index)
    plt.xticks(np.arange(0, len(df.columns), 1), df.columns)
    plt.xlabel('Storage hours')
    plt.ylabel('$\mathrm{α^{Fix}}$', fontsize=13)
    plt.clabel(cset, inline=True, fmt='%1.2f', fontsize=10)
    plt.colorbar(im)
    plt.savefig('figures/ecoEAC_'+case+'.eps', format='eps', dpi=1000)
    plt.show()
    
def alphaFlexSnContourPlot(df,case):
    im = plt.contourf(df.values,# np.arange(df.values.min(), df.values.max(), 0.2), 
                      cmap=plt.cm.autumn)#, extent=(-3, 3, 3, -3))  
    cset = plt.contour(df.values,# np.arange(df.values.min(), df.values.max(), 0.2), 
                       linewidths=2,
                       cmap=plt.cm.winter)#,
                       #extent=(-3, 3, -3, 3))#, 
    plt.yticks(np.arange(0, len(df.index), 1), df.index)
    plt.xticks(np.arange(0, len(df.columns), 1), df.columns)
    plt.xlabel('Storage hours', fontsize=10)
    plt.ylabel('$\mathrm{α^{Flex}/α^{Tot}}$', fontsize=13)
    plt.clabel(cset, inline=True, fmt='%1.2f', fontsize=10)
    plt.colorbar(im)
    plt.savefig('figures/alphaFlexSn_'+case+'.eps', format='eps', dpi=1000)
    plt.show()
    
def alphaFlexTotContourPlot(df,case):
    im = plt.contourf(df.values,# np.arange(df.values.min(), df.values.max(), 0.2), 
                      cmap=plt.cm.autumn)#, extent=(-3, 3, 3, -3))  
    cset = plt.contour(df.values,# np.arange(df.values.min(), df.values.max(), 0.2), 
                       linewidths=2,
                       cmap=plt.cm.winter)#,
                       #extent=(-3, 3, -3, 3))#, 
    plt.yticks(np.arange(0, len(df.index), 1), df.index)
    plt.xticks(np.arange(0, len(df.columns), 1), df.columns)
    plt.xlabel('$\mathrm{α^{Tot}}$', fontsize=13)
    plt.ylabel('$\mathrm{α^{Flex}/α^{Tot}}$', fontsize=13)
    plt.clabel(cset, inline=True, fmt='%1.2f', fontsize=10)
    plt.colorbar(im)
    plt.savefig('figures/alphaFlexTot_'+case+'.eps', format='eps', dpi=1000)
    plt.show()

def SnIterPlot(df,studyCaseDict,ylim=[],xlim=[],name=''):
    fig1 = plt.figure(figsize=(5,3))
    ax11 = fig1.add_subplot(1,1,1)
    
    for case in studyCaseDict:
        ax11.plot(df.loc[case,:],'-',label=case)
        
    ax11.set_xlabel('Storage Hours')
    ax11.set_ylabel('Unit Costs [€/kg]')
    ax11.legend()
    
    
def plotBlockUnitCosts(df,studyCaseDict,ylim=[],xlim=[],name=''):
    #self.simuName = simuName
    #self.prefix = prefix         
    
    fig1 = plt.figure(figsize=(7,2.5))
    
    ax11 = fig1.add_subplot(1,1,1)
    ax11.hold(True)
    #ax12 = fig1.add_subplot(2,1,2)
    #ax12.hold(True)
    #ax11.set_title(simuName,y=1.59)

    styleDict = {'Base':'-.',
                 'Simple':'-',
                 'SimpleBlockOrder':'-',
                 'Perfect':'-',
                 'AsCoOpt':'--',
                 'AsCoOptNDP':'--',
                 'AsFix':'--',
                 'As2':'--',
                 'As2_33':'--'}
    
    colorDict = {'Base':'k',
                 'Simple':'b',
                 'SimpleBlockOrder':'g',
                 'Perfect':'m',
                 'AsCoOpt':'c',
                 'AsCoOptNDP':'r',
                 'AsFix':'y',
                 'As2':'#420911',
                 'As2_33': '#ea40af'}
#                 
    nameDict =  {'Base':'DABase',
                 'Simple':'DASimple',
                 'SimpleBlockOrder':'DASimpleB.O.',
                 'Perfect':'DAPerfect',
                 'AsCoOpt':'RPCoOpt',
                 'AsCoOptNDP':'RPCoOptNDP',
                 'AsFix':'RPFix',
                 'As2':'RPPostDA',
                 'As2_33': 'RPPostDA33'}
    
    for column in studyCaseDict:
        ax11.plot([float(a) for a in df.index.tolist()],
                  [df.loc[index,column] for index in df.index.tolist()],
                  styleDict[column],color=colorDict[column],label=nameDict[column])
#    for column,name in zip(df.columns.tolist(),['Simple','SimpleNt','SimpleBo','SimpleBoNt']):
#        ax12.plot([float(a) for a in df.index.tolist()],
#                  [df.loc[index,column] for index in df.index.tolist()],
#                  label=name)
        
    #ax11.legend(loc=0)
    lgd = ax11.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=8, ncol=3, 
                    borderaxespad=0.02, mode="expand")
    
    ax11.set_xlabel('$\mathrm{τ^{Dyn} [€/kg]}$', fontsize=13)
    ax11.set_ylabel('Total Cost, Base = 100')
    #ax12.set_ylabel('$\mathrm{H_2\ Unit\ Cost\ [€/kg]}$')
    
#    ax11.set_xlabel('$\mathrm{H_2 Unic Cost} [€/kg]}$')
#    ax11.set_ylabel('$\mathrm{ [€/(kg h^{-1}]$')
    #ax11.set_ylim([0.95*min(min([df.loc[:,column].tolist() for column in ['Simple','SimpleBlockOrder']])),
    #               1.5*max(max([df.loc[:,column].tolist() for column in ['Simple','SimpleBlockOrder']]))])
    #ax11.set_ylim([1.4,2.5])
    #ax11.set_xlim([0,2])
    #ax11.set_ylim([0.9,1.25])
    if ylim != []:
        ax11.set_ylim(ylim)
    if xlim != []:
        ax11.set_xlim(xlim)
    #ax11.set_xlim([0,8])
    
    fig1.savefig('figures/TauBigCompare'+str(name)+'.eps', format='eps', dpi=1000, bbox_extra_artists=(lgd,), bbox_inches='tight')
    
def plotBlockUnitCosts2(df):
    #self.simuName = simuName
    #self.prefix = prefix

    styleDict = {'SimBoNt_0.05':'--g',
                 'Simple_0.05':'-g',
                 'SimBoNt_0.2':'--b',
                 'Simple_0.2':'-b',
                 'SimBoNt_2.0':'--r',
                 'Simple_2.0':'-r'}
                 
    nameDict =  {'SimBoNt_0.05':'SimBo_0.05',
                 'Simple_0.05':'Sim_0.05',
                 'SimBoNt_0.2':'SimBo_0.2',
                 'Simple_0.2':'Sim_0.2',
                 'SimBoNt_2.0':'SimBo_2.0',
                 'Simple_2.0':'Sim_2.0'} 
    
    fig1 = plt.figure(figsize=(6,2.5))
    
    ax11 = fig1.add_subplot(1,1,1)
    ax11.hold(True)
    #ax11.set_title(simuName,y=1.59)
    
    for column in df.columns.tolist():
        ax11.plot([float(a) for a in df.index.tolist()],
                  [df.loc[index,column] for index in df.index.tolist()],
                  styleDict[column],label=nameDict[column])
        
    #ax11.legend(loc=0)
    
    ax11.set_xlabel('$\mathrm{Block\ Size\ [Hours]}$')
    ax11.set_ylabel('$\mathrm{H_2\ Unit\ Cost\ [€/kg]}$')
    
#    box = ax11.get_position()
#    ax11.set_position([box.x0, box.y0, box.width*1, box.height])
    lgd = ax11.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=8, ncol=3, 
                    borderaxespad=0.02, mode="expand")
                    
    
    
#    ax11.set_xlabel('$\mathrm{H_2 Unic Cost} [€/kg]}$')
#    ax11.set_ylabel('$\mathrm{ [€/(kg h^{-1}]$')
    #ax11.set_ylim([0.95*min(min([df.loc[:,column].tolist() for column in ['Simple']])),
                   #1.05*max(max([df.loc[:,column].tolist() for column in ['Simple']]))])
    ax11.set_ylim([1.0,1.3])
    
    
    
    fig1.savefig('figures/BlockOrderUCblockSize.eps', format='eps', dpi=1000, bbox_extra_artists=(lgd,), bbox_inches='tight')

def blockContourPlot(df):
    im = plt.contourf(df.values,figsize=(2,2),# np.arange(df.values.min(), df.values.max(), 0.2), 
                      cmap=plt.cm.autumn)#, extent=(-3, 3, 3, -3))  
    cset = plt.contour(df.values,figsize=(2,2),# np.arange(df.values.min(), df.values.max(), 0.2), 
                       linewidths=2,
                       cmap=plt.cm.winter)#,
                       #extent=(-3, 3, -3, 3))#, 
    plt.yticks(np.arange(0, len(df.index), 1), df.index)
    plt.xticks(np.arange(0, len(df.columns), 1), df.columns)
    plt.clabel(cset, inline=True, fmt='%1.2f', fontsize=10)
    plt.colorbar(im)
    plt.xlabel('$\mathrm{Block\ Size\ [Hours]}$')
    plt.ylabel('$\mathrm{τ^{Dyn} [€/kg]}$')
    plt.savefig('figures/blockContourPlot.eps', format='eps', dpi=1000)
    plt.show()
    
def fixContourPlot(df):
    im = plt.contourf(df.values,figsize=(2,2),# np.arange(df.values.min(), df.values.max(), 0.2), 
                      cmap=plt.cm.autumn)#, extent=(-3, 3, 3, -3))  
    cset = plt.contour(df.values,figsize=(2,2),# np.arange(df.values.min(), df.values.max(), 0.2), 
                       linewidths=2,
                       cmap=plt.cm.winter)#,
                       #extent=(-3, 3, -3, 3))#, 
    plt.yticks(np.arange(0, len(df.index), 1), df.index)
    plt.xticks(np.arange(0, len(df.columns), 1), df.columns)
    plt.clabel(cset, inline=True, fmt='%1.2f', fontsize=10)
    plt.colorbar(im)
    plt.xlabel('$\mathrm{\gamma{Fix}}$')
    plt.ylabel('$\mathrm{τ^{Dyn} [€/kg]}$')
    plt.savefig('figures/fixContourPlot.eps', format='eps', dpi=1000)
    plt.show()

def plotFixFracUnitCosts(df):
    #self.simuName = simuName
    #self.prefix = prefix

#    styleDict = {'SimBoNt_0.05':'--g',
#                 'Simple_0.05':'-g',
#                 'SimBoNt_0.2':'--b',
#                 'Simple_0.2':'-b',
#                 'SimBoNt_2.0':'--r',
#                 'Simple_2.0':'-r'}
#                 
#    nameDict =  {'SimBoNt_0.05':'SimBo_0.05',
#                 'Simple_0.05':'Sim_0.05',
#                 'SimBoNt_0.2':'SimBo_0.2',
#                 'Simple_0.2':'Sim_0.2',
#                 'SimBoNt_2.0':'SimBo_2.0',
#                 'Simple_2.0':'Sim_2.0'} 
    
    fig1 = plt.figure(figsize=(6,2.5))
    
    ax11 = fig1.add_subplot(1,1,1)
    ax11.hold(True)
    #ax11.set_title(simuName,y=1.59)
    
    for column in df.columns.tolist():
        ax11.plot([float(a) for a in df.index.tolist()],
                  [df.loc[index,column] for index in df.index.tolist()],
                  label=column)#styleDict[column],
        
    #ax11.legend(loc=0)
    
    ax11.set_xlabel('$\mathrm{Block\ Size\ [Hours]}$')
    ax11.set_ylabel('$\mathrm{H_2\ Unit\ Cost\ [€/kg]}$')
    
#    box = ax11.get_position()
#    ax11.set_position([box.x0, box.y0, box.width*1, box.height])
    lgd = ax11.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=8, ncol=3, 
                    borderaxespad=0.02, mode="expand")
                    
    
    
#    ax11.set_xlabel('$\mathrm{H_2 Unic Cost} [€/kg]}$')
#    ax11.set_ylabel('$\mathrm{ [€/(kg h^{-1}]$')
    #ax11.set_ylim([0.95*min(min([df.loc[:,column].tolist() for column in ['Simple']])),
                   #1.05*max(max([df.loc[:,column].tolist() for column in ['Simple']]))])
    #ax11.set_ylim([1.0,1.3])


    fig1.savefig('figures/fixFracUC.eps', format='eps', dpi=1000, bbox_extra_artists=(lgd,), bbox_inches='tight')

