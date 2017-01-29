import requests
import pandas as pd


ACS_ENDPOINT = 'https://api.census.gov/data/{year}/{frequency}'
VARIABLES = {'NAME': 'geography_name',
             'B01001_001E': 'total_population',
             'B19013_001E': 'median_household_income',
             'B11011_001E': 'total_households',
             'B25001_001E': 'housing_units',
             'B25075_001E': 'owner_occupied_housing_units',
             'B25003_003E': 'renter_occupied_housing_units',
             'B25002_003E': 'vacant_housing_units'}


class ACSError(Exception):
    def __init__(self, error, url, variables):
        self.error = error
        self.url = url
        self.variables = variables

    def __str__(self):
        return self.error


class CensusACS(object):
    def __init__(self, year, frequency='acs5', variables=VARIABLES.keys()):
        self.year = year
        self.frequency = frequency
        if isinstance(variables, str):
            variables = [variables]
        self.variables = list(variables)

    @property
    def acs_endpoint(self):
        return ACS_ENDPOINT.format(year=self.year, frequency=self.frequency)

    def get_data(self, state, geography_type, geography="*"):
        if not isinstance(geography, str):
            geography = ','.join(geography)
        variables = ','.join(self.variables)
        state = 'state:{}'.format(state)
        geographies = "{}:{}".format(geography_type, geography)
        params = {'get': variables, 'for': geographies, 'in': state}
        params_str = "&".join("{}={}".format(k, v) for k, v in params.items())
        response = requests.get(self.acs_endpoint, params_str)
        if not response.ok:
            raise ACSError(response.text, response.url, self.variables)
        response = response.json()
        columns = response.pop(0)
        df = pd.DataFrame(response, columns=columns)
        df.rename(columns=VARIABLES, inplace=True)
        df.owner_occupied_housing_units = pd.to_numeric(df.owner_occupied_housing_units)
        df.renter_occupied_housing_units = pd.to_numeric(df.renter_occupied_housing_units)
        df.housing_units = pd.to_numeric(df.housing_units)
        df['owner_occupied_percent'] = (
            100 * df['owner_occupied_housing_units'] / df['housing_units'])
        df.owner_occupied_percent = df.owner_occupied_percent.round(0)
        df['renter_occupied_percent'] = (
            100 * df['renter_occupied_housing_units'] / df['housing_units'])
        df.renter_occupied_percent = df.renter_occupied_percent.round()
        return df.to_dict(orient='records')

    def get_zcta(self, state, zcta="*"):
        geography_type = 'zip+code+tabulation+area'
        return self.get_data(state, geography_type, zcta)

    def get_congressional_districts(self, state, district="*"):
        geography_type = 'congressional+district'
        return self.get_data(state, geography_type, district)

    def get_counties(self, state, county="*"):
        return self.get_data(state, 'county', county)

    def get_census_tracts(self, state, tract="*"):
        tracts = self.get_data(state, 'tract', "*")
        if tract != "*":
            tracts = [t for t in tracts if t['tract'] == tract][0]
        return tracts

    def get_state_legislative_districts_upper(self, state, district="*"):
        geography_type = 'state+legislative+district+(upper+chamber)'
        return self.get_data(state, geography_type, district)

    def get_state_legislative_districts_lower(self, state, district="*"):
        geography_type = 'state+legislative+district+(lower+chamber)'
        return self.get_data(state, geography_type, district)


if __name__ == "__main__":
    c = CensusACS('2015')
    print(c.get_census_tracts("09", "904100"))
