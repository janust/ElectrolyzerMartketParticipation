# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 08:48:45 2016

@author: Janus
"""

# This function makes a simple forecast based on historic data
# NEEDS priceWDate dictionary

from datetime import timedelta

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
        
    
    
#from datetime import datetime   
#fDate = [datetime(2015,1,1,0,0,0)]
#for t in list(range(1,24)):
#    # Increase by one hour
#    fDate.append(fDate[t-1]+timedelta(0,0,0,0,0,1))
#
#testSimple = priceForecast(fDate,2,yAsDown).simple()
#testScn = priceForecast(fDate,2,yAsDown).scn()
#
#testAsScnDn = priceForecast(fDate,10,yAsDown).scn()
#testAsScnUp = priceForecast(fDate,10,yAsUp).scn()
#
#for key in testAsScnDn:
#    testAsScnDn[key].append(1)
#    testAsScnUp[key].append(0)
