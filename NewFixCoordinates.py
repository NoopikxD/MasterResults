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
def newRemoveWithProps(obj_df, latlon, adress, temp):
    #temp = obj_df[(obj_df.latitude==latlon[0]) & (obj_df.longitude==latlon[1])]
    #print(temp)
    test = temp.iloc[:, :-3]
    test['Full_address']=test.apply(formAddress_df,axis=1)
    #print(sumsum)
    for i in range(1,temp.shape[0]):
        #print("there we go")
        for j in range(5,temp.shape[1]-3):
            test.iloc[0,j]+=test.iloc[i,j]
    temp1=test[:]
    for i in range(1,test.shape[0]):
        print("i = " + str(i))
        obj_df=obj_df[obj_df['id']!=temp.iloc[i,-2]]
        #temp1=temp1[test['id']!=temp.iloc[i,-1]]

        #removeObjectWithProps(test, item_latlon[1], item_address)

    return obj_df

def removeMisleadObj(obj_df):

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


        addr_list = obj_df_cur.Full_address.tolist()
        addr_num = len(addr_list)

        if addr_num > 2: #checking a suspicious location for uniqueness of address
            print('Checking a suspicious location')
            print('Looping through unique addresses')
            obj_df = newRemoveWithProps(obj_df, latlon_cur,addr_list[0], obj_df_cur)
            print(obj_df.shape[0])

    return obj_df

# check_df = pd.read_excel(r'output\database.xlsx')
# check_df.to_pickle(r'output\database.p')


if __name__ == '__main__':
    check_df = pd.read_pickle(r'output\databaseNew.p')


    print('Init length: ', check_df.shape[0])
    print(check_df.shape[1])
    test=check_df.iloc[:-2,:-2]
    #print(test.shape[1])
    sumofall=test.sum(axis=1)
    sumsum=sumofall.sum()
    #print(sumsum)
    #print(sumofall)
    check_df = removeMisleadObj(check_df)
    #check_df=DoSomeThing(check_df)
    print('Resulting length: ', check_df.shape[0])

    print(sumofall)
    test=check_df.iloc[:-2,:-2]
    #print(test.shape[1])
    sumofall=test.sum(axis=1)


    check_df.to_csv(r'output\database_cleantTEST.csv')
    check_df.to_pickle(r'output\database_cleantTEST.p')

