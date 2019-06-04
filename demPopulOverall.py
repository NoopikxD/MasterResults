import pandas as pd
from geopy.geocoders import Yandex

import time

def formAgeColumnsNames():
    list_names = []

    for gender in ['m', 'g']:
        for i in range(0,101):
            list_names.append(gender+str(i))

    print(list_names)
    return list_names

def calcSumDwellers(df, age_names):
    sum = 0
    for name in age_names:
        sum+= df[name].sum()

    print(sum)


for filename in ['0_Жительства_1_fix.xls', '0_Жительства_2.xls']:

    address_frame = pd.read_excel('input\\' +filename)

    calcSumDwellers(address_frame, formAgeColumnsNames())





