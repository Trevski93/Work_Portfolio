from selenium import webdriver 
from bs4 import BeautifulSoup
import numpy as np
import time 
import pandas as pd 

global TishmanTenants 
TishmanTenants = pd.read_csv("tenants_for_priceindex.csv",header=None)
TishmanTenants.rename(columns = {0:'Tenant'}, inplace = True)
TishmanClients = list(TishmanTenants['Tenant'].values)

def Scraper():
               
    url = 'https://www.google.com'
    out = []
    
    #driver initialization #You will need to update path to run
    driver = webdriver.Chrome(executable_path='/Users/Master_Trevor/chromedriver')
    count = 0
    partition = 0
    
    for client in TishmanClients:
        #Partition Count
        count += 1

        #Search client data
        driver.get(url)
        SearchBar = driver.find_element_by_xpath("//input[@aria-label='Search']")
        SearchBar.send_keys(client+' number of employees')
        SearchBar.submit()
        time.sleep(np.random.uniform(3,5))
        
        #Scrape
        try: 
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            size = soup.find('div',attrs={'data-attrid':'hw:/collection/organizations:no of employees'}).find('div',attrs={"class":"Z0LcW"}).text
            company = soup.find('div',attrs={'data-attrid':'title'}).find('span').text
            out.append([company,size])
            
        except: 
            pass

        try:
            link = str(driver.find_element_by_partial_link_text('owler.com').get_attribute("href"))
            driver.get(link)
            html = driver.page_source
            soup = BeautifulSoup(html,'html.parser')
            size = soup.find('div',attrs={'class':'count-container EMPLOYEE_EXACT CP'}).find('h2',attrs={'class':"botifyemployeedata title black"}).text
            company = soup.find('h1',attrs={'class': 'tp-title card-title title black bold'}).text
            out.append([company,size])

        except:
            pass
        
        #Save data throughout scrape
        if count == 100: 
            partition += 1
            print("Percentage Complete:",(partition*100/len(TishmanClients))*100,"%")
            df = pd.DataFrame(out,columns = ['Company','EmployeeCount'])
            df.to_csv('EmployeeCnt_partition_'+str(partition))
            count = 0

                
    df = pd.DataFrame(out,columns = ['Company','EmployeeCount'])
    df.to_csv('EmployeeCnt_full.csv', sep=',')
    
    return df 


def renameCompany(x):
     
    if x[len(x)-70:] == "'s Competitors, Revenue, Number of Employees, Funding and Acquisitions" : 
        return x[:len(x)-70]

    else: 
        return x 
    
def ClientMatchAlgorithm(CompanySize_Directory):
    
    TishmanTenants['EmployeeCount'] = ""
    #Iterate through Tishman Speyer Clients 
    for t in range(0,len(TishmanTenants)):
        tenant = TishmanTenants['Tenant'].loc[t].replace(" ","").replace(",","").upper()
        best_match = {}
    
        #Compare Tishman Client to LinkedIn Search Results 
        for l in range(0,len(CompanySize_Directory)):
            SearchResult = CompanySize_Directory['Company'].loc[l].replace(" ","").replace(",","").upper()
            
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
            employee_count = CompanySize_Directory['EmployeeCount'].loc[indexOfBest]
            TishmanTenants['EmployeeCount'].loc[t] = employee_count
            
    return TishmanTenants    

def categorizeSize(df):
    
    size_ls = []
    
    for row in range(0,len(df)):
        
        try:
            employee_count = df['EmployeeCount'].loc[row]

            if employee_count == 1:
                df['CompanySize'].loc[row] = '1'
                size_lis.append('1')

            elif employee_count >= 2 and employee_count <= 10: 
                size_ls.append('2-10')

            elif employee_count >= 11 and employee_count <= 50: 
                size_ls.append('11-50')

            elif employee_count >= 51 and employee_count <= 200: 
                size_ls.append('51-200')

            elif employee_count >= 201 and employee_count <= 500: 
                size_ls.append('201-500')

            elif employee_count >= 501 and employee_count <= 1000: 
                size_ls.append('501-1000')

            elif employee_count >= 1001 and employee_count <= 5000: 
                size_ls.append('1001-5000')

            elif employee_count >= 5001 and employee_count <= 10000: 
                size_ls.append('5001-10,000')

            elif employee_count >= 10000 : 
                size_ls.append('10,000+')
        
        except TypeError:
            size_ls.append('Unknown')

    df['CompanySize'] = size_ls
        
    return df 
 
def processing():
    #ONLY Uncomment Scraper() if you need to collect data 
    #CompanySize_Directory = Scraper() 
    
    #Load Scraped Data & Prep data 
    CompanySize_Directory = pd.read_csv('EmployeeCnt_full.csv',index_col = 0)
    CompanySize_Directory.rename(columns={'Employee Count': 'EmployeeCount'}, inplace=True)
    TishmanTenants = pd.read_csv("tenants_for_priceindex.csv",header=None)
    CompanySize_Directory['Company'] = CompanySize_Directory.apply(lambda x: renameCompany(x['Company']), axis = 1)
    CompanySize_Directory['EmployeeCount'] = CompanySize_Directory.apply(lambda x: float(x['EmployeeCount'].replace(',','')), axis = 1)
    CompanySize_Directory['EmployeeCount'] = CompanySize_Directory['EmployeeCount'].astype(float)
    
    #Match scrape data company names with tishman speyer clients - about 36% of client list identified
    TishmanTenants = ClientMatchAlgorithm(CompanySize_Directory)
    TishmanTenants = categorizeSize(TishmanTenants)
    
    TishmanTenants['EmployeeCount'] = [np.nan if type(c) == str else c for c in TishmanTenants['EmployeeCount'].values ]
    
    #Return Tishman Clients w. company sizes for join back to main dataset 
    return TishmanTenants