# -*- coding: cp1251 -*-
import pickle
from types import SimpleNamespace as O
from geopy.geocoders import Yandex
import time,os.path
import numpy as np

proxies = {'http': 'http://proxy.ifmo.ru:3128/'}
geolocator = Yandex( timeout=5 ) #  proxies = proxies -

def getGeocoderLatLon(oneAddr):
    print(oneAddr)
    while True:
        try:
            addr = "Санкт-Петербург, {0}".format(oneAddr)
            location = geolocator.geocode(addr)
            time.sleep(1)
            break
        except:
            print("Network Error!! Wait five seconds!")
            time.sleep(5)

    latlon = (location.latitude, location.longitude)
    return latlon

def Test():
    address = ["Василеостровский район, Биржевая линия, д.4",
               "Центральный район, Невский проспект, д.6",
               "Петроградский район, Кронверский просп., 49",
               "Петроградский район, Кронверская набережная"]

    allLatLon = []
    for addr in address:
        latnon = getGeocoderLatLon(addr)
        allLatLon.append(latnon)

    for l in allLatLon:
        print(l)