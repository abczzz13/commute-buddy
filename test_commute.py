# -*- coding: utf-8 -*-
"""
Created on Sun Apr 16 15:48:41 2023 by Guido Meijer
"""

import json
import numpy as np
import pandas as pd
import googlemaps
import dotenv
from datetime import datetime

# Initialize Google Maps API
api_key = dotenv.get_key('.env', 'API_KEY')
gmaps = googlemaps.Client(key=api_key)

# Load in stations
stations = pd.read_csv('stations-2022-01-nl.csv')


def commute(address_1, address_2):
    
    travel_df = pd.DataFrame()
    
    # Get transit times to all stations
    for i, station in enumerate(stations['name_long']):
        
        # From address 1
        dir_result = gmaps.directions(address_1,
                                      f'Station {station}',
                                      mode='transit',
                                      departure_time=datetime.strptime(
                                          '2023-04-10_12:00',
                                          '%Y-%m-%d_%H:%M'))
        travel_time_1 = dir_result[0]['legs'][0]['duration']['value']  # in s
        
        # From address 2
        dir_result = gmaps.directions(address_2,
                                      f'Station {station}',
                                      mode='transit',
                                      departure_time=datetime.strptime(
                                          '2023-04-10_12:00',
                                          '%Y-%m-%d_%H:%M'))
        travel_time_2 = dir_result[0]['legs'][0]['duration']['value']  # in s
        
        # Add to dataframe
        travel_df = pd.concat((travel_df, pd.DataFrame(
            index=[travel_df.shape[0]+1],
            data={'station': station,
                  'travel_time_1': travel_time_1,
                  'travel_time_2': travel_time_2})))
        
    # Get best stations
    travel_df['total_travel'] = travel_df['travel_time_1'] + travel_df['travel_time_2']
    travel_df['ratio'] = ((travel_df['travel_time_1'] - travel_df['travel_time_2'])
                          / (travel_df['travel_time_1'] + travel_df['travel_time_2']))
    travel_df['abs_ratio'] = np.abs(travel_df['ratio'])
      
    
if __name__ == '__main__':
    
    address_1 = 'Huygensgebouw, Nijmegen'
    address_2 = 'TNO Utrecht'
    
    commute(address_1, address_2)
