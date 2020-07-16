import pandas as pd
import numpy as np
import warnings
import math
import statistics
warnings.simplefilter('ignore')

def create(): 

    leases = pd.read_csv('leases_buildings_merged.csv')[['LeaseID', 'ContractId', 'TenantId', 'Tenant', 'Industry',
       'PropertyName', 'PropertyId', 'PropertyIsActive', 'PropertyLoc',
       'City_leases', 'GreaterCity_leases', 'Subregion_leases',
       'Country_leases', 'UseType_leases', 'ConstructionType_leases', 'Floor',
       'Unit', 'UnitArea', 'UnitType', 'BillingType', 'FromDate', 'ToDate',
       'Currency', 'LeaseCommencement', 'LeaseExpiration', 'Vacate',
       'LeaseSource', 'Reason', 'ReasonDescription', 'Renewal', 'Mistake',
       'NumPriceChanges', 'NumRentCharges', 'NumFreeRentPeriods',
       'MonthsFreeRent', 'FreeRentAmount', 'LeaseLengthDays',
       'LeaseLengthMonths', 'TotalSpent', 'StartingCharge', 'EndingCharge',
       'StartingPerSqFt', 'EndingPerSqFt', 'MaxPerSqFt', 'MaxCharge',
       'AvgRateInc>5', 'AvgRateInc>10', 'AvgRateIncrease', 'MaxRateInc>5',
       'MaxRateInc>10', 'MaxRateIncrease', 'IsCurrentLease', 'IsTS',
       'IsRenewal', 'HasSimultaneousOffice', 'HasSimultaneousAntenna',
       'HasSimultaneousStorage', 'HasPreviousLease', 'HasLeaseInSameProperty',
       'HasLeaseInOtherProperty', 'ZoAvailable', 'ZoLaunchDate',
       'ZoAvailableLeaseStart', 'ZoAvailableDuringLease', 'ZoUsed',
       'LastLease', 'ZoUsedNoRenewal', 'PropNumber', 'Property',
       'address', 'lat,lon']]

    leases = leases.rename(columns = {'City_leases': 'City', 'GreaterCity_leases': 'GreaterCity', 'Subregion_leases':'Subregion',
       'Country_leases':'Country', 'UseType_leases':'Use_Type', 'ConstructionType_leases': 'ConstructionType'})
    
    return leases 

