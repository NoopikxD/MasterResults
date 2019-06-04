import pandas as pd
import numpy as np
import time
#removes erroneously assigned coordinates


def formAddress_df(obj):
    return formAddress(obj.district, obj.street, obj.house, obj.corpus).upper()

def formAddress(distr, street, house, korpus):


    if str(street) == "nan":
        return ""

    oneAddr = distr + ' район, ' + ' ' + street
    if house != '' and not (str(house).isspace()):
        oneAddr += ', дом ' + str(house) #str(int(house))
    else:
        if korpus != '' and not (str(korpus).isspace()):
            oneAddr += ', корпус ' + str(int(korpus))

    return "Санкт-Петербург, {0}".format(oneAddr)


# def isSameAddress(obj, address):
#     return formAddress(obj.district, obj.street, obj.house, obj.corpus).upper() == address.upper()

def notIsSameAddressB(obj, address):
    return not(formAddress(obj.district, obj.street, obj.house, obj.corpus).upper() == address.upper())

def notIsSameAddress(distr, street, house, korpus, address):
    return not(formAddress(distr, street, house, korpus).upper() == address.upper())


def removeObjectWithProps(obj_df, latlon, address):
    #removing ALL objects with that properties
    res = obj_df[(obj_df.latitude != latlon[0])  &  (obj_df.longitude != latlon[1]) & (obj_df.Full_address != address.upper())]
    return res

def removeMisleadObj(obj_df):

    file = open("removed_places_mislead.txt", "a")
    file2 = open("sentenced_non_unique_places.txt", "a")

    obj_df = obj_df.drop_duplicates()
    print(obj_df.shape[0])

    obj_df['Full_address'] = obj_df.apply(formAddress_df, axis=1)

    # print(obj_df['Full_address'].drop_duplicates().shape[0])
    # print(obj_df[:5])

    #create a set for unique values

    #print(obj_df[:5])
    print("Finding unique coords...")

    latlon_unique_df = obj_df[['latitude', 'longitude']]

    latlon_unique_df = latlon_unique_df.drop_duplicates()
    print('Unique coords: {}'.format(latlon_unique_df.shape[0]))


    print("Browsing through the list to assess the coord occurrence...")
    for item_latlon in latlon_unique_df.iterrows():
        #print(item_latlon)
        #print(item_latlon[0])
        latlon_cur = item_latlon[1]

        lat = latlon_cur.latitude
        lon = latlon_cur.longitude

        obj_df_cur = obj_df[(obj_df.latitude == lat) & (obj_df.longitude == lon)]  # addresses for cur coord
        print(obj_df_cur)
        addr_list = obj_df_cur.Full_address.tolist()
        addr_num = len(addr_list)

        if addr_num > 5: #checking a suspicious location for uniqueness of address
            print('Checking a suspicious location')
            ####Adding information for debugging purposes#####
            file.write('[')
            for item in addr_list:
                file.write(item + ', ')
            file.write('] \n')
            #########



            addr_list_unique = set(addr_list)
            ##########
            addr_list_unique_remained = []
            print('Looping through unique addresses')
            for item_address in addr_list_unique:
                if addr_list.count(item_address) == 1:
                    file.write(item_address + '\n')
                    obj_df = removeObjectWithProps(obj_df, item_latlon[1], item_address)
                else:
                    addr_list_unique_remained.append(item_address)

            #checking if the remaining addresses vary (indicates a mistake in geocoder localization routine)
            if len(addr_list_unique_remained)>3:
                print('Looping through remained unique addresses')
                ####Adding information for debugging purposes#####
                file2.write('*** \n')
                for item in addr_list_unique_remained:
                    file2.write(item + '\n')
                file2.write('*** \n')

                #########

                for item_address in addr_list_unique_remained: #removing all the remaining objects, cannot decide which is the correct one
                    obj_df = removeObjectWithProps(obj_df, latlon_cur, item_address)


    file.close()
    file2.close()
    return obj_df



# check_df = pd.read_excel(r'output\database.xlsx')
# check_df.to_pickle(r'output\database.p')

check_df = pd.read_pickle(r'output\databaseNew.p')


print('Init length: ', check_df.shape[0])
check_df = removeMisleadObj(check_df)
print('Resulting length: ', check_df.shape[0])

check_df.to_csv(r'output\database_cleant1.csv')
check_df.to_pickle(r'output\database_cleant1.p')

