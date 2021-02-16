'''
Functions for getting input and performing
main operations.
'''
from sys import exit as leave
from math import cos, radians
import numpy as np

def read_input():
    '''
    Returns user's input.
    '''
    #Getting user's year.
    year = int(input('Enter a year you are interested in (must be integer number): '))

    try:
        year = int(year)

    #Excepting an event when users gives wrong year number.
    except ValueError:
        print('     THE YEAR VALUE MUST BE INTEGER NUMBER    ')
        leave()

    try:
        #Getting coordinates of the place.
        lattitude, longtitude = input('Enter lattitude and longtitude separated with a coma \
(example: 50.456322,98.23423423): ').split(',')

    #Excepting an event when users gives only one number.
    except ValueError:
        print('         THERE MUST BE TWO VALUES IN INPUT FIELD!!!        ')
        leave()
    try:
        lattitude, longtitude = float(lattitude), float(longtitude)

    #Excepting an event when users gives wrong numbers.
    except ValueError:
        print(' THE COORDINATES VALUES MUST BE FLOAT NUMBERS ')
        leave()

    return (year, lattitude, longtitude)

def find_distances(locations_dataframe, point: tuple):
    '''
    Returns a dataframe of distances between the given point
and locations from dataframe.
    '''

    lattitude, longtitude = point
    lattitude, longtitude = radians(lattitude), radians(longtitude)
    locations_dataframe['lattitude_radians'] = np.radians(locations_dataframe['lattitude'])
    locations_dataframe['longtitude_radians'] = np.radians(locations_dataframe['longtitude'])
    locations_dataframe['delta_longtitude'] = locations_dataframe['longtitude_radians'] - longtitude
    locations_dataframe['delta_lattitude'] = locations_dataframe['lattitude_radians'] - lattitude
    locations_dataframe['half_chord'] = np.sin(locations_dataframe['delta_lattitude']/2)**2 + \
                                        cos(lattitude) * \
                                        np.cos(locations_dataframe['lattitude_radians']) * \
                                        np.sin(locations_dataframe['delta_longtitude']/2)**2
    locations_dataframe['distances'] = 6367 * 2 * np.arctan2(
                                                  np.sqrt(locations_dataframe['half_chord']),
                                                  np.sqrt(1 - locations_dataframe['half_chord']))

    return locations_dataframe

def find_closes_locations(locations_dataframe):
    '''
    Returns 10 closest locations.

    >>> import pandas as pd
    >>> closest_locations_dataframe = pd.DataFrame(columns = { \
                                                  'distances' \
                                                  })
    >>> closest_locations_dataframe['distances'] = [100, 90, 80, 30, \
                                                    20, 10, 5, 5, 4, \
                                                    3, 2, 4, 54, 33]
    >>> find_closes_locations(closest_locations_dataframe)
        distances
    10          2
    9           3
    8           4
    11          4
    6           5
    7           5
    5          10
    4          20
    3          30
    13         33
    '''
    top_closest_points = locations_dataframe.nsmallest(10, 'distances',  keep = 'all')
    return top_closest_points[:10]

if __name__ == '__main__':
    import doctest
    doctest.testmod()
