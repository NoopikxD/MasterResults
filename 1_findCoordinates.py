import pandas as pd
from geopy.geocoders import Yandex

import time,os.path


geolocator = Yandex( timeout=1) #  proxies = proxies -


def formAddress(distr, street, house, korpus):
    #print(distr, street)
    oneAddr = str(distr) + ' район, ' + ' ' + str(street)
    if house != '' and house != 'NaN':
        oneAddr += ',  ' + str(house)
    if korpus != '' and str(korpus).lower() != 'nan' and str(korpus)!='1':
            oneAddr += 'к' + str(korpus)
    #print("distr  = " +str(distr) + "; street = " + str(street) + "; house = " + str(house) + "; korpus = " + str(korpus) + "\n")
    #print(oneAddr)
    return "Санкт-Петербург, {0}".format(oneAddr)

def getGeocoderLatLon_crim(distr, street, house, korpus):
    #print(addr)
    oneAddr = formAddress(distr,street,house,korpus)
    print(oneAddr)
    #oneAddr = str(distr)+' район, '+' '+str(street)
    #if house!='' and house != 'NaN':
        #oneAddr += ', дом '+str(house)
    #else:
        #if korpus!='' and korpus != 'NaN':
            #oneAddr += ', корпус '+str(korpus)
    #print(oneAddr)

    while True:
        try:
            addr = "Санкт-Петербург, {0}".format(oneAddr)
            location = geolocator.geocode(addr)
            time.sleep(1)
            break
        except:
            print("Network Error!! Wait five seconds!")
            #time.sleep(5)
            location = None
            break
    if (location):
        return (location.latitude, location.longitude)
    else:
        return  (0.0, 0.0)


def getLatLon(distr, addr, house, korpus, objaddr_detected_dic):
    #Getting latlon either from the previous data (objaddr_detected_list) if any, or through geocoder if not found

    search_string = formAddress(distr, addr, house, korpus).upper()
    #if(korpus!='' and korpus!= "NaN"):
        #print(korpus)

    if search_string in objaddr_detected_dic.keys():
        #print('Found: ')
        #print(search_string)
        return objaddr_detected_dic[search_string], objaddr_detected_dic

    else:
        #print('No dic value: ')
        latlon = getGeocoderLatLon_crim(distr, addr, house, korpus)
        objaddr_detected_dic[search_string] = latlon
        return latlon, objaddr_detected_dic

#for filename in ['0_Жительства_1.xls', '0_Жительства_2.xls']:
for filename in ['0_Жительства_1_fix.xls']:

    address_frame = pd.read_excel('input\\' +filename)

    #***
    address_frame = address_frame[24997:] #TODO: 4000..4100 - seconf file, first file - chck end (div 1000?)
    #***
    len = address_frame.shape[0]

    objaddr_detected_dic = {} #Словарь координат найденных объектов

    for index, row in address_frame.iterrows():
       #print("{} from {}".format(index, len))
        latlon_new, objaddr_detected_dic = getLatLon(row['district'], row['street'], row['house'], row['corpus'], objaddr_detected_dic)
        #print(latlon_new)
        address_frame.loc[index, 'latitude'] = latlon_new[0]
        address_frame.loc[index, 'longitude'] = latlon_new[1]
        print(index)
        #if index>0 and index % 500 == 0 or index==len-1:
            #with open('output\\database.csv', 'a') as f:
                #address_frame[index-500:index].to_csv(f, header=False)

        #address_frame[:index].to_excel('output\\database.xlsx')

address_frame.to_excel('output\\database2part.xlsx')





