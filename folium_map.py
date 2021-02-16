'''
Module for crating folium map.
'''

from random import choice, random
import folium as flm
from folium.plugins import MarkerCluster

def create_map(closest_locations_dataframe, point):
    '''
    Creates a folium map.
Returns 'Success!!!' if there was no problems.

    >>> import pandas as pd
    >>> closest_locations_dataframe = pd.DataFrame(columns = { \
                                 'title':['film1','film2'], \
                                 'release_year':['2015','2015'], \
                                 'related_locations':['Nieria','Nigeria'], \
                                 'coordinates':[(6,(9.6000359,9.6000359)), \
                                                (6,(7.9999721,7.9999721))] \
                                        })
    >>> create_map(closest_locations_dataframe, (10,10))
    'Success!!!'
    '''
    try:
        lattitude, longtitude = point
        map_folium = flm.Map(location = (lattitude, longtitude),
                                         zoom_start = 10)
        figure = flm.FeatureGroup(name = 'Films map.')
        marker_cluster = MarkerCluster(name = 'Output points').add_to(map_folium)
        ten_random_points = MarkerCluster(name = 'Random_points_random_layer').add_to(map_folium)
        for _ in range(10):
            ten_random_points.add_child(flm.CircleMarker(
                                        location = (random() * 90,
                                                    random() * 90),
                                        radius = random() * 20,
                                        color = choice(['yellow', 'green', 'red']),
                                        fill_color = choice(['yellow', 'green', 'red']),
                                        icon = flm.Icon(icon = 'cloud'),
                                        popup = 'Random user point',
                                        fill_opacity = random()
                                                        ))
        figure.add_child(flm.Marker(location = (lattitude, longtitude),
                   icon = flm.Icon(icon = 'cloud'),
                   popup = 'User point'
                   ))
        for location_index in range(len(closest_locations_dataframe)):
            coordinates = closest_locations_dataframe.iloc[location_index]['coordinates']
            flm.Marker(location = coordinates[-1],
                                  icon = flm.Icon(icon = 'cloud'),
                                  popup = 'Location: ' + \
                                  closest_locations_dataframe.iloc[location_index]
                                                                  ['related_locations'] + '\n' + \
                                  'Film captured: ' + \
                                  closest_locations_dataframe.iloc[location_index]
                                                                  ['title'] + '\n'  + \
                                  'Year of release: ' + \
                                  closest_locations_dataframe.iloc[location_index]
                                                                  ['release_year'] + '.'
                        ).add_to(marker_cluster)

        map_folium.add_child(figure)
        map_folium.add_child(ten_random_points)
        map_folium.add_child(flm.LayerControl())
        map_folium.save('Best_locations_.html')

    except ValueError:
        return 'Error.'

    return 'Success!!!'

if __name__ == '__main__':
    import doctest
    doctest.testmod()
