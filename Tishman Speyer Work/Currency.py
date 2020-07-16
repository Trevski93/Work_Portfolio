import pandas as pd
import numpy as np
import warnings
import math
import statistics
warnings.simplefilter('ignore')

def processing(leases):
    
    ## create new features for all charges in USD
    currency_rates = {'BRL': 4.10, 'CNY': 7.09, 'EUR': 0.91, 'GBP': 0.79, 'INR': 70.88, 'USD': 1}
    leases['StartingCharge_USD'] = 0
    leases['EndingCharge_USD'] = 0
    leases['MaxCharge_USD'] = 0
    leases['TotalSpent_USD'] = 0 
    leases['FreeRentAmount_USD'] = 0
    leases['StartingPerSqFt_USD'] = 0
    leases['EndingPerSqFt_USD'] = 0
    leases['MaxPerSqFt_USD'] = 0
    
    for i in range(leases.shape[0]):
        converted_starting = leases.iloc[i]['StartingCharge']/currency_rates[leases.iloc[i]['Currency']]
        leases.set_value(i, 'StartingCharge_USD', converted_starting)
        converted_ending = leases.iloc[i]['EndingCharge']/currency_rates[leases.iloc[i]['Currency']]
        leases.set_value(i, 'EndingCharge_USD', converted_ending)
        converted_max = leases.iloc[i]['MaxCharge']/currency_rates[leases.iloc[i]['Currency']]
        leases.set_value(i, 'MaxCharge_USD', converted_max)
        converted_totalspent = leases.iloc[i]['TotalSpent']/currency_rates[leases.iloc[i]['Currency']]
        leases.set_value(i, 'TotalSpent_USD', converted_max)
        converted_freerentamount = leases.iloc[i]['FreeRentAmount']/currency_rates[leases.iloc[i]['Currency']]
        leases.set_value(i, 'FreeRentAmount_USD', converted_max)
        converted_startingpersqft = leases.iloc[i]['StartingPerSqFt']/currency_rates[leases.iloc[i]['Currency']]
        leases.set_value(i, 'StartingPerSqFt_USD', converted_max)
        converted_endingpersqft = leases.iloc[i]['EndingPerSqFt']/currency_rates[leases.iloc[i]['Currency']]
        leases.set_value(i, 'EndingPerSqFt_USD', converted_max)
        converted_endingpersqft = leases.iloc[i]['MaxPerSqFt']/currency_rates[leases.iloc[i]['Currency']]
        leases.set_value(i, 'MaxPerSqFt_USD', converted_max)
        
    return leases