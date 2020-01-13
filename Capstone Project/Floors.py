import pandas as pd
import numpy as np
import warnings
import math
import statistics
warnings.simplefilter('ignore')

def processing(leases): 
    group_by_building = leases[['PropertyName', 'Floor']].groupby('PropertyName')
    building_floors = group_by_building.apply(lambda x: x['Floor'].unique())

    EuropeFloors = ['100 NOX', 'TS KLS 29 S.A.R.L.', 'WESERSTRASSE', '33 HOLBORN', 'AREA PRIMA','CBX', 'DELTA', 'ELAND HOUSE','INFLUENCE', 'JUNGHOF', 'BCJA_EDIFICIO JATOBA', 
                   'BCGT_TORRE NORTE','BCGA_COND ED GALERIA', 'BCGT_TORRE CENTRAL', 'BCGT_TORRE SUL', 'BCCB_EDIFICIO JACARANDA', 'BCNU _ TORRE OESTE', 'BCNU_TORRE NORTE',
                   'ONE GOTHAM CENTER', 'LE CRISTALIA', 'LUMIERE', 'PONT CARDINET REZO', 'TAUNUSTURM', 'TESSUTO', 'THREE GOTHAM CENTER', 'CAP DE SEINE', 'HAHNSTRASSE',
                   'PARIS BOURSE', 'THE POINT', 'TOUR PACIFIC', 'Q205']

    ## these buildings will be treated differently
    BuildingsWithNum = ['BUILDING 1', 'BUILDING 2', 'BUILDING 3','BUILDING 5', 'BUILDING 6', 'BUILDING 7', 'BUILDING 8']

    ## all buildings with special cases
    SpecialCaseBuildings = ['HAHNSTRASSE', 'WEST END PLAZA', 'ARBORETUM COURTYARD','125 HIGH STREET', 
                            'LONG RIDGE OFFICE PARK','Q205','BUILDING 1', 'BUILDING 2', 'BUILDING 3','BUILDING 5', 
                            'BUILDING 6', 'BUILDING 7', 'BUILDING 8']
    
    ## get lists of all numeric and non-numeric floors
    numeric_floors = []
    non_numeric_floors = []
    for i, val in enumerate(leases['Floor'].values):
        try:
            int(val)
            numeric_floors.append(int(val))
        except:
            non_numeric_floors.append(str(val))
     
    ## for each building make a max of the numeric floors
    ## max for each building
    sub_df = pd.DataFrame(columns=['Building', 'Floor'])
    i = 0
    for k, val in enumerate(leases['Floor'].values):
        try:
            int(val)
            if int(val) in numeric_floors:
                if leases.iloc[k]['PropertyName'] in EuropeFloors:
                    if int(val) >= 0:
                        out = int(val) + 1
                    else:
                        out = int(val)
                    sub_df.loc[i] = [leases.iloc[k]['PropertyName'], out]
                else:
                    sub_df.loc[i] = [leases.iloc[k]['PropertyName'], int(val)]
                i = i+1
        except:
            continue

    group_by_building_numeric = sub_df.groupby('Building')
    numeric_building_floors = group_by_building_numeric.apply(lambda x: x['Floor'].unique())
    
    ## Combine Garage, Parking, Metro
    Garage_and_Park = ['Gar', 'GAR', 'GAR1', 'GAR-B', 'GAR-1', 'P1', 'P2', 'P3', 'P4', 'O-P1', 'GAR2', 'GAR-C', 
                       'GAR-A', 'GA', 'G', 'GH', 'PARK', 'PRK', 'P', '01P','PARKING', 'METRO', 'MET', 'A-P1'] #-2

    ## Combine Basement and Storage
    Basement_and_Storage = ['ST','B', 'BSMT', 'SB', 'B02', 'B01', 'B03', 'B04', 'B1', 'CBSMT', 'B-1',
                            'BSM','LB', '1A', '01A', 'LB2', 'LL2','SS', 'AR','LB1',
                            'ANT', 'AUDIT', 'EXT', 'SM', 'BM'] #-1

    ## Combine Ground floor and Lobby
    Ground_Lobby =['GRND', 'LOB', 'LOBBY','GROUND','L', 'MEZZ', 'MEZ','WMEZ', 'EMEZ', 'M', '0M1', '1F',
                   'GR', '01M', 'STORE', 'ROOM1', 'WM', 'ME', '2M', 'PL', 'G', '0E1'] #1

    ## Combine all versions of lower lobby, lower level, etc
    Lower_Lobby = ['LL','LL1', 'GF', 'CO', 'CA', 'C', 'CL', 'CM', 'F00', 'R00', 'F'] #0

    ## Combine roof, terrace, and penthouse
    Roof = ['ROOF', 'TERRACE', 'TERR', 'TER', 'TR', 'RF', 'PH', 'Penthouse'] #max numeric floor of that building +1

    ## Combine all lower lobby floors in European buildings
    Lower_LobbyEUR = ['LG', 'LL', 'IL', '0E0', '0G0', 'ZZ0', 'ZZ'] #0
    
    ## functions
    def general_rules(floor, building):
        try:
            int(floor)
            ## if floor is an integer, return the floor, or -2 if the floor is less than -2
            if int(floor) < -2:
                return -2
            else:
                return int(floor)
        except:
            try:
                ## if floor is a string, check for known string floors, otherwise return missing val
                str(floor)
                if str(floor) in Basement_and_Storage:
                    return -1
                elif str(floor) in Garage_and_Park:
                    return -2
                elif str(floor) in Ground_Lobby:
                    return 1
                elif str(floor) in Lower_Lobby:
                    return 0
                elif str(floor) in Roof:
                    return max(numeric_building_floors[building]) + 1
                else:
                    return 'missing'
            except:
                return 'missing'


    def remove_first_char(floor):
        ## used when every floor in the building starts with 'A','C', etc. for example
        chars = [char for char in str(floor)]
        out = chars[1:]
        return ''.join(out)

    def remove_last_char(floor):
        ## used when every floor in the building ends with 'F', for example
        chars = [char for char in str(floor)]
        out = chars[:-1]
        return ''.join(out)

    def remove_prefix(floor):
        ## used when every floor in the building starts with 'N-','S-', etc. for example
        chars = [char for char in str(floor)]
        out = chars[2:]
        return ''.join(out)

    def hyphen_slash(floor, hyphen):
        ## function if multiple floors are given, separated by hyphen (-) or slash (/)
        ## returns max floor as the numeric floor, along with the amount of floors
        floors = [f for f in str(floor).split(hyphen)]
        fs = []
        for i in floors:
            chars = [char for char in str(i)]
            if 'B' in chars:
                fs.append(remove_first_char(i))
            elif 'F' in chars:
                fs.append(remove_last_char(i))
            else:
                fs.append(i)
        num_floors = (int(fs[1]) - int(fs[0])) + 1
        numeric_floor = int(fs[1])
        return numeric_floor, num_floors

    def comma(floor):
        ## function if multiple floors are given, separated by a comma
        ## returns max floor as the numeric floor, along with the amount of floors
        floors = [f for f in str(floor).split(',')]
        fs = []
        for i in floors:
            chars = [char for char in str(i)]
            if 'F' in chars:
                fs.append(int(remove_last_char(i)))
            else:
                fs.append(int(i))
        num_floors = len(fs)
        numeric_floor = max(fs)
        return numeric_floor, num_floors


    def all_floors(building):
        ## function if floor = 'ALL', returns the max floor number of that building and that building's amount of floors (besides the 'ALL' floor), 
        ##or if that doesn't exist, return avg floor number of all records as the numeric floor and as the amount of floors
        try:
            numeric_building_floors[building]
            if len(numeric_building_floors[building]) > 0:
                return max(numeric_building_floors[building]), len(building_floors[building])-1
            else:
                return np.mean(numeric_floors), np.mean(numeric_floors)
        except:
            return np.mean(numeric_floors), np.mean(numeric_floors)

    def missing_val(building):
        ## if missing value (NaN, DUM, DUMMY, etc.), return the avg floor number of that building, or 
        ## if that doesn't exist, return the avg floor number of all records
        try:
            numeric_building_floors[building]
            if len(numeric_building_floors[building]) > 0:
                return np.mean(numeric_building_floors[building])
            else:
                return np.mean(numeric_floors)
        except:
            return np.mean(numeric_floors)
        

    remove_first_char_buildings = ['125 HIGH STREET','ARBORETUM COURTYARD', 'LONG RIDGE OFFICE PARK']
    def SpecialCases(building, floor):
        if building in remove_first_char_buildings:
            ## if not a known floor, remove first character and treat as normal input
            if floor not in Garage_and_Park and floor not in Basement_and_Storage and floor not in Ground_Lobby and floor not in Lower_Lobby and floor not in Roof and floor not in Lower_LobbyEUR:
                out = remove_first_char(floor)
                return general_rules(out, building)
            else:
                ## in this case it's a known floor, so treat as normal input
                return general_rules(floor, building)
        elif building == 'WEST END PLAZA':
            out = remove_first_char(floor)
            return int(out)+1
        elif building == 'HAHNSTRASSE':
            if str(floor) in ['A', 'B', 'C', 'D']:
                return -1
            else:
                return general_rules(floor, building)
        elif building in BuildingsWithNum:
            chars = [char for char in str(floor)]
            ## see if floor is hyphen separated, which will get treated differently in for loop
            if '-' in chars:
                return '-'
            ## see if floor is comma separated, which will get treated differently in for loop
            elif ',' in chars:
                return ','
            elif 'F' in chars:
                return int(remove_last_char(floor))
            ## see if floor is ALL, which will get treated differently in for loop
            elif str(floor) == 'ALL':
                return 'all'
            elif str(floor) == 'T8':
                return 8
            else:
                return general_rules(floor, building)
        elif building == 'Q205':
            if str(floor) in ['777','700']:
                return 7
            else:
                return general_rules(floor, building)
            
            
    leases['NumericFloor'] = 0
    leases['MissingFloor'] = 0
    leases['AmountofFloors'] = 1
    for i, val in enumerate(leases['Floor'].values):
        ## check if europe lobby
        if val in Lower_LobbyEUR:
            output = 0
        ## check special cases
        elif leases.iloc[i]['PropertyName'] in SpecialCaseBuildings:
            output = SpecialCases(building = leases.iloc[i]['PropertyName'], floor = val)
            if leases.iloc[i]['PropertyName'] in EuropeFloors and output != 'missing' and output != '-':
                ## if european floor, add 1
                if output >= 0 and val not in Ground_Lobby and val not in Lower_Lobby:
                    output +=1
        ## check if multiple floors in North/South Summit, which are indicated by - or / 
        elif leases.iloc[i]['PropertyName'] in ['NORTH BUILDING - SUMMIT', 'SOUTH BUILDING - SUMMIT']:
            out = remove_prefix(val)
            chars = [char for char in str(out)]
            if '/' in chars:
                floor, amount_of_floors = hyphen_slash(out, '/')
                leases.set_value(i, 'NumericFloor', floor)
                leases.set_value(i, 'AmountofFloors', amount_of_floors)
            elif '-' in chars:
                floor, amount_of_floors = hyphen_slash(out, '-')
                leases.set_value(i, 'NumericFloor', floor)
                leases.set_value(i, 'AmountofFloors', amount_of_floors)
            else:
                output = general_rules(out, leases.iloc[i]['PropertyName'])
        else:
            ## for all reminaing floors, follow general rules
            output = general_rules(floor = val, building = leases.iloc[i]['PropertyName'])
            if leases.iloc[i]['PropertyName'] in EuropeFloors and output != 'missing':
                ## if european floor, add 1
                if output >= 0 and val not in Ground_Lobby and val not in Lower_Lobby:
                    output +=1
        ## check if missing value (NaN)
        if output == 'missing':
            floor = missing_val(building = leases.iloc[i]['PropertyName'])
            leases.set_value(i, 'NumericFloor', floor)
            leases.set_value(i, 'MissingFloor', 1)
        ## check if floor = 'ALL'
        elif output == 'all':
            floor, amount_of_floors = all_floors(building=leases.iloc[i]['PropertyName'])
            leases.set_value(i, 'NumericFloor', floor)
            leases.set_value(i, 'AmountofFloors', amount_of_floors)
        ## check if multiple floors on a diff building besides North/South Summit
        elif output == '-':
                floor, amount_of_floors = hyphen_slash(val, '-')
                leases.set_value(i, 'NumericFloor', floor)
                leases.set_value(i, 'AmountofFloors', amount_of_floors)
        ## check if multiple floors on a diff building besides North/South Summit
        elif output == ',':
                floor, amount_of_floors = comma(val)
                leases.set_value(i, 'NumericFloor', floor)
                leases.set_value(i, 'AmountofFloors', amount_of_floors)
        else:
            leases.set_value(i, 'NumericFloor', output)

    return leases 

# ### Assumptions made when converting floors
# - Parking, Garage, Metro (including all levels of each) can all be treated the same (-2)
# - Basement, Storage (including all levels of each) can all be treated the same (-1)
# - Ground Floor, First Floor, Lobby, Mezzanine, Store, Plaza can all be treated the same (1)
# - Lower Lobby, Lower Level can all be treated the same (0)
# - European buildings all follow European floor naming convention (what would be 2nd floor in US is 1st floor in Europe)
# - SB = sub-basement
# - LB = lower-basement
# - GH = garage
# - 01A, ANT, AUDIT, EXT, AR, ST, SS, SM = storage
# - E01 = ground floor
# - C, CL, CO, CM, CA, F00, R00, F = lower level
# - T8 = Floor 8




