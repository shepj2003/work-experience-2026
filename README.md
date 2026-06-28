# WORK EXPERIENCE PROJECT - Value at Risk, Expected Shortfall and Initial Margin

over the week we will investigate *initial margin* for a *bilteral  OTC derivative* portfolio. The aim is to have some idea of 
* what is initial margin ?
* why do banks care about it ?
* how do banks calculate how much initial margin to pay ? 
* how true are the underlying mathematical assumptions of models of initial margin ?
* **hard** how would a bank minimise the initial margin that they have to post - if you get this far, you may be interested working at Quantile


To help with this, in this repo there is 
* a README file (this file) with some basic definitions and some suggestions for how to investigate these topics
* some data
* some python helper functions
* some slides from a presentation that discussed these topics

There is not enough info here to answer all the above questiohs. You will most likely need to 
* use Google, ChatGPT, Claude (or read a book)
* ask the people you talk to during the week. This is somewhat quantile-centric, but everybody you talk to should be able to help
* compare notes and otherwise help eachother. This is not a competion.   


## financial background
* *bilateral OTC derivative* is any trade agreed between 2 parties (the party and the counterpaty) that somehow depends on 1 or more underlyig assets
* *initial margin* is an amount of money (collateral) exchanged to cover potential future exposure between when a counterparty defaults and the close out of the position (typically around 10 days) 

* *value at risk* is the estimated maximum loss over a given time horizon at a chosen confidence interval eg if you have 100 scenarios, $VaR(95\%)$ is the 5th worst loss

* *expected shortfall* is the average expected loss given that we have alredy lost at least $VaR$


## data
The file *google-finance-data-2006-2024.csv* contains some publicly available historical data for some stock indices (eg IBEX), some commodities (eg Gold) and some fxrates (eg USDEUR)

Annoyingly, not every date is available for every factor (why might this be ?). If a date is not avaialable for some factor then it is safe to assume that the value on that date is the same as on the most recent available date (eg if there is no data for July 4th, then assume that it does not change since July 3rd)

The file *utils.py* contains some python code to load this data into a pandas dataframe, and put everything on a consistent set of dates


## some ideas for an OTC derivative  portfolio 
1. buy or sell a combination of the  underlying assets $ V = \sum_i \alpha_i S_i$ (where $\alpha_i$ are constants, $S_i$ represents the value of the asset (eg the stock) )
2. buy or sell a *call option* on one underlying asset $ V = max (S - K_j, 0)$, for some fixed strikes, $K_j$
3. buy or sell a *put option* on one underlying asset $ V = max (K_j - S, 0)$ for some fixed strikes, $K_j$
4. buy or sell a *binary option* $V = 1 $  if  $ B_{lo} \lt S \lt B_{hi}$ ,   $0$ otherwise


## historical simulation 
1. compute the value at risk ($VaR$) and Expected Shortfall ($ES$) for some simple portfolios using the historical data provided. How do the values depend on 
   *  confidence interval, $\beta$
   *  number of scenarios (dates), $n_{dates}$
   *  time horizon, $\Delta T$
   *  start date, $T_0$   

2. for any set of parameters ($\beta, n_{dates},  \Delta T, T_0 $) what do you notice about the relationship between $VaR$ and $ES$ ?

3. Do both $VaR$ and $ES$ depend on $\beta, n_{dates},  \Delta T, T_0 $ in the same way ?

4. combine 2 portfolios and recomoute $VaR$ and $ES$. Can you find any examples where the $VaR$ or $ES$ of the combined portfolio is bigger than the sum of the $VaR or $ES$ of the original 2 portfolios ?

## analytic (parametric) solutions

Simple parametric versions of Margin (eg SIMM), Expected Shortfall and Value at Risk all assume 
* the daily changes of each risk factor follow a normal distribution 
* the daily changes of each risk factor are independent (ie today's change does not depend on yesterday's change)
* the correlation between risk factors is fixed 

1. compute the correlation matrix for some of the assets
2. are any of the assumptions true ?
3. (**hard**) whatever your answer to (2), if you assume that all of these assumptions *are* true, 
   * find an analytic representation for VaR and ES ?
   * estimate the necessary values using the historical data
   * compare the VaR and E/S to what you found in the historical simulation. What does that tell you about how the real data compares to the model assumptions ?

4. Why would anybody prefer this method over historical simualtion since its clearly only an approximation  


## (**hard**) monte carlo simulatios 
If we did not have any available historial data, then we can generate some data by using random numbers. We need the made up numbers to have the same properties as the historical data so we need a model. Using the same assumptions as before,
1. generate 1000 days of made up data that follow the same (idealised) distributions as the original data 
2. recompute the VaR and ES using this made up data
3. compare the numbers for VaR and ES to the vlaues you found before    

4. Finally, can you thnk of any reasons why would a bank ever bother to use this method (you need some historical data and some model assumptions to generate the monte-carlo simualtions)
