import pandas as pd
from GEOCODERS import GEOCODERS
from multiprocesspandas import applyparallel
def test(x):
    return list(map(lambda i:GEOCODERS(i),x))
Travel_person = pd.read_json('../documents/Travel_locates.json')
Travel_person['LocationDecode'] = Travel_person['LocationAddress'].apply_parallel(test,num_processes=30)
Travel_person.to_json('../documents/Travel_locates_by_lon_lat.json')


