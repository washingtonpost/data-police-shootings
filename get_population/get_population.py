"""
Gets population of us cities in police shootings file
"""

import urllib.request
import csv
import ast


API_KEY = '728083e8ebb522935279c284a900a4cd9d491f12'
LOCATION_CSV = './places.csv'


class Census:
    def __init__(self, key):
        self.key = key

    def get(self, fields, geo, year=2010, dataset='sf1'):
        fields = [','.join(fields)]
        base_url = 'http://api.census.gov/data/%s/%s?key=%s&get=' % (str(year), dataset, self.key)
        query = fields
        for item in geo:
            query.append(item)
        add_url = '&'.join(query)
        url = base_url + add_url
        print(url)
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)

        return response.read()


class CSV:
    """
    Read and write to and from the CSV file
    """
    def __init__(self, csv):
        file = open(csv)
        self.csv_file = csv.reader(file)

    def build_cityState_list(self):
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


def count_pop_county(county_result):
    count = 0
    for item in county_result[1:]:
        count += int(item[0])
    return count


def count_pop_city(city_result):
    count = 0
    for item in city_result[1:]:
        count += int(item[0])
    return count


def get_population_value(location, census):
    """
    Returns the population for a given city and state
    :param location: Tuple denoting (city, state)
    :param census: Census object
    :return: Int -> population of city, state
    """
    row_index = 0  # for skipping the places.csv header
    city_fips_to_search = None
    state_fips_to_search = None
    _city = location[0]
    _state = location[1]

    # Get city FIPS code from places.csv

    file = open(LOCATION_CSV)
    places = csv.reader(file)

    for row in places:
        if row_index > 0:
            state_name = row[0]
            state_fips = row[1]
            city_fips = row[2]
            city_name = row[3]
            county_name = row[4]

            if city_name == _city:
                city_fips_to_search = city_fips
                state_fips_to_search = state_fips

        row_index += 1

    city = c.get(['P0010001'], 'in=state:{}'.format(state_fips_to_search), 'for=place:{}'.format(city_fips_to_search))

    return city


def main():
    """
    Run the thing
    :return: None
    """

    c = Census(API_KEY)
    state = c.get(['P0010001'], ['for=state:25'])
    # url: http://api.census.gov/data/2010/sf1?key=<mykey>&get=P0010001&for=state:25
    county = c.get(['P0010001'], ['in=state:25', 'for=county:*'])
    # url: http://api.census.gov/data/2010/sf1?key=<mykey>&get=P0010001&in=state:25&for=county:*
    city = c.get(['P0010001'], ['in=state:25', 'for=place:*'])
    # url: http://api.census.gov/data/2010/sf1?key=<mykey>&get=P0010001&in=state:25&for=place:*

    # Cast result to list type
    #state_result = ast.literal_eval(state.decode('utf8'))
    #county_result = ast.literal_eval(county.decode('utf8'))
    city_result = ast.literal_eval(city.decode('utf8'))

    print(city_result[0])
    for i in city_result:
        if i[2] == '76450':
            input("Graham: {}".format(i))

if __name__ == '__main__':
    main()
