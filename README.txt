This Github Repo contains Python 3.5 code that was written to solve 
electrolyzer participation strategies in the Western Denmark day-ahead
and regulating power markets. The strategies are formulated as mixed
integer linear programs and are solved using Gurobi 6.5.0. 
Further the code makes several plotting and out of sample calculations.
A master thesis was prepared as part of the work which gives a detailed
description of the theory behind. The thesis can be obtained by contacting
janus@tougaard.net.

----

Explanation of the files in this Github Repo:

* ImportPrices.py: RUN FIRST. This function shall be run first to import 
  market data from MarketData20102015.xlsx. Data is imported once to the
  Python Workspace to save time importing between model runs.

* styduYearsCall.py: Is the main script that calls the rest of scripts. 
  It contains a number of different study cases. All are commented out 
  except for the one under investigation.

* studyYeasrAncFcns.py: Contains functions that construct the different study
  cases and are called by styduYearsCall.py.

* elecStudyCases.py: This file activates the different participation 
  strategies based on the input from StudyCaseDict. It is called by 
  studyYeasrAncFcns.py

* DayIterationClass.py: Is called by elecStudyCases.py. This function itera-
  tes over the input days, calls the electrolyzer optimization class in
  elecOptClass.py and conducts the out of sample calculations.

* elecOptClass.py: This class contains the optimization model. The class
  is called by DayIterationClass.py

* PriceForecast.py: Class to perform the deterministic and stochastic 
  forecasting.

* PlotResults.py: File that contains the plotting scripts.

* EconomicsOfFlexibility.py: Function that conducts economic evaluation
  calculations on different investments in flexibility.

* MarketData20102015.xlsx: Day-ahead and regulating power market data 
  for Wesern Denmark from 2010 to 2015. Obtained from "http://energinet.dk/
  EN/El/Engrosmarked/Udtraek-af-markedsdata/Sider/default.aspx"
