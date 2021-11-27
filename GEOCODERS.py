import os
from geopy.geocoders import Baidu


def GEOCODERS(address):
    Baidu_key = 'FhPo8GtDOmU9SMZFowSfYWGe9kR9hoCG'

    try:
        geolocator = Baidu(Baidu_key)
        if address[:2] == '京外':
            location = geolocator.geocode(address[2:])
            return location.raw
        elif address == '无地址无地址':
            location = -99999
            return location
        else:
            tt = '北京市'+address
            location = geolocator.geocode(tt)
            return location.raw
    except:
        print('ERROR in sample named {}'.format(address))
        return -99999
