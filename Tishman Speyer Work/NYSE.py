from selenium import webdriver
from bs4 import BeautifulSoup
import numpy as np
import time
import pandas as pd
import json
import urllib.request
import pandas as pd
from pandas.io.json import json_normalize
from datetime import datetime, timedelta

global TishmanTenants
TishmanTenants = pd.read_csv("tenants_for_priceindex.csv",header=None)
TishmanTenants.rename(columns = {0:'Tenant'}, inplace = True)

def NYSEScraper():
    
    url = 'https://www.nyse.com/listings_directory/stock'
    out = []
    
    #driver initialization
    driver = webdriver.Chrome(executable_path='/Users/Master_Trevor/chromedriver')
    
    #Access NYSE URL 
    driver.get(url)
    time.sleep(np.random.uniform(3,5)) 
    
    for i in range(0,646):
        
        time.sleep(np.random.uniform(6,10))
        driver.find_element_by_xpath("//a[@rel='next']").click()
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        table_rows = soup.findAll('tr')[1:]
        
        for tr in table_rows:
            company = tr.findAll('td')[0].text
            code = tr.findAll('td')[1].text
            out.append([code,company])

    df = pd.DataFrame(out,columns = ['Company','Code'])
    df.to_csv('NYSE_Codes.csv', sep=',')
    return df

def ClientMatchAlgorithm(NYSE_Directory):
    
    TishmanTenants['NYSE Code'] = ""
    #Iterate through Tishman Speyer Clients 
    for t in range(0,len(TishmanTenants)):
        tenant = TishmanTenants['Tenant'].loc[t].replace(" ","").replace(",","").upper()
        best_match = {}
    
        #Compare Tishman Client to LinkedIn Search Results 
        for l in range(0,len(NYSE_Directory)):

            SearchResult = NYSE_Directory['Company'].loc[l].replace(" ","").replace(",","").upper()
            
            if (len(SearchResult) <= 3 and SearchResult[len(SearchResult)-1] in ['A','E','I','O','U']):
                #checks for common vowel endings - stronger matching requirement: 
                tenant = tenant.replace(", INC.","")
                SearchResult = SearchResult.replace(", INC.","")
                if tenant == SearchResult: 
                    best_match[l] = len(tenant)
                
            elif ((tenant in SearchResult)):
                best_match[l]= len(tenant)
                
            elif ((SearchResult in tenant)):
                best_match[l] = len(SearchResult)
        
        #Find Closest Matching
        best = 0
        indexOfbest = ""
        for key, value in best_match.items(): 
            if (best_match[key] >= best): 
                best = best_match[key]
                indexOfBest = key
        
        if best_match != {}: 
            code = NYSE_Directory['Code'].loc[indexOfBest]
            TishmanTenants['NYSE Code'].loc[t] = code
            
    return TishmanTenants   

def YahooFinanceScraper(Tishman_Codes):
    QUERY_URL = "https://www.alphavantage.co/query?function={REQUEST_TYPE}&apikey={KEY}&symbol={SYMBOL}"
    API_KEY = 'RG3MY4ZIWNEBVF8F'

    def _request(symbol, req_type):
        with urllib.request.urlopen(QUERY_URL.format(REQUEST_TYPE=req_type, KEY=API_KEY, SYMBOL=symbol)) as req:
            data = req.read().decode("UTF-8")
        return data

    def get_monthly_data(symbol):
        return json.loads(_request(symbol, 'TIME_SERIES_MONTHLY'))
    
    company_list = Tishman_Codes ### change this part right here!

    company_data = pd.DataFrame(columns = ['yyyy-mm'])
    for company in company_list:
        df = pd.DataFrame.from_dict(json_normalize(get_monthly_data(company)))
        cols_to_use = [i for i in df.columns if 'Monthly' in i and 'close' in i] #data at close
        cols_to_use_renamed = {i:i.replace('Monthly Time Series.', '')[:7] for i in cols_to_use}

        df = df.rename(columns = cols_to_use_renamed)[cols_to_use_renamed.values()].T
        data = pd.DataFrame(columns = ['yyyy-mm', company])
        data[company] = df[0].tolist()
        data['yyyy-mm'] = df.index.tolist()

        company_data = company_data.merge(data, how = 'outer')
        
    company_data = company_data.set_index(['yyyy-mm'])
    company_data = company_data.T    
    return company_data
    
def call_scraper():
    #Only call if you want to rescrape
    #NYSE_Directory = NYSEScraper()
    
    #Scraped NYSE Code Data Prepped 
    NYSE_Directory = pd.read_csv('NYSE_Codes.csv',index_col = 0) 
    NYSE_Directory['Company'] = NYSE_Directory['Company'].replace('', np.nan)
    NYSE_Directory = NYSE_Directory.dropna(axis=0, subset=['Company']).reset_index(drop=True)
    
    TishmanTenants = ClientMatchAlgorithm(NYSE_Directory)
    TishmanCodes = TishmanTenants[TishmanTenants['NYSE Code'] != '']['NYSE Code'].unique()
    YahooData = YahooFinanceScraper(TishmanCodes)
    
    #Join Tenants to Yahoo Finance Data using codes
    TishmanTenants = pd.merge(TishmanTenants, YahooData, left_on = 'NYSE Code', right_index = True)
    TishmanTenants.reset_index(drop=True)
    
    return TishmanTenants, YahooData
    
def preprocessing(TenantsFinancialData, leases):
    ## combines leases with financial data
    
    leases['TenantFinanceStart'] = ''
    leases['TenantFinanceEnd'] = ''
    
    for i, val in enumerate(leases['FromDate'].values):
        from_date_minus_two_months = pd.to_datetime(val) - timedelta(days=60)
        to_date_minus_two_months = pd.to_datetime(leases.iloc[i]['ToDate']) - timedelta(days=60)
        start_date = str(from_date_minus_two_months)[:7]
        end_date = str(to_date_minus_two_months)[:7]
        
        if start_date in TenantsFinancialData.columns:
            start_v = TenantsFinancialData[TenantsFinancialData['Tenant'] == leases.iloc[i]['Tenant']][start_date].values
            if len(start_v) > 0:
                start_price = start_v[0]
            else:
                start_price = np.nan
        else:
            start_price = np.nan
        leases.set_value(i, 'TenantFinanceStart', start_price)
        
        if end_date in TenantsFinancialData.columns:
            end_v = TenantsFinancialData[TenantsFinancialData['Tenant'] == leases.iloc[i]['Tenant']][end_date].values
            if len(end_v) > 0:
                end_price = end_v[0]
            else:
                end_price = np.nan
        else:
            end_price = np.nan
        leases.set_value(i, 'TenantFinanceEnd', end_price)
    leases['TenantFinanceStart'] = pd.to_numeric(leases['TenantFinanceStart'], errors='coerce')
    leases['TenantFinanceEnd'] = pd.to_numeric(leases['TenantFinanceEnd'], errors='coerce')
    return leases


