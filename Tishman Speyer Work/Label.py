import pandas as pd
import numpy as np
import warnings
import math
import statistics
warnings.simplefilter('ignore')


def processing(leases): 
    ### Label Creation 
    lease_data = leases
    lease_data.sort_values(['Tenant','GreaterCity','FromDate'])
    #add lease variables for historic information initialized at 0
    lease_data['hist_count'] = 0
    lease_data['hist_months'] = 0
    lease_data['hist_usdSpend'] = 0
    lease_data['simult_count'] = 0
    lease_data['simult_months'] = 0
    lease_data['simult_usdSpend'] = 0

    #list that will hold label values 
    labels_list = []

    counter = 0

    #We are iterating through each record (lease) in the dataframe
    for i in range(0,len(lease_data)):

        if counter % 700==0:
            print(counter/len(lease_data),"% Complete")

        current_record = lease_data.loc[i]
        current_tenant = current_record['Tenant']
        current_market = current_record['GreaterCity']
        current_fromdate = current_record['FromDate']
        current_id = current_record['LeaseID']

        #Excluding Current Deals that are on-going with Tishman Speyer
        if (current_record['IsCurrentLease'] == 1 ): 
            labels_list.append(3)

        elif (current_record['IsCurrentLease'] == 0): 

            #Captures all leases related to current Tenant/market combination
            all_tenant_record_dates =  lease_data[(lease_data['Tenant'] == current_tenant) & (lease_data['GreaterCity'] == current_market)]['FromDate']
            continued_relationship = False 

            #checks if the this tenant has starting lease dates after the current ending lease date in question
            #implies whether a client continued their relationship w/ Tishman after this deal 
            for potential_future_date in all_tenant_record_dates:
                if ((pd.to_datetime(current_record['ToDate']) < pd.to_datetime(potential_future_date))):
                    continued_relationship = True

                #New Clause
                elif (list(all_tenant_record_dates).count(current_record['FromDate']) > 1):
                    simult_leases = lease_data[(lease_data['Tenant'] == current_tenant) & (lease_data['FromDate'] == current_record['FromDate']) \
                                                                                           & (lease_data['GreaterCity']==current_market)]

                    for s in simult_leases.index:
                        if (pd.to_datetime(current_record['ToDate']) < pd.to_datetime(simult_leases['ToDate'].loc[s])):
                            continued_relationship = True

            if (continued_relationship == True): 
                labels_list.append(1)
            else: 
                labels_list.append(0)

        #now that target has been set, generate historic lease info
        historic_leases = lease_data[(lease_data['Tenant'] == current_tenant) & (lease_data['GreaterCity'] == current_market) & (lease_data['FromDate']<current_fromdate)]
        if len(historic_leases)>0:
            historic_count = len(historic_leases)
            historic_length_months = np.sum(historic_leases['LeaseLengthMonths'])
            historic_spend = np.sum(historic_leases['TotalSpent_USD'])
            lease_data.set_value(i,'hist_count',historic_count)
            lease_data.set_value(i,'hist_months',historic_length_months)
            lease_data.set_value(i,'hist_usdSpend',historic_spend)

        #generate simultaneous lease info
        #redefine to exclude our current record
        simult_leases = lease_data[(lease_data['Tenant'] == current_tenant) & (lease_data['GreaterCity'] == current_market) \
                                   & (lease_data['FromDate']==current_fromdate) & (lease_data['LeaseID']!=current_id)]
        if len(simult_leases)>0:
            simult_count = len(simult_leases)
            simult_length_months = np.sum(simult_leases['LeaseLengthMonths'])
            simult_spend = np.sum(simult_leases['TotalSpent_USD'])
            lease_data.set_value(i,'simult_count',simult_count)
            lease_data.set_value(i,'simult_months',simult_length_months)
            lease_data.set_value(i,'simult_usdSpend',simult_spend)

        counter+=1

    lease_data['ContinuedRelationship'] = labels_list     
    leases = lease_data[((lease_data['ContinuedRelationship'] == 1) | (lease_data['ContinuedRelationship'] == 0)) ]
    leases.reset_index(drop=True, inplace=True)
    
    return leases