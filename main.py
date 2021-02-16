'''
Main module.
'''
from time import sleep, time
from folium_map import create_map
from preprocess import read_data, preprocess_step2
from extract_process_funcset import read_input, \
                                    find_distances, \
                                    find_closes_locations

if __name__ == '__main__':
    year, lattitude, longtitude = read_input()
    start = time()
    locations_data = read_data('locations.list')
    locations_data = preprocess_step2(locations_data, year, (lattitude, longtitude))

    print('Generating map....')

    locations_data = find_distances(locations_data, (lattitude, longtitude))
    closest_locations = find_closes_locations(locations_data)

    for index in range(500):
        print('.', flush = True, end = '')
        if index % 100 == 0:
            print('\b'*100, flush = True, end = '')

        sleep(0.000000005)

    print('\n')
    print('Execution time: ' + str(time() - start))

    print(create_map(closest_locations, (lattitude, longtitude)))
