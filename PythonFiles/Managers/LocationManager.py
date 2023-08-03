import requests
import pycountry

class LocationManager:
    _default_country = "Singapore"

    def getCurrentCountry(self):
        """
        Try and get the country of current computer is in by going online. Requires internet to do so. 
        
        return: Country the user is in and None if fails.
        """

        try:
            # Go online and try to get current location
            response = requests.get('http://ip-api.com/json').json()
            return str(response['country'])
        except Exception as e:
            print(f'[{str(self.__class__.__name__).upper()}](getCurrentCountry()): {e}')
            return None
    
    def getCountryCode(self, country_name: str):
        """
        Attempt to get the country code given the name of a country
        
        return: Country code of country
        """

        try:
            mapping = {country.name: country.alpha_2 for country in pycountry.countries}
            return str(mapping.get(country_name))
        except Exception as e:
            print(f'[{str(self.__class__.__name__).upper()}](getCountryCode()): {e}')
            return None

# For testing
def main():
    location_manager = LocationManager()

    # print(location_manager.getCurrentCountry())

    test_country_name = "Singapore"
    print(location_manager.getCountryCode(country_name=test_country_name))

if __name__ == "__main__":
    main()