'''
Preprocessing process.
'''

import re
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable, GeocoderServiceError

def preprocess_step2(dataframe, year, point):
    '''
    Returns a filtered dataframe.
    '''
    def helper(cell):
        '''
        Returns coordinates of the place.

        >>> cell = 'Nigeria'
        >>> print(helper(cell))
        'Nigeria'
        '''
        try:
            coordinates = geolocator.geocode(cell)
            return coordinates

        except (GeocoderUnavailable, GeocoderServiceError):
            return None

    def find_country(point, dataframe):
        '''
        Returns a dataframe of the points of the
    locations nearby the given point.
        '''
        latitude, longtitude = point
        point_location = geolocator.reverse((latitude, longtitude))
        determinator = 0
        directions = [latitude, longtitude, latitude, longtitude,
                      latitude, longtitude, latitude, longtitude,
                      latitude, longtitude, latitude, longtitude]
        points = pd.DataFrame(columns = {'title':[],
                                         'release_year':[],
                                         'country':[],
                                         'related_locations':[]})
        number_of_points = 0
        while True:
            for index in range(8):
                for _ in range(5):
                    if index == 4:
                        directions[4] += 0.5
                        directions[5] += 0.5
                        point_location = geolocator.reverse((directions[4], directions[5]))

                    elif index == 5:
                        directions[6] -= 0.5
                        directions[7] -= 0.5
                        point_location = geolocator.reverse((directions[6], directions[7]))

                    elif index == 6:
                        directions[8] += 0.5
                        directions[9] -= 0.5
                        point_location = geolocator.reverse((directions[8], directions[9]))

                    elif index == 7:
                        directions[10] -= 0.5
                        directions[11] += 0.5
                        point_location = geolocator.reverse((directions[10], directions[11]))

                    elif index % 2 == 0:
                        directions[index] += 0.5
                        point_location = geolocator.reverse((directions[index], longtitude))

                    else:
                        point_location = geolocator.reverse((latitude, directions[index]))

                    if directions[index] not in range(-91, 91):
                        directions[index] = 0

                    if point_location is not None:
                        point_location = point_location[0].split()[-1]
                        dataframe_try = dataframe.loc[dataframe['country'] == point_location]

                        if len(dataframe_try) > 0:
                            number_of_points += len(dataframe_try)
                            points = pd.concat([points, dataframe_try])

                            if len(points) >= needed_number:
                                return points

                    else:
                        continue

            determinator += 1

    geolocator = Nominatim(user_agent = 'FilmMapsFolium')
    dataframe.loc[dataframe['title'] == '', 'title'] = 'Unknown'
    dataframe.reset_index(inplace = True)
    dataframe.drop(columns = ['index'], inplace = True)
    dataframe.drop_duplicates(keep = 'first', inplace = True)

    dataframe = dataframe.loc[dataframe['release_year'] == str(year)]
    needed_number = 50
    if len(dataframe) < needed_number:
        while len(dataframe) < needed_number:
            needed_number /= 10
            needed_number = int(needed_number)

    dataframe = find_country(point, dataframe)

    dataframe.reset_index(inplace = True)
    dataframe.drop(columns = 'index', inplace = True)

    dataframe['coordinates'] = dataframe['related_locations'].apply(helper)
    dataframe['lattitude'] = dataframe['coordinates'].apply(lambda cell: cell.latitude)
    dataframe['longtitude'] = dataframe['coordinates'].apply(lambda cell: cell.longitude)

    return dataframe

def read_data(path_to_file: str):
    '''
    Returns input data in a pandas dataframe.
    '''

    with open(path_to_file, 'r', encoding='latin1') as file:
        content = file.readlines()[14:]
        data = {'title':[], 'release_year':[], 'country':[], 'related_locations':[]}
        for line_index in range(len(content)-1):
            current_line = content[line_index]

            if '{' in current_line:
                current_line = current_line[:current_line.find('{')] + \
                               current_line[current_line.find('}')+1:]

            if line_index != 1155410:
                current_line = current_line[:current_line.rfind('\t(')]

            current_line = current_line.split('\t')
            current_line = [element for element in current_line if element != '']

            title_pattern = re.compile(r'^.+ \(')
            release_year_pattern = re.compile(r'[\(]+[0-9?/I]+[^\)]+')

            film_title = title_pattern.findall(current_line[0])
            film_title = film_title[0].replace('"','')
            film_title = film_title[:film_title.find('(')]

            release_year = release_year_pattern.findall(current_line[0])[0][1:]

            locations = current_line[1]
            if line_index == 1155410:
                locations = locations[locations.find('(')+1:locations.find(')')]

            if 'Federal' in locations or 'Highway' in locations:
                continue

            country = locations.split(',')[-1]
            if country == 'Russia':
                country = 'Россия'

            data['title'] += [film_title]
            data['release_year'] += [release_year]
            data['country'] += [country]
            data['related_locations'] += [locations]

        output_dataframe = pd.DataFrame(data,
                                        columns = {'title',
                                                   'release_year',
                                                   'country',
                                                   'related_locations'})

    return output_dataframe

if __name__ == '__main__':
    import doctest
    doctest.testmod()
