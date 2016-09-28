"""
Gets population of us cities in police shootings file

Go to the US Census Bureau and sign up for an API key (there are only two fields to worry about):

http://api.census.gov/data/key_signup.html

Fill in the API key in the API_KEY field below.
"""

import urllib.request
import urllib.error
from time import sleep
import csv
import ast


API_KEY = '728083e8ebb522935279c284a900a4cd9d491f12'
LOCATION_CSV = './places.csv'
SHOOTINGS_CSV = '../fatal-police-shootings-data.csv'
OUTPUT_CSV = '../shootings_with_population_data.csv'
REPORT_YEAR = 2010

class Census:
    def __init__(self, key):
        self.key = key

    def get(self, fields, geo, year=REPORT_YEAR, dataset='sf1'):
        fields = [','.join(fields)]
        base_url = 'http://api.census.gov/data/%s/%s?key=%s&get=' % (str(year), dataset, self.key)
        query = fields
        for item in geo:
            query.append(item)
        add_url = '&'.join(query)
        url = base_url + add_url
        req = urllib.request.Request(url)

        try:
            response = urllib.request.urlopen(req)
        except urllib.error.URLError:
            # Might be going to fast. Sleep a few seconds and give it another shot.
            print(" -> Could not connect to Census Bureau. Sleeping for 15 seconds and trying again.")
            sleep(15)
            response = urllib.request.urlopen(req)

        return response.read()


class CSV:
    """
    Read and write to and from the CSV file
    """
    def __init__(self, csv_file):
        file = open(csv_file)
        self.csv_file = csv.reader(file)
        self.writer = csv.writer(file)

    def build_city_state_list(self):
        """
        Build city, state list. The city is in row 8, and the state is in row 9
        :return: a list containing (city, state)
        """

        city_states = []

        for row in self.csv_file:
            city = row[8]
            state = row[9]

            city_state = (city, state)
            city_states.append(city_state)

        return city_states

    def write_new_columns(self, population_data):
        """
        Write new columns to the CSV after getting races per city.
        :return: None
        """

        new_column_names = ['total_population',
                            'white_population',
                            'black_population',
                            'asian_population',
                            'hispanic_population',
                            'state_fips',
                            'city_fips']

        with open(OUTPUT_CSV, 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            all = []

            row_0 = next(self.csv_file)

            for column_name in new_column_names:
                row_0.append(column_name)

            all.append(row_0)

            for row in self.csv_file:

                row.append(None)
                all.append(row)

            for row in all:  # add the pop data to new table
                for location, race_population in population_data.items():
                    city = location.split(',')[0]
                    state = location.split(',')[1]

                    if city == row[8] and state == row[9]:  # found a match!

                        try:
                            if row[14]:
                                row[14] = race_population['total_population'][0]  # there already seems to be a cell here.
                            else:
                                row.append(race_population['total_population'][0])
                            row.append(race_population['white_population'][0])
                            row.append(race_population['black_population'][0])
                            row.append(race_population['asian_population'][0])
                            row.append(race_population['hispanic_population'][0])
                            row.append(race_population['total_population'][1])
                            row.append(race_population['total_population'][2])

                        except KeyError or TypeError:  # TypeError is prob. because results not found
                            print("Could not find population data for {}".format(location))

            writer.writerows(all)



def get_total_population(location, census):
    """
    Returns the population for a given city and state
    :param location: Tuple denoting (city, state)
    :param census: Census object
    :return: Int -> population of city, state
    """
    row_index = 0  # for skipping the places.csv header
    _city = location[0].strip()
    _state = location[1].strip()

    error_status = False

    results = {}

    # Get city FIPS code from places.csv

    reports = {
        'total_population':     'P0080001',
        'white_population':     'P0080003',
        'black_population':     'P0080004',
        'asian_population':     'P0080006',
        'hispanic_population':  'P0090002'
    }  # Total, White, Black, Asian and Hispanic

    file = open(LOCATION_CSV)
    places = csv.reader(file)

    for row in places:
        error_status = False
        if row_index > 0:
            state_name = row[0].strip()
            state_fips = row[1].strip()
            city_fips = row[2].strip()
            city_name = row[3].strip()

            if city_name == _city and state_name == _state:
                city_fips_to_search = city_fips
                state_fips_to_search = state_fips

                search_string = 'in=state:{0}&for=place:{1}'.format(state_fips_to_search, city_fips_to_search)

                for re, value in reports.items():  # Get the population for each race
                    city = census.get(['{}'.format(value)], ['{}'.format(search_string)])

                    if len(city) > 0:
                        _result = ast.literal_eval(city.decode('utf8'))[1]

                        results[re] = (_result[0], state_fips_to_search, city_fips_to_search)

                    else:
                        error_status = True
                        results[re] = None  # Couldn't get population

        row_index += 1

    if error_status == False:
        print(" -> Success\n")
    else:
        print(" -> Failure\n")

    return results


def get_populations():
    """
    Gets population per race, per city
    :return: A dict of dicts containing populatin per race, per city
    """

    population_results = {}
    location_index = 0
    c = Census(API_KEY)
    shooting_data = CSV(SHOOTINGS_CSV)
    locations = shooting_data.build_city_state_list()

    i = 0

    for location in locations:
        if location_index > 0:
                print("Parsing {0}, {1}".format(location[0], location[1]))
                location_name = '{0},{1}'.format(location[0], location[1])
                results = get_total_population(location, c)

                population_results[location_name] = results

        location_index += 1

    return population_results


def main():
    """
    Run the thing
    :return: None
    """

    results = get_populations()

    test = CSV(SHOOTINGS_CSV)
    test.write_new_columns(results)

if __name__ == '__main__':
    main()
