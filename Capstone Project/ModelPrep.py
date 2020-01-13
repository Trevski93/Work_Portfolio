import pandas as pd
import numpy as np
import warnings
import math
import statistics
warnings.simplefilter('ignore')


#functions 
def percent_change(x, start_col, end_col):
    if x[start_col] == 0:
        return 0
    else:
        try:
            return 100*(x[end_col] - x[start_col])/x[start_col]
        except:
            return np.nan
    
def lease_length(x):
    return (x['ToDate'] - x['FromDate']).days

def has_nulls(x, col_name):
    if str(x[col_name]) == 'nan':
        return 1
    else:
        return 0
    
def numeric_replace_null_with_mean(x, col_name, col_mean):
    if str(x[col_name]) == 'nan':
        return col_mean
    else:
        return x[col_name]

def categorical_replace_null_with_mean(x, col_name, col_mode):
    if str(x[col_name]) == 'nan':
        return col_mode
    else:
        return x[col_name]

def conversion_latlong(x,axis):
        
    try:
        value = tuple(x['lat,lon'].replace(')',"").replace('(',"").split(','))
    
        lat = float(value[0])
        long = float(value[1])
    
    
        if axis == 'x':
            return math.cos(lat) * math.cos(long)
    
        elif axis == 'y': 
            return math.cos(lat) * math.sin(long)
    
        elif axis == 'z':
            return math.sin(lat)
        
    except:
        return None  

def replace_nan_with_str_nan(x, col_name):
    if str(x[col_name]) == 'nan':
        return "nan"
    else:
        return x[col_name]
    
def processing(leases): 
    # Filter out leases that are a current lease
    modeling_data = leases

    #'StartingPerSqFt','EndingPerSqFt','MaxPerSqFt' have inf values - need to replace inf with nan
    modeling_data = modeling_data.replace(np.inf, np.nan)

    # make date cols datetime
    modeling_data['FromDate'] = pd.to_datetime(modeling_data['FromDate'])
    modeling_data['ToDate'] = pd.to_datetime(modeling_data['ToDate'])
    
    # percent change of starting charge to ending charge
    modeling_data['charge_percent_change'] = modeling_data.apply(lambda x: percent_change(x, 'StartingCharge', 'EndingCharge'), axis = 1)

    # lease length in days
    modeling_data['lease_length'] = modeling_data.apply(lambda x: lease_length(x), axis = 1)

    # percent change of starting sq foot to ending sq foot
    modeling_data['sq_foot_percent_change'] = modeling_data.apply(lambda x: percent_change(x, 'StartingPerSqFt', 'EndingPerSqFt'), axis = 1)
    
    # percent change of starting and ending financial data
    modeling_data['finance_percent_change'] = modeling_data.apply(lambda x: percent_change(x, 'TenantFinanceStart', 'TenantFinanceEnd'), axis = 1)

    modeling_data['lat_lon_x'] = modeling_data.apply(lambda x: conversion_latlong(x,'x'), axis = 1)
    modeling_data['lat_lon_y'] = modeling_data.apply(lambda x: conversion_latlong(x,'y'), axis = 1)
    modeling_data['lat_lon_z'] = modeling_data.apply(lambda x: conversion_latlong(x,'z'), axis = 1)
    
    return modeling_data 